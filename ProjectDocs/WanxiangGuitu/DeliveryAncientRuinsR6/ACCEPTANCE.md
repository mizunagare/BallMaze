# R6 验收

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| 两份原始发行包、R5 原始截图、历史证据、用户文件保护 | PASS | [哈希核对](Evidence/protection.json) |
| Development=false、Bee 五项关闭，原始包无本轮驱动 | PASS | [发行核对](Evidence/protection.json) |
| 七机位各包 10 次有效独立进程采集 | PASS | [采集结果](CAPTURE_REPEATABILITY.md) |
| PSO 设置写回值、两包序列化值与实际原生对象一致 | PASS | [字段审计](GRAPHICS_SETTINGS_IMPACT.md) |
| 选定机位的 Camera、Shader、材质、纹理、照明和 URP 结构化对照 | PASS | [对照](CROSS_BUILD_RENDER_COMPARISON.md) |
| 局部及全帧差异测量、场内阴影隔离 | PASS | [全量统计](Evidence/ComparisonFinal/summary.json) |
| 七机位的全帧跨包 MAE 上限处于同包范围 | PASS | [对照](CROSS_BUILD_RENDER_COMPARISON.md) |
| 七机位严格逐像素一致 | FAIL | [配对明细](Evidence/ComparisonFinal/metrics.json.gz) |
| 禁止 GraphicsSettings 写回的独立发行影响及缺字段的完整 Editor 内部默认值 | UNRESOLVED | [字段审计](GRAPHICS_SETTINGS_IMPACT.md) |
| 每次 GPU draw 的实际 Shader Variant | NOT_RUN | [取证边界](GRAPHICS_SETTINGS_IMPACT.md) |
| 活动后处理开关像素对照 | NOT_RUN | [相机分支](GRAPHICS_SETTINGS_IMPACT.md) |
| 人工体验、原生键鼠、遗迹玩法矩阵重跑 | NOT_RUN | 本轮只做固定场景渲染 |

合计 7 PASS、1 FAIL、3 NOT_RUN、1 UNRESOLVED。
