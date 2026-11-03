# 分项验收

|项目|结果|证据|
|---|---|---|
|固定Release Profile与正式入口|PASS|源码、RELEASE_PROFILE.md|
|真实Editor非开发构建|PASS|Raw/Build2/Unity.log.gz、summary快照|
|Bee五服务关闭|PASS|Raw/bee-disabled.json|
|BuildPipeline拒绝错误/Enabled/ProjectSettings/旧输出/重新启用|PASS|Raw/RealNegatives2/real-negatives.json|
|缺失/启用字段检查|PASS|Raw/GuardTests/guard-tests.json，17项|
|发布标记不匹配与旧输出|PASS|Raw/marker-tests.json，4项|
|UnityConnectSettings与Profile构建前后SHA|PASS|发布回执含pre哈希；post gate必须相等才发回执|
|纯发行程序集/文件SHA|PASS|Raw/assembly-audit.json、release-files.json|
|实际Player启动与普通关闭|PASS（进程层）|Raw/DisabledPlayer/runtime-result.json|
|菜单交互/战斗/四武器/存档读取/暂停恢复|NOT_RUN|本轮未执行真实业务输入；不可继承旧PASS|
|原生键鼠/人工体验|NOT_RUN|无操作者证据|
|所有外部诊断发送路径|UNRESOLVED|CrashHandler/OS仍待独立调查|
|用户文件与CombatAim|PASS|Raw/protection.json|

没有单一总PASS。先前FAIL、UNKNOWN和人工开放项保持原状态。未完成游戏功能回归不能被构建成功覆盖。
