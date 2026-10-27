# INPUT-01 I01～I15 验收

产品/执行测试冻结：`f16bdcaee45553c9d53d525bdceecdd2e2238a1a`。状态针对下述范围，非独立审核结论。源码落点按[动作映射](INPUT_ACTIONS.md)，执行步骤按[复跑](TESTING.md)。

|ID|状态|实际范围及限制|证据|
|---|---|---|---|
|I01|PASS|默认及旧v1字段，26规则；正式Missing/Ready不自动建Run|[input01-rules.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-rules.json)|
|I02|PASS|真实虚拟事件的新/旧移动、技能和交互消费|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I03|PASS|按住应用、失焦/恢复、断开/重连及新场景；不放宽原断言|[refocus-observation.json](Evidence/Runtime/FinalFrozenValidation/Rules/refocus-observation.json)|
|I04|PASS|同场景冲突、Esc/右键/开发保留、重复别名，UI真实冲突；互斥R/鼠标复用|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I05|PASS|虚拟指针点击捕获入口、启动点击不误录、虚拟Esc取消和释放镜头、模态不穿透|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I06|PASS|编辑副本/有效值/磁盘分离，恢复默认可取消；实际UI应用和返回|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I07|PASS|坏设置/未知动作/冲突/外部变化、保存失败可见与UI重试，原件和其他值保留|[input01-rules.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-rules.json)|
|I08|PASS|不同Editor进程，标题→设置→继续原Run，身份/来源账/装备/库存/回执/布局/随机一致|[input01-play-resume.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-resume.json)|
|I09|PASS|背包/角色/路线/帮助/设置/管理鼠标旋转/技能选择及原营地时钟|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I10|PASS|实际J最近拾取、O出口；显示/执行目标一致，同帧单次收费/取消，原受击中断回归|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I11|PASS|四武器默认与自定义的普攻/技能；切换、翻滚、药水使用正式消费链和冷却|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I12|PASS|实际1280×720、1920×1080及150%HUD，结构边界/重叠/键帽/按钮文字检查与截图；非人工|[input01-play-normal.json](Evidence/Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)|
|I13|PASS|全AI Gather三进程真实采集、修渡口、撤离、结算、制造及再次森林|[normal-results.txt](Evidence/Runtime/FinalFrozenValidation/Normal-Gather/normal-results.txt)|
|I14|UNRESOLVED|非开发产出/正式标题/测试剔除已证实，但2条URP包资产Error与91警告，构建质量待定位|[BuildSummary.txt](Evidence/Runtime/FinalFrozenValidation/Build/BuildSummary.txt)|
|I15|NOT_RUN|没有安全已授权的独立原生交互/人工环境，不用虚拟设备或WM_CLOSE替代|[环境](Evidence/Runtime/interactive-environment.json)|

自动化有限项13 PASS、1 UNRESOLVED、1 NOT_RUN；不将布局断言数量当玩家次数。编排行级35P/2预期FAIL/92NR/2UR原样保留，构建新增质量问题另列，不能从编排器exit0推出全部验收通过。

[完整结果](Evidence/Runtime/FINAL_RESULTS.json)包含276条分层断言（26规则、239受控、11新进程），各组交集不相加作独立场景。历史引擎、原生、人工、性能均开放；[失败历史](FAILURE_HISTORY.md)不被本表覆盖。
