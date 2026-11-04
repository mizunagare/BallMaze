# CP05-C复跑

Unity6000.6.5f1及现有依赖；独立根 `I:/WGCombat/CP05C-1104-A`。测试源码仅在本目录Tests，复制到新隔离工程，不放进用户Assets。用户主工程及真实存档不参与验证。

## 构造与入口

从固定基准冷复制Assets/Packages/ProjectSettings（不复制Library缓存），保留owner.json。先放入本目录CPCProbe.cs/CPCFormal.cs到隔离Assets根；CPCEditor.cs放Assets/CombatPrototype/Editor/B06LocalChecks。已有B06依赖由现有Invoke-Check补入。基准运行需用BaselineProduct中的原产品源，修复运行使用本提交产品源；每次新输出目录，禁止覆盖旧运行。

复用 `H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1`：

```powershell
& $existingEntry -Project $isolatedProject -Output $freshOutput -Method CPCEditor.Run -NonBatch
& $existingEntry -Project $isolatedProject -Output $freshRunnerOutput -StorageRoot $seededRoot -Method CPCEditor.Formal -NonBatch
& $existingEntry -Project $isolatedProject -Output $freshBuildOutput -Method CP05Build.Run
```

正式配对的seededRoot中WanxiangGuitu/ForestRuins只原样复制BeforeFormal/SeedPackage（真实ConfirmNew/Depart/SaveProgress创建）；不修改JSON字段。训练带存档canary也复制相同文件，并预先记录相对路径=SHA256的按ordinal排序ledger到canary-before.txt。该ledger只比字节，不重写存档。

```powershell
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshPlayerOutput -Mode training -SeedPackage $genuineCheckpoint
& ./Invoke-Player.ps1 -Build $testRelease -Output $freshFormalOutput -Mode formal -SeedPackage $genuineCheckpoint
```

测试用真实Strike/AI攻击造成死亡，无Damage注入。规则矩阵独立替换合成Run随机状态作纯工厂输入，finally恢复原对象，不保存或领取规则产物。固定合成检查点和实际死亡身份独立配对。暂停走真实Inventory.SetOpen；重开走真实UI回调，故障走CreateScene真实拒绝。

## 纯发行

移出CPCProbe/CPCFormal/CPCEditor及meta，保留执行副本在工程外。再次CP05Build.Run，经固定WindowsRelease Profile、Development=false构建；核验实际Bee五项false。执行Tools/AssemblyAudit.ps1，确认无驱动、无测试原生桥、无UnityEditor引用，12类产品IL与测试包一致。Invoke-PureSmoke.ps1只普通启动和WM_CLOSE，不能当人工或原生键鼠验收。

## 独立门禁

```powershell
python Tools/Audit.py $freshProtectionJson
python Tools/AuditSelfTest.py $freshSelfTestJson
python Tools/Compare.py $runRoot $freshPairedJson
```

Audit.py当前固定审核根和2347项保护清单，需要复跑者提供同样布局或明确改为自己新建的等价路径，不能静默跳过。所有保护文件前后哈希及116项产品编译输入匹配；输出纯构建前后输入清单、release-files全文件SHA、Assembly-CSharp SHA。三套构建摘要/完整警告及每次命令、NativeProbe退出回执均保留。进程exit0、非空语义回执、无FAIL及无非预期空引用共同判断。

测试Player在独立不活动桌面显示（SW_SHOWNOACTIVATE），不切桌面、不抢焦点；Editor隐藏运行，不据截图推导原生操作。仅对自有编译失败窗口使用精确Quit，无强杀。所有编译/夹具/工具失败另起目录保留，NOT_RUN不当PASS。

## 本机纯包试玩

包位于 `I:/WGCombat/CP05C-1104-A/PureBuild/Release`，全文件SHA见Evidence/release-files.json。使用新独立storage root，加 `-cp05-training -wanxiang-storage-root <new-root>`。四武器、自由/辅助切换沿用原训练按钮和当前键位。物理键鼠及独立人工测试本批未执行，不预填结论。训练地面临时收益不结算入正式仓库。
