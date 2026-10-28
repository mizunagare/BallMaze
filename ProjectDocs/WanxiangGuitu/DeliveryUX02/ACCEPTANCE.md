# UX-02 验收表

逐轮机器结果在Evidence/FINAL_SUMMARY.json，修复前与失败历史独立保留，不与最终通过相抵。

|条目|结果/层级|证据|
|---|---|---|
|开工SHA、四领域审计、保护文件|PASS，源码/哈希|AUDIT_AND_DESIGN；protected-final|
|普通、远程、精英、波次Boss、森林双Boss死亡动作结束隐藏|PASS，受控Play Mode|最终UX规则、对应entityId截图|
|死亡当帧停止碰撞/攻击，重复掉落不增加奖励或随机消费|PASS，受控|最终UX规则，保留根身份|
|已死恢复隐藏、重置重新显示|PASS，受控|最终UX规则|
|左右配方、分类/搜索/详情、空结果无旧制造动作|PASS，受控uGUI回调|最终UX规则、受控截图|
|营地仅仓库、混合供料、随身优先|PASS，真实事务/合成初始库存|材料核账与UX结果|
|29高级配方逐项研究/制造/消耗、重复解锁|PASS，受控真实事务|最终Extras与新进程恢复|
|不足/满包/保存前失败/发布后回调失败/重入|PASS，故障注入与真实提交|UX规则、原始日志|
|药水及普通容器营地原子提交，容器失败回滚|PASS，受控|UX规则；未引入新存档字段|
|当前/候选容量、格形、属性、旧容器去向|PASS，受控布局/预览|受控1280/1920截图、Preview不改状态|
|容器点击、旧按钮重复回调、装备后保存恢复|PASS，受控|UX规则；无新拖动装备实现|
|四武器时序/命中、双Boss经济/战斗、随机流及UI输入回归|PASS，分层规则|CombatBatchFinal与AffectedFinal；不合并为人工通过率|
|正常AI采集→结算→制造→再出征与三进程恢复|PASS，Editor正常AI|AffectedFinal/Normal-Gather的三阶段回执|
|最终非开发构建|PASS，BuildOptions.None|0错误94警告，所有警告保留|
|长时大量尸体/临时特效压力|NOT_RUN|本轮验证有限六类逐一死亡，不冒称长期压力|
|原生键鼠/原生U16/新发行包完整人工操作|NOT_RUN|没有独立获准试玩记录|
|独立人工可理解性及动态审美|NOT_RUN|受控截图不替代|
|完整性能预算|NOT_RUN|本轮不测量|
|旧C15、UNKNOWN、青色帧、Search、JobTempAlloc、旧Editor阻塞|UNRESOLVED|历史保留，无根因结论|

所有PASS只适用于明确层级。原始GameView青色截图不作为布局证据；受控RenderRequest另列。旧历史FAIL不回写。COMBAT02未实施。
