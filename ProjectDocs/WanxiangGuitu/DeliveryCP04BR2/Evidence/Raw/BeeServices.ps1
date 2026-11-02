$ErrorActionPreference='Stop'
[Reflection.Assembly]::LoadFrom('C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Tools/Burst/Client/Unity.Burst.Cecil.dll')|Out-Null
$rows=@()
foreach($file in Get-ChildItem 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Managed' -Filter 'UnityEditor*.dll'){
 $a=[Mono.Cecil.AssemblyDefinition]::ReadAssembly($file.FullName)
 foreach($t in $a.MainModule.Types){foreach($m in $t.Methods){if($m.HasBody -and $m.Name -eq 'PlayerBuildConfigFor'){$rows+=@{assembly=$file.FullName;method=$m.FullName;instructions=@($m.Body.Instructions|Where-Object Offset -lt 0x114|ForEach-Object ToString)}}}}
 $a.Dispose()
}
$rows|ConvertTo-Json -Depth 6|Set-Content I:/WGCombat/CP04BR2-1102-A/bee-services-il.json
