using UnityEngine;
using UnityEngine.InputSystem;

public class OrbitCamera : MonoBehaviour
{
    public Transform target;
    public float distance = 6, sensitivity = .12f;
    public bool shoulderMode=true;
    public float shoulderOffset=.55f;
    public Vector3 SafePivot {get;private set;}
    public float AppliedDistance {get;private set;}
    Vector3 previousSafe,lastTargetPosition;Transform previousTarget;bool hasPrevious;
    public bool CameraPositionClear {get;private set;}
    float yaw, pitch = 28;
    float shakeRemaining, shakeDuration, shakeAmplitude;
    public float ShakeRemaining => shakeRemaining;
    public float ViewYaw => yaw;
    public float ViewPitch => pitch;
    public void RestoreView(float savedYaw, float savedPitch) { yaw = Mathf.Repeat(savedYaw, 360); pitch = Mathf.Clamp(savedPitch, -10, 65); ClearShake();hasPrevious=false; }
    public void Shake(float strength, float duration)
    {
        if (strength <= 0 || duration <= 0) return;
        shakeAmplitude = Mathf.Min(.15f, Mathf.Max(shakeAmplitude, strength));
        shakeDuration = Mathf.Max(shakeRemaining, duration); shakeRemaining = shakeDuration;
    }
    public void ClearShake() { shakeRemaining = shakeDuration = shakeAmplitude = 0; }
    void Start() { if(GetComponent<CameraActorFade>()==null)gameObject.AddComponent<CameraActorFade>();Capture(); }
    public void Capture() { Cursor.lockState = CursorLockMode.Locked; Cursor.visible = false; }
    void Update()
    {
        if(PlayerInput.UIBlocked)return;
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
        if (target == null){hasPrevious=false;previousTarget=null;return;}
        if(previousTarget!=target||(target.position-lastTargetPosition).sqrMagnitude>Mathf.Max(1,distance*distance*4))hasPrevious=false;
        previousTarget=target;lastTargetPosition=target.position;
        Vector3 focus = target.position + Vector3.up * 1.5f;
        Quaternion look = Quaternion.Euler(pitch, yaw, 0);
        Vector3 direction = look * Vector3.back;
        Vector3 side=look*Vector3.right*(shoulderMode?shoulderOffset:0);
        // Sweep the lateral pivot as well as the rear arm. Never offset after occlusion.
        if(side.sqrMagnitude>.000001f){foreach(var hit in Physics.SphereCastAll(focus,.2f,side.normalized,side.magnitude,~0,QueryTriggerInteraction.Ignore)){
            if(hit.collider.transform.IsChildOf(target)||IgnoreCameraActor(hit.collider))continue;
            side=side.normalized*Mathf.Min(side.magnitude,Mathf.Max(0,hit.distance-.1f));}}
        focus+=side;SafePivot=focus;
        float length = distance;
        foreach (var hit in Physics.SphereCastAll(focus, .2f, direction, distance, ~0, QueryTriggerInteraction.Ignore)) {
            if (hit.collider.transform.IsChildOf(target)) continue;
            // Forest actors are not static camera walls. Their collision/combat stays intact.
            if(IgnoreCameraActor(hit.collider))continue;
            length = Mathf.Min(length, Mathf.Max(.3f, hit.distance - .1f));
        }
        bool paused = Time.timeScale <= 0 || target.TryGetComponent<ThirdPersonHero>(out var actor) && actor.GameplayPaused;
        if (!paused) shakeRemaining = Mathf.Max(0, shakeRemaining - Time.deltaTime);
        float strength = shakeDuration > 0 ? shakeAmplitude * shakeRemaining / shakeDuration : 0;
        strength *= Mathf.Clamp01(length / 2);
        Vector3 shake = look * new Vector3(Mathf.Sin(Time.time * 97) * strength, Mathf.Sin(Time.time * 131 + 1) * strength * .65f, 0);
        // Keep the shake inside the swept arm; close geometry takes priority over feedback.
        if(length<distance-.01f)shake=Vector3.zero;
        AppliedDistance=length;
        Vector3 candidate=focus+direction*length+shake;
        if(hasPrevious&&ClearAt(previousSafe)){var travel=candidate-previousSafe;if(travel.sqrMagnitude>.000001f)foreach(var hit in Physics.SphereCastAll(previousSafe,.2f,travel.normalized,travel.magnitude,~0,QueryTriggerInteraction.Ignore)){
            if(hit.collider.transform.IsChildOf(target)||IgnoreCameraActor(hit.collider))continue;
            candidate=previousSafe+travel.normalized*Mathf.Min((candidate-previousSafe).magnitude,Mathf.Max(0,hit.distance-.02f));}}
        if(!ClearAt(candidate)){if(hasPrevious&&ClearAt(previousSafe))candidate=previousSafe;else for(int i=1;i<=8;i++){var sample=Vector3.Lerp(candidate,focus,i/8f);if(ClearAt(sample)){candidate=sample;break;}}}
        CameraPositionClear=ClearAt(candidate);if(CameraPositionClear){previousSafe=candidate;hasPrevious=true;}
        transform.SetPositionAndRotation(candidate, look * Quaternion.Euler(0, 0, Mathf.Sin(Time.time * 83) * strength * 4));
        if (shakeRemaining <= 0) shakeAmplitude = 0;
    }
    bool ClearAt(Vector3 p){foreach(var c in Physics.OverlapSphere(p,.2f,~0,QueryTriggerInteraction.Ignore))if(!c.transform.IsChildOf(target)&&!IgnoreCameraActor(c))return false;return true;}
    bool IgnoreCameraActor(Collider c){var h=target==null?null:target.GetComponent<ThirdPersonHero>();return h!=null&&(AdventureFlow.Find(h)?.ActiveRun?.mode==AdventureMode.ForestExploration||h.GetComponent<CP05TrainingMarker>()!=null)&&c.GetComponentInParent<CombatEnemy>()!=null;}
    void Release() { Cursor.lockState = CursorLockMode.None; Cursor.visible = true; }
    void OnDisable() { Release(); ClearShake();hasPrevious=false;previousTarget=null; }
    void OnApplicationFocus(bool focused) { if (!focused) Release(); }
}



