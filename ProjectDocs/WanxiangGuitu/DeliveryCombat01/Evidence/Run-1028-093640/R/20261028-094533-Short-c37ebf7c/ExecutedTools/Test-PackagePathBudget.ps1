[CmdletBinding()]
param([Parameter(Mandatory)][string]$SourceProject,[Parameter(Mandatory)][string]$WorkProject)
$ErrorActionPreference='Stop'
$version=Get-Content -LiteralPath (Join-Path $SourceProject 'ProjectSettings/ProjectVersion.txt') -Raw
$lock=Get-Content -LiteralPath (Join-Path $SourceProject 'Packages/packages-lock.json') -Raw|ConvertFrom-Json
$supported=$version -match 'm_EditorVersion: 6000\.6\.5f1\s' -and $lock.dependencies.'com.unity.render-pipelines.core'.version -eq '17.6.0' -and $lock.dependencies.'com.unity.render-pipelines.universal'.version -eq '17.6.0'
# These are actual locked-package importer inputs, not an arbitrary project-prefix limit.
# Cache folder hash widths and the longest USS/UXML/URT input were audited in BUILD-01.
$probes=@(
 'Library/PackageCache/com.unity.render-pipelines.core@285af6b8c83f/Editor/Lighting/ProbeVolume/RenderingLayerMask/TraceRenderingLayerMask.urtshader',
 'Library/PackageCache/com.unity.render-pipelines.core@285af6b8c83f/Editor-PrivateShared/Tools/Converter/Window/RenderPipelineConverterVisualElementListFilter.uxml',
 'Library/PackageCache/com.unity.render-pipelines.core@285af6b8c83f/Editor-PrivateShared/Tools/Converter/Window/RenderPipelineConverterVisualElementListFilter.uss',
 'Library/PackageCache/com.unity.render-pipelines.core@285af6b8c83f/Runtime/PathTracing/Shaders/LightmapDirectDirectionalAndEnvironmentIntegration.urtshader',
 'Library/PackageCache/com.unity.render-pipelines.universal@2309ae255609/Editor/2D/Profiler/UI/U2DGraphicsHierarchyView/U2DGraphicsHierarchyView.uss',
 'Library/PackageCache/com.unity.render-pipelines.universal@2309ae255609/Editor/2D/Profiler/UI/U2DGraphicsStatisticView/U2DGraphicsStatisticView.uxml')
$paths=@($probes|ForEach-Object {$p=[IO.Path]::GetFullPath((Join-Path $WorkProject $_));[pscustomobject]@{relative=$_;full=$p;length=$p.Length;safe=$p.Length -lt 260}})
$unsafe=@($paths|Where-Object {!$_.safe})
[pscustomobject]@{allowed=$supported -and !$unsafe.Count;supportedInput=$supported;project=[IO.Path]::GetFullPath($WorkProject);limitExclusive=260;paths=$paths;reason=$(if(!$supported){'PACKAGE_PATH_POLICY_UNREVIEWED_INPUT: re-audit this tool policy for changed Unity/Core/URP'}elseif($unsafe.Count){'PACKAGE_PATH_BUDGET_EXCEEDED: choose a shorter external TestRoot before importing; never change system long-path settings or patch PackageCache'}else{'Known importer paths fit; this is not a guarantee for all future package assets'})}
