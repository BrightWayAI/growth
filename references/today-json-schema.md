# `today.json` schema

The structured artifact produced by `/relationships` after each daily brief run. Written to `<config-root>/relationships/today.json` (and a date-stamped copy at `<config-root>/relationships/<YYYY-MM-DD>.json`).

This is the **stable contract** that downstream surfaces depend on — a future Next.js web app, the Operator desktop app, daily-brief tight-coupling, and any third-party reader. Treat it like a public API.

## Versioning

The JSON includes a `schema_version` field at the root. Backward-incompatible changes bump the major version; additive (new optional fields) bumps minor.

Current schema version: **`0.1.0`**.

## Top-level shape

```json
{
  "schema_version": "0.1.0",
  "date": "2026-05-28",
  "brief_id": "550e8400-e29b-41d4-a716-446655440000",
  "generated_at": "2026-05-28T07:30:00-04:00",
  "user": {
    "name": "Jane Doe",
    "first_name": "Jane",
    "company": "Acme Consulting",
    "one_liner": "AI-powered workflow automation for professional services"
  },
  "budget_minutes": 30,
  "budget_mode": "default | variable | override",
  "quarter_focus": "Q3 anchor accounts",
  "quarter_target": "2 Phase-1 anchors signed and onboarded",
  "buckets": [
    { /* see Bucket shape */ }
  ],
  "carrying": {
    "operational_overdue": 23,
    "strategic_cooling": 4,
    "inner_overdue_not_surfaced": 0,
    "personal_overdue_not_surfaced": 2
  },
  "best_fits_for_budget": [
    {
      "bucket_id": "relationship",
      "option_rank": 1,
      "time_estimate_min": 5
    }
  ],
  "warnings": [
    "Pipeline analyst returned Medium confidence — CRM data partial."
  ]
}
```

## Bucket shape

```json
{
  "id": "new_biz | relationship | network",
  "label": "New Business Development",
  "weight": 1.0,
  "options": [
    { /* see Option shape */ }
  ],
  "sub_tabs": [
    { "id": "business", "label": "Business" },
    { "id": "personal", "label": "Close Personal" }
  ],
  "empty_state_note": null
}
```

`sub_tabs` is present only on the `relationship` bucket when the user has enabled the close-personal track. Options inside sub-tabs carry a `sub_tab` field tying them to one. Other buckets omit `sub_tabs`.

`empty_state_note` is present (non-null) when the bucket has fewer than 3 options — explains why ("no urgent actions; quietly carrying X overdue Operational contacts").

## Option shape

**Stable option ID format:** `<bucket>_<person-slug>_<YYYY-MM-DD>` — bucket + slug + date. Same person on the same day → same ID across re-runs, so a UI can correlate "did I act on Sarah's card?" reliably across page reloads.

```json
{
  "rank": 1,
  "id": "new_biz_sarah-chen_2026-05-28",
  "bucket_id": "new_biz",
  "sub_tab": null,
  "person": {
    "slug": "sarah-chen",
    "name": "Sarah Chen",
    "first_name": "Sarah",
    "title": "Head of Content",
    "company": "Vantage Health",
    "tier": "operational",
    "intent": "keep_warm",
    "relationship_class": "business",
    "icp_fit": "primary",
    "cadence_days_override": null,
    "preferred_channels": [],
    "cortex_page_path": "<config-root>/memory/person/sarah-chen.md",
    "hubspot_id": "12345"
  },
  "why_now": "Funding announced 6d ago + ICP primary + WAITING:you on intro he asked for last month.",
  "score": 0.78,
  "score_breakdown": {
    "decay": 0.08,
    "trigger": 0.22,
    "icp": 0.20,
    "reciprocity": 0.15,
    "goal": 0.05,
    "cooling_penalty": 0.00,
    "total": 0.70
  },
  "confidence": "high | medium | low",
  "research_thin": false,
  "channel": "linkedin_dm_cold",
  "time_estimate_min": 5,
  "template": {
    "path": "references/templates/dm/linkedin-cold-icp.md",
    "scenario": "linkedin-cold-icp",
    "voice_used": "primary"
  },
  "draft": {
    "subject": null,
    "body": "Sarah — saw the Series B at Vantage Health. Reaching out because...",
    "variables_filled": [
      "person.first_name",
      "person.company",
      "trigger.context",
      "user.one_liner",
      "user.first_name"
    ],
    "variables_missing": [],
    "needs_user_touch": false,
    "voice_signoff": "—Zach"
  },
  "trigger": {
    "type": "funding | job_change | their_post | news | cadence_overdue | warm_intro | cold_icp | mutual_mention | none",
    "summary": "Vantage Health announced $12M Series B last week (TechCrunch)",
    "source": "websearch | crm | gmail | cortex | manual",
    "observed_at": "2026-05-22"
  },
  "actions": {
    "copy_payload": "Sarah — saw the Series B at Vantage Health...",
    "next_steps_if_done": [
      "Append to cortex person page Recent interactions",
      "Update next_touch_target"
    ],
    "snooze_options_days": [1, 3, 7, 30]
  }
}
```

