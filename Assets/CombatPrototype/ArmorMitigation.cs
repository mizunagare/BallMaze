using System;
// Player incoming damage only. Stored Defense remains raw points; no save migration.
public static class ArmorMitigation {
    public const float HalfReductionDefense = 20f;
    public const float MaximumReduction = .75f;
    public static float Incoming(float raw, float defense) {
        if (float.IsNaN(raw) || float.IsInfinity(raw) || raw <= 0) return 0;
        if (float.IsNaN(defense) || float.IsInfinity(defense) || defense < 0) defense = 0;
        // Double intermediate avoids overflow for large finite legacy defenses.
        double fraction = (double)defense / ((double)defense + HalfReductionDefense);
        return (float)Math.Max(1.0, (double)raw * (1.0 - Math.Min(MaximumReduction, fraction)));
    }
}
