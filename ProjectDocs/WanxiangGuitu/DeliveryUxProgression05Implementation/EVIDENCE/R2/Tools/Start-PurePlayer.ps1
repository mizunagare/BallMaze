param(
    [Parameter(Mandatory=$true)][ValidateSet('NoDefine','Release')][string]$Kind,
    [Parameter(Mandatory=$true)][ValidateSet('BOOT','RESTART')][string]$Phase,
    [Parameter(Mandatory=$true)][string]$Attempt,
    [switch]$Seed
)
$ErrorActionPreference='Stop'
$repo='I:\unity\WanxiangGuitu'
$delivery=Join-Path $repo 'ProjectDocs\WanxiangGuitu\DeliveryUxProgression05Implementation'
$evidence=Join-Path $delivery 'EVIDENCE\R2'
$runId="UX05-R2-CLOSURE-$($Kind.ToUpper())-$Phase-$Attempt"
$runDir=Join-Path $evidence $runId
if(Test-Path -LiteralPath $runDir){throw 'Run directory already exists; never overwrite'}
New-Item -ItemType Directory -Path $runDir | Out-Null
$storage=Join-Path $evidence ($Kind.ToLower()+'-storage')
if($Kind -eq 'NoDefine'){$build='Builds\ux05-validation-01\Project\Builds\WanxiangGuitu.AcceptanceNoDefine';$buildId='UX05-R2-NoDefine-A02'}
else{$build='Builds\ux05-validation-01\ReleaseValidationR2A02\Release';$buildId='UX05-R2-Release-A02'}
$exe=Join-Path $repo ($build+'\WanxiangGuitu.exe')
$dll=Join-Path $repo ($build+'\WanxiangGuitu_Data\Managed\Assembly-CSharp.dll')
function Snapshot($name){
    $items=@(Get-ChildItem -LiteralPath $storage -Recurse -File | Where-Object Extension -ne '.lock' | ForEach-Object {
        [ordered]@{path=$_.FullName.Substring($storage.Length+1);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash;lastWriteTimeUtc=$_.LastWriteTimeUtc.ToString('o')}
    })
    ConvertTo-Json -InputObject $items -Depth 6 | Set-Content -LiteralPath (Join-Path $runDir $name) -Encoding utf8
}
Snapshot 'storage.before.json'
Copy-Item -LiteralPath (Join-Path $storage 'WanxiangGuitu\ForestRuins-v10\save.json') -Destination (Join-Path $runDir 'save.before.json')
$argsList=@('-wanxiang-storage-root',('"'+$storage+'"'),'-logFile',('"'+(Join-Path $runDir 'Player.log')+'"'),'-screen-fullscreen','0','-screen-width','1280','-screen-height','720')
$manifest=[ordered]@{runId=$runId;kind=$Kind;phase=$Phase;buildId=$buildId;exe=$exe;exeSha256=(Get-FileHash -LiteralPath $exe).Hash;productDll=$dll;productDllSha256=(Get-FileHash -LiteralPath $dll).Hash;driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash;driverSource=$PSCommandPath;driver='native @oai/sky input; no injected assembly';isolatedStorageRoot=$storage;arguments=$argsList;startedUtc=[DateTime]::UtcNow.ToString('o')}
$player=Start-Process -FilePath $exe -ArgumentList $argsList -WorkingDirectory (Split-Path $exe) -WindowStyle Normal -PassThru
$nativeHandle=$player.Handle
$manifest.pid=$player.Id
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $runDir 'run-manifest.json') -Encoding utf8
$player.WaitForExit()
$exitReceipt=[ordered]@{pid=$player.Id;exitCode=$player.ExitCode;endedUtc=[DateTime]::UtcNow.ToString('o');source='native process handle held before exit; WaitForExit'}
$exitReceipt | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runDir 'host-exit.json') -Encoding utf8
Copy-Item -LiteralPath (Join-Path $storage 'WanxiangGuitu\ForestRuins-v10\save.json') -Destination (Join-Path $runDir 'save.after.json')
Snapshot 'storage.after.json'
