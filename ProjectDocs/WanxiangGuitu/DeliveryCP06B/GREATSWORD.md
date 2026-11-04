# B2 巨剑

独立GreatswordMotor。普攻1.05s请求间隔，.45s启动、.5s恢复，2.6m球体候选＋前方65度半角＋Sight；105%攻击。崩山重斩.8s启动、3.1m/50度半角、170%，实际物理命中存活非Boss才添加.75s GuardBroken，不能清除已释放威胁。裂地冲击.8s启动、8m/s、8m距离、.3m碰撞半径，OverlapSphere+SphereCastAll，目标集合去重，墙体真实停止。旧武器/弹体/CombatAim不变。参数是初版，非平衡结论。

真实模型为原创三部分厚剑刃、横护手、长握柄。动作复用2H_Melee_Attack_Slice，加双手腕程序化旋转；不是完整新双手剑动画套装。左右手接触及整体观感需要人工核验。

B2Editor1 34 PASS；B2Player1 独立非开发 Player 34 PASS，实际exit=0。失败样本未删除。B2PureBuild单独冻结构建。
