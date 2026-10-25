using System.Collections.Generic;
using UnityEngine;

public static class AdventureCatalog
{
    static readonly Dictionary<string, ItemDefinition> items = new Dictionary<string, ItemDefinition>();
    static readonly Dictionary<string, ContainerDefinition> containers = new Dictionary<string, ContainerDefinition>();
    static readonly Dictionary<GearQuality, QualityDefinition> qualities = new Dictionary<GearQuality, QualityDefinition>();
    public static readonly string[] GearIds = { "sword", "spear", "staff", "bow", "armor", "trousers", "arms", "boots", "accessory" };
    public static readonly string[] ContainerIds = { "rig_standard", "rig_light", "rig_heavy", "bag_standard", "bag_gather", "bag_relic" };
    public static readonly string[] MaterialIds = { "material_hide", "material_crystal", "material_core", "material_wood", "material_stone", "material_ore" };
    public static ItemDefinition Material(MaterialKind kind)=>Item(MaterialIds[(int)kind]);
    public static ItemDefinition Item(string id)
    {
        if (string.IsNullOrEmpty(id)) return null;
        if (!items.TryGetValue(id, out var value) || value == null) { value = Resources.Load<ItemDefinition>("ItemData/" + id); items[id] = value; }
        return value;
    }
    public static ContainerDefinition Container(string id)
    {
        if (string.IsNullOrEmpty(id)) return null;
        if (!containers.TryGetValue(id, out var value) || value == null) { value = Resources.Load<ContainerDefinition>("ContainerData/" + id); containers[id] = value; }
        return value;
    }
    public static QualityDefinition Quality(GearQuality quality)
    {
        if (!qualities.TryGetValue(quality, out var value) || value == null) { value = Resources.Load<QualityDefinition>("QualityData/" + quality); qualities[quality] = value; }
        return value;
    }
}
