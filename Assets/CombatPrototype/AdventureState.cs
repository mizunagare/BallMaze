using System;
using UnityEngine;
[Serializable] public class ProfileState
{
    public bool hasCamp;
    public string profileId;
    // JsonUtility inline classes cannot reliably round-trip null. An invalid type
    // already means "untracked" to all v9 consumers; existing valid targets are retained.
    public CraftingTarget craftingTarget=new CraftingTarget{type=(GearType)(-1),quality=GearQuality.White,containerId=""};
    public bool hasTutorial;
    public TutorialState tutorial;
    public GearItem[] warehouse=new GearItem[0];
    public int[] materials=new int[6];
    public string[] unlockedRecipes=new string[0], committedRuns=new string[0], badges=new string[0], regions=new string[0];
    public PendingReward[] pending=new PendingReward[0];
    public CombatCheckpoint camp;
    public BossHuntRecord[] bossHunts=new BossHuntRecord[0];
    public SpecialRewardReceipt[] specialRewards = Array.Empty<SpecialRewardReceipt>();
    public ObjectiveHistoryEntry[] objectiveHistory = Array.Empty<ObjectiveHistoryEntry>();
    public bool objectiveHistoryLegacyUnknown;
}
[Serializable] public sealed class ObjectiveHistoryEntry
{
    public string runId, objectiveId, regionId, completedAtUtc, committedAtUtc, displayNameSnapshot;
    public string SettlementId => runId + ":terminal";
    public static string UtcNow() => DateTime.UtcNow.ToString("o", System.Globalization.CultureInfo.InvariantCulture);
    public static bool ValidTime(string value)
    {
        return value != null && value.Length == 28 && value[27] == 'Z' &&
            DateTime.TryParseExact(value, "o", System.Globalization.CultureInfo.InvariantCulture,
                System.Globalization.DateTimeStyles.RoundtripKind, out var time) && time.Kind == DateTimeKind.Utc;
    }
    public bool SameKey(ObjectiveHistoryEntry other) =>
        runId == other.runId && SettlementId == other.SettlementId && objectiveId == other.objectiveId;
}
public enum AdventureMode { TestChallenge, EndlessWaves, ForestExploration }
public enum ExpeditionGoal { Gather, Treasure, Challenge }
public enum ItemOrigin { Unspecified, DeploymentProtected, RunLoot, LegacyProtected }
public enum RunPhase { Running, Extracting, OutcomePending }
public enum AdventureOutcome { Extracted, Death, Abandoned, TestChallengeComplete }
public enum SettlementStatus { Pending, Committed }
[Serializable] public class RunState
{
    public bool ruinsR1;
    public bool hasRandomStreams;
    public AdventureRandomState randomStreams;
    public string runId,region="ForestRuins";
    public AdventureMode mode;
    public ExpeditionGoal goal;
    public string regionInstanceId,contentRevision="B05-1";
    public int supplySlots=6,materialStack=99,potionStack=5;
    public int seed,generationVersion=1,targetWave=5;
    public RunPhase phase;
    public bool legacyProtected,targetReached;
    public GearItem[] entryGear=new GearItem[0];
    public string entryMain,entryReserve;
    public int[] broughtRemaining=new int[6], earnedRemaining=new int[6];
    public int broughtPotions,earnedPotions;
    public string exitId;
    public float extractionRemaining;
    public CombatCheckpoint checkpoint;
    public string[] pendingRecipeProofs=new string[0];
}
[Serializable] public class PendingReward
{
    public string pendingId,sourceRunId,reason;
    public bool equipment;
    public GearItem item;
    public MaterialKind material;
    public int amount;
}
[Serializable] public class SettlementRecord
{
    public string settlementId,runId;
    public AdventureOutcome outcome;
    public SettlementStatus status;
    public bool acknowledged,legacyProtection;
    public GearItem[] returnedGear=new GearItem[0], keptGear=new GearItem[0], lostGear=new GearItem[0];
    public int[] returnedMaterials=new int[6],keptMaterials=new int[6],lostMaterials=new int[6];
    public int returnedPotions,lostPotions,lostLevel;
    public int[] clearedSkills=new int[6];
    public string[] permanentUnlocks=new string[0];
    public ProfileState plan;
}
public static class AdventureData
{
    [Serializable] class Box<T>{public T value;}
    public static T Clone<T>(T value)=>value==null?default(T):JsonUtility.FromJson<Box<T>>(JsonUtility.ToJson(new Box<T>{value=value})).value;
    public static CombatCheckpoint World(CombatSaveData data){var c=Clone<CombatCheckpoint>(data);c.warehouseGear=null;c.warehouseMaterials=null;c.unlockedRecipes=null;return c;}
}

