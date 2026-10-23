# 万象归途：A1 定向补丁与验证

日期：2026-10-23（Asia/Shanghai）。仓库mizunagare/BallMaze，分支main。实际本地HEAD与fetch后的origin/main均为审阅基线 **deaf0258b9335273546b4cfb20dda5d306780b82**；基线后没有新提交，开始工作区干净。没有reset、覆盖用户修改、重写历史或启用CI。

产品修复提交：**4eb69c6ce61213d1083f5a6e9a5bca890c924010**。后续提交补充跨进程测试和报告，不再改变产品代码；最终完整SHA与推送后的远端核对见交付回复及本报告Git历史。提交不能内含自身SHA。

Unity保持6000.6.5f1 / 3ff58d469c8a，URP17.6.0、Input System1.20.0、uGUI2.6.0，格式仍v9，兼容链未改。Packages和ProjectSettings本轮没有变更。R01/R02、品牌、旧示例清理、分页、来源账和唯一结算直接保留。本轮没有扩地图、修改冻结规则、实施交付B或进入B07。

## A1 对照表

| 编号 | 最小增量 | 修复前 | 最终复测 |
| --- | --- | --- | --- |
| A1-01 启动隔离 | 包装器启动前确定根并传-wanxiang-storage-root；Run在打开场景/Play之前验证；缺参/相对/驱动器相对/LocalLow/重解析拒绝。默认Start与驱动共享唯一根，移除后续InitializeStorage切换；记录首次定位、初始化、读写、退出 | Isolation结构入口回归FAIL，旧驱动没有pre-Play验证；为避免真实档风险没有执行旧缺参正常AI | PASS：静态/进程负例、正常AI完整收益路线、退出和新进程恢复、根外初始化拒绝及替身哨兵 |
| A1-02 重复确认 | 将不可覆盖迁移证明与可更新选择回执分开。选择用唯一临时文件、Flush(true)、File.Replace，保留.previous；UI绑定检查时新旧集合指纹，提交前再查变化；不动游戏主备/页/收益 | 首次选择后旧集合变化，再次ChooseNew因确认文件已存在而FAIL | PASS：首次/再次、陈旧UI、提交中变化、写前失败保留旧确认、重试、写后中断；另起两个Editor进程验证失败后恢复并确认 |
| A1-03 空目标/恢复 | 发布前复查目标非文件、非重解析且仍为空，Directory.Delete(path,false)只处理空目录，再Directory.Move；OS拒绝非空竞争，不递归删除。成功ApplyCamp后清旧Error，失败不假清理 | Empty与Recovery均FAIL：安全空目录阻止发布；新建营地残留旧定位Error，初始保存失败 | PASS：缺失/空目标成功，文件/异常内容保留，发布前新增文件停止，修复后重试，真实/失效junction拒绝，初始化可保存并再次出征 |

选择回执更新不覆盖迁移发布回执；没有合并两个Profile或Run。已使用的材料/药水与死亡、保护、结算规则不变。迁移/确认按现有v8/v9及稳定实体数据检查，不重生成/重抽奖励。

## 修复前回归与实现过程

先将审阅基线复制到不带Library的RedProject，安装回归，使用显式测试Root和batch Editor执行四项：Isolation、Choice、Empty、Recovery，**4 FAIL / 0超时**。原始回归源码保存在Evidence/Red-test-source.cs.txt，结果和失败断言保存于Red-results.json、Red-assertions.txt。Isolation是安全的结构入口检查，未进入旧不安全正常AI生命周期；其余只操作合成档与隔离目录。

首次修复后同组 **4 PASS**。补测发现Unity Mono对Windows正斜杠绝对路径的根字符串保留方式不同，新的完全限定路径检查误拒绝合法路径；规范化根分隔符后复测PASS，同时继续拒绝C:relative与\relative。扩展矩阵复跑还发现固定夹具目录重名，改为每次GUID目录后通过。没有削弱业务断言。

较早的Full回归曾有一次B05EditChecks进程在Editor启动/程序集加载阶段exit=-1，未到规则断言，原因**未核实**；后续干净副本及最终受影响复测该项均exit0。保留失败，不能声称从未发生或已确定某个引擎原因。

## 本轮实际验证（不继承deaf0258的PASS）

| 类别 | 实际结果 | 说明 |
| --- | --- | --- |
| 干净隔离导入/编译与原19方法 | PASS，19/19，0超时 | 本轮FinalProject首次不含Library，原19方法全执行；100种子规则、20种子真实碰撞、装备/容器/双武器/冷却/词缀/仓库/配方/旧档均保留 |
| 最终代码受影响复测 | PASS | 最后规范化路径/重解析检查后，再跑WGDeliveryACheck、A1、历史v1～v8/旧森林、Edit规则、资源审计与正式构建；latest-method-status共26个方法最后一次均通过，历史失败仍保留 |
| A1核心四项 | PASS | 失败→修复后结果分别记录；不得把预期负例exit1当任意启动错误通过 |
| v8/v9×营地/在途/Pending/Committed | PASS，8组合 | 选择/再选/陈旧UI/写后恢复前后主备、页、档案字节不变，检查可读状态与收益不重复 |
| 重复确认跨进程 | PASS，2个Editor进程exit0 | 第一进程在更新前失败保留旧回执；第二进程恢复Conflict、重试确认、同一新版Run及文件不变 |
| 三个受控游戏进程 | PASS，3个exit0，0超时 | 最终产品代码重建验证版后，zero-save→zero-resume→terminal-resume；保持既有显式目录/批处理隔离，不使用真实档 |
| 正常AI原工程自动试玩 | PASS，Normal和Resume两个进程exit0 | 实际箭击/警报/追击返巢、击杀、伐木拾取、引导撤离、入库取材制造、再出征及新进程身份/收益核对 |
| 非开发Windows构建 | PASS | BuildOptions.None，错误0、警告47；源68个C#文件与最终构建副本一致，见source-manifest |
| 无运行驱动正式版启动 | PASS（启动/初始隔离存档） | 创建v9营地档；隐藏窗口CloseMainWindow=false，工具最终终止exit=-1；**不是正常退出验收** |
| 人工试玩 | NOT_RUN | 自动移动/API攻击调用与真实正常AI不等于人工试玩 |
| 内核级全进程文件访问跟踪 | NOT_RUN | 存档入口回执+前置守卫+合成目录哨兵，不冒充ProcMon/内核审计 |
| 真实断电/磁盘损坏/所有恶意并发或路径别名 | NOT_RUN | 使用隔离失败注入，不在真实档破坏测试 |

