# RUNLOOP-01 失败与未执行历史

- 历史COMBAT02四exit1、R1失败、COMBAT03的5FAIL/4NOT_RUN/5UNRESOLVED全部保留；1409文件SHA不变，不覆盖aggregate或输入。
- Before：真实发布后回调异常，磁盘Committed/rev4与内存Pending/rev3不一致，actualexit1。After是独立合成Run的同一故障，actualexit0，不改旧结果。
- Cycle：新夹具把Read方法当作委托使用，C#9报CS8773，actualexit1。修正调用括号，不升级语言/依赖；原执行源及完整编译日志保留。
- Stages/Running：关闭面板同帧受ClosedFrame屏蔽，DisplayedH为空，夹具NullReference，actualexit1。只让测试等待下一帧并显式检查提示存在；不修改产品输入规则。
- Stages/Committed-2：无ActiveRun时JSON把null表示为空字符串，夹具比较不规范，actualexit1。只规范化测试序列化表示；Committed按settlement.runId携带已终结身份，不能错误要求它仍有ActiveRun。
- 后续各尝试用不同输出目录；Shared内被后续更新的阶段JSON已先复制至失败目录。Verified另用新合成根，冻结每阶段主备档，未继承旧PASS。
- Missing/Corrupt为预期存储故障，日志保留异常。测试先移动精确已发布文件，缺失或写入明确坏档，再恢复原字节，调用正常完整读取；不修改奖励、回执或库存字段伪造成功。
- Editor.Search/JobTempAlloc与94构建警告不删除、不归因为已定位的本轮产品缺陷。历史引擎根因仍开放；非开发构建不是正常标题栏退出验收。
- 没有运行原生/人工、隔离验收Player本轮业务链和性能基准；没有穷举每个terminal/ack回调中断位置。只给源码审计或NOT_RUN，不继承历史PASS。
- 发布校验首次用Python默认GBK读取UTF-8 SUMMARY，UnicodeDecodeError，Python退出1；外层后续Git命令0不能抵销该失败。保存Publication/encoding-failure.txt，显式UTF-8重新验证，未修改运行原件。
- 发布索引门禁发现合成.tmp/.bak被全局ignore排除，git show退出128、校验失败并阻止提交。没有删证据或关闭门禁，只对本批清单下合成证据做限定force-add，保留失败记录，再验证全部哈希；未修改全局ignore或force push。
