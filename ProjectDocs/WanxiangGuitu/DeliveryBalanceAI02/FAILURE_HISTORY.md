# 首次失败与尝试历史

所有旧交付原件不变，本批根I:/WGCombat/BAL02-1030-A。

- BeforeRules：13PASS/29FAIL。27个新护甲预期与旧固定减法不同，2个非有限raw旧防护不足；作为真实旧负例保留，不将全部29条称为独立产品缺陷。修复后AfterRules2为42PASS。
- AfterRules：新增矩阵类先被非矩阵规则阶段复制，但当时未注入BAL01Trace，导致编译exit1。最小工具修复：非矩阵阶段不复制/保留该依赖类，移出到拥有根并保存；未修改产品来迎合编译。原log保留。
- Normal-Gather：沿用旧Normal包装时，与Prepare已有WGNormalAICheck/WGA1NormalResume/B06OriginalPlay重复，编译失败。旧包装close带空桌面参数，返回句柄无效，保存审计不存在，脚本也报错；不是业务死亡/胜利。仅对精确PID35180、精确合成项目路径核对后CloseMainWindow请求正常关闭，ended=true，无kill/激活/全局按键；该退出不当产品退出验收。失败包装原文仅归档Tools/Failed-Legacy-NormalRunner.ps1.txt，勿执行。
- Normal-Gather2：复用Step时以batch启动，真实CombatSaveSystem.Start明确在batch跳过默认初始化，老Normal驱动等待IsInitialized至自己的320秒deadline，exit1。日志同时有历史Editor.Search内部IndexOutOfRange完整栈，不把它猜成初始化首因、不改产品Search或生命周期。
- Normal-Gather3：改为复用同Step在不激活的私有测试桌面以非batch启动，原正式隔离初始化生效；驱动去重并适配实际相机，正常AI三进程通过。没有重复相同失败条件来挑选胜利。
- 原始矩阵Mixed rep2的policy字符串仍为CorrectDodge，但冻结源码有意早闪且scope已声明；汇总另列effectivePolicy=WrongDodge，保留原始标签/源/时序，不覆写老JSON。不能把它计为正确闪避成功。

受控老/新死亡8/13、删失86/81、零伤样本108/107与各22个90秒完整窗口均保留。不是清除失败/删失后只报122清场。该变化属于结果，不把所有死亡当测试工具错误，也不把编排器exit0当全部验收通过。

AIM01以前的所有FAIL与UNKNOWN、青色帧、Search/C15/JobTempAlloc和原生/人工NOT_RUN保持。正常AI、规则与Player的正常Application.Quit不等于原生标题栏关闭或引擎根因已解决。
