using UnityEngine;

[RequireComponent(typeof(ThirdPersonHero))]
public class HeroDodge : MonoBehaviour
{
    [Min(.1f), InspectorName("翻滚持续秒数")] public float duration = .42f;
    [Min(0), InspectorName("翻滚距离（米）")] public float distance = 4.2f;
    [Min(0), InspectorName("起手无敌秒数")] public float invulnerability = .24f;
    [Min(.1f), InspectorName("翻滚冷却（从起手计算）")] public float cooldown = 1.5f;
    ThirdPersonHero hero;
    float startedAt, endsAt, invulnerableUntil, readyAt, activeDuration, activeSpeed;
    public Vector3 Direction { get; private set; }
    public bool IsRolling => hero != null && !hero.Health.Dead && Time.time < endsAt;
    public bool IsInvulnerable => IsRolling && Time.time < invulnerableUntil;
    public float CooldownRemaining => Mathf.Max(0, readyAt - Time.time);
    public float Progress => activeDuration > 0 ? Mathf.Clamp01((Time.time - startedAt) / activeDuration) : 1;
    void Awake() { hero = GetComponent<ThirdPersonHero>(); }
    public bool TryDodge(Vector3 movementDirection)
    {
        if (hero == null || hero.Health.Dead || hero.GameplayPaused || Time.timeScale <= 0 || IsRolling || CooldownRemaining > 0
            || hero.Inventory != null && hero.Inventory.ClosedFrame == Time.frameCount) return false;
        var controller = GetComponent<CharacterController>();
        if (!controller.enabled) return false;
        Direction = Vector3.ProjectOnPlane(movementDirection, Vector3.up);
        if (Direction.sqrMagnitude < .01f) Direction = Vector3.ProjectOnPlane(transform.forward, Vector3.up);
        Direction = Direction.normalized;
        startedAt = Time.time; activeDuration = Mathf.Max(.1f, duration);
        endsAt = startedAt + activeDuration;
        invulnerableUntil = startedAt + Mathf.Clamp(invulnerability, 0, activeDuration);
        readyAt = startedAt + Mathf.Max(activeDuration, cooldown);
        activeSpeed = Mathf.Max(0, distance) / activeDuration;
        transform.rotation = Quaternion.LookRotation(Direction);
        CombatFeedback.Find(this)?.Dodge(this);
        return true;
    }
    // Integrate only the part of the current frame inside the roll; speed is independent of frame rate.
    public Vector3 FrameDisplacement(float deltaTime)
    {
        if (hero == null || hero.Health.Dead || hero.GameplayPaused || Time.timeScale <= 0 || deltaTime <= 0) return Vector3.zero;
        float frameStart = Mathf.Max(startedAt, Time.time - deltaTime);
        float overlap = Mathf.Max(0, Mathf.Min(Time.time, endsAt) - frameStart);
        return Direction * (activeSpeed * overlap);
    }
    public void ResetDodge() { startedAt = endsAt = invulnerableUntil = readyAt = activeDuration = activeSpeed = 0; Direction = Vector3.zero; }
    public void RestoreCooldown(float remaining) { ResetDodge(); readyAt = Time.time + Mathf.Max(0, remaining); }
}
