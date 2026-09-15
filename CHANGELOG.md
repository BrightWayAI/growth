# Changelog

## [0.4.0] — renamed to growth (2026-09-15)

### Changed
- Renamed from `relationships` to `growth` (display name: Growth Engine) as part of the 2026-09-15 Nucleus plugin rename. The `/relationships` command is unchanged. Old plugin ID/repo name redirects; see marketplace catalog.

## [0.3.6] — compatibility and role metadata hardening (2026-09-15)

### Changed
- Marked retired-plugin reads as explicit one-time compatibility branches so active architecture checks can prevent new runtime dependencies.
- Added host-neutral reasoning-tier metadata to the relationships director.
- Standardized setup and person-page persistence on the vendor-neutral config-root resolver.

## [0.3.5] — Codex adapter synchronization (2026-09-15)

### Added
- OpenAI host bindings for the absorbed buying-signal workflows.

### Fixed
- Updated the read-only `relationships-director` Codex binding and portability contract for its rank/research modes and native signal/referral configuration.

## [0.3.4] — claude plugin eval suite (2026-09-15)

Nucleus Operating Model Refactor Phase 4 step 4.2.

### Added
- `evals/relationships-natural-language/` — eval case testing the relationships skill's natural-language trigger, with an `llm` grader
  checking the response acts on the natural-language request directly rather
  than asking the user to type the explicit command. Run with
  `claude plugin eval . --case relationships-natural-language`; `--ablation with-without`
  (the default when the plugin resolves) reports the delta between installed
  and not — a delta near zero means the skill's description isn't matching
  natural phrasing and needs work.
- `.gitignore` — excludes `evals/results/` (per-run output, not checked in).

## [0.3.3] — Skill auto-invocation audit (2026-09-15)

Nucleus Operating Model Refactor Phase 3 step 3.7. Ritual and side-effecting
skills marked `disable-model-invocation: true` so they only run on explicit
invocation, not loose natural-language matching — the model can still be
asked to run them by name. Read-mostly, low-stakes, or high-frequency
conversational skills are left auto-invocable. Marketplace-wide this brings
model-invocable skills from ~81 to 27, under the ≤30 target audited with
`/skill-doctor`.

### Changed
- Marked `disable-model-invocation: true` on: `relationships-action`, `network-rebalance`, `pull-signals`, `connect-signal`, `warm-signal`, `draft-signal`, `setup`, `setup-relationships`.

## [0.3.2] — relationship-ranker + contact-researcher merged into relationships-director (2026-09-15)

Nucleus Operating Model Refactor Phase 3 step 3.6.

### Changed
- New `agents/relationships-director.md` replaces `relationship-ranker` and
  `contact-researcher`, mode-dispatched (`mode: rank` / `mode: research`).
  Both procedures are preserved verbatim under their mode — this is a
  packaging change, not a behavior change. Callers (`/pull-signals`,
  `/pre-call-brief`, `/draft-touchpoint`, `/relationships`,
  `/setup-relationships`) updated to pass `subagent_type="relationships-director"`
  with an explicit `mode`.
- `.codex/agents/relationship-ranker.toml` + `.codex/agents/contact-researcher.toml`
  replaced by `.codex/agents/relationships-director.toml`.

### Removed
- `agents/relationship-ranker.md`, `agents/contact-researcher.md` — content
  fully preserved in `relationships-director.md`.

## [0.3.1] — nucleus-router routing docs updated (2026-09-15)

### Changed
- "Routing for nucleus-router" sections in `network-rebalance`, `touchpoint`,
  `relationships`, `draft-touchpoint`, `relationships-action` skill docs
  renamed to "Routing for /cos (chief-of-staff)" — `nucleus-router` was
  retired in favor of a `chief-of-staff` agent in `core-ops` (Nucleus
  Operating Model Refactor Phase 3 step 3.1). No behavior change.

## [0.3.0] — Absorbs lead-engine and referral-engine (2026-09-15)

Nucleus Operating Model Refactor Phase 3 step 3.2. Both plugins retire; their
functionality merges into `relationships` (already treated them as config
peers before this — this makes the dependency native instead of optional).

