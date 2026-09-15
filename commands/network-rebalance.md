---
description: Walk your existing cortex person pages and propose tier + intent + buckets + relationship_class + icp_fit + preferred_channels frontmatter for each. Batch-interactive (10-15 at a time) — you approve, edit, or defer per row. Idempotent; safe to re-run. Run once after /setup-relationships to tag your network, then quarterly to keep tiers honest. v0.2.2+ also migrates legacy weekly-outreach + bizdev-outreach user-context files.
---

# /network-rebalance

The migration + maintenance command that bridges cortex person pages and the `growth` plugin. Without it, every person on every page defaults to `tier: operational`, `buckets: [relationship]`, `icp_fit: none` — which means the daily brief has nothing meaningful to rank.

Designed to be **run twice**:
1. **Once at install** — bulk-propose frontmatter for your existing network.
2. **Quarterly** — re-evaluate. Demote contacts who've gone quiet. Promote contacts who've earned closer cadence. Re-tag ICP as your business focus evolves.

---

## Step 0 — Preflight

Read `<config-root>/plugins/growth.user-context.md`. If missing → route to `/setup-relationships` and stop.

Read `<config-root>/memory/me/identity.md` for the user's name (used in confirmation prose).

Verify cortex is installed: `<config-root>/memory/` directory must exist. If missing → "This command requires cortex installed for person-page data. Install cortex + run /setup-identity first."

Read `<config-root>/memory/index.md` if available — gives you the catalog of person pages without walking every file.

Extract from user-context:
- Tier definitions (sizes, cadences, names if user customized)
- Primary + secondary ICP definitions
- Out-of-ICP exclusions
- Current quarter focus
- Default `relationship_class` for net-new pages (defaults to `business`)
- Close-personal track enabled? (affects how personal contacts are tagged)
- HubSpot tier-property name (if user maps cortex tiers to a CRM property)

---

## Step 0.5 — Retired-plugin user-context migration (v0.2.3+)

Detect legacy plugin user-context files from the retired `weekly-outreach` + `bizdev-outreach` plugins. If present, offer to migrate relevant fields into the active `growth.user-context.md` before walking person pages.

```
legacy_files = [
  <config-root>/plugins/weekly-outreach.user-context.md, <!-- LEGACY_COMPAT -->
  <config-root>/plugins/bizdev-outreach.user-context.md,
]

If any legacy file exists AND was not yet migrated (no `<config-root>/plugins/.relationships-migrated-from-legacy` marker):
  Surface:
    "Detected legacy plugin configs from retired plugins:
       - <list of legacy files that exist>

     These plugins were retired in favor of `relationships`. Their user-context files
     can be migrated — relevant fields (ICP, voice rules, banned phrases, CRM
     mappings, cadence definitions) get copied into your growth.user-context.md
     where they're still consulted. Original files preserved at
     <config-root>/plugins/archive/<original-name>.<today>.md (renamed, not deleted).

     Migrate now? (y/n/show-diff)"

  On show-diff: render a per-file summary of which fields would be copied where, then re-prompt.
  On y:
    For each legacy file:
      Parse known sections (ICP, Voice, CRM, Cadence, Banned phrases, Value-adds, etc.)
      For each field, compare against current growth.user-context.md:
        - If relationships.user-context lacks the field → copy it over (with provenance: <!-- migrated-from: <legacy-file> @ <today> -->).
        - If relationships.user-context already has the field with the SAME value → skip silently.
        - If relationships.user-context has a DIFFERENT value → surface a per-field reconciliation prompt: "[Field name] differs:
           legacy: <legacy-value>
           current: <current-value>
           keep-current / use-legacy / show-context / merge-manually"
      After all fields handled, mv <legacy-file> <config-root>/plugins/archive/<original-name>.<today>.md
    Write <config-root>/plugins/.relationships-migrated-from-legacy with timestamp + list of files migrated.
    Surface count: "Migrated <N> fields from <M> legacy files. Originals archived to <config-root>/plugins/archive/."
  On n:
    Surface: "Migration skipped. Re-run /network-rebalance later to migrate, or run /setup-relationships --refresh-imports for the same effect. The legacy files will not be read again unless explicitly requested."
    Write skip-marker so this prompt doesn't re-fire on every /network-rebalance run.
```

This migration is idempotent. The skip-marker prevents prompt-fatigue; re-running with `--migrate-legacy` flag forces a re-check.

