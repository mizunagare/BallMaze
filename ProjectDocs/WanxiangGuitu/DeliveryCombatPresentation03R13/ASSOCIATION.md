# 同次运行来源关联合同

`Receipt.py.evaluate` 新增可缺省为None的路径参数：command_receipt、process_origin、desktop_receipt。None表示缺证据，不表示成功。CLI对应 --command-receipt、--process-origin、--desktop-receipt。

必需文件必须解析到 presentation.json同一规范化根目录；Runner仅接受process-results.json。角色决定CP03Editor.Run或CP03Runtime前缀。

1. 原Runner/NativeProbe检查继续强制：角色、scope、单一阶段、状态类型、整数退出码、布尔超时、未强制终止、时间顺序和退出码一致。
2. command.hostPid为正整数，且等于NativeProbe.hostPid。desktop.pid为应用子进程，不能与宿主PID混同。
3. command.exe、Runner.command[0]、desktop.exe为绝对完整路径，规范化后相同。arguments必须逐项等于Runner.command[1:]，不重新分词或按basename匹配。
4. origin.source必须是本目录results.json且存在；origin.snapshot必须是本目录process-results.json。捕获时的sourceSHA256AtSnapshot及snapshotSHA256必须都是合法64位hex，并等于读取到的process-results.json字节SHA256。
5. command、desktop、exit的时间必须位于阶段区间内且顺序正确，origin捕获不得早于结束。
6. 每份来源只读取一次字节后进行JSON解析与哈希；报表记录路径和哈希。缺失、异目录、PID、参数、路径或SHA不符均INCOMPLETE/3。

分类分层：证据不完整INCOMPLETE/3；明确产品/断言失败FAIL/1；有效强制开放项BLOCKED/2；只有全部强制条件通过PASS/0。进程PASS/0可以与整体BLOCKED/2并存。

边界：这是一套本地证据关联校验，不是对恶意同时伪造全部文件的数字签名或远程证明。NativeProbe与包装器源码、目录保护和冻结合同仍是信任基础。本轮没有改变原始来源或其信任级别。
