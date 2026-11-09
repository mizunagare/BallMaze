#!/usr/bin/env bash
# Produce PROTECTION_HASHES.tsv: proves the protected (economy / RNG / save-schema /
# scoring / layout / projection) files are unchanged between the design baseline and
# the bytes this batch commits.
#
# Two things this script deliberately does NOT do:
#   1. it never compares raw on-disk bytes against `git show` (that would report a
#      false "changed" for every CRLF working-tree file), and
#   2. it never treats a missing file as "identical" (a `git show` of a bad path
#      yields an empty stream, whose sha256 would silently match another bad path).
# Verdict comes from `git diff --quiet BASE -- path`, which is exactly the comparison
# git itself would make; blob ids are recorded for hand verification.
set -u
cd /i/unity/WanxiangGuitu || exit 1
BASE=59190b7036307e69420d43e23e5610f2ddbab9fc
OUT=ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/PROTECTION_HASHES.tsv
PATHS=(
  Assets/CombatPrototype/AdventureRules.cs
  Assets/CombatPrototype/AdventureValidation.cs
  Assets/CombatPrototype/CombatSaveData.cs
  Assets/CombatPrototype/CombatSaveSystem.cs
  Assets/CombatPrototype/AdventureState.cs
  Assets/CombatPrototype/RouteScoring.cs
  Assets/CombatPrototype/ForestRewards.cs
  Assets/CombatPrototype/RuinsExploration.cs
  Assets/CombatPrototype/CrystalCavernLayout.cs
  Assets/CombatPrototype/ForestLayout.cs
  Assets/CombatPrototype/RuinsLayout.cs
  Assets/CombatPrototype/AdventureRandom.cs
  Assets/CombatPrototype/CraftingTargets.cs
  Assets/CombatPrototype/WeaponSkillExpansion.cs
  Assets/CombatPrototype/NewWeaponCombat.cs
  Assets/CombatPrototype/GreatswordCombat.cs
  Assets/CombatPrototype/ScytheCombat.cs
  Assets/CombatPrototype/PlayerInventory.cs
  Assets/CombatPrototype/CombatHealth.cs
  ProjectSettings/ProjectSettings.asset
  Packages/manifest.json
  Packages/packages-lock.json
)
printf "path\tbase_blob\thead_blob\tidentical\n" > "$OUT"
bad=0
for p in "${PATHS[@]}"; do
  # A path that exists in neither the baseline nor the tree cannot be protected.
  if ! git cat-file -e "$BASE:$p" 2>/dev/null; then
    printf "%s\tMISSING_AT_BASE\t-\tERROR\n" "$p" >> "$OUT"
    bad=1
    continue
  fi
  b=$(git rev-parse "$BASE:$p")
  h=$(git rev-parse "HEAD:$p" 2>/dev/null || echo "MISSING_AT_HEAD")
  if git diff --quiet "$BASE" -- "$p"; then same=YES; else same=NO; bad=1; fi
  printf "%s\t%s\t%s\t%s\n" "$p" "$b" "$h" "$same" >> "$OUT"
done
awk -F'\t' 'NR>1 && $4!="YES"{print "CHANGED: "$0}' "$OUT"
echo "wrote $OUT"
if [ "$bad" -ne 0 ]; then
  echo "RESULT: NOT_ALL_IDENTICAL"
  exit 1
fi
echo "RESULT: ALL_IDENTICAL"