### Added
- `contact-researcher` agent (moved from lead-engine, updated for the new
  namespace) + matching `.codex/agents/contact-researcher.toml` role binding.
- Six new commands, ported from lead-engine's signal-cadence commands (kept
  separate rather than collapsed into one flagged command, to preserve the
  real per-touch nuance — warming decision tree, 3 connection-request
  patterns, per-touch DM rules, quality gates):
  `/pull-signals` (was `/lead-pull`), `/capture-signal` (`/lead-capture`),
  `/connect-signal` (`/lead-connect`), `/warm-signal` (`/lead-warm`),
  `/draft-signal` (`/lead-draft`), `/pre-call-brief` (`/lead-brief`). Each has
  a matching `skills/<name>/SKILL.md` OpenAI-adapter wrapper.
- `references/seven-signals.md`, `references/signal-voice-rules.md`,
  `references/signal-methodology.md` — moved from lead-engine, paths updated.
- `references/templates/referral-ask/` — the 4 referral-ask templates from
  referral-engine (post-positive-touch, post-project, re-warm, trigger-based),
  now selectable from `/draft-touchpoint`'s intent menu (option e).

### Changed
- `/touchpoint` now also handles the signal-pipeline action form
  (`/touchpoint SIG-[id] sent|reply|booked|dead`), absorbed from lead-engine's
  `/lead-log` — same "record what happened" verb, one command.
- `/relationships` Bucket A inlines lead-pipeline's overdue/reply-ready
  signal-pipeline logic instead of an optional `lead-engine`-installed
  delegation. Bucket B/C inline referral-engine's `/referrals` weekly-digest
  classification (high-leverage asks, going-quiet value-shares, approaching
  triggers) the same way.
- `/setup-relationships` captures ICP, signal preferences, Apollo config, and
  referral cooling rules **natively** now (Q6/Q7) instead of importing them
  from `lead-engine.user-context.md` / `referral-engine.user-context.md` peer
  files, since those plugins no longer exist. Existing installs get a
  one-time carry-forward of their legacy values instead of being re-asked.
- `relationships.user-context.md`'s real config (Zach's) was migrated:
  lead-engine's ICP/Apollo/signal-priority answers and referral-engine's
  connector-taxonomy/cooling-rule answers are now native content in this
  file; the two legacy config files were archived, not deleted.

## [0.2.8] — writing-style renamed to voice (2026-09-15)

### Changed
- `commands/setup-relationships.md`, `references/user-context.template.md` —
  plugin-name and config-file references updated from `writing-style` to
  `voice` (Nucleus Operating Model Refactor Phase 3 step 3.4).

## [0.2.7] — Follow-up privacy fix: MedBridge, sang-lee (2026-09-15)

Caught in a second sweep after v0.2.5 shipped — a real prospect company name
("MedBridge") and a real contact slug ("sang-lee") remained in
`references/today-json-schema.md`, `references/person-page-extensions.md`,
`commands/draft-touchpoint.md`, and `references/ui-integration.md`.
Genericized. No functional change.

## [0.2.6] — Identity/voice moved to memory/me/ (2026-09-15)

### Changed
- Path references updated from `<config-root>/identity.md` / `<config-root>/voice.md` to `<config-root>/memory/me/identity.md` / `<config-root>/memory/me/voice.md`, per the Nucleus Operating Model Refactor Phase 2 scopes restructure (identity/voice are personal, not org-shared facts). No behavior change beyond the path.

## [0.2.5] — Genericize hardcoded proprietary examples (2026-09-15)

Nucleus Operating Model Refactor privacy audit: reference docs and command
examples hardcoded real BrightWay client/contact data (real names, a real
company, a real current-quarter strategic target, real contract terms).
Since this plugin is MIT-licensed and public, that data shipped to every
Nucleus user. All examples replaced with fictional placeholders — no
functional/schema change.

### Fixed
- `references/today-json-schema.md` — schema example no longer hardcodes
  "Zach Wagner" / "BrightWay AI" / the real "Studio K-12 anchors" quarter
  target.
- `references/scoring.md` — same quarter-target example genericized.
- `references/person-page-extensions.md` — intent-type examples no longer
  name real contacts (Sang Lee, Rob Buelow, Jennifer Ives, etc.) or a real
  contract figure ("$7K engagement, 35–40 hrs").
