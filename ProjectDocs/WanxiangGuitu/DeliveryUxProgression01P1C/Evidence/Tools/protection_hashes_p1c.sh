#!/usr/bin/env bash
# P1C 保护比对：本批（P1C）相对 P1 交付点是否改动受保护文件。
# 与 P1 的 protection_hashes.sh 同口径：判定只用 `git diff --quiet`，
# 不比较工作区原始字节（CRLF 会误报），不把缺失文件当"相同"。
# BASE 取 P1 交付提交 ff81eb1cb（P1C 的全部内容应是"工具 + 证据 + 文档"）。
set -u
cd /i/unity/WanxiangGuitu || exit 1
BASE=ff81eb1cb
OUT=ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/PROTECTION_HASHES.tsv
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
  Assets/CombatPrototype/ObjectiveCatalog.cs
  Assets/CombatPrototype/ObjectiveEvaluator.cs
  Assets/CombatPrototype/AdventureFlow.Objectives.cs
  Assets/CombatPrototype/RouteCards.cs
  Assets/CombatPrototype/SkillTradeoffs.cs
  ProjectSettings/ProjectSettings.asset
  Packages/manifest.json
  Packages/packages-lock.json
)
printf "path\tbase_blob\thead_blob\tidentical\n" > "$OUT"
bad=0
for p in "${PATHS[@]}"; do
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