### Channel enum

```
linkedin_dm_cold
linkedin_dm_warm
linkedin_dm_followup
linkedin_dm_congrats
linkedin_comment
instagram_dm
email_cold
email_warm
email_followup
email_intro_request
email_recap
text_checkin
text_congrats
phone_call_warm
phone_call_discovery
conference_dm_pre
conference_dm_post
self_post
```

The channel maps directly to a template family in `references/templates/`. If a future surface (e.g., web app) renders cards, the channel determines the icon, the channel label, and the typical action (copy + open the right app).

## JSON Schema (draft)

A formal JSON Schema document for validation is shipped alongside this doc at `references/today-json-schema.json` (TBD — to be generated when the writer is implemented). The high-level shape from this doc is authoritative until then.

## Example (full)

```json
{
  "schema_version": "0.1.0",
  "date": "2026-05-28",
  "generated_at": "2026-05-28T07:30:00-04:00",
  "user": {
    "name": "Sample User",
    "first_name": "Sample",
    "company": "Sample Co",
    "one_liner": "We do X for Y."
  },
  "budget_minutes": 30,
  "budget_mode": "default",
  "quarter_focus": "Anchor accounts",
  "quarter_target": "$150K new contracted",
  "buckets": [
    {
      "id": "new_biz",
      "label": "New Business Development",
      "weight": 1.0,
      "options": [
        {
          "rank": 1,
          "id": "new_biz_sarah-chen_2026-05-28",
          "bucket_id": "new_biz",
          "sub_tab": null,
          "person": {
            "slug": "alex-jones",
            "name": "Alex Jones",
            "first_name": "Alex",
            "title": "Director of Content",
            "company": "Acme Learning",
            "tier": "operational",
            "intent": "keep_warm",
            "relationship_class": "business",
            "icp_fit": "primary",
            "cadence_days_override": null,
            "preferred_channels": [],
            "cortex_page_path": null,
            "hubspot_id": null
          },
          "why_now": "Posted about content velocity bottleneck 3d ago + ICP primary.",
          "score": 0.65,
          "score_breakdown": {
            "decay": 0.30,
            "trigger": 0.15,
            "icp": 0.20,
            "reciprocity": 0.00,
            "goal": 0.00,
            "cooling_penalty": 0.00,
            "total": 0.65
          },
          "confidence": "medium",
          "research_thin": true,
          "channel": "linkedin_dm_cold",
          "time_estimate_min": 5,
          "template": {
            "path": "references/templates/dm/linkedin-cold-icp.md",
            "scenario": "linkedin-cold-icp",
            "voice_used": "primary"
          },
          "draft": {
            "subject": null,
            "body": "Alex — saw your post about content velocity at Acme Learning...",
            "variables_filled": [
              "person.first_name",
              "person.company",
              "trigger.context",
              "user.one_liner"
            ],
            "variables_missing": ["shared_context"],
            "needs_user_touch": true,
            "voice_signoff": "—Sample"
          },
          "trigger": {
            "type": "their_post",
            "summary": "LinkedIn post 3d ago about pre-production bottleneck.",
            "source": "websearch",
            "observed_at": "2026-05-25"
          },
          "actions": {
            "copy_payload": "Alex — saw your post about content velocity...",
            "next_steps_if_done": [
              "Create cortex person page",
              "Tag in HubSpot as ICP primary"
            ],
            "snooze_options_days": [1, 3, 7, 30]
          }
        }
      ],
      "sub_tabs": null,
      "empty_state_note": null
    }
  ],
  "carrying": {
    "operational_overdue": 23,
    "strategic_cooling": 4,
    "inner_overdue_not_surfaced": 0,
    "personal_overdue_not_surfaced": 0
  },
  "best_fits_for_budget": [
    { "bucket_id": "new_biz", "option_rank": 1, "time_estimate_min": 5 }
  ],
  "warnings": []
}
```

## Reader expectations

Surfaces consuming this artifact should:

