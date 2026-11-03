# Player实际渲染调查

## 固定输入与启动差异

产品和旧B3验收驱动均来自指定基准；LegacyShownD12与LegacyHiddenD12使用同一个原B3 FinalTestBuild。前者完整矩阵，后者yaw专项只在相机截帧之后分流；相机前缀代码相同。两包都未重新生成历史截图。旧运行器实际launch-spec和desktop-process记录 `showInInactiveDesktop=false / SW_HIDE`，不是可见Player。

|样本|条件|实际图像|首张状态|
|---|---|---|---|
|历史B2 Player2|D3D12隐藏|10/10黑|原件保留|
|历史B3 PlayerFinal|D3D12隐藏|71/71黑|原件保留|
|本轮LegacyHiddenD12|原B3包，隐藏|8/8黑|相同相机前缀|
|本轮LegacyShownD12|原B3包，不激活显示|71/71非黑|实际可见训练场|
|PlayerHiddenD12|同一新诊断包，隐藏|7/7黑|visible=false，cameraRendered=0|
|PlayerShownD12|同一诊断包，不激活显示|7/7非黑|visible=true，cameraRendered=489|
|PlayerShownD11|同一诊断包，force-d3d11，不激活显示|7/7非黑|visible=true，cameraRendered=585|
|PlayerRepeatD12|独立新进程，不激活显示|7/7非黑|visible=true，cameraRendered=475|

[原始状态对照](Evidence/render-comparison.json)、[D3D12正例](Evidence/PlayerShownD12/initial-screen.png)、[隐藏负例](Evidence/PlayerHiddenD12/initial-screen.png)、[D3D11](Evidence/PlayerShownD11/initial-screen.png)、[最终Player](Evidence/PlayerFinal/initial-screen.png)、[Editor](Evidence/EditorFinal/initial-screen.png)。截图没有裁切或改像素。

## 原始空间/渲染状态

Player记录本进程自己的GetActiveWindow、可见/最小化状态、client 1280×720、MonitorFromWindow句柄、运行时targetDisplay=0、activeDisplayCount=1、相机enabled/cullingMask、世界位置/forward、targetTexture=BACKBUFFER、URP资产类型、图形API与实际RTX3060适配器。外部Worker同时记录PID、exe、独立桌面、实际显示策略；`inputDesktopActive=false`。没有激活用户桌面或注入输入。

隐藏时Application.isFocused和READY仍可能为真，但endCameraRendering回调0、backbuffer截图全黑；显示条件同一相机和管线有回调及真实训练内容。现有证据定位的是**本机此隐藏窗口启动条件下未发生相机渲染**，不是PNG编码器把一个已证实正常的Frame涂黑。未逆向声称所有Unity版本隐藏策略都相同，也不将此结论扩展到历史D3D12 UNKNOWN或Editor青色帧根因。

一般computer-use窗口工具在两次初始化及一次reset后仍报`failed to write kernel assets ... os error 3`，没有假装使用它查看了窗口。替代诊断在自己的Player内只读原生状态、从Unity实际Frame抓取，不发送鼠标/键盘。纯包的独立外部窗口截图仍NOT_RUN；原生输入和人工可见性评价仍NOT_RUN。

## 工具整改与门禁

`Invoke-Measure.ps1`默认SW_SHOWNOACTIVATE且仍在不活动桌面；`-HiddenControl`为明确负例。不能只看process exit。RenderReceipt逐一检查7个唯一截图、实际尺寸/非黑/非恒色、实际相机回调和窗口状态，以及实际exit/timedOut/forcedTermination。缺少或坏格式INCOMPLETE/3；有明确不合格FAIL/1；全部必需条件满足PASS/0。PlayerGated实际重跑已通过门禁。

隐藏负例的[视觉回执](Evidence/PlayerHiddenD12/render-receipt.json)保留FAIL，不能把负例重标PASS；测试“正确识别该负例”另算工具自测。7项CLI自测覆盖有效、缺图、坏JSON、隐藏、无渲染回调、黑图及进程失败，实际分类/退出码/输出均归档。没有修改原CP05B运行器或历史JSON。
