# COMBAT-01-R1 复审结论与 UX-01 任务建议

## A. 固定 SHA 复审
- 仓库：`mizunagare/BallMaze`
- 基线：`be448f56cb629022047c5de35ca3bfb03eac7604`
- 最终交付：`2caa2bb91c518078ea16c4230614eb2eb26034d9`
- 远端 `main` 已重新读取，完整 SHA 与交付一致。

证据：[报告](https://github.com/mizunagare/BallMaze/blob/2caa2bb91c518078ea16c4230614eb2eb26034d9/ProjectDocs/WanxiangGuitu/DeliveryCombat01R1/REPORT.md) · [验收](https://github.com/mizunagare/BallMaze/blob/2caa2bb91c518078ea16c4230614eb2eb26034d9/ProjectDocs/WanxiangGuitu/DeliveryCombat01R1/ACCEPTANCE.md) · [复跑](https://github.com/mizunagare/BallMaze/blob/2caa2bb91c518078ea16c4230614eb2eb26034d9/ProjectDocs/WanxiangGuitu/DeliveryCombat01R1/TESTING.md) · [证据索引](https://github.com/mizunagare/BallMaze/blob/2caa2bb91c518078ea16c4230614eb2eb26034d9/ProjectDocs/WanxiangGuitu/DeliveryCombat01R1/Evidence/INDEX.md)

## B. 复审结论

**COMBAT-01-R1 的两项新增验证在交付方证据范围内有条件接受；原 COMBAT-01 的历史失败和未执行项不回写，整体验收仍未全部通过。**

### R1-01：前摇中保存与新进程恢复
交付证据形成专用时间线：
- 攻击进入 Startup、pending=1，目标 HP 55、投射物 0。
- F5 保存和实际退出前仍未释放，HP、库存、来源账未变化。
- 新进程恢复同一 Profile/Run/区域/seed/布局/随机流/装备，动作回到 Idle、pending=0。
- 等待超过前摇与弹体寿命后，没有补发旧攻击或延迟伤害。
- 后续新攻击正常命中，资源 HP 55→22。
- 两个 Player 进程有独立句柄信号与退出码 0。

该证据支持未释放攻击不序列化、不在恢复后补发，冷却按既有合同恢复。

### R1-02：发行 Player 关闭确认
Close2/Close3 新样本具有独立窗口/进程观测、Player 与宿主句柄信号、退出码 0 和产品退出审计。它支持新样本中后台 WM_CLOSE 可以完成可审计退出。

**旧 C15 的 30 秒关闭超时根因仍 UNRESOLVED。** 新样本成功不能解释旧样本，也不能把旧 FAIL 改成 PASS。物理标题栏与原生 U16 仍未执行。

### 其他边界
- 188 项规则与 31 项核账属于不同层级，不能相加为总通过率。
- 发行构建 0 错误、93 警告；验收构建 0 错误、133 警告。警告继续按既有清单管理。
- 用户场景、ProjectSettings、Recovery 文件及 1152 项产品输入哈希不变。
- 原生 U16、独立人工试玩、完整性能预算仍 `NOT_RUN`。
- D3D12 UNKNOWN、Editor 青色帧、Editor.Search、JobTempAlloc、旧额外 Editor 启动阻塞与旧 C15 根因继续 `UNRESOLVED`。

本次核查了固定 SHA 上的报告、验收表、时序/存档证据与进程观测记录，没有在 Windows 上独立重跑。因此运行结果仍属于交付方证据。

## C. 下一步建议：UX-01 原生操作与人工试玩准备

COMBAT-01/R1 已覆盖相当多自动化规则，但仍缺少独立玩家对攻击时序、武器差异、界面理解与操作可发现性的直接反馈。继续堆自动化断言不能替代真实试玩。

### UX01-01：固定版本
- 固定正式非开发 Player、配置、分辨率、画质、键位映射和合成存档身份。
- 不把隔离验收 Player、虚拟输入或 Editor 场景称为正式人工试玩。
- 用户覆盖层只记哈希，不发布用户文件内容。

### UX01-02：新玩家任务脚本
由独立试玩者按固定步骤执行，不提前讲解：
1. 从标题进入或继续。
2. 查看装备并出征。
3. 森林移动、转向、观察目标。
4. 使用指定武器完成普攻和技能。
5. 闪避敌人攻击，观察命中/受击反馈。
6. 采集资源并检查背包。
7. 决定继续探索或撤离，完成合法撤离。
8. 回营核对仓库、制造物品并再次出征。
9. 修改一个键位，验证提示、实际操作与重启持久化。

记录是否独立完成、耗时、首次输入、失败/重复次数、玩家对目标/交互/撤离/仓库的理解、输入到动作反馈与真实伤害的一致性。观察者提示、技术中断和无效试次单独记录，不删除失败。

### UX01-03：Codex 能做什么
Codex 可以准备固定版本、任务脚本、记录表、缺陷分类与证据工具，也可以修复之后被实际试玩稳定复现并获授权的具体缺陷。

Codex 不能把虚拟输入、自动化 AI、截图或代码审查伪装成独立人工试玩。没有实际试玩人员或授权环境时，原生 U16 和人工试玩必须保持 `NOT_RUN`。

### UX01-04：退出条件
UX-01 的准备工作通过只代表协议与记录工具准备完成，不代表人工体验通过。提交任务脚本、空白记录模板、缺陷分类、版本身份和证据索引。没有独立试玩环境时暂停，不根据猜测修改战斗数值。

## D. Codex 指令
归档 COMBAT-01-R1 复审边界：前摇保存恢复专用证据可接受；新关闭协议样本可接受，但旧 C15 根因继续 UNRESOLVED。不得改写历史矩阵。

若开始 UX-01，只准备原生操作/人工试玩协议、版本固定和记录工具；不得将自动化标记为人工通过。保护用户文件与真实存档，不升级依赖、不新增 CI。推送后核对远端完整 SHA 并暂停等待复审。
