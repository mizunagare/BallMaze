"""Read-only structural validation, not stack unwinding or proof of crash absence."""
import argparse
import hashlib
import json
import struct
from pathlib import Path


def inspect(path):
    data = path.read_bytes()
    def bounds(rva, size):
        if rva < 0 or size < 0 or rva + size > len(data):
            raise ValueError(f'Out-of-file range {rva}+{size}/{len(data)}')
    def unpack(fmt, at):
        bounds(at, struct.calcsize(fmt))
        return struct.unpack_from(fmt, data, at)
    bounds(0, 32)
    sig, version, count, directory = unpack('<4sIII', 0)
    if sig != b'MDMP' or version & 0xffff != 0xa793 or count < 1 or count > 10000:
        raise ValueError('Invalid minidump header')
    bounds(directory, count * 12)
    streams = {}
    for index in range(count):
        kind, size, rva = unpack('<III', directory + index * 12)
        bounds(rva, size)
        # MINIDUMP_STREAM_TYPE.UnusedStream entries are reserved empty slots.
        if kind == 0:
            if size or rva: raise ValueError('Non-empty unused stream')
            continue
        if kind in streams:
            raise ValueError('Duplicate stream type')
        streams[kind] = dict(size=size, rva=rva)
    for required in (3, 4, 7):
        if required not in streams:
            raise ValueError(f'Missing thread/module/system stream {required}')
    threads = []
    r = streams[3]['rva']; n, = unpack('<I', r)
    if 4 + n * 48 > streams[3]['size'] or n == 0:
        raise ValueError('Invalid thread table')
    for index in range(n):
        at = r + 4 + index * 48
        thread, = unpack('<I', at)
        stack_size, stack_rva, context_size, context_rva = unpack('<IIII', at + 32)
        bounds(stack_rva, stack_size); bounds(context_rva, context_size)
        threads.append(dict(id=thread, stackBytes=stack_size, contextBytes=context_size))
    r = streams[4]['rva']; n, = unpack('<I', r)
    if 4 + n * 108 > streams[4]['size'] or n == 0:
        raise ValueError('Invalid module table')
    modules = []
    for index in range(n):
        name_rva, = unpack('<I', r + 4 + index * 108 + 20)
        size, = unpack('<I', name_rva); bounds(name_rva + 4, size)
        modules.append(data[name_rva + 4:name_rva + 4 + size].decode('utf-16-le'))
    if 5 in streams:
        r = streams[5]['rva']; n, = unpack('<I', r)
        if 4 + n * 16 > streams[5]['size']: raise ValueError('Invalid memory table')
        for i in range(n):
            size, loc = unpack('<II', r + 4 + i * 16 + 8); bounds(loc, size)
    if 9 in streams:
        r = streams[9]['rva']; n, loc = unpack('<QQ', r)
        if 16 + n * 16 > streams[9]['size']: raise ValueError('Invalid memory64 table')
        total = sum(unpack('<Q', r + 16 + i * 16 + 8)[0] for i in range(n)); bounds(loc, total)
    exception = None
    if 6 in streams:
        r = streams[6]['rva']; exception = dict(thread=unpack('<I', r)[0], code=hex(unpack('<I', r + 8)[0]))
    return dict(status='PASS', file=path.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                version=hex(version), streams=streams, threads=threads, modules=modules, exception=exception,
                limitation='Structural range validation only; no symbolized stack, memory dump stays local')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('dump', type=Path); p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    try:
        result = inspect(args.dump); code = 0
    except Exception as e:
        result = dict(status='FAIL', file=args.dump.name, reason=str(e)); code = 1
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    raise SystemExit(code)
