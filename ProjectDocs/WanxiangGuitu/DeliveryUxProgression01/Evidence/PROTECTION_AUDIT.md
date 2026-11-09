# UX-PROGRESSION-01 · 保护审计（零产品改动）

> 审计对象：`design/ux-progression-01` 相对起点 `09e2a6eb486ee36cc6d85a60ab4f629d0c522581` 的全部改动。
> 结论：**仅新增文档与图，产品源码、场景、设置、包、存档、用户文件零改动。**

---

## 1. 工作树状态

命令：

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --porcelain
```

输出（原样）：

```
design/ux-progression-01
09e2a6eb486ee36cc6d85a60ab4f629d0c522581
?? ProjectDocs/WanxiangGuitu/DeliveryUxProgression01/
```

**唯一变更**是新增交付目录（未跟踪 → 待提交）。无修改文件、无删除文件。

---

## 2. 保护路径 diff

命令：

```bash
git diff --numstat -- Assets ProjectSettings Packages
```

输出：**空**（0 行）。

| 保护路径 | 改动文件数 | 改动行数 |
|---|---|---|
| `Assets/**`（142 个运行时脚本 + 29 配方 + 25 物品 + 5 品质 + 6 容器 + 全部场景/资源） | **0** | **0** |
| `ProjectSettings/**` | **0** | **0** |
| `Packages/**` | **0** | **0** |
| `ProjectDocs/WanxiangGuitu/` 历史交付目录 | **0**（未删除/未移动/未改写） | **0** |

---

## 3. 与本批禁区的逐项对照

| 禁区 | 是否触碰 | 证据 |
|---|---|---|
| v9 存档语义 | 否 | 无代码改动；设计层明确"只允许向后兼容新增，且需 D-15 单独决策"（`DESIGN.md` §0.1 I4、`DECISIONS.md` D-15） |
| 经济（材料产出/消耗/配方成本） | 否 | 无代码改动；成本梯度仅为**读取现有公式**的结果展示（`DESIGN.md` §5.2） |
| 掉落 / 宝箱概率 | 否 | 无代码改动；引用现有常量（`ForestRewards.cs:36`、`NewWeaponDropRules.cs:4`） |
| 随机流 | 否 | 无代码改动；设计要求目标层"零 RNG 调用"（`ACCEPTANCE_CRITERIA.md` B0-10） |
| 护甲减伤 | 否 | 无代码改动 |
| 经验曲线 | 否 | 无代码改动；D-06 明确"不引入持久等级" |
| 武器伤害 | 否 | 无代码改动；D-10 明确"不做单件升级" |
| 技能冷却 | 否 | 无代码改动；D-04 明确"不加第 3 技能" |
| 地图 / 场景 / 地形 | 否 | 无改动 |
| 用户文件 / 真实存档 | 否 | 未读取、未写入；本批未启动 Player，未产生任何存档目录 |
| 依赖 / CI | 否 | `Packages/**`、`.github/**` 无改动 |

---

## 4. 本批未运行项（如实声明）

| 项 | 状态 | 说明 |
|---|---|---|
| Player 构建 | 未运行 | 本批无代码改动，无需构建 |
| Player 真实运行 | 未运行 | 设计批次，不产生运行时证据；**不得**用历史 run 冒充本批证据 |
| 人工试玩 / 观感 | `NOT_RUN` | 按项目惯例，不用推断代替 |
| 单元测试 / CI | 未运行 | 仓库无对应 CI；本批不新增 |

> 本批的证据类型是**静态事实**（文件、行号、哈希、diff），不是运行时断言。二者不可互相替代。

---

## 5. 交付文件哈希

全量清单：[PROTECTION_HASHES.tsv](PROTECTION_HASHES.tsv)（`path` + `sha256` 两列，制表符分隔）。

复核命令：

```bash
cd ProjectDocs/WanxiangGuitu/DeliveryUxProgression01
python - <<'PY'
import hashlib
ok=bad=0
for line in open('Evidence/PROTECTION_HASHES.tsv',encoding='utf-8'):
    if line.startswith('path\t'): continue
    rel,want=line.rstrip('\n').split('\t')
    got=hashlib.sha256(open(rel,'rb').read()).hexdigest()
    ok,bad=(ok+1,bad) if got==want else (ok,bad+1)
    if got!=want: print('MISMATCH',rel)
print('ok',ok,'bad',bad)
PY
```

> 注意：`Evidence/PROTECTION_HASHES.tsv` 自身不在清单内（自引用会破坏哈希）。

本目录附带 [`.gitattributes`](../.gitattributes)（`* -text`），禁止 Git 做 CRLF 归一化，
否则 `core.autocrlf=true` 的机器在 checkout 后会把 LF 换成 CRLF，导致同一提交在不同机器上哈希不一致。
这与仓库既有 `DeliveryUX01/Evidence/** -text` 的字节保持约定一致。

---

## 6. 复核结论

1. 产品源码零改动，可由 `git diff --numstat -- Assets ProjectSettings Packages` 一条命令证明。
2. 本批全部产出为 `.md` 与 `.svg`，无二进制、无凭据、无用户数据。
3. 设计中的每个"改动点"都被显式分类：P1 只读、P2 需决策、P4 不做（`ROADMAP.md` 总览表）。
4. 历史交付目录未被触碰；本批不覆盖任何既有 PASS/FAIL 结论。
