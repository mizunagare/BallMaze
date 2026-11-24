import pathlib,json,csv,hashlib
D=pathlib.Path(__file__).resolve().parent;G=D/'RELEASE_RUNTIME'
if (D/'DELIVERY_CONTROL/PACKAGE_RECEIPTS.json').exists():
    raise SystemExit('Delivery metadata is frozen; do not regenerate prior reports without a new explicit document authorization.')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
report=D/'REPORT.md';text=report.read_text(encoding='utf-8')
text=text.replace('本批没有新增纯 Release Player 运行，不将构建排除扫描冒充运行验收。','本轮复用 BUILD12_RELEASE 完成两条纯 Release 实际运行，未重建；构建排除扫描与运行证据分别保留。').replace('全部 30 条 Run 保留原判定','补验前的 30 条 Run 保留原判定')
marker='## 纯 Release 补验与历史退出关联（2026-11-24）'
if marker in text:text=text.split(marker)[0].rstrip()+'\n'
text+='''
## 纯 Release 补验与历史退出关联（2026-11-24）

结论仍为 **CONDITIONAL_PASS**。复用 BUILD12_RELEASE，产品源码、1516项冻结构建输入与产物原始字节未变，本轮未构建、未注入验收工具。新增两条 Run，九局及原57次点击矩阵未重跑。

|Run ID|PID|buildId|实际退出码|实际覆盖|
|---|---|---|---|---|
|UX06-RELEASE-CORE-R01-20261124|912|UX06-7a4fa23741a53c83|0|正式标题继续游戏；128条历史；三地区uGUI档案、森林近期快照、洞窟复访；遗迹/洞窟历史跳转及返回|
|UX06-RELEASE-COLD-R02-20261124|3236|UX06-7a4fa23741a53c83|0|同根冷启动再次读取；128条和森林126/遗迹1/洞窟1一致；三地区uGUI浏览、洞窟跳转及返回|

EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；产品 DLL SHA256 `7a4fa23741a53c8361b546fb9054e504a65b868edd0e453938004fc840d6e18f`。外部原生输入源码及SHA、启动参数、原始PNG/JPEG、按键/点击、进程观察器均逐Run归档。正常退出使用 Windows Alt+F4，原有 quit/before-exit/save 审计与干净关闭日志匹配真实OS退出0，不是强制结束，也不宣称已验证标题菜单退出按钮。

新根来自本批已登记容量隔离样本的132文件逐字节副本，不访问原UX05或真实用户目录；[来源指纹](RELEASE_RUNTIME/SAMPLE_COPY.json)。原样本SHA/大小/mtime及此前1176项原始证据均未变；[结束保护](RELEASE_RUNTIME/PROTECTION_AFTER.json)。

**纯浏览磁盘结论有边界：** 既有自动保存没有关闭。R01 revision 655→667，R02 695→705；主档原始SHA确实变化。逐字段检查表明，各自浏览窗口内仅revision、保存时间、校验和和营地resources数组顺序变化。84个唯一实体的完整值映射一致；保留历史、全部其他Profile字段、材料、配方、回执及累计账本一致。原捕获使用 FindObjectsSortMode.None，比较仅规范化这个已证实的数组顺序，没有改写存档或忽略其他字段。每Run的 PERSISTED_BROWSE_COMPARISON.json 与原始快照可复算。

跨进程历史和全部非camp的Profile字段一致。camp.randomStateJson、camp.events在启动间有差异，不能声称完整检查点或实时RNG跨启动相等。源码依据是既有 ApplyCamp 调用 session.Restart、选择性恢复营地，不走 RestoreWorld；本轮没有改变该路径。[跨启动差异](RELEASE_RUNTIME/COLD_PROFILE_DIFFERENCES.json)。Release实时UI状态、内部revision及RNG未被探针观测，磁盘事实不能替代这些内部断言。

**纯 Release IMGUI = NOT_RUN_NO_PRODUCT_ENTRY。** CombatSession.Awake始终创建PlayerHudPresenter；本批唯一关闭该组件的renderer切换在UX06_ACCEPTANCE探针内，Release不含此入口。没有通过注入或改造产物完成切换，既有Acceptance IMGUI结论保留，但不升级为纯Release IMGUI通过。

两Run共30次外部输入记录，24次取得相应可见结果/正常退出确认，6次未取得预期可见确认（R01返回标题/释放鼠标/Tab/窗口X尝试、R02关闭历史）。这些尝试原样保留，不推定为产品缺陷、不计为输入消费通过；[逐输入可见结果](RELEASE_RUNTIME/INPUT_VISIBLE_REVIEW.tsv)。最终Alt+F4退出0；没有触发新原生异常。

历史F07属于BUILD09，DLL `5bfa8d0e278367d62d763fa9bd8f349cb8e882f3386e6f91764bd816a2150649`，与最终BUILD11/12 DLL及Driver不同。BUILD09与BUILD11的EXE和UnityPlayer.dll相同，不能因产品DLL变化排除引擎层共因；Release的引擎二进制不同，[引擎关联SHA](RELEASE_RUNTIME/ENGINE_CORRELATION.json)。日志在Input System Shutdown之后记录Crash!!!，OS退出3221226525（0xc000041d）。只能确定退出阶段，不能确定原生根因。原始PASS、验收NOT_ACCEPTED不变，不宣称修复。最终BUILD11的C04退出1为未收到前台信号的驱动主动失败，非同类崩溃；其余非零退出与证据见[完整关联表](RELEASE_RUNTIME/EXIT_CORRELATION.csv)。最终BUILD11/12未观察到该原生崩溃，不等于证明不存在。

原30行的身份与判定逐字段不变，追加2条限定uGUI范围的Release PASS后，总32条：原始PASS26/FAIL6，进程验收PASS25/NOT_ACCEPTED7；UI-A02的局部结论仍不扩大。F-02保持OWNER_ACCEPTED_HISTORICAL_LIMITATION。

**提交准备状态：CONDITIONAL_READONLY_READY。** 固定源码/构建身份、运行证据与保护材料已足够开展只读提交候选审查；仍需负责人确认接受纯Release IMGUI不可达、历史原生崩溃根因不明及未覆盖人工/显示环境限制。不是无条件验收收口，不构成暂存/提交授权。本轮不生成提交白名单，不暂存、不提交、不推送、不合并。
'''
report.write_text(text,encoding='utf-8')
risk=D/'RISK_REGISTER.md';text=risk.read_text(encoding='utf-8')
text=text.replace('|UX06-R01|NOT_RUN_RELEASE_PLAYER|纯Release构建与工具排除通过；本批真实Player使用Acceptance Mono产物，不扩大发行运行结论。|',
 '|UX06-R01|CLOSED_FOR_REACHABLE_UGUI_SCOPE|BUILD12_RELEASE两条真实运行退出0，三地区uGUI及冷启动验证完成；不重建、不注入探针，IMGUI另列未执行。|')
