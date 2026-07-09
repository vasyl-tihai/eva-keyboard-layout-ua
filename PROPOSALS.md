# Layout Improvement Proposals (data, not taste)

🇺🇦 [Українська версія](ПРОПОЗИЦІЇ.md)

This document is the result of a quantitative audit of the repository's layouts.
All numbers were computed with [analyzer.py](analyzer.py) on a **mixed corpus of
6.2 million letters** across three genres:

| Genre | Source | Size |
|---|---|---|
| Balanced written (press, fiction, science) | [Brown-UK](https://github.com/brown-uk/corpus) | ~3.0 M letters |
| Conversational (dialogue) | [OpenSubtitles UA](https://opus.nlpl.eu/OpenSubtitles.php) | ~3.0 M letters |
| Encyclopedic | random [Wikipedia](https://uk.wikipedia.org/) articles | ~0.25 M letters |

The finger model is honest: the inner column is pressed by **the same index finger**,
and bigrams are counted **only inside words** (between words there is a thumb-key Space).

> ⚠️ Before relearning anything, recompute the metrics on your own texts:
> `python analyzer.py my_corpus.txt`. Every conclusion below was checked on the three
> genres separately; wherever genre affects the result, it is noted.

## Diagnosis of Eva 3.8 (mixed corpus)

| Metric | Value | Comment |
|---|---|---|
| SFB | **2.92 %** | 6× better than ЙЦУКЕН (18.3 %), but there is headroom |
| Hand alternation | 57.1 % | good |
| Home row | **58.3 %** | the best of all layouts in the table |
| Pinkies | **19.9 %** | heavy: И (6.2 %) on the left pinky + Е (5.6 %) on the right |

Top SFB bigrams: **кр** 0.27 %, **ск** 0.21 %, **чн** 0.20 %, **жи** 0.16 %, **бр** 0.16 %, **др** 0.12 %.

Nearly all of them cluster around the **left index finger** (it owns К, С, Б, Д, Р, М),
plus the **чн** pair on the right index.

**The key observation:** in every one of these pairs at least one letter sits OUTSIDE
the home row (к, ч, д, б are on the top/bottom rows). The conflicts can therefore be
untangled without touching the home row at all — the "core letters on the home row"
philosophy stays intact.

## 🥇 Proposal "Eva 3.9" — three swaps outside the home row (recommended)

> ✅ **Accepted.** Eva 3.9 has been added to the repository ([Eva-3.9.vil](Eva-3.9.vil))
> and became the recommended version in the README.

Swap **М ↔ Ч**, **К ↔ Ц**, **Д ↔ З** (all six letters are on the top/bottom rows;
the home row, the pinkies and the vowel block are untouched):

```
[   ] [ Я ] [ Й ] [ П ] [ Ц ] [ З ]        [ Г ] [ Л ] [ У ] [ І ] [ Щ ] [ Ї ]
[ Є ] [ И ] [ В ] [ Т ] [ С ] [ Р ]        [ Х ] [ Н ] [ О ] [ А ] [ Е ] [ Ю ]
[   ] [ Ж ] [ К ] [ Д ] [ Б ] [ Ч ]        [ Ш ] [ М ] [ , ] [ . ] [ Ь ] [ Ф ]
```

| Metric | Eva 3.8 | Eva 3.9 |
|---|---|---|
| SFB (mixed corpus) | 2.92 % | **1.96 %** (−33 %) |
| Home row | 58.3 % | **58.3 %** (unchanged) |
| Pinkies | 19.9 % | 19.9 % (unchanged) |
| Inward rolls | 17.0 % | **17.8 %** |
| Hand alternation | 57.1 % | 55.4 % |

Genre robustness (SFB, Eva 3.8 → Eva 3.9):

| Genre | 3.8 | 3.9 | Gain |
|---|---|---|---|
| Written (Brown-UK) | 2.95 % | 1.86 % | −37 % |
| Conversational (subtitles) | 3.04 % | 2.22 % | −27 % |
| Wikipedia | 3.29 % | 1.89 % | −42 % |

Why it works:

- **М ↔ Ч**: Ч escapes the right index finger away from Н — «чн» becomes hand alternation.
- **К ↔ Ц**: К leaves the index-finger column — «кр» and «ск»/«кс» disappear.
- **Д ↔ З**: Д moves away from Р — «др»/«рд» disappear.

A relearning bonus: the home row — the deepest muscle memory — does not change at all.
If you want the absolute minimum step, the single swap **М ↔ Ч** alone gives 2.92 % → 2.67 %.

What remains:

- **«мн»** (0.10 % overall, but 0.21 % in conversational text — the word «мені»):
  after the swap М neighbours Н on the right index. If you mostly type chats, an extra
  **Б ↔ М** swap removes «мн» (conversational SFB 2.22 % → 2.14 %), but it slightly
  hurts the written genres — live with 3.9 first and see whether «мн» bothers you at all.
- **«рс»** (0.07 %): Р and С sit next to each other on the index home row. The only way
  to remove it is to evict one of them from the home row — under the "home row above
  all" principle, not worth it.

## Proposal "Eva 3.9+" — five swaps, minimal SFB (experimental)

Swaps **Й↔Р**, **М↔Ч**, **Г↔Й**, **А↔У**, **Е↔У**:

```
[   ] [ Я ] [ Р ] [ П ] [ К ] [ Д ]        [ Й ] [ Л ] [ А ] [ І ] [ Щ ] [ Ї ]
[ Є ] [ И ] [ В ] [ Т ] [ С ] [ Г ]        [ Х ] [ Н ] [ О ] [ Е ] [ У ] [ Ю ]
[   ] [ Ж ] [ Ц ] [ З ] [ Б ] [ Ч ]        [ Ш ] [ М ] [ , ] [ . ] [ Ь ] [ Ф ]
```

On the mixed corpus: SFB 1.87 %, pinkies 17.7 %, but the home row drops to 50.5 %.
Its SFB advantage over Eva 3.9 is a mere 0.09 pp, while the cost is 8 pp of home row
and 9 relocated letters instead of 6. **On the large corpus this variant lost its
purpose — Eva 3.9 is better on almost every axis.** Kept for the record.

## Comparison table (mixed corpus, 6.2 M letters)

| Layout | SFB % | Alternation % | Home row % | Pinkies % |
|---|---|---|---|---|
| ЙЦУКЕН | 18.30 | 54.2 | 43.9 | 9.4 |
| Eva 3.8 | 2.92 | 57.1 | 58.3 | 19.9 |
| **Eva 3.9** (recommended) | **1.96** | 55.4 | **58.3** | 19.9 |
| Eva 3.9+ (experimental) | 1.87 | 57.2 | 50.5 | 17.7 |
| Lina 10M (old) | 0.97 | 74.9 | 53.8 | 24.5 |
| **Lina 2.0** | **0.53** | 64.3 | 50.6 | ~12 |
| Canary Phonetic UA | 5.15 | 56.7 | 47.1 | 14.8 |

## Proposal "Lina 2.0" — regenerate with the honest model

The old Lina was optimized by code with two model bugs (a separate "finger" for the
inner column + cross-word bigrams), which is why it pays for its beautiful hand
alternation with a **24.5 % pinky load**.

The fixed `main.py` (500 000 iterations × 4 restarts, seed 42, mixed corpus) produces:

```
[ Ю ] [ З ] [ Л ] [ Д ] [ Ц ]        [ Ь ] [ Е ] [ А ] [ Р ] [ Г ] [ Ф ]
[ К ] [ С ] [ Н ] [ Т ] [ Б ]        [ У ] [ И ] [ О ] [ В ] [ П ] [ Х ]
[ Ї ] [ Ч ] [ Є ] [ М ] [ Щ ]        [ Ґ ] [ І ] [ Я ] [ Й ] [ Ш ] [ Ж ]
```

- **SFB 0.53 %**, pinkies ~12 % (instead of 24.5 %), inward rolls 15.8 %.
- The main win is **genre robustness**. A version generated on Wikipedia alone degraded
  to 1.66 % SFB on conversational text; this one holds 0.47–0.80 % across all three genres:

| Genre | Lina 2.0 (mixed) | Lina trained on Wikipedia only |
|---|---|---|
| Written | 0.47 % | 0.51 % |
| Conversational | **0.80 %** | **1.66 %** |
| Wikipedia | 0.51 % | 0.48 % |

The moral: **optimize on what you actually type**, and always mix genres — a
homogeneous corpus yields a layout that breaks on any other style of text.

## Canary Phonetic UA — the honest price of phonetics

SFB 5.15 % is the highest among the custom layouts, and almost all of it sits in the
left middle-finger column **И-С-В**: the bigrams «ви», «ис», «ив», «си», «вс» add up to
~2 % SFB. This is a direct consequence of the phonetic principle (И on Y, С on S, В
on V) — it cannot be fixed without breaking the phonetics. Proposal: keep it as is,
but position it honestly: Canary Phonetic UA trades ~2 pp of SFB for zero relearning,
aimed at people who type mostly English.

## Minor proposals

1. **Document Ґ and the apostrophe.** They are invisible in the Eva diagrams: Ґ lives
   on a tap-hold of Г, the apostrophe on a combo. The apostrophe occurs more often in
   Ukrainian text than Ґ does, so it deserves its own line in the README.
2. **Reconcile Eva.vil with the diagram.** In the file's Vial matrix Ї/Ю/Ф are wired
   into the fourth row, the config has 46 active positions, and PrtScr/Tab/Delete sit
   on layer 0 — the README must state honestly which board the file targets, or a
   "clean" variant for the standard Corne 42 should be built.
3. **Publish Canary Phonetic UA as a file** (.vil or keymap.json), not just a picture.

## How to reproduce

```bash
# metrics of all layouts on your own corpus
python analyzer.py my_corpus.txt

# generate your own Lina (honest model, minutes instead of days)
python main.py --corpus corpus_texts --iterations 500000 --restarts 4 --seed 42
```

Corpora used here: [Brown-UK](https://github.com/brown-uk/corpus) (git clone),
[OpenSubtitles UA mono](https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/mono/uk.txt.gz),
random Wikipedia articles via the [API](https://uk.wikipedia.org/w/api.php).
