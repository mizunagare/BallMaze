#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UX-PROGRESSION-03A-R1 可复算数值模型（只读，不改产品代码）

用法：
    python build_balance_model.py --out <交付目录>

输入：本文件里的源码参数表，全部来自 Assets/CombatPrototype 逐行读取，每行带 src
      锚点；不含任何设计想象的数值。
输出：
    SKILL_VALUE_MODEL.csv         7 套普攻 + 4 旧槽0 + 14 扩展技能的模型读数
    BEFORE_AFTER_MATRIX.csv       14 技能 + 10 词缀规则 + 9 品质专属 + 7 武器构筑
    SENSITIVITY.csv               N/H 敏感度（cap、H 为理论假设）
    FOCUS_SYMMETRY_IMPACT.csv     聚能 E-A +1s 对 8 个旧扩展技能的影响
    MODEL_SUMMARY.csv             T1/T2 与 T3 分离的统计摘要
    Evidence/Tools/model-run.json 参数表 SHA、全部输出 SHA、行数与统计摘要

R1 口径（见 ERRATA.md）：
  * T1/T2 = 12 项输出技能，用 B/η 评价，通过只能称 MODEL_PASS；
  * T3 = 2 项（twin.counter 条件反击、sc.pull 纯控制），B/η 仅保留在附录，
    不作目标判定、不调整任何数值；
  * 8/14 B<1 是「全 14 项」的计数，其中 2 项是 T3；T1/T2 中 B<1 为 6/12；
  * 品质专属 9 条全部 DESIGN_ONLY，不进默认实施包；
  * cap / H 是理论假设，不是 Player 实测；
  * 公式与假设是模型边界，不是完整实战 DPS 模拟。

