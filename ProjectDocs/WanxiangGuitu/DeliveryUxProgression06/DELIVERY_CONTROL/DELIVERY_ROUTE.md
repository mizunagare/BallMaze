# UX-06 正式交付路由

整体CONDITIONAL_PASS，未暂存。此目录为拟入库的便携控制材料；读取本目录元数据及收到的ZIP即可核验，不依赖原机器PRESUBMIT_REVIEW目录。

|包|原始文件数|零字节|ZIP字节|SHA256|
|---|---:|---:|---:|---|
|UX06_RAW_EVIDENCE_1463.zip|1463|17|41370912|75d8306d0990ee688173fb968e565364bf7f170220a8ec8b730171f05c30b24b|
|UX06_PRECORRECTION_CONTROL_54.zip|54|9|343817|2b7df2827d0033788719caece44f79bcbd98c7832788def7a173aae6f13bf507|

原1463项与新增54份控制封存副本分别计数。前者完整保留失败、日志、外置分页和既有源码归档；后者封存本次修正前的REVIEW/480白名单/SHA表/提案、四份派生材料、旧总索引和旧属性原件。原件未删除。

**当前仅本地封装与两次新目录解包核验通过，未向外部接收者传输，未取得外部签收。** [实际本地位置与包身份](PACKAGE_RECEIPTS.json)准确登记；首次长路径失败目录仍保留。Git不收录两个ZIP、解包目录或重复原始载荷，仅保留本目录控制材料和经过筛选的正式证据。

## 接收者验证

取得这两个同名ZIP后，在含本目录的仓库中执行：

```
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression06/DELIVERY_CONTROL/verify_packages.py --package-dir <收到ZIP的目录> --extract-root <全新隔离解包目录>
```

校验器核对包整体SHA、精确路径集合、大小、每文件SHA及零字节。它只使用本目录[原证据manifest](EXTERNAL_MANIFEST.tsv)、[控制封存manifest](CONTROL_ARCHIVE_MANIFEST.tsv)与包身份，不读取原存档或旧LFS缓存。两个包保留仓库相对路径；**尤其控制包含旧版本同名文件，只能在隔离目录展开，不能覆盖当前仓库。** [独立校验回执](PACKAGE_VERIFICATION.json)

## 引用与风险

[运行源码关联](RUN_SOURCE_LINKAGE.tsv)逐Run使用已记录SHA；32条运行Driver/外部原生输入来源匹配，九条早期外部启动器精确源码未在现有归档找到，不伪造、不套用UX05 F-02。[纠正后的画面引用](REFERENCE_RESOLUTION.tsv)区分JPEG与仅退出JSON，六次未确认输入不改判。[七处精确格式授权](FORMAT_EXCEPTION_APPROVAL.tsv)只适用登记原SHA和行号。

F07、Release IMGUI无正式入口、启动器缺口、人工体验及其他显示环境限制均未被本次授权接受或关闭。风险以[现行登记](../RISK_REGISTER.md)为准。Release浏览结论仅限已核对业务字段，不是零写盘、主档SHA不变或跨启动RNG一致。

旧1927项索引版本封存在控制包中，当前索引明确记录四项派生修正及新增本目录材料。不要运行旧聚合脚本覆盖已冻结交付材料；后续修改需要新授权。本轮不运行clean、不生成实际索引pointer，实际blob/LFS/索引验收均NOT_RUN。
