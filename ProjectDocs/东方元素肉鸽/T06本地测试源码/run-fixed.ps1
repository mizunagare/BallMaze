$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$project='C:/Users/guan/Documents/unitytest/MazeValidation'
$root='C:/Users/guan/Documents/unitytest/T06Validation'
$methods=@('T06BlockedRecoveryCheck.Run','T06RegProgressionRuntimeCheck.Run','T06FaultCheck.Run','T06MatrixCheck.Run','T06MatrixCheck.Read','T06BuildCheck.Build')
foreach($method in $methods){
 $arguments=@('-batchmode','-projectPath',"`"$project`"",'-executeMethod',$method,'-logFile',"`"$root/$method.fixed.log`"")
 if($method -eq 'T06BuildCheck.Build'){$arguments+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $arguments -WindowStyle Hidden -PassThru
 $p.WaitForExit()
 "$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/fixed-runner.txt" -Append
}
