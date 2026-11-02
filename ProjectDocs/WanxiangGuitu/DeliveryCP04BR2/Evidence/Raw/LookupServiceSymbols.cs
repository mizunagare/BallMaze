using System;using System.Collections.Generic;using System.Runtime.InteropServices;using System.Text;public static class BR2ServiceLookup{
const string D="C:/Program Files (x86)/Windows Kits/10/Debuggers/x64/dbghelp.dll";
[DllImport(D,CharSet=CharSet.Unicode,SetLastError=true)]static extern bool SymInitializeW(IntPtr p,string path,bool invade);
[DllImport(D,CharSet=CharSet.Unicode,SetLastError=true)]static extern ulong SymLoadModuleExW(IntPtr p,IntPtr file,string image,string module,ulong bas,uint size,IntPtr data,uint flags);
[DllImport(D,SetLastError=true)]static extern bool SymEnumSymbols(IntPtr p,ulong bas,string mask,Callback cb,IntPtr user);
[DllImport(D)]static extern uint SymSetOptions(uint opts);[DllImport(D)]static extern bool SymCleanup(IntPtr p);
delegate bool Callback(IntPtr symbol,uint size,IntPtr context);
[DllImport(D,SetLastError=true)]static extern bool SymFromAddr(IntPtr p,ulong address,out ulong disp,IntPtr info);public static string[] Read(){IntPtr h=(IntPtr)0x123456;string dir="C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor";var rows=new List<string>();SymSetOptions(0x2|0x4|0x10|0x400);if(!SymInitializeW(h,dir,false))throw new Exception("SymInitialize "+Marshal.GetLastWin32Error());try{ulong b=SymLoadModuleExW(h,IntPtr.Zero,dir+"/Unity.dll","Unity",0,0,IntPtr.Zero,0);rows.Add("base="+b+" error="+Marshal.GetLastWin32Error());foreach(ulong addr in new ulong[]{0x1849fc5c8,0x1849fc7a8,0x1849fc1e0,0x1849fc288,0x1849fc3d8,0x1849fc490,0x182711c00,0x182717c80}){var info=Marshal.AllocHGlobal(4096);try{Marshal.WriteInt32(info,88);Marshal.WriteInt32(info,80,2048);ulong disp;bool ok=SymFromAddr(h,addr,out disp,info);rows.Add(addr.ToString("x")+" "+ok+" "+(ok?Marshal.PtrToStringAnsi(info+84):"error="+Marshal.GetLastWin32Error()));}finally{Marshal.FreeHGlobal(info);}}return rows.ToArray();}finally{SymCleanup(h);}}
}


