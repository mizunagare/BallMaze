using System;
using System.Collections.Generic;
using UnityEngine;

// Ephemeral scene ownership only. Never a Profile, Run, CombatSession or fictitious wave.
public sealed class TrainingLootContext : MonoBehaviour
{
    static readonly Dictionary<UnityEngine.SceneManagement.Scene,TrainingLootContext> scenes = new Dictionary<UnityEngine.SceneManagement.Scene,TrainingLootContext>();
    AdventureRandomState streams;
    ThirdPersonHero hero;
    bool initialized;
    public int CompletedDeaths { get; private set; }
    public string RandomFingerprint => JsonUtility.ToJson(streams);
    internal AdventureRandomState Streams => streams;
    public static int ActiveCount => scenes.Count;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void ResetRegistry() { scenes.Clear(); }

    public void Initialize(int seed)
    {
        if(initialized)throw new InvalidOperationException("训练掉落上下文不能重置或复用。");
        RequireTemporaryScene();
        if(scenes.ContainsKey(gameObject.scene))throw new InvalidOperationException("训练场存在重复掉落上下文。");
        streams=AdventureRandom.Create(seed);initialized=true;
        scenes.Add(gameObject.scene,this);
    }
    public void BindHero(ThirdPersonHero owner)
    {
        if(!initialized||owner==null||owner.gameObject.scene!=gameObject.scene||owner.GetComponent<CP05TrainingMarker>()==null)
            throw new InvalidOperationException("训练掉落必须绑定本场角色。");
        if(hero!=null&&hero!=owner)throw new InvalidOperationException("训练掉落角色不能替换。");
        hero=owner;
    }
    void RequireTemporaryScene()
    {
        foreach(var root in gameObject.scene.GetRootGameObjects())
            if(root.GetComponentInChildren<CombatSession>(true)!=null||root.GetComponentInChildren<AdventureFlow>(true)!=null)
                throw new InvalidOperationException("正式冒险场景不能注册训练掉落上下文。");
    }
    internal static TrainingLootContext For(Component owner)
    {
        if(owner==null||!scenes.TryGetValue(owner.gameObject.scene,out var context))return null;
        if(context==null||!context.isActiveAndEnabled)throw new InvalidOperationException("训练掉落上下文已失效。");
        context.RequireTemporaryScene();
        return context;
    }
    internal static TrainingLootContext ForDeath(CombatEnemy enemy)
    {
        var context=For(enemy);
        if(context==null){
            if(enemy.target!=null&&enemy.target.GetComponent<CP05TrainingMarker>()!=null)
                throw new InvalidOperationException("训练敌人缺少有效的临时掉落上下文。");
            return null;
        }
        if(context.hero==null||enemy.target!=context.hero)throw new InvalidOperationException("训练敌人与角色不属于同一临时上下文。");
        return context;
    }
    internal void CompleteDeath() { CompletedDeaths++; }
    internal GearItem RollEquipment(CombatEnemy enemy) => AdventureItems.RollTraining(enemy);
    void OnEnable() { if(initialized){RequireTemporaryScene();if(scenes.TryGetValue(gameObject.scene,out var other)&&other!=this)throw new InvalidOperationException("训练场存在重复掉落上下文。");scenes[gameObject.scene]=this;} }
    void OnDisable() { if(scenes.TryGetValue(gameObject.scene,out var registered)&&registered==this)scenes.Remove(gameObject.scene); }
    void OnDestroy() { OnDisable();streams=null;hero=null; }
}
