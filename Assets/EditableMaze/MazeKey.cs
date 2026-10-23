using UnityEngine;

[RequireComponent(typeof(Collider))]
public class MazeKey : MonoBehaviour
{
    public float spinSpeed = 75;
    Quaternion initialRotation;
    public bool Collected { get; private set; }
    void Awake() { initialRotation = transform.rotation; }
    void Update() { transform.Rotate(0, spinSpeed * Time.deltaTime, 0, Space.World); }
    void OnTriggerEnter(Collider other)
    {
        MazePlayer player = other.GetComponentInParent<MazePlayer>();
        if (Collected || player == null || player.game == null || player.game.Won) return;
        Collected = true;
        gameObject.SetActive(false);
        player.game.Collect();
    }
    public void ResetKey()
    {
        Collected = false;
        transform.rotation = initialRotation;
        gameObject.SetActive(true);
    }
}
