import pathlib, json, hashlib, gzip, os, collections
R = pathlib.Path.cwd()
D = R / 'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation'
O = D / 'EVIDENCE/R2'
original = json.loads((O / 'driver-search.json').read_text())
targets = set(original['matches'])
matches, inventory, errors = [], [], []
stats = collections.Counter()

def longpath(p):
    return pathlib.Path(chr(92)*2 + '?' + chr(92) + str(p.resolve()))

def scan(p, label):
    digest = hashlib.sha256()
    with longpath(p).open('rb') as f:
        while True:
            block = f.read(1024*1024)
            if not block:
                break
            digest.update(block)
    h = digest.hexdigest().upper()
    stats['files'] += 1
    if h in targets:
        matches.append({'location': label, 'sha256': h})
    return h

for e in original['errors']:
    p = R/e['path']
    try:
        scan(p, e['path'])
        stats['long_path_recovered'] += 1
    except Exception as ex:
        errors.append({'path': e['path'], 'error': str(ex)})
for entry in original['inventory']:
    if entry['kind'] == 'archive' and entry['path'].endswith('.gz'):
        with gzip.open(R/entry['path'], 'rb') as f:
            data = f.read()
        h = hashlib.sha256(data).hexdigest().upper()
        if h in targets:
            matches.append({'location': entry['path']+'!gzip', 'sha256': h})
        inventory.append({'path': entry['path'], 'status': 'GZIP_READ', 'sha256': h, 'size': len(data)})
for base, dirs, files in os.walk(R):
    dirs[:] = [n for n in dirs if n not in {'.git','Temp','node_modules','.vs','.idea','UserSettings','Packages'} and (pathlib.Path(base)/n).resolve() != O.resolve()]
    for name in files:
        f = pathlib.Path(base)/name
        try:
            n = longpath(f).stat().st_size
            cached = 'Library' in f.parts and f.suffix.lower() in {'.rsp','.ps1','.psm1','.cs','.py','.pdb'}
            large = n > 64*1024*1024 and f.suffix.lower() in {'.dll','.exe','.pdb','.ps1','.psm1','.cs','.py','.log','.txt','.json','.jsonl','.bak'}
            if not (cached or large):
                continue
            rel = f.relative_to(R).as_posix()
            h = scan(f, rel)
            stats['cached' if cached else 'large'] += 1
            if f.suffix.lower() == '.rsp':
                inventory.append({'path': rel, 'kind': 'cached_compiler_response', 'sha256': h, 'size': n, 'launcherCompilation': 'N/A interpreted PowerShell source'})
        except Exception as ex:
            errors.append({'path': str(f), 'error': str(ex)})
report = {'stats': dict(stats), 'matches': matches, 'inventory': inventory, 'errors': errors, 'scope': 'cached Library sources/PDB/compiler responses, large binaries and recoverable source files, gzip and long-path supplement; exact SHA matching only'}
(O/'driver-search-supplement.json').write_text(json.dumps(report, ensure_ascii=True, indent=2))
print(json.dumps({'stats': dict(stats), 'matches': len(matches), 'errors': len(errors), 'responseCount': len(inventory)}))
