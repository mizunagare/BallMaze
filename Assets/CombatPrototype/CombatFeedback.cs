using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public enum CombatSound { Swing, Hit, Hurt, Defeat, Cast, BossWarning, Slam }

// Scene-owned presentation. No damage, movement, loot or time-scale changes happen here.
public class CombatFeedback : MonoBehaviour
{
    [Range(0, 1), InspectorName("战斗音量")] public float volume = .55f;
    [Range(0, 1), InspectorName("镜头震动强度")] public float shakeStrength = .65f;
    [InspectorName("显示伤害数字")] public bool showDamageNumbers = true;
    [InspectorName("启用战斗特效")] public bool effectsEnabled = true;
    public const int EffectLimit = 24, VoiceLimit = 10, NumberLimit = 32;
    CombatSession session;
    readonly List<CombatFeedbackEffect> effects = new List<CombatFeedbackEffect>();
    readonly List<DamageNumber> numbers = new List<DamageNumber>();
    AudioSource[] voices;
    bool[] voicePaused;
    AudioClip[] clips;
    float[] soundReady;
    Material glow;
    bool ownsMaterial, wasPaused;
    int voiceIndex;
    float hurtOverlay;
    // Independent randomness prevents particles and sound variations from changing loot/skill RNG.
    readonly System.Random random = new System.Random(88217);
    public bool Paused => Time.timeScale <= 0 || session != null && session.hero != null && session.hero.GameplayPaused;
    public int ActiveEffectCount { get { int count = 0; foreach (var effect in effects) if (effect.gameObject.activeSelf) count++; return count; } }
    public int DamageNumberCount => numbers.Count;
    public Material EffectMaterial => glow;

