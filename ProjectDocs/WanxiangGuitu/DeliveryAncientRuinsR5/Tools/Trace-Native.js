'use strict';
const targets = /(?:EditorBuildSettings|GraphicsSettings)\.asset(?:$|[.~])/i;
const files = new Map();
const hooks = [];
function string(p, n) {
  if (p.isNull()) return "";
  try { return n === undefined ? p.readUtf16String() : p.readUtf16String(n); } catch (_) { return ""; }
}
function trace(ctx) {
  return Thread.backtrace(ctx, Backtracer.ACCURATE).map(addr => {
    const module = Process.findModuleByAddress(addr);
    return {address: addr.toString(), module: module ? module.name : null,
            modulePath: module ? module.path : null, rva: module ? addr.sub(module.base).toString() : null};
  });
}
function report(event, args, ctx) {
  send({event, args, thread: Process.getCurrentThreadId(), utc: new Date().toISOString(), stack: trace(ctx)});
}
function intercept(module, name, callbacks) {
  const dll = Process.findModuleByName(module);
  const address = dll && dll.findExportByName(name);
  if (!address) return;
  Interceptor.attach(address, callbacks);
  hooks.push(module + "!" + name);
}
intercept("KERNELBASE.dll", "CreateFileW", {
  onEnter(args) {
    const path = string(args[0]);
    if (!targets.test(path)) return;
    this.path = path;
    const access = args[1].toUInt32();
    if ((access & 0x40000000) !== 0 || (access & 0x116) !== 0 || args[4].toUInt32() !== 3)
      report("CreateFileW-write", {path, access, disposition: args[4].toUInt32()}, this.context);
  },
  onLeave(ret) {
    if (this.path && !ret.isNull() && !ret.equals(ptr("0xffffffffffffffff"))) files.set(ret.toString(), this.path);
  }
});
intercept("KERNELBASE.dll", "WriteFile", {
  onEnter(args) {
    const path = files.get(args[0].toString());
    if (path) report("WriteFile", {path, bytes: args[2].toUInt32()}, this.context);
  }
});
intercept("KERNELBASE.dll", "CloseHandle", {onEnter(args) { files.delete(args[0].toString()); }});
for (const name of ["MoveFileExW","ReplaceFileW"]) {
  intercept("KERNELBASE.dll", name, {onEnter(args) {
    const first = string(args[0]), second = string(args[1]);
    if (targets.test(first) || targets.test(second)) report(name, {first, second}, this.context);
  }});
}
intercept("ntdll.dll", "NtSetInformationFile", {onEnter(args) {
  const kind = args[4].toUInt32();
  if (kind !== 10 && kind !== 65) return;
  try {
    const bytes = args[2].add(16).readU32();
    if (bytes > args[3].toUInt32() || bytes > 32768 || (bytes & 1) !== 0) return;
    const path = string(args[2].add(20), bytes / 2);
    if (targets.test(path)) report("NtSetInformationFile-rename", {path, kind}, this.context);
  } catch (_) {}
}});
send({event:"hooks-ready", pid:Process.id, hooks, utc:new Date().toISOString()});
