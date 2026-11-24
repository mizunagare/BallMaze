# UX-06 复现与证据层级

固定起点为 `1c3fb90bf5902c147fda35252dc59e3b3a5f8872`，开发分支为 `feature/ux-progression-06-region-records`。不要求合并 main。所有运行均使用 `EVIDENCE/STORAGE/` 下的显式隔离根，不读取真实用户存档。

## 构建

Unity 6000.6.5f1，Windows64 Mono；Packages 与锁文件保持原件。依次执行 `prepare_build.py <新记录>`、`build_isolated.py <新记录> acceptance|release`、`verify_build.py <新记录>`。Python 使用 UTF-8 模式。必须先确认没有该批 Player/Unity 正在运行，不能同时构建、修改输入或抢占游戏焦点。

`prepare_build.py` 冻结 1516 个输入的逐路径大小/SHA，并复制到仓库外可写项目；源码、配置压缩快照与完整输入清单均随构建记录保留。构建启动器直接等待原始进程，记录真实 OS 退出码。`SETTINGS/` 保存导入、批准有效状态、打包和结束状态以及实际 Bee 输入；两个 URP 资源必须与批准原件反序列化后的完整有效对象相等，五项服务开关必须为 false。保护开发树不是靠构建后恢复来认可产物。

## 自动化夹具 [T]

`RegionRecordsTests.Run` 在最终构建流程实际执行，共 14 个独立断言。构造数据明确标为夹具：空历史/旧历史未知、五项遗迹与洞窟分组、领取状态、背包无关性、只读投影、真实首领统计来源、名称快照、确定性排序、128 覆盖说明、Pending 不作为输入、文案与 DATA_GAP。重复构建执行不增加独立用例数。

## 真实 Player [P]

设置 `UX06_EXE` 为最终 Acceptance 产物后执行 `run_player.py <地区> <全新RunId> <隔离根名>`。每局启动新 PID，同地区使用同一隔离根连续冷启动。正常标题入口、出征、结算确认调用产品动作；运动与交互使用 InputSystem 输入，不直接写位置、HP、完成标记、目标历史或回执。原始 `product-interaction`、`movement-input`、Pending/Committed 全量快照及两次存档指纹用于独立复算。每局必须取得真实退出码 0；Driver 汇总 PASS 不能覆盖进程失败。

最终九局为 F10/F11/F12、R07/R08/R09、C07/C08/C09（统一日期后缀 20261124）。旧的三地区各三局阶段运行保留；不把混合构建结果替代最终同一源码/Driver 构建验证。

## 原生 UI [P]

通过 computer-use 的 Windows SendInput 点击实际 Player 窗口，使用观测截图坐标。记录实际 HWND/PID、前台、窗口/客户端、ClientToScreen 和 DPI 元数据。1280×720、DPI96 为本次验证环境。`native-inputs.jsonl` 对应逐次产品状态 `native-steps/` 与原始截图。工具命令仅切换 renderer、请求截图、结束观察，不生成或改写业务数据。

UI 观察在初始正常自动保存后开始；验收构建临时延长自动保存间隔，避免定时写盘混入只读比较，结束前恢复原间隔。独立比较观察窗口内 Profile、revision、Unity RNG、攻防和主档 SHA。正常退出保存发生于观察窗口之外，不伪称进程整个生命周期从未写盘。

容量/未知 UI 使用已完成 UX-05 隔离样本的逐字节副本，来源与源文件保护见两个 `REUSED_*_FIXTURE_RECEIPT.json`；这些是复用 UI 数据，不计入本批真实目标生成九局，也不重开 UX-05 验收。新空根由产品正常创建。

## 独立复算 [C] 与失败保留

运行 `recompute_runs.py`、`protect_end.py`、`finalize_delivery.py`，读取原始事件和产物，不更改原判定。每次失败保留原目录；重试使用新 Run ID。F07 虽原探针写 PASS，但 OS 异常退出，验收为 NOT_ACCEPTED；没有回写原结果。UI-A02 原只读检查 PASS 但浏览不完整，单独限定其结论。

最终报告明确区分源码 [S]、构建 [B]、夹具 [T]、Player [P]、独立复算 [C]。可读性/手感/长期留存和其他分辨率/DPI 属未验证 [H]。

## 纯 Release 外部验证

本轮未执行prepare_build/build_isolated，也未启动Unity。release_prepare.py核对固定输入并冻结原30行、旧证据哈希；登记样本只复制本批隔离根。release_run.py直接启动BUILD12_RELEASE，仅观察进程退出和新隔离根文件，不加载DLL、不修改运行中状态。native_release_input.js通过computer-use 26.1117.41037的@oai/sky发送实际输入，逐次观察后才操作；源码、调用记录和原始PNG按Run保存，截图用于交付证据。

两个进程分别使用原登记PID及正常Alt+F4退出，未调用kill。release_finalize.py核对进程、原始存档校验、资源实体逐值映射、历史/永久字段、源样本SHA/mtime、原证据、HEAD/index/refs和构建字节；recompute_runs.py对Release不伪造Pending/Committed或内部探针事件。输入可见结果由截图复核单独登记，不能把工具调用成功等同于产品消费。

工具诊断保留说明：JavaScript环境不允许eval，改为直接定义同一归档函数；跨启动全Profile等值假设被真实camp重建差异否定，未声明全Profile一致，改为显式保留差异及非camp逐字段核对；CSV字段对账先统一为CSV字符串表示后逐值比较。以上是工具/断言范围修正，不改任何产品断言、原始Run或失败判定。
