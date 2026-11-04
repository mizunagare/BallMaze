# 本轮失败与重试历史

旧批8111f1b3c868b67d03605b66ef24cf7eb5313cf4及DeliveryMapTools01证据不覆盖。本轮原始根I:/WGCombat/MAPTOOLS02-A，发布副本见Evidence。

|尝试|实际结果|判断/处理|
|---|---|---|
|Generate1|58PASS、2FAIL、exit1；18条资产销毁错误|工具把已保存Graph当临时对象；邻接自动序列化假设失败。保留Graph，显式加载绑定，不修改供应商|
|Generate2|60PASS、exit0|18组四块布局、两阶段接缝、随机隔离、Scene重开通过|
|EditorPlay1|目标Scene未在有效列表；无运行时完成回执|入口FAIL/证据不完整；普通close选择器不匹配Editor，使用已有editor-close严格核对owner/PID/桌面后正常退出0。不能将清理退出0当测试通过|
|EditorPlay2|32PASS、1FAIL、2NOT_RUN、exit1|二维无限高矩形误拒绝干燥高岸；保留原轨迹，补三维碰撞/可视水面及正负对照，地图和目标不移动|
|EditorPlay3|36PASS、2NOT_RUN、exit0|导航、碰撞、加载/卸载、运行时再生成通过；仍未完成视觉检查|
|Build1|0错误6警告|5条供应商UAC0005、1条自有拱形Mesh预烘焙碰撞兼容警告；结束JobTempAlloc开放|
|Build1原生包头探测|空输出|只查字段未取jsonInfo，不作为包版本证据；Version1修订为本地包头白名单提取|
|Version1|真实本地SDK元数据|id165180/version2.1.20等确认；没有写入或接受条款|
|PlayerWrite1/Read1|34/38PASS，各2FAIL、2NOT_RUN，均exit1|异步PNG尚未写出就做5帧检查；最后文件存在不改写原FAIL。改为有界等待并独立解码校验|
|Build2|0错误1增量警告|旧5警告未消失，仅未重新编译发出；JobTempAlloc仍开放|
|PlayerWrite2/Read2|36/40PASS，各2NOT_RUN，exit0|截图和跨进程检查通过；原型胶囊粉色、地板穿插与道路背面在图中进一步发现|
|Refine1|exit0，地形哈希不变|只改自有原型：地板+0.3m、道路绕序、重烘焙导航；旧Scene/路面副本保留，身份升v2；胶囊共享URP材质|
|EditorPlay4|1FAIL、exit1|切换默认Build Profile清空共享Scene表；错误收尾生效，不再静默等待|
|EditorPlay5|入口回调未进入Play；缺少运行时回执|INCOMPLETE；已有受控editor-close正常结束，未强杀；入口改为SessionState+update恢复，固定显式Profile|
|EditorPlay6|36PASS、2NOT_RUN、exit0|修正后的v2、固定Profile入口和完整运行链重新验证|
|Build3|最终非开发构建|实际结果和所有警告见Evidence/Build3；不覆盖Build1/2|

最终Player配对单列在验收表中，不用后续PASS覆盖上述失败。GC正分配三次均返回0，校准失败；GPU未校准，均NOT_RUN。没有把0计数、进程消失或编排退出码当作玩法/人工成功。

原型画面修正没有修改正式地图、碰撞、AI、存档或用户文件；供应商源码保持原包哈希。已有产品UI/引擎/人工开放项仍保持原状态。
