#!/usr/bin/env python3
"""Date math and "do not flag twice" bookkeeping for the daily nudges check.

Pure and deterministic: it reads JSON, returns JSON, and touches no files except
the thresholds file it is asked to parse. The `/nudges` command gathers the
deals, threads and commitments, hands them here with the ledger and today's
date, and stages what comes back. Spec: nucleus docs/proposals/sweep-heartbeat.md
and the "Nudges" section of nucleus docs/contracts.md.

Usage:
    python3 scripts/nudge_check.py check < input.json
    python3 scripts/nudge_check.py parse-triggers <path-to-triggers.md>

Output never includes anything that was not in the input.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

TRIGGERS = ("stale-deal", "no-reply", "owed-follow-up")
DEFAULTS = {
    "stale-deal": {"on": True, "threshold": 15, "unit": "days"},
    "no-reply": {"on": True, "threshold": 5, "unit": "business-days"},
    "owed-follow-up": {"on": True, "threshold": 7, "unit": "days"},
}
UNITS = ("days", "business-days")
_ID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/+-]{0,199}$")


def parse_date(value: object) -> date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def business_days_between(start: date, end: date) -> int:
    """Weekdays after `start` up to and including `end`. No holiday calendar."""
    if end <= start:
        return 0
    days = (end - start).days
    full_weeks, extra = divmod(days, 7)
    count = full_weeks * 5
    for i in range(1, extra + 1):
        if (start + timedelta(days=i)).weekday() < 5:
            count += 1
    return count


def elapsed(start: date, end: date, unit: str) -> int:
    return business_days_between(start, end) if unit == "business-days" else max((end - start).days, 0)


def default_thresholds() -> dict:
    return {k: dict(v) for k, v in DEFAULTS.items()}


def parse_triggers(markdown: str) -> dict:
    """Read the user's thresholds table. Anything missing or malformed keeps its default."""
    out = default_thresholds()
    header: list[str] | None = None
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            header = None if not line else header
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        lowered = [c.lower() for c in cells]
        if "trigger" in lowered and "threshold" in lowered:
            header = lowered
            continue
        if header is None or len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        name = row.get("trigger", "").lower()
        if name not in out:
            continue
        on = row.get("on", "").lower()
        if on in ("yes", "no"):
            out[name]["on"] = on == "yes"
        try:
            n = int(row.get("threshold", ""))
            if 1 <= n <= 365:
                out[name]["threshold"] = n
        except ValueError:
            pass
        unit = row.get("unit", "").lower()
        if unit in UNITS:
            out[name]["unit"] = unit
    return out


def normalize_thresholds(given: object) -> dict:
    out = default_thresholds()
    if not isinstance(given, dict):
        return out
    for name in TRIGGERS:
        item = given.get(name)
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("on"), bool):
            out[name]["on"] = item["on"]
        if isinstance(item.get("threshold"), int) and not isinstance(item.get("threshold"), bool) and 1 <= item["threshold"] <= 365:
            out[name]["threshold"] = item["threshold"]
        if item.get("unit") in UNITS:
            out[name]["unit"] = item["unit"]
    return out


def ledger_state(ledger: object) -> dict:
    """Latest relevant facts per key: dismissed, snoozed-until, last flag."""
    state: dict[str, dict] = {}
    if not isinstance(ledger, list):
        return state
    for entry in ledger:
        if not isinstance(entry, dict) or not isinstance(entry.get("key"), str):
            continue
        s = state.setdefault(entry["key"], {"dismissed": False, "until": None, "flag_as_of": None, "flag_on": None})
        event = entry.get("event")
        if event == "dismissed":
            s["dismissed"] = True
        elif event == "snoozed":
            until = parse_date(entry.get("until"))
            if until and (s["until"] is None or until > s["until"]):
                s["until"] = until
        elif event == "flagged":
            flagged_on = parse_date(entry.get("ts"))
            if flagged_on and (s["flag_on"] is None or flagged_on >= s["flag_on"]):
                s["flag_on"] = flagged_on
                s["flag_as_of"] = parse_date(entry.get("as_of"))
    return state


def _suppressed(key: str, as_of: date, today: date, rule: dict, state: dict) -> str | None:
    s = state.get(key)
    if not s:
        return None
    if s["dismissed"]:
        return "dismissed"
    if s["until"] and today < s["until"]:
        return "snoozed"
    if s["flag_on"]:
        new_activity = s["flag_as_of"] is None or as_of > s["flag_as_of"]
        threshold_again = elapsed(s["flag_on"], today, rule["unit"]) >= rule["threshold"]
        if not new_activity and not threshold_again:
            return "already-flagged"
    return None


