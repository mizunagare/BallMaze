import hashlib
import json
from pathlib import Path
import sys
import time

import frida

run = Path(sys.argv[1])
receipt = run / 'Player.desktop-process.json'
script_path = Path(__file__).with_suffix('.js')
expected = '3bdc6e4cd1b5eb85e1562b1c6018949145cdedf50cf7aceab0d1518143f9aa7c'
deadline = time.monotonic() + 35
while not receipt.is_file() and time.monotonic() < deadline:
    time.sleep(.025)
data = json.loads(receipt.read_text('utf-8-sig'))
assert not data['inputDesktopActive'] and data['desktop'].startswith('WGTest_')
dll = Path(data['exe']).with_name('UnityPlayer.dll')
assert hashlib.sha256(dll.read_bytes()).hexdigest() == expected
out = run / 'native-readback.jsonl'
def event(payload):
    with out.open('a',encoding='utf-8') as file:
        file.write(json.dumps(payload)+'\n')
session = frida.attach(data['pid'])
script = session.create_script(script_path.read_text('utf-8'))
script.on('message',lambda message,_: event(message.get('payload',message)))
script.load()
try:
    while time.monotonic() < deadline:
        values = script.exports_sync.read()
        if values is not None:
            event(dict(kind='native-live-object',pid=data['pid'],values=values))
            break
        time.sleep(.04)
    else:
        raise TimeoutError('No GraphicsSettings instance before deadline')
    # Keep startup hooks registered through title capture.
    while not (run/'render-complete.txt').exists() and time.monotonic()<deadline:
        time.sleep(.05)
finally:
    if not session.is_detached:
        session.detach()
