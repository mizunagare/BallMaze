"""Portable evidence verifier. Requires only this repository metadata and the two received ZIPs."""
import argparse,csv,hashlib,json,os,pathlib,zipfile
def native(p):
    p=p.resolve()
    return pathlib.Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def sha(p):
    h=hashlib.sha256()
    with native(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--package-dir',required=True,type=pathlib.Path);parser.add_argument('--extract-root',required=True,type=pathlib.Path)
    args=parser.parse_args();repo=pathlib.Path(__file__).resolve().parents[4]
    control=pathlib.Path(__file__).resolve().parent
    receipts=json.loads((control/'PACKAGE_RECEIPTS.json').read_text(encoding='utf-8'))
    assert not native(args.extract_root).exists(),'Use a new isolated extraction root; never overlay a repository'
    native(args.extract_root).mkdir(parents=True)
    result=[]
    for receipt in receipts['packages']:
        archive=args.package_dir/receipt['archiveFileName'];assert native(archive).stat().st_size==receipt['archiveBytes'] and sha(archive)==receipt['archiveSha256']
        manifest=repo/receipt['manifestRepositoryPath'];assert sha(manifest)==receipt['manifestSha256']
        with native(manifest).open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
        assert len(rows)==receipt['payloadFiles'] and len({r['Path'] for r in rows})==len(rows)
        out=args.extract_root/receipt['kind'];native(out).mkdir()
        with zipfile.ZipFile(native(archive)) as z:
            assert z.testzip() is None and len(z.namelist())==len(rows) and set(z.namelist())=={x['Path'] for x in rows}
            for row in rows:
                rel=pathlib.PurePosixPath(row['Path']);assert not rel.is_absolute() and '..' not in rel.parts
                p=out/pathlib.Path(*rel.parts);assert p.resolve().is_relative_to(out.resolve())
                data=z.read(row['Path']);assert len(data)==int(row['Bytes']) and hashlib.sha256(data).hexdigest()==row['Sha256']
                native(p.parent).mkdir(parents=True,exist_ok=True);native(p).write_bytes(data)
        actual={p.relative_to(native(out)).as_posix() for p in native(out).rglob('*') if p.is_file()}
        assert actual=={r['Path'] for r in rows}
        for row in rows:
            p=out/row['Path'];assert native(p).stat().st_size==int(row['Bytes']) and sha(p)==row['Sha256']
        result.append({'archiveFileName':receipt['archiveFileName'],'archiveSha256':sha(archive),'payloadFiles':len(rows),
          'zeroByteFiles':sum(int(r['Bytes'])==0 for r in rows),'extractedAt':str(out.resolve()),'status':'PASS_EXACT_SET_SIZE_SHA256'})
    print(json.dumps({'status':'PASS_LOCAL_FRESH_EXTRACT','verifierSourceSha256':sha(pathlib.Path(__file__)),'results':result,'externalTransfer':'NOT_VERIFIED_BY_THIS_LOCAL_TEST'},ensure_ascii=False))
if __name__=='__main__':main()
