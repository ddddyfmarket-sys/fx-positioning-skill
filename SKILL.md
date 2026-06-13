---
name: fx-positioning
description: >-
  Generate a sell-side-style FX speculative positioning note from live CFTC
  data. Runs the bundled fx_positioning.py (fetches CFTC TFF Futures+Options
  Combined data for EUR, JPY, GBP, CHF, CAD, AUD, NZD, MXN, BRL, ZAR and DXY,
  computes Leveraged-Funds + Asset-Manager net positioning as % of open
  interest with 13W/52W/5Y percentiles and z-scores, WoW/MoM changes, a YTD
  distribution chart and a full-history chart), then writes a macro-PM-grade
  positioning note in the style of the JPM FX Positioning Monitor / Morgan
  Stanley G10 FX positioning reports. Use this skill whenever the user asks
  about FX positioning, CFTC / COT / TFF data, speculative or spec positioning,
  leveraged funds vs asset managers, who is long/short a currency, crowded or
  stretched or saturated FX positions, contrarian FX setups, positioning
  squeezes, the FX positioning monitor, or wants a positioning update / read /
  note on G10 or EM FX — even if they don't name the script or CFTC explicitly.
---

# FX Positioning Monitor

Produce a positioning note for a hedge-fund macro PM: run the data pipeline,
read the outputs (table + two charts), and write the analysis in sell-side
house style. The pipeline and the writing are equally the job — a correct
table with a generic writeup is a failure, and so is good prose on stale data.

## Workflow

### 1. Run the pipeline

The pipeline is a self-contained Python script bundled with this skill at
`scripts/fx_positioning.py`. Run it with **the skill's own directory** as the
script path and **the user's working directory** as the current directory (so
outputs land where the user is working):

```bash
python3 "<skill-dir>/scripts/fx_positioning.py"
```

Replace `<skill-dir>` with the directory this `SKILL.md` lives in — your host
provides this when the skill loads. Typical locations:

- Claude Code: `~/.claude/skills/fx-positioning`
- Cursor: `~/.cursor/skills-cursor/fx-positioning`
- Codex: `$CODEX_HOME/skills/fx-positioning` (usually `~/.codex/skills/...`)
- Other agents: wherever your host installs skills.

- Add `--outdir <path>` to direct outputs elsewhere; default is the current
  directory.
- Add `--refresh` only if the user explicitly wants to bypass the cache. The
  script caches the CFTC API response for 24h, so back-to-back runs are fast
  and won't re-hit the API. The first run of the day fetches fresh data.
- Dependencies (`requests`, `openpyxl`, `matplotlib`, `numpy`) are normally
  present. If a run fails on a missing package, install it and retry once.

The script writes four files to the output directory:

| File | What it is |
|---|---|
| `positioning_table.csv` | The table incl. the Leveraged-Funds vs Asset-Manager split. **Source of truth for all numbers you cite.** |
| `ytd_positioning.png` | YTD distribution box plot: each currency's YTD range of 52W z-scores, with current (×) and 1-week-ago (•) marked. |
| `history_positioning.png` | Full-history small multiples per currency, y-axis = full-history percentile of Total Net % OI (0–100), with 90th/10th range-end bands and the 50th-percentile median. |
| `Positioning_Data.xlsx` | Formatted table + both charts embedded — the deliverable workbook for the PM. |

### 2. Read the outputs

Read all three analytical outputs before writing a word:

1. `positioning_table.csv` — every number you cite comes from here. Note the
   COT date in the header comment; lead the note with it.
2. `ytd_positioning.png` — for the YTD picture: where each currency sits in
   its own year's range, and whether it moved toward or away from an extreme
   in the last week (× vs •).
3. `history_positioning.png` — for the long-run *shape*: the trajectory, regime
   shifts, how the current move compares to past swings. The y-axis is now the
   **full-history percentile** of Total Net % OI (0–100), so the line's level
   reads directly as `Hist Pctl`: 50 = the currency's own median, the 90th/10th
   bands mark the long/short ends of its range, and the fill is green above the
   median, red below. The current endpoint equals the `Hist Pctl` column. For a
   genuine multi-year *extreme* read, still cross-check `Hist Z` in the table
   (|Hist Z| ≳ 2 is a true outlier); the 90th/10th bands flag range ends, which
   is a softer bar than ±2SD.

If the script reports a currency skipped for insufficient history, say so
rather than inventing a read.

If your runtime can't view images, work from `positioning_table.csv` alone —
its 13W/52W/5Y and full-history (Hist Z / Hist Pctl) columns capture the
positioning state — and note in the output that the chart-based reads were
inferred from the table rather than the figures.

### 3. Reading the metrics

The table columns, and what each tells you:

- **Total Net** — (Leveraged Funds + Asset Managers) net long−short, % of open
  interest. Positive = net long the currency vs USD. This is the headline
  position. (DXY is the dollar itself: positive = net long USD.)
- **LevFd Net / AstMgr Net** — the two cohorts that sum to Total Net. Fast
  money vs real money. When they disagree, that's a story — surface it.

The percentile/z columns come in **three nested lookback windows** — read them
as a horizon ladder, and always name which one you mean:

- **13W Pctl / 13W Z** — vs the last ~3 months: the **tactical** read (recent
  build/unwind).
- **52W Pctl / 52W Z** — vs the trailing year: the **cyclical** read. Pctl ≥ 90
  = at the long end of the range; ≤ 10 = at the short end. Z = SDs from the mean.
- **5Y Pctl / 5Y Z** — vs the last ~5 years (260 reports): the **structural /
  multi-year** read. This is what catches a position that looks unremarkable on
  the year but is stretched on a multi-year basis, or vice versa (e.g. AUD here
  is only the 7.7th %ile on 13W yet the 93.8th / +2.2z on 5Y — tactically being
  cut, but still structurally a large long). When the windows disagree, that
  *is* the story — a regime shift or a position rebuilding/unwinding — so spell
  it out.
