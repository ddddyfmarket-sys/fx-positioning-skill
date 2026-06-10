# FX Positioning — house writing style

This captures the voice, structure, and analytical angles of sell-side FX
positioning notes (JPM FX Positioning Monitor; Morgan Stanley G10 FX
Positioning). The reader is a hedge-fund macro PM: assume fluency. No
hand-holding, no defining what a z-score is, no generic market education.
Lead with the signal and quantify it.

## What this note is — and is not

This is a **description of where the market is positioned**, not a trade
recommendation. The job is to tell the PM, precisely and quantitatively:
who is long/short what, how crowded or extended that is vs history, how it
changed this week/month, and how the leveraged-fund and asset-manager cohorts
are positioned. The PM supplies the trade view; the note supplies the
positioning picture they reason from.

**Do not tell the PM what to trade.** No "fade," "buy," "sell," "we'd be long
X," "this screens as a contrarian short," "squeeze candidate to position
for." Describe the positioning and its character; stop there.

**Crowding is not, by itself, a directional signal.** It is tempting to read
an extended long as a contrarian short setup, but that is only one
interpretation and the empirical evidence is mixed — if positioning is
justified by fundamentals it can persist or extend (positioning then *confirms*
a trend; some research treats it as a supplement to momentum). So describe an
extreme as a **fact about the market's state** — where it sits in its range,
how it changed, which cohort holds it — and let the PM draw the directional
conclusion.

**Strictly data-only.** Confine the note to what is in `positioning_table.csv`
and the two charts. **No external macro, carry, rate-differential, central-bank
or event references, and no `[PM: …]` placeholders.** Don't speculate on *why*
a position is where it is or whether it's justified — that's the PM's domain.
Report the positioning; stop there. (If the PM gives you macro context in the
prompt, you may use it — but never invent it.)

## Structure of the note

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
   - **Aggregate / USD** — what the DXY line and the broad G10 picture say. Is
     the market broadly long or short USD? Is the aggregate neutral while
     *dispersion* is high? Name the regime.
   - **G10 divergences** — where G10 is offside. Who sits long, who short, who
     just flipped, who's at a range extreme. Call out the asset-manager vs
     leveraged-fund split where they disagree (see below).
   - **EM** — MXN, BRL, ZAR. Note levels, range position, the cohort split, and
     any sharp WoW build/unwind.
   - **At a glance** — a compact scoreboard, not prose. Which positions sit at
     range extremes, which moved most this week, where the leveraged-fund /
     asset-manager cohorts diverge. Terse tags, no re-narration, no trade calls.

Keep the whole thing to roughly one page. Density over length.

## Vocabulary (use it, don't overdo it)

- Extension / range position: *crowded, stretched, extended, elevated, at the
  top/bottom of its range, at a range extreme, one-sided, light, balanced,
  near the floor/ceiling of its 12-month range.*
- Neutrality: *fairly neutral, roughly flat, close to home, mid-range, no
  strong directional skew.*
- Flow / change: *added to, pared, trimmed, covered, built, extended,
  unwound, reduction, the market bought/sold X this week.*
- Magnitude: always give the number — *"+2.5z," "98th %ile," "+12.8% OI WoW,"
  "biggest weekly build since…"* Sigma/z and percentile are the currency of
  the genre.

## Analytical angles to hit

- **Aggregate vs dispersion.** A flat aggregate USD read often masks large
  currency-level divergence — say so explicitly when the data shows it.
- **Leveraged funds vs asset managers.** Different cohorts (fast money vs real
  money). When they diverge it is informative — e.g. *"asset managers carry
  the EUR length while leveraged funds are marginally short."* The
  `positioning_table.csv` has both legs; use them.
- **Percentile vs z-score.** Percentile = where today sits in the range
  (how crowded/extended). Z-score = how many SD from the mean. A high
  percentile with a modest z is range-bound-high; a high z is a genuine
  outlier. 52W = the cyclical read, 13W = the tactical/recent read. When 13W
  and 52W disagree, a regime shift is in progress — name it descriptively.
- **WoW / MoM flow.** The *change* often matters as much as the level. A large
  WoW move into a position vs out of one is worth flagging. Describe the
  biggest movers and the direction of flow — don't editorialise it into a
  signal.
- **Level vs range position.** Note when these diverge — e.g. a position still
  net short in absolute terms but sitting at the *top* of its own range
  (shorts heavily covered). Describe both the absolute net and where it sits
  vs history; don't collapse them.
- **±2SD bands (history chart).** Where a currency sits vs its own ±2SD
  envelope is the cleanest "extreme or not" read. Use it to say whether the
  current print is genuinely at an extreme or merely elevated.

## Punch, and no repetition

A desk note is dense and fast to read. Every line earns its place.

- **Punchy.** Short, declarative sentences, currency and number first. Cut
  hedges and throat-clearing ("it is worth noting…", "interestingly…",
  "as mentioned…"). One idea per sentence.
- **No repetition.** Key Takeaways summarise, so they preview the body — fine.
  But body sections must not restate each other, and the closing scoreboard
  must be terse tags, not prose re-narrating what's above. Say each number
  once, in its most relevant home (takeaway + one body mention is plenty).

## Tone

Crisp, declarative, numerate, descriptive. This is a positioning monitor, not a strategy piece: report the state of the market clearly and let the PM act on it.
