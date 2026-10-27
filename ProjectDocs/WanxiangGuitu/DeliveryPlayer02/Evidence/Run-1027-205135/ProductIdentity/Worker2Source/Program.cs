using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Text;
// External test worker. Never loaded into Unity/Player. No focus stealing or virtual InputSystem devices.
internal static class Program {
 delegate bool EnumProc(IntPtr w,IntPtr p);
 [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb,IntPtr p);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr w,out uint pid);
 [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] static extern bool IsWindow(IntPtr w);
 [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr w);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr w,StringBuilder text,int count);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetWindowText(IntPtr w,StringBuilder text,int count);
 [DllImport("user32.dll")] static extern bool GetClientRect(IntPtr w,out Rect r);
 [DllImport("user32.dll")] static extern bool ClientToScreen(IntPtr w,ref Point p);
 [DllImport("user32.dll")] static extern int GetSystemMetrics(int n);
 [DllImport("user32.dll",SetLastError=true)] static extern IntPtr SendMessageTimeout(IntPtr w,uint msg,IntPtr a,IntPtr b,uint flags,uint timeout,out IntPtr result);
 [DllImport("user32.dll",SetLastError=true)] static extern bool PostMessage(IntPtr w,uint msg,IntPtr a,IntPtr b);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetExitCodeProcess(IntPtr process,out uint code);
 [DllImport("user32.dll",SetLastError=true)] static extern uint SendInput(uint count,Input[] input,int size);
 [StructLayout(LayoutKind.Sequential)] struct Rect {public int left,top,right,bottom;}
 [StructLayout(LayoutKind.Sequential)] struct Point {public int x,y;}
 [StructLayout(LayoutKind.Sequential)] struct Mouse {public int dx,dy;public uint data,flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Sequential)] struct Key {public ushort vk,scan;public uint flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Explicit,Size=32)] struct Union {[FieldOffset(0)]public Mouse mouse;[FieldOffset(0)]public Key key;}
 [StructLayout(LayoutKind.Sequential)] struct Input {public uint type;public Union data;}
 static readonly List<object> events=new();static int pid;static IntPtr window;
 static bool Own(IntPtr w){GetWindowThreadProcessId(w,out uint p);return p==pid;}
 static string desktop="";
 static bool Ready()=>(desktop==""||DesktopHost.IsInput(desktop))&&IsWindow(window)&&Own(window)&&GetForegroundWindow()==window&&IsWindowVisible(window);
 static void Write(string path,string status,string reason){File.WriteAllText(path,JsonSerializer.Serialize(new{status,reason,pid,utc=DateTime.UtcNow,events},new JsonSerializerOptions{WriteIndented=true}));}
 static void Click(int x,int y,string name){if(!Ready())throw new InvalidOperationException("Foreground changed; no more input");var p=new Point{x=x,y=y};ClientToScreen(window,ref p);int vx=GetSystemMetrics(76),vy=GetSystemMetrics(77),vw=GetSystemMetrics(78),vh=GetSystemMetrics(79);var m=new Mouse{dx=(p.x-vx)*65535/Math.Max(1,vw-1),dy=(p.y-vy)*65535/Math.Max(1,vh-1),flags=0xC001};var move=new Input{type=0,data=new Union{mouse=m}};SendInput(1,new[]{move},Marshal.SizeOf<Input>());if(!Ready())throw new InvalidOperationException("Focus changed after move");m.flags=2;var down=new Input{type=0,data=new Union{mouse=m}};m.flags=4;var up=new Input{type=0,data=new Union{mouse=m}};uint n=SendInput(2,new[]{down,up},Marshal.SizeOf<Input>());events.Add(new{action=name,method="Win32 SendInput mouse",sent=n,utc=DateTime.UtcNow});Thread.Sleep(300);}
 static int Main(string[] args){if(args.Length>0&&args[0]=="host")return DesktopHost.Run(args[1]);if(args.Length>0&&args[0]=="fixture-window")return WindowFixture.Run(args[1]);string output=args.Length>2?args[2]:"worker.json";try{
  if(args.Length>4){desktop=args[4];DesktopHost.Attach(desktop);}
  pid=int.Parse(args[1]);var process=Process.GetProcessById(pid);string exe=process.MainModule!.FileName!;
  // Caller supplies exact exe identity; reject targeting another user's program even if a PID was recycled.
  if(args.Length<4||!Path.GetFullPath(exe).Equals(Path.GetFullPath(args[3]),StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Executable identity mismatch");
  var windows=new List<IntPtr>();EnumWindows((w,p)=>{if(Own(w))windows.Add(w);return true;},IntPtr.Zero);
  foreach(var w in windows){var name=new StringBuilder(256);var title=new StringBuilder(512);GetClassName(w,name,256);GetWindowText(w,title,512);GetClientRect(w,out var size);events.Add(new{action="owned window inventory",handle=w.ToInt64(),windowClass=name.ToString(),title=title.ToString(),visible=IsWindowVisible(w),width=size.right,height=size.bottom});}
  // Separate opt-in cleanup of a failed, owned Editor test. Never broaden the
  // Player/native-UI window selector or activate a desktop to achieve this.
  if(args[0]=="editor-close"){
   if(args.Length<7||!Path.GetFileName(exe).Equals("Unity.exe",StringComparison.OrdinalIgnoreCase)
      ||!System.Text.RegularExpressions.Regex.IsMatch(desktop,"^WGTest_[a-f0-9]{32}$")||DesktopHost.IsInput(desktop))
    throw new InvalidOperationException("Editor close requires an inactive owned test desktop");
   string project=Path.GetFullPath(args[5]);string owner=Path.Combine(Path.GetDirectoryName(project)!,"owner.json");
   if(Path.GetFileName(project)!="Project"||!Directory.Exists(project)||!File.Exists(owner))throw new InvalidOperationException("Owned isolated Project required");
   using var ownership=JsonDocument.Parse(File.ReadAllText(owner));string kind=ownership.RootElement.GetProperty("kind").GetString()!;
   if(kind!="WanxiangGuitu isolated unattended run"&&kind!="B4 directed checks using existing orchestration")throw new InvalidOperationException("Unknown test owner");
   string receipt=Path.GetFullPath(args[6]);if(!receipt.StartsWith(Path.GetDirectoryName(project)!+Path.DirectorySeparatorChar,StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Interruption receipt outside owned root");
   using var interruption=JsonDocument.Parse(File.ReadAllText(receipt));
   if(interruption.RootElement.GetProperty("pid").GetInt32()!=pid||interruption.RootElement.GetProperty("desktop").GetString()!=desktop)throw new InvalidOperationException("Interruption PID/desktop mismatch");
   window=windows.FirstOrDefault(w=>{var c=new StringBuilder(256);var t=new StringBuilder(512);GetClassName(w,c,256);GetWindowText(w,t,512);return c.ToString()=="UnityContainerWndClass"&&t.ToString().StartsWith("Project - ",StringComparison.Ordinal)&&t.ToString().Contains("Unity");});
   if(window==IntPtr.Zero){Write(output,"NOT_RUN","No exact owned Editor main window; no fallback or input");return 3;}
   events.Add(new{action="failed owned Editor normal close",method="WM_CLOSE; not kill/native acceptance",handle=window.ToInt64(),project});
   // Keep the native handle BEFORE closing. Process.ExitCode is not supported
   // for every GetProcessById object, even when WaitForExit observed termination.
   var handle=process.SafeHandle;bool queued=PostMessage(window,0x10,IntPtr.Zero,IntPtr.Zero);bool ended=queued&&process.WaitForExit(15000);
   uint code=0;bool known=ended&&GetExitCodeProcess(handle.DangerousGetHandle(),out code);
   events.Add(new{action="owned Editor exit observation",actualExitCode=known?(uint?)code:null,timedOut=!ended,forcedTermination=false});
   Write(output,known?"PASS":queued?"NOT_RUN":"FAIL","Cleanup only; failed test is not reclassified as normal Player/native success");return known?0:queued?3:1;
  }
  // MainWindowHandle may be the process's visible 50x50 Windows input indicator.
  // Select the actual game/fixture class, never an IME/overlay owned by the same PID.
  window=windows.FirstOrDefault(w=>{var c=new StringBuilder(256);GetClassName(w,c,256);return c.ToString() is "UnityWndClass" or "WGTestWorkerFixture";});
  if(window==IntPtr.Zero){Write(output,"NOT_RUN","No owned top-level window");return 3;}
  events.Add(new{action="selected owned game window",handle=window.ToInt64()});
  if(args[0]=="close"){
   events.Add(new{action="normal close request",method="WM_CLOSE to owned window; not physical mouse",utc=DateTime.UtcNow});
   var ok=PostMessage(window,0x10,IntPtr.Zero,IntPtr.Zero);
   Write(output,ok?"PASS":"FAIL",ok?"OS window close queued; parent must check actual exit/audit/log/save":"Window close could not be queued");return ok?0:1;
  }
  if(args[0]=="post-pointer"){
   // PLAYER-02 synthetic window-message input, never global/physical SendInput.
   // Restrict to the exact owned Player on an INACTIVE private test desktop.
   if(args.Length<7||!System.Text.RegularExpressions.Regex.IsMatch(desktop,"^WGTest_[a-f0-9]{32}$")||DesktopHost.IsInput(desktop)||!Path.GetFileName(exe).Equals("WanxiangGuitu.exe",StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Queued pointer requires inactive owned Player desktop");
   GetClientRect(window,out var bounds);int x=int.Parse(args[5]),y=int.Parse(args[6]);
   if(bounds.right!=1280||bounds.bottom!=720||x<0||y<0||x>=bounds.right||y>=bounds.bottom)throw new InvalidOperationException("Exact client size and bounded coordinates required");
   IntPtr point=(IntPtr)((y<<16)|(x&0xffff));bool moved=PostMessage(window,0x200,IntPtr.Zero,point);bool down=PostMessage(window,0x201,(IntPtr)1,point);Thread.Sleep(80);bool up=PostMessage(window,0x202,IntPtr.Zero,point);
   events.Add(new{action="synthetic pointer queued",method="WM_MOUSEMOVE/WM_LBUTTONDOWN/WM_LBUTTONUP; NOT SendInput/native/human",x,y,moved,down,up,inputDesktopActive=DesktopHost.IsInput(desktop),utc=DateTime.UtcNow});
   Write(output,moved&&down&&up?"PASS":"FAIL","Delivery receipt only; runtime must independently assert actual UI/business state; no activation or global cursor move");return moved&&down&&up?0:1;
  }
  if(!Ready()){Write(output,"NOT_RUN","Player not foreground/visible; no activation, global hotkey or input sent");return 3;}
  GetClientRect(window,out var r);if(r.right!=1280||r.bottom!=720){Write(output,"NOT_RUN","Unsupported client size; no guessed coordinates");return 3;}
  Click(1190,74,"help open");Click(360,502,"help close");Click(1060,74,"route open");Click(360,502,"route close");Click(865,652,"bag open");
  // Delivery is not a semantic oracle. Without readable accessibility/visual assertions never mark U16 PASS.
  Write(output,"NOT_RUN","Native input attempted, but Unity custom Canvas has no verified UI accessibility oracle; screenshots/domain tests cannot substitute for native semantic E2E");return 3;
 }catch(Exception e){Write(output,"NOT_RUN",e.ToString());return 3;}}
}
