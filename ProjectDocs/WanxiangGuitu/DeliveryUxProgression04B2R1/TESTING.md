# R1 测试与复跑

## 环境与边界

- Windows真实Standalone Player，1280×720窗口，D3D12；逐个启动，避免原生鼠标争抢前台。
- 产品：Unity 6000.6.5f1 Bee响应文件 + 对应Roslyn完整重编产品程序集，复用Acceptance Player壳的**全新隔离副本**。不是Unity资产重导入/BuildPipeline全量重构建。场景/Prefab/ProjectSettings/Packages不写。
- driver：独立sidecar程序集，只注入隔离副本；不进入Assets、不修改产品Schema。
- 每个Run同时使用 `-wanxiang-storage-root` 与 `UNITY_TEST_ROOT`；run-root/evidence拒绝复用。重启仅把成功collection的隔离存档复制到另一新root，绝不打开用户默认存档。

## 构建与运行命令

以下示例在仓库根运行，`NEW`必须替换为从未使用过的ID。Python可使用本机已提供的bundled Python。

```powershell
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/Tools/build_b2_product.py --project I:/unity/WanxiangGuitu --source-build Builds/WanxiangGuitu.Acceptance --copy Builds/ux04b2r1/NEW/player --work Evidence/Runs04B2R1/NEW/_build --evidence Evidence/Runs04B2R1/NEW/_build/receipt
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/build_driver_r1.py --managed Builds/ux04b2r1/NEW/player/WanxiangGuitu_Data/Managed --data Builds/ux04b2r1/NEW/player/WanxiangGuitu_Data --source ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/IntDriverR1.cs --work Evidence/Runs04B2R1/NEW/_build/driver --evidence Evidence/Runs04B2R1/NEW/_build/driver/receipt
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/audit_r1_workspace.py --baseline I:/unity/WanxiangGuitu-UX04B2R1-snapshot-20261116-1108/PRECHANGE_SHA256.json --output Evidence/Runs04B2R1/NEW/prebuild-audit
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/run_suite_r1.py --session Evidence/Runs04B2R1/NEW --player Builds/ux04b2r1/NEW/player --attempt A01
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/recompute_r1.py --session Evidence/Runs04B2R1/NEW/A01 --output ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-NEW
```

## 真实输入与证据

- IMGUI：Win32自身窗口PID/前台校验、必要原生线程输入附接聚焦、SetCursorPos/mouse_event发送，原始down/up与坐标落盘，控件状态变化和截图验证接收。绝不以InputSystem代替IMGUI。
- uGUI：QueueStateEvent → 正常EventSystem/InputSystemUIInputModule；记录模块、raycast首命中、目标、down/up。不直接Invoke按钮回调。开页、工厂样本、RestoreProgress、API门禁测试明确分别标注。
- 每Run记录buildId、产品DLL/EXE/driver SHA256、统一runId、PID、exitCode、result、原始输入、状态变化、raw装备/容器及canonical指纹，run-manifest含全部归档文件SHA256/bytes。
- 独立复算：标准库float32逐步舍入、原始资产冻结数值、D-24活动装备、Strength×5、Main预览、排序序列、UTF16 FNV九状态、运行身份及归档哈希。不会运行产品计算函数。
- 独立复算限制：当前资产输入另有构建源指纹对照，但不能把当前资产天然等同于任意历史二进制；legacyTier/LegacyProtected/legacy来源装备不使用新装备冻结值预言机。Inventory canonical因缺完整原始Inventory字段，只独立重算所提供UTF16明文的指纹，不能宣称其全部文本已独立重建。其它九项前后相等仍由逐项原始指纹与canonical证明。
- 人工截图审查与自动PASS独立：A02虽9/9自动PASS，营地门禁使其fallback截图无数值HUD，另存人工不足记录，不能用自动PASS覆盖；须以真实出征场景补证。

历史结果和所有尝试均见 [全部Run矩阵](<PLAYER_RUN_MATRIX.csv>)、[证据索引](<EVIDENCE/INDEX.json>)；原B2 6/6不覆盖。
