// External Windows input only; invoked one action at a time after observing the returned screenshot.
// Screenshot bytes are saved as requested immutable run evidence, never used to infer hidden product state.
globalThis.releaseStep=0;
globalThis.releaseObserve=async function(label){
 globalThis.releaseState=await sky.get_window_state({window:releaseWindow});
 for(const shot of releaseState.screenshots??[]){
   const match=/^data:image\/([a-z]+);base64,(.*)$/s.exec(shot.url);
   if(match)await fs.writeFile(releaseDir+'/'+String(releaseStep).padStart(3,'0')+'-'+label+'.'+match[1],Buffer.from(match[2],'base64'));
 }
 await fs.appendFile(releaseDir+'/observations.jsonl',JSON.stringify({step:releaseStep,label,utc:new Date().toISOString(),window:releaseState.window,screenshotIds:releaseState.screenshots.map(s=>s.id)})+'\n');
};
globalThis.releaseClick=async function(label,x,y){
 const before=releaseState;if(!before?.screenshots?.[0]?.id)throw new Error('Fresh observed screenshot required');
 const n=++releaseStep;
 await fs.appendFile(releaseDir+'/native-inputs.jsonl',JSON.stringify({step:n,label,type:'click',x,y,window:before.window,screenshotId:before.screenshots[0].id,utc:new Date().toISOString()})+'\n');
 releaseState=null;await sky.click({window:before.window,screenshotId:before.screenshots[0].id,x,y});await new Promise(r=>setTimeout(r,350));
 await releaseObserve(label);
};
globalThis.releaseKey=async function(label,key){
 const before=releaseState;if(!before)throw new Error('Observe before key');
 ++releaseStep;await fs.appendFile(releaseDir+'/native-inputs.jsonl',JSON.stringify({step:releaseStep,label,type:'key',key,window:before.window,utc:new Date().toISOString()})+'\n');
 releaseState=null;await sky.press_key({window:before.window,key});await new Promise(r=>setTimeout(r,350));await releaseObserve(label);
};
