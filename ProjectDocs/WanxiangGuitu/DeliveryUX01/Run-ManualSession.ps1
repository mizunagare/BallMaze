param([Parameter(Mandatory)][string]$Session,[Parameter(Mandatory)][string]$ParticipantCode,[Parameter(Mandatory)][string]$ObserverCode,[switch]$InteractiveConfirmed,[switch]$IndependentTesterDeclared,[ValidateSet('none','some','expert')][string]$PriorExposure='none',[switch]$RecordingConsent,[int]$TimeoutMinutes=90)
$ErrorActionPreference='Stop'
# MANUAL OPERATOR ENTRY ONLY. This script is never run by UX01 preparation or unattended tests.
if(!$InteractiveConfirmed -or !$IndependentTesterDeclared){throw 'A human operator must first confirm an authorized interactive session and independent tester; do not auto-confirm'}
if($ParticipantCode -notmatch '^[A-Za-z0-9_-]{1,32}$' -or $ObserverCode -notmatch '^[A-Za-z0-9_-]{1,32}$' -or $ParticipantCode -eq $ObserverCode){throw 'Use distinct pseudonymous participant and observer codes, not real names'}
if($TimeoutMinutes -lt 1 -or $TimeoutMinutes -gt 180){throw 'Bounded wait 1..180 minutes required'}
if(![IO.Path]::IsPathFullyQualified($Session)){throw 'Explicit absolute session required'}
$sessionPath=[IO.Path]::GetFullPath($Session)
for($p=$sessionPath;$p;$p=[IO.Path]::GetDirectoryName($p)){if((Test-Path -LiteralPath $p) -and ((Get-Item -LiteralPath $p -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse path refused'}}
if($sessionPath -match '(?i)(^|[\/])LocalLow([\/]|$)'){throw 'Never use actual player LocalLow'}
$meta=Get-Content "$sessionPath/session.json" -Raw|ConvertFrom-Json;$pack=[IO.Path]::GetFullPath($meta.packageRoot);$storage=[IO.Path]::GetFullPath($meta.storageRoot)
if((Get-Content "$pack/owner.json" -Raw|ConvertFrom-Json).kind -ne 'UX01 preparation only' -or !$sessionPath.StartsWith($pack+'\',[StringComparison]::OrdinalIgnoreCase) -or $storage -ne (Join-Path $sessionPath 'Storage')){throw 'Owned session/storage identity mismatch'}
if(@(Get-CimInstance Win32_Process -Filter "name='WanxiangGuitu.exe'").Count){throw 'Existing Player conflict; do not close user programs'}
if($meta.participantId -and ($meta.participantId -ne $ParticipantCode -or $meta.observerId -ne $ObserverCode)){throw 'Participant/observer changed; create a new session rather than merge trials'}
$releaseFiles=Get-Content "$pack/release-files.json" -Raw|ConvertFrom-Json
if(@(Get-ChildItem -LiteralPath "$pack/Release" -Recurse -Force|Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Release reparse member refused'}
if(@(Get-ChildItem -LiteralPath "$pack/Release" -Recurse -File -Force).Count -ne @($releaseFiles).Count){throw 'Release file membership changed'}
foreach($f in $releaseFiles){if((Get-FileHash -LiteralPath (Join-Path "$pack/Release" $f.path)).Hash -ne $f.sha256){throw "Release file changed: $($f.path)"}}
$lock=Get-Content "$pack/version-lock.json" -Raw|ConvertFrom-Json;$exe="$pack/Release/WanxiangGuitu.exe";$assembly="$pack/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll"
if((Get-FileHash $exe).Hash -ne $lock.exeSha256 -or (Get-FileHash $assembly).Hash -ne $lock.assemblySha256){throw 'Fixed pure-release identity changed'}
$meta.participantId=$ParticipantCode;$meta.observerId=$ObserverCode;$meta.priorExposure=$PriorExposure;$meta.independenceDeclared=$true;$meta.consent=[bool]$RecordingConsent;$meta.observationSource='HUMAN_OPERATOR_DECLARED_NATIVE_INPUT_NOT_AUTOMATICALLY_VERIFIED';$meta.status='IN_PROGRESS';$meta|ConvertTo-Json -Depth 8|Set-Content "$sessionPath/session.json"
$run=Join-Path $sessionPath ('Runs/'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,6));New-Item -ItemType Directory $run|Out-Null
function SaveInventory($file){
 for($p=$storage;$p;$p=[IO.Path]::GetDirectoryName($p)){if((Test-Path -LiteralPath $p) -and ((Get-Item -LiteralPath $p -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Storage reparse path refused'}}
 if(@(Get-ChildItem -LiteralPath $storage -Recurse -Force|Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Storage member reparse refused'}
 $rows=@(Get-ChildItem -LiteralPath $storage -Recurse -File|ForEach-Object {@{path=[IO.Path]::GetRelativePath($storage,$_.FullName);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}});ConvertTo-Json -InputObject $rows -Depth 5|Set-Content $file}
SaveInventory "$run/storage-before.json"
$launchArgs=@('-force-d3d11','-wanxiang-storage-root',$storage,'-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$run/Player.log")
$start=[datetime]::UtcNow;@{utc=$start.ToString('o');exe=$exe;exeSha256=(Get-FileHash $exe).Hash;assemblySha256=(Get-FileHash $assembly).Hash;arguments=$launchArgs;sessionId=$meta.sessionId;participantCode=$ParticipantCode;observerCode=$ObserverCode;priorExposure=$PriorExposure;recordingConsent=[bool]$RecordingConsent;independenceIsHumanDeclarationNotVerification=$true;method='Human operator explicitly starts visible Player; no injected driver/keys/messages; physical closing method must be observed separately'}|ConvertTo-Json -Depth 6|Set-Content "$run/launch.json"
# Visible is intentional only after the human operator's explicit -InteractiveConfirmed.
$psi=[Diagnostics.ProcessStartInfo]::new($exe);$psi.UseShellExecute=$false;$psi.WindowStyle='Normal';foreach($arg in $launchArgs){$psi.ArgumentList.Add($arg)}
$player=[Diagnostics.Process]::Start($psi);$retainedHandle=$player.Handle
@{pid=$player.Id;createdUtc=$player.StartTime.ToUniversalTime().ToString('o');sessionId=$player.SessionId;handleRetained=$retainedHandle -ne [IntPtr]::Zero;observerStartedUtc=$start.ToString('o')}|ConvertTo-Json|Set-Content "$run/process-start.json"
$deadline=$start.AddMinutes($TimeoutMinutes);while(!$player.WaitForExit(500) -and [datetime]::UtcNow -lt $deadline){}
$exited=$player.HasExited
@{pid=$player.Id;ended=$exited;exitCode=$(if($exited){$player.ExitCode}else{$null});exitObservedUtc=[datetime]::UtcNow.ToString('o');timedOut=!$exited;forcedTermination=$false;status=$(if($exited){'EXIT_OBSERVED_NOT_GAMEPLAY_VERDICT'}else{'UNRESOLVED_PROCESS_PRESERVED'});nativeInputVerified=$false;humanAcceptance='AWAITING_INDEPENDENT_EVIDENCE_REVIEW';note='Exit code, process absence and logs cannot prove physical UI or comprehension; observer must record actual close action'}|ConvertTo-Json|Set-Content "$run/process-end.json"
if($exited){SaveInventory "$run/storage-after.json";$meta.status='RECORDS_READY_FOR_REVIEW'}else{$meta.status='TECHNICAL_INTERRUPTION_PROCESS_PRESERVED'}
$meta|ConvertTo-Json -Depth 8|Set-Content "$sessionPath/session.json"
Write-Output "EVIDENCE=$run; no native/human PASS inferred"
