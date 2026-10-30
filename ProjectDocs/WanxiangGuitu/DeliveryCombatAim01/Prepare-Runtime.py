from pathlib import Path
import re,json,hashlib,sys,subprocess
root=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve();buildName=sys.argv[3] if len(sys.argv)>3 else 'AimBuild'
assert str(root).lower().replace('\\','/').startswith('i:/wgcombat/') and (root/'owner.json').is_file() and re.fullmatch(r'[A-Za-z0-9_-]+',buildName)
clone=root/'F/Project'
probe=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"name='Unity.exe'\" | Select-Object -ExpandProperty CommandLine"],text=True,encoding='utf-8',errors='replace')
assert str(clone).lower().replace('\\','/') not in probe.lower().replace('\\','/'),'Owned clone occupied; preserve process'
dest=clone/'Assets/Player02AcceptanceOnly';dest.mkdir(exist_ok=True)
base=repo/'ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Tests/PlayerAcceptanceDriver.cs.txt'
s=base.read_text(encoding='utf-8-sig').replace('sealed class PlayerAcceptanceDriver','sealed partial class PlayerAcceptanceDriver')
s=s.replace('if(mode=="Observe")','if(File.Exists(Path.Combine(root,"aim01-config.json"))){yield return Aim01Run();yield break;} if(mode=="Observe")')
s,n=re.subn(r'Vector2 AimDelta\(Vector3 goal\)\{[^\n]*\}', 'Vector2 AimDelta(Vector3 goal){return Aim01Delta(goal);}',s)
assert n==1 and 'yield return Aim01Run()' in s
(dest/'PlayerAcceptanceDriver.cs').write_text(s,encoding='utf-8')
scenario=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombatAim01/Tests/Aim01Scenarios.cs.txt'
(dest/'Aim01Scenarios.cs').write_bytes(scenario.read_bytes())
build=root/'Runtime/T'/buildName;build.mkdir(parents=True,exist_ok=True)
(build/'owner.json').write_text(json.dumps(dict(variant='Acceptance',source=str(repo),scope='AIM01 isolated nondevelopment runtime acceptance, not native/human')),encoding='utf-8')
(build/'driver-inputs.json').write_text(json.dumps(dict(base=str(base),baseSha256=hashlib.sha256(base.read_bytes()).hexdigest(),files=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in dest.glob('*.cs')]),indent=2),encoding='utf-8')
