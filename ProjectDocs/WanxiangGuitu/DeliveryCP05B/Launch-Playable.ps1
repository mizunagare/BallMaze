param([ValidateSet('B1','B2','B3')][string]$Stage='B3')
$ErrorActionPreference='Stop'
# User-invoked visible launch only. Never used to claim native/human acceptance.
$root='I:/WGCombat/CP05B-1103-A'
$paths=@{B1='B1/Build4/Release';B2='B2/ReleaseBuild/Release';B3='B3/ReleaseBuild/Release'}
$build=Join-Path $root $paths[$Stage]
$manifest=Get-Content (Join-Path $PSScriptRoot "Evidence/$Stage/release-files.json") -Raw|ConvertFrom-Json
foreach($row in $manifest){$file=Join-Path $build $row.path;if(!(Test-Path -LiteralPath $file)-or(Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant()-ne$row.sha256){throw "Playable package mismatch: $($row.path)"}}
if(Get-Process WanxiangGuitu -ErrorAction SilentlyContinue){throw 'Existing Player; close it yourself before launching another'}
$save=Join-Path $root ('Manual-'+$Stage+'-'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Path $save|Out-Null
Write-Host "Synthetic isolated root: $save"
Start-Process -FilePath (Join-Path $build 'WanxiangGuitu.exe') -ArgumentList @('-cp05-training','-wanxiang-storage-root',$save,'-windowed','-screen-width','1280','-screen-height','720','-logFile',(Join-Path $save 'Player.log'))
