# 新资源与 Player 表现

资源路径 Assets/Resources/CrystalCavernC23。本批由自有 CrystalCavernAuthoring 编辑器工具制作并保存固定 Prefab；Player 不依赖 Editor 生成。新增岸岩网格是确定性八面分层形体；晶簇沿用自有六面水晶形体。材质使用既有 URP Lit，不引入新 Shader、贴图或供应商资源，无全局 URP/后处理配置修改。

第一版实机发现高低顶盖之间露天空、湖岸过于方正、版本标签过长。保留 PlayerLake1 原截图。后续在新资源内对齐顶盖高度、增加自有侵蚀岩层、改为可辨认石栅桥门，缩短标签；第二次检查发现湖口与原通道连接处的边肩空隙，补齐新区域的四段过渡墙，保留第二版截图。所有变化限于新增湖区及其新资源制作代码。

不会以 shader.isSupported 或对象数量证明人工审美通过；受控 Player 原始肩后截图与实际移动日志共同证明资源加载。人工可读性、原生输入和最终表现品质仍 NOT_RUN。

最终 PureBuild6 新Prefab统计：611个Transform对象、105个Collider、22种sharedMaterial（含既有C2.2部分）。Assets/Resources/CrystalCavernC23 内资源逐文件来源/SHA见 Evidence/asset-catalog.json；自产固定模块、材质和网格，无外部新素材。本次运行中相关Shader均isSupported，并有未裁剪Player截图，仍不等于人工审美通过。

受控采样硬件与原始数据见 Evidence/hardware-and-measurement.json、runtime-measurements.json。正常南岸样本Editor采样49.311s，Player48.936s；场景快照总AllocatedMemory分别649778104B和421429708B。这不是逐调用GC、稳定内存基准或泄漏判断；驱动写文件有额外开销。CPU帧、GPU、GC校准、DrawCalls及加载卸载性能预算均NOT_RUN。
