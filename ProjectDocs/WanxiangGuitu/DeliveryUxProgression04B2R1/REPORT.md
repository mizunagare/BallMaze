# UX-04-B2-R1 修复与验收报告

## 结论：七项关闭，暂停等待负责人复审

最终 **A03：9/9真实Player Run、99/99检查PASS**；独立float32/证据复算 **23191 PASS、0 FAIL、20 INFO**。这不是提交授权。本轮不暂存、不提交、不推送、不合并main、不启动UX-05。

基线 `95caf234256613d4a6e4f89a8ab0dc09c397c6b2`；分支 `feature/ux-progression-04-b2`，均未改变。接手时已有部分R1代码、meta和工具，先完整保存再核查、补充，未覆盖已有产品修改。详见 [工作区快照](<WORKSPACE_SNAPSHOT.md>)。

## 七项关闭依据

| 条件 | 处理与最终证据 | 结论 |
|---|---|---|
| C-01 | 全局ID收藏；批次仅检查本容器before→after。SortBag严格InBag；移动不清收藏，成功分解后清理，失败保留。存活ID联合含待领取装备，避免误删。A03 collection反向跨容器整理均通过。 | CLOSED |
| C-02 | 两UI使用同一个filter→sort纯投影；4顺序实际目录、uGUI Text行序、真实按钮循环与滚轮到22/22；真实切UI比较相同ID序列，不手填Publish。底层顺序/装备状态不改。 | CLOSED |
| C-03 | 原两次B2Controls同一业务控件被重复绘制：顶部一次遮标题，底部一次为正常操作条。保留y+338一处，热键/原控件逻辑不变。Windows原生鼠标点击旧位置无效、保留条切到AttackDesc，截图确认标题无遮挡。 | CLOSED |
| C-04 | 现有三个新增CS的meta完整保留，格式与已有脚本相同；三个GUID合法且各唯一，与10442个其它扫描GUID不碰撞；已有GUID未改变。 | CLOSED |
| C-05 | 正常出征至真实ActiveRun后RestoreProgress设置rank0/3，实际链为25+8+0=33、25+8+15=48；预览主武器157/172。角色页、默认HUD、显式既有IMGUI HUD分别留图，人工确认33/48。 | CLOSED |
| C-06 | 8种角色分别九项canonical+指纹前后相同（72项比较），离线UTF16 FNV复算；随后真实EventSystem选中并设为主武器成功。 | CLOSED |
| C-07 | 收藏→入库→取回仍收藏→取消→整理→再收藏拒绝分解→取消后确认分解（铁矿+1、ID消失）→同角色同装备新PID重启清收藏；每步before/action/after归档。 | CLOSED |

详细 [验收](<ACCEPTANCE.md>)、[全部27次Run矩阵](<PLAYER_RUN_MATRIX.csv>)、[证据索引](<EVIDENCE/INDEX.json>)。

## 构建与可追溯身份

- buildId：`ux04b2r1-6f876c60-b70442f9-5a2654de`。
- Assembly-CSharp.dll SHA256：`6f876c6090ce57e498359bf93fb812583f848d3064612c10940f24f83c389db7`。
- EXE SHA256：`b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436`。
- Driver SHA256：`5a2654dead65d59485ad4810dc44a8746609a8546e7c93c068fa8867e55da384`。
- [产品构建凭据](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/_build/receipt/b2-product-build.json>)、[最终driver凭据](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/_build/driver-A03/receipt/r1-driver-injection-A03.json>)；执行driver源与交付源SHA一致；产品构建后166份源文件无漂移。
- 为遵守保护约束，使用Unity Bee/Roslyn重编产品C#至全新Acceptance Player副本，**不是资产重导入的完整Unity BuildPipeline构建**。产品DLL未注入测试逻辑；sidecar只用于隔离副本。
- 各Run独立目录、统一runId、PID/exitCode、result、原始输入/状态、归档文件hash都在各自manifest；不把编译凭据当作Player通过。

## 失败保留与证据纠错

A01 8/9通过，IMGUI因前台窗口不可用未发送原生鼠标而FAIL，原始结果不改。修复driver聚焦后A02 9/9自动通过；人工发现营地AtCamp门禁使fallback图没有攻击数字，因此没有据此关闭C-05。A03真实出征补齐自然绘制HUD后才关闭。所有A01/A02结果、二进制、旧复算失败和人工不足记录原样保留。原B2 6/6及历史FAIL逐字节保持，未覆盖。

[人工A02不足记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A02-review.json>)、[人工A03通过记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A03-review.json>)、[最终复算](<EVIDENCE/recompute-A03/summary.json>)。

## 保护与非目标边界

[保护清单](<PROTECTION_SHA256.tsv>)覆盖11609项修改前文件，无丢失、无未授权变更。相对本次完整快照仅三个授权产品源与两个R1工具发生变化；整个B2相对HEAD仍为原五个tracked修改及三新增CS/meta，未重建/丢弃B1和UX-03。

v9/v10/v11 Schema、D-24、品质/返还/成本/概率/随机流/尺寸/Boss/P1/P1C、ProjectSettings、Packages、场景/Prefab和UX-03均无本轮修改；测试仅消费隔离世界的正常随机状态，不修改随机算法或正式存档。

默认uGUI HUD本无攻击数值字段，本轮不新增；数值HUD验证明确来自产品既有IMGUI fallback。既有容器替换预览数值/容量可行性风险未扩大修复，C-06只关闭只读及实际可用性，详见 [风险登记](<RISK_REGISTER.md>)。

**停止状态：修复、相关构建、真实Player、独立复算、保护检查与双UI一致性检查完成。暂停，等待负责人复审。**
