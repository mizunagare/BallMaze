# PERF-01 复审结论与 PERF-02 Codex 任务书

## A. PERF-01 复审结论

仓库：`mizunagare/BallMaze`  
开始基线：`6f2abca5f89fc80fc5d298623eda12f557654b78`  
最终提交：`94dcc009ff971272fc46d8c5b323cbb3251619b5`

复审时远端 `main` 完整 SHA 与最终提交一致。

**结论：PERF-01 的测量与警告审计交付在其声明范围内有条件接受；不代表性能达标、瓶颈已经定位或 91 条警告已经修复。**

确认的成果：
- 24 个有效测量窗口覆盖 8 类场景、每类 3 次；另有 3 次 Title 采样开/关对照。首轮失败、补跑、校准与未执行项均独立保留。
- CPU 主/渲染帧时间、帧间隔、GPU 有效子集、GC 集合、托管/Unity/系统进程内存、加载边沿分别统计，没有用 CPU 补填 GPU 缺失，也没有把不可用 GC 分配指标解释为零。
- 91 条警告逐条保留原文、源位置、源码/报告哈希、调用路径、风险与处置建议；中风险 18、低风险 37、信息 36，全部仍为 OPEN。
- 测试产物、工具、运行配置、用户覆盖层哈希和保护记录有归档；没有修改产品玩法、依赖或 v9 合同。
- 首轮失败、失败工具版本与原始样本保留，没有用补跑覆盖历史。

限制：
- 我核对了固定 SHA 的报告、统计、警告清单与源保护记录；没有在 Windows 上重新执行 Unity Player 或重新计算全部归档数据。因此运行窗口和警告分类仍属于交付方本轮证据，不冒称审核方独立重跑。
- GPU 有效计时存在缺失；每帧 GC Alloc 和采样器自分配字节不可用；进程专用/共享 GPU 内存没有有效实例；纯区域生成耗时没有独立 marker。
- 采样来自 1280×720、D3D11、临时带观测的非开发验收 Player，输入含用户场景/设置覆盖层。这不是无观测正式发行包的完整性能证明，也不是纯 Git main 场景的无条件复现。
- 尚无用户确认的目标硬件/分辨率/画质性能预算，故 CPU P95 等数字只是描述性基线，不能解释为达标。
- 91 条警告只是审计完毕，全部仍 OPEN；不自动修改是正确的。
- 原生 U16、独立人工试玩、完整性能预算验收仍 `NOT_RUN`；D3D12 UNKNOWN、Editor 青色帧、Editor Search、JobTempAlloc 根因仍 `UNRESOLVED`。

