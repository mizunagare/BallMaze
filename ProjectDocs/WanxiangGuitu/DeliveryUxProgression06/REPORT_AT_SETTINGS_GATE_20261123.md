# UX-06 地区档案与复访引导

当前阶段：BLOCKED（构建后的受保护设置漂移；产品实现已形成，Player 未启动）。不是 UX-06 完成验收。

## 实际实现
- 从固定 UX-05 提交建立独立 worktree / feature/ux-progression-06-region-records。
- 营地冒险历程新增地区档案；IMGUI/uGUI 共用只读投影、行文与行高；地区切换、原目标历史地区筛选跳转与返回。
- 已发布存档独立回读；不读 Settlement.plan；保存失败/待核对时禁止入口。
- 森林真实首领回执/徽章；遗迹五项稳定ID与洞窟首奖分组；永久回执区分领取状态；历史名称快照、最近128覆盖说明与DATA_GAP。
- 原历史与地区预览共用保留历史排序。修正森林新武器来源唯一性误述。

## 验证
[T] 14个构造夹具通过，见 FIXTURE_RESULT.json 和 BUILD_02.log 的逐项记录；不代表真实出征。
[B] BUILD_01 包缓存 EEXIST 失败保留；BUILD_02 在隔离缓存解析成功，Unity 报 Succeeded / 0 errors / 113 warnings。Get-Process 观察器未取得真实 OS 退出码（null），不伪称已捕获0。
[B] EXE/DLL身份见 BUILD_02_IDENTITY.json。构建期间继续准备了共享行高/查询与驱动保护代码，因此该产物仅为准备构建，未用于验收；进入运行前仍需冻结最终源并重新构建。
[P] Player 0 条；九局、双UI、截图、发行构建排除测试工具仍 NOT_RUN。
[C] 原工作树分支/HEAD/index/status保持不变，非授权既有产品CS文件未变化，新meta GUID唯一，见 PROTECTION_AT_GATE.json / PREPLAYER_PROTECTION.json。

## 保护闸门
Unity首次导入/构建后六个受保护设置持久差异（四个ProjectSettings及两个URP资源）已归档于 SETTINGS_GATE/。原工作树对应六文件与开工SHA一致。没有自动恢复，没有重新构建，没有启动Player。
按根 AGENTS.md 的保护漂移暂停规则，等待负责人裁决 RECOVERY_PROPOSAL_6FILES.md。Packages未变，Schema/迁移/结算/奖励/RNG等源码未改；两个工作树均无暂存操作，未提交/推送/合并，未操作main。

UX-05 继续沿用 CONDITIONAL_PASS；F-02 = OWNER_ACCEPTED_HISTORICAL_LIMITATION，历史证据及结论未回写。
