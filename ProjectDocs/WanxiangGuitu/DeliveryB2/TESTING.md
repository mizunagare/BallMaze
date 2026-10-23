# B2 本地复跑

使用 Unity6000.6.5f1，不升级包、不启用CI。不要手工改真实存档或结束用户进程。所有原始运行目录保留；当前提交仅发布脱敏诊断、截图、哈希与断言。

## 业务及受影响回归

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
  -SourceProject '<工程绝对路径>' -TestRoot '<工程外部测试父目录>' -GameplayOnly
```

可选 `-ShaderCacheSource '<闲置同版本隔离工程>'` 仅复用ShaderCache，不复用程序集、结果、构建、玩家档；不能声称干净shader编译。入口创建新的唯一根，按依赖运行18个选定方法、夹具、正式构建、B2正常AI/Resume及92张受控布局截图。`-FullRegression`可额外选择保留的历史矩阵；本批没有将未选项记PASS。B2正常AI在石1铁矿2的合成准备上真实采木/采石、修复、撤离、制造；木不够修复加制造时再实际采，不改掉落。

GameplayOnly不运行正式Player关闭矩阵或ProcDump，不重复无新证据的D3D12实验。正常AI是Editor驱动，不是原生UI；规则可能冻结NPC、直接触发领域行为，均与正常AI分类。两个故意故障探针原样FAIL，非预期失败使协调器exit1。超时保留进程，不强杀；依赖阻断记NOT_RUN，无关任务继续。

## B2目标视觉

前一步完全结束、隔离工程空闲后：

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryB2/Invoke-Visual.ps1' `
  -PreparedRunRoot '<前一步RESULT_ROOT>' -SourceProject '<工程绝对路径>'
```

复用既有编排辅助函数和private-desktop worker，在已核对owner的隔离副本中安装Editor-only B2Visual；工程占用则拒绝，不关闭或改用户工程。新建独立合成根、启动前传路径。非batch Editor捕获8张实际图像，验证720p/1080p和摘要不裁切，含目标/路线/150%详情。域接口布置状态且NPC禁用；不发送原生输入，不算U16或人工可理解性。详情通过滚轮查看长内容。

输出results、真实command/exit回执、逐帧语义/分辨率记录、PNG和进程列表。最终复跑空进程列表为有效JSON `[]`。batch规则内的截图请求没有生成PNG，不算捕获通过。

## 发布诊断

`Publish-Evidence.py --run <运行根> --target <新的仓库证据目录>`，视觉另加`--visual`。必须使用新目标目录，保留旧轮；复用既有白名单/脱敏器，日志ZIP另列前后哈希。不复制任何save、完整存档分页、DMP、Release、Library或缓存。PNG逐份列尺寸和SHA256。

本轮结果见REPORT、Evidence/SUMMARY。UI-01原生U16、人工理解NOT_RUN，UNKNOWN UNRESOLVED。必须取得独立交互环境或新因果证据才继续这些工作，不能用本脚本/后台WM_CLOSE替代。
