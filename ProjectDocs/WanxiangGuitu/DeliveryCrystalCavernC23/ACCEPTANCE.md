# C2.3 分层验收

本批是内部开发候选，不是独立审核通过或正式发行全项通过。

## 本轮实际运行统计

| 层 | 独立进程 | PASS 断言 | FAIL 断言 | 说明 |
|---|---:|---:|---:|---|
| Editor 最终主矩阵及补充 | 17 | 536 | 0 | 主矩阵14 + 导航失败/危险区/死亡3 |
| 非开发测试 Player 最终及补充 | 20 | 625 | 0 | 主矩阵14 + 上述3 + 连续流程/新进程入仓/岸壁路线3 |
| 无驱动纯发行包 | 1 | 单独回执 | 0 | 标题呈现、合成档不变、真实退出；非原生游戏交互 |

最终断言合计 **1161 PASS / 0 FAIL**。这不是整个项目“1161 全通过”：人工及性能缺口未被做成虚假 PASS，历史失败另列。原始两次 legacy-c22-original-prefab FAIL（Editor/Player）与初版画面问题、编译/工具失败全部保留。详见 [final-results.json](Evidence/final-results.json)、[FAILURE_HISTORY.md](FAILURE_HISTORY.md)。每个最终进程都核对退出0、无超时、complete标记及非空断言结果。

## 功能与保护

| 项目 | 结果 | 证据 |
|---|---|---|
| 显式 C2.3 9/12 固定资源与稳定来源 ID | PASS | StoreVerified/run-identity.json、源码映射 |
| 两条环湖路线实际双向连通、未开桥返回 | PASS | EditorRoutesVerified、PlayerRoutesAudited、route-measurements.json |
| 可见岸壁、深水无导航、角色真实碰撞阻挡 | PASS | actual-controller-stops-at-visible-bank、deep-water-no-nav、路径/AI采样 |
| 南岸普通巡守正常 AI、实际承伤/命中和退出 | PASS | InnerVerified/ai.tsv、health.tsv、enemy-health.tsv |
| 合法机关、门/导航同步、桥双向、重复拒绝 | PASS | StoreVerified/bridge-* |
| 导航拒绝后的闭门、返回与重试 | PASS | EditorNavFailure、PlayerNavFailure；预期错误日志保留 |
| 普通矿物实际采集及拾取、防重复 | PASS | StoreVerified、ContinuousAudited |
| 落地奖励 ID/种类/数量/装备属性跨进程恢复 | PASS | ResumeVerified/ground.txt 与断言 |
| 实际撤离、材料入仓、重复确认、新进程回执 | PASS | ResumeVerified、WarehouseVerified、ContinuousWarehouse |
| 新 Run 普通来源可重新获得 | PASS | RepeatVerified |
| 关闭桥门保存与新进程恢复 | PASS | ClosedVerified、ClosedResumeVerified |
| C2.1/C2.2/森林/遗迹旧在途定向恢复 | PASS | 两层 Legacy21/Legacy22/Forest/Ruins Verified |
| 七武器普攻/默认技能实际伤害与晶柱遮挡 | PASS | 两层 LiveVerified/combat.tsv；固定靶受控测试 |
| 旧危险区恢复/预警安全、真实翻滚、死亡卸载 | PASS | 两层 HazardFinal、DeathFinal；1HP死亡夹具单列 |
| 新材质支持与肩后实机截图、门前后表现 | PASS | PlayerStoreVerified/PlayerInnerVerified；只证明运行显示 |
| 非开发纯包、固定发行Profile、Bee五项关闭 | PASS | release-audit-PureBuild6.json，构建0错105警告 |
| 纯包标题与实际退出、合成文件不变 | PASS | PureBoot6/pure-runtime.json；WM_CLOSE不是人工菜单退出 |
| 受保护产品输入与5个用户未提交文件不变 | PASS | final-protection.json，1392项已有输入仅7项授权源码变化 |
| Resources.meta 内容/GUID/构建写回核查 | PASS | release-audit-PureBuild6.json，仅本次字节相同及引用扫描结论 |

## 不可替代的未执行与开放项

| 项目 | 状态 | 边界 |
|---|---|---|
| 原生物理键鼠 | NOT_RUN | API 驱动、截图、后台关闭均不能替代 |
| 独立人工体验与预警可读性 | NOT_RUN | 仍需真实玩家反馈 |
| 最终平衡 | NOT_RUN | 新地图增加普通供给，单样本不能证明平衡 |
| 经校准逐调用 GC | NOT_RUN | allocated memory 总量不是 GC Alloc |
| 经校准 GPU | NOT_RUN | 没有有效 GPU 帧采样 |
| 性能预算判定 | NOT_RUN | 无已批准阈值 |
| CPU帧/DrawCalls/加载卸载性能基准 | NOT_RUN | 本批只采对象、内存快照与正常路线时间，不冒充Profiler |
| GraphicsSettings 因果及发行语义等同性 | UNRESOLVED | 5项隔离写回仍在；不重启R4–R7相同调查 |
| 三个历史阶段指纹来源 | UNRESOLVED | 无新增因果证据 |
| JobTempAlloc | UNRESOLVED | 原始日志保留，没有过滤或引擎修改 |
| 原生内存漂移 | UNRESOLVED | 快照不证明泄漏或回收完成 |
| MapMagic版本标签差异 | UNRESOLVED | 本批未导入/修改供应商插件 |

上述功能/保护表 **19 PASS**，未执行表 **7 NOT_RUN / 5 UNRESOLVED**。历史 C1/R7 **7 PASS / 1 FAIL / 2 NOT_RUN / 2 UNRESOLVED** 原样保留，严格像素 FAIL 未关闭。历史项目与本轮分组不同，不机械相加作为“总通过率”。
