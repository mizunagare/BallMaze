# UX-TECH-01 失败与尝试记录

## 产品负例：Before

Before/uxtech.json：18断言中9PASS/9FAIL。四类根因：死亡时Management优先；解锁鼠标缺EventSystem仍放行世界技能；焦点/设备变化绕过设置捕获屏障；偏好发布钩子期间外部更改被覆盖。原执行源码、日志、退出码及输出保留。After相同18断言全部PASS，不删除Before。

## 隔离构建与运行工具

1. AcceptanceBuild：exit1、CS0117。共享夹具调用Editor限定SetNextSeedForValidation，Player编译失败。改为UNITY_EDITOR条件，Player使用真实产品新出征种子；不修改产品随机流/入口。AcceptanceBuild2真实非开发构建成功，原失败输入清单和日志保留。
2. Runtime：正式Player保持Title。驱动误认为Editor专用直达标志会在Player生效；240秒驱动期限触发Application.Quit(1)。exit1/forcedTermination=false；没有业务断言回执，不能算输入PASS/正常退出验收。修订驱动显式经GameEntry AskNew/ConfirmNew进入产品；不是原生点击，也不修改发行入口。
3. Inspect-Build第一次本地脚本文本替换产生ParserError exit1，源存ToolFailures。修正仅工具文本，后续PE检查独立输出，不改构建内容。
4. Normal1：旧BAL02NormalObserve依赖未导入BAL01Trace导致CS0103，方法没有开始，无冒险证据。停在隔离Editor Safe Mode提示。退出0也被旧脚本编译错误扫描标FAIL；不把该进程行PASS当作正常AI成功。
5. Normal1工具退出：首次worker传错预期exe，身份保护拒绝；随后精确Editor窗口选择器因只有Safe Mode对话框而NOT_RUN；第一版辅助线程桌面附着失败。最终在独立线程附着同一非激活测试桌面，仅枚举已核对PID/项目的“Enter Safe Mode?”对话框并BM_CLICK Quit。该操作非强杀、未激活桌面、不属于原生UI验收。辅助源码/回执保留。删除本轮包装器中不适用于本轮的可选BAL02观察器复制，保留旧文件在ToolFailures，不改旧批次工具或产品。

## 历史

原ENCOUNTER与既有批次所有失败保持原文件；本批不改历史aggregate、原始输入或日志。UNKNOWN/C15/青色帧/Search/JobTempAlloc仍UNRESOLVED；原生U16、人工试玩、完整性能NOT_RUN。有限技术通过不能关闭上述项。

所有后续尝试均使用独立输出目录；最终实际结果汇总在REPORT/SUMMARY，不用后续PASS擦除本表。

## 本轮追加的引擎日志

Pause有6项时钟/投射物/只读查询断言PASS、进程exit0，但原日志包含UnityEditor.Search.SearchDatabase.EnumerateAll/GetDefaultSearchDatabase/IndexationOnStartup的ArgumentOutOfRangeException。不能宣称干净Editor退出，也不归因于产品输入。该历史引擎根因继续UNRESOLVED。log-analysis.json单独索引全原始异常上下文，不修改各次原results.json。PureBuild原日志JobTempAlloc亦保留。

文档发布检查首次git diff --check把按-text保留的CRLF原始证据判为尾随空白，并报告工具文档EOF空行。原始运行证据不为风格检查改写；仅修整本轮工具/Markdown的EOF。源码风格检查以命令局部cr-at-eol解释CRLF，排除原始Evidence与执行夹具；发布完整性另由SHA256逐项核验，不降低产品断言。
