using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class AdventureCombat : MonoBehaviour
{
    public AdventureLoadout Gear { get; private set; }
    ThirdPersonHero hero;
    float attackAt, skillAt, switchAt;
    // Release fractions are initial per-weapon tuning, not clip-frame indices.
    [SerializeField] Vector4 basicRelease = new Vector4(.35f,.40f,.45f,.40f);
    [SerializeField] Vector4 skillRelease = new Vector4(.40f,.45f,.50f,.45f);
    sealed class AttackAction {
        public long id; public GearItem source; public GearType type; public bool skill,released;
        public float releaseAt,endsAt,power,range,reach,area; public int quality;
    }
    readonly List<AttackAction> actions = new List<AttackAction>();
    long nextAttackId;
    public int PendingAttackCount {get{int count=0;foreach(var a in actions)if(!a.released)count++;return count;}}
    public long LastAttackId {get;private set;}
    public float LastReleaseTime {get;private set;}
    public int LastReleaseFrame {get;private set;}=-1;
    public string LastAttackPhase {get;private set;}="Idle";
    public static float ActionDuration(float interval)=>Mathf.Max(.01f,Mathf.Min(.55f,interval));
    public void CancelPending() {
        bool cancelled=false;
        for(int i=actions.Count-1;i>=0;i--)if(!actions[i].released){actions.RemoveAt(i);cancelled=true;}
        if(cancelled){LastAttackPhase="Cancelled";GetComponent<FantasyActorVisual>()?.CancelAttack();}
    }
    // COMBAT02 first measured experiment: basic thrust trades cadence for reach and power.
    public const float SpearCadence=1.30f, SpearPower=1.25f, SpearReach=3.1f, SpearHalfWidth=.4f;
    public float BasicInterval=>hero.AttackInterval*(Gear.Weapon==GearType.Spear?SpearCadence:1)*(WeaponTraits.Has(Gear.Main,1)?.82f:1);
    public float BasicPower=>hero.AttackPower*(Gear.Weapon==GearType.Spear?SpearPower:1);
    void BeginAttack(bool skill) {
        float duration=ActionDuration(hero.AttackInterval*(!skill&&Gear.Weapon==GearType.Spear?SpearCadence:1));
        var source=Gear.Main?.Clone();var type=Gear.Weapon;
        float fraction=(skill?skillRelease:basicRelease)[(int)type];
        var a=new AttackAction{id=++nextAttackId,source=source,type=type,skill=skill,
            releaseAt=Time.time+duration*Mathf.Clamp(fraction,.05f,.95f),endsAt=Time.time+duration,
            power=skill?hero.AttackPower:BasicPower,range=hero.AttackRange,reach=hero.Progression.ReachBonus,
            area=WeaponTraits.Has(source,2)?1.25f:1,quality=source==null?0:(int)source.quality};
        actions.Add(a);LastAttackId=a.id;LastAttackPhase="Startup";
        GetComponent<FantasyActorVisual>()?.AttackTimed((int)type>=2,duration);
        CombatFeedback.Find(this)?.AttackStarted(hero);
    }
    void AdvanceAttacks() {
        if(!Ready||PlayerInput.Suspended){CancelPending();return;}
        // Reverse iteration tolerates damage callbacks that reset combat or change equipment.
        for(int i=actions.Count-1;i>=0;i--){
            if(i>=actions.Count)continue;var a=actions[i];
            if(!a.released&&Time.time>=a.releaseAt){a.released=true;LastAttackPhase="Active";LastReleaseTime=Time.time;LastReleaseFrame=Time.frameCount;Release(a);}
            if(i<actions.Count&&actions[i]==a&&Time.time>=a.endsAt){actions.RemoveAt(i);if(actions.Count==0)LastAttackPhase="Idle";}
            else if(a.released)LastAttackPhase="Recovery";
        }
    }
    void OnDisable(){CancelPending();AdventureProjectile.ClearOwner(hero);}
    void OnApplicationFocus(bool focused){if(!focused)CancelPending();}
    public float AttackRemaining=>Mathf.Max(0,attackAt-Time.time);
    public float SwitchRemaining=>Mathf.Max(0,switchAt-Time.time);
    public void EquipmentChanged(){CancelPending();attackAt=Mathf.Max(attackAt,Time.time+.25f);}
    public bool SwitchWeapon(){if(!Ready||Time.time<switchAt||!Gear.SwapWeapons())return false;switchAt=Time.time+.7f;EquipmentChanged();return true;}
    GameObject weapon;
    string displayedWeaponId;
    public float SkillDuration=>7+(WeaponTraits.Has(Gear.Main,5)?1:0);
    public float SkillRemaining => Mathf.Max(0, skillAt-Time.time);
    public string ClassName => new[] {"剑战士","枪卫士","法杖法师","弓游侠"}[(int)Gear.Weapon];
    public string SkillName => new[] {"旋风横扫","贯穿突刺","陨火爆裂","扇形箭雨"}[(int)Gear.Weapon];
    public string SkillDescription => new[] {"周围 4 米造成 200% 攻击伤害", "前方 7 米直线造成 240% 攻击伤害", "前方火球命中后 4 米范围造成 220% 伤害", "发射 5 支箭，每支造成 120% 攻击伤害"}[(int)Gear.Weapon];
    void Awake() { hero=GetComponent<ThirdPersonHero>(); Gear=GetComponent<AdventureLoadout>(); if(Gear==null)Gear=gameObject.AddComponent<AdventureLoadout>(); }
    void Update() {AdvanceAttacks();if(PlayerInput.Down(PlayerAction.SwitchWeapon))SwitchWeapon();if(PlayerInput.Down(PlayerAction.Skill))UseSkill();}
    bool Ready => hero!=null&&!hero.Health.Dead&&!hero.GameplayPaused&&Time.timeScale>0&&!hero.Dodge.IsRolling&&hero.Inventory.ClosedFrame!=Time.frameCount&&!PlayerInput.Suspended&&!(AdventureFlow.Find(hero)?.BlockCombat==true);
    public bool Strike()
    {
        if(!Ready||Time.time<attackAt)return false;
        attackAt=Time.time+BasicInterval;
        BeginAttack(false);
        return true;
    }
    public bool UseSkill()
    {
        if(!Ready||Time.time<skillAt)return false;
        skillAt=Time.time+7+(WeaponTraits.Has(Gear.Main,5)?1:0);
        BeginAttack(true);
        return true;
    }
    void Release(AttackAction a)
    {
        CombatFeedback.Find(this)?.Swing(hero,a.type==GearType.Spear);
        if(!a.skill){
            if((int)a.type>=2)Fire(a,transform.forward,a.power,a.type==GearType.Staff?.9f:0,a.type==GearType.Bow?23:16);
            else Melee(a,a.type==GearType.Spear?SpearReach+a.reach:a.range,a.power,a.type==GearType.Spear?.88f:.25f,a.type==GearType.Spear?SpearHalfWidth:.85f);
            return;
        }
        float area=a.area;int q=a.quality;float power=a.power;
        switch(a.type){
            case GearType.Sword: Melee(a,4*area,power*2,-1);if(q>=2){int n=q>=3?1:0;for(int i=-n;i<=n;i++)Fire(a,Quaternion.Euler(0,i*18,0)*transform.forward,power*.75f,q>=4?1.8f:0,19);}break;
            case GearType.Spear: Melee(a,7*area,power*2.4f,.94f);if(q>=2)Melee(a,9*area,power*.8f,q>=3?.80f:.94f,q>=3?1.6f:.85f);if(q>=4)Fire(a,transform.forward,power,2,25);break;
            case GearType.Staff: Fire(a,transform.forward,power*2.2f,(q>=2?5:4)*area,14);if(q>=3)for(int i=-1;i<=1;i+=2)Fire(a,Quaternion.Euler(0,i*22,0)*transform.forward,power*.8f,(q>=4?3:1.6f)*area,14);break;
            case GearType.Bow:for(int i=-(q>=4?4:q>=2?3:2);i<=(q>=4?4:q>=2?3:2);i++)Fire(a,Quaternion.Euler(0,i*12*area,0)*transform.forward,power*1.2f,q>=3?1.5f:0,23);break;
        }
    }
    void Fire(AttackAction a,Vector3 dir,float damage,float radius,float speed) { AdventureProjectile.Spawn(hero,transform.position+Vector3.up*1.25f+transform.forward*.7f,dir,damage,radius,speed,a.source,a.skill); }
    void Melee(AttackAction a,float radius,float damage,float dot,float width=.85f)
    {
        var visited=new HashSet<Component>();
        foreach(var c in Physics.OverlapSphere(transform.position+Vector3.up,radius)){
            var enemy=c.GetComponentInParent<CombatEnemy>(); var node=c.GetComponentInParent<AdventureResource>();
            Component target=enemy!=null?(Component)enemy:node;
            if(target==null||!visited.Add(target))continue;
            Vector3 aim=target.transform.position+Vector3.up;
            Vector3 toward=Vector3.ProjectOnPlane(aim-transform.position,Vector3.up);
            if(toward.sqrMagnitude>.01f&&Vector3.Dot(transform.forward,toward.normalized)<dot)continue;
            if(a.type==GearType.Spear && Mathf.Abs(Vector3.Dot(transform.right,toward))>width)continue;
            if(!Sight(transform.position+Vector3.up,aim,target))continue;
            if(enemy!=null)WeaponHit.Apply(hero,enemy,damage,aim,toward,a.source,a.skill);else node.Hit(damage,hero);
        }
        AdventurePulse.SpawnMelee(transform,radius,dot,a.type==GearType.Spear?width:float.PositiveInfinity,new Color(.9f,.7f,.25f));
    }
    public static bool Sight(Vector3 a,Vector3 b,Component target)
    {
        foreach(var h in Physics.RaycastAll(a,(b-a).normalized,Vector3.Distance(a,b),~0,QueryTriggerInteraction.Ignore)) {
            if(h.collider.GetComponentInParent<ThirdPersonHero>()!=null)continue;
            if(h.collider.transform==target.transform||h.collider.transform.IsChildOf(target.transform))continue;
            if(h.collider.GetComponentInParent<CombatEnemy>()!=null)continue;
            return false;
        }return true;
    }
    public void ResetCombat(){CancelPending();actions.Clear();attackAt=skillAt=switchAt=0;AdventureProjectile.Clear(gameObject.scene);}
    public void RestoreCooldown(float remaining,float attack=.2f,float swap=0){CancelPending();actions.Clear();attackAt=Time.time+attack;skillAt=Time.time+remaining;switchAt=Time.time+swap;}
    public void RefreshWeapon()
    {
        if(Gear==null)return;
        string currentId=Gear.Main?.id;
        if(displayedWeaponId!=currentId){CancelPending();displayedWeaponId=currentId;}
        if(weapon!=null){weapon.SetActive(false);Destroy(weapon);}
        var visual=GetComponent<FantasyActorVisual>();if(visual==null||visual.model==null)return;
        Transform hand=null;
        foreach(var t in visual.model.GetComponentsInChildren<Transform>(true)){
            if(t.name=="handslot.r")hand=t;
            if(t.name=="1H_Sword"||t.name=="Badge_Shield")t.gameObject.SetActive(false);
        }
        var prefab=Resources.Load<GameObject>("CatWorld/Weapons/"+Gear.Weapon.ToString().ToLowerInvariant())??Resources.Load<GameObject>("AdventureWeapons/"+Gear.Weapon);
        if(prefab!=null&&hand!=null){weapon=Instantiate(prefab,hand,false);weapon.name="主武器外观";}
        hero.Health.RefreshVisuals();
    }
    void OnGUI()
    {
        if(PlayerHudPresenter.Running)return;
        if(hero==null||Gear==null||hero.GameplayPaused)return;
        var m=CombatUI.Begin();float x=CombatUI.Width/2+250,y=CombatUI.Height-86;
        CombatUI.Panel(new Rect(x,y-87,240,80));
        CombatUI.Text(new Rect(x+10,y-83,220,25),"手持："+(Gear.Main!=null?AdventureItems.TypeName(Gear.Main.type):"徒手"),17,CombatUI.Gold);
        CombatUI.Text(new Rect(x+10,y-57,220,45),"备用："+(Gear.Reserve!=null?AdventureItems.TypeName(Gear.Reserve.type):"未配置")+"\n"+PlayerInput.Key(PlayerAction.SwitchWeapon)+" 切换"+(SwitchRemaining>0?$" · {SwitchRemaining:0.0} 秒":" · 背包内配置"),15);
        CombatUI.Panel(new Rect(x,y,240,64));var icon=AdventureItems.Texture(AdventureItems.Icon(Gear.Weapon));if(icon!=null)GUI.DrawTexture(new Rect(x+8,y+10,42,42),icon,ScaleMode.ScaleToFit);
        CombatUI.Text(new Rect(x+58,y+5,180,25),PlayerInput.Key(PlayerAction.Skill)+"  "+SkillName,18,CombatUI.Gold);
        CombatUI.Text(new Rect(x+58,y+32,180,25),SkillRemaining>0?$"冷却 {SkillRemaining:0.0} 秒":ClassName+" · 就绪",16);
        GUI.matrix=m;
    }
}
public class AdventureProjectile : MonoBehaviour
{
    ThirdPersonHero hero;Vector3 direction;float damage,radius,speed,life;bool consumed;Material mat;GearItem source;bool skill;
    public static void Spawn(ThirdPersonHero owner,Vector3 p,Vector3 dir,float damage,float radius,float speed,GearItem source=null,bool skill=false)
    {
        var g=GameObject.CreatePrimitive(radius>0?PrimitiveType.Sphere:PrimitiveType.Capsule);var collider=g.GetComponent<Collider>();collider.enabled=false;Destroy(collider);
        g.name=source!=null&&source.type==GearType.Bow?"主角箭矢":source!=null&&source.type==GearType.Sword?"主角剑气":source!=null&&source.type==GearType.Spear?"主角枪芒":"主角火球";g.transform.position=p;g.transform.rotation=Quaternion.LookRotation(dir)*Quaternion.Euler(90,0,0);g.transform.localScale=radius>0?Vector3.one*.32f:new Vector3(.08f,.38f,.08f);
        var shot=g.AddComponent<AdventureProjectile>();shot.hero=owner;shot.source=source?.Clone();shot.skill=skill;shot.direction=dir.normalized;shot.damage=damage;shot.radius=radius;shot.speed=speed;shot.life=2.5f;
        shot.mat=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=radius>0?new Color(1,.4f,.08f):new Color(.75f,.9f,.65f)};g.GetComponent<Renderer>().sharedMaterial=shot.mat;
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(g,owner.gameObject.scene);
    }
    void Update()
    {
        if(consumed)return;
        if(hero==null||hero.Health.Dead){Dispose();return;}if(hero.GameplayPaused||Time.timeScale<=0)return;
        life-=Time.deltaTime;
        if(life<=0){Dispose();return;}
        float distance=speed*Time.deltaTime;
        var hits=Physics.SphereCastAll(transform.position,.16f,direction,distance,~0,QueryTriggerInteraction.Ignore);System.Array.Sort(hits,(a,b)=>a.distance.CompareTo(b.distance));
        foreach(var h in hits){if(h.collider.GetComponentInParent<ThirdPersonHero>()!=null)continue;Impact(h.point,h.collider);return;}
        transform.position+=direction*distance;
    }
    void Dispose(){consumed=true;gameObject.SetActive(false);Destroy(gameObject);}
    void Impact(Vector3 p,Collider c)
    {
        if(consumed)return;consumed=true;
        if(radius>1){
            var seen=new HashSet<Component>();
            foreach(var hit in Physics.OverlapSphere(p,radius)){
                var e=hit.GetComponentInParent<CombatEnemy>();var n=hit.GetComponentInParent<AdventureResource>();Component t=e!=null?(Component)e:n;
                if(t==null||!seen.Add(t)||!AdventureCombat.Sight(p-direction*.2f,t.transform.position+Vector3.up,t))continue;
                if(e!=null)WeaponHit.Apply(hero,e,damage,p,direction,source,skill);else n.Hit(damage,hero);
            }
        }else{var e=c.GetComponentInParent<CombatEnemy>();var n=c.GetComponentInParent<AdventureResource>();if(e!=null)WeaponHit.Apply(hero,e,damage,p,direction,source,skill);else if(n!=null)n.Hit(damage,hero);}
        AdventurePulse.Spawn(p,Mathf.Max(.5f,radius),mat.color,gameObject.scene);Dispose();
    }
    public static void ClearOwner(ThirdPersonHero owner){if(owner==null)return;foreach(var p in FindObjectsByType<AdventureProjectile>(FindObjectsSortMode.None))if(p.hero==owner)p.Dispose();}
    public static void Clear(UnityEngine.SceneManagement.Scene scene){foreach(var p in FindObjectsByType<AdventureProjectile>(FindObjectsSortMode.None))if(p.gameObject.scene==scene){p.gameObject.SetActive(false);Destroy(p.gameObject);}}
    void OnDestroy(){if(mat!=null)Destroy(mat);}
}
public class AdventurePulse : MonoBehaviour
{
    float until,start;LineRenderer line;Material mat;float radius;
    bool footprint;
    public static void SpawnMelee(Transform actor,float reach,float dot,float halfWidth,Color tint)
    {
        var v=Spawn(actor.position+Vector3.up*.08f,reach,tint,actor.gameObject.scene);v.footprint=true;
        float angle=Mathf.Acos(Mathf.Clamp(dot,-1,1));
        bool full=dot<=-1;int n=full?49:51;v.line.positionCount=n;
        for(int i=0;i<n;i++){
            if(!full&&(i==0||i==n-1)){v.line.SetPosition(i,v.transform.position);continue;}
            float u=full?i/48f:(i-1)/48f;float a=Mathf.Lerp(-angle,angle,u);
            float lateral=Mathf.Abs(Mathf.Sin(a));float length=lateral>.0001f?Mathf.Min(reach,halfWidth/lateral):reach;
            v.line.SetPosition(i,v.transform.position+actor.rotation*new Vector3(Mathf.Sin(a)*length,0,Mathf.Cos(a)*length));
        }
    }
    public static AdventurePulse Spawn(Vector3 p,float radius,Color color,UnityEngine.SceneManagement.Scene scene=default){var g=new GameObject("攻击范围反馈");if(scene.IsValid()&&scene.isLoaded)UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(g,scene);g.transform.position=p;var v=g.AddComponent<AdventurePulse>();v.radius=radius;v.start=Time.time;v.until=Time.time+.24f;v.line=g.AddComponent<LineRenderer>();v.line.positionCount=49;v.line.startWidth=v.line.endWidth=.055f;v.mat=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=color};v.line.sharedMaterial=v.mat;return v;}
    void Update(){if(Time.time>=until){Destroy(gameObject);return;}if(footprint)return;float r=radius*Mathf.Lerp(.6f,1,(Time.time-start)/.24f);for(int i=0;i<49;i++){float a=i*Mathf.PI*2/48;line.SetPosition(i,transform.position+new Vector3(Mathf.Cos(a)*r,0,Mathf.Sin(a)*r));}}
    void OnDestroy(){if(mat!=null)Destroy(mat);}
}


