# CP03-R1.1 独立整改交付

基准 `42cfd3d8f3abd4861cd672dbb8f440fae48e4b65`；分支 `fix/cp03-review-r1.1`。main 仍为 `72db192a527bd256e2ba18cd7ab334d8334051da`，不合并、不推送 main。最终完整 SHA 由本报告所属提交及回复绑定。[基线](BASELINE.md)。

仅修复文档目录中的 Receipt.py、两个正式包装器及原自测适配，新增冻结合同、专项自测和一致性验证。正式验收必需角色及合同；SHA 与代码可信锚比较，合同和回执 layer/scope 精确绑定，名称集合完整。调用方不能提供新 hash 自我授权，缺合同无降级路径。原 rows/status 不修改。[规范](CONTRACT.md)。

| 集合 | 真实结果 |
|---|---|
| 修复前 | 5 个预期 guard FAIL，旧工具错误放行的 PASS/exit0 保留 |
| 原工具回归 | 50 PASS；全部检查保留，分类夹具改用完整 293 项冻结结构 |
| 新绑定专项 | 33 PASS / 0 FAIL |
| 一致性 | 35 PASS；校验 R1 Git 字节、进程、合同、JSON/CSV/Markdown |
| 真实 Editor | 进程 PASS/exit0；291 PASS、2 UNRESOLVED；binding PASS，整体 BLOCKED/分类与宿主 exit2 |
| 真实非开发验收 Player | 进程 PASS/exit0；291 PASS、2 UNRESOLVED；binding PASS，整体 BLOCKED/分类与宿主 exit2 |
| 新真实回执错误重分类 | 3 项正确拒绝 INCOMPLETE/3；只读，源 SHA 不变，不是另 3 次运行 |

[汇总](Evidence/consistency-final.json)、[Editor](Evidence/Editor/Semantic/acceptance.json)、[Player](Evidence/Runtime/Semantic/acceptance.json)、[真实错误绑定](Evidence/RealCrossContext/results.json)。CLI 负例均核对退出码、JSON/CSV/Markdown、绑定资格及错误原因；API 无合同和单次读取另验。

受控 Editor 使用原战斗矩阵；非开发 Player 从 Boot/Title 受控 Continue 原合成检查点，再调用真实公开战斗 API。原不可变构建重跑，不冒称原生操作、正常 AI、人工试玩或新构建。无超时、无强杀。[输入与二进制哈希](Evidence/input-binding.json)。

[保护复核](Evidence/protected-after.json)2,664 项不变，原始证据和用户修改保留；产品 Assets/CombatAim/依赖/设置/v9 无修改。[失败历史](FAILURE_HISTORY.md)保留旧 5 个 guard FAIL、初轮与最终自测和网络/工具错误。

本轮合同绑定整改已验证；产品整体验收仍 BLOCKED。两项法杖及历史引擎根因保持 UNRESOLVED；原生 U16、独立人工、性能仍 NOT_RUN。完成独立分支推送后暂停等待复审。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [证据](Evidence/INDEX.md)。
