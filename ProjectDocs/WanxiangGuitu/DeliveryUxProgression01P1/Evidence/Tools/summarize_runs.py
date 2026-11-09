#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build PLAYER_RUN_MATRIX.csv from the archived raw Player artefacts.

Reads only what run_player.py / the driver actually wrote; it never edits a
verdict. Anything missing is reported as MISSING, not inferred.
"""
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(ROOT, "Player")
OUT = os.path.join(os.path.dirname(ROOT), "PLAYER_RUN_MATRIX.csv")


def read_json(path):
    try:
        with io.open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def counts(path):
    n = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    fails, skips = [], []
    if not os.path.isfile(path):
        return n, fails, skips
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            verdict = parts[1]
            if verdict in n:
                n[verdict] += 1
            if verdict == "FAIL":
                fails.append(parts[0] + ": " + (parts[2] if len(parts) > 2 else ""))
            elif verdict == "SKIP":
                skips.append(parts[0] + ": " + (parts[2] if len(parts) > 2 else ""))
    return n, fails, skips


def first_event(path, kind, stage):
    if not os.path.isfile(path):
        return ""
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("kind") == kind and e.get("stage") == stage:
                return e.get("detail", "")
    return ""


def main():
    rows = []
    for name in sorted(os.listdir(PLAYER)):
        d = os.path.join(PLAYER, name)
        if not os.path.isdir(d) or name.startswith("_"):
            continue
        s = read_json(os.path.join(d, "run-summary.json"))
        if not s:
            rows.append([name, "MISSING_SUMMARY", "", "", "", "", "", "", "", ""])
            continue
        n, fails, skips = counts(os.path.join(d, "assertions.tsv"))
        rows.append([
            name, s.get("mode", ""), s.get("verdict", ""), str(s.get("exitCode", "")),
            s.get("completeTxt", ""), str(s.get("pid", "")),
            (s.get("exeSHA256") or "")[:16], (s.get("buildSHA256") or "")[:16],
            (s.get("driverDllSHA256") or "")[:16],
            "%d/%d/%d" % (n["PASS"], n["FAIL"], n["SKIP"]),
            " | ".join(fails), " | ".join(skips),
            first_event(os.path.join(d, "int-events.jsonl"), "identity", "p1-plan"),
        ])
    header = ["run", "mode", "verdict", "exitCode", "completeTxt", "pid",
              "exeSHA256_16", "buildSHA256_16", "driverDLLSHA256_16",
              "PASS/FAIL/SKIP", "failures", "skips", "plan"]
    with io.open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", OUT, "rows", len(rows))


if __name__ == "__main__":
    sys.exit(main())
