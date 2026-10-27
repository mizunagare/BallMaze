# S2-R2 独立复审材料

审核提交：`a5e770064eedb8bfc478e54d54732b991f454658`。
本包只含代码快照、合成回执、离线测试输出和审核说明；没有Unity运行、真实玩家存档或构建包。

## 已实际执行

- `executed35/results.json`：仓库原35项，35 PASS。
- `executed58_final/results.json`：仓库新增58项，58 PASS；完整进程回执见 `executed58_final.exit.json`。
- `original12/`：使用上一轮独立复现脚本及其原版被审源码，原样重建的12场景。这里包括旧缺陷的错误PASS，不是候选通过。
- `candidate12/results.json`：本次最终候选对同一输入的12项审核方断言，12 PASS；输入哈希前后未变。
- `source-provenance.json`：实际运行源码逐字节Git blob、SHA256及LF/CRLF核对。
- `REVIEW_RESULTS.json`：分组结论。各组覆盖有交集，不相加为105种独立条件或105次游戏测试。

`executed58/` 和 `executed58_complete/` 是审核侧20秒、45秒容器命令期限中断的旧尝试，分别留下38、47份断言。原件保留，不拼接为最终58通过；原因见 `reviewer_attempts.json`。最终58来自独立新目录、一次完整执行。

## 复跑

在解压目录运行：

```bash
python -B run_review.py --output <不存在的绝对路径>
```

Python环境需支持当前脚本使用的pathlib/ast接口。本包在Python版本见source-provenance.json的环境实际执行，标准库之外无依赖。
复跑入口先验证四份源码的Git blob；输出到新目录，原始材料不被覆盖。240秒是每个自有离线子进程的安全执行截止，不是游戏性能指标。
`run_review.py` 是便捷复跑入口，交付前已做语法检查。本次实际结果来自上述各组已执行命令，而非声称新包装器已经又把全部组跑了一遍。

## 范围

历史46个原案例的本机拥有者根不在本审核环境，本次只读取交付方重审脚本、报告片段与索引，不用公开摘要重建完整原件。
原生UI、独立人工、性能、UNKNOWN/青色帧/Search/JobTempAlloc根因均不由本包关闭。
本次未改GitHub。下一轮任务见随附Markdown。
