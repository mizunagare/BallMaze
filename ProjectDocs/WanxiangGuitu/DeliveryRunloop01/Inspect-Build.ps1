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
  $drivers=@($types|Where-Object {$_ -match 'RunloopFault|RunloopCycle|RunloopUncertain|RunloopEntry|RunloopOverflow'})
  if($drivers.Count){$unexpected+=$drivers}
  $modules+=@{module=$file.Name;sha256=(Get-FileHash $file.FullName).Hash;types=$types;references=$references;testDriverTypes=$drivers}
 }finally{$pe.Dispose();$stream.Dispose()}
}
$hashes=foreach($rel in 'WanxiangGuitu.exe','UnityPlayer.dll','WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'){$p=Join-Path $BuildRoot $rel;@{path=$rel;sha256=(Get-FileHash $p).Hash;bytes=(Get-Item $p).Length}}
@{status=$(if($unexpected.Count){'FAIL'}else{'PASS'});scope='Read-only PE metadata: no RUN01 Editor fixtures in release modules';hashes=$hashes;modules=$modules}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $Output -Encoding utf8
if($unexpected.Count){exit 1}
