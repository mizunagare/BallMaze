using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
[Serializable] public class GroundLootPage { public string hash; public int count,bytes; }
// Immutable, bounded pages are durable before the atomic envelope references them.
// Unreferenced pages are retained: backup envelopes may still own them.
public static class GroundLootStore
{
    [NonSerialized] public static Action<string> ValidationHook;
    public const int PageSize=256;
    [Serializable] class Page { public SavedLoot[] items; }
    static IEnumerable<CombatCheckpoint> Worlds(CombatSaveData d) {
        yield return d;
        if(d.profile!=null&&d.profile.camp!=null)yield return d.profile.camp;
        if(d.activeRun!=null&&d.activeRun.checkpoint!=null)yield return d.activeRun.checkpoint;
        if(d.settlement!=null&&d.settlement.plan!=null&&d.settlement.plan.camp!=null)yield return d.settlement.plan.camp;
    }
    static string Hash(byte[] b){using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
    static string PathFor(string root,string hash){if(hash==null||hash.Length!=64||hash.Any(c=>!"0123456789abcdef".Contains(c)))throw new InvalidDataException("掉落分页标识损坏");return Path.Combine(root,"ground-loot",hash+".json");}
    public static void Pack(CombatSaveData d,string root) {
        Directory.CreateDirectory(Path.Combine(root,"ground-loot"));
        foreach(var c in Worlds(d)) {
            var items=c.loot??new SavedLoot[0];var refs=new List<GroundLootPage>();
            for(int start=0;start<items.Length;start+=PageSize){
                var chunk=items.Skip(start).Take(PageSize).ToArray();byte[] b=Encoding.UTF8.GetBytes(JsonUtility.ToJson(new Page{items=chunk}));string hash=Hash(b),path=PathFor(root,hash);
                if(File.Exists(path)){if(Hash(File.ReadAllBytes(path))!=hash)throw new InvalidDataException("已有掉落分页损坏，停止覆盖");}
                else {ValidationHook?.Invoke("before-page-write");string temp=path+".tmp";using(var f=new FileStream(temp,FileMode.Create,FileAccess.Write,FileShare.None)){f.Write(b,0,b.Length);f.Flush(true);}File.Move(temp,path);ValidationHook?.Invoke("after-page-write");}
                refs.Add(new GroundLootPage{hash=hash,count=chunk.Length,bytes=b.Length});
            }
            c.loot=new SavedLoot[0];c.groundLootPages=refs.ToArray();
        }
    }
    public static void Unpack(CombatSaveData d,string root) {
        foreach(var c in Worlds(d)) {
            if(c.groundLootPages==null)throw new InvalidDataException("缺少掉落分页清单");
            if(c.loot==null||c.loot.Length!=0)throw new InvalidDataException("掉落同时存在内联与分页，拒绝重复恢复");
            var items=new List<SavedLoot>();
            foreach(var r in c.groundLootPages){
                if(r==null||r.count<1||r.count>PageSize||r.bytes<1||r.bytes>4*1024*1024)throw new InvalidDataException("掉落分页范围损坏");
                string path=PathFor(root,r.hash);if(!File.Exists(path)||new FileInfo(path).Length!=r.bytes)throw new InvalidDataException("掉落分页缺失或被截断");
                byte[] b=File.ReadAllBytes(path);if(Hash(b)!=r.hash)throw new InvalidDataException("掉落分页校验失败");
                var page=JsonUtility.FromJson<Page>(Encoding.UTF8.GetString(b));if(page==null||page.items==null||page.items.Length!=r.count)throw new InvalidDataException("掉落分页计数错误");items.AddRange(page.items);
            }
            c.loot=items.ToArray();c.groundLootPages=null;
        }
    }
}
