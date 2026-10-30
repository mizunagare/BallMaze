using UnityEngine;
using System.Linq;
using System.Collections.Generic;

public enum EnemyArchetype { Melee, Ranged, Elite, Boss }
public enum EnemyCombatState { Idle, Approach, Reposition, Telegraph, Recovery, Returning, Dead }

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
    public float ExpectedHideYield => (Mathf.Max(1,hideMin)+Mathf.Max(hideMin,hideMax))*.5f;
    public float GearDropChance => target==null||archetype==EnemyArchetype.Boss?0:archetype==EnemyArchetype.Elite?.85f:.4f;
    public const int OutpostCrystalMinimum=2,OutpostCrystalMaximumExclusive=5;
    public static float OutpostCrystalMean=>(OutpostCrystalMinimum+OutpostCrystalMaximumExclusive-1)*.5f;
    [InspectorName("击杀经验值")] public int experienceReward = 25;
    public float projectileSpeed = 8, preferredDistance = 7;
    public Material projectileMaterial;
    bool lootDropped;
    Collider[] deathColliders;
    float deadFor;
    Renderer[] hiddenFallback;
    void StopDeadCollision(){if(deathColliders==null){deathColliders=GetComponentsInChildren<Collider>().Where(c=>c.enabled).ToArray();foreach(var c in deathColliders)c.enabled=false;}}
    CharacterController controller;
    CombatHealth health;
    Vector3 spawn, lockedAim;
    Quaternion rotation;
    float verticalSpeed, strikeAt = -1, nextAttack;
    float recoverUntil;
    Vector3 attackOrigin,lockedDirection;float predictedFlight,releasedThreatStart=-1,releasedThreatEnd=-1;
    EnemyAttackSignal signal;
    static readonly HashSet<CombatEnemy> activeEnemies=new HashSet<CombatEnemy>();
    public const float ReleaseSeparation=.24f;
    public EnemyCombatState State {get;private set;}
    public float RecoveryRemaining=>Mathf.Max(0,recoverUntil-Time.time);
    public float TelegraphRemaining=>strikeAt<0?0:Mathf.Max(0,strikeAt-Time.time);
    public float AttackHalfAngle=>archetype==EnemyArchetype.Elite?60:75;
    void OnEnable(){activeEnemies.Add(this);}
    void OnDisable(){activeEnemies.Remove(this);CancelAttack();ClearReleasedThreat();recoverUntil=0;}
    public CombatHealth Health => health;
    public bool WindingUp => strikeAt >= 0;
    public string DisplayName => CatActorVisual.DisplayName(this);
    void Awake() { controller = GetComponent<CharacterController>(); health = GetComponent<CombatHealth>(); health.Observed+=OnHealthObserved;spawn = transform.position; rotation = transform.rotation; }
    void OnHealthObserved(HealthObservation observation){if(observation.deathTransition){StopDeadAttacks();StopDeadCollision();}}
    void OnDestroy(){activeEnemies.Remove(this);if(health!=null)health.Observed-=OnHealthObserved;}
    void StopDeadAttacks(){CancelAttack();GetComponent<BossBrain>()?.StopAttack();GetComponent<ForestBossBrain>()?.EndDeathPresentation();}
    void Update()
    {
        if (health.Dead) {
            State=EnemyCombatState.Dead;
            DropLootOnce();
            StopDeadAttacks();
            StopDeadCollision();
            controller.enabled = false;
            if (warningRing != null) warningRing.gameObject.SetActive(false);
            if (GetComponent<FantasyActorVisual>() == null){
                transform.localScale = Vector3.Lerp(transform.localScale, new Vector3(1, .12f, 1), Time.deltaTime * 7);
                deadFor+=Time.deltaTime;if(deadFor>=1.35f&&hiddenFallback==null){hiddenFallback=GetComponentsInChildren<Renderer>().Where(r=>r.enabled).ToArray();foreach(var r in hiddenFallback)r.enabled=false;}
            }
            return;
        }
        if (target!=null&&AdventureFlow.Find(target)?.AtCamp==true){CancelAttack();return;}
        if(target!=null&&(target.GameplayPaused||Time.timeScale<=0)){releasedThreatStart+=Time.deltaTime;releasedThreatEnd+=Time.deltaTime;}
        if (archetype == EnemyArchetype.Boss) return;
        if (target != null && (target.GameplayPaused||Time.timeScale<=0)) {if(strikeAt>=0)strikeAt+=Time.deltaTime;nextAttack+=Time.deltaTime;recoverUntil+=Time.deltaTime;return;}
        if (target == null || target.Health.Dead) { CancelAttack(); return; }
        var guard=GetComponent<EncounterGuard>();if(guard!=null&&guard.enabled&&guard.IdleOrReturn(controller,speed,ref verticalSpeed)){State=guard.State==2?EnemyCombatState.Returning:EnemyCombatState.Idle;CancelAttack();return;}
        Vector3 offset = Vector3.ProjectOnPlane(target.transform.position - transform.position, Vector3.up);
        float distance = offset.magnitude;
        Vector3 movement = Vector3.zero;bool blockedReposition=false;
        if (strikeAt >= 0) {
            State=EnemyCombatState.Telegraph;
            if (Time.time >= strikeAt) { ReleaseAttack();recoverUntil=Time.time+(archetype==EnemyArchetype.Elite?.65f:archetype==EnemyArchetype.Ranged?.45f:.35f);CancelAttack();State=EnemyCombatState.Recovery; }
        }
        else if(Time.time<recoverUntil){State=EnemyCombatState.Recovery;}
        else if (guard!=null&&guard.enabled?guard.Engaged:distance < detectionRange&&HasSight()) {
            State=EnemyCombatState.Approach;
            if (offset.sqrMagnitude > .001f) transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(offset), Time.deltaTime * 8);
            if (archetype == EnemyArchetype.Ranged) {
                State=EnemyCombatState.Reposition;
                bool sight = HasSight() && FiringLane(transform.position,offset.sqrMagnitude>.001f?offset.normalized:transform.forward,target.transform.position+Vector3.up);
                if (distance < 4.5f) movement = -offset.normalized * speed;
                else if (!sight && distance <= attackRange) {movement=Vector3.Cross(Vector3.up,offset.normalized)*speed;blockedReposition=true;}
                else if (distance > preferredDistance || !sight) movement = offset.normalized * speed;
                if (distance <= attackRange && sight && Time.time >= nextAttack) PrepareAttack();
            }
            else if (distance > attackRange) movement = offset.normalized * speed;
            else if (Time.time >= nextAttack && HasSight()) PrepareAttack();
        }else State=EnemyCombatState.Idle;
        if(strikeAt>=0)movement=Vector3.zero;
        // A barrel-blocked shooter tries a physical sidestep. Controller collision remains authoritative.
        movement = guard!=null&&guard.enabled?(blockedReposition?guard.Navigate(movement):guard.Chase(movement)):blockedReposition?movement:Steer(movement);
        if (controller.isGrounded && verticalSpeed < 0) verticalSpeed = -2;
        verticalSpeed += Physics.gravity.y * Time.deltaTime;
        controller.Move((movement + Vector3.up * verticalSpeed) * Time.deltaTime);
    }
    public bool FiringLane(Vector3 origin,Vector3 direction,Vector3 aim) {
        var anchor=origin+Vector3.up*1.25f;var muzzle=anchor+direction*.7f;
        return EnemyProjectile.ClearWorldSegment(anchor,muzzle)&&EnemyProjectile.ClearWorldSegment(muzzle,aim);
    }
    // Reuse the existing live-actor registry. These are predicted threat windows,
    // not a global damage throttle: moving into independent projectiles can still hurt.
    public bool HasAttackSlot(float at,float duration=0) {
        foreach(var other in activeEnemies) {
            if(other==null||other==this||other.target!=target||other.gameObject.scene!=gameObject.scene)continue;
            if(other.ThreatWindow(out var start,out var end)&&at<=end+ReleaseSeparation&&at+duration>=start-ReleaseSeparation)return false;
        }
        return true;
    }
    public bool ThreatWindow(out float start,out float end) {
        start=end=0;if(!isActiveAndEnabled||health==null||health.Dead||target==null||target.Health.Dead)return false;
        if(releasedThreatEnd>=0&&Time.time<=releasedThreatEnd+ReleaseSeparation){start=releasedThreatStart;end=releasedThreatEnd;return true;}
        if(archetype==EnemyArchetype.Boss){var forest=GetComponent<ForestBossBrain>();if(forest!=null&&forest.isActiveAndEnabled)return forest.ThreatWindow(out start,out end);var boss=GetComponent<BossBrain>();return boss!=null&&boss.isActiveAndEnabled&&boss.ThreatWindow(out start,out end);}
        if(strikeAt<0)return false;start=end=strikeAt+predictedFlight;return true;
    }
    public void RememberReleasedThreat(float start,float duration=0){releasedThreatStart=start;releasedThreatEnd=start+duration;}
    public void ClearReleasedThreat(){releasedThreatStart=releasedThreatEnd=-1;}
    void PrepareAttack()
    {
        float scheduled=Time.time+windup;
        var delta=Vector3.ProjectOnPlane(target.transform.position-transform.position,Vector3.up);var direction=delta.normalized;if(direction.sqrMagnitude<.01f)direction=transform.forward;
        float flight=archetype==EnemyArchetype.Ranged?EnemyProjectile.PredictedTravel(this,transform.position+Vector3.up*1.25f+direction*.7f,target.transform.position+Vector3.up,projectileSpeed):0;
        if(!HasAttackSlot(scheduled+flight)){BAL01Trace.Deny(this);return;}
        predictedFlight=flight;
        attackOrigin=transform.position;lockedDirection=Vector3.ProjectOnPlane(target.transform.position-attackOrigin,Vector3.up).normalized;if(lockedDirection.sqrMagnitude<.01f)lockedDirection=transform.forward;transform.rotation=Quaternion.LookRotation(lockedDirection);
        BAL01Trace.Begin(this);lockedAim = target.transform.position + Vector3.up;
        strikeAt = Time.time + windup;
        nextAttack = Time.time + windup + attackInterval;
        State=EnemyCombatState.Telegraph;
        if (warningRing != null) warningRing.gameObject.SetActive(false);
        if(signal==null)signal=GetComponentInChildren<EnemyAttackSignal>(true);
        if(signal==null){var obj=new GameObject("敌人锁定攻击预警");obj.transform.SetParent(transform,false);signal=obj.AddComponent<EnemyAttackSignal>();}
        signal.Show(attackOrigin,lockedDirection,attackRange+.15f,AttackHalfAngle,archetype==EnemyArchetype.Ranged,lockedAim);
    }
    public void ReleaseAttack()
    {
        if (health.Dead || target == null || target.Health.Dead || target.GameplayPaused || AdventureFlow.Find(target)?.AtCamp==true) return;
        if(strikeAt<0||Time.time<strikeAt)return;
        if(Time.timeScale<=0)return;
        if(archetype==EnemyArchetype.Ranged&&!FiringLane(attackOrigin,lockedDirection,lockedAim)){CancelAttack();return;}
        RememberReleasedThreat(Time.time+predictedFlight);strikeAt=-1;signal?.Hide();
        BAL01Trace.Release(this);GetComponent<FantasyActorVisual>()?.Attack(archetype == EnemyArchetype.Ranged);
        CombatFeedback.Find(this)?.EnemyAttack(this, archetype == EnemyArchetype.Ranged);
        if (archetype == EnemyArchetype.Ranged) {
            if (projectileMaterial != null)
                EnemyProjectile.Fire(this, attackOrigin + Vector3.up * 1.25f + lockedDirection * .7f, lockedAim, damage, projectileSpeed, projectileMaterial);
        }
        else {
            var offset=Vector3.ProjectOnPlane(target.transform.position-attackOrigin,Vector3.up);float distance=offset.magnitude;
            if (distance <= attackRange + .15f && (offset.sqrMagnitude<.01f||Vector3.Dot(lockedDirection,offset.normalized)>=Mathf.Cos(AttackHalfAngle*Mathf.Deg2Rad)) && HasSight()) BAL01Trace.Direct(this,target,damage,target.transform.position+Vector3.up,target.transform.position-transform.position);
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
        var forestBoss=GetComponent<ForestBossBrain>();
        if(forestBoss!=null&&target!=null){AdventureFlow.Find(target)?.RecordForestBoss(this,forestBoss.Kind);}
        if (forestBoss==null && archetype == EnemyArchetype.Boss && target != null) {
            EnemyProjectile.Clear(gameObject.scene);
            var core = LootPickup.Spawn(MaterialKind.BossCore, 2, transform.position + Vector3.up * .5f + Vector3.forward);
            UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(core.gameObject, gameObject.scene);
            string reward = target.Equipment.GrantBossEquipment();
            target.Inventory.NotifyMessage("首领已击败！" + reward + " 已掉落在你附近，按 "+PlayerInput.Key(PlayerAction.Interact)+" 拾取；领主核心在首领身旁。");
        }
        if (target != null && archetype != EnemyArchetype.Boss && AdventureRandom.Value(owner:this) < GearDropChance) LootPickup.SpawnGear(AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave,owner:this), transform.position + Vector3.up * .6f);
        var rewardSite=ForestRewards.Site(this,GetComponent<EncounterGuard>()?.poi);
        if(rewardSite?.siteKind==ForestSiteKind.Outpost&&archetype==EnemyArchetype.Elite){var bonus=LootPickup.Spawn(MaterialKind.CrystalShard,AdventureRandom.Range(OutpostCrystalMinimum,OutpostCrystalMaximumExclusive,owner:this),transform.position+Vector3.up*.7f);UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(bonus.gameObject,gameObject.scene);}
        if (target != null && target.Progression != null) BAL01Trace.Award(this,experienceReward);
        Vector3 p = transform.position + Vector3.up * .5f;
        int hides = AdventureRandom.Range(Mathf.Max(1, hideMin), Mathf.Max(hideMin, hideMax) + 1,owner:this);
        var hide = LootPickup.Spawn(MaterialKind.MonsterHide, hides, p + Vector3.left * .45f);
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(hide.gameObject, gameObject.scene);
        if (crystalAmount > 0) {
            var shard = LootPickup.Spawn(MaterialKind.CrystalShard, crystalAmount, p + Vector3.right * .45f);
            UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(shard.gameObject, gameObject.scene);
        }
    }
    public bool HasSight()
    {
        Vector3 origin = transform.position + Vector3.up;
        Vector3 line = target.transform.position + Vector3.up - origin;
        foreach (var hit in Physics.RaycastAll(origin, line.normalized, line.magnitude, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.GetComponentInParent<CombatEnemy>() != null || hit.collider.GetComponentInParent<ThirdPersonHero>() != null) continue;
            return false;
        }
        return true;
    }
    void CancelAttack() { strikeAt = -1; if (warningRing != null) warningRing.gameObject.SetActive(false);signal?.Hide(); }
    public void SetSpawn(Vector3 position) { spawn = position; }
    public void RestoreState(SavedEnemy state)
    {
        ResetEnemy(); controller.enabled = false;
        transform.SetPositionAndRotation(state.position, Quaternion.Euler(0, state.yaw, 0));
        health.RestoreHealth(state.health); lootDropped = health.Dead;
        controller.enabled = !health.Dead;
        if(health.Dead){StopDeadAttacks();StopDeadCollision();GetComponent<FantasyActorVisual>()?.HideRestoredDeath();}
    }
    public void ResetEnemy()
    {
        if(deathColliders!=null){foreach(var c in deathColliders)if(c!=null)c.enabled=true;deathColliders=null;}deadFor=0;
        if(hiddenFallback!=null){foreach(var r in hiddenFallback)if(r!=null)r.enabled=true;hiddenFallback=null;}
        GetComponent<FantasyActorVisual>()?.ResetDeathVisual();
        controller.enabled = false;
        transform.SetPositionAndRotation(spawn, rotation);
        transform.localScale = Vector3.one;
        controller.enabled = true;
        health.ResetHealth();
        GetComponent<FantasyActorVisual>()?.ResetRecoil();
        lootDropped = false;
        verticalSpeed = 0;
        nextAttack = Time.time + .8f;
        recoverUntil=0;ClearReleasedThreat();State=EnemyCombatState.Idle;
        CancelAttack();
        var brain = GetComponent<BossBrain>(); if (brain != null) brain.ResetBrain();
        GetComponent<ForestBossBrain>()?.ResetBrain();
    }
}





