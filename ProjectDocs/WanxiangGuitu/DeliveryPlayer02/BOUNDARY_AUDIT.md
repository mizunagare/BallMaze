# PLAYER-02 开工边界审计

开工本地及远端main均 `428c41fa4f82e7a95c3163319384cad668b5ef6b`。用户场景/设置及Recovery三项只复制到隔离工程，源清单1152项；不改产品或依赖。

| 现有 Gather/输入实现 | 不能直接搬入正式 Player 的内容 | 本批临时验收实现 |
|---|---|---|
| UnityEditor、EnterPlaymode、OpenScene、GameView、-executeMethod | 编译/场景启动依赖Editor | RuntimeInitialize+MonoBehaviour，正常Boot/Title，不绕过GameEntry授权 |
| 给初始库存Add材料、直接选装备 | 不是完整玩家输入链 | 从新游戏标准初始物品开始，经装备UI选弓；采集所需木/石/矿 |
| 相机RestoreView、直接写hero.rotation | 直接设表现姿态 | 虚拟Mouse delta与正常移动转向；NavMesh只读规划 |
| AdventureCombat.Strike、LootPickup.PickUp | 跳过输入/提示 | 虚拟攻击；靠近且DisplayedE匹配后发送真实有效交互键 |
| RepairExit、BeginExtraction | 跳过实际出口交互 | 接近真实导航位置，H经InteractionResolver执行费用/撤离/取消 |
| Commit/AcknowledgeSettlement | 直接结算调用 | 独立进程向本次私有非活动桌面的精确Player窗口投递鼠标消息；驱动等待原按钮带来的状态变化，不以投递成功代替语义成功 |
| TransferMaterial、Craft、Depart | 直接管理调用 | uGUI按钮取材/制造；准备UI确认出征 |
| SaveProgress、EditorApplication.Exit | Editor检查点/退出 | F5实际保存消费者、Application.Quit与外部进程/审计核对 |
| Input01Play editorInputBehavior、反射preferences故障钩子 | Editor属性及私有状态 | 仅runtime InputSystem API；合成目录制造真实.tmp写入障碍，不改业务JSON |

运行时只安排虚拟设备/明确标注的窗口消息请求、等待、读取状态及写测试回执。PlayerInput.Focus用于明确的虚拟焦点测试，InputSystem设备禁用仅作用于本进程；不操作操作系统键盘、快捷键或用户桌面。无传送、AI停用、属性覆盖、奖励注入、私有反射。

发行/验收分别新建副本与Library。复用BUILD-01入口，默认Release不注入；显式Acceptance仅在新拥有者工程Assets/Player02AcceptanceOnly注入文档目录.cs.txt。无需修改Define、asmdef、Build Profile或用户设置。两者均BuildOptions.None，临时包不替代发行产物。发行包须额外检查类型/字符串/场景，不能凭目录约定认为已经剔除。

runtime IMGUI为旧出征/结算UI；uGUI为标题/键位/背包。隐藏窗口没有Repaint、以及直接改Event.current未触发生产按钮两种失败都保留。最终采用现有SW_SHOWNOACTIVATE私有桌面窗口与独立post-pointer工具：校验PID、精确EXE、WGTest桌面、确认为非活动输入桌面、1280×720客户区与坐标边界，仅PostMessage，不切桌面、不发送全局SendInput。请求/响应只是输入元数据，不含业务状态。虚拟InputSystem、合成Windows消息、领域测试、原生键鼠与人工各自单列。原生/人工/完整性能与历史引擎问题不由本批自动关闭。
