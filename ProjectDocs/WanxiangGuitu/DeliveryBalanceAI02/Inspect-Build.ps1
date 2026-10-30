param([Parameter(Mandatory)][string]$BuildRoot,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
if(!$BuildRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned build required'}
$modules=@();$unexpected=@()
foreach($file in Get-ChildItem "$BuildRoot/WanxiangGuitu_Data/Managed" -Filter '*.dll'){
 $stream=[IO.File]::OpenRead($file.FullName);$pe=[Reflection.PortableExecutable.PEReader]::new($stream)
 try{
  if(!$pe.HasMetadata){continue}
  $md=[Reflection.Metadata.PEReaderExtensions]::GetMetadataReader($pe)
  $types=@($md.TypeDefinitions|ForEach-Object {$t=$md.GetTypeDefinition($_);$md.GetString($t.Namespace)+'.'+$md.GetString($t.Name)})
  $references=@($md.AssemblyReferences|ForEach-Object {$md.GetString($md.GetAssemblyReference($_).Name)})
  $drivers=@($types|Where-Object {$_ -match 'BAL02|PlayerAcceptanceDriver|Aim01Before|Aim01Rules|Aim01Scenarios|BAL01|UX04|WorldAudit|WorldCycle|WorldFeedback|WorldPoi|WorldCompileFailureExit|R1Matrix|R1Migration|RunloopFault|RunloopCycle|RunloopUncertain|RunloopEntry|RunloopOverflow|RunloopRuntimeAudit'})
  if($drivers.Count){$unexpected+=$drivers};if(@($references|Where-Object {$_ -like 'UnityEditor*'}).Count){$unexpected+=$file.Name+':UnityEditor'}
  $modules+=@{module=$file.Name;sha256=(Get-FileHash $file.FullName).Hash;types=$types;references=$references;testDriverTypes=$drivers}
 }finally{$pe.Dispose();$stream.Dispose()}
}
$hashes=foreach($rel in 'WanxiangGuitu.exe','UnityPlayer.dll','WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'){$p=Join-Path $BuildRoot $rel;@{path=$rel;sha256=(Get-FileHash $p).Hash;bytes=(Get-Item $p).Length}}
@{status=$(if($unexpected.Count){'FAIL'}else{'PASS'});scope='Read-only PE metadata: no AIM01/PLAYER02/BAL01/UX04/WORLD/R1/RUN01 observation or Editor fixtures or UnityEditor references in release modules';hashes=$hashes;modules=$modules}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $Output -Encoding utf8
if($unexpected.Count){exit 1}
