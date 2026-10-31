# CP03-R1.3：进程证据来源关联整改

开始基准：`c1d510dd7eb12b5b2168b4eee6e2913644b5c312`。独立分支 `fix/cp03-review-r1.3`，未修改或合并 main。最终完整提交以 GitHub 此文件所属提交及交付回复为准。

仅修改 Receipt.py 与 Editor/Runtime 两个包装器；新增工具测试与证据。本轮未修改产品 Assets、CombatAim、参数、玩法、存档或依赖，未启动新的 Unity/Player。

## 根因与修复

旧版本只核对 Runner 与 NativeProbe 的退出码、角色、范围及时间，未要求命令、快照来源和实际子进程可执行文件形成关联。修复前10个错误关联夹具均错误得到 PASS/0；1个正向控制 PASS/0。首次失败原样保留。

新分类器强制读取同目录匹配前缀的 command、process-origin、desktop-process 文件；核对 hostPid、完整 exe、精确参数数组、双 SHA256、source/snapshot 路径和实际 desktop exe。保留旧的冻结合同、Runner/NativeProbe退出码及时间校验。缺失或不符一律 INCOMPLETE/3，不以手工 PASS/0 补足。每个报告记录五份进程来源文件路径与读取字节 SHA256。

包装器明确传入三份新增来源文件。真实运行器的 process-results.json 是追加 semantic 行前的不可变快照；origin中的两个捕获时哈希必须与该快照相同。当前 results.json 可合法追加 semantic 行，不拿其事后哈希替代快照哈希。

## 实际结果

|验证|结果|性质|
|---|---|---|
|旧50项|50 PASS|合成工具及源码审计自测试|
|R1.1 33项|33 PASS|合成合同自测试|
|R1.2 60项|60 PASS|合成进程证据自测试|
|R1.3来源关联|35 PASS / 0 FAIL|API与真实CLI退出码、JSON/CSV/Markdown检查|
|一致性|44 PASS / 0 FAIL|独立只读交叉校验|
|原始Editor证据复核|进程PASS/0；291 PASS、2 UNRESOLVED；整体BLOCKED/2|读取R1.2真实运行原件，无新Editor运行|
|原始非开发Player证据复核|进程PASS/0；291 PASS、2 UNRESOLVED；整体BLOCKED/2|读取R1.2真实运行原件，无新Player运行|
|保护文件|3476项 + 额外3191项，无变化|包含用户修改、旧证据和R1.2交付|
|产品输入|1147项及3个构建二进制，无变化|原R1.2测试副本与既有非开发构建|

两项法杖 `w2-s0-near`、`w2-s1-near` 继续 UNRESOLVED，历史 CAMERA_SURFACE_BEHIND_MUZZLE 未修复。历史引擎、关闭异常开放项不关闭。原生输入、人工观感、可读性、音质及最终打击感 NOT_RUN；本轮性能测量 NOT_RUN。推送不代表独立审核通过。

参见 [验收](ACCEPTANCE.md)、[复跑](TESTING.md)、[证据](Evidence/INDEX.md)、[来源合同](ASSOCIATION.md)、[失败历史](FAILURE_HISTORY.md)。交付后暂停等待固定SHA复审。
