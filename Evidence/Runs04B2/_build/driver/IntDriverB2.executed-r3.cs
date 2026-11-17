// UX-04-B2 OBSERVATION driver (SIDECAR ONLY).
//
// Compiled as a separate assembly, injected into an isolated COPY of the B2
// Player. NEVER shipped, NEVER edits product source/save/schema/random stream.
//
// All ACTIONS under test are triggered by real InputSystem mouse events on the
// product's own buttons (uGUI UnityEngine.UI.Button or IMGUI GUI.Button).
// Sample GEAR is prepared through the product's OWN factory (AdventureItems.New
// + AdventureLoadout.Add / CampRuntime.Restore) -- preparation, not the action
// under test -- and every state is read from real runtime objects.
//
// Modes (b2-mode.txt):
//   golden    - bit-for-bit golden matrix: legacy calculation vs B2 unified chain,
//               7 weapon types, 5 qualities, reserve/overflow/worn/container/spear
//   ugui      - real-click uGUI filter tabs, comparison, collection, 2-step
//               dismantle, deposit/withdraw, warehouse-full reason
//   imgui     - real-click IMGUI filter tabs (presenter disabled for this run)
//   readback  - seeded v9 save: gold/red readable + B1 gate + collection cleared
//   restart   - fresh process: verify collection is empty at process start

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

namespace B2Observation
{
    public sealed class Driver : MonoBehaviour
    {
        static string root;
        string mode, runId, obsPath, inputPath;
        CombatSession session;
        ThirdPersonHero hero;
        AdventureLoadout gear;
        PlayerInventory inv;
        readonly StringBuilder obs = new StringBuilder();
        readonly StringBuilder inputs = new StringBuilder();
        int seq;
        bool failed;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        public static void Boot()
        {
            var env = Environment.GetEnvironmentVariable("UNITY_TEST_ROOT");
            if (string.IsNullOrEmpty(env)) return;
            if (!File.Exists(Path.Combine(env, "b2-mode.txt"))) return;
            root = env;
            Application.runInBackground = true;
            var host = new GameObject("UX04-B2 observation driver");
            DontDestroyOnLoad(host);
            host.AddComponent<Driver>();
        }

        static string F(float v) { return v.ToString("R", CultureInfo.InvariantCulture); }
        static string Esc(string s)
        {
            if (s == null) return "";
            return s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", " ").Replace("\r", " ");
        }
        static string Short(string id)
        {
            if (string.IsNullOrEmpty(id)) return "null";
            return id.Length <= 10 ? id : id.Substring(0, 10);
        }
        // IEEE-754 bit pattern: proves bit-for-bit equality, not rounding.
        static string Bits(float v) => BitConverter.SingleToInt32Bits(v).ToString(CultureInfo.InvariantCulture);

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
            sb.Append("\"CompareRole\":\"").Append(ContainerInventoryView.CompareRoleValue.ToString()).Append("\"");
            for (int i = 0; i + 1 < extra.Length; i += 2)
                sb.Append(",\"").Append(Esc(extra[i])).Append("\":\"").Append(Esc(extra[i + 1])).Append("\"");
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
        }
        void Input(string kind, string detail)
        {
            inputs.AppendLine("{\"kind\":\"" + Esc(kind) + "\",\"detail\":\"" + Esc(detail) +
                             "\",\"frame\":" + Time.frameCount + ",\"time\":" + F(Time.realtimeSinceStartup) + "}");
            Flush();
        }
        void Fail(string why)
        {
            failed = true;
            Snap("error", "driver", why);
            try { File.WriteAllText(Path.Combine(root, "b2-failure.txt"), why); } catch { }
        }
        IEnumerator WaitFrames(int n) { for (int i = 0; i < n; i++) yield return null; }

