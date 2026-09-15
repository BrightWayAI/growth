---
disable-model-invocation: true
name: setup-relationships
description: "Configure the relationships plugin. Auto-imports identity, voice, CRM, and banned phrases from peer plugin configs when they exist. ICP/Apollo/signal preferences and referral-connector/cooling rules are captured natively (absorbed from the retired lead-engine and referral-engine plugins, 2026-09-15) rather than imported. For full-stack Nucleus users this collapses to a handful of confirmations plus the native questions; standalone installs run the full interview. Writes results to <config-root>/plugins/growth.user-context.md. Re-run anytime to update."
---

# setup-relationships

Read `../../references/openai-portability.md`, then read
`../../commands/setup-relationships.md` completely and follow it as the canonical workflow.
Treat `/setup-relationships`, `$setup-relationships`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
