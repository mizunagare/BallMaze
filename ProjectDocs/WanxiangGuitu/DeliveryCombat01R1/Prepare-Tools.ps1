param([Parameter(Mandatory)][string]$ParentRoot)
$ErrorActionPreference='Stop';$parent=[IO.Path]::GetFullPath($ParentRoot);$owner=Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json
if($owner.kind -ne 'PLAYER-02 isolated runtime acceptance'){throw 'Create an explicit isolated owner first'}
if(!(Get-Command dotnet -ErrorAction SilentlyContinue)){throw 'Existing .NET runtime/SDK required; do not install or upgrade'}
New-Item -ItemType Directory "$parent/HostSource","$parent/Host","$parent/ObserverSource","$parent/Observer"|Out-Null
$native=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/NativeProbe'
Copy-Item "$native/*.cs" "$parent/HostSource";Copy-Item "$native/*.csproj" "$parent/HostSource"
$path="$parent/HostSource/DesktopHost.cs";$code=Get-Content $path -Raw
$old='WaitForSingleObject(p.process,0xFFFFFFFF);GetExitCodeProcess(p.process,out uint code);return unchecked((int)code);'
$new='uint wait=WaitForSingleObject(p.process,0xFFFFFFFF);bool known=GetExitCodeProcess(p.process,out uint code);File.WriteAllText(s.Receipt+".native-exit.json",JsonSerializer.Serialize(new{pid=p.pid,waitResult=wait,exitCodeKnown=known,actualExitCode=known?(uint?)code:null,utc=DateTime.UtcNow,phase="native process signaled before desktop handle cleanup"},new JsonSerializerOptions{WriteIndented=true}));return known?unchecked((int)code):2;'
if(!$code.Contains($old)){throw 'Native host observation anchor changed'};Set-Content $path $code.Replace($old,$new) -NoNewline
@{kind='WanxiangGuitu isolated unattended run';source=[IO.Path]::GetFullPath($owner.source);root="$parent/Host";head=$owner.head}|ConvertTo-Json|Set-Content "$parent/Host/owner.json"
dotnet build "$parent/HostSource/NativeProbe.csproj" -c Release -o "$parent/Host/Worker" --nologo;if($LASTEXITCODE){throw 'Host build failed'}
Copy-Item "$PSScriptRoot/Tools/ExitObserver.cs*" "$parent/ObserverSource"
dotnet build "$parent/ObserverSource/ExitObserver.csproj" -c Release -o "$parent/Observer" --nologo;if($LASTEXITCODE){throw 'Observer build failed; existing .NET10 required, do not install runtimes'}
Get-ChildItem "$parent/Host/Worker","$parent/Observer" -File|ForEach-Object {@{path=$_.FullName;bytes=$_.Length;sha256=(Get-FileHash $_.FullName).Hash}}|ConvertTo-Json|Set-Content "$parent/tool-binary-hashes.json"
