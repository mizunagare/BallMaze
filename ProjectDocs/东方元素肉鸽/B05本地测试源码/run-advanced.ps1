$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$root='C:/Users/guan/Documents/unitytest/B05Validation'
foreach($method in @('B05LegacyMigrationCheck.Run','B05AdvancedCheck.Run','B05AdvancedCheck.Read','B05LiveRegression.Run','B05ConsistencyCheck.Run','B05UICheck.Run','B05UICheck.Restart')){
 $p=Start-Process -FilePath $unity -ArgumentList @('-batchmode','-projectPath','C:/Users/guan/Documents/unitytest/MazeValidation','-executeMethod',$method,'-logFile',"$root/$method.log") -WindowStyle Hidden -PassThru;$p.WaitForExit();"$method exit=$($p.ExitCode)" | Tee-Object -FilePath "$root/advanced-runner.txt" -Append
}
