---
description: Lightweight ad-hoc relationship logging from natural language. "I had a great catch-up with Sang, he's connecting me to two folks at NationSwell." Updates the person page's Recent Interactions log, sets Last meaningful contact, optionally appends a generosity_ledger entry, optionally proposes intent/tier shift if the touch signals a change. Drafts only — never sends. Lower friction than /relationships-action for the "I just did this and want to capture it" flow.
---

# /touchpoint

The fast capture command for "I just did something with this person and want to log it." Distinct from `/relationships-action` (which records an action on a brief option's structured event) — `/touchpoint` is for free-form ad-hoc updates that don't necessarily come from a brief.

## When to use

- "I had a great catch-up with Sang, he's connecting me to two folks at NationSwell"
- "Just texted my brother — he's coming for dinner Sunday"
- "Had a call with Charity, she asked for the PRB feedback by EOD Wednesday"
- "Quick LinkedIn comment on Rob's latest post"

Not for:
- Bulk relationship tagging (use `/network-rebalance`)
- Surfacing daily priorities (use `/relationships`)
- Acting on a brief card (use `/relationships-action`)
- Drafting outreach (use `/draft-touchpoint`)

---

## Step 0 — Preflight

Read `<config-root>/plugins/relationships.user-context.md`. If missing → route to `/setup-relationships` and stop.

---

## Step 1 — Parse the touchpoint

The user invokes via:

### A. Natural-language utterance (skill-triggered)

```
"I had a great catch-up with Sang"
"Texted my brother about dinner Sunday"
"Just commented on Charity's LinkedIn post"
```

Parse out:
- **Person reference** — fuzzy match against `<config-root>/memory/person/*.md`. If ambiguous (e.g., "Sarah" with multiple Sarah pages), surface candidates and ask which.
- **Channel** — infer from verbs/context: "catch-up" → call or meet; "texted" → text; "commented" → comment; "DM'd" → linkedin_dm or instagram_dm; "emailed" → email. If unclear, ask.
- **Direction** — Zach to them (outbound) by default. If the utterance is "she reached out," "he called me," → inbound.
- **Summary** — the rest of the user's sentence (the "what happened").
- **Date** — default to today_local. If user says "yesterday," "Thursday," parse accordingly.

### B. Explicit invocation

```
/touchpoint <person-slug> [--channel=<channel>] [--date=<YYYY-MM-DD>] [--direction=in|out] [--summary="..."]
```

Skip parsing; use args directly.

### C. Resolution failures

- **No matching person page** — surface "No person page for '[name]' found. Want to (a) create a new page via cortex `/remember`, (b) confirm a different slug, (c) skip?" Don't silently no-op.
- **Multiple matches** — list the candidates with last meaningful contact dates; user picks.
- **Channel ambiguous and no fallback** — ask "What channel? (call / text / email / linkedin_dm / instagram_dm / comment / meet)"

---

## Step 2 — Detect signal-of-change

Before writing, check whether this touchpoint signals a tier/intent shift. Cheap-tier classifier (Haiku-class):

1. **Read the current `relationships:` frontmatter** on the target person page.
2. **Compare the touchpoint to the current intent + tier:**
   - `intent: awaiting_reply` + touchpoint is a reply landing → propose shift to `drive_active` or `reciprocal` (depending on direction + tone).
   - `tier: operational + intent: keep_warm` + touchpoint is substantive (long meeting, deal context, multiple commitments) → propose promotion to strategic + intent shift.
   - `tier: strategic + intent: drive_active` + touchpoint is the goal closing (e.g., "deal signed") → propose shift to `client_delivery` or `keep_warm` per context.
   - `tier: inner` + touchpoint is light (1-min text) → no shift; expected behavior.
3. **If a shift is suggested**, surface inline AFTER the write:
   > "Touchpoint logged. Pattern note: Sang shifted from `awaiting_reply` to a real-conversation state. Promote intent → drive_active? (y / n / later)"

Best-effort only. False positives are fine — the user can ignore. The point is to keep the schema fresh without forcing a `/network-rebalance` run.

---

## Step 3 — Write to the person page

Append to the page's `## Recent Interactions` section (creating the section if missing):

```
- [YYYY-MM-DD] <channel> — <summary>
```

Update **Last meaningful contact** in the Relationship section:
```
- **Last meaningful contact:** YYYY-MM-DD (<channel>)
```

If the page has `relationships:` frontmatter with `next_touch_target`, recompute:
```
new_next_touch_target = today + (cadence_days_override or tier_cadence_days)
```

Update the frontmatter field.

**Idempotent against same-day repeats:** if the same `(date, channel, summary)` already exists in Recent Interactions, skip (don't double-log).

---

## Step 4 — Optional: generosity_ledger entry

If the touchpoint involves explicit giving (an intro made, a share, a referral, a piece of advice given) OR receiving (they introduced you, they shared, they gave a referral), prompt:

> "Log this as a generosity_ledger entry? Direction: gave / received? (y to add, n to skip, edit to specify)"

Default: skip (don't proliferate ledger entries from routine touches). Add only when there's a clear give/receive signal.

On `y`, append to the page's `relationships:` frontmatter `generosity_ledger:` array:
```yaml
generosity_ledger:
  - date: YYYY-MM-DD
    direction: gave | received
    note: "<short string from touchpoint summary>"
```

Cap the ledger at 20 entries (oldest dropped — rolling window).

---

## Step 5 — Append to relationships events log (v0.2.2 unified shape)

Append to `<config-root>/relationships/events.jsonl`. Uses the v0.2.2 unified shape (harmonized with `/relationships-action`):

### Step 5.0 — Ensure directory exists (v0.2.2+)

```
mkdir -p <config-root>/relationships/
```

Idempotent — silent on existing. Prevents silent failure when `/touchpoint` is the first relationships-plugin write on a fresh install.

### Step 5.1 — Compose the event

```json
{
  "schema_version": "0.2.2",
  "ts": "<ISO 8601 with timezone>",
  "brief_id": null,
  "option_id": null,
  "person_slug": "<slug>",
  "bucket": null,
  "channel": "<channel>",
  "action": "touchpoint",
  "notes": "<user's summary — truncated to fit 4KB cap; see Step 5.2>",
  "meta": {
    "direction": "in" | "out",
    "intent_at_time": "<intent value from frontmatter>",
    "tier_at_time": "<tier value from frontmatter>",
    "source": "natural-language" | "explicit-args"
  }
}
```

**Shape unification rationale (v0.2.2 fix):**
- `notes` is the canonical user-supplied-text field. Same key `/relationships-action` uses. UI readers see `event.notes` regardless of which command produced the event.
- `meta` nests touchpoint-specific extensions so v0.1.x readers (which don't know about `meta`) ignore it gracefully.
- `schema_version` lets readers gate compatibility. v0.2.0 events lacked this field; readers must default to "0.2.0" when missing.
- `action: "touchpoint"` extends the existing enum `copied | sent | skipped | snoozed`. UI readers should accept unknown `action` values gracefully (treat as a generic logged event).

### Step 5.2 — Enforce atomic-append safety (v0.2.2+)

The events.jsonl file is appended by THREE writers (`/touchpoint`, `/relationships-action`, `/relationships` Step 7). POSIX `O_APPEND` writes are atomic ONLY when the write is ≤ `PIPE_BUF` (typically 4096 bytes on macOS and Linux). Longer writes can interleave under concurrent access and corrupt the JSONL.

```
event_json = serialize event with newline appended
if len(event_json) > 4000:   # safety margin under 4096
  Truncate `notes` so the total event_json stays ≤ 4000 bytes.
  Append "[truncated — see person page Recent Interactions for full summary]" marker to notes.
  Re-serialize and verify size.

# Use O_APPEND open mode (bash `>>` does this by default; in Python: open(path, "a"))
# Single write call (not multiple write() calls — they're not atomic across calls)
append event_json to events.jsonl
```

The full unredacted summary lives on the person page's `## Recent Interactions` section (already written in Step 3). The events.jsonl stays atomic-safe for downstream analytics.

Append-only. Same file as `/relationships-action`'s event log — gives a UI a unified action stream regardless of where the action originated.

---

## Step 6 — Log to cortex log.md

Invoke `log-writer` if available:

```
## [YYYY-MM-DD HH:MM] /touchpoint | <slug> — <channel> — <summary first 60 chars>
```

---

## Step 7 — Confirm + maybe prompt shift

Render confirmation:

```
✓ Touchpoint logged for Taylor Diaz (call, today).
  Updated: Recent Interactions, Last meaningful contact, next_touch_target.
  Events log: 1 entry appended.

  Pattern: Taylor's intent was `advising` (compatible with the touchpoint).
  No shift suggested.
```

If a shift IS suggested (per Step 2), append:

```
  ⚠ Pattern note: this touchpoint suggests `intent` may need updating.
    Current: tier=strategic + intent=advising
    Suggested: shift intent → reciprocal (substantive two-way exchange)
    Apply? (y / n / later — defer 7 days)
```

On `y` → update the frontmatter intent field. On `n` → no change. On `later` → log to `<config-root>/memory/staged/skip-logs/touchpoint-shifts.md` for re-surface in 7 days.

---

## Behavior rules

- **Drafts only.** Never sends, never modifies CRM, never creates calendar events. Just logs to memory.
- **Additive writes only** to the person page. Never overwrites Identity, Notes, or non-Relationship sections.
- **Idempotent same-day repeats.** Won't double-log the same touchpoint within a session.
- **Free-form summary preserved verbatim.** Don't editorialize the user's words into "smoothed" prose — log exactly what they said. Closes the user.md observation from 2026-05-18 ("notes sections must reflect what the user actually said").
- **Pattern-shift suggestions are opt-in.** Default behavior is just-log. Shift prompts only surface when the heuristic is high-confidence.

---

## Edge cases

- **Person page is in `team/`** — surface "That person is in team/ (internal team member, not subject of relationship maintenance). Log to their team/ page anyway? (y/n)" If y, append to the team/ page Recent Interactions but skip Last meaningful contact (team/ doesn't track that). Don't trigger pattern-shift detection (intent N/A for team).
- **Person page doesn't exist (net-new contact mentioned)** — offer `/remember` to create a new person page first; resume touchpoint after.
- **User invokes /touchpoint in the middle of /relationships brief review** — DO NOT silently apply. Surface "You're in a brief review — applying touchpoint won't affect today's surfaced cards. Continue? (y/n)" If yes, log and return to brief.
- **Direction unclear** — default to outbound; the user can correct.
- **Pattern-shift suggests demotion (e.g., shift to keep_warm)** — be careful. Demotions are user judgment. Surface as "consider" not "should." Default decline.
- **events.jsonl write fails** (disk full, permissions) — log to user but still write the person page (the page is canonical; the events log is analytics). Re-attempt event-log write on next /touchpoint or /relationships-action.
