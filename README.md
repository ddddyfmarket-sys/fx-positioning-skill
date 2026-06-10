# claude-fx-positioning

A [Claude Code](https://claude.com/claude-code) **skill** that turns live CFTC
positioning data into a sell-side-style FX positioning note for a macro PM.

When invoked, it:

1. Runs a self-contained Python pipeline that pulls **CFTC TFF
   (Traders in Financial Futures), Futures+Options Combined** data from the
   CFTC Socrata API for 11 markets — **EUR, JPY, GBP, CHF, CAD, AUD, NZD, MXN,
   BRL, ZAR, DXY** — and computes **Leveraged-Funds + Asset-Manager net
   positioning as a % of open interest**, with 52-week and 13-week percentiles
   and z-scores, week-over-week and month-over-month changes.
2. Produces a formatted Excel workbook, two charts (a YTD positioning-score
   distribution and a full-history time series with ±2SD bands), and a
   machine-readable CSV.
3. Has Claude read the table and **view the charts**, then write a one-page
   positioning note in the house style of the JPM FX Positioning Monitor /
   Morgan Stanley G10 FX positioning reports.

The note is **descriptive, not advisory** — it tells you where the market is
positioned (levels, range position, cohort splits, flows), and leaves the
trade and the macro narrative to you. It is **strictly data-only**: no external
macro/carry/event commentary is invented.

## Example output

See [`examples/sample_note.md`](examples/sample_note.md) for a full note, and
the two charts the analysis reads:

| YTD positioning-score distribution | Full-history net positioning (±2SD) |
|---|---|
| ![YTD](examples/ytd_positioning.png) | ![History](examples/history_positioning.png) |

## Install

This is a **personal skill** — it lives in `~/.claude/skills/`.

```bash
git clone https://github.com/ddddyfmarket-sys/claude-fx-positioning.git \
  ~/.claude/skills/fx-positioning
pip install -r ~/.claude/skills/fx-positioning/requirements.txt
```

Then start (or restart) a Claude Code session — the skill is picked up
automatically. Verify it's loaded with `/skills`.

> **Note:** the skill folder must be named `fx-positioning` (it matches the
> `name:` in `SKILL.md`), hence the clone target above.

## Usage

In Claude Code, just ask for a positioning read, e.g.:

- *"Give me an FX positioning update."*
- *"What's the CFTC/COT data saying on G10 and EM?"*
- *"Run the FX positioning monitor."*

Claude runs the pipeline and writes the note into your current working
directory alongside the data outputs.

You can also run the pipeline directly:

```bash
python3 ~/.claude/skills/fx-positioning/scripts/fx_positioning.py            # outputs to CWD
python3 ~/.claude/skills/fx-positioning/scripts/fx_positioning.py --outdir . # explicit dir
python3 ~/.claude/skills/fx-positioning/scripts/fx_positioning.py --refresh  # bypass 24h cache
```

### Outputs

| File | What it is |
|---|---|
| `positioning_table.csv` | The table incl. the Leveraged-Funds vs Asset-Manager split — the source of truth for every number in the note. |
| `ytd_positioning.png` | YTD distribution of each currency's 52W positioning score, with current (×) and 1-week-ago (•) marked. |
| `history_positioning.png` | Full-history small multiples per currency: Total Net % OI with ±2SD bands. |
| `Positioning_Data.xlsx` | Formatted table + both charts embedded. |

The CFTC API response is cached locally (`~/.fx_cache/`) for 24h, so repeated
runs are fast and don't re-hit the API.

## Repository layout

```
SKILL.md                  the skill definition (workflow + metric interpretation)
scripts/fx_positioning.py the CFTC pipeline
references/writing_style.md the house writing style the analysis follows
examples/                 a sample note + charts
requirements.txt          Python dependencies
```

## Methodology

- **Net % OI** = (Leveraged Funds net + Asset Managers net) / Open Interest × 100,
  using CFTC TFF Futures+Options Combined.
- **Percentile** = where the latest Total Net % OI sits within its trailing
  52-week / 13-week window (crowding / range position).
- **Z-score** = standard deviations of the latest reading from the mean of that
  window (extension).
- 52W ≈ the cyclical read; 13W ≈ the tactical/recent read.

## Disclaimer

This tool summarizes publicly available CFTC positioning data. It is not
investment advice and produces no trade recommendations. Data is sourced from
the CFTC; accuracy is not guaranteed. Use at your own risk.

## License

[MIT](LICENSE).
