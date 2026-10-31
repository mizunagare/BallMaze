# 可复跑调查

代码从main72db192a分出，不拷贝用户未提交场景。工程外全新CP04根；原1163产品输入逐字节校验。既有R1.2 Editor辅助测试目录及Library仅独立复制；helper清单见Evidence/isolated-helper-inputs.json，来源CP03-R1-1031-C/P/Project。不得在正在使用的工程运行。

```powershell
$d='H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04A'
$project='I:/WGCombat/CP04-NEW/P/Project'
& "$d/Invoke-Diagnosis.ps1" -Project $project -Output 'I:/WGCombat/CP04-NEW/Historical' -Suite Historical
& "$d/Invoke-Diagnosis.ps1" -Project $project -Output 'I:/WGCombat/CP04-NEW/Matrix' -Suite Matrix
& "$d/Invoke-Diagnosis.ps1" -Project $project -Output 'I:/WGCombat/CP04-NEW/CameraWall' -Suite CameraWall
```

包装器为本轮复跑入口：复用既有Invoke-Check/NativeProbe，未激活私有desktop、不发虚拟输入，原进程超时1200秒，Editor历史上限480/新矩阵900秒。环境不足或占用则不启动，不强杀。首次实际执行使用同一既有Invoke-Check直接传入CP03Editor.Run、CP04Editor.Run及CP04Editor.CameraWall；完整实际命令见各*.command.json与results.json。包装器已语法检查，不冒称它另外运行过一轮游戏。

Historical注入保留的CP03Cases-Historical/CP03Editor-Historical，来自只读R1.3参考；新CP04Cases/Editor在隔离Editor目录使用，无产品程序集改动。Matrix首次执行源与补充CameraWall源分别随Evidence归档；最终复跑源只增添可选择的补充入口，标准Matrix仍38项。

```powershell
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py "$d/Analyze.py" 'I:/WGCombat/CP04-1031-A' --output 'I:/WGCombat/CP04-1031-A/NewAnalysis'
```

Analyze依赖Historical、Matrix和paired-24数据；输出目录必须全新。正常exit0表示六项证据一致性通过，不表示所有目标命中。Matrix/CameraWall进程exit0分别指驱动完成。原Historical分类器实际exit2、整体BLOCKED，两UR不变。

失败记录：首次只读分析漏指定UTF-8导致GBK解码exit1，保留analysis-attempt1-error.json；paired-24已生成不覆盖。复跑包装器编写出现一次PowerShell变量替换语法错误，保留初稿和wrapper-parse.json FAIL；修订后wrapper-parse-final PASS。首次相机墙候选未实际阻挡，保留并以独立CameraWall输出补证。Unity Search内部异常完整保留，未归为产品、未宣布根因解决。未重做关闭实验。
