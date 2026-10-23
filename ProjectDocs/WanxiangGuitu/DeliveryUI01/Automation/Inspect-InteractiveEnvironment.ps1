# Read-only inventory. Never treats an active user console or an RDP client as authorization.
[CmdletBinding()]
param([Parameter(Mandatory)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$target = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $target) { throw 'OutputDirectory must be new; no existing evidence is overwritten.' }
New-Item -ItemType Directory -Path $target | Out-Null
$commands = @('VBoxManage','vmrun','vmconnect','mstsc','cdb','windbg','windbgx','dumpchk')
$services = @(Get-Service -Name vmms,vmcompute,TermService,VMAuthdService,VMnetDHCP,VBoxSDS -ErrorAction SilentlyContinue | ForEach-Object {
    [pscustomobject]@{name=$_.Name; status=$_.Status.ToString()}
})
$sessionText = (& quser 2>&1 | Out-String)
$sessionExit = $LASTEXITCODE
$inventory = [ordered]@{
    observedUtc = [datetime]::UtcNow.ToString('o')
    scope = 'Read-only local discovery; no login, activation, input, Player launch or save access'
    sessions = $sessionText
    sessionCommandExitCode = $sessionExit
    observerSessionId = (Get-Process -Id $PID).SessionId
    computer = Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,HypervisorPresent
    services = $services
    tools = @($commands | ForEach-Object {
        $found = Get-Command $_ -ErrorAction SilentlyContinue
        [pscustomobject]@{name=$_; path=if($found){$found.Source}else{$null}}
    })
    sandboxPresent = Test-Path "$env:windir/System32/WindowsSandbox.exe"
    virtualMachineProcesses = @(Get-Process -Name vmware-vmx,VirtualBoxVM,VBoxHeadless,vmconnect,WindowsSandbox,mstsc -ErrorAction SilentlyContinue | Select-Object ProcessName,Id,SessionId)
    playerProcesses = @(Get-Process -Name WanxiangGuitu -ErrorAction SilentlyContinue | Select-Object ProcessName,Id,SessionId)
    authorization = 'NOT_ESTABLISHED: discovery cannot grant an exclusive session lease or remote-host permission'
    nativeU16 = 'NOT_RUN: inventory is not native input or semantic verification'
}
$inventory | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $target 'environment.json') -Encoding utf8
Write-Output (Join-Path $target 'environment.json')
# Successful inventory is not U16 PASS. A discovered VM still requires an explicit exclusive lease.
