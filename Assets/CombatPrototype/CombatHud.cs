using UnityEngine;

public static class CombatHud
{
    public static void Draw(CombatSession session)
    {
        var hero = session.hero;
        var bag = hero.Inventory; if(bag.IsOpen)return;
        var p = hero.Progression;
        var previous = CombatUI.Begin();
        float width = CombatUI.Width, height = CombatUI.Height;
        bool choosing = p != null && p.IsChoosing;
        if (!bag.IsOpen && !choosing) {
            CombatUI.Panel(new Rect(20, 20, 300, 152));
            CombatUI.Text(new Rect(35, 28, 260, 30), $"{hero.GetComponent<AdventureCombat>().ClassName} · 等级 {p.Level}", 22, CombatUI.Ink, true);
            CombatUI.Bar(new Rect(36, 66, 268, 24), hero.Health.Current / hero.Health.maxHealth, CombatUI.Health, $"生命 {hero.Health.Current:0} / {hero.Health.maxHealth:0}");
            CombatUI.Text(new Rect(36, 96, 268, 24), $"经验 {p.Experience} / {p.RequiredExperience}", 16, CombatUI.Muted);
            CombatUI.Bar(new Rect(36, 123, 268, 8), (float)p.Experience / p.RequiredExperience, CombatUI.Experience);
            CombatUI.Text(new Rect(36, 140, 270, 27), $"攻击 {hero.AttackPower:0}    防御 {hero.Defense:0}    C 查看角色", 16);
            bool forest=session.GetComponent<ForestRegionRuntime>()?.Active==true;
            int kills = 0;
            foreach (var enemy in session.enemies) if (enemy.Health.Dead) kills++;
            CombatUI.Panel(new Rect(width - 300, 20, 280, 106));
            CombatUI.Text(new Rect(width - 282, 29, 245, 30), forest?"森林自由探索":$"第 {session.Wave} 波{(session.Wave % 5 == 0 ? " · 首领战" : "")}", 23, CombatUI.Gold, true);
            CombatUI.Text(new Rect(width - 282, 65, 245, 28), forest?$"击败 {kills} / {session.enemies.Length} · 可绕行":session.WaitingForNextWave ? $"下一波 {Mathf.CeilToInt(session.NextWaveRemaining)} 秒后" : $"击杀 {kills} / {session.enemies.Length}", 20);
            CombatUI.Text(new Rect(width - 282, 96, 250, 25), forest?"随时寻找出口 · 无需清场":session.WaitingForNextWave ? "Tab 整理暂停 · N 提前开始" : "战斗进行中 · 清场后自动刷新", 15, CombatUI.Muted);
            if (session.Saves != null && session.Saves.IsInitialized)
                CombatUI.Text(new Rect(width - 295, 132, 280, 28), session.Flow!=null&&session.Flow.Enabled?"F5 检查点 · 退出后自动继续 · R 放弃…":"F5 保存 · R 新开局", 15, CombatUI.Muted);
            CombatUI.Text(new Rect(20, height - 96, 340, 78), "WASD 移动 · Shift 跑步 · 左键攻击\n空格 翻滚 · F 武器技能 · E 互动\nH 撤离装置 · Esc 释放鼠标", 16, CombatUI.Muted);
            if (hero.Dodge != null && !hero.Health.Dead) {
                string status = hero.Dodge.IsInvulnerable ? "翻滚中 · 无敌" : hero.Dodge.IsRolling ? "翻滚中 · 小心后摇" : hero.Dodge.CooldownRemaining > 0 ? $"冷却 {hero.Dodge.CooldownRemaining:0.0} 秒" : "就绪";
                CombatUI.Panel(new Rect(width / 2 - 160, height - 133, 320, 33));
                CombatUI.Text(new Rect(width / 2 - 150, height - 129, 300, 28), "空格  翻滚闪避 · " + status, 17, hero.Dodge.IsInvulnerable ? CombatUI.Experience : CombatUI.Ink);
            }
            if (hero.Health.Dead) {
                CombatUI.Panel(new Rect(width / 2 - 250, height / 2 - 40, 500, 80));
                CombatUI.Text(new Rect(width / 2 - 225, height / 2 - 20, 450, 45), "已倒下 · 请完成结算", 25, CombatUI.Gold);
            }
        }
        bool enabled = !choosing && !hero.Health.Dead;
        float barX = width / 2 - 230, barY = height - 90;
        CombatUI.Panel(new Rect(barX, barY, 460, 70));
        string potion = bag.PotionOnQuickbar ? $"Q  药水 ×{bag.HealthPotionCount}" : "Q  空道具栏";
        if (bag.PotionCooldownRemaining > 0 && bag.PotionOnQuickbar) potion = $"Q  冷却 {bag.PotionCooldownRemaining:0.0}秒";
        if (CombatUI.Button(new Rect(barX + 12, barY + 13, 166, 43), potion, enabled)) {
            if (!bag.PotionOnQuickbar) bag.OpenPage(PlayerInventory.Page.Items);
            else if (bag.HealthPotionCount == 0) bag.OpenPage(PlayerInventory.Page.Crafting);
            else bag.UseHealthPotion();
        }
        if (CombatUI.Button(new Rect(barX + 190, barY + 13, 125, 43), "Tab  背包", enabled)) {
            if (bag.IsOpen) bag.SetOpen(false); else bag.OpenPage(PlayerInventory.Page.Items);
        }
        if (CombatUI.Button(new Rect(barX + 327, barY + 13, 121, 43), "C  角色", enabled)) bag.OpenPage(PlayerInventory.Page.Character);
        GUI.matrix = previous;
    }
}



