---
description: Produce today's relationship brief — 3 buckets (new business / relationship building / network expansion), 3 options each, with recommended channel, time estimate, and copy-ready draft per option. Drafts only — never sends. Respects time-budget filtering, persistent snoozes, and tier-based cadence rules. Reads from cortex person pages, CRM, calendar, inbox; delegates to contact-researcher and pipeline-analyst when installed. Writes a structured `today.json` artifact for downstream UI consumers and appends to a persistent events log on user actions.
---

# /relationships

The daily relationship cockpit. Run in the morning (or anytime) to see who matters today, what to say, and how to spend the next 5/15/30/60+ minutes on relationship work.

---

## Brief ID

Generate a UUID v4 at the start of every run. Set `brief_id` to this value. Included in `today.json` and in every event written to `events.jsonl` so the structured event stream can be correlated back to the specific brief that produced it. Useful for analytics, debugging, and any future UI showing "your last brief."

---

## Step 0 — Preflight

Read `<config-root>/plugins/relationships.user-context.md`. If missing → route to `/setup-relationships` and stop.

Extract:
- Identity (name, first-name form, company, one-line description)
- Business context (primary/secondary ICP, out-of-ICP, current quarter focus, quarterly outcome target)
- Tiers (sizes + cadences) + close-personal track config
- Buckets (weights + hide-empty toggle)
- Voices (each named voice with descriptors, banned phrases, length, sign-off)
- Time budget defaults (typical availability + highly-variable toggle)
- CRM config (tool, owner, stages, tier-property, ICP-fit property, do-not-engage)
- Apollo config (enabled? daily/weekly cap)
- Companion plugins available

Also read (best-effort, skip silently if missing):
- `<config-root>/memory/me/identity.md`, `<config-root>/memory/me/voice.md`
- `<config-root>/memory/hot.md` (cortex hot cache — recent context)
- `<config-root>/memory/DASHBOARD.md` (cortex dashboard — active threads, P0s)

### Schema validation preflight (v0.2.1+)

Before scoring, walk every `memory/person/*.md` file and validate its `relationships:` frontmatter. For each invalid combination OR untagged-page, surface as a warning batch BEFORE the brief renders. The user can either fix in-place or proceed with documented defaults applied silently.

### Step 0.0 — Untagged-page defaults (v0.2.2+)

