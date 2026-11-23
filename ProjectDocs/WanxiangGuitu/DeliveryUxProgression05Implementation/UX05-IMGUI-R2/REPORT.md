# UX05-IMGUI-R2 真实交互报告

**PASS（本轮 IMGUI-R2 范围）。** 最终三条隔离 Player Run 全部正常退出0，IMGUI/uGUI 各24次真实历程交互通过，17对查询状态一致。先前缺少退出回执及滚轮截图的运行原样保留，由新 Run 补齐。等待负责人复审，不代表自动获准发布。

## 改动与根因 [S] [P]

本轮唯一产品变化为 `Assets/CombatPrototype/AdventureFlow.UI.cs`，对接手 R1 文件的差异可由 [原文件](EVIDENCE/AdventureFlow.UI.before.cs.txt) 复核。

1. MIXED-A01：前台 PID/HWND 正确，原生 Down/Up 已到 Player，但非活动 uGUI canvas 的清理每帧将 `historyOpen` 清零。改为仅在该 canvas 仍活动时关闭其旧页面。
2. MIXED-A02：IMGUI 关闭按钮穿透到底层 uGUI“出征准备”；类型筛选也影响底层页签。添加透明 raycast 输入遮罩，仅在 IMGUI 历程打开时屏蔽底层 uGUI。最终 MIXED-A06 的关闭后状态保持 Camp、`preparing=false`，随后实际点击背包关闭，恢复 `inputContext=Camp`、`inventoryOpen=false`、`inputBlocked=false`。

ObjectiveHistory、Schema、迁移和结算模块本轮字节未变。没有重新设计查询或第二套数据逻辑。两项修复均在原始产品失败留档之后实施。

## 原生输入与业务消费 [P] [C]

正式复核选用 MIXED-A06、EMPTY-A03、UNKNOWN-A03：

| Run | IMGUI 交互 | uGUI 交互 | 相同查询状态 | 退出码 | 最终证据状态 |
|---|---:|---:|---:|---|---|
| MIXED-A06 | 20 | 20 | 15 | 0 | PASS |
| EMPTY-A03 | 2 | 2 | 1 | 0 | PASS |
| UNKNOWN-A03 | 2 | 2 | 1 | 0 | PASS |
| 合计 | 24 | 24 | 17 | 三条均为0 | PASS |

最终三条 Run 共55次前台验证、55次实际投递操作，其中48次历程控件操作（IMGUI24，uGUI24）有对应状态及截图，无未投递操作。[逐交互矩阵](INTERACTION_MATRIX.csv) 将原始动作、消费状态和归档截图关联。早期 MIXED-A05 第14步工具中断未投递及第45/46行误关联意图仍原样保留，均不计入最终三条 Run；详见 [关联诊断](EVIDENCE/MIXED-A05/foreign-actions.json)。

每次有效操作前记录 PID、HWND、HWND PID、Foreground HWND/PID、WindowRect、ClientRect、DPI、ClientToScreen 原点与截图/客户端/屏幕坐标。实测为 1280×720 客户端、DPI 96、Scale 1；截图原点 (319,160)，客户端屏幕原点 (320,191)。坐标由所观察的截图转换，未猜测窗口位置。使用 `@oai/sky` 激活和原生输入，Player 侧 P/Invoke 仅观察窗口事实，不投递输入。前台检查与真实消费分开判断。

`observer/input.jsonl` 证明原生 MouseDown/Up 到达；`outcomes.jsonl`、`observer/states.jsonl` 与截图证明产品响应。上述“消费”数是实际页面、筛选、分页、关闭状态及滚动显示的成功操作数，不是 `Event.Use` 回调次数；观察器的 `used=false` 不能解释为控件未消费。

| 操作要求 | 实际证据 |
|---|---|
| 打开、全部历史 | 原生点击后 `open=true`，128 条，1/7 页 |
| 地区 | 森林126、遗迹1、洞窟1、全部128；实际按钮逐项循环，页码重置1 |
| 类型 | 采集0、寻宝126、讨伐2、首领2、特殊0、全部128 |
| 时间排序 | 对每次实际查询独立重算 CompletedAtUtc 降序、CommittedAtUtc 降序、稳定身份键升序；并列时间确定性一致 |
| 七页与末条 | 两种 UI 原生逐页前进，20×6+8，实际滚动显示末条 `ruins.challenge` / Run `2a10985d3681439e9ffe65d26f5dc04c`；原生返回第6页 |
| 历史名称 | 当前隔离内存目录改名后，历史仍显示“扫箱”；未写历史或存档。改名设置通过控制文件，打开/筛选为原生输入 |
| 空历史 | 文案为空历史，无成功记录；两种 UI 实际打开与关闭 |
| 未知历史 | 文案“旧版目标历史未知”，未伪装成未完成；两种 UI 实际打开与关闭 |
| 关闭与恢复 | 页面关闭不进入准备；背包实际关闭后输入上下文回到 Camp。未将营地按 W 无移动宣称为行走验证 |

时间排序按冻结产品合同固定从新到旧；没有虚构一个不存在的升序按钮。查询的全部六字段、排序与分页边界逐项比较，17 对状态完全一致。两种 UI 在每个 Run 内共用同一隔离存档和同一查询业务层。

末条像素证据已独立打开复核：[IMGUI末条](EVIDENCE/MIXED-A06/observer/screen-0009.png)、[uGUI末条](EVIDENCE/MIXED-A06/observer/screen-0033.png)，均完整显示“守誓”及同一Run身份。此项为Agent图像检查，不冒充负责人[M]人工验收。

## 驱动、夹具与只读范围

