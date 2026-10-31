# CP04-A 调查交付

产品基准：`72db192a527bd256e2ba18cd7ab334d8334051da`；独立分支 `investigate/cp04-staff-near-aim`。仅文档目录内调查工具、报告和证据；不改产品Assets，不合并main。

- 原历史矩阵：291 PASS、2 UNRESOLVED，进程exit0，语义BLOCKED/2。
- 扩展38案例 + 相机墙补充2案例均真实执行：38项中28有伤害/10无伤害，补充2项无伤害。它们是观测结果，不是“40项命中通过”。
- 原24组发射点/方向：24/24精确相同。
- 分析一致性6 PASS；最终独立核验16 PASS，无非预期产品异常断言。
- 2329项产品/用户保护文件、1163项隔离产品输入、5项历史原始证据均未变化。
- 工具曾出现UTF-8解码遗漏和包装器语法错误，均保留首次失败与修订结果；首轮未挡住相机的候选墙也保留。
- 两项法杖问题仍UNRESOLVED，已定位固定样本的几何原因，产品修复等待单独授权。
- 正式Player新运行、原生UI、人工体验、新构建与性能NOT_RUN；历史引擎问题未关闭。

[基准](BASELINE.md) · [根因](ROOT_CAUSE.md) · [相机几何](CAMERA_GEOMETRY.md) · [真实调用与轨迹](AIM_TRACE.md) · [复跑](REPRODUCTION.md) · [修复提案](FIX_PROPOSAL.md) · [验收计划](ACCEPTANCE_PLAN.md) · [证据索引](Evidence/INDEX.md)

交付后暂停等待固定SHA独立审核与修复授权。推送成功不等于通过审核。
