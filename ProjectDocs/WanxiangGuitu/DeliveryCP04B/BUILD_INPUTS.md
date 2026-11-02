# 构建输入保护与不确定性

源产品工作树与用户文件受保护：2329项中仅获准的整改树CombatAim.cs变化；用户原有ForestRuins/ProjectSettings/Recovery状态不变。main和历史分支不修改。

隔离工程经过Editor/BuildPipeline后，1163项原产品文件中1158与源工作树完全一致，以下5项不同：

- Assets/Settings/PC_RPAsset.asset：新增序列化字段、shader预过滤缓存值变化。
- Assets/Settings/UniversalRenderPipelineGlobalSettings.asset：runtime settings列表写回。
- ProjectSettings/GraphicsSettings.asset：新增序列化字段和shader build设置。
- ProjectSettings/ProjectSettings.asset：中文字符串的YAML转义写回。
- ProjectSettings/UnityConnectSettings.asset：m_Enabled从0到1。

所有差异仅在工程外测试副本，未拷回、未提交到产品/用户工程。两侧原始文本、unified diff、SHA全部保存BuildInputDrift。没有恢复副本再谎称构建时输入相同。包清单、锁文件、场景、战斗源码等其余文件无对应差异。

目前没有每个BuildPipeline读取瞬间的全输入冻结钩子，不能仅凭构建后的写回文件判定它们在编译/打包哪个时刻生效，也不能从功能PASS推导其无影响。**构建输入逐字节等同性UNRESOLVED**；需要后续单独审核这些Unity序列化/构建生成项及可复跑冻结策略，不擅自修改产品配置以追求全绿。

最终BuildShippingInput两个构建各自保存CombatAim.executed.cs.txt、测试驱动执行源、原始BuildReport消息、Unity日志、EXE/UnityPlayer/程序集SHA及PE类型检查。构建选项均None；纯发行宏中不包含CP04B_ACCEPTANCE。
