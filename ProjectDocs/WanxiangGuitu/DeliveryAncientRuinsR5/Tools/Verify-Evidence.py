from pathlib import Path
import hashlib, json, re, struct, sys, uuid

root, prior, historical = map(Path, sys.argv[1:4])
audit = root / 'Audit'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()
def write(name, value):
    (audit / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
def pdb_id(path):
    with path.open('rb') as f:
        header = f.read(56)
        assert header.startswith(b'Microsoft C/C++ MSF 7.00')
        block, _, _, count, _, blockmap = struct.unpack_from('<6I', header, 32)
        n = (count + block - 1) // block
        f.seek(blockmap * block)
        pages = struct.unpack(f'<{n}I', f.read(4*n))
        def read_page(p):
            f.seek(p * block)
            return f.read(block)
        directory = b''.join(map(read_page, pages))[:count]
        streams, = struct.unpack_from('<I', directory)
        sizes = struct.unpack_from(f'<{streams}I', directory, 4)
        assert sizes[1] >= 28
        first_stream_pages = 0 if sizes[0] == 0xffffffff else (sizes[0]+block-1)//block
        info_page, = struct.unpack_from('<I', directory, 4 + 4*streams + 4*first_stream_pages)
        info = read_page(info_page)
        age, = struct.unpack_from('<I', info, 8)
        return uuid.UUID(bytes_le=info[12:28]).hex.upper(), age
symbols = []
for name in ('editor-pdb-id.json', 'unitydll-pdb-id.json'):
    pe = load(root / name)[0]
    path = root / 'Symbols' / pe['file']
    guid, age = pdb_id(path)
    matched = (guid, age) == (pe['guid'], pe['age'])
    symbols.append(dict(pdb=pe['file'], sha256=sha(path), bytes=path.stat().st_size,
                        pdbGuid=guid, pdbAge=age, embeddedPeGuid=pe['guid'],
                        embeddedPeAge=pe['age'], match=matched))
write('pdb-identity.json', symbols)
assert all(s['match'] for s in symbols)
release_manifest = load(prior / 'Audit/build-file-hashes.json')
fields = ('EnableUnityConnect', 'EnableCrashReporting', 'EnableInsights',
          'EnableAnalytics', 'EnablePerformanceReporting')
expected = {'C1R5RenderProbe.dll', 'RuntimeInitializeOnLoads.json', 'ScriptingAssemblies.json'}
releases = {}
source_paths = {}
for arm in 'AB':
    key = f'Project{arm}-Build'
    release = prior / key / 'Release'
    record = release_manifest[key]
    source_paths[arm] = release
    def compare(directory):
        actual = {p.relative_to(directory).as_posix(): sha(p) for p in directory.rglob('*') if p.is_file()}
        return sorted(p for p in record.keys() | actual.keys() if record.get(p) != actual.get(p))
    original = compare(release)
    pure = compare(root / f'Pure{arm}/Release')
    sidecar = compare(root / f'Render{arm}/Release')
    bee = load(release / 'WanxiangGuitu.exe.bee.json')
    config = bee['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
    flags = {k: config['Services'][k] for k in fields}
    releases[arm] = dict(root=str(release), files=len(record), originalDelta=original, pureDelta=pure,
                         sidecarDelta=sidecar, exeSHA256=record['WanxiangGuitu.exe'],
                         assemblySHA256=record['WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'],
                         development=config['Development'], services=flags)
    assert not original and not pure and {Path(p).name for p in sidecar} == expected
    assert len(sidecar) == 3 and not config['Development'] and all(v is False for v in flags.values())
write('release-protection.json', releases)
left,right = (release_manifest[f'Project{x}-Build'] for x in 'AB')
different = sorted(p for p in left.keys() | right.keys() if left.get(p) != right.get(p))
write('release-differences.json', [{'path':p,'a':left.get(p),'b':right.get(p)} for p in different])
assert len([p for p in different if p.startswith('WanxiangGuitu_Data/')]) == 5
protected = load(historical)
bad = [x['path'] for x in protected if not Path(x['path']).is_file() or sha(Path(x['path'])) != x['sha256']]
if len(sys.argv) > 5:
    raw, published = map(Path, sys.argv[4:6])
    history = load(published/'manifest.json')
    historic_bad = [x['path'] for x in history if
        sha(raw/x['sourceRelative']) != x['sourceSHA256'] or sha(published/x['path']) != x['publishedSHA256']]
else:
    history, historic_bad = [], []
write('protected-inputs.json', dict(userFiles=len(protected), userMismatch=bad,
                                   r4ManifestEntries=len(history), r4Mismatch=historic_bad))
print(f'Protected files: {len(protected)}; mismatch: {len(bad)}. R4 history: {len(history)}; mismatch: {len(historic_bad)}.')
assert not bad and not historic_bad
