# 同场景运行前后对比

收尾新增的[原生帮助/背包/渡口画面](Evidence/CloseInvestigation/NativeEmpty)来自同一产品版本的非开发Player，鼠标操作与用户协助E/H分开记录；它们不属于原92帧受控矩阵，也不是无提示人工理解试玩。关闭异常及原生未完成项见[验收表](ACCEPTANCE.md)。原生路线/缩放/受击中断/结算没有取得的新画面不以旧图冒充。

受控真实运行画面，种子418、渡口旁、相同视角，NPC关闭。Before为3574审阅基线，After为9d4产品代码；不是正常AI或人工试玩。旧版提示只看拾取而执行会选更近渡口，新版明确显示付费目标与材料。

## 1280×720：更近渡口、较远掉落

修改前：

![720 before](Evidence/BeforeEvidence/before-1280x720-mismatch.png)

修改后：

![720 after](Evidence/ScreensFinal/after-1280x720-100-mismatch.png)

## 1920×1080：同一状态

修改前：

![1080 before](Evidence/BeforeEvidence/before-1920x1080-mismatch.png)

修改后：

![1080 after](Evidence/ScreensFinal/after-1920x1080-100-mismatch.png)

## 主次交互、引导和故障

![E拾取H修复](Evidence/ScreensFinal/after-1280x720-100-dual.png)

![真实引导](Evidence/ScreensFinal/after-1280x720-100-channel.png)

![受击中断](Evidence/ScreensFinal/after-1280x720-100-hit.png)

![保存失败](Evidence/ScreensFinal/after-1280x720-100-save-failed.png)

![结果待核对](Evidence/ScreensFinal/after-1280x720-100-uncertain.png)

![150%布局](Evidence/ScreensFinal/after-1280x720-150-ready.png)

完整缺料、可修、已修、结算/满仓及4种分辨率见 [截图目录](Evidence/ScreensFinal)；[正常AI截图](Evidence/NormalLatest) 单独记录。无驱动正式包 [启动窗口](Evidence/ReleaseUI/01-hud.png) 与未完成操作限制见报告。
