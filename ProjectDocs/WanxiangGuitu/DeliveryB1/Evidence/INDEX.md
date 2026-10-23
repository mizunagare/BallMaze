# B1 证据索引

- `latest-method-status.json`：19历史方法+B1规则/恢复/通行共22方法的最后状态，均成功；保留各次结果来源，不代表单次22方法全绿。
- `Rules/`：首轮2方法、最终产品6方法及补充2方法各自的timestamp结果、断言标记、最终summary。
- `Regression/`：首轮19方法17成功2失败的原始结果和summary，相关失败由Rules最后结果修正；不删除原FAIL。
- `PublishCrash2/`：发布完成、确认前受控终止29及新进程恢复0；intent/expected只含合成身份。
- `ReleaseResume/`：无运行驱动正式Player两次正常关闭退出0、同Run/区域/种子/出口/材料/来源账快照与quit审计。
- `NormalAI4/`：最终正常AI及Resume进程结果、metadata、逐步断言、移动/生命CSV、45条存档入口审计、expected-normal及4张真实运行截图（含修复、引导、结算、再次出征）。没有把源图重画成效果图。
- `RejectMissing/`、`RejectRelative/`、`RejectLocalLow/`：启动前负例，预期拒绝退出1、无存档访问回执、哨兵不变。
- `Failures/`：前三次正常AI的失败结果与轨迹，首次中断测试的超时失败；原因见REPORT。
- `BuildSummary.txt`：最终非开发构建成功、0错误、50警告。
- `source-build-correspondence.json`：非Editor源码与隔离构建副本逐文件哈希、最终Player主程序集和启动器哈希；没有运行时验证驱动。
- `process-logs.zip`：42份原始进程日志，包含上述成功及失败；`process-log-hashes.json`列出每份SHA256。压缩包不含存档、Library、Temp或凭据。

所有存档故障测试使用显式隔离目录；引用的身份/数组为合成测试状态。运行审计未覆盖内核全部文件访问；人工试玩NOT_RUN。截图不单独证明提交入库，须结合驱动断言、最终余额及新进程恢复记录。
