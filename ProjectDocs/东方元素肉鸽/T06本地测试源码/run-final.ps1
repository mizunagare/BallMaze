$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$project='C:/Users/guan/Documents/unitytest/MazeValidation'
$root='C:/Users/guan/Documents/unitytest/T06Validation'
$methods=@('T06UICheck.Run','T06UICheck.Restart','T06LiveRegression.Run','T06RegDualWeaponCheck.Run','T06RegDualGameplayRegression.Run','T06RegWorkbenchCheck.Run','T06RegWorkbenchCheck.Read','HeroDodgeRuntimeCheck.Run','WorldEventsRuntimeCheck.Run','ProgressionRuntimeCheck.Run','PotionRuntimeCheck.Run','AutoWaveRuntimeCheck.Run','T06MigrationCheck.Run','T06FaultCheck.Run','T06BuildCheck.Build')
foreach($method in $methods){
 $log="$root/$method.final.log"
 $arguments=@('-batchmode','-projectPath',"`"$project`"",'-executeMethod',$method,'-logFile',"`"$log`"")
 if($method -eq 'T06BuildCheck.Build'){$arguments+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $arguments -WindowStyle Hidden -PassThru
 $p.WaitForExit()
 "$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/final-runner.txt" -Append
}
