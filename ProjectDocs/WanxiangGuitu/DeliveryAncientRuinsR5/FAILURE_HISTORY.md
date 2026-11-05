# 失败历史

| 尝试 | 实际结果 | 后续证据 |
| --- | --- | --- |
| 首次取证 DLL 编译 | 缺少 UnityEngine.ScreenCaptureModule 引用。 | [首轮编译日志](Evidence/render-compile1.log.gz) · [加引用后编译](Evidence/render-compile2.log.gz) · [最终取证编译](Evidence/render-compile3.log.gz) |
| 首次原生符号解析 | DbgHelp 按映像载入失败，错误 126。 | [首次结果](Evidence/Audit/symbolize-first-attempt.json) · [直接载入经 GUID/age 核对的 PDB](Evidence/Audit/symbolized-writebacks.json) |
| 首轮画面 | 营地背包遮住部分画面，标题 A/B 有 1,927 像素差异。 | [原图对照](Evidence/RenderComparison1/montage.png) · [首轮像素数据](Evidence/RenderComparison1/pixel-metrics.json) |
| 最终两轮画面 | 标题严格匹配，六个场内机位仍未严格匹配，同包复跑也有差异。 | [复跑对照](Evidence/Audit/repeatability.json) |
| 独立跟踪构建退出 | 构建及进程成功，退出日志仍报告 JobTempAlloc。根因未调查。 | [Unity 原始日志](Evidence/NativeProject-Build/Unity.log.gz) |

历史 R4 失败、资源分析和 R3 产物按原路径保留。[R4 失败历史](https://github.com/mizunagare/BallMaze/blob/8a4ce422f97174160662e8f9acb7982e9d68502b/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR4/FAILURE_HISTORY.md) · [R4 清单复核](Evidence/Audit/protected-inputs.json)
