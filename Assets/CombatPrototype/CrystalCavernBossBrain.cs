using System;
using System.Linq;
using UnityEngine;

[DefaultExecutionOrder(23000)]
[RequireComponent(typeof(CombatEnemy))]
public sealed class CrystalCavernBossBrain : MonoBehaviour
{
    public enum CombatState { Dormant, Ready, Approach, Warning, Active, Recovery, Transition, Returning, Dead }
    public CombatState State { get; private set; }
    public bool ChallengeCommitted { get; private set; }
    public CrystalCavernBossRules.Attack Attack { get; private set; }
    public int Releases { get; private set; }
    public Vector3 AttackOrigin { get; private set; }
    public Vector3 AttackDirection { get; private set; }
    public float Remaining => Mathf.Max(0,until-Time.time);
    CombatEnemy enemy;
    CombatSession session;
    EncounterGuard guard;
    CharacterController controller;
    Collider[] body;
    LineRenderer[] warnings; Material warningMaterial;
    Animation poseSource;
    float until, readyAt, vertical;
    int sequence;
    Vector3 aim;
    bool engaged, phase2, attackPhase2, hit;
    int crossStep;
    public bool Phase2 => phase2;
    public int CrossStep => crossStep;
    public struct ReleaseObservation { public int frame, release; public float time, rawDamage; public bool phase2; public CrystalCavernBossRules.Attack attack; public Vector3 origin,direction; }
    public event Action<ReleaseObservation> Released;


