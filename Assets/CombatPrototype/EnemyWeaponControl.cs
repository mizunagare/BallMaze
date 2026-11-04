using UnityEngine;
// Transient opt-in weapon control. Not serialized; Bosses immune. Released threats remain owned by their projectiles.
public sealed class EnemyWeaponControl:MonoBehaviour {
 float guardUntil;CombatEnemy enemy;public bool GuardBroken=>Time.time<guardUntil;public bool Immune=>enemy.archetype==EnemyArchetype.Boss||GetComponent<ForestBossBrain>()!=null;
 void Awake(){enemy=GetComponent<CombatEnemy>();}
 public bool Break(float duration){if(Immune||enemy.Health.Dead)return false;guardUntil=Mathf.Max(guardUntil,Time.time+duration);return true;}
 void OnDisable(){guardUntil=0;}
}
