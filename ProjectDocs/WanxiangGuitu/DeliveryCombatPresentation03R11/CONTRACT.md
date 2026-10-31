# 冻结合同绑定规范

R1 的合同可省略，给出时只比名称集合；layer/scope 只检查非空，SHA 只记录。[修复前 5 个负例](Evidence/Before/regressions.json)均被旧工具错误放行。它们是合成分类器夹具，不是游戏通过证据。

R1.1 正式 CLI/API 必须提供 `profile + contract`。缺失生成 INCOMPLETE/3 及 JSON/CSV/Markdown，没有无合同通过模式。参数解析保留缺省值只是为了输出结构化拒绝报告，任何缺省调用都不能 PASS。两个正式包装器明确传对应角色和合同。

可信锚在 [Receipt.py](../DeliveryCombatPresentation03/Receipt.py) 的 `FROZEN_CONTRACTS` 中，由审核代码固定；运行时不从待检合同、PROVENANCE.json 或调用方临时 SHA 取得期望值。更换合同须修改并复审代码锚，不能重算待检文件 hash 自我放行。

| Profile | 原字节 SHA256 |
|---|---|
| Editor | `6fb6024da5052be6604c23cb7be5e219860815278ebfae0bd0e86fc74e15a6f8` |
| Runtime | `3f438369c590dfecfe27523dff3064ba9a2eba08caa89569425e5efd4418fb7a` |

源提交固定 42cfd3d8，完整 layer/scope/path 见 [来源](Contracts/PROVENANCE.json)。Editor layer 是 `controlled-editor`；Runtime 是原非开发验收 Player 的完整说明，不能前缀或模糊匹配。两者 scope 目前文字相同，仍各自精确绑定，不混同角色。

先验原字节 SHA（不归一化 BOM/换行），再验证合同自身 metadata、回执 metadata、完整唯一的冻结名称集合。报告同时记录 expected/actual SHA、角色、路径、合同/回执 metadata、来源提交及数量。SHA 来自被解析的同次读取，避免解析和报告使用不同版本。

`contractVerified=true` 只说明合同本身可信；只有 `binding.status=PASS` 表示回执也匹配。错误绑定时原 counts 只作未获资格的原始信息，assertionStatus=INVALID、整体 INCOMPLETE/3。已知 FAIL 仍优先 FAIL/1；有效 UNRESOLVED 保持 BLOCKED/2；全强制项通过才 PASS/0。

完全相同字节的合同可以换位置，身份不靠文件名。跨角色、标签、单字节、BOM/换行、配套改名/减项及重算 hash 均不能绕过代码锚。Contracts/Evidence 禁止 Git 文本转换，gzip 保留已有 LFS。
