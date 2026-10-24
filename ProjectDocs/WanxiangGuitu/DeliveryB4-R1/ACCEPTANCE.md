# B4-R1 验收

本轮最终完整运行：`20261024-165747-a3f1be5c`。只有该次实际执行结果用于最终汇总；历史尝试保留于Evidence/Attempts。下表区分验证层级，不将截图、领域bot或后台窗口消息称为原生UI操作。

**83 PASS / 2预期探针FAIL / 19 NOT_RUN / 1 UNRESOLVED，0非预期FAIL。** 协调器实际exit0，无遗留测试进程。[分类](Evidence/FinalAll/classification.json)、[逐项JSON](Evidence/FinalAll/results.json)、[CSV](Evidence/FinalAll/results.csv)。PASS包含预检、编排和进程步骤，不是83个独立玩法验收。timeout探针无正常退出码，保留后自行结束，不能当作正常关闭。

| 验收 | 状态 | 证据及边界 |
|---|---|---|
| 30不同实际seed、相同seed重复生成 | PASS | R1Rules：31次请求、30实际seed，30套地形参数；前三个运行时Capture也重复一致 |
| 地形有高度、可离路探索 | PASS | r1-open-space.csv：每布局140～192个远离图路线的完整导航采样；不是全区域穷举或人工体验 |
| POI/资源/遭遇/出口完整可达 | PASS | R1Rules/R1Audit及B4Physics，30布局实际NavMesh与受控CharacterController逐边走通；NPC仅此受控专项关闭 |
| 湖水/岩脊/边界不被推荐路径穿越 | PASS | R1Rules对完整corners路径段检查；碰撞体/网格导出另存 |
| 岸线物理地面完整 | PASS | R1Shore：30不同实际seed，1364次水体边界外物理射线；修复前缺口FAIL保留 |
| 危险路径与真实绕行 | PASS | 同目的地21条风险/避让对；种子1湖岸137.8273米风险路径、142.1693米避让路径。前往哨站确实接近精英，不能声称开放森林的湖岸在物理上必经精英 |
| 推荐距离与实际路径/不可达目标 | PASS | R1Rules：corners长度一致、5000米外目标拒绝推荐；最多1.5秒/2米缓存误差 |
| 查询缓存/剩余收益/随机隔离 | PASS | R1Rules重复20次无额外路径查询且全局/本局RNG不变；B2/B3/B4状态回归实际执行，不自动领取/移动 |
| 旧revision1/2/3/4与旧在途 | PASS | B4StateRules及历史FullRegression，新增R1Rules/Resume核对rev4完整保存布局和原平面；测试回执仅绑定自身合成Run |
| 遗迹概率/五地点收益/重复奖励 | PASS | B2Rules、B3Checks、B3StreamRules、B4PickupRules实际执行；未修改ShouldDropChestGear |
| 渡口扣费/来源账/唯一结算 | PASS | 既有B1/B05及Gather实际木2石1修复/重复调用拒绝，三策略结算重复提交断言；未另起系统 |
| 正常AI三种有收益策略/制造/再次森林出征 | PASS | 九进程均exit0；Gather木6扣2、入仓4取2后余2；Treasure真实3件装备和皮7晶8木6矿2，取木2后余4；Bypass木4、取2后余2，距精英最近81.44389米，未触发哨站。均为正常NPC领域bot，不是原生输入 |
| 新进程地形/布局/RNG/实体/装备ID/来源账 | PASS | 每策略stage1/stage2完整快照；九进程实际执行，后继mode=ForestExploration；新增terrain1/revision5断言及R1旧档Resume |
| 非开发构建、输入/产物哈希 | PASS | BuildOptions.None，0错误75警告；75产品源码一致，781输入六项副本差异逐项披露，不能称全部字节相同 |
| 受控1280×720/1920×1080地形/湖岸/路线 | PASS | 4张R1实际PNG逐张检查，另92张原UI受控矩阵本轮重新生成；私有非激活桌面、固定镜头，不是正常AI/原生UI |
| 非开发Player后台关闭/恢复 | PASS | 8进程（4组×2）实际WM_CLOSE、exit0、无超时、退出审计/恢复断言通过；不证明真实标题栏关闭或UNKNOWN根因 |
| 原生U16 | NOT_RUN | 无安全独立交互环境；后台WM_CLOSE和受控GUI不代替 |
| 人工可理解性 | NOT_RUN | 未安排独立人类试玩 |
| D3D12 UNKNOWN根因 | UNRESOLVED | 沿用历史证据，无新因果线索，不重复试探产品生命周期 |

主观的“自然地形观感/自由探索是否有趣”未做人类验收，NOT_RUN。本轮提供可复跑的物理与收益证据，不宣称完成正式地图美术。首次直接隐藏Unity辅助调用的隔离缺陷及桌面焦点影响未核实独立披露，不能用后续私有worker通过抹去。
