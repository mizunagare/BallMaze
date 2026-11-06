param([Parameter(Mandatory)][string]$Source,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
$src=[IO.Path]::GetFullPath($Source)
$out=[IO.Path]::GetFullPath($Output)
if(!$src.StartsWith('I:\WGCombat\', [StringComparison]::OrdinalIgnoreCase) -or !$out.StartsWith('I:\WGCombat\C24B1-1107-A\', [StringComparison]::OrdinalIgnoreCase)){throw 'Synthetic fixtures only'}
$expected=Join-Path $src 'expected.txt'
$container=Join-Path $src 'WanxiangGuitu/ForestRuins'
if(Test-Path -LiteralPath $container){$src=$container}
$dest=Join-Path $out 'WanxiangGuitu/ForestRuins'
if(Test-Path $dest){throw 'Fresh copy required'}
New-Item -ItemType Directory $dest|Out-Null
$items=@(foreach($file in Get-ChildItem -LiteralPath $src -Recurse -File){
    if($file.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Fixture links are forbidden'}
    $relative=[IO.Path]::GetRelativePath($src,$file.FullName)
    $target=Join-Path $dest $relative
    New-Item -ItemType Directory ([IO.Path]::GetDirectoryName($target)) -Force|Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $target
    $a=(Get-FileHash -LiteralPath $file.FullName).Hash
    if($a-ne(Get-FileHash -LiteralPath $target).Hash){throw 'Fixture changed'}
    @{path=$relative;sha256=$a}
})
if(!$items -or !(Test-Path "$dest/save.json")){throw 'No synthetic saved checkpoint'}
if(Test-Path -LiteralPath $expected){Copy-Item -LiteralPath $expected -Destination "$out/expected.txt"}
@{source=$src;files=$items}|ConvertTo-Json -Depth 5|Set-Content "$out/fixture.json"
if(Test-Path -LiteralPath (Join-Path $Source "ground.txt")){Copy-Item -LiteralPath (Join-Path $Source "ground.txt") -Destination (Join-Path $Output "ground.txt")}
