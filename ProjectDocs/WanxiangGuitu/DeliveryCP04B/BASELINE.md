# CP04-B 基准与保护

产品起点/main：`72db192a527bd256e2ba18cd7ab334d8334051da`；调查参考`5ed519b00d1ba18084c0eaaa4e45e80dd71d7f31`。独立分支`fix/cp04-staff-near-aim`直接从产品基准创建，没有合并调查分支。调查目录只读复制在工程外Reference，未并入本分支。

工作树H:/unity/WanxiangGuitu-CP04；测试根I:/WGCombat/CP04B-1102-A。Unity6000.6.5f1与原依赖不变；未新增CI或素材。产品唯一修改Assets/CombatPrototype/CombatAim.cs。用户工程H:/unity/WanxiangGuitu的ForestRuins.unity、ProjectSettings.asset、Recovery及原工作区状态保留；其余产品/用户文件哈希保护清单共2329项，仅整改树中获准CombatAim不同。

27个真实进程：18次Editor（包含对照、诊断、6次构建）与9次非开发验收Player（7套主验证及2套运行器控制）。进程均exit0、未超时、不强杀；API驱动不冒充原生键鼠、正常AI或人工体验。旧失败/历史UR不改写。

所有1163项原产品输入已与隔离副本核对：1158匹配，构建后5项配置有Unity写回差异，单列UNRESOLVED输入等同性。它们未写回、未提交到产品或用户工程，不能据此宣称全部构建输入逐字节等同。见BUILD_INPUTS.md。

冻结输入/执行副本、命令、日志、构建消息及二进制SHA见Evidence。最终SHA以固定提交链接及交付回复为准；推送不是独立审核认可。
