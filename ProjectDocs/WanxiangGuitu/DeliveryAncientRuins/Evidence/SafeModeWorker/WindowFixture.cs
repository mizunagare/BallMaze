using System.Runtime.InteropServices;
using System.Text.Json;
// Synthetic Win32 window for automation safety self-tests; never a Player/U16 substitute.
internal static class WindowFixture {
 delegate IntPtr WndProc(IntPtr h,uint m,IntPtr w,IntPtr l);
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct WClass{public uint style;public WndProc proc;public int extra,windowExtra;public IntPtr instance,icon,cursor,brush;public string? menu;public string name;}
 [StructLayout(LayoutKind.Sequential)] struct Msg{public IntPtr h;public uint message;public UIntPtr w;public IntPtr l;public uint time;public int x,y;public uint privateData;}
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]static extern ushort RegisterClass(ref WClass c);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]static extern IntPtr CreateWindowEx(uint e,string c,string title,uint style,int x,int y,int width,int height,IntPtr parent,IntPtr menu,IntPtr instance,IntPtr param);
 [DllImport("user32.dll")]static extern IntPtr DefWindowProc(IntPtr h,uint m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")]static extern int GetMessage(out Msg m,IntPtr w,uint a,uint b);
 [DllImport("user32.dll")]static extern IntPtr DispatchMessage(ref Msg m);
 [DllImport("user32.dll")]static extern void PostQuitMessage(int code);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)]static extern IntPtr GetModuleHandle(string? n);
 internal static int Run(string marker){WndProc callback=(h,m,w,l)=>{if(m==0x10){File.WriteAllText(marker,JsonSerializer.Serialize(new{kind="synthetic worker window, not game",closedUtc=DateTime.UtcNow}));PostQuitMessage(0);}return DefWindowProc(h,m,w,l);};var c=new WClass{proc=callback,instance=GetModuleHandle(null),name="WGTestWorkerFixture"};if(RegisterClass(ref c)==0)throw new Exception("Cannot register synthetic window");var window=CreateWindowEx(0,c.name,"WGTest synthetic worker fixture",0x00CF0000,0,0,1300,760,IntPtr.Zero,IntPtr.Zero,c.instance,IntPtr.Zero);if(window==IntPtr.Zero)throw new Exception("Cannot create test window");File.WriteAllText(marker+".ready.json",JsonSerializer.Serialize(new{kind="synthetic worker window",readyUtc=DateTime.UtcNow}));while(GetMessage(out var msg,IntPtr.Zero,0,0)>0)DispatchMessage(ref msg);GC.KeepAlive(callback);return 0;}
}
