# BUILD-01 失败与尝试

| 顺序 | 独立根 | 结果与处理 |
|---|---|---|
| 历史 | INPUT-01 FinalFrozenValidation/20261027-161647-ab2a444e | 目标路径 260；首次导入失败，后续 Succeeded + 2 Error/91 Warning；未修改该根 |
| 1 | 20261027-173924-Long-086d18f4 | 工具 CS0104：PackageInfo 歧义；Unity/协调器 exit 1，尚未执行构建。以完全限定别名修复，只在新目录重跑。保留原失败源与日志 |
| 2 | 20261027-174115-Long-7b1262fc | 实测目标路径 251；目标 ComputeShader，0 Error/91 Warning；其他较长包文件仍有导入异常，未伪称干净导入 |
| 3 | 20261027-174542-Long-383ac3cb | 将前缀准确设为旧值 113；目标路径 260、DefaultAsset、普通读取失败、扩展只读成功；复现相同两阶段 Error。预期的质量 FAIL，取证进程 exit 0 |
| 4 | 20261027-175029-Short-85699e2d | 短根修复验证，新 Library，目标路径 194；0 Error/91 Warning，包路径异常 0 |
| 5 | 20261027-175503-Repeat-d42b8bc9 | 工具冻结后另一新工程，新 Library，重复短根验证；完整结果见 RESULTS |

两次独立离线预检结果均保留；其中实际超限 prepare 子进程预期 exit 1，证明拒绝发生在创建工程/结果目录之前，不是游戏失败。

首次审计辅助 Python 曾直接普通路径读历史长 `.meta` 抛 FileNotFoundError；随后只读审计使用扩展路径取得相同 meta/GUID。该探查错误没有触发构建或修改历史文件；命令问题与产品问题区分记录。

新 BuildReport 仍有 91 条警告；Editor 原始日志 JobTempAlloc 等不删除。历史 INPUT-01 的日志、BuildReport、失败结果均未覆盖。没有对 D3D12 UNKNOWN、Editor 青色帧、Search 或 JobTempAlloc 作修复结论。
