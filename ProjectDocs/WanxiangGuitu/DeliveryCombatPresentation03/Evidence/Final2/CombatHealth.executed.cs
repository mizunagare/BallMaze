using UnityEngine;

// Exact health-transition observation only. Simulation time has frame precision;
// the callback never supplies a guessed attacker or changes health decisions.
public enum HealthObservationKind { Damage, Heal, Reset, Restore, Unload }
public struct HealthObservation {
    public HealthObservationKind kind;
    public float before, after, applied;
    public double activeTime;
    public int frame;
    public bool deathTransition;
}
public class CombatHealth : MonoBehaviour
{
    public float maxHealth = 100;
    public float Current { get; private set; }
    // Transient observation only: actual applied HP loss, excluding healing and
    // overkill. Not serialized, restored, or used by damage/settlement rules.
    public float TotalDamageTaken { get; private set; }
    public bool Dead => Current <= 0;
    public event System.Action<HealthObservation> Observed;
    HealthObservation Sample(HealthObservationKind kind, float before) => new HealthObservation {
        kind = kind, before = before, after = Current,
        applied = kind == HealthObservationKind.Damage ? before - Current : 0,
        activeTime = Time.timeAsDouble, frame = Time.frameCount,
        deathTransition = kind == HealthObservationKind.Damage && before > 0 && Current <= 0
    };
    void Notify(HealthObservation sample) {
        if (Observed == null) return;
        foreach (System.Action<HealthObservation> observer in Observed.GetInvocationList()) {
            try { observer(sample); }
            catch (System.Exception error) {
                // Only a new observation subscriber is isolated. Existing product
                // damage/feedback exceptions retain their original propagation.
                Debug.LogException(new System.InvalidOperationException("Health observation subscriber failed after " + sample.kind, error));
            }
        }
    }
    void OnDestroy() { Notify(Sample(HealthObservationKind.Unload, Current)); }
    Renderer[] visuals;
    MaterialPropertyBlock block;
    float flashUntil;
    int visualTint=-1;
    void Awake() { ResetHealth(); RefreshVisuals(); block = new MaterialPropertyBlock(); }
    public void RefreshVisuals() { visuals = GetComponentsInChildren<Renderer>(true); visualTint=-1; }
    public void ResetHealth() { float before = Current; Current = maxHealth; flashUntil = 0; Notify(Sample(HealthObservationKind.Reset, before)); }
    public void RestoreHealth(float value) { float before = Current; Current = Mathf.Clamp(value, 0, maxHealth); flashUntil = 0; Notify(Sample(HealthObservationKind.Restore, before)); }
    public void Heal(float amount) { if (!Dead && amount > 0) { float before = Current; Current = Mathf.Min(maxHealth, Current + amount); Notify(Sample(HealthObservationKind.Heal, before)); } }
    public void Damage(float amount)
    {
        Damage(amount, transform.position + Vector3.up, -transform.forward);
    }
    public void Damage(float amount, Vector3 hitPoint, Vector3 direction)
    {
        if (Dead || amount <= 0 || float.IsNaN(amount) || float.IsInfinity(amount)) return;
        var hero = GetComponent<ThirdPersonHero>();
        if(hero!=null&&AdventureFlow.Find(hero)!=null&&AdventureFlow.Find(hero).BlockCombat)return;
        if (hero != null && hero.Dodge != null && hero.Dodge.IsInvulnerable) return;
        float defense = hero != null ? hero.Defense : 0;
        float before = Current;
        Current = Mathf.Max(0, Current - (hero != null ? ArmorMitigation.Incoming(amount, defense) : Mathf.Max(1, amount)));
        TotalDamageTaken += before - Current;
        var observation = Sample(HealthObservationKind.Damage, before);
        if(hero!=null)AdventureFlow.Find(hero)?.OnHeroDamaged();
        GetComponent<EncounterGuard>()?.OnDamaged();
        GetComponent<ForestBossBrain>()?.OnDamaged();
        flashUntil = Time.time + .15f;
        GetComponent<FantasyActorVisual>()?.Hurt();
        CombatFeedback.Find(this)?.Hit(this, before - Current, hitPoint, direction, Dead);
        Notify(observation);
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


