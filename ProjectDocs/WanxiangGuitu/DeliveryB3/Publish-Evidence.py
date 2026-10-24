"""Reuse the B2 redacted diagnostic publisher; add B3 assertions only."""
import argparse, importlib.util, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--run',type=Path,required=True)
p.add_argument('--target',type=Path,required=True)
a=p.parse_args()
here=Path(__file__).resolve().parent
if a.target.exists():p.error('Fresh evidence target required')
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB2/Publish-Evidence.py'),
                '--run',str(a.run),'--target',str(a.target)],check=True)
path=here.parent/'DeliveryUI01/Automation/publish-evidence.py'
spec=importlib.util.spec_from_file_location('reviewed_diagnostic_publisher',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
names=['Rules/b3-results.txt','Rules/b3-stream-results.txt','Normal/b3-normal-streams.txt']
m.publish(a.run,a.target/'B3Assertions',[n for n in names if (a.run/n).is_file()])
