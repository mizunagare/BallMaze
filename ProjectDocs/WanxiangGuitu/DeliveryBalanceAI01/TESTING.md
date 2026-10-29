# 复跑与证据口径

Unity 6000.6.5f1；依赖不变。使用现有 DeliveryUI01 PrepareOnly / Step / Invoke-NormalAI / Build01Audit，新增文件仅是本批负例、被动观测和输出适配，不重建测试框架。

## 安全入口

本轮拥有者：`I:/WGCombat/BAL01-1029-A/owner.json`；隔离工程 `P/Project`。所有 StorageRoot 均在这个工程外的独立子目录，startup参数与环境变量一致。启动器检查占用、提交内存、私有测试桌面和超时；不激活用户桌面，不发物理Esc、不强杀、不关闭用户程序。旧工程/用户文件只读。再次运行必须新建唯一根，不能覆盖本轮。

准备步骤沿用 `DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly`；已安装夹具与方法计划见 Evidence/Prepare。首次准备命令未单独生成进程回执，不虚构该回执；各实际验证进程均有完整command/exit记录。仅复制已退出的隔离工程 Library 缓存作为加速，不上传 Library。保留上一批已审查的 B07RulesStable 初始化顺序；不得复制旧版夹具覆盖它。

```powershell
# 在仓库根执行，替换为新建且有 owner.json 的根/工程。
$testRoot = 'I:/WGCombat/BAL01-<unique>'
$project = "$testRoot/P/Project"
$check = './ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/Invoke-Check.ps1'
pwsh -NoProfile -File $check -Project $project -Output "$testRoot/Before" -Method BAL01Baseline.Run -NoGraphics
pwsh -NoProfile -File $check -Project $project -Output "$testRoot/Rules" -StorageRoot "$testRoot/Compatibility" -Method BAL01Rules.Run -NoGraphics
pwsh -NoProfile -File $check -Project $project -Output "$testRoot/RulesResume" -StorageRoot "$testRoot/Compatibility" -Method BAL01Rules.Resume -NoGraphics
```

第二条前提为新产品源码已显式复制到**闲置的隔离工程**，不能据此覆盖源工程的场景/设置。

## 严格配对与只读观测

`Stage-Observation.py repo root before/after/clean` 校验拥有者与无活跃Editor，只在隔离副本还原5个明确源码；before来源固定开工SHA，不对仓库reset。`Instrument.py repo project fresh-output` 保存每个原始/观测源码和SHA，包裹相同的 Damage / GainExperience 调用各一次；额外读取状态并记事件，不注入奖励、不改结果。测试 BAL01Trace 只存在隔离工程，正式构建前移动到拥有根的 DeferredObservation；Matrix测试也一并移出（它依赖观测组件）。

同样的Matrix模板必须各运行一次before和after，方法 `BAL01Matrix.Run -NoGraphics`，输出目录不同。最新模板覆盖普通与Boss的正确/错误时机闪避：从实际前摇开始即翻滚是WrongDodge，剩余≤.18秒时才翻滚是CorrectDodge；不是保证每次成功躲避的作弊模式。Boss必须读取ForestBossBrain.State，不能误用普通敌WindingUp。

固定种子418/419/420、每种3个真实独立出征Run。每Run6主敌组×2策略，共108行/版本：

| rep | 角色/防御 | 策略 |
|---|---|---|
|0|等级1、基础白剑、HP100、防御0、药水2|原地攻击 / 正确闪避|
|1|等级5、Strength2/IronSkin1/Vitality1、HP125、防御2、药水2|走位 / 错时闪避|
|2|同等级技能+实际穿戴紫甲、HP125、防御19.2、药水2|原地攻击 / 被夹击|

主敌组为近战/远程/精英/角卫/潮灵/混合；Surrounded在主敌外加2个现有敌人，Mixed本身为近战+远程+精英。因此按主敌组汇总不能当成全部单敌样本。

