using UnityEngine;

public class MazeExit : MonoBehaviour
{
    void OnTriggerEnter(Collider other) { TryFinish(other); }
    void OnTriggerStay(Collider other) { TryFinish(other); }
    void TryFinish(Collider other)
    {
        MazePlayer player = other.GetComponentInParent<MazePlayer>();
        if (player != null && player.game != null) player.game.TryWin();
    }
}
