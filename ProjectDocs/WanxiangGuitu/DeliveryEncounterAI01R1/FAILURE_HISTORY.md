# 所有尝试保留

目录相对本批Evidence，原ENCOUNTER-AI-01目录不变。

| 尝试 | 实际结果 | 分类/处理 |
|---|---|---|
| Before | 编译exit1 | Unity固定版禁止SceneHandle→int隐式转换；工具改GetRawData，不改依赖 |
| Before2Store | 64PASS/16FAIL | 12威胁生命周期失败+4普通敌恢复夹具失败 |
| AfterStore | 76PASS/4FAIL | 单行产品修复后12项转PASS；仍有4夹具问题，未改判 |
| BeforeFinalStore | 68PASS/12FAIL | 修正Guard空区域仍启用的测试配置；相同基线继续暴露12真实失败 |
| After418Store | 80PASS | 第一版固定418聚焦例，不冒充覆盖全部seed |
| After419Store | 79PASS/1FAIL | 潮矢真实命中失败，最初编排停止下一seed；原420未运行，不偷填PASS |
| Lane419Store | 只读诊断 | 原射线被石柱在9.611793米挡住；2项seed元数据断言不算生命周期通过 |
| BeforeClear418Store / BeforeClear419Store | 各68PASS/12FAIL | 新有界无遮挡初始姿态规则，旧版仍精确失败同12项 |
| AfterClear418/419/420Store | 各80PASS | 新同条件聚焦结果，旧失败仍在原处 |

无遮挡夹具最多扫描8个现有导航候选；原候选和遮挡名称也记录。不能找到合法点会失败，不换seed、不清障碍、不关闭碰撞、不降低“实际扣血”断言。仅受控初始位置变化，不是产品难度/地图修改。新两版相同驱动/配置/候选日志逐字节配对；不将旧夹具与新夹具混为同输入。

8个既有回归阶段均实际exit0；最初verification-processes整体仍包含After419的FAIL，不删除或改为全绿。最终聚焦结果另存clear-lane-processes.json。

PureBuild首次0E96W，PureBuildFinal缓存0E2W，完整消息分别保留。缓存只输出Boot/Title两条旧序列化告警，不视为94条编译警告被修复。

UI01 UNKNOWN、C15、青色帧、Search等历史根因UNRESOLVED；原生/人工NOT_RUN。无强杀、外部软件/快捷键或依赖调整。
