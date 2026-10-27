[CmdletBinding()]
param([Parameter(Mandatory)][string]$AssemblyPath)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Reflection.Metadata
$stream=[IO.File]::OpenRead($AssemblyPath);$pe=[Reflection.PortableExecutable.PEReader]::new($stream)
try {
 $md=[Reflection.Metadata.PEReaderExtensions]::GetMetadataReader($pe)
 $module=$md.GetModuleDefinition();$methods=[Collections.Generic.List[object]]::new()
 foreach($th in $md.TypeDefinitions){$t=$md.GetTypeDefinition($th);$name=$md.GetString($t.Namespace)+'.'+$md.GetString($t.Name)
  foreach($mh in $t.GetMethods()){$m=$md.GetMethodDefinition($mh);$signature=[Convert]::ToHexString($md.GetBlobBytes($m.Signature));$body=''
   if($m.RelativeVirtualAddress -gt 0){$body=[Convert]::ToHexString([Reflection.Metadata.PEReaderExtensions]::GetMethodBody($pe,$m.RelativeVirtualAddress).GetILBytes())}
   $methods.Add([pscustomobject]@{type=$name;method=$md.GetString($m.Name);signature=$signature;ilHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($body)))})
  }
 }
 [pscustomobject]@{path=$AssemblyPath;sha256=(Get-FileHash -LiteralPath $AssemblyPath).Hash;mvid=$md.GetGuid($module.Mvid).ToString();peTimestamp=$pe.PEHeaders.CoffHeader.TimeDateStamp;methods=$methods}
}finally{$pe.Dispose();$stream.Dispose()}
