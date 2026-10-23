using System;
using System.Linq;
using UnityEngine;
public partial class AdventureFlow
{
    GameObject exitObject;Material exitMaterial;
    void Start()
    {
        exitObject=new GameObject("ForestRuins 普通撤离祭坛");UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(exitObject,gameObject.scene);exitObject.transform.position=ExitPosition;
        var basePart=GameObject.CreatePrimitive(PrimitiveType.Cylinder);basePart.transform.SetParent(exitObject.transform,false);basePart.transform.localScale=new Vector3(1.5f,.08f,1.5f);Destroy(basePart.GetComponent<Collider>());
        var beacon=GameObject.CreatePrimitive(PrimitiveType.Cube);beacon.transform.SetParent(exitObject.transform,false);beacon.transform.localPosition=new Vector3(0,1,0);beacon.transform.localScale=new Vector3(.25f,2,.25f);Destroy(beacon.GetComponent<Collider>());
        exitMaterial=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=new Color(.1f,.8f,1)};basePart.GetComponent<Renderer>().sharedMaterial=exitMaterial;beacon.GetComponent<Renderer>().sharedMaterial=exitMaterial;
    }
    public bool ClaimPending(string id,bool toWarehouse)
    {
        if(!AtCamp||HasResult)return false;var pending=Profile.pending.FirstOrDefault(p=>p.pendingId==id);if(pending==null)return false;
        var gear=session.hero.GetComponent<AdventureLoadout>();
        if(pending.equipment){
            if(AdventureCatalog.Item(pending.item.definitionId)==null||pending.item.Container&&AdventureCatalog.Container(pending.item.definitionId)==null){session.hero.Inventory.NotifyMessage("缺失模板，请补回原模板后取回，或明确弃置。");return false;}
            var copy=pending.item.Clone();copy.worn=copy.board=copy.overflow=false;copy.x=copy.y=-1;
            if(toWarehouse&&session.Camp.Items.Count>=200||!toWarehouse&&!gear.CanAdd(copy)){session.hero.Inventory.NotifyMessage("目标空间不足，物品仍在待领取区。");return false;}
            return session.Camp.CommitChange(()=>{if(toWarehouse){var items=session.Camp.Items.Select(i=>i.Clone()).Concat(new[]{copy}).ToArray();session.Camp.Restore(items,session.Camp.Materials);}else if(!gear.Add(copy))throw new InvalidOperationException("背包空间不足");Profile.pending=Profile.pending.Where(p=>p.pendingId!=id).ToArray();});
        }
        int current=toWarehouse?session.Camp.Materials[(int)pending.material]:session.hero.Inventory.Count(pending.material),amount=Math.Min(pending.amount,CampRuntime.MaterialLimit-current);if(amount<=0)return false;
        return session.Camp.CommitChange(()=>{if(toWarehouse){var materials=(int[])session.Camp.Materials.Clone();materials[(int)pending.material]+=amount;session.Camp.Restore(session.Camp.Items.ToArray(),materials);}else session.hero.Inventory.Add(pending.material,amount);pending.amount-=amount;if(pending.amount==0)Profile.pending=Profile.pending.Where(p=>p.pendingId!=id).ToArray();});
    }
    public bool DiscardPending(string id)
    {
        if(!AtCamp||HasResult||!Profile.pending.Any(p=>p.pendingId==id))return false;
        return session.Camp.CommitChange(()=>Profile.pending=Profile.pending.Where(p=>p.pendingId!=id).ToArray());
    }
    void OnDestroy(){if(session!=null&&!object.ReferenceEquals(session.hero,null))owners.Remove(session.hero);if(exitObject!=null)Destroy(exitObject);if(exitMaterial!=null)Destroy(exitMaterial);}
}
