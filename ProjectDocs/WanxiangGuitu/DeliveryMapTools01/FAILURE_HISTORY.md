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
