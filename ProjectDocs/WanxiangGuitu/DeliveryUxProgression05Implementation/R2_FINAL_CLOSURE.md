# UX-05 R2 最终证据收尾

**CONDITIONAL_PASS。F-01 已关闭，F-02 未关闭。** 最终 NoDefine、Release 均实际启动、通过原生输入读取 v10 及128条目标历史、正常退出，并在新进程中再次读取成功。历史 Driver 追溯已执行，但114条 Run 对应的18个原始脚本 SHA 仍没有精确源码副本，其中包括31条 R1 PASS。不能将“搜索完成”写成“身份缺口消除”。等待负责人复审，不自动接受此限制。

日期：2026-11-20。执行依据为根 AGENTS.md 及 UX-05-R2-FINAL-CLOSURE。使用 computer-use 技能的 node_repl / @oai/sky 原生输入，未使用 Acceptance Harness、观察 sidecar、反射探针或直接构造产品历史。没有修改产品源码、Schema、迁移/结算逻辑，没有构建。

## 基线与保护

- 当前分支 `feature/ux-progression-05-objective-history`；HEAD `ae705b944b7d0fe851fbd395229dfc30ec636f5c`，父提交 `95caf234256613d4a6e4f89a8ab0dc09c397c6b2`。
- 接手时已有11个 tracked 产品修改，暂存区为空，sparse-checkout 已启用；既有修改没有归因于本轮。开工路径、大小、SHA256、工作区状态及 Index SHA 在 [preflight](EVIDENCE/R2/preflight.json)。
- 本轮远端实测：UX-05独立远端分支不存在；B2仍为上述 HEAD；main=`72db192a527bd256e2ba18cd7ab334d8334051da`。未fetch或改变分支、Index。
- 原159条分类、4142个历史证据及5404个既有索引项均重新核对；历史失败、旧归档、旧结果及旧矩阵不改。产品、Packages、ProjectSettings与本轮前指纹一致。
- 存档仅使用 EVIDENCE/R2/nodefine-storage 和 release-storage。两根由完整复制既有 CAPACITY-A02 隔离测试集合形成，包含主档、bak、129个外置分页；未修改源集合、未接触用户真实存档。复制集合不是生成新的目标完成事实，原129次真实结算证据仍在原Run。

## 最终纯构建运行 [P][C]

| Run（共同前缀 UX05-R2-CLOSURE-） | PID | 原生退出码 | 分类 | 证据范围 |
|---|---:|---:|---|---|
| NODEFINE-BOOT-A01 | 18808 | 0 | PASS | 启动、继续、128条/第1页、正常WM_CLOSE |
| NODEFINE-RESTART-A01 | 29804 | 未取得 | INSTRUMENT_INTERRUPTED | 标题已到达；前台输入拒绝，后续工具重置终止，不能算正常退出 |
| NODEFINE-RESTART-A02 | 14992 | 0 | PASS | 新PID重读、128条/第1页、正常WM_CLOSE |
| RELEASE-BOOT-A01 | 1216 | 未取得 | INSTRUMENT_INTERRUPTED | 标题已到达；输入拒绝及工具重置，没有正常关闭证据 |
| RELEASE-BOOT-A02 | 18956 | 0 | PASS | 继续、128条/第1页、正常WM_CLOSE |
| RELEASE-RESTART-A02 | 31504 | 0 | PASS | 新PID重读、128条/第1页、正常WM_CLOSE |

新增6条：4 PASS、2 INSTRUMENT_INTERRUPTED。不是修改旧FAIL为PASS。全部原始输入、失败原因、截图、Player.log、run-manifest.json、result.json与可取得的原生退出回执在 [新Run矩阵](NODEFINE_RELEASE_RUN_MATRIX.csv)。完整性索引见 [R2 INDEX](EVIDENCE/R2/INDEX.json)。

实际路径：标题“继续游戏”→产品 continue-selected/game-ready→营地背包→“冒险历程”。四份历史截图均显示“共128条、1/7页”，首条 Run=`6cb5640385a947f3af45cca5712e9fde`、名称“扫箱”、完成时间 `2026-11-19 07:16:20 UTC`，后续记录顺序一致。本轮只补最小纯构建路径，没有重跑既有七页/筛选/IMGUI全矩阵。正常退出使用原生 Alt+F4/WM_CLOSE，非Kill；后面三份成功回执由独立宿主持有原生进程句柄并WaitForExit取得0，首份由原启动进程取得exit事件0。

原生工具曾报 `foreground window did not report a process id`。拒绝调用不计为成功输入；刷新/重选及新 helper 会话恢复后，才以实际游戏画面和产品入口记录证明消费。两次工具中断保留，无退出码倒填。随后启动监控独立于交互内核，避免内核重置终止Player。Release BOOT-A02中的一次输入拒绝也保留在 input-errors.jsonl，不计为已消费点击；新会话中重新观察并实际点击成功。

## 最终构建身份 [B][S][P]

| 构建 | 产品DLL SHA256 | EXE SHA256 | Unity build-guid |
|---|---|---|---|
| UX05-R2-Acceptance-A02 | BA0A2FC8FF10C1C0DF8AC4E445A5AA2A6C9F9AFD00E631B5B54682463C7889C8 | B70442F90F50CD91F7AF7BF2272602645FC5D02C4D3156FB221FC27C328D2436 | c485f267e5ad485e8f529e9e9901391f |
| UX05-R2-NoDefine-A02 | E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78 | B70442F90F50CD91F7AF7BF2272602645FC5D02C4D3156FB221FC27C328D2436 | ab9a568dafa24c12b5fc6ed6b3e8250a |
| UX05-R2-Release-A02 | 18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C | 001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A | 90a8eedf0f334167ae3c7d3f54827bf6 |

