$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$root='C:/Users/guan/Documents/unitytest/B05Validation'
foreach($method in @('B05ScenarioCheck.Run','B05V7MigrationCheck.Run','B05LegacyMigrationCheck.Run','B05FaultCheck.Run','B05BlockedRecoveryCheck.Run','B05EditChecks.Run')){
 $args2=@('-batchmode','-projectPath','C:/Users/guan/Documents/unitytest/MazeValidation','-executeMethod',$method,'-logFile',"$root/$method.log")
 if($method -eq 'B05EditChecks.Run'){$args2+='-quit'}
 $p=Start-Process -FilePath $unity -ArgumentList $args2 -WindowStyle Hidden -PassThru;$p.WaitForExit();"$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/runner.txt" -Append
}