    class DamageNumber { public Vector3 position; public string text; public Color color; public float age; public bool lethal; }
    void Awake()
    {
        session = GetComponent<CombatSession>();
        glow = Resources.Load<Material>("CombatFeedback/Glow");
        if (glow == null) {
            glow = new Material(Shader.Find("Universal Render Pipeline/Particles/Unlit"));
            ownsMaterial = true;
        }
        clips = CombatSoundBank.Create(); soundReady = new float[clips.Length];
        voices = new AudioSource[VoiceLimit]; voicePaused = new bool[VoiceLimit];
        for (int i = 0; i < voices.Length; i++) {
            var obj = new GameObject("战斗音效声道 " + (i + 1)); obj.transform.SetParent(transform, false);
            var source = obj.AddComponent<AudioSource>(); source.playOnAwake = false;
            source.spatialBlend = .65f; source.minDistance = 4; source.maxDistance = 35;
            source.rolloffMode = AudioRolloffMode.Linear; source.dopplerLevel = 0;
            voices[i] = source;
        }
    }
    public static CombatFeedback Find(Component actor)
    {
        if (actor == null) return null;
        foreach (var item in FindObjectsByType<CombatFeedback>(FindObjectsSortMode.None))
            if (item.gameObject.scene == actor.gameObject.scene) return item;
        return null;
    }
    public void AttackStarted(ThirdPersonHero hero)
    {
        if(!Paused)PlaySound(CombatSound.Swing,hero.transform.position,.16f);
    }
    public void Swing(ThirdPersonHero hero)
    {
        if (Paused) return;
        PlaySound(CombatSound.Swing, hero.transform.position, .45f);
        Color color = hero.Equipment != null && hero.Equipment.SwordEquipped
            ? hero.Equipment.SwordTier >= 2 ? new Color(1, .75f, .23f) : new Color(.3f, .85f, 1)
            : new Color(1, .89f, .58f);
        if (effectsEnabled) GetEffect().Slash(hero.transform, hero.AttackRange * .87f, color);
    }
    public void Dodge(HeroDodge dodge)
    {
        if (Paused) return;
        PlaySound(CombatSound.Swing, dodge.transform.position, .4f);
        if (effectsEnabled) GetEffect().GroundRing(dodge.transform.position, .85f, new Color(.25f, .85f, 1));
    }
    public void Hit(CombatHealth victim, float actualDamage, Vector3 position, Vector3 direction, bool lethal)
    {
        if (Paused || actualDamage <= 0) return;
        bool player = victim.GetComponent<ThirdPersonHero>() != null;
        var enemy = victim.GetComponent<CombatEnemy>();
        bool boss = enemy != null && enemy.archetype == EnemyArchetype.Boss;
        Color color = player ? new Color(1, .24f, .16f) : lethal ? new Color(1, .72f, .2f) : new Color(1, .91f, .55f);
        if (effectsEnabled) GetEffect().Impact(position, direction, color, lethal ? 1.5f : 1, random.Next());
        if (showDamageNumbers) {
            if (numbers.Count >= NumberLimit) numbers.RemoveAt(0);
            numbers.Add(new DamageNumber { position = position + Vector3.up * .5f + Vector3.right * ((float)random.NextDouble() - .5f) * .35f,
                text = "−" + actualDamage.ToString("0"), color = color, lethal = lethal });
        }
        PlaySound(player ? CombatSound.Hurt : CombatSound.Hit, position, player ? .85f : .7f);
        if (lethal && !player) PlaySound(CombatSound.Defeat, position, boss ? 1 : .6f);
        if (player) hurtOverlay = .24f;
        float shake = player ? .1f : lethal ? .065f : .035f;
        if (session != null && session.orbit != null) session.orbit.Shake(shake * shakeStrength, player ? .19f : .11f);
        victim.GetComponent<FantasyActorVisual>()?.Recoil(direction);
        if (lethal && boss && effectsEnabled) GetEffect().GroundRing(victim.transform.position, 3.5f, color);
    }
    public void EnemyAttack(CombatEnemy enemy, bool spell)
    {
        if (Paused) return;
        PlaySound(spell ? CombatSound.Cast : CombatSound.Swing, enemy.transform.position, spell ? .55f : .3f);
        if (!spell && effectsEnabled) GetEffect().Slash(enemy.transform, Mathf.Min(2.4f, enemy.attackRange), new Color(1, .45f, .23f));
    }
    public void BossWarning(Vector3 position) { if (!Paused) PlaySound(CombatSound.BossWarning, position, .65f); }
    public void BossRelease(CombatEnemy enemy, BossAttack attack)
    {
        if (Paused) return;
        PlaySound(attack == BossAttack.Fan ? CombatSound.Cast : CombatSound.Slam, enemy.transform.position, .9f);
        if (effectsEnabled && attack == BossAttack.Slam) GetEffect().GroundRing(enemy.transform.position, 4.3f, new Color(1, .56f, .15f));
        if (attack == BossAttack.Slam && session != null && session.orbit != null && session.hero != null) {
            float proximity = Mathf.Clamp01(1 - Vector3.Distance(enemy.transform.position, session.hero.transform.position) / 16);
            session.orbit.Shake(.14f * shakeStrength * proximity, .24f);
        }
    }
    public void ProjectileImpact(Vector3 position)
    {
        if (!Paused && effectsEnabled) GetEffect().Impact(position, Vector3.up, new Color(1, .55f, .15f), .55f, random.Next());
    }
    public void AddProjectileTrail(GameObject projectile)
    {
        if (!effectsEnabled) return;
        var trail = projectile.AddComponent<TrailRenderer>(); trail.sharedMaterial = glow;
        trail.time = .14f; trail.minVertexDistance = .04f; trail.widthMultiplier = .16f;
        trail.startColor = new Color(1, .64f, .15f, .8f); trail.endColor = new Color(1, .2f, .05f, 0);
        trail.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; trail.receiveShadows = false;
    }
    CombatFeedbackEffect GetEffect()
    {
        foreach (var effect in effects) if (!effect.gameObject.activeSelf) { effect.gameObject.SetActive(true); return effect; }
        if (effects.Count >= EffectLimit) {
            var recycled = effects[0]; effects.RemoveAt(0); effects.Add(recycled); recycled.Clear(); recycled.gameObject.SetActive(true); return recycled;
        }
        var obj = new GameObject("战斗特效"); obj.transform.SetParent(transform, false);
        var item = obj.AddComponent<CombatFeedbackEffect>(); item.Initialize(this, glow); effects.Add(item); return item;
    }
    public void PlaySound(CombatSound cue, Vector3 position, float gain = 1)
    {
        if (Paused || volume <= 0 || voices == null) return;
        int index = (int)cue;
        if (Time.time < soundReady[index]) return;
        soundReady[index] = Time.time + .035f;
        AudioSource source = null;
        for (int i = 0; i < voices.Length; i++) {
            int slot = (voiceIndex + i) % voices.Length;
            if (!voices[slot].isPlaying) { source = voices[slot]; voiceIndex = slot; break; }
        }
        if (source == null) { voiceIndex = (voiceIndex + 1) % voices.Length; source = voices[voiceIndex]; }
        source.Stop(); voicePaused[voiceIndex] = false; source.transform.position = position;
        source.clip = clips[index]; source.volume = Mathf.Clamp01(volume * gain);
        source.pitch = .94f + (float)random.NextDouble() * .12f; source.Play();
    }
    void Update()
    {
        bool paused = Paused;
        if (paused != wasPaused) {
            for (int i = 0; i < voices.Length; i++) {
                if (paused) { voicePaused[i] = voices[i].isPlaying; if (voicePaused[i]) voices[i].Pause(); }
                else if (voicePaused[i]) { voices[i].UnPause(); voicePaused[i] = false; }
            }
            foreach (var effect in effects) effect.SetPaused(paused);
            wasPaused = paused;
        }
        if (paused) return;
        hurtOverlay = Mathf.Max(0, hurtOverlay - Time.deltaTime);
        for (int i = numbers.Count - 1; i >= 0; i--) { numbers[i].age += Time.deltaTime; if (numbers[i].age > .85f) numbers.RemoveAt(i); }
    }
    public void ResetFeedback()
    {
        numbers.Clear(); hurtOverlay = 0; wasPaused = false;
        foreach (var effect in effects) effect.Clear();
        if (voices != null) for (int i = 0; i < voices.Length; i++) { voices[i].Stop(); voicePaused[i] = false; }
        if (soundReady != null) Array.Clear(soundReady, 0, soundReady.Length);
        if (session != null && session.orbit != null) session.orbit.ClearShake();
    }
    void OnGUI()
    {
        if (Paused || session == null || session.hero == null || session.hero.Inventory == null) return;
        Camera camera = session.orbit != null ? session.orbit.GetComponent<Camera>() : Camera.main;
        if (camera == null) return;
        CombatChineseUI.Apply();
        float scale = CombatUI.Scale;
        if (hurtOverlay > 0) {
            Color old = GUI.color; GUI.color = new Color(.8f, .03f, .02f, hurtOverlay * .6f);
            float width = Screen.width, height = Screen.height, edge = Mathf.Min(width, height) * .035f;
            GUI.DrawTexture(new Rect(0, 0, width, edge), Texture2D.whiteTexture); GUI.DrawTexture(new Rect(0, height - edge, width, edge), Texture2D.whiteTexture);
            GUI.DrawTexture(new Rect(0, edge, edge, height - 2 * edge), Texture2D.whiteTexture); GUI.DrawTexture(new Rect(width - edge, edge, edge, height - 2 * edge), Texture2D.whiteTexture); GUI.color = old;
        }
        foreach (var number in numbers) {
            var p = camera.WorldToScreenPoint(number.position + Vector3.up * number.age * .9f);
            if (p.z <= 0 || p.x < 0 || p.x > Screen.width || p.y < 0 || p.y > Screen.height) continue;
            float alpha = Mathf.Clamp01((.85f - number.age) / .25f);
            var style = new GUIStyle(GUI.skin.label) { fontSize = Mathf.RoundToInt((number.lethal ? 30 : 25) * scale), fontStyle = FontStyle.Bold, alignment = TextAnchor.MiddleCenter };
            var area = new Rect(p.x - 65 * scale, Screen.height - p.y - 25 * scale, 130 * scale, 50 * scale);
            if(ForestBossHud.ImportantOverlap(area))area.y=ForestBossHud.Instance.BossRects.Max(r=>r.yMax)+6;
            style.normal.textColor = new Color(.08f, .06f, .03f, alpha); GUI.Label(new Rect(area.x + 2, area.y + 2, area.width, area.height), number.text, style);
            style.normal.textColor = new Color(number.color.r, number.color.g, number.color.b, alpha); GUI.Label(area, number.text, style);
        }
    }
    void OnDisable() { ResetFeedback(); }
    void OnDestroy() { if (clips != null) foreach (var clip in clips) if (clip != null) Destroy(clip); if (ownsMaterial && glow != null) Destroy(glow); }
}
