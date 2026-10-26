using System.Collections.Generic;using System.Linq;using UnityEngine;using UnityEngine.UI;

// Samples one shared item texture across exactly its occupied cells, including holes and rotation.
// Rendering and hit testing remain separate; this decorative mesh never blocks grid targets.
public sealed class CatItemGraphic:MaskableGraphic {
 Texture texture;Vector2Int size;Vector2Int[] cells;float cell;
 public override Texture mainTexture=>texture!=null?texture:Texture2D.whiteTexture;
 public void Bind(GearItem item,int rotation,float pixels){texture=AdventureItems.Texture(item.Icon);size=item.SizeAt(rotation);cells=item.Cells(rotation).ToArray();cell=pixels;raycastTarget=false;SetAllDirty();}
 protected override void OnPopulateMesh(VertexHelper vh){vh.Clear();if(cells==null)return;foreach(var p in cells){float x=p.x*cell,y=-p.y*cell;float u=p.x/(float)size.x,v=1-p.y/(float)size.y,du=1f/size.x,dv=1f/size.y;int n=vh.currentVertCount;vh.AddVert(new Vector3(x,y-cell),color,new Vector2(u,v-dv));vh.AddVert(new Vector3(x,y),color,new Vector2(u,v));vh.AddVert(new Vector3(x+cell,y),color,new Vector2(u+du,v));vh.AddVert(new Vector3(x+cell,y-cell),color,new Vector2(u+du,v-dv));vh.AddTriangle(n,n+1,n+2);vh.AddTriangle(n,n+2,n+3);}}
}
