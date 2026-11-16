from __future__ import annotations

import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import nudge_check as nc  # noqa: E402

TODAY = "2026-11-16"  # a Monday


def run(**kw) -> dict:
    return nc.check({"today": TODAY, "actor": "sample-user", **kw})


def keys(result: dict) -> list[str]:
    return [n["key"] for n in result["nudges"]]


def reasons(result: dict) -> dict:
    return {s["key"]: s["reason"] for s in result["skipped"]}


class DateMath(unittest.TestCase):
    def test_business_days_skip_weekends(self) -> None:
        mon, fri = date(2026, 11, 9), date(2026, 11, 13)
        self.assertEqual(nc.business_days_between(mon, fri), 4)
        self.assertEqual(nc.business_days_between(fri, date(2026, 11, 16)), 1)   # Fri -> Mon
        self.assertEqual(nc.business_days_between(mon, date(2026, 11, 16)), 5)   # Mon -> next Mon
        self.assertEqual(nc.business_days_between(date(2026, 11, 14), date(2026, 11, 15)), 0)  # Sat -> Sun
        self.assertEqual(nc.business_days_between(mon, mon), 0)
        self.assertEqual(nc.business_days_between(fri, mon), 0)
        self.assertEqual(nc.business_days_between(date(2026, 10, 5), date(2026, 11, 16)), 30)

    def test_business_days_match_a_brute_force_count(self) -> None:
        from datetime import timedelta
        start = date(2026, 1, 1)
        for a in range(0, 40, 3):
            for b in range(0, 60, 7):
                s, e = start + timedelta(days=a), start + timedelta(days=a + b)
                brute = sum(1 for i in range(1, b + 1) if (s + timedelta(days=i)).weekday() < 5)
                self.assertEqual(nc.business_days_between(s, e), brute, (s, e))


class StaleDeal(unittest.TestCase):
    def test_fires_at_15_days_not_14(self) -> None:
        r = run(deals=[{"id": "d15", "name": "A", "last_activity": "2026-11-01"},
                       {"id": "d14", "name": "B", "last_activity": "2026-11-02"}])
        self.assertEqual(keys(r), ["stale-deal:d15"])
        n = r["nudges"][0]
        self.assertEqual((n["days_quiet"], n["quiet_since"], n["subject"], n["unit"]), (15, "2026-11-01", "A", "days"))

    def test_custom_threshold_and_off_switch(self) -> None:
        deals = [{"id": "d", "name": "A", "last_activity": "2026-11-06"}]
        self.assertEqual(keys(run(deals=deals)), [])
        self.assertEqual(keys(run(deals=deals, thresholds={"stale-deal": {"threshold": 10}})), ["stale-deal:d"])
        off = run(deals=[{"id": "d", "last_activity": "2026-01-01"}], thresholds={"stale-deal": {"on": False}})
        self.assertEqual((keys(off), off["triggers_off"]), ([], ["stale-deal"]))

    def test_integer_ids_and_timestamps_are_accepted(self) -> None:
        r = run(deals=[{"id": 4471, "name": "A", "last_activity": "2026-10-01T14:03:00Z"}])
        self.assertEqual(keys(r), ["stale-deal:4471"])


class NoReply(unittest.TestCase):
    def test_counts_business_days(self) -> None:
        r = run(threads=[{"id": "t5", "subject": "S", "last_sent": "2026-11-09"},   # Mon -> Mon = 5
                         {"id": "t4", "subject": "S", "last_sent": "2026-11-10"}])  # Tue -> Mon = 4
        self.assertEqual(keys(r), ["no-reply:t5"])
        self.assertEqual((r["nudges"][0]["days_quiet"], r["nudges"][0]["unit"]), (5, "business-days"))


class OwedFollowUp(unittest.TestCase):
    def test_dated_fires_the_day_after_the_date(self) -> None:
        r = run(commitments=[{"id": "due-yesterday", "summary": "x", "due": "2026-11-15", "created": "2026-11-14"},
                             {"id": "due-today", "summary": "x", "due": "2026-11-16", "created": "2026-10-01"},
                             {"id": "due-later", "summary": "x", "due": "2026-11-30", "created": "2026-09-01"}])
        self.assertEqual(keys(r), ["owed-follow-up:due-yesterday"])
        self.assertTrue(r["nudges"][0]["overdue"])
        self.assertEqual(r["nudges"][0]["days_quiet"], 1)

    def test_undated_fires_at_seven_days(self) -> None:
        r = run(commitments=[{"id": "c7", "summary": "x", "due": None, "created": "2026-11-09"},
                             {"id": "c6", "summary": "x", "created": "2026-11-10"}])
        self.assertEqual(keys(r), ["owed-follow-up:c7"])
        self.assertFalse(r["nudges"][0]["overdue"])

    def test_unreadable_due_date_is_skipped_not_guessed(self) -> None:
        r = run(commitments=[{"id": "c", "summary": "x", "due": "next Friday", "created": "2026-01-01"}])
        self.assertEqual((keys(r), reasons(r)), ([], {"owed-follow-up:c": "bad-date"}))


