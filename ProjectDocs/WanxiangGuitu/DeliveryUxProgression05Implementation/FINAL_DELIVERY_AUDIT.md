# UX-05 ObjectiveHistory v10 最终交付审计

**CONDITIONAL_PASS。** 产品、最终构建运行和历史证据可核验。F-02正式登记为 **OWNER_ACCEPTED_HISTORICAL_LIMITATION**，不再追溯或修复。5659条精确提交候选已逐路径核验，尚未暂存。提交前须复审字节规范化、ignored日志和LFS载荷门禁。

日期：2026-11-20。依据根AGENTS.md及本轮任务书。唯一既有文件改动是FINAL_RISK_REGISTER.md追加负责人裁决；新建本报告及两份白名单。没有产品/Schema/存档/历史工件/旧INDEX修改，没有构建、Player、新Run或Git Index操作。

## 当前结论

| 项目 | 结论 | 范围 |
| --- | --- | --- |
| Git | PASS | 分支/HEAD/tree/merge-base实测，Index空；远端经GitHub只读API核验 |
| 产品与Schema | PASS（已验证范围） | 六字段、v9迁移、事务/裁剪/双UI/D-20/D-23与源码和原证据相符 |
| 构建 | PASS（既有最终身份/运行） | 三类SHA匹配；纯构建4条正常原生运行，另2条中断保留 |
| 历史运行 | PASS（分类保留） | 159历史+6收尾=165唯一Run，含9条IMGUI中间尝试 |
| 可复现性 | OWNER_ACCEPTED_HISTORICAL_LIMITATION | 114条/18个SHA/31条R1 PASS不能位级复现Driver；保留历史结论 |
| 历史保护 | PASS | 4142原始项与5404旧索引项SHA/大小匹配，失败目录保留 |
| 提交候选 | CONDITIONAL_PASS | 5659条路径/SHA通过；规范化、ignored、LFS门禁待复审 |
| 整体 | CONDITIONAL_PASS | F-02已接受，不扩大验证环境，不自动授权提交 |

## Git实测

