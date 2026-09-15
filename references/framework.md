# The `relationships` framework

A hybrid framework for prioritizing relationship work. Draws from Herminia Ibarra's tiered cadence model (the spine), Keith Ferrazzi's *Never Eat Alone* (the qualitative layer), and a reality-layer adjustment for solo operators with finite time.

## Why hybrid

Pure tiered cadence (Ibarra) is operationally clean but doesn't capture qualitative depth — generosity, open loops, voice. Pure Ferrazzi is qualitative but doesn't give you a daily ranking. The Dunbar 5/15/50/150 model gives capacity guardrails but no cadence. The hybrid:

- **Tiered cadence (Ibarra spine):** Inner / Strategic / Operational / Dormant — gives every contact a target frequency and surfaces the overdue ones.
- **Ferrazzi qualitative layer:** touch types, generosity ledger, open loops.
- **Reality layer:** the "no guilt" and "how much time today?" adjustments that make this usable for someone running a real life.

## The three buckets

Every daily action falls into one of three buckets. They're separated visually in the brief so prospecting energy doesn't crowd out maintenance, and content/event work doesn't crowd out direct outreach.

### 1. New Business Development

Outbound + active-deal forward motion.

**Who:**
- ICP-fit cold prospects (from Apollo or manually staged)
- Open-deal contacts where the ball is in your court
- Warm-intro asks to connectors

**Why it's separate:** prospecting energy is different from maintenance energy. Lumping them together leads to either prospecting drift or relationship neglect, never both well.

### 2. Relationship Building

Maintenance + deepening of strategic and personal relationships.

**Who:**
- Inner-core contacts (biweekly cadence)
- Strategic contacts (monthly cadence)
- Operational contacts surfaced only on trigger
- **Close personal** sub-track (family, closest friends) — visible alongside business but in its own column so the personal doesn't compete with biz priorities

**Why it's separate:** maintenance compounds. If the brief mixes "send Sarah a cold LinkedIn DM" with "call your mom because it's been three weeks," the operator's brain treats the personal call as work-equivalent. The split keeps them honest.

### 3. Network Expansion

Surface-area work that doesn't target a specific contact.

**Who/what:**
- LinkedIn engagement targets (comment on posts of people in your engagement set)
- Content posting prompts — one or more voices (e.g., personal brand + business brand)
- Conferences, meetups, events worth attending
- Podcast / interview opportunities

**Why it's separate:** network expansion is a leading indicator. It generates the inputs to the other two buckets. Without protecting time for it, the pipeline starves over the next 6-12 months.

## The four tiers

Configurable per user. Defaults:

| Tier | Default size | Default cadence | Surfacing rule |
|---|---|---|---|
| **Inner Core** | 10–15 | every 14 days | Always surfaces when overdue |
| **Strategic** | 30–50 | every 30 days | Surfaces when overdue + trigger present |
| **Operational** | 100–200 | every 90 days | Surfaces on trigger only |
| **Dormant** | rest | trigger-only | Never proactively surfaced |

### How to decide who's where

**Inner Core** — people whose relationship is essential to your current life chapter. Spouse, closest mentors, top 5 business partners, the 3 friends you'd call at 2am. Not "everyone I like." Capacity-limited.

**Strategic** — people who matter to your trajectory but you can be intentional about over months, not weeks. Most clients during active engagement. Peer founders. Key advisors. Active connectors.

**Operational** — the wider network. Past clients in maintenance mode. Industry peers you know but rarely work with. Connectors in dormant cycles. Most of your LinkedIn.

**Dormant** — historical. Demoted from Operational over time. Surfaces only when a trigger fires (they post, they change jobs, they reach out).

### Honest sizing

If you say your inner core is 30 people, the cadence math breaks and you'll feel guilty constantly. The framework refuses to be cruel: if 30 people sit in `inner` and you can't touch them all every 14 days, the brief surfaces the highest-leverage 3 and the rest go quiet. But the better fix is honest sizing during `/setup-relationships`.

## The Ferrazzi layer (qualitative)

Tier-based cadence handles the "when" — Ferrazzi-style tracking handles the "what" and "how."

### Touch types

Every interaction has a type. Logged in cortex person pages' `## Recent interactions` log:

- `meet` — in-person or video meeting
- `call` — phone or scheduled video call
- `message` — DM, email, text
- `comment` — public engagement (LinkedIn comment, etc.)
- `gift` — physical or experience gift
- `intro` — you introduced them to someone
- `referral` — you sent them a paid opportunity

### Generosity ledger

Tracks giving and receiving over time. Drives the reciprocity factor in scoring. The principle: relationships are debited and credited by what you do for each other. Surfacing this gives the brief a way to weight "you owe them" actions higher than "they owe you."

### Open loops

WAITING:them and WAITING:you tags on the cortex page (already in v4.2 schema). The brief surfaces open loops aggressively — especially WAITING:you because those are reputation-impacting.

## The reality layer

Adjustments for the actual operator running this — solo, finite time, kids, other obligations.

### No guilt

If 40 contacts are technically overdue, the brief surfaces the 3 highest-leverage. The rest get quietly noted in a "carrying" footnote. No nagging, no red flags. The user can run `/network-rebalance` quarterly to demote whoever doesn't deserve their tier slot.

### Time-budget honesty

Every option carries an estimated time-to-execute. At the top of every brief, a "best fits for your X min" summary picks the cards that fit. Available budgets: 5 / 15 / 30 / 60+ min.

The user can also turn on **highly variable mode** in setup — then the brief asks at the top of every run.

### Trigger-driven Operational

Operational contacts (100-200 of them) don't get cadence-driven surfacing. They surface only when a trigger fires:
- They post something worth engaging with
- They change jobs
- Their company hits a milestone
- Mutual connection mentioned them
- They reached out (which becomes WAITING:you for you)

This keeps the brief sized to the user's actual capacity. Cadence-driven surfacing is for ~50 people max; trigger-driven scales to the rest of the network.

### Quarterly resets

Every ~90 days, run `/network-rebalance` (Phase 3) to:
- Demote contacts who don't deserve their tier (Inner → Strategic, Strategic → Operational, Operational → Dormant)
- Promote contacts who've earned a closer tier
- Re-tag ICP fit as your business focus evolves
- Archive dormant pages that haven't seen interaction in a year+

This is the maintenance ritual that keeps the framework honest.

## What this is NOT

- **A CRM.** No deal stages, no pipeline forecasting, no sales reporting. That's `ops`, `weekly-outreach` (being retired), and your actual CRM.
- **An autopilot.** Drafts only. The user always decides whether to send.
- **A guilt machine.** It will not tell you "you've been a bad friend." It will tell you "if you have 5 minutes, here's the highest-leverage thing."
- **A scoring black box.** Scoring math is documented in `scoring.md`. Weights are user-configurable.

## See also

- `references/scoring.md` — the weighted-scoring math, channel-selection table, and signal definitions
- `references/person-page-extensions.md` — the schema additions on cortex person pages
- `references/templates/README.md` — the templates library powering the drafts
