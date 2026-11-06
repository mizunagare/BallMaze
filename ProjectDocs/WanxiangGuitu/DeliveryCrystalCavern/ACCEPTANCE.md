# C2.1 验收

| 项目 | Editor | 非开发测试 Player | 证据 |
| --- | --- | --- | --- |
| 三段实际往返、巡守移动、顶盖和实体晶柱 | PASS | PASS | start 与 restore 记录 |
| 铁矿和晶石真实命中、掉落、拾取，重复拾取拒绝 | PASS | PASS | start 记录 |
| 新进程恢复同一 Run、矿脉与库存 | PASS | PASS | restore 记录 |
| 脉冲预警、范围外规避、墙隔离、暂停、真实伤害、单次脉冲不重复伤害 | PASS | PASS | start 记录 |
| 死亡结算和危险区卸载 | PASS | PASS | death 记录 |
| 七武器普攻和默认技能实际释放、法杖撞墙 | PASS | PASS | weapons 记录 |
| 真实免费撤离、确认结算、返回营地、新 Run 矿脉恢复 | PASS | PASS | restore 记录 |
| 旧森林与 C1 在途兼容 | PASS | PASS | 旧档恢复和森林/C1 接口测试 |
| URP Lit 新材质与剔除、实际肩后截图和连续记录 | 适用配置读取 PASS | PASS | 包内材质、BuildLog、实际截图和连续轨迹 |

独立纯包构建与标题退出 PASS。最终选定运行统计为 Editor 9 次、146 个 PASS，非开发 Player 10 次、187 个 PASS，均 0 个 FAIL。连续采集是单独重复样本。人工体验/原生键鼠、最终平衡、未经校准的 GC/GPU 各为 NOT_RUN。洞窟扩展内容留待后续授权。过程中的 FAIL 不进入最终通过计数，原结果独立保留。[证据索引](Evidence/INDEX.md) · [历史失败](FAILURE_HISTORY.md)
