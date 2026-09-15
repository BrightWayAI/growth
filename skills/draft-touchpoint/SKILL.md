---
name: draft-touchpoint
description: Natural-language entrypoint for per-contact on-demand drafting. Fires when the user says "draft a message to [name]," "help me follow up with [name]," "write something to [name]," or names a person they want to reach. Confirms scope, then routes to /draft-touchpoint.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — draft a touchpoint

This skill activates on phrases like:

- "draft a message to Sarah"
- "help me follow up with Derek"
- "write something to my brother"
- "what should I say to [name]"
- "draft a LinkedIn DM to [name]"
- "I want to reach out to [name]"
- "send a note to [name]" (recognized but the result is a draft, not a send)

## Behavior

1. Parse the contact reference from the utterance. If it's a clear single match, proceed. If ambiguous, ask which person.
2. Parse any explicit intent or channel from the utterance ("about her funding news" / "via email").
3. Run `/draft-touchpoint` with the parsed inputs.

Respect the autonomy slider — in `auto` mode, skip the disambiguation prompt if there's exactly one match.

## Distinguishing from /relationships

- **`/relationships`** = the daily brief. 3 buckets × 3 options. Run in the morning.
- **`/draft-touchpoint`** = on-demand single-contact draft. Run when you already know who you want to reach.

If the user says "who should I reach out to today" — that's `/relationships`, not this skill. If the user names a specific person — that's this skill.

## Routing for nucleus-router

Suggested intent rows to add:

| Utterance | Routes to |
|---|---|
| "draft a message to [name]" | `/draft-touchpoint [name]` |
| "help me follow up with [name]" | `/draft-touchpoint [name]` |
| "what should I say to [name]" | `/draft-touchpoint [name]` |
| "write something to [name]" | `/draft-touchpoint [name]` |
| "draft a DM to [name]" | `/draft-touchpoint [name] --channel=dm` |
| "draft an email to [name]" | `/draft-touchpoint [name] --channel=email` |
