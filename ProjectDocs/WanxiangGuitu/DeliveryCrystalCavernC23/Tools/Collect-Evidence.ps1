param([string]$Root='I:/WGCombat/C23-1106-A')
$ErrorActionPreference='Stop'
$dest=Join-Path (Split-Path $PSScriptRoot) 'Evidence'
New-Item -ItemType Directory -Force $dest|Out-Null
$files=[Collections.Generic.List[object]]::new()
$runs=[ordered]@{}
$names=@('process.json','complete.txt','failure.txt','fixture.json','expected.txt','ground.txt','run-identity.json','scene-counts.json','pure-runtime.json','entry-audit.jsonl','close-delivery.json','modal-cleanup.json','Editor.command.json','Player.command.json','Editor.desktop-process.json','Player.desktop-process.json','Driver.executed.cs.txt','LakeDriver.executed.cs.txt','C23ValidationDriver.cs','C23LakeDriver.cs')
foreach($run in Get-ChildItem -LiteralPath $Root -Directory|Sort-Object Name){
    if($run.Name -in 'Project','EditorProject'){continue}
    $assertions=Join-Path $run.FullName 'assertions.tsv'
    if(Test-Path -LiteralPath $assertions){
        $states=@(Get-Content -LiteralPath $assertions|ForEach-Object{($_ -split "`t",3)[1]})
        $result=[ordered]@{}
        foreach($status in 'PASS','FAIL','NOT_RUN','UNRESOLVED'){
            $result[$status]=@($states|Where-Object{$_ -ceq $status}).Count
        }
        $result.completionMarker=Test-Path -LiteralPath (Join-Path $run.FullName 'complete.txt')
        $process=Join-Path $run.FullName 'process.json'
        $result.process=if(Test-Path $process){Get-Content $process -Raw|ConvertFrom-Json}else{$null}
        $result.semantic=if(!$result.completionMarker -or !$result.process -or !$result.process.exited){'INCOMPLETE'}elseif($result.FAIL -gt 0 -or $result.process.exitCode -ne 0){'FAIL'}elseif($result.UNRESOLVED -gt 0){'BLOCKED'}elseif($result.NOT_RUN -gt 0 -or $result.PASS -eq 0){'INCOMPLETE'}else{'PASS'}
        $runs[$run.Name]=$result
    }
    foreach($file in Get-ChildItem -LiteralPath $run.FullName -File|Sort-Object Name){
        if($file.Extension -notin '.log','.tsv','.png','.json','.jsonl','.stdout','.stderr' -and $file.Name -notin $names){continue}
        $relative=$null
        if($file.Extension -ne '.log'){
            $relative="Raw/$($run.Name)/$($file.Name)"
            $target=Join-Path $dest $relative
            New-Item -ItemType Directory -Force (Split-Path $target)|Out-Null
            if(Test-Path $target){throw "Existing collected evidence: $target"}
            Copy-Item -LiteralPath $file.FullName -Destination $target
        }
        $hash=$null
        $hashError=$null
        try {$hash=(Get-FileHash -LiteralPath $file.FullName -ErrorAction Stop).Hash}
        catch {$hashError=$_.Exception.Message}
        $files.Add(@{path=$file.FullName;sha256=$hash;hashError=$hashError;bytes=$file.Length;repo=$relative})
    }
}
foreach($file in Get-ChildItem -LiteralPath $Root -Filter 'player-driver-compile-*.log' -File|Where-Object Length -gt 0){
    $files.Add(@{path=$file.FullName;sha256=(Get-FileHash -LiteralPath $file.FullName).Hash;bytes=$file.Length;repo=$null})
}
$runs|ConvertTo-Json -Depth 6|Set-Content -Encoding utf8 (Join-Path $dest 'runs.json')
ConvertTo-Json -InputObject $files -Depth 6|Set-Content -Encoding utf8 (Join-Path $dest 'manifest.json')
