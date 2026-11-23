param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$EvidenceRoot,[string]$Attempt="A02",[string]$BuildId="UX05-Acceptance-04-Mono",[string[]]$Scenario=@())
$ErrorActionPreference='Stop'
$Exe=(Resolve-Path -LiteralPath $Exe).Path
$EvidenceRoot=(Resolve-Path -LiteralPath $EvidenceRoot).Path
$dll=Join-Path (Split-Path -Parent $Exe) 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
$dllSha=(Get-FileHash -LiteralPath $dll).Hash
$exeSha=(Get-FileHash -LiteralPath $Exe).Hash
$cases=@(
 @('sword-triple','Sword','1','0','7','damage'),
 @('sword-circle','Sword','2','0','10','damage'),
 @('spear-charge','Spear','1','0.60','8','damage'),
 @('spear-sweep','Spear','2','0','9','damage'),
 @('staff-field','Staff','1','0','9','damage'),
 @('staff-echo','Staff','2','0','9','damage'),
 @('bow-burst','Bow','1','0','9','damage'),
 @('bow-pierce','Bow','2','0.70','10','damage'),
 @('twin-volley','TwinBlades','0','0','7','damage'),
 @('gs-cleave','Greatsword','0','0','9','damage'),
 @('gs-wave','Greatsword','1','0','10','damage'),
 @('sc-reap','Scythe','0','0','8','damage'),
 @('twin-counter','TwinBlades','1','0','0','twin_counter'),
 @('sc-pull','Scythe','1','0','0','soul_pull')
)
foreach ($case in $cases) {
    if($Scenario.Count -gt 0 -and $case[0] -notin $Scenario){continue}
    $runId='UX05-20261119-UX03-'+$case[0]+'-'+$Attempt
    $run=Join-Path $EvidenceRoot $runId
    if (Test-Path -LiteralPath $run){throw "Run already exists: $runId"}
    $root=Join-Path $run 'root'
    New-Item -ItemType Directory $root | Out-Null
    '[]' | Set-Content -LiteralPath (Join-Path $run 'before.json')
    $argsRun=@(
       '--acceptance', '-wanxiang-storage-root', ('"' + $root + '"'), '--data-root', ('"' + $root + '"'),
       '--scenario-id', $case[0], '--run-id', $runId, '--build-sha', $dllSha,
       '--build-id',$BuildId,'--expected-exe-sha',$exeSha,'--expected-dll-sha',$dllSha,
       '--weapon',$case[1],'--slot',$case[2],'--charge',$case[3],'--expected-cooldown',$case[4],'--mode',$case[5],
       '-screen-fullscreen','0','-screen-width','1280','-screen-height','720',
       '-logFile',('"' + (Join-Path $run 'player.log') + '"')
    )
    $process=Start-Process -FilePath $Exe -ArgumentList $argsRun -WindowStyle Normal -PassThru
    @{
      runId=$runId; buildId=$BuildId; exeSha256=$exeSha; productDllSha256=$dllSha
      pid=$process.Id; isolatedStorageRoot=$root; driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash
      startedUtc=[DateTime]::UtcNow.ToString('o')
    }|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $run 'manifest.json') -Encoding utf8
    $timeout=!$process.WaitForExit(80000)
    if($timeout){$process.Kill();$process.WaitForExit()}
    $files=@(Get-ChildItem $root -Recurse -File | Sort-Object FullName | ForEach-Object{
      @{path=$_.FullName.Substring($root.Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName).Hash;bytes=$_.Length}
    })
    ConvertTo-Json -InputObject $files | Set-Content -LiteralPath (Join-Path $run 'after.json') -Encoding utf8
    @{runId=$runId;pid=$process.Id;exitCode=$process.ExitCode;timedOut=$timeout;finishedUtc=[DateTime]::UtcNow.ToString('o')} |
      ConvertTo-Json | Set-Content -LiteralPath (Join-Path $run 'result.json') -Encoding utf8
    "$runId exit=$($process.ExitCode) timeout=$timeout"
}


