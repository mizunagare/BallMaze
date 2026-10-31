# CP03 独立复审整改交付

开始基准与开工远端：`72db192a527bd256e2ba18cd7ab334d8334051da`。从该提交建立独立 `fix/cp03-review-r1`，最终完整整改 SHA 由本报告所属提交和交付回复绑定。**不推送 main，不合并；交付后暂停。整体验收 BLOCKED。**

## 已修复并验证

1. `Invoke-Runtime.ps1` 不再把 status!=PASS 一律 FAIL。新只读分类器验证格式、缺件、空结果、未知状态、重复 JSON key/断言、帧/时间、冻结 293 项完整性，分开记录真实进程、断言和整体。UNRESOLVED 保持原值，整体 BLOCKED/exit2；缺证 INCOMPLETE/3；真实失败 FAIL/1；全部强制项通过才 PASS/0。
2. `Audit-Locked.py` 不再宽泛删除 MeleeTrace 整行。固定 3 处完整行替换、1 处锚点插入，逐处数量/位置/内容断言和完整正文相等；13 锁定源码、采样区段及 24 组真实发射坐标/方向验证不变；唯一新增暂停箭另列。合成额外玩法/重复 Trace/时钟/弹体身份等负例自动拒绝。
3. Editor 适配器及一致性检查将原始进程结果与统一语义报告关联。原始 CP03 JSON/失败/输入不修改，旧 Runtime2 只读重审另存。

[修改与审计细节](TEST_AUDIT.md) · [复跑](TESTING.md) · [完整验收](ACCEPTANCE.md)。产品 Assets/Packages/ProjectSettings 相对基准无 Git 变化，没有修改玩法/数值/CombatAim/MeleeGeometry/弹速/AI/经济/随机/v9 或引入资源、依赖、CI。

## 本轮实际结果（分层，不相加为通过率）

| 验证集合 | PASS | FAIL | UNRESOLVED | 实际退出/整体 |
|---|---:|---:|---:|---|
| 最终工具自测 | 50 | 0 | 0 | exit0；负例拒绝另存 |
| 报告/进程/输入一致性 | 20 | 0 | 0 | 一致性 PASS，不是产品通过 |
| EditorFinal | 291 | 0 | 2 | Editor exit0 / 整体 BLOCKED，分类器及宿主 exit2 |
| EditorDiagnosis | 291 | 0 | 2 | Editor exit0 / 整体 BLOCKED；仅增加只读观测 |
| RuntimeFinal 非开发验收 Player | 291 | 0 | 2 | Player exit0 / 整体 BLOCKED，分类器及宿主 exit2 |

[汇总](Evidence/result-summary.json)保留每次原身份、超时 false、forcedTermination=false 及真实过程回执；没有用进程消失判断成功。[原始 Editor](Evidence/EditorFinal/CP03Editor.Run.exit.json)、[Player](Evidence/RuntimeFinal/CP03Runtime.exit.json)。本轮同样保留 Editor/Runtime 首次成功矩阵与早期工具失败，不覆盖旧记录。

非开发验收 Player 使用原 AcceptanceBuild2 不可变二进制，正常 Boot/Title 后受控 Continue 原合成检查点，再使用真实公开战斗 API 运行矩阵。不是原生键鼠/正常 AI 冒险/人工试玩；未新构建，也未宣称新的纯发行验收。exe/UnityPlayer/程序集哈希与 1,147 个冻结产品输入绑定见 [BASELINE](BASELINE.md)。

## 法杖只读调查与等待授权

两项近距仍 hpLoss=0，保持 UNRESOLVED。新的三维记录确认：相机命中目标，但意图表面相对真实杖首沿相机方向投影为负，触发防倒射回退；实际弹体沿相机平行方向偏离目标，观察窗口无碰撞/目标 Damage。不是关闭 Collider 或注入 Damage 后的伪造结果。[根因、几何、限制及提案](ROOT_CAUSE.md)。CombatAim 未改，修复必须单独授权；不能把找到原因等同于修复通过。

## 未执行与遗留

- CPU Main Thread、GC Alloc、GPU Frame Time、Particle System、池动态开销、声道、加载卸载、长时间资源趋势全部 NOT_RUN；没有真实 Profiler 基线/最终对照，不报告 0 或性能良好。[专项方案](PERFORMANCE.md)。
- 原生 U16、独立人工观感/可读性/音质/最终打击感 NOT_RUN。受控自动化不代替。
- 新 Editor 日志出现 SearchDatabase 内部异常，原始上下文保留；UNKNOWN/C15/青色帧/Search/JobTempAlloc 历史根因仍 UNRESOLVED，不以 exit0 清除。
- 最初两个自测试工具实现错误、绑定脚本编码/路径问题、CRLF 检查和宿主退出传播异常全部保留，[失败历史](FAILURE_HISTORY.md)。

## 用户与历史保护

主工程用户场景、ProjectSettings、Recovery、全部原 CP03 Evidence 共 1,802 个文件原/后 SHA 一致，原 Git 状态未变。独立新根仅合成存档，未关闭用户程序、抢桌面或强杀进程。发布日志只遮盖凭据值，完整原日志留在隔离根，异常不删除，发布 manifest 同时记录原字节与发布字节哈希。[证据索引](Evidence/INDEX.md)。

提交/推送独立分支仅供复审，不代表已获独立认可，不自动开始任何后续批次。
