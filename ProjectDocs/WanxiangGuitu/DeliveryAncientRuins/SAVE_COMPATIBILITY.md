# 存档与恢复边界

保留v9原子封装、校验和、Profile/Run、Pending/Committed、来源账、装备和地面分页。没有新增顶层存档版本，也没有向已有GearType插入枚举。新地图仅在ForestLayout既有容器加入可空mapId/mapAssetVersion、默认0的ruinsStage，使用revision6/内容C1-RUINS-1/生成9/保存资产C1-BAKED-1。字段缺失仍走旧森林1–5，旧Run不在读取时升级为遗迹。

本轮真实跨进程以产品SaveProgress生成SeedPackage，逐文件原样复制（含ground-loot页，SHA核对），正常标题Continue读取；Expected只是只读观测对照，不编辑游戏存档。校验Run/区域实例/seed、完整布局、Terrain高度与孔洞、三流、事件、敌人生命、装备ID、地面ID、位置、材料来源账和教程/徽章。重复读取三次、取消撤离、真实Pending→Committed→确认→营地→新Run均独立验证。Boss死后材料拾取和地面紫装也做新进程恢复，重复领取/提交不变。

新地图没有森林首次徽章或旧Boss首次奖励；既有永久仓库、配方和徽章由原事务保留。新奖励全部落地，不把地面紫装当作已入仓收益。旧B3流与B07经济在本轮重新执行；B07受控填包/直接Damage夹具仅作为旧规则回归，不是C1正常战斗证据。完整v1–v8迁移矩阵本轮NOT_RUN，未继承历史PASS。

中间stage3样本恢复只证明逻辑区域/事件不增加，不是已发行C1旧资产逐值兼容。最终原型发布前资产迭代已冻结SHA；未来修改C1-BAKED-1须保留旧版本资产解析。当前程序不承诺旧二进制能够打开新增revision6地图。
