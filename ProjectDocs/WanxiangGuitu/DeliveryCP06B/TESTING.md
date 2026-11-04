# 复跑说明

Unity6000.6.5f1及原依赖；工程外唯一根I:/WGCombat/CP06B-1104-A。产品源H:/unity/WanxiangGuitu-CP04，用户主工程H:/unity/WanxiangGuitu不参与测试写入。复跑必须换新根、输出和合成存档目录；不要覆盖本轮或历史证据。

沿用DeliveryEncounterAI01/Invoke-Check.ps1与既有NativeProbe独立桌面。文档Tests仅注入隔离Project：Editor适配器进Editor/B06LocalChecks，其他运行时驱动进Assets顶层。不得提交驱动到产品Assets。Invoke-LatestEditor.ps1执行新武器/取消/性能及旧核心。StatsBefore/After是合成等级恢复和真实装备工厂/拾取夹具，不是正常成长；旧迁移适配器通过正常标题/新游戏/出征后调用原迁移规则，保留早期Time.time等待超时。

Invoke-LatestPlayer.ps1使用LatestTestBuild4，重跑三武器、死亡/取消、CPU/GC、存档、独立进程、旧四武器/八技能、正式掉落、追加通道控制/完整路径和训练金丝雀。每个进程都有实际NativeProbe命令/退出回执和独立语义probe.json。进程exit0不能替代语义结果。

NearPlayer4专用CP04回归按历史相对几何（near=1.5m，侧相机偏移5/4/-5）复建到独立训练，补充.35/6/20m。不是原冻结二进制复刻。固定步进只用于AI禁用后的测量，不作用于场景重建；真实重开取得健康角色，不改HP，不注入伤害。首三次Player失败及就绪日志保留。NWUpgradeProbe验证旧Run合法放弃→Pending→Committed→确认→营地→新森林Run。

追加通道GroundPackage/PickedPackage由产品SaveProgress实际生成，原样复制到新根再恢复；Expected JSON只是只读对照元数据，不能编辑游戏保存正文。旧/新通道配对见CompareChannels.py；12项负例自测确认数量、品质、词缀、随机流、身份和重复追加不会被放行。

纯包：移出全部运行时驱动和Editor适配器到工程外快照，再用既有CP05Build.Run/WanxiangBuild/固定PRIVACY-A Profile构建。AssemblyAudit比较产品类型IL并排除测试类型/桥；LegacyIL核对基线核心与v9字段；Audit核对用户及受保护文件。纯启动脚本只启动训练并发送后台关闭请求，实际退出与日志单列，不能冒充菜单原生退出或纯包手工战斗。

所有失败、超时和引擎异常保留；不关闭用户程序、不抢桌面、不强杀。原始日志在隔离根，发布副本仅压缩/脱敏，并记录原始与发布SHA。性能范围见PERFORMANCE，未采指标不填零。
