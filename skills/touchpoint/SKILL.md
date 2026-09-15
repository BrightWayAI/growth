---
name: touchpoint
description: Natural-language entrypoint for ad-hoc relationship logging. Fires when the user describes a touchpoint they just had — "I had a great catch-up with Sang," "Just texted my brother," "Commented on Charity's LinkedIn post," "Had a call with [name]." Resolves the person from context, infers channel, drafts a Recent Interactions log entry, optionally proposes intent/tier shift. Drafts only — never sends, never modifies CRM.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — touchpoint

Activates on phrases like:

- "I had a [meeting/call/catch-up/coffee] with [name]"
- "Just [texted/emailed/DM'd/messaged] [name]"
- "Spoke with [name] about [X]"
- "[Commented/replied] on [name]'s [post/LinkedIn/email]"
- "[name] reached out about [X]"
- "Quick check-in with [name]"

## Behavior

1. **Parse** the person, channel, and summary from the utterance.
2. **Disambiguate** if multiple matches (list candidates with last-contact dates; user picks).
3. **Invoke `/touchpoint`** with parsed args.
4. **Render confirmation** + any pattern-shift suggestion from the command.

Respect autonomy slider:
- `auto` → skip disambiguation prompts when unambiguous; skip pattern-shift prompts and just log.
- `suggest` (default) → confirm channel inference and any shift prompts.
- `confirm` → confirm every field before write.

## Distinguishing from sibling commands

| Phrase | Skill |
|---|---|
| "I had a catch-up with Sang" | `/touchpoint` (ad-hoc log) |
| "Draft a message to Sang" | `/draft-touchpoint` (compose, don't send) |
| "I sent that to Sarah" (during brief review) | `/relationships-action` (action on a brief card) |
| "Who should I reach out to today" | `/relationships` (daily brief) |
| "Rebalance my network" | `/network-rebalance` (bulk re-tag) |

## When to NOT fire

- For drafting messages → that's `/draft-touchpoint`
- For acting on a brief card → that's `/relationships-action`
- For bulk relationship-tagging → that's `/network-rebalance`

## Routing for nucleus-router

| Utterance | Routes to |
|---|---|
| "I had a [verb] with [name]" | `/touchpoint` |
| "just [texted/emailed/DM'd] [name]" | `/touchpoint --channel=<inferred>` |
| "[name] reached out" | `/touchpoint --direction=in` |
| "commented on [name]'s post" | `/touchpoint --channel=comment` |
