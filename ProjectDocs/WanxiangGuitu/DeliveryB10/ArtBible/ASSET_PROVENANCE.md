# B10 资产来源与用途

| 集合 | 来源 | 用途和权利口径 |
| --- | --- | --- |
| 原始概念 01～09 | 用户提供 D:/WanxiangArtSource/万象归途_概念设计板.zip | 字节级副本，仅参考；不自行断言 CC0、第三方权利已转移或模型可提取 |
| 修订 02、03、04 | 本次内置 imagegen，根据用户简化及厚重立体/材质区分意见与前版参考生成 | AI 辅助 CONCEPT_ONLY；不是手绘、不是实机、不是正式资产许可验收 |
| 现有 KayKit 角色与骨骼动画 | 项目既有 FantasyArt 许可证 | 沿用已记录许可；新概念不改变已有资源来源，不冒称本轮原创建模 |
| 后续实际制作资源 | 必须逐项记录真实 Unity 路径、哈希、导入/使用与证据 | 尚未完成的不得标 VERIFIED |

原包 SHA256：`75333a5660b5ece0d7cd9224afa0c4fe70b812293790efa9d0767f9f4fa3addf`。原始文件逐项大小与 SHA256 见 Concepts/IMPORT_MANIFEST.json；ZIP 文件名编码纠正与首次失败见 IMPORT_ATTEMPTS.json，未改图像载荷。

修订图片、提示词与来源图路径见 Concepts/Revisions/GENERATION_MANIFEST.json。风格参考只记录官方入口，不复制第三方游戏画面到发行资源，不把参考游戏权利混记为本项目许可。

## 猫族实际资源

CatWorldArt、CatWorldProps、CatUI、CatItemGraphic及CatIconStudio为本项目本轮原创代码与几何定义；CatWorldBake由这些定义生成Mesh、Material、Prefab和透明PNG，未从概念板裁图。来源不是第三方资源下载，也不冒称用户已授予这些新代码CC0。依项目代码许可管理；旧KayKit/Kenney及game-icons许可各自保留。

实际演员沿用现有KayKit骨架及CC0动作剪辑。刚性猫族部件跟随旧骨骼，不是新制作的柔性蒙皮。缺少新猫族面部和尾巴动画的事实见CHARACTER_SPEC。NPC静态，武器与物品图标均由原创实体模型摄影。

黑猫材质方向05为内置imagegen生成的新增设计参考，原样保留输出与提示词；CONCEPT_ONLY，不是Unity渲染或手工美术，不改变原始9图的来源或许可。不将概念图中的毛发、皮革纹理、植物细节称为已经接入的贴图。

全量实际文件字节数与SHA256由Build-AssetInventory.py写入ASSET_INVENTORY.json，最终验收应在证据齐备后另行引用，禁止从文件存在直接推导VERIFIED。

## B10-R1 用户主视觉与实际制作（当前优先级）

最新输入 `Concepts/Revisions/用户主要视觉参考_黑猫猫族世界.png` 为用户提供的主要概念依据，3170953 bytes，SHA256 `ac7cb7a365e43c8af09d4212916b0e56327590b849d0b129129b51b00a5eb074`。原始输入及仓库副本哈希见 `black-cat-primary-reference.json`。三份猫族文档及本轮任务书原文在 UserBriefs；不把用户提供等同第三方权利已验证。

新版圆润体积、服饰肩带、铜扣、职业工具及Boss肩铠/鬃鳍均由原创几何配方制作。不是AI概念板裁图、不是新下载角色包、不宣称完整软蒙皮。Mesh/Material/Prefab/PNG的文件路径、大小、SHA256和Git文本归一化SHA见ASSET_INVENTORY.json；Runtime引用与实际截图另列，文件存在不等于验收。

新增草药、食用蘑菇、布料、卷轴和任务卷图标/道具只制作资源，现有六种材料经济没有对应业务定义，状态为CREATED。没有自动给予玩家、伪造拾取或新增制作材料。独立角色宣传立绘仍CONCEPT_ONLY。