- `commands/touchpoint.md`, `commands/draft-touchpoint.md`,
  `commands/network-rebalance.md`, `commands/relationships-action.md`,
  `skills/relationships-action/SKILL.md`, `skills/draft-touchpoint/SKILL.md`
  — example output/prompts no longer name real contacts or clients (Sang Lee,
  Derek/Holt, MedBridge).

## [0.2.4] — OpenAI host adapter (2026-09-14)

### Added
- Native Codex/ChatGPT plugin manifest, durable `AGENTS.md` entrypoint, and an explicit OpenAI capability/degradation contract.
- GPT-discoverable skill aliases for canonical command workflows and read-only Codex role bindings where this plugin ships agents.
- Shared config-root resolution compatible with Cortex and Claude; all GPT tests use repository fixtures or temporary directories only.

## 0.2.3 — Reference docs + retired-plugin migration (2026-05-28)

Followup to v0.2.2 completing the deferred items from the v0.2.0 → v0.2.2 review punch list. Coordinated with cortex v4.12.3 + daily-brief v0.4.2.

### Added — Events.jsonl spec in references/today-json-schema.md

The v0.2.2 unified events shape was documented only in `commands/touchpoint.md` and `commands/relationships-action.md`. UI builders reading the schema reference wouldn't see it. v0.2.3 adds a dedicated **"Events.jsonl shape"** section to `references/today-json-schema.md` covering:
- Full canonical event object with all per-action variants
- Reader rules (missing schema_version → v0.2.0; missing meta → null; unknown action enum → log + render generic; unknown meta fields → ignore)
- Atomic-append safety (4KB cap explanation)
- Version history (v0.1.1 → v0.2.1 divergence → v0.2.2 unified)

### Added — Forward-compat reading discipline in references/ui-integration.md

UI builders need explicit rules for handling mixed-version events.jsonl. v0.2.3 expands the "Reading the events stream" section with:
- 5 forward-compat reading rules (schema_version check, open action enum, optional meta block, null option_id signals touchpoint, 4KB line guarantee)
- Touchpoint event sample shape (was missing from the write-contract section)
- New analytics queries: touchpoint cadence per person, reciprocity balance via meta.direction

### Added — `/network-rebalance` Step 0.5 retired-plugin migration

Detects legacy `weekly-outreach.user-context.md` + `bizdev-outreach.user-context.md` files (from plugins retired earlier today). Offers to migrate relevant fields (ICP, voice rules, banned phrases, CRM mappings, cadence definitions) into the active `relationships.user-context.md`. Conflicts surface per-field reconciliation prompts. Originals archived to `<config-root>/plugins/archive/<name>.<today>.md` (renamed, not deleted). Marker prevents re-prompt.

Idempotent: skip-marker prevents prompt-fatigue. `--migrate-legacy` flag forces re-check.

### Acceptance

- [ ] `references/today-json-schema.md` has "Events.jsonl shape" section with full v0.2.2 spec.
- [ ] `references/ui-integration.md` has forward-compat reading rules + touchpoint sample shape.
- [ ] `/network-rebalance` Step 0.5 retired-plugin migration prompt.
- [ ] `plugin.json` bumped to 0.2.3.

---

## 0.2.2 — Events.jsonl unification + untagged-page defaults + override-log enum (2026-05-28)

Same-day patch fixing 3 CRITICAL findings surfaced by post-ship review. Coordinated with cortex v4.12.2 + daily-brief v0.4.1.

### CRITICAL — Events.jsonl shape unified

v0.2.1's `/touchpoint` wrote events with `summary` field while `/relationships-action` wrote events with `notes` — UI readers would see `null` for every touchpoint. v0.2.2 unifies:

- Canonical `notes` field across both writers (free-form user text, ≤ 4KB cap).
- Touchpoint-specific fields (`direction`, `intent_at_time`, `tier_at_time`, `source`) nested under `meta: {...}`.
- `schema_version: "0.2.2"` on every new event. Missing → treat as v0.2.0 (top-level fields, no meta block).
- `/relationships-action` shape similarly updates to nest `snooze_until`, `late_action`, `source` under `meta:` for consistency.
- `action: "touchpoint"` extends the existing enum `copied | sent | skipped | snoozed`. UI readers must accept unknown action values gracefully.

