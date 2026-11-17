import json
from pathlib import Path
p=Path("Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/isolated-save/save.json")
d=json.loads(json.loads(p.read_text(encoding="utf-8-sig"))["payload"])
print(json.dumps(d["profile"],ensure_ascii=False,indent=2))
