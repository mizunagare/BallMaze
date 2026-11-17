# R2 验收与停止记录

## R03定向结果

唯一新增Run UX04B2R2-FLOAT-001，PID17352，实际exit21，verdict=BIT_DIFFERENCE_STOP；Mono6.13.0、Unity6000.6.5f1 WindowsPlayer。身份、输入、逐前缀迹、夹具不变及Random.state不变均在原件中成立。**逐位一致性FAIL，停止闸门成功触发；不是整批修复PASS。**

旧bits418B999A，新bits418B9999，ULP1。原始[result](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json>)、[manifest](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/run-manifest.json>)、[逐步输入/状态](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/state-changes.jsonl>)。

## R01及六场景

NOT_STARTED/NOT_RUN_STOP_GATE。没有实现PreviewAdd/PreviewReplace，没有执行A～F六个Run，不声称通过正常用户操作的替换验收。没有复跑完整B2/R1、没有借用旧9/9替代本批新验收。

## 保护

完整备份后新增隔离Player副本，仅编译观察sidecar；当前产品DLL源码/二进制未改变。12763份R2前原件逐项保护，961项候选白名单保持原样；详见[实物保护结果](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/protection-result.json>)。没有git add/commit/push/merge main或UX-05。

## 停止

立即停止并仅交付证据/方案。下一步必须等待负责人对[浮点方案](<FLOAT_FIX_PROPOSAL.md>)和恢复工作单独审批。
