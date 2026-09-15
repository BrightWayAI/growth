---
description: Record a user action on a relationships brief option — copied / sent / skipped / snoozed. Decoupled from the full /relationships orchestration so a UI (web app, Operator desktop, CLI script) can post events without re-running the daily brief. Appends to events.jsonl, updates cortex person page (when applicable), updates snoozes.json. The structured-state side of the daily flow.
---

# /relationships-action

The action endpoint. Invoked when the user (or a UI on the user's behalf) takes a single action on a brief option. Surfaces the same writes that `/relationships` Step 7 does, but standalone — so it can be called repeatedly throughout the day as the user works through their cards.

## When to use

- **Inline** — user says "I sent that to Sarah" or "snooze the Sam one for 3 days" mid-conversation. Skill detects, invokes this command.
- **From a UI** — a future Next.js / Operator app calls this command (via a sync daemon, CLI subprocess, or direct file write that this command can also consume) when the user taps Copy / Sent / Skip / Snooze on a card.
- **From a CLI script** — for users who want to log actions outside of an interactive session.

Not for: running the full brief (that's `/relationships`). Not for: drafting (that's `/draft-touchpoint`). Single-action only.

---

## Step 0 — Preflight

Read `<config-root>/plugins/growth.user-context.md`. If missing → route to `/setup-relationships` and stop.

---

## Step 1 — Parse the input

The command accepts a JSON event payload, either as an argument string or as a path to a JSON file.

### Accepted input shapes

**A. Inline argument** (interactive use):
```
/relationships-action {"action": "sent", "option_id": "new_biz_sarah-chen_2026-05-28", "channel": "linkedin_dm_cold"}
```

**B. File path** (UI / sync daemon):
```
/relationships-action --file=<config-root>/relationships/inbox/<uuid>.json
```

The UI writes pending events to `<config-root>/relationships/inbox/` (one file per event); this command processes one event per invocation. The sync daemon invokes this command once per inbox file, then moves the file to `<config-root>/relationships/inbox/processed/` on success.

**C. Natural-language phrase** (autonomy: auto mode):
If the parent skill passes "user sent the Sarah Chen card," resolve to the most recent matching option from today's `today.json` and proceed.

### Required fields in the event payload

```json
{
  "action": "copied | sent | skipped | snoozed",
  "option_id": "<bucket>_<slug>_<date>",
  "person_slug": "(derived from option_id if missing)",
  "bucket": "(derived from option_id if missing)",
  "channel": "(derived from today.json if missing)"
}
```

Optional fields:
```json
{
  "brief_id": "<from today.json — auto-resolved if missing>",
  "notes": "free-form user comment",
  "snooze_until": "YYYY-MM-DD or relative like '+7d' — required if action=snoozed"
}
```

If `option_id` doesn't exist in today's `today.json`, surface a warning: "Option ID not found in today's brief. Was this from a previous day? Proceeding with cortex-only side effects."

---

## Step 2 — Resolve full context

Read `<config-root>/relationships/today.json` (current run) for:
- Person details (name, title, company, tier, relationship_class) — for the cortex side-effects
- Channel (if not in payload) — to write a meaningful interactions log entry
- Brief ID — to correlate the event

If `today.json` is older than today's date OR the `option_id` references a different date, this is a "late action" on yesterday's brief or earlier. Still process — just use the previous brief's data and note in the event that it's a late action.

---

## Step 3 — Append to events log (v0.2.2 unified shape)

### Step 3.0 — Ensure directory exists

```
mkdir -p <config-root>/relationships/
```

Idempotent.

### Step 3.1 — Compose the event

Append a single line to `<config-root>/relationships/events.jsonl` (create file if missing):

```json
{
  "schema_version": "0.2.2",
  "ts": "<ISO 8601 timestamp with local timezone>",
  "brief_id": "<from today.json or event payload>",
  "option_id": "<from event payload>",
  "person_slug": "<from option_id>",
  "bucket": "<from option_id>",
  "channel": "<from event payload or today.json>",
  "action": "copied" | "sent" | "skipped" | "snoozed",
  "notes": "<from event payload if present>",
  "meta": {
    "snooze_until": "<from event payload if action=snoozed; else null>",
    "late_action": "<true|false — true if option_id date != today>",
    "source": "inline" | "file" | "natural-language"
  }
}
```

**v0.2.2 shape changes:**
- Added `schema_version` field. Default to "0.2.0" if missing on read (back-compat with v0.1.x and v0.2.0 events).
- Moved `snooze_until`, `late_action`, `source` into `meta` block — harmonizes with `/touchpoint` v0.2.2 event shape. UI readers receiving any v0.2.2 event read `event.meta.<field>`.
- Backward-compat read rule: if `meta` missing, read top-level fields directly (v0.1.x / v0.2.0 events).

### Step 3.2 — Atomic-append safety

The events.jsonl file is appended by THREE writers (`/touchpoint`, `/relationships-action`, `/relationships` Step 7). POSIX `O_APPEND` writes are atomic ONLY when the write is ≤ `PIPE_BUF` (typically 4096 bytes). Longer writes can interleave under concurrent access and corrupt the JSONL.

```
event_json = serialize event with newline appended
if len(event_json) > 4000:
  Truncate `notes` so total stays ≤ 4000 bytes.
  Append "[truncated]" marker.
append event_json to events.jsonl (O_APPEND, single write call).
```

Append-only. Never modify prior entries.

---

## Step 4 — Cortex person-page update (when applicable)

Action-specific behavior:

### `action: copied`
No cortex write. The user copied but hasn't sent yet. Just the events log. If the parent skill confirms a send later, a follow-up `action: sent` event will fire.

### `action: sent`
Cortex side-effects (only if cortex installed):

1. Open `<config-root>/memory/person/<slug>.md`.
2. Append to **## Recent interactions**:
   ```
   <today> — <channel> — relationships brief touch (<bucket>)
   ```
   (Don't double-add if an identical line for today already exists.)
3. Update **Last meaningful contact** in the Relationship section: `<today> ([type: dm / email / call / text / comment])` — derive type from channel.
4. If the page has `relationships:` frontmatter with `next_touch_target`, recompute: `today + tier_cadence_days`. Update the field.

### `action: skipped`
Lighter cortex write. Log to events.jsonl only by default. **Optional** — if user-context has `log_skips_to_cortex: true`, also append a non-canonical "skipped" entry to person page Recent interactions.

### `action: snoozed`
Three writes:

1. Append to `<config-root>/relationships/snoozes.json` (create as JSON array if missing):
   ```json
   { "slug": "<slug>", "until_date": "<resolved date>", "reason": "<from payload notes>", "snoozed_at": "<ts>", "brief_id": "<brief_id>" }
   ```
2. Resolve `snooze_until` if it's relative (e.g., `+7d` → today + 7 days). Default if not specified: 7 days.
3. No cortex write — snooze is a UI-state concept, not a relationship event.

---

## Step 5 — Confirmation output

After all writes succeed, output a tight confirmation:

```
✓ Logged: <action> — <person.name> via <channel>
  - Events log: 1 entry appended (brief_id: <short>)
  - Cortex: <recent-interactions updated | skipped (cortex not installed) | skipped (action does not trigger cortex)>
  - Snoozes: <added | n/a>

  Next: this person's next_touch_target is now <date>.
```

If invoked via `--file=`, also move the inbox file to `inbox/processed/` after success.

If any write fails, surface the failure clearly and DO NOT move the inbox file (so the sync daemon can retry).

---

## Step 6 — Log to cortex log.md

If cortex `log-writer` skill is available, append a one-line entry to `<config-root>/memory/log.md`:

```
## [YYYY-MM-DD HH:MM] /relationships-action | <action> — <person.slug> · <channel> · <bucket>
```

Otherwise skip.

---

## Behavior rules

- **One event per invocation.** Batch processing happens at the caller level (sync daemon loops). Don't try to be clever.
- **Idempotent on duplicate events.** If the events.jsonl already has an identical event for the same option_id + action + (close timestamp), skip the cortex write but still append to events log. Don't double-log the cortex page.
- **Read-only against today.json.** Don't modify the brief artifact. `today.json` is a snapshot; events are the action stream.
- **Crash-safe.** If a write fails mid-flow, no partial state should be left. Use atomic file writes (write to temp, rename).
- **Privacy.** Events log can contain person names + channels. Treated as sensitive; gitignored at the plugin level (config-root is the user's; covered by cortex's `.gitignore` template).

---

## Edge cases

- **Option ID references a person not in cortex.** Skip the cortex write; still append to events log. Note `"cortex_skipped": "no_person_page"` in the event.
- **Snooze without `until_date`.** Default to 7 days. Surface this in the confirmation.
- **Action on yesterday's brief.** Process normally. Flag `late_action: true` in the event so analytics can surface late-completion patterns.
- **`person_slug` mismatch with option_id.** Trust `option_id`; warn if mismatched.
- **Cortex log-writer skill missing.** Skip silently; the local events.jsonl is the canonical log anyway.
- **inbox/ file is malformed JSON.** Move to `inbox/quarantine/` with a `.error` sidecar file describing the parse failure. Don't crash the sync daemon's loop.

---

## File layout

```
<config-root>/relationships/
  today.json                   # current brief (overwritten each /relationships run)
  today.md                     # human-readable brief snapshot
  <YYYY-MM-DD>.json            # date-stamped copy
  <YYYY-MM-DD>.md
  events.jsonl                 # append-only event log (canonical action stream)
  snoozes.json                 # active + expired snoozes (persistent state)
  inbox/                       # UI / sync daemon drops pending events here
    <uuid>.json
  inbox/processed/             # /relationships-action moves files here after success
  inbox/quarantine/            # malformed inbox files end up here
  templates/                   # optional user template overrides (loaded preferentially)
```

The `inbox/` pattern decouples a future UI from this command: the UI writes a JSON file; the sync daemon polls and calls `/relationships-action --file=<path>`. No HTTP, no IPC — just files on a shared volume.
