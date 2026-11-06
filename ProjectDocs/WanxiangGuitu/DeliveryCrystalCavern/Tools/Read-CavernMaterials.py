import hashlib
import json
from pathlib import Path
import sys

import UnityPy

root=Path(sys.argv[1])
path=root/'PureBuild2/Release/WanxiangGuitu_Data/resources.assets'
names={'Basalt','Slate','Rift','Vein','EnergyRecovery','EnergyWarning','EnergyActive'}
rows={}
for entry in UnityPy.load(str(path)).objects:
    if entry.type.name!='Material' or entry.peek_name() not in names:
        continue
    value=entry.read_typetree()
    assert value['m_Name'] not in rows
    rows[value['m_Name']]=dict(pathId=entry.path_id,sha256=hashlib.sha256(entry.get_raw_data()).hexdigest(),
        shader=value['m_Shader'],keywords=value['m_ValidKeywords'],
        colors=[v for v in value['m_SavedProperties']['m_Colors'] if v[0] in ('_BaseColor','_EmissionColor')])
assert set(rows)==names and len({tuple(m['shader'].values()) for m in rows.values()})==1
assert all('_EMISSION' not in m['keywords'] for m in rows.values())
(root/'Audit/packaged-cavern-materials.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
