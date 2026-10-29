# RUNLOOP-01 审核侧分支模型

审核提交：`d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179`
仓库：`mizunagare/BallMaze`

## 这些材料是什么

- `review_branch_model.py`：根据 GitHub 连接器返回源码逐项转写的两个控制流模型。
- `model-results.json`：审核侧实际执行模型的输出。
- `source-excerpts.txt`：用于模型的关键源码摘录。
- `source-references.json`：固定 SHA、路径、连接器返回的文件 blob SHA 与链接。

这是 **Python 离线分支模型，不是 Unity/C# 产品程序**。没有启动 Unity、Windows Player、文件发布器或 v9 校验器；没有使用真实玩家存档。模型的简化字典不是可以直接导入游戏的完整存档。实际 v9 合法冲突夹具和场景恢复故障，应按任务书在隔离 Unity 中补做。

本模型只验证：
1. 指定的失败核对表达式会不会忽略 `settlement.plan`、`outcome` 或完整 `activeRun` 的差异。
2. `Restore` 提前清除标记后，若后续装载失败，当前 UI 分支是否仍选择“读取完整存档”。

11 个模型条件：7 个符合预期，4 个反例，归属 2 个审查问题。不是 11 场游戏测试，也不是 4 个不同的产品缺陷。

## 复跑

```bash
python review_branch_model.py --out model-results-rerun.json
```

输出文件必须不存在。脚本退出 0 只表示模型完成执行；具体反例查看 `matchesContract: false`，不据此推断游戏通过或失败。

## 限制

源码由 GitHub 连接器读取。文件 blob SHA 是连接器返回的元数据；未在本地重新计算完整源码 blob。摘录为人工转存，不声称等于完整文件。连接器引用和准确函数位置见 source-references.json。

模型不模拟 Unity 的 JsonUtility 全部语义、存档结构验证、碰撞、场景载入、消息循环或真实磁盘故障。它支持源码审查结论，不代替任务书中的 Unity 故障注入验收。
