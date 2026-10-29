# 尝试与历史失败

不改写 RUNLOOP-01、COMBAT-02/R1/03 的任何原始失败、aggregate 或报告。此次保护核对覆盖 2040 个旧文件，全部 SHA256 不变。

| 尝试 | 原结果 | 解释及后续 |
|---|---|---|
| Before01 | 编译失败，exit 1 | 测试将实例 ForestRegionRuntime.ValidationHook 误作 static；修夹具，不改产品 |
| Before02 | 夹具异常，Editor exit 2 | SuspendEntry 后 InitializeStorage 不解除 blocked；改用真实 InitializeFromEntry 新档事务 |
| Before03 | 合法负例已有 6 PASS/10 FAIL，随后 Editor exit 2 | 仅改 settlementId 的身份负例不满足 v9 runId:terminal 约束；不能计作合法身份样本，随后整体替换关联身份 |
| Before04 | 17 PASS/15 FAIL，exit 1 | 实际 Unity 复现两发现；完整矩阵跑完，所有候选先完整 v9 校验 |
| After01 | 33 PASS，exit 0 | 最小产品修复后的独立矩阵，尚无受控 F5 项 |
| After02 | 33 PASS，exit 0 | 增加受控 InputSystem F5 和回调前后文件指纹 |
| Migration 目录准备 | 包装器 exit 1；未启动 Unity | 提前创建输出目录被既有运行器拒绝；不覆盖目录，另用 Migration01 |
| Migration01/02 | 每次 8 用例，exit 0 | 旧版迁移失败保留与重试成功，避免门禁自锁 |
| Before05 | 编译失败，exit 1 | 新迁移夹具直接引用前版没有的 presenter API；改测试反射兼容，不改变前版产品以求通过 |
| After03 | 33 PASS，exit 0 | 保存发布前 Pending、完整恢复期望及当前产品正常行为 |
| Before06 | 17 PASS/15 FAIL，exit 1 | 最终相同夹具针对旧产品；15 条产品合同断言失败保留，不是工具退出即认定产品失败 |
| After04 | 33 PASS，exit 0 | 最终相同夹具针对新产品，精确旧 Pending 与合法冲突均覆盖 |
| Migration03 | 8 用例，exit 0 | 最终冻结兼容夹具的新运行 |
| 汇总工具首次 | Python TypeError，exit 1 | 原运行器的单项 results.json 是对象而非数组；汇总器兼容两种封装，保留 publication-attempts.json，不修改原结果 |

初始工具尝试没有另存当时全部夹具源码，保留真实日志并明确该证据限制，不补造快照。Before06/After04/Migration03 补齐实际执行源码与完整对照。过程退出/超时详见原 results/children/sequence，包装器退出码与 Editor 实际退出码分别保留。

上述 FAIL 不得删除，也不能机械等同当前产品仍存在同样数量的缺陷。当前有限验收、findings FIXED/待复审与 deferred 分开。所有旧引擎/关闭根因保持 UNRESOLVED，原生/人工/性能仍 NOT_RUN。
