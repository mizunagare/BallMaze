# 失败与尝试记录

1. Build1：旧Invoke-Check自动复制夹具但缺UI01Before，编译失败后停Safe Mode。保留Unity.log、普通关闭NOT_RUN回执；未强杀，占用未回收。此轮不是产品编译通过。
2. Build2：在补齐依赖的新副本batch构建成功。所有96警告与JobTempAlloc退出诊断保留，不吞日志。
3. 首次Preflight Python因默认GBK解码UTF8 Bee失败（UnicodeDecodeError），未启动Player；改为显式UTF8后重跑。工具失败不计产品通过。
4. RealNegatives第一轮4项、第二轮增加NativeReenabled后5项保留，各轮独立目录；预期构建失败是负例成功，不能当正向构建失败率消失。
5. 发布模型测试使用独立复制字节和回执，不修改原构建证据。所有外部路径与人工项未关闭。
