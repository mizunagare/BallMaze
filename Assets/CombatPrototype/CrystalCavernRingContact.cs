using UnityEngine;

// C2.4 HollowRing geometry contract C24-B2-RING-1. Frozen in
// ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/DESIGN_DECISIONS.md
// BEFORE any test was written. Pure geometry: no damage, no physics query, no
// state. Both the warning markers and the actual hit test consume these values.
public static class CrystalCavernRingContact
{
    public const float InnerRadius = 2.2f;
    public const float OuterRadius = 6f;
    public const float HalfHeight = 1.2f;              // relative to FROZEN AttackOrigin.y
    public const float WarningGroundOffset = .08f;
    public const float ContactEpsilon = 1f / 10000f;   // float noise only, frozen before tests

    // Any collider touching the annular cylinder is within this distance of the
    // frozen origin, so the broad phase can never exclude a real contact.
    public static float BroadPhaseRadius =>
        Mathf.Sqrt(OuterRadius * OuterRadius + HalfHeight * HalfHeight) + ContactEpsilon;

    // The 2D warning circles are the ground projection of the annulus; keep that
    // projection inside the very same vertical band used by the narrow phase.
    public static Vector3 WarningPlane(Vector3 origin) =>
        origin + Vector3.up * Mathf.Clamp(WarningGroundOffset, -HalfHeight, HalfHeight);

    // One real hit body expressed as an upright world-space capsule.
    public struct Body { public Vector3 center; public float radius, height; }

    // Exact intersection of an upright capsule (segment S swept by a sphere of
    // radius r) with the finite annular cylinder A:
    //   min dist(S, A) = sqrt(dr^2 + vgap^2) <= r + epsilon
    // dr   = radial gap from S's axis to [inner, outer]
    // vgap = vertical gap from S to [origin.y - half, origin.y + half]
    public static bool Touches(Body body, Vector3 origin)
    {
        if (body.radius <= 0 || body.height <= 0) return false;
        float dx = body.center.x - origin.x, dz = body.center.z - origin.z;
        float d = Mathf.Sqrt(dx * dx + dz * dz);
        float dr = d < InnerRadius ? InnerRadius - d : d > OuterRadius ? d - OuterRadius : 0;
        float stem = Mathf.Max(0, body.height * .5f - body.radius);
        float low = body.center.y - stem, high = body.center.y + stem;
        float bandLow = origin.y - HalfHeight, bandHigh = origin.y + HalfHeight;
        float vgap = Mathf.Max(0, Mathf.Max(bandLow - high, low - bandHigh));
        float reach = body.radius + ContactEpsilon;
        return dr * dr + vgap * vgap <= reach * reach;   // closed set: tangency counts
    }

    // Effective hit bodies are ONLY enabled, non-trigger colliders attached to
    // the hero ROOT. Child weapon models, renderers and decorative MeshColliders
    // are never hit bodies. No AABB / bounds / Renderer is used as a hit test.
    // Multiple colliders are OR-ed (never double-counted) and returned for audit.
    public static int Bodies(GameObject heroRoot, Body[] buffer)
    {
        int count = 0;
        if (heroRoot == null || buffer == null || buffer.Length == 0) return 0;
        foreach (var c in heroRoot.GetComponents<Collider>())
        {
            if (c == null || !c.enabled || c.isTrigger || count >= buffer.Length) continue;
            Body body;
            if (c is CharacterController controller)
                body = From(controller.transform, controller.center, controller.radius, controller.height);
            else if (c is CapsuleCollider capsule && capsule.direction == 1)
                body = From(capsule.transform, capsule.center, capsule.radius, capsule.height);
            else if (c is SphereCollider sphere)
                body = From(sphere.transform, sphere.center, sphere.radius, 2 * sphere.radius);
            else continue;   // box / mesh / trigger shapes are not C24 hit bodies
            if (body.radius <= 0 || body.height <= 0) continue;
            buffer[count++] = body;
        }
        return count;
    }

    public static bool TouchesAny(Body[] buffer, int count, Vector3 origin)
    {
        for (int i = 0; i < count; i++) if (Touches(buffer[i], origin)) return true;
        return false;
    }

    static Body From(Transform t, Vector3 localCenter, float radius, float height)
    {
        var scale = t.lossyScale;
        float radial = Mathf.Max(Mathf.Abs(scale.x), Mathf.Abs(scale.z));
        float r = radius * radial;
        return new Body {
            center = t.TransformPoint(localCenter),
            radius = r,
            height = Mathf.Max(height * Mathf.Abs(scale.y), 2 * r)
        };
    }
}
