# UI integration contract

The `relationships` plugin produces a structured `today.json` artifact and consumes structured event payloads. This doc is the contract for whoever builds a UI on top — whether that's a Next.js + Supabase web app, the Operator desktop app (`docs/proposals/jarvis-app.md`), a future mobile-first PWA, or a third-party tool.

**Schema version:** `0.1.0`. Read `today.json`'s `schema_version` field on every load; if it's a major-version mismatch, render a "schema upgrade required" warning and refuse to act on actions (rendering the brief is still safe).

---

## The contract surface

The plugin commits to three files and one command:

| Path / Command | Direction | Cadence |
|---|---|---|
| `<config-root>/relationships/today.json` | Plugin → UI (read) | Refreshed on every `/relationships` run |
| `<config-root>/relationships/snoozes.json` | UI → Plugin (read) · Plugin (write via `/relationships-action`) | Mutated on snooze action |
| `<config-root>/relationships/events.jsonl` | Plugin → UI (read for analytics) · `/relationships-action` (write) | Append-only |
| `/relationships-action` command | UI → Plugin (write) | Called once per user action |

That's it. No HTTP, no IPC, no auth. Files on a shared volume + a single command.

---

## The "sync daemon" pattern

The plugin is markdown — it doesn't run a server. A UI hosted at Vercel/Supabase needs a bridge. The recommended pattern:

```
┌─────────────────┐     reads        ┌──────────────────┐
│                 │ ───────────────→ │                  │
│  Sync daemon    │   today.json     │   Web app UI     │
│  (Node script   │                  │   (Next.js +     │
│   on operator's │   writes events  │    Supabase)     │
│   machine)      │ ←─────────────── │                  │
│                 │   to inbox/      │                  │
└────────┬────────┘                  └──────────────────┘
         │
         │ invokes
         ↓
   /relationships-action --file=<inbox/uuid.json>
```

**Sync daemon responsibilities:**
1. Watch `<config-root>/relationships/today.json` for changes; mirror to Supabase row when updated.
2. Watch `<config-root>/relationships/inbox/` directory; for each new JSON file, invoke `/relationships-action --file=<path>` via Claude Code CLI or similar.
3. Watch `<config-root>/relationships/events.jsonl` for new lines (tail); mirror to Supabase for UI analytics.
4. Watch `<config-root>/relationships/snoozes.json`; mirror to UI state.

**Default interval:** 50 minutes (as agreed with the user). Watcher mode preferred over polling where filesystem events are available (e.g., `fs.watch` on macOS).

The daemon lives in `<config-root>/relationships/bin/sync-daemon.js` (or similar — out of scope for v0.1.x). The plugin itself does not ship the daemon. v0.1.x UI consumers can build their own using this contract.

---

## today.json — read contract

Full schema in `today-json-schema.md`. The fields a UI cares about most:

### Top-level

```json
{
  "schema_version": "0.1.0",
  "date": "2026-05-28",
  "brief_id": "550e8400-e29b-41d4-a716-446655440000",
  "generated_at": "2026-05-28T07:30:00-04:00",
  "user": { ... },
  "budget_minutes": 30,
  "buckets": [ ... ],
  "carrying": { ... },
  "best_fits_for_budget": [ ... ],
  "warnings": [ ... ]
}
```

**`schema_version`** — MUST be checked. Refuse to act on actions if mismatched.
**`brief_id`** — UUID v4. Use for analytics correlation; include in any event you post back.
**`generated_at`** — ISO 8601 with timezone. Render the "last refreshed" timestamp in the UI.
**`budget_minutes`** — the time budget the brief was generated for. UI should re-fetch a fresh `today.json` if user changes their budget (which means re-running `/relationships`).

### Options (the cards)

Each option has a **stable ID** in the form `<bucket>_<person-slug>_<YYYY-MM-DD>`:

- `new_biz_sarah-chen_2026-05-28`
- `relationship_derek-patel_2026-05-28`
- `network_self-post-monday_2026-05-28`

Use this ID for:
- Correlating across page reloads (same person → same ID)
- Posting actions back via `/relationships-action`
- Tracking "did the user act on this today?" in UI state

