using System;
using UnityEngine;

public partial class AdventureFlow
{
    bool regionRecordsOpen;
    int regionRecordIndex,regionRecordPage;
    ProfileState regionPublished;
    long regionPublishedRevision=-1;
    string regionReadError;

    RegionRecordView QueryRegionRecord()
    {
        // Explicit disk read: never use a Pending plan or a mutable/unconfirmed live Profile.
        try
        {
            if(regionPublished==null || regionPublishedRevision!=Revision)
            {
                var data=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
                regionPublished=data.profile;
                regionPublishedRevision=data.revision;
            }
            regionReadError=null;
            return RegionRecords.Query(regionPublished,HistoryRegions[regionRecordIndex+1]);
        }
        catch(Exception e) { regionReadError="已发布地区档案暂不可读："+e.Message;return null; }
    }

    void OpenRegionRecords()
    { regionRecordsOpen=true;regionRecordPage=0;regionPublished=null; }
    void NextRegionRecord()
    { regionRecordIndex=(regionRecordIndex+1)%3;regionRecordPage=0; }
    void OpenRegionHistory()
    { historyRegion=regionRecordIndex+1;historyType=0;historyPage=0;historyScroll=Vector2.zero;regionRecordsOpen=false; }

    static string[] RegionLines(RegionRecordView view)
    {
        var lines=new System.Collections.Generic.List<string>{view.coverage,"明确记录 / 收藏纪念"};
        lines.AddRange(view.records);lines.Add(RegionRecords.Gaps);
        lines.Add("最近完成（仅显示最近保留记录中的前三条）");lines.AddRange(view.recent);
        lines.Add("复访方向（仅提示，不发奖、不领取、不出征）");lines.AddRange(view.revisit);
        return lines.ToArray();
    }

    static float RegionLineHeight(string line)=>Mathf.Max(58,((line.Length+45)/46)*23+12);

    string[][] RegionPages(RegionRecordView view)
    {
        var lines=view==null?new[]{regionReadError}:RegionLines(view);
        var pages=new System.Collections.Generic.List<string[]>();
        var current=new System.Collections.Generic.List<string>();float height=0;
        foreach(var line in lines)
        {
            float next=RegionLineHeight(line);
            if(current.Count>0 && height+next>430){pages.Add(current.ToArray());current.Clear();height=0;}
            current.Add(line);height+=next;
        }
        if(current.Count>0)pages.Add(current.ToArray());
        regionRecordPage=Mathf.Clamp(regionRecordPage,0,pages.Count-1);
        return pages.ToArray();
    }
    void DrawRegionRecords()
    {
        var pages=RegionPages(QueryRegionRecord());
        Panel("冒险历程 · 地区档案");float x=Left+28,y=Top+76;
        if(CombatUI.Button(new Rect(x,y,180,34),"地区："+ObjectiveCatalog.RegionLabel(HistoryRegions[regionRecordIndex+1]))) NextRegionRecord();
        if(CombatUI.Button(new Rect(x+200,y,230,34),"查看该地区目标历史")) OpenRegionHistory();
        if(CombatUI.Button(new Rect(x+450,y,150,34),"返回历程")) regionRecordsOpen=false;
        if(CombatUI.Button(new Rect(x+834,y,160,34),"关闭")) historyOpen=false;
        float row=y+49;
        foreach(var line in pages[Mathf.Clamp(regionRecordPage,0,pages.Length-1)])
        {float h=RegionLineHeight(line);CombatUI.Text(new Rect(x+8,row,944,h-2),line,17);row+=h;}
        if(CombatUI.Button(new Rect(x,y+492,140,36),"上一屏",regionRecordPage>0))regionRecordPage--;
        if(CombatUI.Button(new Rect(x+156,y+492,140,36),"下一屏",regionRecordPage+1<pages.Length))regionRecordPage++;
        CombatUI.Text(new Rect(x+320,y+492,240,36),$"档案 {regionRecordPage+1} / {pages.Length}",18);
    }

    void BuildRegionRecordsUgui(RectTransform panel)
    {
        var pages=RegionPages(QueryRegionRecord());
        CatUI.Text(panel,"Title","冒险历程 · 地区档案",24,14,680,40,28,CatUI.Gold);
        CatUI.Button(panel,"地区："+ObjectiveCatalog.RegionLabel(HistoryRegions[regionRecordIndex+1]),24,61,180,38,()=>{NextRegionRecord();RebuildHistoryUgui();});
        CatUI.Button(panel,"查看该地区目标历史",219,61,230,38,()=>{OpenRegionHistory();RebuildHistoryUgui();});
        CatUI.Button(panel,"返回历程",464,61,150,38,()=>{regionRecordsOpen=false;RebuildHistoryUgui();});
        CatUI.Button(panel,"关闭",846,19,150,38,()=>{historyOpen=false;RebuildHistoryUgui();});
        float row=112;
        foreach(var line in pages[regionRecordPage])
        {float h=RegionLineHeight(line);CatUI.Text(panel,"Record",line,32,row,936,h-2,17).supportRichText=false;row+=h;}
        CatUI.Button(panel,"上一屏",24,559,130,40,()=>{regionRecordPage--;RebuildHistoryUgui();},regionRecordPage>0);
        CatUI.Button(panel,"下一屏",168,559,130,40,()=>{regionRecordPage++;RebuildHistoryUgui();},regionRecordPage+1<pages.Length);
        CatUI.Text(panel,"RecordPage",$"档案 {regionRecordPage+1} / {pages.Length}",322,565,240,34);
    }
}
