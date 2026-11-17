"""Run isolated R1 Player modes sequentially; never reuse a run directory."""
import argparse, pathlib, sys, subprocess, json, datetime

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--session',required=True)
    ap.add_argument('--player',required=True)
    ap.add_argument('--attempt',required=True)
    ap.add_argument('--modes',default='sort-ugui,sort-imgui,strength0,strength3,preview9,guid,golden,collection,restart')
    ap.add_argument('--restart-from')
    a=ap.parse_args(); session=pathlib.Path(a.session).absolute(); player=pathlib.Path(a.player).absolute()
    tool=pathlib.Path(__file__).with_name('run_r1_player.py').absolute()
    batch=session/a.attempt
    if batch.exists(): raise SystemExit('Refuse reused suite: '+str(batch))
    batch.mkdir(parents=True)
    roots=session/'_roots'/a.attempt; roots.mkdir(parents=True,exist_ok=False)
    results=[]; collection=pathlib.Path(a.restart_from).absolute() if a.restart_from else None
    for mode in a.modes.split(','):
        run_id='UX04B2R1-'+a.attempt+'-'+mode
        args=[sys.executable,str(tool),'--exe',str(player/'WanxiangGuitu.exe'),'--managed',str(player/'WanxiangGuitu_Data'/'Managed'),'--data',str(player/'WanxiangGuitu_Data'),'--run-root',str(roots/mode),'--evidence',str(batch/mode),'--mode',mode,'--run-id',run_id,'--timeout','180']
        if mode=='guid': args+=['--guid-manifest',str(session/'prebuild-audit'/'guid-manifest.json')]
        if mode=='restart':
            if collection is None:
                results.append({'mode':mode,'exitCode':None,'result':'NOT_RUN','reason':'No successful collection root'}); continue
            args+=['--restart-from',str(collection)]
        print('RUN',run_id,flush=True)
        rc=subprocess.run(args).returncode
        results.append({'mode':mode,'runId':run_id,'exitCode':rc,'evidence':str(batch/mode)})
        if mode=='collection' and rc==0: collection=roots/mode
        (batch/'suite-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
    return 0 if results and all(r['exitCode']==0 for r in results) else 1
if __name__=='__main__': raise SystemExit(main())
