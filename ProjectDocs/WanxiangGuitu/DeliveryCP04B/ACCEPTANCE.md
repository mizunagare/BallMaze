# 分层验收

|项目|状态|依据|
|---|---|---|
|唯一产品修改CombatAim|PASS|2329项保护、Git差异；无场景/ProjectSettings提交|
|历史两项真实首次碰撞及正确Damage|PASS|Editor/Player各293项及events.jsonl|
|原38项与额外2相机墙|PASS|两层独立diagnosis与预测/碰撞/Damage核对|
|背向、近墙、双Collider|PASS|两层各6项；首阻挡无穿透、拒绝反向、同Owner不重复伤害|
|相机选择身份与预测一致性|PASS|每个Matrix/Wall/Boundary的原始Shot/Trace|
|24组历史合同追溯|PASS（有授权差异）|24 origin与22 direction不变；2近距direction改变，不伪称24方向全相同|
|四武器普攻/技能及取消|PASS|Editor293/Player293，沿用原断言，原2UR变为更严格首次Collision+Damage检查|
|已释放暂停、恢复、切武器、寿命、场景卸载|PASS|各10项lifecycle|
|真实死亡后清理已释放弹体|PASS|各4项death，实际敌弹扣血，无HP覆盖|
|非开发验收构建|PASS|0错198警告，含显式受控测试驱动|
|纯发行构建|PASS|0错96警告，单独PE检查无驱动与Editor引用|
|查询计数、CPU和并发负载采样|PASS（测量完成）|实测计数/Profiler/Stopwatch，不等于性能达标|
|逐Solve GC Alloc|NOT_RUN|正分配校准失败，不把0当无分配|
|隔离构建输入逐字节等同|UNRESOLVED|5项Unity配置写回差异，不影响源工作树保护结论|
|原生输入|NOT_RUN|没有物理键鼠验收|
|独立人工体验|NOT_RUN|无人试玩证据|

最终AssessmentDelivery：174 PASS、1 UNRESOLVED、3 NOT_RUN、0 FAIL，整体验收BLOCKED/2。另有旧失败/工具异常/首次无效GC读数，详见失败历史；没有删掉或覆盖。
