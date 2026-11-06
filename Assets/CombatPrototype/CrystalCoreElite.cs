using UnityEngine;

// Candidate encounter configuration, scoped to the C2.2 actor.
public sealed class CrystalCoreElite : MonoBehaviour
{
    public enum CombatPhase { Shell, Warning, Exposed, Recovery }

    const float Reach = 3.7f;
    const float HalfAngle = 52f;
    const float WarningSeconds = .95f;
    const float ExposureSeconds = 2.2f;
    const float RecoverySeconds = 1.35f;
    const float PulseDamage = 23f;
    const float ShellMultiplier = .45f;
    const float ExposedMultiplier = 1.15f;

    CombatEnemy enemy;
    CavernEnergyHazard hazard;
    EnemyAttackSignal signal;
    Vector3 origin, direction;
    float remaining;
    bool paused;

    public CombatPhase Phase { get; private set; }
    public float Remaining => remaining;
    public float DamageMultiplier => Phase == CombatPhase.Exposed ? ExposedMultiplier : ShellMultiplier;
    public bool Active => enemy != null && isActiveAndEnabled && !enemy.Health.Dead;

    internal void Bind(CombatEnemy actor, CavernEnergyHazard energy)
    {
        enemy = actor;
        hazard = energy;
        var marker = new GameObject("晶核扇形预警");
        marker.transform.SetParent(transform, false);
        signal = marker.AddComponent<EnemyAttackSignal>();
    }

    internal Vector3 Tick(Vector3 offset, bool engaged)
    {
        paused = false;
        var hero = enemy.target;
        if (Phase != CombatPhase.Shell)
        {
            remaining -= Time.deltaTime;
            if (remaining > 0) return Vector3.zero;
            if (Phase == CombatPhase.Warning)
            {
                signal.Hide();
                var contact = Vector3.ProjectOnPlane(hero.transform.position - origin, Vector3.up);
                if (!Contested(hero) && contact.sqrMagnitude <= Reach * Reach &&
                    Mathf.Abs(hero.transform.position.y - origin.y) < 1.6f &&
                    Vector3.Angle(direction, contact) <= HalfAngle && enemy.HasSight())
                    hero.Health.Damage(PulseDamage, hero.transform.position + Vector3.up, contact.normalized);
                enemy.RememberReleasedThreat(Time.time);
                Set(CombatPhase.Exposed, ExposureSeconds);
            }
            else if (Phase == CombatPhase.Exposed) Set(CombatPhase.Recovery, RecoverySeconds);
            else Set(CombatPhase.Shell, 0);
            return Vector3.zero;
        }

        if (!engaged) return Vector3.zero;
        if (offset.sqrMagnitude > .001f)
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(offset), Time.deltaTime * 8);
        if (Contested(hero)) return Vector3.zero;
        if (offset.sqrMagnitude > Reach * Reach || !enemy.HasSight()) return offset.normalized * enemy.speed;
        if (!enemy.HasAttackSlot(Time.time + WarningSeconds)) return Vector3.zero;
        origin = transform.position;
        direction = offset.sqrMagnitude > .001f ? offset.normalized : transform.forward;
        transform.rotation = Quaternion.LookRotation(direction);
        signal.Show(origin, direction, Reach, HalfAngle, false, Vector3.zero);
        Set(CombatPhase.Warning, WarningSeconds);
        return Vector3.zero;
    }

    bool Contested(ThirdPersonHero hero) => hazard != null &&
        hazard.Phase != CavernEnergyHazard.CyclePhase.Recovery &&
        hazard.Area.Contains(hero.transform.position + Vector3.up * .65f);

    internal bool Threat(out float start, out float end)
    {
        start = end = Time.time + Mathf.Max(0, remaining);
        return Active && !paused && Phase == CombatPhase.Warning;
    }

    internal void Pause() => paused = true;

    internal void Cancel()
    {
        signal?.Hide();
        Set(CombatPhase.Shell, 0);
        paused = false;
    }

    void OnDisable() => Cancel();

    void Set(CombatPhase phase, float duration)
    {
        Phase = phase;
        remaining = duration;
    }

    void OnGUI()
    {
        var hero = enemy?.target;
        if (!Active || hero == null || hero.GameplayPaused || hero.Health.Dead ||
            (hero.transform.position - transform.position).sqrMagnitude > 81) return;
        var camera = Camera.main;
        if (camera == null) return;
        var screen = camera.WorldToScreenPoint(transform.position + Vector3.up * 2.4f);
        if (screen.z <= 0 || screen.x < 90 || screen.x > Screen.width - 90 ||
            screen.y < 36 || screen.y > Screen.height - 36) return;
        var hint = Phase == CombatPhase.Warning ? "晶壳 · 扇形冲击" :
            Phase == CombatPhase.Exposed ? "晶核暴露 · 反击" :
            Phase == CombatPhase.Recovery ? "晶壳正在恢复" : "晶壳防护";
        CombatChineseUI.Apply();
        GUI.Box(new Rect(screen.x - 90, Screen.height - screen.y, 180, 25), hint);
    }
}

