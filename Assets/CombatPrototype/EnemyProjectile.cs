using UnityEngine;

public class EnemyProjectile : MonoBehaviour
{
    public ThirdPersonHero Target { get; private set; }
    public float Damage { get; private set; }
    public Vector3 Velocity { get; private set; }
    float remainingLife = 6;
    bool consumed;
    float remainingDistance=float.PositiveInfinity;
    public static EnemyProjectile Fire(CombatEnemy owner, Vector3 origin, Vector3 aim, float damage, float speed, Material material,float maxDistance=float.PositiveInfinity)
    {
        var obj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        obj.name = "远程怪能量弹";
        obj.GetComponent<Collider>().enabled = false;
        obj.transform.position = origin;
        obj.transform.localScale = Vector3.one * .32f;
        obj.GetComponent<Renderer>().sharedMaterial = material;
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(obj, owner.gameObject.scene);
        var shot = obj.AddComponent<EnemyProjectile>();
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
        if (Target == null || Target.Health.Dead) { Consume(); return; }
        if (Target.GameplayPaused) return;
        remainingLife -= Time.deltaTime;
        if (remainingLife <= 0) { Consume(); return; }
        Advance(Time.deltaTime);
    }
    public void Advance(float deltaTime)
    {
        if (consumed || Target == null || Target.GameplayPaused || deltaTime <= 0) return;
        if(remainingDistance<=0){Consume();return;}
        Vector3 step = Vector3.ClampMagnitude(Velocity * deltaTime,remainingDistance);
        var hits = Physics.SphereCastAll(transform.position, .16f, step.normalized, step.magnitude, ~0, QueryTriggerInteraction.Ignore);
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
