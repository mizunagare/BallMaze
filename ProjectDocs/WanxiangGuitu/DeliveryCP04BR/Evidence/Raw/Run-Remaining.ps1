$ErrorActionPreference='Stop';$r='I:/WGCombat/CP04BR-1102-A';$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1'
foreach($v in 'Fixed','Baseline'){
 & $entry -Project "$r/$v/Project" -Output "$r/${v}Scoped" -Method BRScopedEditor.Run -NonBatch
 if(Select-String "$r/${v}Scoped/Unity.log" -Pattern 'error CS' -Quiet){throw 'compiler error'}
 & $entry -Project "$r/$v/Project" -Output "$r/${v}AcceptanceBuild" -Method BRBuildAudit.Acceptance -NonBatch
 if(Select-String "$r/${v}AcceptanceBuild/Unity.log" -Pattern 'error CS' -Quiet){throw 'compiler error'}
}
