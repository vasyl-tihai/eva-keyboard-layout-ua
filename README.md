# 🇺🇦 Eva & Lina — Ergonomic Ukrainian Keyboard Layouts

🇺🇦 [Українська версія](README.uk.md)

Ergonomic layouts for typing Ukrainian on split keyboards
(Corne/crkbd, Kyria, Lily58, Sofle and other column-staggered or ortholinear boards).

If you have tried [Colemak](https://colemak.com/), Colemak-DH, Dvorak, Workman or
[Canary](https://github.com/Apsu/Canary), you know how much finger-motion optimization matters.
This repository brings those practices to the Ukrainian alphabet: ready-to-use layouts,
their evolution history, a Python optimizer that generates a layout for your own texts,
and an analyzer that computes the metrics on any corpus.

## Contents

- [Why ЙЦУКЕН fails on 40 % keyboards](#-why-йцукен-fails-on-40--keyboards)
- [Metrics: numbers instead of promises](#-metrics-numbers-instead-of-promises)
- [Eva — manual optimization](#-the-eva-branch--manual-optimization-recommended)
- [Installation (Vial)](#-installing-evavil-in-vial)
- [Eva evolution history](#-eva-evolution-history)
- [Lina — mathematical optimization](#-the-lina-branch--mathematical-optimization)
- [Canary Phonetic UA](#-canary-phonetic-ua-a-bridge-between-languages)
- [Generate a layout for yourself](#-generate-a-layout-tailored-to-you)
- [Improvement proposals](#-improvement-proposals)
- [Sources](#-sources)

## 🛑 Why ЙЦУКЕН fails on 40 % keyboards

ЙЦУКЕН (the standard Ukrainian layout, a sibling of the Russian ЙЦУКЕН and a
typewriter-era design like QWERTY) was never optimized for typing comfort. On a compact
split keyboard its problems are visible in numbers (6.2 M-letter corpus, [analyzer.py](analyzer.py)):

- **Index-finger overload.** The left index finger owns К, Е, А, П, М, И — 29.7 %
  of all keystrokes; the right one owns Н, Г, Р, О, Т, Ь — another 29.9 %.
  **Two fingers do 59.6 % of all the work.**
- **High SFB rate** (Same Finger Bigram — two consecutive letters typed with one finger).
  In ЙЦУКЕН **18.3 % of all bigrams** are SFBs: «ро», «но», «ор», «го», «то», «ка», «ки»…
  This breaks the rhythm and strains the joints.
- **Hand imbalance:** 54 % of keystrokes land on the left hand, with long one-hand runs.

To fix this we went down two roads: **Eva** (manual, logic-driven optimization)
and **Lina** (mathematical optimization by code).

## 📊 Metrics: numbers instead of promises

Computed with [analyzer.py](analyzer.py) on a mixed corpus of **6.2 million letters**
across three genres: balanced written Ukrainian ([Brown-UK](https://github.com/brown-uk/corpus)),
conversational ([OpenSubtitles](https://opus.nlpl.eu/OpenSubtitles.php) dialogue) and
encyclopedic (Ukrainian Wikipedia). The model is honest: the inner column belongs to
the index finger, and bigrams are counted only inside words (the thumb-key Space
breaks them between words).

| Layout | SFB % ↓ | Hand alternation % ↑ | Home row % ↑ | Pinkies % ↓ |
|---|---|---|---|---|
| ЙЦУКЕН | 18.30 | 54.2 | 43.9 | 9.4 |
| Eva 3.8 | 2.92 | 57.1 | 58.3 | 19.9 |
| **Eva 3.9** | **1.96** | 55.4 | **58.3** | 19.9 |
| Lina | 0.97 | 74.9 | 53.8 | 24.5 |
| Canary Phonetic UA | 5.15 | 56.7 | 47.1 | 14.8 |

**Eva 3.9 has 9× fewer SFBs than ЙЦУКЕН** while keeping 58 % of typing on the home row.
The price is heavier pinkies (И and Е live on them). Lina wins on SFB and alternation
but loads the pinkies even more — see the [improvement proposals](PROPOSALS.md).

## 👑 The Eva branch — manual optimization (recommended)

Eva was designed by a human for humans: Ukrainian letter-frequency analysis, hand
alternation (consonants mostly on the left, the core vowels О-А-Е-У-І under the right
hand) and comfortable rolls.

### 🏆 Best pick: Eva 3.9

The latest version — the result of a quantitative audit of Eva 3.8 (method and numbers
in [PROPOSALS.md](PROPOSALS.md)). Three swaps outside the home row — **М↔Ч, К↔Ц, Д↔З** —
untangled the most frequent same-finger conflicts («кр», «ск», «чн», «др»):
SFB dropped from 2.92 % to **1.96 %** (−33 %) while the home row (58.3 %), the pinkies
and the Н-О-А-Е vowel block stayed exactly the same. Relearning is minimal: all six
relocated letters sit on the top/bottom rows. Layout file: [Eva-3.9.vil](Eva-3.9.vil)

<p align="center">
  <img src="images/eva-3.9.svg" alt="Eva 3.9 layout — orange outline marks the keys changed relative to 3.8" width="700">
</p>

```text
[   ] [ Я ] [ Й ] [ П ] [ Ц ] [ З ]        [ Г ] [ Л ] [ У ] [ І ] [ Щ ] [ Ї ]
[ Є ] [ И ] [ В ] [ Т ] [ С ] [ Р ]        [ Х ] [ Н ] [ О ] [ А ] [ Е ] [ Ю ]
[   ] [ Ж ] [ К ] [ Д ] [ Б ] [ Ч ]        [ Ш ] [ М ] [ , ] [ . ] [ Ь ] [ Ф ]
```

Used to 3.8? It is not going anywhere: the file is [Eva.vil](Eva.vil), the diagram is in
the [evolution history](#-eva-evolution-history) below.

Letters you do not see on the diagram:

- **Ґ** — tap-hold on the **Г** key;
- **apostrophe** — a combo (simultaneous press) of **И + В**;
- digits and symbols live on a separate layer (Layer 2).

## 🔧 Installing Eva.vil in Vial

1. Flash your keyboard with a [Vial](https://get.vial.today/)-compatible firmware.
2. Open the Vial app → **File → Load saved layout** → pick `Eva-3.9.vil`
   (or `Eva.vil` if you prefer the classic 3.8).
3. Enable the **Ukrainian layout in your OS** — layer 0 sends host scancodes, so the OS
   must interpret them as ЙЦУКЕН (the file does the rest).
4. Language switching uses macros: **M0** = `Ctrl+0` + switch to layer 0 (Ukrainian),
   **M1** = `Ctrl+1` + layer 1 (English Canary). Bind `Ctrl+0`/`Ctrl+1` as language
   hotkeys in your OS, or replace the macros with your own (`Alt+Shift`, `Win+Space`).

Layers in the file: **0** — Eva (Ukrainian), **1** — English Canary, **2** — digits and
symbols, **7** — service layer (layer switching). Combos on layer 0 produce the
apostrophe, brackets, dashes and more.

> Combos in `Eva-3.9.vil` are bound to letters, so they keep working after the swaps,
> but two gestures (з+б and к+п) physically ended up on different keys — remap them in
> Vial to more comfortable pairs if you like.

> ⚠️ `Eva.vil` is my personal config for a board with extra keys (46 active positions:
> PrtScr, Tab, Copy/Paste etc.; Ї/Ю/Ф are wired into the fourth row of the Vial matrix).
> On a standard Corne 42 the layout works, but you will have to place the service keys
> yourself. The diagram above shows the core 3×6+3×6 zone.

## 📜 Eva evolution history

The layout did not get here in one day:

- **Eva 3.0 — bigram analysis.** The first serious attempt to untangle the most frequent
  bigrams («сп», «тр», «нш») for comfortable rolls.

  <img src="images/eva-3.0.png" alt="Eva 3.0 layout" width="600">

  ```text
  [   ] [ Я ] [ Й ] [ П ] [ К ] [ Д ]        [ Г ] [ Ю ] [ У ] [ Л ] [ Щ ] [ Ї ]
  [   ] [ И ] [ В ] [ Т ] [ С ] [ Р ]        [ Х ] [ Н ] [ О ] [ А ] [ Е ] [ І ]
  [   ] [ Ж ] [ Ц ] [ З ] [ Б ] [ М ]        [ Ф ] [ Ч ] [ Ш ] [ . ] [ Ь ] [ Є ]
  ```

- **Eva 3.2 — punctuation and periphery.** First experiments with punctuation and with
  pushing rare letters to the edges; Є moved to the left pinky.

  <img src="images/eva-3.2.png" alt="Eva 3.2 layout" width="600">

- **Eva 3.6 — layer work.** The core matrix stayed as in 3.2; the logic of the extra
  layers and service keys changed.

  <img src="images/eva-3.6.png" alt="Eva 3.6 layout" width="600">

- **Eva 3.7 — almost final.** І, Ю and Л found their places (І in the centre of the top
  row, Ю on the pinky), but the comma and the period still needed work.

  <img src="images/eva-3.7.png" alt="Eva 3.7 layout" width="600">

  ```text
  [   ] [ Я ] [ Й ] [ П ] [ К ] [ Д ]        [ Г ] [ Л ] [ У ] [ І ] [ Щ ] [ Ї ]
  [   ] [ И ] [ В ] [ Т ] [ С ] [ Р ]        [ Х ] [ Н ] [ О ] [ А ] [ Е ] [ Ю ]
  [   ] [ Ж ] [ Ц ] [ З ] [ Б ] [ М ]        [ Ф ] [ Ч ] [ Ш ] [ , ] [ Ь ]
  ```

- **Eva 3.8 — perfect punctuation.** Delete left the core zone, letting the comma and
  the period take comfortable bottom-row spots. It was the recommended version for a
  long time (file: [Eva.vil](Eva.vil)).

  <img src="images/eva-3.8.png" alt="Eva 3.8 layout" width="600">

  ```text
  [   ] [ Я ] [ Й ] [ П ] [ К ] [ Д ]        [ Г ] [ Л ] [ У ] [ І ] [ Щ ] [ Ї ]
  [ Є ] [ И ] [ В ] [ Т ] [ С ] [ Р ]        [ Х ] [ Н ] [ О ] [ А ] [ Е ] [ Ю ]
  [   ] [ Ж ] [ Ц ] [ З ] [ Б ] [ М ]        [ Ш ] [ Ч ] [ , ] [ . ] [ Ь ] [ Ф ]
  ```

- **Eva 3.9 — the quantitative audit** (see above). Analysis on a 6.2 M-letter corpus
  showed that all the most frequent SFBs (кр, ск, чн, др) can be untangled with three
  swaps outside the home row: М↔Ч, К↔Ц, Д↔З. SFB −33 % with zero losses elsewhere.

## 🤖 The Lina branch — mathematical optimization

Once the logical base existed, we asked: what would pure math decide?
[main.py](main.py) is a **simulated annealing** optimizer: hundreds of thousands of
times it swaps letters on a virtual keyboard, "types" your corpus and searches for the
arrangement with minimal effort and minimal SFB.

> Honest note: the algorithm places only the 33 letters. Putting the comma and the
> period on the thumb keys was our manual design decision, not a conclusion of the code.

How the result evolves as iterations grow:

- **10 000 iterations** — the layout is still chaotic:

  <img src="images/lina-10k.png" alt="Lina layout after 10 thousand iterations" width="600">

- **1 000 000 iterations** — vowels cluster, conflicts melt away:

  <img src="images/lina-1m.png" alt="Lina layout after 1 million iterations" width="600">

- **10 000 000 iterations** — the final version:

  <img src="images/lina-10m.png" alt="Lina layout after 10 million iterations" width="600">

  ```text
  [ Е ] [ Я ] [ Ґ ] [ З ] [ Ю ]        [ Є ] [ Г ] [ М ] [ С ] [ Ф ] [ Ц ]
  [ І ] [ А ] [ О ] [ Т ] [ Ї ]        [ Й ] [ К ] [ Н ] [ Р ] [ В ] [ Д ]
  [ Ь ] [ И ] [ У ] [ Ж ] [ Ш ]        [ Х ] [ П ] [ Л ] [ Ч ] [ Б ] [ Щ ]
  ```

Lina's SFB is 0.97 % with 75 % hand alternation. Its weak spot is the 24.5 % pinky
load. The first version of the optimizer had two model bugs (fixed in the current
`main.py`); the regenerated **Lina 2.0** with half the SFB and light pinkies lives in
[PROPOSALS.md](PROPOSALS.md).

## 🦜 Canary Phonetic UA: a bridge between languages

A specialized layout for people who type English 70 %+ of the time (code,
documentation, terminal) but want to switch to Ukrainian comfortably.

The core problem of switching languages is broken muscle memory: your brain knows N
sits under the right index finger, yet the system gives that key Т (as ЙЦУКЕН does).
Canary Phonetic UA solves this with a **phonetic mapping** onto the English
[Canary](https://github.com/Apsu/Canary) layout: same key — same sound.

- **The central block matches:** English N-E-I-A become Ukrainian Н-Е-І-А.
- **Phonetic consonant pairs:** W→Ш, L→Л, R→Р, S→С, T→Т, B→Б, P→П, V→В, D→Д, M→М…
- **Letters with no direct analogue** got logical slots: Я on Q (a phonetic-layout
  tradition), Ж on H, Ь on the apostrophe, Ю and Щ on the comma and period positions.
- **Tap-hold:** Є = hold Е, Ї = hold І, Ґ = hold Г.

<p align="center">
  <img src="images/canary-phonetic-ua.png" alt="Canary Phonetic UA — a phonetic Ukrainian layout based on Canary" width="600">
</p>

The result: your fingers travel the same paths for the same sounds, and switching the
language does not break habits. The honest price: SFB 5.15 % — higher than Eva's
(the phonetic positions of І and С share a finger with В and И — bigrams «ви», «ис»,
«си»). If Ukrainian is your primary language, take Eva; Canary Phonetic UA is for a
mostly-English workday.

> Note: the base is a hybrid of the ANSI and matrix Canary variants, adapted to
> column-staggered geometry.

## 💻 Generate a layout tailored to you

The optimizer adapts to your writing style:

1. Create a `corpus_texts` folder next to `main.py`.
2. Put `.txt` files there: Telegram chat exports, favourite books, work texts —
   the more the better (at least ~100 000 letters).
3. Run:

   ```bash
   python main.py
   # or with parameters:
   python main.py --iterations 500000 --restarts 4 --seed 42
   ```

The script runs on pure Python 3 with no dependencies, prints the layout to the
terminal and saves it to `layout_result.txt` together with its metrics. To compare
against the ready-made layouts:

```bash
python analyzer.py corpus_texts/my_text.txt
```

## 🛠 Firmware recommendations (QMK/ZMK/Vial)

- **Home Row Mods:** put Shift/Ctrl/Alt/Win on hold-taps of the home-row letters —
  your pinkies will never reach for modifiers again.
- **Combos:** simultaneous presses of two neighbouring keys for the apostrophe,
  backspace, brackets (`Eva.vil` ships with a dozen of these).

## 💡 Improvement proposals

The quantitative audit of the layouts with concrete, measured variants lives in
[PROPOSALS.md](PROPOSALS.md): Eva 3.9 (three swaps outside the home row: −33 % SFB
with the home row untouched), Eva 3.9+ (minimal SFB) and Lina 2.0 (regenerated with
the honest model).

## 🤝 Contributing

Ergonomics is a never-ending process. Test Eva 3.9, experiment with Lina, run the
metrics on your own texts — and share the results via an Issue or a Pull Request.
Let's make Ukrainian typing fast and comfortable! 🇺🇦⌨️

## 📚 Sources

- [Canary keyboard layout](https://github.com/Apsu/Canary) — the original English Canary (Apsu and the AKL community).
- [Keyboard layouts doc](https://bit.ly/keyboard-layouts-doc) — the alternative-layout community reference (SFB, rolls, alternation).
- [Vial](https://get.vial.today/) — the firmware configurator.
- Frequency data (6.2 M letters): [Brown-UK](https://github.com/brown-uk/corpus) — a balanced corpus of Ukrainian,
  [OpenSubtitles UA](https://opus.nlpl.eu/OpenSubtitles.php) — conversational register,
  random articles of the [Ukrainian Wikipedia](https://uk.wikipedia.org/); script [analyzer.py](analyzer.py).

## 📄 License

[MIT](LICENSE) — use, modify, share.
