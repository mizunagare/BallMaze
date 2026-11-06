# CP06-C2.3 地下湖与环湖探索

开工基准：`35efda203b0b36801139fa2cc80ab7ba895207af`。分支：`feature/cp06-crystal-cavern-c23`。本报告所在最终提交即交付版本，完整 SHA 由交付消息及远端分支核对给出，避免在提交内部写入自引用 SHA。main 保持 `72db192a527bd256e2ba18cd7ab334d8334051da`，不合并。

## 实际变化

新增固定湖区资源 `Assets/Resources/CrystalCavernC23/Cavern.prefab`，连接原能量通道。北岸路线较长且无新增遭遇，南岸较短且有普通巡守；两侧均可以往返。对岸机关打开固定石桥两端门，物理阻挡、可见门、导航和保存的事件状态共同变化。深水有明确低水面与可见实体岸壁，不是可行走的蓝色地面。

新增铁矿脉、晶石脉、普通宝箱及普通巡守各一个。复用现有采集、掉落、拾取、来源账和结算路径；这是额外普通资源供给，不宣称经济总量不变。本批不添加 Boss、永久特殊奖励、材料枚举、配方或独立经济系统。

修改七个既有源码文件：CrystalCavernLayout（显式 9/12 版本及稳定 ID）、CrystalCavernRegion（固定资源和桥门导航事务）、AdventureFlow（仅新 Run 默认 C2.3）、WorldEventPoint（桥门合法交互）、PlayerHudPresenter/SaveCatalog（简短版本与路线提示）、Editor/CrystalCavernAuthoring（编辑器制作固定资源）。其余已有产品文件通过哈希核对；CombatAim、TargetAssist、镜头、武器、技能、奖励工厂及存档合同不变。

版本兼容详见 [SAVE_COMPATIBILITY.md](SAVE_COMPATIBILITY.md)。C2.1/C2.2 原固定 Prefab 与旧 Run 的布局、实体、已采集状态保持原路径。v9 不新增字段。新增机关复用 SavedWorldEvent.used；所有新增来源 ID 使用 c23 前缀。

## 运行证据口径

- Editor：独立 EditorProject，真实产品程序集，测试驱动只存在于隔离工程。
- 非开发测试 Player：从 PureBuild6 原始纯包复制，单独添加观测驱动。真实角色移动、采集、敌人 AI、伤害、交互、保存及结算由产品代码执行。此层属于自动化 API 驱动，不是原生键鼠。
- 纯发行包：PureBuild6 无测试驱动，固定 WindowsRelease Profile，Development=false，实际 Bee 五项服务 false。实际标题 ready/rendered、无游戏 HUD/Run 自动启动、后台关闭后实际进程退出和合成档不变分别记录。后台 WM_CLOSE 不是人工菜单退出。

最终用例结果由 [Evidence/final-results.json](Evidence/final-results.json) 与 [ACCEPTANCE.md](ACCEPTANCE.md) 汇总，断言、完成标记和真实进程退出共同核对。历史失败不混入最终重跑统计，也不删除。

连续样本 PlayerContinuousAudited：营地正常新建 Run，实际步行穿过原区域及北岸，真实攻击采矿并拾取，远岸开启机关/宝箱，通过石桥和旧通道返回免费出口，实际撤离 Pending→Committed→回营，再由 PlayerContinuousWarehouse 新进程核对材料与唯一回执。开始后不传送、不改 HP、不冻结敌人。南岸正常遭遇在 InnerVerified 中独立记录，敌人移动和生命事件有连续轨迹。七武器专项在 LiveVerified 中是明确标注的受控夹具，不能替代正常遭遇。

## 构建与保护

Unity 6000.6.5f1，Windows64，最终 PureBuild6 构建成功，0 错误 / 105 警告。全部构建日志原样保留并归档。产品程序集、EXE、全包文件清单、Profile SHA 和 Bee 输入见 [release-audit-PureBuild6.json](Evidence/release-audit-PureBuild6.json)，不只用通用 Unity EXE 识别版本。

Assets/Resources.meta 构建前后相同，GUID `6aaf8bcf5205f18438fdf3b076d7c003`，扫描未发现序列化引用。五项已有 Unity 自动写回仍单列于 [build-input-differences.json](Evidence/build-input-differences.json)，不将差异改写成完整输入语义等同性 PASS。

测试根 I:/WGCombat/C23-1106-A。所有测试数据均为合成存档，已有 C22 合成恢复样本只复制到新的测试目录。用户五个未提交文件原始/最终 SHA 保持相同，详见保护清单。未升级依赖、修改用户 ProjectSettings、真实存档或历史证据。

## 限制与开放项

原生物理键鼠、人工体验、最终平衡、未校准 GC/GPU 及未批准性能预算仍 NOT_RUN。当前环境是固定模块原型，实机截图证明资源显示和空间遮挡，不等于最终美术或人工可读性通过。C1/R7 原 7 PASS / 1 FAIL / 2 NOT_RUN / 2 UNRESOLVED、严格像素失败、三个阶段指纹、GraphicsSettings 写回因果、发行语义等同性、原生内存漂移、JobTempAlloc、MapMagic 标签差异继续保留，不启动同范围 R8。

本批完成后等待固定 SHA 独立复审，不进入洞窟 Boss、地下新区域或下一批地图。
