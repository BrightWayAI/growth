# growth (Growth Engine)

**Daily relationship cockpit for solo operators and small teams.** One command — `/relationships` — gives you a prioritized brief of who to reach out to today, across three buckets:

1. **New Business Development** — outbound to ICP fits, follow-ups on active opps, warm intros
2. **Relationship Building** — strategic peers, mentors, clients, partners, close personal
3. **Network Expansion** — LinkedIn engagement, conferences, meetups, content opportunities

Each bucket gives you **3 options**. Each option ships with a **recommended channel** (comment / DM / email / text / call), a **time estimate**, and a **copy-ready draft** pulled from a template library you can edit.

> Designed for operators who run a real life alongside their pipeline. The brief adapts to "I have 5 minutes" days and "I have an hour" days. No guilt-tripping about overdue contacts — it surfaces the highest-leverage few and lets the rest stay quiet.

## What you get

- `/setup-relationships` — short interview that captures your ICP, tier definitions, voices (you can have more than one), time-budget defaults, and which integrations you have running. Writes to `<config-root>/plugins/growth.user-context.md`.
- `/relationships` — the daily brief. Reads your cortex person pages, identity, voice, CRM, calendar, and inbox; ranks; drafts; presents.
- `references/templates/` — bundled defaults across **comment / dm / email / text / call / conference** categories. Variable-driven (`{{person.name}}`, `{{trigger.context}}`, `{{user.business}}`). Editable. Add your own.
- `references/person-page-extensions.md` — additive YAML fields the plugin recognizes on cortex person pages (`tier`, `buckets`, `icp_fit`, `generosity_ledger`, `next_touch_target`). Untagged people fall back to sensible defaults.

## How it ranks

A weighted score per contact:

- **Cadence decay** — how overdue against the tier's target frequency
- **External triggers** — job change, funding, content posted (via `/pull-signals`)
- **ICP fit** — alignment with the focus you set in setup
- **Reciprocity debt** — open loops, especially WAITING-you items
- **Quarterly goal alignment** — what you said matters this quarter

## How it drafts

Each surfaced contact gets a channel recommendation (based on relationship class + tier + trigger) and a template-driven draft in your voice. Two voice streams supported by default — your personal voice and a business voice — so DMs to friends don't sound like cold outreach and vice versa.

## Companion plugins

Signal sourcing (Apollo/ICP/7-signal taxonomy), the `relationships-director` deep-dive mode (`mode: research`), and referral-network cooling rules are bundled directly in this plugin as of 2026-09-15 (absorbed from the retired lead-engine and referral-engine plugins) — no separate install needed for those.

Works standalone, but smarter with:

- **cortex** — person pages, voice, identity, hot cache, workstream nodes
- **briefing** — pairs with `/brief` as the morning surface; briefing calls this plugin's `pipeline-analyst` for daily prioritization

If a companion is missing, the plugin degrades gracefully — no required dependency beyond cortex foundation files.

## Privacy

Drafts only. Never sends. Reads your authorized connectors; writes only to your config root and (additively) to cortex person-page interaction logs. See `SECURITY.md` for the full data map.

## Status

v0.1.0 — scaffold. Setup command, daily command, templates library, and person-page extensions documented but stubbed. See `CHANGELOG.md` for what's in this release and `nucleus/docs/proposals/relationships-plugin.md` (in the nucleus repo) for the design spec.

<!-- OPENAI-SUPPORT:START -->
## ChatGPT and Codex

Relationships ships as a native OpenAI plugin as well as a Claude plugin. In
ChatGPT desktop Local Work, enable **Relationships** and ask naturally or mention
`@Relationships`. In Codex, use natural language or the namespaced skills exposed
by the plugin. Claude slash-command names in this README remain workflow aliases.

All hosts resolve the same `<config-root>` used by Cortex, so Claude, ChatGPT desktop,
and Codex can share identity, voice, memory, and per-plugin settings without copying
them. The installed plugin directory is read-only at runtime. See
[`references/openai-portability.md`](references/openai-portability.md) for capability
mapping, connector checks, permissions, and honest degraded behavior.

Import the full catalog from
[`BrightWayAI/nucleus`](https://github.com/BrightWayAI/nucleus); Nucleus is the master
marketplace, while each plugin remains independently installable.
<!-- OPENAI-SUPPORT:END -->
