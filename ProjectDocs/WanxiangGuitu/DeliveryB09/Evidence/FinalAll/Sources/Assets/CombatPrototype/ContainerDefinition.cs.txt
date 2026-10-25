using UnityEngine;

[CreateAssetMenu(menuName = "森林遗迹/容器模板")]
public class ContainerDefinition : ScriptableObject
{
    public string definitionId, displayName, description;
    public GearType type;
    public GearQuality quality;
    [Min(1)] public int width = 8, height = 6;
    public Vector2Int[] blockedCells = new Vector2Int[0];
    public float moveBonus, attackBonus, defenseBonus;
    public int harvestBonus;
    public int woodCost, hideCost, oreCost;
    public bool Allows(int x, int y)
    {
        if (x < 0 || y < 0 || x >= width || y >= height) return false;
        foreach (var cell in blockedCells) if (cell.x == x && cell.y == y) return false;
        return true;
    }
    public int Capacity => width * height - blockedCells.Length;
}