未复制/替换最终产品程序集。manifest中的buildId沿用已核验构建身份，不冒充程序集自身输出的业务标记；boot.config另有Unity build-guid。进程路径、日志及实际SHA与对应构建相符，NoDefine/Release不混用。

两种纯构建Assembly-CSharp的UTF8/UTF16扫描均无 UX_ACCEPTANCE、PlayerAcceptanceHarness/03、HarnessRunner/Harness03Runner、ObjectiveHistoryEntryProbe/ContractProbe、MigrationValidationHook、ObserveMigration、ObserveHistoryRepaint、UX05_ENTRY_PROBE、CavernValidation；Managed目录/RuntimeInitializeOnLoads也无测试启动项或注入sidecar。静态排除与真实运行分别记录，前者不代替后者。Acceptance保持原验收身份，不用于冒充纯发行。详见 [独立复核](EVIDENCE/R2/revalidation.json)。

日志保留D3D12信息队列查询失败以及可选URP景深/Panini shader未支持/剥离警告；已实际显示营地和历程并正常关闭，未出现产品异常/隔离拒绝。没有因这些警告重建或修改渲染设置，也不宣称所有后处理功能正常。

## 存档指纹、重启和只读边界 [S][P][C]

四个成功Run的前后完整主档均通过v10版本及payload SHA256校验；历史六字段数组与原128条逐字段相等，committedRuns仍为原129个，Profile除camp快照外其他字段全部相等（包含材料、仓库、徽章、领取队列和结算事实）。双UTC字符串没有重采样。

原档revision648；NoDefine首次正常退出661、重启退出666；Release首次正常退出654、重启退出658。存档SHA实际变化完整保存在矩阵/result和前后主档；不能声称整个运行期文件字节不变。原因是既存 CombatSaveSystem.Update 使用unscaledTime周期保存，焦点丢失及正常退出也保存；不是历史页的新写入。

Release历史显示时副本相对运行前主档，仅payload revision/profile不同；Profile仅camp不同，camp仅randomStateJson/events/resources不同。历史和所有其他Profile字段不变。初版审计工具曾错误要求全程SHA相等，失败脚本及诊断保留在Tools/Verify-ClosureRuns-A01.py、audit-assumption-A01-failure.json；A02逐项检查实际变化及业务不变量，没有将整档零变化改判PASS。未修改产品或历史断言。

具备逐文件前后采样的三个成功后续Run均有129个分页SHA完全不变。初次NoDefine有完整来源/前后主档与源集合保护记录，但未在启动前独立采样整个副本目录，未倒填该指标。存档业务通过与采样完备性分开描述。未通过探针写入历史、构造目标或提交额外奖励。

## 历史Driver追溯 [C]

[逐Run恢复表](DRIVER_ARCHIVE_RECOVERY.csv)保留114条关联、18个SHA，以及原分类。84条原分类PASS中包括31条R1 PASS；均不因来源缺口而回写旧判定，也不把“不可重现”列标记PASS。

已执行：

1. `git fsck --full --no-reflogs --unreachable`退出0，发现1555个unreachable对象；`cat-file --batch-all-objects`列85751个对象，精确SHA256检查69703个不超过8MiB的blob，包含可达和不可达对象。Git OID与Driver SHA256分列，不混同。
2. 检查Builds、历史Evidence、工具备份及仓库文件34973个；检查6910份PDB和220份编译响应/日志候选。PDB未发现.ps1源关联。
3. ZIP检查1761个成员；另解读gzip归档。补充长路径、59个大文件流式哈希，以及Library中10991个缓存源码/PDB/编译响应候选（含716份缓存响应文件）。补充11051项，错误0；初次唯一长路径异常已单独补读，不删除原错误记录。
4. 原始搜索、补充清单、Git对象、错误及工具源码均在EVIDENCE/R2。初次Git批处理分隔符工具缺陷中断记录保留，修复的是新审计读取器，不是历史材料。

结果：18个原脚本SHA全部未恢复；没有用当前源码、换行变体、重编译DLL或当前PDB冒充历史版本。哈希实际是PowerShell启动脚本源码；脚本是解释执行，独立Driver二进制、Driver PDB和编译参数为N/A，而非“已找到”。可匹配的产品DLL及候选产品符号另列，不能取代脚本；原manifest只保留Run/根/构建等部分参数，完整原启动命令未找到。因此114条均不能按精确历史Driver独立复现。

搜索范围为本仓库Git对象及本仓库拥有的目录/缓存，不读取用户其他聊天、私人目录或真实存档；“未恢复”仅说明这次搜索结果，不宣称全磁盘或任何离线介质永远不存在源码。F-02仍是负责人需要复审的证据限制。

## 其余复核与停止

原159条分类不变，新增Run另表；历史129次结算、128留存和committedRuns129再次从原主档复算。旧终局重放、双UTC/Pending/Committed、八类v9迁移恢复、分页归档、同根竞争、v9拒绝及IMGUI/uGUI、D-20/D-23结论沿用已独立核验且本轮字节未变的原始证据，不冒充本轮又执行了完整矩阵。受保护源码也没有改变。

显示环境仍仅1280×720、DPI96；其他环境未测。历史生命周期/PDB归属等既有边界详见 [风险登记](FINAL_RISK_REGISTER.md)，没有因补证自动消除。

复算入口：Tools/Verify-ClosureRuns-A02.py、Build-DriverRecoveryTable.py及最终保护检查；它们只读历史资料，仅生成本轮新证据/表。全量历史运行矩阵和旧EVIDENCE/INDEX.json保持原样，R2索引独立。

已停止。未add、commit、push、merge、rebase或启动UX-06。最有价值的下一步是负责人复审114条Driver不可恢复限制是否可接受；未经裁决，整体仍为CONDITIONAL_PASS。
