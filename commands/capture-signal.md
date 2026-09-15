---
name: capture-signal
description: >
  Manually capture a buying signal you spotted (LinkedIn post, comment, job change, etc.). Classifies the signal against the 7-signal taxonomy, scores it against the user's ICP, researches the contact across available connectors, and adds it to the active pipeline. Use after spotting something organically — for bulk Apollo pulls, use /pull-signals instead.
---

# /capture-signal — log a signal

You are capturing a single LinkedIn buying signal the user just spotted. Be fast, accurate, and skeptical (not every "they liked a post" is a real signal).

## Step 0: Preflight

Read these files. If `user-context.md` is missing or has placeholder content, stop and tell the user to run `/setup-relationships` first.

- `<config-root>/plugins/relationships.user-context.md`
- `references/seven-signals.md`
- `<config-root>/relationships/pipeline.md`

## Step 1: Get the signal from the user

If the user already pasted a signal description with the command, parse it. Otherwise, ask via AskUserQuestion (one question at a time):

### Q1 — The signal itself
"What did you see? Paste a screenshot description, a LinkedIn URL, or just describe what happened. Examples:
- 'Sarah Chen (VP Growth at Acme) commented on Jane's post about CRO testing'
- 'Bob Lee just changed jobs to Head of RevOps at Beta Co'
- 'Acme Corp announced a $20M Series B yesterday'"

### Q2 — Contact identity (if not clear from Q1)
"Who's the person you'd reach out to? Name + title + company is enough. If there's a LinkedIn URL, even better."

### Q3 — Signal source / link (optional)
"Got a URL for the signal itself? (LinkedIn post, news article, etc.) Helps me reference it precisely later. Skip if not handy."

## Step 2: Classify the signal

Match the signal to the canonical 7-signal taxonomy in `seven-signals.md`. If it fits more than one, pick the strongest. If it fits *none* cleanly, check the user's "Custom signal" entry from `user-context.md` — it might match. If it still doesn't fit, ask the user whether to log it as a soft signal or skip.

Output the classification + a one-line "why this signal fits."

## Step 3: Research the contact (briefly)

Use whatever connectors are available per `user-context.md`:

- **Gmail (if connected):** search threads for the contact's email or name. Note any prior correspondence — last touch date, last topic, tone of last exchange.
- **CRM (if connected):** look up the contact. Note current owner, lifecycle stage, deal history, last activity.
- **Web (if needed):** WebSearch for "[name] [company]" only if the signal is high-priority and you need more context. Don't over-research SMB / low-priority signals.

Keep this lightweight — 60 seconds of digging, not a dossier. Output 3–5 bullet points of what you found.

## Step 4: ICP fit + priority score

Score the signal **High / Medium / Low** based on:

- **ICP match** — does the contact's role + company fit the ICP from `user-context.md`?
- **Signal strength** — how recent is it? How direct is the buying intent? (Direct intent > engagement > job change > funding > hiring > stack change > expansion, roughly.)
- **Disqualifiers** — does the company hit anything in the disqualifier list?

If High: queue for outreach today.
If Medium: queue for this week.
If Low: log it but don't queue (user can promote later).

Output the score with a one-line rationale.

## Step 5: Append to pipeline

Append to `<config-root>/relationships/pipeline.md` using this entry format:

```markdown
---

## SIG-[YYYYMMDD]-[short-slug]

**Captured:** [YYYY-MM-DD HH:MM]
**Status:** new
**Priority:** [High / Medium / Low]
**Signal type:** [one of the 7, or custom]
**Signal source:** [URL or short description]

**Contact:**
- **Name:** [name]
- **Title:** [title]
- **Company:** [company]
- **LinkedIn:** [URL or "not provided"]
- **Email:** [if known from CRM/Gmail, or "unknown"]

**Signal context:**
[2–4 sentences. What they said / did. The specific quote or detail you'll reference in the DM.]

**Prior history:**
[from Gmail/CRM lookup, or "none found"]

**Drafting angle:**
[1–2 sentences. The hook you'll use. The value-add you'll lead with. This becomes the input for /draft-signal.]

**Cadence:**
- Touch 1: [pending] — target send date: [today or tomorrow]
- Touch 2: [pending] — target: +[N] days
- Touch 3: [pending] — target: +[N] days

**Notes:**
[anything else worth remembering]
```

The `SIG-` ID is `SIG-` + today's date in YYYYMMDD + a short slug from the contact's name (e.g., `SIG-20260501-sarah-chen`).

Cadence target dates come from `user-context.md` — don't invent them.

## Step 6: Confirm + offer next step

Tell the user:

```
✅ Signal captured: SIG-[id]

  Type: [signal type] · Priority: [score]
  Contact: [name], [title] @ [company]
  Hook: [one-line drafting angle]

Next:
  /connect-signal SIG-[id]  — draft connection request (skip if already 1st-degree)
  /warm-signal SIG-[id]     — warm them with a comment + 2 likes (skip for direct-intent / hot signals)
  /draft-signal SIG-[id]    — draft the 3-touch DM sequence now
  /relationships          — see everything that's active
```

Pick the right next step based on signal type and contact relationship:
- **Already connected, signal is hot (Direct intent or High priority < 24h old):** skip warming, run `/draft-signal` immediately.
- **Already connected, signal is warm:** run `/warm-signal` first, then `/draft-signal` 24h later.
- **Not connected:** run `/connect-signal` first. Then `/warm-signal` after they accept (optional). Then `/draft-signal`.

If priority is High, nudge: "This one's hot — at minimum get the connection request out today."
If Low, nudge: "Logged but not queued. Promote it later if the contact warms up."
