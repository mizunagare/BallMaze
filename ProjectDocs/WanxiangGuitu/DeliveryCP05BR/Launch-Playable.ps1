$ErrorActionPreference='Stop'
# User-invoked visible launch; no automated input. Not executed to claim human testing.
$build='I:/WGCombat/CP05BR-1103-A/PureBuild/Release'
foreach($r in (Get-Content "$PSScriptRoot/Evidence/release-files.json" -Raw|ConvertFrom-Json)){
 $p=Join-Path $build $r.path;if(!(Test-Path -LiteralPath $p)-or(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()-ne$r.sha256){throw "Package hash mismatch: $($r.path)"}
}
if(Get-Process WanxiangGuitu -ErrorAction SilentlyContinue){throw 'Existing Player; close it yourself before another launch'}
$root='I:/WGCombat/CP05BR-1103-A/Manual-'+[guid]::NewGuid().ToString('N');New-Item -ItemType Directory $root|Out-Null
Write-Host "Synthetic root: $root"
Start-Process -FilePath "$build/WanxiangGuitu.exe" -ArgumentList @('-cp05-training','-wanxiang-storage-root',$root,'-windowed','-screen-width','1280','-screen-height','720','-logFile',"$root/Player.log")
