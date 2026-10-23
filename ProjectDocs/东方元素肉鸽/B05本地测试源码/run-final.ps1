$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$root='C:/Users/guan/Documents/unitytest/B05Validation'
$methods=@('B05CrashCheck.BeforeLock','B05CrashCheck.ReadBeforeLock','B05CrashCheck.AfterLock','B05CrashCheck.ReadAfterLock','B05CrashCheck.BeforeCommit','B05CrashCheck.ReadBeforeCommit','B05CrashCheck.AfterCommit','B05CrashCheck.ReadAfterCommit','B05UICheck.Run','B05UICheck.Restart','T06RegDualWeaponCheck.Run','T06RegDualGameplayRegression.Run','T06RegWorkbenchCheck.Run','T06RegWorkbenchCheck.Read','T06RegProgressionRuntimeCheck.Run','WorldEventsRuntimeCheck.Run','PotionRuntimeCheck.Run','AutoWaveRuntimeCheck.Run','HeroDodgeRuntimeCheck.Run','B05BuildCheck.Build')
foreach($method in $methods){
 $args2=@('-batchmode','-projectPath','C:/Users/guan/Documents/unitytest/MazeValidation','-executeMethod',$method,'-logFile',"$root/$method.final.log")
 if($method -eq 'B05BuildCheck.Build'){$args2+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $args2 -WindowStyle Hidden -PassThru;$p.WaitForExit();"$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/final-runner.txt" -Append
}
