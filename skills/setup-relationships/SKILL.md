---
disable-model-invocation: true
name: setup-relationships
description: "Configure the relationships plugin. Auto-imports identity, voice, ICP, CRM, Apollo, cooling rules, and banned phrases from peer plugin configs when they exist — so for full-stack Nucleus users this collapses to ~3 confirmations. For standalone installs (no peers), runs the full interview. Writes results to <config-root>/plugins/relationships.user-context.md. Re-run anytime to update."
---

# setup-relationships

Read `../../references/openai-portability.md`, then read
`../../commands/setup-relationships.md` completely and follow it as the canonical workflow.
Treat `/setup-relationships`, `$setup-relationships`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
