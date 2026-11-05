# CP06-C1-R5 验收

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| 两项原生写回的调用来源、阶段与配置差异 | PASS | [原生审计](NATIVE_SETTINGS_AUDIT.md) |
| EditorBuildSettings 场景列表及顺序一致 | PASS | [完整 YAML](NATIVE_SETTINGS_AUDIT.md) |
| GraphicsSettings 写回对发行行为的独立因果影响 | UNRESOLVED | [原生审计](NATIVE_SETTINGS_AUDIT.md) |
| 七机位真实非开发 Player 截图及复跑对照 | PASS | [跨场景审计](CROSS_SCENE_RENDER_AUDIT.md) |
| 标题最终两轮像素一致 | PASS | [复跑矩阵](Evidence/Audit/repeatability.json) |
| 营地和遗迹五机位严格像素一致 | FAIL | [差异数据](CROSS_SCENE_RENDER_AUDIT.md) |
| 七机位已记录的相机、光照、材质、纹理和渲染设置一致 | PASS | [运行时 TSV](Evidence/INDEX.md) |
| 每个 GPU draw 的 Shader Variant 与完整纹理内容 | NOT_RUN | [取证范围](CROSS_SCENE_RENDER_AUDIT.md) |
| 两包跨场景渲染语义完全等同 | UNRESOLVED | [同包和交叉对照](CROSS_SCENE_RENDER_AUDIT.md) |
| 五项运行时文件差异归因 | PASS | [发行等同性](RELEASE_SEMANTIC_EQUIVALENCE.md) |
| 发行运行时文件逐字节一致 | FAIL | [实际哈希差异](Evidence/Audit/release-differences.json) |
| 原始两包完整保留，非开发、无取证驱动，Bee 五项关闭 | PASS | [发行保护](Evidence/Audit/release-protection.json) |
| 纯包实际标题启动与后台关闭 | PASS | [纯包运行](Evidence/INDEX.md) |
| 用户文件、历史证据及产品输入保护 | PASS | [保护核对](Evidence/Audit/protected-inputs.json) |
| 遗迹玩法矩阵重跑 | NOT_RUN | 本轮只审计构建与渲染 |
| 原生键鼠、人工体验 | NOT_RUN | [纯包运行边界](RELEASE_SEMANTIC_EQUIVALENCE.md) |

合计 9 PASS、2 FAIL、3 NOT_RUN、2 UNRESOLVED。严格失败项与未解决项保留，等待独立复审。
