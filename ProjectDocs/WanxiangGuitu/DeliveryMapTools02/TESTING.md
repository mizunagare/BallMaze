# 独立复跑

## 输入

Unity6000.6.5f1、URP17.6.0；固定main未动，研究基准8111f1b3c868b67d03605b66ef24cf7eb5313cf4。官方本地包214148132字节，SHA256为6ebe30529ea5a98bac346b7423461e18c66e3c73eb54b31df67fd55646f6b8a5，Native PackageInfo确认id165180、version2.1.20、version_id1425896、upload_id961788。源码常量与旧meta不同标签不改写，见来源审计。

实际运行根I:/WGCombat/MAPTOOLS02-A，独立Project，**没有复制Library/Temp/Logs**。Package仅从本机合法用户下载导入；不重新分发供应商包、源码、DLL或Demo素材。

## 新工程重建

1. 先检查可提交内存，低于3GB不启动Unity。检查目标工程占用；不强杀、不修改系统设置。使用新的实验根/输出，保留旧证据。此处工具路径固定；更换机器需明确改为新的独立路径。
2. 新建独立项目，复用LabInputs的manifest/lock和ProjectVersion，导入合法免费核心。把Tests三份.cs.txt分别复制到Assets/MT02WorldState.cs、Assets/MT02Runtime.cs和Assets/Editor/MT02Editor.cs，按LabInputs对应meta保留脚本GUID。
3. 复跑已固化布局时复制LabInputs/Assets/MT02GeneratedV2即可。若要重生18组，保持目标生成目录不存在，运行MT02Editor.Generate，再使用Tools/Prepare-Profile.py从自有模板生成新Scene GUID对应的Windows64 Profile。不要对已经存在的生成资产重复执行Generate或Refine。
4. Profile固定Boot、World两个Scene，Development=false、Diagnostics Disabled。Editor测试也必须使用同一明确Profile；不能先设置共享场景列表再切默认Profile，否则可能清空入口列表。

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryMapTools02/Tools/Invoke-Lab.ps1 -Method MT02Editor.Generate -Output I:/WGCombat/MAPTOOLS02-A/NewGenerate -Seconds 900
./ProjectDocs/WanxiangGuitu/DeliveryMapTools02/Tools/Invoke-Lab.ps1 -Method MT02Editor.Play -Output I:/WGCombat/MAPTOOLS02-A/NewEditorPlay -Seconds 400 -NonBatch
./ProjectDocs/WanxiangGuitu/DeliveryMapTools02/Tools/Invoke-Lab.ps1 -Method MT02Editor.Build -Output I:/WGCombat/MAPTOOLS02-A/NewBuild -Seconds 900
./ProjectDocs/WanxiangGuitu/DeliveryMapTools02/Tools/Invoke-Player.ps1 -Exe I:/WGCombat/MAPTOOLS02-A/NewBuild/Player/MapTools02.exe -Output I:/WGCombat/MAPTOOLS02-A/NewWrite -Mode write
./ProjectDocs/WanxiangGuitu/DeliveryMapTools02/Tools/Invoke-Player.ps1 -Exe I:/WGCombat/MAPTOOLS02-A/NewBuild/Player/MapTools02.exe -Output I:/WGCombat/MAPTOOLS02-A/NewRead -Mode read
```

先运行生成、准备Profile，再Play/Build。以上命令分批、顺序执行。工具复用现有本机隔离启动函数及NativeProbe；没有等价的私有测试桌面/资源保护时应BLOCKED，不能改成抢占用户桌面。

## 判定与证据

- 每次保留ExecutedTools、命令、PID/hostPid、独立桌面、实际退出回执及完整日志。退出0不能替代runtime/editor.json；缺回执或日志Error必须单列失败/不完整。
- 原型敌人真实NavMesh路径、Warp、逐帧移动CSV、湖水对照、碰撞、卸载/重载分别判定。它们不代表产品战斗AI或原生UI通过。
- 截图是异步写入，最多等待5秒，之后还要检查PNG尺寸/解码/非黑；不是看到请求已发出就PASS。
- 当前合成检查点只记录实验地图身份、种子、哈希和导航位置。写入、读取必须两个独立进程，保留两份检查点副本与进程证据；不得改作产品v9存档。
- 验证Bee时必须选择DestinationPath精确对应本轮Build的PlayerBuildConfig，核对Development和五项Services，不误用旧缓存。
- 已保存逐线程GC正/零校准；正分配仍返回0时NOT_RUN。GPU原始0/无样本不作性能成功。180帧Profiler计数只代表记录的相机/负载，没有预算结论。
- 原始文件保持在独立根；Tools/Publish.py只发布自有资源/工具与脱敏副本，清单列原始和发布SHA。最终输入清单为构建后库存；驱动另有启动快照，不把Unity写回后的文件冒充完整的构建前冻结输入。

RefinePrototype只是本轮从旧MT02-world-v1修正原型视觉的受控迁移；当前从零生成直接得到v2，不再需要Refine。旧失败、旧Scene/路面副本和旧Player日志都保留。
