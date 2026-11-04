$ErrorActionPreference='Stop';$root='I:/WGCombat/CP06B-1104-A';$docs='H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP06B';$build="$root/LatestTestBuild4/Release"
function NewRun([string]$name,[string]$mode,[string]$seed='',[string]$expected=''){
 $args=@{Build=$build;Output="$root/$name";Mode=$mode};if($seed){$args.SeedPackage=$seed};if($expected){$args.Expected=$expected}
 & "$docs/Invoke-Player.ps1" @args;@{name=$name;mode=$mode;actualExit=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"
}
foreach($pair in @(@('PlayerTwinLatest4','training'),@('PlayerHeavyLatest4','heavy'),@('PlayerScytheLatest4','scythe'),@('PlayerBoundaryLatest4','boundary'),@('PlayerPerformanceLatest4','performance'),@('PlayerCancelLatest4','cancel'),@('PlayerSaveLatest4','save'))){NewRun $pair[0] $pair[1]}
NewRun PlayerResumeLatest4 resume "$root/PlayerSaveLatest4/SeedPackage"
NewRun PlayerDropLatest4 drop "$root/PlayerSaveLatest4/SeedPackage"
NewRun PlayerBossLatest4 boss "$root/PlayerSaveLatest4/SeedPackage"
foreach($pair in @(@('LegacyExpandedPlayerLatest4','training'),@('LegacyExtraPlayerLatest4','extra'),@('LegacySavePlayerLatest4','save'))){& "$docs/Invoke-ExpandedRegression.ps1" -Build $build -Output "$root/$($pair[0])" -Mode $pair[1];@{name=$pair[0];actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"}
& "$docs/Invoke-ExpandedRegression.ps1" -Build $build -Output "$root/LegacyResumePlayerLatest4" -Mode resume -SeedPackage "$root/LegacySavePlayerLatest4/SeedPackage";@{name='LegacyResumePlayerLatest4';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"
& "$docs/Invoke-LegacyRegression.ps1" -Build $build -Output "$root/LegacyTrainingPlayerLatest4" -Mode training;@{name='LegacyTrainingPlayerLatest4';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"
& "$docs/Invoke-LegacyRegression.ps1" -Build $build -Output "$root/LegacyFormalPlayerLatest4" -Mode formal -SeedPackage "$root/LegacyPlayerSeedPackage";@{name='LegacyFormalPlayerLatest4';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"

NewRun PlayerChannelControlLatest4 channel-control "$root/StorageEditor1/SeedPackage"
NewRun PlayerChannelNormalLatest4 channel-normal "$root/StorageEditor1/SeedPackage"
NewRun PlayerChannelGroundLatest4 channel-ground "$root/PlayerChannelNormalLatest4/GroundPackage" "$root/PlayerChannelNormalLatest4/GroundPackage-expected.json"
NewRun PlayerChannelPickedLatest4 channel-picked "$root/PlayerChannelNormalLatest4/PickedPackage" "$root/PlayerChannelNormalLatest4/PickedPackage-expected.json"
NewRun PlayerTrainingCanaryLatest4 training "$root/LegacyPlayerSeedPackage"

& "$docs/Invoke-StatsPlayer.ps1" -Build $build -Output "$root/PlayerStatsLatest4";@{name='PlayerStatsLatest4';actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/latest-player-batch4.jsonl"
