# Scoring + channel selection

How `/relationships` ranks candidates and picks channels.

## The score formula

```
score = w_decay × decay_factor
      + w_trigger × trigger_factor
      + w_icp × icp_factor
      + w_reciprocity × reciprocity_factor
      + w_goal × goal_alignment_factor
      − w_penalty × cooling_penalty
```

All factors are clamped to `[0, 1]` (penalty to `[0, 1]` as well). Final scores are not normalized — they're used for within-bucket ranking only.

## Default weights

| Weight | Default | Description |
|---|---|---|
| `w_decay` | 0.30 | How overdue against the tier's cadence target |
| `w_trigger` | 0.25 | External triggers — job change, funding, posts |
| `w_icp` | 0.20 | ICP alignment for the new-business bucket |
| `w_reciprocity` | 0.15 | Open loops + recent give/receive balance |
| `w_goal` | 0.10 | Quarterly goal alignment from user-context |
| `w_penalty` | 0.40 | Cooling-period and do-not-engage penalty (subtracted) |

User-context can override per bucket — e.g., a user focused on prospecting could weight `w_icp` higher in the new-business bucket.

## The factors

### `decay_factor`

```
effective_cadence_days = cadence_days_override OR tier_default_cadence_days
decay_factor = clamp(
  (days_since_last_touch − effective_cadence_days) / effective_cadence_days,
  0.0, 1.0
)
```

- `0.0` if the contact is within cadence
- `0.5` if the contact is one full cadence period overdue
- `1.0` if the contact is two or more cadence periods overdue (or more, clamped)

`cadence_days_override` (v0.2.0+) lets a person use a custom cadence regardless of tier default — e.g., strategic-feel + quarterly cadence. If unset, the tier default applies.

Untouched-since-graduation contacts use a baseline `last_touch = graduation_date`.

**Follow-up window override for `intent: awaiting_reply` (v0.2.0+):** when a person's intent is `awaiting_reply`, the decay_factor formula is replaced by a follow-up window:
- 0-7 days since outreach: `decay_factor = 0.0` (fresh, give them space)
- 7-21 days: `decay_factor` ramps linearly from 0.0 to 0.8 (gentle "follow up if no response" pressure)
- 21+ days: `decay_factor = 1.0` (clear signal to either re-touch or shift intent to `keep_warm`)

This prevents "just sent a DM 5/28" people from getting the full operational 90-day cooling period when the real question is "when should I bump if no reply?"

### `trigger_factor`

The presence + recency + relevance of an external signal. Signals come from `/pull-signals`; otherwise from CRM custom-property changes or manual flagging.

| Signal type | Base value | Recency decay |
|---|---|---|
| Job change in last 30d | 0.9 | linear to 0 at 90d |
| Funding round in last 30d | 0.8 | linear to 0 at 90d |
| Promotion / new role | 0.7 | linear to 0 at 60d |
| Content posted in last 7d | 0.6 | linear to 0 at 21d |
| Mutual mentioned them | 0.5 | linear to 0 at 14d |
| Company milestone (launch, news) | 0.5 | linear to 0 at 30d |
| (no trigger) | 0.0 | — |

