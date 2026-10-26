# B10：卡通化体系与正式入口

实施中，尚未交付/推送，不认定复审通过。开工main本地与远端均b474765dc9c28aaf7d2d267bc0362f828f1902b0。用户ForestRuins.unity与ProjectSettings.asset保护，原始哈希见开工台账。

附件第8节在 `ProjectDocs/Wan` 处截断；用户已回复有后续、稍后粘贴。先做已明确P0与工程审计，不猜测缺失验收。

P0修复前实际隔离回归：B10Before/20261026-095151-6e594ed6，场景ForestRuins、CombatSession=1、HUD=1、没有Title，回归exit1且有实际PNG。源码还保留正式Player的-wanxiang-test-gameplay直入路径；B09旧证据也明确其为受控绕过。B09正式无绕过参数的六种启动图原先正常，所以没有证据把用户现场归因于登录服务或默认Player一定无菜单；项目源码搜索未发现游戏账号登录模块。

增量修复：Boot→Title→选择→Forest；Editor普通Play通过专用playModeStartScene走Boot，不写用户场景/ProjectSettings。明确隔离root+-executeMethod的Editor验证可直开测试场景，强制普通入口回归可取消该豁免。正式程序集剔除直入分支，旧直入参数在有效隔离根下忽略并仍显示菜单；缺失/不合法隔离配置仍先拒绝。CombatSession与保存入口另有授权门禁，避免误加载Forest时初始化HUD或存档。尚待本轮实际验证。

不升级Unity/依赖，不启用CI，不操作真实存档或用户桌面。LFS本地fsck通过；剩余账户配额当前无可用账单权限，不用fsck推导远端剩余额度，最终以实际对象上传与验证记录交付。
