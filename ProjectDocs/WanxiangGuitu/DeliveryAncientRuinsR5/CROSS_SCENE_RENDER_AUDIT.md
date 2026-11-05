# 非开发 Player 跨场景画面对照

使用原始纯包 A/B 的审计副本，在同一台 Windows 机器、RTX 3060、D3D12、1280×720 和各包原有画质配置运行。每个副本仅附加取证程序集和两份加载注册。产品程序集、资源、场景和可执行文件保持各自原始 SHA256。另用字节不变的两套纯包副本验证标题启动和退出。 [哈希边界](Evidence/Audit/release-protection.json) · [纯 A](Evidence/PureBootA/pure-runtime.json) · [纯 B](Evidence/PureBootB/pure-runtime.json)

副本通过正式 Continue 路径加载独立合成档。营地实景样本关闭背包，遗迹使用门已开启的既有快照。取证驱动在初始化后设置相同机位与帧等待条件，固定 captureDeltaTime 为 1/60，暂停游戏时钟，于帧末读取实际 backbuffer。标题使用原有镜头。每个版本各运行三组营地与遗迹进程，共 12 个进程、42 张原始机位截图。首轮只用于探索，最终两轮另外提供 A/A、B/B 和四组交叉比较。

| 机位 | 最终两轮 A/B 变化像素，分母 921,600 | A/A、B/B 的 RGB MAE | 四组 A/B MAE 范围 |
| --- | ---: | --- | --- |
| 标题 | 0 / 0 | 0 / 0 | 0 |
| 营地 | 41,208 / 38,481 | 0.08207 / 0.04543 | 0.01898–0.08522 |
| 遗迹入口 | 37,204 / 37,036 | 0.02485 / 0.02428 | 0.02426–0.02476 |
| 石柱广场 | 25,841 / 25,890 | 0.01656 / 0.01640 | 0.01631–0.01693 |
| 机关走廊 | 48,457 / 48,404 | 0.03168 / 0.03092 | 0.03069–0.03159 |
| 地下祭坛 | 72,956 / 71,414 | 0.05719 / 0.05668 | 0.05536–0.05747 |
| Boss 大厅 | 22,177 / 22,663 | 0.01450 / 0.01472 | 0.01417–0.01475 |

MAE 为 RGB 每通道平均绝对误差，通道范围 0–255。标题最终四次截图像素一致，首轮 A/B 曾有 1,927 个像素差异。六个场内机位的严格像素一致性 FAIL。同包复跑也出现同量级差异，交叉比较范围与同包范围重叠，当前样本不能将差异归因于包、配置写回或单一渲染过程。场内全面渲染等同性仍 UNRESOLVED。[复跑矩阵](Evidence/Audit/repeatability.json) · [首轮原始指标](Evidence/RenderComparison1/pixel-metrics.json) · [最终轮 2](Evidence/RenderComparison2/pixel-metrics.json) · [最终轮 3](Evidence/RenderComparison3/pixel-metrics.json)

最终两轮的四份运行记录在每个机位均一致，范围包含相机姿态、矩阵、光照与雾、URP 资源、后处理开关和 Volume 覆盖、视锥内材质与 Shader、局部和全局关键字、Pass 数，以及纹理槽和格式元数据。R3 中可匹配的 1,178 项 Shader/Pass/API 裁剪统计也一致。每次 GPU draw 实际选中的变体及完整纹理像素级内容本轮未抓取。[营地 TSV](Evidence/Frames-A-camp-2/camp.tsv) · [大厅 TSV](Evidence/Frames-A-ruins-2/guardian.tsv) · [全部原始图和差分](Evidence/INDEX.md)
