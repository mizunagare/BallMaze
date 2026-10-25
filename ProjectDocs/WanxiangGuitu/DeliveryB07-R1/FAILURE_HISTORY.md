# B07-R1 失败与尝试历史

最终结果必须来自新的完整All；本表不合并为一轮通过。所有状态来自各自results.json。

| 尝试 | 实际方法结果 | 解释 |
|---|---|---|
| [Before](Evidence/Attempts/Before/results.json) | B07ReadabilityProbe.Run: FAIL (exit 1, timeout False) | 实施前契约探针，预期失败，80个原产品脚本与91c6664核对；新探针不属于旧提交。 |
| [Directed1](Evidence/Attempts/Directed1/results.json) | B07ReadabilityProbe.Run: PASS (exit 0, timeout False)；B07ReadabilityRules.Run: PASS (exit 0, timeout False)；B07ReadabilityVisual.Run: FAIL (exit 1, timeout False) | 规则通过，截图夹具初始化竞态。 |
| [Directed2](Evidence/Attempts/Directed2/results.json) | B07ReadabilityProbe.Run: PASS (exit 0, timeout False)；B07ReadabilityRules.Run: PASS (exit 0, timeout False)；B07ReadabilityVisual.Run: FAIL (exit 1, timeout False) | 增加诊断，发现Boss引用被默认初始化重建销毁。原工程后续复用，不冒充原源码冻结。 |
| [Directed3](Evidence/Attempts/Directed3/results.json) | B07ReadabilityProbe.Run: PASS (exit 0, timeout False)；B07ReadabilityRules.Run: PASS (exit 0, timeout False)；B07ReadabilityVisual.Run: PASS (exit 0, timeout False) | 等待初始化后26张断言通过；代理查看截图发现青色帧，另设像素检查失败，不把脚本exit0当视觉验收，也不称为人工试玩。 |
| [Camera1](Evidence/Attempts/Camera1/results.json) | B07ReadabilityVisual.Diagnose: FAIL (exit 1, timeout False) | 诊断入口误入batch，等待不会执行的默认存档初始化，脚本deadline失败。 |
| [Camera2](Evidence/Attempts/Camera2/results.json) | B07ReadabilityVisual.Diagnose: PASS (exit 0, timeout False) | 受控关闭预警/隐藏角色，青色仍在；仅排除这些对象，未确定根因。原工程后续复用。 |
| [Camera3](Evidence/Attempts/Camera3/results.json) | B07ReadabilityVisual.Diagnose: FAIL (exit None, timeout False) | 复用Step时未设置dotnet路径，启动前失败，没有Unity退出码。 |
| [Camera4](Evidence/Attempts/Camera4/results.json) | B07ReadabilityVisual.Diagnose: FAIL (exit 1, timeout False) | 诊断日志对缺少Renderer的碰撞体使用Unity对象?.，日志夹具抛MissingComponentException。 |
| [Camera5](Evidence/Attempts/Camera5/results.json) | B07ReadabilityVisual.Diagnose: PASS (exit 0, timeout False) | 修复日志，观察到drawGizmos本来False，稍后多帧画面正常；不能推导Gizmos为原因。 |
| [VisualReady](Evidence/Attempts/VisualReady/results.json) | B07ReadabilityVisual.Run: PASS (exit 0, timeout False) | 增加稳定渲染帧、编译状态日志、原时长重新前摇及固定青色像素断言，38张受控检查通过；非干净重导入。 |
| [FinalDirected](Evidence/Attempts/FinalDirected/results.json) | B07ReadabilityVisual.Run: PASS (exit 0, timeout False) | 当前产品增量同步到已结束测试工程，38张及暂停/受击/停用/重建通过；不称干净副本或正常AI。 |

青色像素回归首次FAIL：[check](Evidence/Checks/cyan-before.json)，原图纯青色占比约73.58%，固定阈值40%；后续不放宽阈值。

首次证据检查FAIL来自Before截图清单相对路径重复了Before层级；图片未变化，原清单screens-before-fix.json及Checks/attempts.json保留。修正清单路径后Checks/attempts2.json通过。

复用诊断脚本首次在创建目录前因D:/与D:\路径表示不同触发owner保护，随后按GetFullPath比较；该次仅工具返回错误，没有伪造测试结果文件。外层增量脚本exit0不保证内部Unity成功，内层失败在results.json中保留。

部分诊断复用了已结束的隔离工程，原始日志保留；没有逐字节冻结的旧源码明确标注，不使用后来的工程目录冒充原始输入。Directed1/3原副本和Before来源另存快照。
最终All会重新准备新工程；该轮不得继承上述任何PASS。

## 正常聚怪遗漏与后续淡化

- [All1](Evidence/Attempts/All1/results.json)：完整执行，协调器exit0，118 PASS / 2预期FAIL / 27 NOT_RUN / 2 UNRESOLVED；15个正常AI和12个Player进程。输入adb7e9688443de15ba95771756afb34e82c2d863的83产品脚本、57注入测试、45执行驱动分别匹配。随后实际查看Normal-Land聚怪照片发现主角仍被不透明Boss身体遮住，[单独视觉检查FAIL](Evidence/Attempts/All1/Readability/b07r1-visual-review.json)保留，不改原编排结果，不将其当最终验收通过。
- [OcclusionBefore](Evidence/Attempts/OcclusionBefore/results.json)：新相机遮挡契约探针缺少CameraActorFade而exit1；实际正常战斗照片已确认问题。
- [OcclusionAfter](Evidence/Attempts/OcclusionAfter/results.json)：新组件把MaterialPropertyBlock放在实例字段初始化，Unity禁止该时机的CreateImpl，后续Refresh收到空块。是新增组件缺陷；最小修复移入Awake，不修改原产品存档或退出生命周期。
- [OcclusionAfter2](Evidence/Attempts/OcclusionAfter2/results.json)：身体淡化/恢复与碰撞、HP、随机和Profile检查通过；查看照片发现枝冠仍不透明，因此没有结束交付。
- [CrownBefore](Evidence/Attempts/CrownBefore/results.json)：扩大Renderer断言后失败“Boss body or crown still opaque”；后续断言只检查实际启用Renderer，并覆盖独立枝冠及启用的原始外形，不将攻击预警一起淡化。
- [OcclusionFinal](Evidence/Attempts/OcclusionFinal/results.json)：38项之外的独立受控相机对照通过；身体/枝冠淡化，镜头转开恢复，停用清空所有自有克隆；原HP、控制器、随机、Profile、时间倍率不变。它不是正常AI胜利。

新最终完整All必须基于dc55ece3c3d880090f562e120ebbc472a9f3eae4重新执行，不能继承All1的任何PASS。
