# CP05-A 设计交付验收

|内容|状态|证据与边界|
|---|---|---|
|远端/分支/基准关系|PASS（只读核对）|main72db、CP04-B cc9独立，不合并|
|相机/输入/攻击/表现/武器源码审计|PASS（源码层）|Evidence/source-audit.json，10个文件SHA及行号|
|历史相机/英雄/目标/枪口空间复核|PASS（历史证据读取）|Evidence/spatial-analysis.json及原jsonl；不是本轮实测|
|自由镜头＋软锁定＋近战面向设计|设计提案|CAMERA_DESIGN/TARGET_ASSIST/MELEE_COMBAT_DESIGN|
|真实弹道与武器差异设计|设计提案|RANGED_COMBAT_DESIGN/WEAPON_BEHAVIOR|
|滞回、主动输入、无合法目标/遮挡退回|设计提案|TARGET_ASSIST_DESIGN|
|128工况及补充可视化矩阵|设计提案|PROTOTYPE_PLAN；没有执行结果|
|新Unity原型/Editor/Player/性能测量|NOT_RUN|本轮只读，不声称运行通过|
|角色准星遮挡、植被占用、自然切换的新现场复现|NOT_RUN|源码不能替代当前实机空间采样|
|物理键鼠/独立人工/最终手感|NOT_RUN|不能以历史自动化或图示替代|
|保护文件/用户改动|PASS（哈希）|Evidence/protection.json，2329项不变|

历史引擎问题、近距法杖旧失败、外部诊断路径等不在本轮关闭；保留既有UNRESOLVED。软件设计完成不等于产品或玩法验收PASS。等待独立设计复审及逐文件实施授权。
