# UX-04-B2-R1 最终验收

最终采用 **A03 9/9 PASS，99/99检查PASS**，全部Player exitCode=0。buildId `ux04b2r1-6f876c60-b70442f9-5a2654de`。

| RunId（前缀UX04B2R1-A03-） | PID | 检查 | 关闭条件 |
|---|---:|---:|---|
| sort-ugui | 4372 | 22/22 | C-02：四种排序、过滤、ID稳定次序、真实按钮循环、滚轮到末项、底层不变 |
| sort-imgui | 2520 | 11/11 | C-02/C-03：同投影、Windows原生鼠标、标题无重复控件、真实切回uGUI序列一致 |
| strength0 | 32228 | 15/15 | C-05：真实出征、rank0、bonus0、装备8、AP33、preview157、角色/default/fallback截图 |
| strength3 | 14380 | 15/15 | C-05：rank3、bonus15、装备8、AP48、preview172；未写最终AP |
| preview9 | 3156 | 10/10 | C-06：8×9只读指纹，预览后真实装备可用 |
| guid | 14532 | 3/3 | C-04：三个合法GUID互异且无其它GUID碰撞 |
| golden | 32172 | 2/2 | 实时/统一D-24链回归；原B2完整黄金矩阵及6/6继续保留 |
| collection | 2120 | 20/20 | C-01/C-07：完整跨容器及分解生命周期，真实UI与API守卫分列 |
| restart | 7324 | 1/1 | C-07：新PID加载同角色同装备，收藏清空 |

具体PID、完整SHA256、exitCode、result和原始记录见 [PLAYER_RUN_MATRIX](<PLAYER_RUN_MATRIX.csv>) / [INDEX](<EVIDENCE/INDEX.json>)，无缺项。每Run的result/manifest/input-events/state-changes/observations单独存放。

## 必要人工确认

- [IMGUI最终画面](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/A03/sort-imgui/native-C03-kept-strip-sort-cycle.png>)：标题清晰，正常操作条仅一处。
- [uGUI攻击排序](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/A03/sort-ugui/r1-sort-key-AttackDesc.png>)：目录首项为神话长剑；[真实滚动末项](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/A03/sort-ugui/r1-sort-roster-bottom.png>)可读22/22。空间网格位置刻意不重排。
- 真实冒险场景既有IMGUI数值HUD：[Strength0攻击33](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/A03/strength0/r1-fallback-hud-strength-0.png>) / [Strength3攻击48](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/A03/strength3/r1-fallback-hud-strength-3.png>)。默认uGUI无攻击数字，不冒充。
- [人工记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A03-review.json>)独立于自动PASS。

## 独立门禁

[最终独立复算](<EVIDENCE/recompute-A03/summary.json>)：23211项＝23191 PASS、0 FAIL、20 INFO。INFO包括初始化前无hero的boot、未提供structured publishedIds的额外点击日志和非Main角色预览数值（不属于C-06只读关闭依据）。所有8条结构化排序序列及Main预览、九指纹与文件哈希均通过。

[最终保护核验](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/final-audit-A03/workspace-audit.json>)：11609文件、无缺失/未授权变化。[Git/构建状态](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/final-audit-A03/git-build-state.json>)：HEAD不变、staged为空、diff-check=0、166源构建后未漂移。

历史A01原生窗口FAIL、A02人工HUD不足与原有B2历史全部保留，不通过更名或覆盖伪装通过。仅最终A03作为七项关闭批次。
