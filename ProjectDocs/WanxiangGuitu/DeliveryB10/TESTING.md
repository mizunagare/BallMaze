# B10 / B10-R1 复跑说明

统一入口继续使用DeliveryUI01/Automation/Invoke-LocalValidation.ps1。要求Unity6000.6.5f1、本机现有.NET/Python、独立工程外测试根与足够磁盘/内存。无系统快捷键改动，不激活私有桌面、不强杀超时进程。

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 -SourceProject D:/unity/WanxiangGuitu -TestRoot D:/WanxiangValidationRuns/B10FreshAll -B10 -FullRegression -GameplayOnly -ShaderCacheSource <已退出的同版本隔离工程>
```

每次TestRoot自动创建唯一子目录。缓存只复制版本一致的ShaderCache，不是干净shader编译声明。GameplayOnly避免重复无新线索的关闭矩阵；仍运行完整规则、正常AI、发行构建、正式标题状态与独立受控Player。预期探针FAIL与非预期失败分别统计。

定向复跑复用DeliveryB4/Invoke-Directed.ps1：Methods可指定B10Rules.Run/Resume、B10Comparison.Run、B10Cats.Run。Rules在初始化后设置独立合成档，真实业务回调、写盘故障回滚、过期按钮拒绝与跨进程身份检查。Comparison用固定seed31415，四分辨率菜单与两分辨率管理页，实际运动/伤害的受控截图；禁用敌方AI，不冒充正常AI。

精确旧版：Export-Baseline.py从本地Git对象导出b474765dc9c28aaf7d2d267bc0362f828f1902b0，验证本地LFS载荷，不checkout/reset。Invoke-BaselineComparison.ps1仅注入同一比较驱动与尺寸助手；旧版产品Assets/Packages/Settings保持提交内容。前后同名图片可直接比较，不裁切隐藏问题。

Invoke-ControlledPlayer.ps1调用现有编排函数构建独立非开发验证Player；驱动以.cs.source显式注入外部副本，不能进入发行程序集。四场景：read、continue（新进程）、new、pending。真实uGUI回调/截图/退出按钮、退出码、审计和校验由Verify-ControlledPlayer.py核对。不是原生鼠标键盘。独立桌面名严格WGTest_加32位十六进制；禁止激活桌面。

Publish-Evidence.py复用既有脱敏工具，白名单发布结果、日志和截图，不发布完整存档、分页、Library、构建或凭据。原始日志外部保留，发布日志记录原始/脱敏SHA。截图直接复制原始像素。

性能计数只属于独立受控Player的菜单/背包序列（含截图、驱动和非活动桌面开销），不是正常冒险性能门槛。无效GC计数标NOT_RUN。原生U16、独立人工理解仍NOT_RUN，D3D12 UNKNOWN与Editor青色帧仍UNRESOLVED。

## 当前冻结输入与专用检查

产品输入 `6cad42d535347e0d96ede0e40f3d6a889a846bab`，最新主参考为用户黑猫概念PNG，STYLE_GUIDE v0.7。最终All采用 `D:/WanxiangValidationRuns/B10R1ReadinessFinalAll` 唯一子目录。此前其他All不是最终输入，结果独立保留。

- `B10ArtSpec.Run`检查14个持久角色、面部/肩带、无Collider、钢/布/皮参数和全局RNG只读；不代表审美验收。
- `Check-Icons.py --icons <Resources/CatWorld/Icons> --output <fresh.json>`默认要求47张实际PNG，256 RGBA/nonempty，以及portrait/hero/potion/sword完整形状alpha覆盖阈值。只观察，不修改PNG。
- `CatWorldBake.Batch`仅在隔离副本制作资源。显式写入Mesh顶点、法线、索引、包围盒并上传，保留原GUID。禁止在正式Player中生成或写Assets。
- `B10Comparison.Run`四分辨率菜单、两分辨率管理页、真实移动/翻滚/伤害与受控攻击姿态；标题镜头到猫脸的树冠包围盒遮挡和屏内构图断言。普通敌关闭，只证明受控表现，不替代正常AI。
- `B10Cast.Run`按实际出生位置选择可用相机位置，记录LOS/冠层与可见性；不改HP或伪造战胜。before近战不可见的FAIL保留。
- `B08CampPause`batchmode沿用明确合成目录初始化；非batch等待Start。使用实际CC、位移总上限.2m和E目标/教程阶段日志，避免Editor回调频率造成无界位移；不修改移动速度或冷却。

最终审计复用 `DeliveryB10/Audit-Release.py`，额外拒绝发行程序集含B10测试驱动，比较276个猫族文件的实际构建输入。`DeliveryB4/Provenance.py`另记录全量产品源码/运行副本/构建输入/执行驱动哈希；`DeliveryB08/Verify-Staged.py`核对仓库证据与LFS载荷。发布仍复用原脱敏器，所有失败另存。

当前发布资产目录明确6个CONCEPT_ONLY、5个仅CREATED；不要为了全绿添加无业务的材料、商店或任务，也不要由一张截图自动认定全部137条VERIFIED。

正常启动：Unity6000.6.5f1等待资源导入后普通Play，或通过“万象归途/构建/Windows 正式版”构建；正式入口为Boot→Title→明确选择。已烘焙资源不要求用户手动生成。测试必须使用上述工程外隔离命令，不把真实玩家目录作为故障样本。

## UI未就绪与日志门禁

B10InventoryReadiness.Run为batchmode合成LegacyHarness，先在没有Profile时实际打开背包，观察异常日志但不抑制；验证真实未就绪Text、库存/随机不变，再经InitializeStorage进入正常页面。修复前有真实FAIL，修复后与药水/双武器/交易/恢复/视觉定向共7 PASS。

Check-RuntimeLogs.py要求显式工程外owner.json根，扫描产品源码栈的NullReference/MissingReference/MissingComponent并实际返回非零。已对旧冻结目录复核549 findings/FAIL，对修复后6日志复核0/PASS。当前完整编排在结尾执行此门禁；它不豁免其他异常，不过滤原日志，也不将Editor内部异常强归为产品。

性能观测是在受控Player用例结束、返回标题前后的Resources/ProfilerRecorder采样；含驱动、截图、非活动桌面与资源卸载时序。纹理计数不是GPU显存峰值，主线程不是正常森林帧预算，0 Draw计数标NOT_RUN而非优化成功，GC无有效计数标NOT_RUN。
