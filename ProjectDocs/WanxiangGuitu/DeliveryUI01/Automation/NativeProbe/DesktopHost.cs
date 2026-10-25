using System.Collections;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
// A per-run window desktop, never switched onto the user's input desktop. No global settings.
internal static class DesktopHost {
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct Startup {public int cb;public string? reserved,desktop,title;public uint x,y,xSize,ySize,xChars,yChars,fill,flags;public ushort show,reserved2;public IntPtr reservedPtr,input,output,error;}
 [StructLayout(LayoutKind.Sequential)] struct Proc {public IntPtr process,thread;public uint pid,tid;}
 [DllImport("user32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr CreateDesktop(string name,IntPtr device,IntPtr mode,uint flags,uint access,IntPtr security);
 [DllImport("user32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr OpenDesktop(string name,uint flags,bool inherit,uint access);
 [DllImport("user32.dll")] static extern bool CloseDesktop(IntPtr h);
 [DllImport("user32.dll")] static extern bool SetThreadDesktop(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr OpenInputDesktop(uint flags,bool inherit,uint access);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern bool GetUserObjectInformation(IntPtr h,int index,StringBuilder text,int length,out int needed);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateProcess(string app,StringBuilder command,IntPtr processSecurity,IntPtr threadSecurity,bool inherit,uint flags,IntPtr env,string cwd,ref Startup startup,out Proc info);
 [DllImport("kernel32.dll")] static extern uint WaitForSingleObject(IntPtr h,uint timeout);
 [DllImport("kernel32.dll")] static extern bool GetExitCodeProcess(IntPtr h,out uint code);
 [DllImport("kernel32.dll")] static extern IntPtr GetStdHandle(int n);
 [DllImport("kernel32.dll")] static extern bool SetHandleInformation(IntPtr h,uint mask,uint flags);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr h);
 internal sealed class Spec {public string Exe{get;set;}="";public string[] Arguments{get;set;}=Array.Empty<string>();public string Desktop{get;set;}="";public string Receipt{get;set;}="";public string EnvRoot{get;set;}="";public bool ShowInInactiveDesktop{get;set;}}
 static string Quote(string s){if(!s.Any(c=>char.IsWhiteSpace(c)||c=='"')&&s.Length>0)return s;var b=new StringBuilder("\"");int slashes=0;foreach(char c in s){if(c=='\\'){slashes++;continue;}if(c=='"')b.Append('\\',slashes*2+1);else b.Append('\\',slashes);b.Append(c);slashes=0;}b.Append('\\',slashes*2).Append('"');return b.ToString();}
 internal static bool IsInput(string desktop){var h=OpenInputDesktop(0,false,1);if(h==IntPtr.Zero)return false;try{var b=new StringBuilder(256);return GetUserObjectInformation(h,2,b,512,out _)&&b.ToString().Equals(desktop,StringComparison.OrdinalIgnoreCase);}finally{CloseDesktop(h);}}
 internal static IntPtr Attach(string desktop){var h=OpenDesktop(desktop,0,false,0x10000000);if(h==IntPtr.Zero||!SetThreadDesktop(h))throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());return h;}
 internal static int Run(string file){var s=JsonSerializer.Deserialize<Spec>(File.ReadAllText(file))!;if(!s.Desktop.StartsWith("WGTest_",StringComparison.Ordinal)||s.Desktop.Any(c=>!char.IsAsciiLetterOrDigit(c)&&c!='_'))throw new Exception("Test desktop name rejected");
  var d=CreateDesktop(s.Desktop,IntPtr.Zero,IntPtr.Zero,0,0x10000000,IntPtr.Zero);if(d==IntPtr.Zero)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
  IntPtr block=IntPtr.Zero;Proc p=default;try{
   var vars=Environment.GetEnvironmentVariables().Cast<DictionaryEntry>().ToDictionary(e=>(string)e.Key,e=>(string)e.Value!,StringComparer.OrdinalIgnoreCase);if(s.EnvRoot!="")vars["UNITY_TEST_ROOT"]=s.EnvRoot;
   block=Marshal.StringToHGlobalUni(string.Join('\0',vars.OrderBy(e=>e.Key,StringComparer.OrdinalIgnoreCase).Select(e=>e.Key+"="+e.Value))+"\0\0");
   if(s.ShowInInactiveDesktop&&IsInput(s.Desktop))throw new Exception("Refuse showing test window on active input desktop");
   var si=new Startup{cb=Marshal.SizeOf<Startup>(),desktop="WinSta0\\"+s.Desktop,flags=0x101,show=(ushort)(s.ShowInInactiveDesktop?4:0),input=GetStdHandle(-10),output=GetStdHandle(-11),error=GetStdHandle(-12)};
   SetHandleInformation(si.output,1,1);SetHandleInformation(si.error,1,1);SetHandleInformation(si.input,1,1);
   var command=new StringBuilder(string.Join(' ',new[]{s.Exe}.Concat(s.Arguments).Select(Quote)));
   if(!CreateProcess(s.Exe,command,IntPtr.Zero,IntPtr.Zero,true,0x400,block,Path.GetDirectoryName(s.Exe)!,ref si,out p))throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
   File.WriteAllText(s.Receipt,JsonSerializer.Serialize(new{pid=p.pid,desktop=s.Desktop,exe=s.Exe,utc=DateTime.UtcNow,inputDesktopActive=IsInput(s.Desktop),showInInactiveDesktop=s.ShowInInactiveDesktop,showMode=s.ShowInInactiveDesktop?"SW_SHOWNOACTIVATE":"SW_HIDE"},new JsonSerializerOptions{WriteIndented=true}));
   WaitForSingleObject(p.process,0xFFFFFFFF);GetExitCodeProcess(p.process,out uint code);return unchecked((int)code);
  }finally{if(p.process!=IntPtr.Zero)CloseHandle(p.process);if(p.thread!=IntPtr.Zero)CloseHandle(p.thread);if(block!=IntPtr.Zero)Marshal.FreeHGlobal(block);CloseDesktop(d);}}
}