        // ---- real physical input -------------------------------------------
        Button FindButton(string name)
        {
            var all = UnityEngine.Object.FindObjectsByType<Button>(FindObjectsInactive.Include,
                                                                   FindObjectsSortMode.None);
            return all.FirstOrDefault(b => b.gameObject.name == name);
        }
        Vector2 ScreenCentre(Button b)
        {
            var rt = b.GetComponent<RectTransform>();
            var canvas = b.GetComponentInParent<Canvas>();
            var cam = canvas != null && canvas.renderMode != RenderMode.ScreenSpaceOverlay
                      ? canvas.worldCamera : null;
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
            if (b == null) { Input("button-missing", tag + " name=" + buttonName); yield return null; yield break; }
            bool interactable = b.interactable;
            Input("button-found", tag + " name=" + buttonName + " interactable=" + interactable +
                  " active=" + b.gameObject.activeInHierarchy);
            if (expectInteractable && !interactable)
                Input("button-disabled", tag + " name=" + buttonName + " (expected enabled but disabled)");
            var m = CurMouse();
            if (m == null) { Input("no-mouse-device", tag); yield break; }
            Vector2 at = ScreenCentre(b);
            yield return RealClickAt(at, tag);
        }
        IEnumerator RealClickAt(Vector2 at, string tag)
        {
            var m = CurMouse();
            if (m == null) { Input("no-mouse-device", tag); yield break; }
            Input("mouse-down", tag + " pos=" + F(at.x) + "x" + F(at.y));
            InputSystem.QueueStateEvent(m, new MouseState { position = at }.WithButton(MouseButton.Left));
            yield return null; yield return null;
            InputSystem.QueueStateEvent(m, new MouseState { position = at });
            Input("mouse-up", tag + " pos=" + F(at.x) + "x" + F(at.y));
            yield return null; yield return null;
        }
        // IMGUI GUI.Button consumes Event.current from the native event loop.
        // InputSystem.QueueStateEvent only feeds the uGUI EventSystem, so IMGUI
        // must be driven by REAL OS-level mouse input. Win32 P/Invoke below is
        // sidecar-only observation tooling; it never edits product source.
#if UNITY_STANDALONE_WIN || UNITY_EDITOR_WIN
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool SetCursorPos(int x, int y);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern void mouse_event(uint flags, uint dx, uint dy, uint data, IntPtr extra);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern IntPtr GetForegroundWindow();
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool GetClientRect(IntPtr hWnd, out RECT rect);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool ClientToScreen(IntPtr hWnd, ref POINT point);
        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
        struct RECT { public int Left, Top, Right, Bottom; }
        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
        struct POINT { public int X, Y; }
        const uint MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004;
#endif
        IEnumerator RealClickGui(float guiX, float guiY, float w, float h, string tag)
        {
#if UNITY_STANDALONE_WIN || UNITY_EDITOR_WIN
            float scale = CombatUI.Scale;
            // GUI.matrix scales drawing; IMGUI mouse coords stay in GUI space.
            // Physical client pixels are top-left origin -> no Screen.height flip.
            float cx = (guiX + w * .5f) * scale;
            float cy = (guiY + h * .5f) * scale;
            IntPtr hwnd = IntPtr.Zero;
            try { hwnd = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle; } catch { }
            if (hwnd == IntPtr.Zero) hwnd = GetForegroundWindow();
            RECT cr;
            GetClientRect(hwnd, out cr);
            POINT origin = new POINT { X = 0, Y = 0 };
            ClientToScreen(hwnd, ref origin);
            int sx = origin.X + Mathf.RoundToInt(cx);
            int sy = origin.Y + Mathf.RoundToInt(cy);
            Input("native-mouse-down", tag + " client=" + F(cx) + "x" + F(cy) +
                  " screen=" + sx + "x" + sy + " scale=" + F(scale) +
                  " clientRect=" + cr.Right + "x" + cr.Bottom + " origin=" + origin.X + "x" + origin.Y);
            SetCursorPos(sx, sy);
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, IntPtr.Zero);
            yield return null; yield return null; yield return null;
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, IntPtr.Zero);
            Input("native-mouse-up", tag + " screen=" + sx + "x" + sy);
            yield return null; yield return null; yield return null;
#else
            Input("native-mouse-unavailable", tag);
            yield return null;
