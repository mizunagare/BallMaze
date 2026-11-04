# 证据索引

原始根I:/WGCombat/MAPTOOLS02-A，原始文件不改写。发布副本只做脱敏/压缩，[manifest.json](manifest.json)逐项记录来源路径、原始SHA256、发布SHA256和脱敏标记。没有发布供应商源码/包、Player二进制或真实存档。

## 基准、来源与保护

- [独立所有权](owner.json)、[原始包信息](package.json)、[包模块/旧meta审计](package-audit.json)。
- [实际本地包头](Version1/native-package-metadata.txt)：id165180、版本2.1.20；Build1首次空探测保留，不当证据。
- [保护前2413项](protected-before.json)、[保护后](protected-after.json)：无变化、无新增。
- [199项供应商源码对原包](source-protection.json)：没有源码修改。
- [manifest与lock未升级](package-lock-check.json)：与既有独立工程相同字节。
- [自有资源SHA/来源](asset-manifest.json)、[最终驱动一致性](driver-consistency.json)。

## 生成与历史失败

- [Generate1结果](Generate1/editor.json)、原日志与ExecutedTools：58PASS/2FAIL，错误销毁持久Graph及邻接假设；实际exit1。
- [Generate2结果](Generate2/editor.json)、[18组原始数据](Generate2/generation.csv)、[墙钟分布](generation-summary.json)。
- EditorPlay1加载失败日志、缺少完成回执；owned-editor-close.json只证明受控清理，不是业务通过。
- [EditorPlay2旧湖泊FAIL](EditorPlay2/runtime.json)与逐帧CSV；地图/目标未为测试成功而改变。
- [EditorPlay3修正判定](EditorPlay3/runtime.json)，仍保留其早期视觉缺陷原图。
- [Refine1原型修正](Refine1/refinement.json)；before-world.unity.txt、before-road.asset.txt保留修改前内容。
- [EditorPlay4入口FAIL](EditorPlay4/runtime.json)、EditorPlay5入口缺回执及受控关闭记录；不由exit0补成PASS。
- [最终EditorPlay6](EditorPlay6/runtime.json)、[入口Profile记录](EditorPlay6/play-entry.json)、[实际进程](EditorPlay6/process.json)。

## 构建与最终Player

- [Build1结果](Build1/build.json)、[完整6警告](Build1/build-messages.txt)。
- [Build2结果](Build2/build.json)，对应旧PlayerWrite2/Read2，不混作最终原型。
- [Build3结果](Build3/build.json)、[实际Bee服务](Build3/bee-services.json)、[184项二进制/数据SHA](Build3/binary-manifest.json)、[构建后输入库存](Build3/post-build-inputs.json)。原驱动另在Build3/ExecutedTools于启动前保存；库存不是完整构建前冻结声明。
- [最终写入](PlayerWrite3/runtime.json)、[真实进程](PlayerWrite3/process.json)、[实际桌面/PID](PlayerWrite3/Player.desktop-process.json)、[合成检查点](PlayerWrite3/checkpoint-written.json)。
- [新进程读取](PlayerRead3/runtime.json)、[真实进程](PlayerRead3/process.json)、[实际桌面/PID](PlayerRead3/Player.desktop-process.json)、[读取的同一检查点](PlayerRead3/checkpoint-read.json)。
- 旧PlayerWrite1/Read1的异步截图FAIL以及Write2/Read2早期视觉图都保留，不由最终PNG覆盖。

## 性能、轨迹和图片

- [性能与内存汇总](performance-summary.json)；每次运行的main-thread.csv、draw-calls.csv、gpu-raw.csv、gc-calibration.json和memory.jsonl原样保留。长CSV压缩为.csv.gz。
- 最终两个Player目录包含enemy-road-across-seam、enemy-lake-bypass、enemy-room-port三组实际移动轨迹。
- [最终PNG独立解码/像素检查](image-checks.json)，不是人工美术或原生操作验收。
- [当前185/0/10/4具名矩阵](acceptance.json)，历史FAIL不混入当前统计，也没有删除。

![四块地形、道路与植被](PlayerRead3/four-tiles.png)

![湖泊与山脊](PlayerRead3/lake-ridge-road.png)

![封闭遗迹](PlayerRead3/closed-ruin.png)

自有Scene/Prefab/TerrainData/材质/配置位于../LabInputs，脚本在../Tests，复跑见[TESTING.md](../TESTING.md)。当前图片是非开发Player实帧技术原型，不是产品新地图或最终美术成品。
