"""Tool tests only: no Player, input, gameplay or human acceptance."""
import argparse,csv,json,uuid
from pathlib import Path
from types import SimpleNamespace as N
import ux_pack as u
from inspect_session import inspect

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();r=u.safe(a.root);out=r/('ToolSelfTest-'+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False);rows=[]
 def check(name,fn):
  try:assert fn();rows.append(dict(test=name,status='PASS'))
  except Exception as e:rows.append(dict(test=name,status='FAIL',error=str(e)))
 def rejects(fn):
  try:fn();return False
  except (ValueError,FileExistsError):return True
 check('191 exact pure release files',lambda:len(u.load(r/'release-files.json'))==191 and u.verify_tree(r/'Release',u.load(r/'release-files.json')) is None)
 check('Complete four-file synthetic collection',lambda:len(u.load(r/'fixture-files.json'))==4 and u.verify_tree(r/'Golden/WanxiangGuitu',u.load(r/'fixture-files.json')) is None)
 for name in ['Sword','Spear','Staff','Bow']:
  s=r/'Sessions'/('Planned-'+name)
  check(name+' fresh has no progress',lambda s=s:inspect(s)['saveState']=='MISSING' and u.load(s/'session.json')['participantId'] is None)
 c=r/'Sessions/Planned-Continue'
 check('Continue identity checksum valid',lambda:inspect(c)['runId']=='82032de5ba5e483ea8ef08629d51b2bf')
 check('Reusing session rejected',lambda:rejects(lambda:u.session(N(root=str(r),session='Planned-Sword',weapon='Sword',fixture='fresh'))))
 check('Traversal session rejected',lambda:rejects(lambda:u.session(N(root=str(r),session='../bad',weapon='Sword',fixture='fresh'))))
 check('Relative path refused',lambda:rejects(lambda:u.safe('relative')))
 check('Real LocalLow refused',lambda:rejects(lambda:u.safe('C:/Users/guan/AppData/LocalLow/test')))
 check('Changed file hash rejected',lambda:rejects(lambda:u.verify_tree(r/'Golden/WanxiangGuitu',[dict(x,sha256='0'*64) for x in u.load(r/'fixture-files.json')])) )
 fake=out/'SyntheticNotHuman';fake.mkdir();u.write(fake/'session.json',dict(sessionId='TOOL_TEST_NOT_HUMAN'));u.write(fake/'process-end.json',dict(exitCode=0))
 u.csv_template(fake/'tasks.csv',['statusClaim'],[dict(statusClaim='NOT_RUN')])
 check('Exit zero cannot imply human PASS',lambda:u.summarize(N(session=str(fake)))['humanStatus']=='NOT_RUN')
 u.csv_template(fake/'tasks.csv',['statusClaim'],[dict(statusClaim='PASS')])
 check('Claim requires independent review',lambda:u.summarize(N(session=str(fake)))['humanStatus']=='AWAITING_INDEPENDENT_REVIEW' and not u.summarize(N(session=str(fake)))['automaticHumanPass'])
 result=dict(scope='PREPARATION TOOL SELFTEST ONLY; no game launched',tests=rows,human='NOT_RUN',nativeUI='NOT_RUN',failed=sum(x['status']=='FAIL' for x in rows));u.write(out/'results.json',result);print(json.dumps(result,ensure_ascii=False));return bool(result['failed'])
if __name__=='__main__':raise SystemExit(main())
