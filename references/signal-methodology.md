# Signal methodology (absorbed from lead-engine, 2026-09-15)

This reference carries the *methodology*, the *7 signals*, the *voice rules*, and the *cadence logic* behind `/pull-signals`, `/capture-signal`, `/connect-signal`, `/warm-signal`, `/draft-signal`, and `/pre-call-brief`. Each of those commands reads this file and the reference files below for context before acting.

## Core principle

**The unlock isn't the message. It's the timing.**

Cold outbound averages 1–2% reply rates because the recipient has no current reason to care. Intent-based outbound averages 25–40% because you only message people who are *currently exhibiting a buying signal*. The DM still has to be good — but a great DM with no timing beats a cold list, and a decent DM with great timing crushes both.

When in doubt, prioritize *signal freshness* over *message polish*. A 4-hour-old signal with a workmanlike DM beats a 4-day-old signal with a perfect one.

## Always read these references before acting

Before you draft, capture, or log anything, **read in this order**:

1. `<config-root>/plugins/growth.user-context.md` — the user's company, ICP, voice, value-adds, tools, cadence preferences. If this file is missing or contains the placeholder, tell the user to run `/setup-relationships` first and stop.
2. `references/seven-signals.md` — the canonical 7-signal taxonomy with the prompts for classifying each.
3. `references/signal-voice-rules.md` — banned phrases, tone-matching rules, length caps, the 27-word opener pattern.
4. `<config-root>/relationships/pipeline.md` — current active signals.
5. `<config-root>/relationships/sent-log.md` — what's been sent and when (drives follow-up timing).

Don't skip these. Generic outreach is what we're trying to *not* produce.

## The 7 signals (summary)

| # | Signal              | What it looks like                                                              | Drafting angle                                            |
|---|---------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------|
| 1 | Engagement          | Liked / commented on a post in your problem space                               | React to the specific post / comment they engaged with    |
| 2 | Job change          | New role at an ICP company in last ~60 days                                     | Congratulate genuinely + frame your offer to first-90-day priorities |
| 3 | Funding             | Their company raised in last ~90 days                                           | Tie your offer to "what funding gets spent on"            |
| 4 | Hiring              | Posting roles that imply your problem (e.g., "Head of CRO", "VP RevOps")        | Reference the role, frame yourself as a force multiplier  |
| 5 | Growth/expansion    | New office, market, product line                                                | Connect your offer to scaling pain                        |
| 6 | Tech-stack change   | Adopting / dropping vendors in your space                                       | Lean into "I see you just moved to X — common gotcha is…" |
| 7 | Direct intent       | Asking for recs / posting a problem                                             | Answer the actual question; soft-pitch only at the end    |

Full prompts and scoring rubric in `references/seven-signals.md`.

## The 27-word opener

The proven pattern for the first DM. Roughly 27 words, four sentences:

1. **Hook** — name the signal you saw, specifically. *Not* "saw your post" — "saw your comment about [specific thing]."
2. **Resonance** — one sentence that shows you actually *got* what they said. Not flattery.
3. **Bridge** — one sentence that connects their thing to your thing without pitching.
4. **Light ask** — a low-friction next step. Not "30 minutes." More like "worth a 5-min thread on this?" or "want me to send the teardown?"

Length cap: 27 words. Stretch to 40 only if the signal genuinely demands it.

Full rules and examples: `references/signal-voice-rules.md`.

## The full lifecycle of a signal

Before the DM cadence even starts, there are two preparation steps that materially boost reply rates:

- **Warming** (`/warm-signal`) — like 2 of the contact's recent posts, comment with substance on 1, then DM 24 hours later. Their notification feed shows your name 2–3 times before the DM arrives, so the DM doesn't read cold. Skip warming for high-priority direct-intent signals where speed matters more than warming.
- **Connection request** (`/connect-signal`) — most LinkedIn DMs require an accepted connection first. The connection-request note is *not* the DM — it's lighter, peer-level, and shouldn't reference the signal directly. Skip if the contact is already a 1st-degree connection.

Then the 3-touch DM cadence (override per `user-context.md`):

- **Touch 1:** the 27-word opener, sent same-day or next-day after warming/connection.
- **Touch 2:** day 3–7. Reference touch 1 obliquely. Add new value (a link, a stat, an offer). Do NOT say "just following up" or "circling back."
- **Touch 3:** day 10–14. Polite breakup. Acknowledge the silence. Leave the door open. *This often pulls the most replies.*

After a meeting books, generate a **pre-call brief** (`/pre-call-brief`) with contact research, talking points, and likely objections.

If they reply at any point: pause the cadence, switch to context-driven response.

## When the user asks for a DM

The commands handle this end-to-end, but if the user asks naturally ("draft a DM for the Sarah signal") rather than via slash command:

1. Read `user-context.md` for voice/ICP/value-adds.
2. Read ``<config-root>/relationships/pipeline.md` to find the relevant signal entry.
3. Read `voice-rules.md` for the opener pattern.
4. Read `sent-log.md` to see if any prior touches exist (if so, this is a follow-up, not an opener).
5. Draft the message. Output:
   - The DM itself (copy-paste ready)
   - A one-line note explaining *why* this lands (signal + angle + value-add used)
   - A reminder of the next-touch date if the cadence applies

Do not output multiple alternates by default. One good DM > three mediocre ones. Only offer alternates if the user asks.

## When the user logs a send or reply

Update `sent-log.md` with the timestamp, signal ID, touch number, and verbatim message sent. Update ``<config-root>/relationships/pipeline.md` status. If CRM is connected per `user-context.md`, push the engagement to CRM.

If the reply is a *no*, mark the signal `dead` and stop the cadence.
If the reply is a *yes / interested*, mark `replied` and prompt the user for next steps (book a call, send the resource, etc.).
If the reply is *neutral / question*, draft a context-aware response — DON'T fall back to the cadence template.

## What this skill should NEVER do

- Auto-send DMs (LinkedIn blocks this and we shouldn't pretend otherwise — output is always copy-paste).
- Use any banned phrase from `voice-rules.md`.
- Draft generic openers that ignore the specific signal — every DM must reference the actual signal in sentence one.
- Skip the user-context check. If the profile isn't set up, the output will be generic; bail and tell the user to `/setup-relationships` first.
- Pretend Apollo / CRM connectors exist when they don't. Read `user-context.md` to know what's actually wired.

## Files this skill writes to

- `<config-root>/relationships/pipeline.md` — current state of every signal.
- `<config-root>/relationships/sent-log.md` — append-only history.
- (CRM, if connected, via the appropriate MCP tools.)

The user-context, seven-signals, voice-rules, and rollout-plan references are *read-only at runtime* — only `/setup-relationships` modifies them.
