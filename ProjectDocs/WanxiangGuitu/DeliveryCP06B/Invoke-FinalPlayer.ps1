$ErrorActionPreference='Stop';$root='I:/WGCombat/CP06B-1104-A';$docs='H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP06B';$build="$root/FinalTestBuild2/Release"
function NewRun([string]$name,[string]$mode,[string]$seed='',[string]$expected=''){
 $args=@{Build=$build;Output="$root/$name";Mode=$mode};if($seed){$args.SeedPackage=$seed};if($expected){$args.Expected=$expected}
 & "$docs/Invoke-Player.ps1" @args;@{name=$name;mode=$mode;actualExit=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/final-player-batch.jsonl"
}
foreach($pair in @(@('PlayerTwin2','training'),@('PlayerHeavy2','heavy'),@('PlayerScythe2','scythe'),@('PlayerBoundary2','boundary'),@('PlayerPerformance2','performance'),@('PlayerCancel2','cancel'),@('PlayerSave2','save'))){NewRun $pair[0] $pair[1]}
NewRun PlayerResume2 resume "$root/PlayerSave2/SeedPackage"
NewRun PlayerDrop2 drop "$root/PlayerSave2/SeedPackage"
NewRun PlayerBoss2 boss "$root/PlayerSave2/SeedPackage"
foreach($pair in @(@('LegacyExpandedPlayer2','training'),@('LegacyExtraPlayer2','extra'),@('LegacySavePlayer2','save'))){& "$docs/Invoke-ExpandedRegression.ps1" -Build $build -Output "$root/$($pair[0])" -Mode $pair[1];@{name=$pair[0];actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/final-player-batch.jsonl"}
& "$docs/Invoke-ExpandedRegression.ps1" -Build $build -Output "$root/LegacyResumePlayer2" -Mode resume -SeedPackage "$root/LegacySavePlayer2/SeedPackage";@{name='LegacyResumePlayer2';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/final-player-batch.jsonl"
& "$docs/Invoke-LegacyRegression.ps1" -Build $build -Output "$root/LegacyTrainingPlayer2" -Mode training;@{name='LegacyTrainingPlayer2';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/final-player-batch.jsonl"
& "$docs/Invoke-LegacyRegression.ps1" -Build $build -Output "$root/LegacyFormalPlayer2" -Mode formal -SeedPackage "$root/LegacyPlayerSeedPackage";@{name='LegacyFormalPlayer2';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/final-player-batch.jsonl"

NewRun PlayerChannelControl2 channel-control "$root/StorageEditor1/SeedPackage"
NewRun PlayerChannelNormal2 channel-normal "$root/StorageEditor1/SeedPackage"
NewRun PlayerChannelGround2 channel-ground "$root/PlayerChannelNormal2/GroundPackage" "$root/PlayerChannelNormal2/GroundPackage-expected.json"
NewRun PlayerChannelPicked2 channel-picked "$root/PlayerChannelNormal2/PickedPackage" "$root/PlayerChannelNormal2/PickedPackage-expected.json"
NewRun PlayerTrainingCanary2 training "$root/LegacyPlayerSeedPackage"