证据：
- [报告](https://github.com/mizunagare/BallMaze/blob/94dcc009ff971272fc46d8c5b323cbb3251619b5/ProjectDocs/WanxiangGuitu/DeliveryPerf01/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/94dcc009ff971272fc46d8c5b323cbb3251619b5/ProjectDocs/WanxiangGuitu/DeliveryPerf01/ACCEPTANCE.md)
- [复跑说明](https://github.com/mizunagare/BallMaze/blob/94dcc009ff971272fc46d8c5b323cbb3251619b5/ProjectDocs/WanxiangGuitu/DeliveryPerf01/TESTING.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/94dcc009ff971272fc46d8c5b323cbb3251619b5/ProjectDocs/WanxiangGuitu/DeliveryPerf01/Evidence/INDEX.md)

---

## B. 下一批 PERF-02：测量能力缺口与观测开销验证

### B1. 基线与边界

开始基线：`94dcc009ff971272fc46d8c5b323cbb3251619b5`。

先核对远端 `main` 完整 SHA；若已前进，停止并报告，不重置或覆盖工作区。本批不优化产品、不改玩法、不迁移警告。目标是验证当前 Unity 6000.6.5f1、Mono、D3D11 的非开发 Player 能否可靠取得 GC 分配、GPU 时间与进程显存指标，并量化观测工具的影响。

不升级依赖、不新增 CI、不改产品 Assets、场景、ProjectSettings、v9 合同或玩法数值。使用工程外短路径、全新 Library 和合成存档；保护用户场景、设置、真实存档与未提交修改。

### B2. GC 分配测量验证

仅在隔离验收 Player 中：
1. 枚举并记录实际可用的 ProfilerRecorder 名称、单位、有效性、采样时机与版本支持。
2. 对 GC Alloc / GC Allocated In Frame 等实际存在的 recorder 分别验证。
3. 通过受控已知分配探针测试零分配、已知大小分配、不同调用线程与帧边界，区分“确实为零”“Recorder 不可用”“采样时序不覆盖”。
4. 用独立进程/系统指标交叉观测，但不得把进程内存增量当作 GC 分配字节。
5. 对无额外 recorder、最小 recorder、完整采样器三种变体分别记录输入和产物身份。
6. 若当前 Player 无法可靠取得逐帧分配字节，标记 `NOT_RUN/UNAVAILABLE` 并给出可复现证据，不得把 0 解释成无分配。

### B3. GPU 时间与显存验证

- 分别验证 FrameTimingManager GPU 时间、ProfilerRecorder、Windows GPU 进程计数器在当前环境是否可用。
- 记录有效样本、缺失、重复 timestamp、非正值、GPU 适配器与进程身份。
- 分开记录设备总显存、进程专用显存和共享显存；不可用值不能用设备容量替代。
- 多 GPU 或虚拟显示适配器存在时，确认 Player 实际使用的适配器；不把 WMI 溢出值当显存。
- 不为得到数字而更换渲染 API、降低画质或修改系统设置。无法可靠采集时保留 `NOT_RUN/UNAVAILABLE`。

### B4. 观测工具开销对照

同一输入、同一固定场景、相同预热与采样长度，对比：
- A：无额外采样器的临时非开发 Player；
- B：仅最低必要的 FrameTiming/GPU 采样；
- C：完整采样器与系统 sidecar。

每种至少 3 次独立进程。记录产物 SHA、CPU 主/渲染/GPU 帧时间、帧间隔、GC、内存、采样器耗时、进程 CPU 时间与缺失率。保留原始数据、失败、离群值和缺失。不能简单将 A/B/C 的差值称为因果，除非条件足以支持该推断。临时采样构建不能冒充无观测发行包。

### B5. 警告语义审查（只读）

从 91 条清单中最多选 3 个代表类别，进一步检查：
- `FindObjectsByType(..., FindObjectsSortMode)` 及关联诊断；
- `FindFirstObjectByType` 的身份与选择语义；
- 3 条 `CS0414` 字段的生命周期/引用；
- 2 条场景序列化版本警告的安全处理策略。

记录行为等价性、inactive/scene/owner/稳定 ID/实例顺序风险和必要回归。不得机械替换 API，不得打开并保存用户场景来消警告。91 条仍全部 OPEN，除非未来独立修复获准并通过回归。

### B6. 交付与通过条件

提交：
- `REPORT.md`、`ACCEPTANCE.md`、`TESTING.md`、`Evidence/INDEX.md`；
- Recorder 能力枚举、探针输入输出、原始采样、缺失/异常统计、进程与产物身份；
- GPU/显存可用性证据、工具开销对照、统计脚本与复跑命令；
- 最多 3 个警告类别的语义审查与后续建议；
- 失败历史、`NOT_RUN`/`UNRESOLVED` 和用户文件保护哈希。

通过仅表示“测量能力已验证并准确界定”，不表示性能达标。不得在没有有效数据时把 GC Alloc、GPU 覆盖或可用显存改成 PASS。

### B7. Codex 指令

读取本文件并执行 PERF-02。只修改文档目录中的工具与证据，不改产品玩法、场景、ProjectSettings、依赖或存档合同。保留所有原始失败和未执行项。推送 GitHub 后重新读取远端 `main` 核对完整 SHA，返回逐项状态和证据链接，然后暂停等待独立复审。
