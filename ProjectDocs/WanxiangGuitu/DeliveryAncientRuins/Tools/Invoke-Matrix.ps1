param([string]$Root='I:/WGCombat/C1-1105-A')
$ErrorActionPreference='Stop';$tools=$PSScriptRoot;$rows=[Collections.Generic.List[object]]::new()
function Editor([string]$name,[string]$method,[string]$seed='',[bool]$batch=$false){$out="$Root/$name";$a=@('-NoProfile','-File',"$tools/Invoke-Editor.ps1",'-Method',$method,'-Output',$out);if(!$batch){$a+='-NonBatch'};if($seed){$a+=@('-SeedPackage',$seed)};& pwsh @a;$code=$LASTEXITCODE;$semantic=$null;if(Test-Path "$out/probe.json"){$semantic=Get-Content "$out/probe.json" -Raw|ConvertFrom-Json};$fail=@($semantic.rows|Where-Object status -eq FAIL).Count;$rows.Add(@{name=$name;processExit=$code;assertionFailures=$fail;semanticPresent=($null-ne$semantic)});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/matrix-results.json";return ($code-eq0-and$fail-eq0)}
function Player([string]$name,[string]$mode,[string]$seed=''){$out="$Root/$name";$a=@('-NoProfile','-File',"$tools/Invoke-Player.ps1",'-Exe',"$Root/FullTestBuild1/Release/WanxiangGuitu.exe",'-Output',$out,'-Mode',$mode);if($seed){$a+=@('-SeedPackage',$seed)};& pwsh @a;$code=$LASTEXITCODE;$s=if(Test-Path "$out/probe.json"){Get-Content "$out/probe.json" -Raw|ConvertFrom-Json}else{$null};$fail=@($s.rows|Where-Object status -eq FAIL).Count;$rows.Add(@{name=$name;processExit=$code;assertionFailures=$fail;semanticPresent=($null-ne$s)});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/matrix-results.json";return ($code-eq0-and$fail-eq0)}
& pwsh -NoProfile -File "$tools/Invoke-Editor.ps1" -Method WanxiangBuild.ValidateBuild -Output "$Root/FullTestBuild1" -Seconds 900
if($LASTEXITCODE-ne0){throw 'Build failed; no Player matrix'}
$explored=Player 'FullPlayer1' 'explore'
if($explored){[void](Editor 'ResumeEditor1' 'C1Editor.Resume' "$Root/FullPlayer1/SeedPackage");[void](Player 'ResumePlayer1' 'resume' "$Root/FullPlayer1/SeedPackage")}
[void](Editor 'FrontierResumeEditor1' 'C1Editor.FrontierResume' "$Root/FrontierPlayer1/WanxiangGuitu/ForestRuins")
[void](Player 'FrontierResumePlayer1' 'resume-frontier' "$Root/FrontierPlayer1/WanxiangGuitu/ForestRuins")
foreach($case in @(@('Sword',0),@('Spear',1),@('Staff',2),@('Bow',3),@('Twin',11),@('Great',12),@('Scythe',13))){[void](Editor ("WeaponEditor"+$case[0]+'1') ("C1Editor."+$case[0]));[void](Player ("WeaponPlayer"+$case[0]+'1') ("combat-"+$case[1]))}
foreach($case in 'Elite','Boss','Death','Fault'){[void](Editor ($case+'Editor2') ('C1Editor.'+$case));[void](Player ($case+'Player1') $case.ToLower())}
[void](Editor 'LegacyStreams1' 'B3StreamRules.Run' '' $true)
[void](Editor 'LegacyEconomy1' 'B07Economy.Run' '' $true)
Write-Output 'Matrix completed; inspect process AND semantic rows, not this script status.'
