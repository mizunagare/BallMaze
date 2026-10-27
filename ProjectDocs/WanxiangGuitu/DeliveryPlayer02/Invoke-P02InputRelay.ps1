[CmdletBinding()]
param([Parameter(Mandatory)][string]$CaseRoot,[Parameter(Mandatory)][string]$StorageRoot,[Parameter(Mandatory)][string]$Mode,[Parameter(Mandatory)][string]$Worker,[Parameter(Mandatory)][string]$ExpectedExe,[Parameter(Mandatory)][string]$Desktop)
$ErrorActionPreference='Stop';$dotnet=(Get-Command dotnet).Source;$seen=@{};$deadline=[datetime]::UtcNow.AddSeconds(1020)
try{
 while(!(Test-Path "$CaseRoot/relay-stop") -and [datetime]::UtcNow -lt $deadline){
  $receipt="$CaseRoot/runtime.$Mode.desktop-process.json";$request="$StorageRoot/p02-pointer-request.json"
  if((Test-Path $receipt) -and (Test-Path $request)){
   try{$process=Get-Content $receipt -Raw|ConvertFrom-Json;$r=Get-Content $request -Raw|ConvertFrom-Json}catch{Start-Sleep -Milliseconds 50;continue}
   if($r.mode -eq $Mode -and $r.pid -eq $process.pid -and $r.nonce -match '^[a-f0-9]{32}$' -and !$seen.ContainsKey($r.nonce)){
    if($process.desktop -ne $Desktop -or $process.inputDesktopActive){throw 'Relay desktop identity mismatch'}
    $seen[$r.nonce]=$true;$out="$CaseRoot/post-$($r.nonce).json"
    & $dotnet $Worker post-pointer ([string]$process.pid) $out $ExpectedExe $Desktop ([string]$r.x) ([string]$r.y)
    $code=$LASTEXITCODE;if(!(Test-Path $out)){throw 'Queued input helper produced no receipt'}
    Copy-Item -LiteralPath $out -Destination "$StorageRoot/p02-pointer-reply-$($r.nonce).json"
    @{nonce=$r.nonce;workerExit=$code;pid=$process.pid;utc=[datetime]::UtcNow.ToString('o');scope='Synthetic messages to owned inactive window; no native/human claim'}|ConvertTo-Json -Compress|Add-Content "$CaseRoot/relay-events.jsonl"
   }
  }
  Start-Sleep -Milliseconds 25
 }
 if(!(Test-Path "$CaseRoot/relay-stop")){throw 'Relay lifetime timeout; no process killed'}
 @{status='PASS';requests=$seen.Count;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$CaseRoot/relay-result.json";exit 0
}catch{$_|Out-String|Set-Content "$CaseRoot/relay-error.txt";exit 1}
