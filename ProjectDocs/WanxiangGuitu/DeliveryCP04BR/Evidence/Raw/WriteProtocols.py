from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR');p.mkdir(exist_ok=True)
(p/'NATIVE_INPUT.md').write_text('''# 原生输入验收协议（待真实操作者执行）

状态 **NOT_RUN**。本批未发送物理键鼠输入，未激活私有桌面。API 驱动、WM_CLOSE、截图和自动 AI 不计入本表。

## 固定与隔离

登记发行可执行文件、Assembly-CSharp.dll SHA256、分支提交、Unity 版本、分辨率、设备、测试员和时间。仅使用工程外新建的合成存档根；继续组使用一份不可变合成档副本，Fresh 与 Continue 分目录。不得指向真实玩家存档。主菜单正常进入，记录实际键位设置页，不恢复默认、不改用户已有键位。

默认参考（以当前设置实际显示为准）：普攻鼠标左键、技能 F、换武器 V；鼠标/相机操作先查当前帮助。下列步骤必须由操作者执行真实输入，观察者独立记结果。独立会话不可用时保持 NOT_RUN，不抢占正在使用的桌面。

## 测试步骤

1. 物理移动鼠标，观察相机和准星响应；静止、水平、垂直、连续转向均记录。分别在左、中心、右侧相机位置观察同一目标；若产品没有肩位切换功能，使用实际 Orbit 转向并记录相机坐标，不虚构切换键。
2. 剑、矛、法杖、弓各进行普攻和技能（8项）。输入、预警/动作、真实释放、首次碰撞、Damage 分别记录，未命中也保留。
3. 法杖普攻/技能 × 0.35m、1.5m、6m、20m × 左/中/右相机（24项）。距离以真实枪口到目标表面及玩家到目标分别登记；无法可靠测量不判定距离用例通过。禁止移动目标或放宽断言替代原案例。
4. 墙体真实存在且 Collider 开启：相机遮挡、枪口遮挡分别测试，确认不穿墙；记录首次碰撞对象和实际伤害。
5. 释放前、释放后分别暂停/恢复；观察冻结和继续，无补发、重复命中。
6. 飞行中换武器，验证已释放弹体生命周期；连续普攻、连续技能、移动中攻击分别记录。不得修改冷却或注入 Damage。
7. 正常退出并新进程继续；比对合成存档身份。不将后台关闭结果当作标题栏关闭或人工输入证据。

录屏需覆盖输入、准星、目标、碰撞反馈和日志对应时间。每项独立填 PASS/FAIL/NOT_RUN/UNRESOLVED；过程安全冲突立即停止该项。

记录表见 [Evidence/Templates/native-input.csv](Evidence/Templates/native-input.csv)。自动化结果另见报告，绝不能预填本表。
''',encoding='utf8')
(p/'HUMAN_PLAYTEST.md').write_text('''# 独立人工体验记录

状态 **NOT_RUN**。以下由真实试玩者填写，本批仅准备协议，不从自动化推导体验。

记录试玩者（是否参与开发）、日期、固定版本/构建哈希、设备、分辨率、设置、合成档身份、是否接受提示。观察者记录困惑、停顿、失败和重试，不能把提示后的操作当作独立理解。

请分别评价并附原始录屏时间：

1. 法杖近距准星是否自然；何处出现不符合预期的方向。
2. 准星与真实弹体方向是否一致。
3. 遮挡拒绝发射/撞墙反馈是否清楚。
4. 是否出现穿墙或不合理命中。
5. 四武器动作是否协调。
6. 普攻和技能是否可辨。
7. 音效与命中时机是否匹配。
8. 连续战斗是否有可观察卡顿、残留或资源异常。

每项填写 PASS/FAIL/NOT_RUN/UNRESOLVED、描述、操作、期望、实际、录屏时间和严重度；不能仅写“感觉正常”。异常只形成问题/修复提案，不在本批修改产品。表见 [Evidence/Templates/human-playtest.csv](Evidence/Templates/human-playtest.csv)。
''',encoding='utf8')
t=p/'Evidence/Templates';t.mkdir(parents=True,exist_ok=True)
import csv
with (t/'native-input.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['case','tester','buildSHA256','saveRoot','physicalInput','camera','distance','firstCollision','damage','status','evidence','notes'])
 for weapon in ['sword','spear','staff','bow']:
  for action in ['basic','skill']:w.writerow([weapon+'-'+action]+['']*8+['NOT_RUN','',''])
 for action in ['basic','skill']:
  for d in [.35,1.5,6,20]:
   for cam in ['left','center','right']:w.writerow([f'staff-{action}-{d}-{cam}']+['']*8+['NOT_RUN','',''])
 for case in ['mouse-crosshair','camera-wall','muzzle-wall','pause-before-release','pause-flight','switch-flight','continuous','moving-attack','continue']:w.writerow([case]+['']*8+['NOT_RUN','',''])
with (t/'human-playtest.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['question','tester','version','input','expected','actual','status','videoTime','notes'])
 for q in ['近距准星','方向一致','遮挡反馈','穿墙异常','动作协调','普攻技能区别','音画时机','持续战斗']:w.writerow([q]+['']*5+['NOT_RUN','',''])
print('protocols written')
