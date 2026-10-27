# BUILD-01 验收

仅当前包路径诊断/工具修复范围，未声明产品整体验收通过。输入与完整消息见 [报告](REPORT.md)、[结果](Evidence/RESULTS.json)。

| ID | 状态 | 本轮证据 |
|---|---|---|
| B01-01 固定输入 | PASS | FINAL_AUDIT.json、输入/保护文件清单、逐次 input-hashes、完整复制清单、工具冻结 SHA |
| B01-02 资产身份 | PASS | ReadOnlyAudit 历史副本、各次 asset-before/after、包 source/version/path、meta GUID/hash |
| B01-03 根因判定 | PASS | 新 260 字符复现同两阶段 Error；251 和短根对照；普通/扩展只读读取与 DefaultAsset/ComputeShader 对照 |
| B01-04 修复有效性 | PASS | 修改仅验证工具；两份新短工程独立导入构建，0 目标 Error；超限预检实际拒绝且不创建目录 |
| B01-05 构建质量 | PASS（计数与目标错误范围） | 2/91/4 失败原样保留；短根重复 0/91/4；91 警告未关闭，非零错误复现不算干净构建 |
| B01-06 产物身份 | PASS | 每次 exe/UnityPlayer/Assembly-CSharp SHA、大小；MVID/时间戳/2278 方法签名与 IL 指纹对比；不宣称字节可复现 |
| B01-07 用户文件保护 | PASS | 两保护文件原始哈希与结束相同，未进入提交；Assets/Packages 产品 diff 为空 |
| B01-08 受影响回归 | PASS（限定） | 脚本预检 10 项、导入编译/正式构建/程序集 Editor 测试隔离；其他运行未执行 |
| B01-09 历史保留 | PASS | 首次工具 FAIL、近边界导入异常、目标复现 FAIL、两次短根结果、完整日志/命令/真实退出与哈希 |

上述 PASS 等待审核方复审，不是 Codex 自行授予发行通过。

| 不在本轮执行范围 | 状态 |
|---|---|
| 最终 Player 实际运行、原生菜单/键鼠、原生 U16 | NOT_RUN |
| 正常 AI、跨进程冒险/结算恢复、INPUT-01 全套运行回归 | NOT_RUN（未继承） |
| 独立人工可理解性、性能基准 | NOT_RUN |
| D3D12 UNKNOWN、Editor 青色帧、Editor.Search、JobTempAlloc 根因 | UNRESOLVED（未诊断/未关闭） |
| 历史 91 条构建警告 | 未修复；本批仅分类留证 |
