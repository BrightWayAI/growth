---
name: connect-signal
description: >
  Draft a LinkedIn connection-request note for a captured signal. Connection requests are not DMs — they're shorter, peer-level, and intentionally don't reference the signal. Use when the contact isn't a 1st-degree connection yet and you need to send a request before you can DM them. Skip if you're already connected.
---

# /connect-signal — connection-request copy

You are drafting the note that goes inside a LinkedIn connection request. This is *not* the DM. Different rules apply.

## Step 0: Preflight

Read:
- `<config-root>/plugins/growth.user-context.md`
- `references/signal-voice-rules.md`
- `<config-root>/relationships/pipeline.md`

If `user-context.md` is missing/placeholder: stop, tell user to run `/setup-relationships`.

## Step 1: Identify the signal

If the user passed a SIG-ID, use it. Otherwise list active SIGs and ask.

If the SIG-ID doesn't exist, list available and stop.

## Step 2: Confirm the contact isn't already connected

Ask the user via AskUserQuestion: "Quick check — are you already connected to [name] on LinkedIn? (yes / no / not sure)"

- **yes** → "Then skip the connection request entirely. Go straight to `/draft-signal SIG-[id]`." Stop.
- **not sure** → "Open their profile. If the button says 'Message', you're connected — skip to `/draft-signal`. If it says 'Connect' or 'Follow', proceed below."
- **no** → continue.

## Step 3: Decide on the note style

Connection requests have stricter constraints than DMs:

- **300-character cap** (LinkedIn enforces this).
- **No links** (they often get blocked / hurt deliverability of the request).
- **Don't reference the buying signal directly.** The signal-specific hook belongs in the DM. The connection request is a peer-level "let's connect" — referencing the signal in a connection request reads sales-y and reduces accept rates.
- **Tone:** lighter than the DM. More like meeting someone at a conference than walking into their office.

There are three patterns that work. Pick whichever fits the contact best:

### Pattern A — Mutual context (best when there's any mutual ground)
> Hey [Name] — [one-line mutual reference: a person, a company, an event, a topic you both post about]. Worth being connected — feel free to ignore the request if it feels random.

Example: *"Hey Sarah — saw we're both Lenny's Newsletter people / both alums of Bain / both deep in the CRO trenches. Worth being connected — feel free to ignore the request if it feels random."*

### Pattern B — No-pretense (best when there's no obvious mutual ground)
> Hey [Name] — no agenda. I follow your posts on [topic] and figured connecting was overdue. If it feels random, hit decline and I'll take the hint.

### Pattern C — Empty (best when the user has a strong profile and the contact is senior)
> Send the request with **no note**.

Counterintuitive but often the highest accept rate. A strong profile with no note reads less template-y than 99% of requests. Use this when the user's LinkedIn profile clearly signals what they do and the contact is the kind of person who gets a lot of requests.

## Step 4: Draft

Pick the pattern that fits, then draft. Use voice samples from `user-context.md` to match the user's casual register (connection requests are *always* casual, even for `formal-executive` tone setting — that tone is for DMs to senior buyers, not for connection-request notes).

Hard checks:
- ≤ 300 characters (count it).
- No banned phrases from `voice-rules.md`.
- Doesn't pitch.
- Doesn't reference the signal.
- Reads like a person, not a sequence step.

## Step 5: Output

```markdown
## Connection request — SIG-[id]

**Contact:** [name], [title] @ [company]
**Pattern:** [A / B / C]

---

**Note to paste** ([N] / 300 chars):

> [the drafted note]

*Why this pattern: [one-line — e.g., "you both post about CRO; gives natural mutual ground without forcing a signal hook"]*

---

**After they accept** (typically 24–48h):

→ `/warm-signal SIG-[id]` — warm them with a comment + 2 likes
   *or*
→ `/draft-signal SIG-[id]` — go straight to DM if you don't want to warm

If they don't accept within 7 days, the request expires from their feed. Move on — non-acceptance is its own signal.
```

If you went with Pattern C (no note), the output is:

```markdown
## Connection request — SIG-[id]

**Contact:** [name], [title] @ [company]
**Pattern:** C — send with no note

---

**Recommendation:** send the request with no note. With your profile + their seniority, an empty request often outperforms any opener you could write.

If you'd rather have a note, run `/connect-signal SIG-[id]` again and I'll pick from Pattern A or B.

---

**After they accept** (typically 24–48h):

→ `/warm-signal SIG-[id]` — warm them with a comment + 2 likes
   *or*
→ `/draft-signal SIG-[id]` — go straight to DM if you don't want to warm
```

## Step 6: Update the pipeline

Add to the SIG entry in `<config-root>/relationships/pipeline.md`:

```
**Connection request:** [drafted | sent (date)] — pattern: [A / B / C]
```

(Status set to `drafted` until the user logs the send via `/touchpoint`.)

## What this command does NOT do

- Doesn't auto-send the request (LinkedIn blocks this).
- Doesn't replace the DM — the DM still gets drafted separately via `/draft-signal`.
- Doesn't try to be clever. The strongest connection request is the one that doesn't try to do too much.
