$ErrorActionPreference='Stop';$root='I:/WGCombat/CP06B-1104-A';$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1'
function Run([string]$name,[string]$method,[string]$storage=''){$args=@{Project="$root/Project";Output="$root/$name";Method=$method;NonBatch=$true};if($storage){$args.StorageRoot="$root/$storage"}; & $entry @args;@{name=$name;method=$method;storage=$storage;actualExit=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$root/channel-editor-batch2.jsonl"}
foreach($name in 'ChannelControlData2','ChannelNormalData2'){$dest="$root/$name/WanxiangGuitu/ForestRuins";New-Item -ItemType Directory $dest -ErrorAction Stop|Out-Null;Copy-Item "$root/StorageEditor1/SeedPackage/*" $dest -Recurse}
Run StorageEditor3 NWEditor.RunStorage
Run ChannelControlEditor2 NWEditor.ChannelControl ChannelControlData2
Run ChannelNormalEditor2 NWEditor.ChannelNormal ChannelNormalData2
foreach($pair in @(@('GroundPackage','ChannelGroundData2'),@('PickedPackage','ChannelPickedData2'))){$dest="$root/$($pair[1])/WanxiangGuitu/ForestRuins";New-Item -ItemType Directory $dest -ErrorAction Stop|Out-Null;Copy-Item "$root/ChannelNormalData2/$($pair[0])/*" $dest -Recurse;Copy-Item "$root/ChannelNormalData2/$($pair[0])-expected.json" "$root/$($pair[1])/channel-expected.json"}
Run ChannelGroundEditor2 NWEditor.ChannelGround ChannelGroundData2
Run ChannelPickedEditor2 NWEditor.ChannelPicked ChannelPickedData2
Run PerformanceEditor3 NWEditor.RunPerformance
Run TwinEditor3 NWEditor.Run
