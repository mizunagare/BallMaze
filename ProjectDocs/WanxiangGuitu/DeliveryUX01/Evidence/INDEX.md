# 证据索引

- [固定版本](Preparation/version-lock.json)：仓库审查上下文、原构建记录HEAD、产品来源、覆盖层边界、分辨率/画质/19键默认配置。
- [发行完整191文件](Preparation/release-files.json)，[完整合成集合4文件](Preparation/fixture-files.json)。本次不上传二进制包或另复制进度内容。
- [1152项产品输入](Preparation/source-files.json)，[用户保护五项哈希](Preparation/protected-inputs.json)，[交付前再次核对](Preparation/protection-check.json)。只发布哈希，不发布用户场景内容。
- [首次14项准备工具自测](Preparation/tool-selftest.json)、[最终14项复验](Preparation/tool-selftest-final.json)，[PowerShell静态解析](Preparation/powershell-parse.json)。没有启动Player，不能作为人类或原生UI证据。
- [初始失败stderr](Preparation/initial-failure.stderr)；stdout为空，原样保留。失败原因与修复见FAILURE_HISTORY。
- [空白模板](../Templates/)：包含本机准备位置，仅为未分配计划，不能视为完成的参与者记录。
- [收到的复审任务](../Reviews/REVIEW_AND_TASK.md)。原R1发行剔除证明：`DeliveryCombat01R1/Evidence/Run-1028-112303/ProductIdentity/proof-Release-reused-identical.json`；原完整集合清单：该Run的Attempts/113617-Observe-1607f9/storage-after.json。

本机准备根`I:/WUX01/1028-140121-e5720e`。本次无原生录屏、人工操作截图或新增正常AI证据；对应NOT_RUN。所有游戏运行证据仍属于旧固定SHA材料，不继承新PASS。
