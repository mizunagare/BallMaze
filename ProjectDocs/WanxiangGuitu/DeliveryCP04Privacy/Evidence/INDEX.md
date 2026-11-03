# CP04-PRIVACY 证据

独立原件根`I:/WGCombat/CP04PRIVACY-1103-A`。[manifest](Raw/manifest.json)记录源SHA、发布SHA与脱敏；脱敏日志不声称能还原原件，原件留本机。未发布真实存档、用户个人目录或Unity安装二进制。

- [真实BuildReport](Raw/DisabledBuild/build.json)、[Profile资产证据文本](Raw/DisabledBuild/DiagnosticsDisabled.asset.txt)、[构建前](Raw/DisabledBuild/before-build.json)、[构建后](Raw/DisabledBuild/after-build.json)、[UnityConnect不变](Raw/DisabledBuild/connect-unchanged.json)。
- [官方UI对应setter IL](Raw/official-ui-setter-il.json)、[6.6实际枚举/API](Raw/profile-api-details.json)、[最终Bee](Raw/bee-disabled.json)、[190文件SHA](Raw/release-files.json)、[纯程序集](Raw/assembly-audit.json)。
- [第一轮实际运行](Raw/DisabledPlayer/runtime-result.json)、[主进程观测](Raw/DisabledPlayer/endpoint-observations.json)、[第二轮含子进程](Raw/DisabledPlayerChildAudit/endpoint-observations.json)、[分层汇总](Raw/runtime-summary.json)。各目录command、desktop、exit、Player.log.gz保留。所有原生/人工项目NOT_RUN。
- [模型12项](Raw/model-results.json)、[源码网络词法扫描](Raw/product-network-source-scan.json)、[无网络强制沙箱说明](Raw/isolation-capabilities.json)、[文件保护](Raw/protection.json)、[历史分支](Raw/remote-baseline.txt)。

[调查](../UNITY_NATIVE_DIAGNOSTICS.md) · [架构](../CONSENT_ARCHITECTURE.md) · [数据](../DATA_INVENTORY.md) · [负例计划](../SECURITY_TEST_PLAN.md) · [验收](../ACCEPTANCE.md)。仅调查副本创建Profile，仓库产品Assets不变。
