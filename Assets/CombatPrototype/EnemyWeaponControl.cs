using UnityEngine;
// Transient opt-in weapon control. Not serialized; Bosses immune. Released threats remain owned by their projectiles.
public sealed class EnemyWeaponControl:MonoBehaviour {
 float guardUntil,pullLeft;ThirdPersonHero puller;CombatEnemy enemy;public bool Controlled=>GuardBroken||pullLeft>0;public float PullRemaining=>pullLeft;public bool GuardBroken=>Time.time<guardUntil;public bool Immune=>enemy.archetype==EnemyArchetype.Boss||GetComponent<ForestBossBrain>()!=null;
 void Awake(){enemy=GetComponent<CombatEnemy>();}
 public bool Break(float duration){if(Immune||enemy.Health.Dead)return false;guardUntil=Mathf.Max(guardUntil,Time.time+duration);return true;}
 public bool Pull(ThirdPersonHero hero,float seconds){if(Immune||enemy.Health.Dead||hero==null)return false;puller=hero;pullLeft=seconds;return true;}
 void Update(){if(pullLeft<=0)return;if(puller==null||puller.Health.Dead||enemy.Health.Dead||Immune){pullLeft=0;return;}if(puller.GameplayPaused||Time.timeScale<=0)return;pullLeft=Mathf.Max(0,pullLeft-Time.deltaTime);Vector3 delta=Vector3.ProjectOnPlane(puller.transform.position-transform.position,Vector3.up);if(delta.magnitude<=1){pullLeft=0;return;}if(!AdventureCombat.Sight(transform.position+Vector3.up*.8f,puller.transform.position+Vector3.up*.8f,puller)){pullLeft=0;return;}var cc=GetComponent<CharacterController>();if(cc==null||!cc.enabled){pullLeft=0;return;}var rb=GetComponent<Rigidbody>();float mass=rb!=null?Mathf.Max(1,rb.mass):enemy.archetype==EnemyArchetype.Elite?2:1;float speed=Mathf.Min(enemy.speed,3.2f)/mass;cc.Move(delta.normalized*Mathf.Min(speed*Time.deltaTime,delta.magnitude-1)+Vector3.down*2*Time.deltaTime);}
 void OnDisable(){guardUntil=0;pullLeft=0;puller=null;}
}
