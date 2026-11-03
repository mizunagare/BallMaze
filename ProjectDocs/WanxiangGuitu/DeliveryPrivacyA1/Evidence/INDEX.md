# 证据

工程外独立根I:/WGCombat/PRIVACYA1-1103-A。Raw/manifest.json记录原始SHA、发布SHA与脱敏；完整日志gzip，未上传可执行文件、Library或任何真实存档。历史证据目录未覆盖。

- [干净构建日志](Raw/CleanRelease/Unity.log.gz)、[BuildReport摘要](Raw/CleanRelease/WanxiangGuitu.exe.summary.txt)、[发行回执](Raw/CleanRelease/WanxiangGuitu.exe.release.json)、[Bee五服务](Raw/bee-final.json)、[193文件哈希](Raw/release-files.json)。
- [17项](Raw/GuardTests/guard-tests.json)、[5项原负例](Raw/OriginalNegatives/real-negatives.json)、[新增6项实际负例](Raw/R1Negatives/r1-negatives.json)、[4项回执测试](Raw/marker-tests.json)。
- [批准Profile合同](Raw/profile-contract.json)、[用户/产品保护与汇总](Raw/verification.json)、[新旧发行回执只读复核](Raw/release-verification.json)。
- [首次编译失败](Raw/ReleaseBuild/Unity.log.gz)、[复用副本构建](Raw/ReleaseBuild2/Unity.log.gz)。不能将这些目录与CleanRelease混为同次输入。

复跑：使用现有DeliveryEncounterAI01/Invoke-Check.ps1，在新的I:/WGCombat自有隔离副本和每次独立新Output目录依次执行PrivacyAValidation.Run、PrivacyAGuardTests.Run、PrivacyARealNegatives.Run、PrivacyA1Negatives.Run。独立Editor测试源码在Tests/*.cs.txt，勿加入Player程序集。新负例ExistingVerifiedRelease默认指向同根ReleaseBuild2/Release，复跑应明确对应本轮已批准构建。最后用Tests/MarkerTests.py <本轮根>与Tests/VerifyEvidence.py <本轮根>；这些固定路径需按新根显式配置，不能覆盖旧输出。
