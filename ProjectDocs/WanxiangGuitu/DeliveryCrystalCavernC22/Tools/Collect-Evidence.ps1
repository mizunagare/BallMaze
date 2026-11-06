param([string]$Root='I:/WGCombat/C22-1106-A')
$ErrorActionPreference='Stop'
$dest=Join-Path (Split-Path $PSScriptRoot) 'Evidence'
New-Item -ItemType Directory -Force $dest|Out-Null
$files=[Collections.Generic.List[object]]::new()
$runs=[ordered]@{}
$names=@('process.json','complete.txt','failure.txt','fixture.json','expected.txt','pure-runtime.json','entry-audit.jsonl','close-delivery.json','modal-cleanup.json','Editor.command.json','Player.command.json','Editor.desktop-process.json','Player.desktop-process.json')
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
        $runs[$run.Name]=$result
    }
    foreach($file in Get-ChildItem -LiteralPath $run.FullName -File|Sort-Object Name){
        if($file.Extension -notin '.log','.tsv','.png' -and $file.Name -notin $names){continue}
        $relative=$null
        if($file.Extension -ne '.log'){
            $relative="Raw/$($run.Name)/$($file.Name)"
            $target=Join-Path $dest $relative
            New-Item -ItemType Directory -Force (Split-Path $target)|Out-Null
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
