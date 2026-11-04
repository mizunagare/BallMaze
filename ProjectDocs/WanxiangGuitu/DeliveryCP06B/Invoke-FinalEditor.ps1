$ErrorActionPreference='Stop';$root='I:/WGCombat/CP06B-1104-A';$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1'
foreach($case in @(@('FinalTwin2','NWEditor.Run'),@('FinalHeavy2','NWEditor.RunHeavy'),@('FinalScythe2','NWEditor.RunScythe'),@('FinalBoundary3','NWEditor.RunBoundary'),@('FinalPerformance2','NWEditor.RunPerformance'),@('FinalLegacyExpanded2','CP6Editor.Run'),@('FinalLegacyFormal2','CPCEditor.Formal'))){
 $args=@{Project="$root/Project";Output="$root/$($case[0])";Method=$case[1];NonBatch=$true};if($case[0]-eq'FinalLegacyFormal2'){$args.StorageRoot="$root/LegacyFormalData2"}
 & $entry @args;@{name=$case[0];actualExit=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/final-editor-batch.jsonl"
}
& $entry -Project "$root/Project" -Output "$root/FinalTestBuild" -Method CP05Build.Run
@{name='FinalTestBuild';actualExit=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/final-editor-batch.jsonl"
