param([ValidateSet('Editor','Player')][string]$Layer,[string]$Observation='ObservedFinal',[string]$Tag='Final')
$ErrorActionPreference='Stop'
$root='I:/WGCombat/C23-1106-A'
$cases=@(
 @{name='Store';mode='lake-store'},
 @{name='Resume';mode='lake-resume';seed="$root/${Layer}Store$Tag"},
 @{name='Warehouse';mode='warehouse';seed="$root/${Layer}Resume$Tag"},
 @{name='Repeat';mode='lake-repeat';seed="$root/${Layer}Warehouse$Tag"},
 @{name='Closed';mode='lake-closed'},
 @{name='ClosedResume';mode='lake-closed-resume';seed="$root/${Layer}Closed$Tag"},
 @{name='Inner';mode='lake-inner'},
 @{name='InnerResume';mode='lake-resume';seed="$root/${Layer}Inner$Tag"},
 @{name='Routes';mode='lake-routes'},
 @{name='Live';mode='lake-live'},
 @{name='Legacy21';mode='legacy-cavern';seed='I:/WGCombat/C22-1106-A/BaselineMining3'},
 @{name='Legacy22';mode='legacy-c22-resume';seed='I:/WGCombat/C22-1106-A/PlayerChamber3'},
 @{name='Forest';mode='old-forest-resume';seed='I:/WGCombat/C22-1106-A/PlayerForest3'},
 @{name='Ruins';mode='old-ruins-resume';seed='I:/WGCombat/C22-1106-A/PlayerRuins3'}
)
$pwsh=(Get-Command pwsh).Source
foreach($case in $cases){
 $out="$root/$Layer$($case.name)$Tag"
 if(Test-Path -LiteralPath $out){throw "Existing evidence: $out"}
 $argv=if($Layer-eq'Editor'){@('-NoProfile','-File',"$PSScriptRoot/Invoke-Editor.ps1",'-ValidationCopy','-NonBatch','-Method','CavernValidationEditor.Begin','-Seconds','600')}else{@('-NoProfile','-File',"$PSScriptRoot/Invoke-Player.ps1",'-Observation',$Observation)}
 $argv+=@('-Output',$out,'-Mode',$case.mode)
 if($case.seed){$argv+=@('-Seed',$case.seed)}
 & $pwsh @argv
 $code=$LASTEXITCODE
 @{layer=$Layer;mode=$case.mode;output=$out;exitCode=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/matrix-$Layer-$Tag.jsonl"
 if($code-ne0){throw "Preserved failing case: $out ($code). Inspect before continuing."}
}