- **Hist Z / Hist Pctl** — the position vs its **full history** (2006→). This,
  *not* the 13W/52W/5Y windowed stat, is what the history chart plots on its
  y-axis (`Hist Pctl`) and the only correct basis for any "historic extreme /
  multi-year high-low" claim. **Use the right window:** 13W/52W/5Y = *windowed*
  crowding; Hist = *all-time* range position. They can diverge sharply — never
  map one onto the other. The history chart now shows `Hist Pctl` directly, so
  the line's level is trustworthy; use `Hist Z` for whether a level is a true
  *outlier* (|Hist Z| ≳ 2). (Worked example: CHF reads 98th %ile / +1.8z on 52W
  — top of the *past year*, shorts covered — but only 19th %ile / −0.9 Hist Z,
  i.e. *below* its long-run mean and still net short. On the history chart it
  sits in the lower, red, below-median band — well short of the 90th-percentile
  long-end line. Claiming it "presses the top of its range" would be wrong.)
- **WoW Chg / MoM Chg** — change in Total Net % OI vs last week / ~4 weeks ago.
  The *flow*. Describe the biggest movers and the direction of flow.

**Level and stretchedness — always read together.** Total Net is the *size and
direction* of the position; percentile/z is how *stretched* it is vs the
currency's own history. They are independent and both matter: a large net
position at a mid-range percentile is big but **not crowded — it has room to
extend** before hitting an extreme, whereas a small net position at a range
extreme is stretched despite its size. Never report the level without the range
position, and flag when they point different ways (e.g. BRL: the book's biggest
long but only the 50th %ile → not stretched, headroom to extend; CHF: net short
but at the 98th %ile → a covered short stretched toward the long end).

This is a **descriptive** positioning monitor, not a trade-recommendation
engine. Crowding is **not by itself a directional signal**: if positioning is
justified by fundamentals/carry it can persist or extend (positioning then
*confirms* a trend — some research treats it as a supplement to momentum), and
only an extreme with little fundamental support is closer to the classic
contrarian read. The empirical evidence is mixed. So describe *where the market
is positioned* and the position's character/robustness — do **not** tell the PM
what to trade (no "fade," "buy," "sell," "squeeze candidate"). Let the PM draw
the directional conclusion. See `references/writing_style.md`.

### 4. Write the note

Read `references/writing_style.md` now — it carries the house voice,
structure, vocabulary, and the analytical angles (aggregate-vs-dispersion,
lev-vs-asset-manager split, percentile-vs-z, WoW flow, level-vs-range,
full-history range position). Follow it.

Write the note as a markdown file in the output directory
(`fx_positioning_note_<COT-date>.md`) **and** present it in the chat. Use this
structure:

```markdown
# FX Positioning Monitor — <COT date, e.g. 2 Jun 2026>
*CFTC TFF Futures+Options Combined · Net = Leveraged Funds + Asset Managers, % of open interest*

**Key Takeaways**
- <4–6 bullets, each a claim with a number, currency/theme first>

## Aggregate / USD
<DXY and the broad picture: net long/short USD, neutral-but-dispersed?, regime>

## G10 divergences
<who's crowded long / short / just flipped; lev-vs-asset-manager splits; biggest WoW movers>

## EM
<MXN, BRL, ZAR: levels, range position, cohort split, sharp builds/pares>

## At a glance
<a compact scoreboard, NOT prose that repeats the sections above. One terse line each — e.g. "Range extremes: CHF (top, 98%ile) · JPY (floor, 4th) · NZD (13W top, 100th)" / "Biggest WoW: NZD +12.8 · CAD −8.4 · ZAR −7.8" / "Cohort splits: USD AM-long vs lev-short · AUD all-lev · BRL all-AM". If it would just restate the body in full sentences, cut it.>

---
*Source: CFTC TFF Combined. Charts: ytd_positioning.png, history_positioning.png.*
```

Reference the two charts by name so the PM knows which figure backs each read.

### Punch and no repetition

This is a desk note — make every line earn its place.

- **Punchy.** Short, declarative sentences. Lead with the currency and the
  number. Cut hedges, filler, and throat-clearing ("it is worth noting that…",
  "interestingly…"). One idea per sentence.
- **No repetition across sections.** The Key Takeaways are a summary, so they
  necessarily preview the body — that's fine. But the body sections must not
  restate each other, and the closing "At a glance" must be a *scoreboard*
  (terse, scannable), not a paragraph re-narrating G10/EM. If a fact is in the
  body, don't say it again in full prose at the end — reduce it to a tag.
- **Say each number once, in its most relevant home.** Don't quote CHF's
  98th %ile in the takeaway, again in G10, again in the closing section as a
  sentence. Take + one body mention is enough.

### 5. Strictly data-only — no macro, no placeholders

Confine the note to what is in `positioning_table.csv` and the two charts.
**Do not** add external macro, carry, rate-differential, central-bank or event
references, and **do not** insert `[PM: …]` placeholders. Don't speculate on
*why* a position sits where it does or whether it's justified — that's the
PM's domain. Report the positioning state and stop there. Analyse positioning
vs USD as the data is computed. (If the user supplies macro context in the
prompt, you may use it — but never invent it.)

## What good looks like

A PM should be able to read the Key Takeaways in 20 seconds and know where the
market is positioned and what sits at an extreme; read the body in two minutes
and understand the cohort splits, flows, and how each position sits vs its own
history; and trust every number because it traces to `positioning_table.csv`.
Lead with the signal, quantify everything, describe the state of positioning —
and leave the trade to the PM.
