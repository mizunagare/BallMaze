using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;

// C1 is an explicit new schema in the existing region snapshot envelope. Old forest
// revisions never enter this generator or validator, including during resume.
public static class RuinsLayout {
 public const string Map="ancient-ruins",Content="C1-RUINS-1",Region="AncientRuins";
 public static bool Is(ForestLayout l)=>l!=null&&l.revision==6&&l.mapId==Map;
 public static ForestLayout Generate(int seed){
  var l=new ForestLayout{mapId=Map,revision=6,seed=seed,requestedSeed=seed,boundsCenter=new Vector3(0,2,235),boundsSize=new Vector3(90,26,154),entry=new Vector3(0,.1f,176),terrain=null,bossVersion=0};
  var pos=new[]{l.entry,new Vector3(0,.1f,202),new Vector3(0,.1f,227),new Vector3(-12,-2.9f,253),new Vector3(10,.1f,285)};
  string[] labels={"遗迹入口","石柱广场","机关走廊","地下祭坛","守护者大厅"};
  l.points=pos.Select((p,i)=>new ForestPoi{id="c1:p"+i,label=labels[i],position=p,risk=i==4?3:i==2||i==3?2:1,siteKind=i==0?ForestSiteKind.Entrance:ForestSiteKind.Ruins}).ToArray();
  l.routes=Enumerable.Range(0,4).Select(i=>new ForestRoute{from="c1:p"+i,to="c1:p"+(i+1)}).ToArray();
  l.nodes=new ForestNode[0];l.rocks=new Vector3[0];
  // Jitter only within surveyed clear spaces; no reward/global stream used.
  var rng=new System.Random(unchecked(seed^0x613ac));
  l.encounters=new[]{new ForestEncounter{id="c1:guard",poi="c1:p1",home=new Vector3(-7+rng.Next(3),.1f,202),type=0},new ForestEncounter{id="c1:archer",poi="c1:p1",home=new Vector3(8,.1f,207+rng.Next(3)),type=1},new ForestEncounter{id="c1:elite",poi="c1:p3",home=new Vector3(-16,-2.9f,257),type=2},new ForestEncounter{id="c1:guardian",poi="c1:p4",home=new Vector3(12,.1f,287),type=3}};
  l.exits=new[]{new ExtractionConfig{id="c1:exit-entry",label="遗迹入口归途",position=new Vector3(0,.1f,171)},new ExtractionConfig{id="c1:exit-hall",label="大厅归途碑",position=new Vector3(25,.1f,296)}};
  Validate(l);return l;
 }
 public static SavedWorldEvent[] Events()=>new[]{
  Event("c1:lever",WorldEventKind.Altar,new Vector3(-5,0,211)),Event("c1:door",WorldEventKind.Altar,new Vector3(-2.6f,0,218)),
  Event("c1:archive",WorldEventKind.Altar,new Vector3(-14,-3,250)),Event("c1:hidden",WorldEventKind.Treasure,new Vector3(-29,-3,254)),
  Event("c1:plaza-chest",WorldEventKind.Treasure,new Vector3(11,0,202)),Event("c1:hall-chest",WorldEventKind.Treasure,new Vector3(24,0,289))};
 static SavedWorldEvent Event(string id,WorldEventKind kind,Vector3 p)=>new SavedWorldEvent{entityId=id,kind=kind,position=p};
 public static bool Used(IEnumerable<SavedWorldEvent> events,string id)=>events?.Any(e=>e.entityId==id&&e.used)==true;
 public static void Validate(ForestLayout l){
  if(!Is(l)||l.bossVersion!=0||l.terrain!=null||l.seed!=l.requestedSeed||l.fallback||l.generationAttempt!=0||l.generationFailures==null||l.generationFailures.Length!=0)Bad();
  if(l.points==null||l.points.Length!=5||l.encounters==null||l.encounters.Length!=4||l.nodes==null||l.nodes.Length!=0||l.rocks==null||l.rocks.Length!=0||l.routes==null||l.routes.Length!=4||l.exits==null||l.exits.Length!=2)Bad();
  if(!l.points.Select(p=>p.id).SequenceEqual(Enumerable.Range(0,5).Select(i=>"c1:p"+i))||l.encounters.Select(e=>e.id).Distinct().Count()!=4||l.encounters.Count(e=>e.type==3&&e.id=="c1:guardian")==0)Bad();
  if(l.exits.Any(e=>e.repairRequired||e.repaired||e.range<1||e.range>4||e.duration<.1f||e.duration>30)||!l.exits.Select(e=>e.id).SequenceEqual(new[]{"c1:exit-entry","c1:exit-hall"}))Bad();
  foreach(var p in l.points.Select(p=>p.position).Concat(l.encounters.Select(e=>e.home)).Concat(l.exits.Select(e=>e.position)).Append(l.entry))if(!CombatAim.Finite(p)||!l.WorldBounds.Contains(p))Bad();
  if(l.routes.Where((r,i)=>r.from!="c1:p"+i||r.to!="c1:p"+(i+1)).Any()||l.encounters.Any(e=>e.type<0||e.type>3||e.boss!=ForestBossKind.None||!l.points.Any(p=>p.id==e.poi)))Bad();
 }
 public static void ValidateCheckpoint(CombatCheckpoint c){
  if(!Is(c.forest))return;Validate(c.forest);var expected=Events();
  if(c.events==null||c.events.Length!=expected.Length||expected.Any(e=>!c.events.Any(s=>s.entityId==e.entityId&&s.kind==e.kind&&s.position==e.position)))Bad();
  if(Used(c.events,"c1:door")&&!Used(c.events,"c1:lever")||Used(c.events,"c1:hidden")&&!Used(c.events,"c1:archive"))Bad();
 }
 static void Bad(){throw new System.IO.InvalidDataException("C1遗迹版本、身份或交互快照不合法");}
}