实际AI启用、真实Strike/Dodge/移动/治疗/掉落/XP，只有初始场地、装备、等级和状态重置为夹具控制；没有冻结全部敌人或直接写胜利。Flow关闭仅避免受控反复重置污染真实Boss永久回执，此时随机取自legacy全局流。每样本按 `seed*10000+rep*1000+kindIndex*100+policyId` 固定该流；这是夹具输入，不改产品随机合同。Run-owned随机流由独立B3、真实保存/恢复及正常AI验证。

每样本预热2.12秒（目标暂空，消除ResetEnemy原.8秒武装延迟），随后6秒**活动时间**。未杀完记 `WINDOW_END_CENSORED`、TTK=-1，不当作胜利/0秒击杀，也不是编排器超时。条件控制器相同，不宣称完全相同的物理按键帧。完整布局JSON、实际Run/Profile/种子/初始字段、随机状态、来源XP和事件时间均留存；Unity坐标显示字符串有舍入，不冒充逐位物理快照。初始配置固定，窗口内真实升级与选择继续生效并记录finalRanks，所以是“AI+曲线的组合改动”对照，不能将差异全部因果归于某一AI改动。

原准备脚本复制工作区，包括用户未提交场景的只读副本。Before/After及配对均用同一开工SHA256场景，未提交该场景。输入绑定识别出它不同于Git HEAD后保留初次FAIL，再仅在隔离工程里保存副本、写入开工提交的ForestRuins与ProjectSettings，并移走复制的_Recovery。`TrackedReplay/RulesBaseline`、`TrackedFinal`正常AI三进程与发行构建是额外的固定提交场景验证；二者不能混淆。原用户文件始终不变。

```powershell
python -B ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/Stage-Observation.py <repo> <root> before
python -B ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/Instrument.py <repo> <project> <fresh-input-folder>
pwsh -NoProfile -File $check -Project $project -Output <fresh-before-output> -Method BAL01Matrix.Run -NoGraphics
# 闲置后以after重复，使用新的输入和结果目录；不可覆盖before。
python -B ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/Summarize-Matrix.py <root> <fresh-summary> <before-folder-name> <after-folder-name>
python -B ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/Stage-Observation.py <repo> <root> clean
```

## 分层最终检查

`Invoke-Final.ps1` 按顺序执行旧UX02、品质/几何、范围、时序、Boss经济、R1完整恢复、输入、B3随机流、B07四进程、Gather正常AI三进程和Build01Audit。失败后继续无依赖项目，依赖失败则NOT_RUN；汇总退出1不能改成0。

UX02Checks包含Camera.SubmitRenderRequest：**不能加 -nographics**。本轮首次错误启动的原生失败保留；当前入口明确为它保留图形设备，定向更正后通过。BAL01Visual同样需要图形设备，图像是实际运行相机的受控渲染请求，非原生UI和人工可读性。

Build01Audit复用正式 WanxiangBuild.Build，BuildOptions.None。记录全部96警告，不靠过滤/隐藏错误减少计数。`Inspect-Build.ps1` 检查PE类型/引用，观测驱动与UnityEditor不能出现在发行DLL；源码/构建输入另外逐文件绑定。

## 指标

逐行CSV包含TTK、censor状态、HP损失、治疗/翻滚、实际出招/释放/正实伤动作数、命中率、升级数/时点与XP来源。命中率=窗口内造成正实伤的已释放动作数/释放动作数；无释放则-1，不填成0%高闪避。未命中包括走位、墙阻挡、未到达/窗口截断，不能都叫成功翻滚。每个已命中动作可以有多次接触，事件与动作计数分开。

汇总保留样本量、范围、标准差、只对杀完样本计算的TTK均值及所有删失样本；不以选择性完成均值证明某类更快。首次失败、环境NOT_RUN、错误工具启动及输入修订单列。独立玩家/原生U16/最终平衡/完整性能未执行，不继承历史PASS。