class DoNotFlagTwice(unittest.TestCase):
    DEAL = [{"id": "d", "name": "A", "last_activity": "2026-10-20"}]

    def flag(self, ts: str, as_of: str = "2026-10-20") -> dict:
        return {"ts": ts, "key": "stale-deal:d", "event": "flagged", "as_of": as_of, "by": "sample-user"}

    def test_not_flagged_again_inside_the_threshold(self) -> None:
        r = run(deals=self.DEAL, ledger=[self.flag("2026-11-05")])
        self.assertEqual((keys(r), reasons(r)), ([], {"stale-deal:d": "already-flagged"}))
        self.assertEqual(r["ledger_append"], [])

    def test_flagged_again_once_the_threshold_passes_again(self) -> None:
        self.assertEqual(keys(run(deals=self.DEAL, ledger=[self.flag("2026-11-01")])), ["stale-deal:d"])
        self.assertEqual(keys(run(deals=self.DEAL, ledger=[self.flag("2026-11-02")])), [])

    def test_flagged_again_after_new_activity_goes_quiet(self) -> None:
        deal = [{"id": "d", "name": "A", "last_activity": "2026-10-30"}]
        r = run(deals=deal, ledger=[self.flag("2026-11-10", as_of="2026-10-20")])
        self.assertEqual(keys(r), ["stale-deal:d"])

    def test_latest_flag_wins(self) -> None:
        r = run(deals=self.DEAL, ledger=[self.flag("2026-10-01", as_of="2026-09-01"), self.flag("2026-11-10")])
        self.assertEqual(keys(r), [])

    def test_dismissed_is_never_flagged(self) -> None:
        deal = [{"id": "d", "name": "A", "last_activity": "2026-01-01"}]
        r = run(deals=deal, ledger=[{"ts": "2026-02-01", "key": "stale-deal:d", "event": "dismissed"}])
        self.assertEqual(reasons(r), {"stale-deal:d": "dismissed"})

    def test_snooze_holds_until_its_date(self) -> None:
        snooze = lambda until: [{"ts": "2026-11-10", "key": "stale-deal:d", "event": "snoozed", "until": until}]
        self.assertEqual(reasons(run(deals=self.DEAL, ledger=snooze("2026-11-17"))), {"stale-deal:d": "snoozed"})
        self.assertEqual(keys(run(deals=self.DEAL, ledger=snooze("2026-11-16"))), ["stale-deal:d"])

    def test_one_keys_history_does_not_affect_another(self) -> None:
        r = run(deals=self.DEAL + [{"id": "e", "name": "B", "last_activity": "2026-10-20"}],
                ledger=[self.flag("2026-11-10")])
        self.assertEqual(keys(r), ["stale-deal:e"])

    def test_ledger_lines_for_new_flags(self) -> None:
        r = nc.check({"today": TODAY, "now": "2026-11-16T06:30:00-05:00", "actor": "sample-user", "deals": self.DEAL})
        self.assertEqual(r["ledger_append"], [{"ts": "2026-11-16T06:30:00-05:00", "key": "stale-deal:d",
                                               "event": "flagged", "as_of": "2026-10-20", "by": "sample-user"}])
        again = run(deals=self.DEAL, ledger=r["ledger_append"])
        self.assertEqual(keys(again), [])


