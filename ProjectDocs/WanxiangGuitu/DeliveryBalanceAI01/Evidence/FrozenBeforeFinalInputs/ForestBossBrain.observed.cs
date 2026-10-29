using UnityEngine;
using UnityEngine.AI;

// The tide spirit has an always corporeal, attackable shore body. Water casts
// originate from its lake manifestation; it never requires walking on blocked water.
[RequireComponent(typeof(CombatEnemy))]
public class ForestBossBrain : MonoBehaviour {
    public ForestBossKind Kind {get;private set;}
    public ForestBossState State {get;private set;}
    public ForestBossAttack Attack {get;private set;}
    public Vector3 LockedPoint {get;private set;}
    public float Remaining=>Mathf.Max(0,until-Time.time);
    public bool Enraged=>enemy!=null&&enemy.Health.Current<=enemy.Health.maxHealth*.5f;
    public int Releases {get;private set;}
    CombatEnemy enemy;EncounterGuard guard;CharacterController controller;
    Vector3 direction,origin,waterOrigin,lockedAim;
    float until,readyAt,vertical,chargeLeft,staggerAt,lastMovedAt;
    int sequence;bool hit;
    GameObject manifestation;Material waterMaterial;ForestBossTelegraph warning;
    public GameObject VisualManifestation=>manifestation;
    public ForestBossTelegraph Warning=>warning;
    public Vector3 WarningOrigin=>origin;public Vector3 WarningDirection=>direction;public Vector3 WarningAim=>lockedAim;public Vector3 WarningSource=>Attack==ForestBossAttack.WaterFan?waterOrigin:origin+Vector3.up*1.4f;
    public void ResetBrain(){State=ForestBossState.Idle;sequence=Releases=0;vertical=chargeLeft=0;readyAt=Time.time+2;until=staggerAt=Time.time;lastMovedAt=Time.time;HideHint();if(manifestation!=null)manifestation.SetActive(true);}
    public void Configure(ForestBossKind kind,ForestRegionRuntime owner,Vector3 spawn) {
        Kind=kind;enemy=GetComponent<CombatEnemy>();guard=GetComponent<EncounterGuard>();controller=GetComponent<CharacterController>();
        enemy.Health.maxHealth=kind==ForestBossKind.Warden?320:290;enemy.Health.ResetHealth();guard.Restore(0);enemy.speed=2.5f;enemy.detectionRange=12;enemy.experienceReward=150;
        // Forest navigation is baked for radius .65 / height 2.5. The wave boss
        // uses a larger arena capsule, which must not be copied into narrow paths.
        controller.enabled=false;controller.radius=.6f;controller.height=2.5f;controller.center=Vector3.up*1.25f;controller.enabled=true;
        State=ForestBossState.Idle;readyAt=Time.time+2;lastMovedAt=Time.time;
        var old=GetComponent<BossBrain>();if(old!=null)old.enabled=false;
        name=ForestBossRules.Name(kind);
        if(GetComponent<CatWaterManifestation>()==null)gameObject.AddComponent<CatWaterManifestation>();
        var crown=GameObject.CreatePrimitive(kind==ForestBossKind.Warden?PrimitiveType.Cube:PrimitiveType.Sphere);crown.name=kind==ForestBossKind.Warden?"角卫枝冠":"潮灵水冠";crown.transform.SetParent(transform,false);crown.transform.localPosition=Vector3.up*3.4f;crown.transform.localScale=kind==ForestBossKind.Warden?new Vector3(.65f,.25f,.45f):new Vector3(.55f,.8f,.55f);crown.GetComponent<Collider>().enabled=false;
        waterMaterial=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=kind==ForestBossKind.Warden?new Color(.3f,.7f,.2f):new Color(.1f,.7f,1)};crown.GetComponent<Renderer>().sharedMaterial=waterMaterial;
        if(kind==ForestBossKind.Tide){waterOrigin=owner.Layout.terrain.lakeCenter+new Vector3(0,1.4f,owner.Layout.terrain.lakeSize.z*.5f+1);manifestation=GameObject.CreatePrimitive(PrimitiveType.Sphere);manifestation.name="湖心水面显灵（不可碰撞表现）";manifestation.transform.SetParent(transform.parent);manifestation.transform.position=waterOrigin;manifestation.transform.localScale=new Vector3(1.2f,2.2f,1.2f);manifestation.GetComponent<Collider>().enabled=false;manifestation.GetComponent<Renderer>().sharedMaterial=waterMaterial;}
    }
    void Update() {
        if(enemy==null)return;
        if(enemy.Health.Dead){EndDeathPresentation();return;}
        if(enemy.target==null||enemy.target.Health.Dead){HideHint();return;}
        if(enemy.target.GameplayPaused)return;
        if(guard.IdleOrReturn(controller,enemy.speed,ref vertical)){State=guard.State==2?ForestBossState.Returning:ForestBossState.Idle;HideHint();chargeLeft=0;readyAt=Mathf.Max(readyAt,Time.time+1);return;}
        if(State==ForestBossState.Telegraph){if(Time.time>=until)Release();return;}
        if(State==ForestBossState.Attacking){AdvanceCharge(Time.deltaTime);return;}
        if((State==ForestBossState.Recovery||State==ForestBossState.Hurt)&&Time.time<until){Ground(Vector3.zero);return;}
        State=ForestBossState.Tracking;
        var def=ForestBossRules.Definition(ForestBossRules.Next(Kind,sequence,Enraged));
        var offset=Vector3.ProjectOnPlane(enemy.target.transform.position-transform.position,Vector3.up);
        if(offset.sqrMagnitude>.01f)transform.rotation=Quaternion.Slerp(transform.rotation,Quaternion.LookRotation(offset),Time.deltaTime*5);
        if(Time.time>=readyAt&&offset.magnitude<=def.range&&Sight(transform.position+Vector3.up*1.4f,enemy.target.transform.position+Vector3.up)){Begin(def.attack);return;}
        var move=offset.magnitude>2?guard.Chase(offset.normalized*enemy.speed):Vector3.zero;var before=transform.position;Ground(move);
        if(Vector3.Distance(before,transform.position)>.005f)lastMovedAt=Time.time;
        // A failed path never starts an unbounded charge or grants immunity. Return
        // using the same nav guard, then allow the player to re-engage normally.
        if(offset.magnitude>2&&Time.time-lastMovedAt>6){guard.Restore(2);lastMovedAt=Time.time;}
    }
    public bool Begin(ForestBossAttack attack) {
        if(enemy==null||enemy.Health.Dead||enemy.target==null||enemy.target.Health.Dead||enemy.target.GameplayPaused||State==ForestBossState.Telegraph||State==ForestBossState.Attacking)return false;
        if((Kind==ForestBossKind.Warden)!=(attack<=ForestBossAttack.SeedVolley))return false;
        BAL01Trace.Begin(enemy);Attack=attack;origin=transform.position;direction=Vector3.ProjectOnPlane(enemy.target.transform.position-origin,Vector3.up).normalized;if(direction.sqrMagnitude<.1f)direction=transform.forward;
        lockedAim=enemy.target.transform.position+Vector3.up;LockedPoint=attack==ForestBossAttack.TidalMark?enemy.target.transform.position:origin;until=Time.time+ForestBossRules.Definition(attack).windup;State=ForestBossState.Telegraph;hit=false;
        ShowHint();CombatFeedback.Find(this)?.BossWarning(transform.position);return true;
    }
    public bool Release() {
        if(State!=ForestBossState.Telegraph||enemy.Health.Dead||enemy.target==null||enemy.target.Health.Dead||enemy.target.GameplayPaused)return false;
        var d=ForestBossRules.Definition(Attack);BAL01Trace.Release(enemy);HideHint();Releases++;GetComponent<FantasyActorVisual>()?.Attack(Attack==ForestBossAttack.WaterFan||Attack==ForestBossAttack.SeedVolley);
        if(Attack==ForestBossAttack.AntlerCharge){chargeLeft=d.range;until=Time.time+1.5f;State=ForestBossState.Attacking;return true;}
        if(Attack==ForestBossAttack.SeedVolley||Attack==ForestBossAttack.WaterFan){
            Vector3 start=Attack==ForestBossAttack.WaterFan?waterOrigin:transform.position+Vector3.up*1.4f;
            for(int i=-2;i<=2;i++){var offset=BossWarningGeometry.FanDirection(start,lockedAim,i+2);EnemyProjectile.Fire(enemy,start, start+offset,d.damage,Attack==ForestBossAttack.WaterFan?9:8,enemy.projectileMaterial,d.range);}
        }else {
            // Tidal mark is a delayed ground eruption at the locked shore position;
            // unlike a projectile it doesn't travel through the intervening lake.
            if(BossWarningGeometry.Contains(Attack,enemy.target.transform.position,origin,direction,LockedPoint)&&Sight(LockedPoint+Vector3.up,enemy.target.transform.position+Vector3.up))BAL01Trace.Direct(enemy,enemy.target,d.damage,enemy.target.transform.position+Vector3.up,direction);
        }
        Recover();return true;
    }
    public void AdvanceCharge(float dt) {
        if(State!=ForestBossState.Attacking||enemy.Health.Dead||enemy.target.GameplayPaused||dt<=0)return;
        var before=transform.position;var desired=before+direction*Mathf.Min(chargeLeft,10*dt);
        if(!NavMesh.SamplePosition(desired,out var nav, .8f,NavMesh.AllAreas)||Vector3.ProjectOnPlane(nav.position-desired,Vector3.up).magnitude>.5f){Recover();return;}
        Ground(direction*(Mathf.Min(chargeLeft,10*dt)/dt),dt);var after=transform.position;float moved=Vector3.ProjectOnPlane(after-before,Vector3.up).magnitude;chargeLeft-=moved;
        var def=ForestBossRules.Definition(Attack);
        if(!hit&&ForestBossRules.InCharge(enemy.target.transform.position,before,after,def.radius)&&Sight(after+Vector3.up,enemy.target.transform.position+Vector3.up)){BAL01Trace.Direct(enemy,enemy.target,def.damage,enemy.target.transform.position+Vector3.up,direction);hit=true;}
        if(chargeLeft<=.1f||Time.time>=until||moved<dt)Recover();
    }
    void Recover(){State=ForestBossState.Recovery;until=Time.time+ForestBossRules.Definition(Attack).recovery;readyAt=until+ForestBossRules.Definition(Attack).cooldown*(Enraged?.75f:1);lastMovedAt=readyAt;sequence++;HideHint();}
    public void EndDeathPresentation(){if(enemy==null||!enemy.Health.Dead)return;State=ForestBossState.Dead;chargeLeft=0;HideHint();if(manifestation!=null)manifestation.SetActive(false);}
    public void OnDamaged() {
        if(enemy==null||enemy.Health.Dead)return;
        if(Time.time<staggerAt||State==ForestBossState.Attacking)return;
        float recoveryUntil=State==ForestBossState.Recovery?until:0;staggerAt=Time.time+7;State=ForestBossState.Hurt;until=Mathf.Max(recoveryUntil,Time.time+.45f);readyAt=Mathf.Max(readyAt,until+.8f);lastMovedAt=readyAt;chargeLeft=0;HideHint();
    }
    void Ground(Vector3 velocity,float delta=-1){if(!controller.enabled)return;if(delta<0)delta=Time.deltaTime;if(controller.isGrounded&&vertical<0)vertical=-2;vertical+=Physics.gravity.y*delta;controller.Move((velocity+Vector3.up*vertical)*delta);}
    bool Sight(Vector3 a,Vector3 b){var delta=b-a;if(delta.sqrMagnitude<.001f)return true;foreach(var h in Physics.RaycastAll(a,delta.normalized,delta.magnitude,~0,QueryTriggerInteraction.Ignore))if(h.collider.GetComponentInParent<CombatEnemy>()==null&&h.collider.GetComponentInParent<ThirdPersonHero>()==null)return false;return true;}
    void ShowHint(){if(warning==null){var g=new GameObject("森林首领攻击预警");g.transform.SetParent(transform,false);warning=g.AddComponent<ForestBossTelegraph>();}warning.Show(Attack,origin,direction,LockedPoint,WarningSource,lockedAim);}
    void HideHint(){if(warning!=null)warning.Hide();}
    void OnDisable(){HideHint();}
    void OnDestroy(){if(warning!=null)Destroy(warning.gameObject);if(manifestation!=null)Destroy(manifestation);if(waterMaterial!=null)Destroy(waterMaterial);}
}
