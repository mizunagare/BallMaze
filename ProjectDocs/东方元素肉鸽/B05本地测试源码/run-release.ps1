$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe';$root='C:/Users/guan/Documents/unitytest/B05Validation'
foreach($method in @('B05LoadFailureCheck.Run','B05ScenarioCheck.Run','B05V7MigrationCheck.Run','B05FaultCheck.Run','B05BuildCheck.Build')){
 $args2=@('-batchmode','-projectPath','C:/Users/guan/Documents/unitytest/MazeValidation','-executeMethod',$method,'-logFile',"$root/$method.release.log");if($method -eq 'B05BuildCheck.Build'){$args2+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $args2 -WindowStyle Hidden -PassThru;$p.WaitForExit();"$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/release-runner.txt" -Append
}
