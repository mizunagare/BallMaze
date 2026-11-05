using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public enum RuinsBossState { Idle, Tracking, Telegraph, Recovery, Dead, Transition }
public enum RuinsBossAttack { StoneArc, RuneVolley, SealPulse, RiftSweep, EchoRing }

[Serializable]
public sealed class RuinsBossTrace
{
    public string stage, attack;
    public int phase, frame;
    public float time, before, after, damage, windup, recovery, gap, reach, width, innerRadius;
    public Vector3 origin, direction, aim;
}

[RequireComponent(typeof(CombatEnemy))]
public sealed class RuinsBossBrain : MonoBehaviour
{
    readonly struct AttackSpec
    {
        public readonly float Windup, Reach, Recovery, Damage, Width, InnerRadius;
        public AttackSpec(float windup, float reach, float recovery, float damage, float width = 0, float innerRadius = 0)
        {
            Windup = windup;
            Reach = reach;
            Recovery = recovery;
            Damage = damage;
            Width = width;
            InnerRadius = innerRadius;
        }
    }

    static readonly RuinsBossAttack[] EmpoweredRotation = {
        RuinsBossAttack.RiftSweep, RuinsBossAttack.EchoRing,
        RuinsBossAttack.RuneVolley, RuinsBossAttack.SealPulse
    };
    static readonly string[] Names = { "石刃横扫", "符文三连矢", "封印震波", "裂地直扫", "回响外环" };
    static readonly Color BaseWarning = new Color(1, .52f, .12f);
    static readonly Color EmpoweredWarning = new Color(1, .21f, .56f);
    static readonly Color TransitionWarning = new Color(.58f, .35f, 1);

    public RuinsBossState State { get; private set; }
    public RuinsBossAttack Attack { get; private set; }
    public int Phase => revised ? (empowered ? 2 : 1) : (BelowHalf ? 2 : 1);
    public int Releases { get; private set; }
    public float Remaining => Mathf.Max(0, until - Time.time);
    public Vector3 Origin { get; private set; }
    public Vector3 Direction { get; private set; }
    public Vector3 Aim { get; private set; }
    public event Action<RuinsBossTrace> Observed;

    CombatEnemy enemy;
    CharacterController controller;
    EncounterGuard guard;
    LineRenderer warning;
    Material warningMaterial;
    float until, readyAt, vertical;
    int sequence, attackPhase;
    bool initialized, revised, empowered;
    AttackSpec current;
    bool BelowHalf => enemy != null && enemy.Health.Current <= enemy.Health.maxHealth * .5f;

    static AttackSpec Spec(RuinsBossAttack attack, bool empowered)
    {
        switch (attack)
        {
            case RuinsBossAttack.StoneArc: return new AttackSpec(1, 3.5f, 1.2f, 16);
            case RuinsBossAttack.RuneVolley: return empowered ? new AttackSpec(.85f, 18, .65f, 19) : new AttackSpec(1.25f, 18, .9f, 12);
            case RuinsBossAttack.SealPulse: return empowered ? new AttackSpec(1.05f, 5, .7f, 23) : new AttackSpec(1.35f, 5, 1.5f, 14);
            case RuinsBossAttack.RiftSweep: return new AttackSpec(.9f, 7.5f, .65f, 25, width: 2.7f);
            case RuinsBossAttack.EchoRing: return new AttackSpec(1, 5.8f, .65f, 22, innerRadius: 2.2f);
            default: throw new ArgumentOutOfRangeException(nameof(attack));
        }
    }

    public static float Windup(RuinsBossAttack attack) => Spec(attack, false).Windup;
    public static float Reach(RuinsBossAttack attack) => Spec(attack, false).Reach;
    public static float Recovery(RuinsBossAttack attack) => Spec(attack, false).Recovery;

    float AttackGap(int phase) => phase == 1 ? .65f : revised ? .32f : .45f;

