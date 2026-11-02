using System;using System.Collections.Generic;using System.Runtime.InteropServices;using System.Text;public static class BR2Insights{
const string D="C:/Program Files (x86)/Windows Kits/10/Debuggers/x64/dbghelp.dll";
[DllImport(D,CharSet=CharSet.Unicode,SetLastError=true)]static extern bool SymInitializeW(IntPtr p,string path,bool invade);
[DllImport(D,CharSet=CharSet.Unicode,SetLastError=true)]static extern ulong SymLoadModuleExW(IntPtr p,IntPtr file,string image,string module,ulong bas,uint size,IntPtr data,uint flags);
[DllImport(D,SetLastError=true)]static extern bool SymEnumSymbols(IntPtr p,ulong bas,string mask,Callback cb,IntPtr user);
[DllImport(D)]static extern uint SymSetOptions(uint opts);[DllImport(D)]static extern bool SymCleanup(IntPtr p);
delegate bool Callback(IntPtr symbol,uint size,IntPtr context);
public static string[] Read(){IntPtr h=(IntPtr)0x123456;string dir="C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor";var rows=new List<string>();SymSetOptions(0x2|0x4|0x10|0x400);if(!SymInitializeW(h,dir,false))throw new Exception("SymInitialize "+Marshal.GetLastWin32Error());try{ulong b=SymLoadModuleExW(h,IntPtr.Zero,dir+"/Unity.dll","Unity",0,0,IntPtr.Zero,0);rows.Add("base="+b+" error="+Marshal.GetLastWin32Error());Callback cb=(s,n,c)=>{int len=Marshal.ReadInt32(s,76);string name=Marshal.PtrToStringAnsi(s+84,len);long addr=Marshal.ReadInt64(s,56);rows.Add(addr.ToString("x")+" size="+n+" "+name);return true;};bool ok=SymEnumSymbols(h,b,"*Insights*",cb,IntPtr.Zero);rows.Add("enumerated="+ok+" error="+Marshal.GetLastWin32Error());return rows.ToArray();}finally{SymCleanup(h);}}
}

