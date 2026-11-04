# CP06-A复跑与运行身份

工程外唯一测试根：`I:/WGCombat/CP06A-1104-A`。Unity6000.6.5f1及原依赖；不读取真实存档。基准来自397d53fe87ce5b6c490c86c63d59015de26a46af，当前用户工程与只读历史分支不参与测试写入。

## Editor

使用现有DeliveryEncounterAI01/Invoke-Check.ps1与其StartChild/FinishChild/NativeProbe独立桌面。将本目录Tests/*.cs.txt复制到隔离Project/Assets（CP6Editor进Editor/B06LocalChecks），只在隔离测试副本中编译。

```powershell
& $existingEntry -Project $project -Output $freshRoot -Method CP6Editor.Run -NonBatch
& $existingEntry -Project $project -Output $freshExtraRoot -Method CP6Editor.Extra -NonBatch
& $existingEntry -Project $project -Output $freshSaveRoot -Method CP6Editor.Save -NonBatch
```

CP6Probe先逐一重建真实训练实例，选择真实装备，等待原换装门槛；不写HP或注入Damage。AI禁用只用于受控固定碰撞场景，辅助目标用实际启用AI；另有真实AI致死回归。技能开始走UseSkill，命中来自原Melee/真实Projectile/新物理Field及Piercing。记录HealthObservation、真实释放、碰撞、配置及阶段截图。

前摇保存走GameEntry确认新游戏/正常森林出征/原子SaveProgress。独立进程恢复：将SaveEditorFinal/SeedPackage原样复制到新storageRoot/WanxiangGuitu/ForestRuins，并把expected.json复制到根；使用新OutputRunner和-StorageRoot该根再次CP6Editor.Save。expected.json是只读比较元数据，不是伪造进度文件，不改任何保存字段。

## 非开发测试Player

```powershell
& $existingEntry -Project $project -Output $freshBuildRoot -Method CP05Build.Run
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshPlayer -Mode training
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshExtra -Mode extra
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshSave -Mode save
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshResume -Mode resume -SeedPackage $freshSave/SeedPackage
```

Player在不活动桌面显示SW_SHOWNOACTIVATE，不切桌面、不抢焦点。样本由正式运行时业务API与真实Physics推进，是测试包，不冒充纯发行人工游戏。虚拟KeyboardState只验证真实Down/Held消费者，非物理键鼠。

旧回归复用CP05-C的CPCProbe/CPCFormal/CPCEditor，源码来自固定397提交，不重建框架；Invoke-LegacyRegression.ps1用相同包的-cp05-c受控入口。正式森林种子包为CP05-C真实保存产物的原样合成副本LegacySeedPackage。每层480工厂规则与真实死亡独立记录，生成规则对象不入背包或存档。

## 纯发行

移出全部CP6Probe/Expanded/Save/Extra、CPCProbe/Formal及CP6Editor/CPCEditor与meta到工程外ExecutedDriverSnapshot；再次使用CP05Build.Run。固定PRIVACY-A Release Profile/Development=false，验证实际Bee五字段false。用Tools/AssemblyAudit.ps1对比18类产品IL及排除测试类型、原生桥和UnityEditor引用。Invoke-PureSmoke.ps1只普通启动和WM_CLOSE收尾，实际exit0+日志；不能当键鼠或纯包战斗验收。

纯包本机：`I:/WGCombat/CP06A-1104-A/PureBuild/Release`。新建独立storage root，使用产品训练入口参数 `-cp05-training -wanxiang-storage-root <root>`；Esc释放鼠标选择技能，沿用当前Skill键释放；蓄势按住/松开。选择临时，不创建正式进度或给仓库奖励。原生/人工记录未执行，不预填结论。

## 对照与保护

```powershell
python Tools/Audit.py $runRoot $newAuditJson
python Tools/Analyse.py $runRoot $newAnalysisJson
```

Audit逐位置验证AdventureCombat10处允许接入和完整未变正文，不用宽泛删除字符串；其余2349保护清单只允许这个既有脚本变化。完整构建输入与119产品脚本匹配；保存原始构建摘要、警告、EXE/程序集/所有文件SHA。Tools/Publish.py只生成新证据发布目录，原始文本不改写，压缩/脱敏分别保留sourceSHA和publishedSHA。

脚本中隔离根/本机工具位置是本次固定环境；复跑者可明确替换为新受控位置，不能静默跳过所有权、进程冲突或内存保护。每次新目录，保留失败/退出/超时；不强杀。

Editor核心最后一次之后仅UI面板位置下移20px，旧脚本单列快照；最终UI已在ExtraEditorFinal/保存/旧回归/Player测试。纯发行包与测试包产品IL完全相同。所有原始尝试见FAILURE_HISTORY，历史黑帧、近距法杖、旧关闭问题不重定性。
