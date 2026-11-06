# C1 内部开发检查点

开发检查点固定为 712fffb7eb9196dfbb7d880e4c31a4c21e0dd28e。这是带开放项的内部基线。R7 原结论为 **7 PASS / 1 FAIL / 2 NOT_RUN / 2 UNRESOLVED**，正式发行验收仍未关闭。

| 冻结身份 | Git 树 |
| --- | --- |
| Assets | eddea63bac0adc755e119762db08b0b00ae3c197 |
| Packages | ca46f9594c2ecab1788502c0b88092762f4c805d |
| ProjectSettings | 70ef819d3b93250c44a0b58f3b4cf2ed2d740a6c |

两套原始 A/B 包在 I:/WGCombat/C1R3-1105-A 的 ProjectA-Build/Release 和 ProjectB-Build/Release。版本身份须使用完整逐文件清单和产品程序集，两个通用 EXE 恰好同哈希。原包 A 的 Assembly-CSharp.dll SHA256 为 5b20e95b23850b2a0c47a29e51cbcaa68b0e9a9024df82ea34c4e57c5dc29a03，B 为 64e375bff21397110264ce050bbd25a2f72d608b7b6ee418cbbe240384be7436。每套 193 文件。[完整发行清单](https://github.com/mizunagare/BallMaze/blob/8a4ce422f97174160662e8f9acb7982e9d68502b/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR4/Evidence/Audit/release-manifest.json) · [两包复核](https://github.com/mizunagare/BallMaze/blob/f21f807fb39f38653d7d3a5d9a3e3371936fedbe/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR5/Evidence/Audit/release-protection.json)

继续保留严格像素 FAIL、三个运行阶段指纹尚无包内精确来源、GraphicsSettings 写回的独立因果影响及完整渲染语义等同性未解决。其他后处理、图形 API、原生人工及玩法重跑等沿用各历史记录的原状态。有新证据、实际回归或相关依赖变化时，再单独调查对应问题。[R7 验收](https://github.com/mizunagare/BallMaze/blob/712fffb7eb9196dfbb7d880e4c31a4c21e0dd28e/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR7/ACCEPTANCE.md) · [R7 原始证据](https://github.com/mizunagare/BallMaze/blob/712fffb7eb9196dfbb7d880e4c31a4c21e0dd28e/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR7/Evidence/INDEX.md)
