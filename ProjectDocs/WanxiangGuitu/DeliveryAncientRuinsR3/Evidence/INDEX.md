# R3 证据索引与复跑

原始证据使用 I:/WGCombat/C1R3-1105-A。发布只压缩或脱敏副本，源与发布哈希见 [清单](manifest.json)。构建二进制留在隔离本机目录，使用 [全包 SHA256](build-files.json) 核对。

- [白色实际运行和离线复算](Audit/white-audit.json)，各原始 White1–White8 目录包含进程命令、实际退出、语义结果与地面存档页。
- [固定构建校验](frozen-build-check.json) 和 [双副本输入清单](frozen-inputs.json)。
- [首次导入](ProjectA-Import/)、[导入后构建](ProjectA-Build/)、[首次打开即构建](ProjectB-Build/) 的输入快照、写回样本与原始日志。
- [构建输入与运行文件对照](Audit/build-audit.json)、[序列化字段对照](Audit/serialized-fields.txt)、[二进制差异](Audit/runtime-byte-deltas.json)、[变体计数](Audit/shader-variant-counts.json)。
- [纯包 A 实际启动](PureBootA/pure-runtime.json)、[纯包 B 实际启动](PureBootB/pure-runtime.json) 和 [旧原始证据保护](Audit/protection.json)。

复跑使用当前目录 Tools 下的脚本及全新隔离根。Prepare.py 接受与 R2 产品树一致、LFS 已实体化的本机参考工作树与输出根。Invoke-CleanUnity.ps1 依次对 ProjectA 执行 Import、Build，再对 ProjectB 执行 Build，工具复用私有非活动桌面与既有 Windows Player 启动器。白色复跑用 Invoke-Player.ps1 调用哈希核对后的 R2 VerificationBuild 和 r2-white 模式，每组使用唯一根。Audit-White.py、Audit-Build.py 与 Audit-History.py 只读复核原始记录。纯包使用 Invoke-Pure.ps1 与正常保存产生的合成存档。
