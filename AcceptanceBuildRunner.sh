#!/bin/bash
# Build chain for UX-PROGRESSION-03A real Player acceptance.
# Runs the three AcceptanceBuild entry points across separate Unity invocations
# so the UX_ACCEPTANCE scripting-define toggle + recompile does not interrupt a
# running build.
set -u
UNITY="/c/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe"
PROJECT="/i/unity/WanxiangGuitu"
LOGDIR="$PROJECT/Builds"
mkdir -p "$LOGDIR"

run_step() {
  local step="$1"; local method="$2"; local log="$LOGDIR/acc_build.$step.log"
  echo "===== [$step] $method  ($(date -u +%H:%M:%S)) ====="
  "$UNITY" -batchmode -quit -projectPath "$PROJECT" -executeMethod "$method" -logFile "$log"
  local code=$?
  echo "[$step] exit=$code"
  return $code
}

run_step set   AcceptanceBuild.SetAcceptanceDefine
run_step acc   AcceptanceBuild.BuildAcceptance
run_step nodef AcceptanceBuild.BuildNoDefine

echo "===== BUILD CHAIN COMPLETE ($(date -u +%H:%M:%S)) ====="
echo "--- acceptance_manifest.json (if present) ---"
cat "$PROJECT/Builds/acceptance_manifest.json" 2>/dev/null || echo "(no manifest)"
echo "--- EXE presence ---"
ls -la "$PROJECT/Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe" 2>/dev/null || echo "(no acceptance exe)"
ls -la "$PROJECT/Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu.exe" 2>/dev/null || echo "(no nodefine exe)"
