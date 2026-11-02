# CP04-BR 独立验收收尾

本批完成工具、调查、协议和独立运行；**整体仍 BLOCKED，不宣称产品最终验收通过**。未修改产品，不合并 main。

产品基准 `72db192a527bd256e2ba18cd7ab334d8334051da`；冻结修复与分支起点 `cc9b73679458b0b868d875890a16b4c5238fb878`。交付分支 `verify/cp04-staff-acceptance-br`，本文件所属最终提交即固定审查版本（完整 SHA 由提交后回执提供，避免自引用）。Unity 6000.6.5f1，URP/Core 17.6.0、Input System 1.20.0、uGUI 2.6.0，未升级。

| 分项 | 状态 | 实际结论 |
|---|---|---|
| 构建输入等同性 | UNRESOLVED | 已逐字段及阶段定位；UnityConnect 原生启用原因与完整行为等同性未证明 |
| GC Alloc 完整测量 | NOT_RUN | Editor 基线/修复逐 Solve 有效；非开发 Player 字节接口校准失败，不填零 |
| CPU 测量 | PASS（有限范围） | Editor 配对和修复版 Player 实测；基线 Player 配对及准确查询数量未完成，无性能预算通过结论 |
| Editor 功能 | PASS | 本轮 293 PASS，exit 0，无超时 |
| 非开发验收 Player 功能 | PASS | 本轮 293 PASS，exit 0，无超时；受控 API，不是原生输入 |
| 原生输入 | NOT_RUN | 已准备脚本与空白表，等待真实操作者 |
| 人工体验 | NOT_RUN | 已准备独立记录表，不能预填 |

七个分项：3 PASS（含范围限制）、3 NOT_RUN、1 UNRESOLVED。功能断言合计 586 PASS/0 FAIL；不包含工具失败，也不删除其历史。Editor 两组各 152 个采样作用域，不等同 304 项产品功能断言。

## 关键结果

冷打开、导入、编译五文件字节不变。BuildPipeline 内 URP 预筛选、运行时设置序列化、Input System 预加载和默认字段写回。连接开关从 false 变 true，并实际进入 Bee Services 配置；不能说“只是文本差异”。两次纯发行构建均成功、0 错误/96 警告；Shader 回调各 1050 次、变体观察值之和 2016，不是去重后最终 shader 数。纯发行程序集无 BRPlayer/BRProbe/CP03Cases、无 UnityEditor 引用。[构建审计](BUILD_INPUT_AUDIT.md)

Editor 原始 GC.Alloc 元数据通过正/零/释放引用校准。1.5m 夹具的中位数基线 2516 B、修复 4460 B；它不是零分配，也不是 Player 数据。非开发 Player GC.Alloc recorder 不可用且线程 API 正校准返回 0，明确拒绝其字节结论。[性能](PERFORMANCE.md)

固定修复版 Player 实际产生 13 次 Spawn、3590 次 Flight、一次接触解析和 33 点真实伤害，最大并发 5；完整功能组另有 293 条断言。基线 Player 有缺失脚本警告且没有性能回执，保留中断，未据此归因产品。[失败历史](FAILURE_HISTORY.md)

## 保护

2329 项产品/用户文件和 889 项旧 CP04-B 文档/证据全部哈希一致。CombatAim 与 cc9 冻结字节一致，SHA256 `9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a`。用户场景、ProjectSettings、恢复目录均保留。仅隔离副本由 Unity 自动写回五文件，无手工恢复值制造一致性。主分支与历史修复/调查分支未改变。[保护证据](Evidence/Raw/protection-after.json)

历史 D3D12 UNKNOWN、Editor 青色帧等未关闭；历史 w2-s0-near / w2-s1-near 原始失败未改写。本批新功能断言不追溯修改旧 UNRESOLVED。下一步需要原生试玩环境、Player 逐调用可靠字节事件，以及 UnityConnect 原生构建行为的新因果证据。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md) · [原生协议](NATIVE_INPUT.md) · [人工表](HUMAN_PLAYTEST.md)
