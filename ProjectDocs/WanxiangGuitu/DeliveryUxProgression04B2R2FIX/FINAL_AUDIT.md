# UX-04-B2-R2-FIX 最终独立审计（2026-11-17）

## 结论与授权边界

**本轮 R2FIX 限定范围：PASS。整包 B2 提交/发布候选：CONDITIONAL，等待负责人复审。**

这是对当前源码、实际二进制、原始证据和 Git 状态的新审计，不是采用旧交付报告的 PASS。未修改任何既有产品、历史证据、旧901索引或961清单；没有构建、启动Player、暂存、提交、推送、合并main或启动UX-05。新增内容仅为本轮审计、白名单和运输包。

条件不隐去：ComputeDefense 相对 FIX 前未改，不代表其与 HEAD 原 LINQ 防御链已逐位等价；旧 B2/R1 防御精度及历史归档条件、本轮未运行的 IMGUI/平台边界仍需负责人接受或另行授权。白名单不是提交授权。

## 1. 当前工作区与两套差异基准

- HEAD：95caf234256613d4a6e4f89a8ab0dc09c397c6b2；tree：e46232da0b87c97c39174fe58737c394a773b649；分支 feature/ux-progression-04-b2；暂存区为空。
- [完整当前Git状态](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/GIT_STATUS.txt>)、[porcelain v2](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/GIT_STATUS_PORCELAIN_V2.txt>)、[全部tracked HEAD差异](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/GIT_DIFF_HEAD.patch>)均已保存，不把目录级状态缩略当完整清单。
- HEAD差异包含累积B2/R1修改；FIX前快照差异只界定本次四源变化，两者不可混用。[四源及身份入口](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/ENTRY_STATE.json>)。
- 未跟踪的 [B2AttackModel.cs完整新增diff](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/DIFF_HEAD/B2AttackModel.cs.diff>) 从 /dev/null 单列，未被普通git diff遗漏；四份当前源码、HEAD原件、FIX前原件和完整逐文件diff已包含在复审包内。
- 当前工作区文件完整外部备份位于 [workspace](<I:/unity/WanxiangGuitu-UX04B2R2FIX-FinalAudit-snapshot-20261117-0940/workspace/>)。robocopy：44,943文件、5,108目录、4.817 g、Mismatch/FAILED均0、退出1（成功复制）。[原日志](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/WORKSPACE_SNAPSHOT_ROBOCOPY.log>)。复制期间仅新审计输出可能新增，因此不把它冒称原子文件系统或Git对象库克隆；旧901与四产品源由入口/闭环指纹分别锁定。

## 2. 独立源码审查与源码→DLL链

[源码独立结论](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_REVIEW.md>) / [完整数据](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_REVIEW.json>)：

- ComputeAttack 实际为 Active.Sum → Rig → Bag；不是提高容差或另加补偿公式。
- Active、ComputeDefense 的实际原始方法字节与 FIX 前快照完全相等。旧报告方法长度受提取边界影响，本审计以明确边界下前后实际字节和SHA相等为准，不把长度标签当证明。
- Add 不移旧；Replace 传确切新旧ID/目标/角色/旋转；只在Clone中模拟，复用真实空间及双向交换；旧件安全回包，失败不Find兜底绕过非法交换；Apply重验，Main/Reserve/容器沿既有事务路径。未发现FIX新增明确缺陷。
- UI存在真实按钮及正常事件链；静态接线本身不作为历史物理输入认证。

原构建回执只记录三个B2新增源SHA，166源盘点是事后记录，本审计没有追写旧回执。新增 [PDB源码审计](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/PDB_SOURCE_AUDIT.json>) 直接只读解析既有产品PE与Portable PDB：

1. DLL CodeView 的 GUID、stamp 与PDB ID相符，绑定实际 ab3d5ba4… 产品。
2. 153份实际编译项目源码的编译器Document校验和与当前源码全部相符，包含四个修改源。
3. 第154份为Unity生成的虚拟源码，不是项目源码缺失；从PDB EmbeddedSource提取原文，校验和亦相符。独立源码审查员又用另一实现复核153+1及绑定。
4. 最初“全部Document均必须有磁盘文件”的审计诊断保留，不覆盖其FAIL；后续按生成源内嵌数据闭环。见 [诊断说明](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/AUDIT_DIAGNOSTICS.md>)。没有重新编译、重新生成或修改旧PDB/DLL。

## 3. 原始证据独立核验（不是只核附件）