---

## Step 1 — Scope selection

Ask the user:

> "Rebalance — which scope?
> (a) **All person pages** (full audit, recommended on first run)
> (b) **Untagged only** (person pages without `relationships:` frontmatter yet)
> (c) **Stale tags only** (pages with frontmatter older than 90 days)
> (d) **Specific tier** (e.g., 'just my inner core')
> (e) **Specific workstream** (people linked to one cortex workstream node)"

Default: **untagged only** (least invasive).

Apply the scope filter. Enumerate the candidate pages. If the count is > 100, warn the user and ask whether to proceed (large rebalance is heavy work).

---

## Step 2 — Per-page proposal generation (read-only)

For each candidate page:

1. **Read the existing person page.** Capture: name, title, company, temperature, last meaningful contact, recent interactions, linked entities, existing notes, mention frequency.
2. **Read existing `relationships:` frontmatter** if present (this is a re-tag, not a first-tag).
3. **Cross-reference HubSpot** (if connected): pull the contact record, lifecycle stage, owner, tier-property value, deal associations.
4. **Cross-reference workstream nodes:** check `<config-root>/memory/workstream/*.md` for links to this person.

Then **propose** values for each field:

### `tier` proposal

Default rule chain (apply in order, first match wins):
- If existing frontmatter `tier` exists and the user picked scope (a) "full audit": surface the existing value as the proposal but flag it for re-evaluation.
- If person has linked workstream + recent interactions in last 30d → `tier: strategic` baseline; bump to `inner` if recent interactions ≥ 5 in 30d.
- If person is the **primary contact for an active client workstream** → `tier: strategic` minimum.
- If `temperature: Active` AND interactions ≥ 4 in last 60d → `tier: strategic`.
- If `temperature: Warm` AND interactions ≥ 2 in last 90d → `tier: operational`.
- If `temperature: Dormant` OR no interactions in 180d → `tier: dormant`.
- Default → `tier: operational`.

Honor user-context tier-size targets. If proposing `tier: inner` would push the inner-core count above the user's stated max (default 15), surface that to the user during review: "This would bring inner-core to 17 (target 15) — promote anyway, demote someone else, or downgrade to strategic?"

### `buckets` proposal

- If person has active deal in CRM OR is in the primary ICP definition → include `new_biz`.
- If person has any business-relationship signal (past meetings, ongoing work, mentor/peer linkage) → include `relationship`.
- If person is in the user's named network-expansion engagement set OR posts frequently in the user's space → include `network`.
- Most contacts get 1-2 buckets. Very few get all 3.
- If no signals → default `[relationship]`.

### `relationship_class` proposal

- If linked entities include only client/workstream/bizdev nodes → `business`.
- If linked entities include personal nodes OR the user's identity flagged them as family/close-friend → `personal`.
- If ambiguous → propose `business` and flag for user review.

### `icp_fit` proposal

- Match title + company against user-context **primary ICP** definition → `primary`.
- Match against **secondary** → `secondary`.
- Match against **out-of-ICP exclusions** → `none` (with note "explicitly out-of-ICP").
- No match → `none`.

### `next_touch_target` proposal

