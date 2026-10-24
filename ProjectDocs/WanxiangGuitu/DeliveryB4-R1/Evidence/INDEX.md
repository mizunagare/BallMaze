# B4-R1 证据索引

本轮统一评分：[规范与参数](../SCORING_V1.md)，证据单列`ScoringV1/`；历史地形FinalAll和Attempts不覆盖、不继承。ScoringV1下包含新增模型修复前失败、定向分项/顺序/实际路径、新进程恢复和本轮完整All。

统一评分最终本轮86PASS/2预期FAIL/19NOT_RUN/1UNRESOLVED，非预期FAIL0，详见[ScoringV1索引](ScoringV1/INDEX.md)。不要将下列83/2/19/1旧地形结果当作本轮评分验收。

入口及复跑：[REPORT](../REPORT.md)、[ACCEPTANCE](../ACCEPTANCE.md)、[TESTING](../TESTING.md)。最终运行与历史尝试分目录，不覆盖首次失败。

- `FinalAll/`：独立最终完整All，原始逐项JSON/CSV、命令/退出码/超时、完整日志归档、非开发构建、实际正常AI轨迹/存档审计及受控截图。发布后以该目录真实文件清单为准。
- 最终实际[逐项JSON](FinalAll/results.json)、[CSV](FinalAll/results.csv)、[完整编排报告](FinalAll/REPORT.md)、[83/2/19/1分类](FinalAll/classification.json)、[经济汇总](FinalAll/adventure-economy-summary.json)、[构建摘要](FinalAll/build-summary.json)、[全部警告行](FinalAll/build-warning-lines.json)、[构建文件哈希](FinalAll/build-manifest.json)。Windows启动器SHA256为`001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A`，UnityPlayer.dll为`3BDC6E4CD1B5EB85E1562B1C6018949145CDEDF50CF7ACEAB0D1518143F9AA7C`；完整游戏内容不能只用启动器哈希代表，以manifest的Assembly-CSharp/data文件核对。
- 30seed[实际导航长度](FinalAll/R1Diagnostics/Rules/r1-nav.csv)、[地形与布局](FinalAll/R1Diagnostics/Rules/r1-terrain.jsonl)、[路线边](FinalAll/R1Diagnostics/Rules/r1-edges.csv)、[离路采样](FinalAll/R1Diagnostics/Rules/r1-open-space.csv)、[岸线物理射线](FinalAll/R1Diagnostics/Rules/r1-shore.csv)、[最终与旧版52目的地对照](Audit/seed1-final-distance-comparison.csv)、[对照来源](Audit/final-provenance.json)。
- 实际受控[1280全景](FinalAll/R1Screens/r1-overview-1280x720.png)、[1920全景](FinalAll/R1Screens/r1-overview-1920x1080.png)、[湖岸](FinalAll/R1Screens/r1-lakeshore-1920x1080.png)、[路线说明](FinalAll/R1Screens/r1-route-details-1920x1080.png)、[尺寸/SHA](FinalAll/r1-screens.json)。逐张可见性检查通过，图形仍是简化矩形湖泊/岩脊，非正式美术。
- [初始输入来源](Provenance/Initial/source-build-provenance.json)：75个产品C#与隔离输入按CRLF归一后相等；完整Assets/Packages/ProjectSettings原字节另列，不把BOM或Unity重序列化差异隐藏。
- `Provenance/Final/`：最终编译/执行后的来源与输入核对、执行驱动哈希；原始ProjectSettings未提交。
- [Git暂存区证明](Provenance/git-index-proof.json)：75产品C#与隔离输入归一后一致，25份历史失败输入原始字节保留，禁止文件/用户ProjectSettings未暂存。[发布清单校验](publication-checks.json)：1232个清单条目哈希一致，1400个文本/归档条目扫描未发现已知令牌模式；许可参数另外核查均已脱敏，不宣称检测所有可能的秘密。
- [原世界审计对照](Audit/seed1-distance-comparison.csv)、[来源](Audit/provenance.json)：旧版与首轮prototype，非最终All混称。
- [隔离启动失误披露](launch-isolation-incident.json)：临时辅助调用直接隐藏Unity，桌面焦点影响未核实；后续原编排器启动前拒绝检查单独计证。
- [可逆缓存迁移](cache-moves.json)：仅已结束、明确owner的隔离Library，日志/源码/存档留原处，未动用户工程缓存。

## 历史尝试

`Attempts/`下目录名保留原唯一运行ID：

| 运行 | 原结果/用途 |
|---|---|
| 155011-917dbfcb | 修复前平面森林断言FAIL，真实路径先导出 |
| 155557-c070ec0d | 第一轮定向6PASS；含Editor.Search索引异常原日志 |
| 160023-43a0c368 | 2PASS/2FAIL；测试夹具的异Run修复回执正确被产品拒绝 |
| 160526-287fdaa0 | 4PASS/1FAIL；旧batch截图驱动deadline |
| 161214-3a04ca75 | C盘8GiB门槛预检FAIL，未降低门槛 |
| 161708-89d94233 | 首次D盘All：80PASS/3FAIL/19NOT_RUN/1UNRESOLVED，1非预期截图失败 |
| 161905-37d81e4a | 隔离辅助调用缺陷，隐藏Unity直接启动，exit1，无私有桌面回执 |
| 162606-edc5c84b | 私有worker截图完成但全景青色，不当作可用全景 |
| 163445-4fb6ab4f | 垂直全景仍青色，保留而不猜引擎根因 |
| 164009-08f4d825 | 斜俯视完成但farClip160裁剪远景 |
| 164407-7532e484 | 诊断镜头farClip500后可用全景，仍是岸线修复前 |
| 164906-f41cf90c | 真实岸边物理缺口FAIL |
| 165405-6c9a7ecd | 岸线修复后30不同seed/1364射线PASS，最终All仍独立重跑 |

发布内容不含真实玩家档、save.json、ground-loot分页、Library/Temp、可执行构建二进制或转储。合成布局与选定检查点摘要用于断言，不发布完整Profile。原始未脱敏日志留外部唯一测试根；仓库日志经原发布器白名单与脱敏处理，SHA/ZIP清单可核对。早期复用副本缺乏当时精确源码快照的事实保留，不用当前副本冒充。

UI-01历史65PASS/2预期FAIL/20NOT_RUN/1UNRESOLVED不改写。所有PNG均标注来源；受控截图不是原生U16或人工试玩。
