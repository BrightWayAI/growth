---
name: network-rebalance
description: Natural-language entrypoint for the quarterly network re-tagging walk. Fires when the user says "rebalance my network," "re-tag my contacts," "audit my tiers," "review my relationship tiers," or asks for the quarterly relationship review. Confirms, then routes to /network-rebalance.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — network rebalance

This skill activates on phrases like:

- "rebalance my network"
- "re-tag my contacts"
- "audit my tiers"
- "review my relationship tiers"
- "run my quarterly relationship review"
- "I want to redo my contact tiers"
- "let's clean up my network tagging"
- "who's in my inner core right now"

## Behavior

1. Confirm with a one-liner: "Walk your cortex person pages and propose `tier` + `buckets` + `relationship_class` + `icp_fit` frontmatter? You'll approve/edit/skip in batches of 10-15. Idempotent; safe to run."
2. If yes → run `/network-rebalance`.
3. If user wants to scope it tighter (e.g., "just my inner core"), pass the scope hint forward.

Respect the autonomy slider — in `auto` mode, accept high-confidence proposals automatically; pause only on medium/low.

## Routing for nucleus-router

Suggested intent rows to add:

| Utterance | Routes to |
|---|---|
| "rebalance my network" | `/network-rebalance` |
| "audit my tiers" | `/network-rebalance` |
| "review my relationship tiers" | `/network-rebalance` |
| "quarterly relationship review" | `/network-rebalance` |