Computed deterministically: `last_meaningful_contact_date + tier_cadence_days`. Not user-edited during rebalance — derived field. If `last_meaningful_contact` is missing on the page, set to `today` (so the contact starts the clock fresh, doesn't immediately surface as overdue).

### `intent` proposal (v0.2.0+)

Propose intent based on the page's existing context + the (tier, intent) compatibility rules in `references/person-page-extensions.md`:

- Active client engagement → `client_delivery`
- Active deal pursuit → `drive_active`
- Connector with active door-opening → `door_opening`
- Mutual referral peer → `reciprocal`
- Explicit advisor with help offer → `advising`
- Pure-give cadence (closed-lost-but-stay-warm) → `content_share`
- Quiet maintenance, no active goal → `keep_warm`
- Network-only / never-direct-outreach → `passive_visibility`
- Just-sent-outreach, awaiting reply → `awaiting_reply`

Validate (tier × intent) compatibility:
- Inner / strategic tier expects active-drive intents
- Operational / dormant tier expects passive intents
- If proposed combination is invalid, surface to user during review batch: "Tier:strategic + intent:keep_warm is contradictory. Demote tier to operational or shift intent to drive_active?"

### `cadence_days_override` proposal (v0.2.0+)

Default: null (use tier default). Propose a custom value only when the user has explicitly indicated a non-default cadence preference during the walk (e.g., "she's strategic but I only need quarterly").

### `preferred_channels` proposal (array, v0.1.2+)

Propose an ordered array based on observed patterns:
- All recent interactions are LinkedIn DM → propose `[linkedin_dm]`.
- All recent interactions are email → propose `[email]`.
- All recent interactions are calls → propose `[call]`.
- Mixed pattern with clear primary + secondary (e.g., page Notes say "text usually; phone for big news") → propose `[text, call]`.
- Sparse or no clear pattern → omit (let the daily brief decide per-action).

Surface the proposal in plain language during the review batch: "Tom: preferred_channels: [text, call] — text default; phone for substantive."

### `generosity_ledger`

Not auto-populated. Empty ledger on first tag. (Future: a `/log-give` command will append entries.)

---

## Step 3 — Batch-interactive review

Present batches of **10-15 candidates at a time**. Format for fast scanning:

```
REBALANCE BATCH 1 of N

────────────────────────────────────────────────────────
1. Sarah Chen — Head of Content, Vantage Health
   Existing: temp=Active, last contact 2026-05-12 (email), interactions=4/30d
   Linked: [[workstream/studio-icp-pipeline]], [[client/acme-corp]]

   PROPOSED FRONTMATTER:
     tier: strategic              [reason: workstream link + 4 interactions in 30d]
     buckets: [new_biz, relationship]
     relationship_class: business
     icp_fit: primary             [reason: matches "Heads of Content at mid-market EdTech"]
     preferred_channels: [email]
     next_touch_target: 2026-06-11 (auto-computed)

   [ accept ] [ edit ] [ skip ] [ defer ] [ archive page ]
   Notes: ___________________________

────────────────────────────────────────────────────────
2. Sam Patel — VP Production, Acme Corp
   ...
────────────────────────────────────────────────────────
```

For each row, the user can:

- **accept** — write the proposed frontmatter to the page
- **edit** — open a free-form edit prompt: "What would you change?" — user types, you re-propose with their change
- **skip** — leave the page untouched this run; surface again next rebalance
- **defer** — explicitly defer (no resurface for 90 days; stored in `<config-root>/memory/staged/skip-logs/rebalance.md`)
- **archive page** — fold to cortex's `/forget` flow (rebalance is a natural moment to retire dormant pages)

Batch responses can be shorthand:
- `"1: accept, 2: skip, 3: edit (downgrade to operational), 4-10: accept all"` — parse and apply.
- `"accept all"` — apply proposals as-is to the whole batch.

After each batch, summarize: "Batch 1 complete — N accepted, M skipped, K edited, J deferred, L archived. Continuing to Batch 2..."

---

## Step 3.5 — Schema validation pre-write (v0.2.1+)

Before writing accepted proposals, validate each one against the schema rules in `references/person-page-extensions.md`:

1. **(tier × intent) compatibility** — see `/relationships` schema validation preflight for the rules.
2. **Required-field presence** — every accepted proposal must include all required fields.
3. **Enum validity** — values come from documented enum lists.
4. **(class × bucket) sanity** — flag personal + new_biz, etc.
5. **(intent × buckets) sanity** — passive_visibility + non-network bucket = warn; client_delivery without relationship bucket = warn.

If any accepted proposal fails validation, surface inline before the write:

```
⚠ Proposal validation failed for [name]:
  Rule: (tier × intent) compatibility
  Conflict: tier=strategic + intent=keep_warm
  Options:
    (1) Demote tier to operational
    (2) Shift intent to drive_active or door_opening
    (3) Override anyway (logged to schema-validation.md)
    (4) Skip — don't write this page

  Choose: 1 / 2 / 3 / 4
```

If override is chosen, log to `<config-root>/memory/staged/skip-logs/schema-validation.md` with `(slug, rule-violated, override-rationale)` for audit.

This catches the case where the user accepts proposals quickly in batch and a compatibility issue slips through. Fail-loud, fix-now.

---

## Step 4 — Frontmatter writing

For each accepted proposal:

1. **Read the existing page file** (`<config-root>/memory/person/<slug>.md`).
2. **Check for existing frontmatter:**
   - If the file starts with `---` → parse existing frontmatter, merge the `relationships:` namespace (overwriting only that namespace, preserving any other namespaces other plugins might use).
   - If no frontmatter exists → prepend a new frontmatter block with just the `relationships:` namespace.
3. **Preserve the body content verbatim.** Never touch sections below the frontmatter.
4. **Write the page back.**

### Edge case — page is currently open by another tool

If you detect a `.swp` or lockfile, skip with a warning. The user can re-run after closing their editor.

### Edge case — name collision detected

If two pages would slug to the same name (per cortex v4.10 wikilink convention), pause: "Two pages slug to `sarah-chen` — `sarah-chen.md` (Vantage Health) and `sarah-chen-acme.md` (Acme). Continue tagging both separately?" Yes proceeds; no skips both.

---

## Step 5 — HubSpot back-sync (optional)

After all approved frontmatter writes complete, ask:

> "You have a HubSpot tier-property mapped (`<property_name>` per user-context). Want me to back-sync the cortex tiers to HubSpot so they stay aligned? [Y/N]"

If Y:
1. Build a confirmation table: HubSpot Contact ID, Name, Old Tier Value, New Tier Value.
2. Wait for explicit approval.
3. Batch-update HubSpot in chunks of 10.
4. Report successes and failures.

If N: skip silently. Cortex stays the source of truth.

If user-context doesn't define a HubSpot tier-property mapping: skip this step entirely.

---

## Step 6 — Refresh derived state

- **Re-index cortex.** If `cortex` `indexer` skill is available, fire `/reindex` (or write `.reindex-queue` marker per the cortex contract).
- **Update DASHBOARD.md** active-people section to reflect new tiers (cortex `/remember` Step 3 handles this on next run; trigger it if available).
- **Update hot.md.** Tier changes might bring previously-quiet contacts into the rolling 7d cache. Cortex `/listen` handles this on next nightly run; no action here.

---

## Step 7 — Summary + log

Final summary:

```
NETWORK REBALANCE — 2026-05-28

Scope: untagged only
Pages processed: 47
  Accepted: 38
  Edited: 5
  Skipped: 3
  Deferred: 1
  Archived: 0

Tier distribution (post-rebalance):
  inner:        12  (target: 10-15)  ✓
  strategic:    34  (target: 30-50)  ✓
  operational: 121  (target: 100-200) ✓
  dormant:     247

ICP distribution:
  primary:      18
  secondary:    32
  none:        364

HubSpot back-sync: skipped (no mapping in user-context)

Next steps:
- Run /relationships to get your first tagged daily brief.
- Re-run /network-rebalance quarterly (~90 days).
```

Log to `<config-root>/memory/log.md` via cortex `log-writer` skill:

```
## [YYYY-MM-DD HH:MM] /network-rebalance | N pages reviewed, M tagged, K archived
```

---

## Behavior rules

- **Idempotent.** Re-running is safe. Pages with up-to-date frontmatter are skipped from the proposal queue (unless scope = "all" or "stale").
- **Additive only.** Never delete or modify body content of person pages. Only touch the `relationships:` namespace inside frontmatter.
- **Respects existing namespaces.** If a page has frontmatter from other plugins (e.g., `referral_engine:`), preserve it verbatim.
- **Reversible.** All changes are markdown frontmatter — easily diffed and reverted via git if the user has memory-as-git enabled (cortex proposal).
- **Honor the autonomy slider.** In `auto` mode, accept all high-confidence proposals automatically; pause only for `medium`/`low` confidence rows. In `confirm` mode, walk every row.
- **No CRM writes by default.** Back-sync is opt-in per run.
- **No drafting.** This command tags. The daily brief drafts.
- **Surfaces tier-size overflow gracefully.** If a proposal would push inner-core over target, prompt for trade-off ("promote anyway / pick someone to demote / downgrade this proposal").

---

## Future-state additions (not in v0.1)

- **LinkedIn-export importer.** Stage a CSV of LinkedIn connections; rebalance creates net-new person pages with proposed tagging.
- **iCloud contacts importer.** Same shape, drives the close-personal track.
- **Decay-based auto-demotion suggestions.** Pages with no interaction in 6+ months get auto-flagged for demotion in the next rebalance.
- **Generosity-ledger import.** Parse Gmail's "Sent" folder for outbound value (intros sent, shares, congrats) and seed the ledger.

These come in Phase 5+. The v0.1 command works on existing cortex person pages and CRM data only.
