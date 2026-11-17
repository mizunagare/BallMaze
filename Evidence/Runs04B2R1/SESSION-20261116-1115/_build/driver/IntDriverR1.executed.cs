// UX-04-B2-R1 OBSERVATION driver (SIDECAR ONLY).
//
// Compiled as a separate assembly, injected into an isolated COPY of the R1
// Player. NEVER shipped. Test setup mutates ONLY isolated runtime/save data;
// factory-created samples may consume the isolated test random stream.
//
// Covers the seven R1 defect closures with REAL Player input:
//   C-01 scoped favourite batch guard + stale cleanup + dismantle cleanup
//   C-02 filter-then-sort genuinely wired into IMGUI + uGUI display order
//   C-03 IMGUI duplicate B2Controls removed (behavioural proof)
//   C-04 GUID uniqueness of the three new .meta files
//   C-05 Strength=0 / Strength=N through the REAL attribute chain
//   C-06 PreviewReplacement nine-item before/after state fingerprints
//   C-07 full favourite lifecycle + process-restart clearing
//
// uGUI actions use real InputSystem mouse events consumed by the product's
// EventSystem. IMGUI actions use real Win32 OS mouse events (InputSystem does
// NOT reach IMGUI Event.current). All state is read from real runtime objects.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.UI;

namespace B2R1Observation
{
    public sealed class Driver : MonoBehaviour
    {
        static string root;
        string mode, runId, obsPath, inputPath, stepsPath, resultPath;
        CombatSession session;
        ThirdPersonHero hero;
        AdventureLoadout gear;
        PlayerInventory inv;
        readonly StringBuilder obs = new StringBuilder();
        readonly StringBuilder inputs = new StringBuilder();
        readonly StringBuilder steps = new StringBuilder();
        readonly List<string> checks = new List<string>();
        int seq, stepSeq;
        bool failed;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        public static void Boot()
        {
            var env = Environment.GetEnvironmentVariable("UNITY_TEST_ROOT");
            if (string.IsNullOrEmpty(env)) return;
            if (!File.Exists(Path.Combine(env, "r1-mode.txt"))) return;
            root = env;
            Application.runInBackground = true;
            var host = new GameObject("UX04-B2-R1 observation driver");
            DontDestroyOnLoad(host);
            host.AddComponent<Driver>();
        }

        static string F(float v) => v.ToString("R", CultureInfo.InvariantCulture);
        static string Esc(string s)
        {
            if (s == null) return "";
            return s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n").Replace("\r", "\\r").Replace("\t", "\\t");
        }
        static string Short(string id) => string.IsNullOrEmpty(id) ? "null" : (id.Length <= 10 ? id : id.Substring(0, 10));
        // Deterministic FNV-1a 64 over a canonical state string (no crypto deps).
        static string Hash(string s)
        {
            ulong h = 14695981039346656037UL;
            for (int i = 0; i < s.Length; i++) { h ^= s[i]; h *= 1099511628211UL; }
            return h.ToString("x16", CultureInfo.InvariantCulture);
        }

        // ---- canonical nine-item state ------------------------------------
        string ItemState(GearItem i)
        {
            if (i == null) return "null";
            string aff = i.affixes == null ? "" : string.Join(",", i.affixes.Select(a => a.ToString(CultureInfo.InvariantCulture)));
            return string.Join("|", new[] {
                i.id ?? "", ((int)i.type).ToString(CultureInfo.InvariantCulture),
                ((int)i.quality).ToString(CultureInfo.InvariantCulture),
                i.x.ToString(CultureInfo.InvariantCulture), i.y.ToString(CultureInfo.InvariantCulture),
                i.rotation.ToString(CultureInfo.InvariantCulture),
                i.board ? "1" : "0", i.worn ? "1" : "0", i.overflow ? "1" : "0",
                i.definitionId ?? "", i.dataRevision.ToString(CultureInfo.InvariantCulture),
                F(i.savedAttack), F(i.savedDefense), F(i.Attack), F(i.Defense),
                aff, i.widthOverride.ToString(CultureInfo.InvariantCulture),
                i.heightOverride.ToString(CultureInfo.InvariantCulture),
                ((int)i.origin).ToString(CultureInfo.InvariantCulture), i.originRunId ?? "",
                i.legacyTier.ToString(CultureInfo.InvariantCulture) });
        }
        string ContainerState(ContainerDefinition d)
        {
            if (d == null) return "null";
            return JsonUtility.ToJson(d);
        }
        // Nine independent fingerprints: GearItem / Inventory / EquipmentGrid /
        // Main / Reserve / Worn / Overflow / AttackPower / Container.
        Dictionary<string, string> NineCanonical()
        {
            var d = new Dictionary<string, string>();
            d["GearItem"] = (string.Join(";", gear.items.OrderBy(i => i.id, StringComparer.Ordinal).Select(ItemState)));
            var mats = new StringBuilder();
            for (int k = 0; k < 6; k++) mats.Append(inv.Count((MaterialKind)k)).Append(",");
            mats.Append("itemOrder=").Append(string.Join(",", gear.items.Select(i => i.id))).Append("|");
            mats.Append(inv.HealthPotionCount).Append(",").Append(inv.PotionOnQuickbar).Append(",").Append(F(inv.PotionCooldownRemaining));
            d["Inventory"] = (mats.ToString());
            d["EquipmentGrid"] = (string.Join(";", gear.items.OrderBy(i => i.id, StringComparer.Ordinal)
                .Select(i => i.id + "," + i.x + "," + i.y + "," + i.board + "," + i.rotation + "," + i.worn + "," + i.overflow)));
            d["Main"] = ((gear.mainWeapon ?? "") + "|" + (gear.Main == null ? "null" : ItemState(gear.Main)));
            d["Reserve"] = ((gear.reserveWeapon ?? "") + "|" + (gear.Reserve == null ? "null" : ItemState(gear.Reserve)));
            d["Worn"] = (string.Join(";", gear.items.Where(i => i.worn).OrderBy(i => i.id, StringComparer.Ordinal).Select(ItemState)));
            d["Overflow"] = (string.Join(";", gear.items.Where(i => i.overflow).OrderBy(i => i.id, StringComparer.Ordinal).Select(ItemState)));
            var combat = hero.GetComponent<AdventureCombat>();
            d["AttackPower"] = (string.Join("|", F(hero.AttackPower), F(hero.Defense),
                F(gear.Attack), F(gear.Defense), F(combat == null ? 0f : combat.BasicPower),
                F(hero.Progression.AttackBonus)));
            d["Container"] = (ContainerState(gear.Rig) + ";" + ContainerState(gear.Bag));
            return d;
        }
        Dictionary<string, string> Nine() => NineCanonical().ToDictionary(kv => kv.Key, kv => Hash(kv.Value));
        string ItemIdentity(GearItem item)
        {
            if (item == null) return "null";
            var c = item.Clone(); c.x = c.y = 0; c.rotation = 0; c.board = c.worn = c.overflow = false;
            return ItemState(c);
        }
        string ItemJson(GearItem i) => JsonUtility.ToJson(i).TrimEnd('}') + ",\"derivedAttack\":" + F(i.Attack) + ",\"derivedDefense\":" + F(i.Defense) + "}";
        string RawState()
        {
            var camp = AdventureRecipes.Camp(hero);
            return "{\"items\":[" + string.Join(",", gear.items.Select(ItemJson)) +
                "],\"warehouse\":[" + string.Join(",", (camp == null ? new List<GearItem>() : camp.Items.ToList()).Select(ItemJson)) +
                "],\"rig\":" + JsonUtility.ToJson(gear.Rig) + ",\"bag\":" + JsonUtility.ToJson(gear.Bag) +
                ",\"baseDamage\":" + F(hero.attackDamage) + ",\"rank\":" + hero.Progression.Rank(BasicSkill.Strength) +
                ",\"bonus\":" + F(hero.Progression.AttackBonus) + ",\"attackPower\":" + F(hero.AttackPower) +
                ",\"basicPower\":" + F(hero.GetComponent<AdventureCombat>().BasicPower) +
                ",\"main\":\"" + Esc(gear.mainWeapon) + "\",\"reserve\":\"" + Esc(gear.reserveWeapon) +
                "\",\"canonical\":" + NineJson(NineCanonical()) + "}";
        }
        string NineJson(Dictionary<string, string> d) =>
            "{" + string.Join(",", d.OrderBy(kv => kv.Key).Select(kv => "\"" + Esc(kv.Key) + "\":\"" + Esc(kv.Value) + "\"")) + "}";