Per-card fields the UI renders:
- `person.name`, `person.title`, `person.company` — header
- `person.tier`, `person.icp_fit` — chips/badges
- `why_now` — sub-header (the trigger explanation)
- `channel` — icon + label (see channel enum in schema)
- `time_estimate_min` — small "~5 min" tag
- `draft.body` — main body (monospace recommended for clarity)
- `draft.subject` — only render for email channels (null otherwise)
- `draft.needs_user_touch` — render a yellow border / warning icon if true
- `confidence` — "research-thin" badge when `low`
- `actions.copy_payload` — what gets copied on tap-to-copy (NOT `draft.body` directly; use `copy_payload`)
- `actions.snooze_options_days` — array of integers; render as a dropdown ([1, 3, 7, 30])

### Bucket-level

- `bucket.label` — human-readable header
- `bucket.sub_tabs` — only present on `relationship` bucket when close-personal track is enabled; render as tabs
- `bucket.empty_state_note` — present (non-null) when fewer than 3 options; render below cards

### Top-level carrying

```json
"carrying": { "operational_overdue": 23, "strategic_cooling": 4 }
```

Render as a small footnote: "Quietly carrying: 23 operational overdue, 4 strategic cooling." No call-to-action — this is the "no guilt" surface area.

---

## Posting actions back — write contract (v0.2.2 unified shape)

When the user taps Copy / Sent / Skip / Snooze on a card, write a JSON event to `<config-root>/relationships/inbox/<uuid>.json`:

```json
{
  "schema_version": "0.2.2",
  "action": "copied" | "sent" | "skipped" | "snoozed",
  "option_id": "<from today.json>",
  "person_slug": "<from option_id>",
  "bucket": "<from option_id>",
  "channel": "<from option.channel>",
  "brief_id": "<from today.json>",
  "notes": "(optional, free-form, ≤ 4KB total event size)",
  "meta": {
    "snooze_until": "<YYYY-MM-DD when action: snoozed>",
    "source": "file"
  }
}
```

The sync daemon picks up the file and invokes `/relationships-action --file=<path>`. On success, the file moves to `inbox/processed/`. On malformed payload, it moves to `inbox/quarantine/` with a `.error` sidecar.

**Atomicity tip:** write to `<config-root>/relationships/inbox/.tmp/<uuid>.json` first, then rename into `inbox/<uuid>.json`. Avoids the daemon picking up a partially-written file.

### Touchpoint events (UI is not a writer, but should know the shape)

`/touchpoint` is invoked from natural-language sessions, not via the inbox/ pattern. But the events.jsonl stream will contain `action: "touchpoint"` events that a UI displays in any unified action log. The shape:

```json
{
  "schema_version": "0.2.2",
  "action": "touchpoint",
  "option_id": null,
  "brief_id": null,
  "bucket": null,
  "person_slug": "jordan-diaz",
  "channel": "call",
  "notes": "had a great catch-up; he's intro'ing me to two folks at NationSwell",
  "meta": {
    "direction": "out",
    "intent_at_time": "advising",
    "tier_at_time": "strategic",
    "source": "natural-language"
  }
}
```

UI readers must accept `action: "touchpoint"` gracefully and render `option_id: null` events with a different visual treatment (no "from today's brief card #N" header, no copy-button).

---

## Reading the events stream (v0.2.2 forward-compat rules)

For analytics, the UI reads `<config-root>/relationships/events.jsonl` directly (or via Supabase mirror). Each line is one event. Append-only. Full event shape spec lives in `references/today-json-schema.md` "Events.jsonl shape" section.

### Forward-compat reading discipline

The event shape evolves over plugin versions. UI readers MUST follow these rules to handle mixed-version logs gracefully:

1. **`schema_version` check first.** If missing → treat as v0.2.0 (pre-meta-nesting). If `schema_version` is a NEWER major version than the reader knows → render the event read-only with a "schema mismatch — display only" badge; don't take destructive actions on it.

2. **Action enum is open.** Known actions: `copied | sent | skipped | snoozed | touchpoint`. Future versions may add more (`commented`, `connected`, etc.). Render unknown actions as "logged event" with the event's `notes` content; never crash.

