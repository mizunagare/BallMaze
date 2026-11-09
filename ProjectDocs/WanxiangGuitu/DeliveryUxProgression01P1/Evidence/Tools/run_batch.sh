#!/usr/bin/env bash
# UX-PROGRESSION-01 P1 · real Player run batch (unsandboxed so run roots persist).
set -u
cd /i/unity/WanxiangGuitu || exit 1
T=ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/run_player.py
EXE=I:/WGUP01/Observe/Release/WanxiangGuitu.exe
MAN=I:/WGUP01/Observe/Release/WanxiangGuitu_Data/Managed
LOG=I:/WGUP01/run-batch.log
: > "$LOG"
run () {
  local name="$1" mode="$2"
  echo "=== $name ($mode) $(date -u +%FT%TZ)" | tee -a "$LOG"
  rm -rf "I:/WGUP01/Runs/$name"
  python "$T" --exe "$EXE" --managed "$MAN" \
    --run-root "I:/WGUP01/Runs/$name" \
    --evidence "ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Player/$name" \
    --mode "$mode" --timeout 600 >> "$LOG" 2>&1
  echo "exit=$? name=$name" | tee -a "$LOG"
}
run p1-forest-gather-success   "p1:forest:gather:success"
run p1-forest-treasure-death   "p1:forest:treasure:death"
run p1-ruins-gather-success    "p1:ruins:gather:success"
run p1-ruins-challenge-abandon "p1:ruins:challenge:abandon"
run p1-cavern-gather-success   "p1:cavern:gather:success"
run p1-cavern-treasure-abandon "p1:cavern:treasure:abandon"
run p1-forest-counter          "p1:forest:gather:counter"
echo "=== BATCH DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
