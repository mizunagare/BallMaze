# CP03 复跑

固定制定9fbe；实际输入c7efb644f38387f7588f4bd58fe5697e4ecdd9c4。唯一根I:/WGCombat/CP03-1031-A，全部合成数据；禁止指向真实存档。先记录本地/远端/用户五文件SHA，原DeliveryUI01/Invoke-Rules.ps1 PrepareOnly复制到工程外。WorkProject与ArtifactsRoot为独立目录；复制场景/设置用冻结Git原字节，用户覆盖层另留存，Recovery不进测试输入。

## 入口

- Audit-Resources.py：静态资源/调用点，本轮BASELINE_RESOURCE_AUDIT.json。
- Invoke-Editor.ps1 -Project <owned clone> -Output <new folder> -Graphics -NonBatch：默认CP03Editor.Run。原Step、独立非激活桌面、原NativeProbe；CP03Editor复用UI01Before.Size/Queue/Repaint，等待Saves初始化及至少6帧；480秒有界适配器，不强杀。
- 同入口 -Method CP03Editor.Visual：8个实际动作、16张原始start/release截图，固定1280×720；旧产品负例版本exit1仍保留，不因截图文件存在忽略断言失败。
- Before2为修正真实宽度/寿命/长度后的有效基线；After为相同229项。Extended/Final/Final2为逐步新增生命周期/装备色/音色预占检查，不继承旧PASS。

全部业务由原Strike/UseSkill、WeaponHit、Projectile/CombatHealth产生。夹具关闭的是AI/玩家输入移动脚本，目标Collider保持开启；没有直接Damage/改HP/奖励注入。普通/精英/Boss死亡真实攻击循环不重置其HP，冷却正常等待。玩家死亡经原伤害敌弹真实碰撞，仅用于取消合同，不冒称正常AI战斗。代际池与增量场景资源探针单列，不是命中证据。

固定120 capture-fps仅在测试进程；原Animation.LateUpdate不修改。timeline/events缓冲后落盘；SCHEMA见EVIDENCE_SCHEMA.md，Damage观察没有攻击者，不据上下文ID做武器平衡归因。

## 非开发与纯发行

1. 仅隔离副本将CP03Cases/CP03Player放Assets/CP03AcceptanceOnly，Editor共享类不可重复。原DeliveryEncounterAI01/Invoke-Check.ps1 -Method Build01Audit.Run使用原Options=None入口，完整输入/警告保留。
2. Invoke-Runtime.ps1 -Build <acceptance Release> -Output <new root> -FixtureSave <CP03 owned Final2/Game/ForestRuins/save.json>。源是Editor真实生成的初始合成检查点，文件原样复制到新根WanxiangGuitu/ForestRuins；SHA回执，不编辑payload。正常Boot/Title、受控Continue恢复同seed418，不是原生点击。共享Cases非Editor分支只使用真实恢复Run，禁用自动保存后进行受控矩阵；SuspendEntry后自退出不冒充完整退出保存验收。
3. 最终AcceptanceBuild2/Runtime2/PureBuild2绑定最终源；无2后缀为保留中间变体。
4. 纯发行前整个AcceptanceOnly移出Assets，把共享Cases放回Editor，再构建；Inspect-Build.ps1核验无CP03/旧驱动/UnityEditor。验收变体用ExpectAcceptance，必须有驱动。产品仓库没有运行时验收驱动。

## 审核/发布

Audit-Locked.py比较冻结源码，AdventureCombat只允许4类表现调用差异；检查13份禁止域文件和动画采样循环；24配对实际Spawn位置/方向逐项比较（新增暂停箭另列）。Bind-Inputs.py核对最终两个全构建输入/9源码/54资源/用户五文件。中间构建可与最终不同，不能伪称一致。

Summarize.py生成独立集合/进程CSV/原身份；Audit-Logs.py单列全部异常上下文；Collect.py发布原始gzip日志、源码与SHA，不发布缓存、用户覆盖层和构建二进制；Verify-Publication.py核验发布字节、链接、暂存范围与保护。所有输出新建目录，不覆盖失败。

人工/原生/观感/音质/最终打击感、全部品质等级与Profiler开销NOT_RUN。没有零值替代不可采集指标，没有性能/完整平衡结论。源码/资源/自动化/非开发/纯发行/原生/人工不得混为一谈。
