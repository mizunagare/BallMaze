using UnityEngine;

// Original synthesized effects: no external recordings, downloads or audio licences required.
public static class CombatSoundBank
{
    public static AudioClip[] Create()
    {
        var clips = new AudioClip[7];
        float[] durations = { .21f, .17f, .26f, .4f, .3f, .65f, .5f };
        for (int cue = 0; cue < clips.Length; cue++) {
            const int rate = 44100;
            float duration = durations[cue]; var samples = new float[Mathf.CeilToInt(rate * duration)];
            var random = new System.Random(6721 + cue);
            float low = 0, phase = 0;
            for (int i = 0; i < samples.Length; i++) {
                float t = i / (float)rate, u = t / duration;
                float noise = (float)random.NextDouble() * 2 - 1;
                low += .12f * (noise - low); float high = noise - low;
                float value;
                if (cue == (int)CombatSound.Swing) value = (low * .85f + high * .12f) * Mathf.Sin(u * Mathf.PI) * Mathf.Exp(-1.6f * u);
                else if (cue == (int)CombatSound.Hit) {
                    phase += 2 * Mathf.PI * Mathf.Lerp(210, 75, u) / rate;
                    value = .6f * Mathf.Sin(phase) * Mathf.Exp(-19 * t) + .35f * noise * Mathf.Exp(-55 * t) + .12f * Mathf.Sin(t * 2 * Mathf.PI * 1640) * Mathf.Exp(-35 * t);
                }
                else if (cue == (int)CombatSound.Hurt) {
                    phase += 2 * Mathf.PI * Mathf.Lerp(175, 80, u) / rate;
                    value = (Mathf.Sin(phase) + .28f * Mathf.Sin(phase * 2.03f) + low * .35f) * .4f * Mathf.Sin(Mathf.PI * Mathf.Pow(u, .45f));
                }
                else if (cue == (int)CombatSound.Defeat) value = (.5f * low + .2f * Mathf.Sin(2 * Mathf.PI * (180 * t - 100 * t * t))) * Mathf.Exp(-8 * t) + noise * .15f * Mathf.Exp(-20 * t);
                else if (cue == (int)CombatSound.Cast) {
                    phase += 2 * Mathf.PI * Mathf.Lerp(440, 1100, u) / rate;
                    value = (Mathf.Sin(phase) * .25f + Mathf.Sin(phase * 1.5f) * .12f + low * .35f) * Mathf.Sin(Mathf.PI * u);
                }
                else if (cue == (int)CombatSound.BossWarning) {
                    phase += 2 * Mathf.PI * Mathf.Lerp(80, 155, u) / rate;
                    value = (Mathf.Sin(phase) * .4f + low * .15f) * Mathf.Sin(Mathf.PI * u) * (.7f + .3f * Mathf.Sin(2 * Mathf.PI * 8 * t));
                }
                else value = (.65f * Mathf.Sin(2 * Mathf.PI * (85 * t - 40 * t * t)) + .55f * low + .15f * high) * Mathf.Exp(-9 * t);
                float fade = Mathf.Clamp01(t / .003f) * Mathf.Clamp01((duration - t) / .012f);
                samples[i] = Mathf.Clamp(value * fade, -.9f, .9f);
            }
            var clip = AudioClip.Create("战斗_" + (CombatSound)cue, samples.Length, 1, rate, false);
            clip.SetData(samples, 0); clips[cue] = clip;
        }
        return clips;
    }
}
