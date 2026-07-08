# -*- coding: utf-8 -*-
"""
Оптимізатор української розкладки для спліт-клавіатур (метод імітації відпалу).

Використання:
    python main.py                         # корпус з папки corpus_texts
    python main.py --iterations 500000 --restarts 3 --seed 42

Що виправлено порівняно з першою версією:
  * Внутрішня колонка = ТОЙ САМИЙ вказівний палець (раніше вона вважалась
    окремим "пальцем", і реальні SFB вказівного не штрафувались).
  * Пробіли та розділові знаки розривають біграми: між словами реальний
    набір іде через Space, тож міжслівні пари літер не оптимізуються.
  * Інкрементальний перерахунок score (тільки дельта від обміну двох літер)
    — сотні тисяч ітерацій за хвилини замість діб.
  * Температура відпалу калібрується автоматично від масштабу score.
  * Результат зберігається у файл, є seed для відтворюваності.
"""
import argparse
import math
import os
import random
import re
import sys
from collections import Counter

ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"  # 33 літери
N = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}

# ==========================================
# 1. БІОМЕХАНІЧНА КОНФІГУРАЦІЯ (33 слоти)
# ==========================================
# Пальці: 0=Л.мізинець 1=Л.безіменний 2=Л.середній 3=Л.вказівний
#         4=П.вказівний 5=П.середній 6=П.безіменний 7=П.мізинець
# Внутрішні колонки (розтяжка) належать вказівним пальцям 3 і 4!
# Фізіологічна вартість: 1 (ідеально) ... 10 (боляче)

SLOTS = [
    # --- ЛІВА РУКА: 5 колонок (мізинець -> внутрішня) ---
    (0, 8), (1, 4), (2, 2), (3, 3), (3, 7),   # верхній ряд
    (0, 5), (1, 3), (2, 1), (3, 1), (3, 6),   # домашній ряд
    (0, 10), (1, 6), (2, 5), (3, 4), (3, 8),  # нижній ряд
    # --- ПРАВА РУКА: 6 колонок (внутрішня -> зовнішній мізинець) ---
    (4, 7), (4, 3), (5, 2), (6, 4), (7, 8), (7, 10),  # верхній ряд
    (4, 6), (4, 1), (5, 1), (6, 3), (7, 5), (7, 8),   # домашній ряд
    (4, 8), (4, 4), (5, 5), (6, 6), (7, 10), (7, 10), # нижній ряд
]
assert len(SLOTS) == N

# Ваги алгоритму
SFB_PENALTY = 100.0      # штраф за біграму одним пальцем
EFFORT_WEIGHT = 2.0      # вага фізіологічної вартості клавіші
ALTERNATION_BONUS = 3.0  # бонус за чергування рук
INWARD_ROLL_BONUS = 5.0  # перекат до вказівного (зручно)
OUTWARD_ROLL_BONUS = 1.0 # перекат до мізинця (терпимо)


def hand(finger):
    return 0 if finger <= 3 else 1


def pair_cost(slot_a, slot_b):
    """Вартість переходу між двома слотами (за одну біграму)."""
    fa, fb = SLOTS[slot_a][0], SLOTS[slot_b][0]
    if hand(fa) != hand(fb):
        return -ALTERNATION_BONUS
    if fa == fb:
        return SFB_PENALTY
    # перекати: inward = у напрямку вказівного пальця
    inward = fb > fa if hand(fa) == 0 else fb < fa
    return -INWARD_ROLL_BONUS if inward else -OUTWARD_ROLL_BONUS


# Матриця вартостей слот-слот (рахується один раз)
PAIR = [[pair_cost(a, b) for b in range(N)] for a in range(N)]
EFFORT = [s[1] * EFFORT_WEIGHT for s in SLOTS]


# ==========================================
# 2. АНАЛІЗАТОР КОРПУСУ
# ==========================================
def load_corpus(directory):
    """Частоти літер і ВНУТРІШНЬОСЛІВНИХ біграм (пробіл/апостроф розривають)."""
    word_re = re.compile(f"[{ALPHABET}]+")
    char_counts = Counter()
    bigram_counts = Counter()
    total_chars = 0

    if not (os.path.exists(directory) and os.path.isdir(directory)):
        os.makedirs(directory)
        print(f"Створено папку '{directory}'. Покладіть туди .txt тексти і запустіть знову.")
        sys.exit(1)

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(directory, filename)
        print(f"  - Зчитування: {filename}")
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                for word in word_re.findall(line.lower()):
                    char_counts.update(word)
                    total_chars += len(word)
                    bigram_counts.update(zip(word, word[1:]))

    if total_chars < 10_000:
        print(f"[!] У '{directory}' замало тексту ({total_chars} літер). "
              f"Для осмисленого результату потрібно хоча б ~100 000 літер "
              f"(книга, експорт чатів тощо). Оптимізація на випадкових частотах "
              f"дає випадкову розкладку, тому зупиняюсь.")
        sys.exit(1)

    print(f"\nОброблено {total_chars:,} літер, {sum(bigram_counts.values()):,} біграм.")
    return char_counts, bigram_counts


# ==========================================
# 3. СКОРИНГ (повний + інкрементальний)
# ==========================================
def build_tables(char_counts, bigram_counts):
    """Частоти у щільні масиви (нормовані на 1000 літер корпусу)."""
    total = sum(char_counts.values()) or 1
    U = [0.0] * N
    for c, n in char_counts.items():
        U[IDX[c]] = 1000.0 * n / total
    B = [[0.0] * N for _ in range(N)]
    for (a, b), n in bigram_counts.items():
        if a != b:  # повтор літери — не рух пальця між клавішами
            B[IDX[a]][IDX[b]] = 1000.0 * n / total
    return U, B