#endif
        }
        void SelectSample(string id)
        {
            var p = CatInventoryPresenter.Instance;
            if (p != null) { p.Select(id); Input("select-sample", "CatInventoryPresenter.Select id=" + Short(id)); }
            else { ContainerInventoryView.Select(id); Input("select-sample", "ContainerInventoryView.Select id=" + Short(id)); }
        }

        // ---- golden matrix --------------------------------------------------
        // Legacy oracle: VERBATIM pre-B2 AdventureLoadout expression. Independent
        // of B2AttackModel. Compared by IEEE-754 bits with the unified chain.
        static float LegacyAttack(List<GearItem> items, string mainId,
                                  ContainerDefinition rig, ContainerDefinition bag)
        {
            var main = items.Find(i => i.id == mainId && i.InBag && i.Weapon);
            var unique = items.GroupBy(i => i.id).Select(g => g.First());
            var active = unique.Where(i => !i.overflow && !i.worn && (i.board || i == main));
            return active.Sum(i => i.Attack) + (rig != null ? rig.attackBonus : 0f) + (bag != null ? bag.attackBonus : 0f);
        }
        static float LegacyDefense(List<GearItem> items, string mainId,
                                   ContainerDefinition rig, ContainerDefinition bag)
        {
            var main = items.Find(i => i.id == mainId && i.InBag && i.Weapon);
            var unique = items.GroupBy(i => i.id).Select(g => g.First());
            var active = unique.Where(i => !i.overflow && !i.worn && (i.board || i == main));
            return active.Where(i => i.board).Sum(i => i.Defense) +
                   (rig != null ? rig.defenseBonus : 0f) + (bag != null ? bag.defenseBonus : 0f);
        }

        void GoldenRow(string name, List<GearItem> list, string mainId, string reserveId,
                       ContainerDefinition rig, ContainerDefinition bag,
                       float expectAttackPower, string expectNote)
        {
            float legacy = LegacyAttack(list, mainId, rig, bag);
            float unified = B2AttackModel.ComputeAttack(list, mainId, rig, bag);
            float legacyD = LegacyDefense(list, mainId, rig, bag);
            float unifiedD = B2AttackModel.ComputeDefense(list, mainId, rig, bag);
            bool bitsEqual = Bits(legacy) == Bits(unified);
            bool bitsEqualD = Bits(legacyD) == Bits(unifiedD);
            var snap = B2AttackModel.Snapshot(list, mainId, reserveId, rig, bag, hero);
            bool apMatch = expectAttackPower < 0 || Bits(snap.attackPower) == Bits(expectAttackPower);
            if (!bitsEqual || !bitsEqualD) Fail("GOLDEN bit mismatch: " + name);
            Snap("golden", "G-" + name,
                 "legacy=" + F(legacy) + " bits=" + Bits(legacy) +
                 " unified=" + F(unified) + " bits=" + Bits(unified) +
                 " defBitsLegacy=" + Bits(legacyD) + " defBitsUnified=" + Bits(unifiedD) +
                 " attackPower=" + F(snap.attackPower) + " basicPower=" + F(snap.basicPower) +
                 " main=" + F(snap.mainContribution) + " reserve=" + F(snap.reserveContribution) +
                 " accessory=" + F(snap.accessoryContribution) + " arms=" + F(snap.armsContribution) +
                 " container=" + F(snap.containerBonus) + " active=" + snap.activeCount +
                 " weapon=" + snap.weaponType + " | " + expectNote,
                 "goldenName", name, "bitsEqual", bitsEqual.ToString(),
                 "bitsEqualDefense", bitsEqualD.ToString(),
                 "apMatch", apMatch.ToString(),
                 "expectedAttackPower", F(expectAttackPower),
                 "legacyBits", Bits(legacy), "unifiedBits", Bits(unified),
                 "legacyDefenseBits", Bits(legacyD), "unifiedDefenseBits", Bits(unifiedD));
        }

        List<GearItem> CloneList()
        {
            var baseItems = gear.items.Select(i => i.Clone()).ToList();
            return baseItems;
        }

        IEnumerator RunGolden()
        {
            var rig0 = gear.Rig;
            var bag0 = gear.Bag;
            var baseList = CloneList();
            string main0 = gear.mainWeapon;
            string reserve0 = gear.reserveWeapon;

            // G0: unmodified baseline -- must equal live product chain bit-for-bit.
            float live = gear.Attack;
            float unifiedBase = B2AttackModel.ComputeAttack(gear.items, main0, rig0, bag0);
            bool liveMatch = Bits(live) == Bits(unifiedBase);
            if (!liveMatch) Fail("G0 live Attack != unified chain");
            Snap("golden", "G0-live", "live=" + F(live) + " bits=" + Bits(live) +
                 " unified=" + F(unifiedBase) + " bits=" + Bits(unifiedBase) +
                 " heroAttackPower=" + F(hero.AttackPower) + " liveMatch=" + liveMatch,
                 "liveBits", Bits(live), "unifiedBits", Bits(unifiedBase), "liveMatch", liveMatch.ToString());

            GoldenRow("baseline", baseList, main0, reserve0, rig0, bag0, -1f, "unmodified state");

            // G1: five qualities as main weapon (5-tier coverage).
            GearQuality[] qs = { GearQuality.White, GearQuality.Green, GearQuality.Purple, GearQuality.Gold, GearQuality.Red };
            foreach (var q in qs)
            {
                var l = CloneList();
                var it = AdventureItems.New(GearType.Sword, q, hero);
                it.worn = it.board = it.overflow = false;
                l.Add(it);
                GoldenRow("main-" + q, l, it.id, reserve0, rig0, bag0, -1f,
                          "quality=" + q + " power=" + F(it.Power) + " itemAttack=" + F(it.Attack));
            }

            // G2: SEVEN weapon types (incl. 3 new weapons).
            GearType[] weapons = { GearType.Sword, GearType.Spear, GearType.Staff, GearType.Bow,
                                   GearType.TwinBlades, GearType.Greatsword, GearType.Scythe };
            foreach (var t in weapons)
            {
                var l = CloneList();
                var it = AdventureItems.New(t, GearQuality.Purple, hero);
                it.worn = it.board = it.overflow = false;
                l.Add(it);
                var s = B2AttackModel.Snapshot(l, it.id, reserve0, rig0, bag0, hero);
                bool spear = s.weaponType == GearType.Spear;
                bool ratioOK = spear ? Mathf.Approximately(s.basicPower, s.attackPower * AdventureCombat.SpearPower)
                                     : Mathf.Approximately(s.basicPower, s.attackPower);
                if (!ratioOK) Fail("G2 spear multiplier mismatch: " + t);
                GoldenRow("weapon-" + t, l, it.id, reserve0, rig0, bag0, -1f,
                          "type=" + t + " basicPower=" + F(s.basicPower) + " spear=" + spear);
            }

            // G3: accessory (x0.5) and arms (x0.35) ON BOARD.
            foreach (var t in new[] { GearType.Accessory, GearType.Arms })
            {
                var l = CloneList();
                var it = AdventureItems.New(t, GearQuality.Red, hero);
                it.board = true; it.worn = false; it.overflow = false; it.x = 0; it.y = 0;
                l.Add(it);
                var s = B2AttackModel.Snapshot(l, main0, reserve0, rig0, bag0, hero);
                float factor = t == GearType.Accessory ? .5f : .35f;
                bool coeffOK = Mathf.Abs(it.Attack - it.Power * factor) < .01f;
                if (!coeffOK) Fail("G3 coefficient mismatch " + t + " attack=" + F(it.Attack));
                GoldenRow("board-" + t, l, main0, reserve0, rig0, bag0, -1f,
                          "type=" + t + " itemAttack=" + F(it.Attack) + " factor=" + F(factor) +
                          " accessoryContribution=" + F(s.accessoryContribution) +
                          " armsContribution=" + F(s.armsContribution));
            }

            // G4: RESERVE weapon contributes exactly 0 (the key anti-pattern).
            {
                var l = CloneList();
                var it = AdventureItems.New(GearType.Sword, GearQuality.Red, hero);
                it.worn = it.board = it.overflow = false;
                l.Add(it);
                var s = B2AttackModel.Snapshot(l, main0, it.id, rig0, bag0, hero);
                bool zero = Bits(s.reserveContribution) == Bits(0f);
                if (!zero) Fail("G4 reserve contribution is not zero");
                GoldenRow("reserve-red", l, main0, it.id, rig0, bag0, -1f,
                          "reserveContribution=" + F(s.reserveContribution) + " zero=" + zero);
            }

            // G5: Overflow / Worn / Board / InBag states for the SAME item.
            foreach (var state in new[] { "InBag", "Board", "Overflow", "Worn" })
            {
                var l = CloneList();
                var it = AdventureItems.New(GearType.Sword, GearQuality.Gold, hero);
                it.board = state == "Board";
                it.overflow = state == "Overflow";
                it.worn = state == "Worn";
                it.x = it.board ? 0 : -1; it.y = it.board ? 0 : -1;
                l.Add(it);
                GoldenRow("state-" + state, l, main0, reserve0, rig0, bag0, -1f,
                          "state=" + state + " InBag=" + it.InBag);
            }

            // G6: container attackBonus (bag_relic +6) and rig_heavy defenseBonus.
            {
                var l = CloneList();
                var bagRelic = AdventureCatalog.Container("bag_relic");
                var rigHeavy = AdventureCatalog.Container("rig_heavy");
                var s = B2AttackModel.Snapshot(l, main0, reserve0, rigHeavy, bagRelic, hero);
                bool bonusOK = Mathf.Abs(s.containerBonus - (rigHeavy.attackBonus + bagRelic.attackBonus)) < .001f;
                if (!bonusOK) Fail("G6 container bonus mismatch");
                GoldenRow("container-bonus", l, main0, reserve0, rigHeavy, bagRelic, -1f,
                          "rig=" + F(rigHeavy.attackBonus) + " bag=" + F(bagRelic.attackBonus) +
                          " containerBonus=" + F(s.containerBonus));
            }

            // G7: Preview() must be read-only AND must use the same chain.
            {
                int before = gear.items.Count;
                string mainBefore = gear.mainWeapon;
                var cand = AdventureItems.New(GearType.Sword, GearQuality.Red, hero);
                var evMain = gear.PreviewReplacement(cand, B2EquipRole.Main);
                var evReserve = gear.PreviewReplacement(cand, B2EquipRole.Reserve);
                bool unchanged = gear.items.Count == before && gear.mainWeapon == mainBefore;
                bool reserveZero = Bits(evReserve.deltaAttackPower) == Bits(0f);
                bool mainPositive = evMain.deltaAttackPower > 0f;
                if (!unchanged) Fail("G7 Preview mutated live state");
                if (!reserveZero) Fail("G7 reserve preview delta is not zero");
                if (!mainPositive) Fail("G7 main preview delta is not positive");
                Snap("golden", "G7-preview",
                     "readOnly=" + unchanged + " mainDelta=" + F(evMain.deltaAttackPower) +
                     " reserveDelta=" + F(evReserve.deltaAttackPower) +
                     " mainAP=" + F(evMain.before.attackPower) + "→" + F(evMain.after.attackPower) +
                     " reserveAP=" + F(evReserve.before.attackPower) + "→" + F(evReserve.after.attackPower) +
                     " mainRoleFeasible=" + evMain.feasible,
                     "readOnly", unchanged.ToString(), "reserveZero", reserveZero.ToString(),
                     "mainDelta", F(evMain.deltaAttackPower), "reserveDelta", F(evReserve.deltaAttackPower));
            }

            // G8: shared semantic filter rules (both UI paths use the SAME table).
            {
                var spec = B2FilterState.SpecForTab(1);
                bool weaponOK = spec.category == B2Category.Weapon;
                var filtered = B2InventoryQuery.Apply(gear.items, spec, gear, false);
                bool allWeapon = filtered.All(i => B2InventoryQuery.CategoryOf(i) == B2Category.Weapon);
                bool deterministic = Bits(B2AttackModel.ComputeAttack(gear.items, main0, rig0, bag0)) == Bits(live);
                if (!weaponOK || !allWeapon || !deterministic) Fail("G8 filter/determinism mismatch");
                Snap("golden", "G8-filter", "tabLabels=" + B2FilterTabs.Labels.Length +
                     " weaponTabOK=" + weaponOK + " filtered=" + filtered.Count +
                     " allWeapon=" + allWeapon + " chainDeterministic=" + deterministic +
                     " sourceLabel=" + B2InventoryQuery.SourceLabel(gear.items.FirstOrDefault()),
                     "tabCount", B2FilterTabs.Labels.Length.ToString(),
                     "filteredCount", filtered.Count.ToString());
            }
            yield return WaitFrames(2);
        }

        // ---- real-input acceptance (uGUI) ----------------------------------
        IEnumerator RunUgui()
        {
            yield return PrepareSamples();
            if (inv != null) { inv.OpenPage(PlayerInventory.Page.Items); Input("open-items", "OpenPage(Items)"); }
            yield return WaitFrames(4);
            Snap("entry", "ui", "uGUI Items page open=" + (inv != null && inv.IsOpen));

            // F1: real-click the 8 shared semantic tabs, one by one.
            for (int t = 0; t < B2FilterTabs.Labels.Length; t++)
            {
                yield return RealClick(B2FilterTabs.Labels[t], true, "uGUI-tab-" + t);
                yield return WaitFrames(3);
                Snap("filter", "uGUI-tab-" + t, "clicked=" + B2FilterTabs.Labels[t] +
                     " sharedTab=" + B2FilterState.Tab + " spec=" + B2FilterState.Describe());
            }
            B2FilterState.SetTab(0);
            yield return WaitFrames(2);

            // F2: comparison via real clicks on the role-cycle button.
            // Choose a NON-Carried red sword so Main/Reserve/Board deltas are
            // meaningful (using the starter main weapon would be a no-op swap).
            var sword = gear.items.FirstOrDefault(i => i.quality == GearQuality.Red && i.Weapon && i.InBag && !gear.Carried(i));
            if (sword != null)
            {
                SelectSample(sword.id);
                yield return WaitFrames(3);
                for (int r = 0; r < 8; r++)
                {
                    yield return RealClick("对比角色↻", true, "uGUI-compare-" + r);
                    yield return WaitFrames(2);
                    var ev = gear.PreviewReplacement(sword, ContainerInventoryView.CompareRoleValue);
                    Snap("compare", "uGUI-compare-" + r, "role=" + ContainerInventoryView.CompareRoleValue +
                         " feasible=" + ev.feasible + " AP=" + F(ev.before.attackPower) + "→" +
                         F(ev.after.attackPower) + " delta=" + F(ev.deltaAttackPower) +
                         " main=" + F(ev.after.mainContribution) + " reserve=" + F(ev.after.reserveContribution) +
                         " accessory=" + F(ev.after.accessoryContribution) + " arms=" + F(ev.after.armsContribution),
                         "role", ContainerInventoryView.CompareRoleValue.ToString(),
                         "delta", F(ev.deltaAttackPower), "feasible", ev.feasible.ToString());
                }
            }
            else Fail("uGUI: no weapon sample for comparison");

            // F3: collection toggle -> dismantle protection -> un-favourite.
            // Must NOT be the Carried starter main weapon (Salvage correctly
            // refuses carried items); pick a fresh non-carried white sample.
            var white = gear.items.FirstOrDefault(i => i.quality == GearQuality.White && i.InBag && i.Weapon && !gear.Carried(i));
            if (white != null)
            {
                SelectSample(white.id);
                yield return WaitFrames(3);
                yield return RealClick("★收藏", true, "uGUI-fav-add");
                yield return WaitFrames(3);
                bool added = B2Collection.IsFavorite(white.id);
                Snap("collection", "uGUI-fav-add", "favorite=" + added + " count=" + B2Collection.Count +
                     " token=" + B2Collection.SessionToken, "favorite", added.ToString());
                if (!added) Fail("uGUI: favourite was not added");

                // Dismantle must be blocked while favourited (button disabled).
                yield return RealClick("已收藏 · 先取消收藏", false, "uGUI-fav-blocked");
                yield return WaitFrames(3);
                bool canQuick = B2Collection.CanQuickDismantle(white);
                bool stillOwned = gear.items.Any(i => i.id == white.id);
                Snap("collection", "uGUI-fav-blocked", "canQuickDismantle=" + canQuick +
                     " stillOwned=" + stillOwned + " ore=" + inv.Count(MaterialKind.Ore),
                     "canQuickDismantle", canQuick.ToString(), "stillOwned", stillOwned.ToString());
                if (canQuick || !stillOwned) Fail("uGUI: favourite did not block dismantle");

                // Explicit un-favourite is always allowed.
                yield return RealClick("★取消收藏", true, "uGUI-fav-remove");
                yield return WaitFrames(3);
                bool removed = !B2Collection.IsFavorite(white.id);
                Snap("collection", "uGUI-fav-remove", "removed=" + removed + " count=" + B2Collection.Count,
                     "removed", removed.ToString());
                if (!removed) Fail("uGUI: un-favourite failed");

                // Two-step dismantle now succeeds only after confirm.
                yield return RealClick("拆解换铁矿…", true, "uGUI-salvage-arm");
                yield return WaitFrames(3);
                Snap("salvage", "uGUI-salvage-arm", "armed (no item consumed yet) stillOwned=" +
                     gear.items.Any(i => i.id == white.id));
                yield return RealClick("确认拆解", true, "uGUI-salvage-confirm");
                yield return WaitFrames(4);
                bool consumed = !gear.items.Any(i => i.id == white.id);
                Snap("salvage", "uGUI-salvage-confirm", "consumed=" + consumed +
                     " ore=" + inv.Count(MaterialKind.Ore), "consumed", consumed.ToString());
                if (!consumed) Fail("uGUI: two-step dismantle did not consume the white item");
            }
            else Fail("uGUI: no white sample");

            // F4: B1 gold/red gate still holds after B2.
            foreach (var q in new[] { GearQuality.Gold, GearQuality.Red })
            {
                var it = gear.items.FirstOrDefault(i => i.quality == q && i.InBag);
                if (it == null) continue;
                SelectSample(it.id);
                yield return WaitFrames(3);
                yield return RealClick("不可分解 · 可入库", false, "uGUI-B1-" + q);
                yield return WaitFrames(2);
                bool allowed = AdventureLoadout.SalvageAllowed(it);
                Snap("b1", "uGUI-B1-" + q, " SalvageAllowed=" + allowed +
                     " stillOwned=" + gear.items.Any(i => i.id == it.id), "allowed", allowed.ToString());
                if (allowed) Fail("uGUI: B1 gate broken for " + q);
            }

            // F5: deposit + withdraw a GOLD item (B1 invariant) via real clicks.
            var gold = gear.items.FirstOrDefault(i => i.quality == GearQuality.Gold && i.InBag);
            if (gold != null)
            {
                int wh0 = WarehouseCount();
                SelectSample(gold.id);
                yield return WaitFrames(2);
                inv.OpenPage(PlayerInventory.Page.Camp);
                yield return WaitFrames(4);
                Snap("storage", "deposit-before", "warehouse=" + wh0 + " gold=" + Short(gold.id));
                yield return RealClick("存入选中装备", true, "deposit");
                yield return WaitFrames(4);
                int wh1 = WarehouseCount();
                bool inWh = AdventureRecipes.Camp(hero).Items.Any(i => i.id == gold.id);
                Snap("storage", "deposit-after", "warehouse=" + wh1 + " inWarehouse=" + inWh +
                     " loadoutHas=" + gear.items.Any(i => i.id == gold.id), "inWarehouse", inWh.ToString());
                if (!inWh) Fail("deposit: gold did not reach warehouse");
                yield return RealClick(gold.Name, true, "withdraw-select");
                yield return WaitFrames(3);
                yield return RealClick("取回选中装备", true, "withdraw");
                yield return WaitFrames(4);
                bool back = gear.items.Any(i => i.id == gold.id);
                Snap("storage", "withdraw-after", "warehouse=" + WarehouseCount() +
                     " backInLoadout=" + back, "backInLoadout", back.ToString());
                if (!back) Fail("withdraw: gold did not return to loadout");
            }

            // F6: warehouse FULL -> explicit reason, no item movement.
            yield return RunWarehouseFull();

            // F7: save v9 (real product entry) and read it back in-run.
            bool saved = session.Saves.SaveProgress(false);
            string savePath = session.Saves.SavePath;
            string payload = (!string.IsNullOrEmpty(savePath) && File.Exists(savePath))
                             ? File.ReadAllText(savePath) : "";
            Snap("save", "v9", "SaveProgress=" + saved + " bytes=" + payload.Length +
                 " version=" + ExtractVersion(payload));
            try { File.WriteAllText(Path.Combine(root, "b2-persisted-save.json"), payload); } catch { }
            if (!saved) Fail("SaveProgress failed");
        }

        string ExtractVersion(string json)
        {
            if (string.IsNullOrEmpty(json)) return "";
            int i = json.IndexOf("\"version\"", StringComparison.Ordinal);
            return i < 0 ? "?" : json.Substring(i, Math.Min(28, json.Length - i));
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
            // Seven weapon types + accessory + arms for coefficient coverage.
            foreach (var t in new[] { GearType.Spear, GearType.Staff, GearType.Bow,
                                      GearType.TwinBlades, GearType.Greatsword, GearType.Scythe,
                                      GearType.Accessory, GearType.Arms })
            {
                var it = AdventureItems.New(t, GearQuality.Green, hero);
                bool added = gear.Add(it);
                Input("sample-prepared", "AdventureItems.New(" + t + ",Green) Add=" + added + " id=" + Short(it.id));
            }
            Snap("samples-ready", "prepare", "samples prepared via product factory; no action under test yet");
            yield return WaitFrames(2);
        }

        IEnumerator RunWarehouseFull()
        {
            // Fill the warehouse to Capacity using the product's OWN restore
            // entry (preparation), then perform ONE real deposit click whose
            // refusal is the action under test.
            var camp = AdventureRecipes.Camp(hero);
            if (camp == null) { Fail("warehouse: no CampRuntime"); yield break; }
            var filler = new List<GearItem>();
            var existing = camp.Items.Select(i => i.Clone()).ToList();
            for (int n = existing.Count; n < CampRuntime.Capacity; n++)
            {
                var it = AdventureItems.New(GearType.Sword, GearQuality.White, hero);
                it.worn = it.board = it.overflow = false; it.x = it.y = -1;
                filler.Add(it);
            }
            camp.Restore(existing.Concat(filler).ToArray(), camp.Materials.ToArray());
            Snap("storage", "warehouse-full-before", "count=" + WarehouseCount() +
                 " capacity=" + CampRuntime.Capacity + " line=" + B2InventoryQuery.CapacityLine(gear, camp));

            var candidate = gear.items.FirstOrDefault(i => i.InBag && !gear.Carried(i) && i.quality == GearQuality.Green);
            if (candidate == null) { Fail("warehouse: no candidate"); yield break; }
            SelectSample(candidate.id);
            inv.OpenPage(PlayerInventory.Page.Camp);
            yield return WaitFrames(4);
            int whBefore = WarehouseCount();
            yield return RealClick("存入选中装备", true, "warehouse-full-deposit");
            yield return WaitFrames(4);
            int whAfter = WarehouseCount();
            bool stillOwned = gear.items.Any(i => i.id == candidate.id);
            string notice = inv.CurrentNotice ?? "";
            bool reasonOK = notice.Contains("仓库已满") || notice.Contains("已满");
            Snap("storage", "warehouse-full-after", "count=" + whAfter + " (before=" + whBefore + ")" +
                 " stillOwned=" + stillOwned + " notice=" + Esc(notice) + " reasonOK=" + reasonOK,
                 "reasonOK", reasonOK.ToString(), "notice", notice,
                 "warehouseCount", whAfter.ToString());
            if (whAfter != whBefore || !stillOwned) Fail("warehouse full: item was moved");
            if (!reasonOK) Fail("warehouse full: explicit reason not shown");
            // Restore the warehouse to the pre-fill state (no product state left dirty).
            camp.Restore(existing.ToArray(), camp.Materials.ToArray());
            yield return WaitFrames(2);
        }

        // ---- IMGUI real-input filter acceptance ----------------------------
        IEnumerator RunImgui()
        {
            // Disable the uGUI presenter for THIS run only so PlayerInventory.OnGUI
            // renders the IMGUI path. This is observation setup, not a product edit.
            var p = CatInventoryPresenter.Instance;
            if (p != null) { p.enabled = false; Input("imgui-setup", "CatInventoryPresenter.enabled=false"); }
            if (inv != null) { inv.OpenPage(PlayerInventory.Page.Items); Input("open-items", "OpenPage(Items)"); }
            yield return WaitFrames(4);
            Snap("entry", "imgui", "IMGUI path active=" + (p == null || !p.enabled) +
                 " open=" + (inv != null && inv.IsOpen));

            // IMGUI panel geometry (CombatInventoryView + ContainerInventoryView).
            float panelX = CombatUI.Width / 2f - 560f + 28f;
            float panelY = CombatUI.Height / 2f - 335f + 128f;
            for (int t = 0; t < B2FilterTabs.Labels.Length; t++)
            {
                float bx = panelX + 386f + t * 54f;
                float by = panelY + 30f;
                yield return RealClickGui(bx, by, 50f, 28f, "IMGUI-tab-" + t + ":" + B2FilterTabs.Labels[t]);
                yield return WaitFrames(2);
                Snap("filter", "IMGUI-tab-" + t, "clicked=" + B2FilterTabs.Labels[t] +
                     " sharedTab=" + B2FilterState.Tab + " spec=" + B2FilterState.Describe());
            }
            // Quality/status/sort cycles in the compact strip.
            float stripY = panelY + 338f;
            for (int n = 0; n < 3; n++)
            {
                yield return RealClickGui(panelX + n * 72f, stripY, 68f, 26f, "IMGUI-cycle-" + n);
                yield return WaitFrames(2);
                Snap("filter", "IMGUI-cycle-" + n, "spec=" + B2FilterState.Describe() +
                     " key=" + B2FilterState.Current.Key);
            }
            // Both paths must resolve through the SAME shared rule.
            var spec = B2FilterState.Current;
            var projected = B2InventoryQuery.Apply(gear.items, spec, gear, false);
            bool sameRule = projected.All(i => B2InventoryQuery.Matches(i, spec, gear, false));
            Snap("verify", "IMGUI-shared-rule", "specKey=" + spec.Key + " projected=" + projected.Count +
                 " sameRule=" + sameRule + " tabLabels=" + B2FilterTabs.Labels.Length,
                 "sameRule", sameRule.ToString());
            if (!sameRule) Fail("IMGUI: shared rule mismatch");
            B2FilterState.Reset();
            yield return WaitFrames(2);
        }

        // ---- v9 readback ----------------------------------------------------
        IEnumerator RunReadback()
        {
            yield return WaitFrames(3);
            Snap("loaded", "readback", "loadout count=" + gear.items.Count);
            foreach (var it in gear.items)
            {
                bool allowed = AdventureLoadout.SalvageAllowed(it);
                Snap("item", "readback-" + it.quality, "id=" + Short(it.id) + " quality=" + (int)it.quality +
                     " name=" + Esc(it.Name) + " InBag=" + it.InBag + " SalvageAllowed=" + allowed +
                     " source=" + B2InventoryQuery.SourceLabel(it));
            }
            bool goldPresent = gear.items.Any(i => i.quality == GearQuality.Gold);
            bool redPresent = gear.items.Any(i => i.quality == GearQuality.Red);
            bool goldLocked = gear.items.Where(i => i.quality == GearQuality.Gold).All(i => !AdventureLoadout.SalvageAllowed(i));
            bool redLocked = gear.items.Where(i => i.quality == GearQuality.Red).All(i => !AdventureLoadout.SalvageAllowed(i));
            bool collectionEmpty = B2Collection.Count == 0;
            Snap("verify", "readback", "goldPresent=" + goldPresent + " redPresent=" + redPresent +
                 " goldLocked=" + goldLocked + " redLocked=" + redLocked +
                 " collectionEmpty=" + collectionEmpty + " token=" + B2Collection.SessionToken,
                 "goldLocked", goldLocked.ToString(), "redLocked", redLocked.ToString(),
                 "collectionEmpty", collectionEmpty.ToString());
            if (!goldPresent || !redPresent || !goldLocked || !redLocked) Fail("readback: gold/red not present+locked");
            if (!collectionEmpty) Fail("readback: collection not empty across process restart");
        }

        // Cross-process proof: a PREVIOUS process seeded favourites and wrote a
        // marker; this fresh process must have an empty set and a DIFFERENT token.
        static string SeedPath => Path.Combine(root, "..", "_favseed.json");

        IEnumerator RunFavSeed()
        {
            yield return PrepareSamples();
            var picks = gear.items.Where(i => i.InBag && !gear.Carried(i)).Take(3).ToArray();
            foreach (var p in picks) B2Collection.Add(p.id);
            Snap("collection", "favseed", "seeded=" + B2Collection.Count +
                 " token=" + B2Collection.SessionToken +
                 " ids=" + string.Join(",", picks.Select(p => Short(p.id))),
                 "seededCount", B2Collection.Count.ToString());
            var marker = new Dictionary<string, string>
            {
                {"token", B2Collection.SessionToken},
                {"count", B2Collection.Count.ToString(CultureInfo.InvariantCulture)},
                {"ids", string.Join(",", picks.Select(p => p.id))}
            };
            try { File.WriteAllText(SeedPath, JsonUtility.ToJson(new SeedMarker
                 { token = marker["token"], count = marker["count"], ids = marker["ids"] })); } catch { }
            if (B2Collection.Count == 0) Fail("favseed: no favourites seeded");
        }

        [Serializable]
        class SeedMarker { public string token, count, ids; }

        IEnumerator RunRestart()
        {
            yield return WaitFrames(2);
            string priorToken = "", priorCount = "", priorIds = "";
            bool hasSeed = false;
            try
            {
                if (File.Exists(SeedPath))
                {
                    var m = JsonUtility.FromJson<SeedMarker>(File.ReadAllText(SeedPath));
                    priorToken = m.token; priorCount = m.count; priorIds = m.ids; hasSeed = true;
                }
            }
            catch { }
            bool empty = B2Collection.Count == 0;
            bool tokenChanged = !hasSeed || priorToken != B2Collection.SessionToken;
            bool priorWasNonEmpty = !hasSeed || priorCount != "0";
            string[] ids = string.IsNullOrEmpty(priorIds) ? new string[0] : priorIds.Split(',');
            bool noneFavourite = ids.All(id => !B2Collection.IsFavorite(id));
            Snap("verify", "restart", "freshProcess collectionCount=" + B2Collection.Count +
                 " token=" + B2Collection.SessionToken + " empty=" + empty +
                 " priorSeedPresent=" + hasSeed + " priorToken=" + priorToken +
                 " priorCount=" + priorCount + " priorIds=" + priorIds.Length +
                 " tokenChanged=" + tokenChanged + " noneFavourite=" + noneFavourite,
                 "empty", empty.ToString(), "token", B2Collection.SessionToken,
                 "priorToken", priorToken, "priorCount", priorCount,
                 "tokenChanged", tokenChanged.ToString(), "noneFavourite", noneFavourite.ToString(),
                 "priorSeedPresent", hasSeed.ToString());
            if (!empty) Fail("restart: collection persisted across process restart");
            if (!tokenChanged) Fail("restart: session token did not change across process restart");
            if (!noneFavourite) Fail("restart: a prior favourite survived the restart");
            if (hasSeed && !priorWasNonEmpty) Fail("restart: prior seed was empty, proof is inconclusive");
        }

        IEnumerator Run()
        {
            mode = (File.Exists(Path.Combine(root, "b2-mode.txt"))
                        ? File.ReadAllText(Path.Combine(root, "b2-mode.txt")).Trim() : "golden");
            runId = "B2-" + Guid.NewGuid().ToString("N").Substring(0, 8);
            obsPath = Path.Combine(root, "b2-observations.jsonl");
            inputPath = Path.Combine(root, "b2-input-events.jsonl");
            File.WriteAllText(obsPath, "");
            File.WriteAllText(inputPath, "");
            Snap("boot", "driver", "mode=" + mode + " unity=" + Application.unityVersion +
                 " dll=Assembly-CSharp (B2)");

            float deadline = Time.realtimeSinceStartup + 60f;
            bool attempted = false;
            while (!GameEntry.GameSceneAuthorized && Time.realtimeSinceStartup < deadline)
            {
                var ge = GameEntry.Instance;
                if (ge != null && !attempted)
                {
                    attempted = true;
                    try { if (!ge.Continue()) { ge.AskNew(); ge.ConfirmNew(); } }
                    catch (Exception e) { Fail("GameEntry: " + e.GetType().Name); }
                }
                yield return null;
            }
            if (!GameEntry.GameSceneAuthorized) { Fail("GameEntry never authorized"); Exit(2); yield break; }
            float sceneDeadline = Time.realtimeSinceStartup + 90f;
            while (GameEntry.Loading && Time.realtimeSinceStartup < sceneDeadline) yield return null;
            session = FindAnyObjectByType<CombatSession>();
            if (session == null) { Fail("no CombatSession"); Exit(2); yield break; }
            try { GameEntry.DirectReady(); } catch { }
            hero = session.hero;
            if (hero == null) { Fail("no hero"); Exit(2); yield break; }
            gear = hero.GetComponent<AdventureLoadout>();
            inv = hero.Inventory;
            if (gear == null || inv == null) { Fail("no AdventureLoadout/PlayerInventory"); Exit(2); yield break; }
            Snap("entry", "driver", "real Player entry complete; CatUI running=" + CatInventoryPresenter.Running +
                 " InCamp=" + (AdventureRecipes.Camp(hero) != null && AdventureRecipes.Camp(hero).InCamp));

            switch (mode)
            {
                case "golden": yield return RunGolden(); break;
                case "ugui": yield return RunUgui(); break;
                case "imgui": yield return RunImgui(); break;
                case "readback": yield return RunReadback(); break;
                case "favseed": yield return RunFavSeed(); break;
                case "restart": yield return RunRestart(); break;
                default: Fail("unknown mode " + mode); break;
            }

            Snap("done", "driver", "mode=" + mode + " complete; failed=" + failed);
            try { File.WriteAllText(Path.Combine(root, "b2-complete.txt"), failed ? "FAIL" : "PASS"); } catch { }
            Exit(failed ? 3 : 0);
        }

        void Start() { StartCoroutine(Run()); }
        static void Exit(int code)
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(code);
#else
            Application.Quit(code);
#endif
        }
    }
}
