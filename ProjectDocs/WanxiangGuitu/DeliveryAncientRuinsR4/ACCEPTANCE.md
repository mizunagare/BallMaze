# R4 验收

| 项目 | 状态 |
| --- | --- |
| 两套固定原始构建、相同发行配置与产品树 | PASS |
| 五文件真实写回路径、阶段及前后值 | PASS |
| 原生 EditorBuildSettings/GraphicsSettings 精确写回调用 | UNRESOLVED |
| 仓库原始跟踪输入保持逐字节不变 | FAIL |
| 两套 resources.assets 逐字节一致 | FAIL |
| 对象清单、键索引、依赖和全部差异字节归因 | PASS |
| 运行时资源加载与两个换位 TextAsset 的内容 | PASS |
| 两套完整发行包逐字节一致 | FAIL |
| 非开发、五项服务关闭、无审计驱动、纯包实际启动和退出 | PASS |
| 全面构建输入与所有渲染及运行行为等同 | UNRESOLVED |
| 遗迹玩法重跑、原生输入、人工体验、最终平衡 | NOT_RUN |

产品输入与历史证据保护核对通过。候选继续等待独立复审。
