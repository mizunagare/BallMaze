# PRIVACY-A 交付

起点cc9b73679458b0b868d875890a16b4c5238fb878；分支fix/privacy-release-diagnostics-disabled，从产品基准创建，未合并调查分支或main。最终SHA以本提交及远端核对为准。

正式入口WanxiangBuild现在明确使用WindowsRelease Profile，Diagnostics Disabled。新增ReleaseDiagnosticsGuard（Editor程序集）拒绝错误/默认Profile，并在真实BuildPipeline前后验证原生桥、输入SHA、新输出和Bee五服务；仅成功后签发发布回执。[保护合同](BUILD_GUARD.md) · [Profile](RELEASE_PROFILE.md)

## 本轮实际证据
- Build2：非开发None，Succeeded，0错误96警告。完整Unity日志保留全部警告与退出时JobTempAlloc诊断；不以退出码推断无引擎问题。
- Bee：EnableUnityConnect/CrashReporting/Insights/Analytics/PerformanceReporting均false。
- 纯程序集：无CP03、BR2、Privacy验证驱动，无UnityEditor引用；外部NativeProbe仅启动器使用，未加入发行包。
- GuardTests 17 PASS；发布回执文件测试4 PASS；最终真实BuildPipeline负例5 PASS。前一轮真实负例4 PASS亦保留，不重复计为新增覆盖。缺失与开启五字段逐项拒绝，Profile与旧输出及NativeReenabled在真实构建中拒绝。
- 纯Player在独立合成存档根实际启动，普通后台WM_CLOSE后exit0，无超时/强杀。这不是原生退出/菜单操作验收。
- 其余受保护2329项基线，除获准WanxiangBuild入口外无意外变化；CombatAim SHA为9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a，与CP04-B相同。

## 不得宣称通过
菜单实际交互、四武器、战斗、存档读取、暂停恢复本轮未执行：NOT_RUN，不能继承历史PASS。人工体验与原生键鼠NOT_RUN。全部外部诊断路径UNRESOLVED：CrashHandler/操作系统路径并未由五字段和端点快照排除。未实现授权UI和三个自有诊断模块。

首次隔离非batch Editor编译因测试夹具依赖不全停在Safe Mode；普通关闭工具未找到允许的顶层主窗口，未强杀。进程33348在封存时仍存在，不宣称已回收。补齐依赖后使用另一隔离副本batch运行成功。[失败历史](FAILURE_HISTORY.md)

当前是构建配置交付，不是完整游戏功能或隐私端到端验收通过。完成推送后暂停，等待独立复审。[验收](ACCEPTANCE.md) · [原始证据](Evidence/INDEX.md)
