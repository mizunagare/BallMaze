# 失败历史

- 修复前证据：[Before/regressions.json](Evidence/Before/regressions.json)。10个错误关联样本被旧R1.2分类器判为PASS/0，守卫期待INCOMPLETE/3，因此记录10FAIL；完整正向控制1PASS。旧Receipt与两包装器的原始字节在Evidence/*.before.txt保留。
- 修复后：50、33、60项以及新增35项均首次运行通过，没有删除负例或降低断言。旧测试只适配新增必需来源文件；合成快照的origin重建仅用于保持原60项各自测试变量，R1.3快照篡改负例不会重建origin。
- 原真实运行的两项法杖UNRESOLVED完整保留，旧R1/R1.1/R1.2所有失败、旧semantic分类和原始进程结果未修改。
- 本轮未运行产品、原生输入或人工试玩；不能据工具负例通过宣布产品或体验全绿。
