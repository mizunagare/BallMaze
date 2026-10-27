# PLAYER-02 复审结论与 PERF-01 Codex 任务书

## A. PLAYER-02 复审

### 固定身份
- 仓库：`mizunagare/BallMaze`
- 开始基线：`428c41fa4f82e7a95c3163319384cad668b5ef6b`
- 最终交付：`6f2abca5f89fc80fc5d298623eda12f557654b78`
- 复审时远端 `main` 完整 SHA 与最终交付一致。

### 结论
**PLAYER-02 的隔离非开发验收 Player 自动化纵切，在交付方证据范围内有条件接受；不等于正式发行包完整冒险已通过，也不等于原生、人工或性能验收通过。**

依据：
- `PlayerAcceptanceDriver` 以 RuntimeInitialize 方式运行，不依赖 `UnityEditor`；源文件仅保存在文档目录，并只注入隔离验收副本。
- 驱动经虚拟 InputSystem/uGUI 和本次私有非活动桌面窗口消息执行 UI 操作；报告说明不直接调用业务回调、不反射、不传送、不冻结 AI、不改奖励或直接修改正例存档。
- 最终 Story5 六个独立 Player 进程完成设置、主流程、Pending、Committed、制造、后继 Run；有逐阶段账目和新进程身份核对。
- 正式发行构建为 `0 Error / 91 Warning / 4 Log`；隔离验收构建为 `0 Error / 114 Warning / 4 Log`。PE/字符串/程序集引用/场景检查声称发行包不含测试驱动。
- 产品玩法、v9 存档结构和依赖未修改；用户场景、ProjectSettings 和 Recovery 覆盖层未提交。
- 历史 31 PASS/6 FAIL 保留，未以最终成功覆盖失败。

限制：
- 本次复审读取固定 SHA 的报告、验收表、复跑说明、边界审计、失败历史、运行时驱动源码与产物排除证明；没有重新在 Windows 上构建或启动 Player。因此运行结果属于交付方本轮证据，不冒称为审核方重跑。
- 完整冒险发生在隔离验收 Player，不是原始发行产物。准确表述是“隔离验收 Player 自动化纵切通过”，不能说“发行包完整冒险已独立通过”。
- 虚拟输入和非活动窗口消息不等于物理键鼠；没有独立试玩人员。原生 U16、人工试玩、完整性能仍 `NOT_RUN`。
- 91 条发行警告仍开放；D3D12 `UNKNOWN`、Editor 青色帧、Editor Search、JobTempAlloc 根因仍 `UNRESOLVED`。
- 运行输入含用户场景/设置覆盖层，不是纯 Git `main` 场景的无条件复现证明。
- 本批没有发现要求回滚 PLAYER-02 测试工具或产品代码的明确问题；产品代码和依赖未变。

