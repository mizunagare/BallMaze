# B10 存档与入口边界（实施记录）

本轮没有新增多槽、Profile ID规则、存档版本或经济字段。仍是v9封装中的Profile/Run/Settlement、分页地面掉落和完整主备档集合；v1～v9兼容由既有迁移回归重新执行，结果最终以本批All为准。

Boot先检查目录和存档状态，Title展示当前一个自动档。Missing/Ready/Corrupt/Incompatible/Uncertain/待确认及已保存结算分别显示，不自动开始或覆盖。Continue/Read保留原Run、区域实例、seed、布局、随机流、装备ID、来源账和教程。New必须确认，使用原NewProfileTransaction staging/发布，不映射无确认Restart。

猫族显示名不改forest:warden/forest:tide、GearType、MaterialKind、设施四ID、配方、徽章和回执。湖面显灵为表现代理；已开箱、已生成奖励、地形版本和旧在途状态不因换皮重抽。B1扣费、来源保护和唯一结算未重写。

正式构建从Boot→Title→玩家选择→ForestRuins。Editor执行测试方法需要启动前隔离，正式Player不接受旧测试参数绕过Title。另建包含受控驱动的非开发验证二进制，明确不等于无测试驱动的发行二进制。

所有故障检查只使用工程外合成档，原始完整存档不上传。记录Initialize/Save/Load/退出审计与校验，不单凭exit0称干净关闭。标题按钮退出、后台WM_CLOSE、真实标题栏关闭和原生输入为不同证据。

定向测试曾在SaveSystem.Start完成前切换目录，导致外部指定fixture停留于旧营地快照；已修正驱动等待，并追加InspectReadOnly确认写盘ActiveRun。该历史失败保留，不放宽正式Player不变量检查。

B10-R1 6cad42d5仅增加界面未就绪状态与运行日志门禁，不新增任何Profile/Run字段或存档版本。Profile缺失时不创建空档，不存取/制造；实际初始化后恢复数据界面。旧药水/双武器LegacyHarness仍保留，但其无Profile状态不再引发UI空引用。修复前549次产品错误与对应FAIL审计保留。
