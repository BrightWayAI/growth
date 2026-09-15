---
name: pre-call-brief
description: >
  Generate a pre-call brief once a meeting is booked. Pulls everything we know about the contact and company (signal context, prior touches, replies, CRM record, recent web mentions) and produces a structured brief: contact snapshot, company snapshot, signal recap, talking points, likely objections, and a soft next-step. Use after /touchpoint SIG-X booked.
---

# /pre-call-brief — pre-call brief

You are generating a pre-call brief for a booked meeting. This is the highest-leverage moment in the entire pipeline — the user is about to spend 30+ minutes with the prospect, and the difference between a great brief and no brief is the difference between booking the next step and getting "let me think about it."

## Step 0: Preflight

Read:
- `<config-root>/plugins/growth.user-context.md`
- `<config-root>/relationships/pipeline.md`
- `<config-root>/relationships/sent-log.md`
- `references/seven-signals.md`

If `user-context.md` is missing/placeholder: stop, tell user to run `/setup-relationships`.

## Step 1: Identify the signal

If the user passed a SIG-ID, use it. Otherwise list `booked` SIGs and ask which one.

The SIG must have status `booked` (or at minimum `replied` with the user about to take a meeting). If status is anything earlier (`new`, `drafted`, `sent`), confirm: "This signal hasn't been logged as booked yet — are you generating a brief for a meeting that's already on the calendar? (yes / no — if no, log it first with `/touchpoint SIG-[id] booked`)".

## Step 2: Pull all known context for this signal

Gather from the local files:
- **From the SIG entry in `<config-root>/relationships/pipeline.md`:** signal type, captured date, contact details, signal context, drafting angle, notes, meeting time/date.
- **From `sent-log.md`:** every touch sent + every reply received. Read the verbatim messages — *what* they replied with tells you their language and what they care about.

## Step 3: Pull contact + company context — delegate to relationships-director (mode: research)

Instead of doing CRM + Gmail + web pulls inline (which bloats this conversation's context), delegate the dossier to the `relationships-director` subagent (`mode: research`).

**Use the Task tool with `subagent_type="relationships-director"` and `mode: "research"`.** Pass:

- **Contact name** + email (from the SIG entry)
- **Company name** (from the SIG entry)
- **Purpose:** `pre-call-brief`
- **Time horizon:** 180 days (briefs benefit from a longer lookback than first-touch outreach)

The agent returns:
- **Contact Snapshot** — title, current company, lifecycle, owner, time-in-role
- **Relationship History** — last email, last meeting, open deals, cumulative touches
- **Recent Public Signals** — job changes, funding/press, LinkedIn activity
- **Three Talking Points** — signal-tied seeds (you'll likely use these as raw material for Step 4's Talking Points section, but rewrite them in your own framing)
- **Suggested Next Step** — informs Step 4's "Soft next step" section
- **Confidence & Gaps** — flag anything missing (e.g., "no Gmail connector — relationship history limited")

### Confidence check before assembling the brief

**Read the dossier's `Confidence & Gaps` section first.** If `Confidence: Low` AND key sections (Contact Snapshot, Relationship History) are sparse, pause and ask the user:

> "Heads up — `relationships-director` came back Low confidence on this contact: [specific gap]. The brief is going to be thin without it. Want to share what you know — relationship history, why they're considering this, anything not in the CRM — so I can build a stronger brief? Or 'proceed' and I'll work with what we have."

If the user provides context, incorporate it into Step 4's structure. If they say "proceed," do so and flag in the brief's bottom that confidence was low and verify before the call.

### Use the dossier as raw material for Step 4

Don't paste the dossier into the brief verbatim. Step 4 has its own structure (Who you're meeting, The company, Signal recap, Their reply analysis, etc.). Use the dossier's findings as inputs to those sections — your job is to synthesize, not relay.

