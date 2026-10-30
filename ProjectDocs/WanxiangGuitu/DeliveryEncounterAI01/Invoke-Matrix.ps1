param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[string]$OnlyFailedFrom)
$ErrorActionPreference='Stop'
$RunRoot=[IO.Path]::GetFullPath($RunRoot)
if(!$RunRoot.StartsWith('I:\WGCombat\EAI01-',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned isolated root required'}
if(Test-Path -LiteralPath $RunRoot){throw 'Preserve previous attempts: matrix root must be new'}
New-Item -ItemType Directory -Path $RunRoot|Out-Null
$results=@();$old=if($OnlyFailedFrom){@(Get-Content -LiteralPath $OnlyFailedFrom -Raw|ConvertFrom-Json)}else{@()}
foreach($seed in 418,419,420){foreach($rep in 0,1,2){
 if($OnlyFailedFrom -and @($old|Where-Object {$_.seed -eq $seed -and $_.rep -eq $rep -and $_.status -eq "PASS"}).Count){continue}
 $case=Join-Path $RunRoot "S$seed-R$rep";New-Item -ItemType Directory $case|Out-Null
 @{seed=$seed;rep=$rep}|ConvertTo-Json|Set-Content "$case/enc-config.json" -Encoding utf8
 $begin=[datetime]::UtcNow
 & "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -StorageRoot $case -Output "$case/Launch" -Method EncaiMatrix.Run -NoGraphics
 $code=$LASTEXITCODE
 $results+=@{seed=$seed;rep=$rep;startUTC=$begin.ToString('o');endUTC=[datetime]::UtcNow.ToString('o');exitCode=$code;status=if($code -eq 0){'PASS'}else{'FAIL'};evidence=$case}
 $results|ConvertTo-Json -Depth 5|Set-Content "$RunRoot/process-results.json" -Encoding utf8
 # Independent next process is safe after a normal exit. Never race an occupied project.
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains([IO.Path]::GetFullPath($Project))}).Count){throw 'Previous owned Unity remains: preserve it and stop dependent launches'}
}}
if(@($results|Where-Object status -eq FAIL).Count){exit 1}

