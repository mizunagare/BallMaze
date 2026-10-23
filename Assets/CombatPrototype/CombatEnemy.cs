using UnityEngine;

public enum EnemyArchetype { Melee, Ranged, Elite, Boss }

[RequireComponent(typeof(CharacterController), typeof(CombatHealth))]
public class CombatEnemy : MonoBehaviour
{
    public string entityId;
    public ThirdPersonHero target;
    public EnemyArchetype archetype;
    public float speed = 2.5f, detectionRange = 25, attackRange = 1.7f, damage = 12;
    public float windup = .65f, attackInterval = 1.5f;
    public Transform warningRing;
    public int hideMin = 1, hideMax = 3, crystalAmount = 1;
    [InspectorName("击杀经验值")] public int experienceReward = 25;
    public float projectileSpeed = 8, preferredDistance = 7;
    public Material projectileMaterial;
    bool lootDropped;
    CharacterController controller;
    CombatHealth health;
    Vector3 spawn, lockedAim;
    Quaternion rotation;
    float verticalSpeed, strikeAt = -1, nextAttack;
    public CombatHealth Health => health;
    public bool WindingUp => strikeAt >= 0;
    public string DisplayName => archetype == EnemyArchetype.Boss ? "骸骨领主" : archetype == EnemyArchetype.Ranged ? "骷髅法师" : archetype == EnemyArchetype.Elite ? "精英骷髅战士" : "骷髅仆从";
    void Awake() { controller = GetComponent<CharacterController>(); health = GetComponent<CombatHealth>(); spawn = transform.position; rotation = transform.rotation; }
    void Update()
    {
        if (health.Dead) {
            DropLootOnce();
            controller.enabled = false;
            if (warningRing != null) warningRing.gameObject.SetActive(false);
            if (GetComponent<FantasyActorVisual>() == null)
                transform.localScale = Vector3.Lerp(transform.localScale, new Vector3(1, .12f, 1), Time.deltaTime * 7);
            return;
        }
        if (archetype == EnemyArchetype.Boss) return;
        if (target != null && target.GameplayPaused) return;
        if (target == null || target.Health.Dead) { CancelAttack(); return; }
        var guard=GetComponent<EncounterGuard>();if(guard!=null&&guard.enabled&&guard.IdleOrReturn(controller,speed,ref verticalSpeed)){CancelAttack();return;}
        Vector3 offset = Vector3.ProjectOnPlane(target.transform.position - transform.position, Vector3.up);
        float distance = offset.magnitude;
        Vector3 movement = Vector3.zero;
        if (strikeAt >= 0) {
            if (Time.time >= strikeAt) { ReleaseAttack(); CancelAttack(); }
        }
        else if (distance < detectionRange) {
            if (offset.sqrMagnitude > .001f) transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(offset), Time.deltaTime * 8);
            if (archetype == EnemyArchetype.Ranged) {
                bool sight = HasSight();
                if (distance < 4.5f) movement = -offset.normalized * speed;
                else if (distance > preferredDistance || !sight) movement = offset.normalized * speed;
                if (distance >= 4.5f && distance <= attackRange && sight && Time.time >= nextAttack) PrepareAttack();
            }
            else if (distance > attackRange) movement = offset.normalized * speed;
            else if (Time.time >= nextAttack && HasSight()) PrepareAttack();
        }
        movement = guard!=null&&guard.enabled?guard.Chase(movement):Steer(movement);
        if (controller.isGrounded && verticalSpeed < 0) verticalSpeed = -2;
        verticalSpeed += Physics.gravity.y * Time.deltaTime;
        controller.Move((movement + Vector3.up * verticalSpeed) * Time.deltaTime);
    }
    void PrepareAttack()
    {
        lockedAim = target.transform.position + Vector3.up;
        strikeAt = Time.time + windup;
        nextAttack = Time.time + windup + attackInterval;
        if (warningRing != null) warningRing.gameObject.SetActive(true);
    }
    public void ReleaseAttack()
    {
        if (health.Dead || target == null || target.Health.Dead || target.GameplayPaused) return;
        GetComponent<FantasyActorVisual>()?.Attack(archetype == EnemyArchetype.Ranged);
        CombatFeedback.Find(this)?.EnemyAttack(this, archetype == EnemyArchetype.Ranged);
        if (archetype == EnemyArchetype.Ranged) {
            if (projectileMaterial != null)
                EnemyProjectile.Fire(this, transform.position + Vector3.up * 1.25f + transform.forward * .7f, lockedAim, damage, projectileSpeed, projectileMaterial);
        }
        else {
            float distance = Vector3.ProjectOnPlane(target.transform.position - transform.position, Vector3.up).magnitude;
            if (distance <= attackRange + .15f && HasSight()) target.Health.Damage(damage, target.transform.position + Vector3.up, target.transform.position - transform.position);
        }
    }
    public Vector3 Steer(Vector3 movement)
    {
        if (movement.sqrMagnitude < .01f) return movement;
        Vector3 direction = movement.normalized;
        if (ClearDirection(direction)) return movement;
        foreach (float angle in new[] { 45f, -45f, 90f, -90f, 135f, -135f }) {
            Vector3 alternate = Quaternion.Euler(0, angle, 0) * direction;
            if (ClearDirection(alternate)) return alternate * movement.magnitude;
        }
        return Vector3.zero;
    }
    bool ClearDirection(Vector3 direction)
    {
        foreach (var hit in Physics.SphereCastAll(transform.position + Vector3.up, .35f, direction, 1.1f, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.GetComponentInParent<CombatEnemy>() != null || hit.collider.GetComponentInParent<ThirdPersonHero>() != null) continue;
            return false;
        }
        return true;
    }
    public void DropLootOnce()
    {
        if (health == null || !health.Dead || lootDropped) return;
        lootDropped = true;
        if (archetype == EnemyArchetype.Boss && target != null) {
            EnemyProjectile.Clear(gameObject.scene);
            var core = LootPickup.Spawn(MaterialKind.BossCore, 2, transform.position + Vector3.up * .5f + Vector3.forward);
            UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(core.gameObject, gameObject.scene);
            string reward = target.Equipment.GrantBossEquipment();
            target.Inventory.NotifyMessage("首领已击败！" + reward + " 已掉落在你附近，按 E 拾取；领主核心在首领身旁。");
        }
        if (target != null && archetype != EnemyArchetype.Boss && Random.value < (archetype == EnemyArchetype.Elite ? .85f : .4f)) LootPickup.SpawnGear(AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave), transform.position + Vector3.up * .6f);
        if (target != null && target.Progression != null) target.Progression.GainExperience(experienceReward);
        Vector3 p = transform.position + Vector3.up * .5f;
        int hides = Random.Range(Mathf.Max(1, hideMin), Mathf.Max(hideMin, hideMax) + 1);
        var hide = LootPickup.Spawn(MaterialKind.MonsterHide, hides, p + Vector3.left * .45f);
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(hide.gameObject, gameObject.scene);
        if (crystalAmount > 0) {
            var shard = LootPickup.Spawn(MaterialKind.CrystalShard, crystalAmount, p + Vector3.right * .45f);
            UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(shard.gameObject, gameObject.scene);
        }
    }
    bool HasSight()
    {
        Vector3 origin = transform.position + Vector3.up;
        Vector3 line = target.transform.position + Vector3.up - origin;
        foreach (var hit in Physics.RaycastAll(origin, line.normalized, line.magnitude, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.GetComponentInParent<CombatEnemy>() != null || hit.collider.GetComponentInParent<ThirdPersonHero>() != null) continue;
            return false;
        }
        return true;
    }
    void CancelAttack() { strikeAt = -1; if (warningRing != null) warningRing.gameObject.SetActive(false); }
    public void SetSpawn(Vector3 position) { spawn = position; }
    public void RestoreState(SavedEnemy state)
    {
        ResetEnemy(); controller.enabled = false;
        transform.SetPositionAndRotation(state.position, Quaternion.Euler(0, state.yaw, 0));
        health.RestoreHealth(state.health); lootDropped = health.Dead;
        controller.enabled = !health.Dead;
    }
    public void ResetEnemy()
    {
        controller.enabled = false;
        transform.SetPositionAndRotation(spawn, rotation);
        transform.localScale = Vector3.one;
        controller.enabled = true;
        health.ResetHealth();
        GetComponent<FantasyActorVisual>()?.ResetRecoil();
        lootDropped = false;
        verticalSpeed = 0;
        nextAttack = Time.time + .8f;
        CancelAttack();
        var brain = GetComponent<BossBrain>(); if (brain != null) brain.ResetBrain();
    }
}



