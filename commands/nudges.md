---
description: Daily check for things that went quiet. Finds open deals with no activity for 15 days, emails to clients or prospects that got no reply, and follow-ups you said you would send and have not. Drafts a check-in for each and stages them for review in /morning. Never sends and never changes a deal. Designed to run unattended once a day; also runs on demand.
---

# /nudges [--dry-run]

Finds what slipped because nothing prompted you, and prepares the next step. It only
prepares: every result is a staged item with a draft. Sending a draft or changing a deal
is high risk under the autonomy policy and happens only when you approve that item.

Spec: nucleus `docs/proposals/sweep-heartbeat.md`. File formats: nucleus
`docs/contracts.md`, "Nudges".

---

## Step G — Config-root guard (run first)

Run cortex's `python3 scripts/cortex_cli.py root-status`. If it exits non-zero, **stop** and show its sentence verbatim; write nothing anywhere else and do not ask for folder access more than once per session. Exception: in a remote session with the sync repos attached, run cortex's documented `bootstrap` once and re-check before stopping.

If cortex is not installed, the checks can still run but nothing can be staged: run
Steps 1 to 4, show the results in chat, say "Not staged: cortex is not installed", and
stop.

## Step 0 — Thresholds, identity, sync

1. If the root is a synced checkout, run cortex's `cortex_cli.py sync` before reading.
2. Read thresholds:
   `python3 scripts/nudge_check.py parse-triggers <config-root>/plugins/growth/triggers.md`.
   A missing file means the defaults (15 days, 5 business days, 7 days). Do not create
   the file; `references/triggers.template.md` is the starter if the user wants one.
3. Read the Actor ID from `<config-root>/memory/me/identity.md`. If there is none, use
   `unresolved` and say so in the output.
4. Read the ledger, `<config-root>/memory/staged/nudges/ledger.jsonl`, if it exists.

## Step 1 — Gather (read-only)

Skip any trigger that is turned off. A missing connector skips that trigger for this
run: record `skipped: <trigger> — <connector> not connected` and continue.

**Open deals (`stale-deal`).** From the CRM, list every open deal (not closed-won, not
closed-lost). For each take its record ID, name, and **last activity date**: the latest
of the last logged email, call, meeting, note, or task, and the date it entered its
current stage. Do not use a generic "last modified" timestamp on its own; automated
property updates move it. Look up which activity-date properties the CRM exposes before
relying on a name. If no activity date can be found for a deal, leave it out and count
it under `skipped`.

**Sent with no reply (`no-reply`).** From mail, find threads from the last 45 days where
the most recent message is yours, it went to a person, and no one has replied since.
Keep a thread only if the recipient is a client or prospect: they have a page under
`memory/person/`, `memory/client/`, or `memory/bizdev/`, or are a contact on an open
deal. Leave out a message that does not expect an answer (a thank-you, a
confirmation, an FYI). Take the thread ID, subject, and the date you sent it.

