using UnityEngine;
public static class CombatAssistOptions {
 public const string Stage="B3";
 public static bool Ranged=true,Melee=true;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]static void Reset(){Ranged=true;Melee=true;}
}
