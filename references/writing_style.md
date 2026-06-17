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
and the charts. **No external macro or events, carry, rate-differentials,
central-bank narrative, or self-explanation (e.g. "broad de-risk/risk-on,"
"structural vs cyclical") — and no `[PM: …]` placeholders.** Don't speculate on
*why* a position is where it is or whether it's justified — that's the PM's
domain. Describe, don't explain; stop there. (If the PM gives you macro context
in the prompt, you may use it — but never invent it.)

## Vocabulary (use it, don't overdo it)

- Extension / range position: *crowded, stretched, extended, elevated, at the
  top/bottom of its range, at a range extreme, one-sided, light, balanced,
  near the floor/ceiling of its 12-month range.*
- Headroom (a *data* observation — distance from a crowding extreme, not a
  price call): *not stretched, room to extend, headroom to build, far from its
  range extreme, mid-range despite the size.*
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
  percentile with a modest z is range-bound-high; a high z is a genuine outlier.
- **Three horizons — name the one you mean.** 13W = tactical/recent, 52W =
  cyclical (1Y), 3Y = structural/multi-year (the rolling-3Y percentile is also
  the history chart's y-axis); plus Hist (full history, full sample), used for
  all-time extreme reads. The windows nest, and when they disagree *that is the signal*:
  a position can be at its 13W floor yet near its 3Y high (being cut but still
  structurally large), or fresh on the year but neutral over 3Y. Spell the
  divergence out descriptively — it's the difference between a tactical wobble
  and a structural shift. Don't quote all three windows for every currency;
  lead with the one that carries the point and bring in another only when they
  diverge.
- **WoW/MoM flow.** The *change* often matters as much as the level. A large
  WoW/MoM move into a position vs out of one is worth flagging. Describe the
  biggest movers and the direction of flow — don't editorialise it into a
  signal. If there is meaningful directional nuance for WoW vs MoM flow (
  strong MoM and WoW add/drop further or huge WoW reverse MoM direction), tell the story.
  
- **Level *and* stretchedness — always together.** These are two different
  facts and both matter. The **absolute net** (% OI) gives the *size and
  direction* of a position; the **percentile / z-score** gives how *stretched*
  that is vs the currency's *own* history. Report both — one without the other
  is misleading. A large net position sitting **mid-range is big but not
  crowded**, so it has **headroom to extend** further before reaching a
  historical extreme; a **modest net position at a range extreme is stretched**
  despite its size. Always say where a position sits in its range, not just how
  big it is, and flag when level and stretchedness point different ways.
  - Big but not stretched: *"BRL holds the book's largest net long (+54.9% OI)
    — almost all asset-manager (+51.9), leveraged funds near flat (+3.0) — but
    sits only mid-range (50th %ile), so the long is far from stretched and has
    room to extend. Pared −12.7 MoM, added back +3.4 WoW."*
  - Mirror case (stretched despite the sign): *"CHF is net short (−34% OI) yet
    sits at the top of its range (98th %ile) — a heavily-covered short,
    stretched toward the long end despite the negative net."*
- **History chart = rolling 3Y percentile (endpoint = `3Y Pctl`; use `Hist Pctl` /
  `Hist Z` for all-time reads).** The history chart's y-axis is the **rolling 3Y
  (trailing-156-report) percentile** of Total Net % OI — each point ranked only
  against its prior ~3 years, so it reads as how stretched positioning was *at that
  time* — with the 50th-percentile median dotted and the 90th/10th range-ends
  dashed. The chart endpoint equals the **`3Y Pctl`** column, *not* `Hist Pctl`.
  For the all-time "where in its full range" read, use the `Hist Pctl` column, and
  for "genuine outlier vs merely elevated" lean on `Hist Z` (|Hist Z| ≳ 2 is a true
  extreme; the 90th/10th bands flag range ends, a softer bar). The windows can
  diverge hard: a book can sit at the top of its trailing year (52W 98th %ile) yet
  below its long-run mean (Hist Z −0.9) and mid-low on its 3Y percentile — the
  recent picture is "shorts covered to a 1-yr high," the structural picture is
  "still net short, mid-low range." Say which window you mean. Never attribute a
  52W extreme to the history chart — that chart is the rolling-3Y percentile.

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

### Strictly data-only — no macro, no placeholders

Restating the hard rule because it's the most common failure: confine the note
to `positioning_table.csv` and the charts — no external macro, carry,
rate-differential, central-bank or event references, and no `[PM: …]`
placeholders. Analyse positioning **vs USD**, as the data is computed. (See "What
this note is" above for the full rationale.)

## Tone

Crisp, declarative, numerate, descriptive, professional. This is a positioning monitor, not a strategy piece: 
report the state of the market clearly and let the PM explain and act on it.
