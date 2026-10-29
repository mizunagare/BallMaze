using System;

// Runtime threshold only. Persisted level, in-level XP, offers and rewards remain v9.
public static class ProgressionCurve {
 public static int Required(int level,int first,int growth){double n=Math.Max(0d,(double)level-1),slope=Math.Max(0d,growth);double value=first+15d+slope*n+Math.Floor(slope*n*n/2);return (int)Math.Max(1,Math.Min(int.MaxValue,value));}
}
