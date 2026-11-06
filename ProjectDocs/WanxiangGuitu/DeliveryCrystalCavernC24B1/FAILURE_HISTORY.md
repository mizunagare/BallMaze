# 失败与开放项（追加记录）

1. 原B不修改：18 PASS / 2 FAIL / 1 INCOMPLETE / 6 NOT_RUN / 2 UNRESOLVED。C02、C04原FAIL，C05半血扇扫证据缺口INCOMPLETE；未改容差、未再采样。
2. BeforeNotice1复现提前显示首奖成功；BeforeNames1Run复现C24上下名称不一致。捕获脚本PASS表示成功复现，不代表旧行为正确。
3. Windows tar展开参考产品时部分Unicode路径失败，保留 `I:/WGCombat/C24B1-1107-A/ReferenceProject`；改用Python UTF-8及显式LFS解析到新的ReferenceProject2，不使用残缺参考。原tar保留，reference-inputs.json记录实际输入。
4. ReferenceForest1第一次采集使用Evaluate原顺序，不能充当Ranked排序证据；保留全部输出。ReferenceForest2与其他两端运行使用真实Ranked，工具源码归档。
5. ScoreComparison1：8 PASS / 27 FAIL，评分字段全部一致，失败来自无序快照数组按下标比较。ScoreComparison2以稳定entityId关联同批输入，35 PASS；空ID及重复ID拒绝，不改值／容差，不删除旧FAIL。
6. Editor-b1-first-before-A1：误用Windows PowerShell5.1启动旧框架，StartChild返回空导致调用失败，Unity未启动，无业务结果。PureTitle1同因框架缺少Path.GetRelativePath启动前失败。保留不完整目录；改用PowerShell7，新目录A2/PureTitle2，非覆盖重试。
7. 一次只读Python统计因默认GBK读取UTF-8失败，之后显式UTF-8；一次rg Windows通配符路径不被接受。均无产品副作用，非测试PASS。
8. 新发行构建111警告，完整Unity.log和BuildReport摘要保留。JobTempAlloc、历史引擎、构建输入等同性、外部发送路径未在本批关闭；不从成功构建推导这些问题解决。
9. 新Boss路线收益误计／漏计确认为FAIL，需另批授权修改只读投影。本批未改RouteScoring、真实奖励或随机流。
10. 晶环根节点安全侧但Collider相交的设计口径UNRESOLVED；实际数据已记录，不调整伤害、半径或断言。原生输入、人工体验、最终平衡与未测性能NOT_RUN。

本轮工具失败未强杀进程、未关闭用户程序、未操作真实存档。
