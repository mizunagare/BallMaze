# B2 遗迹必出装备边界修复（2026-10-24）

审阅/开始基线：`1be7ad6819aec8f642eae59f3b8d447686ca63b1`。开始核对本地 HEAD 与远端 main 一致；已有 ProjectSettings 修改保留，不暂存。此次只处理用户明确提出的遗迹必出装备边界，不进入 B3/B4/B07。

## 问题与最小改动

`WorldEventPoint.Interact` 原先判断 `Random.value < ChestGearChance(site)`。遗迹概率为 1，但 Unity 浮点随机值的上界也可为 1，导致该边界漏掉装备。新增 `ForestRewards.ShouldDropChestGear(site, roll)` 作为可验证判定：概率达到 1 时必定成功，其余地点保持原严格小于比较。实际宝箱调用依旧先采样一次 Random.value，再传入判定，不跳过或增加随机数消耗。

没有指定装备类型/品质保证，没有新增存档字段、重新生成旧布局、补发历史宝箱、改写来源账或结算。旧 revision1/2 的原奖励分支不变。当前事件已用标记、地面生成、手动拾取与防重复机制继续复用。

## 回归

`Tests/B2Rules.cs.txt` 在冒险测试开始前检查遗迹 roll=0、0.25、0.8、0.99999994、1，以及其他四类地点在 0、概率下方、恰好概率及 1 的结果。既有实际开箱、重复开启不发奖、拾取前来源账不增长、旧版奖励隔离、保存/新进程恢复仍执行。

修复前副本：新判定函数仍使用原表达式，仅提取测试缝；它在 roll=1 精确失败，exit1，未超时。修复后另建唯一隔离副本，不复用前轮结果。规则与正常 AI 的分类继续保留，不代替原生 UI 或人工理解。

## 实际结果

| 项目 | 修复前 | 修复后 |
|---|---|---|
| 遗迹随机值 1 边界 | FAIL，exit1，无超时 | PASS，exit0，无超时 |
| B2 完整领域流程及新进程恢复 | 边界先失败，Resume 依赖跳过 | PASS |
| 选定的 B1/A1/装备/容器/双武器/制造/掉落/存档/UI 规则 | PASS | PASS |
| 正常 AI 实际采集、修复、撤离、入库、制造、再出征及新进程恢复 | PASS（不修复边界失败） | PASS |
| 非开发 Windows 构建 | PASS | PASS，0 errors / 61 warnings |
| 92 帧受控 UI 捕获与布局检查 | PASS | PASS |
| 原生 U16 / 人工理解 | NOT_RUN | NOT_RUN |
| 历史 UNKNOWN 根因 | UNRESOLVED | UNRESOLVED |

修复前总计 32 PASS / 3 FAIL / 18 NOT_RUN / 1 UNRESOLVED，其中两个 FAIL 是原编排器预期故障探针，新增实际失败仅 B2Rules.Run；协调器 exit1。修复后 34 PASS / 2 预期探针 FAIL / 17 NOT_RUN / 1 UNRESOLVED，非预期失败为 0，协调器 exit0。无测试超时（预期超时探针除外），两轮最终受保护的运行进程列表均为空。

正常 AI 是 Editor 脚本驱动；后继出征为波次，重复森林由 B2 受控规则验证。规则内会禁用敌人，不可冒充正常 AI。未执行正式 Player 原生交互、标题栏关闭或人工理解，不继承旧轮 PASS，不重试 UNKNOWN。

[汇总](Evidence/BoundaryPatch/SUMMARY.json) / [修复前](Evidence/BoundaryPatch/Before/REPORT.md) / [修复后](Evidence/BoundaryPatch/After/REPORT.md)。具体命令、起止时间、真实退出码、超时状态、构建哈希、初始化审计和轨迹均随证据发布。完整日志经既有脱敏器发布并列转换前后哈希，不上传合成存档本身、玩家档、构建二进制或缓存。

原始根位于 `C:/Users/guan/Documents/unitytest/WanxiangB2BoundaryBefore/20261024-113044-b4924cd3` 与 `C:/Users/guan/Documents/unitytest/WanxiangB2BoundaryAfter/20261024-113309-e3c3846b`。两套独立目录；修复前保留原比较表达式的 ForestRewards 源码快照。72 个业务源码与修复后隔离副本归一化 LF 字节一致，见 source-provenance.json。旧 B2 Evidence/Final 及所有失败历史保留。

## 复跑与限制

按 [TESTING](TESTING.md) 的 GameplayOnly 命令运行即可自动包含新增边界断言及既有实际开箱/防重复/来源账/恢复链。可单独用隔离副本执行 `B2Rules.Boundary`，仍须启动前显式 `-wanxiang-storage-root` 和 UNITY_TEST_ROOT。重现旧失败时仅在全新隔离副本将判定返回式改为 `roll < ChestGearChance(site)`，保留新测试，不改真实工程或玩家档。

本轮不扩展奖励规则，不保证特定装备品质，不修复历史已开箱结果；推送不等于复审通过。
