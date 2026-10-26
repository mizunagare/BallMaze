# 阶段2复跑

Unity6000.6.5f1与既有包版本固定，PowerShell7/.NET/Python沿用本机现有工具。所有测试只用工程外唯一根/合成档，不访问真实玩家目录。旧测试/用户程序不关，不强杀。私有WGTest桌面不切换为输入桌面。

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 `
  -SourceProject D:/unity/WanxiangGuitu -TestRoot D:/WanxiangValidationRuns/Stage2FreshAll `
  -Stage2 -FullRegression -GameplayOnly -ShaderCacheSource '<已退出的同版本隔离Project>'
```

Stage2显式包含B10/B09/B08/B07/B4已有流程；不进入无新线索的关闭诊断矩阵。沿用现有编排，新增五规则与19条×三进程正常AI矩阵、数量统计和日志门禁。每步实际退出码/超时/命令/日志保留。协调器exit0仍不表示原生/人工/引擎问题或整个阶段通过。

- `Stage2Rules.Seeds`：100固定种子纯布局/边界/随机隔离，非物理场景。
- `Stage2Physics.Run`：20不同实际种子，真实主角CC参数的探针走全部边/POI/出口；资源/遭遇全NavMesh路径。关闭AI但保留敌人碰撞；不算正常敌人AI或人工。
- `Stage2Rules.Builds`：真实容器/主武器/上盘API，四武器×三构筑，实际属性/格数。
- `Stage2Rules.DamageMetric`：实际伤害、回血、过量、无效调用的瞬时观测合同，不存档、不调数值。
- `Stage2Rules.RetryBoundary`：精确保留历史自然失败→fallback、已验证第三候选、全部失败回营；原WGDeliveryA夹具固定请求1，未放宽断言。

正常AI变体由`Build-Driver.py`从B07原驱动生成，精确锚点不匹配即失败，DRIVER_PROVENANCE记录基底/输出SHA。用已有真实移动/普攻/技能/拾取/修复/结算/制造/恢复，不切成弓假冒其他武器。合成起始物资和自动选技能均明示，不称新手或人工体验。

```powershell
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Build-Driver.py
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Test-LogGate.py --output '<全新外部探针根>'
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Summarize-Matrix.py `
  --matrix '<本次All根>/Stage2Matrix' --output '<全新统计目录>'
```

Invoke-Matrix仅接受既有编排生成的owner/Project，不能指向用户工程。OnlyCase仅用于明确试跑，不代表19条矩阵完成。每次Normal必须新根；Resume/FinalResume恢复原独立Run并核对实体/装备/来源账/RNG；未完成或显式中断即失败，OS正常关闭不是完成回执。

原生四武器人工试玩需独立获准输入环境与独立人员，本轮缺少时NOT_RUN，不由脚本替代。性能量测仍依P0硬件/负载方案，不拿AI模拟时长或受控菜单计数冒充帧预算。

## 本轮实际命令与结果

2026-10-27最终根 `D:/WanxiangValidationRuns/Stage2FinalAll/20261027-010900-ab700d91`。同版本ShaderCache来自`Stage2FinalDirected`已经退出的Project。当前入口仍是既有`Invoke-LocalValidation.ps1 -Stage2 -FullRegression -GameplayOnly`，每项超时和所有命令/原始退出码见发布results.json/CSV。All154P/2预期F/3NR/2UR，协调exit0；57矩阵进程全部exit0无超时、带完成身份断言；原21步AI另记；受控Player15PASS另记，不能累加为154的独立子步骤。

结束后只读复核（目标必须全新；不得覆盖原证据）：

```powershell
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Publish-Evidence.py --run '<本次根>' --target '<全新发布目录>'
python -B ProjectDocs/WanxiangGuitu/DeliveryB10/Audit-Release.py --project D:/unity/WanxiangGuitu --run '<本次根>' --target '<新建空审计目录>' --baseline '<开工完整Git SHA，非JSON路径>'
python -B ProjectDocs/WanxiangGuitu/DeliveryB4/Provenance.py --project D:/unity/WanxiangGuitu --run '<本次根>' --target '<上述审计目录>'
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Audit-Transactions.py --run '<本次根>' --output '<全新守恒结果.json>'
python -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Audit-Final.py --run '<本次根>' --output '<全新覆盖与日志结果.json>'
```

`Audit-Final`要求report.finalized，独立记录所有非Project/Library/Worker日志及异常上下文；用logManifest.path数组配合既有Automation/publish-evidence.py `--zip`发布全日志，原文件在外部根保留。最终192份脱敏完整日志见Evidence/FinalLogs，不以窄门禁替代独立错误检查。新审计/出版脚本都是运行结束后读证据，不影响冻结的产品或规则输入。

CombatHealth唯一产品改动先由Stage2MetricBefore失败暴露；精确观测测试在FinalAll重新运行。RetryBoundary保留故障候选与fallback原日志；非任意第三候选必成功。新editor-close正向退出观察路径仍NOT_RUN；本次57进程走既有正常完成退出，没有使用该中断路径。

原生/人工执行清单见HUMAN_PLAY_PROTOCOL.md。不得切换私有桌面为输入桌面；Console上只存在用户会话，不要求用户守候。旧B10根PID30340仍是先前占用，不强杀、不称本轮干净关闭。受控截图与实际机器人战斗逐类标明；D3D12/青色帧不做无新线索重试。
