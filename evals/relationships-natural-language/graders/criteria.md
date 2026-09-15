---
type: llm
weight: 1
---

The user asked a natural-language question about who to contact today, never typing `/relationships`. A successful response recognizes this as a request for the daily relationships brief and produces (or attempts to produce) the 3-bucket prioritized outreach brief — new business, relationship building, network expansion — with recommended channel/time-estimate/draft per candidate, without first asking the user to type the explicit command. A failing response ignores the request, asks the user to run `/relationships` themselves, or gives a generic non-specific answer with no bucket structure or candidate ranking.
