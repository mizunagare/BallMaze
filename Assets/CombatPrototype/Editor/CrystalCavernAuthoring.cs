using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public static class CrystalCavernAuthoring
{


    [MenuItem("Wanxiang/Author C2.1 Fixed Cavern")]
    public static void Bake() => Bake(false);
    [MenuItem("Wanxiang/Author C2.2 Fixed Cavern")]
    public static void BakeExpanded() => Bake(true);
    [MenuItem("Wanxiang/Author C2.3 Fixed Cavern")]
    public static void BakeLake() => Bake(true, true);

    static void Bake(bool expanded, bool lake = false)
    {
        var folderName = lake ? "CrystalCavernC23" : expanded ? "CrystalCavernC22" : "CrystalCavern";
        var folder = "Assets/Resources/" + folderName;
        if (!AssetDatabase.IsValidFolder(folder)) AssetDatabase.CreateFolder("Assets/Resources", folderName);
        var shader = Shader.Find("Universal Render Pipeline/Lit");
        var stone = Material(folder,"Basalt", shader, new Color(.22f,.27f,.32f));
        var floor = Material(folder,"Slate", shader, new Color(.27f,.33f,.36f));
        var trim = Material(folder,"Rift", shader, new Color(.14f,.33f,.39f));
        var crystal = Material(folder,"Vein", shader, new Color(.17f,.62f,.73f));
        var recovery = Material(folder,"EnergyRecovery", shader, new Color(.14f,.33f,.38f));
        var warning = Material(folder,"EnergyWarning", shader, new Color(.80f,.47f,.09f));
        var active = Material(folder,"EnergyActive", shader, new Color(.91f,.18f,.20f));
        var prism = CrystalMesh(folder);
        var root = new GameObject((lake ? "C2.3" : expanded ? "C2.2" : "C2.1") + " 水晶洞窟 · 固定室内资源");
        try
        {
            var floors = new List<BoxCollider>();
            var walls = new List<BoxCollider>();
            var layout = lake ? CrystalCavernLayout.GenerateLake(1) : expanded ? CrystalCavernLayout.GenerateExpanded(1) : CrystalCavernLayout.Generate(1);
            BoxCollider Box(string pieceName, Vector3 center, Vector3 size, Material surface, bool solid = true)
            {
                var piece = GameObject.CreatePrimitive(PrimitiveType.Cube);
                piece.name = pieceName;
                piece.transform.SetParent(root.transform, false);
                // Store collider size explicitly and render at the same dimensions.
                piece.transform.localPosition = center;
                piece.transform.localScale = size;
                piece.GetComponent<Renderer>().sharedMaterial = surface;
                var collider = piece.GetComponent<BoxCollider>();
                if (!solid) Object.DestroyImmediate(collider);
                return solid ? collider : null;
            }
            void Wall(string name, float x, float z, float width, float depth) =>
                walls.Add(Box(name, new Vector3(x, 4.5f, z), new Vector3(width, 9, depth), stone));
            void Room(string name, float x0, float x1, float z0, float z1)
            {
                float x = (x0+x1)/2, z = (z0+z1)/2;
                var span = new Vector3(x1-x0, .5f, z1-z0);
                floors.Add(Box(name+" · 实体地面", new Vector3(x,-.25f,z), span, floor));
                Box(name+" · 实体顶盖", new Vector3(x,9.25f,z), span, stone);
            }
            void Prism(string name, Transform parent, Vector3 p, Vector3 scale, float angle)
            {
                var item = new GameObject(name, typeof(MeshFilter), typeof(MeshRenderer));
                item.transform.SetParent(parent, false);
                item.transform.localPosition = p;
                item.transform.localRotation = Quaternion.Euler(0, angle, 0);
                item.transform.localScale = scale;
                item.GetComponent<MeshFilter>().sharedMesh = prism;
                item.GetComponent<MeshRenderer>().sharedMaterial = crystal;
            }
            Room("洞窟入口", -6,6,380,396);
            Room("水晶矿脉区", -10,10,396,416);
            Room("能量通道", 10,34,406,414);
            Wall("入口西壁", -6,388,.8f,16);
            Wall("入口东壁", 6,388,.8f,16);
            Wall("入口后壁", 0,380,12,.8f);
            Wall("矿室入口左肩", -8,396,4,.8f);
            Wall("矿室入口右肩", 8,396,4,.8f);
            BoxCollider door = null;
            if (expanded)
            {
                Wall("矿室西壁南段", -10,401.5f,.8f,11);
                Wall("矿室西壁北段", -10,414,.8f,4);
                Room("晶纹岔路", -16,-10,407,412);
                Room("隐藏矿室", -27,-16,404,416);
                Wall("岔路南壁", -13,407,6,.65f);
                Wall("岔路北壁", -13,412,6,.65f);
                Wall("隐藏矿室南壁", -21.5f,404,11,.7f);
                Wall("隐藏矿室北壁", -21.5f,416,11,.7f);
                Wall("隐藏矿室后壁", -27,410,.7f,12);
                Wall("隐藏矿室门肩南", -16,405.5f,.7f,3);
                Wall("隐藏矿室门肩北", -16,414,.7f,4);
                Wall("隐藏矿室支柱", -23.7f,406.1f,1.1f,1.1f);
                Wall("隐藏矿室对称支柱", -23.7f,413.9f,1.1f,1.1f);
                door = Box("实体矿室机关门", new Vector3(-10,4.5f,409.5f), new Vector3(.85f,9,5.35f), trim);
                walls.Add(door);
                for(int i=0;i<6;i++)
                    Box("往返晶纹 "+i,new Vector3(-8-i*2.35f,.023f,409.5f),new Vector3(1.05f,.035f,.30f),crystal,false);
                for(int i=0;i<4;i++)
                    Prism("矿室晶纹壁龛 "+i,root.transform,new Vector3(-25.9f,0,405.8f+i*2.6f),new Vector3(.55f,1.6f+i*.27f,.7f),18*i);
                Box("矿室门额",new Vector3(-9.65f,4.9f,409.5f),new Vector3(.62f,.5f,5.1f),crystal,false);
                Box("矿室门额背面",new Vector3(-10.35f,4.9f,409.5f),new Vector3(.62f,.5f,5.1f),crystal,false);
            }
            else Wall("矿室西壁", -10,406,.8f,20);
            Wall("矿室北壁", 0,416,20,.8f);
            Wall("转角南壁", 10,401,.8f,10);
            Wall("转角北壁", 10,415,.8f,2);
            Wall("通道南壁", 22,406,24,.8f);
            Wall("通道北壁", 22,414,24,.8f);
            var bridgeDoors = new List<BoxCollider>();
            if (!lake) Wall("勘察边界封壁", 34,410,.8f,8);
            else
            {
                var water = Material(folder,"DeepLake",shader,new Color(.055f,.24f,.30f));
                water.SetFloat("_Smoothness",.32f);
                var pale = Material(folder,"ShoreLimestone",shader,new Color(.38f,.46f,.47f));
                // A real void under the water: no navigation or walking collider on the lake surface.
                Box("地下湖 · 无碰撞深水面",new Vector3(59,-1.35f,410),new Vector3(22,.08f,22),water,false);
                Box("湖底 · 不可达低层",new Vector3(59,-5,410),new Vector3(22,.6f,22),stone);
                Room("湖岸入口平台",34,48,403,417);
                Room("西侧环湖岸",38,48,389,438);
                Room("外环北岩岸",38,84,427,438);
                Room("内环南石径",38,84,389,399);
                Room("对岸观察点",70,84,389,438);
                Room("北侧岩岸连接",38,48,417,427);
                Room("回程石桥",46,72,407.5f,412.5f);
                // Elevated ceiling covers the water without creating a walkable source.
                Box("湖穹顶",new Vector3(59,9.25f,413.5f),new Vector3(22,.5f,29),stone);
                // Solid visible shore walls and railings prevent stepping into deep water.
                void Bank(string name,float x,float z,float width,float depth)
                {
                    walls.Add(Box(name,new Vector3(x,-1.55f,z),new Vector3(width,4.5f,depth),pale));
                }
                Bank("西岸南断崖",48,403,1,8);
                Bank("西岸北断崖",48,420,1,15);
                Bank("东岸南断崖",70,403,1,8);
                Bank("东岸北断崖",70,420,1,15);
                Bank("内环湖岸",59,399,22,1);
                Bank("北岸阶层",59,427,22,1);
                // Lake border extends to z427; fill the northern shelf with visible low rock, never walkable water.
                Box("湖面北湾",new Vector3(59,-1.35f,424),new Vector3(22,.08f,6),water,false);
                Bank("石桥南栏",59,407.5f,22,.45f);
                Bank("石桥北栏",59,412.5f,22,.45f);
                Wall("湖室南壁",61,389,46,1);
                Wall("湖室北壁",61,438,46,1);
                Wall("湖室东壁",84,413.5f,1,49);
                Wall("湖室西南壁",38,396,1,14);
                Wall("湖室西北壁",38,427.5f,1,21);
                Wall("湖口西南门肩",34,404.5f,.8f,3);
                Wall("湖口西北门肩",34,415.5f,.8f,3);
                Wall("湖口南过渡壁",36,403,4,.8f);
                Wall("湖口北过渡壁",36,417,4,.8f);
                // No wall at x34: the old energy passage joins the entry platform physically.
                for(int i=0;i<2;i++)
                {
                    var gate=Box("回程桥门 "+i,new Vector3(i==0?47:71,3,410),new Vector3(.75f,6,5),trim);
                    bridgeDoors.Add(gate);walls.Add(gate);
                    gate.GetComponent<Renderer>().enabled=false;
                    for(int bar=0;bar<5;bar++)
                    {
                        var g=GameObject.CreatePrimitive(PrimitiveType.Cube);
                        Object.DestroyImmediate(g.GetComponent<Collider>());
                        g.name="供能石栅";g.transform.SetParent(gate.transform,false);
                        g.transform.localPosition=new Vector3(0,0,-.4f+bar*.2f);
                        g.transform.localScale=new Vector3(1,1,.075f);
                        g.GetComponent<Renderer>().sharedMaterial=crystal;
                    }
                }
                var shoreMesh=ShoreMesh(folder);
                void Rock(string name,Vector3 p,Vector3 scale,float yaw)
                {
                    var g=new GameObject(name,typeof(MeshFilter),typeof(MeshRenderer));
                    g.transform.SetParent(root.transform,false);g.transform.localPosition=p;
                    g.transform.localRotation=Quaternion.Euler(0,yaw,0);g.transform.localScale=scale;
                    g.GetComponent<MeshFilter>().sharedMesh=shoreMesh;g.GetComponent<Renderer>().sharedMaterial=pale;
                }
                // Faceted rocks stay inside the visible bank collider footprint or over the inaccessible water.
                // They neither add hidden walls nor change route widths.
                for(int i=0;i<7;i++)
                {
                    float x=49.5f+i*3.1f;
                    Rock("南岸侵蚀岩层 "+i,new Vector3(x,-1.7f,399.7f),new Vector3(1.9f,2.55f,1.3f),i*19);
                    Rock("北岸侵蚀岩层 "+i,new Vector3(x,-1.7f,426.3f),new Vector3(1.8f,2.7f,1.4f),i*23);
                    Rock("穹顶垂岩 "+i,new Vector3(x,7.4f,424),new Vector3(1.7f,2,1.5f),i*31);
                }
                for(int i=0;i<4;i++)
                {
                    float z=414.5f+i*3.2f;
                    Rock("西岸层理 "+i,new Vector3(48.8f,-1.6f,z),new Vector3(1.4f,2.5f,2),i*21);
                    Rock("东岸层理 "+i,new Vector3(69.2f,-1.6f,z),new Vector3(1.4f,2.55f,2),i*29);
                }
                for(int i=0;i<8;i++)
                {
                    float x=41+i*5.5f;
                    Box("湖岸高位岩层 "+i,new Vector3(x,8.4f,436.4f),new Vector3(3.5f,1.2f,2.2f),pale);
                    Prism("外环晶簇 "+i,root.transform,new Vector3(x,0,436.9f),new Vector3(.65f,1.8f+(i%3)*.6f,.65f),i*23);
                    Box("外环地面路标 "+i,new Vector3(x,.02f,430),new Vector3(1.2f,.03f,.22f),crystal,false);
                }
                for(int i=0;i<5;i++)
                {
                    float x=46+i*7;
                    Box("内环路标 "+i,new Vector3(x,.02f,392),new Vector3(1.2f,.03f,.22f),trim,false);
                    Box("穹顶悬岩 "+i,new Vector3(x,10.5f,421),new Vector3(2,3,2.5f),stone);
                }
                Prism("对岸巨晶地标",root.transform,new Vector3(82,0,423),new Vector3(1.4f,7,1.4f),14);
                Wall("内环实心晶柱",63,396,1.3f,1.3f);
                Prism("内环晶柱包覆",root.transform,new Vector3(63,0,396),new Vector3(1.1f,4.5f,1.1f),31);
                Box("机关供能纹",new Vector3(74,.02f,413),new Vector3(4,.03f,.25f),crystal,false);
            }
            for (int i = 0; i < 4; i++)
            {
                float z = 398+i*5;
                if (!expanded || i != 2) Wall("矿室层状岩肋 "+i,-9.35f,z,1.1f,1.35f);
                Box("矿室高位岩层 "+i, new Vector3(0,8.55f,z), new Vector3(19,.65f,1.1f), trim);
            }
            for (int i = 0; i < 5; i++)
            {
                float x = 13+i*4.5f;
                Box("通道拱顶横肋 "+i,new Vector3(x,8.4f,410),new Vector3(.65f,.85f,7.5f),trim);
                Box("通道侧道标记 "+i,new Vector3(x,.018f,407.05f),new Vector3(3.2f,.025f,.14f),trim,false);
                Box("通道侧道标记北 "+i,new Vector3(x,.018f,412.95f),new Vector3(3.2f,.025f,.14f),trim,false);
            }
            Wall("实体晶柱 · 阻挡直射", 4.3f,406,1.35f,1.8f);
            Prism("晶柱包覆",root.transform,new Vector3(4.3f,0,406),new Vector3(1.35f,5.7f,1.3f),24);
            for (int i=0;i<6;i++)
                Prism("墙根晶簇 "+i, root.transform, new Vector3(-9,0,398+i*2.8f),new Vector3(.6f,1.3f+i*.22f,.7f),i*17);
            var veins = new List<AdventureResource>();
            for (int i=0;i<layout.nodes.Length;i++)
            {
                var node=layout.nodes[i];
                var g = new GameObject(i == 0 ? "可采集铁矿脉" : "可采集晶石脉");
                g.transform.SetParent(root.transform,false);
                g.transform.localPosition=node.position;
                var hit=g.AddComponent<BoxCollider>();
                hit.center=Vector3.up*.65f;
                hit.size=new Vector3(1.7f,1.3f,1.45f);
                Prism("主脉",g.transform,Vector3.zero,new Vector3(.72f,1.75f,.62f),12);
                Prism("伴生脉",g.transform,new Vector3(.49f,0,.15f),new Vector3(.45f,1.1f,.40f),36);
                var vein=g.AddComponent<AdventureResource>();
                vein.nodeId=CrystalCavernLayout.FirstMineId+i;
                vein.entityId=node.id;
                vein.kind=(MaterialKind)node.kind;
                vein.maxHealth=CrystalCavernRegion.MineHealth;
                veins.Add(vein);
            }
            var e = new GameObject("洞窟入口归途",typeof(ExtractionPoint));
            e.transform.SetParent(root.transform,false);
            e.transform.localPosition=layout.exits[0].position;
            Box("归途地标",e.transform.position-Vector3.up*.07f,new Vector3(2.8f,.05f,2.8f),crystal,false);
            for(int i=0;i<3;i++)
                Box("入口导向 "+i,new Vector3(0,.018f,388+i*2),new Vector3(.28f,.025f,1.25f),crystal,false);

            var energy = new GameObject("能量通道 · c2:energy-pulse",typeof(BoxCollider),typeof(CavernEnergyHazard));
            energy.transform.SetParent(root.transform,false);
            energy.transform.localPosition = new Vector3(22,1,410);
            var volume = energy.GetComponent<BoxCollider>();
            volume.isTrigger = true;
            volume.size = new Vector3(6,2,4.8f);
            var marker = GameObject.CreatePrimitive(PrimitiveType.Cube);
            Object.DestroyImmediate(marker.GetComponent<BoxCollider>());
            marker.name="能量范围地面标记";
            marker.transform.SetParent(energy.transform,false);
            marker.transform.localPosition=new Vector3(0,-.974f,0);
            marker.transform.localScale=new Vector3(volume.size.x,.035f,volume.size.z);
            var visual=marker.GetComponent<Renderer>();
            visual.sharedMaterial=recovery;
            var hazard=energy.GetComponent<CavernEnergyHazard>();
            var serialized = new SerializedObject(hazard);
            Set(serialized,"volume",volume);
            Set(serialized,"field",visual);
            Set(serialized,"recoveryMaterial",recovery);
            Set(serialized,"warningMaterial",warning);
            Set(serialized,"activeMaterial",active);
            serialized.ApplyModifiedPropertiesWithoutUndo();
            var region=root.AddComponent<CrystalCavernRegion>();
            serialized=new SerializedObject(region);
            SetArray(serialized,"floors",floors);
            SetArray(serialized,"blockers",walls);
            SetArray(serialized,"veins",veins);
            Set(serialized,"exit",e.GetComponent<ExtractionPoint>());
            Set(serialized,"hazard",hazard);
            Set(serialized,"chamberDoor",door);
            SetArray(serialized,"bridgeDoors",bridgeDoors);
            serialized.ApplyModifiedPropertiesWithoutUndo();
            PrefabUtility.SaveAsPrefabAsset(root,folder+"/Cavern.prefab");
            AssetDatabase.SaveAssets();
        }
        finally { Object.DestroyImmediate(root); }
    }

    static void Set(SerializedObject target,string name,Object value) =>
        target.FindProperty(name).objectReferenceValue=value;

    static void SetArray<T>(SerializedObject target,string name,List<T> values) where T:Object
    {
        var property=target.FindProperty(name);
        property.arraySize=values.Count;
        for(int i=0;i<values.Count;i++) property.GetArrayElementAtIndex(i).objectReferenceValue=values[i];
    }

    static Material Material(string folder,string name,Shader shader,Color color)
    {
        var path=folder+"/"+name+".mat";
        var value=AssetDatabase.LoadAssetAtPath<Material>(path);
        if(value==null)
        {
            value=new Material(shader);
            AssetDatabase.CreateAsset(value,path);
        }
        value.color=color;
        value.SetFloat("_Smoothness",.12f);
        value.SetColor("_EmissionColor",Color.black);
        value.DisableKeyword("_EMISSION");
        EditorUtility.SetDirty(value);
        return value;
    }

    static Mesh CrystalMesh(string folder)
    {
        var path=folder+"/FacetedCrystal.asset";
        var mesh=AssetDatabase.LoadAssetAtPath<Mesh>(path);
        if(mesh!=null)return mesh;
        var vertices=new List<Vector3>();
        var faces=new List<int>();
        void Face(Vector3 a,Vector3 b,Vector3 c)
        {
            faces.Add(vertices.Count);vertices.Add(a);
            faces.Add(vertices.Count);vertices.Add(b);
            faces.Add(vertices.Count);vertices.Add(c);
        }
        for(int side=0;side<6;side++)
        {
            float a=side*Mathf.PI/3,b=(side+1)*Mathf.PI/3;
            var p=new Vector3(Mathf.Cos(a),0,Mathf.Sin(a));
            var q=new Vector3(Mathf.Cos(b),0,Mathf.Sin(b));
            var top=new Vector3(.14f,1.22f,.12f);
            Face(p,p+Vector3.up,q+Vector3.up);
            Face(p,q+Vector3.up,q);
            Face(p+Vector3.up,top,q+Vector3.up);
            Face(Vector3.zero,p,q);
        }
        mesh=new Mesh{name="六面水晶脉"};
        mesh.SetVertices(vertices);mesh.SetTriangles(faces,0);mesh.RecalculateNormals();mesh.RecalculateBounds();
        AssetDatabase.CreateAsset(mesh,path);
        return mesh;
    }

    static Mesh ShoreMesh(string folder)
    {
        var path=folder+"/FacetedShoreRock.asset";
        var prior=AssetDatabase.LoadAssetAtPath<Mesh>(path);if(prior!=null)return prior;
        var vertices=new List<Vector3>();var triangles=new List<int>();
        Vector3 Ring(int side,int level)
        {
            float a=side*Mathf.PI/4;
            float radius=level==0?1:level==1?.86f:.57f;
            radius*=side%3==0?.88f:1;
            return new Vector3(Mathf.Cos(a)*radius,level==0?0:level==1?.62f:1,Mathf.Sin(a)*radius);
        }
        void Face(Vector3 a,Vector3 b,Vector3 c){int n=vertices.Count;vertices.Add(a);vertices.Add(b);vertices.Add(c);triangles.Add(n);triangles.Add(n+1);triangles.Add(n+2);}
        for(int i=0;i<8;i++)
        {
            for(int level=0;level<2;level++){Face(Ring(i,level),Ring(i,level+1),Ring(i+1,level+1));Face(Ring(i,level),Ring(i+1,level+1),Ring(i+1,level));}
            Face(Ring(i,2),Vector3.up,Ring(i+1,2));
        }
        var mesh=new Mesh{name="自有八面侵蚀岸岩"};mesh.SetVertices(vertices);mesh.SetTriangles(triangles,0);mesh.RecalculateNormals();mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,path);return mesh;
    }
}
