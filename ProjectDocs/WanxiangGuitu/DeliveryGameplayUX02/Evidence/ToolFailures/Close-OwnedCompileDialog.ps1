param([int]$TargetPid,[string]$Desktop,[string]$Output)
$ErrorActionPreference='Stop'
$p=Get-CimInstance Win32_Process -Filter "ProcessId=$TargetPid";if(!$p.CommandLine.Replace('/','\').Contains('I:\WGCombat\GU02-1030-B\P\Project') -or $p.Name -ne 'Unity.exe'){throw 'exact owned compiler-failed process required'}
Add-Type @"
using System;using System.Text;using System.Collections.Generic;using System.Runtime.InteropServices;
public class OwnedCompileDialog {
 public delegate bool CB(IntPtr w,IntPtr p);
 [DllImport("user32.dll")]public static extern IntPtr OpenDesktop(string n,uint f,bool i,uint a);
 [DllImport("user32.dll")]public static extern bool SetThreadDesktop(IntPtr d);
 [DllImport("user32.dll")]public static extern bool EnumWindows(CB c,IntPtr p);
 [DllImport("user32.dll")]public static extern bool EnumChildWindows(IntPtr w,CB c,IntPtr p);
 [DllImport("user32.dll")]public static extern uint GetWindowThreadProcessId(IntPtr w,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern int GetWindowText(IntPtr w,StringBuilder t,int n);
 [DllImport("user32.dll")]public static extern bool PostMessage(IntPtr w,uint m,IntPtr a,IntPtr b);
 public static string Name(IntPtr w){var b=new StringBuilder(512);GetWindowText(w,b,512);return b.ToString();}
 public static List<string> Run(int pid,string desk){List<string> result=null;Exception error=null;var thread=new System.Threading.Thread(()=>{try{result=Inner(pid,desk);}catch(Exception e){error=e;}});thread.Start();thread.Join();if(error!=null)throw error;return result;} public static List<string> Inner(int pid,string desk){if(!SetThreadDesktop(OpenDesktop(desk,0,false,0x10000000)))throw new Exception("desktop attach failed");var log=new List<string>();EnumWindows((w,p)=>{uint id;GetWindowThreadProcessId(w,out id);if(id!=pid||Name(w)!="Enter Safe Mode?")return true;EnumChildWindows(w,(c,q)=>{var name=Name(c);log.Add(name);if(name.Replace("&","")=="Quit"){log.Add("owned compile-failure Quit BM_CLICK="+PostMessage(c,0xF5,IntPtr.Zero,IntPtr.Zero));}return true;},IntPtr.Zero);return true;},IntPtr.Zero);return log;}
}
"@
[OwnedCompileDialog]::Run($TargetPid,$Desktop)|ConvertTo-Json|Set-Content $Output


