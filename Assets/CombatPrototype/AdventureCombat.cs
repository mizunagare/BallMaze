using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class AdventureCombat : MonoBehaviour
{
    public AdventureLoadout Gear { get; private set; }
    ThirdPersonHero hero;
    float attackAt, skillAt, switchAt;
    public float AttackRemaining=>Mathf.Max(0,attackAt-Time.time);
    public float SwitchRemaining=>Mathf.Max(0,switchAt-Time.time);
    public void EquipmentChanged(){attackAt=Mathf.Max(attackAt,Time.time+.25f);}
    public bool SwitchWeapon(){if(!Ready||Time.time<switchAt||!Gear.SwapWeapons())return false;switchAt=Time.time+.7f;EquipmentChanged();return true;}
    GameObject weapon;
    public float SkillDuration=>7+(WeaponTraits.Has(Gear.Main,5)?1:0);
    public float SkillRemaining => Mathf.Max(0, skillAt-Time.time);
    public string ClassName => new[] {"剑战士","枪卫士","法杖法师","弓游侠"}[(int)Gear.Weapon];
    public string SkillName => new[] {"旋风横扫","贯穿突刺","陨火爆裂","扇形箭雨"}[(int)Gear.Weapon];
    public string SkillDescription => new[] {"周围 4 米造成 200% 攻击伤害", "前方 7 米直线造成 240% 攻击伤害", "前方火球命中后 4 米范围造成 220% 伤害", "发射 5 支箭，每支造成 120% 攻击伤害"}[(int)Gear.Weapon];
    void Awake() { hero=GetComponent<ThirdPersonHero>(); Gear=GetComponent<AdventureLoadout>(); if(Gear==null)Gear=gameObject.AddComponent<AdventureLoadout>(); }
    void Update() {var k=Keyboard.current;if(k==null)return;if(k.vKey.wasPressedThisFrame)SwitchWeapon();if(k.fKey.wasPressedThisFrame)UseSkill();}
    bool Ready => hero!=null&&!hero.Health.Dead&&!hero.GameplayPaused&&Time.timeScale>0&&!hero.Dodge.IsRolling&&hero.Inventory.ClosedFrame!=Time.frameCount&&!(AdventureFlow.Find(hero)?.BlockCombat==true);
    public bool Strike()
    {
        if(!Ready||Time.time<attackAt)return false;
        attackAt=Time.time+hero.AttackInterval*(WeaponTraits.Has(Gear.Main,1)?.82f:1);
        bool ranged=(int)Gear.Weapon>=2;
        GetComponent<FantasyActorVisual>()?.Attack(ranged);
        CombatFeedback.Find(this)?.Swing(hero);
        if(ranged) Fire(transform.forward,hero.AttackPower,Gear.Weapon==GearType.Staff?.9f:0,Gear.Weapon==GearType.Bow?23:16);
        else Melee(Gear.Weapon==GearType.Spear?3.8f+hero.Progression.ReachBonus:hero.AttackRange,hero.AttackPower,Gear.Weapon==GearType.Spear?.88f:.25f);
        return true;
    }
    public bool UseSkill()
    {
        if(!Ready||Time.time<skillAt)return false;
        skillAt=Time.time+7+(WeaponTraits.Has(Gear.Main,5)?1:0);
        GetComponent<FantasyActorVisual>()?.Attack((int)Gear.Weapon>=2); CombatFeedback.Find(this)?.Swing(hero);
        float area=WeaponTraits.Has(Gear.Main,2)?1.25f:1;
        int q=Gear.Main==null?0:(int)Gear.Main.quality;
        switch(Gear.Weapon){
            case GearType.Sword: Melee(4*area,hero.AttackPower*2,-1,true); if(q>=2){int n=q>=3?1:0;for(int i=-n;i<=n;i++)Fire(Quaternion.Euler(0,i*18,0)*transform.forward,hero.AttackPower*.75f,q>=4?1.8f:0,19,true);}break;
            case GearType.Spear: Melee(7*area,hero.AttackPower*2.4f,.94f,true);if(q>=2)Melee(9*area,hero.AttackPower*.8f,q>=3?.80f:.94f,true,q>=3?1.6f:.85f);if(q>=4)Fire(transform.forward,hero.AttackPower,2,25,true);break;
            case GearType.Staff: Fire(transform.forward,hero.AttackPower*2.2f,(q>=2?5:4)*area,14,true);if(q>=3)for(int i=-1;i<=1;i+=2)Fire(Quaternion.Euler(0,i*22,0)*transform.forward,hero.AttackPower*.8f,(q>=4?3:1.6f)*area,14,true);break;
            case GearType.Bow:for(int i=-(q>=4?4:q>=2?3:2);i<=(q>=4?4:q>=2?3:2);i++)Fire(Quaternion.Euler(0,i*12*area,0)*transform.forward,hero.AttackPower*1.2f,q>=3?1.5f:0,23,true);break;
        }
        return true;
    }
    void Fire(Vector3 dir,float damage,float radius,float speed,bool skill=false) { AdventureProjectile.Spawn(hero,transform.position+Vector3.up*1.25f+transform.forward*.7f,dir,damage,radius,speed,Gear.Main,skill); }
    void Melee(float radius,float damage,float dot,bool skill=false,float width=.85f)
    {
        var visited=new HashSet<Component>();
        foreach(var c in Physics.OverlapSphere(transform.position+Vector3.up,radius)){
            var enemy=c.GetComponentInParent<CombatEnemy>(); var node=c.GetComponentInParent<AdventureResource>();
            Component target=enemy!=null?(Component)enemy:node;
            if(target==null||!visited.Add(target))continue;
            Vector3 aim=target.transform.position+Vector3.up;
            Vector3 toward=Vector3.ProjectOnPlane(aim-transform.position,Vector3.up);
            if(toward.sqrMagnitude>.01f&&Vector3.Dot(transform.forward,toward.normalized)<dot)continue;
            if(Gear.Weapon==GearType.Spear && Mathf.Abs(Vector3.Dot(transform.right,toward))>width)continue;
            if(!Sight(transform.position+Vector3.up,aim,target))continue;
            if(enemy!=null)WeaponHit.Apply(hero,enemy,damage,aim,toward,Gear.Main,skill);else node.Hit(damage,hero);
        }
        AdventurePulse.Spawn(transform.position+Vector3.up*.08f,radius,new Color(.9f,.7f,.25f));
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
    public void ResetCombat(){attackAt=skillAt=switchAt=0;AdventureProjectile.Clear(gameObject.scene);}
    public void RestoreCooldown(float remaining,float attack=.2f,float swap=0){attackAt=Time.time+attack;skillAt=Time.time+remaining;switchAt=Time.time+swap;}
    public void RefreshWeapon()
    {
        if(Gear==null)return;
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
        CombatUI.Text(new Rect(x+10,y-57,220,45),"备用："+(Gear.Reserve!=null?AdventureItems.TypeName(Gear.Reserve.type):"未配置")+"\nV 切换"+(SwitchRemaining>0?$" · {SwitchRemaining:0.0} 秒":" · 背包内配置"),15);
        CombatUI.Panel(new Rect(x,y,240,64));var icon=AdventureItems.Texture(AdventureItems.Icon(Gear.Weapon));if(icon!=null)GUI.DrawTexture(new Rect(x+8,y+10,42,42),icon,ScaleMode.ScaleToFit);
        CombatUI.Text(new Rect(x+58,y+5,180,25),"F  "+SkillName,18,CombatUI.Gold);
        CombatUI.Text(new Rect(x+58,y+32,180,25),SkillRemaining>0?$"冷却 {SkillRemaining:0.0} 秒":ClassName+" · 就绪",16);
        GUI.matrix=m;
    }
}
public class AdventureProjectile : MonoBehaviour
{
    ThirdPersonHero hero;Vector3 direction;float damage,radius,speed,life;Material mat;GearItem source;bool skill;
    public static void Spawn(ThirdPersonHero owner,Vector3 p,Vector3 dir,float damage,float radius,float speed,GearItem source=null,bool skill=false)
    {
        var g=GameObject.CreatePrimitive(radius>0?PrimitiveType.Sphere:PrimitiveType.Capsule);Destroy(g.GetComponent<Collider>());
        g.name=source!=null&&source.type==GearType.Bow?"主角箭矢":source!=null&&source.type==GearType.Sword?"主角剑气":source!=null&&source.type==GearType.Spear?"主角枪芒":"主角火球";g.transform.position=p;g.transform.rotation=Quaternion.LookRotation(dir)*Quaternion.Euler(90,0,0);g.transform.localScale=radius>0?Vector3.one*.32f:new Vector3(.08f,.38f,.08f);
        var shot=g.AddComponent<AdventureProjectile>();shot.hero=owner;shot.source=source?.Clone();shot.skill=skill;shot.direction=dir.normalized;shot.damage=damage;shot.radius=radius;shot.speed=speed;shot.life=Time.time+2.5f;
        shot.mat=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=radius>0?new Color(1,.4f,.08f):new Color(.75f,.9f,.65f)};g.GetComponent<Renderer>().sharedMaterial=shot.mat;
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(g,owner.gameObject.scene);
    }
    void Update()
    {
        if(hero==null||hero.Health.Dead){Destroy(gameObject);return;}if(hero.GameplayPaused||Time.timeScale<=0)return;
        if(Time.time>=life){Destroy(gameObject);return;}
        float distance=speed*Time.deltaTime;
        var hits=Physics.SphereCastAll(transform.position,.16f,direction,distance,~0,QueryTriggerInteraction.Ignore);System.Array.Sort(hits,(a,b)=>a.distance.CompareTo(b.distance));
        foreach(var h in hits){if(h.collider.GetComponentInParent<ThirdPersonHero>()!=null)continue;Impact(h.point,h.collider);return;}
        transform.position+=direction*distance;
    }
    void Impact(Vector3 p,Collider c)
    {
        if(radius>1){
            var seen=new HashSet<Component>();
            foreach(var hit in Physics.OverlapSphere(p,radius)){
                var e=hit.GetComponentInParent<CombatEnemy>();var n=hit.GetComponentInParent<AdventureResource>();Component t=e!=null?(Component)e:n;
                if(t==null||!seen.Add(t)||!AdventureCombat.Sight(p-direction*.2f,t.transform.position+Vector3.up,t))continue;
                if(e!=null)WeaponHit.Apply(hero,e,damage,p,direction,source,skill);else n.Hit(damage,hero);
            }
        }else{var e=c.GetComponentInParent<CombatEnemy>();var n=c.GetComponentInParent<AdventureResource>();if(e!=null)WeaponHit.Apply(hero,e,damage,p,direction,source,skill);else if(n!=null)n.Hit(damage,hero);}
        AdventurePulse.Spawn(p,Mathf.Max(.5f,radius),mat.color);Destroy(gameObject);
    }
    public static void Clear(UnityEngine.SceneManagement.Scene scene){foreach(var p in FindObjectsByType<AdventureProjectile>(FindObjectsSortMode.None))if(p.gameObject.scene==scene){p.gameObject.SetActive(false);Destroy(p.gameObject);}}
    void OnDestroy(){if(mat!=null)Destroy(mat);}
}
public class AdventurePulse : MonoBehaviour
{
    float until,start;LineRenderer line;Material mat;float radius;
    public static void Spawn(Vector3 p,float radius,Color color){var g=new GameObject("攻击范围反馈");g.transform.position=p;var v=g.AddComponent<AdventurePulse>();v.radius=radius;v.start=Time.time;v.until=Time.time+.24f;v.line=g.AddComponent<LineRenderer>();v.line.positionCount=49;v.line.startWidth=v.line.endWidth=.055f;v.mat=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=color};v.line.sharedMaterial=v.mat;}
    void Update(){if(Time.time>=until){Destroy(gameObject);return;}float r=radius*Mathf.Lerp(.6f,1,(Time.time-start)/.24f);for(int i=0;i<49;i++){float a=i*Mathf.PI*2/48;line.SetPosition(i,transform.position+new Vector3(Mathf.Cos(a)*r,0,Mathf.Sin(a)*r));}}
    void OnDestroy(){if(mat!=null)Destroy(mat);}
}