分支：feature/ux-progression-05-objective-history；HEAD：ae705b944b7d0fe851fbd395229dfc30ec636f5c；HEAD tree：64ded86dbabd22ff2e668445055d87fc7b102116。
HEAD parent：95caf234256613d4a6e4f89a8ab0dc09c397c6b2；与本地B2及origin/B2的merge-base均为HEAD；与main的merge-base：72db192a527bd256e2ba18cd7ab334d8334051da。HEAD仍是B2起点，不代表未提交产品DLL身份。
本地UX-05无upstream；B2和origin/B2均为ae705b944b7d0fe851fbd395229dfc30ec636f5c。Git传输两次连接重置、一次HTTP/1.1连接失败，未fetch。改用当前GitHub只读GET核验：远端B2仍为该SHA，无UX-05远端分支，main为72db192a527bd256e2ba18cd7ab334d8334051da。没有把cached引用当远端实测。
远端依据：[feature前缀引用](https://api.github.com/repos/mizunagare/BallMaze/git/matching-refs/heads/feature/ux-progression-0)、[main](https://api.github.com/repos/mizunagare/BallMaze/branches/main)。
tracked modified=11、tracked added=0、deleted=0、staged=0。开工untracked8959文件，结束8962（新增3文件）；ignored75890文件。既有修改保留。
Git Index SHA256前后均为5A03EB17D73F6F02167F382787C1AE7BBA4EC8BCC1FD1E71532C363DE4BB1FC1。sparse-checkout启用且未变，core.autocrlf=true；git diff --check退出0，仅CombatSaveSystem.Location.cs既有LF/CRLF提示。

### tracked modified（既有UX-05实施）

- Assets/CombatPrototype/AdventureFlow.Objectives.cs
- Assets/CombatPrototype/AdventureFlow.UI.cs
- Assets/CombatPrototype/AdventureFlow.cs
- Assets/CombatPrototype/AdventureRules.cs
- Assets/CombatPrototype/AdventureState.cs
- Assets/CombatPrototype/AdventureValidation.cs
- Assets/CombatPrototype/CombatSaveSystem.Entry.cs
- Assets/CombatPrototype/CombatSaveSystem.Location.cs
- Assets/CombatPrototype/CombatSaveSystem.cs
- Assets/CombatPrototype/GameEntry.cs
- Assets/CombatPrototype/ObjectiveCatalog.cs

### tracked added / staged

均为空。SaveSchemaMigration.cs及meta当前为untracked；候选ADD指未来提交动作，不表示已tracked或staged。

### untracked（Git合并显示）

以下按git status --untracked-files=normal逐项列coalesced项。8959个untracked及75890个ignored由git ls-files -z全量枚举统计；目录项绝不代表整体入选，逐文件候选只以白名单为准。

```text
?? AGENTS.md
?? Assets/CombatPrototype/SaveSchemaMigration.cs
?? Assets/CombatPrototype/SaveSchemaMigration.cs.meta
?? Assets/Resources.meta
?? Evidence/PH-R2-FINAL-AUDIT/
?? Evidence/PH-R2-R1/
?? Evidence/PH-R2/
?? Evidence/Runs/R01-20261111-112957/
?? Evidence/Runs/R01-20261111-113957/
?? Evidence/Runs/R01-20261111-120707/
?? Evidence/Runs/R02-20261111-113957/
?? Evidence/Runs/R02-20261111-120707/
?? Evidence/Runs/R03-20261111-113957/
?? Evidence/Runs/R03-20261111-120707/
?? Evidence/Runs/R04-20261111-113957/
?? Evidence/Runs/R04-20261111-120707/
?? Evidence/Runs/R05-20261111-113957/
?? Evidence/Runs/R05-20261111-120707/
?? Evidence/Runs/R06-20261111-113957/
?? Evidence/Runs/R06-20261111-120707/
?? Evidence/Runs/R07-20261111-113957/
?? Evidence/Runs/R07-20261111-120707/
?? Evidence/Runs/R08-20261111-113957/
?? Evidence/Runs/R08-20261111-120707/
?? Evidence/Runs/R09-20261111-113957/
?? Evidence/Runs/R09-20261111-120707/
?? Evidence/Runs/R10-20261111-113957/
?? Evidence/Runs/R10-20261111-120707/
?? Evidence/Runs/R11-20261111-113957/
?? Evidence/Runs/R11-20261111-120707/
?? Evidence/Runs/R12-20261111-113957/
?? Evidence/Runs/R12-20261111-120707/
?? Evidence/Runs/R13-20261111-113957/
?? Evidence/Runs/R13-20261111-120014/
?? Evidence/Runs/R13-20261111-120707/
?? Evidence/Runs/R14-20261111-113957/
?? Evidence/Runs/R14-20261111-120014/
?? Evidence/Runs/R14-20261111-120707/
?? Evidence/Runs/R15-20261111-113957/
?? Evidence/Runs/R15-20261111-120707/
?? Evidence/Runs/R16-20261111-113957/
?? Evidence/Runs/R16-20261111-120707/
?? Evidence/Runs/R17-20261111-113957/
?? Evidence/Runs/R17-20261111-120707/
?? Evidence/Runs/R18-20261111-113957/
?? Evidence/Runs/R18-20261111-120707/
?? Evidence/Runs/R19-20261111-113957/
?? Evidence/Runs/R19-20261111-120707/
?? Evidence/Runs/SELFTEST-positive-094414/
?? Evidence/Runs/SELFTEST-positive-095104/
?? Evidence/Runs/SELFTEST-positive-100045/
?? Evidence/Runs/SELFTEST-positive-100506/
?? Evidence/Runs/SELFTEST-positive-101400/
?? Evidence/Runs/SELFTEST-positive-101730/
?? Evidence/Runs/SELFTEST-positive-102139/
?? Evidence/Runs/SELFTEST-positive-102429/
?? Evidence/Runs/SELFTEST-positive-113726/
?? Evidence/Runs/SELFTEST-positive-113913/
?? Evidence/Runs/SELFTEST-positive-120623/
?? Evidence/Runs/SELFTEST-stale-094414/
?? Evidence/Runs/SELFTEST-stale-095104/
?? Evidence/Runs/SELFTEST-stale-100045/
?? Evidence/Runs/SELFTEST-stale-100506/
?? Evidence/Runs/SELFTEST-stale-101400/
?? Evidence/Runs/SELFTEST-stale-101730/
?? Evidence/Runs/SELFTEST-stale-102139/
?? Evidence/Runs/SELFTEST-stale-102429/
?? Evidence/Runs/SELFTEST-stale-113726/
?? Evidence/Runs/SELFTEST-stale-113913/
?? Evidence/Runs/SELFTEST-stale-120623/
?? Evidence/Runs/SELFTEST-timeout-094414/
?? Evidence/Runs/SELFTEST-timeout-095104/
?? Evidence/Runs/SELFTEST-timeout-100045/
?? Evidence/Runs/SELFTEST-timeout-100506/
?? Evidence/Runs/SELFTEST-timeout-101400/
?? Evidence/Runs/SELFTEST-timeout-101730/
?? Evidence/Runs/SELFTEST-timeout-102139/
?? Evidence/Runs/SELFTEST-timeout-102429/
?? Evidence/Runs/SELFTEST-timeout-113726/
?? Evidence/Runs/SELFTEST-timeout-113913/
?? Evidence/Runs/SELFTEST-timeout-120623/
?? Evidence/Runs/SELFTEST-wrongsha-094414/
?? Evidence/Runs/SELFTEST-wrongsha-095104/
?? Evidence/Runs/SELFTEST-wrongsha-100045/
?? Evidence/Runs/SELFTEST-wrongsha-100506/
?? Evidence/Runs/SELFTEST-wrongsha-101400/
?? Evidence/Runs/SELFTEST-wrongsha-101730/
?? Evidence/Runs/SELFTEST-wrongsha-102139/
?? Evidence/Runs/SELFTEST-wrongsha-102429/
?? Evidence/Runs/SELFTEST-wrongsha-113726/
?? Evidence/Runs/SELFTEST-wrongsha-113913/
?? Evidence/Runs/SELFTEST-wrongsha-120623/
?? Evidence/Runs03/
?? Evidence/Runs03R1/
?? Evidence/Runs03R1C/
?? Evidence/Runs03R2/
?? Evidence/Runs03R2b/
?? Evidence/Runs04B0/
?? Evidence/Runs04B1/_builds/
?? Evidence/Runs04B1/_roots/
?? Evidence/Runs04B2/_build/Assembly-CSharp.ref.dll
?? Evidence/Runs04B2/runs/
?? Evidence/Runs04B2R1/SESSION-20261116-1115/_build/Assembly-CSharp.ref.dll
?? Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/
?? Evidence/Runs04B2R1/_build/Assembly-CSharp.ref.dll
?? Evidence/Runs04B2R2/SESSION-20261116-R2-01/_roots/
?? Evidence/Runs04B2R2FIX/FINAL-A02/_roots/
?? Evidence/Runs04B2R2FIX/FLOAT-GATE/_roots/
?? Evidence/Runs04B2R2FIX/UI-A01/_roots/
?? Evidence/Runs04B2R2FIX/UI-A02/_roots/
?? Evidence/Runs04B2R2FIX/UI-A03/_roots/
?? Evidence/Runs04B2R2FIX/UI-A04-PROBE/_roots/
?? Evidence/Runs04B2R2FIX/UI-A05/_roots/
?? Evidence/Runs04B2R2FIX/UI-A06-PROBE/_roots/
?? Evidence/Runs04B2R2FIX/UI-A07/_roots/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03Impl/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03ImplR1/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03ImplR1C/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03ImplR2/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression03ImplR2b/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B0/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B1/FINAL_AUDIT.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B1/PUSH_REPORT.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B1/SUBMIT_WHITELIST.txt
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B1/Tools/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/player/structure.txt
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/player/structure_utf8.txt
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_RISK_RECHECK.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/COMMIT_REPORT.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/COMMIT_TOOLS/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_PACKAGE.zip
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_PACKAGE_SHA256.txt
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_AUDIT.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_AUDIT_SEMANTIC.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_EXCEPTIONS.md
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_MANIFEST.csv
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_SEMANTIC_MANIFEST.csv
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_SEMANTIC_TOOLS/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/STAGING_TOOLS/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Preflight/
```

### ignored（matching合并显示）

与untracked分列；Library、Builds、Temp和缓存不入选。267个受ignore影响的正式Run/Build/编译原始日志逐路径标记，等待复审，不执行-f。

```text
!! .workbuddy/
!! Assembly-CSharp-Editor.csproj
!! Assembly-CSharp.csproj
!! Builds/
!! Evidence/PH-R2-R1/runs/C-GATE/harness.log
!! Evidence/PH-R2-R1/runs/C-GATE/player.log
!! Evidence/PH-R2-R1/runs/STAFF-FIELD/harness.log
!! Evidence/PH-R2-R1/runs/STAFF-FIELD/player.log
!! Evidence/PH-R2-R1/runs/TWIN-COUNTER/harness.log
!! Evidence/PH-R2-R1/runs/TWIN-COUNTER/player.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-positive-153637/harness.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-positive-153637/player.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-stale-153637/harness.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-stale-153637/player.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-timeout-153637/harness.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-timeout-153637/player.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-wrongdllsha-153637/harness.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-wrongdllsha-153637/player.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-wrongsha-153637/harness.log
!! Evidence/PH-R2-R1/selftest/SELFTEST-wrongsha-153637/player.log
!! Evidence/PH-R2-R1/selftest/console.log
!! Evidence/PH-R2/all_console.log
!! Evidence/PH-R2/all_console_final.log
!! Evidence/PH-R2/selftest_console.log
!! Evidence/PH-R2/t3_retry.log
!! Evidence/Runs/R01-20261110-174744/harness.log
!! Evidence/Runs/R01-20261110-174744/player.log
!! Evidence/Runs/R01-20261111-112957/harness.log
!! Evidence/Runs/R01-20261111-112957/player.log
!! Evidence/Runs/R01-20261111-113957/harness.log
!! Evidence/Runs/R01-20261111-113957/player.log
!! Evidence/Runs/R01-20261111-120707/harness.log
!! Evidence/Runs/R01-20261111-120707/player.log
!! Evidence/Runs/R01/harness.log
!! Evidence/Runs/R01/player.log
!! Evidence/Runs/R02-20261110-174744/harness.log
!! Evidence/Runs/R02-20261110-174744/player.log
!! Evidence/Runs/R02-20261111-113957/harness.log
!! Evidence/Runs/R02-20261111-113957/player.log
!! Evidence/Runs/R02-20261111-120707/harness.log
!! Evidence/Runs/R02-20261111-120707/player.log
!! Evidence/Runs/R02/harness.log
!! Evidence/Runs/R02/player.log
!! Evidence/Runs/R03-20261110-174744/harness.log
!! Evidence/Runs/R03-20261110-174744/player.log
!! Evidence/Runs/R03-20261111-113957/harness.log
!! Evidence/Runs/R03-20261111-113957/player.log
!! Evidence/Runs/R03-20261111-120707/harness.log
!! Evidence/Runs/R03-20261111-120707/player.log
!! Evidence/Runs/R03/harness.log
!! Evidence/Runs/R03/player.log
!! Evidence/Runs/R04-20261110-174744/harness.log
!! Evidence/Runs/R04-20261110-174744/player.log
!! Evidence/Runs/R04-20261111-113957/harness.log
!! Evidence/Runs/R04-20261111-113957/player.log
!! Evidence/Runs/R04-20261111-120707/harness.log
!! Evidence/Runs/R04-20261111-120707/player.log
!! Evidence/Runs/R04/harness.log
!! Evidence/Runs/R04/player.log
!! Evidence/Runs/R05-20261110-174744/harness.log
!! Evidence/Runs/R05-20261110-174744/player.log
!! Evidence/Runs/R05-20261111-113957/harness.log
!! Evidence/Runs/R05-20261111-113957/player.log
!! Evidence/Runs/R05-20261111-120707/harness.log
!! Evidence/Runs/R05-20261111-120707/player.log
!! Evidence/Runs/R05/harness.log
!! Evidence/Runs/R05/player.log
!! Evidence/Runs/R06-20261110-174744/harness.log
!! Evidence/Runs/R06-20261110-174744/player.log
!! Evidence/Runs/R06-20261111-113957/harness.log
!! Evidence/Runs/R06-20261111-113957/player.log
!! Evidence/Runs/R06-20261111-120707/harness.log
!! Evidence/Runs/R06-20261111-120707/player.log
!! Evidence/Runs/R06/harness.log
!! Evidence/Runs/R06/player.log
!! Evidence/Runs/R07-20261110-174744/harness.log
!! Evidence/Runs/R07-20261110-174744/player.log
!! Evidence/Runs/R07-20261111-113957/harness.log
!! Evidence/Runs/R07-20261111-113957/player.log
!! Evidence/Runs/R07-20261111-120707/harness.log
!! Evidence/Runs/R07-20261111-120707/player.log
!! Evidence/Runs/R07/harness.log
!! Evidence/Runs/R07/player.log
!! Evidence/Runs/R08-20261110-174744/harness.log
!! Evidence/Runs/R08-20261110-174744/player.log
!! Evidence/Runs/R08-20261111-113957/harness.log
!! Evidence/Runs/R08-20261111-113957/player.log
!! Evidence/Runs/R08-20261111-120707/harness.log
!! Evidence/Runs/R08-20261111-120707/player.log
!! Evidence/Runs/R08/harness.log
!! Evidence/Runs/R08/player.log
!! Evidence/Runs/R09-20261110-174744/harness.log
!! Evidence/Runs/R09-20261110-174744/player.log
!! Evidence/Runs/R09-20261111-113957/harness.log
!! Evidence/Runs/R09-20261111-113957/player.log
!! Evidence/Runs/R09-20261111-120707/harness.log
!! Evidence/Runs/R09-20261111-120707/player.log
!! Evidence/Runs/R09/harness.log
!! Evidence/Runs/R09/player.log
!! Evidence/Runs/R10-20261110-174744/harness.log
!! Evidence/Runs/R10-20261110-174744/player.log
!! Evidence/Runs/R10-20261111-113957/harness.log
!! Evidence/Runs/R10-20261111-113957/player.log
!! Evidence/Runs/R10-20261111-120707/harness.log
!! Evidence/Runs/R10-20261111-120707/player.log
!! Evidence/Runs/R10/harness.log
!! Evidence/Runs/R10/player.log
!! Evidence/Runs/R11-20261110-174744/harness.log
!! Evidence/Runs/R11-20261110-174744/player.log
!! Evidence/Runs/R11-20261111-113957/harness.log
!! Evidence/Runs/R11-20261111-113957/player.log
!! Evidence/Runs/R11-20261111-120707/harness.log
!! Evidence/Runs/R11-20261111-120707/player.log
!! Evidence/Runs/R11/harness.log
!! Evidence/Runs/R11/player.log
!! Evidence/Runs/R12-20261110-174744/harness.log
!! Evidence/Runs/R12-20261110-174744/player.log
!! Evidence/Runs/R12-20261111-113957/harness.log
!! Evidence/Runs/R12-20261111-113957/player.log
!! Evidence/Runs/R12-20261111-120707/harness.log
!! Evidence/Runs/R12-20261111-120707/player.log
!! Evidence/Runs/R12/harness.log
!! Evidence/Runs/R12/player.log
!! Evidence/Runs/R13-20261110-174744/harness.log
!! Evidence/Runs/R13-20261110-174744/player.log
!! Evidence/Runs/R13-20261111-113957/harness.log
!! Evidence/Runs/R13-20261111-113957/player.log
!! Evidence/Runs/R13-20261111-120014/harness.log
!! Evidence/Runs/R13-20261111-120014/player.log
!! Evidence/Runs/R13-20261111-120707/harness.log
!! Evidence/Runs/R13-20261111-120707/player.log
!! Evidence/Runs/R13/harness.log
!! Evidence/Runs/R13/player.log
!! Evidence/Runs/R14-20261110-174744/harness.log
!! Evidence/Runs/R14-20261110-174744/player.log
!! Evidence/Runs/R14-20261111-113957/harness.log
!! Evidence/Runs/R14-20261111-113957/player.log
!! Evidence/Runs/R14-20261111-120014/harness.log
!! Evidence/Runs/R14-20261111-120014/player.log
!! Evidence/Runs/R14-20261111-120707/harness.log
!! Evidence/Runs/R14-20261111-120707/player.log
!! Evidence/Runs/R14/harness.log
!! Evidence/Runs/R14/player.log
!! Evidence/Runs/R15-20261110-174744/harness.log
!! Evidence/Runs/R15-20261110-174744/player.log
!! Evidence/Runs/R15-20261111-113957/harness.log
!! Evidence/Runs/R15-20261111-113957/player.log
!! Evidence/Runs/R15-20261111-120707/harness.log
!! Evidence/Runs/R15-20261111-120707/player.log
!! Evidence/Runs/R15/harness.log
!! Evidence/Runs/R15/player.log
!! Evidence/Runs/R16-20261110-174744/harness.log
!! Evidence/Runs/R16-20261110-174744/player.log
!! Evidence/Runs/R16-20261111-113957/harness.log
!! Evidence/Runs/R16-20261111-113957/player.log
!! Evidence/Runs/R16-20261111-120707/harness.log
!! Evidence/Runs/R16-20261111-120707/player.log
!! Evidence/Runs/R16/harness.log
!! Evidence/Runs/R16/player.log
!! Evidence/Runs/R17-20261110-174744/harness.log
!! Evidence/Runs/R17-20261110-174744/player.log
!! Evidence/Runs/R17-20261111-113957/harness.log
!! Evidence/Runs/R17-20261111-113957/player.log
!! Evidence/Runs/R17-20261111-120707/harness.log
!! Evidence/Runs/R17-20261111-120707/player.log
!! Evidence/Runs/R17/harness.log
!! Evidence/Runs/R17/player.log
!! Evidence/Runs/R18-20261110-174744/harness.log
!! Evidence/Runs/R18-20261110-174744/player.log
!! Evidence/Runs/R18-20261111-113957/harness.log
!! Evidence/Runs/R18-20261111-113957/player.log
!! Evidence/Runs/R18-20261111-120707/harness.log
!! Evidence/Runs/R18-20261111-120707/player.log
!! Evidence/Runs/R18/harness.log
!! Evidence/Runs/R18/player.log
!! Evidence/Runs/R19-20261110-174744/harness.log
!! Evidence/Runs/R19-20261110-174744/player.log
!! Evidence/Runs/R19-20261111-113957/harness.log
!! Evidence/Runs/R19-20261111-113957/player.log
!! Evidence/Runs/R19-20261111-120707/harness.log
!! Evidence/Runs/R19-20261111-120707/player.log
!! Evidence/Runs/R19/harness.log
!! Evidence/Runs/R19/player.log
!! Evidence/Runs/SAMPLE01/harness.log
!! Evidence/Runs/SAMPLE01/player.log
!! Evidence/Runs/SAMPLE03/harness.log
!! Evidence/Runs/SAMPLE03/player.log
!! Evidence/Runs/SAMPLE10/harness.log
!! Evidence/Runs/SAMPLE10/player.log
!! Evidence/Runs/SELFTEST-positive-094414/harness.log
!! Evidence/Runs/SELFTEST-positive-094414/player.log
!! Evidence/Runs/SELFTEST-positive-095104/harness.log
!! Evidence/Runs/SELFTEST-positive-095104/player.log
!! Evidence/Runs/SELFTEST-positive-100045/harness.log
!! Evidence/Runs/SELFTEST-positive-100045/player.log
!! Evidence/Runs/SELFTEST-positive-100506/harness.log
!! Evidence/Runs/SELFTEST-positive-100506/player.log
!! Evidence/Runs/SELFTEST-positive-101400/harness.log
!! Evidence/Runs/SELFTEST-positive-101400/player.log
!! Evidence/Runs/SELFTEST-positive-101730/harness.log
!! Evidence/Runs/SELFTEST-positive-101730/player.log
!! Evidence/Runs/SELFTEST-positive-102139/harness.log
!! Evidence/Runs/SELFTEST-positive-102139/player.log
!! Evidence/Runs/SELFTEST-positive-102429/harness.log
!! Evidence/Runs/SELFTEST-positive-102429/player.log
!! Evidence/Runs/SELFTEST-positive-113726/harness.log
!! Evidence/Runs/SELFTEST-positive-113726/player.log
!! Evidence/Runs/SELFTEST-positive-113913/harness.log
!! Evidence/Runs/SELFTEST-positive-113913/player.log
!! Evidence/Runs/SELFTEST-positive-120623/harness.log
!! Evidence/Runs/SELFTEST-positive-120623/player.log
!! Evidence/Runs/SELFTEST-positive-172920/harness.log
!! Evidence/Runs/SELFTEST-positive-172920/player.log
!! Evidence/Runs/SELFTEST-positive-173653/harness.log
!! Evidence/Runs/SELFTEST-positive-173653/player.log
!! Evidence/Runs/SELFTEST-positive/harness.log
!! Evidence/Runs/SELFTEST-positive/player.log
!! Evidence/Runs/SELFTEST-stale-094414/harness.log
!! Evidence/Runs/SELFTEST-stale-094414/player.log
!! Evidence/Runs/SELFTEST-stale-095104/harness.log
!! Evidence/Runs/SELFTEST-stale-095104/player.log
!! Evidence/Runs/SELFTEST-stale-100045/harness.log
!! Evidence/Runs/SELFTEST-stale-100045/player.log
!! Evidence/Runs/SELFTEST-stale-100506/harness.log
!! Evidence/Runs/SELFTEST-stale-100506/player.log
!! Evidence/Runs/SELFTEST-stale-101400/harness.log
!! Evidence/Runs/SELFTEST-stale-101400/player.log
!! Evidence/Runs/SELFTEST-stale-101730/harness.log
!! Evidence/Runs/SELFTEST-stale-101730/player.log
!! Evidence/Runs/SELFTEST-stale-102139/harness.log
!! Evidence/Runs/SELFTEST-stale-102139/player.log
!! Evidence/Runs/SELFTEST-stale-102429/harness.log
!! Evidence/Runs/SELFTEST-stale-102429/player.log
!! Evidence/Runs/SELFTEST-stale-113726/harness.log
!! Evidence/Runs/SELFTEST-stale-113726/player.log
!! Evidence/Runs/SELFTEST-stale-113913/harness.log
!! Evidence/Runs/SELFTEST-stale-113913/player.log
!! Evidence/Runs/SELFTEST-stale-120623/harness.log
!! Evidence/Runs/SELFTEST-stale-120623/player.log
!! Evidence/Runs/SELFTEST-stale-172920/harness.log
!! Evidence/Runs/SELFTEST-stale-172920/player.log
!! Evidence/Runs/SELFTEST-stale-173653/harness.log
!! Evidence/Runs/SELFTEST-stale-173653/player.log
!! Evidence/Runs/SELFTEST-stale/harness.log
!! Evidence/Runs/SELFTEST-stale/player.log
!! Evidence/Runs/SELFTEST-timeout-094414/harness.log
!! Evidence/Runs/SELFTEST-timeout-094414/player.log
!! Evidence/Runs/SELFTEST-timeout-095104/harness.log
!! Evidence/Runs/SELFTEST-timeout-095104/player.log
!! Evidence/Runs/SELFTEST-timeout-100045/harness.log
!! Evidence/Runs/SELFTEST-timeout-100045/player.log
!! Evidence/Runs/SELFTEST-timeout-100506/harness.log
!! Evidence/Runs/SELFTEST-timeout-100506/player.log
!! Evidence/Runs/SELFTEST-timeout-101400/harness.log
!! Evidence/Runs/SELFTEST-timeout-101400/player.log
!! Evidence/Runs/SELFTEST-timeout-101730/harness.log
!! Evidence/Runs/SELFTEST-timeout-101730/player.log
!! Evidence/Runs/SELFTEST-timeout-102139/harness.log
!! Evidence/Runs/SELFTEST-timeout-102139/player.log
!! Evidence/Runs/SELFTEST-timeout-102429/harness.log
!! Evidence/Runs/SELFTEST-timeout-102429/player.log
!! Evidence/Runs/SELFTEST-timeout-113726/harness.log
!! Evidence/Runs/SELFTEST-timeout-113726/player.log
!! Evidence/Runs/SELFTEST-timeout-113913/harness.log
!! Evidence/Runs/SELFTEST-timeout-113913/player.log
!! Evidence/Runs/SELFTEST-timeout-120623/harness.log
!! Evidence/Runs/SELFTEST-timeout-120623/player.log
!! Evidence/Runs/SELFTEST-timeout-172920/harness.log
!! Evidence/Runs/SELFTEST-timeout-172920/player.log
!! Evidence/Runs/SELFTEST-timeout-173653/harness.log
!! Evidence/Runs/SELFTEST-timeout-173653/player.log
!! Evidence/Runs/SELFTEST-timeout/harness.log
!! Evidence/Runs/SELFTEST-timeout/player.log
!! Evidence/Runs/SELFTEST-wrongsha-094414/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-094414/player.log
!! Evidence/Runs/SELFTEST-wrongsha-095104/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-095104/player.log
!! Evidence/Runs/SELFTEST-wrongsha-100045/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-100045/player.log
!! Evidence/Runs/SELFTEST-wrongsha-100506/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-100506/player.log
!! Evidence/Runs/SELFTEST-wrongsha-101400/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-101400/player.log
!! Evidence/Runs/SELFTEST-wrongsha-101730/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-101730/player.log
!! Evidence/Runs/SELFTEST-wrongsha-102139/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-102139/player.log
!! Evidence/Runs/SELFTEST-wrongsha-102429/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-102429/player.log
!! Evidence/Runs/SELFTEST-wrongsha-113726/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-113726/player.log
!! Evidence/Runs/SELFTEST-wrongsha-113913/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-113913/player.log
!! Evidence/Runs/SELFTEST-wrongsha-120623/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-120623/player.log
!! Evidence/Runs/SELFTEST-wrongsha-172920/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-172920/player.log
!! Evidence/Runs/SELFTEST-wrongsha-173653/harness.log
!! Evidence/Runs/SELFTEST-wrongsha-173653/player.log
!! Evidence/Runs/SELFTEST-wrongsha/harness.log
!! Evidence/Runs/SELFTEST-wrongsha/player.log
!! Evidence/Runs03/UX03-CD-01/harness03.log
!! Evidence/Runs03/UX03-CD-01/player.log
!! Evidence/Runs03/UX03-CD-02/harness03.log
!! Evidence/Runs03/UX03-CD-02/player.log
!! Evidence/Runs03/UX03-PULL-01/harness.log
!! Evidence/Runs03/UX03-PULL-01/player.log
!! Evidence/Runs03/UX03-PULL-02/harness.log
!! Evidence/Runs03/UX03-PULL-02/player.log
!! Evidence/Runs03/UX03-PULL-03/harness.log
!! Evidence/Runs03/UX03-PULL-03/player.log
!! Evidence/Runs03/UX03-SLOT0-01/harness03.log
!! Evidence/Runs03/UX03-SLOT0-01/player.log
!! Evidence/Runs03/UX03-WIN-01/harness03.log
!! Evidence/Runs03/UX03-WIN-01/player.log
!! Evidence/Runs03/UX03-WIN-02/harness03.log
!! Evidence/Runs03/UX03-WIN-02/player.log
!! Evidence/Runs03R1/UX03-R1-CD-01/harness03.log
!! Evidence/Runs03R1/UX03-R1-CD-01/player.log
!! Evidence/Runs03R1/UX03-R1-CD-01B/harness03.log
!! Evidence/Runs03R1/UX03-R1-CD-01B/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-1080/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-1080/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-1440/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-1440/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-720/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT-720/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L1080/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L1080/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L1200/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L1200/player.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L720/harness03.log
!! Evidence/Runs03R1/UX03-R1-LAYOUT2-L720/player.log
!! Evidence/Runs03R1/UX03-R1-P1-CAVERN/Player.log
!! Evidence/Runs03R1/UX03-R1-P1-FOREST-02/Player.log
!! Evidence/Runs03R1/UX03-R1-P1-FOREST/Player.log
!! Evidence/Runs03R1/UX03-R1-P1-RUINS/Player.log
!! Evidence/Runs03R1/UX03-R1-PULL-01/harness.log
!! Evidence/Runs03R1/UX03-R1-PULL-01/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-01B/harness.log
!! Evidence/Runs03R1/UX03-R1-PULL-01B/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-02/harness.log
!! Evidence/Runs03R1/UX03-R1-PULL-02/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-02B/harness.log
!! Evidence/Runs03R1/UX03-R1-PULL-02B/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND-02/harness03.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND-02/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND-03/harness03.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND-03/player.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND/harness03.log
!! Evidence/Runs03R1/UX03-R1-PULL-BOUND/player.log
!! Evidence/Runs03R1/UX03-R1-WIN-01/harness03.log
!! Evidence/Runs03R1/UX03-R1-WIN-01/player.log
!! Evidence/Runs03R1/UX03-R1-WIN-01B/harness03.log
!! Evidence/Runs03R1/UX03-R1-WIN-01B/player.log
!! Evidence/Runs03R1/_driver/evidence/driver-compile.log
!! Evidence/Runs03R1/_driver/r1-evidence/driver-compile.log
!! Evidence/Runs03R1/_roots/UX03-R1-P1-CAVERN/Player.log
!! Evidence/Runs03R1/_roots/UX03-R1-P1-FOREST-02/Player.log
!! Evidence/Runs03R1/_roots/UX03-R1-P1-FOREST/Player.log
!! Evidence/Runs03R1/_roots/UX03-R1-P1-RUINS/Player.log
!! Evidence/Runs03R1C/UX03-R1C-CAVERN-CHALLENGE-02/Player.log
!! Evidence/Runs03R1C/UX03-R1C-CAVERN-CHALLENGE-02/harness.log
!! Evidence/Runs03R1C/UX03-R1C-CAVERN-CHALLENGE/Player.log
!! Evidence/Runs03R1C/UX03-R1C-CAVERN-CHALLENGE/harness.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE-02/Player.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE-02/harness.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE-03/Player.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE-03/harness.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE/Player.log
!! Evidence/Runs03R1C/UX03-R1C-RUINS-CHALLENGE/harness.log
!! Evidence/Runs03R1C/_driver/r1c-evidence-02/driver-compile.log
!! Evidence/Runs03R1C/_driver/r1c-evidence-v3/driver-compile.log
!! Evidence/Runs03R1C/_driver/r1c-evidence/driver-compile.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-CAVERN-CHALLENGE-02/Player.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-CAVERN-CHALLENGE-02/harness.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-CAVERN-CHALLENGE/Player.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-CAVERN-CHALLENGE/harness.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE-02/Player.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE-02/harness.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE-03/Player.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE-03/harness.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE/Player.log
!! Evidence/Runs03R1C/_roots/UX03-R1C-RUINS-CHALLENGE/harness.log
!! Evidence/Runs03R2/UX03-R2-CD-01/harness03.log
!! Evidence/Runs03R2/UX03-R2-CD-01/player.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-1080/harness03.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-1080/player.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-1200/harness03.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-1200/player.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-720/harness03.log
!! Evidence/Runs03R2/UX03-R2-LAYOUT-720/player.log
!! Evidence/Runs03R2/UX03-R2-SLOT0-01/harness03.log
!! Evidence/Runs03R2/UX03-R2-SLOT0-01/player.log
!! Evidence/Runs03R2/UX03-R2-SPEAR0-01/harness03.log
!! Evidence/Runs03R2/UX03-R2-SPEAR0-01/player.log
!! Evidence/Runs03R2/UX03-R2-SPEAR0-02/harness03.log
!! Evidence/Runs03R2/UX03-R2-SPEAR0-02/player.log
!! Evidence/Runs03R2/UX03-R2-WIN-01/harness03.log
!! Evidence/Runs03R2/UX03-R2-WIN-01/player.log
!! Evidence/Runs03R2b/UX03-R2B-CD-01/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-CD-01/player.log
!! Evidence/Runs03R2b/UX03-R2B-LAYOUT-1080/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-LAYOUT-1080/player.log
!! Evidence/Runs03R2b/UX03-R2B-LAYOUT-720/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-LAYOUT-720/player.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-01/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-01/player.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-02/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-02/player.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-03/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-SLOT0SEVEN-03/player.log
!! Evidence/Runs03R2b/UX03-R2B-SPEAR0-01/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-SPEAR0-01/player.log
!! Evidence/Runs03R2b/UX03-R2B-WIN-01/harness03.log
!! Evidence/Runs03R2b/UX03-R2B-WIN-01/player.log
!! Evidence/Runs04B0/UX04-B0-CAVERN-01/Player.log
!! Evidence/Runs04B0/UX04-B0-CAVERN-01/harness.log
!! Evidence/Runs04B0/UX04-B0-CRAFT-01/Player.log
!! Evidence/Runs04B0/UX04-B0-CRAFT-01/harness.log
!! Evidence/Runs04B0/UX04-B0-DRVPROBE-01/Player.log
!! Evidence/Runs04B0/UX04-B0-DRVPROBE-01/harness.log
!! Evidence/Runs04B0/UX04-B0-EQUIPFLOW-01/Player.log
!! Evidence/Runs04B0/UX04-B0-FOREST-01/Player.log
!! Evidence/Runs04B0/UX04-B0-FOREST-01/harness.log
!! Evidence/Runs04B0/UX04-B0-PROBE-01/harness03.log
!! Evidence/Runs04B0/UX04-B0-PROBE-01/player.log
!! Evidence/Runs04B0/UX04-B0-READBACK-01/Player.log
!! Evidence/Runs04B0/UX04-B0-READBACK-01/harness.log
!! Evidence/Runs04B0/UX04-B0-READBACK-02/Player.log
!! Evidence/Runs04B0/UX04-B0-RUINS-01/Player.log
!! Evidence/Runs04B0/UX04-B0-RUINS-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-CAVERN-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-CAVERN-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-CRAFT-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-CRAFT-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-DRVPROBE-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-DRVPROBE-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-EQUIPFLOW-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-FOREST-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-FOREST-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-READBACK-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-READBACK-01/harness.log
!! Evidence/Runs04B0/_roots/UX04-B0-READBACK-02/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-RUINS-01/Player.log
!! Evidence/Runs04B0/_roots/UX04-B0-RUINS-01/harness.log
!! Evidence/Runs04B1/_builds/b1-driver-compile.log
!! Evidence/Runs04B1/_builds/b1_build_chain.log
!! Evidence/Runs04B1/_roots/UX04-B1-DISMANTLE-01/Player.log
!! Evidence/Runs04B1/_roots/UX04-B1-READBACK-01/Player.log
!! Evidence/Runs04B2/_build/Assembly-CSharp.pdb
!! Evidence/Runs04B2/runs/FAVSEED-01/Player.log
!! Evidence/Runs04B2/runs/FAVSEED-FINAL/Player.log
!! Evidence/Runs04B2/runs/GOLDEN-01/Player.log
!! Evidence/Runs04B2/runs/GOLDEN-02/Player.log
!! Evidence/Runs04B2/runs/GOLDEN-FINAL/Player.log
!! Evidence/Runs04B2/runs/IMGUI-01/Player.log
!! Evidence/Runs04B2/runs/IMGUI-02/Player.log
!! Evidence/Runs04B2/runs/IMGUI-03/Player.log
!! Evidence/Runs04B2/runs/IMGUI-04/Player.log
!! Evidence/Runs04B2/runs/IMGUI-FINAL/Player.log
!! Evidence/Runs04B2/runs/READBACK-01/Player.log
!! Evidence/Runs04B2/runs/READBACK-FINAL/Player.log
!! Evidence/Runs04B2/runs/RESTART-01/Player.log
!! Evidence/Runs04B2/runs/RESTART-02/Player.log
!! Evidence/Runs04B2/runs/RESTART-FINAL/Player.log
!! Evidence/Runs04B2/runs/UGUI-01/Player.log
!! Evidence/Runs04B2/runs/UGUI-02/Player.log
!! Evidence/Runs04B2/runs/UGUI-FINAL/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_build/Assembly-CSharp.pdb
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/collection/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/golden/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/guid/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/preview9/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/restart/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/sort-imgui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/sort-ugui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/strength0/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A01/strength3/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/collection/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/golden/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/guid/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/preview9/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/restart/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/sort-imgui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/sort-ugui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/strength0/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A02/strength3/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/collection/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/golden/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/guid/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/preview9/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/restart/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/sort-imgui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/sort-ugui/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/strength0/Player.log
!! Evidence/Runs04B2R1/SESSION-20261116-1115/_roots/A03/strength3/Player.log
!! Evidence/Runs04B2R1/_build/Assembly-CSharp.pdb
!! Evidence/Runs04B2R2/SESSION-20261116-R2-01/_roots/UX04B2R2-FLOAT-001/Player.log
!! Evidence/Runs04B2R2FIX/FINAL-A02/_roots/UX04B2R2FIX-FLOAT-FINAL-001/Player.log
!! Evidence/Runs04B2R2FIX/FLOAT-GATE/_roots/UX04B2R2FIX-FLOAT-001/Player.log
!! Evidence/Runs04B2R2FIX/UI-A01/_roots/UX04B2R2FIX-A01-accessory/Player.log
!! Evidence/Runs04B2R2FIX/UI-A02/_roots/UX04B2R2FIX-A02-accessory/Player.log
!! Evidence/Runs04B2R2FIX/UI-A02/_roots/UX04B2R2FIX-A02-arms/Player.log
!! Evidence/Runs04B2R2FIX/UI-A02/_roots/UX04B2R2FIX-A02-board-insufficient/Player.log
!! Evidence/Runs04B2R2FIX/UI-A02/_roots/UX04B2R2FIX-A02-main/Player.log
!! Evidence/Runs04B2R2FIX/UI-A03/_roots/UX04B2R2FIX-A03-accessory/Player.log
!! Evidence/Runs04B2R2FIX/UI-A03/_roots/UX04B2R2FIX-A03-arms/Player.log
!! Evidence/Runs04B2R2FIX/UI-A03/_roots/UX04B2R2FIX-A03-board-insufficient/Player.log
!! Evidence/Runs04B2R2FIX/UI-A03/_roots/UX04B2R2FIX-A03-main/Player.log
!! Evidence/Runs04B2R2FIX/UI-A04-PROBE/_roots/UX04B2R2FIX-A04-board-insufficient/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-accessory/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-arms/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-board-insufficient/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-illegal-swap/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-legal-swap/Player.log
!! Evidence/Runs04B2R2FIX/UI-A05/_roots/UX04B2R2FIX-A05-main/Player.log
!! Evidence/Runs04B2R2FIX/UI-A06-PROBE/_roots/UX04B2R2FIX-A06-illegal-swap/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-accessory/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-arms/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-board-insufficient/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-illegal-swap/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-legal-swap/Player.log
!! Evidence/Runs04B2R2FIX/UI-A07/_roots/UX04B2R2FIX-A07-main/Player.log
!! Evidence/cgate_probe.log
!! Library/
!! Logs/
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-3/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-4/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-5/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-6/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-7/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-8/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/cavern-boss-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/cavern-loop-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/cross-region-chain-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/fail-paths-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/fail-paths-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-3/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-4/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-5/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-6/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop-7/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/forest-loop/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/reward-loop-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/reward-loop-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/ruins-loop-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/ruins-loop-3/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/ruins-loop/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/skill-smoke-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/skill-smoke-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/skill-smoke-3/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/weapon-smoke-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/weapon-smoke-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/xproc-1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Player/xproc-2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Tools-records/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Bake1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/EditorPhase1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/EditorPhaseRestore1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/EditorStage1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/EditorStage1NonBatch/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/PlayerPhase1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/PlayerPhaseRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/PlayerSalvageRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/PlayerWindupA1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/PlayerWindupB1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Bake1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-AttackPairs1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-LifecycleObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-LifecycleObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-LifecycleObserved3.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-LifecycleObserved4.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-NormalObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-NormalObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-NormalRestoreObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-NormalRestoreObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-Phase2Observed1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-PillarPairs1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-RewardObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-RewardObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-RewardObserved3.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-RouteStates1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-RouteStates2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-Stage1Observed1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-Stage1Observed2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-Stage1Observed3.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-Stage1Observed4.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-WeaponsObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-WeaponsObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-WindupObserved1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Compilation/player-driver-compile-WindupObserved2.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorPhase1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorPhaseRestore1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorStaff1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorStage1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorStage1NonBatch/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorStage1Open/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorSword1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/EditorSword2/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Phase2PureBuild1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerClaimSalvage1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerNormalBankRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerNormalBankRestore2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerNormalRepeat1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerPendingFull1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerPendingFullRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerPhase1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerPhaseRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardAfter1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardAfterRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardBefore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardBefore1/WanxiangGuitu/ForestRuins/save.json.tmp
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardBefore2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardBeforeRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerRewardCamp1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerSalvageRestore1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerStaff1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerStage1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerStage1Bypass/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerStage1Open/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerSword1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon0A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon11A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon12A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon13A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon1A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon2A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWeapon3A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWindupA1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWindupA2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWindupB1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PlayerWindupB2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/PureTitleFinal1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Stage1PureBuild1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/Stage1PureBuild2/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p1-Claw-evade-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p1-Claw-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p1-Volley-evade-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p1-Volley-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-Claw-evade-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-Claw-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-CrossLines-evade-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-CrossLines-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-HollowRing-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-HollowRing-inner-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-HollowRing-outer-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-Volley-evade-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/pair-p2-Volley-hit-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/route-dead-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/route-three-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/route-three-A2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-block-0-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-block-1-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-block-11-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-block-12-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-block-13-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-clear-0-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-clear-1-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-clear-11-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-clear-12-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/weapon-clear-13-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/Evidence/Runs/Editor-RingContract-A1/Unity.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-c05-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-c05-A2/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-c05-A3/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-band-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-dodge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-inner-edge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-inner-safe-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-outer-edge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-outer-safe-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Player/r1-ring-wall-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild1/driver-compile-failed-1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild1/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild2/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild3/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild4/driver-compile-failed-1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/Runs/DriverBuild4/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-both-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-both-multi-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-first-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-none-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-second-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/b-trigger-child-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-boss-a-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-boss-w-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-death-a-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-death-w-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-leave-a-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-leave-w-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-unload-a-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/cancel-unload-w-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-above-cap-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-above-cc-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-in-cap-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-in-cc-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-just-out-cap-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-just-out-cc-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-tangent-bottom-cap-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-tangent-bottom-cc-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-tangent-top-cap-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/h-tangent-top-cc-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/pause-active-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/pause-warning-A1-FAILED/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/pause-warning-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/timescale-only-A1-FAILED/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Player/timescale-only-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Runs/DriverBuild1/driver-compile-failed-1.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Runs/DriverBuild1/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Runs/DriverBuild2/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/Runs/DriverBuild3/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/bow-charge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/bow-charge-cancel-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-baseline-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-death-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-dodge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-global-pause-4s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-natural-expire-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-switch-slot-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-switch-weapon-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-ui-only-2s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-ui-only-4s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/field-unload-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/restore-read-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Before/Player-Runs-Before/restore-write-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/bow-charge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/bow-charge-cancel-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-baseline-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-death-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-dodge-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-global-pause-4s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-natural-expire-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-switch-slot-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-switch-weapon-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-ui-only-2s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-ui-only-4s-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/field-unload-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/restore-read-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/restore-write-A1/Player.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Runs/DriverBuild1/driver-compile-failed-1.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Runs/DriverBuild1/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Runs/DriverBuild2/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B0/EVIDENCE/b0-driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-DRIVER-A01/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-cavern/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-forest/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-ruins/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/replay-driver/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a04.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a05.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-acceptance-a06.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-nodefine-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-nodefine-a02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-nodefine-a03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-release-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-release-a02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/unity-release-a03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-BOOT-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A02/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A02/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-RESTART-A02/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/driver-search-A02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/driver-search.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/REPLAY-DRIVER-A01/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-ABANDON-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-B1-B2-GATES-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-B1-FIXTURE-MIGRATE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-BACKUP-RESTORE-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-BAD-SHA-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CAPACITY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CAPACITY-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CAPACITY-REOPEN-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-CONTRACT-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-FUTURE-SOURCE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-LOCK-CONTENDER-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-LOCK-HOLDER-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATE-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATE-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATE-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATE-PAGED-PENDING-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATE-PAIR-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATION-CUT-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATION-CUT-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-NO-DEFINE-BOOT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-COMMIT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-REOPEN-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-UGUI-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-UI-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-OBJECTIVE-UI-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-P1C-cavern-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-P1C-forest-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-P1C-ruins-A01/Player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-PAGED-RESTORE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-PAIR-V9-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-PENDING-RESUME-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-PENDING-STOP-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-RELEASE-BOOT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-REPLAY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-A02/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/root/harness.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-V9-PAGED-PENDING-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-A3-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-A3-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-AFTER2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-AFTER2-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-ARCHIVE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-ARCHIVE-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-ARCHIVE2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-ARCHIVE2-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-B1B2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-B1B2-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-B1B2-FIXTURE-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-NODEFINE-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-RELEASE-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-nodefine-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-release-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-C3-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-C3-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CANDIDATE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CANDIDATE-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CANDIDATE2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CHECKSUM-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CHECKSUM-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-CONFLICT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-DUAL-BASE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-DUAL-OBJECTIVE-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-LEGACY-FUTURE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-LEGACY-NAMESPACE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-LOCK-CONTENDER-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-LOCK-HOLDER-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-P3-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-P3-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-PAGE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-PAGE-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-PAGE2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-PAGE2-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-Q3-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-Q3-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-RECEIPT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-RECEIPT2-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-RECEIPT2-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-REPLACE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-REPLACE-RECOVERY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-REPLAY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-RULES-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-SAVE-READBACK-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-SAVE-STALE-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-EMPTY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-REPEAT-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-UGUI-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-UGUI-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-UGUI-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-UI-UNKNOWN-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-contract-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-inventory-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-objective-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-player-sources-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-player-sources-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-bridged-v10-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-bridged-v10.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-bridged-v9-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-bridged-v9.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-v10.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-probe-v9.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-repeat-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-v9-fixture-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/roslyn-visual-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-04.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-05.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-06.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-07.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-08.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-09.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-10.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-acceptance-11.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-04.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-05.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-06.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-nodefine-07.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-03.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-04.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-05.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-06.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-07.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/unity-release-08.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/DRIVER-A01/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/DRIVER-A02/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/DRIVER-A03/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/DRIVER-A04/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/DRIVER-A05/driver-compile.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A04/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A05/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A06/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A01/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A02/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A03/player.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-acceptance-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-acceptance-a02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-nodefine-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-nodefine-a02.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-release-a01.log
!! ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/build-release-a02.log
!! UserSettings/
!! WanxiangGuitu.slnx
```

### sparse-checkout

```text
/Assets/
/Packages/
/ProjectSettings/
/ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC22/
/.gitattributes
ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B
ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1
README.md
ProjectDocs/WanxiangGuitu/DEVELOPMENT_PLAN.md
ProjectDocs/WanxiangGuitu/CURRENT_STATUS.md
ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/
ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/
ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/
ProjectDocs/WanxiangGuitu/DeliverySkillState01/
ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02
ProjectDocs/WanxiangGuitu/DeliveryUxProgression01
ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/
ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C
ProjectDocs/WanxiangGuitu/DeliveryUxProgression02
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03A
player_acceptance_driver.py
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03AImpl
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarness
```

## 产品与Schema独立复核 [S][P][C]

| 合同 | 源码（均在Assets/CombatPrototype） | 事实 |
| --- | --- | --- |
| 六字段 | AdventureState.cs:19-35 | 仅runId/objectiveId/regionId/completedAtUtc/committedAtUtc/displayNameSnapshot。SettlementId派生；Profile容器/unknown和plan镜像是批准结构，不是第七业务字段 |
| Pending双UTC | AdventureFlow.Objectives.cs:78；AdventureFlow.cs:185-195；AdventureRules.cs:13-25 | 成功撤离且LastObjective达成才采CompletedAtUtc；首次计划冻结CommittedAtUtc，为计划时间而非磁盘落盘时间；重试复用原计划 |
| Committed发布 | AdventureFlow.cs:196-233；CombatSaveSystem.cs:85-153,194 | 收益、committedRuns、历史同一候选，完整发布后独立回读；不确定进入SettlementNeedsRead，不另写历史或重发奖励 |
| 永久去重/容量 | AdventureRules.cs:13-30；AdventureValidation.cs:27-68 | committedRuns拒绝旧Run；129条在候选裁剪最旧提交项，仅历史受影响；同Run多目标由验证器拒绝 |
| v9迁移 | SaveSchemaMigration.cs；CombatSaveSystem.cs:306-327；GameEntry.cs:91-107 | 显式入口，v9/v10分根；归档主备/分页/事务；空历史且unknown，不Evaluator/Plan倒填、不自动Commit旧Pending |
| 锁/恢复 | SaveSchemaMigration.cs:20-44；CombatSaveSystem.Entry.cs:19-44 | FileShare.None单写者和父世代SHA校验，不凭PID/mtime解锁；新版读旧档不等于无损降级 |
| 双UI/显示 | AdventureFlow.UI.cs:47-105,119-220；ObjectiveCatalog.cs:88-103 | 共同QueryHistory，双UTC降序及稳定三元键；20条分页；DisplayNameSnapshot旧名称，稳定ID历史类型映射 |
| D-20/D-23 | AdventureFlow.cs:156；ObjectiveCatalog.cs与保护文件 | 每次出征Select(0)，无技能槽持久化和地区收益字段；DATA_GAP不补造；技能机制/B1/B2保护文件未改 |

Profile的objectiveHistory、objectiveHistoryLegacyUnknown和plan同型镜像为批准的支撑结构；每条历史严格六字段。未加持久化SettlementId、DefinitionVersion、CompletionType、技能槽索引、地区成长或D-24字段。CombatSaveData/CombatCheckpoint、UX-03机制、B1/B2保护文件无非授权diff。

### 原始业务证据重算

CAPACITY-A02：387条宝箱使用、129条撤离、129条默认槽恢复、129份Pending冻结。128条逐字段等于冻结序列第2至129项，committedRuns等于全部129个Run。最旧被裁剪Run=e1d4120981c9482899f63c1ce465abf6；主档SHA256=17B41C690B3A53A8FDC04342F9F78B457D3A0D22F9368C2FEAB64646B1488845。
UX05-R1-REPLAY-A01原结果与生产Plan入口证明旧Run重放被拒，前后SHA与容量档一致。PENDING-STOP/RESUME和R1-SAVE-READBACK/SAVE-STALE冻结六字段与Committed完全相等，Run仅一次，不确定发布时禁止重复确认。
容量链调用真实出征/宝箱Interact/撤离/提交，但含RestorePosition受控导航和timeScale=8；不宣称129次Windows原生行走。混合地区/时间/名称夹具仅用于查询，不用于制造真实完成证明。

| 故障 | 恢复Run | 归档条目 | 复算 |
| --- | --- | --- | --- |
| A3 | UX05-R1-A3-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| P3 | UX05-R1-P3-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| Q3 | UX05-R1-Q3-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| C3 | UX05-R1-C3-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| CHECKSUM | UX05-R1-CHECKSUM-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| REPLACE | UX05-R1-REPLACE-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| AFTER2 | UX05-R1-AFTER2-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |
| RECEIPT2 | UX05-R1-RECEIPT2-RECOVERY-A01 | 4 | v9/v10校验；原Pending/计划投影相等，历史空且unknown |

八例共32个归档条目，逐文件核对SHA/大小，含主档、bak、分页和关联事务。原v9ActiveRun及Settlement.plan旧字段投影一致，status仍Pending，不自动Commit或重抽奖励；不是只看迁移摘要PASS。

### 双UI原始输入与查询

| Run | 前台验证 | IMGUI消费 | uGUI消费 | 查询对 |
| --- | --- | --- | --- | --- |
| UX05-IMGUI-R2-MIXED-A06 | 43 | 20 | 20 | 15 |
| UX05-IMGUI-R2-EMPTY-A03 | 6 | 2 | 2 | 1 |
| UX05-IMGUI-R2-UNKNOWN-A03 | 6 | 2 | 2 | 1 |

合计55次前台验证、两UI各24次历程操作、17对查询。根据原Profile独立重算地区/类型、双UTC与稳定身份排序和20条分页，query/visible逐项相等；七页/末页成立。screen-0033.png显示旧名称“守誓”及Run2a10985d3681439e9ffe65d26f5dc04c。Agent看图不冒充[M]人工体验。
仅1280×720、DPI96被验证。UI修复仅处理非活动canvas重置historyOpen及底层穿透，两个展示共用QueryHistory。D-20与129次默认槽事件相符。D-23读取UX05-R1-RULES-A01四组原始Mono比较：三地区及forest:hunts-complete，各256个固定掉落输入，攻击/防御/背包/仓库/配方均True；这是受控内存投影，不用Python double冒充Mono，不补DATA_GAP。

## Run集合与原始分类

68+79=147；IMGUI-R2完整12条使历史集合159，最终3条只是子集，另9条中间尝试保留。收尾6条与159无交集，故全量165唯一Run。任务列举68+79+最终3+收尾6为156条，另9条中间尝试使完整审计为165，不重复统计。

| 分组 | 数量 | 原分类计数 |
| --- | --- | --- |
| original68 | 68 | {'PASS': 59, 'SUPPLEMENTAL_STOPPED': 1, 'FAIL_LAUNCH': 1, 'EXPECTED_NEGATIVE_BLOCKED': 1, 'FAIL': 2, 'PROCESS_CUT_WITNESSED': 2, 'OBSERVED_STARTUP_ONLY': 2} |
| r1new79 | 79 | {'PASS': 43, 'FAIL_TIMEOUT': 4, 'PROCESS_CUT_WITNESSED': 11, 'INCOMPLETE_EVIDENCE': 5, 'FAIL': 15, 'EXPECTED_NEGATIVE_BLOCKED': 1} |
| r2all12 | 12 | {'FAIL': 2, 'INTERACTION_OBSERVED_AUTOSAVE_ACTIVE': 1, 'PASS_INTERACTION_INCOMPLETE_EXIT': 3, 'PASS': 4, 'INCOMPLETE_INPUT_TOOL': 1, 'FAIL_DRIVER': 1} |
| closure6 | 6 | {'PASS': 4, 'INSTRUMENT_INTERRUPTED': 2} |

重新读取manifest及存在的raw result，解析历史Run目录1617个JSON、302个JSONL文件/3754行；再读收尾6条输入/入口/主档/退出回执。历史106条记录PASS和收尾4条PASS分开保留，不当最终构建通过率。7条旧记录无raw_result路径，原生退出缺项不倒填0；预期拒绝、进程切断、工具中断、缺证不重分类为PASS/FAIL。
114条沿用DRIVER_ARCHIVE_RECOVERY.csv，不再追溯；84条原分类PASS中有31条R1 PASS，Driver位级可复现性依然NO。其他24条源码SHA匹配现有归档；15条sidecar二进制不自动证明源码位级重编译；6条纯启动N/A。收尾3条有持久启动器SHA，其余3条早期内联会话无合成Driver SHA，保留NOT_RECORDED。

### 全部165条逐Run表

| 批次 | RunId | PID | ExitCode | 原Verdict | raw Verdict | BuildId | Product DLL SHA256 | Driver SHA256 | manifest / result | 源码状态 | 可复现性 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| original68 | UX05-20261119-ABANDON-A01 | 22104 | 0 | PASS | PASS | UX05-Acceptance-11-Mono | F9FD2AF5DE6085E1A9A89399A8CA3AD2B873E11E5A43FD59AFC52DB4F6E21347 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-ABANDON-A01/manifest.json / EVIDENCE/UX05-20261119-ABANDON-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-B1-B2-GATES-A01 | 25300 | 0 | PASS | PASS | UX05-v10-Mono-inventory-probe-01 | B9F53AFE26B0AAF44C023F316147E7A6D0E68116D7B030919EBB73FE0117E3AC | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-B1-B2-GATES-A01/manifest.json / EVIDENCE/UX05-20261119-B1-B2-GATES-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-B1-FIXTURE-MIGRATE-A01 | 30844 | 0 | PASS | PASS | UX05-v10-Mono-inventory-probe-01 | B9F53AFE26B0AAF44C023F316147E7A6D0E68116D7B030919EBB73FE0117E3AC | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-B1-FIXTURE-MIGRATE-A01/manifest.json / EVIDENCE/UX05-20261119-B1-FIXTURE-MIGRATE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-BACKUP-RESTORE-A04 | 32996 | 0 | PASS | PASS | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-BACKUP-RESTORE-A04/manifest.json / EVIDENCE/UX05-20261119-BACKUP-RESTORE-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-BAD-SHA-A01 | 7488 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-BAD-SHA-A01/manifest.json / EVIDENCE/UX05-20261119-BAD-SHA-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CAPACITY-A01 | 17896 | 0 | SUPPLEMENTAL_STOPPED | OBSERVED | UX05-Acceptance-08-Mono | E617F55C9B2842E6EEB26A300B8E0F33E37FCCBD858CE24971D345CF90B612E6 | 96FD9C73FE5884E2062D3A34A87980946337CBE9B18805AA0C798E0E8AA5F7E6 | EVIDENCE/UX05-20261119-CAPACITY-A01/manifest.json / EVIDENCE/UX05-20261119-CAPACITY-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CAPACITY-A02 | 31584 | 0 | PASS | PASS | UX05-Acceptance-09-Mono | 93B518191A5C050249B043B5938A0786959D85FF44F433346DD5C22DEC0A8910 | 96FD9C73FE5884E2062D3A34A87980946337CBE9B18805AA0C798E0E8AA5F7E6 | EVIDENCE/UX05-20261119-CAPACITY-A02/manifest.json / EVIDENCE/UX05-20261119-CAPACITY-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CAPACITY-REOPEN-A02 | 36592 | 0 | PASS | PASS | UX05-Acceptance-09-Mono | 93B518191A5C050249B043B5938A0786959D85FF44F433346DD5C22DEC0A8910 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-CAPACITY-REOPEN-A02/manifest.json / EVIDENCE/UX05-20261119-CAPACITY-REOPEN-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V10-A03 | 31844 | 0 | PASS | PASS | UX05-v10-Mono-cooked-shell-02 | FE2820E9CF368D8E2EA147A63DB017AB3049BE9F8975EE713B73B080C3FA0186 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A03/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V10-A04 | 15636 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A04/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V10-A05 | 33032 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A05/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V10-A05/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V9-A03 | 33552 | 0 | PASS | PASS | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A03/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V9-A04 | 7136 | 0 | PASS | PASS | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A04/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CLIENTPAIR-V9-A05 | 4440 | 0 | PASS | PASS | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A05/manifest.json / EVIDENCE/UX05-20261119-CLIENTPAIR-V9-A05/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-CONTRACT-A01 | 34516 | NOT_CAPTURED | FAIL_LAUNCH | NOT_RECORDED_SEE_RAW | UX05-HistoryContract-Mono | 645C393DCBFD2200D60B9F3030AE0AE2DF155AC1DA95879EE311E117164A8BC8 | 011DE93D0D4707123F012535E6C5D762295EA7F88B082044CE905B56B2CD6AB2 | EVIDENCE/UX05-20261119-CONTRACT-A01/manifest.json / NOT_RECORDED | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| original68 | UX05-20261119-CONTRACT-A02 | 24860 | NOT_CAPTURED | PASS | PASS | UX05-HistoryContract-Mono | 645C393DCBFD2200D60B9F3030AE0AE2DF155AC1DA95879EE311E117164A8BC8 | 011DE93D0D4707123F012535E6C5D762295EA7F88B082044CE905B56B2CD6AB2 | EVIDENCE/UX05-20261119-CONTRACT-A02/manifest.json / EVIDENCE/UX05-20261119-CONTRACT-A02/contract-result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| original68 | UX05-20261119-FUTURE-SOURCE-A01 | 14840 | 0 | PASS | PASS | UX05-Acceptance-04-Mono | 1250496B23B0C5FBF629D2604C676B36AE51EE9C5E479E8ED2EA7CE65D66C95C | 4365581A3BF49AF01AB9561F545EB82E2748E7E7E9965DA34DEE82D284AB3460 | EVIDENCE/UX05-20261119-FUTURE-SOURCE-A01/manifest.json / EVIDENCE/UX05-20261119-FUTURE-SOURCE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-LOCK-CONTENDER-A04 | 34992 | 1 | EXPECTED_NEGATIVE_BLOCKED | FAIL | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-LOCK-CONTENDER-A04/manifest.json / EVIDENCE/UX05-20261119-LOCK-CONTENDER-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-LOCK-HOLDER-A04 | 10732 | 0 | PASS | PASS | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-LOCK-HOLDER-A04/manifest.json / EVIDENCE/UX05-20261119-LOCK-HOLDER-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATE-A02 | 35864 | 1 | FAIL | FAIL | UX05-Acceptance-01-Mono | 3848CF7FB06E10823F70821D2B16774B0AF793C0E1652BEBB6F54DE2A4652049 | 717F483B89F440FDE16B52B49D4EB6129924C57BEA62E62EEE1FD5DE08F1DC5E | EVIDENCE/UX05-20261119-MIGRATE-A02/manifest.json / EVIDENCE/UX05-20261119-MIGRATE-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATE-A03 | 34076 | 0 | PASS | PASS | UX05-v10-Mono-cooked-shell-02 | FE2820E9CF368D8E2EA147A63DB017AB3049BE9F8975EE713B73B080C3FA0186 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-MIGRATE-A03/manifest.json / EVIDENCE/UX05-20261119-MIGRATE-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATE-A04 | 30596 | 0 | PASS | PASS | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 03244F09CC84B2E1B95AE83FBFD884E701D95F9DB28CBC54585581FD5BB11E14 | EVIDENCE/UX05-20261119-MIGRATE-A04/manifest.json / EVIDENCE/UX05-20261119-MIGRATE-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATE-PAGED-PENDING-A01 | 5972 | 0 | PASS | PASS | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 589B6668DFFAE42DB3B4D1266D681B822C8146CD7D752021117DD0F7EFA270FB | EVIDENCE/UX05-20261119-MIGRATE-PAGED-PENDING-A01/manifest.json / EVIDENCE/UX05-20261119-MIGRATE-PAGED-PENDING-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATE-PAIR-A05 | 22904 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-MIGRATE-PAIR-A05/manifest.json / EVIDENCE/UX05-20261119-MIGRATE-PAIR-A05/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATION-CUT-A02 | 31840 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-Acceptance-04-Mono | 1250496B23B0C5FBF629D2604C676B36AE51EE9C5E479E8ED2EA7CE65D66C95C | 4365581A3BF49AF01AB9561F545EB82E2748E7E7E9965DA34DEE82D284AB3460 | EVIDENCE/UX05-20261119-MIGRATION-CUT-A02/manifest.json / EVIDENCE/UX05-20261119-MIGRATION-CUT-A02/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATION-CUT-A03 | 3668 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-MIGRATION-CUT-A03/manifest.json / EVIDENCE/UX05-20261119-MIGRATION-CUT-A03/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATION-RECOVER-A02 | 36668 | 0 | PASS | PASS | UX05-Acceptance-04-Mono | 1250496B23B0C5FBF629D2604C676B36AE51EE9C5E479E8ED2EA7CE65D66C95C | 4365581A3BF49AF01AB9561F545EB82E2748E7E7E9965DA34DEE82D284AB3460 | EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A02/manifest.json / EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-MIGRATION-RECOVER-A03 | 15852 | 0 | PASS | PASS | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A03/manifest.json / EVIDENCE/UX05-20261119-MIGRATION-RECOVER-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-NO-DEFINE-BOOT-A01 | 29292 | 0 | PASS | PASS | UX05-NoDefine-07-Mono | 594943C3416187C4F16A354702D9D212F1CEEB2862FD5779B16E0B5436F4A90B | N/A | EVIDENCE/UX05-20261119-NO-DEFINE-BOOT-A01/manifest.json / EVIDENCE/UX05-20261119-NO-DEFINE-BOOT-A01/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| original68 | UX05-20261119-OBJECTIVE-COMMIT-A01 | 33860 | 0 | PASS | PASS | UX05-v10-Mono-objective-probe-01 | 4855D4A0D8282F23211052A2211B32B098478734580645ED28ECD1446CD99D90 | 1F9CDF541E61F28183FFD6885519892B7C93BD967C0CA51352C369129B0F41FF | EVIDENCE/UX05-20261119-OBJECTIVE-COMMIT-A01/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-COMMIT-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-NEW-A03 | 35516 | 0 | PASS | PASS | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A03/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-NEW-A04 | 5188 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A04/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-NEW-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-READBACK-A03 | 14900 | 0 | PASS | PASS | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A03/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-READBACK-A04 | 34276 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A04/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-READBACK-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-REOPEN-A01 | 34280 | 0 | PASS | PASS | UX05-v10-Mono-objective-probe-01 | 4855D4A0D8282F23211052A2211B32B098478734580645ED28ECD1446CD99D90 | 1F9CDF541E61F28183FFD6885519892B7C93BD967C0CA51352C369129B0F41FF | EVIDENCE/UX05-20261119-OBJECTIVE-REOPEN-A01/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-REOPEN-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-REPEAT-A01 | 32680 | 0 | PASS | PASS | UX05-v10-Mono-repeat-probe-01 | CC0A4D41F93533A06AF782B0C551A19219BDE5B1F12C5B8A8922E9644CD95282 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A01/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-REPEAT-A02 | 34532 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A02/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A01 | 380 | 0 | PASS | PASS | UX05-v10-Mono-repeat-probe-01 | CC0A4D41F93533A06AF782B0C551A19219BDE5B1F12C5B8A8922E9644CD95282 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A01/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A02 | 5048 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A02/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-REPEAT-REOPEN-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-UGUI-A01 | 33512 | 0 | PASS | PASS | UX05-v10-Mono-visual-probe-01 | D0DE139490B741C1B8CCD28432629FB7D50562BA56F924887C860B6B6BD1EC08 | 3786EDB0B72D16945F52CC036E2337F044F0D349B98847DC02665D36F0C70700 | EVIDENCE/UX05-20261119-OBJECTIVE-UGUI-A01/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-UGUI-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-UI-A03 | 25704 | 0 | PASS | PASS | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | A3EA8C92829821C448CB177B1E6805A21D162E3EDBFDD4EC2DF77020C496FB72 | EVIDENCE/UX05-20261119-OBJECTIVE-UI-A03/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-UI-A03/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-OBJECTIVE-UI-A04 | 22204 | 0 | PASS | PASS | UX05-Acceptance-07-Mono | BDEAD316BADC6E62358437C57A27390EF67CB92F26A27AAF2449D0AE6DF77C55 | 09B09147CC1AF2CCEB417776EC28468E3BB136A6AB2F7F5CA3ED2591A563765B | EVIDENCE/UX05-20261119-OBJECTIVE-UI-A04/manifest.json / EVIDENCE/UX05-20261119-OBJECTIVE-UI-A04/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-P1C-cavern-A01 | 36260 | 0 | PASS | PASS | UX05-Release-08-P1C-sidecar | 1B2E3C21CED9857ED524C62A29428CEFF2FC8B77766664646B5D6CBBE7E508C7 | 8A8D0EF57451DB778BC227A4110CC37EBF1B1055BF0E0AC58F3DEE4845C98D2E | EVIDENCE/UX05-20261119-P1C-cavern-A01/manifest.json / EVIDENCE/UX05-20261119-P1C-cavern-A01/review-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| original68 | UX05-20261119-P1C-forest-A01 | 6028 | 0 | PASS | PASS | UX05-Release-08-P1C-sidecar | 1B2E3C21CED9857ED524C62A29428CEFF2FC8B77766664646B5D6CBBE7E508C7 | 8A8D0EF57451DB778BC227A4110CC37EBF1B1055BF0E0AC58F3DEE4845C98D2E | EVIDENCE/UX05-20261119-P1C-forest-A01/manifest.json / EVIDENCE/UX05-20261119-P1C-forest-A01/review-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| original68 | UX05-20261119-P1C-ruins-A01 | 32512 | 0 | PASS | PASS | UX05-Release-08-P1C-sidecar | 1B2E3C21CED9857ED524C62A29428CEFF2FC8B77766664646B5D6CBBE7E508C7 | 8A8D0EF57451DB778BC227A4110CC37EBF1B1055BF0E0AC58F3DEE4845C98D2E | EVIDENCE/UX05-20261119-P1C-ruins-A01/manifest.json / EVIDENCE/UX05-20261119-P1C-ruins-A01/review-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| original68 | UX05-20261119-PAGED-RESTORE-A01 | 9480 | 0 | PASS | PASS | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | 3786EDB0B72D16945F52CC036E2337F044F0D349B98847DC02665D36F0C70700 | EVIDENCE/UX05-20261119-PAGED-RESTORE-A01/manifest.json / EVIDENCE/UX05-20261119-PAGED-RESTORE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-PAIR-V9-A01 | 16672 | 0 | OBSERVED_STARTUP_ONLY | OBSERVED | UX04-B2R2FIX-FINAL-A02-Mono | AB3D5BA4F4A234598056915AB7B1DCA4AD4BE57F68298FC24D1B718D267A2DF1 | BD4E72802CE929C1E3F93A510A6E3CD26BFAA5F912E44D2B9D87A51DA52B1C62 | EVIDENCE/UX05-20261119-PAIR-V9-A01/manifest.json / EVIDENCE/UX05-20261119-PAIR-V9-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-PENDING-RESUME-A01 | 35584 | 0 | PASS | PASS | UX05-Acceptance-11-Mono | F9FD2AF5DE6085E1A9A89399A8CA3AD2B873E11E5A43FD59AFC52DB4F6E21347 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-PENDING-RESUME-A01/manifest.json / EVIDENCE/UX05-20261119-PENDING-RESUME-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-PENDING-STOP-A01 | 31488 | 0 | PASS | PASS | UX05-Acceptance-11-Mono | F9FD2AF5DE6085E1A9A89399A8CA3AD2B873E11E5A43FD59AFC52DB4F6E21347 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-PENDING-STOP-A01/manifest.json / EVIDENCE/UX05-20261119-PENDING-STOP-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-RELEASE-BOOT-A01 | 17220 | 0 | PASS | PASS | UX05-Release-08 | 1B2E3C21CED9857ED524C62A29428CEFF2FC8B77766664646B5D6CBBE7E508C7 | N/A | EVIDENCE/UX05-20261119-RELEASE-BOOT-A01/manifest.json / EVIDENCE/UX05-20261119-RELEASE-BOOT-A01/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| original68 | UX05-20261119-REPLAY-A01 | 34168 | 0 | PASS | PASS | UX05-Release-08-Replay-sidecar | 1B2E3C21CED9857ED524C62A29428CEFF2FC8B77766664646B5D6CBBE7E508C7 | 2E400BC81C110F6280600509AA169A3FC27C58EB90DEFCF0BABA8B8121226867 | EVIDENCE/UX05-20261119-REPLAY-A01/manifest.json / EVIDENCE/UX05-20261119-REPLAY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-bow-burst-A02 | 23528 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-bow-burst-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-bow-burst-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-bow-burst-R1-A01 | 14568 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-bow-pierce-A02 | 35728 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-bow-pierce-R1-A01 | 33800 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-gs-cleave-A02 | 36856 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-gs-cleave-R1-A01 | 36336 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-gs-wave-A02 | 34796 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-gs-wave-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-gs-wave-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-gs-wave-R1-A01 | 36340 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sc-pull-A02 | 5248 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sc-pull-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-sc-pull-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-sc-pull-R1-A01 | 30672 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sc-reap-A02 | 29952 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sc-reap-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-sc-reap-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-sc-reap-R1-A01 | 27780 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-spear-charge-A02 | 34088 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-spear-charge-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-charge-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-spear-charge-R1-A01 | 7796 | -1 | FAIL_TIMEOUT | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-spear-charge-R1-A02 | 35720 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A05 | E053AC000F3EDBECA8CAB8C8BB5617FF91507AB8CB34262BB4D07133EA653013 | 38BBC1A3232BB4CC84D4AB30DF29A4E9E444AE01E5F500D3C06028B726211679 | EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/root/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| original68 | UX05-20261119-UX03-spear-sweep-A02 | 33072 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-spear-sweep-R1-A01 | 25264 | -1 | FAIL_TIMEOUT | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-spear-sweep-R1-A02 | 22440 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A05 | E053AC000F3EDBECA8CAB8C8BB5617FF91507AB8CB34262BB4D07133EA653013 | 38BBC1A3232BB4CC84D4AB30DF29A4E9E444AE01E5F500D3C06028B726211679 | EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/root/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| original68 | UX05-20261119-UX03-staff-echo-A02 | 26300 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-staff-echo-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-staff-echo-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-staff-echo-R1-A01 | 25744 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-staff-field-A02 | 22960 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-staff-field-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-staff-field-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-staff-field-R1-A01 | 18304 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sword-circle-A01 | 36588 | NOT_CAPTURED | OBSERVED_STARTUP_ONLY | NOT_RECORDED_SEE_RAW | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 0FC079710BB8CF456BED9C86C252FD4C5B4016EC8E9B3BB47BB96D48377906DF | EVIDENCE/UX05-20261119-UX03-sword-circle-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sword-circle-A02 | 30852 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sword-circle-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-sword-circle-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-sword-circle-R1-A01 | 15444 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sword-triple-A01 | 36516 | 1 | FAIL | NOT_RECORDED_SEE_RAW | UX05-Acceptance-02-Mono | 57556E961E581C4B2DD33F6B05C5B3003888CA066AF158653F7F47EBCBC85977 | 0FC079710BB8CF456BED9C86C252FD4C5B4016EC8E9B3BB47BB96D48377906DF | EVIDENCE/UX05-20261119-UX03-sword-triple-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-sword-triple-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-sword-triple-A02 | 13660 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sword-triple-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-sword-triple-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-sword-triple-R1-A01 | 15272 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-twin-counter-A02 | 33384 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-twin-counter-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-twin-counter-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-twin-counter-R1-A01 | 23840 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-UX03-twin-volley-A02 | 35940 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-Acceptance-05-Mono | 342D175E5696467B2C904E901C95B39FBA84EE5BA580B69AAA53DCE6EF7926F8 | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-twin-volley-A02/manifest.json / EVIDENCE/UX05-20261119-UX03-twin-volley-A02/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-20261119-UX03-twin-volley-R1-A01 | 10072 | 0 | PASS | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 8465ABAD8B8F61594F9E4FCE7F80AD6581DAF6EB2E97A2B03513B1EFC6C9B423 | EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/manifest.json / EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/root/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| original68 | UX05-20261119-V9-PAGED-PENDING-A01 | 15976 | 0 | PASS | PASS | B2-v9-pending-fixture-probe | D5F5C1004307735BA2787DD378374920FF807E57E23F5CD9128512B7ED834A21 | 589B6668DFFAE42DB3B4D1266D681B822C8146CD7D752021117DD0F7EFA270FB | EVIDENCE/UX05-20261119-V9-PAGED-PENDING-A01/manifest.json / EVIDENCE/UX05-20261119-V9-PAGED-PENDING-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-A3-A01 | 34920 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-A3-A01/manifest.json / EVIDENCE/UX05-R1-A3-A01/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-A3-RECOVERY-A01 | 36008 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-A3-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-A3-RECOVERY-A01/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-AFTER2-A01 | 21268 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-AFTER2-A01/manifest.json / EVIDENCE/UX05-R1-AFTER2-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-AFTER2-RECOVERY-A01 | 35688 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-AFTER2-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-AFTER2-RECOVERY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-ARCHIVE-A01 | 24072 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-ARCHIVE-A01/manifest.json / EVIDENCE/UX05-R1-ARCHIVE-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-ARCHIVE-RECOVERY-A01 | 35116 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-ARCHIVE-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-ARCHIVE-RECOVERY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-ARCHIVE2-A01 | 14832 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-ARCHIVE2-A01/manifest.json / EVIDENCE/UX05-R1-ARCHIVE2-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-ARCHIVE2-RECOVERY-A01 | 21616 | NOT_CAPTURED | INCOMPLETE_EVIDENCE | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-ARCHIVE2-RECOVERY-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-B1B2-A01 | 12568 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-B1B2-A01/manifest.json / EVIDENCE/UX05-R1-B1B2-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-B1B2-A02 | 24772 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-B1B2-A02/manifest.json / EVIDENCE/UX05-R1-B1B2-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-B1B2-FIXTURE-A02 | 7128 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-B1B2-FIXTURE-A02/manifest.json / EVIDENCE/UX05-R1-B1B2-FIXTURE-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-BOOT-nodefine-A01 | 34288 | 0 | PASS | PASS | UX05-R1-NoDefine-A01 | F95DC6B1758E8DAE4DBC04A68878338F3788460A8CEDCC65F15C5265CE0B34BD | N/A | EVIDENCE/UX05-R1-BOOT-nodefine-A01/manifest.json / EVIDENCE/UX05-R1-BOOT-nodefine-A01/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| r1new79 | UX05-R1-BOOT-NODEFINE-A03 | 15860 | 0 | PASS | PASS | UX05-R1-NoDefine-A03 | EFD66E556FB1038835744C5F8EC38B166DE6FFC849526E9EC3C43DB404D6949B | N/A | EVIDENCE/UX05-R1-BOOT-NODEFINE-A03/manifest.json / EVIDENCE/UX05-R1-BOOT-NODEFINE-A03/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| r1new79 | UX05-R1-BOOT-release-A01 | 36480 | 0 | PASS | PASS | UX05-R1-Release-A01 | 000F97C78B7FCC6F34869DF9D1D551B2A5BAF6B84D3A3ECDFC8EFCF8EF54E87C | N/A | EVIDENCE/UX05-R1-BOOT-release-A01/manifest.json / EVIDENCE/UX05-R1-BOOT-release-A01/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| r1new79 | UX05-R1-BOOT-RELEASE-A03 | 5680 | 0 | PASS | PASS | UX05-R1-Release-A03 | B67AC254F6CB7FCA96A2169340229157B22584184A65C5F1750FA8FD14DEB837 | N/A | EVIDENCE/UX05-R1-BOOT-RELEASE-A03/manifest.json / EVIDENCE/UX05-R1-BOOT-RELEASE-A03/review-result.json | N/A_NO_DRIVER | N/A_PURE_BOOT |
| r1new79 | UX05-R1-C3-A01 | 24160 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-C3-A01/manifest.json / EVIDENCE/UX05-R1-C3-A01/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-C3-RECOVERY-A01 | 33484 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-C3-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-C3-RECOVERY-A01/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-CANDIDATE-A01 | 5892 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-CANDIDATE-A01/manifest.json / EVIDENCE/UX05-R1-CANDIDATE-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-CANDIDATE-RECOVERY-A01 | 36448 | NOT_CAPTURED | INCOMPLETE_EVIDENCE | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-CANDIDATE-RECOVERY-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-CANDIDATE2-A01 | 26252 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-CANDIDATE2-A01/manifest.json / EVIDENCE/UX05-R1-CANDIDATE2-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-CHECKSUM-A01 | 36648 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | CA2CD0ECDEBA66014890FD27C3741BFD78A99C8D7608CEAA03DC2350A9A62B5C | EVIDENCE/UX05-R1-CHECKSUM-A01/manifest.json / EVIDENCE/UX05-R1-CHECKSUM-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-CHECKSUM-RECOVERY-A01 | 36104 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | CA2CD0ECDEBA66014890FD27C3741BFD78A99C8D7608CEAA03DC2350A9A62B5C | EVIDENCE/UX05-R1-CHECKSUM-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-CHECKSUM-RECOVERY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-CONFLICT-A01 | 2652 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-CONFLICT-A01/manifest.json / EVIDENCE/UX05-R1-CONFLICT-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-DUAL-BASE-A01 | 34316 | 0 | PASS | PASS | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-DUAL-BASE-A01/manifest.json / EVIDENCE/UX05-R1-DUAL-BASE-A01/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-DUAL-OBJECTIVE-A02 | 26496 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-DUAL-OBJECTIVE-A02/manifest.json / EVIDENCE/UX05-R1-DUAL-OBJECTIVE-A02/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-LEGACY-FUTURE-A01 | 33032 | 1 | FAIL | FAIL | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | BEC64B77C49B39593DC04EA77291F05D56BFB6F77C0806BF877C34548A726FBC | EVIDENCE/UX05-R1-LEGACY-FUTURE-A01/manifest.json / EVIDENCE/UX05-R1-LEGACY-FUTURE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-LEGACY-NAMESPACE-A01 | 14416 | 1 | FAIL | FAIL | B2-baseline-v9-Mono-cooked-shell-02 | 1600CB6CC7879768F864CDA22E9BA8100AA9C0C8802584265357686C46DB8751 | BEC64B77C49B39593DC04EA77291F05D56BFB6F77C0806BF877C34548A726FBC | EVIDENCE/UX05-R1-LEGACY-NAMESPACE-A01/manifest.json / EVIDENCE/UX05-R1-LEGACY-NAMESPACE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-LOCK-CONTENDER-A01 | 7128 | 1 | EXPECTED_NEGATIVE_BLOCKED | FAIL | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-LOCK-CONTENDER-A01/manifest.json / EVIDENCE/UX05-R1-LOCK-CONTENDER-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-LOCK-HOLDER-A01 | 33008 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-LOCK-HOLDER-A01/manifest.json / EVIDENCE/UX05-R1-LOCK-HOLDER-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-P3-A01 | 30672 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-P3-A01/manifest.json / EVIDENCE/UX05-R1-P3-A01/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-P3-RECOVERY-A01 | 35692 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-P3-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-P3-RECOVERY-A01/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-PAGE-A01 | 31420 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-PAGE-A01/manifest.json / EVIDENCE/UX05-R1-PAGE-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-PAGE-RECOVERY-A01 | 34240 | NOT_CAPTURED | INCOMPLETE_EVIDENCE | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | F401F572B230E3A7676F4DF23F360C38A0A41BFCC321C27427DC0FD52FA4503F | EVIDENCE/UX05-R1-PAGE-RECOVERY-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-PAGE2-A01 | 11232 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-PAGE2-A01/manifest.json / EVIDENCE/UX05-R1-PAGE2-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-PAGE2-RECOVERY-A01 | 32308 | NOT_CAPTURED | INCOMPLETE_EVIDENCE | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-PAGE2-RECOVERY-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-Q3-A01 | 22104 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-Q3-A01/manifest.json / EVIDENCE/UX05-R1-Q3-A01/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-Q3-RECOVERY-A01 | 15636 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-Q3-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-Q3-RECOVERY-A01/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-RECEIPT-A01 | 35416 | NOT_CAPTURED | INCOMPLETE_EVIDENCE | NOT_RECORDED_SEE_RAW | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | CA2CD0ECDEBA66014890FD27C3741BFD78A99C8D7608CEAA03DC2350A9A62B5C | EVIDENCE/UX05-R1-RECEIPT-A01/manifest.json / NOT_RECORDED | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-RECEIPT2-A01 | 27316 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-RECEIPT2-A01/manifest.json / EVIDENCE/UX05-R1-RECEIPT2-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-RECEIPT2-RECOVERY-A01 | 7128 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-RECEIPT2-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-RECEIPT2-RECOVERY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-REPLACE-A01 | 32456 | -1 | PROCESS_CUT_WITNESSED | OBSERVED | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | CA2CD0ECDEBA66014890FD27C3741BFD78A99C8D7608CEAA03DC2350A9A62B5C | EVIDENCE/UX05-R1-REPLACE-A01/manifest.json / EVIDENCE/UX05-R1-REPLACE-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-REPLACE-RECOVERY-A01 | 33676 | 0 | PASS | PASS | UX05-R1-Acceptance-A01 | FD64C831664A8B800A52365B0A8DAB5676057D52C6BCFD6E5FC8ABE04BFC98B2 | CA2CD0ECDEBA66014890FD27C3741BFD78A99C8D7608CEAA03DC2350A9A62B5C | EVIDENCE/UX05-R1-REPLACE-RECOVERY-A01/manifest.json / EVIDENCE/UX05-R1-REPLACE-RECOVERY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-REPLAY-A01 | 36268 | 0 | PASS | PASS | UX05-R1-Release-Replay-A01 | 000F97C78B7FCC6F34869DF9D1D551B2A5BAF6B84D3A3ECDFC8EFCF8EF54E87C | A357B615E0757F87EE4BC0A0F47940E6D57D5BE22554A602E4FF8FDCCA75BA25 | EVIDENCE/UX05-R1-REPLAY-A01/manifest.json / EVIDENCE/UX05-R1-REPLAY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-RULES-A01 | 35444 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-RULES-A01/manifest.json / EVIDENCE/UX05-R1-RULES-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-SAVE-READBACK-A01 | 31600 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | BEC64B77C49B39593DC04EA77291F05D56BFB6F77C0806BF877C34548A726FBC | EVIDENCE/UX05-R1-SAVE-READBACK-A01/manifest.json / EVIDENCE/UX05-R1-SAVE-READBACK-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-SAVE-STALE-A01 | 4784 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | BEC64B77C49B39593DC04EA77291F05D56BFB6F77C0806BF877C34548A726FBC | EVIDENCE/UX05-R1-SAVE-STALE-A01/manifest.json / EVIDENCE/UX05-R1-SAVE-STALE-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-EMPTY-A01 | 36248 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-EMPTY-A01/manifest.json / EVIDENCE/UX05-R1-UI-EMPTY-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-IMGUI-A01 | 32936 | -1 | FAIL_TIMEOUT | OBSERVED | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-IMGUI-A01/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-IMGUI-A02 | 36760 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-IMGUI-A02/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-IMGUI-A03 | 35020 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A04 | 82191EC188576C7940170DF9F3EA6226FC7F2BC982AAC2F17D894FF9B24D8185 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-A03/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-A03/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-A04 | 30012 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A05 | E053AC000F3EDBECA8CAB8C8BB5617FF91507AB8CB34262BB4D07133EA653013 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-A04/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-A04/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-A05 | 32108 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-A05/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-A05/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-EMPTY-A03 | 3136 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A04 | 82191EC188576C7940170DF9F3EA6226FC7F2BC982AAC2F17D894FF9B24D8185 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A03/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A03/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-EMPTY-A04 | 33980 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A05 | E053AC000F3EDBECA8CAB8C8BB5617FF91507AB8CB34262BB4D07133EA653013 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A04/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A04/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-EMPTY-A05 | 4212 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A05/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-EMPTY-A05/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-UNKNOWN-A03 | 34348 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A04 | 82191EC188576C7940170DF9F3EA6226FC7F2BC982AAC2F17D894FF9B24D8185 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A03/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A03/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-UNKNOWN-A04 | 13888 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A05 | E053AC000F3EDBECA8CAB8C8BB5617FF91507AB8CB34262BB4D07133EA653013 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A04/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A04/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-IMGUI-UNKNOWN-A05 | 19628 | 1 | FAIL | FAIL | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A05/manifest.json / EVIDENCE/UX05-R1-UI-IMGUI-UNKNOWN-A05/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-REPEAT-A01 | 25648 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-REPEAT-A01/manifest.json / EVIDENCE/UX05-R1-UI-REPEAT-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-UGUI-A01 | 33488 | -1 | FAIL_TIMEOUT | OBSERVED | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | BEC64B77C49B39593DC04EA77291F05D56BFB6F77C0806BF877C34548A726FBC | EVIDENCE/UX05-R1-UI-UGUI-A01/manifest.json / EVIDENCE/UX05-R1-UI-UGUI-A01/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-UGUI-A02 | 33216 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-UGUI-A02/manifest.json / EVIDENCE/UX05-R1-UI-UGUI-A02/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r1new79 | UX05-R1-UI-UGUI-A03 | 18512 | 0 | PASS | PASS | UX05-R1-Acceptance-A04 | 82191EC188576C7940170DF9F3EA6226FC7F2BC982AAC2F17D894FF9B24D8185 | 183CE302BA5B2263D7D0275C19D6DB466CE447A63481C975999A490048F5F082 | EVIDENCE/UX05-R1-UI-UGUI-A03/manifest.json / EVIDENCE/UX05-R1-UI-UGUI-A03/probe/result.json | YES_EXACT_SOURCE_HASH | SOURCE_IDENTIFIED_NOT_RERUN_THIS_AUDIT |
| r1new79 | UX05-R1-UI-UNKNOWN-A01 | 35376 | 0 | PASS | PASS | UX05-R1-Acceptance-A03 | 40F86E91111B69F79FDC7A7DFE371AFFA683498D03A4DEF31956D8C902C0EC0E | 7760A5ABB6A264BC05ED0B0E2251D611071B7594ACB5BDA9C9D4C521D91AECC6 | EVIDENCE/UX05-R1-UI-UNKNOWN-A01/manifest.json / EVIDENCE/UX05-R1-UI-UNKNOWN-A01/probe/result.json | NO_EXACT_SOURCE; OWNER_ACCEPTED_HISTORICAL_LIMITATION | NO_BITWISE_DRIVER_REPRODUCTION |
| r2all12 | UX05-IMGUI-R2-MIXED-A01 | 21536 | NOT_CAPTURED | FAIL | FAIL | UX05-R1-Acceptance-A06 | 7EA950EC852FA3BF2B73927A9BAFBD3DA7B64438EA02894E9754988CA0B16FB9 | 84313D5889E69B790BCF84327701DA76D7419FA53036D187E87B86400FED47AE | UX05-IMGUI-R2/EVIDENCE/MIXED-A01/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A01/result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-MIXED-A02 | 30500 | NOT_CAPTURED | FAIL | FAIL | UX05-R2-Acceptance-A01 | AFA0ADCA2BAF2AE4C8EB2E42BB2693081470D371BEB6EA3C8154E7A0A91F6976 | 47CEB8DE7EA501D5DF013EB20728FDCA7FBF681FD7298615F988A8CA10977340 | UX05-IMGUI-R2/EVIDENCE/MIXED-A02/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A02/diagnosis.jsonl | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-MIXED-A03 | 4884 | NOT_CAPTURED | INTERACTION_OBSERVED_AUTOSAVE_ACTIVE | INTERACTION_OBSERVED_AUTOSAVE_ACTIVE | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | 202E9A79B14D8FE2A2B05945022DDC317F94D49E8CBDB9A2594BD52AD28598A9 | UX05-IMGUI-R2/EVIDENCE/MIXED-A03/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A03/classification.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-MIXED-A04 | 31876 | NOT_CAPTURED | PASS_INTERACTION_INCOMPLETE_EXIT | PASS | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/MIXED-A04/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A04/result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-MIXED-A05 | 424 | 0 | PASS | PASS | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/MIXED-A05/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A05/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-MIXED-A06 | 28720 | 0 | PASS | PASS | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | 983A936C423F7140AC8BA34214DF12D427B7777FE4D72D1D2419F787AE4EC393 | UX05-IMGUI-R2/EVIDENCE/MIXED-A06/manifest.json / UX05-IMGUI-R2/EVIDENCE/MIXED-A06/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-EMPTY-A01 | 22924 | NOT_CAPTURED | PASS_INTERACTION_INCOMPLETE_EXIT | PASS_INTERACTION_INCOMPLETE_EXIT | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/EMPTY-A01/manifest.json / UX05-IMGUI-R2/EVIDENCE/EMPTY-A01/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-EMPTY-A02 | 5560 | -1 | INCOMPLETE_INPUT_TOOL | INCOMPLETE_INPUT_TOOL | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/EMPTY-A02/manifest.json / UX05-IMGUI-R2/EVIDENCE/EMPTY-A02/result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-EMPTY-A03 | 23248 | 0 | PASS | PASS | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | 983A936C423F7140AC8BA34214DF12D427B7777FE4D72D1D2419F787AE4EC393 | UX05-IMGUI-R2/EVIDENCE/EMPTY-A03/manifest.json / UX05-IMGUI-R2/EVIDENCE/EMPTY-A03/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-UNKNOWN-A01 | 30408 | NOT_CAPTURED | FAIL_DRIVER | FAIL_DRIVER | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A01/manifest.json / UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A01/diagnosis.jsonl | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-UNKNOWN-A02 | 12656 | NOT_CAPTURED | PASS_INTERACTION_INCOMPLETE_EXIT | PASS_INTERACTION_INCOMPLETE_EXIT | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | DF5883858D1A865FBB3452E95C335992D7C39890A51652BECC0A97BF3456EE52 | UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A02/manifest.json / UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A02/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| r2all12 | UX05-IMGUI-R2-UNKNOWN-A03 | 32476 | 0 | PASS | PASS | UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | 983A936C423F7140AC8BA34214DF12D427B7777FE4D72D1D2419F787AE4EC393 | UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A03/manifest.json / UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A03/verified-result.json | SIDECAR_BINARY_IDENTIFIED; SOURCE_VERSION_NOT_INFERRED_FROM_DLL | ARCHIVED_BINARY_ONLY_NOT_RECOMPILED |
| closure6 | UX05-R2-CLOSURE-NODEFINE-BOOT-A01 | 18808 | 0 | PASS | PASS | UX05-R2-NoDefine-A02 | E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78 | NOT_RECORDED_INLINE_NATIVE_SESSION | EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-BOOT-A01/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-BOOT-A01/result.json | INLINE_NATIVE_SESSION_INPUT_RECORDS; NO_COMBINED_DRIVER_SHA | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |
| closure6 | UX05-R2-CLOSURE-NODEFINE-RESTART-A01 | 29804 | NOT_RECORDED | INSTRUMENT_INTERRUPTED | INSTRUMENT_INTERRUPTED | UX05-R2-NoDefine-A02 | E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78 | NOT_RECORDED_INLINE_NATIVE_SESSION | EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A01/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A01/result.json | INLINE_NATIVE_SESSION_INPUT_RECORDS; NO_COMBINED_DRIVER_SHA | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |
| closure6 | UX05-R2-CLOSURE-NODEFINE-RESTART-A02 | 14992 | 0 | PASS | PASS | UX05-R2-NoDefine-A02 | E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78 | 6F767E8CECB503A6E392FFBAD83BBB5255220DC521A13B559D2912C854275011 | EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A02/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-NODEFINE-RESTART-A02/result.json | YES_LAUNCHER_EXACT_HASH | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |
| closure6 | UX05-R2-CLOSURE-RELEASE-BOOT-A01 | 1216 | NOT_RECORDED | INSTRUMENT_INTERRUPTED | INSTRUMENT_INTERRUPTED | UX05-R2-Release-A02 | 18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C | NOT_RECORDED_INLINE_NATIVE_SESSION | EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A01/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A01/result.json | INLINE_NATIVE_SESSION_INPUT_RECORDS; NO_COMBINED_DRIVER_SHA | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |
| closure6 | UX05-R2-CLOSURE-RELEASE-BOOT-A02 | 18956 | 0 | PASS | PASS | UX05-R2-Release-A02 | 18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C | 6F767E8CECB503A6E392FFBAD83BBB5255220DC521A13B559D2912C854275011 | EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A02/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-BOOT-A02/result.json | YES_LAUNCHER_EXACT_HASH | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |
| closure6 | UX05-R2-CLOSURE-RELEASE-RESTART-A02 | 31504 | 0 | PASS | PASS | UX05-R2-Release-A02 | 18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C | 6F767E8CECB503A6E392FFBAD83BBB5255220DC521A13B559D2912C854275011 | EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-RESTART-A02/run-manifest.json / EVIDENCE/R2/UX05-R2-CLOSURE-RELEASE-RESTART-A02/result.json | YES_LAUNCHER_EXACT_HASH | NATIVE_INPUT_RECORDS_PRESERVED_NOT_RERUN |

## 最终构建身份 [B][S][P]

| buildId | EXE SHA256 | DLL SHA256 | Unity build-guid | 验收标记 |
| --- | --- | --- | --- | --- |
| UX05-R2-Acceptance-A02 | B70442F90F50CD91F7AF7BF2272602645FC5D02C4D3156FB221FC27C328D2436 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | c485f267e5ad485e8f529e9e9901391f | UX_ACCEPTANCE,PlayerAcceptanceHarness,PlayerAcceptanceHarness03,HarnessRunner,Harness03Runner,ObjectiveHistoryEntryProbe,MigrationValidationHook,ObserveMigration,ObserveHistoryRepaint |
| UX05-R2-NoDefine-A02 | B70442F90F50CD91F7AF7BF2272602645FC5D02C4D3156FB221FC27C328D2436 | E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78 | ab9a568dafa24c12b5fc6ed6b3e8250a | NONE |
| UX05-R2-Release-A02 | 001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A | 18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C | 90a8eedf0f334167ae3c7d3f54827bf6 | NONE |

实际产物SHA、Managed清单、RuntimeInitializeOnLoads已核验。NoDefine/Release无UX_ACCEPTANCE、PlayerAcceptanceHarness/03、HarnessRunner/03Runner、Entry/ContractProbe、迁移/观察探针、sidecar或验收启动项；Acceptance保留自身验收身份。静态排除与运行分层，不相互替代。
NoDefine PID18808/14992与Release PID18956/31504均原生加载v10、显示128条历史、正常WM_CLOSE退出0，且各有新PID重读。PID29804/1216为仪器中断，无正常退出码。持久启动器SHA=6F767E8CECB503A6E392FFBAD83BBB5255220DC521A13B559D2912C854275011，仅用于原manifest记录该字段的3条。Acceptance多个Driver SHA按逐Run表保留，没有重建或混用。
日志保留D3D12 info-queue和可选URP后处理警告，不宣称所有后处理已验。周期/失焦/退出保存推进主档revision和SHA，历史/committedRuns/非camp Profile字段不变，未声称会话整档零变化。

## 历史保护与索引世代

| 索引 | 实测条目 | 初核差异 | 索引SHA256 |
| --- | --- | --- | --- |
| UX05-IMGUI-R2/EVIDENCE/history-before.json | 4142 | 0 | 13949AB0AB6C9C3C5439C8E0AEC8B00175B0899BD844D6E44B2211A243E11DB0 |
| EVIDENCE/INDEX.json | 5404 | 0 | 28D17AC774C4AE283B5B4898B649AC2CF6C7BFB2C329FE4AADCD1D6C729CBC5B |
| EVIDENCE/R2/INDEX.json | 378 | 0 | DB2F5F2984DFDB990B3EA441522B0A3CAF9A2C8515F8036CC490F53DA9DCC5F6 |

4142是history-before原保护项，不是当前目录总文件数；5404是原159条集合索引，收尾R2索引另有378项。覆盖有重叠，不能相加当唯一文件数。失败目录和分类保持原样。
R2索引风险文档条目在追加前整文件匹配。附记后产生新世代，旧版本为当前风险文件前4872字节，SHA256=F2DA0CFA181C1D04BF0C784662E5F761B531C74FA8CA26B5E0537C28D50E112A。旧INDEX字节不改，其余377项仍整文件匹配。新SHA表记录当前风险版本，不回写旧索引掩盖世代。
本轮无新增Player索引，逐路径SHA表是本轮候选索引，行数/唯一性/存在性/SHA自洽。旧INDEX是历史完整现场清单，不等于本轮提交选择，可能引用排除的锁/临候选或Builds；现场仍保留，不宣称提交包位级复现整个测试现场。
保护清单601项相对初实施仅11个既有授权差异；R2接手1504项仅AdventureFlow.UI.cs不同。本轮7328个开工指纹仅风险附记改变。ProjectSettings/Packages零变化。用户真实存档未访问；访问日志结论限隔离入口，不冒充OS级历史法证。

## 精确提交候选

[SUBMIT_WHITELIST.txt](SUBMIT_WHITELIST.txt)：5659条仓库相对路径，11 MODIFY、5648 ADD、0 DELETE，无通配符、父目录跳转或绝对条目。Index空，ADD不是已暂存。组成：产品11修改+1新增+必要meta1、实施交付5627、预检设计19。
[SUBMIT_WHITELIST_SHA256.tsv](SUBMIT_WHITELIST_SHA256.tsv)逐路径记录状态、增改、大小、原始SHA256、HEAD/Index OID、text/filter/eol、LFS载荷SHA及ignored/规范化风险。SHA256不是Git OID，载荷SHA不是Pointer OID；未运行LFS clean或创建Index对象。
- 本报告及两份白名单不自动入选，既有FINAL_AUDIT.md也排除；FINAL_RISK_REGISTER.md作为负责人正式裁决文档显式入选。
- 168锁文件、10临候选/暂存文件排除但不删除。原始正式Player/Build/编译/失败日志保留为证据，不当可清洗临时日志。
- Library、Builds、Temp、缓存、无关历史Evidence、根AGENTS.md和无关Resources.meta不入选。真实用户存档不入选。候选仅13个精确产品/meta路径和两处UX05正式交付范围。
- 条目全部相对路径；原证据内部测试时绝对路径为不可改写的诊断元数据，不是应提交的本机路径，也不承诺跨机器原路径可用。没有用户主页私有文件进入候选。
- core.autocrlf=true，1005个CRLF文本有规范化风险：产品/meta12、实施交付977（EVIDENCE951）、设计16；267个ignored正式日志及246个LFS载荷需复核。不能直接批量add后声称保留原字节。提交前须复审保字节方案，本轮不改属性或配置。
白名单SHA256=4E4D0A04642B3351353D708CD12B9172F5E8534FC5DBFC039E6F0FF4EE982A6B；SHA表文件SHA256=4E0F69A66FC467655DEB4DF39B4DE106FA938EF4F11297DB1DD1E7D912C2553E。不自索引，避免循环，审计报告不自动入选。

### 明确排除的UX05既有现场文件

| 路径 | 原因 |
| --- | --- |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/FINAL_AUDIT.md | PRIOR_AUDIT_REPORT_NOT_AUTO_INCLUDED |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/ABANDON-A01/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/ABANDON-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/BAD-SHA-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CAPACITY-A01/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CAPACITY-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CAPACITY-A02/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CAPACITY-A02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CUT-A02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/CUT-A03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/FUTURE-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/INVENTORY-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/isolated-client-pair-b02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/isolated-client-pair-retest-a04/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A01/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A01/WanxiangGuitu/ForestRuins-v10/save.json.candidate-3aab837c99444c92812cde580c75a8dd | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A03/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A03/WanxiangGuitu/ForestRuins-v10/.ux05-w-1f9ebc82b69744cf | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A04/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A04/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A04/WanxiangGuitu/ForestRuins-v10/.ux05-w-52c5fba433ef419b | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/OBJECTIVE-A04/WanxiangGuitu/ForestRuins-v10/.ux05-w-a0ce0731ab98475b | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-cavern/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-cavern/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-forest/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-forest/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-ruins/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/P1C-root-ruins/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAGED-RESTORE-A01/WanxiangGuitu/ForestRuins.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAGES-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAGES-A01/WanxiangGuitu/ForestRuins.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAIR03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAIR04/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PAIR05/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PENDING-A01/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/PENDING-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/A3/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/AFTER2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/ARCHIVE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/ARCHIVE2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/B1B2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/B1B2-02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/C3/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/CANDIDATE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/CANDIDATE2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/CHECKSUM/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/CONFLICT/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/CONFLICT/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/DUAL-CHECK/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/DUAL-SOURCE/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/DUAL-SOURCE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/FOCUS-IMGUI/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/FOCUS-IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/FOCUS-IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/FOCUS-IMGUI-UNKNOWN/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/IMGUI-UNKNOWN/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/LOCK/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/P3/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/PAGE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/PAGE2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/Q3/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/RECEIPT/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/RECEIPT2/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/REPLACE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/RULES/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/SAVE-READBACK/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/SAVE-READBACK/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/SAVE-STALE/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/SAVE-STALE/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/SAVE-STALE/WanxiangGuitu/ForestRuins-v10/.ux05-w-c4942614a9314ace | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-EMPTY/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-EMPTY/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-IMGUI/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-IMGUI-02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-IMGUI-MIXED/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-REPEAT/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-REPEAT/WanxiangGuitu/ForestRuins-v10/.ux05-w-1f9ebc82b69744cf | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-REPEAT/WanxiangGuitu/ForestRuins-v10/.ux05-w-71299bb463a64eab | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-UGUI/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-UGUI-02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-UGUI-MIXED/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/UI-UNKNOWN/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/WIN-IMGUI/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/WIN-IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/WIN-IMGUI-EMPTY/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R1/WIN-IMGUI-UNKNOWN/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/nodefine-storage/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/R2/release-storage/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/REPEAT-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/REPEAT-A01/WanxiangGuitu/ForestRuins-v10/.ux05-w-1f9ebc82b69744cf | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/REPEAT-A01/WanxiangGuitu/ForestRuins-v10/.ux05-w-d21099c76b0d42a6 | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-NO-DEFINE-BOOT-A01/isolated-root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-RELEASE-BOOT-A01/isolated-root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-burst-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-bow-pierce-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-cleave-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-gs-wave-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-pull-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sc-reap-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-charge-R1-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-spear-sweep-R1-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-echo-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-staff-field-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-circle-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-sword-triple-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-counter-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-A02/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-A02/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/root/WanxiangGuitu/ForestRuins-v10.entry.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-20261119-UX03-twin-volley-R1-A01/root/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-nodefine-A01/isolation/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-NODEFINE-A03/isolation/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-release-A01/isolation/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/UX05-R1-BOOT-RELEASE-A03/isolation/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/VIEW-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/EVIDENCE/VIEW-A01/WanxiangGuitu/ForestRuins-v10/save.json.candidate-3aab837c99444c92812cde580c75a8dd | TRANSIENT_CANDIDATE_OR_STAGE |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/EMPTY-A03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A04/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A05/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/MIXED-A06/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A01/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A02/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |
| ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE/UNKNOWN-A03/WanxiangGuitu/ForestRuins-v10.v10.lock | TRANSIENT_LOCK |

## 完成边界

执行只读git rev-parse/status/diff/merge-base/ls-files/check-attr、GitHub GET、Python csv/json/hashlib及确定性排序复算。未执行会重写旧result/INDEX的工具。没有构建、Player或新Run。
完成Git/源码/Schema/165条Run/三构建/4142保护复核、F-02接受登记及5659候选SHA核验。人工体验、其他显示环境和提交后Index/LFS复核未执行，不冒充通过。
已停止。下一步仅请负责人复审5659条候选及FD-01字节/ignored/LFS门禁；没有提交、推送、合并授权，不启动UX-06。