def check(payload: dict) -> dict:
    today = parse_date(payload.get("today"))
    if today is None:
        raise ValueError("`today` must be an ISO date (YYYY-MM-DD)")
    rules = normalize_thresholds(payload.get("thresholds"))
    state = ledger_state(payload.get("ledger"))
    actor = payload.get("actor") if isinstance(payload.get("actor"), str) and payload.get("actor") else "unresolved"
    ts = payload.get("now") if isinstance(payload.get("now"), str) and parse_date(payload.get("now")) else today.isoformat()

    nudges: list[dict] = []
    skipped: list[dict] = []
    seen: set[str] = set()

    def consider(trigger: str, item: object, quiet_since_field: str, subject_field: str) -> None:
        if not isinstance(item, dict):
            skipped.append({"key": f"{trigger}:?", "reason": "not-an-object"})
            return
        raw_id = item.get("id")
        if not isinstance(raw_id, (str, int)) or isinstance(raw_id, bool) or not _ID_OK.match(str(raw_id)):
            skipped.append({"key": f"{trigger}:?", "reason": "bad-id"})
            return
        key = f"{trigger}:{raw_id}"
        if key in seen:
            skipped.append({"key": key, "reason": "duplicate-in-input"})
            return
        seen.add(key)
        rule = rules[trigger]

        if trigger == "owed-follow-up":
            due = parse_date(item.get("due"))
            created = parse_date(item.get("created"))
            if item.get("due") not in (None, "") and due is None:
                skipped.append({"key": key, "reason": "bad-date"})
                return
            if due is not None:
                quiet_since, days, fires = due, max((today - due).days, 0), today > due
            elif created is not None:
                quiet_since = created
                days = elapsed(created, today, rule["unit"])
                fires = days >= rule["threshold"]
            else:
                skipped.append({"key": key, "reason": "bad-date"})
                return
        else:
            quiet_since = parse_date(item.get(quiet_since_field))
            if quiet_since is None:
                skipped.append({"key": key, "reason": "bad-date"})
                return
            days = elapsed(quiet_since, today, rule["unit"])
            fires = days >= rule["threshold"]

        if quiet_since > today:
            skipped.append({"key": key, "reason": "date-in-future"})
            return
        if not fires:
            return
        why = _suppressed(key, quiet_since, today, rule, state)
        if why:
            skipped.append({"key": key, "reason": why})
            return
        nudge = {
            "trigger": trigger,
            "key": key,
            "subject": item.get(subject_field) if isinstance(item.get(subject_field), str) else "",
            "quiet_since": quiet_since.isoformat(),
            "days_quiet": days,
            "unit": "days" if trigger == "owed-follow-up" and item.get("due") else rule["unit"],
            "source": item.get("source") if isinstance(item.get("source"), str) else str(raw_id),
        }
        if trigger == "owed-follow-up":
            nudge["overdue"] = bool(parse_date(item.get("due")))
        nudges.append(nudge)

    plan = (
        ("stale-deal", "deals", "last_activity", "name"),
        ("no-reply", "threads", "last_sent", "subject"),
        ("owed-follow-up", "commitments", "created", "summary"),
    )
    off: list[str] = []
    for trigger, field, date_field, subject_field in plan:
        if not rules[trigger]["on"]:
            off.append(trigger)
            continue
        items = payload.get(field)
        for item in items if isinstance(items, list) else []:
            consider(trigger, item, date_field, subject_field)

    order = {t: i for i, t in enumerate(TRIGGERS)}
    nudges.sort(key=lambda n: (order[n["trigger"]], -n["days_quiet"], n["key"]))
    ledger_append = [
        {"ts": ts, "key": n["key"], "event": "flagged", "as_of": n["quiet_since"], "by": actor}
        for n in nudges
    ]
    by_trigger = {t: sum(1 for n in nudges if n["trigger"] == t) for t in TRIGGERS}
    return {
        "today": today.isoformat(),
        "thresholds": rules,
        "triggers_off": off,
        "nudges": nudges,
        "ledger_append": ledger_append,
        "skipped": skipped,
        "summary": {"total": len(nudges), **by_trigger, "skipped": len(skipped)},
    }


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "check":
        try:
            payload = json.load(sys.stdin)
            if not isinstance(payload, dict):
                raise ValueError("input must be a JSON object")
            print(json.dumps(check(payload), indent=2))
        except (ValueError, json.JSONDecodeError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        return 0
    if len(argv) == 3 and argv[1] == "parse-triggers":
        path = Path(argv[2]).expanduser()
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        print(json.dumps({"file_found": path.is_file(), "thresholds": parse_triggers(text)}, indent=2))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
