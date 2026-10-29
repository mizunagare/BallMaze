# WORLD-01 失败与尝试

| 尝试 | 实际结果 | 处理及边界 |
|---|---|---|
| Before/WorldFeedback | exit1，consistent=false | 两名活Boss、预计核心4，与“森林无核心”矛盾；真实产品反馈负例 |
| After/WorldFeedback | exit0，一致且只读 | 最小提示修复；不同合成Run，不冒充同一身份 |
| Samples/418-A/Run | C#编译失败；包装器FAIL | 夹具错误访问 internal CaptureLegacy；改为公开保存+InspectReadOnly，不改变产品访问权限 |
| 418-A 清理 | 首次editor-close NOT_RUN | Safe Mode对话框没有精确Editor主窗口，未宽泛回退、未发物理输入 |
| 外部清理Worker首编译 | CS0136，exit1 | 局部变量冲突，修工具变量名；未修改共享Worker源或产品 |
| 418-A Safe Mode Quit | 自有Editor实际exit0、无超时/强杀 | 仅精确拥有者PID、inactive desktop、Safe Mode/Quit；原编译失败仍FAIL，不算正常Player退出或原生UI |
| Samples/418-A2/Run | 内部240秒deadline，exit1；外部未超时 | 击杀后真实升级选择暂停，夹具等scaled time未处理；改用真实SelectChoice并限定等待，不清成长/不改TimeScale绕过 |
| Samples/418-A3及五后续样本 | 均PASS | 修夹具后每例独立目录；原A/A2不删除，不称总尝试100%通过 |
| Build | DirectoryNotFound，exit1 | 验证器预构建输出目录不存在，BuildPlayer未开始；薄包装器先创建已验证隔离根 |
| Build02 | Succeeded，0E96W | 完整构建消息保留；有五个隔离设置文件被Unity重序列化 |
| 汇总前置保护文件缺失 | FileNotFound，exit1 | 工具拒绝不完整前置输入；补真实哈希后再读，没有填造结果 |
| Build03 | Succeeded，0E2W（增量） | 有界输入复验1375文件不变；不是修复94条警告，原96条完整清单保留 |

首个编译尝试/外部清理工具首编译未单独冻结完整当时源码，只保留实际日志/错误记录和清理回执，不重构文件冒称原件。后续冻结夹具、所有有效样本实际执行源及哈希可定位。

六份有效样本没有生成重试、fallback、身份重复、路径或保存不一致。源数据原件保留在拥有者根，发布日志gzip附原始SHA256。旧RUNLOOP/COMBAT历史3589文件不变。D3D12、青色帧、Search、JobTempAlloc、旧C15不关闭，原生/人工/性能仍未执行。
