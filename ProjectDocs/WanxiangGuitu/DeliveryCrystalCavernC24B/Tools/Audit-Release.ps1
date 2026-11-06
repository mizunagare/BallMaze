param([string]$Root='I:/WGCombat/C24-1106-A',[string]$Build='PureBuild4')
$ErrorActionPreference='Stop'
$project=Join-Path $Root Project
$release=Join-Path $Root "$Build/Release"
$exe=Join-Path $release 'WanxiangGuitu.exe'
$meta=Join-Path $project 'Assets/Resources.meta'
$data=Get-Content -LiteralPath $meta -Raw
$guid=[regex]::Match($data,'(?m)^guid: (\w+)').Groups[1].Value
if(!$guid){throw 'Missing Resources folder GUID'}
$beforePath=Join-Path $Root 'resources-meta-before-build.json'
$before=if(Test-Path -LiteralPath $beforePath){Get-Content $beforePath -Raw|ConvertFrom-Json}else{$null}
$refs=@(Get-ChildItem (Join-Path $project Assets),(Join-Path $project Packages),(Join-Path $project ProjectSettings) -Recurse -File |
    Where-Object { $_.FullName -ne (Get-Item $meta).FullName -and $_.Extension -in '.meta','.asset','.prefab','.unity','.mat','.json','.asmdef','.controller' } |
    Select-String -SimpleMatch $guid -List|ForEach-Object { [IO.Path]::GetRelativePath($project,$_.Path) })
$bee=Get-Content "$exe.bee.json" -Raw|ConvertFrom-Json
$config=$bee.'PlayerBuildProgramLibrary.Data.PlayerBuildConfig'
$services=[ordered]@{}
foreach($name in 'EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting'){
    if($config.Services.$name -ne $false){throw "Invalid Bee service $name"}
    $services[$name]=$false
}
$assemblies=(Get-Content (Join-Path $release 'WanxiangGuitu_Data/ScriptingAssemblies.json') -Raw|ConvertFrom-Json).names
if($config.Development -ne $false -or $assemblies -contains 'CavernValidationDriver.dll' -or
    (Get-ChildItem -LiteralPath $release -Filter 'CavernValidationDriver.dll' -Recurse -File)){throw 'Release not pure'}
$assemblyPath=Join-Path $release 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
$noEmbeddedDriver=-not [Text.Encoding]::Latin1.GetString([IO.File]::ReadAllBytes($assemblyPath)).Contains('CavernValidation')
if(!$noEmbeddedDriver){throw 'Validation driver embedded in Assembly-CSharp'}
$afterHash=(Get-FileHash -LiteralPath $meta).Hash
$files=[ordered]@{}
foreach($file in Get-ChildItem -LiteralPath $release -Recurse -File|Sort-Object FullName){
    $relative=[IO.Path]::GetRelativePath($release,$file.FullName).Replace('\','/')
    $files[$relative]=@{sha256=(Get-FileHash -LiteralPath $file.FullName).Hash;bytes=$file.Length}
}
$output=@{
    summary=Get-Content "$exe.summary.txt" -Raw
    buildReceipt=Get-Content "$exe.release.json" -Raw|ConvertFrom-Json
    beeSha256=(Get-FileHash "$exe.bee.json").Hash
    noEmbeddedDriver=$noEmbeddedDriver
    development=$config.Development
    services=$services
    resourcesMeta=@{isolatedPath=$meta;content=$data;guid=$guid;sha256BeforeBuild=$before.Hash;sha256AfterBuild=$afterHash;serializedReferences=$refs;sameBytes=if($null-ne$before){$before.Hash -eq $afterHash}else{$null};status=if($null-ne$before){'OBSERVED'}else{'NOT_RUN'};missingBeforeManifest=$null-eq$before}
    files=$files
}
$dest=Join-Path (Split-Path $PSScriptRoot) Evidence
New-Item -ItemType Directory -Force $dest|Out-Null
$output|ConvertTo-Json -Depth 20|Set-Content -Encoding utf8 (Join-Path $dest "release-audit-$Build.json")
