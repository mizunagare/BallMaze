# 失败历史

- 首次生成 PowerShell 运行器因标量索引选中了错误的 String.Replace 重载，在启动前停止。修正后，首轮运行器又检测到自己位于默认桌面并主动拒绝启动 Player。后续改为私有桌面启动。[生成失败记录](Evidence/runner-prep-failure.txt) · [默认桌面拒绝](Evidence/Frames-A-camp-smoke/Runner.stderr.gz)
- 前两次 D3D12 取证看到队列提交和绘制，未完整关联场景 PSO。其中一轮还记录了错误的 COM 参数读取。随后使用精确匹配 Player 的 Unity 缓存前描述符并核对实际 COM 对象，末轮八个进程完整关联本次窗口的提交绘制。[第一轮轨迹](Evidence/Frames-A-camp-smoke2/gpu.jsonl.gz) · [第二轮轨迹](Evidence/Frames-A-camp-smoke3/gpu.jsonl.gz) · [验证轨迹](Evidence/Frames-A-camp-smoke4/gpu.jsonl.gz)
- RenderDoc 官方便携包下载在 80 秒时超时。本轮改用本地 Frida 与 Windows D3D12 路径，没有使用未下载完成的工具。[下载日志](Evidence/renderdoc-download.log.gz)
- 第一次纯包启动遇到低于 3 GB 的提交内存门槛，启动前即停止。随后在余量恢复后使用新目录重新完成两套纯包验证。[首次记录](Evidence/pure-first-attempt.txt)
- UnityPy 通用 GraphicsSettings 类型树未完整读出 864 字节。PSO 专项解析另与原生对象交叉核验。日志中的 Depth of Field 和 Panini 裁剪或不支持警告、严格像素 FAIL 和三项包内匹配缺失均保留。[读取差异](Evidence/graphics-payload.json) · [Player 原始日志](Evidence/Frames-A-camp-gpu-1/Player.log.gz)

- 保护检查首轮仍指向低内存挡下的旧目录，因缺少进程回执退出。改为引用两份成功复跑回执后重新核对。[检查失败](Evidence/protection-first-attempt.txt)
