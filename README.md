# growth (Growth)

**Daily relationship cockpit for solo operators and small teams.** One command — `/relationships` — gives you a prioritized brief of who to reach out to today, across three buckets:

1. **New Business Development** — outbound to ICP fits, follow-ups on active opps, warm intros
2. **Relationship Building** — strategic peers, mentors, clients, partners, close personal
3. **Network Expansion** — LinkedIn engagement, conferences, meetups, content opportunities

Each bucket gives you **3 options**. Each option ships with a **recommended channel** (comment / DM / email / text / call), a **time estimate**, and a **copy-ready draft** pulled from a template library you can edit.

> Designed for operators who run a real life alongside their pipeline. The brief adapts to "I have 5 minutes" days and "I have an hour" days. No guilt-tripping about overdue contacts — it surfaces the highest-leverage few and lets the rest stay quiet.

## Install

```
/plugin marketplace add BrightWayAI/nucleus
/plugin install growth@nucleus
```

## What you get

### Commands

| Command | What it does |
|---|---|
| `/setup-relationships` | Short interview: ICP, tier definitions, voices (you can have more than one), time-budget defaults, signal and referral preferences. Writes to `<config-root>/plugins/growth.user-context.md`. |
| `/relationships` | The daily brief. Reads your cortex person pages, identity, voice, CRM, calendar and inbox; ranks; drafts; presents. |
| `/relationships-action` | Records what you did with a brief option (copied, sent, skipped, snoozed) without re-running the brief. |
| `/draft-touchpoint` | One message to one named contact, on demand, with the right channel and template. |
| `/touchpoint` | Logs a catch-up from plain language ("had coffee with Sam, he's introducing me to two people") on the person page. Also records signal outcomes (`/touchpoint SIG-12 sent`). |
| `/network-rebalance` | Walks your person pages in batches and proposes tier, intent and bucket tags for each. Run once after setup, then quarterly. |
| `/nudges` | Daily check for things that went quiet (see Nudges below). |
| `/pull-signals` | Pulls job changes, funding and hiring signals for your ICP from Apollo into the signal pipeline. |
| `/capture-signal` | Adds a buying signal you spotted yourself, classified and scored against your ICP. |
| `/warm-signal` | Pre-DM warming: a comment to post, two posts to like, and the DM queued for a day later. |
| `/connect-signal` | Drafts a short LinkedIn connection-request note for a signal contact you aren't connected to yet. |
| `/draft-signal` | Drafts the three-touch DM sequence for a captured signal, in your voice. |
| `/pre-call-brief` | Once a meeting is booked: contact and company snapshot, signal recap, talking points, likely objections. |

### Agents

| Agent | What it does |
|---|---|
| `relationships-director` | `mode: rank` scores candidates for a brief bucket; `mode: research` builds a dossier on one contact or company. |
| `pipeline-analyst` | Ranks the open CRM pipeline: the roughly ten contacts and deals that deserve attention this week, with reasons. |
| `pipeline-forecast` | Projects revenue over a future window from stage probabilities, deal values and close rates, with best, expected and worst cases. |

### Reference files

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

All commands above are implemented. See `CHANGELOG.md` for the version history.

<!-- OPENAI-SUPPORT:START -->
## ChatGPT and Codex

Growth ships as a native OpenAI plugin as well as a Claude plugin. In
ChatGPT desktop Local Work, enable **Growth** and ask naturally or mention
`@Growth`. In Codex, use natural language or the namespaced skills exposed
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

## Nudges (0.7.0+)

`/nudges` is a daily check for things that went quiet: an open deal with no activity for 15 days, an email to a client or prospect with no reply after 5 business days, and a follow-up you said you would send and have not. Each gets a drafted check-in, staged for review in `/morning` under "Needs a nudge". Schedule it with Ops's `/register-schedules` (the `daily-nudges` row). It never sends and never changes a deal. Thresholds live in your own `<config-root>/plugins/growth/triggers.md`; `references/triggers.template.md` is the starter.

## Tests

`python3 -m unittest discover -s tests` covers `scripts/nudge_check.py`, the date math behind the daily nudges check. The script is pure: JSON in, JSON out, no file writes.
