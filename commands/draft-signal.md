---
name: draft-signal
description: >
  Draft the 3-touch DM sequence (opener + 2 follow-ups) for a captured signal, in the user's voice. Reads the signal context from the pipeline, applies the user's voice rules and value-adds, and outputs copy-paste-ready messages with timing. Use after /capture-signal or /pull-signals. Accepts a SIG- ID as an argument or asks which signal to draft for.
---

# /draft-signal — write the DMs

You are drafting outreach messages for a signal already captured in the pipeline. Your job: produce a 27-word opener + two follow-ups that sound like the user wrote them.

## Step 0: Preflight

Read all of:

- `<config-root>/plugins/growth.user-context.md`
- `references/signal-voice-rules.md`
- `<config-root>/relationships/pipeline.md`
- `<config-root>/relationships/sent-log.md`

If `user-context.md` is missing or placeholder, stop and tell the user to run `/setup-relationships`.

### Soft warming check

Look at the SIG entry. If there's no `**Warming:**` field and no `**Connection request:**` field, the user is going straight to DM without warming. That's fine for hot signals (Direct intent, recent High-priority) but suboptimal for everything else. Mention it once, briefly, then proceed:

> "Heads up — no warming logged for this signal. For job-change / funding / engagement signals, warming first (`/warm-signal SIG-[id]`) typically lifts reply rates by 1.5–2x. Want to do that first, or proceed with the DM now?"

If the user says "proceed", continue. If they say "warm first", run `/warm-signal` instead. Don't nag — ask once, accept the answer.

## Step 1: Identify the signal

If the user passed a `SIG-` ID with the command, use it. Otherwise:

- Show them a numbered list of all `new` and `drafted` entries in the pipeline (limit to 10 most recent) and ask which one.
- If only one is `new`, default to that one.

If a SIG-ID is passed but doesn't exist, say so and list the available IDs.

## Step 2: Decide which touch you're drafting

Check `sent-log.md` for entries tagged with this SIG-ID:

- **No prior touches:** you're drafting Touch 1 (opener) + 2 follow-ups (full sequence).
- **Touch 1 already sent:** you're drafting just Touch 2 (the user is asking for the follow-up).
- **Touch 2 already sent:** drafting just Touch 3 (breakup).
- **Touch 3 already sent:** the cadence is done. Don't auto-draft a Touch 4. Ask the user if they want to start a new sequence or close the signal.

## Step 3: Draft Touch 1 — the 27-word opener

Use the four-sentence pattern from `voice-rules.md`:

1. **Hook** — name the signal specifically. The contact must read sentence one and think "yes, that's literally what I just did."
2. **Resonance** — show you understood the substance. *Not* "great post!" *Not* "I loved your insight."
3. **Bridge** — connect their thing to your offer in one sentence. Don't pitch.
4. **Light ask** — low-friction, specific, easy to say yes to. Not "30 minutes." More like "want me to send the teardown?" or "worth a 5-min thread?"

Hard rules (enforce strictly — re-read your draft and fix):

- **Length:** target 27 words; hard cap 40.
- **No banned phrases.** Re-check against the bans in `voice-rules.md` AND in `user-context.md`. Common offenders: "just checking in", "circling back", "hope this finds you well", "quick question", "I noticed", "wanted to hop on a call", "I'd love to", "exciting opportunity".
- **No "Dear [Name]" / "Hi [Name],"** — LinkedIn DMs don't open like that. Start with the hook.
- **No emoji** unless the user's voice samples in `user-context.md` show they use them.
- **Match the user's tone setting** from `user-context.md` (warm-professional / casual-peer / direct-operator / formal-executive). When in doubt, lean shorter and blunter.
- **Reference the actual signal detail** — pull the specific quote / fact / role from the pipeline entry's "Signal context."

If the contact has prior history (from the pipeline's "Prior history" field), the opener changes: skip the hook formality and *reference the prior context* explicitly. "Last time we talked you were on the hunt for X — saw your comment about Y, looks like that's still live."

## Step 4: Draft Touch 2 — value-add follow-up

Send 3–7 days after Touch 1 (per `user-context.md` cadence).

Rules:
- **DO NOT** say "following up", "circling back", "just bumping this", "wanted to check in".
- **Lead with new value.** Pick one value-add move from the user's list in `user-context.md`. Examples: a relevant link, a stat, a teardown offer, a 1-line insight, an intro.
- **Reference Touch 1 obliquely** — "Forgot to mention…" or "One more thing — …" or just dive in.
- **Length:** 35–60 words. Slightly longer than the opener because you're delivering value.
- **Soft re-ask** at the end. Same low-friction CTA family as Touch 1, framed differently.

## Step 5: Draft Touch 3 — the breakup

Send 7–14 days after Touch 2.

Rules:
- **Acknowledge the silence honestly.** "I'll stop here" / "Closing the loop on this one" / "Last note from me."
- **Leave the door open.** "If [signal] becomes more pressing, hit me up."
- **No guilt-trip.** No "I assume you're not interested." No "I'll take your silence as a no."
- **Length:** 25–40 words. Short, clean, polite.
- **The breakup often pulls the most replies.** Don't phone it in.

## Step 6: Output

Use this exact format:

```markdown
## SIG-[id] — DM sequence

**Contact:** [name], [title] @ [company]
**Signal:** [signal type] — [one-line context]

---

### Touch 1 — opener (send: [date])

[the DM, copy-paste-ready, no markdown formatting inside]

*Word count: [N] · Why this lands: [one-line note on signal + angle]*

---

### Touch 2 — value-add (send: [date])

[the DM]

*Word count: [N] · Value-add used: [which move from user's list]*

---

### Touch 3 — breakup (send: [date])

[the DM]

*Word count: [N]*

---

When you've sent each one, log it with `/touchpoint SIG-[id] sent [touch-number]`.
If they reply, run `/touchpoint SIG-[id] reply` and we'll handle it from there.
```

## Step 7: Update the pipeline

Update the SIG entry in `<config-root>/relationships/pipeline.md`:

- Status: `new` → `drafted`
- Cadence section: replace `[pending]` for each touch with the actual draft, dated.

## Quality gate (don't skip)

Before showing output, re-read every draft and ask:

1. Could a competitor copy-paste this and have it land for them? If yes, it's too generic — rewrite with more signal-specific detail.
2. Does Touch 1 reference the *specific* thing they posted / did, in the first sentence? If not, fix it.
3. Are there any banned phrases? Search literal strings.
4. Does it sound like the voice samples in `user-context.md`, or like ChatGPT? If ChatGPT-y, rewrite with shorter sentences, fewer hedges, and at least one piece of specific texture (a number, a name, a moment).

Only output when all four gates pass.
