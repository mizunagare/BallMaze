using UnityEngine;
using UnityEngine.InputSystem;

public class OrbitCamera : MonoBehaviour
{
    public Transform target;
    public float distance = 6, sensitivity = .12f;
    float yaw, pitch = 28;
    float shakeRemaining, shakeDuration, shakeAmplitude;
    public float ShakeRemaining => shakeRemaining;
    public float ViewYaw => yaw;
    public float ViewPitch => pitch;
    public void RestoreView(float savedYaw, float savedPitch) { yaw = Mathf.Repeat(savedYaw, 360); pitch = Mathf.Clamp(savedPitch, -10, 65); ClearShake(); }
    public void Shake(float strength, float duration)
    {
        if (strength <= 0 || duration <= 0) return;
        shakeAmplitude = Mathf.Min(.15f, Mathf.Max(shakeAmplitude, strength));
        shakeDuration = Mathf.Max(shakeRemaining, duration); shakeRemaining = shakeDuration;
    }
    public void ClearShake() { shakeRemaining = shakeDuration = shakeAmplitude = 0; }
    void Start() { Capture(); }
    public void Capture() { Cursor.lockState = CursorLockMode.Locked; Cursor.visible = false; }
    void Update()
    {
        if (target != null && target.TryGetComponent<PlayerInventory>(out var inventory) && (inventory.IsOpen || inventory.ClosedFrame == Time.frameCount)) return;
        if (target != null && target.TryGetComponent<ThirdPersonHero>(out var hero) && hero.GameplayPaused) return;
        if (Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame) Release();
        if (Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame && Application.isFocused) Capture();
        if (Mouse.current != null && Cursor.lockState == CursorLockMode.Locked) {
            Vector2 delta = Mouse.current.delta.ReadValue();
            yaw += delta.x * sensitivity;
            pitch = Mathf.Clamp(pitch - delta.y * sensitivity, -10, 65);
        }
    }
    void LateUpdate()
    {
        if (target == null) return;
        Vector3 focus = target.position + Vector3.up * 1.5f;
        Quaternion look = Quaternion.Euler(pitch, yaw, 0);
        Vector3 direction = look * Vector3.back;
        float length = distance;
        foreach (var hit in Physics.SphereCastAll(focus, .2f, direction, distance, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.transform.IsChildOf(target)) continue;
            length = Mathf.Min(length, Mathf.Max(.3f, hit.distance - .1f));
        }
        bool paused = Time.timeScale <= 0 || target.TryGetComponent<ThirdPersonHero>(out var actor) && actor.GameplayPaused;
        if (!paused) shakeRemaining = Mathf.Max(0, shakeRemaining - Time.deltaTime);
        float strength = shakeDuration > 0 ? shakeAmplitude * shakeRemaining / shakeDuration : 0;
        strength *= Mathf.Clamp01(length / 2);
        Vector3 shake = look * new Vector3(Mathf.Sin(Time.time * 97) * strength, Mathf.Sin(Time.time * 131 + 1) * strength * .65f, 0);
        transform.SetPositionAndRotation(focus + direction * length + shake, look * Quaternion.Euler(0, 0, Mathf.Sin(Time.time * 83) * strength * 4));
        if (shakeRemaining <= 0) shakeAmplitude = 0;
    }
    void Release() { Cursor.lockState = CursorLockMode.None; Cursor.visible = true; }
    void OnDisable() { Release(); ClearShake(); }
    void OnApplicationFocus(bool focused) { if (!focused) Release(); }
}



