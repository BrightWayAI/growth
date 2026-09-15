# Person-page extensions

The `relationships` plugin extends cortex person pages (`<config-root>/memory/person/<slug>.md`) with additive fields that drive tier-based prioritization and bucket eligibility. **Existing person pages remain valid** — untagged people fall back to sensible defaults.

## The new fields

```yaml
relationships:
  tier: inner | strategic | operational | dormant
  intent: client_delivery | drive_active | door_opening | reciprocal | advising | content_share | keep_warm | passive_visibility | awaiting_reply
  buckets: [new_biz, relationship, network]
  relationship_class: business | personal
  icp_fit: primary | secondary | none
  next_touch_target: YYYY-MM-DD
  cadence_days_override: null | <integer>   # optional; overrides tier default cadence for this person
  preferred_channels: [text, call]          # ordered by preference; first is the default
  generosity_ledger:
    - date: YYYY-MM-DD
      direction: gave | received
      note: "short string"
  notes:
    - "free-form, optional — see notes-field principle below"
```

## Field reference

### `tier` (required for ranking; default `operational`)

Drives cadence. Tier targets are configurable per user in `growth.user-context.md`. Default targets:

| Tier | Default cadence |
|---|---|
| `inner` | 14 days |
| `strategic` | 30 days |
| `operational` | 90 days |
| `dormant` | trigger-only — never proactively surfaced |

### `buckets` (required for eligibility; default `[relationship]`)

Which daily-brief buckets this person is eligible for. Most people are eligible for one or two; very few belong in all three.

- `new_biz` — appears in the New Business Development bucket. Use for ICP-fit prospects and active-deal contacts.
- `relationship` — appears in the Relationship Building bucket. Use for inner-core, strategic, and operational contacts you maintain.
- `network` — appears in the Network Expansion bucket. Use for people whose content you actively engage with, conference cohort, etc.

### `relationship_class` (default `business`)

Drives channel and voice selection. `personal` people use the personal voice (if defined) and channel defaults skew to text/Instagram DM/phone call. Surfaced in a separate sub-tab if the user enabled the close-personal track in setup.

### `icp_fit` (default `none`)

For new-business weighting. `primary` matches the user-context primary ICP definition; `secondary` matches secondary; `none` is out-of-ICP for this user's current focus. Recompute as ICP evolves.

### `intent` (required for ranking; default by tier)

Specifies the **dynamic of how you engage** with this person. Distinct from tier (cadence + drive level) — intent encodes the texture of engagement within that cadence.

**Active-drive intents** (compatible with inner / strategic tiers):
- `client_delivery` — active client engagement; cadence is delivery-driven (Marcus, Priya, Renee)
- `drive_active` — actively driving a relationship goal (deal, deepening, specific ask in flight)
- `door_opening` — they connect you to other people; cadence is about staying useful + visible
- `reciprocal` — mutual referral / match the energy (Jordan Cole)
- `advising` — asymmetric help; they've offered counsel and you should use it intentionally (Taylor Diaz)
- `content_share` — pure-give cadence; share tools/practices/frameworks with no quid pro quo (Alex Rivera post-Nova)

**Passive intents** (compatible with operational / dormant tiers):
- `keep_warm` — quiet maintenance; surface only on triggers (Casey Little, Dana, Elena)
- `passive_visibility` — `[network]`-bucket only; engage with their content, never direct outreach (Chris Harms)
- `awaiting_reply` — just sent outreach; waiting on response. Transient state — re-tier and re-intent once reply lands or window closes.

**Constraint:** not every (tier × intent) combination is valid. Strategic + passive_visibility is a contradiction. The daily brief and `/network-rebalance` validate combinations and prompt the user to reconcile if invalid.

**Dynamic:** intent shifts as the relationship evolves. Lauren Bernstein could move `awaiting_reply` → `drive_active` if a real conversation develops, or back to `keep_warm` if she goes quiet. Re-evaluate intent at every `/network-rebalance`; the daily brief should also propose shifts when patterns indicate.

### `cadence_days_override` (optional, default null)

Overrides the tier's default cadence in days for this specific person. Use when a person fits a tier conceptually but wants a different cadence than the tier default.

Example: Casey Little is operational by intuition (no active pursuit) but you want to touch base every 60 days instead of the 90-day default. Set `cadence_days_override: 60`.

Leave null for the tier default. Most people won't have this set.

### `next_touch_target` (auto-computed)

Date the cadence next becomes due. Computed as `last_meaningful_contact + (cadence_days_override or tier_cadence_days)`. Used by the scoring engine to compute the decay factor. **Auto-maintained** by `/relationships` and `/network-rebalance`; users rarely set manually.

### `preferred_channels` (optional, array; v0.1.2+)

Ordered list of channels the person prefers, most-preferred first. Real people have multi-channel preferences ("text for quick, call for substantive"; "email + LinkedIn DM both work"). The daily brief's channel-selection rules honor this list:

- If the rule-table channel for a trigger matches anything in `preferred_channels` → use that match.
- Otherwise, fall back to `preferred_channels[0]` (the primary).
- If `preferred_channels` is empty or absent → use the rule-table default for the trigger.

Valid values: `email | linkedin_dm | instagram_dm | text | call | comment | conference_dm | none`. Use `none` (alone) to explicitly disable channel-preference override.

Example: `[text, call]` means "text by default; phone for triggers that suggest a call (substantive news, big decisions); never my preferred channel for cold/research-thin cards (those use the rule-table channel)."

**Migration from v0.1.1 `preferred_channel` (singular):** the array form supersedes the single-value field. v0.1.2 readers gracefully accept either shape (single-value becomes a single-item array). The schema document and templates use the array form going forward.

