import json
from pathlib import Path
import sys
import threading
import time
import frida

run, script_path = map(Path, sys.argv[1:])
receipt = run / "Editor.desktop-process.json"
deadline = time.monotonic() + 20
while not receipt.is_file():
    if time.monotonic() > deadline:
        raise TimeoutError(receipt)
    time.sleep(.1)
for attempt in range(30):
    try:
        pid = json.loads(receipt.read_text(encoding="utf-8-sig"))["pid"]
        break
    except (ValueError, KeyError):
        time.sleep(.1)
else:
    raise ValueError("No actual editor PID")

closed = threading.Event()
with (run / "native-stacks.jsonl").open("w", encoding="utf-8", buffering=1) as output:
    session = frida.attach(pid)
    def detached(*args):
        output.write(json.dumps(dict(event="detached", pid=pid, details=[str(x) for x in args])) + "\n")
        closed.set()
    session.on("detached", detached)
    agent = session.create_script(script_path.read_text(encoding="utf-8-sig"))
    def message(msg, data):
        output.write(json.dumps(msg.get("payload", msg), ensure_ascii=False) + "\n")
    agent.on("message", message)
    agent.load()
    if not closed.wait(1050):
        session.detach()
        raise TimeoutError("Trace stopped without terminating editor")
