using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.AI;

public class ForestRouteResult {
    public bool reachable,nearElite;public float distance;public Vector3[] corners=new Vector3[0];
    public NavMeshPathStatus status=NavMeshPathStatus.PathInvalid;
}
public partial class ForestRegionRuntime {
    readonly List<Mesh> terrainMeshes=new List<Mesh>();
    readonly List<NavMeshBuildSource> terrainSources=new List<NavMeshBuildSource>();
    class CachedRoute {public Vector3 from,to;public float time;public ForestRouteResult route;}
    readonly Dictionary<string,CachedRoute> routeCache=new Dictionary<string,CachedRoute>();
    class CachedApproach {public Vector3 position,approach;public float range,time;public bool valid;}
    readonly Dictionary<string,CachedApproach> approachCache=new Dictionary<string,CachedApproach>();
    public int RouteQueries {get;private set;}
    public int ApproachQueries {get;private set;}
    string routeState;
    public void InvalidateRoutes(){routeCache.Clear();approachCache.Clear();}
    public bool TryCachedInteractionApproach(ExtractionConfig exit,out Vector3 approach) {
        if(approachCache.TryGetValue(exit.id,out var cached)&&cached.position==exit.position&&cached.range==exit.range&&Time.realtimeSinceStartup-cached.time<RouteScoringConfig.Read().cacheSeconds){approach=cached.approach;return cached.valid;}
        ApproachQueries++;bool valid=TryInteractionApproach(exit,out approach);
        approachCache[exit.id]=new CachedApproach{position=exit.position,range=exit.range,approach=approach,valid=valid,time=Time.realtimeSinceStartup};return valid;
    }
    public void ObserveRouteState(string value){if(routeState!=value){routeState=value;InvalidateRoutes();}}
    void BuildTerrain() {
        for(int area=0;area<2;area++) {
            var mesh=Layout.terrain.Surface(Layout,area==1);terrainMeshes.Add(mesh);
            var obj=new GameObject(mesh.name);obj.transform.SetParent(root.transform,false);
            obj.AddComponent<MeshFilter>().sharedMesh=mesh;obj.AddComponent<MeshCollider>().sharedMesh=mesh;
            var material=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=new Color(.2f,.32f,.19f)};materials.Add(material);obj.AddComponent<MeshRenderer>().sharedMaterial=material;
            terrainSources.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Mesh,sourceObject=mesh,transform=Matrix4x4.identity,area=area==1?3:0});
        }
        var water=Layout.terrain;Part("深湖水面 · 不可通行",water.lakeCenter+Vector3.up*.015f,new Vector3(water.lakeSize.x,.1f,water.lakeSize.z),new Color(.08f,.32f,.43f),false);
        var blocker=Part("深水实体边界",water.lakeCenter+Vector3.up*2,new Vector3(water.lakeSize.x,6,water.lakeSize.z),Color.blue);blocker.GetComponent<Renderer>().enabled=false;
        Part("自然岩脊 · 两侧可绕行",water.ridgeCenter+Vector3.up*2,water.ridgeSize,new Color(.3f,.32f,.28f));
        var ferry=Layout.exits.Single(e=>e.repairRequired);Part("渡口岸边深水 · 不可通行",ferry.position+new Vector3(-8,2,0),new Vector3(7,6,14),new Color(.13f,.36f,.43f)).GetComponent<Renderer>().enabled=false;
        Part("渡口岸边水面",ferry.position+new Vector3(-8,-.1f,0),new Vector3(7,.1f,14),new Color(.12f,.4f,.5f),false);
    }
    void DrawNavigatedRoads() {
        foreach(var edge in Layout.routes){var path=new NavMeshPath();var from=Layout.points.Single(p=>p.id==edge.from).position;var to=Layout.points.Single(p=>p.id==edge.to).position;
            if(!NavMesh.SamplePosition(from,out var a,3,NavMesh.AllAreas)||!NavMesh.SamplePosition(to,out var b,3,NavMesh.AllAreas)||!NavMesh.CalculatePath(a.position,b.position,NavMesh.AllAreas,path)||path.status!=NavMeshPathStatus.PathComplete)throw new InvalidOperationException("主路缺少完整导航");
            for(int i=1;i<path.corners.Length;i++){var start=path.corners[i-1];var end=path.corners[i];int count=Mathf.Max(1,Mathf.CeilToInt(Vector3.Distance(start,end)/3));
                for(int part=0;part<count;part++){var p=Vector3.Lerp(start,end,(float)part/count);var q=Vector3.Lerp(start,end,(float)(part+1)/count);var mid=(p+q)*.5f;
                    if(Layout.terrain.InLake(mid,2)||Layout.terrain.InRidge(mid,1))continue;p.y=Layout.terrain.Height(Layout,p)+.035f;q.y=Layout.terrain.Height(Layout,q)+.035f;
                    var road=Part("自然主路 · 可离路探索",(p+q)*.5f,new Vector3(3,.02f,Vector3.Distance(p,q)),new Color(.38f,.34f,.24f),false);road.transform.rotation=Quaternion.LookRotation(q-p);
                }
            }
        }
    }
    // Queries are pure with respect to the run/save/RNG. Results are bounded-age,
    // spatially cached; geometry changes explicitly invalidate the cache.
    public ForestRouteResult NavigationRoute(Vector3 from,string target,bool avoidElite=false) {
        var point=Layout?.points.FirstOrDefault(p=>p.id==target);
        return point==null?new ForestRouteResult():NavigationPath(from,point.position,"poi:"+target,avoidElite);
    }
    public ForestRouteResult NavigationPath(Vector3 from,Vector3 to,string target,bool avoidElite=false) {
        if(!Ready||Layout==null)return new ForestRouteResult();
        var config=RouteScoringConfig.Read();
        string key=target+(avoidElite?":safe":":short");
        if(routeCache.TryGetValue(key,out var cache)&&cache.to.Equals(to)&&cache.from.Equals(from)&&Time.realtimeSinceStartup-cache.time<config.cacheSeconds)return CopyRisk(cache.route);
        var result=new ForestRouteResult();
        {var path=new NavMeshPath();int mask=avoidElite&&Layout.revision>=5?NavMesh.AllAreas&~(1<<3):NavMesh.AllAreas;
            RouteQueries++;if(NavMesh.SamplePosition(from,out var a,2,mask)&&NavMesh.SamplePosition(to,out var b,2,mask)&&NavMesh.CalculatePath(a.position,b.position,mask,path)){
                result.status=path.status;result.reachable=path.status==NavMeshPathStatus.PathComplete;
                if(result.reachable){result.corners=path.corners;for(int i=1;i<result.corners.Length;i++)result.distance+=Vector3.Distance(result.corners[i-1],result.corners[i]);}
            }
        }
        routeCache[key]=new CachedRoute{from=from,to=to,time=Time.realtimeSinceStartup,route=result};return CopyRisk(result);
    }
    ForestRouteResult CopyRisk(ForestRouteResult route) {
        float buffer=RouteScoringConfig.Read().perceptionBuffer;
        bool risk=S.enemies.Any(e=>!e.Health.Dead&&(e.archetype==EnemyArchetype.Elite||e.GetComponent<ForestBossBrain>()!=null)&&RouteScoring.NearPath(e,route.corners,buffer));
        return new ForestRouteResult{reachable=route.reachable,status=route.status,distance=route.distance,corners=(Vector3[])route.corners.Clone(),nearElite=risk};
    }
}
