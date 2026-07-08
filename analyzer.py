# -*- coding: utf-8 -*-
"""
Аналізатор клавіатурних розкладок для української мови.

Рахує стандартні метрики спільноти ергономічних розкладок:
  - SFB%        — біграми одним пальцем (Same Finger Bigrams), менше = краще
  - Alternation — чергування рук, більше = краще
  - Rolls       — перекати на одній руці (inward/outward)
  - Баланс рук, навантаження на пальці, використання домашнього ряду
  - Топ найгірших SFB-біграм для кожної розкладки

Використання:
    python analyzer.py шлях/до/корпусу.txt [ще_файли.txt ...]

Пробіл та апостроф розривають біграми: між словами реальний набір іде
через клавішу Space, тож міжслівні пари літер не є ані SFB, ані перекатом.
"""
import sys
import re
from collections import Counter

LETTERS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

# ---------------------------------------------------------------
# Опис розкладок: літера -> (рука, палець, ряд)
# рука: 'L'/'R'; палець: 0=мізинець, 1=безіменний, 2=середній, 3=вказівний
# (внутрішня колонка — це ТОЙ САМИЙ вказівний палець, а не окремий);
# ряд: 0=верхній, 1=домашній, 2=нижній
# ---------------------------------------------------------------

def grid(rows_left, rows_right, fingers_left, fingers_right):
    """Будує мапу з текстових рядків розкладки. '-' = порожньо."""
    m = {}
    for r, row in enumerate(rows_left):
        for c, ch in enumerate(row.split()):
            if ch != "-":
                m[ch] = ("L", fingers_left[c], r)
    for r, row in enumerate(rows_right):
        for c, ch in enumerate(row.split()):
            if ch != "-":
                m[ch] = ("R", fingers_right[c], r)
    return m

LAYOUTS = {}

# ЙЦУКЕН (стандартна українська, класична постановка пальців)
LAYOUTS["ЙЦУКЕН"] = grid(
    ["й ц у к е", "ф і в а п", "я ч с м и"],
    ["н г ш щ з х ї", "р о л д ж є -", "т ь б ю - - -"],
    [0, 1, 2, 3, 3],
    [3, 3, 2, 1, 0, 0, 0],
)
LAYOUTS["ЙЦУКЕН"]["ґ"] = LAYOUTS["ЙЦУКЕН"]["г"]  # AltGr+г

# Ева 3.8 (README, 6 колонок на половину)
LAYOUTS["Ева 3.8"] = grid(
    ["- я й п к д", "є и в т с р", "- ж ц з б м"],
    ["г л у і щ ї", "х н о а е ю", "ш ч - - ь ф"],
    [0, 0, 1, 2, 3, 3],
    [3, 3, 2, 1, 0, 0],
)
LAYOUTS["Ева 3.8"]["ґ"] = LAYOUTS["Ева 3.8"]["г"]  # tap-hold Г→Ґ

# Ліна (10 000 000 ітерацій, README)
LAYOUTS["Ліна 10М"] = grid(
    ["е я ґ з ю", "і а о т ї", "ь и у ж ш"],
    ["є г м с ф ц", "й к н р в д", "х п л ч б щ"],
    [0, 1, 2, 3, 3],
    [3, 3, 2, 1, 0, 0],
)

# Canary Phonetic UA (5 колонок + ь на зовнішній правій)
LAYOUTS["Canary Phonetic UA"] = grid(
    ["ш л и п к", "ц р с т б", "я й в д г"],
    ["з ф о у ь", "м н е і а", "х ж ч ю щ"],
    [0, 1, 2, 3, 3],
    [3, 3, 2, 1, 0, 0],
)
for extra, base in (("є", "е"), ("ї", "і"), ("ґ", "г")):  # tap-hold
    LAYOUTS["Canary Phonetic UA"][extra] = LAYOUTS["Canary Phonetic UA"][base]


# ---------------------------------------------------------------
# Корпус: частоти літер та внутрішньослівних біграм
# ---------------------------------------------------------------

def load_corpus(paths):
    word_re = re.compile(f"[{LETTERS}]+")
    chars = Counter()
    bigrams = Counter()
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                # апостроф і будь-який не-літерний символ розривають слово
                for word in word_re.findall(line.lower()):
                    chars.update(word)
                    bigrams.update(zip(word, word[1:]))
    return chars, bigrams


# ---------------------------------------------------------------
# Метрики
# ---------------------------------------------------------------

def analyze(layout, chars, bigrams):
    total_chars = sum(chars[c] for c in chars if c in layout)
    total_bi = 0
    sfb = 0
    alt = 0
    roll_in = 0
    roll_out = 0
    sfb_top = Counter()
    for (a, b), n in bigrams.items():
        if a not in layout or b not in layout:
            continue
        total_bi += n
        ha, fa, _ = layout[a]
        hb, fb, _ = layout[b]
        if ha != hb:
            alt += n
        elif fa == fb:
            if a != b:  # повтор тієї самої літери не рахуємо як SFB
                sfb += n
                sfb_top[a + b] += n
        elif fb > fa:  # до вказівного = inward
            roll_in += n
        else:
            roll_out += n

    hand_l = sum(n for c, n in chars.items() if c in layout and layout[c][0] == "L")
    fingers = Counter()
    home = 0
    for c, n in chars.items():
        if c not in layout:
            continue
        hand, fin, row = layout[c]
        fingers[(hand, fin)] += n
        if row == 1:
            home += n

    pct = lambda x, t: 100.0 * x / t if t else 0.0
    return {
        "sfb": pct(sfb, total_bi),
        "alt": pct(alt, total_bi),
        "roll_in": pct(roll_in, total_bi),
        "roll_out": pct(roll_out, total_bi),
        "hand_l": pct(hand_l, total_chars),
        "home": pct(home, total_chars),
        "pinky": pct(fingers[("L", 0)] + fingers[("R", 0)], total_chars),
        "fingers": {k: pct(v, total_chars) for k, v in fingers.items()},
        "sfb_top": sfb_top.most_common(10),
        "sfb_top_pct": [(bg, pct(n, total_bi)) for bg, n in sfb_top.most_common(10)],
    }


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        sys.exit(1)
    chars, bigrams = load_corpus(paths)
    total = sum(chars.values())
    print(f"Корпус: {total:,} літер, {sum(bigrams.values()):,} біграм\n")

    results = {name: analyze(lay, chars, bigrams) for name, lay in LAYOUTS.items()}

    header = f"{'Розкладка':<20} {'SFB%':>6} {'Черг.%':>7} {'Rolls in%':>9} {'Rolls out%':>10} {'Дім.ряд%':>9} {'Мізинці%':>9} {'Ліва%':>6}"
    print(header)
    print("-" * len(header))
    for name, r in results.items():
        print(f"{name:<20} {r['sfb']:>6.2f} {r['alt']:>7.1f} {r['roll_in']:>9.1f} "
              f"{r['roll_out']:>10.1f} {r['home']:>9.1f} {r['pinky']:>9.1f} {r['hand_l']:>6.1f}")

    print()
    for name, r in results.items():
        top = ", ".join(f"{bg} {p:.3f}%" for bg, p in r["sfb_top_pct"][:8])
        print(f"Топ SFB [{name}]: {top}")


if __name__ == "__main__":
    main()
