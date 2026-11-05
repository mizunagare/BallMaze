# R7 发行语义结论

**七个固定机位没有观察到可归因于发行包的渲染回归。** 两包实际提交的着色器阶段组合逐机位一致，有效 URP 渲染路径和结构化相机、光照、材质状态一致。曝光控制在七处有真实画面和实际提交证据。两包未重建，原有资源字节差异及 R6 的 140 张重复采集证据均保留。[实际提交](SHADER_VARIANT_AUDIT.md) · [后处理开关](POST_PROCESSING_AUDIT.md)

原生画面严格像素仍 FAIL。R7 中七处均出现非零跨包配对，R6 的同包自然波动对照继续有效。GraphicsSettings 新字段的初始化和已发行行为已核对，单独去掉写回时的发行影响及全面渲染语义等同性继续 UNRESOLVED。结论限于本轮窗口、固定机位、曝光控制及该机器的 D3D12。[像素数据](Evidence/Audit/post-cross-package.json) · [R6 同包范围](https://github.com/mizunagare/BallMaze/blob/3ba94741f91f554b5aa69f0c130f01b17e4f8618/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR6/CROSS_BUILD_RENDER_COMPARISON.md)

两份原包各 193 文件完整复核，Development=false、Bee 五项关闭。R4、R5、R6 的发布证据与相应本地原始文件逐项复核，用户保护路径 2,413 项无差异。[保护记录](Evidence/Audit/protection.json)