marker='## Release 补验后的现行限制'
if marker in text:text=text.split(marker)[0].rstrip()+'\n'
text+='''
## Release 补验后的现行限制

- UX06-P01继续OPEN_HISTORICAL_NATIVE_EXIT：F07为旧BUILD09关闭阶段原生崩溃；最终BUILD11/12身份不同，本轮两个Release退出0，原生根因仍未知，不能声明修复或已被负责人接受。原始PASS/验收NOT_ACCEPTED不变。
- UX06-R02 = NOT_RUN_NO_PRODUCT_ENTRY：纯Release无正式IMGUI renderer选择入口，既有IMGUI只在Acceptance切换；未为补验修改产品。需要负责人接受本批纯Release覆盖限制，不能把uGUI通过扩大到双UI。
- UX06-R03 = VISIBLE_INPUT_LIMITATION：30次原生输入中6次无预期可见确认，原图与输入均保留，不归因产品故障。使用正常Alt+F4取得两次退出0；不声称已验证标题菜单退出路径。
- UX06-R04 = OBSERVABILITY_LIMITATION：本轮只读观察磁盘、可见UI及OS进程，未观测Release实时UI状态、内存revision/RNG。自动保存导致主档字节/revision变化；浏览窗口业务事实未变，仅既有资源捕获数组顺序变化。冷启动camp事件与随机状态会重建，全部非camp永久字段及128条历史一致，不把有限比较描述为全部存档/实时随机流冻结。
- 其他分辨率/DPI、人工手感、长期留存和九局之外的首领/全部收藏正值组合仍按既有未覆盖范围报告。

本批仍CONDITIONAL_PASS；可供只读提交准备审查，尚无暂存/提交授权。F-02继续OWNER_ACCEPTED_HISTORICAL_LIMITATION，与上述UX06限制分别登记。
'''
risk.write_text(text,encoding='utf-8')
a=D/'ACCEPTANCE.md';text=a.read_text(encoding='utf-8').replace('本批未运行Release Player','现已补两条纯Release uGUI/冷启动运行，见本文件追加范围')
marker='## 纯 Release 最小补验'
if marker in text:text=text.split(marker)[0].rstrip()+'\n'
text+='''
## 纯 Release 最小补验

[P] BUILD12_RELEASE原产物，R01 PID912、R02 PID3236，正常系统关闭均OS退出0。正式标题继续入口、三地区uGUI档案核心内容、历史跳转/返回、冷启动128条及地区映射通过。只复用登记隔离样本副本，没有新目标生成，不重跑九局或57次矩阵。

[C] 两个纯浏览窗口均验证磁盘永久业务事实不变；原始字节变化、自动保存revision增长和resources顺序差异如实保留；跨启动只声明非camp字段及历史一致，不声明camp世界/RNG完全一致。内部实时状态NOT_OBSERVED。

纯Release IMGUI为NOT_RUN（产品无renderer开关），不注入探针。30条原始输入中24条有可见结果/退出确认，6条未确认，未计输入消费通过；原生退出异常未复现，F07历史可靠性限制未消除。原30行判定及A02局部范围不变；矩阵追加2行限定范围PASS。
'''
a.write_text(text,encoding='utf-8')
t=D/'TESTING.md';text=t.read_text(encoding='utf-8');marker='## 纯 Release 外部验证'
if marker in text:text=text.split(marker)[0].rstrip()+'\n'
text+='''
## 纯 Release 外部验证

本轮未执行prepare_build/build_isolated，也未启动Unity。release_prepare.py核对固定输入并冻结原30行、旧证据哈希；登记样本只复制本批隔离根。release_run.py直接启动BUILD12_RELEASE，仅观察进程退出和新隔离根文件，不加载DLL、不修改运行中状态。native_release_input.js通过computer-use 26.1117.41037的@oai/sky发送实际输入，逐次观察后才操作；源码、调用记录和原始PNG/JPEG按Run保存，截图用于交付证据。

两个进程分别使用原登记PID及正常Alt+F4退出，未调用kill。release_finalize.py核对进程、原始存档校验、资源实体逐值映射、历史/永久字段、源样本SHA/mtime、原证据、HEAD/index/refs和构建字节；recompute_runs.py对Release不伪造Pending/Committed或内部探针事件。输入可见结果由截图复核单独登记，不能把工具调用成功等同于产品消费。

工具诊断保留说明：JavaScript环境不允许eval，改为直接定义同一归档函数；跨启动全Profile等值假设被真实camp重建差异否定，未声明全Profile一致，改为显式保留差异及非camp逐字段核对；CSV字段对账先统一为CSV字符串表示后逐值比较。以上是工具/断言范围修正，不改任何产品断言、原始Run或失败判定。
'''
t.write_text(text,encoding='utf-8')
out=[]
for run in ['UX06-RELEASE-CORE-R01-20261124','UX06-RELEASE-COLD-R02-20261124']:
    p=D/'EVIDENCE'/run;inputs=[json.loads(x) for x in (p/'native-inputs.jsonl').read_text().splitlines()]
    unconfirmed={15,16,17,18,19} if 'CORE' in run else {9}
    for x in inputs:
        images=sorted(q for q in p.glob(str(x['step']).zfill(3)+'-*') if q.suffix in ['.png','.jpeg','.jpg'])
        exit_only=x['type']=='key' and x.get('key')=='Alt_L+F4'
        if not images and not exit_only:raise FileNotFoundError('Missing actual visual evidence for '+run+' step '+str(x['step']))
        if images and len(images)!=1:raise ValueError('Ambiguous screenshot for '+run+' step '+str(x['step']))
        out.append({'RunId':run,'Step':x['step'],'Input':x['label'],'Review':'NO_EXPECTED_VISIBLE_CONFIRMATION' if x['step'] in unconfirmed else 'VISIBLE_OUTCOME_OR_NORMAL_EXIT_CONFIRMED',
          'Evidence':images[0].relative_to(D).as_posix() if images else (p/'process-result.json').relative_to(D).as_posix(),
          'Scope':'External visual review; internal state NOT_OBSERVED' if images else 'PROCESS_EXIT_ONLY; no visual assertion'})
