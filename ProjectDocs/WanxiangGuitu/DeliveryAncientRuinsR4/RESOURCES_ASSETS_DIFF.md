# resources.assets 解析差异

两份文件均为 Unity 6000.6.5f1 的格式 23，长度 13,947,344 字节。各有 6,930 个对象，PathID 集合、对象索引顺序及类型计数完全一致。两个对象在按 PathID 直接比较时内容不同，其余 6,928 个 payload 字节一致。对象表保存内部名称、类型、索引、偏移、大小及 SHA256。

| Resources 键 | 内部名称 | A PathID | B PathID | 文本内容 |
| --- | --- | ---: | ---: | --- |
| performancetestruninfo | PerformanceTestRunInfo | 249 | 248 | 2,896 字节 JSON，按名称配对的 SHA256 一致 |
| performancetestrunsettings | PerformanceTestRunSettings | 248 | 249 | 23 字节 JSON，按名称配对的 SHA256 一致 |

只读内存重建改动两条对象表项，交换两段实际相等的 payload，并按 B 的对齐边界填零。结果精确等于 B，无未归属字节。另对 globalgamemanagers 仅交换两个 PPtr，结果也精确等于 B。327 条索引记录、316 个唯一键的顺序与逻辑目标一致。两个 TextAsset 无 PPtr 依赖。扫描了根目录其他构建序列化对象中指向这两个 ID 的候选引用，仅命中 ResourceManager 的两条已解析记录。resources.assets.resS 和其他外部目标在两套发行包中相同。项目资产 GUID 从对应 .meta 记录为候选，发行文件 FileID/PathID 单列。

Unity Performance Testing 的 TestRunBuilder.OnPreprocessBuild 生成两份 JSON，构建后清理文件和 .meta。原始日志给出临时资产在 A/B 不同的导入 GUID，且本次导入顺序相反。Unity 内部排序规则仍未验证。纯包中无 R4 探针。

探针副本的正式产品程序集和全部序列化文件逐字节保留，仅增加侧车 DLL 与两份引导注册。通过实际非开发 Player 的 Resources.LoadAll 查询 316 个键。两次各返回 326 条非空记录和一条空记录，有序结果一致。两项换位 TextAsset 分别按运行时实际内容核对 SHA256。唯一空项 ancientruins/bakedenvironment 在原索引指向 FileID=0、PathID=0，源是场景资产。场景进入和玩法未重跑。

[对象 A](Evidence/Audit/inventory-A.json) · [对象 B](Evidence/Audit/inventory-B.json) · [资源引用](Evidence/Audit/resources-comparison.json) · [精确重建与运行核对](Evidence/Audit/exact-reconstruction.json) · [UnityPy 对象读取接口](https://github.com/K0lb3/UnityPy/blob/master/UnityPy/files/ObjectReader.py)