If multiple triggers present, take max (don't sum — avoids double-counting).

### `icp_factor`

```
primary  → 1.0
secondary → 0.6
none      → 0.1
```

Out-of-ICP contacts can still appear in the new-business bucket only if a strong trigger overrides (e.g., they posted something directly relevant).

### `reciprocity_factor`

Composite of two signals:

```
reciprocity_factor = 0.6 × waiting_you_factor + 0.4 × generosity_balance
```

`waiting_you_factor`:
- `1.0` if there's a WAITING:you tag on the person page that's been open > 7 days
- `0.5` if WAITING:you tag exists but < 7 days
- `0.0` otherwise

`generosity_balance`:
- Sum the last 5 generosity-ledger entries. Each `gave` = +1, each `received` = -1.
- Negative balance (you've given more lately) → 1.0 — they're "due" to reach out; deprioritize as outbound target
- Wait — this is inverted. Let's restate:
  - Negative balance (you gave more) → 0.3 (lower priority for you to reach out again; they should)
  - Zero balance → 0.6 (normal)
  - Positive balance (they gave more) → 1.0 (you owe them — high priority for you to reach out)
- Empty ledger → 0.5

### `goal_alignment_factor`

If user-context specifies a current quarter focus (e.g., "Q3 anchor accounts"), score each candidate's alignment:

- Person page explicitly tagged with the focus topic/workstream → 1.0
- Inferred match (ICP + role + recency overlap with focus) → 0.5
- No match → 0.0

If user-context has no quarter focus set → factor is 0.0 (so `w_goal × 0.0 = 0`, no effect).

### `cooling_penalty`

Subtracted from score. High values keep a contact out of the brief.

- Touched within tier's minimum-gap window (defaults: inner 5d, strategic 10d, operational 30d) → penalty `1.0`
- Touched within tier's recommended-gap window → penalty `0.5`
- Marked do-not-engage in CRM or person page → penalty `1.0` (effectively excludes)
- Inside an active-deal cooling window (native referral-cooling rules enforce this) → penalty per its rules

## Intent-driven framing (v0.2.0+)

The person's `intent` field shapes how the daily brief presents the card:

| Intent | Card framing |
|---|---|
| `client_delivery` | "Active engagement touch — [what's open]" with delivery-driven template |
| `drive_active` | "[Specific goal] — drive the conversation" with goal-explicit template |
| `door_opening` | "Stay useful + visible — share [tool/practice/intro]" |
| `reciprocal` | "Match her energy — forward [opp] or thank her for [recent share]" |
| `advising` | "Bring a topic — what door for [name] to open or decision worth their counsel?" |
| `content_share` | "Pure-give — share [tool/framework/practice]. No ask, no quid pro quo." |
| `keep_warm` | "Light touch — no specific goal. Surface only because [trigger]." |
| `passive_visibility` | "Engage with their content — comment, react. NO direct DM." |
| `awaiting_reply` | "Follow-up window [N] days since last outreach. Bump or shift to keep_warm." |

This means the brief doesn't always produce a "drafted message" — for `advising` and `passive_visibility`, it prompts the user to bring intent or engage with content rather than drafting a generic outreach. Templates adapt accordingly.

## Channel selection

Once a contact is selected for a card, pick the channel. The decision table below produces a rule-table default per (relationship_class, tier, trigger).

**The person page's `preferred_channels` array (v0.1.2+) overrides the table:**

1. Compute the rule-table channel for the trigger.
2. If `preferred_channels` is set and the rule-table channel matches any entry → use that match.
3. Otherwise → use `preferred_channels[0]` (primary preference) — UNLESS the trigger is `cold_icp` or `warm_intro` (those override even preferred channels because they require specific formats).
4. If `preferred_channels` is absent/empty → use rule-table default.

This lets a person with `preferred_channels: [text, call]` get text for routine touches AND phone for big-news triggers (since the rule-table routes news to call anyway, matching their array).

| Relationship class | Tier | Trigger | Recommended channel |
|---|---|---|---|
| business | new | cold ICP | `email cold-icp` or `dm linkedin-cold-icp` |
| business | new | warm intro available | `email intro-request` to the connector |
| business | inner / strategic | cadence overdue | `email warm-this-made-me-think-of-you` or `dm linkedin-warm-checkin` (mirror their last channel) |
| business | inner / strategic | their post | `comment on-their-post` (cheap) → optional `dm linkedin-post-followup` (deeper) |
| business | any | job change / news | `dm linkedin-job-change-congrats` or `text congrats-on-news` for inner-core |
| business | any | post-meeting follow | `email post-meeting-recap` |
| business | any | no response on a thread | `email followup-no-response` |
| personal | any | cadence overdue | `text quick-checkin` or `dm instagram-personal-thinking-of-you` |
| personal | any | big news | `call opener-warm-checkin` (or text if call isn't right) |
| network | any | content opportunity | self-post in the named voice (template TBD — Phase 2) |
| network | any | conference attendance | `conference pre-event-dm` to people you know going |
| network | any | post-conference | `conference post-event-followup` |

## Why this composition

- Decay leads. The single most predictive factor of relationship rot is time. Half your tier-strategic contacts are probably overdue right now. The brief surfaces those first.
- Triggers second. Reaching out *when there's a reason* always outperforms reaching out *because it's been a while*.
- ICP for the new-business bucket only. ICP-weighting on a personal contact makes no sense — that's how relationship apps become creepy.
- Reciprocity matters but doesn't dominate. Generosity is a 5-entry rolling window — long enough to capture real patterns, short enough to recover from a single misstep.
- Cooling penalty is steep. The single fastest way to ruin a relationship is over-reaching. The penalty intentionally outweighs most positive factors.

## What this scoring is NOT

- It does not estimate response probability. Response prediction is a hard ML problem and not what we're solving.
- It does not predict revenue. ICP + funnel + close is `pipeline-analyst` / `pipeline-forecast` territory (bundled in this plugin).
- It is not personalized via learning loops in v0.1. Every user gets the same default weights. Phase 4+ might add per-user weight tuning based on which surfaced actions got "done" vs "snoozed."

## Tuning

User-context allows per-bucket weight overrides:

```markdown
## Scoring overrides (optional)

### new_biz bucket
- w_decay: 0.20
- w_icp: 0.40

### relationship bucket
- w_decay: 0.40
- w_reciprocity: 0.25
```

Unspecified weights fall back to defaults.
