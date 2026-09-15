---
name: capture-signal
description: "Manually capture a buying signal you spotted (LinkedIn post, comment, job change, etc.). Classifies the signal against the 7-signal taxonomy, scores it against the user's ICP, researches the contact across available connectors, and adds it to the active pipeline."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# capture-signal

Read `../../references/openai-portability.md`, then read
`../../commands/capture-signal.md` completely and follow it as the canonical workflow.
Treat `/capture-signal`, `$capture-signal`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Also read `../../references/signal-methodology.md` for the shared signal, voice, and cadence methodology.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
