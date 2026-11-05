'use strict';

const hooked = new Set();
const pso = new Map();
const lists = new Map();
const unresolved = new Set();
const catalogs = new Map();
let window = null;
let queueCount = 0;
let deviceCount = 0;
const counters = {};
const missing = {};
function count(key){counters[key]=(counters[key]??0)+1;}

function once(address, callback) {
    const key = address.toString();
    if (address.isNull() || hooked.has(key)) return;
    Interceptor.attach(address, callback);
    hooked.add(key);
}
function vtable(object, slot) {
    return object.readPointer().add(slot * Process.pointerSize).readPointer();
}
function wrap(object, slot, callback) {
    once(vtable(object, slot), callback);
}
function success(hr, out) {
    return hr.toInt32() >= 0 && out.compare(ptr(0x10000))>=0 && !out.readPointer().isNull();
}
function iid(guid) {
    return guid.isNull() ? 0 : guid.readU32();
}
function bytecode(address) {
    const pointer = address.readPointer();
    const length = Number(address.add(8).readU64());
    if (length === 0) return null;
    if (pointer.isNull() || length > 32 * 1024 * 1024) throw Error('invalid bytecode');
    const bytes = pointer.readByteArray(length);
    return {sha256:Checksum.compute('sha256',bytes),length,container:pointer.readUtf8String(4)};
}
function shaders(desc, kind) {
    const stages = kind === 'compute' ? ['CS'] : ['VS','PS','DS','HS','GS'];
    const result = {};
    for (let i=0;i<stages.length;i++) {
        const code = bytecode(desc.add(8+16*i));
        if (code) result[stages[i]]=code;
    }
    return result;
}
// x64 SDK layout. Each subobject is pointer-aligned and its payload uses its natural alignment.
const streamLayout = {
 0:[8,8],1:[16,8],2:[16,8],3:[16,8],4:[16,8],5:[16,8],6:[16,8],
 7:[32,8],8:[328,4],9:[4,4],10:[44,4],11:[52,4],12:[16,8],13:[4,4],
 14:[4,4],15:[36,4],16:[4,4],17:[8,4],18:[4,4],19:[16,8],20:[4,4],
 21:[56,4],22:[24,8],24:[16,8],25:[16,8],26:[60,4],27:[44,4],28:[40,4]
};
const streamStage = {1:'VS',2:'PS',3:'DS',4:'HS',5:'GS',6:'CS',24:'AS',25:'MS'};
function stream(desc) {
    const length = Number(desc.readU64());
    const data = desc.add(8).readPointer();
    if (length<8 || length>16384 || data.isNull()) throw Error('invalid stream length');
    const result = {};
    for (let i=0;i<length;) {
        const id = data.add(i).readU32();
        if (!streamLayout[id]) throw Error('unhandled stream subobject '+id+' at '+i);
        const [bytes, alignment]=streamLayout[id];
        const payload=(i+4+alignment-1)&~(alignment-1);
        if (payload+bytes>length) throw Error('truncated stream '+id);
        if (streamStage[id]) {
            const code=bytecode(data.add(payload));
            if (code) result[streamStage[id]]=code;
        }
        i=(payload+bytes+7)&~7;
    }
    return result;
}
function registerPso(pointer, decoded, origin) {
    if (!decoded || !Object.keys(decoded).length) return;
    const canonical = Object.fromEntries(Object.entries(decoded).sort(([a],[b])=>a.localeCompare(b)));
    const key = JSON.stringify(canonical);
    if (!catalogs.has(key)) catalogs.set(key,{id:catalogs.size+1, stages:canonical, origin});
    pso.set(pointer.toString(),catalogs.get(key).id);
}
function hookPso(object, slot, kind, fromLibrary) {
    wrap(object,slot,{
        onEnter(args) {
            count((fromLibrary?"lib-":"create-")+kind);
            this.out=args[fromLibrary?4:3];
            const desc=args[fromLibrary?2:1];
            try { this.decoded = kind==='stream'?stream(desc):shaders(desc,kind); }
            catch (error) { unresolved.add(kind+': '+error); }
        },
        onLeave(hr) {
            if(success(hr,this.out)) {
                const target=this.out.readPointer();
                if(this.decoded && Object.keys(this.decoded).length) pso.delete(target.toString());
                registerPso(target,this.decoded,(fromLibrary?'library-':'create-')+kind);
            }
        }
    });
}
function getList(pointer) {
    const key=pointer.toString();
    if(!lists.has(key)) lists.set(key,{bound:null, calls:new Map(), sequence:[]});
    return lists.get(key);
}
function bind(pointer, pipeline, reset) {
    const list = getList(pointer);
    if(reset) {list.calls.clear(); list.sequence=[];}
    list.bound = pipeline.isNull()?null:pipeline.toString();
}
function hookList(object) {
    wrap(object,10,{
        onEnter(args){this.list=args[0];this.initial=args[2];},
        onLeave(hr){if(hr.toInt32()>=0)bind(this.list,this.initial,true);}
    });
    wrap(object,25,{onEnter(args){count("SetPipelineState");bind(args[0],args[1],false);}});
    for(const [slot,kind] of [[12,'DrawInstanced'],[13,'DrawIndexedInstanced'],[14,'Dispatch'],[59,'ExecuteIndirect']]) {
        wrap(object,slot,{onEnter(args){
            const state=getList(args[0]);
            const id=pso.get(state.bound)??0;
            if(!id){
                count("drawUnresolved:"+(state.bound===null?"no-binding":"unknown-pso"));
                if(state.bound!==null && Object.keys(missing).length<100)
                    missing[state.bound]=(missing[state.bound]??0)+1;
            }
            const key=kind+':'+id;
            state.calls.set(key,(state.calls.get(key)??0)+1);
        }});
    }
    // D3D12 bundles are recorded independently, then nested in a direct list.
    wrap(object,27,{onEnter(args){getList(args[0]).sequence.push(args[1].toString());}});
}
function collect(state, seen) {
    if(!state || seen.has(state)) return;
    const next=new Set(seen).add(state);
    for(const [key,count] of state.calls) window.calls[key]=(window.calls[key]??0)+count;
    for(const nested of state.sequence) collect(lists.get(nested),next);
}
function hookQueue(object) {
    queueCount++;
    wrap(object,10,{onEnter(args){
        if(!window) return;
        window.submissions++;
        const n=args[1].toUInt32();
        for(let i=0;i<n;i++) collect(lists.get(args[2].add(i*8).readPointer().toString()),new Set());
    }});
}
const levels = new Map([
    [0x189819f1,0],[0x77acce80,1],[0x30baa41e,2],[0x81dadc15,3],[0xe865df17,4],[0x8b4f173b,5],
    [0xc70b221b,6],[0x5c014b53,7],[0x9218e6bb,8],[0x4c80e962,9],[0x517f8718,10],
    [0x5405c344,11],[0x5af5c532,12],[0x14eecffc,13],[0x5f6e592d,14]
]);
function hookLibrary(object, level) {
    hookPso(object,9,'graphics',true);
    hookPso(object,10,'compute',true);
    if(level) hookPso(object,13,'stream',true);
    wrap(object,0,{
        onEnter(args){this.iid=iid(args[1]);this.out=args[2];},
        onLeave(hr){if(success(hr,this.out)&&this.iid===0x80eabf42)hookLibrary(this.out.readPointer(),true);}
    });
}
function hookDevice(object, level) {
    deviceCount++;count("device-level-"+level);
    wrap(object,0,{
        onEnter(args){this.level=levels.get(iid(args[1]));this.out=args[2];},
        onLeave(hr){if(this.level!==undefined&&success(hr,this.out))hookDevice(this.out.readPointer(),this.level);}
    });
    wrap(object,8,{
        onEnter(args){this.out=args[3];},
        onLeave(hr){if(success(hr,this.out))hookQueue(this.out.readPointer());}
    });
    hookPso(object,10,'graphics',false);
    hookPso(object,11,'compute',false);
    wrap(object,12,{
        onEnter(args){this.out=args[6];this.initial=args[4];},
        onLeave(hr){if(success(hr,this.out)){const list=this.out.readPointer();hookList(list);bind(list,this.initial,true);}}
    });
    if(level>=1)wrap(object,47,{
        onEnter(args){this.out=args[4];this.level=iid(args[3])===0x80eabf42;},
        onLeave(hr){if(success(hr,this.out))hookLibrary(this.out.readPointer(),this.level);}
    });
    if(level>=2)hookPso(object,50,'stream',false);
    if(level>=4)wrap(object,54,{
        onEnter(args){this.out=args[5];},
        onLeave(hr){if(success(hr,this.out))hookList(this.out.readPointer());}
    });
}
function createDeviceHook(address, factory) {
    once(address,{
        onEnter(args){this.level=levels.get(iid(args[factory?3:2]));this.out=args[factory?4:3];},
        onLeave(hr){if(this.level!==undefined&&success(hr,this.out))hookDevice(this.out.readPointer(),this.level);}
    });
}
function hookFactory(factory) {
    createDeviceHook(vtable(factory,9),true);
}
function unityGraphics(module) {
    const base=module.base;
    const live=new Map();
function readString(o, off) {
    const s = o.add(off);
    const tag = s.add(31).readU8();
    if (tag > 31) throw Error("unexpected string storage");
    return tag === 31 ? "" : s.readUtf8String(31-tag);
}
function settings(o) {
    if (o.isNull() || !o.readPointer().equals(base.add(0x2118550))) return null;
    return {
        graphicsStateCollectionInstanceId: o.add(0xe0).readS32(),
        collectionStartupAction: o.add(0x194).readS32(),
        traceSavePath: readString(o, 0x198),
        traceSendToEditor: o.add(0x1c0).readU8(),
        additionalWarmupCollectionCount: Number(o.add(0xf8).readU64()),
        warmupAsync: o.add(0x1c1).readU8(),
        enableCacheMissTracing: o.add(0x1c8).readU8(),
        warmupProgressivelyLimit: o.add(0x1c4).readS32(),
        cacheMissCollectionPath: readString(o, 0x1d0)
    };
}
function event(kind, o) {
    try {
        const values = settings(o);
        if (values !== null) send({kind, pid:Process.id, utc:new Date().toISOString(), values});
    } catch(error) {
        send({kind:"read-error", at:kind, error:String(error)});
    }
}
    once(base.add(0x16fa330),{onEnter(args){event("graphics-register-startup",args[0]);}});
    once(base.add(0x16fa510),{onEnter(){send({kind:"graphics-startup-begin-trace",pid:Process.id});}});
    once(base.add(0x16fb390),{onEnter(){send({kind:"graphics-startup-warmup",pid:Process.id});}});
    // Exact UnityPlayer.dll only. The descriptor helper receives a complete
    // D3D12_GRAPHICS_PIPELINE_STATE_DESC before either cache load or creation.
    once(base.add(0x11e6010),{
        onEnter(){this.token={};live.set(this.threadId,this.token);},
        onLeave(result){
            live.delete(this.threadId);
            if(!result.isNull() && this.token.shaders){
                count('unity-graphics-descriptor');
                registerPso(result,this.token.shaders,'unity-graphics-descriptor');
            }
        }
    });
    once(base.add(0x11bfae0),{
        onEnter(args){
            if(this.returnAddress.equals(base.add(0x11e602a))) {
                this.token=live.get(this.threadId);
                this.desc=args[1];
            }
        },
        onLeave(){
            if(!this.token) return;
            try{this.token.shaders=shaders(this.desc,'graphics');}
            catch(error){unresolved.add('unity-descriptor: '+error);}
        }
    });
}
function graphics(module) {
    if(module.name.toLowerCase()==='unityplayer.dll') unityGraphics(module);
    if(!['d3d12.dll','d3d12core.dll'].includes(module.name.toLowerCase())) return;
    const create=module.findExportByName('D3D12CreateDevice');
    if(create)createDeviceHook(create,false);
    const get=module.findExportByName('D3D12GetInterface');
    if(get)once(get,{
        onEnter(args){this.out=args[2];this.factory=iid(args[1])===0x61f307d3;this.sdk=iid(args[1])===0x8aaf9303;},
        onLeave(hr){
            if(!success(hr,this.out)) return;
            if(this.factory)hookFactory(this.out.readPointer());
            if(this.sdk)wrap(this.out.readPointer(),4,{
                onEnter(args){this.out=args[4];this.factory=iid(args[3])===0x61f307d3;},
                onLeave(hr){if(this.factory&&success(hr,this.out))hookFactory(this.out.readPointer());}
            });
        }
    });
}
const debug=Process.getModuleByName('kernelbase.dll').getExportByName('OutputDebugStringA');
once(debug,{onEnter(args){
    const msg=args[0].readCString();
    if(msg.startsWith('R7-BEGIN:')) window={label:msg.slice(9),submissions:0,calls:{}};
    if(msg.startsWith('R7-END:')&&window&&window.label===msg.slice(7)) {
        send({kind:'gpu-window',...window});
        window=null;
    }
}});
Process.attachModuleObserver({onAdded:graphics});
rpc.exports={
    report(){
        return {kind:'catalog',deviceCount,queueCount,
            entries:[...catalogs.values()],unresolved:[...unresolved],boundPsoCount:pso.size,counters,missing,known:[...pso.keys()]};
    }
};
send({kind:'gpu-hooks-ready',pid:Process.id});