3. **`meta` block is optional.** On v0.2.0 events, `meta` is absent — read `snooze_until`, `late_action`, `source` from the top level. On v0.2.2+, read from `meta.<field>`. Reader should try `meta.<field> ?? <top-level-field>` as the safe pattern.

4. **`option_id == null`** signals a touchpoint event (not tied to a brief card). Render differently — no "from card #N" header, no copy-button, more emphasis on the freeform `notes` content.

5. **Each line is < 4KB** (enforced by writers via atomic-append safety rule). Reader can `readline()` and parse-per-line without worrying about partial reads at chunk boundaries.

### Typical analytics queries

- **"Today so far"** — count events with `ts > today_start`
- **Channel mix** — group by `channel` in last 7 days
- **Response time** — diff between brief `generated_at` and first action's `ts`
- **Snooze patterns** — events where `action: snoozed`, grouped by `bucket` (or by `meta.snooze_until - ts` for snooze-duration analysis)
- **Late actions** — events where `meta.late_action == true` (action on yesterday's brief)
- **Touchpoint cadence** — events where `action: "touchpoint"`, grouped by `person_slug`, plotted over time. Helps surface relationships where the user hasn't logged a touchpoint recently.
- **Reciprocity balance** — touchpoint events grouped by `meta.direction` (in vs out) per person. If outbound count substantially exceeds inbound, the user may be over-investing without reciprocity.

The events log is small (one line per action, typically 200-1000 bytes; capped at 4KB). A year of daily use (10 events/day) stays well under 15 MB.

---

## Snoozes contract

`<config-root>/relationships/snoozes.json`:

```json
[
  { "slug": "sarah-chen", "until_date": "2026-06-04", "reason": "she's traveling", "snoozed_at": "2026-05-28T07:34:00-04:00", "brief_id": "550e8400-..." },
  ...
]
```

- UI reads to display active snoozes ("you snoozed 3 people: ...").
- UI does NOT write directly; goes through `/relationships-action` (which writes here as a side-effect of `action: snoozed`).
- `until_date < today` means expired (kept in file for audit; could be cleaned during a future `/relationships` Step 3 sweep).
- A future "unsnooze" action could be added; for now, snoozes expire by date.

---

## What the UI should NOT do

- **Don't write to `today.json` directly.** It's a snapshot of a brief generation. Replaced wholesale by `/relationships`.
- **Don't modify cortex person pages.** That's the plugin's job via `/relationships-action`.
- **Don't sync events.jsonl back to the local file from the cloud.** It's one-way: local writes → cloud mirror, not the other direction. If the UI is offline-first, the local file is the source of truth; the cloud is a cache.
- **Don't assume Cowork is running.** The plugin is invoked as needed. The sync daemon's job is to bridge the gap.
- **Don't trust unsupported `schema_version` values.** Refuse to act; render the brief read-only if the version mismatch is breaking.

---

## Future-state — not in v0.1.x

- **HTTP shim.** A small Express/Hono server wrapping `/relationships-action` for environments where filesystem access is hard. Not v0.1.x scope.
- **WebSocket push.** Sync daemon could push events to UI in real-time. Currently polling/watching is fine.
- **Multi-user mode.** Plugin is single-user. Multi-tenancy is a Phase 6+ web app concern; the plugin contract stays single-user-on-local-machine.
- **Conflict resolution.** Currently the local plugin is canonical; cloud UI is a view. If UIs ever want to "merge" multiple users' briefs (e.g., a manager seeing their team's), that's a separate proposal.

---

## Reference implementations

When v0.1.x ships and the user is ready for a UI, the reference implementation should:

1. Be a single Next.js app on Vercel + Supabase for state mirror
2. Run a sync daemon as a separate Node process on the operator's local machine
3. Use Supabase Realtime to push state changes to the UI
4. Auth: single-user magic link (out of scope for the plugin; UI's concern)
5. Mobile-first responsive design (PWA installable)

The plugin's contract above is sufficient to build this without changing any plugin code. That's the test of whether v0.1.x is structurally UI-ready: a UI builder should be able to read this doc and have everything they need.
