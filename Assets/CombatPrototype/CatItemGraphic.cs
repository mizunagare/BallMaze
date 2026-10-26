using System.Collections.Generic;using System.Linq;using UnityEngine;using UnityEngine.UI;

// Samples one shared item texture across exactly its occupied cells, including holes and rotation.
// Rendering and hit testing remain separate; this decorative mesh never blocks grid targets.
[RequireComponent(typeof(CanvasRenderer))]
public sealed class CatItemGraphic:MaskableGraphic {
 Rect crop;Texture texture;Vector2Int size;Vector2Int[] cells;float cell;int turn;
 public override Texture mainTexture=>texture!=null?texture:Texture2D.whiteTexture;
 public void Bind(GearItem item,int rotation,float pixels){turn=rotation%4;color=Color.white;texture=AdventureItems.Texture(item.Icon);crop=CatIconLayout.UV(item.Icon);size=item.SizeAt(rotation);cells=item.Cells(rotation).ToArray();cell=pixels;raycastTarget=false;SetAllDirty();}
 Vector2 SourceUV(float x,float y){float a=x,b=y;if(turn==1){a=y;b=1-x;}else if(turn==2){a=1-x;b=1-y;}else if(turn==3){a=1-y;b=x;}return new Vector2(crop.x+a*crop.width,crop.yMax-b*crop.height);}
 protected override void OnPopulateMesh(VertexHelper vh){vh.Clear();if(cells==null)return;foreach(var p in cells){float x=p.x*cell,y=-p.y*cell;float a=p.x/(float)size.x,b=p.y/(float)size.y,dx=1f/size.x,dy=1f/size.y;int n=vh.currentVertCount;vh.AddVert(new Vector3(x,y-cell),color,SourceUV(a,b+dy));vh.AddVert(new Vector3(x,y),color,SourceUV(a,b));vh.AddVert(new Vector3(x+cell,y),color,SourceUV(a+dx,b));vh.AddVert(new Vector3(x+cell,y-cell),color,SourceUV(a+dx,b+dy));vh.AddTriangle(n,n+1,n+2);vh.AddTriangle(n,n+2,n+3);}}
}
