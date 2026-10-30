# BALANCE-AI-02 验收

| 项目 | 状态 | 有限证据与边界 |
|---|---|---|
| 当前防御/伤害来源 | PASS | ARMOR_DAMAGE_BASELINE，BeforeRules真实装备0/3.2/7.6/19.2 |
| 多候选可复算曲线 | PASS | Model.py、1224行COMPARISON、DAMAGE_CURVE与85边界断言 |
| 高防普通/远程不全部1 | PASS | 活体非致死45近战+33远程，旧100%触底→新0% |
| D0、低中高、精英、双Boss、混合/夹击 | PASS（受控） | 3seed×3独立Run/版本，各216样本；六Boss真实raw均出现 |
| 30/90活动秒、移动/早晚闪、治疗/冷却 | PASS（受控） | 窗口提前死亡/清场停止，各22个达到90秒；不是全排列 |
| 正常AI完整出征与成长观察 | PASS | 3进程Gather、撤离结算/制造/再出征恢复；实际30XP，无升级，不改XP |
| 旧v9、回调、低HP撤离与Committed | PASS | LegacySave旧代码2夹具断言 + LegacyLoad9；当前Damage42单事件 |
| 相机/枪口/武器/弹体回归 | PASS | AIM31+132、时序188、区域34，源不改 |
| Boss经济/死亡记录 | PASS（受控域） | BossEconomy阶段，不当正常AI Boss胜利 |
| 非开发验收Player Damage与恢复 | PASS（受控规则） | 两进程，九Damage独立标量夹具、菜单真实继续、正常保存；非原生/AI |
| 纯发行/验收构建与输入 | PASS | 0错96/121警告，完整消息/哈希；纯发行无驱动 |
| 用户文件/v9/经济/RNG/地图/依赖 | PASS | SHA保护，源码对比，无新必需字段 |
| 原生U16/独立人工/最终乐趣 | NOT_RUN | 不用虚拟设备/AI/截图替代 |
| 完整性能 | NOT_RUN | 本批无有效CPU/GPU/GC基准，不能用零值称通过 |
| 历史引擎根因 | UNRESOLVED | UNKNOWN、青色帧、Search等不因本批关闭 |

当前产品规则521PASS/0FAIL；旧v9夹具2PASS分开。正常AI3进程、验收Player2进程、构建2类PASS。原始旧预期29FAIL和工具失败保留。18个独立受控Run内432条件样本不等于432独立局；现有矩阵不能证明最终玩家难度或所有合法装备组合。