The dossier and the local SIG context (signal recap, sent-log, the verbatim reply) are the two main inputs. If they conflict (e.g., dossier says they're VP Marketing but the signal captured them as Director), trust the dossier — it's pulled from current data — and note the discrepancy in the brief.

### If relationships-director is not available

If the agent isn't registered, fall back to inline pulls (CRM lookup, Gmail search, 3-5 web searches). Tell the user once: "Heads up — `relationships-director` isn't available. Briefs are slower and noisier without it. relationships-director is bundled with this plugin — check it's registered." Then proceed inline.

## Step 4: Synthesize the brief

Use this exact structure. Skip any section that has nothing real to say — better an empty brief than fluff.

```markdown
# Pre-call brief — SIG-[id]

**Meeting:** [date + time + meeting link if known]
**Duration:** [from SIG entry, or "unknown — ask user"]
**Channel:** [Zoom / Google Meet / phone / in person]

---

## Who you're meeting

**[Full name]** — [title] @ [company]

- **Tenure:** [time in role + prior role if relevant]
- **Background:** [1-2 sentences on what they did before. Source from LinkedIn or prior research.]
- **Public posture:** [what they post about, what they care about — pulled from posts/articles. 1-2 sentences.]

---

## The company

**[Company]** — [one-line description]

- **Stage:** [Series X / public / private / bootstrapped]
- **Headcount:** [N]
- **Recent news (last 90 days):** [bullets — funding, hires, launches, layoffs. Skip the section if nothing material.]

---

## Signal recap — why this meeting exists

**Original signal ([type], captured [date]):**
[2-3 sentences on the specific signal and why it qualified.]

**Outreach sequence:**
- [Date] · Touch 1 — [one-line summary, NOT verbatim]
- [Date] · Touch 2 — [one-line summary]
- [Date] · Reply received — [one-line summary]
- [Date] · Booked.

**Time from signal to booking:** [N days]

---

## What they actually said in their reply

> [verbatim reply — pasted from sent-log]

**Read it carefully.** [1-2 sentences of analysis: what they're prioritizing, what they're skeptical of, what language they use. This is the most important section of the brief.]

---

## Talking points (3)

Each grounded in either the signal, their reply, or the company context. Don't pad to three if you only have two real ones.

1. **[short title]** — [2-3 sentence elaboration. Specific to this contact, not generic.]
2. **[short title]** — [...]
3. **[short title]** — [...]

---

## Questions to ask them (2)

The point is to learn what's *actually* driving the buying signal — context the messages couldn't give you.

1. **[question]** — [one-line: why this question, what you're trying to learn]
2. **[question]** — [...]

---

## Likely objections + responses

For each, anticipate based on signal type, company stage, and what they said in their reply.

1. **"[likely objection]"** → [your response — short, direct, no hedging]
2. **"[likely objection]"** → [...]
3. **"[likely objection]"** → [...]

(Skip section if the conversation is genuinely warm — direct-intent signals where they reached out *to* you sometimes have no objections to anticipate.)

---

## Soft next step (if call goes well)

[1-2 sentences: what's the natural step after this meeting? Send a teardown? Free trial? Intro to their CTO? Don't try to close on the call — set up the next step.]

If it goes well: [suggest the close]
If it's lukewarm: [suggest the holding pattern]
If it's a no: [suggest the long-tail follow-up — quarterly value-share, relevant intros, etc.]

---

## Vibe check

[1-2 sentences. What's the tone you should bring? Match the signal type + their reply tone. E.g., "They replied short and direct — meet them there. Don't open with small talk." or "Their reply was warm and curious — fine to open with 30 seconds of genuine catch-up before diving in."]

---

## What you're NOT going to do

[1-2 sentences on traps to avoid. E.g., "Don't pitch the full agency offer — they signaled interest in a teardown. Stay narrow." Or "Don't quote price unless they ask — this is discovery, not negotiation."]

This part is short and surgical. Skip if nothing comes to mind.
```

## Step 5: Output + save

Output the brief to the user in chat.

Also save it to `<config-root>/relationships/briefs/SIG-[id].md` so it's archived. If the `briefs/` directory doesn't exist, create it.

## Step 6: Offer post-call follow-up

End with:

> "After the call, log how it went with `/touchpoint SIG-[id] [reply / booked / dead]` — and if there's a clear next step, I can draft the follow-up message that locks it in. Just ask."

## Quality gate

Before output, re-read your draft and ask:

1. Is *anything* in this brief generic enough that you could swap the contact's name and have it still apply? If yes, that section is filler — cut it or rewrite with specifics.
2. Did you actually use what they said in their reply? Or did you ignore it and write the brief from the signal alone? The reply > the signal — it's the most recent and most direct data point.
3. Are the talking points + questions + objections grounded in *this contact*, not in the user's offer? The brief is about *them*, not you.

If any answer is shaky, rewrite the relevant section before showing the user.
