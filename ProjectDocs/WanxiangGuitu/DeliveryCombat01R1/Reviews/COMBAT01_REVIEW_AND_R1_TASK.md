# COMBAT-01 复审结论与 COMBAT-01-R1 任务书

## A. 固定 SHA 复审

- 仓库：`mizunagare/BallMaze`
- 基线：`d37b9ba98deea109fa67900314a2f6864b24c98a`
- 最终交付：`be448f56cb629022047c5de35ca3bfb03eac7604`
- 已重新读取远端 `main`，完整 SHA 与交付一致。

证据：
- [报告](https://github.com/mizunagare/BallMaze/blob/be448f56cb629022047c5de35ca3bfb03eac7604/ProjectDocs/WanxiangGuitu/DeliveryCombat01/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/be448f56cb629022047c5de35ca3bfb03eac7604/ProjectDocs/WanxiangGuitu/DeliveryCombat01/ACCEPTANCE.md)
- [复跑说明](https://github.com/mizunagare/BallMaze/blob/be448f56cb629022047c5de35ca3bfb03eac7604/ProjectDocs/WanxiangGuitu/DeliveryCombat01/TESTING.md)
- [时序合同](https://github.com/mizunagare/BallMaze/blob/be448f56cb629022047c5de35ca3bfb03eac7604/ProjectDocs/WanxiangGuitu/DeliveryCombat01/TIMING.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/be448f56cb629022047c5de35ca3bfb03eac7604/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Evidence/INDEX.md)

## B. 复审结论

**COMBAT-01 产品实现与受控战斗规则在交付方证据范围内有条件接受；整批不能判定通过。**

交付方报告为 `14 PASS / 1 FAIL / 4 NOT_RUN / 5 UNRESOLVED`。不能将188项受控断言、正常AI三进程和验收Player六进程相加成“全流程全绿”。

### 接受的实现范围
- 四武器普攻/技能加入可配置前摇与单次释放。
- 冷却在接受动作时开始，取消不退款。
- 已释放投射物与当前武器解耦；切武器保留，暂停冻结寿命/移动/碰撞。
- 翻滚、UI暂停、死亡、切武器取消尚未释放的攻击。
- 保留原伤害、品质分支、长枪追加段、弓独立箭、经济、随机流和v9合同。
- 受控测试覆盖命中、未命中、遮挡、多Collider、取消、暂停、生命周期；正常AI与验收Player分别有独立证据。
- 发行构建0错误93警告，隔离验收构建0错误116警告；测试驱动剔除证据已提供。
- 用户文件哈希保持不变。

### 必须保留的失败与缺口
1. **C15 FAIL：**纯发行Player后台关闭的限时退出确认超时。请求已发出不等于退出成功，后续PID消失也不能补造退出码。
2. **C16 NOT_RUN：**专用“前摇中写盘，再新进程恢复”测试未执行。一般冷却恢复和跨进程恢复不能替代。
3. **C17/C18/C19 NOT_RUN：**原生U16、独立人工战斗手感、完整性能预算未执行。
4. **C20–C24 UNRESOLVED：**D3D12 UNKNOWN、Editor青色帧、Editor.Search、JobTempAlloc以及额外Editor启动阻塞仍开放。

本次复审读取固定SHA上的源码、设计、报告、验收矩阵和证据索引，没有在Windows上重新构建或运行游戏。运行结果仍属于交付方证据，不冒称审核方独立重跑。

## C. 下一批：COMBAT-01-R1——只关闭两项具体缺口

开始基线：`be448f56cb629022047c5de35ca3bfb03eac7604`。

本轮不扩展战斗系统，不加新武器/连招，不改伤害、冷却、经济、地图、随机流、v9合同，不进行无证据的对象池重构。

### R1-01：前摇中保存与新进程恢复
1. 使用隔离工程和合成存档，保留用户场景/设置/Recovery覆盖层哈希，不访问真实存档。
2. 通过真实游戏业务入口开始有前摇的攻击；在释放前触发正常检查点保存/退出路径。
3. 保存结果必须证明攻击仍未释放，且没有伤害、投射物或资源消耗被提交。
4. 关闭测试进程并确认实际退出回执；启动全新进程读取同一Profile/Run。
5. 恢复后不得补发旧攻击、重复扣冷却/发奖或造成延迟伤害；后续合法新攻击仍能执行。
6. 记录保存前后动作ID、阶段、HP、投射物数、库存/来源账、冷却和新进程身份。
7. 若待释放动作不序列化，恢复后应无待释放动作；冷却按现有存档合同恢复，不引入新存档字段。

若检查点无法在前摇期间触发，先证明限制并提交最小测试接线方案；不得直接改JSON、反射调用内部保存方法或人为设置最终存档。

### R1-02：纯发行Player关闭确认超时诊断
1. 使用BUILD-01短路径、独立测试根和纯发行非开发Player，固定EXE SHA、启动参数、PID、窗口句柄/类名、会话和时间。
2. 保留原WM_CLOSE超时样本；新增诊断用新目录，不能覆盖原日志。
3. 分别记录关闭请求是否送达、窗口是否响应、进程是否退出、退出码是否可取得、宿主何时观察到PID消失。
4. 仅诊断本轮拥有者进程；不激活或抢占用户桌面、不发送物理Esc、不关闭用户程序、不强杀进程。
5. 若后台WM_CLOSE不适用于该Player窗口，明确标记机制不适用，改用可审计的测试拥有者退出协议；不能声称验证了物理标题栏关闭。
6. 若超时来自Player无法退出，保留日志并给出根因证据；没有因果证据则保持UNRESOLVED。

不得用“后来PID消失”将旧FAIL改成PASS。只有新样本按预先定义的退出协议完成，才可报告该新样本结果。

### R1-03：回归边界
- 运行直接受影响的COMBAT-01规则、Player存档恢复和发行启动/退出回归。
- 保留188 PASS、14/1/4/5原矩阵及全部失败历史；新结果单独归档。
- 不重跑100种子、20场景、全PERF窗口或全部旧战斗配对。
- 原生人工、性能预算、历史引擎根因不因本批关闭。

### R1-04：交付与退出条件
提交`REPORT.md`、`ACCEPTANCE.md`、`TESTING.md`、`Evidence/INDEX.md`、前摇保存/恢复时间线、关闭请求与进程日志、修复前失败、修复后独立样本、固定输入/产物哈希、用户文件保护哈希和未解决项。

只允许将本批实际执行的专用用例标记PASS。未执行继续NOT_RUN，根因未证实继续UNRESOLVED。更新`DEVELOPMENT_PLAN.md`只增量记录，不覆盖历史。推送后重读远端`main`核对完整SHA，然后暂停等待独立复审。

## D. 给 Codex 的执行指令

读取本文件，核对远端main是否仍为开始基线。仅实施COMBAT-01-R1两项任务：前摇中保存/新进程恢复专用用例，以及纯发行Player关闭确认超时的有界诊断。

不扩展战斗系统，不改产品数值/经济/随机流/地图/v9合同，不升级依赖、不新增CI，不覆盖用户文件或真实存档。保留所有原始失败；不得把进程消失、退出码0或编排器完成直接等同于游戏业务成功。完成后提交推送、核对远端完整SHA，返回证据并暂停。
