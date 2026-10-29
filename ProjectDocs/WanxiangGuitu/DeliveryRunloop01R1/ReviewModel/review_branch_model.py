"""Offline control-flow models of two inspected RUNLOOP-01 branches.

This is NOT the Unity/C# program, JsonUtility, the v9 validator, or game evidence.
It tests the Boolean predicates and UI routing transcribed from the fixed source.
All records below are synthetic minimal dictionaries, not player save files.
Run: python review_branch_model.py --out <fresh-results.json>
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path

SHA = "d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179"

def json_equal(a, b):
    # Object field-order is irrelevant to these cases; no null/empty
    # normalization or Unity serializer behavior is being tested here.
    return json.dumps(a, ensure_ascii=False, separators=(",", ":")) == json.dumps(b, ensure_ascii=False, separators=(",", ":"))

old_profile = {"profileId": "synthetic-profile", "materials": [0, 0, 0, 100, 0, 0], "committedRuns": []}
old_run = {"runId": "synthetic-run", "phase": "OutcomePending", "checkpoint": {"resourceHealth": 55}}
record = {
    "settlementId": "synthetic-run:terminal", "runId": "synthetic-run",
    "status": "Pending", "acknowledged": False, "outcome": "Extracted",
    "plan": {"profileId": "synthetic-profile", "materials": [0, 0, 0, 105, 0, 0], "committedRuns": ["synthetic-run"]},
}
old_revision = 3
pending = {"revision": old_revision, "hasActiveRun": True, "hasSettlement": True,
           "activeRun": copy.deepcopy(old_run), "profile": copy.deepcopy(old_profile), "settlement": copy.deepcopy(record)}
expected_committed = copy.deepcopy(record)
expected_committed["status"] = "Committed"
committed = {"revision": old_revision + 1, "hasActiveRun": False, "hasSettlement": True,
             "activeRun": None, "profile": copy.deepcopy(record["plan"]), "settlement": copy.deepcopy(expected_committed)}

def source_classify(disk):
    """Translation of CommitSettlement's failed-save reconciliation predicates."""
    try:
        if disk is None:
            raise OSError("synthetic missing/unreadable main file")
        if (disk["revision"] == old_revision + 1
            and not disk["hasActiveRun"] and disk["hasSettlement"]
            and disk["settlement"]["settlementId"] == expected_committed["settlementId"]
            and disk["settlement"]["runId"] == expected_committed["runId"]
            and disk["settlement"]["status"] == "Committed"
            and not disk["settlement"]["acknowledged"]
            and json_equal(disk["profile"], record["plan"])
            and json_equal(disk["settlement"], expected_committed)):
            return "CONFIRMED_COMMITTED"
        unknown = (disk["revision"] != old_revision
                   or not disk["hasActiveRun"]
                   or disk["activeRun"]["runId"] != old_run["runId"]
                   or not disk["hasSettlement"]
                   or disk["settlement"]["status"] != "Pending"
                   or disk["settlement"]["settlementId"] != expected_committed["settlementId"]
                   or not json_equal(disk["profile"], old_profile))
        return "UNKNOWN_READ_REQUIRED" if unknown else "RETRY_ALLOWED"
    except (KeyError, TypeError, OSError):
        return "UNKNOWN_READ_REQUIRED"

def changed(base, *path_and_value):
    result = copy.deepcopy(base)
    *path, value = path_and_value
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return result

predicate_cases = [
    ("exact_prior_pending", pending, "RETRY_ALLOWED"),
    ("exact_published_committed", committed, "CONFIRMED_COMMITTED"),
    ("committed_plan_conflict", changed(committed, "settlement", "plan", "materials", [0,0,0,106,0,0]), "UNKNOWN_READ_REQUIRED"),
    ("pending_plan_conflict", changed(pending, "settlement", "plan", "materials", [0,0,0,106,0,0]), "UNKNOWN_READ_REQUIRED"),
    ("pending_outcome_conflict", changed(pending, "settlement", "outcome", "Abandoned"), "UNKNOWN_READ_REQUIRED"),
    ("pending_checkpoint_conflict", changed(pending, "activeRun", "checkpoint", "resourceHealth", 22), "UNKNOWN_READ_REQUIRED"),
    ("pending_revision_conflict", changed(pending, "revision", 8), "UNKNOWN_READ_REQUIRED"),
    ("missing_or_unreadable_main", None, "UNKNOWN_READ_REQUIRED"),
]

def route(state):
    # AdventureFlow.OnGUI chooses HasResult before the generic Error panel.
    if state["hasResult"]:
        if state["needsRead"]:
            return "READ_COMPLETE_SAVE"
        return "COMMIT_SETTLEMENT" if state["status"] == "Pending" else "ACK_RETURN_CAMP"
    return "READ_COMPLETE_SAVE" if state["error"] else "NO_RECOVERY_PANEL"

def restore_sequence(fail_at):
    state = {"needsRead": True, "blocked": False, "hasResult": True, "status": "Pending", "error": True}
    if fail_at == "read_parse":
        # Restore was never entered; old marker remains set.
        state["blocked"] = True
    else:
        # AdventureFlow.Restore clears the marker BEFORE ApplyCamp/RestoreWorld.
        state["needsRead"] = False
        state["status"] = "Committed"
        state["error"] = False
        if fail_at == "before_camp_load":
            # LoadProgress catch -> blocked=true -> BlockRecovery/MigrationFailed.
            state["blocked"] = True
            state["error"] = True
        else:
            state["blocked"] = False
    state["button"] = route(state)
    state["SaveProgressCanCapture"] = not state["blocked"] and not state["needsRead"]
    return state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit("Refusing to overwrite results")
    result = {"sha": SHA, "scope": "OFFLINE_TRANSCRIBED_BRANCH_MODEL_NOT_UNITY", "v9ValidatorExecuted": False,
              "gameLaunched": False, "predicateCases": [], "recoveryCases": []}
    for name, fixture, expected in predicate_cases:
        actual = source_classify(fixture)
        row = {"case": name, "expectedByReviewContract": expected, "actualModel": actual,
               "matchesContract": actual == expected, "syntheticInput": fixture}
        result["predicateCases"].append(row)
        print(f"predicate {name}: {actual}; matches={row['matchesContract']}")
    for case, expected in [("read_parse", "READ_COMPLETE_SAVE"),
                           ("before_camp_load", "READ_COMPLETE_SAVE"),
                           ("success", "ACK_RETURN_CAMP")]:
        state = restore_sequence(case)
        row = {"case": case, "expectedButton": expected, "actualModel": state,
               "matchesContract": state["button"] == expected}
        result["recoveryCases"].append(row)
        print(f"recovery {case}: {state['button']}; blocked={state['blocked']}; matches={row['matchesContract']}")
    rows = result["predicateCases"] + result["recoveryCases"]
    result["summary"] = {"cases": len(rows), "matches": sum(r["matchesContract"] for r in rows),
                         "counterexamples": sum(not r["matchesContract"] for r in rows),
                         "distinctFindings": 2}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0  # Model execution completed; counterexamples are NOT gameplay verdicts.

if __name__ == "__main__":
    raise SystemExit(main())
