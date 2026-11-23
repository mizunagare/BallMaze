using System;
using System.Collections;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.UI;

namespace CavernValidation
{
    public sealed class Driver : MonoBehaviour
    {
        [Serializable] public struct NativeRect { public int left, top, right, bottom; }
        [Serializable] public struct NativePoint { public int x, y; }
        [Serializable] sealed class WindowFacts
        {
            public int playerPid, hwndPid, foregroundPid;
            public long hwnd, foregroundHwnd;
            public NativeRect windowRect, clientRect;
            public NativePoint clientOriginScreen, cursorScreen, cursorClient;
            public uint dpi;
            public float dpiScale;
            public bool converted, foregroundVerified;
        }
        [Serializable] sealed class State
        {
            public string utc, ui, phase, notice, saveSha256, profileJson, inputContext;
            public WindowFacts window;
            public bool open, inventoryOpen, unknown, focused, available, inputBlocked;
            public int page, pages, regionFilter, typeFilter, repaintCount, nativeMouseDown, nativeMouseUp;
            public int screenWidth, screenHeight;
            public float uiScale;
            public Vector3 heroPosition;
            public ObjectiveHistoryEntry[] query, visible;
            public string[] text;
        }
        [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
        [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")] static extern bool GetWindowRect(IntPtr h, out NativeRect rect);
        [DllImport("user32.dll")] static extern bool GetClientRect(IntPtr h, out NativeRect rect);
        [DllImport("user32.dll")] static extern uint GetDpiForWindow(IntPtr h);
        [DllImport("user32.dll")] static extern bool ClientToScreen(IntPtr h, ref NativePoint point);
        [DllImport("user32.dll")] static extern bool ScreenToClient(IntPtr h, ref NativePoint point);
        [DllImport("user32.dll")] static extern bool GetCursorPos(out NativePoint point);
        static readonly BindingFlags Private = BindingFlags.Instance | BindingFlags.NonPublic;
        string root, output, ui="imgui", phase="starting", command="", lastState="";
        CombatSession session;
        int paints, downs, ups;
        float next;
        int capture;

        public static void Boot()
        {
            var args=Environment.GetCommandLineArgs();
            int at=Array.IndexOf(args,"-ux05-r2");
            if(at<0 || at+1>=args.Length)return;
            var root=ValidationStorage.Root(args,true);
            var driver=new GameObject("UX05 R2 read-only history observer").AddComponent<Driver>();
            DontDestroyOnLoad(driver.gameObject);
            driver.root=root;
            driver.output=Path.Combine(root,"observer");
            Directory.CreateDirectory(driver.output);
            Application.runInBackground=true;
        }

        IEnumerator Start()
        {
            while((session=FindAnyObjectByType<CombatSession>())==null || !session.Saves.IsInitialized)
                yield return null;
            // Isolated acceptance setup. History interactions are supplied by native Windows input.
            session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
            yield return null;
            if(PlayerHudPresenter.Instance!=null)PlayerHudPresenter.Instance.enabled=false;
            var hook=typeof(AdventureFlow).GetField("ObserveHistoryRepaint",BindingFlags.Static|BindingFlags.NonPublic);
            if(hook!=null)hook.SetValue(null,new Action<string,ObjectiveHistoryEntry[],int,int>((n,rows,p,total)=>{paints++;}));
            phase="ready";
        }

        T Field<T>(string name)=>(T)typeof(AdventureFlow).GetField(name,Private).GetValue(session.Flow);
        static string Sha(string path)
        {
            if(!File.Exists(path))return "missing";
            using(var sha=System.Security.Cryptography.SHA256.Create())
            using(var f=File.OpenRead(path))return BitConverter.ToString(sha.ComputeHash(f)).Replace("-","");
        }
        WindowFacts Facts()
        {
            using(var process=Process.GetCurrentProcess())
            {
                process.Refresh();var h=process.MainWindowHandle;var foreground=GetForegroundWindow();
                uint p,f;GetWindowThreadProcessId(h,out p);GetWindowThreadProcessId(foreground,out f);
                NativeRect wr,cr;GetWindowRect(h,out wr);GetClientRect(h,out cr);
                var origin=new NativePoint();bool converted=ClientToScreen(h,ref origin);
                NativePoint cursor;GetCursorPos(out cursor);var client=cursor;ScreenToClient(h,ref client);
                uint dpi=GetDpiForWindow(h);
                return new WindowFacts{playerPid=process.Id,hwnd=h.ToInt64(),hwndPid=(int)p,
                    foregroundHwnd=foreground.ToInt64(),foregroundPid=(int)f,windowRect=wr,clientRect=cr,
                    clientOriginScreen=origin,cursorScreen=cursor,cursorClient=client,dpi=dpi,dpiScale=dpi/96f,
                    converted=converted,foregroundVerified=p==process.Id && f==process.Id};
            }
        }
        void Update()
        {
            string control=Path.Combine(root,"control.txt");
            if(File.Exists(control))
            {
                string value=File.ReadAllText(control).Trim();
                if(value!=command)
                {
                    command=value;
                    var parts=value.Split(' ');
                    if(parts[0]=="quit"){Application.Quit(0);return;}
                    if(session!=null && parts[0]=="ui")
                    {
                        ui=parts[1];
                        if(PlayerHudPresenter.Instance!=null)PlayerHudPresenter.Instance.enabled=ui=="ugui";
                    }
                    if(session!=null && parts[0]=="snapshot-name")
                    {
                        int index=Array.FindIndex(ObjectiveCatalog.All,c=>c.id=="forest.treasure");
                        var old=ObjectiveCatalog.All[index];
                        ObjectiveCatalog.All[index]=new ObjectiveCard(old.id,old.region,old.goal,"R2 当前新名称",
                            old.oneLine,old.nextHint,old.conditions);
                    }
                }
            }
            if(Time.realtimeSinceStartup<next)return;next=Time.realtimeSinceStartup+.15f;
            var facts=Facts();
            File.WriteAllText(Path.Combine(output,"window.json"),JsonUtility.ToJson(facts,true));
            if(session==null || !session.Saves.IsInitialized)return;
            var flow=session.Flow;
            var rows=(ObjectiveHistoryEntry[])typeof(AdventureFlow).GetMethod("QueryHistory",Private).Invoke(flow,null);
            int page=Field<int>("historyPage");
            bool open=Field<bool>("historyOpen");
            var canvas=FindObjectsByType<Canvas>(FindObjectsSortMode.None).FirstOrDefault(c=>c.name=="冒险历程入口");
            var visible=open?rows.Skip(page*20).Take(20).ToArray():Array.Empty<ObjectiveHistoryEntry>();
            var state=new State{utc=DateTime.UtcNow.ToString("o"),ui=ui,phase=phase,window=facts,
                open=open,inventoryOpen=session.hero.Inventory.IsOpen,unknown=flow.Profile.objectiveHistoryLegacyUnknown,
                focused=Application.isFocused,available=(bool)typeof(AdventureFlow).GetProperty("HistoryAvailable",Private).GetValue(flow,null),
                inputBlocked=PlayerInput.UIBlocked,inputContext=typeof(PlayerInput).GetMethod("Context",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,null).ToString(),
                page=page+1,pages=Math.Max(1,(rows.Length+19)/20),regionFilter=Field<int>("historyRegion"),
                typeFilter=Field<int>("historyType"),query=rows,visible=visible,repaintCount=paints,
                nativeMouseDown=downs,nativeMouseUp=ups,screenWidth=Screen.width,screenHeight=Screen.height,uiScale=CombatUI.Scale,
                saveSha256=Sha(session.Saves.SavePath),profileJson=JsonUtility.ToJson(flow.Profile),heroPosition=session.hero.transform.position,
                notice=(string)typeof(AdventureFlow).GetMethod("HistoryNotice",Private).Invoke(flow,new object[]{rows.Length}),
                text=canvas!=null?canvas.GetComponentsInChildren<Text>().Select(t=>t.text).ToArray():Array.Empty<string>()};
            string json=JsonUtility.ToJson(state);
            File.WriteAllText(Path.Combine(output,"state.json"),json);
            string signature=ui+"|"+open+"|"+page+"|"+state.regionFilter+"|"+state.typeFilter+"|"+downs+"|"+ups+"|"+facts.foregroundHwnd;
            if(signature!=lastState){lastState=signature;File.AppendAllText(Path.Combine(output,"states.jsonl"),json+"\n");ScreenCapture.CaptureScreenshot(Path.Combine(output,"screen-"+(++capture).ToString("D4")+".png"));}
        }
        void OnGUI()
        {
            if(Event.current.type==EventType.MouseDown || Event.current.type==EventType.MouseUp)
            {
                if(Event.current.type==EventType.MouseDown)downs++;else ups++;
                File.AppendAllText(Path.Combine(output,"input.jsonl"),JsonUtility.ToJson(new InputFact{
                    utc=DateTime.UtcNow.ToString("o"),kind=Event.current.type.ToString(),mouse=Event.current.mousePosition,
                    used=Event.current.type==EventType.Used,window=Facts()})+"\n");
            }
        }
        [Serializable] sealed class InputFact { public string utc,kind;public Vector2 mouse;public bool used;public WindowFacts window; }
    }
}
