# R1.3验收

|项目|状态|证据|
|---|---|---|
|强制command/origin/desktop来源|PASS|Receipt.py；Association-First/selftest.json|
|同名同退出码但hostPid不同|PASS|native-hostpid、foreign-native-content；均INCOMPLETE/3|
|外轮退出、command/origin/desktop路径|PASS|foreign-*；均INCOMPLETE/3|
|替换command、参数不符|PASS|command-exe、command-args、runner-args|
|origin双SHA及快照修改|PASS|origin-source-sha、origin-snapshot-sha、snapshot-modified|
|实际desktop exe不符|PASS|desktop-exe|
|必需来源文件缺失|PASS|missing-command/origin/desktop及omit-*|
|完整Editor/Runtime控制|PASS|positive-* PASS/0；open-* BLOCKED/2|
|旧50/33/60项保留|PASS|三组Legacy*/selftest.json|
|原始Editor/Player只读复核|PASS|Reaudit；对关联校验通过，不代表整体通过|
|真实Editor/Player整体验收|UNRESOLVED|各291PASS/2UR；整体BLOCKED/2|
|3476+3191保护文件、1147输入及3二进制|PASS|protected-after、input-binding|
|锁定源码与24组弹体证据|PASS|locked-contract.json，复用只读旧实际样本|
|包装器语法与来源传参|PASS|powershell-parse、consistency|
|新Editor/Player运行|NOT_RUN|本轮按任务只读复核原始真实证据|
|原生UI、人工试玩、性能|NOT_RUN|不在本轮证据链整改范围|

全部工具自测试178 PASS；一致性44 PASS。修复前10个守卫FAIL独立保留。法杖两项仍UNRESOLVED，整体验收继续BLOCKED；等待独立复审。
