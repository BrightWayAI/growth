---
disable-model-invocation: true
name: warm-signal
description: "Pre-DM warming sequence. Drafts a substantive comment for one of the contact's recent posts, identifies 2 more posts to like, and queues the DM for 24h later."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# warm-signal

Read `../../references/openai-portability.md`, then read
`../../commands/warm-signal.md` completely and follow it as the canonical workflow.
Treat `/warm-signal`, `$warm-signal`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Also read `../../references/signal-methodology.md` for the shared signal, voice, and cadence methodology.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
