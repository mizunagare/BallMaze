using UnityEngine;
public static class CombatAssistOptions {
 public const string Stage="B1";
 public static bool Ranged=false,Melee=false;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]static void Reset(){Ranged=false;Melee=false;}
}
