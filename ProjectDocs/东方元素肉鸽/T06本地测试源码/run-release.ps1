$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$project='C:/Users/guan/Documents/unitytest/MazeValidation'
$root='C:/Users/guan/Documents/unitytest/T06Validation'
foreach($method in @('T06ConsistencyCheck.Run','T06EditChecks.Run','T06FaultCheck.Run','T06BuildCheck.Build')){
 $arguments=@('-batchmode','-projectPath',"`"$project`"",'-executeMethod',$method,'-logFile',"`"$root/$method.release.log`"")
 if($method -eq 'T06BuildCheck.Build' -or $method -eq 'T06EditChecks.Run'){$arguments+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $arguments -WindowStyle Hidden -PassThru
 $p.WaitForExit()
 "$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/release-runner.txt" -Append
}