    public void Bind(CombatSession owner)
    {
        session=owner; enemy=GetComponent<CombatEnemy>();guard=GetComponent<EncounterGuard>();
        controller=GetComponent<CharacterController>();
        var legacy=GetComponent<BossBrain>();if(legacy!=null)legacy.enabled=false;
        enemy.Health.maxHealth=CrystalCavernBossRules.Health;enemy.Health.ResetHealth();
        enemy.speed=CrystalCavernBossRules.Speed;enemy.detectionRange=12;enemy.experienceReward=0;
        controller.enabled=false;controller.radius=.6f;controller.height=2.5f;controller.center=Vector3.up*1.25f;
        body=GetComponentsInChildren<Collider>().Where(c=>c==controller||c.enabled).ToArray();
        warningMaterial=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=new Color(1,.55f,.12f)};
        warnings=new LineRenderer[3];
        for(int i=0;i<warnings.Length;i++)
        {
            var marker=new GameObject("晶脊守望者 · 实际攻击范围 "+i);marker.transform.SetParent(transform,false);
            var line=marker.AddComponent<LineRenderer>();line.sharedMaterial=warningMaterial;
            line.useWorldSpace=true;line.startWidth=line.endWidth=.09f;line.enabled=false;warnings[i]=line;
        }
        var mesh=Resources.Load<Mesh>("CrystalCavernC24/FacetedCrystal");
        var material=Resources.Load<Material>("CrystalCavernC24/Vein");
        for(int i=0;i<5;i++)
        {
            var spine=new GameObject("守望者晶脊 "+i,typeof(MeshFilter),typeof(MeshRenderer));spine.transform.SetParent(transform,false);
            spine.transform.localPosition=new Vector3((i-2)*.35f,2.3f,-.3f);
            spine.transform.localScale=new Vector3(.25f,.8f+(2-Mathf.Abs(i-2))*.2f,.25f);
            spine.GetComponent<MeshFilter>().sharedMesh=mesh;spine.GetComponent<MeshRenderer>().sharedMaterial=material;
        }
        enemy.Health.RefreshVisuals();
        poseSource=GetComponent<FantasyActorVisual>()?.model?.GetComponentInChildren<Animation>(true);
        name="晶脊守望者";
        ChallengeCommitted=CrystalCavernBossRules.Challenged(session);
        ResetIntent();
    }
    public void ResetIntent()
    {
        engaged=false;sequence=0;phase2=enemy.Health.Current<=enemy.Health.maxHealth*.5f;readyAt=Time.time+CrystalCavernBossRules.ReentrySafety;
        State=ChallengeCommitted?CombatState.Ready:CombatState.Dormant;
        HideWarning();SetBody(ChallengeCommitted&&!enemy.Health.Dead);
    }
    void SetBody(bool active){if(body!=null)foreach(var c in body)if(c!=null)c.enabled=active;}
    public static CrystalCavernBossBrain For(WorldEventPoint point)
    {
        if(point.entityId!=CrystalCavernLayout.Challenge)return null;
        return FindObjectsByType<CrystalCavernBossBrain>(FindObjectsSortMode.None).FirstOrDefault(b=>
            b.gameObject.scene==point.gameObject.scene&&b.session!=null&&
            CrystalCavernBossRules.Exact(b.session.GetComponent<ForestRegionRuntime>()?.Layout,b.enemy));
    }
    // The durable event commits before activation. An uncertain write never starts combat.
    public bool Challenge(WorldEventPoint point)
    {
        if(ChallengeCommitted||point.Used||For(point)!=this||!point.CanInteract(enemy.target))return false;
        long revision=session.Flow.Revision;
        try
        {
            var before=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
            if(before.revision!=revision||before.activeRun?.runId!=session.Flow.ActiveRun.runId)
                throw new InvalidOperationException("挑战存档身份未同步");
            string prior=RuinsExploration.Snapshot(before);
            var checkpoint=AdventureData.World(session.Saves.CaptureLegacy());
            point.RestoreUsed(true);
            string expected=RuinsExploration.Snapshot(session.Flow.Compose(session.Saves.CaptureLegacy()));
            if(!session.Saves.SaveProgress(false))
            {
                var disk=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
                if(disk.revision==revision+1&&RuinsExploration.Snapshot(disk)==expected)
                {session.Flow.Published(disk.revision);session.Saves.ConfirmPublishedSave();}
                else if(disk.revision==revision&&RuinsExploration.Snapshot(disk)==prior)
                {
                    point.RestoreUsed(false);session.Flow.ActiveRun.checkpoint=checkpoint;
                    enemy.target.Inventory.NotifyMessage("挑战未保存，未启战；可重试或沿湖岸返回。");return false;
                }
                else throw new InvalidOperationException("挑战保存结果不确定");
            }
            ChallengeCommitted=true;ResetIntent();session.GetComponent<ForestRegionRuntime>().InvalidateRoutes();
            enemy.target.Inventory.NotifyMessage("晶脊守望者已唤醒 · 战场外可脱战，原回程路线保持开放");return true;
        }
        catch(Exception e){session.Flow.MigrationFailed("挑战未启战，请读取完整存档核对："+e.Message);return false;}
    }
    void Update()
    {
        if(enemy==null)return;
        if(enemy.Health.Dead){StopDeath();return;}
        if(!ChallengeCommitted){SetBody(false);return;}
        if(enemy.target==null||enemy.target.Health.Dead){CancelIntent();engaged=false;return;}
        if(enemy.target.GameplayPaused||Time.timeScale<=0){until+=Time.deltaTime;readyAt+=Time.deltaTime;return;}
        SetBody(true);
        if(!CrystalCavernBossRules.InsideArena(enemy.target.transform.position))
        {
            CancelIntent();engaged=false;State=CombatState.Returning;
            var delta=guard.home-transform.position;
            Move(delta.magnitude>1?guard.Navigate(delta.normalized*enemy.speed):Vector3.zero);
            readyAt=Time.time+CrystalCavernBossRules.ReentrySafety;return;
        }
        if(!engaged){engaged=true;readyAt=Time.time+CrystalCavernBossRules.ReentrySafety;State=CombatState.Ready;}
        if(State==CombatState.Warning)
        {
            float tracking=Attack==CrystalCavernBossRules.Attack.Claw?.75f:.6f;
            if((Attack==CrystalCavernBossRules.Attack.Claw||Attack==CrystalCavernBossRules.Attack.Volley)&&Remaining>tracking)
            {
                var next=Vector3.ProjectOnPlane(enemy.target.transform.position-AttackOrigin,Vector3.up);
                if(next.sqrMagnitude>.001f)AttackDirection=Vector3.RotateTowards(AttackDirection,next.normalized,150*Mathf.Deg2Rad*Time.deltaTime,0);
                aim=enemy.target.transform.position+Vector3.up;transform.rotation=Quaternion.LookRotation(AttackDirection);ShowWarning();
            }
            if(Time.time>=until)Release();
            Move(Vector3.zero);return;
        }
        if(State==CombatState.Active)
        {
            if(Time.time<until){HitArea();Move(Vector3.zero);return;}
            if(Attack==CrystalCavernBossRules.Attack.CrossLines&&crossStep==0)
            {crossStep=1;State=CombatState.Warning;until=Time.time+1.1f;ShowWarning();return;}
            Recover();return;
        }
        if(!phase2&&enemy.Health.Current<=enemy.Health.maxHealth*.5f&&
            (State!=CombatState.Recovery||Time.time>=until))
        {
            phase2=true;sequence=0;State=CombatState.Transition;until=Time.time+1.2f;readyAt=until+.55f;
            HideWarning();CombatFeedback.Find(this)?.BossWarning(transform.position);return;
        }
        if(Time.time<readyAt){Move(Vector3.zero);return;}
        var offset=Vector3.ProjectOnPlane(enemy.target.transform.position-transform.position,Vector3.up);
        Attack=CrystalCavernBossRules.Next(sequence,phase2);
        var def=CrystalCavernBossRules.Definition(Attack,phase2);
        if(offset.sqrMagnitude>.001f)transform.rotation=Quaternion.RotateTowards(transform.rotation,Quaternion.LookRotation(offset),150*Time.deltaTime);
        if(offset.magnitude<=def.range&&enemy.HasSight()){Begin();Move(Vector3.zero);return;}
        State=CombatState.Approach;Move(guard.Chase(offset.normalized*enemy.speed));
    }
    void Begin()
    {
        attackPhase2=phase2;crossStep=0;hit=false;
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        if(!enemy.HasAttackSlot(Time.time+def.windup))return;
        AttackOrigin=transform.position;AttackDirection=Vector3.ProjectOnPlane(enemy.target.transform.position-AttackOrigin,Vector3.up).normalized;
        if(AttackDirection.sqrMagnitude<.001f)AttackDirection=transform.forward;
        aim=enemy.target.transform.position+Vector3.up;
        until=Time.time+def.windup;State=CombatState.Warning;
        ShowWarning();
        CombatFeedback.Find(this)?.BossWarning(AttackOrigin);
    }
    void Release()
    {
        if(State!=CombatState.Warning||!ChallengeCommitted||enemy.Health.Dead||enemy.target.Health.Dead)return;
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        HideWarning();Releases++;
        if(Released!=null)foreach(Action<ReleaseObservation> observer in Released.GetInvocationList())
        {try{observer(new ReleaseObservation{frame=Time.frameCount,release=Releases,time=Time.time,rawDamage=def.damage,phase2=attackPhase2,attack=Attack,origin=AttackOrigin,direction=AttackDirection});}catch(Exception error){Debug.LogException(error);}}
        GetComponent<FantasyActorVisual>()?.Attack(Attack==CrystalCavernBossRules.Attack.Volley);
        if(Attack==CrystalCavernBossRules.Attack.Volley)
        {
            var source=AttackOrigin+Vector3.up*1.4f;
            var direction=(aim-source).normalized;
            for(int i=-1;i<=1;i++)
            {
                var d=Quaternion.AngleAxis(i*12,Vector3.up)*direction;
                if(EnemyProjectile.ClearWorldSegment(source,source+d*.17f))
                    EnemyProjectile.Fire(enemy,source,source+d,def.damage,8,enemy.projectileMaterial,def.range);
            }
            enemy.RememberReleasedThreat(Time.time,def.range/8);
        }
        else if(Attack==CrystalCavernBossRules.Attack.CrossLines||Attack==CrystalCavernBossRules.Attack.HollowRing)
        {
            hit=false;State=CombatState.Active;until=Time.time+(Attack==CrystalCavernBossRules.Attack.CrossLines?.12f:.15f);
            enemy.RememberReleasedThreat(Time.time,until-Time.time);HitArea();return;
        }
        else HitArea();
        Recover();
    }
    Vector3 LineDirection => Quaternion.AngleAxis(crossStep==0?-25:25,Vector3.up)*AttackDirection;
    void HitArea()
    {
        if(hit)return;
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        var target=enemy.target;
        var delta=target.transform.position-AttackOrigin;
        var flat=Vector3.ProjectOnPlane(delta,Vector3.up);
        bool contact,geometry;
        if(Attack==CrystalCavernBossRules.Attack.CrossLines)
        {
            var d=LineDirection;
            contact=Physics.OverlapBox(AttackOrigin+d*4+Vector3.up,new Vector3(1.2f,1.2f,4),Quaternion.LookRotation(d),~0,QueryTriggerInteraction.Ignore).Any(c=>c.GetComponentInParent<ThirdPersonHero>()==target);
            float along=Vector3.Dot(flat,d),side=Mathf.Abs(Vector3.Dot(flat,Vector3.Cross(Vector3.up,d)));
            geometry=along>=0&&along<=8&&side<=1.2f&&Mathf.Abs(delta.y)<=1.2f;
        }
        else
        {
            contact=Physics.OverlapSphere(AttackOrigin,def.range,~0,QueryTriggerInteraction.Ignore).Any(c=>c.GetComponentInParent<ThirdPersonHero>()==target);
            geometry=Attack==CrystalCavernBossRules.Attack.HollowRing ? flat.magnitude>=2.2f&&flat.magnitude<=6&&Mathf.Abs(delta.y)<=1.2f :
                Mathf.Abs(delta.y)<=1.6f&&Vector3.Angle(AttackDirection,flat)<=60;
        }
        var from=AttackOrigin+Vector3.up;var to=target.transform.position+Vector3.up;
        bool clear=!Physics.RaycastAll(from,(to-from).normalized,Vector3.Distance(from,to),~0,QueryTriggerInteraction.Ignore)
            .Any(h=>h.collider.GetComponentInParent<CombatEnemy>()==null&&h.collider.GetComponentInParent<ThirdPersonHero>()==null);
        if(contact&&geometry&&clear){hit=true;target.Health.Damage(def.damage,to,Attack==CrystalCavernBossRules.Attack.CrossLines?LineDirection:AttackDirection);}
    }
    void Recover()
    {
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        State=CombatState.Recovery;until=Time.time+def.recovery;readyAt=until+(attackPhase2?.55f:.75f);sequence++;
    }
    void Move(Vector3 movement)
    {
        if(!controller.enabled)return;
        if(controller.isGrounded&&vertical<0)vertical=-2;
        vertical+=Physics.gravity.y*Time.deltaTime;
        controller.Move((movement+Vector3.up*vertical)*Time.deltaTime);
    }
    public bool ThreatWindow(out float start,out float end)
    {start=State==CombatState.Active?Time.time:until;end=until;return isActiveAndEnabled&&ChallengeCommitted&&!enemy.Health.Dead&&(State==CombatState.Warning||State==CombatState.Active);}
    public void StopDeath(){CancelIntent();State=CombatState.Dead;SetBody(false);}
    void CancelIntent(){HideWarning();if(State==CombatState.Warning||State==CombatState.Active){State=CombatState.Ready;readyAt=Mathf.Max(readyAt,Time.time+2);}}
    // Sample only this new actor's existing clip; never drive damage or attack clocks.
    // Windup displays the raised-paw/charging portion. Release advances to the strike.
    void LateUpdate()
    {
        if(poseSource==null||enemy==null||enemy.Health.Dead||enemy.target==null||enemy.target.GameplayPaused||
            (State!=CombatState.Warning&&State!=CombatState.Recovery))return;
        string name=Attack==CrystalCavernBossRules.Attack.Volley?"Spellcast_Shoot":"2H_Melee_Attack_Slice";
        var clip=poseSource[name]?.clip;if(clip==null)return;
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        float fraction=State==CombatState.Warning?Mathf.Lerp(0,.35f,1-Mathf.Clamp01(Remaining/def.windup)):
            Mathf.Lerp(.35f,1,1-Mathf.Clamp01(Remaining/def.recovery));
        clip.SampleAnimation(poseSource.gameObject,clip.length*fraction);
    }
    void ShowWarning()
    {
        HideWarning();
        var def=CrystalCavernBossRules.Definition(Attack,attackPhase2);
        if(Attack==CrystalCavernBossRules.Attack.Volley)
        {
            var source=AttackOrigin+Vector3.up*1.4f;
            for(int i=0;i<3;i++)
            {
                var d=Quaternion.AngleAxis((i-1)*12,Vector3.up)*(aim-source).normalized;
                warnings[i].enabled=true;warnings[i].positionCount=2;warnings[i].SetPosition(0,source);warnings[i].SetPosition(1,source+d*def.range);
            }
        }
        else if(Attack==CrystalCavernBossRules.Attack.CrossLines)
        {
            var line=warnings[0];var d=LineDirection;var side=Vector3.Cross(Vector3.up,d)*1.2f;var p=AttackOrigin+Vector3.up*.08f;
            line.enabled=true;line.positionCount=5;line.SetPositions(new[]{p-side,p+side,p+d*8+side,p+d*8-side,p-side});
        }
        else if(Attack==CrystalCavernBossRules.Attack.HollowRing)
        {
            for(int j=0;j<2;j++){var line=warnings[j];line.enabled=true;line.positionCount=65;float radius=j==0?2.2f:6;
                for(int i=0;i<=64;i++)line.SetPosition(i,AttackOrigin+Vector3.up*.08f+Quaternion.AngleAxis(i*360f/64,Vector3.up)*Vector3.forward*radius);}
        }
        else
        {
            var line=warnings[0];line.enabled=true;line.positionCount=43;
            var ground=AttackOrigin+Vector3.up*.08f;line.SetPosition(0,ground);line.SetPosition(42,ground);
            for(int i=0;i<=40;i++)line.SetPosition(i+1,ground+Quaternion.AngleAxis(Mathf.Lerp(-60,60,i/40f),Vector3.up)*AttackDirection*def.range);
        }
    }
    void HideWarning(){if(warnings!=null)foreach(var line in warnings)if(line!=null)line.enabled=false;}
    void OnDisable(){CancelIntent();}
    void OnDestroy(){if(warningMaterial!=null)Destroy(warningMaterial);}
}
