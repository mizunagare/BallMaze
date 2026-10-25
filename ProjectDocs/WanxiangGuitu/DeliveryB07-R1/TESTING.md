# B07-R1 复跑与证据分类

Unity 6000.6.5f1（3ff58d469c8a）；URP17.6.0、Input System1.20.0、uGUI2.6.0。未升级版本、依赖或CI。

## 完整 All

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 `
 -SourceProject D:/unity/WanxiangGuitu `
 -TestRoot D:/WanxiangValidationRuns/B07R1ReleaseAll `
 -Phase All -FullRegression -B4 -B07 `
 -ShaderCacheSource D:/WanxiangValidationRuns/B07R1FinalAll/20261025-135732-ace2c02a/Project
```

最后一项可省略以重新编译着色器。实际运行创建唯一子目录 `20261025-145529-a973b767`。冻结产品/规则/正常AI输入 `dc55ece3c3d880090f562e120ebbc472a9f3eae4`。只复用匹配版本的ShaderCache，不复用AssetDatabase、已编译程序集或存档；这是新隔离副本重新导入/编译，不宣称着色器从零编译。

所有存档为工程外合成数据；先验证启动参数再进入Play。私有桌面只承载测试进程，不激活到用户输入桌面。超时保留进程与诊断，不强杀，不关闭用户程序。目录或资源占用按既有编排跳过不安全步骤。原生键鼠环境缺失保持NOT_RUN。

用户未提交的ForestRuins场景和ProjectSettings不会进入Git；测试副本包含其开工时内容，源码/副本/构建输入哈希明确区分。不要指向真实存档运行故障测试。

## 定向规则与渲染

复用 `DeliveryB4/Invoke-Directed.ps1`，Methods 为 `B07ReadabilityProbe.Run,B07ReadabilityRules.Run,B07ReadabilityVisual.Run`；WorkerFrom使用已审查、已结束完整运行的工作目录。该入口复用现有Step、超时、退出码和私有桌面worker。`Diagnose`仅作本轮受控诊断，不在完整All中反复运行。

- Probe：旧独立OnGUI停用，共享显示几何与拥有生命周期的预警。
- Rules：6534个位置样本对比原命中谓词，六攻击伤害/前摇/恢复/范围/半径冻结值，36个布局矩形，重复查询及全局随机不变。
- Visual：1280×720、1920×1080的100/150%；2560×1440、3440×1440的150%；每种6攻击，共36张，另2张坡地，共38张。150%场景构造双Boss同屏并验证预警优先和无重叠。125%及高分辨率100%有规则布局检查，不冒充该组合的新Boss运行截图。
- 该视觉夹具明确停用NPC与主角输入，使用实际OrbitCamera、地形和renderer；危险形状采用原定义，弹道起点/方向与五条真实投射物一致。不是正常AI胜利或原生UI。
- 等待稳定渲染帧并记录ShaderUtil状态后，重新Begin原时长前摇再截图；不会修改产品伤害/前摇、游戏时间或随机流。截图有固定纯青色占比阈值40%的退化检查；它仅捕捉本次明确缺陷，不是通用美术验收。
- 暂停后倒计时冻结、恢复原时间倍率、受击隐藏、组件停用隐藏、场景重建零预警残留均在真实运行中断言。原B07Combat补充死亡后无可见预警断言，仍检查实际伤害/翻滚/四武器。

`b07r1-render-ready.csv`字段为case、before/ready、frame、anythingCompiling、allowAsyncCompilation；`b07r1-pixels.csv`为图片名和纯青色比例，无表头。几何、布局CSV有各自表头。

## 正常 AI、最终 Player 与未完成项目

沿用B07的Gather/Treasure/Bypass/Land/Lake，每策略三个进程。Boss流程实际采集制造、战斗、拾取、撤离、结算、入仓取材制造、再次森林出征和新进程继续；合成初始物资及领域机器人行为沿用B07 TESTING，不加生命、不冻结敌人、不直接设置胜利。陆地固定重放1132820888，湖中745672572。

非开发Player另测启动、后台WM_CLOSE、真实退出码、退出审计与新进程恢复，不把它当真实标题栏关闭或原生Boss战。原生U16和人工理解NOT_RUN；D3D12 UNKNOWN仍UNRESOLVED。首次Editor青色帧在稳定帧前曾出现，内部根因仍UNRESOLVED，不把等待就绪称作引擎修复。

失败历史、增量诊断及各轮原始日志单独保留；最终All不继承历史PASS。每项状态按实际PASS/FAIL/NOT_RUN/UNRESOLVED记录。

## 遮挡淡化补充

B07OcclusionProbe.Run和B07ActorOcclusion.Run也在最终完整All中重新执行。Actor夹具在相同相机/角色位置比较淡化关闭/开启，保持前摇定义相同；检查所有启用的身体/枝冠Renderer、原材质恢复、自有材质清理，以及控制器/HP/随机/Profile/时间倍率。它只验证渲染，不是原生操作或正常战斗。最终All的正常AI仍独立执行两条Boss完整循环。

CameraActorFade只替换挡在相机与主角之间的渲染材质，保留贴图和颜色；预警与生命UI不参与淡化。透明着色的光照是首版近似，不宣称美术/平衡完成。镜头离开立即恢复原材质；不改变Collider、导航、伤害或持久化数据。原始All1被正常截图复核发现仍遮挡，因此保留在Attempts/All1。

## 结束后的证据封存

只有results.json含成功的report.finalized后才能发布最终证据。复用DeliveryB07的Seal-Evidence.py、Summarize-Evidence.py和Verify-Evidence.py，以及DeliveryB4/Provenance.py；R1的Publish-Evidence.py只增加本轮白名单文件，Finalize-Report.py只从该轮结果派生表格。输出使用新的Evidence子目录，不覆盖失败记录。

Audit-Release.py是只读后处理：传入--project、--run、--target和--baseline，检查正式程序集包含显示组件而不含Editor测试入口，记录用户文件哈希、完整日志的Exception行与构建warning行索引。它不读取存档，不运行游戏，不把元数据检查称作原生战斗验收。build-warning-lines的标记行数与BuildReport警告总数含义不同，二者分别保留。

发布完成后再次检查允许的文件类型、日志压缩包CRC、截图/日志/冻结源哈希、Markdown链接和Git暂存字节；PNG/ZIP沿用仓库既有LFS规则。仅上传诊断与合成断言，不上传测试存档或构建二进制。
