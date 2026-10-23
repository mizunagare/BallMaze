using System;
using System.Collections.Generic;
using UnityEngine;

public enum GearType { Sword, Spear, Staff, Bow, Armor, Trousers, Arms, Boots, Accessory, ChestRig, Backpack }
public enum GearQuality { White, Green, Purple, Gold, Red }
[Serializable] public class GearItem
{
    public ItemOrigin origin;
    public string originRunId;
    public string id;
    public int[] affixes;
    public GearType type;
    public GearQuality quality;
    public int x = -1, y = -1;
    public bool board;
    public int legacyTier;
    public string definitionId;
    public int dataRevision, rotation, widthOverride, heightOverride;
    public bool overflow, worn;
    public float savedAttack, savedDefense;
    public ItemDefinition Definition => AdventureCatalog.Item(definitionId);
    public bool Container => type == GearType.ChestRig || type == GearType.Backpack;
    public bool InBag => !board && !overflow && !worn;
    public string Name => AdventureItems.QualityName(quality) + (Definition != null ? Definition.displayName : AdventureItems.TypeName(type));
    public bool Weapon => (int)type < 4;
    public Vector2Int BaseSize => widthOverride > 0 ? new Vector2Int(widthOverride,heightOverride) : Definition != null ? new Vector2Int(Definition.width,Definition.height) : AdventureItems.Sizes[(int)quality];
    public Vector2Int SizeAt(int turn) => turn % 2 == 0 ? BaseSize : new Vector2Int(BaseSize.y,BaseSize.x);
    public Vector2Int Size => SizeAt(rotation);
    public float Power => AdventureCatalog.Quality(quality) != null ? AdventureCatalog.Quality(quality).power : new float[] { 8, 19, 43, 78, 132 }[(int)quality];
    float LegacyPower => new float[]{8,19,43,78,132}[(int)quality];
    float LegacyAttack => legacyTier > 0 && Weapon ? legacyTier*15 : Weapon ? LegacyPower : type==GearType.Arms ? LegacyPower*.35f : type==GearType.Accessory ? LegacyPower*.5f : 0;
    float LegacyDefense => legacyTier > 0 && !Weapon ? legacyTier*5 : !Weapon && !Container ? LegacyPower*(type==GearType.Armor?.4f:type==GearType.Trousers?.3f:.2f) : 0;
    public float Attack => dataRevision > 0 ? savedAttack : LegacyAttack;
    public float Defense => dataRevision > 0 ? savedDefense : LegacyDefense;
    public string Icon => Definition != null ? Definition.iconKey : AdventureItems.Icon(type);
    public IEnumerable<Vector2Int> Cells(int turn)
    {
        var size=BaseSize;
        if(widthOverride==0 && Definition!=null && Definition.occupiedCells.Length>0){foreach(var p in Definition.occupiedCells)yield return Turn(p,turn,size);}
        else for(int y=0;y<size.y;y++)for(int x=0;x<size.x;x++)yield return Turn(new Vector2Int(x,y),turn,size);
    }
    static Vector2Int Turn(Vector2Int p,int r,Vector2Int size) => r==1?new Vector2Int(size.y-1-p.y,p.x):r==2?new Vector2Int(size.x-1-p.x,size.y-1-p.y):r==3?new Vector2Int(p.y,size.x-1-p.x):p;
    public GearItem Clone(){var copy=(GearItem)MemberwiseClone();copy.affixes=affixes==null?null:(int[])affixes.Clone();return copy;}
    public void UpgradeLegacy()
    {
        if(dataRevision>0)return;
        savedAttack=LegacyAttack;savedDefense=LegacyDefense;
        var old=AdventureItems.Sizes[(int)quality];widthOverride=old.x;heightOverride=old.y;
        definitionId=AdventureCatalog.GearIds[(int)type];rotation=0;dataRevision=1;
    }
    public void FreezeNewStats(){savedAttack=Container?0:Power*(Definition!=null?Definition.attackFactor:0);savedDefense=Container?0:Power*(Definition!=null?Definition.defenseFactor:0);dataRevision=1;}
}
public static class AdventureItems
{
    public const int BagWidth = 12, BagHeight = 8, BoardWidth = 8, BoardHeight = 6;
    public static readonly Vector2Int[] Sizes = { new Vector2Int(1,1), new Vector2Int(1,2), new Vector2Int(2,2), new Vector2Int(2,3), new Vector2Int(3,3) };
    public static string TypeName(GearType t) => new[] { "长剑", "长枪", "法杖", "弓箭", "护甲", "长裤", "护臂", "战靴", "饰品", "胸挂", "背包" }[(int)t];
    public static string QualityName(GearQuality q) => (AdventureCatalog.Quality(q)!=null ? AdventureCatalog.Quality(q).displayName : new[] { "普通", "优良", "史诗", "传说", "神话" }[(int)q])+"·";
    public static Color Color(GearQuality q) => AdventureCatalog.Quality(q)!=null ? AdventureCatalog.Quality(q).color : new[] { new Color(.86f,.89f,.91f), new Color(.3f,.9f,.48f), new Color(.77f,.45f,1), new Color(1,.76f,.25f), new Color(1,.3f,.32f) }[(int)q];
    public static string Icon(GearType t) => new[] { "sword", "spear", "staff", "bow", "armor", "trousers", "arms", "boots", "ring", "armor", "bag" }[(int)t];
    static readonly Dictionary<string, Texture2D> icons = new Dictionary<string, Texture2D>();
    public static Texture2D Texture(string key) { if (!icons.TryGetValue(key, out var icon)) { icon = Resources.Load<Texture2D>("AdventureIcons/" + key); icons[key] = icon; } return icon; }
    public static GearItem New(GearType type, GearQuality quality){if(type==GearType.ChestRig||type==GearType.Backpack)return NewContainer(type==GearType.ChestRig?"rig_standard":"bag_standard");var item=new GearItem { id=Guid.NewGuid().ToString("N"),type=type,quality=quality,definitionId=AdventureCatalog.GearIds[(int)type] };item.FreezeNewStats();if(item.Weapon)item.affixes=WeaponTraits.Roll(quality);return item;}
    public static GearItem NewContainer(string definitionId){var d=AdventureCatalog.Container(definitionId);if(d==null)throw new ArgumentException("未知容器模板");var item=new GearItem{id=Guid.NewGuid().ToString("N"),definitionId=definitionId,type=d.type,quality=d.quality};item.FreezeNewStats();return item;}
    public static GearItem Roll(int wave, bool treasure = false, bool boss = false)
    {
        float r = UnityEngine.Random.value;
        float luck = Mathf.Min(.18f, wave * .004f);
        GearQuality q = r < (boss ? .12f + luck : .005f + luck * .1f) ? GearQuality.Red
            : r < (boss ? .65f : .04f + luck) ? GearQuality.Gold
            : r < (treasure || boss ? .85f : .18f + luck) ? GearQuality.Purple
            : r < .55f ? GearQuality.Green : GearQuality.White;
        if(boss && q < GearQuality.Purple)q = GearQuality.Purple;
        return New((GearType)UnityEngine.Random.Range(0, 9), q);
    }
}

