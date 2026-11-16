# Nudge triggers — starter

_Copy this file to `<config-root>/plugins/growth/triggers.md` and edit your copy. The
installed plugin directory is read-only at runtime. `/nudges` reads your copy on every
run; a missing file, row, or value falls back to the defaults shown here._

| Trigger | On | Threshold | Unit | Notes |
|---|---|---|---|---|
| stale-deal | yes | 15 | days | An open deal with no email, meeting, note, task, or stage change. |
| no-reply | yes | 5 | business-days | Something you sent a client or prospect that got no reply. |
| owed-follow-up | yes | 7 | days | Something you said you would send. Applies to items with no date; an item with a date is flagged the day after that date. |

## How to change it

- **Turn a check off:** set `On` to `no`.
- **Change how long to wait:** edit `Threshold` (a whole number from 1 to 365).
- **Unit** is `days` or `business-days` (weekdays only; public holidays are not known).

Do not add rows. Only the three triggers above exist.
