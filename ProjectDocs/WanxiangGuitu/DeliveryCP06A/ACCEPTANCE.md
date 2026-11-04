# CP06-A验收表

产品基准397d53fe87ce5b6c490c86c63d59015de26a46af；独立分支，不合并main。状态按层次列明，未执行项不能由受控PASS替代。

| 条目 | Editor | 非开发测试Player | 主要证据 |
|---|---|---|---|
| 四武器各2新技能，稳定ID/配置 | PASS | PASS | skill-0..3-1/2及skill-config.json |
| 真实前摇/释放/碰撞/伤害/恢复 | PASS | PASS | 核心157行；各技能jsonl及真实HealthObservation |
| 动画在真实释放阶段有效 | PASS | PASS | release-animation逐段断言，实际绑定4类原剪辑 |
| 墙体不可穿越、不是选中即命中 | PASS | PASS | wall-0..3-1/2；贯矢、符阵及旧弹体实际物理 |
| 多Collider/独立脉冲去重 | PASS | PASS | 额外Collider，new-skill-no-duplicate-collider |
| 按住蓄势及3实体实际贯穿 | PASS | PASS | 虚拟InputSystem Held，3真实接触；旧阵列失败不覆盖 |
| 取消不伤害、不退冷却 | PASS | PASS | 每技能cancel；真实Dodge、uGUI切换及暂停 |
| 已释放物暂停/恢复/切武器 | PASS | PASS | 实际弹体位移、时间、碰撞；符阵脉冲冻结恢复 |
| 有限近战辅助、远程软锁定/自由镜头 | PASS | PASS | 未改参数，真实接触及相机未强转 |
| 普攻→技能→普攻衔接 | PASS | PASS | 真实恢复门槛及拒绝跳过阶段 |
| 敌人真实AI致玩家死亡后的清理 | PASS | PASS | 未改HP/伤害，dead拒绝与效果清理 |
| 前摇真实保存、新进程继续 | PASS | PASS | Save/Resume；Run、装备ID、Profile、三流和cooldown |
| v9无字段/版本变化，无待发动作重播 | PASS | PASS | 实际Envelope.version=9，读档默认旧槽 |
| 旧四武器8条实际路径配对 | PASS | PASS | legacy.json；伤害、发射数及旧7秒冷却不变 |
| CP05重开、临时掉落、唯一性 | PASS | PASS | 各92行新运行 |
| 旧正式森林掉落/经济/随机流 | PASS | PASS | 各480组工厂规则+实际同Run剑击死亡配对 |
| 产品/用户文件保护 | PASS | PASS | 2349项保护核验；仅旧AdventureCombat的10处接入及新增3脚本 |
| 正式发行包无驱动、Privacy关闭 | PASS | PASS | 18类产品IL相同；Development=false，实际Bee5字段false |
| 纯发行普通启动/退出 | NOT_RUN | PASS | PureSmoke，仅启动/窗口普通关闭，非人工操作 |
| 原生物理键鼠 | NOT_RUN | NOT_RUN | 虚拟输入不替代 |
| 独立人工观感/音质/手感/最终平衡 | NOT_RUN | NOT_RUN | 未安排真实独立试玩 |
| 完整自主AI冒险/新Profiler性能 | NOT_RUN | NOT_RUN | 不继承旧PASS或填零 |
| Search/JobTempAlloc及历史引擎根因 | UNRESOLVED | UNRESOLVED | 完整原始日志保留；不凭exit0关闭 |

核心157+附加14+保存7+恢复10=188/层，另旧回归135/层，共646 PASS/0当前FAIL。20项配对/回执汇总与功能有重叠，单列不累加。历史32条断言FAIL及工具失败见FAILURE_HISTORY，未删除或改写。

[核心Editor](Evidence/AfterEditorFinal/probe.json) · [核心Player](Evidence/PlayerFinal/probe.json) · [附加](Evidence/ExtraPlayer/probe.json) · [保存](Evidence/SavePlayer/probe.json) · [恢复](Evidence/ResumePlayer/probe.json) · [数据配对](Evidence/analysis.json) · [保护](Evidence/protection-final.json)
