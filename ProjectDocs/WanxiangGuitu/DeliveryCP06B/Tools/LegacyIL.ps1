param([string]$Baseline='I:/WGCombat/CP06A-1104-A/PureBuild/Release',[Parameter(Mandatory)][string]$Current,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop';Add-Type -Path 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Managed/Unity.Cecil.dll'
function ReadAssembly($folder){[Mono.Cecil.AssemblyDefinition]::ReadAssembly((Join-Path $folder 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'))}
function TypeIL($type){
 $lines=[Collections.Generic.List[string]]::new()
 foreach($m in $type.Methods){$lines.Add($m.FullName);if($m.HasBody){foreach($v in $m.Body.Variables){$lines.Add('local '+$v.VariableType.FullName)};foreach($i in $m.Body.Instructions){$lines.Add($i.ToString())}}}
 foreach($n in $type.NestedTypes){$lines.Add((TypeIL $n))};$lines -join "`n"
}

$a=ReadAssembly $Baseline;$b=ReadAssembly $Current;$rows=[Collections.Generic.List[object]]::new()
try{
 foreach($name in 'CombatAim','TargetAssist','OrbitCamera','CameraActorFade','AdventureRandom','AdventureProjectile','TrainingLootContext','CP05Training','WeaponSkillCatalog','WeaponSkillDefinition','SkillImpactField','SkillPiercingProjectile','WeaponHit'){
 $x=$a.MainModule.Types|Where-Object FullName -eq $name;$y=$b.MainModule.Types|Where-Object FullName -eq $name;$same=$null-ne$x-and$null-ne$y-and(TypeIL $x)-ceq(TypeIL $y);$rows.Add(@{name=$name;scope='entire type IL';status=if($same){'PASS'}else{'FAIL'}})
 }
 foreach($pair in @(@('AdventureCombat','Release'),@('AdventureCombat','Melee'),@('AdventureCombat','Fire'),@('AdventureCombat','SolveRanged'),@('CombatEnemy','DropLootCore'),@('CombatEnemy','ReleaseAttack'),@('CombatEnemy','PrepareAttack'),@('AdventureItems','Roll'),@('AdventureItems','RollTraining'),@('AdventureItems','NewContainer'))){
 $x=$a.MainModule.Types|Where-Object FullName -eq $pair[0];$y=$b.MainModule.Types|Where-Object FullName -eq $pair[0];$xm=@($x.Methods|Where-Object Name -eq $pair[1]);$ym=@($y.Methods|Where-Object Name -eq $pair[1]);$xil=@($xm|ForEach-Object {($_.Body.Instructions|ForEach-Object ToString)-join "`n"})-join "`n";$yil=@($ym|ForEach-Object {($_.Body.Instructions|ForEach-Object ToString)-join "`n"})-join "`n";$same=$xm.Count-gt 0-and$xm.Count-eq$ym.Count-and$xil-ceq$yil;$rows.Add(@{name=$pair-join'.';methods=$xm.Count;scope='exact legacy method IL';status=if($same){'PASS'}else{'FAIL'}})
 }
 $result=@{status=if(@($rows|Where-Object status -eq FAIL).Count){'FAIL'}else{'PASS'};baseline=$Baseline;current=$Current;rows=@($rows);scope='Exact baseline IL, no removed instructions or numeric tolerance'};$result|ConvertTo-Json -Depth 8|Set-Content $Output -Encoding UTF8;Write-Output "$($result.status): $($rows.Count) legacy IL checks"
 if($result.status-ne'PASS'){exit 1}
}finally{$a.Dispose();$b.Dispose()}
