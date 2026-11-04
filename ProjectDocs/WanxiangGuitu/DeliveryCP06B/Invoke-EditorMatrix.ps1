param([string]$Root='I:/WGCombat/CP06B-1104-A')
$ErrorActionPreference='Stop';$project="$Root/Project"
function Run([string]$name,[string]$method,[string]$storage=''){
 if(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine-like"*$project*"}){throw 'Owned project occupied; no processes stopped'}
 $snapshot="$Root/Executed/$name";New-Item -ItemType Directory $snapshot -Force|Out-Null
 foreach($file in Get-ChildItem "$project/Assets" -File -Filter '*Probe.cs'){Copy-Item $file.FullName $snapshot};foreach($file in Get-ChildItem "$project/Assets" -File -Filter 'NW*.cs'){Copy-Item $file.FullName $snapshot}
 foreach($file in Get-ChildItem "$project/Assets/CombatPrototype/Editor/B06LocalChecks" -File -Filter '*Editor.cs'){Copy-Item $file.FullName $snapshot}
 $args=@{Project=$project;Output="$Root/$name";Method=$method;NonBatch=$true};if($storage){$args.StorageRoot="$Root/$storage"}
 & 'H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1' @args
 $code=$LASTEXITCODE;@{name=$name;method=$method;storage=$storage;actualExit=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$Root/editor-batch.jsonl";Write-Output "$name actualExit=$code"
}
Run ResumeEditor2 NWEditor.RunStorage ResumeEditorData2
Run PerformanceEditor1 NWEditor.RunPerformance
Run FinalEditorTwin1 NWEditor.Run
Run FinalEditorHeavy1 NWEditor.RunHeavy
Run FinalEditorScythe1 NWEditor.RunScythe
Run FinalBoundaryEditor2 NWEditor.RunBoundary
Run LegacyExpandedEditor1 CP6Editor.Run
Run LegacyExtraEditor1 CP6Editor.Extra
Run LegacyTrainingEditor1 CPCEditor.Run
Run LegacyFormalEditor1 CPCEditor.Formal LegacyFormalData1
