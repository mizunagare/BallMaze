# CP04-B 交付：功能通过，整体验收BLOCKED

开始基准：`72db192a527bd256e2ba18cd7ab334d8334051da`。分支`fix/cp04-staff-near-aim`，不合并main。唯一产品改动CombatAim.cs；其余为独立文档目录下测试、报告、原始证据。

修复负投影侧置视差：仅允许相机已选中的前向敌人/资源，在实际枪口半径扫掠首先安全到达同一目标时汇聚；墙面/背向/受阻仍保留防倒射，cameraCollider身份保留。[合同](DESIGN.md)。

## 实际验证

- Editor四武器原矩阵293 PASS；非开发验收Player独立293 PASS。原w2-s0-near/w2-s1-near均有首次实际Collision及Damage，普攻33、技能60（目标HP上限导致技能实际扣60），与6m同装备对照一致。
- 两层各38项调查矩阵、2项真实相机墙、6项背向/近墙/多Collider扩展均执行并核对选择、预测与实际碰撞/伤害。允许的未命中保持未命中，不把这些结果算成“全部命中”。
- 每层10项已释放弹体暂停/恢复/切武器/寿命/真实场景卸载，以及4项真实敌弹致死/释放后清理通过。原未释放取消、四武器普攻/技能等仍由293项覆盖。
- 24组origin全部精确保持，22组direction精确保持；只有攻击11/14的Staff近距方向按授权改变，旧原始记录完整保留。
- 最终非开发验收构建0错198警告；纯发行构建0错96警告，BuildOptions.None。PE检查证明纯发行无CP04B/CP03Cases驱动及UnityEditor引用。全部警告、构建轮次保留。
- 174项证据/过程/语义核验PASS、0 FAIL；1 UNRESOLVED、3 NOT_RUN，最终分类BLOCKED/2，不把进程exit0等同验收通过。

## 不能宣称完成的部分

- 隔离构建副本5个配置文件被Unity写回，源产品和用户文件没变；1163项构建输入的逐字节等同性仍UNRESOLVED。[完整差异](BUILD_INPUTS.md)。
- 逐Solve线程分配计数在已知65536字节分配下仍返回0，GC Alloc NOT_RUN。Editor整帧GC可采样，不能替代逐Solve字节；非开发Player整帧GC也不可用。[测量与限制](PERFORMANCE.md)。
- 原生输入、独立人工手感/可理解性NOT_RUN。历史D3D12 UNKNOWN/C15、青色帧、Search/JobTempAlloc等开放项不关闭。

旧main及旧交付的两项UR不改写；本分支受控Editor/Player已通过对应真实命中检查，仍等待独立固定SHA审核。推送不等于审核通过。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [失败历史](FAILURE_HISTORY.md) · [证据](Evidence/INDEX.md)
