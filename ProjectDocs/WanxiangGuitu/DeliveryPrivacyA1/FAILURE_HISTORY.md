# 失败历史

所有PRIVACY-A历史目录未覆盖。新根I:/WGCombat/PRIVACYA1-1103-A。

- ReleaseBuild：GetInstanceID在6000.6.5f1为error级废弃API，编译exit1。保留原日志；改用Unity对象身份比较，不降断言。
- 创建独立测试源码时出现过目录创建竞态，Set-Content未写入；重新创建目录后重做。未将未启动测试计PASS。
- ReleaseBuild2：复用副本成功构建，原生服务负例曾使该研究副本全局EngineDiagnostics字段为0。检测后不隐藏差异，另从仓库基准文件制作CleanProject并新建CleanRelease构建证据。
- 错误平台、错误输出、旧回执和其他负例均预期构建失败；必须观察指定保护错误才算该负例PASS，不以任意exit1代替。
- 先前33348 SafeMode占用属于上批历史，不强杀、不清理用户进程。人工与历史外部路径状态不变。

- 发布包初次JSON完整性检查将2个故意写入的旧回执文本哨兵当作正常JSON解析而失败。保留DELIVERY_VERIFY_ATTEMPT1.json；最终校验仅对路径和原始字节均准确匹配的这2个保存性夹具标记opaque，其余JSON继续严格解析。原始哨兵不修改、不冒充有效发行回执。
