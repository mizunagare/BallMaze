# 独立技术验收

本表：17 PASS / 0 FAIL / 8 NOT_RUN / 3 UNRESOLVED。整体待复审，不能写为全部通过。过程历史存在失败，未纳入当前有效断言的0 FAIL掩盖历史。

| ID | 标准 | 状态 | 证据 |
|---|---|---|---|
| A01 | 基线、独立研究分支，main未更改 | PASS | [REPORT.md](REPORT.md) |
| A02 | 2413项正式产品/用户文件哈希 | PASS | [Evidence/protection.json](Evidence/protection.json) |
| A03 | 199项供应商源码未改 | PASS | [Evidence/protection.json](Evidence/protection.json) |
| A04 | 90项上批自有资源未改 | PASS | [Evidence/fixture-comparison.json](Evidence/fixture-comparison.json) |
| A05 | 启动前3GB内存门槛、无强杀 | PASS | [Evidence/Audit3/resources.json](Evidence/Audit3/resources.json) |
| A06 | 修正后的Profile实际场景列表 | PASS | [Tests/MT03Editor.cs.txt](Tests/MT03Editor.cs.txt) |
| A07 | Windows64非开发研究构建 | PASS | [Evidence/build-summary.json](Evidence/build-summary.json) |
| A08 | 邻接/高度/两向法线/固定视角对照 | PASS | [SEAM_ANALYSIS.md](SEAM_ANALYSIS.md) |
| A09 | 原高亮条带材质原因与真实Player对照 | PASS | [SEAM_ANALYSIS.md](SEAM_ANALYSIS.md) |
| A10 | Player总Native/分配漂移完整归因 | UNRESOLVED | [MEMORY_ANALYSIS.md](MEMORY_ANALYSIS.md) |
| A11 | 活动场景对象卸载、稳定实体集合 | PASS | [Evidence/runtime-summary.json](Evidence/runtime-summary.json) |
| A12 | 已知TerrainData保留/释放控制 | PASS | [Evidence/Audit3/results.json](Evidence/Audit3/results.json) |
| A13 | 空场景Shader编译栈定位 | PASS | [Evidence/job-stacks.json](Evidence/job-stacks.json) |
| A14 | JobTempAlloc原生释放根因与关闭 | UNRESOLVED | [JOBTEMPALLOC_ANALYSIS.md](JOBTEMPALLOC_ANALYSIS.md) |
| A15 | 官方下载包和源码/旧meta来源 | PASS | [VERSION_PROVENANCE.md](VERSION_PROVENANCE.md) |
| A16 | 供应商确认三个版本标签维护原因 | UNRESOLVED | [VERSION_PROVENANCE.md](VERSION_PROVENANCE.md) |
| A17 | 257分辨率四块确定性哈希 | PASS | [Evidence/Audit3/results.json](Evidence/Audit3/results.json) |
| A18 | 四个Player进程32轮加载生成卸载 | PASS | [Evidence/runtime-summary.json](Evidence/runtime-summary.json) |
| A19 | Editor独立8轮加载生成卸载 | PASS | [Evidence/EditorPlay1/results.json](Evidence/EditorPlay1/results.json) |
| A20 | 可靠逐调用GC正/零计数 | NOT_RUN | [PERFORMANCE.md](PERFORMANCE.md) |
| A21 | GC.Alloc事件正/零校准 | NOT_RUN | [PERFORMANCE.md](PERFORMANCE.md) |
| A22 | 非开发Player GPU负载校准 | NOT_RUN | [PERFORMANCE.md](PERFORMANCE.md) |
| A23 | Editor GPU负载与恢复校准 | PASS | [Evidence/EditorPlay1/gpu-status.txt](Evidence/EditorPlay1/gpu-status.txt) |
| A24 | 精确Native分配调用栈/内存全账 | NOT_RUN | [MEMORY_ANALYSIS.md](MEMORY_ANALYSIS.md) |
| A25 | 当前运行时OS私有/工作集可靠计数 | NOT_RUN | [MEMORY_ANALYSIS.md](MEMORY_ANALYSIS.md) |
| A26 | 原生输入、人工美术/试玩 | NOT_RUN | [REPORT.md](REPORT.md) |
| A27 | 独立战斗性能预算/最终性能验收 | NOT_RUN | [PERFORMANCE.md](PERFORMANCE.md) |
| A28 | 正式地图集成 | NOT_RUN | [REPORT.md](REPORT.md) |

有效运行逐层统计：Player四进程186 PASS/0 FAIL/10 NOT_RUN；Editor61 PASS/0 FAIL/2 NOT_RUN。分项重复运行不等于新增独立能力。旧历史、原始异常和失败试验见FAILURE_HISTORY，不因进程exit0、PNG存在或计数器返回0认定整体成功。

未授权正式集成，因此A28是范围外未执行，不是缺陷。全部未解决项有实际数据和下一步所需证据，不用自动化代替人工体验。推送不等于独立复审认可。
