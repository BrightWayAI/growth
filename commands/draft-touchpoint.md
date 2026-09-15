---
description: Draft a single message to a specific contact on demand. Pass a name, slug, or "the person I was just talking about." Picks the right channel + template based on relationship class + tier + trigger, fills variables from cortex + identity + voice, returns a copy-ready draft. Drafts only — never sends. Use when you don't want the full daily brief — you already know who you want to reach.
---

# /draft-touchpoint

Per-contact on-demand drafting. Lighter than `/relationships` — no scoring, no ranking, no buckets. One person, one message, one draft.

Use cases:
- "Draft something to Sarah Chen about her funding news."
- "I want to follow up with Sam on the Acme Corp Phase 2 talks."
- "Write me a check-in to my brother."

---

## Step 0 — Preflight

Read `<config-root>/plugins/relationships.user-context.md`. If missing → route to `/setup-relationships` and stop.

Read `<config-root>/identity.md` and `<config-root>/voice.md` (or named voice files if user has multiple).

---

## Step 1 — Resolve the contact

Parse the user's input. Strategies in priority order:

1. **Explicit slug** (`/draft-touchpoint sarah-chen` or `/draft-touchpoint person/sarah-chen`) — load `<config-root>/memory/person/sarah-chen.md` directly.
2. **Full name** (`/draft-touchpoint "Sarah Chen"`) — slugify and try `<config-root>/memory/person/sarah-chen.md`. If missing, search cortex memory for a name match.
3. **Partial name** (`/draft-touchpoint Sarah`) — search cortex `memory/index.md` and recent `hot.md` mentions. Surface all matches, ask user to disambiguate.
4. **Contextual reference** ("the person I was just talking about," "him") — read recent conversation context. If unambiguous, use that person. If ambiguous, ask.
5. **No cortex page but CRM record exists** — pull the HubSpot record by name match. The card will be marked `research_thin: true`.
6. **Net-new (no cortex, no CRM)** — accept name + company + email; the command works with just that, but flags Confidence Low and recommends running `contact-researcher` first.

If multiple matches, present them and ask which:

> "Found 3 possible matches:
> - Sarah Chen (MedBridge) — last interaction 12d ago
> - Sarah Chen (Acme Learning) — last interaction 4mo ago
> - Sarah Chen-Williams (Globex) — last interaction 18d ago
> Which one?"

---

## Step 2 — Gather context

Read everything relevant to drafting:

1. **Cortex person page** (if exists): frontmatter (tier, intent, buckets, relationship_class, icp_fit, preferred_channels, generosity_ledger), Identity, Relationship (temperature, last meaningful contact), Recent interactions, Open threads, Notes, Linked entities.
2. **CRM record** (if connected): lifecycle stage, owner, open deals, last activity, custom tier/ICP properties.
3. **Recent email threads** (if Gmail/Outlook connected): the 1-2 most recent threads, with subject + ≤30-word summary. Note who sent last.
4. **Recent calendar interactions** (if connected): the most recent past meeting + any upcoming.
5. **Hot cache** (`<config-root>/memory/hot.md`): any fresh mentions in the last 7 days that didn't make it to the person page yet.

If cortex isn't installed, fall back to CRM + email + ask user for relationship context inline.

---

## Step 3 — Determine intent

Two paths:

### A — User specified intent explicitly

If the user's prompt included intent ("about her funding news" / "to follow up on Acme Corp Phase 2" / "just check in"), use that as the **`trigger.summary`** and **`trigger.type`**.

### B — User didn't specify; you infer

Run a short interactive disambiguation:

> "Drafting to Sarah Chen. What's the angle?
> - **a) Cadence check-in** — it's been 12d since you last talked, no specific trigger
> - **b) React to a signal** — she posted/funded/changed roles (you tell me what)
> - **c) Follow-up** — there's an open thread (last waiting: WAITING:you on intro request from 2026-05-10)
> - **d) Cold-but-warm** — I'll go with a general thoughtful touch
> - **e) Something else** — you tell me"

If only one signal is fresh and obvious (e.g., a clear WAITING:you item with a date), skip the disambiguation and proceed with it, telling the user "Drafting follow-up on the intro request you owed her (waiting since 2026-05-10) — say if you want a different angle."

---

## Step 4 — Pick channel + template

Same logic as `/relationships` Step 4 (see `references/scoring.md` channel-selection table).

Apply in order:
1. **User override:** if the user's prompt included a channel ("text my brother" / "draft an email to Sarah") — honor it.
2. **Person page `preferred_channels`** (array, v0.1.2+) — if present and non-empty, use the first matching entry; fall back to `preferred_channels[0]` if no exact channel-to-trigger match.
3. **Channel-selection rule table** — based on relationship_class + tier + trigger.

Then map `(channel, scenario)` → template file. Prefer user overrides at `<config-root>/relationships/templates/` over bundled `references/templates/`.

If no template scenario exactly matches the intent, pick the closest variant and note in the response: "Used the closest template (warm-this-made-me-think-of-you); if you want a custom angle, just tell me."

---

## Step 5 — Fill variables and draft

Variables to fill (full list in `references/templates/README.md`):

- `{{person.first_name}}`, `{{person.full_name}}`, `{{person.title}}`, `{{person.company}}`
- `{{trigger.context}}`, `{{trigger.specific}}` — from Step 3's intent
- `{{user.first_name}}`, `{{user.company}}`, `{{user.one_liner}}` — from identity + user-context
- `{{shared_context}}` — synthesize from cortex page's Recent interactions / Open threads (≤20 words)
- `{{voice.signoff}}` — from the voice block being used

