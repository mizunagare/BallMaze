import sys,json
from pathlib import Path
sys.path.insert(0,'I:/WGCombat/CP04BR2-1102-A/PythonLib');import pefile
p=Path('I:/WGCombat/CP04BR-1102-A/FixedBuildAudit/Release/MonoBleedingEdge/EmbedRuntime/mono-2.0-bdwgc.dll');pe=pefile.PE(str(p));out=[x.name.decode() for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name and any(k in x.name.decode() for k in ['mono_profiler','mono_object_get_size'])];Path('I:/WGCombat/CP04BR2-1102-A/mono-exports.json').write_text(json.dumps(out,indent=2));print('\n'.join(out[:35]))
