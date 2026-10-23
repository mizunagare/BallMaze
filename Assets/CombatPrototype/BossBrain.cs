using UnityEngine;

public enum BossAttack { Slam, Charge, Fan }

[RequireComponent(typeof(CombatEnemy))]
public class BossBrain : MonoBehaviour
{
    public bool Telegraphing { get; private set; }
    public BossAttack CurrentAttack { get; private set; }
    public bool Charging { get; private set; }
    public string AttackName => CurrentAttack == BossAttack.Slam ? "震地重击：离开红圈" : CurrentAttack == BossAttack.Charge ? "直线冲撞：向两侧躲避" : "扇形弹幕：避开橙色射线";
    CombatEnemy enemy;
    CharacterController controller;
    GameObject hints, circle, lane;
    GameObject[] rays;
    Material red, orange;
    Vector3 lockedOrigin, lockedDirection;
    float releaseAt, readyAt, chargeRemaining, verticalSpeed;
    int sequence;
    bool chargeHit;
    const float SlamRadius = 4.3f, ChargeLength = 11f;
    void Awake() { enemy = GetComponent<CombatEnemy>(); controller = GetComponent<CharacterController>(); }
    public void ResetBrain()
    {
        Telegraphing = Charging = false;
        chargeHit = false;
        sequence = 0;
        verticalSpeed = 0;
        readyAt = Time.time + 2;
        if (hints != null) hints.SetActive(false);
    }
    void Update()
    {
        if (enemy.archetype != EnemyArchetype.Boss || enemy.Health == null || enemy.Health.Dead || enemy.target == null || enemy.target.Health.Dead) { StopAttack(); return; }
        if (enemy.target.GameplayPaused) return;
        Vector3 movement = Vector3.zero;
        if (Telegraphing) {
            if (Time.time >= releaseAt) ResolveAttack();
        }
        else if (Charging) {
            AdvanceCharge(Time.deltaTime);
            return;
        }
        else if (Time.time >= readyAt) {
            BossAttack attack = (BossAttack)(sequence % 3);
            Vector3 offset = Vector3.ProjectOnPlane(enemy.target.transform.position - transform.position, Vector3.up);
            float desiredRange = attack == BossAttack.Slam ? 4f : 14f;
            if (offset.magnitude > desiredRange) {
                movement = enemy.Steer(offset.normalized * enemy.speed);
                transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(offset), 5 * Time.deltaTime);
            }
            else BeginAttack(attack);
        }
        MoveGrounded(movement);
    }
    void MoveGrounded(Vector3 movement)
    {
        if (!controller.enabled) return;
        if (controller.isGrounded && verticalSpeed < 0) verticalSpeed = -2;
        verticalSpeed += Physics.gravity.y * Time.deltaTime;
        controller.Move((movement + Vector3.up * verticalSpeed) * Time.deltaTime);
    }
    public bool BeginAttack(BossAttack attack)
    {
        if (enemy.Health.Dead || enemy.target == null || enemy.target.Health.Dead || enemy.target.GameplayPaused || Telegraphing || Charging) return false;
        EnsureHints();
        CurrentAttack = attack;
        lockedOrigin = transform.position;
        lockedDirection = Vector3.ProjectOnPlane(enemy.target.transform.position - lockedOrigin, Vector3.up).normalized;
        if (lockedDirection.sqrMagnitude < .1f) lockedDirection = transform.forward;
        transform.rotation = Quaternion.LookRotation(lockedDirection);
        hints.transform.SetPositionAndRotation(lockedOrigin, Quaternion.LookRotation(lockedDirection));
        hints.SetActive(true);
        circle.SetActive(attack == BossAttack.Slam);
        lane.SetActive(attack == BossAttack.Charge);
        foreach (var ray in rays) ray.SetActive(attack == BossAttack.Fan);
        releaseAt = Time.time + (attack == BossAttack.Charge ? 1.5f : attack == BossAttack.Slam ? 1.4f : 1.2f);
        Telegraphing = true;
        chargeHit = false;
        CombatFeedback.Find(this)?.BossWarning(transform.position);
        return true;
    }
    public void ResolveAttack()
    {
        if (!Telegraphing || enemy.Health.Dead || enemy.target == null || enemy.target.GameplayPaused) return;
        GetComponent<FantasyActorVisual>()?.Attack(CurrentAttack == BossAttack.Fan);
        CombatFeedback.Find(this)?.BossRelease(enemy, CurrentAttack);
        Telegraphing = false;
        if (CurrentAttack == BossAttack.Slam) {
            Vector3 delta = Vector3.ProjectOnPlane(enemy.target.transform.position - lockedOrigin, Vector3.up);
            if (delta.magnitude <= SlamRadius && ClearLine(lockedOrigin + Vector3.up, enemy.target.transform.position + Vector3.up)) enemy.target.Health.Damage(enemy.damage, enemy.target.transform.position + Vector3.up, enemy.target.transform.position - lockedOrigin);
        }
        else if (CurrentAttack == BossAttack.Fan) {
            for (int i = -3; i <= 3; i++) {
                Vector3 direction = Quaternion.Euler(0, i * 12, 0) * lockedDirection;
                Vector3 origin = transform.position + Vector3.up * 1.2f + direction * 1.2f;
                EnemyProjectile.Fire(enemy, origin, origin + direction * 20, Mathf.Round(enemy.damage * .7f), 7.5f, enemy.projectileMaterial);
            }
        }
        else {
            Charging = true;
            chargeRemaining = ChargeLength;
            return;
        }
        FinishAttack();
    }
    public void AdvanceCharge(float deltaTime)
    {
        if (!Charging || enemy.target == null || enemy.target.GameplayPaused || enemy.Health.Dead || deltaTime <= 0) return;
        Vector3 before = transform.position;
        float step = Mathf.Min(chargeRemaining, 13 * deltaTime);
        CollisionFlags flags = controller.Move(lockedDirection * step + Vector3.down * 2 * deltaTime);
        Vector3 after = transform.position;
        chargeRemaining -= Vector3.ProjectOnPlane(after - before, Vector3.up).magnitude;
        Vector3 line = Vector3.ProjectOnPlane(after - before, Vector3.up);
        Vector3 toward = Vector3.ProjectOnPlane(enemy.target.transform.position - before, Vector3.up);
        float t = line.sqrMagnitude > .0001f ? Mathf.Clamp01(Vector3.Dot(toward, line) / line.sqrMagnitude) : 0;
        Vector3 closest = before + line * t;
        if (!chargeHit && Vector3.ProjectOnPlane(enemy.target.transform.position - closest, Vector3.up).magnitude <= 1.5f
            && ClearLine(closest + Vector3.up, enemy.target.transform.position + Vector3.up)) {
            enemy.target.Health.Damage(Mathf.Round(enemy.damage * 1.2f), enemy.target.transform.position + Vector3.up, lockedDirection);
            chargeHit = true;
        }
        if (chargeRemaining < .1f || (flags & CollisionFlags.Sides) != 0 || step > .01f && line.magnitude < step * .15f) FinishAttack();
    }
    bool ClearLine(Vector3 a, Vector3 b)
    {
        Vector3 line = b - a;
        foreach (var hit in Physics.RaycastAll(a, line.normalized, line.magnitude, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.GetComponentInParent<CombatEnemy>() != null || hit.collider.GetComponentInParent<ThirdPersonHero>() != null) continue;
            return false;
        }
        return true;
    }
    void FinishAttack()
    {
        Telegraphing = Charging = false;
        if (hints != null) hints.SetActive(false);
        readyAt = Time.time + 2.2f;
        sequence++;
    }
    void StopAttack()
    {
        Telegraphing = Charging = false;
        if (hints != null) hints.SetActive(false);
    }
    void EnsureHints()
    {
        if (hints != null) return;
        red = new Material(Shader.Find("Universal Render Pipeline/Lit")) { color = new Color(1, .08f, .08f) };
        orange = new Material(red) { color = new Color(1, .55f, .05f) };
        hints = new GameObject("首领攻击预警");
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(hints, gameObject.scene);
        circle = Marker(PrimitiveType.Cylinder, new Vector3(0, .04f, 0), new Vector3(SlamRadius * 2, .025f, SlamRadius * 2), red);
        lane = Marker(PrimitiveType.Cube, new Vector3(0, .05f, ChargeLength / 2), new Vector3(3f, .05f, ChargeLength), orange);
        rays = new GameObject[7];
        for (int i = 0; i < rays.Length; i++) {
            var rotation = Quaternion.Euler(0, (i - 3) * 12, 0);
            rays[i] = Marker(PrimitiveType.Cube, rotation * new Vector3(0, .06f, 7), new Vector3(.2f, .04f, 14), orange);
            rays[i].transform.localRotation = rotation;
        }
    }
    GameObject Marker(PrimitiveType shape, Vector3 position, Vector3 scale, Material material)
    {
        var obj = GameObject.CreatePrimitive(shape);
        obj.GetComponent<Collider>().enabled = false;
        obj.transform.SetParent(hints.transform, false);
        obj.transform.localPosition = position;
        obj.transform.localScale = scale;
        obj.GetComponent<Renderer>().sharedMaterial = material;
        return obj;
    }
    void OnGUI()
    {
        if (enemy == null || enemy.archetype != EnemyArchetype.Boss || enemy.Health == null || enemy.Health.Dead) return;
        CombatChineseUI.Apply();
        float scale = Mathf.Clamp(Mathf.Min(Screen.height / 800f, Screen.width / 1100f), .5f, 2);
        var previous = GUI.matrix;
        GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
        float x = Screen.width / scale / 2 - 250;
        GUI.Box(new Rect(x, 20, 500, 70), "");
        GUI.Label(new Rect(x + 15, 25, 470, 28), $"{enemy.DisplayName}  {enemy.Health.Current:0}/{enemy.Health.maxHealth:0}", new GUIStyle(GUI.skin.label) { fontSize = 21, alignment = TextAnchor.MiddleCenter });
        GUI.Box(new Rect(x + 15, 60, 470 * (enemy.Health.Current / enemy.Health.maxHealth), 16), "");
        if (Telegraphing || Charging) GUI.Box(new Rect(x - 30, 100, 560, 40), Telegraphing ? $"{AttackName} · {Mathf.Max(0, releaseAt - Time.time):0.0}秒" : "正在冲撞！远离黄色区域");
        GUI.matrix = previous;
    }
    void OnDisable() { StopAttack(); }
    void OnDestroy()
    {
        if (hints != null) Destroy(hints);
        if (red != null) Destroy(red);
        if (orange != null) Destroy(orange);
    }
}