        void Snap(string stage, string flow, string note, params string[] extra)
        {
            var items = gear == null ? new List<GearItem>() : gear.items;
            seq++;
            var sb = new StringBuilder();
            sb.Append("{\"seq\":").Append(seq).Append(",");
            sb.Append("\"stage\":\"").Append(Esc(stage)).Append("\",");
            sb.Append("\"flow\":\"").Append(Esc(flow)).Append("\",");
            sb.Append("\"note\":\"").Append(Esc(note)).Append("\",");
            sb.Append("\"runId\":\"").Append(Esc(runId)).Append("\",");
            sb.Append("\"frame\":").Append(Time.frameCount).Append(",");
            sb.Append("\"mode\":\"").Append(Esc(mode)).Append("\",");
            sb.Append("\"Inventory_count\":").Append(items.Count).Append(",");
            sb.Append("\"AttackPower\":\"").Append(hero == null ? "" : F(hero.AttackPower)).Append("\",");
            sb.Append("\"GearAttack\":\"").Append(gear == null ? "" : F(gear.Attack)).Append("\",");
            sb.Append("\"GearDefense\":\"").Append(gear == null ? "" : F(gear.Defense)).Append("\",");
            sb.Append("\"StrengthRank\":").Append(hero == null || hero.Progression == null ? -1 : hero.Progression.Rank(BasicSkill.Strength)).Append(",");
            sb.Append("\"AttackBonus\":\"").Append(hero == null || hero.Progression == null ? "" : F(hero.Progression.AttackBonus)).Append("\",");
            sb.Append("\"Main\":\"").Append(Esc(gear == null ? "" : gear.mainWeapon ?? "")).Append("\",");
            sb.Append("\"Reserve\":\"").Append(Esc(gear == null ? "" : gear.reserveWeapon ?? "")).Append("\",");
            sb.Append("\"Worn\":").Append(items.Count(i => i.worn)).Append(",");
            sb.Append("\"Overflow\":").Append(items.Count(i => i.overflow)).Append(",");
            sb.Append("\"Board\":").Append(items.Count(i => i.board)).Append(",");
            sb.Append("\"MaterialCount\":").Append(inv == null ? 0 : inv.Count(MaterialKind.Ore)).Append(",");
            sb.Append("\"WarehouseCount\":").Append(WarehouseCount()).Append(",");
            sb.Append("\"FavoritesCount\":").Append(B2Collection.Count).Append(",");
            sb.Append("\"SessionToken\":\"").Append(Esc(B2Collection.SessionToken)).Append("\",");
            sb.Append("\"FilterKey\":\"").Append(Esc(B2FilterState.Current.Key)).Append("\",");
            sb.Append("\"FilterTab\":").Append(B2FilterState.Tab).Append(",");
            sb.Append("\"SortKey\":\"").Append(Esc(B2FilterState.Current.sort.ToString())).Append("\",");
            sb.Append("\"CompareRole\":\"").Append(ContainerInventoryView.CompareRoleValue.ToString()).Append("\"");
            for (int i = 0; i + 1 < extra.Length; i += 2)
                sb.Append(",\"").Append(Esc(extra[i])).Append("\":\"").Append(Esc(extra[i + 1])).Append("\"");
            if (gear != null && hero != null && inv != null && hero.Progression != null && hero.GetComponent<AdventureCombat>() != null) sb.Append(",\"raw\":").Append(RawState());
            sb.Append("}");
            obs.AppendLine(sb.ToString());
            Flush();
        }
        int WarehouseCount()
        {
            try { var c = AdventureRecipes.Camp(hero); return c == null ? -1 : c.Items.Count; }
            catch { return -1; }
        }
        void Flush()
        {
            try { File.WriteAllText(obsPath, obs.ToString()); } catch { }
            try { File.WriteAllText(inputPath, inputs.ToString()); } catch { }
            try { File.WriteAllText(stepsPath, steps.ToString()); } catch { }
        }
        void Input(string kind, string detail)
        {
            inputs.AppendLine("{\"kind\":\"" + Esc(kind) + "\",\"detail\":\"" + Esc(detail) +
                             "\",\"frame\":" + Time.frameCount + ",\"time\":" + F(Time.realtimeSinceStartup) + "}");
            Flush();
        }
        // R1-07: record BEFORE/AFTER state for every lifecycle step.
        void Step(string tag, string before, string after, string verdict)
        {
            stepSeq++;
            steps.AppendLine("{\"step\":" + stepSeq + ",\"tag\":\"" + Esc(tag) +
                "\",\"before\":" + before + ",\"after\":" + after +
                ",\"verdict\":\"" + Esc(verdict) + "\",\"frame\":" + Time.frameCount + "}");
            Flush();
        }
        string StateMini() =>
            "{\"inv\":" + gear.items.Count + ",\"wh\":" + WarehouseCount() +
            ",\"fav\":" + B2Collection.Count + ",\"ore\":" + inv.Count(MaterialKind.Ore) +
            ",\"main\":\"" + Esc(gear.mainWeapon ?? "") + "\",\"ap\":\"" + F(hero.AttackPower) + "\"}";
        void Check(string name, bool ok, string detail)
        {
            checks.Add(name + "|" + (ok ? "PASS" : "FAIL") + "|" + detail);
            Snap("check", name, (ok ? "PASS " : "FAIL ") + detail, "result", ok ? "PASS" : "FAIL");
            if (!ok) Fail(name + ": " + detail);
        }
        void Fail(string why)
        {
            failed = true;
            Snap("error", "driver", why);
            try { File.WriteAllText(Path.Combine(root, "r1-failure.txt"), why); } catch { }
        }
        IEnumerator WaitFrames(int n) { float until = Time.unscaledTime + .18f; for (int i = 0; i < Math.Max(n, 10) || Time.unscaledTime < until; i++) yield return null; }

