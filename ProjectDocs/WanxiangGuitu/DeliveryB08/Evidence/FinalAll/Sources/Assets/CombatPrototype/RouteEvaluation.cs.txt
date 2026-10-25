using System;
using System.Linq;
using UnityEngine;

[Serializable] public class RouteRisk {
    public int destinationEnemies, pathEnemies, pathElites;
    public float destinationThreat, pathThreat, eliteExposure, totalPenalty;
}
[Serializable] public class RouteExitEvaluation {
    public string id, label, availability, reason, pathStatus;
    public int repairWood, repairStone;
    public bool usable, requiresRepair;
    public float distance = -1, duration, cost;
}
[Serializable] public class RouteEvaluation {
    public string poiId, label, pathStatus, targetBasis;
    public int configurationVersion;
    public bool reachable, exitAvailable, eligible;
    public float targetMatch, expectedYield, extractionConvenience, novelty, distanceCost, totalScore;
    public float navigationDistance, bypassDistance = -1, expectedGear, expectedMaterialUnits;
    public float[] expectedMaterials = new float[6];
    public int remainingNodes, unopenedChests, livingEnemies, groundGroups, groundGearCount;
    public string noveltyBasis = "未完成来源比例（不代表未到访）";
    public string chosenExit;
    public string[] exclusionReasons = new string[0];
    public Vector3[] path = new Vector3[0];
    public RouteRisk risk = new RouteRisk();
    public RouteExitEvaluation[] exits = new RouteExitEvaluation[0];
}

// One versioned, editable resource owns all scoring/caching thresholds. No UI weights.
[Serializable] public class RouteScoringConfig {
    public int version;
    public float targetWeight, yieldWeight, extractionWeight, noveltyWeight, distanceWeight;
    public float destinationRiskWeight, pathRiskWeight, eliteRiskWeight;
    public float yieldReference, distanceReference, enemyReference, pathEnemyReference;
    public float gearMaterialEquivalent, exitDistanceReference, exitDurationReference, repairSurcharge;
    public float perceptionBuffer, cacheSeconds;
    static RouteScoringConfig loaded;
    public static RouteScoringConfig Read() {
        if (loaded == null) {
            var resource = Resources.Load<TextAsset>("RouteScoring");
            if (resource == null) throw new InvalidOperationException("缺少路线评分配置 RouteScoring.json");
            var candidate = JsonUtility.FromJson<RouteScoringConfig>(resource.text);
            candidate.Validate(); loaded = candidate;
        }
        return JsonUtility.FromJson<RouteScoringConfig>(JsonUtility.ToJson(loaded));
    }
    public void Validate() {
        var values = GetType().GetFields().Where(f => f.FieldType == typeof(float)).Select(f => (float)f.GetValue(this));
        if (version != 1 || values.Any(v => float.IsNaN(v) || float.IsInfinity(v) || v < 0) ||
            yieldReference <= 0 || distanceReference <= 0 || enemyReference <= 0 || pathEnemyReference <= 0 ||
            exitDistanceReference <= 0 || exitDurationReference <= 0 || cacheSeconds <= 0)
            throw new System.IO.InvalidDataException("路线评分配置无效");
    }
}
