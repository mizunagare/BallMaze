param([Parameter(Mandatory=$true)][string]$TestBuild,[Parameter(Mandatory=$true)][string]$ReleaseBuild,[Parameter(Mandatory=$true)][string]$Output)
$ErrorActionPreference='Stop'
Add-Type -Path 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Managed/Unity.Cecil.dll'
function ReadAssembly($folder){[Mono.Cecil.AssemblyDefinition]::ReadAssembly((Join-Path $folder 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'))}
function TypeIL($type){
 $lines=[Collections.Generic.List[string]]::new()
 foreach($m in $type.Methods){$lines.Add($m.FullName);if($m.HasBody){foreach($v in $m.Body.Variables){$lines.Add('local '+$v.VariableType.FullName)};foreach($i in $m.Body.Instructions){$lines.Add($i.ToString())}}}
 foreach($n in $type.NestedTypes){$lines.Add((TypeIL $n))};$lines -join "`n"
}
$test=ReadAssembly $TestBuild;$release=ReadAssembly $ReleaseBuild
try {
 $names=@('OrbitCamera','CameraActorFade','TargetAssist','AdventureCombat','CP05Training','CombatAssistOptions','CombatAim','AdventureProjectile','TrainingLootContext','CombatEnemy','AdventureItems','AdventureRandom','WeaponSkillExpansion','WeaponSkillCatalog','WeaponSkillDefinition','SkillImpactField','SkillPiercingProjectile','WeaponSkillPanel','NewWeaponCombat','TwinBladeMotor','NewWeaponVisual','NewWeaponRegistry','NewWeaponDrop','GreatswordMotor','ScytheMotor','NewGroundShock','EnemyWeaponControl','NewWeaponDropRules','CatDropVisual','RuinsAssets','RuinsLayout','RuinsExploration','RuinsBossBrain','RuinsSpecialRewards','SpecialRewardReceipt','ForestRegionRuntime','AdventureFlow','CombatSaveSystem','AdventureValidation','WorldEventPoint')
 $checks=@(foreach($n in $names){$a=$test.MainModule.Types|Where-Object FullName -eq $n;$b=$release.MainModule.Types|Where-Object FullName -eq $n;[pscustomobject]@{type=$n;present=($null-ne$a-and$null-ne$b);identicalIL=($null-ne$a-and$null-ne$b-and(TypeIL $a)-ceq(TypeIL $b))}})
 $forbidden=@($release.MainModule.Types|Where-Object {$_.FullName-match 'C1Probe|C1R1Cases|C1Metrics|NWStatsProbe|NWStatsEditor|NWUpgradeProbe|NWUpgradeEditor|NWNearProbe|NWNearEditor|NWChannel|NWBoss|NWCancel|NWProbe|NWHeavy|NWScythe|NWStorage|NWDrop|NWBoundary|NWPerformance|NWMetrics|NWEditor|CP6Probe|CP6Expanded|CP6Save|CP6Extra|CP6Editor|CPCProbe|CPCFormal|CPCEditor|CP05Probe|CP05Editor|CP05BRProbe|CP05BREditor|CP03Cases|CP04Cases|BR2|NativeProbe'}|ForEach-Object FullName)
 $nativeRefs=@(foreach($type in $release.MainModule.Types){foreach($method in $type.Methods){if($method.HasPInvokeInfo -and $method.PInvokeInfo.Module.Name -match "BR2AllocationNative|NativeProbe"){$method.FullName+" -> "+$method.PInvokeInfo.Module.Name}}})
 $editorRefs=@($release.MainModule.AssemblyReferences|Where-Object {$_.Name-match '^UnityEditor|MapMagic|Den.Tools'}|ForEach-Object Name)
 $r=[ordered]@{scope='Assembly-CSharp product type IL comparison and pure driver exclusion; package-owned test DLL names not treated as product drivers';checks=$checks;forbiddenTypes=$forbidden;nativeTestReferences=$nativeRefs;editorReferences=$editorRefs;testSHA256=(Get-FileHash (Join-Path $TestBuild 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll')).Hash;releaseSHA256=(Get-FileHash (Join-Path $ReleaseBuild 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll')).Hash;status=if(@($checks|Where-Object {!$_.identicalIL}).Count-or$forbidden.Count-or$editorRefs.Count-or$nativeRefs.Count){'FAIL'}else{'PASS'}}
 $r|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $Output -Encoding UTF8
 $r|ConvertTo-Json -Depth 8
 if($r.status-ne'PASS'){throw 'Assembly verification failed'}
}finally{$test.Dispose();$release.Dispose()}
