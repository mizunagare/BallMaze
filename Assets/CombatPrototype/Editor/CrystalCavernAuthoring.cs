using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public static class CrystalCavernAuthoring
{
    const string Folder = "Assets/Resources/CrystalCavern";

    [MenuItem("Wanxiang/Author C2.1 Fixed Cavern")]
    public static void Bake()
    {
        if (!AssetDatabase.IsValidFolder(Folder)) AssetDatabase.CreateFolder("Assets/Resources", "CrystalCavern");
        var shader = Shader.Find("Universal Render Pipeline/Lit");
        var stone = Material("Basalt", shader, new Color(.22f,.27f,.32f));
        var floor = Material("Slate", shader, new Color(.27f,.33f,.36f));
        var trim = Material("Rift", shader, new Color(.14f,.33f,.39f));
        var crystal = Material("Vein", shader, new Color(.17f,.62f,.73f));
        var recovery = Material("EnergyRecovery", shader, new Color(.14f,.33f,.38f));
        var warning = Material("EnergyWarning", shader, new Color(.80f,.47f,.09f));
        var active = Material("EnergyActive", shader, new Color(.91f,.18f,.20f));
        var prism = CrystalMesh();
        var root = new GameObject("C2.1 水晶洞窟 · 固定室内资源");
        try
        {
            var floors = new List<BoxCollider>();
            var walls = new List<BoxCollider>();
            var layout = CrystalCavernLayout.Generate(1);
            BoxCollider Box(string name, Vector3 center, Vector3 size, Material surface, bool solid = true)
            {
                var piece = GameObject.CreatePrimitive(PrimitiveType.Cube);
                piece.name = name;
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
            Wall("矿室西壁", -10,406,.8f,20);
            Wall("矿室北壁", 0,416,20,.8f);
            Wall("转角南壁", 10,401,.8f,10);
            Wall("转角北壁", 10,415,.8f,2);
            Wall("通道南壁", 22,406,24,.8f);
            Wall("通道北壁", 22,414,24,.8f);
            Wall("勘察边界封壁", 34,410,.8f,8);
            for (int i = 0; i < 4; i++)
            {
                float z = 398+i*5;
                Wall("矿室层状岩肋 "+i,-9.35f,z,1.1f,1.35f);
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
            serialized.ApplyModifiedPropertiesWithoutUndo();
            PrefabUtility.SaveAsPrefabAsset(root,Folder+"/Cavern.prefab");
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

    static Material Material(string name,Shader shader,Color color)
    {
        var path=Folder+"/"+name+".mat";
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

    static Mesh CrystalMesh()
    {
        var path=Folder+"/FacetedCrystal.asset";
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
}