class Robustness(unittest.TestCase):
    def test_bad_rows_are_skipped_with_a_reason_and_the_rest_still_run(self) -> None:
        r = run(deals=[{"id": "ok", "name": "A", "last_activity": "2026-01-01"},
                       {"id": "nodate", "name": "B"}, {"id": "future", "last_activity": "2027-01-01"},
                       {"id": "../x y", "last_activity": "2026-01-01"}, {"id": "ok", "last_activity": "2026-01-01"},
                       "garbage", {"id": True, "last_activity": "2026-01-01"}])
        self.assertEqual(keys(r), ["stale-deal:ok"])
        self.assertEqual(sorted(s["reason"] for s in r["skipped"]),
                         ["bad-date", "bad-id", "bad-id", "date-in-future", "duplicate-in-input", "not-an-object"])

    def test_missing_lists_and_garbage_ledger_do_not_crash(self) -> None:
        self.assertEqual(run()["summary"]["total"], 0)
        r = run(deals=[{"id": "d", "last_activity": "2026-01-01"}], ledger=["x", {"key": 5}, {"key": "stale-deal:d", "event": "flagged", "ts": "nope"}], thresholds="x")
        self.assertEqual(keys(r), ["stale-deal:d"])

    def test_missing_actor_is_recorded_as_unresolved(self) -> None:
        r = nc.check({"today": TODAY, "deals": [{"id": "d", "last_activity": "2026-01-01"}]})
        self.assertEqual(r["ledger_append"][0]["by"], "unresolved")

    def test_today_is_required(self) -> None:
        with self.assertRaises(ValueError):
            nc.check({"today": "tomorrow"})

    def test_ordering_is_by_trigger_then_longest_quiet(self) -> None:
        r = run(deals=[{"id": "a", "last_activity": "2026-10-01"}, {"id": "b", "last_activity": "2026-09-01"}],
                threads=[{"id": "t", "last_sent": "2026-10-01"}])
        self.assertEqual(keys(r), ["stale-deal:b", "stale-deal:a", "no-reply:t"])
        self.assertEqual(r["summary"], {"total": 3, "stale-deal": 2, "no-reply": 1, "owed-follow-up": 0, "skipped": 0})


class Triggers(unittest.TestCase):
    TABLE = (
        "# Triggers\n\n| Trigger | On | Threshold | Unit | Notes |\n|---|---|---|---|---|\n"
        "| `stale-deal` | yes | 21 | days | longer cycle |\n"
        "| no-reply | no | 3 | business-days | |\n"
        "| owed-follow-up | maybe | soon | fortnights | |\n"
        "| made-up | yes | 1 | days | |\n"
    )

    def test_table_overrides_defaults_and_ignores_nonsense(self) -> None:
        t = nc.parse_triggers(self.TABLE)
        self.assertEqual(t["stale-deal"], {"on": True, "threshold": 21, "unit": "days"})
        self.assertEqual(t["no-reply"], {"on": False, "threshold": 3, "unit": "business-days"})
        self.assertEqual(t["owed-follow-up"], nc.DEFAULTS["owed-follow-up"])
        self.assertNotIn("made-up", t)

    def test_empty_or_missing_file_means_defaults(self) -> None:
        self.assertEqual(nc.parse_triggers(""), nc.default_thresholds())
        self.assertEqual(nc.parse_triggers("no table here"), nc.default_thresholds())

    def test_out_of_range_threshold_keeps_default(self) -> None:
        for bad in ("0", "-3", "9999"):
            md = f"| Trigger | On | Threshold | Unit |\n|---|---|---|---|\n| stale-deal | yes | {bad} | days |\n"
            self.assertEqual(nc.parse_triggers(md)["stale-deal"]["threshold"], 15)


class Cli(unittest.TestCase):
    SCRIPT = str(REPO / "scripts" / "nudge_check.py")

    def test_check_round_trip(self) -> None:
        payload = {"today": TODAY, "actor": "sample-user", "deals": [{"id": "d", "name": "Northwind", "last_activity": "2026-10-01"}]}
        out = subprocess.run([sys.executable, self.SCRIPT, "check"], input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout)["nudges"][0]["key"], "stale-deal:d")

    def test_bad_input_exits_nonzero(self) -> None:
        for bad in ("not json", "[1,2]", '{"today": "x"}'):
            out = subprocess.run([sys.executable, self.SCRIPT, "check"], input=bad, capture_output=True, text=True)
            self.assertEqual(out.returncode, 1, bad)

    def test_parse_triggers_reports_a_missing_file(self) -> None:
        out = subprocess.run([sys.executable, self.SCRIPT, "parse-triggers", "/nonexistent/triggers.md"], capture_output=True, text=True)
        report = json.loads(out.stdout)
        self.assertFalse(report["file_found"])
        self.assertEqual(report["thresholds"]["stale-deal"]["threshold"], 15)


if __name__ == "__main__":
    unittest.main()
