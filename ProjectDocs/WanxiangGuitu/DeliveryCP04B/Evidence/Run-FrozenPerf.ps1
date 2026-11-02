$ErrorActionPreference='Stop';$project='I:/WGCombat/CP04B-1102-A/P/Project';$base='I:/WGCombat/CP04B-1102-A';$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1'
Copy-Item "$base/CombatAim.before.cs.txt" "$project/Assets/CombatPrototype/CombatAim.cs"
& $entry -Project $project -Output "$base/BeforePerfFrozen" -Method CP04BEditor.Perf -NonBatch
Copy-Item "$project/Assets/CombatPrototype/CombatAim.cs" "$base/BeforePerfFrozen/CombatAim.executed.cs.txt"
Copy-Item H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/CombatAim.cs "$project/Assets/CombatPrototype/CombatAim.cs"
foreach($pair in @(@('AfterPerfFrozen','CP04BEditor.Perf'),@('AcceptanceBuildShippingInput','CP04BBuild.Acceptance'),@('PureBuildShippingInput','CP04BBuild.Pure'))){
 & $entry -Project $project -Output "$base/$($pair[0])" -Method $pair[1] -NonBatch
 @{suite=$pair[0];exitCode=$LASTEXITCODE}|ConvertTo-Json|Set-Content "$base/$($pair[0])/wrapper-exit.json"
 Copy-Item "$project/Assets/CombatPrototype/CombatAim.cs" "$base/$($pair[0])/CombatAim.executed.cs.txt"
 foreach($f in Get-ChildItem "$project/Assets/CP04BValidation" -Filter '*.cs'){Copy-Item -LiteralPath $f.FullName -Destination "$base/$($pair[0])/$($f.Name).executed.txt"}
 if(Select-String -Path "$base/$($pair[0])/Unity.log" -Pattern 'error CS[0-9]+' -Quiet){throw 'Compile failure preserved'}
}
