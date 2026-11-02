param([Parameter(Mandatory)][string]$Build,[Parameter(Mandatory)][string]$Output,[switch]$Acceptance)
$ErrorActionPreference='Stop';$Build=[IO.Path]::GetFullPath($Build);if(!$Build.StartsWith('I:\WGCombat\CP04B-')){throw 'Owned build required'}
$modules=@();$bad=@();$found=@()
foreach($file in Get-ChildItem "$Build/WanxiangGuitu_Data/Managed" -Filter '*.dll'){
 $stream=[IO.File]::OpenRead($file.FullName);$pe=[Reflection.PortableExecutable.PEReader]::new($stream)
 try{if(!$pe.HasMetadata){continue};$md=[Reflection.Metadata.PEReaderExtensions]::GetMetadataReader($pe);$types=@($md.TypeDefinitions|ForEach-Object {$t=$md.GetTypeDefinition($_);$md.GetString($t.Namespace)+'.'+$md.GetString($t.Name)});$refs=@($md.AssemblyReferences|ForEach-Object {$md.GetString($md.GetAssemblyReference($_).Name)});$drivers=@($types|Where-Object {$_ -match '^\.(CP04B|CP03Cases|CP03Player|Encai|BAL02|PlayerAcceptanceDriver|Aim01|BAL01|UX04|WorldAudit|Runloop)'});$found+=$drivers
 if(@($refs|Where-Object {$_ -like 'UnityEditor*'}).Count){$bad+=$file.Name+':UnityEditor'};if(!$Acceptance -and $drivers.Count){$bad+=$drivers};if($Acceptance){$bad+=@($drivers|Where-Object {$_ -notmatch '^\.(CP04B|CP03Cases)'})}
 $modules+=@{module=$file.Name;sha256=(Get-FileHash $file.FullName).Hash;drivers=$drivers;references=$refs}
 }finally{$pe.Dispose();$stream.Dispose()}
}
if($Acceptance -and '.CP04BPlayer' -notin $found){$bad+='Missing controlled driver'}
$hashes=foreach($rel in 'WanxiangGuitu.exe','UnityPlayer.dll','WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'){@{path=$rel;sha256=(Get-FileHash "$Build/$rel").Hash;bytes=(Get-Item "$Build/$rel").Length}}
@{status=if($bad.Count){'FAIL'}else{'PASS'};acceptance=[bool]$Acceptance;bad=$bad;modules=$modules;hashes=$hashes}|ConvertTo-Json -Depth 8|Set-Content -Encoding utf8 $Output
if($bad.Count){exit 1}