with (G/'INPUT_VISIBLE_REVIEW.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]),delimiter='\t');w.writeheader();w.writerows(out)
save(G/'TOOL_DIAGNOSTIC_NOTES.json',{'eval':'Node disallowed string code generation; helper was entered directly; no process injection',
 'crossProcessAssertion':'Initial full Profile equality failed. Original snapshots show only camp randomStateJson/events plus resource ordering differences. Existing ApplyCamp restarts world; full equality claim rejected, explicit difference report retained. History and all noncamp fields compared strictly.',
 'csvTypes':'Initial old-row dictionary comparison mismatched integer values and CSV strings; corrected representation conversion before exact value comparison, no Run classification changes.',
 'nativeInput':'R01 steps15-19 and R02 step9 lack expected visible confirmation; retained and excluded from consumption PASS count.'})
save(G/'INPUT_TOOL_IDENTITY.json',{'tool':'@oai/sky through mcp__node_repl__js','bundle':'computer-use 26.1117.41037',
 'nativeInputSourceSha256':hashlib.sha256((D/'native_release_input.js').read_bytes()).hexdigest(),
 'observerSourceSha256':hashlib.sha256((D/'release_run.py').read_bytes()).hexdigest(),'binaryInjectedIntoRelease':False})
print(json.dumps({'updated':'existing REPORT/ACCEPTANCE/TESTING/RISK','nativeAttempts':len(out),'confirmed':sum(x['Review']=='VISIBLE_OUTCOME_OR_NORMAL_EXIT_CONFIRMED' for x in out),'unconfirmed':6,'conclusion':'CONDITIONAL_PASS'}))