def full_score(pos, U, B):
    """pos[l] = слот літери l. Повний перерахунок (для контролю)."""
    score = sum(U[l] * EFFORT[pos[l]] for l in range(N))
    for a in range(N):
        Ba, pa = B[a], pos[a]
        for b in range(N):
            if Ba[b]:
                score += Ba[b] * PAIR[pa][pos[b]]
    return score


def swap_delta(pos, U, B, x, y):
    """Зміна score від обміну літер x та y місцями. O(N) замість O(N^2)."""
    px, py = pos[x], pos[y]
    d = U[x] * (EFFORT[py] - EFFORT[px]) + U[y] * (EFFORT[px] - EFFORT[py])
    Px, Py = PAIR[px], PAIR[py]
    Bx, By = B[x], B[y]
    for z in range(N):
        if z == x or z == y:
            continue
        pz = pos[z]
        bxz, bzx = Bx[z], B[z][x]
        if bxz or bzx:
            d += bxz * (Py[pz] - Px[pz]) + bzx * (PAIR[pz][py] - PAIR[pz][px])
        byz, bzy = By[z], B[z][y]
        if byz or bzy:
            d += byz * (Px[pz] - Py[pz]) + bzy * (PAIR[pz][px] - PAIR[pz][py])
    d += Bx[y] * (Py[px] - Px[py]) + By[x] * (Px[py] - Py[px])
    return d


# ==========================================
# 4. ІМІТАЦІЯ ВІДПАЛУ
# ==========================================
def optimize(U, B, iterations, rng):
    pos = list(range(N))
    rng.shuffle(pos)
    score = full_score(pos, U, B)
    best_pos, best_score = pos[:], score

    # Автокалібрування температури від типового масштабу дельт
    sample = []
    for _ in range(300):
        x, y = rng.sample(range(N), 2)
        sample.append(abs(swap_delta(pos, U, B, x, y)))
    sample.sort()
    t0 = max(sample[len(sample) // 2] * 2.0, 1e-6)  # 2×медіана
    t_final = t0 / 10_000.0
    cooling = (t_final / t0) ** (1.0 / iterations)
    temp = t0

    report = max(iterations // 10, 1)
    for i in range(iterations):
        x, y = rng.sample(range(N), 2)
        d = swap_delta(pos, U, B, x, y)
        if d < 0 or rng.random() < math.exp(-d / temp):
            pos[x], pos[y] = pos[y], pos[x]
            score += d
            if score < best_score:
                best_score, best_pos = score, pos[:]
        temp *= cooling
        if (i + 1) % report == 0:
            print(f"  {i + 1:,}/{iterations:,} | поточний {score:,.1f} | найкращий {best_score:,.1f}")

    return best_pos, best_score


# ==========================================
# 5. МЕТРИКИ ТА ВІЗУАЛІЗАЦІЯ
# ==========================================
def quick_metrics(pos, B):
    total = sfb = alt = 0.0
    for a in range(N):
        for b in range(N):
            n = B[a][b]
            if not n:
                continue
            total += n
            fa, fb = SLOTS[pos[a]][0], SLOTS[pos[b]][0]
            if hand(fa) != hand(fb):
                alt += n
            elif fa == fb:
                sfb += n
    return 100 * sfb / total, 100 * alt / total


def layout_rows(pos):
    slot_to_letter = {pos[l]: ALPHABET[l] for l in range(N)}
    rows = []
    for r in range(3):
        left = [slot_to_letter[r * 5 + c] for c in range(5)]
        right = [slot_to_letter[15 + r * 6 + c] for c in range(6)]
        rows.append((left, right))
    return rows


def format_layout(pos):
    lines = ["=" * 52, " ОПТИМІЗОВАНА РОЗКЛАДКА (33 літери)", "=" * 52, ""]
    for left, right in layout_rows(pos):
        lines.append("  " + " ".join(f"{c:^3}" for c in left) +
                     "      " + " ".join(f"{c:^3}" for c in right))
    return "\n".join(lines)


# ==========================================
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Оптимізатор української розкладки")
    ap.add_argument("--corpus", default="corpus_texts", help="папка з .txt текстами")
    ap.add_argument("--iterations", type=int, default=300_000, help="ітерацій на рестарт")
    ap.add_argument("--restarts", type=int, default=3, help="кількість незалежних запусків")
    ap.add_argument("--seed", type=int, default=None, help="seed для відтворюваності")
    ap.add_argument("--out", default="layout_result.txt", help="файл результату")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    char_counts, bigram_counts = load_corpus(args.corpus)
    U, B = build_tables(char_counts, bigram_counts)

    best_pos, best_score = None, float("inf")
    for r in range(args.restarts):
        print(f"\nРестарт {r + 1}/{args.restarts} ({args.iterations:,} ітерацій)...")
        pos, score = optimize(U, B, args.iterations, rng)
        if score < best_score:
            best_pos, best_score = pos, score

    text = format_layout(best_pos)
    sfb, alt = quick_metrics(best_pos, B)
    summary = (f"\nScore: {best_score:,.1f} | SFB: {sfb:.2f}% | Чергування рук: {alt:.1f}%\n"
               f"(порівняйте з іншими розкладками: python analyzer.py <корпус.txt>)")
    print("\n" + text + summary)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text + summary + "\n")
    print(f"\nЗбережено у {args.out}")
