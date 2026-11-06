param([string]$Observation='ObservedFinal',[switch]$Legacy)
$ErrorActionPreference='Stop'
$r='I:/WGCombat/C22-1106-A'
$release=if($Legacy){"I:/WGCombat/C2-1106-A/PureBuild2/Release"}else{"$r/PureBuild2/Release"}
$copy="$r/$Observation/Release"
$exe="$release/WanxiangGuitu.exe"
if(!(Test-Path "$exe.release.json") -or !(Test-Path "$exe.bee.json") -or (Test-Path $copy)){throw 'Verified pure build and fresh test copy required'}
$bee=Get-Content "$exe.bee.json" -Raw|ConvertFrom-Json
$config=$bee.'PlayerBuildProgramLibrary.Data.PlayerBuildConfig'
if($config.Development -ne $false){throw 'Development setting'}
foreach($key in 'EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting'){
 if($config.Services.$key -ne $false){throw "Service $key"}
}
robocopy $release $copy /E /NFL /NDL /NJH /NJS /NP
if($LASTEXITCODE -ge 8){throw 'Isolated copy failed'}
$m="$copy/WanxiangGuitu_Data/Managed"
$csc='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/DotNetSdk/sdk/8.0.318/Roslyn/bincore/csc.dll'
$names='mscorlib','netstandard','System','System.Core','Assembly-CSharp','UnityEngine.CoreModule','UnityEngine.PhysicsModule','UnityEngine.ScreenCaptureModule','UnityEngine.ImageConversionModule','UnityEngine.AIModule','Unity.InputSystem','UnityEngine.ScriptingModule'
$refs=@($names|%{"-r:$m/$_.dll"})
$driver='CavernValidationDriver'
[string[]]$defines=if($Legacy){@()}else{@("-define:C22")}
dotnet $csc @defines -nologo -target:library -nostdlib+ "-out:$m/$driver.dll" @refs "$PSScriptRoot/Driver.cs.txt" 2>&1 | Out-File "$r/player-driver-compile-$Observation.log" -Encoding utf8
if($LASTEXITCODE){throw 'Validation driver compile failed'}
$d="$copy/WanxiangGuitu_Data"
$init=Get-Content "$d/RuntimeInitializeOnLoads.json" -Raw|ConvertFrom-Json
$init.root+=@{assemblyName=$driver;nameSpace='CavernValidation';className='Driver';methodName='Boot';loadTypes=0;isUnityClass=$false}
$init|ConvertTo-Json -Depth 7 -Compress|Set-Content "$d/RuntimeInitializeOnLoads.json"
$asm=Get-Content "$d/ScriptingAssemblies.json" -Raw|ConvertFrom-Json
$asm.names+="$driver.dll"
$asm.types+=16
$asm|ConvertTo-Json -Depth 5 -Compress|Set-Content "$d/ScriptingAssemblies.json"
Get-FileHash "$release/WanxiangGuitu.exe","$release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll","$m/$driver.dll" |
  Select-Object Path,Hash | ConvertTo-Json | Set-Content "$r/player-hashes-$Observation.json"
exit 0
