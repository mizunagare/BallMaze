# MapMagic版本来源核验

| 层次 | 实际值 | 证据 |
|---|---|---|
| 官方Asset Store | FREE，2.1.20，2026-07-28，原Unity2022.3.62 | [官方页面](https://assetstore.unity.com/packages/tools/terrain/mapmagic-2-165180)，2026-11-05读取 |
| 本机官方下载元数据 | product165180、version2.1.20、version_id1425896、upload961788 | 上批冻结的 [下载元数据](../DeliveryMapTools02/Evidence/Version1/native-package-metadata.txt) |
| 原始unitypackage | 214148132字节，SHA256 `6ebe30529ea5a98bac346b7423461e18c66e3c73eb54b31df67fd55646f6b8a5` | [本轮重算](Evidence/package.json)，不重新打包或上传 |
| 包内源码常量 | 2.1.19 | 199项源码与原包逐项相同，[保护清单](Evidence/protection.json) |
| 包内旧meta | MapMagic2 Bundle、product178682、2.1.17，共1079条（含1条CR差异） | [上批原包元数据审计](../DeliveryMapTools02/Evidence/package-audit.json) |
| 官方公开维护库 | Core/MapMagicObject.cs在公开commit83e3cad935a3d5036adaf0ae32b28bbfbb188641为3.0.0 | [本轮API摘取](Evidence/VersionResearch/public-core-version.json) |

导入目录 `I:/WGCombat/MAPTOOLS02-A/Project/Assets/MapMagic`，未移动到正式工程；许可证按官方页 Standard Unity Asset Store EULA / Extension Asset，不因FREE而假定允许再分发原包或受限源码。免费核心Map生成与自有Shape/Prefab/场景脚本明确分开，没有购买Objects、Splines或其他扩展。

## 官方维护记录检索

只读查询 [供应商GitLab](https://gitlab.com/denispahunov/mapmagic)：项目3313900，master。本轮取得Core文件最近30条历史和UnityTemplate文件6条历史；只是有限分页，不冒充全部历史。tags API返回空数组；releases API返回403，不能写成“没有发行说明”。公开仓库说明为beta/patch，公开3.0.0代码不等同商店2.1.20稳定包，不将其导入或替换现有供应商版本。

[官方Wiki](https://gitlab.com/denispahunov/mapmagic/-/wikis/home)及商店Support指向网站也已读取。商店链接的 [站点](https://www.denispahunov.com/) 此次渲染为About Us占位内容，未提供三个标签的正式解释。检索摘要及API原结果在 [VersionResearch](Evidence/VersionResearch/official-observations.json)。没有发送支持消息或购买资源。

结论：三个稳定包标签确实同时存在于官方取得的同一个包，不是本轮擅改、导入另一版本或获得付费Bundle许可的证明。可验证其来源，但无法用现有官方维护材料确认为何内部常量/meta未同步。供应商版本一致性继续UNRESOLVED；下一步需要2.1.20正式变更说明或供应商明确确认。没有自行修正常量或meta以消除差异。
