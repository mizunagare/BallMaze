param([Parameter(Mandatory)][string]$Root)
$ErrorActionPreference='Stop'
$Root=[IO.Path]::GetFullPath($Root)
if(!(Test-Path $Root -PathType Container)){throw 'Create a fresh isolated output root first'}
$source='I:/WGCombat/C1R3-1105-A'
$files=Get-Content "$source/Audit/build-file-hashes.json" -Raw|ConvertFrom-Json -AsHashtable
foreach($label in 'A','B'){
 foreach($kind in 'Pure','Probe'){
  $dir=Join-Path $Root "$kind$label"
  if(Test-Path $dir){throw 'Existing output'}
  New-Item -ItemType Directory $dir|Out-Null
  Copy-Item "$source/Project$label-Build/Release" "$dir/Release" -Recurse
  foreach($file in $files["Project$label-Build"].GetEnumerator()){
   if((Get-FileHash -LiteralPath "$dir/Release/$($file.Key)").Hash.ToLower()-ne$file.Value){throw "Input hash mismatch $($file.Key)"}
  }
 }
}
$managed="$Root/PureA/Release/WanxiangGuitu_Data/Managed"
$csc='C:/Program Files/dotnet/sdk/10.0.402/Roslyn/bincore/csc.dll'
& dotnet $csc /nologo /target:library /nostdlib+ "/reference:$managed/mscorlib.dll" "/reference:$managed/System.dll" "/reference:$managed/netstandard.dll" "/reference:$managed/UnityEngine.CoreModule.dll" "/reference:$managed/UnityEngine.TerrainModule.dll" "/out:$Root/C1R4ResourceProbe.dll" "$PSScriptRoot/ResourceProbe.cs.txt"
if($LASTEXITCODE-ne0){throw 'Sidecar compilation failed'}
foreach($label in 'A','B'){
 $folder="$Root/Probe$label/Release/WanxiangGuitu_Data"
 Copy-Item "$Root/C1R4ResourceProbe.dll" "$folder/Managed/C1R4ResourceProbe.dll"
 $p="$folder/ScriptingAssemblies.json"
 $v=Get-Content $p -Raw|ConvertFrom-Json
 $v.names+='C1R4ResourceProbe.dll'
 $v.types+=16
 $v|ConvertTo-Json -Compress -Depth 6|Set-Content $p -Encoding utf8
 $p="$folder/RuntimeInitializeOnLoads.json"
 $v=Get-Content $p -Raw|ConvertFrom-Json
 $v.root+=@{assemblyName='C1R4ResourceProbe';nameSpace='C1R4';className='ResourceProbe';methodName='Run';loadTypes=1;isUnityClass=$false}
 $v|ConvertTo-Json -Compress -Depth 6|Set-Content $p -Encoding utf8
}
