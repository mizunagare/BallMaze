using UnityEngine;

// Presentation only: collision, damage, inventory and wave logic remain on the actor root.
public class FantasyActorVisual : MonoBehaviour
{
    public GameObject[] skins;
    public GameObject model;
    public int skinIndex;
    public bool isHero;
    Animation animationPlayer;
    CombatHealth health;
    ThirdPersonHero hero;
    CombatEnemy enemy;
    Vector3 previousPosition;
    float actionUntil;
    bool dead;
    [Min(0)] public float corpseHoldSeconds=.35f;
    public bool DeathVisualHidden {get;private set;}
    public void ResetDeathVisual(){DeathVisualHidden=false;dead=false;poseTime=0;current=null;if(model!=null)model.SetActive(true);}
    public void HideRestoredDeath(){if(!isHero&&model!=null){model.SetActive(false);DeathVisualHidden=true;dead=true;}}
    string current;
    float poseTime,actionStarted;string actionClip;
    public string Motion {get;private set;}="Idle";
    public float PoseTime=>poseTime;
    public bool IsDeathMotionPlaying=>isHero&&health!=null&&health.Dead&&(!dead||poseTime<Length("Death_A"));
    public float ObservedSpeed {get;private set;}
    public int BoundBones {get{int count=0;if(model!=null)foreach(var part in model.GetComponentsInChildren<SkinnedMeshRenderer>(true))count+=part.bones.Length;return count;}}
    Material weaponTint, shieldTint;
    Renderer swordRenderer, shieldRenderer;
    Material originalSword, originalShield;
    GameObject shield;
    Vector3 modelRestPosition, recoilDirection;
    float recoilUntil;
    Quaternion modelRestRotation;

