# 工具获取与验证失败历史

原始文件位于I:/WGCombat/MAPTOOLS-1104-A。已发布副本见Evidence/INDEX.md，原始日志保持不变。

|尝试|实际结果|后续|
|---|---|---|
|Acquire1|编排保护拒绝Editor的showInactive选项；未启动Unity|修正隔离启动参数；不标记插件失败|
|Acquire2|独立Unity/URP初始化完成，官方获取返回User is not logged in or user status invalid；Unity exit3|请求用户登录并领取FREE|
|Acquire3|用户确认登录领取后重试，仍报登录无效；exit3|发现请求早于Editor完成账户初始化，增加有界等待|
|Acquire4|非batch启动且账户valid后请求；DownloadRequested持续至180秒上限；exit3，无安装包|保留阻断，不将账户valid或请求已发送当成下载成功|

Acquire2～4工具早期使用内部SDK单项Download入口。核对官方参考源码后发现该入口在服务条款检查下游，已将保存的工具修正为只允许公共Download(IEnumerable<long>)入口，保留Unity自身条款/授权检查。没有写入条款接受标志，没有创建资源权益、购买、提取凭据或使用第三方下载。修订版尚未执行，不继承任何旧结果。

DownloadRequested停滞根因尚未确认：没有证据可将它确定归因于账号、网络或资源本身。用户已领取不等于独立进程已下载。下一步需要官方Package Manager完成下载所得.unitypackage，或者在独立工程中由用户完成下载。未经安装不进行地形、导航或Player通过声明。

日志中的本机账号/许可证客户端标识和令牌片段应在发布副本中脱敏；原始输入不改写。发布清单记录原始与发布SHA256以及脱敏规则。

## 用户完成下载后的继续记录

以上是先前阻断时的原结论。用户随后自行完成官方下载，在Unity缓存找到214148132字节包，复制到独立Inputs并核对SHA256；没有把Acquire4改为成功。

|尝试|结果|处理与证据|
|---|---|---|
|Import1|资源导入/编译发生，但完成事件跨domain reload丢失，编排600秒超时，exitCode=null|保留进程68528，不强杀；正常关闭请求找不到受控窗口；不是导入完整成功回执|
|Importer修订|曾用Assembly-CSharp查找实际位于MapMagic程序集的类型|修订查找和重载检查；原占用项目无法自动刷新收尾，不再重入，改用独立ValidationProject|
|ValidationProject初始化|复制实验Library时Unity日志处理残留ILPP runner|不是无缓存导入/性能样本；后续不复制活跃Library。本轮没有调用kill/强杀命令|
|Generate1|exit1，驱动误调用private StopGenerate，CS1061|改用公开TerrainTile.Stop，不修改插件|
|Generate2|断言10PASS、exit0，但日志有MarkReady重复键后台异常|整体FAIL/不接受；Pin已经启动，移除驱动重复StartGenerate；补全Error/Exception/Assert门槛|
|Generate3|11PASS，exit0，无未捕获生成异常|新目录保存原始结果；没有覆盖Generate2|
|EditorPlay1|14PASS、3NOT_RUN，exit0|四区Agent与实际地形生成通过；GC/GPU未取得有效校准|
|Build1|Succeeded，0错误5条UAC0005警告|完整警告/日志归档；结束JobTempAlloc未定位|
|Player1|exit1；4次截图失败及默认Terrain Shader=null异常|真实运行时生成/导航虽通过，整体不接受；只为新对象显式配置已保存URP材质，测试窗改为独立桌面显示|
|Build1源码重建工具|第一次LF哈希不匹配，AssertionError|没有写入不匹配副本；按CRLF还原后与冻结input-manifest哈希完全匹配，标记为重建副本|
|Build2|增量Succeeded，0错误0条新增BuildReport警告|不是旧5警告已修复；结束JobTempAlloc仍UNRESOLVED|
|Player2|18PASS、3NOT_RUN，exit0，4张实际截图|无运行时Error/Exception/Assert；不等于人工观感/性能预算通过|
|Generate4启动保护|ENV_RESOURCE_BLOCKED，约2.06GB提交余量低于3GB；未启动Unity|扩展种子/分辨率/产品尺寸代理候选保留为NOT_RUN；没有放宽门槛，实测版源码严格恢复到Build2输入哈希|

所有对应原始日志发布副本见Evidence/Validation。Import1占用进程保留是明确环境收尾限制；没有关闭用户Editor、修改系统快捷键或操作真实玩家存档。
