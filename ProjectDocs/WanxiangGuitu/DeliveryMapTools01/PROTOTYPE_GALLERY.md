# 原型图库与来源边界

实际画面来自Player2非开发Windows构建，1280×720；原始图完整保留。是技术白盒与轻量自然区，不是最终美术成品，不据此给三款插件画质打分。

|原型|制作来源|运行结果|未覆盖|
|---|---|---|---|
|远古遗迹房间|自有柱Prefab、石板/墙模块，C#参数布局|NavMesh路径+实际Agent通过|DA房间生成、美术精修、门锁|
|转角通道|自有L形地板/墙体夹具|4角点路径及实际Agent转弯|没有顶盖；完整地下空间未完成|
|Boss大厅|自有放大的柱/墙/地板夹具|实际Agent纵向通行|没有Boss战；本轮不接入产品AI/经济|
|自然地形/森林区|真实MapMagic Noise→Height，树木由自有代码摆放|TerrainCollider、导航、Editor/Player一致|非免费Objects散布、样条道路、完整环境美术|

## 非开发Player原图

![遗迹房间](Evidence/Validation/Player2/ruin-room.png)

![转角通道](Evidence/Validation/Player2/turning-tunnel.png)

![Boss厅](Evidence/Validation/Player2/boss-hall.png)

![自然地形](Evidence/Validation/Player2/natural-forest.png)

Editor原图位于Evidence/Validation/EditorPlay1。Player1四次屏幕采集失败，没有用Editor图替换。Player2测试窗仅显示在独立非输入桌面，无物理鼠标或键盘操作，因此原生验收和人工试玩仍NOT_RUN。

LabInputs保存自有Scene、柱Prefab、TerrainData、NavMesh和材质，Tests保存自有驱动；没有从Gaia/DA或其他网站搬运素材。MapMagic免费包仅本地使用，不公开再分发供应商源码/安装包。技术结构可重建，不意味着完整产品地图、美术或插件体验已通过。
