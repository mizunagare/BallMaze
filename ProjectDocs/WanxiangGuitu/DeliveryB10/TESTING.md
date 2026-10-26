# B10 复跑说明（实施中）

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
