# UX-TECH-01 验收表

不把断言数、进程数、源码审计项相加成单一通过率。各层实际数字见 REPORT/SUMMARY；旧结果不继承。

| TASK §6 | 当前证据与结论 | 层级/限制 |
|---|---|---|
| 1 默认/别名/冲突/非法输入 | 本轮 InputRules 26 项；InputStory 虚拟设置操作与取消/默认/应用 | 受控规则+虚拟uGUI；物理键鼠 NOT_RUN |
| 2 Down/Held/多消费者 | 源码每帧缓存、既有239项实际消费者；新Held双读/释放用例 | 有限自动化 PASS；并非所有时刻/设备排列穷尽 |
| 3 Focus/设备/长按 | Before 相关失败保留；After 新鲜输入恢复/持有键拒绝 | 模拟Focus与虚拟键盘替换 PASS；OS真实切换/热插拔 NOT_RUN |
| 4 主要UI/屏障/返回 | InputStory 设置、背包、HUD帮助/路线、营地、保存、关闭帧 | 源码表+有限虚拟UI回归；原生操作 NOT_RUN |
| 5 暂停/死亡/升级/营地/保存/结果 | 新死态即时拒绝；暂停时钟用例；旧状态业务门及新InputStory | 各实际结果见独立回执；完整交叉组合 NOT_RUN |
| 6 指针/UI/EventSystem | Before unlocked+缺EventSystem允许消耗技能；After拒绝+零消耗，既有虚拟鼠标消费者 | 受控输入 PASS；真实系统焦点 NOT_RUN |
| 7 提示/键帽 | InputStory 实际重绑定后HUD/帮助；新进程K技能消费者 | Editor真实产品代码+虚拟输入；不是人工可读性 |
| 8 保存/失败/Unknown/恢复 | 原偏好失败/损坏/冲突回归，新发布中改写负例，实际v9新进程Run/回执/来源账 | 有限回归；不更改v9合同，不声称全故障模型覆盖 |
| 9 正常AI | 本轮NormalRetry1/2/3实际结果和轨迹 | Editor正常AI，不能称正式Player冒险或人工 |
| 10 非开发/隔离Player/纯发行 | 实际构建消息、PE检查、Runtime与Runtime2独立结果 | 验收Player虚拟输入；纯发行无驱动与Editor引用；不等于原生U16 |

## 不关闭的项目

- 原生U16/物理键鼠、真实设备插拔：NOT_RUN。
- 独立人工理解、舒适度、趣味/手感：NOT_RUN。
- 完整性能验收：NOT_RUN，本轮未授权性能优化。
- D3D12 UNKNOWN、旧C15、Editor青色帧、Search/JobTempAlloc历史根因：UNRESOLVED；未重新实验，不修改历史FAIL。
- 任意菜单组合、所有设备排列、非合作跨进程设置写入的绝对互斥保证：不在有限证据中声称完成。

提交、构建及exit0不等于ChatGPT独立复审通过。交付后暂停。