    public void Configure(bool useR1)
    {
        revised = useR1;
        enemy = GetComponent<CombatEnemy>();
        controller = GetComponent<CharacterController>();
        guard = GetComponent<EncounterGuard>();
        GetComponent<BossBrain>().enabled = false;
        enemy.name = "遗迹守护者 · 回响石像";
        enemy.Health.maxHealth = 320;
        enemy.Health.ResetHealth();
        enemy.speed = 2.1f;
        enemy.detectionRange = 15;
        enemy.experienceReward = 0;
        controller.enabled = false;
        controller.radius = .6f;
        controller.height = 2.5f;
        controller.center = Vector3.up * 1.25f;
        controller.enabled = true;

        var preview = new GameObject("守护者真实几何预警");
        preview.transform.SetParent(transform, false);
        warning = preview.AddComponent<LineRenderer>();
        warning.useWorldSpace = true;
        warning.widthMultiplier = .12f;
        warningMaterial = new Material(Shader.Find("Universal Render Pipeline/Unlit")) { color = BaseWarning };
        warning.sharedMaterial = warningMaterial;
        warning.enabled = false;
        readyAt = Time.time + 2;
        initialized = true;
    }

    void Emit(string stage, float before = 0, float after = 0, EnemyProjectile shot = null)
    {
        bool transition = stage.StartsWith("phase-transition", StringComparison.Ordinal);
        int phase = transition || attackPhase == 0 ? Phase : attackPhase;
        Observed?.Invoke(new RuinsBossTrace {
            stage = stage, attack = transition ? "" : Attack.ToString(), phase = phase,
            frame = Time.frameCount, time = Time.time, before = before, after = after,
            origin = shot != null ? shot.transform.position : Origin,
            direction = shot != null ? shot.Velocity : Direction, aim = Aim,
            damage = transition ? 0 : current.Damage, windup = transition ? .8f : current.Windup,
            reach = current.Reach, width = current.Width, innerRadius = current.InnerRadius,
            recovery = current.Recovery, gap = AttackGap(phase)
        });
    }

    void Update()
    {
        if (!initialized) return;
        if (enemy.Health.Dead)
        {
            if (State != RuinsBossState.Dead) { Cancel(); State = RuinsBossState.Dead; }
            return;
        }
        if (enemy.target == null || enemy.target.Health.Dead) { Cancel(); return; }
        if (enemy.target.GameplayPaused || Time.timeScale <= 0) return;
        if (State == RuinsBossState.Telegraph) { if (Time.time >= until) Release(); return; }
        if (State == RuinsBossState.Recovery && Time.time < until) { Move(Vector3.zero); return; }
        if (State == RuinsBossState.Transition)
        {
            if (Time.time < until) return;
            warning.enabled = false;
            State = RuinsBossState.Tracking;
            Emit("phase-transition-end");
        }

        if (guard.IdleOrReturn(controller, enemy.speed, ref vertical)) { State = RuinsBossState.Idle; return; }
        if (revised && !empowered && BelowHalf) { BeginTransition(); return; }
        State = RuinsBossState.Tracking;
        var offset = Vector3.ProjectOnPlane(enemy.target.transform.position - transform.position, Vector3.up);
        if (offset.sqrMagnitude > .01f)
            transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.LookRotation(offset), 90 * Time.deltaTime);