观察器在正常标题“继续游戏”之后配置营地背包、选择渲染后端、延后隔离自动保存，随后历程控件均使用原生输入。关闭自动保存仅排除定时写盘噪声，没有屏蔽业务显式保存。MIXED-A03 的自动保存活动原样保留，不作为只读通过。

混合夹具来自 R1 已保存的 128 条历史及受控并列时间/地区组合，来源见 [R1 夹具](../EVIDENCE/R1/mixed-ui-fixtures.json)，不是本轮重新取得目标完成链路的证明。空、未知使用历史隔离夹具副本。R2 只验查询交互，不声称夹具本身证明本轮完成了128次目标。所有运行显式指定 evidence 内的新 storage root。

三份有效交互 Run 在查询、切换UI、筛选、翻页及关闭页面期间，Profile JSON 与主档 SHA 均不变。进程退出另有既存 `OnApplicationQuit → SaveBeforeExit → SaveProgress`，主档 SHA 因退出保存变化：revision 加1，payload 仅改变 revision 与 camp 的 events/randomStateJson/resources；封套同步修改 savedAtUtc/checksum。独立复算确认退出后的备份逐字节等于退出前主档、两侧校验正确、历史/结算/收益完全相同；130个关联文件保持原字节。不能将这一结果写成“整次运行从启动到退出主档零变化”。没有读写真实用户存档，也没有为此读取真实存档来取指纹。

## 构建身份 [B] [S]

两项 UI 产品修复使产品 DLL 变化，因此重新完成 Acceptance、NoDefine、Release A02，退出码均为0。DLL SHA：

- Acceptance：`BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8`
- NoDefine：`E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78`
- Release：`18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C`

最终 sidecar Driver SHA：`983A936C423F7140AC8BA34214DF12D427B7777FE4D72D1D2419F787AE4EC393`；它只安装在 Acceptance 的隔离副本，产品 DLL 与正式 Acceptance A02 完全相同。后续修改监控脚本、输入辅助器及滚动观察字段没有重编产品 DLL。编译参数和源 SHA 在 DRIVER-A05 中，完整产物身份见 [构建复核](EVIDENCE/final-build-identity.json)。IMGUI-R2-A05/A06/A07 是同产品、同Driver的不同观察副本，便于每个新PID重新绑定窗口，不是三种产品构建。旧Driver执行源快照保留在各DRIVER目录。NoDefine 与 Release 产品 DLL 中所查验收标记为0，目录无 sidecar。Release 发布回执 EXE SHA 与实际文件一致。本轮新版本 NoDefine/Release 的结论为构建及静态门禁，未冒充本轮该版本完整 Player 矩阵。

## 全部 Run 与失败保留

原68条：PASS59、SUPPLEMENTAL_STOPPED1、FAIL_LAUNCH1、EXPECTED_NEGATIVE_BLOCKED1、FAIL2、PROCESS_CUT_WITNESSED2、OBSERVED_STARTUP_ONLY2。

R1新增79条：PASS43、FAIL_TIMEOUT4、PROCESS_CUT_WITNESSED11、INCOMPLETE_EVIDENCE5、FAIL15、EXPECTED_NEGATIVE_BLOCKED1。147行历史分类及4142个原始证据文件逐项未变。

R2新增12条：PASS4、FAIL2、FAIL_DRIVER1、PASS_INTERACTION_INCOMPLETE_EXIT3、INTERACTION_OBSERVED_AUTOSAVE_ACTIVE1、INCOMPLETE_INPUT_TOOL1。完整159条汇总为PASS106，其余真实类别见 [独立分类](EVIDENCE/run-audit.json)，不将余项统一写成FAIL或NOT_RUN。原始 PASS 文档未被覆写；矩阵保留 `probe_raw_status` 与当前证据完整性判定的区别。

UNKNOWN-A01 的非原子控制文件写入分享冲突属于驱动缺陷，改用原子配置文件发布后 UNKNOWN-A02 交互通过。MIXED-A01/A02 属产品 D 类；MIXED-A03 为自动保存配置噪声；EMPTY-A02 为工具 A/B 类，不判产品缺陷。

## 仪器缺口闭环与停止

EMPTY-A01 和 UNKNOWN-A02 的原生全交互证据齐全，但最初启动器未保存数字退出码。EMPTY-A02 补跑时，工具两次拒绝 `foreground window did not report a process id`。停止该路径并保留诊断，宿主终止隔离PID，退出-1不是产品失败。持久化输入辅助函数还将两条被拒绝意图错误追加到上一 Run；原记录不删。随后使用显式全局Run上下文、manifest/PID/HWND守卫、重新选择新观察副本的窗口，在新Run ID EMPTY-A03、UNKNOWN-A03、MIXED-A06上完成原生输入与监控退出，均为0。未证实Windows工具内部拒绝的根因，未将它判成产品缺陷。

早期观察器只在页码/过滤/鼠标按键等变化时截图，没有捕获单独滚动，早期工具画面不能冒充归档截图。最终Driver增加只读滚动状态和截图触发，MIXED-A06两种UI末条滚动均有位置变化、六字段和归档截图，未修改产品或验收期望。[NativeActions.js](Tools/NativeActions.js) 在最终三条Run实际执行，启动标题无业务state时使用明确null，尚未发送输入前的辅助器装载/空state错误未计作Player失败或有效输入。

本轮授权交互项已关闭。多DPI和人工体验未扩展验证，既有物理断电NOT_RUN保持。下一步为负责人复审交付。本轮停止，不暂存、提交、推送、合并或启动 UX-06。

## 复核入口

[逐 Run 矩阵](PLAYER_RUN_MATRIX.csv) · [证据索引](EVIDENCE/INDEX.json) · [独立复算](EVIDENCE/independent-review.json) · [复算工具](Tools/verify_results.py) · [全项目最终状态](../FINAL_ACCEPTANCE_REPORT.md)
