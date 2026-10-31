# 保留的失败与未解决项

- 旧 CP03 Before/Before2/VisualCueBefore/Runtime/Runtime2 及原报告、原输入、原 aggregate/JSON 均未改。[原 Evidence](../DeliveryCombatPresentation03/Evidence/INDEX.md)、[本轮保护哈希](Evidence/protected-after.json)。原近距两项继续 UNRESOLVED。
- 旧运行器谓词的语义 FAIL 已只读复现；不把旧 results.json 改成新状态。[复现](Evidence/before-classification.json)、[只读重审](Evidence/HistoricalReaudit/acceptance.json)。
- 旧审计对同一 MeleeTrace 行后附 `Time.timeScale=0;` 错误放行。仅合成源码文本，未进入产品/构建。[旧工具输出](Evidence/PostStyle/SelfTest/old-audit-bypass.txt)、[新工具负例](Evidence/PostStyle/SelfTest/selftest.json)。
- SelfTest1 exit1：自测使用 HERE.parents[3]，应为 parents[2]，找不到测试源码。[记录](Evidence/SelfTest1/tool-failure.txt)。
- SelfTest2 exit1 / 首份严格审计 FAIL：OnDestroy 原本是一行实现，初版错误要求独立签名行；改为原文精确整行边界，没有扩大白名单。[记录](Evidence/SelfTest2/tool-failure.txt)、[首次失败审计](Evidence/locked-contract-r1.json)。SelfTest3 的 48 PASS、Final 的 49 PASS、Final2/Delivery 的 50 PASS 分开保留。
- 输入绑定初版 exit1：git ls-tree 引用中文路径，pathlib 报 Invalid argument；改 NUL 分隔。[记录](Evidence/binding-attempt1.txt)。初轮工作树/Git 字节差异没有被抹去，逐项查明换行、LFS 和 5 个既有冻结设置来源，[来源](Evidence/settings-provenance.json)、[最终冻结绑定](Evidence/frozen-build-product-binding.json)。
- 初轮 `git diff --check` 把工具 CRLF 报为 trailing whitespace，后续仅把本轮工具文本规范为 LF；EOF 多空行也已清理。[首次输出](Evidence/diffcheck-before.txt)。没有修改产品采样循环、旧脚本快照或日志。
- 首次组合宿主命令返回 1；内部 Player exit0、分类器输出 BLOCKED/2。宿主传播机制根因未确认，不能归责游戏。最终显式 `exit $LASTEXITCODE` 的 RuntimeFinal/Editor/Diagnosis 均返回 2，与语义报告一致，[宿主记录](Evidence/host-results.json)。
- Editor 新日志出现 UnityEditor.Search 内部 ArgumentOutOfRangeException；源日志完整保留，不过滤、不宣称根因解决。[异常索引](Evidence/log-findings.json)。
- D3D12 UNKNOWN、C15、Editor 青色帧、Search/JobTempAlloc 历史根因仍 UNRESOLVED；原生 U16、人工观感/音质/最终打击感仍 NOT_RUN。不重复无新线索的关闭实验。

无伤害/范围/冷却/时序/CombatAim/碰撞/数值/AI/经济/随机/v9 修改，无新素材/依赖/CI。所有过程不强杀、不关闭用户程序、不触碰真实存档。

- 文档/宿主记录脚本首次使用系统 GBK 读取 UTF8 Markdown 报 UnicodeDecodeError；已显式指定 UTF8，未改产品文件。该组合 shell 最后返回 0 不代表前置 Python 成功，错误单列保留于 [记录](Evidence/metadata-attempt1.txt)。

- 提交前样式检查发现两个新增工具/观测文本 EOF 空行，提交中止；仅移除末尾空行后，最新独立自测仍 50 PASS。新增本目录 `.gitattributes` 为 `Evidence/** -text`，防止 Git 换行转换破坏原始字节 SHA；无修改旧证据。[保留记录](Evidence/PostStyle/stage-attempt1.txt)。

- 第二次提交前字节检查把 Git LFS 指针当日志内容，错误报告 gzip SHA 不等并中止提交；改为同时核验指针 oid/size、LFS 本地对象和发布字节，未改日志或 manifest。[最终核验](Evidence/DELIVERY_VERIFICATION.json)、[核验工具](Verify-Publication.py)。

- 首轮最终发布核验中，845 项字节/LFS 全部一致，但最终回执链接先于文件生成而报缺失；原始 [预检查](Evidence/PUBLICATION_LINK_PRECHECK.json)保留，按先生成回执再挂链接修正顺序，未放宽链接检查。
