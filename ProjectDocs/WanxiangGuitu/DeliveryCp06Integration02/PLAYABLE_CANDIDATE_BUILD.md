# CP06-INTEGRATION-02 · 统一候选纯发行构建身份（INT02-01）

> 本文档声明候选 `2964ad7413d2644f23c12a8c82e1d439e2884a01` 的**独立纯发行构建身份**。
> 本批次不改任何产品源码：`git status` 在交付前仅显示本交付目录为新增未跟踪文件，
> 所有已跟踪文件（产品代码 / ProjectSettings / 场景 / v9 / 用户文件）零改动。

## 1. 候选与分支

| 项 | 值 |
|---|---|
| 候选分支 | `integration/cp06-playable-candidate` |
| 候选 tip（完整 SHA） | `2964ad7413d2644f23c12a8c82e1d439e2884a01` |
| 验证分支 | `verify/cp06-integration-player-01`（从候选 tip 建立，仅新增本交付目录文档与证据） |
| 工作树 | `I:/WGInt02Build`（候选检出副本，用于读取产品源码定位真实业务入口；源码零改动） |

## 2. 构建身份（确定性）

| 项 | 值 |
|---|---|
| Unity 版本 | `6000.6.5f1` |
| 构建 Profile | `Assets/BuildProfiles/WindowsRelease.asset` |
| Profile SHA256 | `235d3703e301574ed8ba8326829d8019410700f9c14e4ddf37ac361e1d975876` |
| UnityConnect SHA256 | `7f2112b8c6ea0885dcc72b312c9726ffcd909f2e89d1eead61889274a4e5d1c0` |
| **可执行文件 SHA256** | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| Assembly-CSharp.dll SHA256 | `4ce1624c77141e2da6878c29082b8e62e7ac26a5cce3b03518a201992fb4a4e3` |
| 身份 sidecar | `WanxiangGuitu.exe.release.json`（构建时间 `2026-11-09T10:59:59Z`） |

确定性核对：可执行文件 SHA256 与历史 C22 / C24B **纯构建**记录一致——同一候选源码 +
同一 Profile + 同一 Unity 版本产出字节级一致的发行二进制。

## 3. 发行 Profile 合同（`WindowsRelease.asset`）

- `m_Development: 0`、`m_EnableProfiler: 0`、`m_EnableDebugBuild: 0`（纯发行，无开发标记）
- 场景序列：`Boot` → `Title` → `ForestRuins`（真实产品启动链，非测试场景直载）
- 构建入口：`WanxiangBuild.ValidateBuild()`，读取环境变量 `UNITY_TEST_ROOT` 作为输出根，
  写出 `<UNITY_TEST_ROOT>/Release/WanxiangGuitu.exe`

## 4. 隐私门禁（ReleaseDiagnosticsGuard）

`OnPostprocessBuild` 全部通过：

| 检查 | 结果 |
|---|---|
| Bee 输入唯一匹配（`Library/Bee/Player*-inputdata.json` 含输出 exe 绝对路径，且仅 1 个匹配） | PASS（`UNITY_TEST_ROOT=I:/WGInt02Release` 位于项目工作树外，Bee 存绝对路径） |
| Unity 版本一致 | PASS |
| Profile 身份 | PASS |
| 全部遥测 / 诊断开关禁用 | PASS |
| `.release.json` 身份文件写出 | PASS |

历史修复记录：输出根位于项目工作树内时 Bee 会把 `DestinationPath` 规范化为相对路径导致
守卫绝对路径匹配失败；全局与项目 Bee 缓存损坏会导致 pdb 复制失败。两项均已通过「项目外
输出根 + 清理 Bee 缓存」解决，重建产物确定性一致。

## 5. 纯构建零验证注入

| 清单 | 纯构建观测副本注入前 | 注入后（仅观察副本） |
|---|---|---|
| `RuntimeInitializeOnLoads.json` 中 `CavernValidation` 项 | 0 | 1 |
| `ScriptingAssemblies.json` 中 `CavernValidationDriver` 项 | 0 | 1 |
| `Managed/CavernValidationDriver.dll` | 不存在 | 存在（仅观察副本） |

验证驱动 **只注入观察副本**（`I:/WGInt02Obs/Release`），纯构建产物
（`I:/WGInt02Release/Release`）与候选工作树永不包含任何验证代码。
注入记录与前后哈希见 [Evidence/Tools-records/driver-injection.json](Evidence/Tools-records/driver-injection.json)。

## 6. 与真实 Player 的边界

- 每个验证 run 使用**独立隔离 run-root**（`I:/WGInt02Runs/<run>`）+ `-wanxiang-storage-root`
  指向该 root；真实用户存档目录（AppData）从未被读写（见 [REPORT.md](REPORT.md) §失败路径与用户文件保护）。
- 启动方式为直启 exe（`-logFile` / 窗口参数 / D3D12），不加载编辑器、不加载场景、不用
  teleport 伪造循环；英雄位置修正仅用于**摆位**（相邻矿脉/敌人/出口），一切进出、战斗、采集、
  撤离、结算、制造均走真实业务 API（`Flow.Depart` / `Combat.Strike` / `InteractionResolver.Execute` /
  `Flow.BeginExtraction` / `Flow.CommitSettlement` / `Loadout.Craft` 等）。
