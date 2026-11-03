# 证据索引

Raw/manifest.json记录每项原始SHA与脱敏发布SHA。日志gzip；不上传可执行文件、真实存档、Library或用户文件正文。

- [构建日志](Raw/Build2/Unity.log.gz)、[Bee](Raw/bee-disabled.json)、[文件哈希](Raw/release-files.json)、[程序集](Raw/assembly-audit.json)。
- [17项检查](Raw/GuardTests/guard-tests.json)、[5个真实构建负例](Raw/RealNegatives2/real-negatives.json)、[4个发布回执测试](Raw/marker-tests.json)。
- [纯Player](Raw/DisabledPlayer/runtime-result.json)、[保护](Raw/protection.json)。
- Build1保留首次失败和未关闭SafeMode状态；不冒充原生操作。真实发行可执行文件在本机隔离根I:/WGCombat/PRIVACYA-1103-A/Build2/Release，按manifest核验。