For every `memory/person/*.md` file where `relationships:` frontmatter is ABSENT entirely (legacy person pages from pre-v0.1.x cortex installs that haven't been touched by `/network-rebalance`), apply the following defaults IN-MEMORY for scoring purposes (do NOT auto-write to the file — that's `/network-rebalance`'s job):

```yaml
relationships:
  tier: operational
  intent: keep_warm
  buckets: [relationship]
  relationship_class: business
  icp_fit: none
  preferred_channels: []
  next_touch_target: <last_meaningful_contact + 90 days, OR today + 90 if no last contact>
```

Surface a count at the top of the warning batch:
> "Note: <N> person pages have no `relationships:` frontmatter — applying default tag (tier:operational, intent:keep_warm, buckets:[relationship]). Run `/network-rebalance` to set explicit values."

This prevents the scoring engine from crashing on `undefined` reads (which was the v0.2.1 bug). Pages with PARTIAL frontmatter (some required fields present, others missing) get individual warnings per Validation Rule 2 below, with defaults filled for the missing fields.

**Validation rules:**

1. **(tier × intent) compatibility** — per `references/person-page-extensions.md`:
   - `tier: inner | strategic` requires `intent ∈ {client_delivery, drive_active, door_opening, reciprocal, advising, content_share}` (active-drive)
   - `tier: operational | dormant` requires `intent ∈ {keep_warm, passive_visibility, awaiting_reply}` (passive)
   - Mismatch (e.g., `strategic + passive_visibility`) → warn.

2. **Required-field presence** — every tagged page must have `tier`, `intent`, `buckets`, `relationship_class`, `icp_fit`.
   - Missing field → warn with which field.

3. **Enum validity** — values must come from the documented enum lists. Free-text values not in the enum → warn.

4. **(class × bucket) sanity:**
   - `relationship_class: personal` + `buckets` containing `new_biz` → unusual; warn ("personal contact tagged for new business — likely tagging error").

5. **(intent × buckets) sanity:**
   - `intent: passive_visibility` + `buckets` containing anything other than `[network]` → warn ("passive_visibility means engage with content only; non-network buckets won't fire").
   - `intent: client_delivery` + `buckets` missing `relationship` → warn.

**Surface format:**

```
SCHEMA VALIDATION — 3 warnings before scoring:

  ⚠ person/sarah-chen.md
    tier: strategic + intent: passive_visibility → contradictory
    Strategic implies active drive; passive_visibility is operational/dormant only.
    Fix: demote tier to operational, OR shift intent to drive_active.

  ⚠ person/jonathan-harms.md
    Missing required field: icp_fit
    Default applied: none

  ⚠ person/derek-patel.md
    intent: client_delivery + buckets: [new_biz]
    client_delivery without `relationship` in buckets — likely tagging error.

Proceed with scoring? (y / fix-now / show-details)
```

- **`y`** — proceed; warnings logged to `<config-root>/memory/staged/skip-logs/schema-validation-<brief_id>.md` (unique per run, v0.2.2+ — avoids concurrent-append race when multiple `/relationships` invocations run in parallel). Older logs are rolled up nightly by `/end-day` into `staged/skip-logs/schema-validation-rollup-<YYYY-MM-DD>.md` to prevent unbounded file growth.
- **`fix-now`** — invoke `/network-rebalance --scoped person/sarah-chen,person/jonathan-harms,person/derek-patel` to walk just the warned pages.
- **`show-details`** — render full validation details for each warning (the rule that fired, the current value, suggested fixes).

Cap: 10 warnings surfaced per run (sorted by severity: contradiction > missing-required > enum-invalid > sanity). Beyond the cap, append "+N more — run `/network-rebalance --validate` for full list."

**Default-on enforcement.** Schema validation runs every `/relationships` invocation. Disable per-run with `--no-validate` (for power users). Disable plugin-wide via `cortex.user-context.md` → `relationships.validate: false`.

---

## Step 1 — Time-budget gate

If user-context has `highly_variable: true`, prompt:

> "How much time do you have today for relationship work? (5 / 15 / 30 / 60+ min)"

Otherwise use the typical default from user-context.

Save the chosen budget — it drives downstream re-ranking. The brief will still show 3 options per bucket, but each option is annotated with its time estimate, and the top-of-brief summary shows "Best fit for your X min" recommendations.

---

## Step 2 — Score and rank candidates

Three buckets. For each, score eligible candidates using the formula in `references/scoring.md`. High-level:

```
score = w_decay × decay_factor
      + w_trigger × trigger_factor
      + w_icp × icp_factor
      + w_reciprocity × reciprocity_factor
      + w_goal × goal_alignment_factor
      − w_penalty × cooling_penalty
```

Weights come from `references/scoring.md` defaults, modulated by the bucket weights in user-context.

### Candidate pool scoping (v0.2.0)

**Read only from `<config-root>/memory/person/*.md`** — never `team/`, `client/`, `bizdev/`, `workstream/`, or any other node prefix. Internal team members live in `team/` and are not subjects of relationship maintenance. The person/ scoping is enforced at this step; no special-case logic later.

### Bucket A — New Business Development

Candidate pool:
- Cortex person pages with `buckets` including `new_biz`
- CRM contacts associated with open deals (read-only)
- Apollo net-new prospects (if Apollo enabled and the weekly cap hasn't been hit; cap from user-context)
- Optional: contacts tagged ICP-fit `primary` or `secondary` in CRM but not in cortex yet
- **Active signal-pipeline entries** (absorbed from lead-engine's `/lead-pipeline`, 2026-09-15) — every non-terminal entry in `<config-root>/relationships/pipeline.md`. For each, compute overdue-ness the same way `/lead-pipeline` did: last-touch date from `<config-root>/relationships/sent-log.md`, next-touch-due from the cadence interval in `relationships.user-context.md`, and flag `overdue: true` if `days_since_last_touch > cadence_interval` and status is `sent` (not `replied`/`booked`/`dead`). Reply-ready signals (`status: replied`, no follow-up sent) get the same top-of-bucket priority `/lead-pipeline` gave them — surface these above everything else in the bucket, even above fresh `new_biz` person-page candidates.
- Cap total signal-pipeline entries surfaced in this bucket at the daily DM budget from `relationships.user-context.md` (same cap `/lead-pipeline` enforced) — the rest stay in the pipeline for tomorrow, don't force them into today's 3 slots.

**If `pipeline-analyst` (core-ops) is installed:** delegate the ranking via Task tool with `subagent_type="pipeline-analyst"`. Pass the user-context path, 90d time window, focus filter "active deals + tier-A overdue + ICP-fit candidates," and `top-n=10` (we only show 3, but get a deeper list to filter).

Apply scoring. Keep the top candidates. For a full standalone "everything active" view of the signal pipeline beyond what fits in today's 3 slots, the user can still ask "what's in my pipeline" — render the same grouped view `/lead-pipeline` used to (🔥 Reply-ready / 📬 Send today / 🟡 Active-waiting / 📥 New-not-drafted / 🪦 Recently closed / 🌡️ Warming-or-awaiting-connection) rather than a separate command.

### Bucket B — Relationship Building

Candidate pool:
- Cortex person pages with `buckets` including `relationship`
- Default `tier: inner` or `tier: strategic` people whose `next_touch_target` has passed
- People with WAITING:you open loops on their person page
- If close-personal track is enabled: people with `relationship_class: personal` and overdue cadence (separate sub-bucket)
- **High-leverage referral moments** (absorbed from referral-engine's `/referrals` weekly digest, 2026-09-15) — for tier-strategic+ people tagged as connectors (per the connector taxonomy in `relationships.user-context.md`), apply the same Bucket-B classification `/referrals` used: a connector with a recent positive moment in the last 14 days (replied warmly, a referred project closed, publicly mentioned you, referred someone recently) is a **gold** high-leverage ask window — surface these with priority. Honor the ask-cadence cap (default 180 days) and quiet threshold (default 60 days) from user-context — never surface a connector inside their cooling window.

Apply scoring. Keep top.

### Bucket C — Network Expansion

Candidate pool (four types — surface a mix):
- **Engagement actions** — LinkedIn comment opportunities on contacts' recent posts (from Apollo pulls via `/pull-signals`), pipeline of "people whose content you actively engage with" from user-context
- **Content posting prompts** — for each named voice, a topic suggestion drawn from cortex recent insights, DECISION entries, or workstream activity. Match topic to voice's surface (e.g., business voice → operational AI on the BrightWay page; personal voice → broader AI thought leadership)
- **Events / conferences / meetups** — Phase 1 surfaces manual entries from user-context only. Phase 5 will add Eventbrite/Luma/Meetup APIs and AI web search.
- **Going-quiet value-share opportunities** (absorbed from `/referrals`, 2026-09-15) — connectors whose `last_meaningful_contact` exceeds the quiet threshold (default 60 days), with no upcoming meeting and no recent activity. Suggested action is a value-share (relevant article/framework/intro), not a direct ask — these are warmth-maintenance, not referral asks (those live in Bucket B).
- **Approaching triggers** (absorbed from `/referrals`) — connectors near a fiscal-year boundary, conference season, or budget cycle per the trigger patterns configured in `relationships.user-context.md`.

Apply scoring. Keep top.

---

## Step 3 — Filter and select 3 per bucket

Before applying hard filters, **read persistent snoozes** from `<config-root>/relationships/snoozes.json`:

```json
[
  { "slug": "sarah-chen", "until_date": "2026-06-10", "reason": "she's traveling", "snoozed_at": "2026-05-28T07:34:00-04:00" },
  ...
]
```

Drop any candidate whose `slug` matches an entry where `until_date >= today`. Entries with `until_date < today` are auto-expired (still in the file for audit; could be cleaned on next run).

If the file is missing, treat as empty — no snoozes active. Don't create it here; it's written by `/relationships-action` when the user snoozes a card.

Then apply hard filters:

- **Cooling period:** if a contact was touched within the tier's minimum-gap window, skip.
- **Do-not-engage:** if CRM marks them DNE, skip.
- **Active-deal sensitivity:** if a contact is mid-active-deal and the next-step is theirs (WAITING:them with a recent commitment from them), skip from new-biz bucket; possibly surface in relationship bucket as a soft touch.
- **"Should we even send?" filter** (ported from `bizdev-outreach`):
  - Is the ball in their court?
  - Did your last message set a tone follow-up would undermine?
  - Is there genuine new value?
  - Too soon based on their bandwidth signals?

Keep the top 3 per bucket post-filter.

If a bucket has < 3 candidates:
- If user-context `hide_empty_buckets: true` → hide the bucket
- Otherwise → show what's available + a "no urgent actions in this bucket — quietly carrying X overdue Operational contacts" footnote

---

## Step 4 — Pick channel + template + draft

For each of the (up to) 9 surfaced cards:

### Intent-driven card framing (v0.2.0+)

Before picking channel + template, read the person's `intent` field. Intent shapes the card's framing — see the intent table in `references/scoring.md`.

For intents `advising` and `passive_visibility`, the brief does NOT draft a generic outreach message. Instead:
- `advising` → render a prompt: "[Person] — monthly advising touch. What's your topic? (door to open or decision worth their counsel)" — wait for user to provide topic, then draft.
- `passive_visibility` → render an "engage with their content" card: "Comment on [their recent post]" or "Engage with [latest LinkedIn activity]." Never propose a direct DM.

For intents `client_delivery`, `drive_active`, `door_opening`, `reciprocal`, `content_share`, `keep_warm`, `awaiting_reply` → proceed to channel + template selection below using intent-appropriate template scenarios.

### Channel selection

A simple rule table (full table in `references/scoring.md`). After the rule-table channel is computed, check the person page's `preferred_channels` array (v0.1.2+) — if the rule-table channel matches an entry, use that match; otherwise fall back to `preferred_channels[0]` unless the trigger is `cold_icp` or `warm_intro` (those override preferences).

| Relationship class | Tier | Trigger | Recommended channel |
|---|---|---|---|
| Business | New (no prior contact) | ICP fit | LinkedIn DM cold OR email cold |
| Business | New | Warm intro available | Email intro request |
| Business | Inner / Strategic | Cadence overdue | Email or LinkedIn DM (their preferred channel from cortex page) |
| Business | Inner / Strategic | They posted | LinkedIn comment on the post |
| Business | Any | Job change / news | LinkedIn DM congrats (5-min touch) |
| Personal | Any | Cadence overdue | Text or Instagram DM |
| Personal | Any | Big news | Phone call |
| Network | — | Content opportunity | Self-post (in the named voice) |
| Network | — | Conference | Pre-event DM to attendees the user knows |

User-context can override per relationship_class.

### Template selection

Map (relationship_class, tier, trigger, channel) → template at `references/templates/<channel>/<scenario>.md`. If user has custom overrides at `<config-root>/relationships/templates/<channel>/<scenario>.md`, prefer those.

### Variable filling

Common variables:
- `{{person.first_name}}`, `{{person.full_name}}`, `{{person.title}}`, `{{person.company}}`
- `{{trigger.context}}` — short string describing why now (e.g., "$12M Series B last week")
- `{{trigger.specific}}` — a more specific reference (e.g., "your post about content velocity")
- `{{user.first_name}}`, `{{user.company}}`, `{{user.one_liner}}`
- `{{shared_context}}` — last-meaningful-contact context from cortex person page (if present)
- `{{voice.signoff}}` — pulled from the voice block being used

If a required variable can't be filled (e.g., no shared context for a cold prospect), pick a template variant that doesn't need it OR mark the card as "draft incomplete — needs your touch" and surface what's missing.

### Voice routing

For Network Expansion content-posting prompts, route to the voice block named in the user-context for that surface (e.g., business voice on the BrightWay page). For all other channels, use the user's primary voice unless `relationship_class: personal` (in which case use the personal voice if defined).

### Time estimate

Each card carries an estimated time-to-execute:
- LinkedIn comment: 2-3 min
- LinkedIn / Instagram DM: 3-5 min
- Text: 1-2 min
- Email cold: 5-8 min
- Email warm: 3-5 min
- Phone call: 10-15 min
- Self-post (with template): 10-15 min draft + review
- Conference DM: 3-5 min

Annotate per card.

---

## Step 5 — Present the brief

Format for fast scanning. Mobile-readable line lengths. This is operational, not a report.

```
GOOD MORNING, [first_name]                    Today's budget: [X] min

  ⚡ Best fits for [X] min (across all buckets):
     • [Bucket] — [Person/topic]  (~Y min)
     • [Bucket] — [Person/topic]  (~Y min)

═══════════════════════════════════════════════════════════════
NEW BUSINESS DEVELOPMENT  (3 options)

1. [Person] · [Title], [Company]
   WHY NOW   [trigger context]
   CHANNEL   [recommended channel]
   TIME      ~[Y] min

   [Drafted message body — copy ready]

   [ Copy ] [ Open in Claude ] [ Skip ] [ Snooze 7d ]

2. ...
3. ...

═══════════════════════════════════════════════════════════════
RELATIONSHIP BUILDING  (3 options) — biz / personal split if both apply

[same per-card format]

═══════════════════════════════════════════════════════════════
NETWORK EXPANSION  (3 options)

[same per-card format]

═══════════════════════════════════════════════════════════════
QUIETLY CARRYING
  [N] Operational contacts overdue; [M] Strategic contacts in cooling.
  Run /network-rebalance quarterly to triage.
```

After presenting, ask: "Want me to draft any deeper, mark anything done, or move on?"

---

## Step 6 — Write the artifact files

After presenting, write the brief in two formats:

### `<config-root>/relationships/today.md`

Markdown snapshot for audit trail and downstream readers (Obsidian, daily-brief integration, the user via grep). Filename `<config-root>/relationships/<YYYY-MM-DD>.md` symlinked or copied to `today.md`.

### `<config-root>/relationships/today.json`

Structured JSON for downstream consumers (future web app, Operator desktop, daily-brief render layer, any third-party UI).

Full JSON schema documented in `references/today-json-schema.md`. Stable contract — schema version `0.1.0`. Includes:

- `schema_version` — bump for breaking changes only
- `brief_id` — UUID v4 generated at the start of this run
- Stable option IDs in form `<bucket>_<person-slug>_<YYYY-MM-DD>` — same person → same ID across re-runs the same day (so a UI can correlate "did I act on Sarah's card?" across page reloads)
- Per-option `actions` block — `copy_payload`, `next_steps_if_done`, `snooze_options_days`
- Per-option `confidence`, `research_thin`, `template` provenance
- Top-level `carrying` summary

A UI consumer reads `today.json` directly; it doesn't need to re-run `/relationships` to render the brief.

---

## Step 7 — User actions (events log + cortex side-effects)

When the user marks a card as "done" / "sent" / "skipped" / "snoozed" (either inline in this conversation OR via `/relationships-action` from a UI), do two things in parallel:

### A — Append to events log

`<config-root>/relationships/events.jsonl` — append-only, newline-delimited JSON. One event per line. Create file if missing.

Event shape:
```json
{
  "ts": "2026-05-28T08:14:33-04:00",
  "brief_id": "<UUID from this run>",
  "option_id": "new_biz_sarah-chen_2026-05-28",
  "person_slug": "sarah-chen",
  "bucket": "new_biz",
  "channel": "linkedin_dm_cold",
  "action": "copied | sent | skipped | snoozed",
  "notes": "(optional free-form, user can dictate)",
  "snooze_until": "2026-06-10 (only when action=snoozed)"
}
```

This log is the canonical event stream a future UI consumes for analytics ("you completed 4/9 today," "weekly volume by channel," etc.). Don't truncate; let it grow. A future `/relationships-stats` command could summarize.

### B — Cortex person-page side-effects (when action ∈ {sent, copied with confirmation})

If cortex is installed (`<config-root>/memory/person/<slug>.md` exists), append to **## Recent interactions** log:

```
<today> — <channel> — relationships brief touch (<bucket>)
```

Update **Last meaningful contact** in Relationship section if appropriate.

**Never** modify Identity, Notes, or other sections. Always additive.

### C — Snooze writes

When `action = snoozed`, also append to `<config-root>/relationships/snoozes.json` (create file if missing):

```json
{ "slug": "sarah-chen", "until_date": "2026-06-04", "reason": "(optional)", "snoozed_at": "2026-05-28T08:14:33-04:00" }
```

The snooze is read by the next `/relationships` Step 3 to filter the candidate pool.

If the user invokes via `/relationships-action` instead of inline, that command handles all three (events log, person-page update, snoozes). This step is the inline equivalent — both paths converge to the same state.

---

## Step 8 — Log to memory/log.md (cortex log-writer)

If cortex `log-writer` skill is available, append:

```
## [YYYY-MM-DD HH:MM] /relationships | brief produced — N actions across 3 buckets, X min budget
```

Otherwise skip.

---

## Behavior rules

- **Drafts only.** Never send a message, never create a CRM task without explicit confirmation, never add a calendar event without confirmation.
- **No guilt.** If the user runs the brief and carries a 40-deep backlog, the brief surfaces the top 3 and quietly notes the rest. No nagging.
- **One-tap actions.** Every card should have a copy-ready draft, a recommended channel, and a time estimate. The user should be able to do the action in under the estimated time without further thinking.
- **Voice-faithful.** Pull from the named voice for the surface. Honor banned-phrases lists (cortex + plugin).
- **Honest about gaps.** If a draft has a missing variable, say so. If pipeline-analyst returns Low confidence, surface it. If a contact has thin cortex data, mark the card as "research-thin — verify before sending."
- **Idempotent within a day.** Running `/relationships` twice in a day re-reads sources and re-ranks; today.md/today.json get overwritten. The user's marked-done actions persist in cortex person pages.
- **Respect the autonomy slider.** In `auto` mode, skip the time-budget prompt (use default) and skip per-card confirmations. In `confirm` mode, walk every card individually.
