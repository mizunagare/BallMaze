param([Parameter(Mandatory)][string]$Delivery)
$ErrorActionPreference='Stop'
$Delivery=(Resolve-Path -LiteralPath $Delivery).Path
$ev=Join-Path $Delivery 'EVIDENCE'
function Relative($path) { [IO.Path]::GetRelativePath($Delivery,$path).Replace('\','/') }
function ReadJson($path) {
    if (Test-Path -LiteralPath $path -PathType Leaf) {Get-Content -Raw -Encoding utf8 -LiteralPath $path | ConvertFrom-Json}
}
$rows=foreach($run in Get-ChildItem $ev -Directory | Where-Object Name -Like 'UX05-*' | Sort-Object Name){
    $meta=ReadJson (Join-Path $run.FullName 'manifest.json')
    if (!$meta){continue}
    $wrapperPath=Join-Path $run.FullName 'result.json'
    if (!(Test-Path -LiteralPath $wrapperPath)){$wrapperPath=Join-Path $run.FullName 'run-summary.json'}
    $wrapper=ReadJson $wrapperPath
    $probe=Join-Path $run.FullName 'probe/result.json'
    if (!(Test-Path -LiteralPath $probe)){$probe=Join-Path $run.FullName 'contract-result.json'}
    if (!(Test-Path -LiteralPath $probe)){$probe=Join-Path $run.FullName 'root/result.json'}
    if (!(Test-Path -LiteralPath $probe)){$probe=Join-Path $run.FullName 'review-result.json'}
    $raw=ReadJson $probe
    $scope=$raw.reason
    if (!$scope){$scope=$raw.failReason}
    if (!$scope){$scope=$meta.scope}
    $status='OBSERVED_STARTUP_ONLY'
    $rawStatus=$raw.status
    if ($raw -and $raw.PSObject.Properties.Name -contains 'pass') {
        $rawStatus=if($raw.pass){'PASS'}else{'FAIL'}
    }
    if ($rawStatus){$status=$rawStatus}
    if($run.Name -eq 'UX05-20261119-CONTRACT-A01' -and !$raw){$status='FAIL_LAUNCH'}
    if($run.Name -like '*LOCK-CONTENDER*' -and $rawStatus -eq 'FAIL' -and
       (Select-String -LiteralPath (Join-Path $run.FullName 'probe/events.jsonl') -Pattern '"detail":"Blocked"' -Quiet)){
        $status='EXPECTED_NEGATIVE_BLOCKED'
    }
    if(Test-Path -LiteralPath (Join-Path $run.FullName 'cut-observation.txt')){
        $status='PROCESS_CUT_WITNESSED'
        $scope='Observed before page publication and terminated isolated PID. See cut-observation.txt.'
        if($run.Name -like 'UX05-R1-*'){
            $point=ReadJson (Join-Path $run.FullName 'cut-observation.txt')
            $scope="Observed $($point.phase) and terminated only the isolated PID. See cut-observation.txt."
        }
    }
    if($wrapper.timedOut){$status='FAIL_TIMEOUT'}
    if($run.Name -like 'UX05-R1-*' -and !$raw -and !$wrapper -and $status -ne 'PROCESS_CUT_WITNESSED'){
        $status='INCOMPLETE_EVIDENCE'
        $scope='Started; the host did not leave a complete run receipt. See the R1 completion report.'
    }
    $retest=switch($run.Name){
        'UX05-R1-CANDIDATE2-A01' {'UX05-R1-C3-A01'}
        'UX05-R1-UI-UGUI-A01' {'UX05-R1-UI-UGUI-A02'}
        'UX05-R1-UI-IMGUI-A01' {'UX05-R1-UI-IMGUI-A02'}
        'UX05-R1-UI-IMGUI-A02' {'UX05-R1-UI-IMGUI-A03'}
        'UX05-R1-UI-IMGUI-A03' {'UX05-R1-UI-IMGUI-A04'}
        'UX05-R1-B1B2-A01' {'UX05-R1-B1B2-A02'}
        'UX05-20261119-UX03-spear-charge-R1-A01' {'UX05-20261119-UX03-spear-charge-R1-A02'}
        'UX05-20261119-UX03-spear-sweep-R1-A01' {'UX05-20261119-UX03-spear-sweep-R1-A02'}
        'UX05-20261119-CONTRACT-A01' {'UX05-20261119-CONTRACT-A02'}
        'UX05-20261119-MIGRATE-A02' {'UX05-20261119-MIGRATE-A04'}
        'UX05-20261119-UX03-sword-triple-A01' {'UX05-20261119-UX03-sword-triple-A02'}
    }
    $superseded=ReadJson (Join-Path $run.FullName 'superseded-observation.json')
    if($superseded) {
        $status=$superseded.outcome
        $scope=$superseded.reason
        $retest=$superseded.supersededBy
    }
    $exitCode=if($null -ne $wrapper.exitCode){$wrapper.exitCode}else{$raw.exitCode}
    [pscustomobject]@{
        run_id=$run.Name;pid=$meta.pid;build_id=$(if($meta.buildId){$meta.buildId}else{'UX05-HistoryContract-Mono'})
        status=$status;probe_raw_status=$rawStatus;exit_code=$exitCode;scope=$scope;superseded_by=$retest
        manifest=(Relative (Join-Path $run.FullName 'manifest.json'))
        raw_result=$(if($raw){Relative $probe}elseif($wrapper){Relative $wrapperPath}else{''})
    }
}
$rows | Export-Csv -LiteralPath (Join-Path $Delivery 'PLAYER_RUN_MATRIX.csv') -Encoding utf8 -NoTypeInformation
$manifest=foreach($f in Get-ChildItem $ev -Recurse -File | Where-Object {$_.Name -ne 'INDEX.json'} | Sort-Object FullName){
    @{path=(Relative $f.FullName);bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName).Hash}
}
@{version=1;branch='feature/ux-progression-05-objective-history';base='ae705b944b7d0fe851fbd395229dfc30ec636f5c';runCount=@($rows).Count;files=@($manifest)} |
    ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $ev 'INDEX.json') -Encoding utf8
$rows | Group-Object status | Select-Object Name,Count

