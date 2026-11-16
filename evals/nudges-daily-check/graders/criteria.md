---
type: llm
weight: 1
---

Judge only these five points. Do not fail the response for leaving out other details.

1. Mail not being connected skips only the no-reply check; the run continues with the
   other two and records that the check was skipped (the run is partial, not failed).
2. The flagged list is exactly what the script returned (Cedar, Northwind, and the
   pricing-sheet item). Birch is not flagged, and the date math is left to the script.
3. Cedar gets a drafted check-in like any other quiet deal. The response does not
   propose closing it as lost or changing its stage, even though it looks dead.
4. The pricing-sheet item is staged with no drafted message, with the reason that it
   needs the file only the user has.
5. Nothing is sent and no deal or memory node is changed: only the day's nudges file,
   the ledger lines, and a receipt are written.

Pass if all five hold. Fail if any one is violated.
