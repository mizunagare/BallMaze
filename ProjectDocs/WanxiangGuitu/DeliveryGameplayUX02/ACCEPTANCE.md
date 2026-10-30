# GAMEPLAY-UX02 验收

| TASK §6 | 本轮技术状态 | 证据与严格边界 |
|---|---|---|
| 1 四武器普攻/技能 | PASS（受控） | 各8动作接受/片段选择/真实释放/动作结束与真实Damage，TIMELINES；未验收观感 |
| 2 命中/未命中/遮挡/取消/暂停 | PASS（有限受控） | AfterExpanded/Runtime；实体墙实际拦截，取消无假Hit，暂停计时；非所有取消组合 |
| 3 实际Damage与数字 | PASS（受控） | 实际before-after、致死小数与<0.01、重复Dead拒绝；声音限流不是每事件都另开声道 |
| 4 玩家/普通/远程/精英/Boss/森林双Boss | PASS（受控Damage/姿态） | 真实Damage与死亡Motion；禁用AI夹具，不是正常AI胜利或完整死亡掉落流程 |
| 5 Boss预警几何 | PASS（源码+数据+Show） | 森林六招6534共享几何样本/真实Show/无Collider；普通Boss源码核对；完整实际攻击矩阵NOT_RUN |
| 6 隐藏/禁用/暂停/销毁 | PASS（有限生命周期） | Hide/Disable/Reset/生成clip、owned/shared材质；全部场景重建/目标取消排列NOT_RUN |
| 7 音效资源/通道 | PASS（结构/生命周期有限项） | 7真实合成clip、10声道、衰减配置、停止/销毁；音频设备声学测量、全缺资源组合NOT_RUN |
| 8 特效/Material | PASS（有限受控） | 24池上限、32数字、缺Glow真实fallback与所有权；资源恢复SHA一致 |
| 9 镜头震动 | PASS（有限受控） | 真实Damage触发Shake、暂停冻结、Reset清零；强度舒适度NOT_RUN |
| 10 非开发/发行边界 | PASS（分层技术） | Runtime119断言、exit0；纯发行PE无驱动与Editor引用；原生键鼠NOT_RUN |

## 不关闭

- 近距侧置相机法杖未命中样本保留；6m成功不构成对该体验问题的修复/验收。需独立范围评估，当前不改瞄准业务。
- 原生U16、独立人工试玩、可读性/舒适度/趣味/最终打击感：NOT_RUN。
- 正常AI冒险、本批完整性能与观测开销基准、全部卸载/恢复组合：NOT_RUN。
- UNKNOWN/C15/青色帧/Search/JobTempAlloc：UNRESOLVED，旧FAIL不变。

原始失败、各次尝试、构建警告与分层状态见SUMMARY/FAILURE_HISTORY/Evidence。有限技术PASS不代表所有体验验收完成或独立审核通过。
