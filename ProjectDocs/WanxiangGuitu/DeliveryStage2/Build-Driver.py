"""Generate a transparent test-only variant of the existing B07 normal AI driver.
No product edits. Exact anchors fail closed; base and output hashes are recorded.
"""
from pathlib import Path
import hashlib
import json

b = Path(__file__).resolve().parent
base = b.parent / 'DeliveryB07/Tests/WGNormalAICheck.cs.txt'
s = base.read_text(encoding='utf-8-sig')
edits = []

def replace(old, new, count=1):
    global s
    if s.count(old) != count:
        raise ValueError('Driver anchor changed: ' + old[:90])
    s = s.replace(old, new)
    edits.append(dict(anchor=old[:100], occurrences=count))

replace('Environment.GetEnvironmentVariable("WG_B4_STRATEGY")??"Land"', 'Stage2Experiment.Config.strategy')
replace('ValidateLaunch(Environment.GetCommandLineArgs(),Root);', 'ValidateLaunch(Environment.GetCommandLineArgs(),Root);Stage2Experiment.Validate(Root);')
start=s.index('var path=new NavMeshPath();Need(')
end=s.index(';var next=path.corners',start)
replace(s[start:end], 'var path=region.NavigationPath(s.hero.transform.position,goal,"stage2-walk:"+goal.ToString("F3"),Strategy=="Bypass");Need(path.reachable&&path.status==NavMeshPathStatus.PathComplete,"normal walk no path "+goal)')
replace('if(s.hero.Health.Current<65)s.hero.Inventory.UseHealthPotion();', 'if(s.hero.Health.Current<65&&s.hero.Inventory.UseHealthPotion())Stage2Experiment.Potion();')
old='if(s.hero.GetComponent<AdventureLoadout>().Weapon!=GearType.Bow){combat.SwitchWeapon();return true;}'
new='''var chosen=s.hero.GetComponent<AdventureLoadout>().Weapon;Need(chosen==(GearType)Stage2Experiment.Config.weapon,"weapon coverage silently changed");float range=chosen==GearType.Sword?2.0f:chosen==GearType.Spear?3.1f:10f;if(Vector3.Distance(enemy.transform.position,s.hero.transform.position)>range){Walk(enemy.transform.position,range);return true;}'''
replace(old, new)
replace('if(Vector3.Distance(enemy.transform.position,s.hero.transform.position)<3){', 'if((int)s.hero.GetComponent<AdventureLoadout>().Weapon>=2&&Vector3.Distance(enemy.transform.position,s.hero.transform.position)<3){')
replace('if(continuing){expected=', 'Stage2Experiment.Attach(s,Root,continuing);if(continuing){expected=')
replace('Mark("ALL_PASS strategy="+Strategy+" second forest new-process continuation");', 'Mark("ALL_PASS strategy="+Strategy+" second forest new-process continuation");Stage2Experiment.Complete(s);')
start=s.index('   s.Camp.Materials[(int)MaterialKind.Stone]')
end=s.index('phase=1;return;',start)+len('phase=1;return;')
replace(s[start:end], '''   s.Camp.Materials[(int)MaterialKind.Stone]=1;s.Camp.Materials[(int)MaterialKind.Ore]=2;
   var gear=s.hero.GetComponent<AdventureLoadout>();Stage2Builds.Common(s.hero);Stage2Builds.Apply(s.hero,Stage2Experiment.Config.build,(GearType)Stage2Experiment.Config.weapon);
   s.hero.Inventory.Add(MaterialKind.Stone,2);s.hero.Inventory.Add(MaterialKind.Ore,2);s.hero.Inventory.Add(MaterialKind.MonsterHide,5);s.hero.Inventory.Add(MaterialKind.CrystalShard,5);Need(Stage2Experiment.Cost("prepare-five-potions",()=>s.hero.Inventory.CraftPotions(5)),"real carried potions");
   Need(CraftingTargets.Select(s.hero,(GearType)Stage2Experiment.Config.target,GearQuality.White)&&s.Flow.SelectExpeditionGoal(Strategy=="Treasure"?ExpeditionGoal.Treasure:Strategy=="Land"||Strategy=="Lake"?ExpeditionGoal.Challenge:ExpeditionGoal.Gather),"real build growth target");
   AdventureRandom.SetNextSeedForValidation(Stage2Experiment.Config.seed);Need(s.Flow.Depart(AdventureMode.ForestExploration),"actual forest departure");Need(s.Flow.ActiveRun.seed==Stage2Experiment.Config.seed,"requested seed not applied");firstRun=s.Flow.ActiveRun.runId;initialEarned=(int[])s.Flow.ActiveRun.earnedRemaining.Clone();Stage2Experiment.Depart(s);
   File.WriteAllText(Root+"/metadata.txt",JsonUtility.ToJson(Stage2Experiment.Config,true)+"\\nAll four actual white weapons available, identical initial owned gear/material set; only main/board/containers vary. Five actually crafted potions. No stat override/AI freeze/teleport after departure; no OS native/human claim.\\n");phase=1;return;''')
