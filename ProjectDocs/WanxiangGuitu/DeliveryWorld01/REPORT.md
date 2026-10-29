# WORLD-01：森林探索内容与路线决策

开工本地/远端 main 均为 `3b14dca0c246abdc71f44c02c765716d989fb6b4`。产品与主要纵切冻结 `21b8a14513bf6b0d0d52c1f797ad653595d05f60`；补充工具/祭坛冻结 `3d7e97ff5971c9be68c0d8637f77f53b4560fa6c`。最终提交见本报告固定 Git 版本及交付块。本批不新增内容系统、不改变地图、经济、掉落、武器参数、随机流或 v9 字段。

## 审计与最小修复

[实际状态图](WORLD_STATE_MAP.md)区分营地、森林 Running/Extracting、地面、背包来源账、Pending、Committed、待领取、制造与后继 Run；[87 行内容审计](CONTENT_AUDIT.csv)逐一覆盖七 POI、42 资源、13 普通/精英/Boss、12 事件、三个出口及反馈/合同/缺失机制/建议，不把未实现机制当作新增授权。

当前森林已经有开放地形与真实 NavMesh、多路线、五类地点收益、宝箱/祭坛、普通遭遇、双 Boss、免费出口与渡口。路线评分观察当前活敌、未耗尽资源/未开宝箱/地面、制造缺口与可用出口；不自动移动或领奖。没有完整小地图，血量/药水/容量由玩家查看 HUD 作决策，评分没有据此预测成功率。[后续提案](CONTENT_PROPOSALS.md)仅记录轻量方向和个人风险解释，未实现新系统或调整权重。

唯一确认产品问题 WORLD-F01：实际森林有两名 Boss、路线预计核心合计 4，制造缺口详情却同时称“此森林无核心来源”。Before/feedback.json 为真实隔离 Unity 输出，consistent=false、queryReadOnly=true，exit1。仅修改 CraftingTargets.Recommendations：根据当前存活森林 Boss / 未拾取核心、布局是否支持 Boss，说明真实来源及可选挑战、绕行/免费撤离。After 同入口新合成 Run，consistent/queryReadOnly=true、exit0。前后是独立 Run，不冒称同一 GUID 跨版本恢复；未改实际掉落量或领取方式。

## 固定样本与可玩纵切

418、419、420 各两次独立 Run，共六份有效纵切；另有首次编译失败和一次夹具暂停处理失败，均单列保留，不隐藏成六次全成功的总成功率。六份样本拥有不同 Profile/Run/区域身份；同 seed 布局数据完全一致，三 seed 有三种路线拓扑。全部请求/实际 seed 相等，attempt0、无 fallback、无生成失败记录。

六份有效样本的实际 Unity 导航输出 **520 行**，覆盖七 POI、所有资源接近点、普通/Boss 出生点、12 事件接近点、出口交互范围、展示边及精英绕行。真实 NavMesh corner 长度与所报距离一致；只读几何复核没有穿越深水/实心岩脊。后者是对真实路径坐标的离线复核，不另计场景运行。不是玩家逐段原生行走；正常 AI 行走另列。

六次纵切共 **320 条受控断言**：真实营地出征；两木节点 Hit（只拾取一份，另一份留地）；普通敌启用 AI，以真实 Sword.Strike 击败、DropLootOnce/真实拾取一次；真实遗迹宝箱和重复拒绝；保存→退出→新进程；资源/敌人/事件状态、布局、随机流、装备、来源余额与地面身份相符；免费撤离、取消、受击中断、保存失败、Pending/Committed、不重复提交、营地真实制造/存取、后继森林与再次新进程。

第一份使用五个独立进程 Running→Pending→Committed 分开恢复，其他五份使用 Run→FinishRun→Final 三个进程；FinishRun 仍走实际倒计时/提交/确认/制造，不直接指定结算字段。Snapshot、主备及每阶段材料/身份检查保留。入口导航测试与纵切采用受控定位和非目标敌人冻结，不能称为正常 AI 探索或人工体验；目标普通敌启用真实 AI、攻击和生命判定，没有改 HP 或伤害伪造胜利。升级后通过实际 offered choice 继续，未清空成长绕过暂停。

初始营地 100×六类材料、带入木2 是显式合成输入，用于真实制造事务，不是本局收入。拾取木材数量、earned/brought、未拾取地面、Pending、仓库变化分别核对；不宣称从零物资完成全部制造。现有材料来源账为带入/本局余额，未新增逐笔存档账本。普通战斗逐次 CSV 保留承伤与耗时，零承伤是实际结果，不作平衡结论。

## 受影响回归与构建

祭坛专项六条交互/一次性检查和四条新进程身份/Used/随机流检查通过；实际选择后解除暂停，再尝试重复交互，避免因暂停而误判一次性。BossEconomy 用受控伤害验证满包留地、拾取/回执一次、死亡保留徽章及第二局重复收益，不冒充正常 AI 双 Boss 讨伐。

新运行的 Death、Abandon/Fault、Missing/Corrupt、R1 33 项恢复矩阵、满仓待领取、武器品质/多目标合同、弓杖命中、输入/伤害观测/Boss 攻击及正常 AI 三阶段分别归档。剑枪边界矩阵另列，不重新平衡。正常 AI 实际采集、修复渡口一次、撤离、入仓制造和后继森林两次新进程恢复均 exit0、无超时，未与受控冻结场景混淆。

非开发 Windows64：原 BuildOptions.None。第一次构建准备因缺少隔离输出目录失败，实际 BuildPlayer 未开始；Build02 完整构建 Succeeded、0错误/**96警告**、38.8540751秒。目录修正不涉及产品。该完整警告包括新增提示查询采用既有已弃用查找 API 的两条警告，不批量迁移 API 或声称警告修复。

发现隔离 Unity 导入/构建对五个设置资产重序列化后，另做一次有界 Build03 输入复验：紧邻前后 **1375 文件 SHA256 全部一致**，Succeeded、0错误、2条本次增量警告、6.9736676秒。增量缓存未重报全部编译警告，不能把 96→2 当作消除 94 个问题；两份完整消息均保留。产品源、运行副本、构建输入绑定及发行 PE 检查见 Evidence/Bindings 与 Build03。

最终 EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；Assembly-CSharp `eb11961cd92a05f6fde2bb41da300279cd0684349af5f1887c7421407dd1c10f`。发行程序集无 WORLD/R1/RUN01 Editor 夹具或 UnityEditor 引用。构建通过不是 Player 运行通过。

## 保护、失败与开放项

工程外根 `I:/WGCombat/WORLD01-1029-A`。用户五文件及既有 **3589 个历史文件**前后 SHA256 不变；没有覆盖/提交用户场景、ProjectSettings、Recovery 或访问真实玩家档案。不升级依赖、不加 CI、不抢桌面、不强杀。测试编译失败的自有隔离 Editor 经精确 Safe Mode Quit 正常退出，仅作清理；真实退出0不能把原编译失败改成 PASS。

原生 U16、独立人工、发行/隔离 Player 本轮业务运行及性能预算 NOT_RUN；D3D12 UNKNOWN、青色帧、Search、JobTempAlloc、旧 C15 根因仍 UNRESOLVED。独立可发现性和动态审美没有自动通过。历史与本轮失败见 FAILURE_HISTORY，不覆写旧 aggregate。完整分层结果见 [验收表](ACCEPTANCE.md)、[状态](Evidence/status.json)、[复跑](TESTING.md)、[证据索引](Evidence/INDEX.md)。交付后暂停等待固定 SHA 复审。
