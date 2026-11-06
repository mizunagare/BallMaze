using System;
using System.Linq;
using UnityEngine;

// C2.4-only candidate configuration. Existing weapons, forest bosses and RNG are untouched.
public static class CrystalCavernBossRules
{
    public const float Health = 360, Speed = 2.1f, ReentrySafety = 2;
    public enum Attack { Claw, Volley, CrossLines, HollowRing }
    public readonly struct Move
    {
        public readonly float windup, recovery, damage, range;
        public Move(float windup, float recovery, float damage, float range)
        { this.windup=windup; this.recovery=recovery; this.damage=damage; this.range=range; }
    }
    public static Move Definition(Attack attack, bool phase2)
    {
        switch (attack)
        {
            case Attack.Claw: return new Move(1.2f, phase2?1.05f:1.35f, phase2?18:16, 3.6f);
            case Attack.Volley: return new Move(1.35f, phase2?1.15f:1.4f, phase2?12:10, 18);
            case Attack.CrossLines: return new Move(1.5f, 1.65f, 20, 8);
            case Attack.HollowRing: return new Move(1.6f, 1.8f, 22, 6);
            default: throw new ArgumentOutOfRangeException(nameof(attack));
        }
    }
    static readonly Attack[] First = { Attack.Claw, Attack.Volley, Attack.Claw };
    static readonly Attack[] Second = { Attack.CrossLines, Attack.Volley, Attack.HollowRing, Attack.Claw };
    public static Attack Next(int sequence, bool phase2) => phase2 ? Second[sequence%Second.Length] : First[sequence%First.Length];
    public static bool InsideArena(Vector3 p) => p.x >= 98 && p.x <= 130 && p.z >= 392 && p.z <= 430;
    public static bool Exact(ForestLayout map, CombatEnemy enemy) =>
        CrystalCavernLayout.HasBoss(map) && enemy != null && enemy.entityId == CrystalCavernLayout.BossId &&
        enemy.archetype == EnemyArchetype.Boss && enemy.GetComponent<CrystalCavernBossBrain>() != null;

    // Shared by navigation annotations and route scoring. Presence in the optional branch
    // is not exposure. Clip each segment to the arena before applying the old distance test.
    public static bool RouteExposure(ForestLayout map, CombatEnemy enemy, Vector3[] path, float buffer)
    {
        if (!Exact(map,enemy) || enemy.Health.Dead || !enemy.gameObject.activeInHierarchy ||
            !enemy.GetComponent<CrystalCavernBossBrain>().ChallengeCommitted || path == null || path.Length == 0) return false;
        if (path.Length == 1) return InsideArena(path[0]) && RouteScoring.NearPath(enemy,path,buffer);
        for (int i=1;i<path.Length;i++)
            if (ClipArena(path[i-1],path[i],out var a,out var b) &&
                ForestTerrain.FlatSegment(enemy.transform.position,a,b)<enemy.detectionRange+buffer) return true;
        return false;
    }
    static bool ClipArena(Vector3 a, Vector3 b, out Vector3 start, out Vector3 end)
    {
        float lo=0,hi=1; var delta=b-a;
        bool Axis(float p,float d,float min,float max)
        {
            if(Mathf.Abs(d)<.00001f)return p>=min&&p<=max;
            float x=(min-p)/d,y=(max-p)/d;
            if(x>y){float t=x;x=y;y=t;}
            lo=Mathf.Max(lo,x);hi=Mathf.Min(hi,y);return lo<=hi;
        }
        bool valid=Axis(a.x,delta.x,98,130)&&Axis(a.z,delta.z,392,430);
        start=a+delta*lo;end=a+delta*hi;return valid;
    }
    public static bool Challenged(CombatSession session) => session != null &&
        session.Flow.ActiveRun?.contentRevision == CrystalCavernLayout.Content24 &&
        session.Events.Points.Any(p=>p.entityId==CrystalCavernLayout.Challenge&&p.Used);
}
