# CP06-C1-R7 验收

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| 旧字段缺失、原生初始化与 Unity 写回区分 | PASS | [配置审计](GRAPHICS_SETTINGS_FINAL_AUDIT.md) |
| 两套非开发 Player 的实际九项 PSO 设置与启动路径 | PASS | [原生回执](Evidence/INDEX.md) |
| 七机位实际 D3D12 绘制 Shader Variant 与 A/B 对照 | PASS | [Shader 审计](SHADER_VARIANT_AUDIT.md) |
| 包内字节码与本次实际提交的使用集合分列 | PASS | [包内清单与匹配](SHADER_VARIANT_AUDIT.md) |
| 七机位 URP、光照与阴影行为证据 | PASS | [配置及场景](GRAPHICS_SETTINGS_FINAL_AUDIT.md) |
| 后处理开、关、再关的真实曝光效果 | PASS | [后处理实测](POST_PROCESSING_AUDIT.md) |
| 纯包实际启动与关闭、原包和历史保护、Bee 五项、非开发配置 | PASS | [保护记录](Evidence/Audit/protection.json) |
| 严格像素等同 | FAIL | [逐状态数据](Evidence/Audit/post-cross-package.json) |
| 三个实际阶段字节码的包内精确来源 | UNRESOLVED | [映射结果](Evidence/Audit/gpu-and-post.json.gz) |
| 独立去掉写回的因果影响与全面渲染语义等同性 | UNRESOLVED | [发行结论](RELEASE_EQUIVALENCE.md) |
| 其他后处理效果、图形 API 和原生人工验收 | NOT_RUN | 本轮仅测试 D3D12 固定机位曝光控制 |
| 已通过的遗迹玩法矩阵重跑 | NOT_RUN | 本轮只读渲染核查 |

合计 7 PASS、1 FAIL、2 NOT_RUN、2 UNRESOLVED。
