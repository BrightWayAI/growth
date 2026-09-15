---
disable-model-invocation: true
name: draft-signal
description: "Draft the 3-touch DM sequence (opener + 2 follow-ups) for a captured signal, in the user's voice, with copy-paste-ready messages and timing."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# draft-signal

Read `../../references/openai-portability.md`, then read
`../../commands/draft-signal.md` completely and follow it as the canonical workflow.
Treat `/draft-signal`, `$draft-signal`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Also read `../../references/signal-methodology.md` for the shared signal, voice, and cadence methodology.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
