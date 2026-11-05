param([string]$Root='I:/WGCombat/C1-1105-A')
$ErrorActionPreference='Stop';$tools=$PSScriptRoot;$rows=[Collections.Generic.List[object]]::new()
function Editor([string]$name,[string]$method,[string]$seed='',[bool]$batch=$false){$out="$Root/$name";$a=@('-NoProfile','-File',"$tools/Invoke-Editor.ps1",'-Method',$method,'-Output',$out);if(!$batch){$a+='-NonBatch'};if($seed){$a+=@('-SeedPackage',$seed)};& pwsh @a;$code=$LASTEXITCODE;$semantic=$null;if(Test-Path "$out/probe.json"){$semantic=Get-Content "$out/probe.json" -Raw|ConvertFrom-Json};$fail=@($semantic.rows|Where-Object status -eq FAIL).Count;$rows.Add(@{name=$name;processExit=$code;assertionFailures=$fail;semanticPresent=($null-ne$semantic)});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/weapon-matrix-results.json";return ($code-eq0-and$fail-eq0)}
function Player([string]$name,[string]$mode,[string]$seed=''){$out="$Root/$name";$a=@('-NoProfile','-File',"$tools/Invoke-Player.ps1",'-Exe',"$Root/FullTestBuild2/Release/WanxiangGuitu.exe",'-Output',$out,'-Mode',$mode);if($seed){$a+=@('-SeedPackage',$seed)};& pwsh @a;$code=$LASTEXITCODE;$s=if(Test-Path "$out/probe.json"){Get-Content "$out/probe.json" -Raw|ConvertFrom-Json}else{$null};$fail=@($s.rows|Where-Object status -eq FAIL).Count;$rows.Add(@{name=$name;processExit=$code;assertionFailures=$fail;semanticPresent=($null-ne$s)});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/weapon-matrix-results.json";return ($code-eq0-and$fail-eq0)}
& pwsh -NoProfile -File "$tools/Invoke-Editor.ps1" -Method WanxiangBuild.ValidateBuild -Output "$Root/FullTestBuild2" -Seconds 900
if($LASTEXITCODE-ne0){throw 'Build failed'}
foreach($case in @(@('Sword',0),@('Spear',1),@('Staff',2),@('Bow',3),@('Twin',11),@('Great',12),@('Scythe',13))){[void](Editor ("WeaponEditor"+$case[0]+'2') ("C1Editor."+$case[0]));[void](Player ("WeaponPlayer"+$case[0]+'2') ("combat-"+$case[1]))}
[void](Editor 'EliteEditor3' 'C1Editor.Elite');[void](Player 'ElitePlayer2' 'elite')
[void](Editor 'DeathEditor3' 'C1Editor.Death');[void](Player 'DeathPlayer2' 'death')
[void](Editor 'BossResumeEditor1' 'C1Editor.Resume' "$Root/BossEditor2/SeedPackage")
[void](Player 'BossResumePlayer1' 'resume' "$Root/BossPlayer1/SeedPackage")
Write-Output 'Weapon matrix finished; check every semantic result separately.'
