$r='I:/WGCombat/CP04BR-1102-A';$entry='H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR/Invoke-Players.ps1'
& $entry -Root "$r/FixedPlayers" -Build "$r/FixedAcceptanceBuild/Release" -Fixture 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json' -Suites Probe,Core
& $entry -Root "$r/BaselinePlayers" -Build "$r/BaselineAcceptanceBuild/Release" -Fixture 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json' -Suites Probe
& 'H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1' -Project "$r/Fixed/Project" -Output "$r/FixedEditorCore" -Method CP03Editor.Run -NonBatch
