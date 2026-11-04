$ErrorActionPreference='Stop';$root='I:/WGCombat/CP06B-1104-A';$project="$root/Project";$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1'
foreach($case in @(@('BossEditor1','NWEditor.RunBoss','BossData1'),@('MigrationEditor1','NWMigration.V1V6','MigrationData1'),@('MigrationEditor7','NWMigration.V7','MigrationData7'),@('MigrationEditor8','NWMigration.V8','MigrationData8'))){
 & $entry -Project $project -Output "$root/$($case[0])" -Method $case[1] -StorageRoot "$root/$($case[2])" -NonBatch
 @{name=$case[0];method=$case[1];storage=$case[2];actualExit=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/extra-editor-batch.jsonl"
}