### CRITICAL — Untagged-person-page defaults

v0.2.1's schema validation in `/relationships` Step 0 silently ignored person pages WITHOUT `relationships:` frontmatter. Scoring engine then crashed on undefined reads. v0.2.2 adds **Step 0.0** that applies documented defaults in-memory for untagged pages (`tier: operational, intent: keep_warm, buckets: [relationship], relationship_class: business, icp_fit: none, next_touch_target: last_meaningful_contact + 90d`). Surfaces a count: "Note: <N> person pages have no frontmatter — applying default tag. Run /network-rebalance to set explicit values."

### CRITICAL — Atomic-append safety on events.jsonl

Three writers (`/touchpoint`, `/relationships-action`, `/relationships` Step 7) append concurrently. Under POSIX, `O_APPEND` is atomic only for writes ≤ `PIPE_BUF` (4KB). v0.2.2 enforces:
- Each event line capped at 4000 bytes (truncate `notes`, append `[truncated]` marker).
- Single `write()` call per event (not multiple appends).
- Full unredacted summary lives on person page Recent Interactions section; events.jsonl stays atomic.

### Other fixes from review

- **Schema-validation override log → constrained enum reason codes** (was free-form text that captured PII like "Sarah is going through a divorce, downgraded tier"). New codes: `user-override | intentional-mismatch | pending-rebalance | migration-residue`. If reasoning needs preserving, put it in the person page `notes` field where it's covered by local-only privacy posture.
- **Schema-validation override log filename → unique per invocation** (`schema-validation-<brief_id>.md` instead of single file). Avoids concurrent-append race when multiple `/relationships` invocations run in parallel. Nightly roll-up planned for `/end-day`.
- **`/touchpoint` Step 5.0 `mkdir -p <config-root>/relationships/`** before first events.jsonl append. Was silent failure for first-run users.
- **Stale `preferred_channel` (singular) refs cleaned up** in `network-rebalance.md:159` (was `preferred_channel: email`, now `preferred_channels: [email]`) and `draft-touchpoint.md:49,88` (description text + lookup logic). v0.1.2 had migrated to array form; these were stragglers.
- **`network-rebalance.md` description** updated to mention `intent` field (was missing) and the v0.2.2 retired-plugin migration step (added to roadmap).

### Coordinated with cortex v4.12.2

- Cortex `/end-day` Step 4.0 reads daily-brief artifact state and sanitizes annotations before reflection — does NOT quote verbatim from annotations (which may contain raw client content).

### Coordinated with nucleus contracts.md

- New section: events.jsonl unified shape (full v0.2.2 schema documented with backward-compat read rule).

### Findings still deferred

- Migration step in `/setup-relationships` for legacy `weekly-outreach.user-context.md` and `bizdev-outreach.user-context.md` files (auto-copy fields, archive originals) — pending v0.3.
- DASHBOARD provenance retrofit baseline (cortex /cleanup Section L flood handling) — pending cortex v4.13.

---

## 0.2.1 — Schema validation + /touchpoint

Dogfooding-driven hardening on top of v0.2.0. Two additions surfaced during the 2026-05-28 build session:

### Added — schema validation enforcement

The v0.2.0 schema documented (tier × intent) constraints and other compatibility rules, but nothing actually enforced them at runtime. v0.2.1 wires validation into two gates:

- **`/relationships` Step 0 preflight** — walks every `memory/person/*.md`, validates `relationships:` frontmatter, surfaces warning batch (cap 10) before scoring. User can proceed (logged), fix-now (invokes scoped `/network-rebalance`), or show-details.
- **`/network-rebalance` Step 3.5 pre-write** — validates each accepted proposal before writing frontmatter. On failure, inline prompt to demote/shift/override/skip.

**Validation rules** (canonical list in `references/person-page-extensions.md`):
1. (tier × intent) compatibility — active-drive intents require inner/strategic; passive intents require operational/dormant.
2. Required-field presence — tier, intent, buckets, relationship_class, icp_fit must all be present.
3. Enum validity — values must come from documented enum lists.
4. (class × bucket) sanity — personal + new_biz flagged as likely tagging error.
5. (intent × buckets) sanity — passive_visibility + non-network bucket flagged; client_delivery without relationship bucket flagged.

