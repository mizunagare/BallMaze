# 证据索引

原始运行根I:/WGCombat/MAPTOOLS-1104-A。发布日志为脱敏副本；压缩保留全部日志行，原始文件未改写。没有插件包或受限供应商源码进入仓库。

- [获取尝试清单与双SHA256](acquisition-manifest.json)：Acquire1～4，sourceSHA256与publishedSHA256分列。
- [首次实际获取结果](Acquire2/acquisition.json)、[原始日志发布副本](Acquire2/Unity.log.gz)、[进程状态](Acquire2/process.json)。
- [用户登录后重试](Acquire3/acquisition.json)、[日志](Acquire3/Unity.log.gz)、[进程状态](Acquire3/process.json)。
- [等待账户valid后的有界请求](Acquire4/acquisition.json)、[状态变迁](Acquire4/states.jsonl.gz)、[日志](Acquire4/Unity.log.gz)、[实际退出](Acquire4/Editor.exit.json)、[进程状态](Acquire4/process.json)。
- [官方来源与观测元数据](official-sources.json)：网页声明，不是本机兼容测试。
- [初始保护清单](protected-before.json)、[早期复核](protected-after.json)、[获取结束复核](protected-after-acquisition.json)。
- ProjectInputs/：独立工程manifest、lock及Unity版本。不是正式产品构建输入。
- [当前分层记录](acceptance.json)：4 PASS、1 BLOCKED、19 NOT_RUN；不删除失败历史。

没有地形/插件截图或Player性能文件：尚未运行，不生成占位图冒充实机。原C1失败、产品历史证据与用户修改保持原位置。
