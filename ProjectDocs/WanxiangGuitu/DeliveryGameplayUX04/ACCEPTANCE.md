# GAMEPLAY-UX04 验收表

结论：四项定向修复有本轮证据；整体验收UNRESOLVED，等待独立复审。明细[summary.json](Evidence/Summary/summary.json)共856条PASS，零当前断言FAIL；所有旧尝试的FAIL独立保留，不合并为全绿。

|项目|状态|证据/边界|
|---|---|---|
|低矮资源范围误导负例|PASS|Before03候选/顶点/HP；不是只改文案或扩大半径|
|剑枪距离/角度/高度/墙/多Collider|PASS|Shared07/matrix-run.json及Summary/range-matrix.csv，120样本|
|四武器/品质/时序/生命周期|PASS|Final2品质15、范围34、TimingDomain-Store188；受控规则，非手感|
|白剑重复目标保存、完成与教程|PASS|目标准备2、矩阵466内实际制造、营地恢复3、在途恢复2|
|缺料/未解锁/空间/保存/已发布回调|PASS|本轮重跑UX02 60项及Shared07事务负例；未声称穷举全部回调组合|
|配方/仓库独立滚动/筛选/缩放|PASS|Scroll08 17项，1280/1920受控截图|
|真实UI制作按钮|PASS|Final3/UI/result.json，10项受控回调；非原生鼠标|
|抓取点旋转/精确偏移/统一放置合同|PASS|共享GrabPoint、四转回原点；数学/受控层|
|整理确定性、幂等、保存失败回滚|PASS|Shared07与Scroll08；仅营地背包/仓库，不重排装备盘|
|整理所有稀有无解形状穷举|NOT_RUN|保留纯预排失败拒绝分支；非最优装箱承诺|
|双击真实存取/单击/重复/失败|PASS|Shared07受控PointerEventData调用真实事务；非原生点击验收|
|正常AI完整搜打撤制造再出征|PASS|Final3/Normal-Gather三进程exit0、无超时|
|旧正常AI phase31停滞原因|UNRESOLVED|Normal-Gather/Resume.log.gz与process-result-Resume.json；后续成功不关闭|
|Editor D3D12 GPU fatal|UNRESOLVED|Final2/CombatTiming/Unity.log.gz，exit-1073740771，无强杀|
|非开发发行构建|PASS|Final3/Build，0E96W；发行原生操作未执行|
|发行排除验收驱动|PASS|Final3/Build/release-inspection.json，PE元数据|
|用户五文件保护|PASS|Bindings/protection-check.json实际前后SHA256|
|历史交付保护|PASS|开工Git对象与工作区diff；不冒称缺失的全量原始工作区哈希|
|产品/副本/构建追溯|PASS|14产品输入匹配；1387构建输入的一项后续Editor夹具差异明确保留|
|原生U16、拖放手感和发行原生UI|NOT_RUN|不能用回调/截图/Editor AI替代|
|独立人工与性能|NOT_RUN|没有独立人员或采样，不能以自动化结果代替|
|历史UNKNOWN/青色帧/Search/JobTempAlloc/C15|UNRESOLVED|沿用历史开放边界，未宣称修复|
|弓/法杖/追踪提案|PASS|仅文档，无新增战斗机制|

各层按实际输入/版本解释，不能把这些PASS互相替代或将推送视为复审认可。完成后暂停。
