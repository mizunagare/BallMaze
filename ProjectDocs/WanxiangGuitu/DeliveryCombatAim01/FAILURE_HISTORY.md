# 失败与中间尝试（原始文件不覆写）

| 尝试 | 原始结果 | 核查 / 后续 |
|---|---|---|
| Before 缓存副本 | deadline/无CombatSession，旧catch误exit0及空结果 | technical-evaluation单列FAIL，不当通过；新鲜Library+明确playModeStartScene=null；首因未单独证明 |
| BeforeFresh / BeforeFrozen / BeforeFinal | 各18P/13F | 实际旧版输入与目标HP，固定实体后的最终旧例为BeforeFinal，不合并独立样本数 |
| AfterCore | 29P/2F | FindObjects.First并未固定实体，不称严格配对 |
| AfterFrozen | 29P/2F | 矿前真实石头先挡住枪口；改为验证矿无伤、前景资源受伤，保留原2F，未移走障碍 |
| PhysicsProbe | 非凸Mesh ClosestPoint不支持原始警告 | 有效物理API边界探针，不当发行产品失败；仅实际overlap后使用当前位置，不放宽可伤害几何 |
| RulesInitial | 205P/2F | 一个真实墙内起始爆炸越墙20伤害，增加solid-origin阻断；一个同ID主/备用武器夹具，改为不同真实物品ID；100次只读查询后合并为一个断言，不重复统计 |
| RulesFinal / Extended | 108P、后132P | 后者额外真实发射验证高/普通、近中远目标，未放宽断言 |
| AcceptanceLaunch | compiler exit1 | 新增测试误写InteractionOffer.id，修正为已有targetId；不改产品接口或吞编译错误 |
| Runtime 103900 | OS exit1，HP断言过早 | 驱动2537帧断言，真实2550帧释放、2559帧命中HP70→37；用有界实际时长等待替代固定25帧，原时序不改 |
| RegArea | 29P/5F | 首次未等启动门禁释放3F；另两项Sphere代理不是同形CharacterController重复，实际弓独立箭分别接触，非同箭重复伤害 |
| RegArea2 | 32P/2F | 初始等待修正；保留代理差异的实际发射/接触日志：两颗不同index箭各命中。CharacterController查询与Sphere有效表面不同，不能称完全相同几何 |
| RegArea3 | 34P/0F | 同形重复使用同height/radius/center/skinWidth的CharacterController，保持原每箭预算、伤害比较断言；并非给产品加“不伤害重复Collider”例外 |
| Story2 | Core/Resume PASS | 中间构建准星字形18px容器被22字号裁切，截图证据揭示；改32px容器，新增实际字形网格断言，不沿用为最终显示通过 |
| FinalStory | 两进程PASS、无超时 | 最终新构建/新合成档，完整重跑核心用例及恢复；两exit0仍仅受控验收退出 |

四个COMBAT-02原始exit1、既有失败和三批原证据均未改写。本批没有诊断并关闭历史引擎根因，没有为了全绿降低历史结果。各Unity日志包含原有引擎/授权/图形警告，原文压缩归档（凭据字段脱敏，原始SHA单列）。