        // ---- real physical input -------------------------------------------
        Button FindButton(string name)
        {
            var all = UnityEngine.Object.FindObjectsByType<Button>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            return all.FirstOrDefault(b => b.gameObject.activeInHierarchy && b.gameObject.name == name);
        }
        Vector2 ScreenCentre(Button b)
        {
            var rt = b.GetComponent<RectTransform>();
            var canvas = b.GetComponentInParent<Canvas>();
            var cam = canvas != null && canvas.renderMode != RenderMode.ScreenSpaceOverlay ? canvas.worldCamera : null;
            Vector3[] corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            return RectTransformUtility.WorldToScreenPoint(cam, (corners[0] + corners[2]) * .5f);
        }
        Mouse CurMouse()
        {
            var m = Mouse.current;
            if (m == null) { InputSystem.AddDevice<Mouse>(); m = Mouse.current; }
            return m;
        }
        IEnumerator RealClick(string buttonName, bool expectInteractable, string tag)
        {
            var b = FindButton(buttonName);
            if (b == null) { Fail("button-missing " + tag + " name=" + buttonName); yield break; }
            bool interactable = b.interactable;
            Input("button-found", tag + " name=" + buttonName + " interactable=" + interactable +
                  " active=" + b.gameObject.activeInHierarchy);
            if (expectInteractable != interactable) { Fail("unexpected interactable " + tag); yield break; }
            Vector2 at = ScreenCentre(b);
            yield return RealClickAt(at, tag, b);
        }
        IEnumerator RealClickAt(Vector2 at, string tag, Button target = null, GameObject expectedObject = null)
        {
            var es = EventSystem.current;
            if (es == null || es.currentInputModule == null || !es.currentInputModule.isActiveAndEnabled ||
                es.currentInputModule.GetType().Name != "InputSystemUIInputModule") { Fail("missing active InputSystem UI module " + tag); yield break; }
            var hits = new List<RaycastResult>();
            es.RaycastAll(new PointerEventData(es) { position = at }, hits);
            bool hit = hits.Count > 0 && (target == null || hits[0].gameObject.GetComponentInParent<Button>() == target) &&
                (expectedObject == null || hits[0].gameObject == expectedObject || hits[0].gameObject.transform.IsChildOf(expectedObject.transform));
            Input("ugui-raycast", tag + " eventSystem=" + es.name + " module=" + es.currentInputModule.GetType().FullName +
                " target=" + (target == null ? "coordinate" : target.name) + " firstHit=" + (hits.Count == 0 ? "none" : hits[0].gameObject.name) + " accepted=" + hit);
            if (!hit) { Fail("raycast missed target " + tag); yield break; }
            var m = CurMouse();
            if (m == null) { Fail("no-mouse-device " + tag); yield break; }
            Input("mouse-down", tag + " pos=" + F(at.x) + "x" + F(at.y));
            InputSystem.QueueStateEvent(m, new MouseState { position = at }.WithButton(MouseButton.Left));
            yield return null; yield return null;
            InputSystem.QueueStateEvent(m, new MouseState { position = at });
            Input("mouse-up", tag + " pos=" + F(at.x) + "x" + F(at.y));
            yield return null; yield return null;
        }
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool SetCursorPos(int x, int y);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern void mouse_event(uint flags, uint dx, uint dy, uint data, IntPtr extra);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern IntPtr GetForegroundWindow();
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool SetForegroundWindow(IntPtr hWnd);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool GetClientRect(IntPtr hWnd, out RECT rect);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool ClientToScreen(IntPtr hWnd, ref POINT point);
        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
        struct RECT { public int Left, Top, Right, Bottom; }
        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
        struct POINT { public int X, Y; }
        const uint MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004;
        IEnumerator RealClickGui(float guiX, float guiY, float w, float h, string tag)
        {
            float scale = CombatUI.Scale;
            float cx = (guiX + w * .5f) * scale;
            float cy = (guiY + h * .5f) * scale;
            IntPtr hwnd = IntPtr.Zero;
            try { hwnd = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle; } catch { }
            uint ownPid = (uint)System.Diagnostics.Process.GetCurrentProcess().Id, windowPid, foregroundPid;
            if (hwnd == IntPtr.Zero) { Fail("no native Player window " + tag); yield break; }
            GetWindowThreadProcessId(hwnd, out windowPid);
            if (windowPid != ownPid) { Fail("native window PID mismatch " + tag); yield break; }
            bool foregroundRequested = SetForegroundWindow(hwnd);
            Input("native-foreground-request", tag + " result=" + foregroundRequested); yield return WaitFrames(10);
            GetWindowThreadProcessId(GetForegroundWindow(), out foregroundPid);
            if (foregroundPid != ownPid) { Fail("Player not foreground; no OS click sent " + tag); yield break; }
            RECT cr;
            POINT origin = new POINT { X = 0, Y = 0 };
            if (!GetClientRect(hwnd, out cr) || !ClientToScreen(hwnd, ref origin) || cx < 0 || cy < 0 || cx >= cr.Right || cy >= cr.Bottom)
            { Fail("invalid native client coordinates " + tag); yield break; }
            Input("native-window", tag + " ownPid=" + ownPid + " windowPid=" + windowPid + " foregroundPid=" + foregroundPid);
            int sx = origin.X + Mathf.RoundToInt(cx);
            int sy = origin.Y + Mathf.RoundToInt(cy);
            Input("native-mouse-down", tag + " client=" + F(cx) + "x" + F(cy) + " screen=" + sx + "x" + sy +
                  " scale=" + F(scale) + " clientRect=" + cr.Right + "x" + cr.Bottom + " origin=" + origin.X + "x" + origin.Y);
            if (!SetCursorPos(sx, sy)) { Fail("SetCursorPos failed " + tag); yield break; }
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, IntPtr.Zero);
            yield return null; yield return null; yield return null;
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, IntPtr.Zero);
            Input("native-mouse-up", tag + " screen=" + sx + "x" + sy);
            yield return WaitFrames(12);
            string shot = Path.Combine(root, "native-" + tag + ".png");
            ScreenCapture.CaptureScreenshot(shot); yield return WaitFrames(12);
            Check("native-screenshot-" + tag, File.Exists(shot), "post-click screenshot " + shot);
        }
        void SelectSample(string id)
        {
            var p = CatInventoryPresenter.Instance;
            if (p != null) { p.Select(id); Input("select-sample", "CatInventoryPresenter.Select id=" + Short(id)); }
            else { ContainerInventoryView.Select(id); Input("select-sample", "ContainerInventoryView.Select id=" + Short(id)); }
        }
        // Real click on a Camp transfer ROW, resolved by the product's own
        // CatTransferClick component (id + warehouse flag) instead of by label,
        // so duplicate item names can never make the click ambiguous.
        IEnumerator RealClickRow(string id, bool warehouse, string tag)
        {
            if (inv.CurrentPage == PlayerInventory.Page.Items && !warehouse) {
                var slot = UnityEngine.Object.FindObjectsByType<CatGridSlot>(FindObjectsInactive.Exclude, FindObjectsSortMode.None)
                    .FirstOrDefault(x => x.id == id);
                if (slot == null) { Fail("grid-item-missing " + tag + " id=" + id); yield break; }
                var rt = slot.GetComponent<RectTransform>(); var corners = new Vector3[4]; rt.GetWorldCorners(corners);
                var at = RectTransformUtility.WorldToScreenPoint(null, (corners[0] + corners[2]) * .5f);
                yield return RealClickAt(at, tag, null, slot.gameObject); yield return WaitFrames(12);
                Check("selected-id-" + tag, CatInventoryPresenter.Instance.SelectedId == id, "real grid selected id=" + id);
                yield break;
            }
            var all = UnityEngine.Object.FindObjectsByType<Button>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            var b = all.FirstOrDefault(x =>
            {
                var t = x.GetComponent<CatTransferClick>();
                return x.gameObject.activeInHierarchy && t != null && t.id == id && t.warehouse == warehouse;
            });
            if (b == null)
            {
                Fail("row-missing " + tag + " id=" + Short(id) + " warehouse=" + warehouse);
                yield return null; yield break;
            }
            var scroll = b.GetComponentInParent<ScrollRect>();
            if (scroll != null && scroll.viewport != null) {
                var rt = b.GetComponent<RectTransform>();
                float range = Mathf.Max(0, scroll.content.rect.height - scroll.viewport.rect.height);
                if (range > 0) scroll.verticalNormalizedPosition = 1f - Mathf.Clamp01((-rt.anchoredPosition.y) / range);
                Canvas.ForceUpdateCanvases(); yield return WaitFrames(10);
            }
            Input("row-found", tag + " id=" + Short(id) + " warehouse=" + warehouse +
                  " name=" + b.gameObject.name + " interactable=" + b.interactable);
            yield return RealClickAt(ScreenCentre(b), tag, b);
        }
        IEnumerator PrepareSamples()
        {
            var qs = new[] { GearQuality.White, GearQuality.Green, GearQuality.Purple, GearQuality.Gold, GearQuality.Red };
            foreach (var q in qs)
            {
                var it = AdventureItems.New(GearType.Sword, q, hero);
                bool added = gear.Add(it);
                Input("sample-prepared", "AdventureItems.New(Sword," + q + ") Add=" + added + " id=" + Short(it.id));
            }
            foreach (var t in new[] { GearType.Spear, GearType.Staff, GearType.Bow,
                                      GearType.TwinBlades, GearType.Greatsword, GearType.Scythe,
                                      GearType.Accessory, GearType.Arms })
            {
                var it = AdventureItems.New(t, GearQuality.Green, hero);
                bool added = gear.Add(it);
                Input("sample-prepared", "AdventureItems.New(" + t + ",Green) Add=" + added + " id=" + Short(it.id));
            }
            // Two identical-attribute items to prove the stable id tie-break.
            for (int n = 0; n < 2; n++)
            {
                var it = AdventureItems.New(GearType.Sword, GearQuality.Purple, hero);
                gear.Add(it);
                Input("sample-prepared", "tie-break sample " + n + " id=" + Short(it.id));
            }
            Snap("samples-ready", "prepare", "samples prepared via product factory; no action under test yet");
            yield return WaitFrames(2);
        }

        // ---- C-02 sorting ---------------------------------------------------
        string Ids(IEnumerable<GearItem> list) => string.Join("|", list.Select(i => i.id));
        string SortedExpected(IEnumerable<GearItem> src, B2SortKey key, B2FilterSpec spec)
        {
            var list = src.Where(i => B2InventoryQuery.Matches(i, spec, gear, false)).ToList();
            switch (key)
            {
                case B2SortKey.AttackDesc: return Ids(list.OrderByDescending(i => i.Attack).ThenBy(i => i.id, StringComparer.Ordinal));
                case B2SortKey.QualityDesc: return Ids(list.OrderByDescending(i => (int)i.quality).ThenBy(i => i.id, StringComparer.Ordinal));
                case B2SortKey.TypeAsc: return Ids(list.OrderBy(i => (int)i.type).ThenBy(i => i.id, StringComparer.Ordinal));
                default: return Ids(list);
            }
        }
        IEnumerator RunSortUgui()
        {
            yield return PrepareSamples();
            inv.OpenPage(PlayerInventory.Page.Items);
            yield return WaitFrames(4);
            B2FilterState.Reset();
            yield return WaitFrames(3);
            string baseIds = Ids(gear.items);
            string originalGear = NineCanonical()["GearItem"];

            foreach (var key in B2FilterState.SortCycle)
            {
                B2FilterState.SetSort(key);
                yield return WaitFrames(4); // let Build() re-render with the new spec key
                var expected = SortedExpected(gear.items, key, B2FilterState.Current);
                var actual = B2SortView.UguiOrderIds;
                string rendered = RenderedSortIds();
                bool same = expected == actual && rendered == expected;
                bool unchanged = Ids(gear.items) == baseIds;
                Check("sort-ugui-" + key, same, "Apply expected=" + expected.Length + "chars published=" + actual.Length +
                      "chars equal=" + same + " rendered=" + rendered + " underlyingOrderUnchanged=" + unchanged +
                      " signature=" + B2SortView.UguiSignature);
                Snap("sort", "ugui-" + key, "sortKey=" + key + " count=" + B2SortView.UguiCount +
                     " expected=" + expected + " published=" + actual + " spec=" + B2FilterState.Current.Key,
                     "sortKey", key.ToString(), "expectedIds", expected, "publishedIds", actual,
                     "signature", B2SortView.UguiSignature);
            }
            // None must preserve the ORIGINAL source order.
            B2FilterState.SetSort(B2SortKey.None);
            yield return WaitFrames(3);
            Check("sort-ugui-default-original", B2SortView.UguiOrderIds == baseIds,
                  "default order equals gear.items original id sequence");
            // Filter first, THEN sort: only Gold items may appear.
            B2FilterState.SetQuality(1 << (int)GearQuality.Gold);
            B2FilterState.SetSort(B2SortKey.AttackDesc);
            yield return WaitFrames(4);
            var filtered = B2InventoryQuery.Apply(gear.items, B2FilterState.Current, gear, false);
            bool allGold = filtered.All(i => i.quality == GearQuality.Gold);
            bool sorted = filtered.Select(i => i.Attack).SequenceEqual(filtered.Select(i => i.Attack).OrderByDescending(a => a));
            Check("sort-ugui-filter-then-sort", allGold && sorted,
                  "filteredCount=" + filtered.Count + " allGold=" + allGold + " attackDesc=" + sorted);
            // Stable tie-break for equal sort values (id ordinal ascending).
            var ties = gear.items.Where(i => i.quality == GearQuality.Purple && i.Weapon).ToArray();
            var tieSorted = B2InventoryQuery.ApplySortOnly(ties, B2SortKey.AttackDesc, gear, false);
            string tieIds = Ids(tieSorted);
            string tieExpect = Ids(ties.OrderByDescending(i => i.Attack).ThenBy(i => i.id, StringComparer.Ordinal));
            Check("sort-ugui-stable-tiebreak", tieIds == tieExpect, "tieGroup=" + ties.Length + " ids=" + tieIds);
            // Real Player click cycles the sort key through the 4 canonical states.
            B2FilterState.Reset();
            yield return WaitFrames(3);
            var seen = new List<string>();
            for (int n = 0; n < 4; n++)
            {
                yield return RealClick("排序↻", true, "ugui-sort-cycle-" + n);
                yield return WaitFrames(3);
                seen.Add(B2FilterState.Current.sort.ToString());
                Snap("sort", "ugui-realclick-" + n, "after real click sortKey=" + B2FilterState.Current.sort +
                     " published=" + B2SortView.UguiOrderIds, "sortKey", B2FilterState.Current.sort.ToString());
            }
            Check("sort-ugui-realclick-4cycles", seen.Distinct().Count() == 4 && seen[0] == "AttackDesc",
                  "real clicks produced " + string.Join(",", seen));
            // Sorting must not mutate ids / main / reserve / favourites / positions.
            Check("sort-ugui-no-state-mutation", Ids(gear.items) == baseIds &&
                  gear.mainWeapon == MainAtStart && B2Collection.Count == FavAtStartInt && NineCanonical()["GearItem"] == originalGear,
                  "ids/main/favourites unchanged after all sort cycles");
            B2FilterState.Reset();
            yield return WaitFrames(2);
        }
        string RenderedSortIds()
        {
            var scroll = UnityEngine.Object.FindObjectsByType<ScrollRect>(FindObjectsInactive.Exclude, FindObjectsSortMode.None)
                .FirstOrDefault(x => x.name == "B2排序目录");
            if (scroll == null || scroll.content == null) return "";
            return string.Join("|", scroll.content.GetComponentsInChildren<Text>(false)
                .Where(t => t.name.StartsWith("SortRow:", StringComparison.Ordinal))
                .OrderBy(t => t.transform.GetSiblingIndex()).Select(t => t.name.Substring("SortRow:".Length)));
        }
        string MainAtStart = "";
        int FavAtStartInt;
        IEnumerator RunSortImgui()
        {
            yield return PrepareSamples();
            var p = CatInventoryPresenter.Instance;
            inv.SetOpen(false); yield return WaitFrames(12);
            if (p != null) { p.enabled = false; Input("imgui-setup", "CatInventoryPresenter.enabled=false"); }
            inv.OpenPage(PlayerInventory.Page.Items);
            yield return WaitFrames(4);
            B2FilterState.Reset();
            yield return WaitFrames(3);
            float panelX = CombatUI.Width / 2f - 560f + 28f;
            float panelY = CombatUI.Height / 2f - 335f + 128f;
            string baseIds = Ids(gear.items);
            string originalGear = NineCanonical()["GearItem"];

            foreach (var key in B2FilterState.SortCycle)
            {
                B2FilterState.SetSort(key);
                yield return WaitFrames(4);
                var expected = SortedExpected(gear.items, key, B2FilterState.Current);
                var actual = B2SortView.ImguiOrderIds;
                bool same = expected == actual;
                Check("sort-imgui-" + key, same, "expected=" + expected.Length + "chars published=" + actual.Length + "chars");
                Snap("sort", "imgui-" + key, "sortKey=" + key + " count=" + B2SortView.ImguiCount +
                     " expected=" + expected + " published=" + actual,
                     "sortKey", key.ToString(), "expectedIds", expected, "publishedIds", actual,
                     "signature", B2SortView.ImguiSignature);
            }
            // C-03: the removed duplicate strip lived at (x, y) overlapping the
            // "装备盘 X/Y 格" title. Clicking there must NOT cycle quality now.
            B2FilterState.Reset();
            yield return WaitFrames(3);
            string beforeOld = B2FilterState.Current.Key;
            yield return RealClickGui(panelX, panelY, 68f, 26f, "C03-removed-duplicate-location");
            yield return WaitFrames(3);
            string afterOld = B2FilterState.Current.Key;
            Check("C03-no-duplicate-strip", beforeOld == afterOld,
                  "clicking old duplicate location did not change filter spec (" + beforeOld + " -> " + afterOld + ")");
            // The single retained strip at y+338 must still work.
            yield return RealClickGui(panelX + 144f, panelY + 338f, 68f, 26f, "C03-kept-strip-sort-cycle");
            yield return WaitFrames(3);
            Check("C03-kept-strip-works", B2FilterState.Current.sort != B2SortKey.None,
                  "clicking retained 排序↻ changed sortKey to " + B2FilterState.Current.sort);
            // IMGUI published order must equal uGUI's published order for the
            // SAME spec (cross-UI equality of the shared projection).
            B2FilterState.SetSort(B2SortKey.AttackDesc);
            yield return WaitFrames(4);
            string imguiIds = B2SortView.ImguiOrderIds;
            if (p == null) { Fail("missing presenter for real UI switch"); yield break; }
            p.enabled = true; inv.OpenPage(PlayerInventory.Page.Items); p.RequestRefresh();
            yield return WaitFrames(15);
            string renderedIds = RenderedSortIds();
            Check("C02-imgui-ugui-same-order", imguiIds.Length > 0 && imguiIds == B2SortView.UguiOrderIds && renderedIds == imguiIds,
                  "real UI switch imgui=" + imguiIds + " ugui=" + B2SortView.UguiOrderIds + " rendered=" + renderedIds);
            Check("sort-imgui-no-state-mutation", Ids(gear.items) == baseIds && NineCanonical()["GearItem"] == originalGear,
                  "underlying gear.items order unchanged");
            B2FilterState.Reset();
            if (p != null) p.enabled = true;
            yield return WaitFrames(2);
        }

        // ---- C-01 + R1-07 collection lifecycle -----------------------------
        IEnumerable<GearItem> LiveItems()
        {
            var camp = AdventureRecipes.Camp(hero);
            var pending = session.Flow.Profile.pending;
            return gear.items.Concat(camp.Items).Concat(pending.Where(r => r.equipment && r.item != null).Select(r => r.item));
        }
        string LifecycleState() => "{\"raw\":" + RawState() + ",\"favCount\":" + B2Collection.Count +
            ",\"favIds\":\"" + Esc(string.Join(",", LiveItems().Where(i => B2Collection.IsFavorite(i.id)).Select(i => i.id).Distinct())) +
            "\",\"ore\":" + inv.Count(MaterialKind.Ore) + "}";
        void LifeCheck(string tag, string before, bool ok, string detail)
        {
            Step(tag, before, LifecycleState(), ok ? "PASS" : "FAIL");
            Check(tag, ok, detail);
        }
        IEnumerator RunCollection()
        {
            yield return PrepareSamples();
            var camp = AdventureRecipes.Camp(hero);
            if (camp == null || !camp.InCamp) { Fail("collection requires real camp"); yield break; }
            inv.OpenPage(PlayerInventory.Page.Items); B2FilterState.Reset();
            CatInventoryPresenter.Instance.RequestRefresh(); yield return WaitFrames(12);
            var target = gear.items.FirstOrDefault(i => i.InBag && !gear.Carried(i) && !gear.ProtectedEntry(i) && i.quality == GearQuality.White && i.Weapon);
            if (target == null) { Fail("no unprotected lifecycle target"); yield break; }
            string tid = target.id, identity = ItemIdentity(target);
            var bagIds = gear.items.Where(i => i.InBag).Select(i => i.id).ToArray();
            B2Collection.Add("r1-ghost-other-container");
            bool scoped = B2Collection.BatchPreservesFavourites(bagIds, bagIds);
            B2Collection.Remove("r1-ghost-other-container");
            Check("C01-scoped-guard-api", scoped, "out-of-scope favourite does not reject same bag id set");
            B2Collection.Add("r1-in-scope-fav");
            bool rejected = !B2Collection.BatchPreservesFavourites(bagIds.Concat(new[] { "r1-in-scope-fav" }), bagIds);
            B2Collection.Remove("r1-in-scope-fav");
            Check("C01-real-loss-api", rejected, "in-scope missing id rejected");

            // Item selection and all lifecycle UI actions use pointer events.
            yield return RealClickRow(tid, false, "life-select-item"); yield return WaitFrames(12);
            string before = LifecycleState();
            yield return RealClick("★收藏", true, "life-1-favourite"); yield return WaitFrames(12);
            LifeCheck("life-1-favourite", before, B2Collection.IsFavorite(tid), "selected id=" + tid);
            if (failed) yield break;

            inv.OpenPage(PlayerInventory.Page.Camp); CampInventoryView.SelectSection(0);
            CatInventoryPresenter.Instance.RequestRefresh(); yield return WaitFrames(12);
            yield return RealClickRow(tid, false, "life-deposit-row"); yield return WaitFrames(12);
            int total = gear.items.Count + camp.Items.Count;
            before = LifecycleState();
            yield return RealClick("存入选中装备", true, "life-2-deposit"); yield return WaitFrames(12);
            var stored = camp.Items.FirstOrDefault(i => i.id == tid);
            bool deposited = !gear.items.Any(i => i.id == tid) && camp.Items.Count(i => i.id == tid) == 1 && stored != null &&
                ItemIdentity(stored) == identity && gear.items.Count + camp.Items.Count == total && B2Collection.IsFavorite(tid);
            LifeCheck("life-2-deposit", before, deposited, "source absent/destination unique/identity/count/favourite");
            if (failed) yield break;

            before = LifecycleState(); string idsBefore = Ids(gear.items.OrderBy(i => i.id));
            yield return RealClick("整理背包", true, "life-sortbag-warehouse-favourite"); yield return WaitFrames(12);
            LifeCheck("C01-sortbag-warehouse-favourite", before, B2Collection.IsFavorite(tid) && idsBefore == Ids(gear.items.OrderBy(i => i.id)) &&
                !(inv.CurrentNotice ?? "").Contains("遗漏收藏"), "real bag sort with favourite in warehouse");

            yield return RealClickRow(tid, true, "life-withdraw-row"); yield return WaitFrames(12);
            before = LifecycleState();
            yield return RealClick("取回选中装备", true, "life-3-withdraw"); yield return WaitFrames(12);
            target = gear.items.FirstOrDefault(i => i.id == tid);
            bool withdrawn = target != null && gear.items.Count(i => i.id == tid) == 1 && !camp.Items.Any(i => i.id == tid) &&
                ItemIdentity(target) == identity && gear.items.Count + camp.Items.Count == total && B2Collection.IsFavorite(tid);
            LifeCheck("life-3-withdraw", before, withdrawn, "source absent/destination unique/identity/count/favourite");
            if (failed) yield break;

            // Ensure the reverse scoped guard is exercised with non-empty warehouse.
            var other = gear.items.FirstOrDefault(i => i.InBag && !gear.Carried(i) && !gear.ProtectedEntry(i) && i.id != tid);
            if (other == null) { Fail("no warehouse sort companion"); yield break; }
            yield return RealClickRow(other.id, false, "life-warehouse-companion"); yield return WaitFrames(12);
            yield return RealClick("存入选中装备", true, "life-companion-deposit"); yield return WaitFrames(12);
            before = LifecycleState(); string whIds = Ids(camp.Items.OrderBy(i => i.id));
            yield return RealClick("整理仓库", true, "life-sortwarehouse-bag-favourite"); yield return WaitFrames(12);
            LifeCheck("C01-sortwarehouse-bag-favourite", before, camp.Items.Any(i => i.id == other.id) && B2Collection.IsFavorite(tid) &&
                whIds == Ids(camp.Items.OrderBy(i => i.id)) && !(inv.CurrentNotice ?? "").Contains("遗漏收藏"), "real warehouse sort with favourite in bag");

            inv.OpenPage(PlayerInventory.Page.Items); CatInventoryPresenter.Instance.RequestRefresh(); yield return WaitFrames(12);
            yield return RealClickRow(tid, false, "life-unfavourite-row"); yield return WaitFrames(12);
            before = LifecycleState();
            yield return RealClick("★取消收藏", true, "life-4-unfavourite"); yield return WaitFrames(12);
            LifeCheck("life-4-unfavourite", before, !B2Collection.IsFavorite(tid), "explicit UI un-favourite");
            inv.OpenPage(PlayerInventory.Page.Camp); CatInventoryPresenter.Instance.RequestRefresh(); yield return WaitFrames(12);
            before = LifecycleState();
            yield return RealClick("整理背包", true, "life-5-normal-sort"); yield return WaitFrames(12);
            LifeCheck("life-5-normal-sort", before, gear.items.Any(i => i.id == tid) && !B2Collection.IsFavorite(tid) &&
                !(inv.CurrentNotice ?? "").Contains("遗漏收藏"), "normal sort keeps item");

            inv.OpenPage(PlayerInventory.Page.Items); CatInventoryPresenter.Instance.RequestRefresh(); yield return WaitFrames(12);
            yield return RealClickRow(tid, false, "life-refavourite-row"); yield return WaitFrames(12);
            before = LifecycleState();
            yield return RealClick("★收藏", true, "life-6-refavourite"); yield return WaitFrames(12);
            LifeCheck("life-6-refavourite", before, B2Collection.IsFavorite(tid), "refavourite");
            before = LifecycleState(); int oreBefore = inv.Count(MaterialKind.Ore);
            yield return RealClick("已收藏 · 先取消收藏", false, "life-6-ui-refusal"); yield return WaitFrames(12);
            LifeCheck("life-6-ui-refusal", before, gear.items.Any(i => i.id == tid) && B2Collection.IsFavorite(tid) && inv.Count(MaterialKind.Ore) == oreBefore,
                "disabled button cannot dismantle");
            before = LifecycleState();
            Input("protection-api", "AdventureLoadout.Salvage favourite id=" + tid);
            gear.Salvage(target); yield return WaitFrames(12);
            LifeCheck("life-6-authoritative-refusal", before, gear.items.Any(i => i.id == tid) && B2Collection.IsFavorite(tid) &&
                inv.Count(MaterialKind.Ore) == oreBefore && (inv.CurrentNotice ?? "").Contains("已收藏"), "real product Salvage guard, explicitly API not UI");
            if (failed) yield break;

            before = LifecycleState();
            yield return RealClick("★取消收藏", true, "life-7-unfavourite"); yield return WaitFrames(12);
            LifeCheck("life-7-unfavourite", before, !B2Collection.IsFavorite(tid), "explicit removal before legal dismantle");
            before = LifecycleState();
            yield return RealClick("拆解换铁矿…", true, "life-7-arm"); yield return WaitFrames(12);
            LifeCheck("life-7-arm", before, gear.items.Any(i => i.id == tid) && inv.Count(MaterialKind.Ore) == oreBefore && FindButton("确认拆解") != null,
                "first click arms only");
            before = LifecycleState(); int reward = (int)target.quality + 1;
            yield return RealClick("确认拆解", true, "life-7-confirm"); yield return WaitFrames(12);
            LifeCheck("life-7-dismantle", before, !gear.items.Any(i => i.id == tid) && !B2Collection.IsFavorite(tid) && inv.Count(MaterialKind.Ore) == oreBefore + reward,
                "consumed exactly once; ore delta=" + reward + "; favourite was explicitly removed, not proof of NotifyGearDestroyed alone");
            if (failed) yield break;

            before = LifecycleState(); B2Collection.Add("r1-nonexistent-equipment-id");
            int countBefore = B2Collection.Count;
            Input("protection-api", "PruneStale loadout+warehouse+pending union");
            int pruned = B2Collection.PruneStale(LiveItems().Select(i => i.id));
            LifeCheck("C01-prune-stale-api", before, pruned == 1 && B2Collection.Count == countBefore - 1, "pending equipment retained in union");

            var picks = LiveItems().GroupBy(i => i.id).Select(g => g.First()).Take(3).ToArray();
            before = LifecycleState();
            foreach (var item in picks) B2Collection.Add(item.id);
            bool saved = session.Saves.SaveProgress(false);
            var marker = new SeedMarker { token = B2Collection.SessionToken, count = B2Collection.Count.ToString(CultureInfo.InvariantCulture),
                ids = string.Join(",", picks.Select(i => i.id)), profileId = session.Flow.Profile.profileId, sourceRunId = runId,
                identities = picks.Select(ItemIdentity).ToArray() };
            if (saved) File.WriteAllText(SeedPath, JsonUtility.ToJson(marker));
            LifeCheck("life-restart-seed-save", before, saved && picks.Length > 0 && File.Exists(session.Saves.SavePath), "same-character isolated save published; seed archived in run root");
            yield return WaitFrames(12);
        }
        static string SeedPath => Path.Combine(root, "r1-seed.json");
        [Serializable] class SeedMarker { public string token, count, ids, profileId, sourceRunId; public string[] identities; }
        IEnumerator RunRestart()
        {
            yield return WaitFrames(12);
            if (!File.Exists(SeedPath)) { Fail("restart requires archived collection seed and copied save"); yield break; }
            var marker = JsonUtility.FromJson<SeedMarker>(File.ReadAllText(SeedPath));
            string before = LifecycleState();
            var ids = marker.ids.Split(','); var live = LiveItems().ToArray();
            bool identity = marker.identities != null && marker.identities.Length == ids.Length && ids.Select((id, n) =>
                live.Count(i => i.id == id) == 1 && ItemIdentity(live.First(i => i.id == id)) == marker.identities[n]).All(v => v);
            bool ok = marker.sourceRunId != runId && marker.profileId == session.Flow.Profile.profileId && identity &&
                marker.count != "0" && B2Collection.Count == 0 && marker.token != B2Collection.SessionToken && ids.All(id => !B2Collection.IsFavorite(id));
            LifeCheck("life-8-same-character-restart", before, ok, "sourceRun=" + marker.sourceRunId + " profile=" + marker.profileId +
                " same-equipment=" + identity + " oldToken=" + marker.token + " newToken=" + B2Collection.SessionToken);
        }

        // ---- C-05 Strength through the REAL chain ---------------------------
        IEnumerator RunStrength(int rank)
        {
            yield return PrepareSamples();
            // RestoreProgress is EXACTLY the product's v9 save-restore entry
            // (CombatSaveSystem.cs:210). It writes ranks[], NOT AttackPower.
            // AttackPower is then derived: 25 + gear.Attack + Rank(Strength)*5.
            var ranks = new int[6]; ranks[(int)BasicSkill.Strength] = rank;
            hero.Progression.RestoreProgress(5, 0, ranks, new string[0], new int[0]);
            yield return WaitFrames(4);
            int actualRank = hero.Progression.Rank(BasicSkill.Strength);
            float bonus = hero.Progression.AttackBonus;
            float gearAtk = gear.Attack;
            float ap = hero.AttackPower;
            float expectedBonus = rank * 5f;
            float expectedAp = hero.attackDamage + gearAtk + expectedBonus;
            var combat = hero.GetComponent<AdventureCombat>();
            Snap("strength", "chain", "rank=" + actualRank + " AttackBonus=" + F(bonus) +
                 " gearAttack=" + F(gearAtk) + " AttackPower=" + F(ap) +
                 " expectedBonus=" + F(expectedBonus) + " expectedAP=" + F(expectedAp) +
                 " BasicPower=" + F(combat.BasicPower) + " StrengthX5=" + F(actualRank * 5f));
            Check("strength-rank-" + rank, actualRank == rank, "Rank(Strength)=" + actualRank);
            Check("strength-x5-" + rank, Mathf.Abs(bonus - expectedBonus) < .001f,
                  "AttackBonus=" + F(bonus) + " expected=" + F(expectedBonus));
            Check("strength-final-ap-" + rank, Mathf.Abs(ap - expectedAp) < .01f,
                  "AttackPower=" + F(ap) + " = 25 + gearAttack " + F(gearAtk) + " + bonus " + F(expectedBonus));
            float expectedBasic = expectedAp * (gear.Weapon == GearType.Spear ? AdventureCombat.SpearPower : 1f);
            Check("strength-basic-power-" + rank, Mathf.Abs(combat.BasicPower - expectedBasic) < .01f, "actual=" + F(combat.BasicPower) + " expected=" + F(expectedBasic));
            // PreviewReplacement must include the SAME progressionBonus.
            var cand = gear.items.FirstOrDefault(i => i.InBag && i.Weapon && !gear.Carried(i) && i.quality == GearQuality.Red);
            if (cand != null)
            {
                var ev = gear.PreviewReplacement(cand, B2EquipRole.Main);
                Check("strength-preview-before-" + rank, Mathf.Abs(ev.before.attackPower - ap) < .01f,
                      "preview before.attackPower=" + F(ev.before.attackPower) + " liveAP=" + F(ap));
                float mainExpected = IndependentAttack(cand, B2EquipRole.Main) + hero.attackDamage + expectedBonus;
                Check("strength-preview-after-" + rank, ev.feasible && Mathf.Abs(ev.after.attackPower - mainExpected) < .01f &&
                    Mathf.Abs(ev.after.progressionBonus - expectedBonus) < .001f && Mathf.Abs(ev.deltaAttackPower - (mainExpected - ap)) < .01f,
                    "after=" + F(ev.after.attackPower) + " expected=" + F(mainExpected));
                Snap("strength", "preview", "real Main candidate", "candidateId", cand.id, "candidateJson", ItemJson(cand), "evaluationJson", JsonUtility.ToJson(ev));
            }
            else { Fail("missing Strength preview candidate"); }
            // HUD / character page: real uGUI Text objects rendered by the product.
            inv.OpenPage(PlayerInventory.Page.Character);
            yield return WaitFrames(5);
            var texts = UnityEngine.Object.FindObjectsByType<Text>(FindObjectsInactive.Exclude, FindObjectsSortMode.None);
            string statLine = "", skillLine = "";
            foreach (var t in texts)
            {
                if (t.text.Contains("普攻 ") && t.text.Contains("防御")) statLine = t.text;
                if (t.text.Contains("强力打击")) skillLine = t.text;
            }
            bool hudRank = skillLine.Contains(actualRank + "级");
            bool hudBasic = statLine.Contains("普攻 " + combat.BasicPower.ToString("0.##", CultureInfo.CurrentCulture));
            Check("strength-hud-display-" + rank, hudRank && hudBasic,
                  "characterPage StatLine=" + Esc(statLine) + " | StrengthLine=" + Esc(skillLine));
            Snap("strength", "hud", "statLine=" + Esc(statLine) + " strengthLine=" + Esc(skillLine) +
                 " imhudSource=CombatHud.cs:19 renders 攻击 {hero.AttackPower:0}");
            // A real screenshot of the rendered HUD (bag closed) as visual evidence.
            inv.SetOpen(false);
            yield return WaitFrames(4);
            bool shotOk = false;
            try
            {
                string shot = Path.Combine(root, "r1-hud-strength-" + rank + ".png");
                ScreenCapture.CaptureScreenshot(shot);
                Input("hud-screenshot", "strength=" + rank + " path=" + shot);
                shotOk = true;
            }
            catch (Exception e) { Input("hud-screenshot-unavailable", e.GetType().Name); }
            yield return WaitFrames(4);
            Check("strength-screenshot-" + rank, shotOk && File.Exists(Path.Combine(root, "r1-hud-strength-" + rank + ".png")), "screenshot file exists");
            Snap("strength", "hud-screenshot", "captured=" + shotOk + " rank=" + rank);
            inv.SetOpen(true);
            yield return WaitFrames(2);
        }

        // Independent enumeration of the active set, not a call to B2AttackModel.
        float IndependentAttack(GearItem candidate = null, B2EquipRole role = B2EquipRole.None)
        {
            string main = role == B2EquipRole.Main ? candidate.id : gear.mainWeapon;
            float value = (gear.Rig == null ? 0 : gear.Rig.attackBonus) + (gear.Bag == null ? 0 : gear.Bag.attackBonus);
            var seen = new HashSet<string>();
            foreach (var i in gear.items) {
                if (!seen.Add(i.id)) continue;
                bool board = i.board, worn = i.worn, overflow = i.overflow;
                if (candidate != null && i.id == candidate.id) {
                    board = role == B2EquipRole.Board; worn = false; overflow = role == B2EquipRole.Overflow;
                }
                if (!worn && !overflow && (board || (i.id == main && i.Weapon && !board))) value += i.Attack;
            }
            return value;
        }
        // ---- C-06 nine-item read-only fingerprints --------------------------
        IEnumerator RunPreview9()
        {
            yield return PrepareSamples();
            inv.OpenPage(PlayerInventory.Page.Items);
            yield return WaitFrames(4);
            var cand = gear.items.FirstOrDefault(i => i.InBag && i.Weapon &&
                                                     !gear.Carried(i) && i.quality == GearQuality.Red);
            if (cand == null) { Fail("no preview candidate"); yield break; }
            string cid = cand.id;
            // Eight roles, each with a full nine-item before/after fingerprint.
            var roles = (B2EquipRole[])Enum.GetValues(typeof(B2EquipRole));
            foreach (var role in roles)
            {
                GearItem roleCandidate = cand;
                if (role == B2EquipRole.Worn || role == B2EquipRole.ContainerRig || role == B2EquipRole.ContainerBag) {
                    var type = role == B2EquipRole.ContainerBag ? GearType.Backpack : GearType.ChestRig;
                    roleCandidate = gear.items.FirstOrDefault(i => i.type == type && !i.worn) ?? gear.items.FirstOrDefault(i => i.type == type);
                }
                if (roleCandidate == null) { Fail("missing valid candidate " + role); continue; }
                var canonicalBefore = NineCanonical(); var before = Nine();
                var ev = gear.PreviewReplacement(roleCandidate, role);
                var canonicalAfter = NineCanonical(); var after = Nine();
                bool allSame = before.Keys.All(k => before[k] == after[k]);
                Snap("preview9", "role-" + role, "allNineEqual=" + allSame +
                     " before=" + NineJson(before) + " after=" + NineJson(after) +
                     " feasible=" + ev.feasible + " deltaAP=" + F(ev.deltaAttackPower),
                     "allNineEqual", allSame.ToString(), "beforeJson", NineJson(before), "afterJson", NineJson(after),
                     "canonicalBeforeJson", NineJson(canonicalBefore), "canonicalAfterJson", NineJson(canonicalAfter),
                     "candidateId", roleCandidate.id, "candidateJson", ItemJson(roleCandidate), "evaluationJson", JsonUtility.ToJson(ev));
                Check("preview9-" + role, allSame && ev.feasible, "nine fingerprints identical with valid candidate " + role + "; container after-number correctness is outside C06");
                yield return null;
            }
            // After all previews the real equipment must still be usable:
            // real-click "设为主武器" and confirm mainWeapon changed.
            string mainBefore = gear.mainWeapon ?? "";
            yield return RealClickRow(cid, false, "preview9-select-real-item");
            yield return WaitFrames(12);
            yield return RealClick("设为主武器", true, "preview9-real-usage");
            yield return WaitFrames(4);
            bool usable = gear.mainWeapon == cid && gear.items.Any(i => i.id == cid);
            Check("preview9-equipment-still-usable", usable,
                  "main " + Short(mainBefore) + " -> " + Short(gear.mainWeapon) +
                  " itemStillPresent=" + gear.items.Any(i => i.id == cid));
            yield return WaitFrames(2);
        }

        // ---- C-04 GUID uniqueness (real data, in real Player process) -------
        IEnumerator RunGuid()
        {
            yield return WaitFrames(2);
            string p = Path.Combine(root, "r1-guid-manifest.json");
            if (!File.Exists(p)) { Check("C04-guid-manifest", false, "manifest missing"); yield break; }
            var man = JsonUtility.FromJson<GuidManifest>(File.ReadAllText(p));
            var all = new List<string>();
            if (man.preExisting != null) all.AddRange(man.preExisting.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries));
            var news = man.newGuids.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
            bool formatOK = news.Length == 3 && news.All(g => g.Length == 32 && g.All(c => "0123456789abcdef".IndexOf(c) >= 0));
            bool uniqueAmongNew = news.Distinct().Count() == 3;
            bool noCollision = news.All(g => !all.Contains(g));
            Check("C04-guid-format", formatOK, "three 32-hex lowercase guids");
            Check("C04-guid-unique", uniqueAmongNew, "pairwise distinct");
            Check("C04-guid-no-collision", noCollision,
                  "no collision against " + all.Count + " pre-existing GUIDs");
            Snap("verify", "guid", "preExisting=" + all.Count + " new=" + string.Join(",", news) +
                 " formatOK=" + formatOK + " unique=" + uniqueAmongNew + " noCollision=" + noCollision);
            yield return WaitFrames(2);
        }
        [Serializable] class GuidManifest { public string preExisting; public string newGuids; }

        // ---- re-verify B2 golden matrix unchanged by R1 ---------------------
        IEnumerator RunGoldenRecheck()
        {
            yield return WaitFrames(2);
            float live = gear.Attack;
            float unified = B2AttackModel.ComputeAttack(gear.items, gear.mainWeapon, gear.Rig, gear.Bag);
            bool bitsEqual = BitConverter.SingleToInt32Bits(live) == BitConverter.SingleToInt32Bits(unified);
            var snap = gear.AttackSnapshot();
            Check("golden-live-vs-unified", bitsEqual,
                  "gear.Attack=" + F(live) + " unified=" + F(unified) + " AP=" + F(snap.attackPower));
            var s = gear.AttackSnapshot();
            bool chain = Mathf.Abs(s.attackPower - (25f + s.loadoutAttack + s.progressionBonus)) < .01f;
            Check("golden-ap-chain", chain, "attackPower=" + F(s.attackPower) +
                  " base=" + F(s.baseDamage) + " loadout=" + F(s.loadoutAttack) + " progression=" + F(s.progressionBonus));
            yield return WaitFrames(2);
        }

        IEnumerator Run()
        {
            mode = File.ReadAllText(Path.Combine(root, "r1-mode.txt")).Trim();
            runId = File.ReadAllText(Path.Combine(root, "r1-run-id.txt")).Trim();
            obsPath = Path.Combine(root, "r1-observations.jsonl");
            inputPath = Path.Combine(root, "r1-input-events.jsonl");
            stepsPath = Path.Combine(root, "r1-state-changes.jsonl");
            resultPath = Path.Combine(root, "result.json");
            File.WriteAllText(obsPath, ""); File.WriteAllText(inputPath, ""); File.WriteAllText(stepsPath, "");
            Snap("boot", "driver", "mode=" + mode + " unity=" + Application.unityVersion + " dll=Assembly-CSharp (R1)");

            float deadline = Time.realtimeSinceStartup + 60f;
            bool attempted = false;
            while (!GameEntry.GameSceneAuthorized && Time.realtimeSinceStartup < deadline)
            {
                var ge = GameEntry.Instance;
                if (ge != null && !attempted)
                {
                    attempted = true;
                    try { if (!ge.Continue()) { if (mode == "restart") throw new InvalidOperationException("restart Continue failed; new character forbidden"); ge.AskNew(); ge.ConfirmNew(); } }
                    catch (Exception e) { Fail("GameEntry: " + e.GetType().Name); }
                }
                yield return null;
            }
            if (!GameEntry.GameSceneAuthorized) { Fail("GameEntry never authorized"); Finish(); yield break; }
            float sceneDeadline = Time.realtimeSinceStartup + 90f;
            while (GameEntry.Loading && Time.realtimeSinceStartup < sceneDeadline) yield return null;
            session = FindAnyObjectByType<CombatSession>();
            if (session == null) { Fail("no CombatSession"); Finish(); yield break; }
            try { GameEntry.DirectReady(); } catch { }
            hero = session.hero;
            if (hero == null) { Fail("no hero"); Finish(); yield break; }
            gear = hero.GetComponent<AdventureLoadout>();
            inv = hero.Inventory;
            if (gear == null || inv == null) { Fail("no AdventureLoadout/PlayerInventory"); Finish(); yield break; }
            MainAtStart = gear.mainWeapon ?? "";
            FavAtStartInt = B2Collection.Count;
            Snap("entry", "driver", "real Player entry complete; CatUI running=" + CatInventoryPresenter.Running +
                 " InCamp=" + (AdventureRecipes.Camp(hero) != null && AdventureRecipes.Camp(hero).InCamp));

            switch (mode)
            {
                case "sort-ugui": yield return RunSortUgui(); break;
                case "sort-imgui": yield return RunSortImgui(); break;
                case "collection": yield return RunCollection(); break;
                case "restart": yield return RunRestart(); break;
                case "strength0": yield return RunStrength(0); break;
                case "strength3": yield return RunStrength(3); break;
                case "preview9": yield return RunPreview9(); break;
                case "guid": yield return RunGuid(); break;
                case "golden": yield return RunGoldenRecheck(); break;
                default: Fail("unknown mode " + mode); break;
            }
            Snap("done", "driver", "mode=" + mode + " complete; failed=" + failed +
                 " checks=" + checks.Count + " pass=" + checks.Count(c => c.Contains("|PASS|")));
            Finish();
        }
        void Finish()
        {
            string verdict = failed ? "FAIL" : "PASS";
            try { File.WriteAllText(Path.Combine(root, "r1-complete.txt"), verdict); } catch { }
            var sb = new StringBuilder();
            sb.Append("{\n\"runId\":\"").Append(Esc(runId)).Append("\",\n");
            sb.Append("\"mode\":\"").Append(Esc(mode)).Append("\",\n");
            sb.Append("\"result\":\"").Append(verdict).Append("\",\n");
            sb.Append("\"checks\":").Append(checks.Count).Append(",\n");
            sb.Append("\"passed\":").Append(checks.Count(c => c.Contains("|PASS|"))).Append(",\n");
            sb.Append("\"failed\":").Append(checks.Count(c => c.Contains("|FAIL|"))).Append(",\n");
            sb.Append("\"detail\":[\n");
            for (int i = 0; i < checks.Count; i++)
            {
                var parts = checks[i].Split(new[] { '|' }, 3);
                sb.Append("  {\"name\":\"").Append(Esc(parts[0])).Append("\",\"result\":\"").Append(Esc(parts[1]))
                  .Append("\",\"detail\":\"").Append(Esc(parts.Length > 2 ? parts[2] : "")).Append("\"}")
                  .Append(i + 1 < checks.Count ? "," : "").Append("\n");
            }
            sb.Append("]\n}\n");
            try { File.WriteAllText(resultPath, sb.ToString()); } catch { }
            Exit(failed ? 3 : 0);
        }
        static void Exit(int code)
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(code);
#else
            Application.Quit(code);
#endif
        }
        void Start() { StartCoroutine(Run()); }
    }
}
