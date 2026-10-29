# COMBAT-03 initial audit and measurement contract

Start local/remote main: 85b8badc4e10679c73e59683f4e92c14fdb27b14. Unity 6000.6.5f1. Product code is initially unchanged. Synthetic Editor measurements are not native input or human balance validation.

## Existing contracts

Sword basic: hero range (default1.8 + reach), dot .25, overlap collider intersection; sword skill full circle4*area,2x power and existing quality sword waves. Spear basic3.1+reach, dot.88, lateral halfwidth.4,1.25 power,1.30 cadence; skill7*area/.94/2.4x plus independent quality extra stage. Staff basic16m/s,2.5s life, nominal radius.9 but actual direct-only because AoE branch requires radius>1; skill14m/s,4/5*area explosion,2.2x plus gold/red sideballs. Bow basic23m/s single independent arrow; skill5/7/9 independent arrows at12*area degree increments,1.2x each, gold/red radius1.5. These are source contracts pending fresh actual measurement, not empirical results.

Startup per-weapon fractions basic .35/.40/.45/.40; skill .40/.45/.50/.45 of capped .55s action duration. Accepted attacks start cooldown; unreleased cancellation does not refund. Released projectiles survive equipment switch; owner death/disable/reset/unload cleans. Paused hero/projectile clocks freeze; pending startup cancellation remains existing contract.

## Suspected presentation defects to test before change

- Fixed skill descriptions omit qualities, affix area and spear extra stage; bow UI says5 when actual7/9.
- Staff basic .9 value is direct impact decoration, not AoE; preserve direct-only semantics and describe honestly, rather than silently introduce damage.
- All four releases invoke melee Swing; ranged should use cast/release presentation while actual projectiles express direction.
- Explosion feedback expands .6→1 radius, unlike actual instantaneous fixed collision radius; non-explosive arrow pulse suggests area despite direct hit only.

## Minimal intended scope

No damage/cooldown/arrows/quality changes without measured need. Derive descriptions from same quality/area definitions as release. Separate ranged cast from melee slash. Draw fixed-radius actual AoE boundary and direct impact marker honestly. Add read-only attack/projectile identity and impact diagnostics only if tests need them; no RNG or save fields. Explicit direct/AoE policy, per-shot hit deduplication and collision obstruction retained. Record baseline, test first, then patch.

Measurements: same origin, seed418, white/no-affix level1, normal/elite/waveBoss colliders; four weapon basic/skill distance/angle grid plus quality/duplicates/wall/lifecycle, actual health events and timings. Rule hit rates are matrix coverage, not human accuracy. DPS theoretical power/acceptance interval separately from observed duel damage/time. Unknown human/performance/native results remain NOT_RUN.
