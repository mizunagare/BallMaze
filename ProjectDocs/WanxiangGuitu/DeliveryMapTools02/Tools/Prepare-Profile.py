from pathlib import Path
import re,hashlib
doc=Path(__file__).resolve().parents[1]
project=Path('I:/WGCombat/MAPTOOLS02-A/Project')
root=project/'Assets/MT02GeneratedV2'
template=(doc/'LabInputs/Assets/MT02GeneratedV2/LabRelease.asset').read_text(encoding='utf-8')
scenes=['  m_Scenes:\n']
for name in ['MT02Boot','MT02World']:
    meta=(root/(name+'.unity.meta')).read_text(encoding='utf-8')
    guid=re.search(r'guid: ([0-9a-f]{32})',meta).group(1)
    scenes.append(f'  - m_enabled: 1\n    m_path: Assets/MT02GeneratedV2/{name}.unity\n    m_guid: {guid}\n')
assert 'm_BuildProfileEngineDiagnosticsState: 0' in template and 'm_Development: 0' in template and 'm_BuildTarget: 19' in template
text=re.sub(r'  m_Scenes:\n.*?(?=  m_HasScriptingDefines:)', ''.join(scenes),template,flags=re.S)
dest=root/'LabRelease.asset'
if dest.exists():raise SystemExit('Profile exists; never overwrite an existing experiment profile')
dest.write_text(text,encoding='utf-8')
print('created isolated profile',dest,hashlib.sha256(dest.read_bytes()).hexdigest())
