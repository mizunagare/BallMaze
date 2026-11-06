# CP06-C2.1 水晶洞窟

起点 712fffb7eb9196dfbb7d880e4c31a4c21e0dd28e。先归档带开放项的 C1 内部检查点，再在独立 feature/cp06-crystal-cavern 实施洞窟入口、矿脉区和能量通道。[C1 检查点](C1_INTERNAL_CHECKPOINT.md) · [区域和资产](CAVERN_LAYOUT.md)

洞窟为固定室内 Prefab。营地选区复用现有出征和 v9 恢复。两处普通矿脉经过真实武器命中、地面掉落和交互拾取。能量区使用与画面标记一致的体积和实体射线遮挡，提供预警、放电、恢复和侧道绕行。现有七武器、软锁定、自动面向、肩后镜头及撤离规则继续使用原实现。[矿脉及危险区](MINING_AND_HAZARD.md) · [存档](SAVE_COMPATIBILITY.md)

隔离 Editor 与非开发 Player 分别核对通行、巡守、矿脉流转、能量区、七武器释放、墙体阻挡、回营和恢复。Player 的恢复进程核对同一 Run、耗尽矿脉和已拾取数量，6 份铁矿进入正常撤离结算。法杖投射物实际接触「转角南壁」。两种矿脉均有独立实采记录。另有 120 条连续采集样本和五张肩后画面。[Editor 146 PASS、Player 187 PASS 的逐进程汇总](Evidence/Audit/results.json) · [验收](ACCEPTANCE.md) · [过程及原始证据](Evidence/INDEX.md)

最终纯发行 Windows64 构建 Succeeded，0 错误、104 条 BuildReport 警告，实际 Editor 退出码 0。纯包实际到达标题并正常退出。Development=false、Bee 五项关闭，纯包没有观测程序集。纯包 193 文件，Assembly-CSharp.dll SHA256 为 5ceb245a2e3428a19204c491eef3bfc52171bfbfaeaa6c1cfff10ef82fb110bb。通用 EXE 哈希与历史版本相同，发行身份以完整清单和产品程序集核对。隔离构建副本出现六项 Unity 序列化差异，五项既有配置/管线写回及一项父 Resources 文件夹 meta。新洞窟资产与最终构建输入核对一致。用户项目文件未被复制覆盖，2,413 项保护文件与 C1 两套原始发行包均复核通过。[发行核查](Evidence/Audit/release-audit.json) · [完整清单](Evidence/Audit/release-manifest.json) · [构建输入差异](Evidence/Audit/build-input-differences.json) · [原始构建日志](Evidence/PureBuild2/Unity.log.gz)

洞窟材质使用已有 URP Lit。最终包的 resources.assets 中核对七份材质的 Shader 引用、基色和关键字，且实际 Player 验证 Shader 可用并显示三色相位。构建日志的 URP Lit ForwardLit 保留数据单独记录。最终能量相位使用材质基色。人工体验、原生键鼠、最终平衡和校准性能保持待验证。[包内材质](Evidence/Audit/packaged-cavern-materials.json) · [构建剔除记录](Evidence/Audit/lit-build.txt) · [已知边界](KNOWN_ISSUES.md)
