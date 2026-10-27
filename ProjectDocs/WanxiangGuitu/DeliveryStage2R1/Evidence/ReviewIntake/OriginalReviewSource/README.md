# 阶段2独立离线复现材料

仅对仓库 `Summarize-Matrix.py` 做离线合成回执实验；未运行Unity、未访问玩家档、未修改GitHub。

`source-provenance.json`记录原脚本固定提交和Git blob，复制后的脚本逐字节匹配原blob。

运行：

```bash
python reproduce.py --output /absolute/path/to/a-new-directory
```

Python标准库即可。输出目录必须不存在。Windows也可使用新的绝对路径。

4例：正常对照、已开始但指标缺失、PASS自报与终态/身份矛盾、中断局部时长混入完整均值。
`results/review-results.json`为本次实际输出，逐例保留输入、输出、stdout/stderr。

这证明汇总器的特定异常处理行为，不证明历史19局记录被篡改或游戏产生了这些故障。
程序中的断言用于重现旧行为；修复后的测试应断言相应非法回执被拒绝、样本正确登记和分层。