replace('if(s.hero.Progression.IsChoosing)s.hero.Progression.SelectChoice(0);', 'if(s.hero.Progression.IsChoosing){Stage2Experiment.Record("before-skill-choice");Need(s.hero.Progression.SelectChoice(0),"actual skill choice rejected");Stage2Experiment.Record("after-skill-choice");}')
replace('Need(!s.hero.Health.Dead,"normal hero died");', 'Stage2Experiment.Observe(s,phase);Need(!s.hero.Health.Dead,"normal hero died");')
replace('if(Walk(node.transform.position,3.8f))', 'if(Walk(node.transform.position,(int)s.hero.GetComponent<AdventureLoadout>().Weapon>=2?3.8f:s.hero.GetComponent<AdventureLoadout>().Weapon==GearType.Spear?2.8f:2.0f))')
replace('loot.PickUp(s.hero.Inventory)', 'Stage2Experiment.Pickup(loot,s.hero.Inventory)', count=2)
replace('drops[0].PickUp(s.hero.Inventory)', 'Stage2Experiment.Pickup(drops[0],s.hero.Inventory)')
replace('Need(s.hero.GetComponent<AdventureLoadout>().Craft(GearType.Bow,GearQuality.White),"craft with actual gathered wood before boss");Mark("ACTUAL_GATHER_CRAFT_PRE_BOSS");phase=80;', '''if(Strategy=="Land"||Strategy=="Lake"){Need(Stage2Experiment.Cost("gathered-pre-boss-weapon",()=>s.hero.GetComponent<AdventureLoadout>().Craft((GearType)Stage2Experiment.Config.weapon,GearQuality.White)),"gathered weapon manufacture");Mark("ACTUAL_GATHER_CRAFT_PRE_BOSS");phase=80;}else phase=Strategy=="Gather"?20:10;''')
replace('Need(s.Flow.RepairExit(exitId),"real ferry repair "+s.Flow.RepairReason(exitId));', 'Need(Stage2Experiment.Cost("ferry",()=>s.Flow.RepairExit(exitId)),"real ferry repair "+s.Flow.RepairReason(exitId));')
replace('File.WriteAllText(Root+"/b4-first-settlement.json",', 'Stage2Experiment.Pending(s);File.WriteAllText(Root+"/b4-first-settlement.json",')
old='Need(s.Camp.TransferMaterial(MaterialKind.Wood,2,false)&&s.Camp.TransferMaterial(MaterialKind.Stone,1,false)&&s.Camp.TransferMaterial(MaterialKind.Ore,2,false)&&s.hero.GetComponent<AdventureLoadout>().Craft(GearType.Sword,GearQuality.White),"withdraw actual yield manufacture");'
new='''Need(s.Camp.TransferMaterial(MaterialKind.Wood,2,false)&&s.Camp.TransferMaterial(MaterialKind.Stone,1,false)&&s.Camp.TransferMaterial(MaterialKind.Ore,2,false),"withdraw real deposited materials");var g=s.hero.GetComponent<AdventureLoadout>();var ids=g.items.Select(i=>i.id).ToArray();float attack=s.hero.AttackPower,defense=s.hero.Defense;Need(Stage2Experiment.Cost("camp-build-growth",()=>g.Craft((GearType)Stage2Experiment.Config.target,GearQuality.White)),"actual build-growth manufacture");var made=g.items.Single(i=>!ids.Contains(i.id));Stage2Builds.Board(g,made);Stage2Experiment.Growth(s,attack,defense,made.id);'''
replace(old,new)
replace('Need(s.Flow.CommitSettlement(),"commit settlement");', 'Stage2Experiment.Record("before-commit");Need(s.Flow.CommitSettlement(),"commit settlement");')
replace('Need(committed==JsonUtility.ToJson(s.Flow.Profile),"duplicate settlement award");', 'Need(committed==JsonUtility.ToJson(s.Flow.Profile),"duplicate settlement award");Stage2Experiment.Record("committed-after-duplicate-check");')
replace('Need(s.Flow.AcknowledgeSettlement(),"ack settlement");', 'Need(s.Flow.AcknowledgeSettlement(),"ack settlement");Stage2Experiment.Record("acknowledged");Stage2Experiment.Record("before-withdraw-materials");')
replace('"withdraw real deposited materials");var g=', '"withdraw real deposited materials");Stage2Experiment.Record("after-withdraw-materials");var g=')
replace('static void Finish(int stage){StopInput();', 'static void Finish(int stage){Stage2Experiment.Record("checkpoint:"+stage);StopInput();')
replace('}catch(Exception e){Debug.LogException(e);if(kb!=null)', '}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;try{Stage2Experiment.Failure(e);}catch(Exception reportError){Debug.LogException(reportError);}if(kb!=null)')
s='// GENERATED test-only B07 driver variant. Rebuild with DeliveryStage2/Build-Driver.py.\n'+s
output=b/'Tests/WGNormalAICheck.cs.source'
output.write_text(s,encoding='utf-8')
(b/'DRIVER_PROVENANCE.json').write_text(json.dumps(dict(base=base.relative_to(b.parent.parent.parent).as_posix(),baseSha256=hashlib.sha256(base.read_bytes()).hexdigest(),output='Tests/WGNormalAICheck.cs.source',outputSha256=hashlib.sha256(output.read_bytes()).hexdigest(),edits=edits),indent=2)+'\n',encoding='utf-8')
print('Generated explicit Stage2 variant; edits='+str(len(edits)))
