using UnityEngine;
public static class CombatAssistOptions {
 public const string Stage="B2";
 public static bool Ranged=true,Melee=false;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]static void Reset(){Ranged=true;Melee=false;}
}
