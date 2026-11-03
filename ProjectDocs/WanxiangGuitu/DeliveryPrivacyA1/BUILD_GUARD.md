# PRIVACY-A.1 构建保护

基准c6473b1832a545a5d348e26220fafa73cca741ac；分支fix/privacy-release-diagnostics-disabled-r1。不修改main。

仅产品Editor/ReleaseDiagnosticsGuard.cs改变：
1. 非开发BuildReport实际summary.platform必须StandaloneWindows64，outputPath必须为.exe文件；不只读取活动Profile平台。
2. 保留原固定Profile路径、GUID、目标和Diagnostics验证。另固定批准内容SHA256：235d3703e301574ed8ba8326829d8019410700f9c14e4ddf37ac361e1d975876。采用UTF8、仅CRLF转LF，避免Git换行差异；不是删除字段或宽泛白名单。原Profile字节SHA继续用于构建前后保护。
3. 预检绑定真实BuildReport对象和规范输出路径。postflight、Publish必须匹配同一对象、平台和输出；postflight成功标志每次预检先清空，禁止继承旧成功状态。
4. 预检不再删除旧发行回执；可执行文件/目录、.bee.json或.release.json任一存在即拒绝。Publish也不覆盖已有发行回执。失败尝试不撤销之前已签发的发行版本。
5. 原生服务前后检查、Bee五字段严格false、输入哈希和成功BuildReport条件保留。

输出字节仍可能由失败BuildPipeline产生，但没有新发行回执不可发布。原旧回执保留并不代表失败的新尝试被批准。开发构建保留原豁免；本批不修改玩法、ProjectSettings或运行时。
