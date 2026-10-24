using UnityEngine;

[CreateAssetMenu(menuName = "森林遗迹/物品定义")]
public class ItemDefinition : ScriptableObject
{
    public string definitionId, displayName, iconKey;
    public ItemCategory category;
    [TextArea] public string description;
    [Min(1)] public int stackLimit = 1;
    public GearType type;
    [Min(1)] public int width = 1, height = 1;
    public Vector2Int[] occupiedCells = new Vector2Int[0];
    public bool canRotate = true;
    public float attackFactor, defenseFactor;
}
public enum ItemCategory { Equipment, Container, Material, Consumable }
