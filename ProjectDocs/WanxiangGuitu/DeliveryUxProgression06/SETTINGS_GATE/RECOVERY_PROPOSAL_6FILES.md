# 构建保护闸门：等待裁决，未应用恢复

Unity 6000.6.5f1 首次导入/构建后保留六项受保护设置差异（四个 ProjectSettings 加两个 Assets/Settings）：
- EditorBuildSettings.asset：移除 UTF-8 BOM。
- GraphicsSettings.asset：增加图形状态集合、预热、LightBaker 和 ShaderBuildSettings 的新默认序列化字段。
- ProjectSettings.asset：中文字符串改为 Unicode 转义；构建中临时预加载 InputSettings 已由原包的 postprocess 正常移除。
- UnityConnectSettings.asset：m_Enabled 0 → 1。

六份修改后原件、实际 diff 和逐路径 SHA 已归档。原工作区对应文件仍与开工基线 SHA 完全一致，其只读副本置于 BASELINE/。

拟议最小处置：仅将新工作树中上述六文件恢复为已核验 BASELINE/ 的原始字节，明确记录这是负责人批准的构建副作用修复，不伪装成 Unity 未产生变化；不执行 git restore/reset/checkout。保留全部 AFTER_BUILD02/ 原件及失败记录。随后针对自动序列化原因，在新的隔离构建项目/只读输入副本中验证，避免再次改写开发工作树的受保护设置；产品测试仍使用获批源码，不接受 UnityConnect m_Enabled 自动启用。

此处置尚未授权、尚未执行；暂停再次构建和 Player，其他源码/数据映射复核可继续。无需重开 Schema、奖励或地区设计。

完整构建后差异另包含 Assets/Settings/PC_RPAsset.asset（URP序列化默认字段及shader prefilter）和 Assets/Settings/UniversalRenderPipelineGlobalSettings.asset（runtime settings引用列表）。六项清单以 SETTINGS_DRIFT_6FILES.json 与 UNITY_SETTINGS_ACTUAL_6FILES.diff 为准；此六项提案取代先前四项提案。二者原工作树原件与 HEAD 规范字节一致。
