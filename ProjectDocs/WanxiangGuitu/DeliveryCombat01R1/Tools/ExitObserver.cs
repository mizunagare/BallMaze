using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

// Independent retained Win32 process handles. No activation, input injection, kills or global settings.
internal static class ExitObserver {
 delegate bool EnumProc(IntPtr window,IntPtr data);
 [DllImport("kernel32.dll",SetLastError=true)]static extern IntPtr OpenProcess(uint access,bool inherit,uint pid);
 [DllImport("kernel32.dll",SetLastError=true)]static extern uint WaitForSingleObject(IntPtr handle,uint timeout);
 [DllImport("kernel32.dll",SetLastError=true)]static extern bool GetExitCodeProcess(IntPtr handle,out uint code);
 [DllImport("kernel32.dll")]static extern bool CloseHandle(IntPtr handle);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]static extern bool QueryFullProcessImageName(IntPtr handle,uint flags,StringBuilder path,ref uint length);
 [DllImport("user32.dll",CharSet=CharSet.Unicode,SetLastError=true)]static extern IntPtr OpenDesktop(string name,uint flags,bool inherit,uint access);
 [DllImport("user32.dll")]static extern IntPtr OpenInputDesktop(uint flags,bool inherit,uint access);
 [DllImport("user32.dll")]static extern bool CloseDesktop(IntPtr handle);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]static extern bool GetUserObjectInformation(IntPtr handle,int index,StringBuilder text,int count,out int needed);
 [DllImport("user32.dll")]static extern bool EnumDesktopWindows(IntPtr desktop,EnumProc callback,IntPtr data);
 [DllImport("user32.dll")]static extern uint GetWindowThreadProcessId(IntPtr window,out uint pid);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]static extern int GetClassName(IntPtr window,StringBuilder text,int count);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]static extern int GetWindowText(IntPtr window,StringBuilder text,int count);
 [DllImport("user32.dll")]static extern bool IsWindow(IntPtr window);
 [DllImport("user32.dll",SetLastError=true)]static extern bool PostMessage(IntPtr window,uint message,IntPtr w,IntPtr l);
 [DllImport("user32.dll",SetLastError=true)]static extern IntPtr SendMessageTimeout(IntPtr window,uint message,IntPtr w,IntPtr l,uint flags,uint timeout,out IntPtr result);
 sealed class Config {public uint pid{get;set;}public uint hostPid{get;set;}public string exe{get;set;}="";public string desktop{get;set;}="";public string output{get;set;}="";public string minimumCreationUtc{get;set;}="";public int timeoutSeconds{get;set;}=90;}
 static string folder="";static Stopwatch clock=new();
 static void Emit(string kind,object value)=>File.AppendAllText(Path.Combine(folder,"timeline.jsonl"),JsonSerializer.Serialize(new{utc=DateTime.UtcNow,elapsedMs=clock.Elapsed.TotalMilliseconds,kind,value})+"\n");
 static bool Inactive(string name){var h=OpenInputDesktop(0,false,1);if(h==IntPtr.Zero)return false;try{var text=new StringBuilder(512);return GetUserObjectInformation(h,2,text,1024,out _)&&text.Length>0&&!text.ToString().Equals(name,StringComparison.OrdinalIgnoreCase);}finally{CloseDesktop(h);}}
 static int Main(string[] args){IntPtr child=IntPtr.Zero,host=IntPtr.Zero,desktop=IntPtr.Zero;try{
  var c=JsonSerializer.Deserialize<Config>(File.ReadAllText(args.Single()))!;folder=Path.GetFullPath(c.output);if(!Directory.Exists(folder)||!System.Text.RegularExpressions.Regex.IsMatch(c.desktop,"^WGTest_[a-f0-9]{32}$")||!Inactive(c.desktop)||c.timeoutSeconds<1||c.timeoutSeconds>180)throw new Exception("Explicit inactive owned test case required");
  clock.Start();child=OpenProcess(0x101000,false,c.pid);host=OpenProcess(0x101000,false,c.hostPid);if(child==IntPtr.Zero||host==IntPtr.Zero)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
  var image=new StringBuilder(2048);uint size=2048;if(!QueryFullProcessImageName(child,0,image,ref size)||!Path.GetFullPath(c.exe).Equals(image.ToString(),StringComparison.OrdinalIgnoreCase))throw new Exception("PID/executable identity mismatch");
  var p=Process.GetProcessById((int)c.pid);var created=p.StartTime.ToUniversalTime();if(created<DateTime.Parse(c.minimumCreationUtc).ToUniversalTime().AddSeconds(-1))throw new Exception("Stale/reused PID refused");
  Emit("identity",new{c.pid,c.hostPid,exe=image.ToString(),sha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(c.exe))),created,session=p.SessionId,observerPid=Environment.ProcessId,c.desktop,inputDesktopActive=false,protocol="predeclared owned background WM_CLOSE; retained Win32 child+host handles; 20ms polling; NOT physical titlebar",c.timeoutSeconds});
  desktop=OpenDesktop(c.desktop,0,false,0x10000000);if(desktop==IntPtr.Zero)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());IntPtr window=IntPtr.Zero;
  EnumDesktopWindows(desktop,(w,_)=>{GetWindowThreadProcessId(w,out uint owner);if(owner!=c.pid)return true;var cls=new StringBuilder(256);var title=new StringBuilder(512);GetClassName(w,cls,256);GetWindowText(w,title,512);Emit("window",new{handle=w.ToInt64(),pid=owner,windowClass=cls.ToString(),title=title.ToString()});if(cls.ToString()=="UnityWndClass")window=w;return true;},IntPtr.Zero);
  if(window==IntPtr.Zero)throw new Exception("Exact owned UnityWndClass absent; no fallback close");
  bool responsive=SendMessageTimeout(window,0,IntPtr.Zero,IntPtr.Zero,2,500,out _)!=IntPtr.Zero;Emit("pre-request-response",new{responsive,lastError=responsive?0:Marshal.GetLastWin32Error(),handle=window.ToInt64()});
  bool queued=PostMessage(window,0x10,IntPtr.Zero,IntPtr.Zero);Emit("close-request",new{queued,lastError=queued?0:Marshal.GetLastWin32Error(),method="PostMessage WM_CLOSE; queued is not delivery or exit proof"});
  bool childDone=false,hostDone=false,childKnown=false,hostKnown=false,windowGone=false,pidGone=false;uint childCode=259,hostCode=259;double? childMs=null,hostMs=null;long poll=0;
  while(clock.Elapsed.TotalSeconds<c.timeoutSeconds){
   if(!childDone&&WaitForSingleObject(child,0)==0){childDone=true;childMs=clock.Elapsed.TotalMilliseconds;childKnown=GetExitCodeProcess(child,out childCode);Emit("child-signaled",new{known=childKnown,code=childKnown?(uint?)childCode:null,lastError=Marshal.GetLastWin32Error()});}
   if(!hostDone&&WaitForSingleObject(host,0)==0){hostDone=true;hostMs=clock.Elapsed.TotalMilliseconds;hostKnown=GetExitCodeProcess(host,out hostCode);Emit("host-signaled",new{known=hostKnown,code=hostKnown?(uint?)hostCode:null});}
   if(!windowGone&&!IsWindow(window)){windowGone=true;Emit("window-destroyed",new{handle=window.ToInt64()});}
   if(poll++%12==0&&!pidGone){try{using var check=Process.GetProcessById((int)c.pid);if(check.StartTime.ToUniversalTime()!=created){pidGone=true;Emit("original-pid-identity-no-longer-listed",new{proofOfExit=false});}}catch(ArgumentException){pidGone=true;Emit("pid-not-listed",new{proofOfExit=false});}}
   if(childDone&&hostDone)break;Thread.Sleep(20);
  }
  // One final independent inventory sample after the handle observation, so the
  // parent can distinguish "not sampled" from an observed missing PID.
  if(!pidGone){try{using var check=Process.GetProcessById((int)c.pid);Emit("final-pid-inventory",new{listed=true,originalIdentity=check.StartTime.ToUniversalTime()==created,proofOfExit=false});}catch(ArgumentException){pidGone=true;Emit("pid-not-listed-final",new{proofOfExit=false});}catch(InvalidOperationException e){Emit("pid-inventory-unavailable",new{error=e.Message,proofOfExit=false});}}
  // PID disappearance is diagnostic metadata only. Actual exit is held-handle signaling plus code.
  var result=new{status=queued&&childDone&&childKnown&&childCode==0&&hostDone&&hostKnown&&hostCode==0?"PASS":"UNRESOLVED",queued,responsive,childDone,childKnown,childCode=childKnown?(uint?)childCode:null,hostDone,hostKnown,hostCode=hostKnown?(uint?)hostCode:null,windowGone,pidGone,childObservedMs=childMs,hostObservedMs=hostMs,timedOut=!(childDone&&hostDone),forcedTermination=false,scope="OS process/host exit observation only; game business/audit/logs need independent validation"};
  File.WriteAllText(Path.Combine(folder,"exit-observer.json"),JsonSerializer.Serialize(result,new JsonSerializerOptions{WriteIndented=true}));return result.status=="PASS"?0:3;
 }catch(Exception e){if(folder!="")File.WriteAllText(Path.Combine(folder,"exit-observer-error.txt"),e.ToString());return 2;}finally{if(child!=IntPtr.Zero)CloseHandle(child);if(host!=IntPtr.Zero)CloseHandle(host);if(desktop!=IntPtr.Zero)CloseDesktop(desktop);}}
}
