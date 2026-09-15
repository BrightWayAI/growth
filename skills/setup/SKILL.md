---
disable-model-invocation: true
name: setup
description: Natural-language entrypoint for configuring the relationships plugin. Fires when the user says "set up relationships," "configure my network," "let's set up my relationships plugin," "I want to track my relationships," or similar. Confirms, then routes to /setup-relationships.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — relationships setup

This skill activates on phrases like:

- "set up relationships"
- "configure my network"
- "configure my relationships"
- "let's set up the relationships plugin"
- "I want to start tracking my outreach daily"
- "build my daily relationship brief"
- "set up my outreach cockpit"

## Behavior

1. Confirm with the user: "Want me to walk you through setting up the relationships plugin — your ICP, tiers, voices, and integrations? Takes about 5-10 minutes."
2. If yes → run `/setup-relationships`.
3. If they want a preview first → describe what `/setup-relationships` captures and what `/relationships` produces.

Respect the autonomy slider — in `auto` mode, skip the confirmation and just run.
