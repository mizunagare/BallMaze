# INPUT-01 复跑与验证分层

使用固定Unity6000.6.5f1和现有包，不升级。所有启动在进入Play前传入`-wanxiang-storage-root`和一致的`UNITY_TEST_ROOT`；使用新建工程外拥有者根、合成进度和独立构建，不访问LocalLow或真实玩家目录。

## 本批完整受影响入口

从工程根运行已存在的本地编排器，增加的Input01选择仅选择本批相关测试，没有第二套调度框架：

```powershell
$pwshPath=(Get-Process -Id $PID).Path
$env:PYTHONUTF8='1'
& $pwshPath -NoProfile -File ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 `
  -SourceProject D:/unity/WanxiangGuitu `
  -TestRoot D:/WanxiangValidationRuns/Input01-NEW `
  -Input01 -GameplayOnly -UnityTimeoutSeconds 600
```

若使用`-ShaderCacheSource <已结束且同版本的隔离工程>`，只复制ShaderCache并记录来源；不能称全新shader编译。编排仍新建Project、Rules和构建；有冲突/资源不足时记录NOT_RUN，保留占用进程。不要关闭原工程、激活私有桌面或发送物理Esc。

方法顺序：Input01Rules.Run → Input01Play.Run → Input01Play.Resume（依赖前一进程）→ 原B09设置、B08营地时钟、UI01、B1、B2及随机流回归 → fixture → 非开发构建 → 正常AI Gather三进程 → 正式Player标题/启动安全。省略的旧全量种子/战斗用NOT_RUN表示，不继承为新PASS。

## 仅定向复验

复用原DeliveryB4/Invoke-Directed.ps1，它从同一编排器取进程/日志/超时函数：

```powershell
& ProjectDocs/WanxiangGuitu/DeliveryB4/Invoke-Directed.ps1 `
  -SourceProject D:/unity/WanxiangGuitu `
  -TestRoot D:/WanxiangValidationRuns/Input01-Directed-NEW `
  -WorkerFrom <本次已验证、已结束的无人值守根> `
  -Methods @('Input01Rules.Run','Input01Play.Run','Input01Play.Resume','UI01Rules.Run')
```

输入Play/Resume使用可渲染的Editor进程、固定GameView分辨率及虚拟InputSystem设备；不是原生窗口测试。Resume明确带`-wanxiang-validate-title-entry`，从真实标题Canvas经虚拟指针点击设置、返回与继续，然后由原GameEntry/CombatSaveSystem恢复原Run，不能直接初始化旧JSON冒称标题继续。

## 证据层级

- **规则**：Input01Rules使用真实JsonUtility/文件系统和产品校验/首选项保存；无业务进度构造为通过证据。
- **虚拟输入与uGUI**：向InputSystem排入键盘/离散鼠标事件，经过产品PlayerInput、Update/LateUpdate消费者以及InputSystemUIInputModule。设置捕获/冲突/取消/保存失败/重试具有实际UI与事件记录。战斗仅测输入及原冷却门禁，合成夹具的敌人停用单列，不声称正常AI或新平衡样本。
- **正常AI**：沿原Gather策略，敌人AI正常、真实采集和掉落/结算/制造/后继森林/新进程；其领域操作不冒充原生玩家键鼠。
- **正式非开发Player**：原发布构建，从Boot进入Title；记录真实入口、截图、存档指纹、退出码和后台关闭方式。WM_CLOSE不等于用户标题栏点击，也不是U16通过。
- **原生/人工/性能**：独立NOT_RUN。环境只读检查不赋予当前用户控制台独占授权；不能为了通过而激活桌面、改Snipaste或要求用户守候。

## 首选项与旧存档

preferences仍version1，新增可选bindingVersion/inputBindings，路径仍由GamePreferences/GameEntry的隔离定位确定。缺字段默认；坏键位/文件警告、原件保留，加载不自动写。应用tmp→原子发布→更新有效快照，保留.bak；失败可重试/取消。未知JSON元数据按原JsonUtility能力忽略，不宣称支持未实现设置。v9封装、Profile/Run、来源账、随机流、徽章、教程和结算结构未变。

新进程核对同Profile/Run/区域/seed、装备ID、来源账、库存/药水、渡口回执、布局和随机状态。正式包不得含Input01Rules/Input01Play/Input01DeviceFocus等Editor注入测试类型；用最终Assembly-CSharp.dll实际字节及构建日志检查，不只看目录名。

每次新根保留命令、起止、退出码、超时、stdout/stderr、原始Unity日志、源码/输入hash及失败。预期非零探针分列；编排器退出0或单项编译成功不等于整批或人工体验通过。
