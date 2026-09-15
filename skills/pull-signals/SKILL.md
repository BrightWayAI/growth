---
disable-model-invocation: true
name: pull-signals
description: "Pull fresh buying signals from Apollo for the user's ICP. Fetches job changes, funding events, and hiring signals (per the user's setup preferences), filters against the ICP, scores priority, and adds them to the pipeline. Use to refresh the pipeline at the start of a session. Requires the Apollo MCP to be connected."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# pull-signals

Read `../../references/openai-portability.md`, then read
`../../commands/pull-signals.md` completely and follow it as the canonical workflow.
Treat `/pull-signals`, `$pull-signals`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Also read `../../references/signal-methodology.md` for the shared signal, voice, and cadence methodology.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
