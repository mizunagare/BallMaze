using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody))]
public class MazePlayer : MonoBehaviour
{
    [Min(0)] public float acceleration = 16f;
    [Min(0)] public float maxSpeed = 5f;
    public MazeGame game;
    Rigidbody body;
    Vector2 input;
    Vector3 startPosition;
    Quaternion startRotation;

    void Awake()
    {
        body = GetComponent<Rigidbody>();
        startPosition = transform.position;
        startRotation = transform.rotation;
    }

    void Update()
    {
        input = Vector2.zero;
        var k = Keyboard.current;
        if (k == null || game == null || game.Won) return;
        input.x = (k.dKey.isPressed || k.rightArrowKey.isPressed ? 1 : 0)
                - (k.aKey.isPressed || k.leftArrowKey.isPressed ? 1 : 0);
        input.y = (k.wKey.isPressed || k.upArrowKey.isPressed ? 1 : 0)
                - (k.sKey.isPressed || k.downArrowKey.isPressed ? 1 : 0);
        input = Vector2.ClampMagnitude(input, 1);
        if (transform.position.y < -3) game.Restart();
    }

    void FixedUpdate()
    {
        if (game == null || game.Won) return;
        body.AddForce(new Vector3(input.x, 0, input.y) * acceleration, ForceMode.Acceleration);
        Vector3 v = body.linearVelocity;
        Vector3 horizontal = Vector3.ClampMagnitude(new Vector3(v.x, 0, v.z), maxSpeed);
        body.linearVelocity = new Vector3(horizontal.x, v.y, horizontal.z);
    }

    public void Stop()
    {
        input = Vector2.zero;
        body.linearVelocity = Vector3.zero;
        body.angularVelocity = Vector3.zero;
        body.isKinematic = true;
    }

    public void ResetPlayer()
    {
        body.isKinematic = false;
        body.position = startPosition;
        body.rotation = startRotation;
        body.linearVelocity = Vector3.zero;
        body.angularVelocity = Vector3.zero;
        input = Vector2.zero;
    }
}