**Owed and not sent (`owed-follow-up`).** From memory, read `## Open threads` on active
client, bizdev, and person nodes. Keep an item only if it is something **you** owe (not
tagged `[WAITING:...]`) **and** it is a message or deliverable to send to a named
person: send, reply, follow up, share, email, intro. Internal to-dos are not nudges. For
each take a stable ID (`<node-path>#<first six words, hyphenated>`), a one-line summary,
`due` (an explicit date in the item, else none), and `created` (the date in its
priority tag or `[confirmed:...]` tag, else the node's last changelog date). Never
invent a date: an item with none is left out.

## Step 2 — Decide what to flag

Build one JSON object and pass it to the script on stdin. Do not do the date arithmetic
or the "already flagged" check yourself.

```
python3 scripts/nudge_check.py check
```

```json
{
  "today": "<YYYY-MM-DD in the user's time zone>",
  "now": "<ISO-8601 timestamp>",
  "actor": "<actor id>",
  "thresholds": { "...from Step 0..." : {} },
  "deals": [{"id": "<record id>", "name": "<deal name>", "last_activity": "<date>", "source": "crm:<record id>"}],
  "threads": [{"id": "<thread id>", "subject": "<subject>", "last_sent": "<date>", "source": "mail:<thread id>"}],
  "commitments": [{"id": "<stable id>", "summary": "<one line>", "due": null, "created": "<date>", "source": "<memory path>"}],
  "ledger": [ "...each ledger line as an object..." ]
}
```

It returns `nudges` (what to flag, in order), `ledger_append` (lines to record),
`skipped` (with reasons), and `summary`. Use exactly that list. Do not add an item the
script did not return, and do not drop one because it looks unimportant.

## Step 3 — Draft

For each nudge, draft the message that would move it:

- `stale-deal`: a short check-in to the deal's main contact, grounded in the last real
  exchange and the deal's next step in memory. No "just checking in" with nothing else.
- `no-reply`: a brief follow-up on the same thread that makes replying easy.
- `owed-follow-up`: the message you said you would send, if memory holds enough to
  write it. If it depends on something only you have (an attachment, a decision), write
  `Draft: none — needs <what>`.

Use the voice rules in `<config-root>/memory/me/voice.md`. Do not invent facts, prices,
dates, or commitments. Do not judge the deal: never suggest closing it, and never
propose a stage change.

With more than 10 nudges for one trigger, draft the 10 that have been quiet longest and
write `Draft: none — not drafted this run` for the rest.

## Step 4 — Stage (skipped with `--dry-run`)

1. Write the day's file with cortex's
   `python3 scripts/cortex_cli.py write-file --memory-root <config-root>/memory staged/nudges/<today>.md -`:

   ```markdown
   # Nudges — <today>

   Generated by /nudges at <ISO timestamp> for <actor id>.
   <total> items: <a> quiet deals, <b> with no reply, <c> owed. Skipped: <reasons or "none">.

   ### Nudge 1 — <subject>
   - **Trigger:** stale-deal | no-reply | owed-follow-up
   - **Key:** <key from the script>
   - **Quiet since:** <date>
   - **Days quiet:** <n> <days | business days>
   - **Source:** <source>
   - **Draft:**
     > <the drafted message, or "none — <why>">
   ```

   Re-running on the same day replaces that day's file.
2. Append each line in `ledger_append`, unchanged, as one JSON line, with cortex's
   `cortex_cli.py append-line --memory-root <config-root>/memory staged/nudges/ledger.jsonl '<json>'`.
   If the day's file could not be written, append nothing.
3. If nothing was flagged, write no file and append nothing.
4. If the root is a synced checkout, run `cortex_cli.py sync`. A failed sync is a failed
   run.

## Step 5 — Receipt and report

When run from a schedule, write one receipt with cortex's `cortex_cli.py write-receipt`
(`--schedule daily-nudges`, `--outcome succeeded | partial | failed`, and
`--extra '{"counts": {"stale-deal": 0, "no-reply": 0, "owed-follow-up": 0, "skipped": 0}}'`).
`partial` means a source was skipped.

Print one line: `/nudges <today>: <total> staged (<a> quiet deals, <b> no reply, <c> owed); skipped: <reasons or none>. Review in /morning.`
Run interactively, also show the list with its drafts.

---

## Behavior rules

- **Never sends, never changes a deal, never edits a memory node.** It writes only the
  day's nudges file, ledger lines, and a receipt.
- **No interactive prompts when scheduled.** Problems go in the summary line and the
  receipt.
- **The script decides what is flagged.** Thresholds, business days, and repeats are
  not judgment calls.
- **Degrade, do not fail.** One missing source skips one trigger.
- **Private.** Deal names and message drafts stay in `memory/staged/`, which syncs
  through the private repository only. The receipt holds counts, never names.

## What this is not

- Not the daily relationship brief. `/relationships` ranks who to reach out to;
  `/nudges` only catches what has already gone quiet.
- Not a pipeline review. It says a deal is quiet; whether to keep pursuing it is yours.
