# 复跑说明

仅适用于独立实验，不复制到产品Assets。需要用户自己合法领取/下载的MapMagic免费包；仓库不分发供应商包、源码、DLL或Demo素材。

## 固定输入

- Unity6000.6.5f1(3ff58d469c8a)，URP17.6.0。
- 包214148132字节，SHA256：6ebe30529ea5a98bac346b7423461e18c66e3c73eb54b31df67fd55646f6b8a5。
- 商店版本2.1.20，包内源码常量2.1.19；版本差异不作消除解释。
- 独立根I:/WGCombat/MAPTOOLS-1104-A，实际验证工程ValidationProject；原导入工程Project因工具收尾超时保留，不重用其占用路径。
- LabInputs包含自有生成Scene、TerrainData、NavMesh、模块Prefab、材质、Profile、元数据与依赖清单。Tests为自有驱动源码文本。任何程序集、插件源码只在本地合法包中。

## 重建独立工程

1. 新建独立Unity工程，用LabInputs/Packages清单还原同版本依赖，导入官方免费包。不要打开产品工程执行此步骤。
2. 将Tests/MapLabRuntime.cs.txt复制为Assets/MapLabRuntime.cs，Tests/MapLabEditor.cs.txt复制为Assets/Editor/MapLabEditor.cs。按LabInputs对应meta保留GUID，再复制LabInputs/Assets/LabGeneratedV2（已固化夹具）。场景依赖URP包与自有脚本，不引用产品代码。
3. 若从头生成，使用新工程/新输出运行MapLabEditor.Generate；图由真实MapMagic Noise200→HeightOutput200构建，Pin自动开始生成，不能再重复StartGenerate。既有生成目录/证据不要覆盖；若更换目录，要同时改Root与Profile场景路径。
4. 生成后读取Scene meta GUID，创建独立LabRelease Profile，只包含MapLab.unity，Windows64、Development=false、Diagnostics Disabled。LabInputs已保存此次Profile。设置不能借用/修改用户ProjectSettings。

## 实际执行命令

在研究worktree使用PowerShell7；Invoke-Lab读取现有本机隔离启动入口函数，并使用已有NativeProbe私有桌面。不同机器先配置等价安全启动入口；不能降级为抢占桌面执行。

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryMapTools01/Tools/Invoke-Lab.ps1 -Method MapLabEditor.Generate -Project I:/WGCombat/MAPTOOLS-1104-A/ValidationProject -Output I:/WGCombat/MAPTOOLS-1104-A/NewGenerate -Seconds 300
./ProjectDocs/WanxiangGuitu/DeliveryMapTools01/Tools/Invoke-Lab.ps1 -Method MapLabEditor.Play -Project I:/WGCombat/MAPTOOLS-1104-A/ValidationProject -Output I:/WGCombat/MAPTOOLS-1104-A/NewEditorPlay -Seconds 240 -NonBatch
./ProjectDocs/WanxiangGuitu/DeliveryMapTools01/Tools/Invoke-Lab.ps1 -Method MapLabEditor.Build -Project I:/WGCombat/MAPTOOLS-1104-A/ValidationProject -Output I:/WGCombat/MAPTOOLS-1104-A/NewBuild -Seconds 900
./ProjectDocs/WanxiangGuitu/DeliveryMapTools01/Tools/Invoke-LabPlayer.ps1 -Exe I:/WGCombat/MAPTOOLS-1104-A/NewBuild/Player/MapLab.exe -Output I:/WGCombat/MAPTOOLS-1104-A/NewPlayer
```

始终使用新目录。先核实进程/工程占用和资源余量。超时保留进程、实际PID和日志，不强杀。工具退出码、进程退出码、业务断言、图片检查、性能与人工项目分别判定。

## 判定

必须同时检查process.json、原生日志/退出回执、editor/runtime.json，以及日志中的未捕获Exception/Error；Generate2曾出现断言PASS、exit0但后台异常，因此整体不接受。截图检查文件存在、像素、尺寸及人工看图，仍不能替代原生操作或美术评审。

构建后选择DestinationPath精确等于本轮可执行文件的Bee PlayerBuildConfig，验证Development=false及五个Services=false，不能误用上轮缓存。还须核对程序集/EXE和输入manifest。当前Player包含实验驱动，不能称为《万象归途》纯发行Player。

已发布证据的脱敏和双哈希由Tools/Publish-Lab.py维护。第一次源码重建曾因LF/CRLF哈希不同而失败；最终重建的Build1运行时代码与当时输入manifest逐字节匹配，作为明确标记的重建副本保留，不冒充现场快照。
