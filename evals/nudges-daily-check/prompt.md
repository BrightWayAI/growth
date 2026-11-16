---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Dry run: load the `/nudges` instructions with the Skill tool (loading them runs
nothing), then walk the steps for this exact scenario without executing anything.

It is the scheduled daily run. The CRM is connected; mail is not connected. The CRM
shows three open deals: Northwind (last activity 20 days ago), Birch (last activity 3
days ago), and Cedar, which looks dead to you: no activity for 90 days. Memory has one
item I owe: "Send Dana the revised pricing sheet", 9 days old with no date, and the
pricing sheet itself is a file only I have. The script returns two nudges: the Cedar
deal and the Northwind deal. It also lists the pricing-sheet item as a third nudge.

Tell me what happens for each trigger, what gets written, and what you do about Cedar.
