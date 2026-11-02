param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$Watch,[Parameter(Mandatory)][string]$Method)
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output);$Watch=[IO.Path]::GetFullPath($Watch)
foreach($path in @($Project,$Output,$Watch)){if(!$path.StartsWith('I:\WGCombat\CP04BR-')){throw 'Owned BR paths required'}}
$py=Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';$stop=$Watch+'.stop';$spec=$Watch+'.spec.json';@{project=$Project;output=$Watch;stop=$stop;log="$Output/Unity.log"}|ConvertTo-Json|Set-Content -Encoding utf8 $spec
$observer=Start-Process -FilePath $py -ArgumentList @("$PSScriptRoot/WatchInputs.py",'--spec',$spec) -WindowStyle Hidden -PassThru
try{& "$PSScriptRoot/../DeliveryEncounterAI01/Invoke-Check.ps1" -Project $Project -Output $Output -Method $Method -NonBatch;$code=$LASTEXITCODE}finally{[IO.File]::WriteAllText($stop,'completed');$observer.WaitForExit(10000)|Out-Null}
exit $code
