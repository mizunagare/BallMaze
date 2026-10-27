[CmdletBinding()]
param([Parameter(Mandatory)][string]$BuildRoot,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
$owner=Get-Content "$BuildRoot/owner.json" -Raw|ConvertFrom-Json
if($owner.kind -ne 'BUILD-01 diagnostic using existing coordinator'){throw 'Owned build required'}
$dll=Join-Path $BuildRoot 'Results/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
$metadata=& "$PSScriptRoot/../DeliveryBuild01/Inspect-Assembly.ps1" -AssemblyPath $dll
$bytes=[IO.File]::ReadAllBytes($dll);$ascii=[Text.Encoding]::UTF8.GetString($bytes);$unicode=[Text.Encoding]::Unicode.GetString($bytes);$unicodeOdd=[Text.Encoding]::Unicode.GetString($bytes,1,$bytes.Length-1)
$tokens=@('PlayerAcceptanceDriver','-p02-mode','-p02-expect','PLAYER02 isolated acceptance driver')
$probes=foreach($token in $tokens){[pscustomobject]@{token=$token;present=$ascii.Contains($token) -or $unicode.Contains($token) -or $unicodeOdd.Contains($token)}}
$types=@($metadata.methods.type|Sort-Object -Unique)
$stream=[IO.File]::OpenRead($dll);$pe=[Reflection.PortableExecutable.PEReader]::new($stream);try{$md=[Reflection.Metadata.PEReaderExtensions]::GetMetadataReader($pe);$references=@($md.AssemblyReferences|ForEach-Object {$md.GetString($md.GetAssemblyReference($_).Name)})}finally{$pe.Dispose();$stream.Dispose()}
$scene=[IO.File]::ReadAllText((Join-Path $BuildRoot 'Project/ProjectSettings/EditorBuildSettings.asset'))
$release=$owner.variant -eq 'Release'
$passed=if($release){!@($probes|Where-Object present).Count -and !@($types|Where-Object {$_ -match 'PlayerAcceptanceDriver|Build01Audit'}).Count -and !(Test-Path "$BuildRoot/Project/Assets/Player02AcceptanceOnly")}else{@($types|Where-Object {$_ -match 'PlayerAcceptanceDriver'}).Count -gt 0 -and @($probes|Where-Object {$_.token -eq '-p02-mode' -and $_.present}).Count -eq 1}
if(@($references|Where-Object {$_ -match '^UnityEditor'}).Count){$passed=$false}
$report=Get-Content "$BuildRoot/Results/build-report-messages.json" -Raw|ConvertFrom-Json
$hashes=foreach($name in 'WanxiangGuitu.exe','UnityPlayer.dll','WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'){$file=Join-Path $BuildRoot "Results/Release/$name";[pscustomobject]@{path=$name;sha256=(Get-FileHash $file).Hash;bytes=(Get-Item $file).Length}}
[pscustomobject]@{status=$(if($passed){'PASS'}else{'FAIL'});variant=$owner.variant;build=$BuildRoot;utc=[datetime]::UtcNow.ToString('o');assemblySha256=$metadata.sha256;mvid=$metadata.mvid;tokens=$probes;types=$types;assemblyReferences=$references;sceneConfiguration=$scene;sceneConfigurationSha256=(Get-FileHash "$BuildRoot/Project/ProjectSettings/EditorBuildSettings.asset").Hash;hashes=$hashes;buildResult=$report.result;errors=$report.errors;warnings=$report.warnings;scope='PE metadata + UTF8/UTF16 string probes + isolated source/scene inspection; not a runtime gameplay result'}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $Output
if(!$passed){throw 'Build exclusion/injection proof failed'}
