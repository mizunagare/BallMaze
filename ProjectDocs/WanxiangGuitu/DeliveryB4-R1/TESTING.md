# B4-R1 本地验证

固定Unity 6000.6.5f1，原项目与Packages不升级。每次使用工程外全新测试根和合成存档，冲突跳过，不抢桌面、不强杀、不使用真实玩家档。

完整复跑沿用原入口：

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
  -SourceProject '<工程>' -TestRoot '<工程外唯一父目录>' `
  -Phase All -FullRegression -B4 -ShaderCacheSource '<已结束的隔离副本Project>'
```

不降低原8 GiB磁盘门槛。缓存不足时只能在核对owner、路径和进程后处理已结束隔离副本的Library；日志、保存、源码与失败证据保留。不得操作正在使用的Editor或用户工程缓存。

定向规则可用原DeliveryB4/Invoke-Directed.ps1，传 `-Methods R1Audit.Run,R1Rules.Run,R1Rules.Resume,B4Physics.Run`，并明确 `-SourceProject`、`-TestRoot`、`-WorkerFrom`。包装器复用原Step/worker，Resume依赖Run；规则/视觉失败后不能把未执行策略称通过。完整All仍不可用定向结果替代。

- R1Audit：保存入口至POI、42资源及3出口的真实路径、长度、碰撞类型；旧版新增断言先实际失败。
- R1Shore：至少30个不同实际seed，在水体碰撞边界外0.4米向下投射物理射线，必须命中真实地形MeshCollider；不以NavMesh可达代替离路岸线安全检查。首个缺口失败与修复后1364次检查分别保留。
- R1Rules：至少30不同实际seed，固定seed重复数据/前三个运行时重复、版本/非法参数拒绝、每个POI真实距离和完整路径、湖水/岩脊/边界、出口/资源/遭遇、离路可达采样、警戒路径与安全绕行、缓存/不可达推荐/RNG；旧revision4来自B4合成检查点，已有修复回执仅在测试夹具中绑定本测试Run，再核对原布局、原平面与新进程恢复。旧revision1/2/3及历史存档继续原FullRegression。
- B4Physics：实际CharacterController逐边、地点与出口走通，仅此受控通行关闭NPC。
- B4正常AI：Gather/Treasure/Bypass，各Normal/Resume/FinalResume三进程，完整采集/开箱/修复/结算/制造/再森林出征；NPC正常，玩家为领域bot，不是原生输入。新增地形版本断言，既有全布局/RNG/来源账/装备ID/仓库/配方恢复断言保留。
- R1Visual：独立非batch Unity进程、私有非激活桌面，复用UI01Before.Size设置真实GameView，核对1280×720/1920×1080目标，保存地形俯视、湖岸和路线详情。仅此专项禁用NPC和玩家控制用于固定镜头，不能冒充正常AI。批处理规则入口不承担渲染截图。

证据发布使用本目录Publish-Evidence.py，复用原脱敏白名单，不发布save.json、ground-loot页、Library、构建二进制或转储；产品/副本/索引及输入哈希使用DeliveryB4/Provenance.py。分开记录源码、规则、Editor正常AI、非开发Player、原生UI和人工结果。

受控全景使用测试专属斜俯视镜头、farClip=500、关闭雾及GameView重绘；不修改产品相机。PNG尺寸、镜头参数与私有桌面回执随每次尝试发布，青色/裁剪失败视图不冒充可用交付截图。StartChild按可执行文件名识别Unity/Player，创建进程前强制要求私有worker；worker.no-direct-unity使用不存在的路径验证拒绝分支，不能启动真实窗口。所有隔离日志仍单独保留。

后台WM_CLOSE不是标题栏点击。UNKNOWN仍UNRESOLVED，原生U16/人工理解仍NOT_RUN，不启用新的无因果诊断实验，也不因All入口exit0声称全部验收通过。
