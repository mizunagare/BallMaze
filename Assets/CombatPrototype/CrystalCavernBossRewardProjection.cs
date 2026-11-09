// C2.4 boss NORMAL drop distribution: the single definition shared by the real
// factory (CrystalCavernBossRewards.Drop) and the read-only route projection.
// Pure values only. Nothing here samples RNG, writes a save, creates an object,
// grants the permanent first reward, or changes a revision.
public static class CrystalCavernBossRewardProjection
{
    public const int OreBase = 2, OreVariants = 3;            // 2 + hash%3 -> 2..4
    public const int CrystalBase = 3, CrystalVariants = 3;    // 3 + hash%3 -> 3..5
    public const int GearCount = 1;                           // exactly one new weapon
    public const int HideCount = 0;                           // no monster hide

    // Deterministic per-death amounts. The hash is the same uint the factory has
    // always derived from identity+suffix; the modulo structure is unchanged.
    public static int OreAmount(uint hash) => OreBase + (int)(hash % (uint)OreVariants);
    public static int CrystalAmount(uint hash) => CrystalBase + (int)(hash % (uint)CrystalVariants);

    // Design projection (nominal means of the discrete distributions), NOT a
    // prediction of the current run's hashed result.
    public static float HideMean => HideCount;
    public static float OreMean => OreBase + (OreVariants - 1) * .5f;
    public static float CrystalMean => CrystalBase + (CrystalVariants - 1) * .5f;
    public static float GearMean => GearCount;
}
