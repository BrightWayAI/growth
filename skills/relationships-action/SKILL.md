---
name: relationships-action
description: Natural-language entrypoint for recording an action on a relationships brief option. Fires when the user says "I sent that to Sarah," "snooze the Sam one for 3 days," "mark #1 done," "skip the second one," or similar. Resolves the referenced option from today's brief, then routes to /relationships-action with a structured event payload.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# Skill — relationships action

This skill activates on phrases like:

- "I sent that to [name]" / "sent the [name] one"
- "mark [name] done" / "mark #1 done" / "done with #2"
- "skip the [bucket] [rank]" / "skip [name]"
- "snooze [name] for [duration]" / "snooze the Sam one a week"
- "I copied the Sarah draft"

## Behavior

1. Resolve the referenced option from `<config-root>/relationships/today.json`:
   - Name match against `option.person.name` (fuzzy)
   - Or rank+bucket match ("the new biz one," "#2")
   - If ambiguous, surface candidates and ask which.
2. Determine the action:
   - "sent" → `action: sent`
   - "done" → `action: sent` (assume sent unless user clarifies)
   - "copied" → `action: copied`
   - "skip" → `action: skipped`
   - "snooze" → `action: snoozed` (parse duration; default 7 days)
3. Build the JSON event payload and invoke `/relationships-action`.
4. Render the confirmation from `/relationships-action` back to the user.

Respect the autonomy slider — in `auto` mode, skip confirmation prompts when the resolution is unambiguous.

## Routing for nucleus-router

Suggested intent rows:

| Utterance | Routes to |
|---|---|
| "I sent that to [name]" | `/relationships-action {action: sent, ...}` |
| "mark [name] done" | `/relationships-action {action: sent, ...}` |
| "skip [name]" | `/relationships-action {action: skipped, ...}` |
| "snooze [name] for [duration]" | `/relationships-action {action: snoozed, snooze_until: ...}` |
