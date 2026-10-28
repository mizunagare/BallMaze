# 复跑与未来人工执行

## 准备检查（不启动游戏）

Python标准库即可，`-B`防止仓库缓存。`ux_pack.py prepare`故意要求源工程HEAD固定在2caa；后续提交不能直接绕过。复建时使用独立检出的2caa产品源与已批准用户覆盖层，逐一核对1152哈希；工具可从本交付读取。不能reset用户工程或忽略哈希差异。

```powershell
python -B ux_pack.py prepare --repo <固定输入工程> --root I:/WUX01/<全新唯一目录> --release <复审纯发行目录> --fixture <复审合成集合WanxiangGuitu目录>
python -B ux_pack.py session --root <包根> --session Planned-Sword --weapon Sword --fixture fresh
# Spear/Staff/Bow各自独立fresh；Continue专项使用--fixture continue。
python -B selftest.py --root <已有四武器和Continue空计划的包根>
python -B inspect_session.py --session <包根>/Sessions/Planned-Continue
python -B ux_pack.py summarize --session <包根>/Sessions/Planned-Sword
```

同名包/会话/自测目录拒绝覆盖；复跑使用新目录。运行前保留本轮原始失败，不清理仍在运行的进程或数据。`inspect_session`仅校验磁盘封装和身份，不能替代产品SaveCatalog验证、输入证明或理解评价。

## 人工开始前

本批**没有执行**下列人工入口。必须先按PROTOCOL确认独立参与者、获准可见交互Windows环境、设备、同意与观察者。不得无人值守替人勾选确认开关。不要关闭用户程序，遇已有Player占用则停止此试次并记录。

```powershell
# 在获准的人工环境中由操作员手动运行，PowerShell 7：
./Run-ManualSession.ps1 -Session <Session绝对路径> -ParticipantCode P01 -ObserverCode O01 -InteractiveConfirmed -IndependentTesterDeclared -PriorExposure none -TimeoutMinutes 90
```

`RecordingConsent`仅记录同意，不自动录制。由获准工具仅捕获游戏窗口，原始证据先审核隐私再提交。启动器不发送任何键/鼠/WM_CLOSE，不抢焦点、不强杀。超时保存进程状态并保留进程；不能继续复用该会话或当作正常退出通过。

每次重启同一Session生成独立Runs目录和真实PID/句柄/退出记录，观察者另记物理操作方式。原生输入必须同时有真实操作来源和对应业务反馈证据；正常退出还需核查退出审计、最后修订与存档一致性。关闭后用只读工具保存身份摘要，再与重启后比较同Profile及适用的Run；任务8再次出征本就应改变Run。

填写tasks/events/inventory/issues、environment、review模板，不把statusClaim当审查结果。summarize从不输出人工PASS；任意非空声明只能进入待独立复审。人工发现可复现产品缺陷后另行确认最小修复，不猜测调战斗数值。