|层|本轮实际结果|
|---|---|
|冻结INDEX的实际文件|901/901 SHA256和bytes一致，无重复/缺失/漂移；不是仅核三个文档和CSV|
|运行矩阵|25/25逐manifest/result核验：19 UI PASS、4 UI FAIL、2 Float BITWISE_EQUAL|
|最终UI-A07|6/6独立PID，641/641原检查；同DLL/Driver/buildId|
|本轮重新执行原始数据计算|18,306检查，0差异；检查名称、结论及级别与旧Oracle逐项吻合，未调用旧工具的硬编码写出器|
|另一路独立核验|2232个九域FNV、394条Save base64/bytes/SHA全部吻合；124次状态转换；A02/A03在Evaluate前失败，缺少state文件属实，不伪造|
|自然保存边界|12个gate：LastSavedAt实际推进且达到旧due、interval=5、focusEpoch不变；不关闭保存，不改clock，不忽略保存字段|
|浮点原件|两个实际Mono6.13门，每门7case/24prefix，合计48扩展前缀零bit/ULP差；未启动新Mono或用Python计算替代实际Mono结果|

[独立原件审计](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/RAW_EVIDENCE_REVIEW.md>)、[本轮fresh Oracle数据](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/ORACLE_RECOMPUTED.json>)、[独立901逐文件核对](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_index_sha256_20261117_0948.json>)。

最终产品：ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1；Driver：0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45；buildId：ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6。

## 4. 四条历史FAIL不可撤销

A01验证器混淆Worn本体0与容器总贡献6；A02/A03真实滚轮过冲、未到Evaluate；A05F跨自然自动保存周期。原manifest/result和失败标记全部保留。

特别是A05F不是“仅时间戳变化”：原磁盘是fixture前camp快照，后续正常autosave写入fixture的gear/level/skills等，payload有239条路径变化并生成旧主档的bak。该次拒绝Commit的live九域和Random确实不变，但磁盘字节不同，所以原Run仍为FAIL。不能用解释豁免它，也不能用A07通过将其改写。

## 5. 保护域与旧961

[独立保护审计](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/PROTECTION_REVIEW.md>) / [逐文件重算](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/PROTECTION_REVIEW.json>)：12808原件的当前与快照均重新读取；仅四授权源变化，其余12804项完全相同。两份保护TSV各12808行全列核对零差异；禁止域、场景/prefab、Packages/ProjectSettings及16份旧INDEX保持原样。

历史961路径全部实存；旧TXT/CSV/AUDIT_INDEX均原样。旧CSV中四个授权源的payload SHA自然已过时，但旧候选清单原件不能刷新；三个原有自引用占位也不是额外损坏。本次新名单与它分离。

## 6. 精确提交候选白名单

[SUBMIT_WHITELIST.txt](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/SUBMIT_WHITELIST.txt>) **1962条唯一字面路径**；[逐路径SHA/bytes/Git类别CSV](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/SUBMIT_WHITELIST.csv>)。

构成：旧961原样路径 + 901冻结R2FIX材料 + 原R2相关补充36项 + 旧901索引本身 + 本轮63项审计/控制文件；所有集合去重。产品仅11路径（5个原tracked修改源、3个B2未跟踪源及3个meta），没有把全部工作区未跟踪内容一并白名单化。

明确排除：Builds/Library/Temp缓存、Assets/Resources.meta、所有无关用户修改/历史Evidence、ProjectSettings/Packages/场景prefab、运行期_live _roots、运输ZIP及其SHA sidecar。规范归档的original-root仍作为原始证据保留；不能把它与运行期_roots混为一谈。

CSV有1961条实际SHA行，唯一不对自身作不可能的自哈希；其实际SHA由ZIP内部材料清单绑定。TXT可正常包含自己及CSV的字面路径，不包含自己的SHA；没有伪造0哈希或偷偷覆盖旧名单。白名单仅冻结候选，不授权任何git add。

## 7. 复审包与远端

[FINAL_AUDIT_PACKAGE.zip](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_PACKAGE.zip>) 含四源实际字节、完整HEAD/FIX前差异、未跟踪B2源码、保护与Oracle原件、六完整交付文档、25运行及历史材料、本轮独立审计和编译源码上下文。ZIP内BUNDLE_MANIFEST逐成员SHA/bytes，解包后可复核，不是构建好的完整Unity Player或完整Git clone。ZIP额外源码上下文不等于提交白名单；运输ZIP本身不提交。[运输包SHA256](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_PACKAGE_SHA256.txt>)。

只读 [远端查询](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/REMOTE_HEADS.txt>)：main仍72db192a527bd256e2ba18cd7ab334d8334051da；feature/ux-progression-04为95caf234…；feature/ux-progression-04-b2未列出。没有fetch/push或改写远端/本地ref。

[最终只读闭环](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/FINAL_INTEGRITY.json>) 检查原901/历史引用、四源与入口一致、HEAD/分支不变、暂存为空。审计结束后暂停，等待负责人复审；不执行任何提交动作。
