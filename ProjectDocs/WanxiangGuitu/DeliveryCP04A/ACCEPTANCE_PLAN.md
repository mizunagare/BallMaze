# 调查验收及后续修复验证计划

|项目|状态|证据|
|---|---|---|
|原w2-s0/1-near重现|已复现|Historical/presentation、aim-diagnosis、events|
|固定样本几何与真实发射因果链|已定位/已验证|Analysis/analysis、Matrix/diagnosis|
|四距离、四相机、两动作|已执行|38项矩阵；其中无伤害结果完整保留|
|枪口前墙实际阻挡|已验证|Matrix muzzle-wall；首撞墙、目标零伤害|
|相机墙候选首次摆放|未命中预期遮挡|Matrix camera-wall，原结果不覆盖|
|相机墙补充真实命中|已验证|CameraWall；2项真实Raycast墙命中|
|24组历史发射合同|已验证|paired-24：24/24精确相同|
|产品与用户保护|已验证|protected-after、product-input-binding|
|产品修复|未执行/等待授权|FIX_PROPOSAL.md|
|两项历史问题关闭|未执行；仍UNRESOLVED|Historical整体BLOCKED/2|
|正式Player/原生操作/人工体验/性能|NOT_RUN|本批受控Editor调查不替代|

已执行分析一致性6 PASS，均为数据/过程完整性断言，不是武器命中修复或完整回归通过。历史291PASS/2UR独立保留。

## 授权修复后的最低配对计划（尚未执行）

1. 固定原seed418、目标CharacterController、1.5m、侧置Camera、同装备和120Hz模拟，逐帧真实采样骨骼Muzzle、Solve、Spawn、Sweep与Damage。
2. 保留本轮0.35/1.5/6/20m、左右/中/Orbit；补充低矮资源、身体背后/目标表面边界、枪口内嵌、近裁剪与墙、移动镜头；不能靠关闭Collider或改距离通过。
3. 四武器及品质分支/多箭，核对24组合同，每次差异明确归因；未授权数值不动。
4. 暂停恢复、切武器、死亡、场景卸载；确保真实弹体生命周期及唯一命中不回归。
5. Editor、隔离非开发Player、正式发行、原生输入和人工观感分层记录；不能互相替代。受影响存档/随机流只读合同回归。
6. 完整保存首次失败、超时、实际进程退出码及新语义回执。推送修复独立分支后等待复审。