**Voice routing:**
- If `relationship_class: personal` AND user has a `personal` voice defined → use it.
- Otherwise use the primary voice from `<config-root>/voice.md`.
- For network-expansion content posts, route to the named voice for that surface.

**Variable resolution failures:**
- If a required variable can't be filled, pick a template variant that doesn't need it.
- If no variant works, fill the template with `{{variable}}` placeholders left in OR fill with `[your touch here]` markers. Set `needs_user_touch: true` in the output.

**Banned phrases:**
- Honor the cortex default banned list ("just checking in," "circling back," "touching base," "I hope this email finds you well," "per my last email," "synergy/leverage/align," "any luck with [X]?").
- Honor user-context additional banned phrases.

---

## Step 6 — Apply the "should we even send?" filter

Before presenting, run the gut-check (ported from `bizdev-outreach`):

- Is the ball in their court? If so, surfacing a draft might be premature.
- Did your last message set a tone that follow-up would undermine?
- Is there genuine new value here?
- Is it too soon based on their bandwidth signals?

If any answer is "no, don't send," **still produce the draft** but prepend a warning:

> ⚠️ **Cooling flag:** Last message sent 4d ago, no reply yet. Their bandwidth might be tight. Draft is below, but consider whether sending now risks the relationship. Alternative: snooze 7d.

The user decides.

---

## Step 7 — Present

Format for fast scanning:

```
DRAFT — to Sarah Chen (MedBridge) via LinkedIn DM (warm)
Voice: primary  ·  Template: dm/linkedin-warm-checkin  ·  Est. 4 min

WHY NOW
  WAITING:you on intro request (open since 2026-05-10, 18d)

DRAFT
─────────────────────────────────────────────────────────
Sarah — overdue for a real catch-up. Last we talked, you'd
asked about an intro to the Acme Corp team. I've been sitting
on it longer than I should — Sam there is the right
person; want me to set it up this week?

No pressure to volley back immediately — also happy with
a "still cooking, ping me in a month."

—Jane
─────────────────────────────────────────────────────────

[ Copy ]  [ Edit & redraft ]  [ Different channel ]  [ Different template ]
[ Mark sent ]  [ Snooze ]
```

If the draft has `needs_user_touch: true`, also surface:

> ⚠️ Template wanted a `{{shared_context}}` value but the cortex page doesn't have recent interactions logged. I dropped a `[your touch here]` marker — replace with one sentence of context.

---

## Step 8 — If user picks an action

- **Copy** — return the draft body in a code block so the user can copy it cleanly. No side effects.
- **Edit & redraft** — accept the user's edit instructions, regenerate. Limit to 3 redraft rounds before suggesting they hand-edit the copy.
- **Different channel** — switch to another channel (LinkedIn DM → email, etc.), pick a different template, regenerate.
- **Different template** — within the same channel, surface the available scenarios and let the user pick.
- **Mark sent** — append to the cortex person page's `## Recent interactions` log:
  ```
  <today> — <channel> — draft-touchpoint sent — <intent summary>
  ```
  Update `Last meaningful contact` in Relationship if appropriate. Update HubSpot contact's `last_activity_date` only if the user explicitly confirms CRM write.
- **Snooze** — append to `<config-root>/memory/staged/skip-logs/touchpoint-snooze.md` with `<slug>` + reason + resurface-after date. The daily brief will respect this.

---

## Step 9 — Log

If cortex `log-writer` skill is available, append to `<config-root>/memory/log.md`:

```
## [YYYY-MM-DD HH:MM] /draft-touchpoint | <person.slug> — <channel> — <intent>
```

---

## Behavior rules

- **Single contact per invocation.** If the user names multiple ("draft to Sarah and Sam"), run twice — don't batch in one draft.
- **Drafts only.** Never send. Mark-sent updates cortex but doesn't actually transmit anything.
- **Voice-faithful.** Always use the right voice (primary vs personal vs business). Banned phrases enforced.
- **Honest about thin data.** If the cortex page is sparse or net-new, the draft will be generic. Tell the user.
- **Respect cooling periods.** If the contact is inside the tier's minimum-gap window, surface the warning loudly.
- **Idempotent.** Running twice on the same contact regenerates; doesn't pile drafts in memory.

---

## Edge cases

- **Contact has no cortex page.** Offer to delegate to `contact-researcher` (lead-engine) first — generates a dossier AND seeds a person page. User can decline; the command still drafts with the data available.
- **Contact has frontmatter `tier: dormant`.** Surface a soft warning: "Sarah is tier=dormant — typically not surfaced in daily briefs. Drafting anyway, but consider whether re-engaging is intentional."
- **Contact has DNE flag** in cortex or CRM. Refuse to draft. Surface: "Sarah is marked do-not-engage. If this is wrong, edit the person page or CRM first; otherwise, this command won't draft."
- **User passes a channel that's incompatible** (e.g., "draft a phone call to a cold prospect"). Push back once: "Phone calls work for warm contacts. For cold ICP, LinkedIn DM or email is the default. Override anyway?" If yes, draft accordingly.
- **Voice file missing** for a requested voice (e.g., user invoked personal voice but `voices/personal.md` doesn't exist). Fall back to primary voice; note in response.
- **Template requires variables that can't be derived.** Use the most-complete template variant available; mark `needs_user_touch: true` on what's left.
