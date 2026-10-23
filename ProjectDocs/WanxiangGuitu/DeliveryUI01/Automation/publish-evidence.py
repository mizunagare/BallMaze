"""Publish an explicit allowlist of test diagnostics, never saves/builds/dumps.

Original files stay local. Published logs are redacted and labelled, not raw-byte claims.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


def redact(text):
    text = re.sub(r'(?i)(-cbm(?:EditorLicense|MachineId)\s+)("[^"]*"|[^\s\r\n]+)', r'\1[REDACTED]', text)
    text = re.sub(r'(?i)(Authorization:\s*Bearer\s+)\S+', r'\1[REDACTED]', text)
    return text


def publish(source, target, paths, archive=False):
    source = source.resolve(strict=True)
    target.mkdir(parents=True, exist_ok=True)
    manifest = []
    output_zip = zipfile.ZipFile(target / 'logs-redacted.zip', 'w', zipfile.ZIP_DEFLATED) if archive else None
    try:
        for relative in paths:
            if Path(relative).is_absolute() or '..' in Path(relative).parts:
                raise ValueError('Only contained relative diagnostics are allowed')
            path = (source / relative).resolve(strict=True)
            if not path.is_relative_to(source) or path.suffix.lower() not in {'.json', '.jsonl', '.csv', '.md', '.txt', '.log', '.stdout', '.stderr'}:
                raise ValueError(f'Not an allowed diagnostic: {relative}')
            if any(p.lower() in {'wanxiangguitu', 'release', 'library', 'dumps', 'profile', 'legacysaves'} for p in Path(relative).parts) or path.name in {'save.json', 'save.backup.json'} or path.name.startswith(('before-', 'after-', 'loaded-')):
                raise ValueError(f'Save/build/dump publishing rejected: {relative}')
            raw = path.read_bytes()
            encoding = 'utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else ('utf-16-le' if raw[1:100:2].count(0) > 20 else 'utf-8-sig')
            clean = redact(raw.decode(encoding, errors='replace')).replace('\r\n', '\n').encode('utf-8')
            if output_zip:
                output_zip.writestr(relative.replace('\\', '/'), clean)
            else:
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(clean)
            manifest.append(dict(path=relative, originalSha256=hashlib.sha256(raw).hexdigest(),
                                 publishedSha256=hashlib.sha256(clean).hexdigest(), changed=raw != clean))
    finally:
        if output_zip:
            output_zip.close()
    (target / ('log-manifest.json' if archive else 'manifest.json')).write_text(
        json.dumps(dict(source=str(source), policy='Explicit diagnostics only; redacted UTF-8 publication; originals retained locally', files=manifest), ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--list', type=Path, required=True, help='JSON string array, explicit relative diagnostics')
    parser.add_argument('--zip', action='store_true')
    args = parser.parse_args()
    publish(args.source, args.target, json.loads(args.list.read_text(encoding='utf-8-sig')), args.zip)