        var next = revised && empowered
            ? EmpoweredRotation[sequence % EmpoweredRotation.Length]
            : (RuinsBossAttack)(sequence % (Phase == 1 ? 2 : 3));
        if (Time.time >= readyAt && offset.magnitude <= Spec(next, revised && empowered).Reach && enemy.HasSight() && (Begin(next) || !revised))
            return;
        Move(offset.magnitude > 2.5f ? guard.Chase(offset.normalized * enemy.speed) : Vector3.zero);
    }

    void BeginTransition()
    {
        empowered = true;
        sequence = 0;
        Origin = transform.position;
        State = RuinsBossState.Transition;
        readyAt = until = Time.time + .8f;
        var points = new List<Vector3>();
        AppendArc(points, 2, 180);
        AppendArc(points, 4, 180);
        Show(points, TransitionWarning);
        CombatFeedback.Find(this)?.BossWarning(Origin);
        Emit("phase-transition-begin");
    }

    void Move(Vector3 direction)
    {
        if (controller.isGrounded && vertical < 0) vertical = -2;
        vertical += Physics.gravity.y * Time.deltaTime;
        controller.Move((direction + Vector3.up * vertical) * Time.deltaTime);
    }

    public bool Begin(RuinsBossAttack attack)
    {
        if (!initialized || !isActiveAndEnabled || enemy.Health.Dead || enemy.target == null ||
            enemy.target.Health.Dead || enemy.target.GameplayPaused || Time.timeScale <= 0 ||
            State == RuinsBossState.Telegraph || State == RuinsBossState.Transition || Time.time < readyAt)
            return false;
        if (attack < RuinsBossAttack.StoneArc || attack > RuinsBossAttack.EchoRing ||
            attack == RuinsBossAttack.SealPulse && Phase < 2 ||
            attack >= RuinsBossAttack.RiftSweep && !(revised && empowered))
            return false;

        var spec = Spec(attack, revised && empowered);
        float flight = attack == RuinsBossAttack.RuneVolley
            ? Vector3.Distance(transform.position, enemy.target.transform.position) / 8 : 0;
        if (!enemy.HasAttackSlot(Time.time + spec.Windup + flight, 0)) return false;

        Attack = attack;
        attackPhase = Phase;
        current = spec;
        Origin = transform.position;
        Aim = enemy.target.transform.position + Vector3.up;
        Direction = Vector3.ProjectOnPlane(Aim - Origin, Vector3.up).normalized;
        if (Direction.sqrMagnitude < .01f) Direction = transform.forward;
        State = RuinsBossState.Telegraph;
        until = Time.time + current.Windup;
        ShowWarning();
        Emit("begin");
        CombatFeedback.Find(this)?.BossWarning(Origin);
        return true;
    }

    void AppendArc(List<Vector3> points, float radius, float angle)
    {
        var forward = Direction.sqrMagnitude > .01f ? Direction : Vector3.forward;
        for (int i = 0; i <= 48; i++)
            points.Add(Origin + Vector3.up * .09f + Quaternion.Euler(0, Mathf.Lerp(-angle, angle, i / 48f), 0) * forward * radius);
    }

    void Show(List<Vector3> points, Color color)
    {
        warningMaterial.color = color;
        warning.positionCount = points.Count;
        warning.SetPositions(points.ToArray());
        warning.enabled = true;
    }

    Vector3 VolleyDirection(int index, Vector3 from) => Quaternion.Euler(0, index * 12, 0) * (Aim - from).normalized;

    void ShowWarning()
    {
        var points = new List<Vector3>();
        var floor = Origin + Vector3.up * .09f;
        switch (Attack)
        {
            case RuinsBossAttack.RuneVolley:
                var from = Origin + Vector3.up * 1.4f;
                for (int i = -1; i <= 1; i++)
                {
                    points.Add(from);
                    points.Add(from + VolleyDirection(i, from) * current.Reach);
                    points.Add(from);
                }
                break;
            case RuinsBossAttack.RiftSweep:
                var side = Vector3.Cross(Vector3.up, Direction) * (current.Width / 2);
                var end = floor + Direction * current.Reach;
                points.AddRange(new[] { floor - side, end - side, end + side, floor + side, floor - side });
                break;
            case RuinsBossAttack.EchoRing:
                // End both outlines on the same radial line; the brief radial seam
                // is part of the preview, not an additional damaging strip.
                AppendArc(points, current.Reach, 180);
                AppendArc(points, current.InnerRadius, 180);
                break;
            case RuinsBossAttack.StoneArc:
                points.Add(floor);
                AppendArc(points, current.Reach, 70);
                points.Add(floor);
                break;
            default:
                AppendArc(points, current.Reach, 180);
                break;
        }
        Show(points, revised && attackPhase == 2 ? EmpoweredWarning : BaseWarning);
    }

    bool AreaContact(ThirdPersonHero target)
    {
        Vector3 difference = target.transform.position - Origin;
        Vector3 horizontal = Vector3.ProjectOnPlane(difference, Vector3.up);
        if (Attack == RuinsBossAttack.RiftSweep)
        {
            float forward = Vector3.Dot(horizontal, Direction);
            float side = Vector3.Dot(horizontal, Vector3.Cross(Vector3.up, Direction));
            if (forward < 0 || forward > current.Reach || Mathf.Abs(side) > current.Width / 2)
                return false;
            var halfExtents = new Vector3(current.Width / 2, 1, current.Reach / 2);
            var center = Origin + Vector3.up + Direction * halfExtents.z;
            return Physics.OverlapBox(center, halfExtents, Quaternion.LookRotation(Direction), ~0,
                QueryTriggerInteraction.Ignore).Any(c => c.GetComponentInParent<ThirdPersonHero>() == target);
        }

        float radius = horizontal.magnitude;
        if (radius > current.Reach || radius < current.InnerRadius) return false;
        if (Attack == RuinsBossAttack.StoneArc && horizontal.sqrMagnitude >= .001f &&
            Vector3.Angle(Direction, horizontal) > 70) return false;
        if (Attack == RuinsBossAttack.EchoRing && Mathf.Abs(difference.y) > 1) return false;
        return Physics.OverlapSphere(Origin + Vector3.up * .7f, current.Reach, ~0,
            QueryTriggerInteraction.Ignore).Any(c => c.GetComponentInParent<ThirdPersonHero>() == target);
    }

    public bool Release()
    {
        if (State != RuinsBossState.Telegraph || Time.time < until || Time.timeScale <= 0 ||
            enemy.target == null || enemy.target.GameplayPaused || enemy.target.Health.Dead || enemy.Health.Dead)
            return false;

        warning.enabled = false;
        Emit("release");
        Releases++;
        bool volley = Attack == RuinsBossAttack.RuneVolley;
        GetComponent<FantasyActorVisual>()?.Attack(volley);
        if (volley)
        {
            Vector3 from = Origin + Vector3.up * 1.4f;
            for (int i = -1; i <= 1; i++)
            {
                var shot = EnemyProjectile.Fire(enemy, from, from + VolleyDirection(i, from), current.Damage, 8,
                    enemy.projectileMaterial, current.Reach);
                Emit("projectile-spawn", shot: shot);
            }
            enemy.RememberReleasedThreat(Time.time + Vector3.Distance(from, Aim) / 8, 0);
        }
        else
        {
            var target = enemy.target;
            var impact = target.transform.position + Vector3.up;
            float before = target.Health.Current;
            if (AreaContact(target) && EnemyProjectile.ClearWorldSegment(Origin + Vector3.up * 1.3f, impact))
            {
                target.Health.Damage(current.Damage, impact, Direction);
                Emit("collision-damage", before, target.Health.Current);
            }
            else Emit("physical-miss", before, target.Health.Current);
            CombatFeedback.Find(this)?.ProjectileImpact(Origin + Direction * 1.5f);
        }

        sequence++;
        State = RuinsBossState.Recovery;
        until = Time.time + current.Recovery;
        readyAt = until + AttackGap(revised ? attackPhase : Phase);
        return true;
    }

    void Cancel()
    {
        if (warning != null) warning.enabled = false;
        if (State != RuinsBossState.Dead) { State = RuinsBossState.Idle; readyAt = Time.time + 1; }
        Emit("cancel");
    }

    void OnDisable() => Cancel();
    void OnDestroy() { if (warningMaterial != null) Destroy(warningMaterial); }

    void OnGUI()
    {
        if (!initialized || enemy.Health.Dead || enemy.target == null || enemy.target.GameplayPaused ||
            Vector3.Distance(enemy.target.transform.position, transform.position) > 22) return;
        var old = CombatUI.Begin();
        var status = State == RuinsBossState.Transition ? "石像觉醒 · 紫色符纹不造成伤害"
            : State == RuinsBossState.Telegraph ? Names[(int)Attack] + $" · {Remaining:0.0}s" : "观察收招窗口";
        CombatUI.Panel(new Rect(CombatUI.Width / 2 - 210, 130, 420, 65));
        CombatUI.Text(new Rect(CombatUI.Width / 2 - 200, 136, 400, 52),
            $"回响石像 · 阶段{Phase}  {enemy.Health.Current:0}/{enemy.Health.maxHealth:0}\n" + status, 18, CombatUI.Gold);
        GUI.matrix = old;
    }
}
