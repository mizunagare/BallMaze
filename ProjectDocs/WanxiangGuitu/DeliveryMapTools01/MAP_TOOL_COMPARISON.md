# CP06-MAP-TOOLS：工具选型与验证边界

2026-11-04。研究分支research/cp06-map-tools，从产品07e47664101b1e4476b675e2b2163ae2ca9f512f独立建立；main仍72db192a527bd256e2ba18cd7ab334d8334051da。当前用户顺序：**先验证MapMagic 2免费基础版，Dungeon Architect只研究；不购买，不导入产品，不修改现有地图。** Gaia仅保留早期资料对照，不安排采购或导入。

## 证据口径

DOC_SUPPORTED=官方声明，非本机PASS；MEASURED=实际采集；NOT_RUN=未执行；BLOCKED=缺少继续条件；UNRESOLVED=证据不足。三款插件当前都没有本机可用安装包。Unity独立工程可启动不等于插件可用；不以自制Noise/房间或原有森林代替插件输出。

|项目|MapMagic 2免费基础版|Dungeon Architect Unity|Gaia Pro VS（资料对照）|
|---|---|---|---|
|当前优先级|先独立实测|官方功能/兼容性研究|暂不实测|
|主要职责|节点图生成Unity Terrain，高度/表面输出|有规则的房间、通道、钥匙/门、Boss房和模块拼接|地形、植被、生态及场景搭建|
|版本/大小（页面观测）|2.1.20；204.2MB|1.23.0；39.2MB|4.2.6；4.8GB|
|费用观测|基础版FREE；Objects等附加模块另售|约USD300/seat|约USD199/seat|
|URP|商店兼容表声明；精确17.6需测|兼容表声明，示例面向URP|兼容表声明|
|精确6000.6.5f1|NOT_RUN|NOT_RUN，不能把6.5声明直接套用|NOT_RUN|
|非开发Windows64|NOT_RUN|NOT_RUN|NOT_RUN|
|NavMesh与现有C#接入|Terrain完成回调后收集碰撞/烘焙的方案待验证|官方有运行时导航及C#接口，仍须适配当前权威布局/身份|需单独核对所选导出/运行时模式|
|室内/地下三维模块|不是免费高度场生成器的直接强项|首选候选；仍需拥有合法包后实测|不是本批室内结构的首选|
|美术质量/编辑效率/稳定性|NOT_RUN，无真人操作计时或插件画面|NOT_RUN，不拿宣传画面打分|NOT_RUN|

MapMagic基础版与收费Objects/Splines/Biomes必须分开：官方产品页把对象自动放置、道路河流及子图列为额外模块。免费Terrain验证不能被表述为免费提供完整森林Prefab散布或遗迹房间拼装。[MapMagic官方页面](https://assetstore.unity.com/packages/tools/terrain/mapmagic-2-165180)

Dungeon Architect的商店列出6000.5.3f1等兼容行、URP支持和1.23.0；不是本项目6000.6.5f1的逐补丁实测证明。其官方FAQ也明确Unity与Unreal产品分别有功能范围。[Unity商店](https://assetstore.unity.com/packages/tools/utilities/dungeon-architect-53895)、[厂商FAQ](https://dungeonarchitect.dev/faq/)

Gaia版本、体积及价格来自官方商店；这些是下载包信息，不是导入后内存或构建体积。[官方商店](https://assetstore.unity.com/packages/tools/terrain/gaia-pro-vs-terrain-trees-grass-water-for-unity-6-263149)

## 价格和许可

价格为研究当日页面观测，税/VAT/促销/地区可能变化，不是购买报价。MapMagic Bundle不能混同FREE基础版：搜索缓存小组件显示157.50，而实际Chrome官方相关商品区显示173.25，数据冲突保留，未作为当前可靠成交价。没有购买或加入任何收费购物车。

三者商店均指向标准Unity Asset Store EULA/席位类型；免费不等于开源或允许把源码/包公开上传GitHub。只发布自有验证代码、截图、配置说明与哈希，不发布插件原包或受限源码。官方条款2.3.2有Extension Asset按席位及设备的约束；使用人数、承包者与组织权利应按实际许可核对。[官方EULA](https://unity.com/legal/as-terms)

## 当前阻断

独立工程I:/WGCombat/MAPTOOLS-1104-A/Project，只配置Unity6000.6.5f1与URP17.6.0，没有产品Assets、ForestLayout、真实存档或产品场景。官方Package Manager服务仅请求FREE产品165180；实际返回“User is not logged in or user status invalid”，进程退出码3，acquisition.json=BLOCKED/Error。没有合法完成包、没有导入，也没有任何生成/Player/性能PASS。

浏览器读取官方FREE页成功；后续领取操作及再次读取超时，未确认资源已加入账号。未接受EULA，未提交支付。用户随后已明确确认登录并领取。Acquire3仍登录失败，Acquire4等待账户valid后进入DownloadRequested但180秒内未完成。已请求官方Package Manager完成下载后的包路径。不能把GitLab公开Beta仓库当作已领取的当前免费包，亦不使用转载下载。完整状态见Evidence/INDEX.md。
