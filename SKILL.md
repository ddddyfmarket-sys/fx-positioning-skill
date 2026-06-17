---
name: fx-positioning
description: >-
  Generate a sell-side-style FX speculative positioning note from live CFTC
  data. Runs the bundled fx_positioning.py (fetches CFTC TFF Futures+Options
  Combined data for EUR, JPY, GBP, CHF, CAD, AUD, NZD, MXN, BRL, ZAR and DXY,
  computes Leveraged-Funds + Asset-Manager net positioning as % of open
  interest with 13W/52W/3Y percentiles and z-scores, WoW/MoM changes, a YTD
  distribution chart and a full-history chart), then writes a macro-PM-grade
  positioning note in the style of sell-side FX positioning reports. Use this 
  skill whenever the user asks about FX positioning, CFTC / COT / TFF data, 
  speculative or spec positioning, leveraged funds vs asset managers, who is 
  long/short a currency, crowded or stretched or saturated FX positions, contrarian 
  FX setups, positioning squeezes, the FX positioning monitor, or wants a positioning update / read / note on G10 or EM FX — even if they don't name the script or CFTC explicitly.
---

# FX Positioning Monitor

Produce a positioning note for a hedge-fund macro PM: run the data pipeline,
read the outputs (table + three charts), and write the analysis in sell-side
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

The script writes five files to the output directory:

| File | What it is |
|---|---|
| `positioning_table.csv` | The table incl. the Leveraged-Funds vs Asset-Manager split. **Source of truth for all numbers you cite.** |
| `ytd_positioning.png` | YTD distribution box plot: each currency's YTD range of 52W z-scores, with current (×) and 1-week-ago (•) marked. |
| `history_positioning.png` | Full-history small multiples per currency, y-axis = **rolling 3Y (trailing 156-report) percentile** of Total Net % OI (0–100), with 90th/10th range-end bands and the 50th-percentile median. Reads as how stretched positioning was *at that point* vs its prior 3 years. |
| `momentum_positioning.png` | **Supplementary** cross-sectional scatter: y = current 52W z-score (level), x = 1-month change in that 52W z-score (momentum), one dot per currency. Quadrants read as long/short × adding/paring (top-right = long & extending, bottom-right = short & covering). |
| `Positioning_Data.xlsx` | Formatted table + all three charts embedded — the deliverable workbook for the PM. |

### 2. Read the writing style
Read `references/writing_style.md` now — it carries the house voice,
structure, vocabulary, the analytical angles (aggregate-vs-dispersion,
lev-vs-asset-manager split, percentile-vs-z, WoW flow, level-vs-range,
full-history range position), and the structure of the note (important).
Strictly follow the rules to read and describe the output later.

### 3. Read the outputs

Read the analytical outputs before writing a word. The first three are the core
read; the fourth (momentum scatter) is a supplement for broader regime discussion:

1. `positioning_table.csv` — every number you cite comes from here. Note the
   COT date in the header comment; lead the note with it.
2. `ytd_positioning.png` — for the YTD picture: where each currency sits in
   its own year's range, and whether it moved toward or away from an extreme
   in the last week (× vs •).
