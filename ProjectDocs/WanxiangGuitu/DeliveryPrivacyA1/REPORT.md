# PRIVACY-A.1

开始基准c6473b1832a545a5d348e26220fafa73cca741ac。独立分支fix/privacy-release-diagnostics-disabled-r1；最终SHA以GitHub固定提交为准。main保持72db192a527bd256e2ba18cd7ab334d8334051da。

补上实际BuildReport Windows64及.exe输出校验，将前后回调和Publish绑定同一实际报告，固定批准Profile内容哈希，取消预检删除历史回执。唯一产品变化为Editor构建保护；其余变更是本独立交付目录。

[实现与合同](BUILD_GUARD.md) · [验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [原始证据](Evidence/INDEX.md)

测试不继承旧PASS：17项既有保护、5项原始真实BuildPipeline负例、4项发布回执检查均在本轮重新执行；新增6项验证错误平台、输出类型、旧完整/孤立回执、真实已批准发行回执，以及Profile内容篡改。每项保留实际结果和具体拒绝理由。

正向构建和五项Bee证据见证据索引。复用副本正向构建成功后发现其全局EngineDiagnostics字段来自上一批测试夹具；另从仓库重新复制Assets/Packages/ProjectSettings形成CleanProject，使用已有Library缓存仅加速编译，重新构建，记录输入及哈希，不把旧副本当作干净输入。

原生键鼠、人工体验NOT_RUN，CrashHandler/操作系统外部诊断路径UNRESOLVED，历史引擎问题和旧失败未关闭。此次不是产品战斗或完整隐私端到端验收。完成推送后暂停等待独立复审，不合并main。

最终干净正向构建CleanRelease：Succeeded，None，0错误2警告；实际Bee五字段false，193个发行文件SHA归档。最终32项自动化PASS（17+5+4+6），首次编译失败另列。构建使用缓存，警告数量不代表旧警告已修复。其余历史构建输入等同性、原生/人工及外部报告路径未因本批关闭。
