# UI-01 图标与来源

没有外部下载、付费插件或依赖升级；没有用 Unicode Emoji 充当图标。

| 用途 | key / 来源 | 许可 |
| --- | --- | --- |
| 四主/副武器 | sword / spear / staff / bow，复用 AdventureIcons | Lorc / Delapouite，Game-icons.net，CC BY 3.0 |
| 材料与掉落 | wood / stone / ore / hide / crystal / core，复用物品定义 iconKey | 同上；原作者逐项页面见工程原许可文件 |
| 药水 | potion | Lorc / drink-me，CC BY 3.0 |
| 宝箱、修复、出口 | chest / repair / exit | 本批项目自制几何图标，CC0-1.0 |
| 路线、帮助、补给 | route / help / supply | 本批项目自制几何图标，CC0-1.0 |
| 保存、错误、翻滚 | save / error / dodge | 本批项目自制几何图标，CC0-1.0 |
| 四武器主动技能 | skill_sword / skill_spear / skill_staff / skill_bow | 本批项目自制几何图标，CC0-1.0 |

自制13张图以透明PNG存放在 Assets/CombatPrototype/Resources/AdventureIcons，采用线条、箭头、工具及轮廓图形，未临摹外部图形。CC0仅适用于这13个新文件，不改变复用资源的CC BY署名或整个工程的许可。

原素材署名与许可保留于 Assets/CombatPrototype/装备素材来源与许可.txt；模型许可未动。已有 Game-icons.net 图片版权不归本项目所有。

HudIconCatalog 缓存 Texture→Sprite；缺失时仍有动作/物品短名。HUD自有Sprite（含填充用白色Sprite）在销毁时释放，不销毁Resources所有的原纹理。连续更新不会每格重复Resources加载。状态改变时替换图标；V切武器不拥有或重置任何战斗冷却。