证据：
- [报告](https://github.com/mizunagare/BallMaze/blob/6f2abca5f89fc80fc5d298623eda12f557654b78/ProjectDocs/WanxiangGuitu/DeliveryPlayer02/REPORT.md)
- [验收](https://github.com/mizunagare/BallMaze/blob/6f2abca5f89fc80fc5d298623eda12f557654b78/ProjectDocs/WanxiangGuitu/DeliveryPlayer02/ACCEPTANCE.md)
- [复跑](https://github.com/mizunagare/BallMaze/blob/6f2abca5f89fc80fc5d298623eda12f557654b78/ProjectDocs/WanxiangGuitu/DeliveryPlayer02/TESTING.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/6f2abca5f89fc80fc5d298623eda12f557654b78/ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Evidence/INDEX.md)

---

## B. 下一批：PERF-01 性能基线与 91 条警告风险分级

### B1. 开始条件与边界
- 开始基线：`6f2abca5f89fc80fc5d298623eda12f557654b78`。
- 开工先核对远端 `main` 完整 SHA；若已前进，停止并报告新 SHA，不重置、不覆盖用户工作区。
- 本批先测量、分类、形成证据；不默认授权修改产品代码或一次性清零所有警告。
- 不升级 Unity/URP/依赖，不新增 CI，不改玩法数值、经济、地图、随机流或 v9 存档合同。

### B2. 固定输入
使用 BUILD-01 短路径预检和 PLAYER-02 隔离工程策略。记录 Git SHA、源文件清单、用户覆盖层哈希（不发布覆盖层内容）、Unity/依赖锁 SHA、CPU/GPU/驱动、内存、分辨率、窗口模式、画质设置、Player 产物 SHA、场景、存档/Run/种子、布局修订、构筑和采样工具版本。

所有测试用合成存档和工程外短路径；不读写真实玩家存档。若输入或硬件无法固定，记录偏差，不与历史样本直接比较。

### B3. 固定场景与重复次数
至少建立下列可复跑场景，每个固定场景至少三次独立运行，先预热再采样：
1. 标题静止 60 秒。
2. 营地空闲与设施交互 60 秒。
3. 森林移动和转向 120 秒。
4. 森林采集、拾取和交互 120 秒。
5. 普通敌战斗 120 秒。
6. 精英或首领战斗 120 秒；无法稳定触发则 `NOT_RUN` 并说明原因。
7. 撤离、结算、制造与场景切换。
8. 新进程恢复后继 Run。

不得冻结 AI、传送角色、减少实体、修改伤害或跳过实际渲染来制造稳定结果。保留所有失败和离群样本。

### B4. 指标与采样
在支持正式 Player 的工具中记录：
- CPU 主线程与渲染线程帧时间 P50/P95/P99。
- GPU 帧时间；无法取得则 `NOT_RUN`，不能用 CPU 时间代替。
- GC Alloc/Collection、托管内存、进程内存与可用显存指标。
- 场景/存档加载耗时、首次进入区域耗时。
- 帧率限制、VSync、分辨率、质量设置、前后台状态。
- 原始 Unity 日志、系统采样日志、启动/结束回执与采样中断。

先固定指标口径再汇总。保留原始采样，不只保存均值；评估采样工具开销。标题启动耗时不能冒充游戏性能基准。缺少目标硬件预算时，不得声称性能达标。

### B5. 91 条警告逐条审计
以 PLAYER-02 `WARNING_REVIEW.json` 和完整 BuildReport 为输入，核对当前冻结输入：
- 86 条 `CS0618`：列文件、行号、API、Player 影响路径与建议替代 API。
- 3 条 `CS0414`：确认字段是否仍被使用、是否为有意保留状态或真实死字段。
- 2 条场景序列化版本警告：定位对应场景/对象并评估风险；禁止直接打开并保存用户场景来消警告。
- `JobTempAlloc` 等导入期日志单独列出，不混入 91 条 BuildReport 警告。
- 每项标记风险（阻断/高/中/低/信息）、是否可能改变运行行为、是否需要回归、处置建议。

本批只做审计和可验证的最小复现，不默认修复全部 91 项。不得大规模替换旧 API。若发现明确高风险缺陷，单独报告影响与最小修复建议，等待授权。

### B6. 报告与通过标准
报告必须包含：
- 每个场景三次运行的原始数据、P50/P95/P99、离群值与失败样本。
- CPU/GPU/GC/内存/加载指标缺口。
- 环境差异、采样工具开销与测量限制。
- 91 条警告逐条表格和风险分布。
- 与旧批次比较时明确输入是否一致；不一致只作背景信息。
- 可确认的性能瓶颈、尚属假设的瓶颈、需要进一步剖析的路径。

PERF-01 通过条件：
1. 输入、产物、硬件、设置与运行场景可追溯。
2. 固定场景按计划至少三次运行；失败/中断/未执行项保留。
3. 原始采样与汇总可复跑，不混用 CPU/GPU 等不同指标。
4. 91 条警告全部逐条归类并给出处置建议。
5. 用户文件、依赖、存档与未提交工作区未被修改或纳入提交。
6. `NOT_RUN`/`UNRESOLVED` 明确保留；不宣称性能达标或发行验收通过。

### B7. 安全与交付
- 不激活或抢占用户桌面，不发送全局物理输入，不关闭用户程序。
- 不强杀超时进程；记录进程并跳过依赖步骤。
- 不上传用户场景、真实存档、凭据、Player 二进制或 Library。
- 交付 `REPORT.md`、`ACCEPTANCE.md`、`TESTING.md`、`Evidence/INDEX.md`、原始采样、警告清单和产物哈希。
- 更新 `DEVELOPMENT_PLAN.md` 时只增量记录本批状态，不覆盖历史结果。
- 提交并推送后重新读取远端 `main` 核对完整 SHA，返回每项 PASS/FAIL/NOT_RUN/UNRESOLVED，随后暂停等待独立复审。

### B8. Codex 执行指令

读取本文件并先完成 PERF-01，不要自动修复所有警告。先建立固定性能基线与逐条警告风险表；只有获得明确授权后才实施产品优化。保护用户文件和未提交修改，不升级依赖、不新增 CI、不重写历史。完成后提交 GitHub、核对远端完整 SHA，并暂停等待复审。
