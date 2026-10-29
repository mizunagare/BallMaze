# 复跑 GAMEPLAY-UX04

只使用工程外新目录和合成存档。不要在用户工程执行测试注入，不复制真实玩家进度，不降低3GB提交容量门槛，不关用户应用/强杀超时子进程。

## 冻结与准备

产品冻结 `fb9dcb828787c6f73b9d5bc078df3d516593d85c`；测试冻结 `5dfe7c39585a03549b67a1cdf675adbca33571a5`。最终交付文档提交还包含证据导出/核验工具。先核对实际远端/工作区及用户保护文件，使用已有 `DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly` 在新的 `I:/WGCombat/<unique>/P/Project` 准备隔离项目。记录owner.json，启动前根必须明确。Unity固定6000.6.5f1；原NativeProbe外部worker路径须有效，不能激活其私有桌面。

现有Step由Invoke-Check动态复用，没有新建第二套进程框架。它检查占用、资源、timeout并记录真实exit。PowerShell父编排调用脚本时使用独立pwsh -File；不要让被调用脚本的exit提前结束父序列。

## 定向复跑

每次Output必须新建；同一目标恢复阶段共享StorageRoot，其余不共享。示意：

```powershell
pwsh -NoProfile -File ProjectDocs/WanxiangGuitu/DeliveryGameplayUX04/Invoke-Check.ps1 -Project I:/WGCombat/<unique>/P/Project -Output I:/WGCombat/<unique>/Target -StorageRoot I:/WGCombat/<unique>/Shared -Method UX04Matrix.Target
# 接着各自新Output：
# UX04Matrix.Run -> UX04Matrix.Resume -> UX04Matrix.RunCraftResume
# 每步确实成功才运行依赖的下一步；失败不得改预期/覆盖原Output。
# 独立根：UX04Before.Run、UX04Scroll.Run、UX04CombatTiming.Run
```

UX04Before在开工产品上应暴露重复追踪、制造结束、滚动、旋转和球截面问题；在交付代码上10项通过。当前测试使用Valid判断是否结束追踪，早期原始结果/日志另行保留，不改写旧失败；首轮夹具源码未单独作字节冻结，不能冒称所有早期输入都已完整冻结。后续包装器复制的执行源与版本可核对。

矩阵120组使用真实Strike、release帧、Overlap候选、方向/横向限制、Sight命中序列与资源HP；受控资源不会被称为正常AI采集。Shared的Store保留营地，GeometryStore与RunCraftStore独立，不能把后继Run覆盖的档案与之前营地期望混比。

UI测试通过真实业务按钮回调和受控PointerEventData；不执行原生键鼠。Camp关闭先走真实Camp.Explore入口。截图是受控RenderRequest，相同场景1280/1920；不能标成人工审美/原生U16通过。

## 受影响回归、AI和构建

```powershell
pwsh -NoProfile -File ProjectDocs/WanxiangGuitu/DeliveryGameplayUX04/Invoke-Final.ps1 -Project I:/WGCombat/<unique>/P/Project -RunRoot I:/WGCombat/<unique>
```

默认跑UX02、品质合同、远程范围、现有时序、B07经济、恢复负例、输入，再走原Invoke-NormalAI Normal/Resume/FinalResume，最后原Build01Audit非开发构建。AI使用虚拟输入和领域交互的既有驱动，敌人正常AI；绝不称为原生玩家。所有seed、收益、轨迹和恢复断言落盘。

`-SkipRules`仅供像本轮最后HUD读取/文案微调后的独立定向UI+AI+构建复验，不是完整All。失败传播不应因后续独立阶段通过而被覆盖；Invoke-Final有失败则exit1。超时或占用则保留子进程和阻断，不强杀。

旧COMBAT01默认存档初始化不适用于batch；本批适配明确隔离，保留现有Spear BasicPower期望，batch不创建非必需GameView或截图。其GPU fatal原样保留UNRESOLVED，适配不是根因修复。只读UX04PauseObserver记录续程timeScale/面板/Editor暂停，不修改时间或状态。

构建后运行Inspect-Build.ps1核对PE排除及哈希。保存全部警告。构建输入之后若仅有Editor夹具改动，应列出旧/新SHA并证明发行排除，不能写成全部输入相同。性能未采样则NOT_RUN。

## 汇总与发布

在拥有owner.json的新根使用Summarize.py（路径清单按新阶段目录调整），导出JSON/CSV；默认当前样本不是一个通用“自动全绿”判定器。Collect.py只发布此拥有根的允许文件类型，排除P/Library/Release/用户数据；日志gzip并仅脱敏凭据，原日志留本机，manifest同时记录原始与发布SHA。Verify-Publication.py核对工作区/索引或LFS oid；Verify-Protection.py核对五个真实开工哈希及历史Git差异。

不上传Library、Temp、发行二进制或转储内存。不把发布成功当作复审通过。全部失败/未执行/未定因必须在REPORT/ACCEPTANCE/INDEX保留。
