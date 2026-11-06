# 保存兼容方案

产品 v9 不新增字段。新建洞窟 Run 写入 C2.3-CAVERN-1 / revision 9 / generation 12；检查点完整布局按 GenerateLake(seed) 精确比对。C2.1 和 C2.2 分别保留 7/10 与 8/11，仍精确加载原资源。不将旧存档升级为新布局。

c23:bridge:lever 使用已有 SavedWorldEvent.used 保存当局捷径开关。加载先读取对应事件，再设置门 Collider、重建导航。运行时打开失败会恢复门状态；事件 Used 只在成功后写入。矿脉复用 SavedResource，首次旧节点编号保持 2100/2101，新节点追加 2102/2103。普通宝箱 c23:far-shore:chest 通过 WorldEventPoint → ForestRewards.Ruins → LootPickup → 来源账路径发奖，不新增永久首奖。

普通宝箱使用原 Ruins 类型规则：晶石 4–7、铁矿 1–3，以及原装备工厂的一次普通品质抽取。节点使用现有采集范围 3–6 加既有采集加成；新增巡守复用既有掉落。上述为新增地图供给，旧来源概率不变并不意味着总经济供给不变。

跨进程验证将分别核对关闭、已开、落地未拾取、已拾取、已撤离入仓；尚未执行的结果不得依据此设计标为 PASS。

最终实测：两层 Store→Resume→Warehouse 核对同Run、已开桥、已采矿物及每项地面奖励的 ID/类型/数量/完整装备JSON，实际撤离后新进程核对已提交回执和永久材料；Closed→ClosedResume保持关闭桥门；Repeat从旧营地正常创建新Run并重新获得普通奖励。旧C2.1/C2.2分别读取原合成档，保持固定资源和已有状态。森林和遗迹入口/恢复也分别执行。参见 Evidence/final-results.json 与原始 Raw。
