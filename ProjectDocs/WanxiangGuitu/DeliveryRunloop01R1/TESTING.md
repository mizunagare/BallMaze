# RUNLOOP-01-R1 复跑

Unity 6000.6.5f1；使用既有 DeliveryUI01、DeliveryCombat01/02 执行器，不启用 CI。所有路径须为自己新建的工程外拥有者根；不要复用占用目录或真实玩家档案。

1. 以 DeliveryUI01/Invoke-Rules.ps1 的 PrepareOnly 创建闲置隔离工程及 Prepare/fixtures，保留源文件保护哈希。Library 可从已确认闲置的旧验证副本复制加速；导入和源码输入均重新记录，不把缓存当测试结果。
2. 新建 owner.json。调用：

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryRunloop01R1/Invoke-R1.ps1 `
  -Project I:/WGCombat/<unique>/P/Project -RunRoot I:/WGCombat/<unique>
```

入口只接受 I:/WGCombat 下的拥有者根，检查 Unity 占用，复用原有有限超时执行器；存在未退出子进程时停止使用该副本，保留现场，不强杀。规则/恢复矩阵失败不会删除其证据；依赖循环失败停止依赖链，独立测试按安全条件继续。脚本不是全验收通过断言，必须检查逐项 JSON 与退出码。

R1Matrix 在同一进程中为每例创建独立合成 Profile：真正出征→资源 Hit 产生 ground-loot→主动放弃 Pending。负例才修改候选 DTO；候选必须先通过完整 v9 读写校验。只读恢复正例使用原已发布文件精确字节。before-camp-load/before-build 仅抛一次，第二次由结算按钮的同一真实 presenter 分派重读。前版不存在该方法时，夹具复刻其原三分支调用，并记录实际标记；不能声称前版有新方法。

Guards 比较主档、备份和全部不可变分页的 SHA256，以及内存 Profile/Run；执行自动保存、直接保存、受控 InputSystem F5、失焦、暂停和退出回调。F5 是 Unity 虚拟设备事件，仅检查保存保护，明确不是原生输入。退出回调不是实际退出；不将进程消失或编排器 0 当业务成功。

R1Migration 使用 Prepare 生成的 v1～v8 合法旧版合成夹具，先建立实际待核对，再完整读取旧夹具；迁移发布前故障应保留字节和门禁，解除故障后相同 UI 命令正常迁移。范围为门禁自锁回归，不是旧版全组合证明。

入口随后运行原 Fault/Uncertain、五进程循环、世界实体审计、标题入口、B09 Catalog 四进程、既有相关回归和正常 AI 三进程、非开发构建。实际执行源码、方法、时间、退出码、超时和日志见每次 results.json/children.json 与 sequence；完整构建警告不滤除。

构建后执行只读 PE 检查，确认发行程序集不含 Editor 夹具及 UnityEditor 引用。用 Collect.py 发布拥有者根白名单证据；压缩日志保留 sourceSHA256，不改原始文件。首次工具失败同样保留。最终核对用户和历史文件哈希、暂存范围，提交推送后重新读取远端完整 SHA。

物理鼠标键盘、独立人工体验、纯发行 Player 实际关闭、性能及全部回调组合不由本夹具证明，分别 NOT_RUN/既有 UNRESOLVED。
