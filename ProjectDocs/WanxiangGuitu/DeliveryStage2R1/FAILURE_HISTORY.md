# S2-R1失败历史（持续追加，原始输出均保留）

- 离线原复现：`D:/WanxiangValidationRuns/S2R1/20261027-085949-review-intake/OriginalReproduction`，4例原脚本匹配blob23900d。1正常+3异常旧行为确实复现，不是产品PASS/旧19局损坏证明。原任务书最初缺失的阻断回执保留，用户补路径后已解除。
- `SummaryBefore`：新29断言5PASS/24FAIL；`SummaryAfter1`29PASS，`After2`31PASS，`After3`32PASS。负子进程的FAIL/exit1是预期，断言PASS不混同游戏PASS。R13只读旧19重审Historical19Audit1为19PASS，警告旧schema缺实际attemptID不回填。
- `ObservationBefore/20261027-093151-1cd96e56`：Unity实际缺事件probe FAIL/exit1；先失败再增加只读health-transition接线。
- `PilotOrd1/20261027-094723-7af75d9d`：准备、事件probe、旧伤害规则、普通敌seed1三构筑预试跑均PASS；三例均首击实际死亡TTK0，不是无限DPS。该预试运行早于parentMethod字段补齐，不能当最终冻结版主矩阵，原来源/数据保留。
- `PilotLake1/20261027-095325-5adc2223`：边界校验在batch模式未进入预期Play初始化，180秒内部deadline后exit1（不是测试通过）；湖Boss首例可选远程后撤点TryGround成功但无完整NavMesh路径，驱动抛错exit1，观测censored、0命中。Search内部异常另列，不是此驱动栈。修复测试入口为同类既有非batch私有桌面；可选4m后撤额外确认完整导航，否则停止输入，不改地图/怪物/攻击/躲避数值，不换失败seed。
- `RecoveryPilot/20261027-095837-2572e8f4`：普通敌真实首次扣血后暂停保存、第二进程继续至死亡/掉落/真实放弃结算均PASS；湖BossStart遇到同一旧后撤驱动问题FAIL。原编排未跳过LakeResume，缺检查点的Start前置异常未捕获，Editor留在等待。仅对该root/PID44576/独立WGTest桌面记录interruption后，使用既有editor-close发送WM_CLOSE正常结束：实际exit0、无超时/无强杀；这是失败清理，不是恢复验收PASS。该原始Resume进程exit0不改变缺少recovery-result的事实。已加R1 Start异常exit1与Start→Resume依赖，保留未完成记录；没有关闭用户程序或历史占用进程。

本轮未因这些边界试验调整任何玩法参数。后续每次复测均用新根/新attempt，原日志和失败不覆盖。
