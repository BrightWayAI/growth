---
name: nudges
description: Natural-language entrypoint for the daily check on things that went quiet. Fires when the user asks "what's gone quiet," "which deals have I been ignoring," "who haven't I heard back from," "what follow-ups did I drop," or "run my nudges." Routes to /nudges. Drafts only; never sends and never changes a deal.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — nudges

This skill activates on phrases like:

- "what's gone quiet?"
- "which deals haven't I touched in a while?"
- "who hasn't replied to me?"
- "what follow-ups did I forget to send?"
- "run my nudges"

## Behavior

1. Run the workflow in `commands/nudges.md`. On demand, pass `--dry-run` if the user
   only wants to see the list and not stage it.
2. Show the flagged items with their drafts.
3. Do not send any draft and do not change any deal. If the user wants to send one,
   that is a separate, explicit approval for that message.

## Not this skill

- "Who should I reach out to today?" → `/relationships`.
- "Draft a note to Sarah." → `/draft-touchpoint`.
