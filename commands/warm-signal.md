---
name: warm-signal
description: >
  Pre-DM warming sequence. Drafts a substantive comment for one of the contact's recent posts, identifies 2 more posts to like, and queues the DM for 24h later. Warming gets the contact to see your name 2–3 times before the DM lands so it doesn't read cold. Use after /capture-signal or /pull-signals, before /draft-signal. Skip for high-priority direct-intent signals where speed matters more than warming.
---

# /warm-signal — pre-DM warming sequence

You are preparing the user to warm a prospect *before* sending the cold DM. The goal: have the prospect see the user's name 2–3 times in their notification feed in the 24–48 hours before the DM, so the DM lands warm.

## Step 0: Preflight

Read:
- `<config-root>/plugins/relationships.user-context.md`
- `references/signal-voice-rules.md`
- `<config-root>/relationships/pipeline.md`

If `user-context.md` is missing/placeholder: stop, tell user to run `/setup-relationships`.

## Step 1: Identify the signal

If the user passed a SIG-ID with the command, use it. Otherwise, list `new` and `drafted` SIGs from the pipeline and ask which one (AskUserQuestion).

If the SIG-ID doesn't exist, list available IDs and stop.

## Step 2: Decide whether to warm at all

Read the SIG entry. Apply this filter:

- **Skip warming entirely** if any of:
  - Signal type is **Direct intent** (Signal #7) — they asked a question; reply fast, before someone else does.
  - Priority is High *and* the signal is < 24 hours old — speed beats warming.
  - The contact has prior history with the user (per the SIG entry's "Prior history" field) — warming a prior connection feels weird.

If skipping: tell the user "Skipping warming for SIG-[id] — [reason]. Go straight to `/draft-signal SIG-[id]`." and stop.

- **Warm** in all other cases.

## Step 3: Get the contact's recent posts

The user needs to identify 3 of the contact's recent posts. Two paths:

### If the contact's LinkedIn URL is in the SIG entry
Tell the user:

> "I need 3 of [name]'s recent posts (last 30 days) to warm them. Open their LinkedIn at [URL], scroll their Activity tab, and paste me the **3 most recent substantive posts** — title or first line is enough for each. Skip pure reshares without commentary."

### If no LinkedIn URL
Ask: "What's [name]'s LinkedIn URL? I need it to identify 3 of their recent posts for warming."

Then proceed as above.

## Step 4: Pick the comment target

Of the 3 posts the user pasted, pick the one most aligned with the user's offer / expertise. Criteria:

- **Best:** the post is in the user's lane — they have a real, substantive take. Their comment will read as expert peer commentary.
- **Good:** the post is adjacent — they can ask a thoughtful follow-up question.
- **Avoid:** posts that are purely personal (career milestones, kid photos, life events). A comment there reads transactional.

If none of the 3 fit, tell the user: "None of those three are great targets. Want to try 3 more recent posts? Or skip warming and go straight to `/draft-signal`?"

## Step 5: Draft the comment

The comment is *not* a DM. It's a public comment on LinkedIn. Different rules:

**Do:**
- Add a real take, a counter, a "yes, and…", or a thoughtful question.
- Reference a specific point in the post (not "great post!").
- Sign-off optional — match the user's voice samples in `user-context.md`.
- Length: 25–60 words. Substantial enough to register; short enough not to seem desperate.
- Sound like a peer, not a follower.

**Don't:**
- Pitch anything. Comment is value-only — the DM is where the soft pitch lives.
- Mention the user's company / offer. The contact will see your profile if they want to know who you are.
- Say anything performative ("loved this", "100%", "🔥", "this hit different"). Cringe.
- Use any banned phrase from `voice-rules.md`.
- Plug a link unless it's directly relevant and not promotional.

If the user's tone setting is `casual-peer` or `direct-operator`, lean shorter and blunter. If `formal-executive`, a single thoughtful sentence is often best — full punctuation, no abbreviations.

## Step 6: Output

Use this format:

```markdown
## Warming sequence — SIG-[id]

**Contact:** [name], [title] @ [company]

---

### 👍 Like these 2 posts (no comment)

1. [post title or first line — paste link if you have it]
2. [post title or first line]

(*Just hit like. Don't comment on these — we want signal of interest, not noise.*)

---

### 💬 Comment on this post

**Post:** [the post title / first line / link]

**Comment to paste:**

> [the drafted comment, copy-paste-ready]

*Why this works: [one-line note on what the comment does — adds a take, asks a question, etc.]*

---

### 📅 Then DM

Send the DM **24 hours after** the comment. By then their notification feed has shown your name 2–3 times.

When you're ready: `/draft-signal SIG-[id]`

DM target date: [today + 1 day]
```

## Step 7: Update the pipeline

Update the SIG entry in `<config-root>/relationships/pipeline.md`:

- Add a new section under the entry: `**Warming:** comment drafted [date] · DM target: [date+1]`
- Push back the Touch 1 target date by 1 day (so it's after the warming).

## Step 8: Reminder to user

End with: "Don't forget — warming only works if you actually do it. Open LinkedIn now, hit the 2 likes + paste the comment, then come back tomorrow for `/draft-signal`."

Resist over-engineering. Warming is dead simple in execution; the user just needs the artifacts to copy and the timing to follow.
