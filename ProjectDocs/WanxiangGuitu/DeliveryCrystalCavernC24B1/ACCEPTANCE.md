# B.1 独立验收表

此表统计需求级条目，不把辅助断言或成功退出次数累加成需求通过数。取证与设计判断分开。

|ID|状态|结论与原始证据|
|---|---|---|
|B1-01|PASS|首次提示时机：Editor-first-before/after-A2及Player b1-first-before/after-A1；写入失败不成功，完整读回确认才成功。|
|B1-02|PASS|旧首奖待领/已领/已拆解后三个Player重杀样本仅提示常规掉落，NoticeAudit1完整奖励快照不变。|
|B1-03|PASS|重试不重复播报：真实noticeUntil与文案保持、revision不重复增加，五场景独立审核。|
|B1-04|PASS|同帧C24两处名称一致，原森林实际辅助目标保持旧名；Editor与Player均记录。|
|N02|PASS|引入C24前基准与候选六份合法同输入，35 POI及排序一致；仅Editor层。原位置比较失败保留。|
|B1-05|FAIL|C24路线预期收益不符专用工厂：兽皮误计、铁矿/装备遗漏、晶石高估；本批禁止修规则。|
|B1-06|PASS|四组晶环边界取证完整：Player实际释放、Collider几何、LOS、HP；Editor独立对照。不是设计一致性PASS。|
|B1-07|UNRESOLVED|晶环根节点余量与Collider接触口径需单独设计决定。|
|B1-08|PASS|新的纯Windows非开发构建成功，实际Editor exit0，111警告原样保留；Bee五服务关闭。|
|B1-09|PASS|新纯包无观测驱动；实际标题启动及进程正常退出，合成存档不变。不是菜单键鼠测试。|
|B1-10|PASS|1448产品输入仅三项授权变化、5用户文件不变、193纯包文件冻结；保护核验零FAIL。|
|B1-11|NOT_RUN|真实原生键鼠输入。|
|B1-12|NOT_RUN|独立人工体验及可读性。|
|B1-13|NOT_RUN|最终平衡。|
|B1-14|NOT_RUN|性能专项，无新校准CPU/GC/GPU结论。|
|B1-15|UNRESOLVED|历史构建输入、引擎及外部诊断发送开放项不在本批关闭。|

需求级合计：**9 PASS / 1 FAIL / 4 NOT_RUN / 2 UNRESOLVED**。本批包含确认但未授权修复的缺陷，不宣称整体全PASS。

原B独立保留：**18 PASS / 2 FAIL / 1 INCOMPLETE / 6 NOT_RUN / 2 UNRESOLVED**，不并入本表分母。原C02/C04仍FAIL，C05仍INCOMPLETE。

Editor、非开发观测Player原始断言汇总见 Evidence/layer-counts.json；旧版本复现、工具失败、纯包启动单独记录，不混为人工验收。完整索引见 [Evidence/INDEX.md](Evidence/INDEX.md)。
