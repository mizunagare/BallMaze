from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2/Tests/BR2Allocation.cs.txt');s=p.read_text();Path('I:/WGCombat/CP04BR2-1102-A/Allocation3/BR2Allocation.executed.cs.txt').write_text(s)
s=s.replace('static void Capture(){','static Dictionary<ulong,string> symbols=new Dictionary<ulong,string>();static string Resolve(UnityEditor.Profiling.RawFrameDataView d,ulong ip){if(symbols.TryGetValue(ip,out var name))return name;var m=d.ResolveMethodInfo(ip);name=m.methodName+" | "+m.sourceFileName+":"+m.sourceFileLine;symbols[ip]=name;return name;}static void Capture(){')
s=s.replace('Math.Max(ProfilerDriver.firstFrameIndex,last-4)','Math.Max(0,ProfilerDriver.firstFrameIndex)').replace('var m=d.ResolveMethodInfo(ip);return m.methodName+" | "+m.sourceFileName+":"+m.sourceFileLine;','return Resolve(d,ip);')
s=s.replace('save=ProfilerDriver.SaveProfile(root+"/scoped-profiler.data");','save=false; // This run exports raw per-scope metadata/callstacks; no full-frame binary dump.\n')
s=s.replace('EditorApplication.Exit(raw.Count>0&&errors.Count==0?0:1);','EditorApplication.Exit(raw.Count==rows.Count&&raw.Select(x=>x.marker).Distinct().Count()==rows.Count&&errors.Count==0?0:1);')
s=s.replace('timeSinceStartup+240','timeSinceStartup+360')
p.write_text(s);Path('I:/WGCombat/CP04BR2-1102-A/Fixed/Project/Assets/BR2Validation/Editor/BR2Allocation.cs').write_text(s)
