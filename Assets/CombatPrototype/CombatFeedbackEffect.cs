using UnityEngine;

public class CombatFeedbackEffect : MonoBehaviour
{
    CombatFeedback owner;
    LineRenderer line, core;
    ParticleSystem sparks;
    Transform follow;
    Color color;
    int mode;
    float age, duration, radius;
    Vector3[] points = new Vector3[33];
    public float Age => age;
    public void Initialize(CombatFeedback feedback, Material material)
    {
        owner = feedback; line = MakeLine("光弧", material); core = MakeLine("高光", material);
        var obj = new GameObject("命中火花"); obj.transform.SetParent(transform, false);
        sparks = obj.AddComponent<ParticleSystem>(); sparks.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
        var main = sparks.main; main.playOnAwake = false; main.loop = false; main.duration = .4f;
        main.startLifetime = new ParticleSystem.MinMaxCurve(.12f, .3f); main.startSpeed = new ParticleSystem.MinMaxCurve(1.5f, 4);
        main.startSize = new ParticleSystem.MinMaxCurve(.035f, .09f); main.gravityModifier = .55f; main.maxParticles = 24;
        main.simulationSpace = ParticleSystemSimulationSpace.World;
        var emission = sparks.emission; emission.enabled = false;
        var shape = sparks.shape; shape.enabled = true; shape.shapeType = ParticleSystemShapeType.Sphere; shape.radius = .07f;
        var colorOverLife = sparks.colorOverLifetime; colorOverLife.enabled = true;
        var gradient = new Gradient(); gradient.SetKeys(new[] { new GradientColorKey(Color.white, 0), new GradientColorKey(Color.white, 1) }, new[] { new GradientAlphaKey(1, 0), new GradientAlphaKey(0, 1) }); colorOverLife.color = gradient;
        var renderer = sparks.GetComponent<ParticleSystemRenderer>(); renderer.sharedMaterial = material;
        renderer.renderMode = ParticleSystemRenderMode.Stretch; renderer.lengthScale = 1.8f; renderer.velocityScale = .04f;
        renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; renderer.receiveShadows = false;
    }
    LineRenderer MakeLine(string name, Material material)
    {
        var obj = new GameObject(name); obj.transform.SetParent(transform, false);
        var result = obj.AddComponent<LineRenderer>(); result.sharedMaterial = material; result.useWorldSpace = false;
        result.positionCount = points.Length; result.numCapVertices = 2; result.alignment = LineAlignment.View;
        result.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; result.receiveShadows = false; return result;
    }
    void Begin(int effectMode, Vector3 position, Color tint, float seconds)
    {
        mode = effectMode; color = tint; duration = seconds; age = 0; follow = null;
        transform.SetPositionAndRotation(position, Quaternion.identity); transform.localScale = Vector3.one;
        line.enabled = true; core.enabled = false; sparks.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
    }
    public void Slash(Transform actor, float reach, Color tint)
    {
        Begin(0, actor.position + Vector3.up * 1.15f, tint, .23f); follow = actor; radius = Mathf.Max(.5f, reach);
        transform.rotation = actor.rotation; core.enabled = true; Draw();
    }
    public void Thrust(Transform actor,Color tint)
    {
        Begin(3,actor.position+Vector3.up*1.15f,tint,.23f);transform.rotation=actor.rotation;Draw();
    }
    public void Impact(Vector3 position, Vector3 direction, Color tint, float scale, int seed)
    {
        Begin(1, position, tint, .34f); radius = .4f * scale;
        var camera = Camera.main; if (camera != null) transform.rotation = camera.transform.rotation;
        sparks.useAutoRandomSeed = false; sparks.randomSeed = (uint)Mathf.Max(1, seed);
        var main = sparks.main; main.startColor = tint; main.startSpeed = new ParticleSystem.MinMaxCurve(1.5f * scale, 4 * scale);
        sparks.Play(); sparks.Emit(Mathf.RoundToInt(12 * scale)); Draw();
    }
    public void GroundRing(Vector3 position, float reach, Color tint)
    {
        Begin(2, position + Vector3.up * .07f, tint, .48f); radius = reach; Draw();
    }
    void Draw()
    {
        float t = Mathf.Clamp01(age / duration), fade = 1 - t;
        Color tint = new Color(color.r, color.g, color.b, fade * (mode == 0 ? .9f : .7f));
        line.startColor = tint; line.endColor = new Color(color.r, color.g, color.b, 0);
        if(mode==3){
            for(int i=0;i<points.Length;i++)points[i]=Vector3.forward*Mathf.Lerp(.45f,AdventureCombat.SpearReach,i/(float)(points.Length-1));
            line.widthMultiplier=.07f*fade;
        }
        else if (mode == 0) {
            for (int i = 0; i < points.Length; i++) {
                float u = i / (float)(points.Length - 1), angle = Mathf.Lerp(-68 + t * 55, 68 + t * 25, u) * Mathf.Deg2Rad;
                points[i] = new Vector3(Mathf.Sin(angle) * radius, Mathf.Sin(u * Mathf.PI) * .08f, Mathf.Cos(angle) * radius);
            }
            line.widthMultiplier = .17f * fade; core.widthMultiplier = .045f * fade;
            core.startColor = new Color(1, 1, .94f, fade); core.endColor = new Color(1, 1, 1, 0); core.SetPositions(points);
        }
        else {
            float size = mode == 1 ? Mathf.Lerp(.04f, radius, t) : radius * Mathf.Lerp(.12f, 1, t);
            for (int i = 0; i < points.Length; i++) {
                float angle = i / (float)(points.Length - 1) * Mathf.PI * 2;
                points[i] = mode == 1 ? new Vector3(Mathf.Sin(angle), Mathf.Cos(angle), 0) * size : new Vector3(Mathf.Sin(angle), 0, Mathf.Cos(angle)) * size;
            }
            line.endColor = tint; line.widthMultiplier = (mode == 1 ? .055f : .1f) * fade;
        }
        line.SetPositions(points);
    }
    void Update()
    {
        if (owner == null) { Clear(); return; }
        if (owner.Paused) return;
        age += Time.deltaTime;
        if (age >= duration) { Clear(); return; }
        if (follow != null) transform.position = follow.position + Vector3.up * 1.15f;
        Draw();
    }
    public void SetPaused(bool paused) { if (sparks == null) return; if (paused) sparks.Pause(); else if (gameObject.activeSelf && mode == 1) sparks.Play(); }
    public void Clear() { if (sparks != null) sparks.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear); follow = null; gameObject.SetActive(false); }
}
