using UnityEngine;
using UnityEngine.EventSystems;
using System.Collections.Generic;

public sealed partial class CatInventoryPresenter {
 string lastClickId,lastClickProfile;bool lastClickStored;float lastClickTime;Vector2 lastClickPosition;float dragCell=32;string placementReason;
 readonly List<RaycastResult> pointerHits=new List<RaycastResult>();readonly List<RectTransform> placementCells=new List<RectTransform>();PointerEventData placementPointer;
 CatGridSlot PointerSlot(){if(EventSystem.current==null||UnityEngine.InputSystem.Mouse.current==null)return null;if(placementPointer==null)placementPointer=new PointerEventData(EventSystem.current);placementPointer.position=UnityEngine.InputSystem.Mouse.current.position.ReadValue();pointerHits.Clear();EventSystem.current.RaycastAll(placementPointer,pointerHits);foreach(var hit in pointerHits){var slot=hit.gameObject.GetComponentInParent<CatGridSlot>();if(slot!=null&&slot.owner==this)return slot;}return null;}
 void PlacementPreview(GearItem item,CatGridSlot slot){placementReason=null;int count=0;if(item!=null&&slot!=null&&ContainerInventoryView.Dragging){int x=slot.x-ContainerInventoryView.Grab.x,y=slot.y-ContainerInventoryView.Grab.y;bool valid=gear.CanPlace(item,slot.board,x,y,ContainerInventoryView.Rotation,true,out var reason);var anchor=(RectTransform)slot.transform;foreach(var p in item.Cells(ContainerInventoryView.Rotation)){if(count==placementCells.Count)placementCells.Add(CatUI.Panel(anchor.parent,"放置预览",0,0,1,1,Color.clear));var cell=placementCells[count++];cell.SetParent(anchor.parent,false);cell.anchoredPosition=anchor.anchoredPosition+new Vector2((p.x-ContainerInventoryView.Grab.x)*slot.cell,-(p.y-ContainerInventoryView.Grab.y)*slot.cell);cell.sizeDelta=Vector2.one*(slot.cell-2);cell.GetComponent<UnityEngine.UI.Image>().color=valid?new Color(.2f,.9f,.5f,.45f):new Color(1,.25f,.2f,.45f);cell.gameObject.SetActive(true);cell.SetAsLastSibling();}placementReason=valid?"松开放置 / 交换 · "+PlayerInput.Key(PlayerAction.Rotate)+"旋转":reason;}
  for(int i=count;i<placementCells.Count;i++)if(placementCells[i]!=null)placementCells[i].gameObject.SetActive(false);
 }
 public void ItemClick(string id,bool warehouse,PointerEventData e){
  if(!DataReady||!Visible||!bag.IsOpen||GameEntry.Loading||ContainerInventoryView.Dragging||e.button!=PointerEventData.InputButton.Left||bag.CurrentPage!=PlayerInventory.Page.Items&&(bag.CurrentPage!=PlayerInventory.Page.Camp||CampInventoryView.Section!=0))return;
  if(warehouse)stored=id;else Select(id);
  bool twice=lastClickId==id&&lastClickStored==warehouse&&lastClickProfile==s.Flow.Profile.profileId&&Time.unscaledTime-lastClickTime<=.35f&&(e.position-lastClickPosition).sqrMagnitude<=25;
  lastClickId=id;lastClickStored=warehouse;lastClickProfile=s.Flow.Profile.profileId;lastClickTime=Time.unscaledTime;lastClickPosition=e.position;
  if(!twice)return;lastClickId=null;
  if(!s.Camp.CanUseWorkbench||s.Flow.HasResult){bag.NotifyMessage("营地数据未就绪或结算待处理，未转移。");return;}
  bool ok=warehouse?s.Camp.WithdrawEquipment(id):s.Camp.DepositEquipment(id);
  if(!ok)bag.NotifyMessage(s.Saves.SaveFailed?s.Saves.FailureDetail:"转移未完成：检查空间、携带保护与存档状态。物品未重复转移。");RequestRefresh();
 }
 public void GrabItem(string id,Vector2Int grab,float cell,Vector2 fraction){lastClickId=null;dragCell=cell;var item=gear.items.Find(i=>i.id==id);if(item==null||!DataReady||!bag.IsOpen)return;selected=id;ContainerInventoryView.BeginDrag(item,grab,fraction);}
 void TransferClicks(UnityEngine.UI.Button button,string id,bool warehouse){var handler=button.gameObject.AddComponent<CatTransferClick>();handler.owner=this;handler.id=id;handler.warehouse=warehouse;}
}
public sealed class CatTransferClick:MonoBehaviour,IPointerClickHandler,IBeginDragHandler,IDragHandler {
 public CatInventoryPresenter owner;public string id;public bool warehouse;
 public void OnPointerClick(PointerEventData e){if(!e.dragging)owner.ItemClick(id,warehouse,e);}
 public void OnBeginDrag(PointerEventData e){owner.CancelDrag();}
 public void OnDrag(PointerEventData e){}
}
