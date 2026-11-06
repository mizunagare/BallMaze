using UnityEngine;

public sealed class CavernEnergyHazard : MonoBehaviour
{
    public enum CyclePhase { Recovery, Warning, Active }
    const float RecoverySeconds = 3f;
    const float WarningSeconds = 2f;
    const float ActiveSeconds = 1.25f;
    const float Damage = 18f;
    [SerializeField] BoxCollider volume;
    [SerializeField] Renderer field;
    [SerializeField] Material recoveryMaterial, warningMaterial, activeMaterial;
    CombatSession session;
    float elapsed;
    bool contacted;

    public string StableId => CrystalCavernLayout.HazardId;
    public CyclePhase Phase { get; private set; }
    public Bounds Area => volume.bounds;
    public float Remaining => Duration - elapsed;
    float Duration => Phase == CyclePhase.Recovery ? RecoverySeconds :
        Phase == CyclePhase.Warning ? WarningSeconds : ActiveSeconds;

    public void Bind(CombatSession owner)
    {
        session = owner;
        ResetCycle();
    }

    void ResetCycle()
    {
        Phase = CyclePhase.Recovery;
        elapsed = 0;
        contacted = false;
        if (field != null) field.sharedMaterial = recoveryMaterial;
    }

    void OnDisable()
    {
        ResetCycle();
        session = null;
    }

    void Update()
    {
        var hero = session?.hero;
        if (hero == null || hero.Health.Dead || hero.GameplayPaused || session.Flow.BlockCombat || Time.timeScale <= 0 ||
            session.Flow.ActiveRun?.region != CrystalCavernLayout.Region) return;

        elapsed += Time.deltaTime;
        if (elapsed >= Duration)
        {
            elapsed = 0;
            Phase = Phase == CyclePhase.Recovery ? CyclePhase.Warning :
                Phase == CyclePhase.Warning ? CyclePhase.Active : CyclePhase.Recovery;
            field.sharedMaterial = Phase == CyclePhase.Recovery ? recoveryMaterial :
                Phase == CyclePhase.Warning ? warningMaterial : activeMaterial;
            contacted = false;
        }
        if (Phase != CyclePhase.Active || contacted || !volume.enabled) return;
        var center = hero.transform.position + Vector3.up * .65f;
        if (!volume.bounds.Contains(center)) return;
        var origin = volume.bounds.center;
        var direction = center - origin;
        if (direction.sqrMagnitude > .0001f && Physics.Raycast(origin, direction.normalized, out var hit,
                direction.magnitude, Physics.DefaultRaycastLayers, QueryTriggerInteraction.Ignore) &&
            hit.collider.GetComponentInParent<ThirdPersonHero>() != hero) return;
        contacted = true;
        hero.Health.Damage(Damage, center, direction.normalized);
    }

    void OnGUI()
    {
        var hero = session?.hero;
        if (hero == null || hero.Health.Dead || hero.GameplayPaused || session.Flow.BlockCombat ||
            (hero.transform.position - transform.position).sqrMagnitude > 100) return;
        var previous = CombatUI.Begin();
        var label = Phase == CyclePhase.Recovery ? "恢复 · 可通行" :
            Phase == CyclePhase.Warning ? "预警 · 离开琥珀区域" : "放电 · 避开红色区域";
        var box = new Rect(CombatUI.Width / 2 - 150, 95, 300, 34);
        CombatUI.Panel(box);
        CombatUI.Text(box, $"能量通道  {label}  {Remaining:0.0}s", 16, CombatUI.Gold, true);
        GUI.matrix = previous;
    }
}
