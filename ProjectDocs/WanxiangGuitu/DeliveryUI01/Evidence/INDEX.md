# 本轮证据索引

- CleanVerified：最终 fresh copy，30方法全部退出0、无超时；results.json、summary、ui01-results、旧领域结果。logs.zip 为本轮原始日志。
- FinalCurrent：最终产品代码的针对规则、B1 Run/Resume与非开发构建；根 BuildSummary 与 build-hashes 记录实际构建。
- NormalLatest：原工程正常AI自动完整路线和独立进程Resume，4+实际游戏截图、CSV、日志与启动到退出存档审计；不是人工试玩。
- LatestRejectMissing / Relative / LocalLow：本次预Play隔离拒绝，预期exit1，无审计，合成哨兵不变。
- BeforeEvidence：3574基线8张真实受控截图、退出0。baseline-source-proof比较关键旧源码。
- ScreensFinal：最终92张实际受控截图，visual-layout记录帧/尺寸/缩放/可见组/目标，退出0。NPC关闭；uncertain/save-failed为合成故障，非真实档损坏。
- ReleaseUI：无运行验证驱动的正式包启动真实窗口；F1被外部Snipaste截获，后续原生操作/正常退出/继续NOT_RUN。hidden launch和被清理进程非正常退出证明。
- Rules / Full / Full2 / Verified / Screens：早期失败与超时原始记录。不可当作最终通过证据；具体修正及最终重跑见REPORT。
- runtime-source-correspondence：最终源工程与出包隔离工程非Editor C#及Resources逐项字节一致。源码SHA是未归一工作文件哈希，不作为Git自动换行后的通用哈希。

没有提交完整合成存档或真实玩家存档。日志中的绝对路径属于当次隔离根；复跑参数见TESTING。压缩日志原字节保留。未验证项不能用旧批PASS覆盖。
