#!/usr/bin/env bash
# UX-PROGRESSION-01 P1 · batch 2: all canonical region runs + B0-12 cross-process pairs.
set -u
cd /i/unity/WanxiangGuitu || exit 1
T=ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/run_player.py
EXE=I:/WGUP01/Observe/Release/WanxiangGuitu.exe
MAN=I:/WGUP01/Observe/Release/WanxiangGuitu_Data/Managed
EV=ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Player
LOG=I:/WGUP01/run-batch2.log
: > "$LOG"

run () { # name mode root extra...
  local name="$1" mode="$2" root="$3"; shift 3
  echo "=== $name ($mode) root=$root $(date -u +%FT%TZ)" | tee -a "$LOG"
  python "$T" --exe "$EXE" --managed "$MAN" --run-root "$root" \
    --evidence "$EV/$name" --mode "$mode" --timeout 600 "$@" >> "$LOG" 2>&1
  echo "exit=$? name=$name" | tee -a "$LOG"
}

S=$(date -u +%H%M%S)
run p1-forest-gather-success  "p1:forest:gather:success"     "I:/WGUP01/Runs/forest-$S"
run p1-forest-treasure-death   "p1:forest:treasure:death"     "I:/WGUP01/Runs/forestdeath-$S"
run p1-ruins-gather-success   "p1:ruins:gather:success"     "I:/WGUP01/Runs/ruins-$S"
run p1-ruins-challenge-abandon "p1:ruins:challenge:abandon"  "I:/WGUP01/Runs/ruinsab-$S"
run p1-cavern-gather-success  "p1:cavern:gather:success"     "I:/WGUP01/Runs/cav-$S"
run p1-cavern-treasure-abandon "p1:cavern:treasure:abandon"  "I:/WGUP01/Runs/cavab-$S"
run p1-forest-counter         "p1:forest:gather:counter"     "I:/WGUP01/Runs/counter-$S"

# B0-12: one save, two processes, per region.
for R in forest ruins cavern; do
  ROOT="I:/WGUP01/Runs/xproc-$R-$S"
  run "p1-xproc-$R-1" "p1:$R:gather:xproc1" "$ROOT"
  run "p1-xproc-$R-2" "p1:$R:gather:xproc2" "$ROOT" --allow-existing-root
done
echo "=== BATCH2 DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