1. **Check `schema_version`.** If it's a major version they don't know, render a "schema mismatch" warning and refuse to act on actions (`actions.copy_payload` is still safe to render, but `actions.next_steps_if_done` may have changed semantics).
2. **Use `draft.needs_user_touch`** to flag incomplete drafts visually (e.g., yellow border on the card).
3. **Honor `confidence`** — Low confidence cards should display a "research-thin" indicator.
4. **Use `actions.copy_payload`** as the canonical thing to copy on tap. Never copy `draft.body` directly — `copy_payload` includes any subject + body assembly.
5. **Use `carrying`** to render a "quietly carrying X overdue" footnote so the user knows nothing was lost.

## Privacy

The artifact contains personally identifying information (full names, companies, sometimes phone-tier indicators). Treat as confidential. The plugin gitignores `<config-root>/relationships/` against accidental commit; downstream consumers should not log or transmit the artifact without user consent.

---

## Related files (the full plugin contract surface)

`today.json` is one of four files a UI consumer interacts with. See `references/ui-integration.md` for the complete contract:

- **`<config-root>/relationships/today.json`** — this file. Overwritten on every `/relationships` run.
- **`<config-root>/relationships/<YYYY-MM-DD>.json`** — date-stamped historical snapshots.
- **`<config-root>/relationships/events.jsonl`** — append-only event log. See "Events.jsonl shape" section below for the unified v0.2.2 schema.
- **`<config-root>/relationships/snoozes.json`** — persistent snooze state. Read by `/relationships` Step 3; written by `/relationships-action`.
- **`<config-root>/relationships/inbox/`** — UI drops JSON events here; sync daemon invokes `/relationships-action --file=<path>`.

---

## Events.jsonl shape (v0.2.2 unified — locks 2026-05-28)

Three writers append to `<config-root>/relationships/events.jsonl`: `/relationships-action`, `/relationships` Step 7 (inline action handling), and `/touchpoint`. All three use the v0.2.2 unified shape.

### Canonical event object

```json
{
  "schema_version": "0.2.2",
  "ts": "2026-05-28T14:32:00-04:00",
  "brief_id": "550e8400-e29b-41d4-a716-446655440000",   // null for /touchpoint (not tied to a brief)
  "option_id": "new_biz_sarah-chen_2026-05-28",           // null for /touchpoint
  "person_slug": "sarah-chen",
  "bucket": "new_biz",                                     // null for /touchpoint
  "channel": "linkedin_dm_warm",
  "action": "copied" | "sent" | "skipped" | "snoozed" | "touchpoint",
  "notes": "<user-supplied free-form text; capped to keep total event ≤ 4KB>",
  "meta": {
    // Common (any writer may include):
    "source": "inline" | "file" | "natural-language" | "explicit-args",

    // /relationships-action only (null elsewhere):
    "snooze_until": "2026-06-04",     // when action: snoozed
    "late_action": true,               // when option_id date != today

    // /touchpoint only (null elsewhere):
    "direction": "in" | "out",
    "intent_at_time": "drive_active",
    "tier_at_time": "strategic"
  }
}
```

### Reader rules

- **Missing `schema_version`** → treat event as v0.2.0 (pre-meta-nesting). Read `snooze_until`, `late_action`, `source` from the TOP level rather than from `meta`.
- **Missing `meta` block on a v0.2.2-flagged event** → treat as if all meta fields are null.
- **Unknown `action` enum value** → log + render as a generic event; DO NOT crash. The action enum may be extended in future versions.
- **Unknown fields inside `meta`** → ignore gracefully. Future writers may add fields without bumping schema_version.

### Atomic-append safety

Per POSIX, single-call `write()` with `O_APPEND` is atomic ONLY when ≤ `PIPE_BUF` bytes (typically 4096 on macOS/Linux). Writers MUST cap each event line at 4000 bytes (safety margin). Truncate `notes` if needed; append `[truncated — see person page Recent Interactions]` marker.

This guarantees concurrent appends from three writers won't interleave-corrupt the JSONL file.

### Version history

- **v0.1.1** — events.jsonl introduced. No schema_version field. Top-level `notes`, `snooze_until`, `late_action`, `source`.
- **v0.2.1** — `/touchpoint` added with DIVERGENT shape (used `summary` instead of `notes`; added `direction`/`intent_at_time`/`tier_at_time` at top level). UI readers expecting v0.1.1 shape would see `null` for `notes` on every touchpoint.
- **v0.2.2** — unified. `summary` renamed to `notes`; per-action extras nested under `meta:`. `schema_version` field added. Backward-compat read rule documented.
- **Future (v0.3+)** — additional `action` enum values likely; readers should accept unknowns.
