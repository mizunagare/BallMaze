$ErrorActionPreference='Stop';$project='I:/WGCombat/CP04B-1102-A/P/Project';$base='I:/WGCombat/CP04B-1102-A';$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1';$rows=@()
foreach($pair in @(@('AfterHistorical','CP03Editor.Run'),@('AfterWall','CP04BEditor.CameraWall'),@('AfterBoundary','CP04BEditor.Boundary'),@('AfterLifecycle','CP04BEditor.Lifecycle'),@('AfterDeath','CP04BEditor.Death'),@('Performance','CP04BEditor.Perf'),@('AcceptanceBuild','CP04BBuild.Acceptance'),@('PureBuild','CP04BBuild.Pure'))){
 & $entry -Project $project -Output "$base/$($pair[0])" -Method $pair[1] -NonBatch
 $code=$LASTEXITCODE;$rows+=@{name=$pair[0];exitCode=$code};$rows|ConvertTo-Json|Set-Content -Encoding utf8 "$base/editor-batch-progress.json"
 foreach($f in Get-ChildItem "$project/Assets/CP04BValidation" -Filter '*.cs'){Copy-Item -LiteralPath $f.FullName -Destination "$base/$($pair[0])/$($f.Name).executed.txt"}
 if(Select-String -Path "$base/$($pair[0])/Unity.log" -Pattern 'error CS[0-9]+' -Quiet){throw 'Compile failure; preserve attempt, skip dependent launches'}
}
