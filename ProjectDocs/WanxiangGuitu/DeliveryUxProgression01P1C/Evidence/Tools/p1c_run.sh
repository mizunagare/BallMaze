#!/usr/bin/env bash
# Rebuild the observation copy + inject the P1C driver, then run ONE Player mode.
# Usage: ./p1c_run.sh <tag> <mode> [timeout]
set -u
cd "I:/unity/WanxiangGuitu" || exit 1
TAG="$1"; MODE="$2"; TIMEOUT="${3:-480}"
TS=$(date +%H%M%S)
BASE=I:/WGUP01
case "$TAG" in
  *-nosrc) ;; # reuse the current observe copy (driver already injected)
  *)
    mv "$BASE/Observe/Release" "$BASE/Observe/Release-$TAG-$TS" 2>/dev/null
    mkdir -p "$BASE/Observe/Release"
    cp -a "$BASE/Build/Release/." "$BASE/Observe/Release/"
    # 每次编译都把记录写到该 tag 自己的目录：这样三条 Run 各自的驱动 SHA 都能单独复核，
    # 不会被下一次编译覆盖。（-deterministic 保证同源同引用逐字节相同。）
    python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/build_driver.py \
      --managed "$BASE/Observe/Release/WanxiangGuitu_Data/Managed" \
      --source ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/IntDriver.cs.txt \
      --work "$BASE/Observe/driver" \
      --data "$BASE/Observe/Release/WanxiangGuitu_Data" \
      --evidence "ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Driver/$TAG" 2>&1 | tail -4
    ;;
esac
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/run_player.py \
  --exe "$BASE/Observe/Release/WanxiangGuitu.exe" \
  --managed "$BASE/Observe/Release/WanxiangGuitu_Data/Managed" \
  --run-root "$BASE/Runs/$TAG-$TS" \
  --evidence "ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Player/$TAG" \
  --mode "$MODE" --timeout "$TIMEOUT" 2>&1 | tail -4
