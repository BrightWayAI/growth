---
name: pre-call-brief
description: "Generate a pre-call brief once a meeting is booked. Pulls everything known about the contact and company and produces contact snapshot, company snapshot, signal recap, talking points, likely objections, and a soft next-step."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# pre-call-brief

Read `../../references/openai-portability.md`, then read
`../../commands/pre-call-brief.md` completely and follow it as the canonical workflow.
Treat `/pre-call-brief`, `$pre-call-brief`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Also read `../../references/signal-methodology.md` for the shared signal, voice, and cadence methodology.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
