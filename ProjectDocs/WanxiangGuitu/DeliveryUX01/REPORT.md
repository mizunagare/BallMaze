# UX-01 准备交付

开工远端与本地 main：`2caa2bb91c518078ea16c4230614eb2eb26034d9`。本批仅新增协议、空白模板、固定版本包与证据工具；没有启动 Player、注入输入、安排模拟玩家或修改产品。交付提交以 GitHub 上包含本报告的完整提交为准，外部交付回执记录最终 SHA，避免报告自引用哈希。

## COMBAT-01-R1 复审归档

[收到的固定 SHA 复审全文](Reviews/REVIEW_AND_TASK.md)。审核方核查提交证据，没有独立运行 Windows。前摇保存/新进程恢复的专用证据、Close2/Close3 新后台 WM_CLOSE 样本在该证据范围内有条件接受。新样本不能解释旧 C15 的30秒超时；**旧 C15 根因仍 UNRESOLVED，旧 FAIL 不变**。物理标题栏关闭不由后台 WM_CLOSE 证明。

188项规则与31项核账分层保留，不相加为通过率。原 COMBAT-01 的14 PASS/1 FAIL/4 NOT_RUN/5 UNRESOLVED，R1 的12 PASS/0 FAIL/3 NOT_RUN/6 UNRESOLVED均为历史结果，不继承为本批测试。发行0错93警告、验收0错133警告亦为复用版本的历史构建信息。

## 本次实际准备

- [协议](PROTOCOL.md)、[参与者九步目标脚本](TASK_SCRIPT.md)、[观察者指引](OBSERVER_GUIDE.md)，区分独立/提示后完成、失败、技术中断和无效试次；四武器记录学习迁移。
- [版本锁](Evidence/Preparation/version-lock.json)：纯非开发发行包191个文件完整校验；无验收驱动证明复用R1已提交材料。本轮没有新构建。
- 本机外部包 `I:/WUX01/1028-140121-e5720e`：四份Fresh无进度起点及一份Continue专项起点，均未分配参与者、全部NOT_RUN。Fresh的Profile/Run只能由玩家真实开始后产生。
- Continue完整复制已复审的合成集合4文件，含主备档、入口租约和新游戏事务。不是人工产生的进度，不用于证明首次营地可发现性。
- [空白记录模板](Templates/)、只读磁盘核对、显式人工启动器。启动器要求操作员确认环境和独立参与者；这些声明不是自动验证。真实进程句柄/退出码也不能自动变成人工PASS。

## 本轮验证与限制

工具自测 **14 PASS /0 FAIL**；PowerShell静态语法解析 **PASS**；产品输入 **1152/1152哈希不变**，用户五项文件哈希不变。证据见[索引](Evidence/INDEX.md)。这些均为准备检查，不是游戏体验或原生验收。

首次包准备因错误比较“发布目录的子集文件”与完整运行时集合而失败，退出1。改为绑定已发布完整 storage-after 清单后，4文件完整复制通过。原始stderr保留，未修改历史材料，详见[失败历史](FAILURE_HISTORY.md)。

尚未确认实际独立参与者和获准交互环境，本轮不启动试玩。原生U16、独立人工理解、战斗手感及完整性能预算继续NOT_RUN。旧C15、D3D12 UNKNOWN、Editor青色帧、Editor.Search、JobTempAlloc及旧额外Editor启动阻塞继续UNRESOLVED。不得因准备完成关闭这些项目。提交后暂停等待固定SHA独立复审，不自动开始玩法修复。
