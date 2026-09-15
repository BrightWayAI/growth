---
description: Configure the relationships plugin. Auto-imports identity, voice, CRM, and banned phrases from peer plugin configs when they exist. ICP/Apollo/signal preferences and referral-connector/cooling rules are captured natively (absorbed from the retired lead-engine and referral-engine plugins, 2026-09-15) rather than imported. For full-stack Nucleus users this collapses to a handful of confirmations plus the native questions; standalone installs run the full interview. Writes results to <config-root>/plugins/relationships.user-context.md. Re-run anytime to update.
---

# /setup-relationships

Configure the plugin. The interview length depends on what's already in your `<config-root>/`:

- **Full Nucleus stack** (cortex + core-ops installed): ~2–3 minutes. Identity/voice/CRM pre-filled from peers; ICP, Apollo, and referral-cooling questions are native to this plugin (absorbed from lead-engine and referral-engine, which retired into this plugin 2026-09-15).
- **Standalone install**: ~10–12 minutes. Full interview, including the native ICP/Apollo/referral questions.

Idempotent — re-running updates rather than restarts.

---

## Step 0 — Resolve plugin config root

Per-plugin config in this marketplace lives under a user-chosen folder, recorded at `~/Documents/.claude-plugin-config-root` (single-line text file in the user's home).

### A — Try the pointer

Ensure access to `~/Documents`. In Cowork, call `request_cowork_directory(~/Documents)` once if not already granted. In Claude Code (or any environment with direct filesystem access), no mount is needed. Then read `~/Documents/.claude-plugin-config-root`.

- **Exists:** read line 1 → that's the config root path. Ensure access to `<config-root>`. If running in Cowork and the folder isn't already mounted in this session, call `request_cowork_directory(<config-root>)`. If running in Claude Code or another environment with direct filesystem access, no mount call is needed. Skip to section C.
- **Missing:** continue to section B.

### B — First-time bootstrap

Prompt: "First-time plugin setup. Where should I store your plugin config — identity, voice, and per-plugin settings? Pick a folder you control (e.g., `~/Documents/Claude/` or `~/Documents/PluginConfig/`). The folder will hold `identity.md`, `voice.md`, and a `plugins/` subdirectory."

Then:
1. Ensure access to `<path>`. If running in Cowork and the folder isn't already mounted, call `request_cowork_directory(<path>)`. In Claude Code, no mount call needed.
2. Create `<path>/plugins/`. Write absolute path to `~/Documents/.claude-plugin-config-root`.

### C — Note resolved root

For the rest of this document, **`<config-root>`** refers to the resolved path. This plugin's config file lives at **`<config-root>/plugins/relationships.user-context.md`**.

---

## Step 0.5 — Peer-plugin import (the heavy lifting)

Before asking the user anything, scan for peer-plugin configs and pre-fill what's there. **Read-only one-time import** — once values land in `relationships.user-context.md`, this plugin does not re-read peer files at runtime. (Re-running setup re-imports.)

Build an internal "detected" dictionary. For each source, read defensively — if a section is missing or renamed, log a `Notes:` entry and skip silently. Do not fabricate values.

### Identity

Source: `<config-root>/memory/me/identity.md` (cortex `/setup-identity`).
Extract:
- Name → `identity.name`
- Company → `identity.company`
- One-sentence description (look for "what we do" / "positioning" / "we do" patterns) → `identity.one_liner`

Fallback: extract from `<config-root>/plugins/bizdev-outreach.user-context.md` `## Company` section if present (legacy migration path).

### Voice — primary

Source: `<config-root>/memory/me/voice.md` (cortex `/setup-voice`) and `<config-root>/plugins/voice.user-context.md` if installed.
Extract:
- Three-word descriptors (e.g., "calibrated, practitioner, honest")
- Sign-off style
- Banned phrases (the cortex defaults are well-known; capture user-added ones)

### Voice — additional named voices (legacy)

Source: `<config-root>/plugins/bizdev-outreach.user-context.md` `## Banned phrases (custom)` and `## Casual email register`.

If the legacy bizdev-outreach file has voice-specific overrides (banned phrases, casual register), capture as a `business` voice block in addition to the primary voice. Note: the user can rename or split this in the confirmation step.

### ICP (primary + secondary + out-of-ICP) — native as of 2026-09-15

This used to import from a separate `lead-engine` plugin; lead-engine retired into `relationships` and its ICP capture is now a native question in Step 2 (see "ICP & signal sourcing" below). For an existing install migrating from lead-engine, check for a legacy `<config-root>/plugins/lead-engine.user-context.md` `## ICP` section once and offer to carry it forward verbatim instead of re-asking. Also check the older legacy sources if lead-engine's file isn't present: `<config-root>/plugins/weekly-outreach.user-context.md` `## ICP` section, or `<config-root>/plugins/bizdev-outreach.user-context.md` `## Company / Target market` block.

### Current quarter focus + outcome target

Source priority order:
1. `<config-root>/memory/workstream/*.md` — scan for active workstream nodes whose status indicates current-quarter priority. Cortex workstream nodes are the canonical place for this; if one named "q3-outbound" or similar is active, capture its focus.
2. `<config-root>/user.md` — check for any `## Quarterly focus` or `## Quarter target` sections.

If neither yields a result, ask in the confirmation step.

### CRM properties

Source: `<config-root>/plugins/core-ops.user-context.md` (preferred) or `<config-root>/plugins/weekly-outreach.user-context.md` `## CRM` section (legacy).
Extract:
- Tool (HubSpot / Salesforce / Pipedrive / Attio)
- Owner ID
- Pipeline stages
- Custom property names (cadence_property, icp_fit_property, do_not_engage_property)
- API tier notes if present (e.g., "Starter — no Sequences API")

### Apollo + signal preferences — native as of 2026-09-15

Captured natively in Step 2 (see "ICP & signal sourcing" below), not imported. For an existing install migrating from lead-engine, check for `<config-root>/plugins/lead-engine.user-context.md`'s Apollo settings (or the older `<config-root>/plugins/weekly-outreach.user-context.md` `## Apollo` section) once and offer to carry them forward instead of re-asking:
- Enabled? (Y/N)
- Daily DM budget, weekly net-new cap
- Signal priorities (job changes, funding, posts)

### Referral cooling + connector taxonomy — native as of 2026-09-15

Captured natively in Step 2 (see "Referral network" below), not imported. For an existing install migrating from referral-engine, check for `<config-root>/plugins/referral-engine.user-context.md` once and offer to carry it forward:
- Connector taxonomy (relationship_type values that count as connector, lists, tags)
- Quiet threshold (default 60 days)
- Trigger patterns (positive moments, fiscal-year, seasonal, conference proximity)
- Ask cadence cap (default 180 days)

### Companion plugin detection

Runtime-detect, do not ask:
- `cortex`: `<config-root>/memory/` directory exists
- `core-ops`: `<config-root>/plugins/core-ops.user-context.md` exists
- `daily-brief`: `<config-root>/plugins/daily-brief.user-context.md` exists
- `voice`: `<config-root>/plugins/voice.user-context.md` exists

Mark each as installed/not. Used to decide whether to delegate to subagents like `pipeline-analyst`. (`relationships-director`, mode: research, is bundled with this plugin as of 2026-09-15 — no longer a companion-detection case.)

---

## Step 1 — Check for existing relationships config

Read `<config-root>/plugins/relationships.user-context.md`.

- **Populated:** ask whether to (a) merge peer-import updates into existing file, (b) update specific sections only, (c) start over. Default: (a) merge — least destructive.
- **Missing:** start fresh from the peer-import dictionary.

---

## Step 2 — Confirmation interview

For full-stack Nucleus users, this is mostly "here's what I detected, confirm or correct." For standalone users, this is the full interview.

Present the detected dictionary as a summary first:

```
Detected from your existing config:
  Identity:           [name] · [company] · [one-liner]
  Primary voice:      [three words] · [sign-off]
  CRM:                [tool] · [N custom properties]
  Companions:         cortex ✓ · core-ops ✓ · daily-brief ✓ · voice ✓ · ...

Look right? (y / fix / replay specific section)
```

If the user says "fix" or names a section, walk that section in detail. Otherwise accept the detected values and move on.

ICP, Apollo/signal preferences, and referral cooling rules are asked natively below — they're not part of the detected-peer summary since they no longer come from a separate plugin (see "ICP & signal sourcing" and "Referral network" below).

### Then ask the relationships-unique questions (these are NOT in any peer file)

One at a time, confirm before moving on. **Surface the default; ask only if user wants to override.**

**Q1 — Close personal track?**
- Most operators run business-only. Do you want a separate `Close personal` track in the daily brief? (family + closest friends, surfaced on its own tab so personal doesn't compete with biz)
- Default: **No**.
- If yes: how many people, what cadence (default 30 days).

**Q2 — Tier sizes (override defaults?)**
- Defaults: Inner Core 10–15 (biweekly cadence) · Strategic 30–50 (monthly) · Operational 100–200 (quarterly) · Dormant rest (trigger-only).
- Surface them, ask: any tier you want to override?
- If yes: which tier, what size, what cadence.

**Q3 — Time budget**
- Most operators run with a consistent daily window. What's your typical availability for relationship work? (5 / 15 / 30 / 60+ min — pick the most common)
- Default: **30 minutes**.
- Variable? If yes: enable the time-budget prompt at the top of every `/relationships` invocation.

**Q4 — Network expansion voices**
- The daily brief's network-expansion bucket suggests content posting prompts. Do you have multiple LinkedIn voices (e.g., personal brand + business page)?
- Default: **One voice** (primary).
- If multiple: name each voice and what surface it posts to.

**Q5 — Bucket emphasis (advanced; default equal)**
- Default: equal weight across new-biz / relationship / network-expansion buckets.
- Want to override? (e.g., prospecting-heavy = 1.5 new-biz, 0.8 others)
- Most users say no. Skip unless they bring it up.

**Q6 — ICP & signal sourcing (native, absorbed from lead-engine 2026-09-15)**

If a legacy lead-engine ICP was detected (see Step 0.5 note above), present it and ask to confirm/edit rather than re-asking from scratch. Otherwise ask:

1. **Target roles** — "Who's the buyer/champion you usually message? List 1-4 titles."
2. **Industries** — "What industries/verticals? Or 'horizontal' if you sell across all."
3. **Company size** — "Sweet-spot company size? (Headcount or revenue range.)"
4. **Disqualifiers** — "Anything that auto-disqualifies a lead even if other signals look strong?"
5. **Signal priorities** (multiSelect) — "Which of the 7 buying signals are highest priority for your ICP?" Choices: Engagement, Job change, Funding, Hiring, Growth/expansion, Tech-stack change, Direct intent. See `references/seven-signals.md` for the full taxonomy each signal maps to.
6. **Custom signal** (optional) — anything not on that list that's a buying signal in this domain.
7. **Apollo** — if the Apollo MCP is connected: "Default to (a) job changes only, (b) job changes + funding, or (c) all three?" Also capture: daily DM send budget (default 10-15) and follow-up cadence (3-7-14 / 5-10 / 7-14 / custom — see `/draft-signal` for how these map to Touch 1/2/3 timing).

**Q7 — Referral network (native, absorbed from referral-engine 2026-09-15)**

If a legacy referral-engine config was detected, present it and confirm/edit. Otherwise ask:

1. **Connector taxonomy** — how do you tag connectors in your CRM? (CRM property, list membership, tag, or "past customers count automatically")
2. **Quiet threshold** — days without contact before someone surfaces as a "going quiet" value-share opportunity. Default 60.
3. **Trigger patterns** — which of the default triggers apply (positive-touch reply, project closed, publicly mentioned you, fiscal-year flip, conference season, funding/press) plus any custom ones.
4. **Ask cadence cap** — how often is it OK to ask the same connector for a referral? Default 180 days (6 months).

That's it. For a full-stack user with peer files populated plus Q6/Q7 answered, that's the whole interview. For a standalone install, expand each peer-imported field into the full interview from the original v0.1.0 setup.

---

## Step 3 — Write the config

Populate `<config-root>/plugins/relationships.user-context.md`. See `references/user-context.template.md` for the slim canonical layout.

The written file contains:
- Identity (minimal — primary key for templates: name, first_name, company, one_liner)
- Relationships preferences (tiers, buckets, close-personal, time budget, voices for network expansion, scoring overrides if any)
- **ICP & signal sourcing** (Q6 answers — native, not peer-imported)
- **Referral network config** (Q7 answers — native, not peer-imported)
- Companion-plugin detection results (so /relationships knows what to delegate to)
- Provenance notes (which fields came from which peer file, vs. answered natively)

Identity, voice, and CRM are NOT written here — `/relationships` reads them live from their canonical peer files (cortex, core-ops) at runtime. ICP, Apollo/signal preferences, and referral cooling rules ARE written here — they're native to this plugin as of the 2026-09-15 lead-engine/referral-engine merge, not read from a peer.

**Exception:** if the cortex/core-ops peer files are missing (standalone install), capture the equivalent identity/voice/CRM fields in `relationships.user-context.md` under `## Standalone fallback` sections. The plugin can run without peers; it just stores its own copy.

### Initialize signal-pipeline files (if first run)

If `<config-root>/relationships/pipeline.md` doesn't exist, create it:

```markdown
# Pipeline — Active Signals

> Each entry: signal type, contact, captured date, status, next action date, last touch.
> Status values: `new` → `drafted` → `sent` → `replied` → `booked` / `dead`.

---

(empty — capture your first signal with /capture-signal or /pull-signals)
```

If `<config-root>/relationships/sent-log.md` doesn't exist, create it:

```markdown
# Sent Log — DMs & Replies

> Append-only log of every touch sent and reply received. Used by /relationships to compute follow-up timing.

---
```

---

## Step 4 — Confirm and offer next step

Summarize what was written.

Offer:
> "Run `/network-rebalance` once to tag your existing cortex person pages with tier + bucket frontmatter. Then `/relationships` daily.
>
> Full command list: `/relationships` (daily brief) · `/draft-touchpoint` (per-contact draft, incl. referral asks) · `/touchpoint` (log what happened, incl. signal sends/replies/bookings) · `/pull-signals` (Apollo fetch) · `/capture-signal` (manual signal log) · `/connect-signal` · `/warm-signal` · `/draft-signal` (signal drafting cadence) · `/pre-call-brief` · `/network-rebalance`."

---

## Behavior rules

- **Peer-import is one-time at setup.** Re-running setup re-imports.
- **Read defensively.** If a peer file has a renamed section, log it in the confirmation step as `Notes:` — don't crash.
- **Confirm, don't interrogate.** For full-stack users, defaults + detected values + a handful of confirmations is the whole experience.
- **Standalone-install fallback.** If no peers exist, expand each peer-imported step into a full interview question. The plugin must work for a stranger who only installed `relationships` + cortex.
- **Respect the autonomy slider** (`<config-root>/plugins/cortex.user-context.md` → `autonomy:`). In `auto` mode, accept detected values and defaults; only ask for sections without sensible defaults.
- **Idempotent.** Re-running merges with existing config; doesn't blow it away unless user explicitly says "start over."
