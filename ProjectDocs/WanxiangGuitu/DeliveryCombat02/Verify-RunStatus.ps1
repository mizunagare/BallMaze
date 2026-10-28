param([Parameter(Mandatory)][string]$RunRoot)
$ErrorActionPreference='Stop';$RunRoot=[IO.Path]::GetFullPath($RunRoot)
if(!$RunRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !(Test-Path "$RunRoot/owner.json")){throw 'Explicit owned run root required'}
$issues=[Collections.Generic.List[object]]::new();$expected=[Collections.Generic.List[object]]::new()
$legacy=$null;if(Test-Path "$RunRoot/LegacyOriginal/combat01.json"){$legacy=Get-Content "$RunRoot/LegacyOriginal/combat01.json" -Raw|ConvertFrom-Json}
$legacyFail=@($legacy.checks|Where-Object status -eq FAIL)
$legacyExpected=$legacyFail.Count -eq 1 -and $legacyFail[0].name -eq 'multi collider single basic hit 1' -and $legacyFail[0].detail -eq 'expected=33 actual=41.25' -and @($legacy.checks|Where-Object status -eq PASS).Count -eq 187
foreach($folder in Get-ChildItem $RunRoot -Directory|Where-Object Name -ne P){foreach($file in Get-ChildItem $folder.FullName -Filter results.csv -Recurse -File){foreach($row in Import-Csv $file.FullName){if($row.status -eq 'FAIL'){$entry=@{file=$file.FullName;name=$row.name;exitCode=$row.exitCode;timedOut=$row.timedOut};if($folder.Name -eq 'LegacyOriginal' -and $legacyExpected -and $row.name -eq 'UX02BatchEntry.Combat' -and $row.exitCode -eq '1'){$expected.Add($entry)}else{$issues.Add($entry)}}}}}
$status=if($issues.Count){'FAIL'}else{'PASS'}
@{status=$status;unexpectedFailures=$issues.ToArray();expectedFailures=$expected.ToArray();note='Child results, not the last command exit; no historical result is rewritten'}|ConvertTo-Json -Depth 6|Set-Content "$RunRoot/aggregate-status.json" -Encoding utf8
Write-Output "$status unexpected=$($issues.Count) expected=$($expected.Count)"
if($issues.Count){exit 1};exit 0
