# R7 证据索引

隔离根 I:/WGCombat/C1R7-1106-A。原始纯包在 I:/WGCombat/C1R3-1105-A 的 ProjectA-Build/Release 和 ProjectB-Build/Release。二进制发行包、PDB、完整引擎反汇编和合成档正文保留在本机隔离根。发布清单记录原始与发布 SHA256，PNG 原图字节不变。[证据清单](manifest.json) · [保护和历史复核](Audit/protection.json)

| 样本 | A 标题和营地 | A 遗迹五区 | B 标题和营地 | B 遗迹五区 |
| --- | --- | --- | --- | --- |
| 1 | [画面及 GPU 轨迹](Frames-A-camp-gpu-1/) | [画面及 GPU 轨迹](Frames-A-ruins-gpu-1/) | [画面及 GPU 轨迹](Frames-B-camp-gpu-1/) | [画面及 GPU 轨迹](Frames-B-ruins-gpu-1/) |
| 2 | [画面及 GPU 轨迹](Frames-A-camp-gpu-2/) | [画面及 GPU 轨迹](Frames-A-ruins-gpu-2/) | [画面及 GPU 轨迹](Frames-B-camp-gpu-2/) | [画面及 GPU 轨迹](Frames-B-ruins-gpu-2/) |

- [进程批次](batch.jsonl.gz) · [GPU 阶段和计数](Audit/gpu-and-post.json.gz) · [包内 Shader](packaged-shaders.json.gz)
- [后处理对照图](Audit/post-contact-sheet.png) · [跨包像素差异](Audit/post-cross-package.json) · [相机和光照快照](Audit/scene-metadata.json)
- [GraphicsSettings 载荷](graphics-payload.json) · [Editor 匹配符号](editor-symbols.json.gz) · [Editor 字段偏移](editor-field-transfer.txt) · [原生初始化](Audit/editor-default-excerpts.txt) · [Player 匹配符号](player-symbols.json.gz) · [描述符来源](Audit/player-descriptor-excerpts.txt)
- [纯 A 标题](PureBootA-final/title-player.png) · [纯 A 回执](PureBootA-final/pure-runtime.json) · [纯 B 标题](PureBootB-final/title-player.png) · [纯 B 回执](PureBootB-final/pure-runtime.json)
- [验收](../ACCEPTANCE.md) · [失败历史](../FAILURE_HISTORY.md)

## 复跑

从冻结 A/B 包各复制两份到独立验证根。PureA/B 不注入驱动。RenderA/B 各自仅在 Managed 下添加 C1R7RenderProbe.dll，并在两份加载 JSON 注册 C1R7.RenderProbe.Run。RenderProbe.cs.txt 以原包 Managed 为引用，由安装的 6000.6.5f1 配套 Roslyn 编译。依赖 CoreModule、ScreenCaptureModule、ImageConversionModule、AnimationModule、PhysicsModule、ParticleSystemModule、UIModule、Core 与 Universal 渲染程序集及 Assembly-CSharp。通过 Invoke-Render.ps1 以 Gpu 参数交错运行 A/B 的 camp 与 ruins，Attempt 为 gpu-1 和 gpu-2。GPU 运行器使用本地 Frida 17.15.0、私有桌面和合成档。在可执行文件的 UnityPlayer.dll SHA 不匹配时拒绝应用内部偏移。纯包通过 Invoke-Pure.ps1 独立复跑。 [验证工具](../Tools/) · [Frida JS API](https://frida.re/docs/javascript-api/)

Inventory-Shaders.py 以 UnityPy 1.25.0 与 LZ4 对原包做只读解包。Compare-GPU-Post.py 以 NumPy 2.3.5 和 Pillow 13.0.0 读取 GPU 轨迹和截图。Read-Graphics.py 交叉检查发行 GraphicsSettings 载荷。Verify-Protection.py 复核原包、纯包副本、观测副本、R4 至 R6 的原始及发布文件和用户路径。所有运行证据留在新目录。
