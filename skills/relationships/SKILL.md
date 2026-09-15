---
name: relationships
description: Natural-language entrypoint for the daily relationship brief. Fires when the user asks who to reach out to today, requests an outreach plan, wants their network priorities, or asks for the relationship cockpit. Confirms, then routes to /relationships.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — relationships daily brief

This skill activates on phrases like:

- "who should I reach out to today"
- "what's my outreach plan"
- "show me today's relationship brief"
- "what should I do for networking today"
- "give me my daily relationships"
- "run my relationship cockpit"
- "what's on the network plate today"

## Behavior

1. Confirm with a one-liner: "Run today's relationship brief? (3 buckets × 3 options)"
2. If yes → run `/relationships`.
3. If the user asks for a single bucket (e.g., "just show me new business today"), pass the bucket as a filter — `/relationships --bucket=new_biz`. (Filtered mode is a Phase 2 enhancement; stub for now.)

Respect the autonomy slider — in `auto` mode, skip confirmation and run directly.

## Routing for nucleus-router

Suggested intent rows to add to `nucleus-router`:

| Utterance | Routes to |
|---|---|
| "who should I reach out to today" | `/relationships` |
| "what's my outreach plan today" | `/relationships` |
| "show me my relationship brief" | `/relationships` |
| "run my daily relationships" | `/relationships` |
| "set up relationships" | `/setup-relationships` |
| "configure my network" | `/setup-relationships` |
| "rebalance my network" | `/network-rebalance` (Phase 3) |
| "draft a message to [name]" | `/draft-touchpoint [name]` (Phase 2) |
