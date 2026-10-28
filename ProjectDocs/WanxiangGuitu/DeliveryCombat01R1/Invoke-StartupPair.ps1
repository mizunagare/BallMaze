param([Parameter(Mandatory)][string]$ParentRoot,[Parameter(Mandatory)][string]$BuildRoot,[string]$Story='Story1')
$ErrorActionPreference='Stop';$parent=[IO.Path]::GetFullPath($ParentRoot);if($Story -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Invalid synthetic story name'}
if((Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PLAYER-02 isolated runtime acceptance' -or !(Test-Path "$BuildRoot/combat-r1-profile.json")){throw 'Owned R1 acceptance profile required'}
$storage=Join-Path $parent $Story;if(Test-Path $storage){throw 'Fresh story required; never overwrite an earlier attempt'};New-Item -ItemType Directory $storage|Out-Null
$stages=[Collections.Generic.List[object]]::new()
foreach($stage in 'Save','Resume'){
 # This is test scenario selection, never progress/save payload editing.
 @{stage=$stage}|ConvertTo-Json|Set-Content "$storage/combat-r1-config.json"
 $before=@(Get-ChildItem "$parent/Attempts" -Directory -ErrorAction SilentlyContinue|ForEach-Object FullName)
 & "$PSScriptRoot/../DeliveryPlayer02/Invoke-P02Case.ps1" -ParentRoot $parent -StorageRoot $storage -Mode Observe -BuildRoot $BuildRoot -WorkerFrom "$parent/Host"
 $code=$LASTEXITCODE;$new=@(Get-ChildItem "$parent/Attempts" -Directory|Where-Object {$_.FullName -notin $before});if($new.Count -ne 1){throw 'Attempt identity ambiguous'}
 $native=Join-Path $new[0].FullName 'runtime.Observe.desktop-process.json.native-exit.json';$known=$false
 if(Test-Path $native){$v=Get-Content $native -Raw|ConvertFrom-Json;$known=$v.waitResult -eq 0 -and $v.exitCodeKnown -and $v.actualExitCode -eq 0}
 $stages.Add([pscustomobject]@{stage=$stage;attempt=$new[0].FullName;wrapperExit=$code;nativeChildExitVerified=$known;nativeReceipt=$native;storage=$storage})
 $stages|ConvertTo-Json -Depth 5|Set-Content "$parent/$Story-stages.json"
 if($code -ne 0 -or !$known){Write-Output "STOP_DEPENDENT_STAGE=$stage; no later PASS inferred";exit 1}
}
