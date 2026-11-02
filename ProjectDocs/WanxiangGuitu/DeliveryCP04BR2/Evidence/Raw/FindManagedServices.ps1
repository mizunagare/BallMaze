$ErrorActionPreference='Stop'
[Reflection.Assembly]::LoadFrom('C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Tools/Burst/Client/Unity.Burst.Cecil.dll')|Out-Null
$rows=@()
foreach($f in Get-ChildItem 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/Managed' -Filter 'UnityEditor*.dll') {
 $a=[Mono.Cecil.AssemblyDefinition]::ReadAssembly($f.FullName)
 foreach($t in $a.MainModule.Types) {
  foreach($m in $t.Methods) {
   if($m.FullName -match 'RequiresCoreStatsInBuild|GetServicesState|Insights.*enabled|Insights.*Enabled') {
    $il=@();if($m.HasBody){$il=@($m.Body.Instructions|ForEach-Object ToString)}
    $rows+=@{assembly=$f.FullName;type=$t.FullName;method=$m.FullName;il=$il}
   }
  }
 }
 $a.Dispose()
}
$rows|ConvertTo-Json -Depth 6|Set-Content I:/WGCombat/CP04BR2-1102-A/managed-services-methods.json
$rows|Select-Object type,method|ConvertTo-Json -Depth 3
