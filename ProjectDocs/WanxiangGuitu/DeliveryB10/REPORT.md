# B10：卡通化体系与正式入口

实施中，尚未交付/推送，不认定复审通过。开工main本地与远端均b474765dc9c28aaf7d2d267bc0362f828f1902b0。用户ForestRuins.unity与ProjectSettings.asset保护，原始哈希见开工台账。

任务书三段已全部收到，B10仍按完整范围实施。原概念包已从用户提供的本机ZIP完整导入9张PNG，逐项大小/哈希见 ArtBible/Concepts/IMPORT_MANIFEST.json。用户随后明确原稿风格不满意，要求减少AI味并参考元气骑士/逃离鸭科夫的设计原则；原9张保持不变，新增02/03修订方向稿和STYLE_GUIDE.md，全部CONCEPT_ONLY，不认定用户定稿或资产完成。

P0修复前实际隔离回归：B10Before/20261026-095151-6e594ed6，场景ForestRuins、CombatSession=1、HUD=1、没有Title，回归exit1且有实际PNG。源码还保留正式Player的-wanxiang-test-gameplay直入路径；B09旧证据也明确其为受控绕过。B09正式无绕过参数的六种启动图原先正常，所以没有证据把用户现场归因于登录服务或默认Player一定无菜单；项目源码搜索未发现游戏账号登录模块。

增量修复：Boot→Title→选择→Forest；Editor普通Play通过专用playModeStartScene走Boot，不写用户场景/ProjectSettings。明确隔离root+-executeMethod的Editor验证可直开测试场景，强制普通入口回归可取消该豁免。正式程序集剔除直入分支，旧直入参数在有效隔离根下忽略并仍显示菜单；缺失/不合法隔离配置仍先拒绝。CombatSession与保存入口另有授权门禁，避免误加载Forest时初始化HUD或存档。

P0定向运行已完成：`D:/WanxiangValidationRuns/B10EntryAfter/20261026-100514-41501e48`，36 PASS、2预期探针FAIL、81 NOT_RUN、2 UNRESOLVED，0非预期FAIL。正式非开发构建0错误88警告，Missing/Ready/Corrupt/Incompatible/Pending/Committed/LegacyFlag七种Player启动检查通过。Editor普通入口观察为Title、Session=0、HUD=0。此为P0定向历史结果，不等于本次美术或B10完整All通过；写入不确定场景、完整新UI/资产运行与最终All仍待执行。

美术方向迭代与限制见 ArtBible/STYLE_REVISION.md；生成图不作为before/after实机证据。本次未宣称完成UI原生操作或人工试玩。

2026-10-26用户已明确风格偏好：“再偏鸭科夫式立体感：更厚重、更有材质区分”。已增加04立体材质方向稿，保留03的简洁与原创人类旅人身份，强调厚度、较圆润体积、钢/布/皮/木/石/水材质差异。更新STYLE_GUIDE首版落地参考；概念修订累计3张，均CONCEPT_ONLY，用户尚未认可具体04图片，实际Unity接入和完整B10验收仍未完成。

不升级Unity/依赖，不启用CI，不操作真实存档或用户桌面。LFS本地fsck通过；剩余账户配额当前无可用账单权限，不用fsck推导远端剩余额度，最终以实际对象上传与验证记录交付。
