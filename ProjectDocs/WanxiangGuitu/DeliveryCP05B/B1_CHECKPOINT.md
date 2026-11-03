# B1 可玩镜头快照

从c6473b1832a545a5d348e26220fafa73cca741ac开始，CombatAim及PRIVACY-A发行Profile/入口不变。原型开关：训练参数`-cp05-training -wanxiang-storage-root <新的I:/WGCombat自有根>`，不能省略隔离根。B1最终本机包：I:/WGCombat/CP05B-1103-A/B1/Build4/Release。使用Evidence/B1/release-files.json核对，不复用失败包。

训练环境由独立运行时Scene创建，无CombatSession、正式Run、结算或真实档案；角色/敌人Prefab从固定原场景导出至新Resources/CP05Training，不覆盖旧场景。两个敌人使用原CombatEnemy AI，武器切换调用SelectMain事务。Esc释放鼠标，右键捕获；原镜头/肩后按钮保留对照，B2/B3未实现按钮在B1禁用。

实际：Build4非开发None，0错误96警告，Bee五服务false；Smoke4训练启动到READY，普通后台WM_CLOSE后exit0，无运行时空引用。受控Editor2：镜头偏移、墙避障、材质恢复、RNG只读及输入屏障通过。GC正分配校准返回0，因此GC为NOT_RUN，不能解释为零分配；CPU原始Stopwatch含反射调用，仅受控采样。

失败全部保留：Smoke1因独立训练缺AdventureFlow产生淡化空引用；Editor1夹具停滞到240s有界deadline exit1，后将Probe从Editor程序集放入隔离运行时程序集并使用实时等待/进度记录，Editor2完成；Build3因移除运行时Probe后仍残留引用它的Editor夹具而编译失败，Build4同时移出两者后成功。Editor.Search内部异常、JobTempAlloc日志不隐去。

截图为Editor API受控截图，不是原生输入或人工试玩。本批后续B2/B3尚在实施，不据此声称整批完成。历史UI-01、人工理解、引擎开放项不关闭。
