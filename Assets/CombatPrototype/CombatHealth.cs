using UnityEngine;

public class CombatHealth : MonoBehaviour
{
    public float maxHealth = 100;
    public float Current { get; private set; }
    public bool Dead => Current <= 0;
    Renderer[] visuals;
    MaterialPropertyBlock block;
    float flashUntil;
    int visualTint=-1;
    void Awake() { ResetHealth(); RefreshVisuals(); block = new MaterialPropertyBlock(); }
    public void RefreshVisuals() { visuals = GetComponentsInChildren<Renderer>(true); visualTint=-1; }
    public void ResetHealth() { Current = maxHealth; flashUntil = 0; }
    public void RestoreHealth(float value) { Current = Mathf.Clamp(value, 0, maxHealth); flashUntil = 0; }
    public void Heal(float amount) { if (!Dead && amount > 0) Current = Mathf.Min(maxHealth, Current + amount); }
    public void Damage(float amount)
    {
        Damage(amount, transform.position + Vector3.up, -transform.forward);
    }
    public void Damage(float amount, Vector3 hitPoint, Vector3 direction)
    {
        if (Dead || amount <= 0) return;
        var hero = GetComponent<ThirdPersonHero>();
        if(hero!=null&&AdventureFlow.Find(hero)!=null&&AdventureFlow.Find(hero).BlockCombat)return;
        if (hero != null && hero.Dodge != null && hero.Dodge.IsInvulnerable) return;
        float defense = hero != null ? hero.Defense : 0;
        float before = Current;
        Current = Mathf.Max(0, Current - Mathf.Max(1, amount - defense));
        if(hero!=null)AdventureFlow.Find(hero)?.OnHeroDamaged();
        GetComponent<EncounterGuard>()?.OnDamaged();
        GetComponent<ForestBossBrain>()?.OnDamaged();
        flashUntil = Time.time + .15f;
        GetComponent<FantasyActorVisual>()?.Hurt();
        CombatFeedback.Find(this)?.Hit(this, before - Current, hitPoint, direction, Dead);
    }
    void Update()
    {
        var hero = GetComponent<ThirdPersonHero>();
        int tint=hero!=null&&hero.Dodge!=null&&hero.Dodge.IsInvulnerable?2:Time.time<flashUntil?1:0;
        if(tint==visualTint)return;
        visualTint=tint;
        foreach (var visual in visuals) {
            if (visual == null) continue;
            block.Clear();
            if (tint==2) block.SetColor("_BaseColor", new Color(.35f, 1.4f, 2));
            else if (tint==1) block.SetColor("_BaseColor", hero != null ? new Color(2, .28f, .2f) : new Color(2, 1.45f, .45f));
            visual.SetPropertyBlock(block);
        }
    }
}


