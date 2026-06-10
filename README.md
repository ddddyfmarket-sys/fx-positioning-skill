# claude-fx-positioning

An **[Agent Skill](https://www.anthropic.com/news/skills)** — works in
[Claude Code](https://claude.com/claude-code), Cursor, OpenAI Codex, and other
`SKILL.md`-compatible agents — that turns live CFTC positioning data into a
sell-side-style FX positioning note for traders and macro PMs.

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
3. Has the agent read the table and **view the charts**, then write a one-page
   positioning note in the house style of the JPM FX Positioning Monitor /
   Morgan Stanley G10 FX positioning reports.

The note is **descriptive, not advisory** — it tells you where the market is
positioned (levels, range position, cohort splits, flows), and leaves the
trade and the macro narrative to you. It is **strictly data-only**: no external
macro/carry/event commentary is invented.

## Example output

The Excel workbook (`Positioning_Data.xlsx`) — the formatted table with
crowding highlights (green = crowded long, red = crowded short):

![Positioning table](examples/positioning_table.png)

The two charts the analysis reads (also embedded in the workbook):

| YTD positioning-score distribution | Full-history net positioning (±2SD) |
|---|---|
| ![YTD](examples/ytd_positioning.png) | ![History](examples/history_positioning.png) |

And the written note Claude produces from them: see
[`examples/sample_note.md`](examples/sample_note.md).

## Install

This is a standard [Agent Skill](https://www.anthropic.com/news/skills) — a
`SKILL.md` (YAML `name`/`description` + instructions) plus a bundled Python
script and reference doc. The format is supported by Claude Code and adopted by
other agent tools (Cursor, OpenAI Codex, and any host that loads `SKILL.md`
skills), so the same repo works across all of them. The pipeline and writing
style are plain Python + Markdown — nothing is Claude-specific.

Clone it into your tool's skills directory. **Keep the folder named
`fx-positioning`** — it must match the `name:` in `SKILL.md`.

```bash
# Claude Code
git clone https://github.com/ddddyfmarket-sys/claude-fx-positioning.git \
  ~/.claude/skills/fx-positioning

# Cursor
git clone https://github.com/ddddyfmarket-sys/claude-fx-positioning.git \
  ~/.cursor/skills-cursor/fx-positioning

# OpenAI Codex  (CODEX_HOME defaults to ~/.codex)
git clone https://github.com/ddddyfmarket-sys/claude-fx-positioning.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/fx-positioning"

# Any other agent: clone into wherever your host loads skills from.
```

Then install the Python dependencies (from inside the cloned folder):

```bash
pip install -r requirements.txt
```

Restart your agent session so it picks up the new skill (in Claude Code,
confirm with `/skills`).

### Requirements

- **Python 3** with the packages in `requirements.txt`.
- A host/agent that can **run shell commands and read files**. Image input is
  recommended (so the agent can view the two charts), but optional — without
  it the skill falls back to the CSV, whose percentile/z-score columns capture
  most of what the charts show.

## Usage

In any agent that has the skill installed, just ask for a positioning read,
e.g.:

- *"Give me an FX positioning update."*
- *"What's the CFTC/COT data saying on G10 and EM?"*
- *"Run the FX positioning monitor."*

The agent runs the pipeline and writes the note into your current working
directory alongside the data outputs.

You can also run the pipeline directly (point Python at wherever you cloned the
skill; outputs go to the current directory):

```bash
SKILL_DIR=~/.claude/skills/fx-positioning   # or ~/.cursor/skills-cursor/fx-positioning, etc.
python3 "$SKILL_DIR/scripts/fx_positioning.py"            # outputs to CWD
python3 "$SKILL_DIR/scripts/fx_positioning.py" --outdir . # explicit dir
python3 "$SKILL_DIR/scripts/fx_positioning.py" --refresh  # bypass 24h cache
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