3. `history_positioning.png` — for the long-run *shape*: the trajectory, regime
   shifts, how the current move compares to past swings. The y-axis is now the
   **rolling 3Y percentile** of Total Net % OI (0–100) — each point ranked only
   against its trailing 156 reports (≈3Y), so the line reads as how stretched
   positioning was *at that time* vs its own recent-3Y range (a point-in-time
   measure, not a full-sample one). 50 = the trailing-3Y median, the 90th/10th
   bands mark the long/short ends of the trailing-3Y range, and the fill is green
   above the median, red below. The current endpoint equals the **`3Y Pctl`**
   column (latest point's trailing-156 window = the 3Y table window) — *not*
   `Hist Pctl`. For a genuine multi-year *extreme* read, still cross-check
   `Hist Z` / `Hist Pctl` in the table (full sample; |Hist Z| ≳ 2 is a true
   outlier); the 90th/10th bands flag trailing-3Y range ends, a softer bar.
4. `momentum_positioning.png` *(supplement only)* — the cross-sectional **level vs
   momentum** snapshot: y = current 52W z-score (how stretched on the year),
   x = the 1-month change in that same 52W z-score (which way, and how fast,
   the book is moving). The four quadrants are long/short (above/below 0) ×
   adding/paring (right/left of 0): **top-right** = net long & extending,
   **top-left** = long but paring, **bottom-right** = short but covering,
   **bottom-left** = short & extending. Use it to group the board by trajectory
   — who is converging on a crowded level vs unwinding off one — and to flag
   positions that are mid-level on the year but moving *fast* (accelerating
   toward crowding). The y-axis equals the `52W Z` column and the x-axis is a
   z-space analogue of `MoM Chg`, so it adds no new numbers — it reorganises
   the table's level + flow into a picture. It's a supplement, not a
   replacement: don't let it override the level/percentile read from the table
   or wow discussion.

If the script reports a currency skipped for insufficient history, say so
rather than inventing a read.

If your runtime can't view images, work from `positioning_table.csv` alone —
its 13W/52W/3Y and full-history (Hist Z / Hist Pctl) columns capture the
positioning state — and note in the output that the chart-based reads were
inferred from the table rather than the figures.

### 4. Reading the metrics

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
- **3Y Pctl / 3Y Z** — vs the last ~3 years (156 reports): the **structural /
  multi-year** read. This is what catches a position that looks unremarkable on
  the year but is stretched on a multi-year basis, or vice versa (a currency can
  be only the 7.7th %ile on 13W yet near the top / +2z on 3Y — tactically being
  cut, but still structurally a large long). When the windows disagree, that
  *is* the story — a regime shift or a position rebuilding/unwinding — so spell
  it out. **The history chart's y-axis is this same rolling-3Y percentile, so
  its current endpoint equals `3Y Pctl`.**
- **Hist Z / Hist Pctl** — the position vs its **full history** (2006→), full
  sample. This is the only correct basis for any "historic extreme / multi-year
  high-low" claim. **Use the right window:** 13W/52W/3Y = *windowed* crowding;
  Hist = *all-time* range position. They can diverge sharply — never map one
  onto the other. Note the history chart now plots the **rolling-3Y** percentile
  (endpoint = `3Y Pctl`), *not* `Hist Pctl`; use `Hist Z` for whether a level is
  a true *outlier* (|Hist Z| ≳ 2). (Worked example: CHF can read 98th %ile / +1.8z
  on 52W — top of the *past year*, shorts covered — yet be far lower on its 3Y
  percentile and below its long-run mean (negative Hist Z), i.e. still net short
  and mid-range structurally. On the history chart (rolling 3Y) it would then sit
  below the 50th-percentile median, in the red band — well short of the 90th
  long-end line. Claiming it "presses the top of its range" would be wrong; that
  is a 52W statement, not a 3Y/historic one.)
- **WoW Chg / MoM Chg** — change in Total Net % OI vs last week / ~4 weeks ago.
  The *flow*. Describe the biggest movers, the direction, and dispersion between
  real and fast money (if any) of flow.


### 5. Write the note

Write the note as a markdown file in the output directory
(`fx_positioning_note_<COT-date>.md`) **and** present it in the chat.

Open the file with this literal title block (fill in the COT date):

```markdown
# FX Positioning Monitor — <COT date, e.g. 2 Jun 2026>
*CFTC TFF Futures+Options Combined · Net = Leveraged Funds + Asset Managers, % of open interest*
```

Then write the body in this order (these are section *instructions*, not text to
copy — use real section headings like `## Key Takeaways`):

1. **Headline** — one line, the single most important descriptive takeaway.
   E.g. *"USD positioning still neutral in aggregate; CHF length at the top of
   its range."* Descriptive, not a call.

2. **Key Takeaways** — 4–6 tight bullets. Each is a *claim with a number*,
   not a vague observation, and not a trade. Lead with the currency/theme,
   state the positioning read, cite the metric in parentheses.
   - Good: *"CHF spec positioning sits at the top of its range — 98th %ile and
     +1.8z on the year — and was added to again this week (WoW +2.8% OI)."*
   - Weak (vague): *"CHF positioning increased this week."*
   - Wrong (a trade call): *"CHF looks crowded — fade the long."*

3. **Body**, organized by theme (not a currency-by-currency march):
   - **Aggregate / USD** — what the DXY line and the broad G10 and EM pictures say. Is
     the market broadly long or short USD? Is the aggregate neutral while
     *dispersion* is high? Name the regime.
   - **G10 divergences** — where G10 is offside. Who sits long, who short, who
     just flipped, who's at a range extreme, and how that extreme compares with
     its prior one. Call out the asset-manager vs leveraged-fund split where they
     disagree.
   - **EM** — MXN, BRL, ZAR. Who sits long, who short, who just flipped, who's at
     a range extreme, and how that extreme compares with its prior one. Call out
     the asset-manager vs leveraged-fund split where they disagree.
   - **At a glance** — a compact scoreboard, not prose. Which positions sit at
     range extremes, which moved most this week, where the leveraged-fund /
     asset-manager cohorts diverge. Terse tags, no re-narration, no trade calls.

Close the file with a source line:

```markdown
---
*Source: CFTC TFF Combined. Charts: ytd_positioning.png, history_positioning.png, momentum_positioning.png.*
```

Keep the whole thing to roughly one page. Density over length.

Reference the charts by name so the PM knows which figure backs each read. The
YTD and history charts are the core evidence; cite `momentum_positioning.png`
when you make a level-vs-trajectory point (who's adding to vs paring a position).

## What good looks like

A PM should be able to read the Key Takeaways in 20 seconds and know where the
market is positioned and what sits at an extreme; read the body in one minute
and understand the cohort splits, flows, and how each position sits vs its own
history; and trust every number because it traces to `positioning_table.csv`.
Lead with the signal, quantify everything, describe the state of positioning —
and leave the trade to the PM.
