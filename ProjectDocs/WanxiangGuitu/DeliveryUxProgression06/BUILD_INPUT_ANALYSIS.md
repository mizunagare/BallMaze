# 有效构建输入核验

开发工作树六文件经负责人授权恢复；不是“Unity未改写”。旧 AFTER_BUILD02、diff、STOP、null退出码原样保留。

- 项目版本仍为 Unity 6000.6.5f1，Packages及锁文件逐字节冻结，未升级/降级依赖。
- 独立可写副本来源为冻结输入清单；原开发树不再由Unity打开。
- BOM移除/中文Unicode转义属表达变化，不据此接受有效配置变化。
- GraphicsSettings打包快照包含全部原基线行，既有值和外置GUID引用没有替换；新增字段来自本版本原生序列化默认值。
- 两个URP资源以批准原件在同版Unity反序列化，再与已导入对象的完整Editor序列化比较，内容相等；原始有效JSON和SHA保存在各成功构建 SETTINGS/。
- shader prefilter相关字段由包源码的 `#if UNITY_EDITOR` 部分在构建预处理阶段更新，不是新的运行时渲染方案。
- runtime settings由原Editor settings列表筛选生成，OnAfterDeserialize清空；没有添加新的产品资源配置。两份包源码证明已归档于 BUILD_INPUT_PROOFS/，不改包源码。
- 隐私门禁在打包前/后均检查Native状态，实际Bee输入另行逐项核对五个Services字段为false。UnityConnect保持负责人批准的关闭状态，不依靠构建结束后的文件恢复认可产物。
- 原ReleaseDiagnosticsGuard继续生效；正式版同时验证profile身份、原生诊断开关和打包服务配置。

BUILD04_RELEASE因构建副本未正确重新初始化被比较门禁拒绝，无产物用于Player。后续构建副本由prepare_build.py精确初始化并逐字节核验。BUILD06_RELEASE完成，但Driver后来修订，因此只保留阶段结果；最终交付以最终冻结源及成功记录为准。
