# S2-R1 独立复审材料

审核对象：mizunagare/BallMaze，最终提交 b4a08e98f6de5cd56d192deb9f027f988d03afd9；冻结输入583f19d905aa1b8d8b575f2441bf942b1e37b24f。

本包只含合成回执测试和仓库已发布的战斗统计CSV，没有真实玩家存档、Unity工程、游戏二进制或凭据。

## 文件

- `source/MatrixEvidence.py`、`source/Summarize-Matrix.py`：最终交付的精确源码；Git blob核验见`source-verification.json`。
- `source/MatrixEvidence.frozen.py.txt`：冻结版原件，仅首行说明文字与最终版不同。
- `reproduce.py`：审核方编写的12场景独立复现，使用真实CLI子进程。
- `results/final_commit/`：最终版真实执行输入、原始输出、每例摘要及总表。
- `results/independent/`：先前对冻结版执行同12场景的原始结果；不是另一组12个新场景。
- `submitted-evidence/combat-results.csv`：仓库已发布26行统计，CRLF原字节blob验证通过。
- `combat-arithmetic-check.json`：独立计数、身份去重、TTK与配对差值计算；不代表重新运行Unity。
- `REVIEW_AND_S2R2_TASK.md`：本次复审及下一轮限定任务。

## 复现

```bash
python reproduce.py --output /absolute/path/to/nonexistent-output
```

Windows可使用一个尚不存在的工程外绝对路径。需要本机Python支持`Path.is_relative_to`，不安装第三方依赖、不联网。

脚本首先核对源码Git blob；输出观察结果，并不把被审程序错误PASS当成正确性PASS。最终程序仍有：错误阶段根类型通过、计划独立缩减必要阶段通过、NOT_RUN计为started、身份冲突的终态仍加入已知成功统计。

完整对照、旧空Run反例、缺阶段文件、缺最终指标的已出征案例、完整60秒/部分2秒也一并保留，体现已完成的修复。

固定原件不能为修复测试而覆写；Codex应在独立候选源码目录建立修复后断言及结果。详情以任务书为准。