所有伤害以 P = hero.AttackPower 归一化；P = 25 + Equipment.AttackBonus +
Progression.AttackBonus（ThirdPersonHero.cs:22）。η/B 是比值，与 P 的具体数值无关。
"""
import argparse, csv, hashlib, io, json, os, datetime

MODEL_VERSION = "UX03A-R1-CALC-02"

# ---------------------------------------------------------------------------
# L0 源码参数表（禁止手改；改数值必须同时改 src 锚点并复核源码）
# ---------------------------------------------------------------------------

# 普攻：mults = 一个完整循环内各次 Release 的伤害系数（×P）
# cycle = 一个完整循环的秒数（连续普攻的闸门间隔和）
# window = 该循环内角色处于动作中的秒数（不参与 R 计算）
# cap = 密集敌群中该形状单 Release 能覆盖的不同目标数上限【理论假设，非 Player 实测】
BASICS = [
    # id, mults, cycle, window, cap, shape, src
    ("Sword",       [1.00],              .50, .50, 3, "横扫 半角75.5° r=1.8+Reach", "AdventureCombat.cs:70-72,79,181;ThirdPersonHero.cs:10"),
    ("Spear",       [1.25],              .65, .55, 2, "窄刺 半角28.4° 横向0.4m r=3.1", "AdventureCombat.cs:70-74,181"),
    ("Staff",       [1.00],              .50, .50, 2, "弹体 + 0.9m 爆半径 v=16 t=2.5", "AdventureCombat.cs:176,180,189;AdventureCombat.cs:271"),
    ("Bow",         [1.00],              .50, .50, 1, "单箭点命中 v=23 t=2.5",        "AdventureCombat.cs:176,189;AdventureCombat.cs:271"),
    ("TwinBlades",  [.42, .42, .85],     .90, .84, 2, "三段局部胶囊 r=0.38",          "NewWeaponCombat.cs:41,43,44"),
    ("Greatsword",  [1.05],              1.05, .95, 4, "扇形 半角65° r=2.6",           "GreatswordCombat.cs:3,5,6,10"),
    ("Scythe",      [.80],               .80, .65, 4, "弧形 半角85° r=3.0",           "ScytheCombat.cs:3,5,6"),
]

# kind: slot0 = 旧武器内置技能（Selected==0），expansion = 14 项扩展技能
# W 由 startup / gap / pulses / charge / recovery 按源码时序算出，不手填
SKILLS = [
    # id, weapon, name, kind, mults, startup, gap, pulses, charge, recovery, cooldown, cap, h_class, mech, quality_extra(w,p,g,r), src
    ("sword.whirl",  "Sword", "旋风横扫", "slot0", [2.00], .20, 0, 1, 0, .30, 7, 5, "melee", "360°", [0,.75,2.25,2.25], "AdventureCombat.cs:186"),
    ("sword.triple", "Sword", "三拍连斩", "expansion", [.65,.65,.65], .22, .22, 3, 0, .22, 8, 3, "melee", "无独占", [0,0,0,0], "WeaponSkillExpansion.cs:9"),
    ("sword.circle", "Sword", "回旋剑阵", "expansion", [.55,.55,.55], .32, .48, 3, 0, .22, 11, 5, "melee", "360°", [0,0,0,0], "WeaponSkillExpansion.cs:10"),
    ("spear.thrust", "Spear", "贯穿突刺", "slot0", [2.40], .225, 0, 1, 0, .275, 7, 2, "melee", "窄线", [0,.80,.80,1.80], "AdventureCombat.cs:187"),
    ("spear.charge", "Spear", "蓄势穿刺", "expansion", [2.22], .24, 0, 1, .85, .22, 9, 1, "charge", "蓄力", [0,0,0,0], "WeaponSkillExpansion.cs:11,46"),
    ("spear.sweep",  "Spear", "扫锋拒敌", "expansion", [.80,.80], .27, .30, 2, 0, .22, 10, 3, "melee", "双扇", [0,0,0,0], "WeaponSkillExpansion.cs:12"),
    ("staff.meteor", "Staff", "陨火爆裂", "slot0", [2.20], .25, 0, 1, 0, .25, 7, 4, "projectile", "爆半径", [0,0,1.60,1.60], "AdventureCombat.cs:188;:109"),
    ("staff.field",  "Staff", "余烬符阵", "expansion", [.65,.40,.40,.40], .34, 0, 1, 0, .22, 10, 4, "field", "留场", [0,0,0,0], "WeaponSkillExpansion.cs:13,53;SkillPhysicalEffects.cs:18-25"),
    ("staff.echo",   "Staff", "回响连珠", "expansion", [.55,.55,.55], .30, .32, 3, 0, .22, 9, 1, "projectile", "分时重瞄", [0,0,0,0], "WeaponSkillExpansion.cs:14"),
    ("bow.rain",     "Bow",   "扇形箭雨", "slot0", [1.20]*5, .225, 0, 1, 0, .275, 7, 3, "projectile", "多箭", [0,2.40,2.40,4.80], "AdventureCombat.cs:189;:108"),
    ("bow.burst",    "Bow",   "追点连射", "expansion", [.55,.55,.55], .25, .22, 3, 0, .22, 9, 1, "projectile", "分时重瞄", [0,0,0,0], "WeaponSkillExpansion.cs:15"),
    ("bow.pierce",   "Bow",   "蓄势贯矢", "expansion", [2.13], .30, 0, 1, 1.00, .22, 11, 3, "pierce", "贯穿3+蓄力", [0,0,0,0], "WeaponSkillExpansion.cs:16,53;SkillPhysicalEffects.cs:3-16"),
    ("twin.volley",  "TwinBlades", "影袭连舞", "expansion", [.40]*6, .14, .13, 6, 0, .23, 7, 2, "melee", "六段", [0,0,0,0], "NewWeaponCombat.cs:10,43,44"),
    ("twin.counter", "TwinBlades", "双刃反击", "expansion", [.65], .28, 0, 1, 0, .24, 8, 1, "conditional", "强化180%", [0,0,0,0], "NewWeaponCombat.cs:20,43,44"),
    ("gs.cleave",    "Greatsword", "崩山重斩", "expansion", [1.70], .80, 0, 1, 0, .50, 9, 4, "melee", "破防0.75s", [0,0,0,0], "GreatswordCombat.cs:5,6,10"),
    ("gs.wave",      "Greatsword", "裂地冲击", "expansion", [.95], .80, 0, 1, 0, .50, 10, 4, "field", "地面贯穿8m", [0,0,0,0], "GreatswordCombat.cs:19-21"),
    ("sc.reap",      "Scythe", "回旋收割", "expansion", [.45,.45,.45], .30, .28, 3, 0, .35, 8, 4, "melee", "三段宽弧", [0,0,0,0], "ScytheCombat.cs:5,6"),
    ("sc.pull",      "Scythe", "灵魂牵引", "expansion", [0.00], .40, 0, 1, 0, .35, 11, 4, "control", "牵引1s·0伤害", [0,0,0,0], "ScytheCombat.cs:5,6;NewWeaponCombat.cs:10;EnemyWeaponControl.cs:4-8"),
]

# R1：T3 两项冻结原始数值，禁止出现在 PROPOSALS 的数值键里，不纳入 B/η 目标判定
T3_SKILLS = {"twin.counter": "条件反击", "sc.pull": "纯控制"}

# 提案：只动 L1 常量（cooldown / power / startup / gap / charge），不改判定路径。
# T3 无数值提案（sc.pull 的 startup 0.40→0.30 / C 11→8 已在 R1 撤销）。
PROPOSALS = {
    "sword.triple": dict(cooldown=7,                                     note="去掉「无独占机制却比槽0长1s」的纯劣势；倍率与判定不动"),
    "sword.circle": dict(gap=.30, scale=1.5454545, cooldown=10,          note="0.55→0.85/段；gap 0.48→0.30（W 1.50→1.14）；360° 是独占机制"),
    "spear.charge": dict(charge=.60, cooldown=8,                         note="蓄力 0.85→0.60 缩短无保护窗口；伤害不动（B 由 W 改善）"),
    "spear.sweep":  dict(gap=.24, scale=1.0625, cooldown=9,               note="0.80→0.85/段；gap 0.30→0.24；两道扇是独占机制"),
    "staff.field":  dict(cooldown=9,                                     note="已达标（B=1.65）；仅把过长冷却对齐到 9s"),
    "staff.echo":   dict(gap=.22, scale=1.2727273,                        note="0.55→0.70/段；gap 0.32→0.22；分时重瞄是独占机制"),
    "bow.burst":    dict(gap=.18, scale=1.1272727,                        note="0.55→0.62/段；gap 0.22→0.18；不与红弓箭雨比倍率"),
    "bow.pierce":   dict(charge=.70, scale=1.1739, cooldown=10,           note="基础 1.15→1.35（满蓄 2.13→2.50）；蓄力 1.0→0.70；贯穿3是独占机制"),
    "twin.volley":  dict(                                                note="基准对照，不改动（B=1.25 已达标）"),
    "gs.cleave":    dict(startup=.65,                                    note="技能前摇 0.80→0.65（W 1.30→1.15）；倍率与破防不动。共用常量需按 wave 分支拆开"),
    "gs.wave":      dict(startup=.60, scale=1.3684,                       note="技能前摇 0.80→0.60（W 1.30→1.10）；0.95→1.30；地面贯穿是独占机制"),
    "sc.reap":      dict(gap=.24,                                        note="技能段间隔 0.28→0.24（W 1.21→1.13）；倍率不动"),
}

# 硬约束：T3 不得有任何数值键
for _t3 in T3_SKILLS:
    assert _t3 not in PROPOSALS or all(k == "note" for k in PROPOSALS[_t3]), \
        "T3 %s 不得有数值提案" % _t3

# L3 词缀规则：现状 vs 提案
AFFIX_ROWS = [
    ("回响", "旧武器普攻 ×4", "不生效：BeginAttack 写了 a.area，Release 普攻分支不读", "R-1 明示为不适用", "L3规则+L4文案", "否", "YES", "03A 默认包（R-1）", "AdventureCombat.cs:81,181"),
    ("回响", "旧武器槽0 ×4", "生效：4*area / 7*area / StaffBlastRadius(q,area) / 12*area", "R-1 保持并枚举到 UI", "L3规则+L4文案", "否", "YES", "03A 默认包（R-1）", "AdventureCombat.cs:117-120,186-189"),
    ("回响", "旧武器扩展技能 ×8", "不生效：ExpandedMelee 直接传 def.reach，不乘 area", "R-1 明示不适用；R-2 才补齐", "L2判定(未授权)", "否", "NO", "R-2 需单独授权，不进默认包", "WeaponSkillExpansion.cs:52;AdventureCombat.cs:71"),
    ("回响", "新武器普攻 ×3", "不生效：NewSector/TwinHit 只在 phase>=10 读 id=2", "R-1 明示不适用", "L3规则+L4文案", "否", "YES", "03A 默认包（R-1）", "NewWeaponCombat.cs:32;GreatswordCombat.cs:10"),
    ("回响", "新武器技能 ×6", "生效：扇形/胶囊/牵引/冲击波 radius,reach,limit ×1.25", "R-1 保持并枚举到 UI", "L3规则+L4文案", "否", "YES", "03A 默认包（R-1）", "GreatswordCombat.cs:10,19;ScytheCombat.cs:10;NewWeaponCombat.cs:32"),
    ("聚能", "普攻 ×7", "不生效：WeaponHit.Apply 的 skill 标志为 false", "E-A 保持", "L3规则", "否", "YES", "03A 默认包（E-A）", "WeaponHit.cs:8"),
    ("聚能", "全部技能伤害", "生效：×1.25（含留场脉冲与地面波）", "E-A 保持（对称的收益侧）", "L3规则", "否", "YES", "03A 默认包（E-A）", "WeaponHit.cs:8;SkillPhysicalEffects.cs:22;GreatswordCombat.cs:21"),
    ("聚能", "旧武器槽0 ×4", "生效：SkillDuration 与 UseSkill 各 +1s", "E-A 保持", "L1数值", "否", "YES", "03A 默认包（E-A）", "AdventureCombat.cs:104,151"),
    ("聚能", "新武器技能 ×6", "生效：SkillDuration +1s", "E-A 保持", "L1数值", "否", "YES", "03A 默认包（E-A）", "NewWeaponCombat.cs:11"),
    ("聚能", "旧武器扩展技能 ×8", "不生效：TryCast→PrepareExpanded(def.cooldown) 绕过 +1s；SkillDuration 也直接返回 def.cooldown", "E-A 补 +1s 到 TryCast 与 SkillDuration", "L1数值+L3规则+L4文案", "是", "YES", "03A 默认包（E-A）", "WeaponSkillExpansion.cs:39;AdventureCombat.cs:66,104"),
]

# 品质专属：R1 全部 DESIGN_ONLY，9 条均不进 03A 默认实施包；2 条 L2 继续需单独授权
QUALITY_DEFAULT_PACKAGE = "NO（DESIGN_ONLY / 不进默认包）"
QUALITY_ROWS = [
    ("TwinBlades", "Purple", "双刃", "无", "第三段双刃交叉额外产生一次侧向胶囊（同目标去重）", "复用 TwinHit 的 hand==2 双胶囊路径", "L2判定(需单独授权)", "NewWeaponCombat.cs:32,44"),
    ("TwinBlades", "Gold",   "双刃", "无", "影袭连舞 6 段 → 8 段（段间隔不变）", "复用 TwinBladeMotor 的 phase<5 循环上限", "L1数值", "NewWeaponCombat.cs:44"),
    ("TwinBlades", "Red",    "双刃", "无", "反击强化倍率 1.8 → 2.2，强化窗 0.85s → 1.20s", "复用 ConsumeEvade 窗口与 counter 倍率", "L1数值", "NewWeaponCombat.cs:20,44"),
    ("Greatsword", "Purple", "巨剑", "无", "崩山重斩破防 0.75s → 1.10s（Boss 仍免疫）", "复用 EnemyWeaponControl.Break(duration)", "L1数值", "GreatswordCombat.cs:10;EnemyWeaponControl.cs:6"),
    ("Greatsword", "Gold",   "巨剑", "无", "裂地冲击波半径 0.3→0.42m、行程 8→10m", "复用 NewGroundShock 的 radius/limit", "L1数值", "GreatswordCombat.cs:19"),
    ("Greatsword", "Red",    "巨剑", "无", "崩山重斩命中后追加一次 50% 伤害的地面波", "复用 NewGroundShock.Spawn（同旧武器「红追加枪芒」的参数族）", "L2判定(需单独授权)", "GreatswordCombat.cs:19;AdventureCombat.cs:187"),
    ("Scythe",     "Purple", "镰刀", "无", "回旋收割扇形 3.4m → 4.0m（角度不变）", "复用 NewSector 的 reach 参数", "L1数值", "ScytheCombat.cs:6"),
    ("Scythe",     "Gold",   "镰刀", "无", "灵魂牵引 4.5m → 5.6m（Boss 仍免疫）", "复用 PullSector 的 reach 参数", "L1数值", "ScytheCombat.cs:10"),
    ("Scythe",     "Red",    "镰刀", "无", "回旋收割 3 段 → 4 段（每段伤害不变）", "复用 ScytheMotor 的 phase<2 循环上限", "L1数值", "ScytheCombat.cs:6"),
]

# 七武器构筑差异（稳定 / 高风险两套）——只读对照，不改叠加规则
BUILDS = [
    ("Sword",       "回旋剑阵 + 三拍连斩", "三拍连斩 + 回旋剑阵", "宽角容错 / 360° 清围", "0-2.5m 贴身；无远程", "1.8m 内"),
    ("Spear",       "扫锋拒敌 + 蓄势穿刺", "蓄势穿刺 + 扫锋拒敌", "窄线单发 / 双扇清横向", "横向移动目标易空枪；蓄力无保护", "2-4.2m"),
    ("Staff",       "陨火爆裂(槽0) + 余烬符阵", "回响连珠 + 蓄势冲击", "留场 / 连续点名", "弹速 16；遮挡即失效", "6-35m"),
    ("Bow",         "扇形箭雨(槽0) + 追点连射", "蓄势贯矢 + 追点连射", "多箭爆发 / 排队贯穿", "被逼近后 1.8m 外无手段", "8-57.5m"),
    ("TwinBlades",  "影袭连舞 + 双刃反击(强化)", "双刃反击 + 影袭连舞", "高频段数 / 翻滚反击", "必须贴身；强化依赖真实被闪避攻击", "0-1.4m"),
    ("Greatsword",  "崩山重斩 + 裂地冲击", "裂地冲击 + 崩山重斩", "破防 / 直线清场", "1.05s 循环；0.8s 前摇", "1.5-8m"),
    ("Scythe",      "回旋收割 + 灵魂牵引", "灵魂牵引 + 回旋收割", "宽弧 / 牵引拉近", "牵引对 Boss 免疫且 0 伤害", "1.2-5.6m"),
]

MODEL_ASSUMPTIONS = [
    ("W", "技能占用且不能普攻的窗口", "由 startup/gap/charge/recovery 按源码时序算出"),
    ("C", "冷却从施放开始计时", "PrepareExpanded / UseSkill / SetNewCooldown 均在 Begin 时写入"),
    ("C>=W", "冷却不短于窗口", "脚本逐行断言"),
    ("冷却剩余", "按纯普攻输出填满", "保守下界；不考虑两个技能交替"),
    ("不考虑", "敌人移动、遮挡、打断、目标死亡溢出、控制收益", "模型边界，不是完整实战 DPS 模拟"),
    ("cap", "形状覆盖目标数上限", "理论假设，非 Player 实测；主模型 N=1"),
    ("H", "弹体/蓄力/留场命中可靠性", "理论假设，非 Player 实测；主模型 H=1.0"),
]


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def window_of(s, p=None):
    """按源码时序算 W（秒）。charge 型先等 charge 再等 startup，然后 recovery。"""
    startup = (p or {}).get("startup", s[5])
    gap = (p or {}).get("gap", s[6])
    pulses = s[7]
    charge = (p or {}).get("charge", s[8])
    recovery = (p or {}).get("recovery", s[9])
    if charge > 0:
        return charge + startup + recovery
    return startup + (pulses - 1) * gap + recovery


def damage_of(s, p=None, quality_index=0):
    scale = (p or {}).get("scale", 1.0)
    return sum(s[4]) * scale + s[14][quality_index]


def cooldown_of(s, p=None):
    return (p or {}).get("cooldown", s[10])


def metrics(D, W, C, R, N=1, H=1.0, cap=1, cap_basic=1):
    """返回 G / eta / B。η = 1 + (B-1)*W/C 是恒等式（见 CALC_MODEL.md §3）。"""
    Dn = D * min(N, cap) * H
    Rn = R * min(N, cap_basic)
    G = Dn - Rn * W
    eta = 1.0 + G / (Rn * C) if Rn > 0 else float("nan")
    B = Dn / (Rn * W) if Rn * W > 0 else 0.0
    return G, eta, B


def f(x, n=4):
    return ("%." + str(n) + "f") % x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = a.out
    os.makedirs(os.path.join(out, "Evidence", "Tools"), exist_ok=True)

    R = {}
    basic_rows = []
    for bid, mults, cycle, window, cap, shape, src in BASICS:
        r = sum(mults) / cycle
        R[bid] = r
        basic_rows.append(dict(
            row_type="basic", id=bid, weapon=bid, name="普攻(完整循环)", kind="basic", band="REFERENCE",
            metric_status="REFERENCE", eta_applicable="否（普攻无冷却）", target_check="N/A (基线)",
            in_default_package="NO（基线）", D="", W=f(window), C="", R=f(r), G="", eta="", B="",
            D_red="", eta_red="", B_red="", D_after="", W_after="", C_after="",
            eta_after="", B_after="", cap=cap, h_class="melee", mech="—", quality_extra="",
            cap_assumption="理论假设", H_assumption="理论假设",
            src=src, note="R=Σm/cycle；普攻无冷却，η/B 不适用"))

    skill_rows, ba_rows, sens_rows, focus_rows = [], [], [], []
    stat = dict(total=0, t1=0, t2=0, t3=0, t3_conditional=0, t3_control=0,
                b_lt1_all=0, b_lt1_t3=0, b_lt1_t12=0,
                model_pass=0, model_fail=0, focus_pass=0, focus_fail=0)
    identity_max = 0.0

    for s in SKILLS:
        sid, w, name, kind = s[0], s[1], s[2], s[3]
        cap, h_class, mech, qextra, src = s[11], s[12], s[13], s[14], s[15]
        r = R[w]
        cap_basic = next(b[4] for b in BASICS if b[0] == w)
        p = PROPOSALS.get(sid, {}) if kind == "expansion" else {}
        D0, W0, C0 = damage_of(s), window_of(s), cooldown_of(s)
        D1, W1, C1 = damage_of(s, p), window_of(s, p), cooldown_of(s, p)
        assert C0 >= W0 and C1 >= W1, "C>=W 违反：%s C0=%.2f W0=%.2f" % (sid, C0, W0)
        G0, e0, B0 = metrics(D0, W0, C0, r, cap=cap, cap_basic=cap_basic)
        G1, e1, B1 = metrics(D1, W1, C1, r, cap=cap, cap_basic=cap_basic)
        identity_max = max(identity_max, abs(e0 - (1 + (B0 - 1) * W0 / C0)))
        D0r = damage_of(s, quality_index=3)
        _, e0r, B0r = metrics(D0r, W0, C0, r, cap=cap, cap_basic=cap_basic)

        # ---- R1 分带：slot0 只是参照基线；T3 由 id 指定；其余按「有无独占机制」分 T1/T2 ----
        is_slot0 = kind == "slot0"
        is_t3 = sid in T3_SKILLS
        if is_slot0:
            band, metric_status = "REFERENCE", "REFERENCE"
            eta_applicable, target_check = "—（槽0 基线）", "N/A (基线)"
        elif is_t3:
            band, metric_status = "T3", "APPENDIX_ONLY (T3)"
            eta_applicable = ("否（%s）" % ("0 伤害纯控制，按牵引成功率验收" if h_class == "control"
                                         else "条件触发，拆未强化/强化双口径"))
            target_check = "N/A (T3)"
        else:
            band = "T1" if mech == "无独占" else "T2"
            metric_status, eta_applicable = "MODEL", "是"
            ok = B1 >= (1.10 if band == "T1" else 1.00) and e1 >= (1.01 if band == "T1" else 1.00)
            target_check = "MODEL_PASS" if ok else "MODEL_FAIL"
        note = (p.get("note", "槽0 参照基线，不参与 14 项统计") if is_slot0 else
                p.get("note", "T3 冻结原始常量（startup/cooldown/伤害均不调整）" if is_t3
                      else "基准（不改动）"))
        in_default = ("NO（槽0 基线）" if is_slot0 else
                      "NO（T3 冻结）" if is_t3 else
                      ("YES" if kind == "expansion" else "NO（基线）"))

        # 统计口径：全 14 项 vs T1/T2 12 项严格分离
        if kind == "expansion":
            stat["total"] += 1
            if is_t3:
                stat["t3"] += 1
                stat["t3_conditional" if h_class == "conditional" else "t3_control"] += 1
                if B0 < 1:
                    stat["b_lt1_t3"] += 1
            else:
                stat["t1" if band == "T1" else "t2"] += 1
                if B0 < 1:
                    stat["b_lt1_t12"] += 1
                stat["model_pass" if target_check == "MODEL_PASS" else "model_fail"] += 1
            if B0 < 1:
                stat["b_lt1_all"] += 1

        skill_rows.append(dict(
            row_type="skill", id=sid, weapon=w, name=name, kind=kind, band=band,
            metric_status=metric_status, eta_applicable=eta_applicable, target_check=target_check,
            in_default_package=in_default,
            D=f(D0), W=f(W0), C=f(C0), R=f(r), G=f(G0), eta=f(e0), B=f(B0),
            D_red=f(D0r), eta_red=f(e0r), B_red=f(B0r),
            D_after=f(D1), W_after=f(W1), C_after=f(C1), eta_after=f(e1), B_after=f(B1),
            cap=cap, h_class=h_class, mech=mech, quality_extra="|".join(f(x, 2) for x in qextra),
            cap_assumption="理论假设（非 Player 实测）", H_assumption="理论假设（非 Player 实测）",
            src=src, note=note))

        if kind == "expansion":
            ba_rows.append(dict(
                category="L1-技能数值", id=sid, weapon=w, band=band,
                metric_status=metric_status, in_default_package=in_default,
                before="D=%s W=%s C=%s eta=%s B=%s" % (f(D0, 2), f(W0, 2), f(C0, 1), f(e0), f(B0, 3)),
                after=("冻结：数值不变" if is_t3 else
                       "D=%s W=%s C=%s eta=%s B=%s" % (f(D1, 2), f(W1, 2), f(C1, 1), f(e1), f(B1, 3))),
                delta=("Δ=0（R1 撤销 startup 0.40→0.30 / C 11→8；sc.pull 维持原值）" if sid == "sc.pull" else
                       "Δ=0（R1 冻结；twin.counter 维持原值，等 T3 专项验证）") if is_t3 else
                       "ΔD=%+.2f ΔW=%+.2f ΔC=%+.1f Δeta=%+.4f ΔB=%+.3f" % (D1 - D0, W1 - W0, C1 - C0, e1 - e0, B1 - B0),
                layer="L1 数值平衡" if not is_t3 else "冻结（无 L1 改动）",
                target_check=target_check,
                needs_code="否（T3 冻结）" if is_t3 else ("是（实现批）" if p else "否（基准）"),
                authorization="T3 专项验证前保持原值" if is_t3 else "03A 规格通过后",
                rationale=note, src=src))

        # E-A 聚能代价补齐：8 个旧扩展技能 +1s 后是否仍在目标带内
        if kind == "expansion" and w in ("Sword", "Spear", "Staff", "Bow"):
            e_focus = 1 + (B1 - 1) * W1 / (C1 + 1)
            ok = (e_focus >= (1.01 if band == "T1" else 1.00)
                  and B1 >= (1.10 if band == "T1" else 1.00))
            stat["focus_pass" if ok else "focus_fail"] += 1
            focus_rows.append(dict(
                id=sid, name=name, band=band, cooldown_proposed=f(C1, 1),
                cooldown_with_focus=f(C1 + 1, 1), B_after=f(B1, 3),
                eta_proposed=f(e1), eta_with_focus=f(e_focus), delta=f(e_focus - e1, 5),
                still_in_band="MODEL_PASS" if ok else "MODEL_FAIL",
                metric_status="MODEL", note="E-A 只收回应有代价；伤害侧 ×1.25 不变"))

        # 敏感度：N ∈ {1,3,5}；H ∈ {1.0,.8,.6}（只作用于非近战类）
        for N in (1, 3, 5):
            for H in (1.0, .8, .6):
                Hs = H if h_class in ("projectile", "pierce", "field", "charge", "control", "conditional") else 1.0
                _, eN, BN = metrics(D0, W0, C0, r, N=N, H=Hs, cap=cap, cap_basic=cap_basic)
                _, eN1, BN1 = metrics(D1, W1, C1, r, N=N, H=Hs, cap=cap, cap_basic=cap_basic)
                sens_rows.append(dict(
                    id=sid, name=name, band=band, metric_status=metric_status, N=N, H=Hs,
                    eta_before=f(eN), B_before=f(BN), eta_after=f(eN1), B_after=f(BN1),
                    cap=cap, cap_basic=cap_basic,
                    cap_assumption="理论假设（非 Player 实测）", H_assumption="理论假设（非 Player 实测）"))

    for row in AFFIX_ROWS:
        ba_rows.append(dict(category="L3-词缀规则", id=row[0] + "/" + row[1], weapon="", band="N/A",
                            metric_status="RULE", in_default_package=row[6],
                            before=row[2], after=row[3], delta="", layer=row[4],
                            target_check="N/A", needs_code=row[5], authorization=row[7],
                            rationale="", src=row[8]))
    for row in QUALITY_ROWS:
        ba_rows.append(dict(category="L4-品质专属", id=row[0] + "/" + row[1], weapon=row[2], band="N/A",
                            metric_status="DESIGN_ONLY", in_default_package=QUALITY_DEFAULT_PACKAGE,
                            before=row[3], after=row[4], delta="", layer=row[6],
                            target_check="N/A", needs_code="否（未授权）",
                            authorization="品质专属单独授权；两条 L2 需单独授权；回响叠乘上界需先拍板",
                            rationale=row[5], src=row[7]))
    for bid, stable, risky, diff, risk, band in BUILDS:
        ba_rows.append(dict(category="构筑对照", id=bid, weapon=bid, band="N/A",
                            metric_status="READ_ONLY", in_default_package="NO（只读对照）",
                            before="稳定/低风险: " + stable, after="高风险/高收益: " + risky,
                            delta="", layer="只读对照（不改叠加规则）", target_check="N/A",
                            needs_code="否", authorization="D-24 未授权",
                            rationale=diff + "；风险=" + risk + "；有效带=" + band,
                            src="SKILL_BUILD_MATRIX.csv(P02)"))

    # ---- MODEL_SUMMARY.csv：T1/T2 与 T3 分离的统计摘要 ----
    assert stat["total"] == 14 and stat["t1"] + stat["t2"] == 12 and stat["t3"] == 2
    assert stat["t3_conditional"] == 1 and stat["t3_control"] == 1
    assert stat["b_lt1_all"] == 8 and stat["b_lt1_t3"] == 2 and stat["b_lt1_t12"] == 6
    assert stat["model_pass"] == 12 and stat["model_fail"] == 0
    assert stat["focus_pass"] == 8 and stat["focus_fail"] == 0
    summary_rows = [
        ("扩展技能总数", stat["total"], "全 14 项", "R1 保留 14 项总数"),
        ("参照基线行", 11, "7 普攻 + 4 旧槽0", "REFERENCE，不参与 14 项统计；25 行 = 11 参照 + 12 T1/T2 + 2 T3"),
        ("T1 输出技能", stat["t1"], "T1/T2 口径", "无独占机制，B≥1.10 且 η≥1.01"),
        ("T2 输出技能", stat["t2"], "T1/T2 口径", "有独占机制，B≥1.00 且 η≥1.00"),
        ("T1/T2 合计", stat["t1"] + stat["t2"], "T1/T2 口径", "唯一使用 B/η 做目标判定的范围"),
        ("T3 条件反击", stat["t3_conditional"], "T3 口径", "twin.counter；B/η 仅附录"),
        ("T3 纯控制", stat["t3_control"], "T3 口径", "sc.pull；B/η 仅附录"),
        ("T3 合计", stat["t3"], "T3 口径", "不纳入 B/η 通过率；数值全部冻结"),
        ("B<1 全 14 项", stat["b_lt1_all"], "全 14 项（含 T3）", "8/14：含 2 个 T3，不代表 8 个输出技能弱于普攻"),
        ("B<1 中的 T3", stat["b_lt1_t3"], "T3 口径", "twin.counter 与 sc.pull，不作目标判定"),
        ("B<1 的 T1/T2", stat["b_lt1_t12"], "T1/T2 口径", "6/12：这才是「输出技能」的现状计数"),
        ("提案后 MODEL_PASS", stat["model_pass"], "T1/T2 口径", "仅离线模型落入目标带，不是真实战斗通过"),
        ("提案后 MODEL_FAIL", stat["model_fail"], "T1/T2 口径", "0"),
        ("E-A 后仍在带内", stat["focus_pass"], "8 个旧扩展技能", "MODEL_PASS 8/8"),
        ("E-A 后掉出带内", stat["focus_fail"], "8 个旧扩展技能", "0"),
        ("模型恒等式最大误差", "%.6g" % identity_max, "18 个技能行", "η=1+(B−1)W/C；CSV 保留 4 位小数"),
        ("cap 性质", "理论假设", "全部行", "非 Player 实测；主模型 N=1"),
        ("H 性质", "理论假设", "全部行", "非 Player 实测；主模型 H=1.0"),
        ("品质专属默认包状态", "DESIGN_ONLY ×9", "品质提案", "9 条全部移出 03A 默认实施包"),
        ("默认包 L1 技能提案", 12, "T1/T2", "排除 2 个 T3；T3 数值冻结"),
    ]
    for key, val, note in MODEL_ASSUMPTIONS:
        summary_rows.append(("模型假设 / " + key, val, "模型边界", note))
    summary = [dict(metric=k, value=v, scope=sc, note=n) for k, v, sc, n in summary_rows]

    def write(path, rows, cols=None):
        if cols is None:
            cols = []
            for row in rows:
                for k in row:
                    if k not in cols:
                        cols.append(k)
        with io.open(os.path.join(out, path), "w", encoding="utf-8", newline="") as fp:
            w = csv.DictWriter(fp, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for row in rows:
                w.writerow(row)
        return os.path.join(out, path)

    p1 = write("SKILL_VALUE_MODEL.csv", basic_rows + skill_rows)
    p2 = write("BEFORE_AFTER_MATRIX.csv", ba_rows)
    p3 = write("SENSITIVITY.csv", sens_rows)
    p4 = write("FOCUS_SYMMETRY_IMPACT.csv", focus_rows)
    p5 = write("MODEL_SUMMARY.csv", summary)

    all_out = [p1, p2, p3, p4, p5]
    manifest = {
        "generatedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "modelVersion": MODEL_VERSION,
        "parameterSourceSHA256": sha256_text(io.open(os.path.abspath(__file__), encoding="utf-8").read()),
        "outputs": {os.path.basename(p): sha256_text(io.open(p, encoding="utf-8").read()) for p in all_out},
        "rows": {"skill_value_model": len(basic_rows) + len(skill_rows),
                 "before_after": len(ba_rows), "sensitivity": len(sens_rows),
                 "focus_symmetry": len(focus_rows), "model_summary": len(summary)},
        "statistics": stat,
        "identityMaxError": identity_max,
        "defaultPackage": {
            "L1_skill_proposals": 12, "T3_frozen": 2,
            "affix": "E-A + R-1", "quality_exclusive": "DESIGN_ONLY (0 in default)",
            "excluded": ["R-2", "R-3", "E-B", "品质专属", "D-24"],
        },
    }
    with io.open(os.path.join(out, "Evidence", "Tools", "model-run.json"), "w", encoding="utf-8", newline="\n") as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)
        fp.write("\n")

    print("rows: skill_value_model=%d before_after=%d sensitivity=%d focus=%d summary=%d" % (
        len(basic_rows) + len(skill_rows), len(ba_rows), len(sens_rows), len(focus_rows), len(summary)))
    print("stat:", stat)
    print("identity max error: %.6g" % identity_max)
    print("param sha:", manifest["parameterSourceSHA256"][:20])
    for k, v in manifest["outputs"].items():
        print("  %-28s %s" % (k, v[:20]))


if __name__ == "__main__":
    main()
