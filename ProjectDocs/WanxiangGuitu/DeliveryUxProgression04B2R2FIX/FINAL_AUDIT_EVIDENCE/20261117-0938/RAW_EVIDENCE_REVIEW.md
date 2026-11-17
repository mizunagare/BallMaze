# UX04B2R2FIX 最终原始证据独立复核

审计者：final-audit-evidence。结论：**归档实物与身份交叉一致；保留全部4项历史FAIL，不等于新增Player验收。**

本层不引用REPORT的PASS作为证据，不继承旧Oracle次数。只读原件；仅新增本审计目录文件。未Build、未运行Player、未用Python模拟实际Mono运算。

## 本轮独立复算

| 项目 | 本轮结果 |
|---|---|
| INDEX全部实际文件SHA256及bytes | 901/901一致，0缺失/差异；结束前再读901原件重哈希，0变化 |
| CSV逐行→真实manifest→真实result | 25组；身份字段及内嵌result全匹配 |
| 原始结论分布 | 19 UI PASS + 4 UI FAIL + 2 Float BITWISE_EQUAL |
| 九域canonical FNV-1a64 | 21个有state文件的UI运行，124 changes、248前后快照、2232域重算，0不符 |
| Save base64→原始bytes/SHA256 | 394记录，0不符 |
| A07自然LastSavedAt门控 | 六run共12 gates，12通过；LastSavedAt前进且达到原due，focusEpoch不变，interval保持5 |
| 两Float原始Mono证据 | 各7cases、24prefix，共48prefix，old/new bits无差、0ULP；与原state-changes逐字段匹配 |

详细原始输出：[independent_index_sha256_20261117_0948.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_index_sha256_20261117_0948.json>)、[independent_25run_crosscheck_20261117.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_25run_crosscheck_20261117.json>)、[independent_runtime_float_identity_20261117.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_runtime_float_identity_20261117.json>)、[independent_canonical_save_crosscheck_20261117.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_canonical_save_crosscheck_20261117.json>)、[independent_natural_gate_20261117.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/independent_natural_gate_20261117.json>)。机器汇总：[RAW_EVIDENCE_REVIEW.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/RAW_EVIDENCE_REVIEW.json>)。

## UI-A07归档/编译/运行身份

accessory/arms/main/board-insufficient/legal-swap/illegal-swap的PID依次为 **19728 / 5132 / 11412 / 31532 / 12660 / 5880**。六run实际归档DLL、source、receipt、result、manifest、process-start一致：

- Product：`ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1`
- Driver：`0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45`
- compiled source / receipt.executedSource / Tools source：`a04a242ee57991227105d098ac53811b8fe8dd1fbdb07991e50f0a22185dfb97`

receipt编译退出码均0，result为真实Mono、非Editor。静态读取[实际编译driver](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/ReplacementDriver.compiled.cs>)中的运行时实物哈希校验（335–338行）；[Raycast检查](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/ReplacementDriver.compiled.cs#L142-L145>)之后是[InputSystem排队mouse-down/up](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/ReplacementDriver.compiled.cs#L174-L175>)，未发现直接onClick.Invoke。

[自然保存门控](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/ReplacementDriver.compiled.cs#L100-L112>)只读取nextSave/interval，等待LastSavedAt自然前进，并核focusEpoch；本段没有关闭计时器、手动保存或写回时钟。

## 原样保留四FAIL与具体限定

1. A01 accessory，PID29960：原错误是Worn-and-container-nonzero-authority；错误文本中Worn/body贡献0与容器贡献6并存，不能把容器总变化6当成Worn身体贡献。原FAIL不改判。
2. A02 board-insufficient，PID7572；A03同模式，PID2532：原错误均为clickable top raycast旧件按钮失败，未进入Evaluate，原本无state-changes文件。两项不删、不当作真实容量失败验收。
3. A05 illegal-swap，PID3364：拒绝Commit九域与live Random前后相同，而Save字节不同，原FAIL保留。解码save.json为revision1→2，savedAtUtc为08:37:19.0774920Z→08:37:24.0203832Z，约4.943秒；符合跨自然5秒周期刷新旧盘快照的解释。**不能说只有时间戳变化**：payload实际239条路径变化，包括fixture gear、level/skills和camp实体；前一磁盘保存尚不是当前fixture状态。

## 两Float实物比较

PID33160/31732均记录Mono 6.13.0，非Editor。7cases覆盖原顺序、逆序、六active、多容器加法顺序、重复及非零rig/bag。每run原始24prefix的old/new bits及ULP与原state-changes一致，fixture及Random前后相同。实际result指向的System.Core文件与各自runtime归档均实际哈希为：

`15081eac9f71fd7817a7d42a963651c89c666a4c21499f2076fb3ab7aacd9b9a`

原Float source实际调用Enumerable.Sum(Single)与产品B2AttackModel.ComputeAttack，每个prefix都实际取两条路径。这里核验原件与实际归档，**没有重新执行Mono计算**。

## 边界

- 此层是独立实物/身份/原始hash与bytes复核；原始canonical与gear的语义对应、完整projection/几何、源代码/PDB保护等属于主审计的互补层，不用本层FNV一致替代。
- fresh Oracle重算单列，不把历史次数当作本层结论。
- 一致哈希与身份不能排除人为整体伪造归档；无新Player动态复验。
- read工具单行会截断到2000字符；先read检查文件，机器复核再解析完整原始bytes，避免把截断当成JSON证据。