原19方法完整重跑后，路径细节补强产生了产品变更，已按受影响范围重编译、复测及重建产物；没有把早一版源码的构建冒充最终产物。正式Release不含WGPlayerFlow；CurrentVariant只为受控验证另加该驱动。二者.exe启动器哈希相同不代表游戏代码相同，build-artifacts.json另记Assembly-CSharp.dll哈希与驱动类型差异。

## 正常 AI 启动到退出证据

最终运行：请求种子 **360410405**，实际固定 **418**，generation3、contentB06-A1。准备弓主武器/剑备用、石1矿2；未改生命/伤害/速度，AI全启用，出征后不传送。正常攻击、木材3收益、提交入库、取木2制造及再次出征有独立断言，不能只凭待提交截图证明入库。

Evidence/NormalAI/storage-audit.jsonl共 **39条**：首次pre-play为playing=false；两个进程各一次initialize、各一次before-exit，均位于同一ISOLATED_ROOT。没有进入Play后改切目录。Normal、Resume退出码0、无超时；根外初始化尝试在触碰目标文件前拒绝，合成Protected/DoNotTouch哨兵哈希保持。应用审计源码与包装器校验路径范围，未宣称覆盖所有OS后台文件访问。

负例三进程：RejectMissing/RejectRelative/RejectLocalLow分别在Play前以明确A1_ISOLATION_REJECTED标记退出1，未产生存档回执，替身哨兵不变。静态入口另覆盖驱动器相对、根相对和合法正斜杠路径；隔离测试覆盖存在/失效junction。所有目标均是工作区合成目录，不指向真实玩家档。

## 对历史运行的核查与更正

核对deaf0258驱动、TESTING与产品Start调用链，以及此前NormalAI3/Editor.log等已有记录：非batch启动的默认Start确实可能先于后半程切换路径；已有日志缺少首次定位和完整存档访问回执。

**历史正常AI是否触及真实玩家目录：未核实。** 没有证据证明已损坏/删除/修改，也没有证据可保证绝对安全。本轮没有为了补证而读取、移动或破坏真实玩家档。旧报告补了更正，旧PASS不能继承为A1启动安全PASS；不将19方法和受控Player误判为同一缺口。

## 复跑与仓库证据

- TESTING.md、Invoke-A1.ps1：全新外部副本，原19方法+三个受控进程+7项A1检查。
- ../DeliveryA/TESTING.md、Invoke-NormalAI.ps1：唯一正常AI启动命令，强制进程参数与pre-Play校验；原工程Editor须关闭；临时驱动退出后移到测试根，不进入产品构建。
- Evidence/Red-*、Green-*：基线失败和过程复测；Evidence/Full-*保留较早Editor启动失败。
- Evidence/Final-results.json、Final-assertions.txt、latest-method-status.json：本轮完整运行、受影响复测及最后结果，含未隐藏的中间失败。
- Evidence/NormalAI/：4张真实截图、CSV、元数据、收益/制造/再出征断言、两进程回执和首次到退出路径审计；raw日志仅保留SHA256。
- Evidence/startup-negative.json、player-process-results.json、player-assertions.txt：实际退出码/超时及拒绝标记。
- Evidence/BuildSummary.txt、build-artifacts.json、source-manifest.json：代码提交/源码/产物对应；正式程序本机位于 C:/Users/guan/Documents/unitytest/WanxiangA1/Final/Release/WanxiangGuitu.exe。

未提交真实玩家档、凭据、Library/Temp、执行用junction、二进制构建或含许可信息的完整Unity日志。历史合成夹具继续复用。

## 已知限制与下一批

没有新增分页垃圾回收或磁盘配额；历史页、迁移档和中断staging仍可能增长。选择.previous保留旧确认，游戏数据主备与唯一结算继续原协议。非递归空目录处理与原子发布拒绝已测竞争变化，但不宣称提供跨进程数据库事务或所有恶意文件系统竞态的安全证明。

一次Editor启动阶段-1原因未核实；后续该项通过不证明底层偶发问题永不再现。无驱动正式版正常退出/人工试玩本轮未验证。下一步仍是A1按最终SHA复审，然后才按B1渡口→B2地点收益目标→B3随机流→B4三条收益路线推进；B07未开工。推送完成不等于已通过复审。