### `generosity_ledger` (optional)

Log of value exchange. Each entry: `date`, `direction` (gave or received), one-line `note`. Used by the reciprocity scoring factor — if you owe them, it weights them up; if they recently owe you, it weights them down (they should reach out next).

Keep this short — the last 5-10 entries are enough. Don't journal every micro-interaction.

### `notes` (optional)

**Notes-field principle (v0.1.3+):** the `notes` array is about THE RELATIONSHIP — communication style, outreach intent context, origin (who introduced), mentor/connector role, personal context affecting cadence, framing rules.

**Notes are NOT for project status.** Outstanding deliverables, WAITING items on specific work, engagement specifics ($X deal, M1 doc drafted, sign-off pending) belong in `client/`, `bizdev/`, or `workstream/` nodes — not on the person's relationships frontmatter.

A test: if removing the person from your network entirely would make the note obsolete → it belongs here. If the note would still matter (because it describes a deliverable, a deadline, a deal stage) → it belongs in the project node.

Examples that belong here:
- "Long-time personal friend AND explicit advisor. Has stated he wants to help."
- "Style: warm, casual, short. -Jane sign-off."
- "Pattern: commits to intros and doesn't follow through. Drive next steps directly."
- "Origin: Taylor Diaz intro Aug 2025."
- "Don't position her as a go-between for the Morgan relationship."

Examples that DON'T belong here (move to client/bizdev node):
- "Architecture doc M1 drafted — WAITING:Renee sign-off"
- "$9K engagement, 25–30 hrs"
- "Bright Futures Inc subcontract opportunity surfaced 5/18"

---

## Where the fields live — YAML frontmatter

**Decision locked (2026-05-28):** the new fields live in YAML frontmatter at the top of the person-page file, between `---` delimiters.

```markdown
---
relationships:
  tier: strategic
  buckets: [new_biz, relationship]
  relationship_class: business
  icp_fit: primary
  next_touch_target: 2026-06-10
  preferred_channels: [linkedin_dm]
  generosity_ledger:
    - date: 2026-05-12
      direction: gave
      note: "intro to Sarah at Vantage Health"
    - date: 2026-04-28
      direction: gave
      note: "shared their LinkedIn post"
---

# person:sarah-chen
[rest of the page unchanged — narrative sections continue as before]
```

### Why frontmatter

- Machine-readable. The indexer, `memory-librarian`, and a future web-app / Operator desktop can parse the fields without bullet-list ambiguity.
- Additive and non-breaking. Existing pages without frontmatter remain valid; the plugin treats missing frontmatter as `tier: operational`, `relationship_class: business`, `icp_fit: none`, empty buckets default to `[relationship]`.
- Aligns with Obsidian's native frontmatter handling — cortex pages opened in Obsidian show frontmatter fields as properties in the UI.

### Cortex coordination

This is a small cortex schema additive (no breaking change — frontmatter is purely additive on top of existing person pages). Treated as a **minor** cortex version bump (v4.12.0 candidate) that:

1. Documents `relationships:` as a recognized frontmatter namespace under the person-page schema in `cortex/CLAUDE.md`.
2. Updates the cortex `indexer` skill to surface the new fields in `memory/index.md` entries (tier label, ICP-fit chip).
3. Adds a graceful no-op for pages without the frontmatter — same as today's behavior.
4. Does NOT migrate existing pages automatically. Migration is opt-in via `/network-rebalance` (this plugin's Phase 3 command).

If cortex maintainers prefer a separate frontmatter namespace pattern (e.g., one block per plugin) rather than `relationships:` at the root, this plugin will follow that. Until then, `relationships:` is the canonical namespace.

### Future plugins reusing the pattern

Other plugins that need to write structured data to person pages should use their own frontmatter namespace (e.g., `referral_engine:`, `weekly_outreach:`). This avoids collisions and keeps each plugin's writes scoped.

---

## Migration

`/network-rebalance` (Phase 3) walks every person page and proposes `tier`, `buckets`, `relationship_class`, and `icp_fit` based on:

- `temperature` field (Cold/Warm/Active/Dormant from cortex v4.2 person-page schema) → seed for `tier`
- `Linked entities` → projects + workstreams → seed for `buckets`
- Mention count + interaction recency → seed for `tier` adjustment
- User-context ICP definition → match to seed `icp_fit`

User approves in batches (10-15 at a time). Idempotent — re-runnable.

---

## Reads + writes

| Source | Reads which fields | Writes which fields |
|---|---|---|
| `/relationships` (this plugin) | all | `next_touch_target` (auto-maintained), `generosity_ledger` (when user logs giving), `## Recent interactions` append |
| `/network-rebalance` (this plugin, Phase 3) | all | `tier`, `buckets`, `relationship_class`, `icp_fit` (proposed; user-approved) |
| `relationships-director` (mode: research, bundled agent) | reads only | does not write these fields |
| `/draft-touchpoint` (referral-ask) | `tier`, `relationship_class`, `generosity_ledger` | may append to `generosity_ledger` on ask draft |
| cortex `/recall` | all (renders the section) | none |
| cortex `/cleanup` | `tier` (uses for archive triggers) | may demote `tier` to `dormant` on inactivity |

---

## Out of scope for v0.1

- Auto-tiering — for now `tier` is user-set (via `/network-rebalance`). Auto-tiering by mention frequency + interaction recency is a Phase 5+ idea.
- ICP fit auto-detection from CRM custom fields — Phase 3 will read CRM tier/ICP properties and propose, but won't blindly sync.
- Generosity-ledger auto-logging from sent messages — out of scope until we have outbound logging.
