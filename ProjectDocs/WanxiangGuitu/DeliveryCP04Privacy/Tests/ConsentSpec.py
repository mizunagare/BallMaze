"""Executable SECURITY TEST DESIGN only. In-memory fake transport, no network and no product integration."""
import json,hashlib
from pathlib import Path
class Spec:
 def __init__(self,stored=None):self.state='Denied';self.epoch=0;self.reports={};self.calls=[];self.stored=stored;self.confirmed={}
 def grant(self):self.state='Granted';self.epoch+=1
 def deny(self):self.state='Denied';self.epoch+=1;self.confirmed={}
 def add(self,name='r1'):self.reports[name]={'state':'Local','digest':hashlib.sha256(b'synthetic minimal fault').hexdigest()}
 def confirm(self,name):
  if self.state!='Granted' or name not in self.reports:return None
  ticket=(name,self.reports[name]['digest'],self.epoch);self.confirmed[ticket]=True;return ticket
 def send(self,ticket,fail=False):
  if not ticket or self.state!='Granted' or ticket[2]!=self.epoch or ticket not in self.confirmed:return 'Denied'
  name,digest,_=ticket;r=self.reports.get(name)
  if not r or r['digest']!=digest or r['state'] in ['Sending','Sent','Unknown']:return 'Rejected'
  del self.confirmed[ticket];r['state']='Sending';self.calls.append({'report':name,'digest':digest,'authorized':True})
  r['state']='Failed' if fail else 'Sent';return r['state']
 def delete(self,name):self.reports.pop(name,None);self.confirmed={t:v for t,v in self.confirmed.items() if t[0]!=name}
rows=[]
def case(name,fn):
 try:fn();rows.append({'case':name,'modelStatus':'PASS','productStatus':'NOT_RUN'})
 except Exception as e:rows.append({'case':name,'modelStatus':'FAIL','productStatus':'NOT_RUN','error':str(e)})
def denied(kind):
 s=Spec();s.add();s.deny() if kind in ['rejected','skipped'] else None;assert s.send(s.confirm('r1'))=='Denied' and not s.calls
case('first_start_without_consent',lambda:denied('fresh'))
case('user_rejects',lambda:denied('rejected'))
case('user_skips_or_closes',lambda:denied('skipped'))
def corrupt():
 try:json.loads('{broken')
 except ValueError:s=Spec(stored='invalid')
 s.add();assert s.state=='Denied' and s.send(s.confirm('r1'))=='Denied' and not s.calls
case('corrupt_consent_store',corrupt)
def revoke():
 s=Spec();s.add();s.grant();ticket=s.confirm('r1');s.deny();assert s.send(ticket)=='Denied' and not s.calls
case('withdraw_before_dispatch',revoke)
def oldqueue():
 s=Spec(stored={'historical':'Granted'});s.add();assert s.state=='Denied' and not s.calls and s.send(s.confirm('r1'))=='Denied'
case('old_queue_currently_denied',oldqueue)
def failed():
 s=Spec();s.add();s.grant();t=s.confirm('r1');assert s.send(t,True)=='Failed';assert s.send(t)=='Denied' and len(s.calls)==1 and 'r1' in s.reports
case('authorized_upload_failure_no_autoretry',failed)
def delete():
 s=Spec();s.add();s.grant();t=s.confirm('r1');s.delete('r1');assert s.send(t)=='Denied' and not s.calls
case('user_deletes_report',delete)
case('restart_requires_fresh_session_consent',oldqueue)
def twice():
 s=Spec();s.add();s.grant();t=s.confirm('r1');assert s.send(t)=='Sent';s.send(t);s.send(s.confirm('r1'));assert len(s.calls)==1
case('double_click_single_attempt',twice)
def changed():
 s=Spec();s.add();s.grant();t=s.confirm('r1');s.reports['r1']['digest']='changed';assert s.send(t)=='Rejected' and not s.calls
case('preview_content_changes_invalidates_ticket',changed)
def positive():
 s=Spec();s.add();s.grant();assert s.send(s.confirm('r1'))=='Sent' and len(s.calls)==1
case('positive_explicit_consent_and_send',positive)
out={'layer':'DESIGN_MODEL_ONLY_NO_REAL_UPLOAD','policy':'Denied at each process start; stored grant is history, not an automatic send credential','warning':'No product DiagnosticConsent/Store/Uploader implemented. No real UI/network/persistence/race guarantee validated.','rows':rows}
p=Path('I:/WGCombat/CP04PRIVACY-1103-A/model-results.json');p.write_text(json.dumps(out,indent=2));print(len(rows),'design-model cases',sum(x['modelStatus']=='PASS' for x in rows),'PASS; product all NOT_RUN');raise SystemExit(any(x['modelStatus']=='FAIL' for x in rows))
