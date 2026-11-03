# CP05-B 可玩动作辅助原型

起点 `c6473b1832a545a5d348e26220fafa73cca741ac`；设计参考 `0f62a5f18b7d3e895ba8fd3693cc944f0f34048f`。独立分支 `prototype/cp05-action-combat-playable`，不合并 main。B1检查点为 `6b2bda265ec95e1a8a9efb3316320fbb342a61f4`，B2为 `442fa8a2e341b3fcdd9e4b9246d637f935896f7e`；最终提交见本报告所在提交及交付消息。最终产品与运行输入对应见 [source-parity](Evidence/B3/source-parity.json)。

当前交付是可运行原型及分层证据，**整体验收 INCOMPLETE**。最终 Editor 与非开发 API Player 各157 PASS、0 FAIL、1 NOT_RUN；这不是人工体验通过。独立桌面 Player 截帧全黑，画面正确性 UNRESOLVED；完整原生操作、持续战斗录像和人工试玩没有执行。

## 实际实现

- **B1 镜头**：自由肩后横移、横向/后向体积避障、连续运动安全检查、近距角色淡化和恢复。玩家仍掌控 yaw/pitch；不增加自动镜头旋转。异常位置跳变会重置上一帧避障缓存。按钮保留居中构图对照；其共享新增避障和淡化，**不是整个历史相机算法的逐字节对照**。
- **B2 远程**：TargetAssist 提供意图，按准星偏差、距离、夹角、连续性评分；0.1秒扫描候选、切换差值/等待时间滞回，主动转镜头可自然换目标。相机视线和真实枪口体积路径分别校验。释放时重新求解；非法/无候选保留原 CombatAim 自由解。不会调用 Damage，不移动敌人，已发射弹体不追踪目标、不因切武器被清除。
- **B3 近战**：剑30°、枪20°单次启动累计转角上限，角速度分别180°/秒、120°/秒；启动末段停止追踪。每帧共享预算，移动中不辅助转身，不添加位移；释放时使用冻结方向，沿原 MeleeGeometry、Sight、品质分支及追加段执行真实命中。参数是原型初值，尚未证明手感或平衡。
- **训练入口**：显式 `-cp05-training` 且必需隔离存储根；独立运行时场景、原角色与敌人派生资源、两个原AI移动敌人、石块、墙体、四武器切换和原/辅助按钮。重开销毁并重建场景，不直接覆盖HP或奖励。没有创建正式 Profile、Run、存档或结算。正常启动仍走原标题界面，训练不替代森林冒险验收。

修改既有产品文件只有 `OrbitCamera.cs`、`CameraActorFade.cs`、`AdventureCombat.cs`；新增 TargetAssist、CombatAssistOptions、CP05Training、CP05Build、两个派生训练Prefab及meta。没有引入新美术或依赖。完整变化以相对起点的 Git diff 为准。

## 构建与运行

本机保留三个独立非开发包：

|阶段|本机路径（I:/WGCombat/CP05B-1103-A 下）|纯包构建|受控验证|
|---|---|---|---|
|B1|B1/Build4/Release|0错误/96警告|Editor2 8 PASS/1 NOT_RUN；Smoke4启动和普通关闭|
|B2|B2/ReleaseBuild/Release|0错误/96警告|Editor1、Player2各99 PASS/1 NOT_RUN|
|B3|B3/ReleaseBuild/Release|0错误/96警告|EditorFinal、PlayerFinal各157 PASS/1 NOT_RUN|

纯包的 SmokeRelease 日志有 READY，普通 WM_CLOSE 后实际exit0；这仅证明受控启动/关闭，不是原生输入测试。含CP05Probe的 FinalTestBuild 是另一份非开发验收包。八类关键产品类型在两包的 IL 相同，纯包 Assembly-CSharp 无本批驱动及 UnityEditor 引用：[程序集核验](Evidence/B3/assembly-audit.json)。纯包使用保留的 PRIVACY-A WindowsRelease Profile，Development=false，Bee五服务false；[marker](Evidence/B3/release-marker.json)、[Bee](Evidence/B3/bee.json)、[全部文件哈希](Evidence/B3/release-files.json)。可执行SHA256：`001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`。

## 真实范围与限制

实际测试调用原 Strike/UseSkill、真实Spawn/飞行/首次碰撞和健康变化；墙首撞、自由瞄准、暂停弹体、切武器后继续飞行、失效目标、滞回、多Collider去重、真实AI移动及近战冻结方向分别有原始轨迹。测试建立合成对象/相机位置，通过受控API驱动，未模拟为物理键鼠。完整历史24组弹道及CP04全矩阵、正式森林完整冒险/结算/恢复没有在本批重新执行，NOT_RUN，不能继承旧PASS。

Player截图缺口见 [Capture audit](Evidence/B3/capture-audit.json)：B2 Player2十张、B3 PlayerFinal七十一张全黑；相应 Editor 帧正常。尚不能确认是独立桌面呈现还是其他渲染原因。保留原图，不用Editor结果替代Player可见性。对照GIF来自 Editor API短截帧序列，无声音、无人工输入、非完整持续战斗录屏，见 [Comparison](Evidence/B3/ComparisonEditor/manifest.json)。

[性能](PERFORMANCE.md)记录可靠Editor原生Profiler分配、原始CPU观测和Player无效GC计数；没有整体性能通过或零分配结论。UI-01 D3D12 UNKNOWN、历史青色帧/关闭根因继续UNRESOLVED；原生U16、人工可理解性/最终打击感继续NOT_RUN。

2,334项开工保护记录复核，仅三份允许修改的既有产品脚本改变；用户工程记录全部未变。CombatAim SHA256保持 `9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a`；原隐私Profile/构建保护、场景、Prefab、ProjectSettings、依赖、AI、经济、RNG、v9存档源码保持原值：[保护审计](Evidence/B3/protection-final.json)。不访问真实存档。

所有失败见 [FAILURE_HISTORY](FAILURE_HISTORY.md)，验收见 [ACCEPTANCE](ACCEPTANCE.md)，复跑见 [TESTING](TESTING.md)，原始证据见 [INDEX](Evidence/INDEX.md)。推送不代表独立审核通过；本批交付后暂停。
