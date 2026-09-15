# Security Policy

## What this plugin does with your data

`growth` produces a daily prioritized brief for new business, relationship building, and network expansion. It reads relationship data from multiple sources, ranks it, and drafts ready-to-send messages. **Drafts only — never sends.**

**Reads:**
- **Cortex memory** (if installed) — person pages (`<config-root>/memory/person/*.md`), workstream nodes, hot cache, identity, voice. Read-only.
- **CRM** (HubSpot / Salesforce / Pipedrive / Attio / etc.) — contacts, deals, tasks, owner properties used for prioritization. Read-only via your authorized MCP connector.
- **Email** (Gmail / Outlook) — recent threads for context on a contact. Read-only.
- **Calendar** (Google / Outlook) — upcoming external meetings to weight prioritization. Read-only.
- **Apollo** (if connected) — net-new prospects matching your ICP. Read-only.
- **Plugin user-context** — `<config-root>/plugins/growth.user-context.md` (your ICP, tiers, voice rules, integrations).
- **Templates** — `references/templates/**/*.md` (bundled defaults + your custom additions).
- **Shared foundation files** — `<config-root>/memory/me/identity.md`, `<config-root>/memory/me/voice.md` (read-only).

**Writes:**
- **Plugin user-context** — `<config-root>/plugins/growth.user-context.md` (after `/setup-relationships`).
- **Daily brief output** — `<config-root>/relationships/today.md` and `<config-root>/relationships/today.json` (structured artifact for downstream consumers like a future web UI).
- **Cortex person pages** (if installed) — additively appends to the **## Recent interactions** log after you confirm an action was taken. Never overwrites Identity or Notes sections.
- **Drafts** — surfaced inline in conversation, ready to copy. Not auto-sent.

**Does not:**
- **Send messages on your behalf.** Every draft is for you to copy, edit, and send yourself.
- **Modify CRM contacts or deals** without explicit per-action confirmation.
- **Edit or delete existing calendar events.** Only adds new placeholder blocks with `sendUpdates: "none"`, and only when you ask.
- **Bypass cooling-period rules.** If your user-context sets cadence rules (e.g., "don't touch a Tier-A contact more than once a week"), the brief honors them.
- **Surface contacts marked "do not engage"** or who are inside an active deal where outreach would be disruptive.

## Where data lives

- Plugin reference files inside the installed plugin directory.
- Plugin runtime state at `<config-root>/relationships/` and `<config-root>/plugins/growth.user-context.md`.
- Drafts inline in conversation.
- Person-page interaction logs in cortex memory (if installed).

## What gets sent off your machine

- Whatever your authorized CRM / Email / Calendar / Apollo / WebSearch MCP connectors send when invoked.
- Nothing else. The plugin does not ship telemetry or analytics.

## Privacy note about the brief

The daily brief reveals who is in each tier of your network, what their ICP fit is, and what you owe them. Treat the brief output and the user-context file as confidential.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a vulnerability

Report privately via GitHub Security Advisories:

https://github.com/BrightWayAI/relationships/security/advisories/new

Do not open a public issue for security concerns. We aim to respond within 5 business days.
