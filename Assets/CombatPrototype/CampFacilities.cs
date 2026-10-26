using System.Linq;
using UnityEngine;

public partial class CampRuntime {
 public bool Exploring {get;private set;}
 public static readonly string[] FacilityIds={"camp:equipment","camp:warehouse","camp:workbench","camp:departure"};
 public static readonly string[] FacilityNames={"装备整备","永久仓库","营地工作台","森林出征"};
 public static readonly Vector3[] FacilityOffsets={new Vector3(-3,0,-1),new Vector3(2,0,2),new Vector3(3,0,-1),new Vector3(-3,0,3)};
 readonly System.Collections.Generic.List<Renderer> facilityMarkers=new System.Collections.Generic.List<Renderer>();
 public Vector3 FacilityPosition(string id){if(id=="camp:help")return CampPosition+new Vector3(-5,0,0);int i=System.Array.IndexOf(FacilityIds,id);return i<0?CampPosition:CampPosition+FacilityOffsets[i];}
 public string FacilityReason(string id){if(!FacilityIds.Contains(id))return "设施不存在。";if(!InCamp||!session.Flow.AtCamp||session.Flow.HasResult||session.Flow.Preparing)return "请先完成结算或出征确认。";if(!session.Saves.IsInitialized||!session.Saves.CanCommitWarehouse||session.Saves.SaveFailed||!string.IsNullOrEmpty(session.Flow.Error))return "存档尚未就绪或保存失败，请先处理。";if(!Exploring||session.hero.GameplayPaused)return "请先关闭面板，进入营地走动。";if(Vector3.Distance(session.hero.transform.position,FacilityPosition(id))>2.2f)return "请靠近设施。";return "";}
 public bool Explore(){if(!InCamp||!session.Flow.AtCamp||session.Flow.HasResult||session.Flow.Preparing||!session.Saves.IsInitialized)return false;Exploring=true;session.hero.Inventory.SetOpen(false);session.hero.SaveMenuOpen=false;Time.timeScale=0;Cursor.lockState=CursorLockMode.Locked;Cursor.visible=false;return !session.hero.Inventory.IsOpen;}
 public bool InteractFacility(string id){if(id=="camp:help"){if(!InCamp||!session.Flow.AtCamp||session.Flow.HasResult||session.Flow.Preparing||!Exploring||session.hero.GameplayPaused||!session.Saves.IsInitialized||session.Saves.SaveFailed||Vector3.Distance(session.hero.transform.position,FacilityPosition(id))>2.2f)return false;PlayerHudPresenter.Instance.SetDetails("教程");return PlayerHudPresenter.Instance.Detail=="教程";}string reason=FacilityReason(id);if(reason!=""){session.hero.Inventory.NotifyMessage(reason);return false;}
  if(id=="camp:departure"){session.Flow.OpenPreparation();return session.Flow.Preparing;}
  if(id=="camp:equipment")session.hero.Inventory.OpenPage(PlayerInventory.Page.Weapons);
  else {CampInventoryView.SelectSection(id=="camp:workbench"?2:1);session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);}
  if(!session.hero.Inventory.IsOpen)return false;Onboarding.Facility(session,id);session.Saves.SaveProgress(false);return true;
 }
 void BuildFacilityMarkers(){for(int i=0;i<FacilityIds.Length;i++){var m=ColorMaterial(new Color(.35f,.55f,.5f));var g=Part(FacilityNames[i]+" · 交互标记",PrimitiveType.Cylinder,FacilityOffsets[i]+Vector3.up*.04f,new Vector3(1,.035f,1),m);facilityMarkers.Add(g.GetComponent<Renderer>());}}
 void TickFacilities(){if(!InCamp||!session.Flow.AtCamp)return;string current=Onboarding.Active(session)?Onboarding.FacilityId(session):null;for(int i=0;i<facilityMarkers.Count;i++)if(facilityMarkers[i]!=null)facilityMarkers[i].sharedMaterial.color=FacilityIds[i]==current?new Color(1,.7f,.2f):new Color(.35f,.55f,.5f);
  if(Exploring&&!session.hero.GameplayPaused){var p=session.hero.transform.position;var bounded=new Vector3(Mathf.Clamp(p.x,CampPosition.x-7.5f,CampPosition.x+7.5f),p.y,Mathf.Clamp(p.z,CampPosition.z-6.5f,CampPosition.z+8));session.hero.GetComponent<CharacterController>().Move(bounded-p);}}
}
