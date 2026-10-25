# 教程保存与兼容

不新增第二个文件、不升级完整封装v9；沿用既有主档、备份、分页与修订号保存。教程只属于Profile，不代表Run奖励、永久仓库或结算账。

| 字段 | 默认/来源 | 恢复与校验 |
|---|---|---|
| Profile.hasTutorial | 旧档缺省false；新建Profile明确true | false时运行时忽略并清空物化的默认Tutorial对象；旧玩家不强制播放 |
| tutorial.version | 1 | 仅接受已实现版本1 |
| enabled / skipped | 新Profile true / false | 不允许同时true；跳过只变更教程设置，通过正常保存 |
| stage | Equipment…Complete (0～12) | 越界拒绝；完成后enabled=false，不自动重播 |
| completedMask / learnedMask / seenMask | 0 / 0 / 1 | 只在真实步骤成功后更新；合法13位，避免每次重复教学通知 |
| firstRunId / firstPickupId | 真实Run/掉落ID | 长度上限128；不是创造奖励的依据 |
| resourceLootIds | 本局实际资源生成的掉落ID，最多32 | 唯一/非空/长度校验；未拾取物仍在地面，教程不代领 |
| moved | 实际水平位移，最多3米 | 拒绝NaN/Infinity/负值/越界；RestorePosition不累计 |
| reviewAllowed | true | 本版始终提供只读重看；不通过重看重置物品或教学 |

Unity JsonUtility会将空内联对象物化，因此不能只用tutorial==null区分旧档。这一问题在Directed1实际失败，后加入显式hasTutorial；旧v9关闭引导和主动启用有专门回归，v1～v8迁移链由本轮完整历史回归重跑。

阶段与业务保存共用现有路径：设施成功打开后保存，采集实际拾取/位移完成后保存；出征、撤离、结算确认、营地取材及制造在原事务内更新。中途退出恢复最后成功保存的阶段；失败未落盘的操作不虚构成已完成。死亡/放弃回到准备，沿用原损失保护，不补材料。再次出征只有确实创建不同森林Run且首局已提交才完成。

明确点击“启用（营地）”可重新开始教学状态；它不会重置Profile、库存、装备、徽章或Run。仅打开“教程/帮助”是纯读，不能推进阶段或消耗随机。旧在途不插入教学物资、怪物、出口或新地形。

设置保存的发布后回调异常，以及营地取材/制造的发布后异常，均先检查实际主档修订/Profile/内容。已发布则确认；确认旧修订才回滚；无法确认则显示待核对并阻止重复消费。测试只注入显式隔离合成档，日志内B08_EXPECTED标记为故障夹具，不能当普通玩家异常隐藏。

独立进程证据包括在途FreeExit、回营制造后的DepartAgain、后继森林Complete，以及跳过状态。正常AI独立核对Profile、Run、区域、seed、布局、装备ID、仓库、材料来源账、随机流、配方、徽章与教程快照。正式Player另核对同一后继森林的启动/退出保存/继续；不冒称原生键鼠教学已验收。
