param(
    [Parameter(Mandatory)][string]$RunId,
    [Parameter(Mandatory)][string]$StorageRoot,
    [Parameter(Mandatory)][string]$PlayerDirectory,
    [Parameter(Mandatory)][string]$EvidenceRoot,
    [switch]$Monitor,
    [string]$FixtureDirectory
)
$ErrorActionPreference='Stop'
$StorageRoot=[IO.Path]::GetFullPath($StorageRoot)
$EvidenceRoot=(Resolve-Path -LiteralPath $EvidenceRoot).Path
if(!$StorageRoot.StartsWith($EvidenceRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){
    throw 'Run storage must be a new child of this batch evidence root.'
}
if(Test-Path -LiteralPath $StorageRoot){throw 'Refusing to overwrite a previous run.'}
New-Item -ItemType Directory -Path (Join-Path $StorageRoot 'WanxiangGuitu')|Out-Null
if($FixtureDirectory){
    Copy-Item -LiteralPath (Resolve-Path -LiteralPath $FixtureDirectory).Path -Destination (Join-Path $StorageRoot 'WanxiangGuitu') -Recurse
}
function Fingerprints($out){
    $records=@(Get-ChildItem -LiteralPath $StorageRoot -Recurse -File|Where-Object Extension -ne '.lock'|ForEach-Object{
        @{path=[IO.Path]::GetRelativePath($StorageRoot,$_.FullName);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}
    })
    ConvertTo-Json -InputObject $records|Set-Content -LiteralPath (Join-Path $StorageRoot $out) -Encoding utf8
}
Fingerprints 'before.json'
$exe=Join-Path $PlayerDirectory 'WanxiangGuitu.exe'
$dll=Join-Path $PlayerDirectory 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
$driver=Join-Path $PlayerDirectory 'WanxiangGuitu_Data/Managed/CavernValidationDriver.dll'
$argsForPlayer=@('-wanxiang-storage-root',('"'+$StorageRoot+'"'),'-ux05-r2',$RunId,'-wanxiang-entry-evidence',
 '-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',('"'+(Join-Path $StorageRoot 'player.log')+'"'))
$process=Start-Process -FilePath $exe -ArgumentList $argsForPlayer -WindowStyle Normal -PassThru
@{runId=$RunId;pid=$process.Id;exe=$exe;exeSha256=(Get-FileHash -LiteralPath $exe).Hash;
 productDll=$dll;productDllSha256=(Get-FileHash -LiteralPath $dll).Hash;driver=$driver;driverSha256=(Get-FileHash -LiteralPath $driver).Hash;
 arguments=$argsForPlayer;storageRoot=$StorageRoot;startedUtc=[DateTime]::UtcNow.ToString('o')}|
 ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $StorageRoot 'manifest.json') -Encoding utf8
$process.Id

if($Monitor){
    $completed=$process.WaitForExit(900000)
    if(!$completed){$process.Kill();$process.WaitForExit()}
    Fingerprints 'after.json'
    @{pid=$process.Id;exitCode=$process.ExitCode;timedOut=(!$completed);finishedUtc=[DateTime]::UtcNow.ToString('o')}|
       ConvertTo-Json|Set-Content -LiteralPath (Join-Path $StorageRoot 'process-exit.json') -Encoding utf8
}