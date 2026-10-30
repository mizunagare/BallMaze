# GAMEPLAY-UX02 复跑说明

环境：Windows、Unity 6000.6.5f1，原依赖不变；本轮唯一有效根 `I:/WGCombat/GU02-1030-B`，首次失败A副本另保留。禁止将此目录或任何合成档当真实玩家进度。

## 准备

1. 记录远端/本地SHA、未提交五项SHA；调用原DeliveryUI01/Invoke-Rules.ps1的PrepareOnly，WorkProject与ArtifactsRoot必须互为独立目录，不能父子冲突。
2. 副本的Scene/ProjectSettings使用冻结Git原字节，用户覆盖层移入根外DeferredUserInputs；不更改主工程。测试目录必须GU02-前缀，进程冲突就停止该项，不关闭用户程序。
3. 只读资源审计：`Audit-Resources.py <repo> <output.json>`。原始音效为运行时合成；不存在可伪称已下载的录音资源。

## 有效时序测试

`Invoke-Editor.ps1 -Project <owned clone> -Output <new folder> -Graphics -NonBatch`

复用原Step与非激活测试桌面；GUXEditor复用UI01Before.Size创建GameView，Queue/Repaint，等待Saves.IsInitialized与实际第6帧后才建立夹具。默认方法GUXEditor.Run，180秒适配器期限，外层保留真实退出与超时；不得强杀。GUXCases是公开Strike/UseSkill/Damage驱动，不是原生输入或正常AI。没有改目标maxHP/Current，不用重置生命来制造通过。

- Before7/After2使用同一份执行夹具，前者CombatFeedback为基线原文，后者仅三行修复；核心115项同条件。
- AfterExpanded加入真实未命中/实体墙反例，119项，不伪装为之前就执行过。
- 剑/枪目标1.5m，法杖/弓命中对照6m；旧法杖1.5m侧置相机失败保留在Before6/After/AfterTrace。不同距离是不同条件，不据此宣称修复瞄准。
- 命令、时间、实际退出码/超时、执行源码及产品源码在各输出目录。Before2等即便OS exit0，无presentation回执仍不算业务成功。
- 四武器轨迹CSV列：weapon, skill, attackId, frame, time, lastReleaseFrame, phase, motion, poseTime, numberCount, targetHP。损失原float与文字在damage-events.jsonl；弹体from/to/真实接触/瞄准reason在projectile-events.jsonl。事件身份采用文件+行号，不虚构Damage观察未提供的攻击者。

## 降级与既有几何

MissingGlow只在已停止的隔离副本中暂移Resources/CombatFeedback/Glow.mat及meta，记录原SHA，运行同矩阵验证现有Shader fallback/ownsMaterial清理，finally原SHA恢复；主工程资产不动。不是把所有Shader/Prefab/音频设备缺失都宣称通过。

BossGeometry复用原B07ReadabilityRules.Run；6534数据采样及36HUD矩形不等于真实Boss战或人工识别。

## 非开发验收Player / 纯发行

- 将GUXCases从隔离Editor目录移入Assets/GUXAcceptanceOnly，与GUXPlayer一起构建；不要复制成两份同名类。调用原DeliveryEncounterAI01/Invoke-Check.ps1 -Method Build01Audit.Run，原正式构建方法Options=None。
- `Invoke-Runtime.ps1 -Build <acceptance Release> -Output <new folder>`：明确合成根+gux-owner.json+opt-in；实际Boot/Title后调用真实NewGame确认公开入口，等待初始化，再运行公开业务API夹具。无UnityEditor依赖，不注入最终存档/奖励。它不是原生点击，SuspendEntry后的退出不是完整退出保存验收。
- 纯发行前将整个AcceptanceOnly移出Assets，把共享Cases放回Editor；再次构建。`Inspect-Build.ps1 -BuildRoot <Release> -Output <json>`核验无GUX/旧驱动/UnityEditor；验收变体用ExpectAcceptance，必须实际含GUX驱动。
- 所有构建保留inputs.json、全部警告与PE/exe/UnityPlayer/核心程序集哈希。

## 汇总/发布

`Bind-Inputs.py <owned root> <repo>`、`Audit-Logs.py <owned root>`、`Summarize.py <owned root> <delivery folder>`、`Collect.py <owned root> <repo>`。只读核对来源/构建/用户文件，发布原始日志gzip与SHA清单，不发布缓存、构建二进制和用户覆盖层。

原生U16、真人可读性/音质/手感、正常AI冒险及完整性能不由这些脚本替代。逐帧文件IO有开销，未测量指标NOT_RUN。历史引擎异常不因exit0改成PASS；所有首次失败保留。
