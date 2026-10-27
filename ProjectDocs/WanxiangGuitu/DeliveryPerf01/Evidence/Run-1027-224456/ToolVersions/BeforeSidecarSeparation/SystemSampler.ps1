param([Parameter(Mandatory)][string]$RuntimeRoot,[Parameter(Mandatory)][string]$StorageRoot,[Parameter(Mandatory)][string]$ExpectedExe)
$ErrorActionPreference='Stop';$deadline=[datetime]::UtcNow.AddSeconds(1050);$writer=$null
try{
 $receipt=$null
 while(!$receipt -and [datetime]::UtcNow -lt $deadline -and !(Test-Path "$StorageRoot/system-stop")){
  foreach($d in @(Get-ChildItem "$RuntimeRoot/Attempts" -Directory -ErrorAction SilentlyContinue)){
   if(!(Test-Path "$($d.FullName)/owner.json") -or !(Test-Path "$($d.FullName)/runtime.Observe.desktop-process.json")){continue}
   $o=Get-Content "$($d.FullName)/owner.json" -Raw|ConvertFrom-Json
   if([IO.Path]::GetFullPath($o.storage) -eq [IO.Path]::GetFullPath($StorageRoot)){$receipt=Get-Content "$($d.FullName)/runtime.Observe.desktop-process.json" -Raw|ConvertFrom-Json;break}
  };if(!$receipt){Start-Sleep -Milliseconds 100}
 }
 if(!$receipt){throw 'No actual owned Player receipt'}
 if($receipt.inputDesktopActive -or $receipt.exe -ne $ExpectedExe){throw 'Owned executable/desktop mismatch'}
 $proc=Get-Process -Id $receipt.pid;if([IO.Path]::GetFullPath($proc.Path) -ne [IO.Path]::GetFullPath($ExpectedExe)){throw 'PID recycled or wrong executable'}
 $writer=[IO.StreamWriter]::new("$StorageRoot/system-samples.csv",$false,[Text.UTF8Encoding]::new($false));$writer.WriteLine('utc,pid,elapsed_s,interval_s,cpu_total_ms,cpu_one_core_pct,cpu_machine_pct,working_set_bytes,private_bytes,gpu_dedicated_bytes,gpu_shared_bytes')
 $start=[datetime]::UtcNow;$last=$null;$lastCPU=$null;$gpu=$true;$gpuTries=0;$gpuNext=$start;$dedicated=-1;$shared=-1
 while(!(Test-Path "$StorageRoot/system-stop") -and [datetime]::UtcNow -lt $deadline){
  $proc.Refresh();if($proc.HasExited){break};$now=[datetime]::UtcNow;$cpu=$proc.TotalProcessorTime.TotalMilliseconds;$interval=if($last){($now-$last).TotalSeconds}else{0};$one=if($last -and $interval -gt 0){($cpu-$lastCPU)/($interval*10)}else{-1}
  if($gpu -and $now -ge $gpuNext){try{$g=@(Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory -Filter "Name LIKE 'pid_$($receipt.pid)_%'");if(!$g.Count){throw 'No GPU process counter instance'};$dedicated=($g|Measure-Object DedicatedUsage -Sum).Sum;$shared=($g|Measure-Object SharedUsage -Sum).Sum}catch{$gpuTries++;if($gpuTries -ge 3){$gpu=$false};@{attempt=$gpuTries;utc=$now.ToString('o');status='NOT_RUN';metric='GPU process memory';error=$_.Exception.ToString()}|ConvertTo-Json -Compress|Add-Content "$StorageRoot/system-errors.jsonl"};$gpuNext=$now.AddSeconds(5)}
  $values=@($now.ToString('o'),$receipt.pid,($now-$start).TotalSeconds,$interval,$cpu,$one,($one/[Environment]::ProcessorCount),$proc.WorkingSet64,$proc.PrivateMemorySize64,$dedicated,$shared)|ForEach-Object {[Convert]::ToString($_,[Globalization.CultureInfo]::InvariantCulture)};$writer.WriteLine(($values -join ','));$writer.Flush();$last=$now;$lastCPU=$cpu;Start-Sleep -Milliseconds 1000
 }
 @{status='PASS';pid=$receipt.pid;scope='Read-only exact owned PID sampling; GPU missing separately NOT_RUN; no exit-code inference';utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$StorageRoot/system-result.json"
}catch{$_|Out-String|Set-Content "$StorageRoot/system-sampler-error.txt";exit 1}finally{if($writer){$writer.Dispose()}}
