using UnityEngine;

[CreateAssetMenu(menuName = "森林遗迹/品质定义")]
public class QualityDefinition : ScriptableObject
{
    public GearQuality quality;
    public float power;
    public string displayName;
    public Color color = Color.white;
}
