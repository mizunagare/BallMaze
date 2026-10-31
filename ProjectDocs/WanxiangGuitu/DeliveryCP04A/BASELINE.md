# CP04-A 固定输入

产品基准 main：`72db192a527bd256e2ba18cd7ab334d8334051da`。开工远端核对相同；独立分支 `investigate/cp04-staff-near-aim` 从此提交创建。只读参考 R1.3：`9ceabf6038878b87dab8a74c92a051860fa60acf`，未合并、未改其文件或分支。

调查工作树 H:/unity/WanxiangGuitu-CP04。唯一测试根 I:/WGCombat/CP04-1031-A；Unity 6000.6.5f1。独立拷贝Assets/Packages/ProjectSettings及既有缓存，无共享可写Library。既有Editor夹具依赖从R1.2隔离工程复制，清单见Evidence/isolated-helper-inputs.json。产品全部1163项与基准副本逐字节一致；新增诊断只在测试副本Editor目录，不在产品Assets提交。

用户工程H:/unity/WanxiangGuitu：ForestRuins.unity、ProjectSettings.asset及_Recovery原有修改保留。两个工作树共2329项产品/用户文件哈希保护；5项旧证据SHA保护；用户工作区前后相同。正式存档不读取、不修改。

三次真实受控Editor运行：Historical、Matrix、CameraWall。各自results.json、command、desktop-process、NativeProbe exit、资源门槛、完整Unity.log均保留。全部在未激活独立测试desktop运行，不抢桌面；不是原生输入、人工试玩或新正式Player验证。未新构建，未测性能。

[保护结果](Evidence/protected-after.json)、[1163输入](Evidence/product-input-binding.json)、[24组合同](Evidence/paired-24.json)、[证据索引](Evidence/INDEX.md)。最终提交见此文件所属Git提交及交付回复；推送不等于复审通过。
