# R2-05 Unity Mono真实浮点结果

## 实测身份

Run UX04B2R2-FLOAT-001，PID17352，WindowsPlayer x64，Unity6000.6.5f1；Mono.GetDisplayName返回6.13.0 (Visual Studio built mono)，Environment.Version=4.0.30319.42000。isMono=true，isEditor=false，身份/输入/前缀迹校验均true。

- 产品DLL SHA256：6f876c6090ce57e498359bf93fb812583f848d3064612c10940f24f83c389db7。
- EXE SHA256：b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436。
- Driver SHA256：20eb10c090a56ac7490507b01f321ca67d04f06c6e909a954b21fc7a0963ec83。
- Driver源SHA256：6c67bb3b25fef7846d42b1a0abd326cdf75ea8ea6b9c223b5740573a6d105c06。
- System.Core SHA256：15081eac9f71fd7817a7d42a963651c89c666a4c21499f2076fb3ab7aacd9b9a；System.Core Version4.0.0.0，ImageRuntimeVersion v4.0.30319。
- 产品MVID：5dc8cfaf-4659-4de1-bc0d-7bd119bee306。

[实际加载路径及结果](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json>)；[Driver编译/复制回执](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/_build/build-receipt.json>)。编译仅sidecar，产品DLL未重编；原产品、Driver和System.Core实物分别归档，不混为一类DLL。

## 完全相同的三输入及顺序

| 顺序 | 夹具与有效状态 | 输入Single bits | 同运行时Single转Double的R文本 |
|---|---|---|---|
| 1 | 白主剑，InBag且Main，Attack8 | 0x41000000 | 8 |
| 2 | 绿护臂，board，(0,0)，Attack指定值 | 0x40D4CCCD | 6.6500000953674316 |
| 3 | 白护臂，board，(1,0)，Attack指定值 | 0x40333333 | 2.7999999523162842 |

这是用户给定Single值的同一bit模式；显示文本长短不是改变输入或扩大容差。GearItem.dataRevision=1，Attack读取savedAttack。三件ID互异，非worn/overflow，原序不排序，rig/bag加成为零。不调用掉落/制造/装备生成随机函数。

## 实际调用，而非Python模型

旧路径在该Player里重建原Unique/Active选择，直接执行active.Sum(i=>i.Attack)+0f+0f。新路径直接调用已加载的权威B2AttackModel.ComputeAttack(items, mainId, null, null)，不在Driver里另写当前产品公式替代它。

每个前缀长度1/2/3也分别调用真实Sum与真实B2方法；伴随double/float累加迹各自与真实前缀返回值逐位相等。double迹是同Mono过程中的观察迹，不是改写System.Core内部；前缀调用是独立交叉核对。

| 步骤 | 输入bits | 旧double累加后R文本 | 旧真实Sum前缀Single bits | 新真实B2前缀Single bits |
|---:|---|---|---|---|
| 1 | 41000000 | 8 | 41000000 | 41000000 |
| 2 | 40D4CCCD | 14.650000095367432 | 416A6666 | 416A6666 |
| 3 | 40333333 | 17.450000047683716 | 418B999A | 418B9999 |

最终旧Single=17.450000762939453，bits1099667866；新Single=17.44999885559082，bits1099667865；整型bit距离=1 ULP。**这次是Unity Mono实测，不再只是旧Python边界假设。**

[3条原始逐步记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/state-changes.jsonl>)含每一步double原位、Single原位及实际前缀结果；[输入记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/input-events.jsonl>)明确为验证夹具初始化，不冒充正常用户UI操作。

## 量测范围

上述位差位于装备攻击贡献ComputeAttack返回值。本Run未实例化玩家背包或写入/测量live Hero.AttackPower，也未测HUD/伤害结算显示；不能把17.45误写成角色最终AP。六场景替换的前后完整AP仍属于未执行验收。

## 退出与停止

result.verdict=BIT_DIFFERENCE_STOP，requestedExitCode=21；进程实际exitCode=21、未超时。启动器exit0只表示“诊断及归档完成”，不代表位一致通过。产品未修复，没有第二次探针Run、没有扩大容差、没有继续R01。

本例证明指定三件装备下位一致性不成立，不外推所有输入/Defense/BasisPower/所有平台均有位差。后续方案见[提案](<FLOAT_FIX_PROPOSAL.md>)。
