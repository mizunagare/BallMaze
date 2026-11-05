# 失败与中间尝试（追加，不覆盖旧交付）

上批全部文件保留：[MAPTOOLS02失败历史](../DeliveryMapTools02/FAILURE_HISTORY.md)。本批原始目录`I:/WGCombat/MAPTOOLS03-A`，下列每个目录均独立，未重用输出文件名。

| 顺序 | 尝试 | 实际结果 | 处置与保留 |
|---|---|---|---|
| 1 | Prepare1 | exit1，CS0619：GetInstanceID已禁止使用 | 改自有观测工具为GetEntityId；源码快照/编译日志保留 |
| 2 | Prepare2 | exit0 | 创建本轮自有Scene与Profile基础 |
| 3 | BuildEmpty1/Terrain1/Audit1 | Build成功，但Profile替换正则未匹配实际换行，仍是旧MT02场景列表 | 三项不能当正确实验控制；保留原BuildReport/日志/工具快照 |
| 4 | Audit1 | 实际运行旧MT02Runtime，缺少MT02_OUTPUT而异常 | 没有本轮有效语义结果。自有窗口正常WM_CLOSE结束，不当业务PASS |
| 5 | close-request | NOT_RUN：未传完整exe身份 | 请求被保护拒绝；补齐owned exe+inactive desktop后close-request2成功排队关闭，保留两次请求 |
| 6 | BuildEmpty2/Terrain2/Audit2 | 构建0错；原生JobTempAlloc仍存在 | 改自有Profile写入为明确字段边界拼接，并强制实际BuildProfile.scenes逐项断言；没有放宽场景范围 |
| 7 | Audit2/Memory1/Memory2 | 完成真实循环，无断言FAIL | GC正控制失败、Player GPU控制无响应，保留NOT_RUN |
| 8 | BuildAudit3/Audit3 | 加入材质光滑度控制和双向法线观测，构建及运行完成 | 保留原高度和资源，返回后恢复全部运行时试验设置 |
| 9 | EditorPlay1 | 真实Editor Play运行完成 | Editor GPU校准可响应；GC仍NOT_RUN，不能替代Player校准 |
| 10 | analysis-attempt1 | Python exit1，memory-only没有gpu-status.txt | 将协议明确未执行GPU记为NOT_RUN，不伪造文件 |
| 11 | analysis-attempt2 | Python AssertionError，错误套用Player的TerrainData=0到Editor | 审阅4项持久资产身份；保留独立活动Terrain卸载断言，按层解释Resources库存，不篡改原结果 |
| 12 | analysis-attempt3 | 全部真实结果与摘要一致性检查完成 | 不修改任何历史JSON |

原始工具日志与已运行C#快照在Evidence各同名目录；本机原始日志完整保存。公开日志的许可标识与原生堆hex载荷做脱敏，manifest记录源/公开双SHA及转换说明。警告、异常和堆栈没有删掉；没有用最终成功覆盖旧exit1。

新增风险继续开放：Player总跟踪分配漂移、原生Shader编译退出释放原因、供应商版本解释。历史UI-01、Editor青色帧、原生U16和人工理解性没有在本研究中关闭；本轮无人工试玩。

文档整理时另有一次Python默认GBK读取UTF-8报告导致UnicodeDecodeError；该命令未写入文件，随后显式UTF-8读取与写入。没有影响任何Unity运行或原始结果。