Validation overrides are logged to `<config-root>/memory/staged/skip-logs/schema-validation.md` for audit. Disable per-run with `--no-validate`; disable plugin-wide via `relationships.validate: false` in user-context.

### Added — `/touchpoint` command + skill

Ad-hoc relationship logging from natural language. "I had a great catch-up with Sang, he's connecting me to two folks at NationSwell." Lighter friction than `/relationships-action` for "I just did this and want to capture it" moments that don't come from a brief card.

- **`commands/touchpoint.md`** — 7-step flow: parse touchpoint → detect signal-of-change → write Recent Interactions → optional generosity_ledger entry → append events.jsonl → log → confirm + optional shift prompt.
- **`skills/touchpoint/SKILL.md`** — natural-language entrypoint with phrase patterns and routing for nucleus-router.
- Idempotent against same-day repeats (won't double-log).
- Pattern-shift detection: if touchpoint signals tier/intent shift (e.g., awaiting_reply + reply landing → drive_active), prompt user post-write. Opt-in.
- Same events.jsonl shape as `/relationships-action` — unified action stream regardless of origin.

### Touchpoint vs sibling commands (clarification table)

| Phrase | Command |
|---|---|
| "I had a catch-up with [name]" | `/touchpoint` |
| "Draft a message to [name]" | `/draft-touchpoint` |
| "I sent that to [name]" (during brief review) | `/relationships-action` |
| "Who should I reach out to today" | `/relationships` |
| "Rebalance my network" | `/network-rebalance` |

### Out of scope for v0.2.1

- CRM write-through on `/touchpoint` (some users may want HubSpot last_contact_date updates).
- Auto-detection of touchpoints from `/listen` mining (would propose `/touchpoint` candidates during `/morning` walk).

---

## 0.2.0 — intent dimension + framework clarifications

Major schema refinement informed by the inaugural `/network-rebalance` walk on 2026-05-28. Six framework gaps surfaced from tagging 12 real person pages; this release addresses all six.

### New schema field: `intent` (required for ranking; default by tier)

The `intent` field encodes the **dynamic of engagement** as a dimension orthogonal to (but constrained by) `tier`. Tier captures cadence + drive level; intent captures the texture of HOW you engage.

**Active-drive intents** (paired with inner / strategic tiers):
- `client_delivery` — active client engagement (Tom, Charity, Kim patterns)
- `drive_active` — actively driving a relationship goal
- `door_opening` — connector role; staying useful + visible
- `reciprocal` — mutual referral; match the energy (Jennifer Ives pattern)
- `advising` — asymmetric help with explicit offer (Sang Lee pattern)
- `content_share` — pure-give cadence; no quid pro quo (Rob Buelow post-Vector pattern)

**Passive intents** (paired with operational / dormant tiers):
- `keep_warm` — quiet maintenance (Lauren Little, Caitlyn, Catherine pattern)
- `passive_visibility` — network-bucket only; engage with content, never direct outreach (Jonathan Harms pattern)
- `awaiting_reply` — transient state for just-sent outreach (Lauren Bernstein post-DM pattern)

The brief validates (tier × intent) compatibility — invalid combinations (e.g., strategic + passive_visibility) surface in `/network-rebalance` for reconciliation.

### Intent-driven card framing (`/relationships` Step 4)

The daily brief now adapts the card's framing based on intent:
- `advising` → "[Person] — monthly touch. What's your topic?" (waits for user input, then drafts)
- `passive_visibility` → "Comment on [their recent post]" (never drafts a direct DM)
- `content_share` → "Pure-give — share [tool/framework/practice]"
- All other intents → standard channel + template + draft flow

### Cadence override field

New optional `cadence_days_override: <integer>` lets a person use a custom cadence regardless of tier default. Use case: "strategic by intuition, quarterly by cadence." Scoring engine reads override if set; falls back to tier default if null.

### Follow-up window for awaiting_reply intent

For people with `intent: awaiting_reply`, the standard decay formula is replaced by a follow-up window:
- 0-7 days: 0.0 (give them space)
- 7-21 days: linear ramp to 0.8 (gentle bump pressure)
- 21+ days: 1.0 (clear signal to bump or shift to keep_warm)

Prevents fresh outreach from sitting under the operational 90-day cooling period.

### Internal-team exclusion documented

`/relationships` Step 2 now explicitly scopes the candidate pool to `<config-root>/memory/person/*.md` ONLY. Never `team/`, `client/`, `bizdev/`, `workstream/`. Internal team members in `team/` are not subjects of relationship maintenance — this is enforced at scoping time, not via special-case logic.

### Notes-field principle documented

`references/person-page-extensions.md` now codifies: the `notes` field is about THE RELATIONSHIP (communication style, outreach intent context, origin, framing rules, personal context). Project status (deliverables, WAITING items, engagement specifics) belongs in `client/`, `bizdev/`, or `workstream/` nodes. Includes test ("would the note still matter without this person?") + examples.

### Network-rebalance updates

`/network-rebalance` Step 2 now proposes:
- `intent` based on page context (active client → client_delivery, etc.)
- `cadence_days_override` only when user explicitly indicates non-default cadence
- Validates (tier × intent) combinations and surfaces invalid pairs to the user

### today.json schema additions

`option.person.intent` and `option.person.cadence_days_override` now included in the structured JSON output. Schema version stays at `0.1.0` (additive fields only; no breaking changes for consumers).

### Backward compatibility

- Existing pages without `intent` default by tier: inner/strategic → `drive_active`; operational → `keep_warm`; dormant → `passive_visibility`. Run `/network-rebalance` to set explicit values.
- Existing pages without `cadence_days_override` use tier default (current behavior).

### Not included in v0.2.0 (deferred)

- `team/` node prefix as a formalized cortex v4.12 node type — needs separate cortex PR.
- Generosity-ledger auto-population — not in scope.
- Multi-intent per person (array form) — single intent for v0.2.0; consider array form in v0.3 if patterns warrant.

---

## 0.1.2 — preferred_channels as array

Schema refinement during the first real-world network-rebalance walk. Real people have multi-channel preferences (text + phone for inner-core, email + LinkedIn DM for warm BD); a single `preferred_channel` field forced a false choice.

### Changes

- **`preferred_channel` (single) → `preferred_channels` (array)** on cortex person-page frontmatter under the `relationships:` namespace. Ordered by preference; first entry is the default.
- **Channel-selection logic** (in `/relationships` Step 4 and `references/scoring.md`) updated:
  1. Compute rule-table channel for the trigger.
  2. If rule-table channel ∈ `preferred_channels` → use that match.
  3. Else → use `preferred_channels[0]` (primary preference).
  4. Exception: triggers `cold_icp` and `warm_intro` override preferences (they require specific formats).
  5. Absent/empty → rule-table default.
- **`/network-rebalance`** updated to propose arrays based on observed patterns ("All emails → `[email]`; mixed with notes → `[text, call]`; sparse → omit").
- **JSON schema** (`today-json-schema.md`): option's `person.preferred_channels` is now an array.

### Backward compatibility

v0.1.2 readers accept either shape — a singular `preferred_channel` value is silently coerced to a single-item array. No migration required for existing pages (only just-introduced in v0.1.1; no person pages have it yet outside this session's rebalance).

### Not breaking

Schema version stays at `0.1.0` (no UI consumers yet to break).

---

## 0.1.1 — Hybrid setup + UI-ready structure

Architectural refinement based on review feedback (three independent perspectives — architecture, shareability, operator UX — all converged on the same hybrid). Two themes: stop duplicating peer-plugin data, and make the plugin's outputs structurally UI-ready before any UI exists.

### Hybrid setup — `/setup-relationships` shrinks for Nucleus-stack users

- **New Step 0.5 — peer-plugin import.** Detects and pre-fills from `identity.md`, `voice.md`, `lead-engine.user-context.md`, `core-ops.user-context.md`, `referral-engine.user-context.md`, `bizdev-outreach.user-context.md` (legacy), `weekly-outreach.user-context.md` (legacy), `writing-style.user-context.md`, and cortex workstream nodes. One-time import at setup; not live runtime reads.
- **Step 2 collapses to confirmation + 5 unique questions.** For full-stack users: ~60 seconds. For standalone installs (no peers): full interview with fallback fields written into the user-context.
- **Provenance.** Each imported field tagged with source path + import date in the written user-context.

### user-context.template — slimmed

- **Dropped:** identity, voice descriptors, full CRM properties, full Apollo config, full referral cooling — all live at their canonical peer files at runtime.
- **Kept:** minimal identity for template-variable filling, tier configurations, bucket weights, close-personal track toggle, time budget, network-expansion voice routing, scoring overrides, companion-plugin detection results, standalone-install fallback sections.
- Net file size cut by ~60%; signal-to-noise improved substantially.

### UI-ready structure (for the future web app / Operator desktop / mobile PWA)

- **Stable option IDs.** Format `<bucket>_<person-slug>_<YYYY-MM-DD>` instead of `<bucket>_<date>_<rank>`. Same person on the same day → same ID across re-runs. UIs can correlate "did I act on this?" reliably.
- **`brief_id`.** UUID v4 generated at the start of every `/relationships` run. Included in `today.json` and in every event. Lets a UI correlate events to specific brief generations.
- **`events.jsonl`** — append-only event log at `<config-root>/relationships/events.jsonl`. Written when the user marks a card copied/sent/skipped/snoozed. Canonical action stream for analytics.
- **`snoozes.json`** — persistent snooze state at `<config-root>/relationships/snoozes.json`. Read by `/relationships` Step 3 (filter pool); written by `/relationships-action`.
- **New command `/relationships-action`** — decoupled action endpoint. Takes a JSON event payload (inline or file-based from a UI inbox). Appends to events log, updates cortex person page, updates snoozes. UIs invoke this once per tap.
- **`inbox/` pattern.** UI writes JSON events to `<config-root>/relationships/inbox/<uuid>.json`; sync daemon invokes `/relationships-action --file=<path>`; processed files move to `inbox/processed/`. No HTTP, no IPC — just files on a shared volume.

### New references

- **`references/ui-integration.md`** — full contract for UI builders: how to consume `today.json`, post events to `/relationships-action`, watch `snoozes.json`, handle schema versioning, the sync-daemon pattern, what NOT to do.

### Updated references

- **`references/today-json-schema.md`** — adds `brief_id` field + new stable option-ID format + related-files section pointing at events.jsonl and snoozes.json.

### Updated contracts (in `nucleus/docs/contracts.md`)

- Added rows for `events.jsonl`, `snoozes.json`, `inbox/`.
- Documented peer-import behavior (one-time at setup, not runtime).

### Skills

- Added `relationships-action` natural-language entrypoint (e.g., "I sent that to Sarah" → resolves option → invokes `/relationships-action`).

### What this is NOT

- Not a UI. v0.1.1 is structure for a future UI. The web app / Operator desktop is Phase 6.
- Not a re-architecture. Existing `/relationships` Step 0 → Step 8 flow is intact; this adds writes (events, snoozes) and reads (snoozes at Step 3).
- Not breaking. Schema version stays at `0.1.0` (option ID format change is a UI-internal concern; the contract was added in this release so no consumers exist yet to break).

---

## 0.1.0 — Initial release

First release of the `relationships` plugin — the daily orchestrator for new business development, relationship building, and network expansion. Three-bucket brief, configurable tiers, templates library, channel-aware draft surface, on-demand drafting, and quarterly migration tooling.

### Commands

- **`/setup-relationships`** — 10-section interview that writes `<config-root>/plugins/relationships.user-context.md` (identity, ICP, current quarter focus, tiers + sizes, buckets, voices, time-budget, CRM, Apollo, companion plugins, network expansion sources). Idempotent.
- **`/relationships`** — daily brief command. 8-step orchestrator: preflight → time-budget gate → score-and-rank (per bucket, via `relationship-ranker` subagent) → filter → pick channel + template → draft → present → write artifacts (`today.md` + `today.json`). Optional person-page write-back on user "mark sent."
- **`/network-rebalance`** — Phase 3 critical-path migration command. Walks cortex person pages, proposes additive `relationships:` frontmatter (tier + buckets + relationship_class + icp_fit + preferred_channel), batch-interactive (10-15 per batch). Optional HubSpot back-sync. Idempotent; runnable quarterly.
- **`/draft-touchpoint`** — per-contact on-demand drafting. Resolve contact → gather context → determine intent → pick channel + template → fill variables → "should we even send" filter → present. Drafts only.

### Subagents

- **`relationship-ranker`** — scoring and ranking subagent invoked once per bucket by `/relationships`. Reads cortex + CRM + Gmail + hot cache, computes weighted score per `references/scoring.md`, returns ranked candidates with score breakdowns and concrete "why now" reasons. Web-search capped at 3 per invocation. Read-only.

### Skills (natural-language entrypoints)

- `relationships` — fires on "who should I reach out to today" / "run my daily relationships."
- `setup` — fires on "set up relationships" / "configure my network."
- `network-rebalance` — fires on "rebalance my network" / "audit my tiers."
- `draft-touchpoint` — fires on "draft a message to [name]" / "help me follow up with [name]."

### Templates library

- **17 bundled defaults** across 6 channels (comment / dm / email / text / call / conference). Variable-driven: `{{person.first_name}}`, `{{trigger.context}}`, `{{user.one_liner}}`, etc.
- User overrides supported at `<config-root>/relationships/templates/<channel>/<scenario>.md` (preferred over bundled by filename).
- Frontmatter schema documented in `references/templates/README.md`.

### Reference docs

- **`framework.md`** — Ibarra tier spine + Ferrazzi qualitative layer + reality-layer adjustments for the time-constrained operator.
- **`scoring.md`** — weighted-score math, default weights, factor definitions, channel-selection table.
- **`person-page-extensions.md`** — the `relationships:` YAML frontmatter namespace (locked: frontmatter, not a section). Additive, non-breaking; treated as candidate cortex v4.12.0 schema bump. Other plugins writing person-page state should use their own frontmatter namespace.
- **`today-json-schema.md`** — formal contract for the structured daily-brief output. Schema version `0.1.0`. Used by `today.json` + downstream surfaces (future web app, Operator desktop).
- **`user-context.template.md`** — full schema for the per-user config file.

### Cross-plugin contracts (added to `nucleus/docs/contracts.md`)

- Writes: `<config-root>/plugins/relationships.user-context.md`, `<config-root>/relationships/today.md`, `<config-root>/relationships/today.json`, `<config-root>/relationships/<date>.md`, optional user overrides under `<config-root>/relationships/templates/`.
- Reads: cortex `identity.md`, `voice.md`, `memory/person/*.md`, `memory/hot.md`, `memory/DASHBOARD.md`, `memory/workstream/*.md` (additive read).
- Additively writes: cortex `memory/person/<slug>.md` `## Recent interactions` log (on user "mark sent" or via `/network-rebalance` frontmatter writes).

### Delegates to (when installed)

- **`contact-researcher`** (lead-engine) — per-contact deep dives.
- **`pipeline-analyst`** (core-ops) — pipeline ranking for the new-business bucket.
- **`memory-librarian`** (cortex) — cross-cortex queries.
- **`referral-engine`** — warm-network ask drafting + cooling-period rules.

### Supersedes / replaces (planned, separate Phase 4 PR)

- **`weekly-outreach`** — its weekly-prep role folds into `/relationships`'s daily flow plus a planned `--week` mode. Step 9 person-page side-effect ported.
- **`bizdev-outreach`** — three-phase research-analyze-draft methodology becomes the contract for `/draft-touchpoint` + the templates library. The standalone plugin is deprecated.

### Out of scope for v0.1

- Web app / mobile UI — Phase 6 (separate proposal).
- Conference / event discovery integrations (Eventbrite, Luma, Meetup) — Phase 5.
- LinkedIn posting cadence orchestration — Phase 5.
- LinkedIn-export and iCloud-contacts bulk importers — Phase 5.
- Auto-tiering / auto-generosity-ledger from sent-mail — future.
- Cortex schema bump to v4.12.0 documenting the `relationships:` frontmatter namespace — separate cortex PR.
