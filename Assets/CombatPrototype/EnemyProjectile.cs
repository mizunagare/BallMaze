using UnityEngine;

public class EnemyProjectile : MonoBehaviour
{
    public const float CollisionRadius=.16f;
    public ThirdPersonHero Target { get; private set; }
    public float Damage { get; private set; }
    public Vector3 Velocity { get; private set; }
    float remainingLife = 6;
    bool consumed;
    CombatEnemy owner;
    float remainingDistance=float.PositiveInfinity;
    static bool World(Collider c) => c.GetComponentInParent<CombatEnemy>() == null && c.GetComponentInParent<ThirdPersonHero>() == null;
    // Same physical radius as the actual projectile; no randomness or target selection.
    public static bool ClearWorldSegment(Vector3 from, Vector3 to) {
        if (!CombatAim.Finite(from) || !CombatAim.Finite(to)) return false;
        foreach (var c in Physics.OverlapSphere(from, CollisionRadius, ~0, QueryTriggerInteraction.Ignore)) if (World(c)) return false;
        var delta = to - from; if (delta.sqrMagnitude < .000001f) return true;
        foreach (var hit in Physics.SphereCastAll(from, CollisionRadius, delta.normalized, delta.magnitude, ~0, QueryTriggerInteraction.Ignore)) if (World(hit.collider)) return false;
        return true;
    }
    public static float PredictedTravel(CombatEnemy source, Vector3 origin, Vector3 aim, float speed) {
        if (source == null || source.target == null || speed <= 0) return 0;
        var delta = aim - origin; float distance = delta.magnitude;
        if (distance < .0001f) return 0;
        foreach (var hit in Physics.SphereCastAll(origin, CollisionRadius, delta.normalized, distance, ~0, QueryTriggerInteraction.Ignore))
            if (hit.collider.GetComponentInParent<ThirdPersonHero>() == source.target) distance = Mathf.Min(distance, hit.distance);
        return distance / speed;
    }
    public static EnemyProjectile Fire(CombatEnemy owner, Vector3 origin, Vector3 aim, float damage, float speed, Material material,float maxDistance=float.PositiveInfinity)
    {
        var obj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        obj.name = "远程怪能量弹";
        obj.GetComponent<Collider>().enabled = false;
        obj.transform.position = origin;
        obj.transform.localScale = Vector3.one * (CollisionRadius*2);
        obj.GetComponent<Renderer>().sharedMaterial = material;
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(obj, owner.gameObject.scene);
        var shot = obj.AddComponent<EnemyProjectile>();
        shot.owner=owner;
        shot.Target = owner.target;
        shot.Damage = damage;
        shot.remainingDistance = Mathf.Max(0,maxDistance);
        shot.Velocity = (aim - origin).normalized * speed;
        CombatFeedback.Find(owner)?.AddProjectileTrail(obj);
        return shot;
    }
    void Update()
    {
        if (consumed) return;
        if (Target == null || Target.Health.Dead || owner==null || owner.Health.Dead || !owner.gameObject.activeInHierarchy) { Consume(); return; }
        if (Target.GameplayPaused || Time.timeScale<=0) return;
        remainingLife -= Time.deltaTime;
        if (remainingLife <= 0) { Consume(); return; }
        Advance(Time.deltaTime);
    }
    public void Advance(float deltaTime)
    {
        if(consumed)return;
        if(Target==null||Target.Health.Dead||owner==null||owner.Health.Dead||!owner.gameObject.activeInHierarchy){Consume();return;}
        if(Target.GameplayPaused||Time.timeScale<=0||deltaTime<=0)return;
        if(remainingDistance<=0){Consume();return;}
        Vector3 step = Vector3.ClampMagnitude(Velocity * deltaTime,remainingDistance);
        var hits = Physics.SphereCastAll(transform.position, CollisionRadius, step.normalized, step.magnitude, ~0, QueryTriggerInteraction.Ignore);
        System.Array.Sort(hits, (a, b) => a.distance.CompareTo(b.distance));
        foreach (var hit in hits) {
            if (hit.collider.GetComponentInParent<CombatEnemy>() != null) continue;
            var hero = hit.collider.GetComponentInParent<ThirdPersonHero>();
            if (hero == Target) hero.Health.Damage(Damage, hit.point, Velocity);
            else CombatFeedback.Find(this)?.ProjectileImpact(hit.point);
            transform.position = hit.point;
            Consume();
            return;
        }
        transform.position += step;
        remainingDistance-=step.magnitude;
        if(remainingDistance<=0)Consume();
    }
    void Consume() { consumed = true; gameObject.SetActive(false); Destroy(gameObject); }
    public static void Clear(UnityEngine.SceneManagement.Scene scene)
    {
        foreach (var shot in FindObjectsByType<EnemyProjectile>(FindObjectsInactive.Include, FindObjectsSortMode.None)) {
            if (shot.gameObject.scene != scene) continue;
            shot.Consume();
        }
    }
}
