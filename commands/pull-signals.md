---
name: pull-signals
description: >
  Pull fresh buying signals from Apollo for the user's ICP. Fetches job changes, funding events, and hiring signals (per the user's setup preferences), filters against the ICP, scores priority, and adds them to the pipeline. Use to refresh the pipeline at the start of a session. Requires the Apollo MCP to be connected — falls back to a clear message if not.
---

# /pull-signals — fetch signals from Apollo

You are pulling fresh signals from Apollo, filtering against the user's ICP, and adding the qualifying ones to the pipeline.

## Step 0: Preflight

Read:
- `<config-root>/plugins/relationships.user-context.md`
- `references/seven-signals.md`
- `<config-root>/relationships/pipeline.md` (so we don't re-add duplicates)

If `user-context.md` is missing/placeholder: stop, tell user to run `/setup-relationships`.

Check available Apollo tools (look for `apollo_*`). If none are available, stop and tell the user:

> "I don't see the Apollo MCP connected, so I can't pull signals automatically. Either connect Apollo (then rerun setup with `/setup-relationships`) or capture signals manually with `/capture-signal`."

## Step 1: Read pull preferences from user-context

From `user-context.md`'s Tools / Apollo entry, find which signal sources are enabled:
- Job changes only, OR
- Job changes + funding, OR
- All three (job changes + funding + hiring)

If the file says Apollo is connected but no preference was captured, default to **job changes + funding** and proceed.

## Step 2: Pull each enabled source

### Job changes (when enabled)

Use `apollo_mixed_people_api_search` with filters:
- Roles matching the user's ICP target roles (from `user-context.md`).
- Industry matching ICP industries.
- Company headcount within ICP company size range.
- Filter for "started new role in last 60 days" (Apollo supports this via job-change-recency filters).

Limit: 25 results per pull. We're going for *quality* signals, not a list.

### Funding (when enabled)

Use `apollo_mixed_companies_search` (or `apollo_organizations_enrich` if you have a starter list) with filters:
- Industry matching ICP.
- Headcount within range.
- Funding event in last 90 days.

For each company, then pull the relevant champion contact (matching ICP roles) — usually 1 per company.

Limit: 15 companies per pull.

### Hiring (when enabled)

Use `apollo_organizations_job_postings` filtered to:
- ICP industries + size.
- Job postings that match keywords from the user's offer (you'll need to derive keywords from `user-context.md`'s positioning + offer descriptions). Examples for a CRO consultancy: "Head of CRO", "Conversion Rate Optimization", "Growth Manager".

For each company with a relevant job post, pull a senior champion contact at that company.

Limit: 15 companies per pull.

## Step 3: Dedupe + filter

For each candidate signal:

1. **Dedupe** — check `<config-root>/relationships/pipeline.md`. If the same contact already has an active SIG (not `dead` / `booked`), skip. If a SIG exists but is closed, you can re-add only if the new signal is materially different from the closed one.
2. **Disqualify** — apply the disqualifier rules from `user-context.md`. Drop anything that hits a disqualifier.
3. **Score** — assign High / Medium / Low using the rubric in `seven-signals.md` and the user's signal-priority weighting from `user-context.md`. A signal type the user marked "high priority" should bias scoring up.

## Step 3.5: (Optional) Enrich the top 10 via contact-researcher

Apollo signals are net-new and often have thin context — title, company, signal type, but not "what does this person actually post about" or "did the user already cross paths with them." For the top 10 by score, optionally enrich each via the `contact-researcher` subagent.

**This step is opt-in.** It costs more tokens and time. Skip if:
- The user passed `--no-enrich`.
- The pull surfaced fewer than 5 signals (just append; enrichment isn't worth it).
- The user is doing a quick refresh and just wants to see what's new.

**Run enrichment when:**
- The user said "enrich" or "deep pull" or asked for context-rich signals.
- The pull surfaced 10+ signals and the top ones are high-priority — enrichment sharpens drafting and prevents wasted DMs on bad-fit contacts.

To enrich, for each of the top 10 signals (cap at 10 — don't go deeper):

**Use the Task tool with `subagent_type="contact-researcher"`.** Pass:
- **Contact name** + email (from Apollo)
- **Company name** (from Apollo)
- **Purpose:** `outreach`
- **Time horizon:** 90 days

For each returned dossier, augment the SIG entry's `**Signal context:**` and `**Drafting angle:**` fields:
- **Signal context:** keep the Apollo data, add a 1-line summary of public signals from the dossier (e.g., "Apollo: joined Acme as VP Growth on 2026-04-15. Recent: posted last week about CRO tooling — alignment with our offer.").
- **Drafting angle:** sharpen using the dossier's Three Talking Points. Pick the strongest seed and use it as the angle.
- **Prior history:** if the dossier shows ANY prior email or meeting touch, replace the default `[Skip]` with a one-line summary so future commands have the context.

If `contact-researcher` isn't available, skip enrichment silently and proceed to Step 4. Tell the user once at the end of Step 5: "Heads up — enrichment was skipped because `contact-researcher` isn't installed. contact-researcher is bundled with this plugin — check it's registered."

## Step 4: Append to pipeline

For each surviving signal, append a SIG entry to `<config-root>/relationships/pipeline.md` using the same format as `/capture-signal`:

```markdown
---

## SIG-[YYYYMMDD]-[short-slug]

**Captured:** [today, HH:MM]
**Status:** new
**Priority:** [High / Medium / Low]
**Signal type:** [Job change / Funding / Hiring]
**Signal source:** Apollo — [specific detail, e.g., "Joined Acme Co as VP Growth on 2026-04-15"]

**Contact:**
- **Name:** [from Apollo]
- **Title:** [from Apollo]
- **Company:** [from Apollo]
- **LinkedIn:** [from Apollo if available]
- **Email:** [from Apollo if available]

**Signal context:**
[2-3 sentences describing the specific signal. For job changes: "Joined [company] as [role] on [date]. Came from [previous company / role] where they [tenure]." For funding: "[Company] raised $XM Series [X] on [date]. Lead investor: [investor]. Stated use of funds: [if available]." For hiring: "[Company] is hiring [role] (posted [date]). Job description emphasizes [relevant keyword]."]

**Prior history:**
[Skip — Apollo pulls are net-new contacts. If the user wants Gmail/CRM cross-check, they can run `/capture-signal` workflow on the SIG manually.]

**Drafting angle:**
[1-2 sentences. The hook for `/draft-signal` to use.]

**Cadence:**
- Touch 1: [pending] — target send date: [today or tomorrow]
- Touch 2: [pending] — target: +[N] days
- Touch 3: [pending] — target: +[N] days

**Notes:**
Pulled by /pull-signals on [date].
```

Cadence intervals come from `user-context.md` — don't invent them.

## Step 5: Output summary

Don't dump every signal — give a tight summary:

```
✅ Apollo pull complete

  Sources pulled: [job changes, funding, hiring — whichever are enabled]
  Candidates fetched: [N]
  Disqualified: [N]  (e.g., "8 dropped — agency disqualifier")
  Duplicates skipped: [N]
  Added to pipeline: [N]

Priority breakdown:
  🔥 High: [N]   ([list 2-3 names with signal type])
  🟡 Medium: [N]
  🔵 Low: [N]

Top signal of the pull: [SIG-id, name @ company, one-line why]

Next:
  /relationships                            — see what's queued for today
  /connect-signal SIG-[top high-priority id]  — connection request for the hottest signal
  /warm-signal SIG-[top high-priority id]     — warm before DMing (if already connected)
  /draft-signal SIG-[top high-priority id]    — draft DM directly (skip warming for hot direct-intent signals)
```

For Apollo-pulled signals, almost all contacts will be net-new (not yet connected). Default flow: `/connect-signal` first, then `/warm-signal` after they accept, then `/draft-signal` 24h after warming.

## Edge cases

- **Apollo returns 0 results:** don't fail silently. Tell the user "0 signals matched your filters — try broadening ICP company size, or adding a different industry. Or capture manually with `/capture-signal`."
- **Apollo returns 100+:** signal sourcing is too loose. Tell the user "Apollo returned [N] candidates — way more than expected. Consider tightening ICP filters in `/setup-relationships`. I capped at 25 per source for this pull."
- **Apollo MCP throws an error:** show the error verbatim, suggest checking the MCP connection, and offer manual capture as the fallback.

## What this command does NOT do

- Doesn't send DMs.
- Doesn't auto-draft. Drafting is a separate, deliberate step (`/draft-signal`) — keeps the user in control of voice.
- Doesn't push to CRM yet — that happens at `/touchpoint sent`. We don't want CRM cluttered with contacts the user might never actually message.
