param(
    [Parameter(Mandatory)][string]$Exe,
    [Parameter(Mandatory)][string]$StorageRoot,
    [Parameter(Mandatory)][string]$EvidenceRoot,
    [Parameter(Mandatory)][string]$RunId,
    [Parameter(Mandatory)][string]$BuildId,
    [ValidateSet("migrate","resume","legacy","objective-new","objective-readback","objective-ui","legacy-pending","inspect-reject","migrate-cut","objective-repeat","objective-repeat-readback","inventory-gates","objective-capacity","objective-capacity-readback","objective-pending-stop","objective-pending-resume","objective-abandon-after-goal","r1-migrate-before-archive","r1-migrate-before-page-write","r1-migrate-before-candidate-write","r1-migrate-bad-candidate","r1-migrate-before-replace","r1-migrate-lost-receipt","r1-migrate-after-replace","r1-migrate-after-page-write","r1-save-readback","r1-save-stale","r1-ui-empty","r1-ui-unknown","r1-ui-ugui","r1-ui-imgui","r1-rules","r1-ui-imgui-empty","r1-ui-imgui-unknown")][string]$Mode,
    [ValidateRange(10,1800)][int]$TimeoutSeconds=115
)
$ErrorActionPreference='Stop'
$Exe=(Resolve-Path -LiteralPath $Exe).Path
$StorageRoot=(Resolve-Path -LiteralPath $StorageRoot).Path
$EvidenceRoot=(Resolve-Path -LiteralPath $EvidenceRoot).Path
if ($RunId -notmatch '^[A-Za-z0-9-]+$' -or
    !$StorageRoot.StartsWith($EvidenceRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Use a unique run identifier and an evidence-owned isolated storage root.'
}
for ($path=$StorageRoot; $path; $path=[IO.Path]::GetDirectoryName($path)) {
    if ((Get-Item -LiteralPath $path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse point rejected'}
}
$run=Join-Path $EvidenceRoot $RunId
if (Test-Path -LiteralPath $run) {throw 'Do not reuse run evidence'}
New-Item -ItemType Directory -Path $run | Out-Null
function Save-Fingerprints($name) {
    $files=@(Get-ChildItem -LiteralPath $StorageRoot -Recurse -File | Sort-Object FullName | ForEach-Object {
        @{path=$_.FullName.Substring($StorageRoot.Length+1);bytes=$_.Length;sha256=if($_.Extension -eq ".lock"){"lock-object"}else{(Get-FileHash -LiteralPath $_.FullName).Hash}}
    })
    ConvertTo-Json -InputObject $files | Set-Content -LiteralPath (Join-Path $run $name) -Encoding utf8
}
Save-Fingerprints 'before.json'
$dll=Join-Path (Split-Path -Parent $Exe) (([IO.Path]::GetFileNameWithoutExtension($Exe))+'_Data/Managed/Assembly-CSharp.dll')
$launchArgs=@(
    '-wanxiang-storage-root',('"' + $StorageRoot + '"'), '-wanxiang-entry-evidence',
    '-screen-fullscreen','0','-screen-width','1280','-screen-height','720',
    '-logFile',('"' + (Join-Path $run 'player.log') + '"')
)
if ($Mode) {$launchArgs+=@("-ux05-entry-probe",$Mode,$RunId)}
$process=Start-Process -FilePath $Exe -ArgumentList $launchArgs -WindowStyle Normal -PassThru
@{
    runId=$RunId; buildId=$BuildId; pid=$process.Id; startedUtc=[DateTime]::UtcNow.ToString('o')
    exe=$Exe; exeSha256=(Get-FileHash -LiteralPath $Exe).Hash
    productDll=$dll; productDllSha256=(Get-FileHash -LiteralPath $dll).Hash
    isolatedStorageRoot=$StorageRoot; driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $run 'manifest.json') -Encoding utf8
$timedOut=$false
$cut=$false
$deadline=[DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
$events=Join-Path $StorageRoot ("probe-results/"+$RunId+"/events.jsonl")
while (!$process.WaitForExit(250)) {
    if (($Mode -eq 'migrate-cut' -or $Mode -like 'r1-migrate-*') -and (Test-Path -LiteralPath $events) -and
        (Select-String -LiteralPath $events -Pattern 'migration-process-cut' -Quiet)) {
        $cut=$true
        $process.Kill()
        $process.WaitForExit()
        break
    }
    if ([DateTime]::UtcNow -ge $deadline) {
        $timedOut=$true
        $process.Kill()
        $process.WaitForExit()
        break
    }
}
Save-Fingerprints 'after.json'
$probeRoot=Join-Path $StorageRoot ("probe-results/"+$RunId)
if (Test-Path -LiteralPath $probeRoot) {Copy-Item -LiteralPath $probeRoot -Recurse -Destination (Join-Path $run "probe")}
@{runId=$RunId;pid=$process.Id;exitCode=$process.ExitCode;status='OBSERVED';interruptedAtCut=$cut;timedOut=$timedOut;finishedUtc=[DateTime]::UtcNow.ToString('o')} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $run 'result.json') -Encoding utf8











