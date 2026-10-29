# BALANCE-AI-01 验收

开工77c4c8c3d11ac87b86ce8999cfb8dbd3e3cfdedf；源码冻结377c556312afd18a3d6af31135863755fe810eb5。本表为本轮证据归类，不是独立审核结论。总体 UNRESOLVED。

| ID | 项目 | 状态 | 依据 |
|---|---|---|---|
| A01 | 实际经验来源/HUD/终态审计 | PASS | PROGRESSION_BASELINE、Before02/runtime-baseline |
| A02 | 三候选与1～30曲线/估算 | PASS | PROGRESSION_CURVES、curve-model；模型不是Run实测 |
| A03 | 同一死敌/恢复死敌XP不重复 | PASS | Before03、TrackedReplay/RulesBaseline |
| A04 | v9旧等级/余量/技能/待选/三流新进程 | PASS | TrackedCompatibility、TrackedReplay/RulesResume |
| A05 | 8项真实负例最小修复 | PASS | Before03 5P8F→13P；状态图与13项跟踪复验 |
| A06 | 3seed×3独立Run有限配对 | PASS | MatrixBeforeFinal/AfterFinal各108，SummaryFinal/paired-check |
| A07 | 实际正常森林AI三进程 | PASS | TrackedFinal/Normal-Gather三退出回执与业务断言 |
| A08 | 受影响可枚举规则 | PASS | SummaryFinal/assertions：420P；不继承旧结果 |
| A09 | B3/B07经济及四进程状态 | PASS | Final/RandomStreams、BossEconomy、Boss-*及BossStore标记 |
| A10 | 前后实际预警画面 | PASS | VisualBefore/After 12图，受控Camera请求，非原生UI |
| A11 | 非开发构建/全部警告 | PASS | TrackedFinal/Build：None、0E96W，messages与warnings.csv |
| A12 | 构建/运行源码绑定与驱动剔除 | PASS | Bindings/source-bindings、code-commit-binding；PE检查 |
| A13 | 用户5文件与历史交付保护 | PASS | Bindings/protection-check；不公开/提交未提交场景 |
| A14 | 不改依赖/CI/经济/随机/地图/v9字段 | PASS | 8文件源码差异、110源码绑定及既有回归 |
| A15 | 提交、证据索引与发布完整性 | PASS | Git提交、Evidence/manifest与publication-check；最终远端完整SHA在交付回复核对 |
| N01 | 原生键鼠U16 | NOT_RUN | 无安全独立交互验收，本批不冒充 |
| N02 | 独立人工试玩/动态可读性 | NOT_RUN | 无独立玩家记录 |
| N03 | 最终平衡与长Run成长/资源压力 | NOT_RUN | 短窗/无药水消耗不足；高防御底伤1与单杀即撤未升级明确保留 |
| N04 | 完整性能测量 | NOT_RUN | 无本批基准，不以0计数代替 |
| U01 | UI01 D3D12 UNKNOWN | UNRESOLVED | 历史保留，无新因果证据 |
| U02 | Editor青色帧 | UNRESOLVED | 历史保留 |
| U03 | Editor.Search内部异常 | UNRESOLVED | 本轮旧夹具启动日志也出现完整调用栈 |
| U04 | JobTempAlloc | UNRESOLVED | 本轮日志仍归档，不过滤 |
| U05 | 旧C15根因 | UNRESOLVED | 没有因此关闭 |
| U06 | UX04旧GPU fatal | UNRESOLVED | 与本轮无图形渲染错误分开 |
| U07 | UX04旧AI phase31停滞 | UNRESOLVED | 后续成功不关闭首次根因 |
| U08 | 无图形RenderRequest原生崩溃的引擎内部原因 | UNRESOLVED | 启动配置已纠正，原exit -1073741819与调用栈保留，不试探改产品生命周期 |

验收条目：15 PASS / 0当前FAIL / 4 NOT_RUN / 8 UNRESOLVED。不是“全部通过”。执行历史另计28P/5F/1NOT_RUN及6正常AI进程；原始FAIL没有从历史删除。首次Final序列exit1仍保留，定向更正不改写它。A15只在实际暂存完整性和远端核对成功后交付，不以本表文字作为推送证明。
