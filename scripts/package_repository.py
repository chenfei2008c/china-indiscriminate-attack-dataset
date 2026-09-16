#!/usr/bin/env python3
"""Copy reviewed deliverables into an existing, explicitly selected repository.

Does not run git or delete files. Build and verify before packaging.
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('destination', type=Path)
args = parser.parse_args()
dest = args.destination.resolve()
if dest == ROOT or not (dest / '.git').exists():
    raise SystemExit('Choose a distinct, existing Git repository.')
ignore = shutil.ignore_patterns('node_modules', '__pycache__', '*.pyc',
    '*.inspect.ndjson', 'dist', '.data-app-offline', '.DS_Store',
    'README_draft.md', 'initial_snapshot.json')
for directory in ['data', 'scripts', 'work', 'report']:
    shutil.copytree(ROOT / directory, dest / directory, dirs_exist_ok=True, ignore=ignore)
for directory in ['validation', 'exports']:
    (dest / directory).mkdir(exist_ok=True)
for source in (ROOT / 'validation').glob('*.json'):
    shutil.copy2(source, dest / 'validation' / source.name)
shutil.copytree(ROOT / 'report/dist', dest / 'docs', dirs_exist_ok=True)
(dest / 'docs/.nojekyll').touch()
shutil.copy2(ROOT / 'exports/中国大陆随机伤人事件_2018-2026.xlsx', dest / 'exports')
shutil.copy2(ROOT / 'report/.data-app-offline/exports/report.html', dest / 'exports/互动报告.html')
shutil.copy2(ROOT / 'work/research_interpretation.md', dest / 'RESEARCH.md')
shutil.copy2(ROOT / 'work/README_draft.md', dest / 'README.md')
shutil.copy2(ROOT / 'RESEARCH_BRIEF.md', dest / 'RESEARCH_BRIEF.md')
print('Packaged reviewed data, research, report, workbook and validation into', dest)