    void Awake() { health = GetComponent<CombatHealth>(); hero = GetComponent<ThirdPersonHero>(); enemy = GetComponent<CombatEnemy>(); Bind(); if(GetComponent<CatActorVisual>()==null)gameObject.AddComponent<CatActorVisual>(); }
    void OnEnable() { previousPosition = transform.position; actionUntil = 0; dead = false; current = null; }
    void Bind()
    {
        if (model == null) return;
        modelRestPosition = model.transform.localPosition;
        modelRestRotation = model.transform.localRotation;
        animationPlayer = model.GetComponentInChildren<Animation>(true);
        if(animationPlayer!=null){animationPlayer.Stop();animationPlayer.enabled=false;}
        previousPosition = transform.position;
        current = null; dead = false; actionUntil = 0;
        foreach (var t in model.GetComponentsInChildren<Transform>(true)) {
            if (t.name == "1H_Sword") swordRenderer = t.GetComponent<Renderer>();
            if (t.name == "Badge_Shield") { shield = t.gameObject; shieldRenderer = t.GetComponent<Renderer>(); }
        }
        originalSword = swordRenderer != null ? swordRenderer.sharedMaterial : null;
        originalShield = shieldRenderer != null ? shieldRenderer.sharedMaterial : null;
        if (isHero && shield != null) shield.SetActive(false);
        if (health != null) health.RefreshVisuals();
    }
    public void SetArchetype(EnemyArchetype type)
    {
        if (isHero || skins == null || skins.Length < 4) return;
        int index = (int)type;
        if (model == null || skinIndex != index) {
            if (model != null) { model.SetActive(false); Destroy(model); }
            model = Instantiate(skins[index], transform);
            model.name = "角色外观"; skinIndex = index;
            Bind();
        }
        float height = type == EnemyArchetype.Boss ? 3.3f : type == EnemyArchetype.Elite ? 2.4f : 2;
        model.transform.localScale = skins[index].transform.localScale * (height / 2);
        actionUntil = 0; dead = false; current = null;
        ResetRecoil();
        Play("Idle", true);
    }
    public void Attack(bool spell = false) => AttackTimed(spell,isHero ? AdventureCombat.ActionDuration(hero.AttackInterval) : .65f);
    public void AttackTimed(bool spell,float duration,bool skill=false)
    {
        if (health != null && health.Dead) return;
        string clip = spell ? "Spellcast_Shoot" : "1H_Melee_Attack_Slice_Horizontal";
        if (!spell && enemy != null && enemy.archetype == EnemyArchetype.Boss) clip = "2H_Melee_Attack_Slice";
        if(isHero && hero.GetComponent<AdventureLoadout>()!=null){var type=hero.GetComponent<AdventureLoadout>().Weapon; if(type==GearType.Sword&&skill)clip="2H_Melee_Attack_Spin";else if(type==GearType.Spear)clip="2H_Melee_Attack_Stab";else if(type==GearType.Bow)clip="2H_Ranged_Shoot";else if(type==GearType.Staff)clip="Spellcast_Shoot";}
        Play(clip, false, true);
        actionUntil = Time.time + duration;
        actionStarted=Time.time;actionClip=clip;Motion="Attack";
        if (animationPlayer != null && animationPlayer[clip] != null)
            animationPlayer[clip].speed = isHero ? animationPlayer[clip].length / Mathf.Max(.18f, actionUntil - Time.time) : 1;
    }
    public void CancelAttack(){if(Motion=="Attack"){actionUntil=0;actionClip=null;Motion="Idle";if(isHero&&hero!=null)CombatFeedback.Find(this)?.CancelStartup(hero);}}
    public void Hurt()
    {
        if (Time.time < actionUntil || health == null || health.Dead) return;
        Play("Hit_A", false, true); actionStarted=Time.time;actionClip="Hit_A";actionUntil = Time.time + .22f;Motion="Hit";
    }
    public void Recoil(Vector3 direction)
    {
        if (model == null) return;
        recoilDirection = transform.InverseTransformDirection(Vector3.ProjectOnPlane(direction, Vector3.up).normalized) * .08f;
        recoilUntil = Time.time + .16f;
    }
    public void ResetRecoil() { recoilUntil = 0; if (model != null) { model.transform.localPosition = modelRestPosition; model.transform.localRotation = modelRestRotation; } }
    public void SetEquipment(bool swordEquipped, int swordTier, bool armorEquipped, int armorTier)
    {
        if (!isHero || model == null) return;
        if (shield != null) shield.SetActive(armorEquipped);
        if (swordRenderer != null) {
            if (weaponTint == null) weaponTint = new Material(originalSword);
            weaponTint.color = swordTier >= 2 ? new Color(1, .72f, .2f) : new Color(.35f, .9f, 1);
            swordRenderer.sharedMaterial = swordEquipped ? weaponTint : originalSword;
        }
        if (shieldRenderer != null) {
            if (shieldTint == null) shieldTint = new Material(originalShield);
            shieldTint.color = armorTier >= 2 ? new Color(1, .75f, .25f) : new Color(.7f, .65f, .5f);
            shieldRenderer.sharedMaterial = armorEquipped ? shieldTint : originalShield;
        }
        if (health != null) health.RefreshVisuals();
    }
    void LateUpdate()
    {
        if (health == null || model == null) return;
        Vector3 displacement = transform.position - previousPosition;
        previousPosition = transform.position;
        bool camp=hero!=null&&AdventureFlow.Find(hero)?.AtCamp==true;
        bool paused=hero!=null&&hero.GameplayPaused||enemy!=null&&enemy.target!=null&&enemy.target.GameplayPaused;
        float dt=camp?Time.unscaledDeltaTime:Time.deltaTime;
        ObservedSpeed=dt>0?Vector3.ProjectOnPlane(displacement,Vector3.up).magnitude/dt:0;
        if(health.Dead){if(!dead){dead=true;poseTime=0;current=null;}Motion="Death";Play("Death_A",false);poseTime+=isHero&&!camp?Time.unscaledDeltaTime:Time.deltaTime;Sample();if(!isHero&&poseTime>=Length("Death_A")+Mathf.Clamp(corpseHoldSeconds,0,2))HideRestoredDeath();return;}
        if(dead){dead=false;actionUntil=0;current=null;poseTime=0;Play("Idle",true);Motion="Idle";Sample();ResetRecoil();}
        if(paused)return;
        if (hero != null && hero.Dodge != null && hero.Dodge.IsRolling) {
            Play("Idle", true);
            Motion="Dodge";Sample();
            float t = hero.Dodge.Progress;
            Quaternion roll = Quaternion.Euler(t * 360, 0, 0);
            model.transform.localRotation = roll * modelRestRotation;
            Vector3 pivot = Vector3.up;
            model.transform.localPosition = modelRestPosition + pivot - roll * pivot - Vector3.up * (.12f * Mathf.Sin(t * Mathf.PI));
            actionUntil = 0;
            return;
        }
        model.transform.localRotation = modelRestRotation;
        float recoilT = Mathf.Clamp01(1 - (recoilUntil - Time.time) / .16f);
        model.transform.localPosition = modelRestPosition + recoilDirection * Mathf.Sin(recoilT * Mathf.PI);
        if (dead) { dead = false; actionUntil = 0; current = null; }
        if(Time.time<actionUntil){Play(actionClip,false);Motion=actionClip=="Hit_A"?"Hit":"Attack";poseTime=Length(actionClip)*Mathf.Clamp01((Time.time-actionStarted)/Mathf.Max(.01f,actionUntil-actionStarted));Sample();return;}
        bool moving=ObservedSpeed>.2f;bool running=moving&&ObservedSpeed>(hero!=null?hero.moveSpeed*hero.MoveMultiplier+.5f:3.4f);
        Motion=moving?(running?"Run":"Walk"):"Idle";string clip=moving?(running?"Running_A":"Walking_A"):"Idle";Play(clip,true);
        if(moving)poseTime+=Vector3.ProjectOnPlane(displacement,Vector3.up).magnitude/(running?2.7f:1.65f)*Length(clip);else if(!camp)poseTime+=Time.deltaTime;
        Sample();model.transform.localRotation=modelRestRotation;model.transform.localPosition=modelRestPosition+recoilDirection*Mathf.Sin(recoilT*Mathf.PI);
    }
    void Play(string clip, bool loop, bool restart = false)
    {
        if(string.IsNullOrEmpty(clip))return;if(current!=clip||restart)poseTime=0;current=clip;
    }
    float Length(string clip)=>animationPlayer!=null&&animationPlayer[clip]!=null?animationPlayer[clip].length:1;
    void Sample(){if(animationPlayer!=null&&current!=null&&animationPlayer[current]!=null){var state=animationPlayer[current];float t=Motion=="Death"||Motion=="Hit"||Motion=="Attack"?Mathf.Min(poseTime,state.length):Mathf.Repeat(poseTime,Mathf.Max(.01f,state.length));state.clip.SampleAnimation(animationPlayer.gameObject,t);}}
    void OnDestroy() { if (weaponTint != null) Destroy(weaponTint); if (shieldTint != null) Destroy(shieldTint); }
}

