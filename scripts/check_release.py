#!/usr/bin/env python3
"""Verify copied publication assets and released source-data identities."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
read = lambda p: json.loads((root / p).read_text(encoding='utf-8'))
snapshot = read('report/src/data.json')
published = list((root / 'docs').glob('snapshot.*.json'))
assert len(published) == 1, 'Release must contain exactly one data snapshot'
assert json.loads(published[0].read_text()) == snapshot
assert snapshot['buildStatus'] == 'complete'
events = read('data/events.json')
expected = {e['id']: e for e in events if e['category'] in ('core', 'expanded')}
assert {e['id']: e for e in snapshot['queries']['events']['rows']} == expected
assert {e['id'] for e in snapshot['queries']['candidates']['rows']} == {e['id'] for e in events if e['category'] not in ('core','expanded')}
assert {e['id'] for e in snapshot['queries']['recent']['rows']} == {e['id'] for e in events if e['year']==2026 or e.get('review_year')==2026}
assert len(snapshot['queries']['sources']['rows']) == len(read('data/sources.json'))
assert len(snapshot['queries']['coverage']['rows']) == len(read('data/search_coverage.json'))
for path in root.rglob('*'):
    if '.git' in path.parts:
        continue
    assert not path.is_symlink(), f'Unportable symlink: {path.relative_to(root)}'
files = ['docs/index.html', str(published[0].relative_to(root)),
         'exports/互动报告.html', 'exports/中国大陆随机伤人事件_2018-2026.xlsx',
         'data/events.json', 'data/sources.json', 'data/analysis.json']
manifest = {'status': 'passed', 'date': '2026-09-16', 'files': []}
for name in files:
    content = (root / name).read_bytes()
    assert len(content) > 100
    manifest['files'].append({'path': name, 'bytes': len(content),
                             'sha256': hashlib.sha256(content).hexdigest()})
(root / 'validation/release_manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'passed', 'files': len(files), 'events': len(events),
                  'publication_snapshot': 'identical to reviewed source'}, ensure_ascii=False))
