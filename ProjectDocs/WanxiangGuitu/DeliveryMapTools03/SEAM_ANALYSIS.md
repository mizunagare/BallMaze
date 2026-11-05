# 地形接缝与材质条带

## 固定输入

沿用上批原场景的四个 64×64m、257×257 Terrain，seed=424242；1280×720 非开发 Player。高度哈希 `dafeb568a01194ae933daebe4063b3db1d6c274add11a4d5309c8f93e71ab652`。

相机位置→观察点：(140,100,-32)→(64,3,64)，(75,15,53)→(64,3,64)，(64,8,42)→(64,3,76)。透视相机；Sun 方向欧拉(48,-35,0)、强度1.2、Soft Shadows，背景色(.4,.6,.75)。所有阶段固定种子、相机及几何。只有明示 no-shadow-control 暂时关闭阴影作诊断，其画面不作为修复。

## 同一场景的顺序控制

| 阶段 | 修改 | 实际结果 |
|---|---|---|
| baseline | 原始 Scene 与 TerrainLayer | 三张原始 Player 截图 |
| rebind-sync | 显式邻接、SyncHeightmap、Flush | 三视图像素与 baseline 完全相同 |
| lod-control | pixelError=1（原已是1）、关闭 drawInstanced | 轻微像素变化，亮带仍在 |
| pixel-normal-control | 恢复实例化，显式逐像素法线关键字 | 三视图像素与 baseline 完全相同 |
| no-shadow-control | 关闭 Sun 阴影，仅作排查 | 近景树影变化，地表亮带仍在，不接受作修复 |
| matte-source-control | 恢复原阴影；克隆草地层及纹理，将其 Alpha 从1置0 | 高亮带消失；未移动地形/相机/道具，未隐藏接缝或加遮挡 |

[实际前图](Evidence/Audit3/baseline-v1.png) · [实际后图](Evidence/Audit3/matte-source-control-v1.png) · [全景前](Evidence/Audit3/baseline-v0.png) · [全景后](Evidence/Audit3/matte-source-control-v0.png)。全部原图未裁切；其他角度在同目录。受控图片不等于原生操作或人工视觉验收。

## 根因证据

原草地层 `m_SmoothnessSource: 1`（Diffuse Alpha），纹理为自制全 Alpha=1 的4×4纯色纹理；虽然 TerrainLayer.m_Smoothness=0，URP17.6 的 TerrainLitPasses 中该来源分支直接取 diffuseAlpha，不乘 smoothness 常量。表面达到高光滑度，坡度/观察角度使反射形成大片浅色条带。该材质对照保留原 RGB、阴影和高度，仅改变光滑度输入；不是后期遮挡。

四块均引用同一 Terrain/Lit 材质和相同纹理缩放8m；64/8为整数，纯色纹理本身没有跨块纹理图案跳变。外沿是有意保留的有限研究平台边缘，不冒充产品远景美术。相邻 Terrain 邻接在 MT02WorldState.OnEnable 和显式 Link 中恢复；重新绑定无像素改善。

两个方向、每条边65个法线采样的最大 TerrainData 法线夹角为1.40653°；所有阶段相同。所有257边缘高度采样最大差0m，所有阶段高度哈希一致。因此排除本样本的高度裂缝；不能把“法线差不为0”直接等同截图主因，也不宣称其他光照、LOD、纹理或更多种子没有接缝。保留正常法线偏差数据用于后续美术验收。

六阶段结束恢复原材质、TerrainLayer、实例化和阴影，并销毁临时克隆。未保存运行时材质试验到上批场景；90项原自有资产与上批冻结输入哈希一致。仅研究性推荐在自有草地层显式选择 Constant 光滑度/正确 Alpha，不修改供应商或正式地图。

数据：[seam-state](Evidence/Audit3/seam-state.jsonl)、[图像比较](Evidence/image-comparison.json)、[边界投影](Evidence/Audit3/boundary-projection.jsonl)、[原草地层](../DeliveryMapTools02/LabInputs/Assets/MT02GeneratedV2/Grass.terrainlayer)。截图由本轮真实非开发 Player 生成并与构建/进程证据绑定。
