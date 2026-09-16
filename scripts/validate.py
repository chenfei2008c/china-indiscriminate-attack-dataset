#!/usr/bin/env python3
"""Independent SQLite and OOXML checks for the published research snapshot."""
import json, sqlite3, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((ROOT/'data'/f'{n}.json').read_text())
events=read('events');analysis=read('analysis');sources=read('sources');context=read('province_year_panel')
db=sqlite3.connect(':memory:')
db.execute('create table e (id text primary key, day text, province text, category text, deaths integer, injured integer, dl integer, il integer, official integer)')
db.executemany('insert into e values (?,?,?,?,?,?,?,?,?)',[(e['id'],e['date'],e['province'],e['category'],e['deaths'],e['injured'],e.get('deaths_lower_bound'),e.get('injured_lower_bound'),int(e['official'])) for e in events])
checks=[]
for scope,where in [('核心',"category='core'"),('扩展',"category in ('core','expanded')")]:
 for year in range(2018,2027):
  for period,cut in [('annual',''),('ytd',"and substr(day,6)<='09-16'")]:
   row=db.execute(f"select count(*),sum(coalesce(deaths,dl,0)),sum(coalesce(injured,il,0)),sum(deaths is null),sum(injured is null) from e where {where} and substr(day,1,4)=? {cut}",(str(year),)).fetchone()
   row=tuple(x or 0 for x in row)
   target=next(x for x in analysis['annual'] if x['year']==year and x['scope']==scope and (x['period']=='01-01至09-16')==(period=='ytd'))
   expected=tuple(target[k] for k in ['events','deaths_lower_total','injured_lower_total','deaths_unknown_events','injured_unknown_events'])
   assert row==expected,(scope,year,period,row,expected)
   checks.append(f'{scope}/{year}/{period}')
for row in context:
 n=db.execute("select count(*) from e where category='core' and province=? and substr(day,1,4)=?",(row['province'],str(row['year']))).fetchone()[0]
 assert n==row['events']
 assert abs(n/(row['population_10k']/100)-row['records_per_million'])<1e-10
assert len({(b['province'],b['year']) for b in context})==248
ids={s['id'] for s in sources};assert len(ids)==len(sources)
assert all(e['source_ids'] and set(e['source_ids'])<=ids for e in events)
assert all(set(ss)<=ids for e in events for ss in e['field_sources'].values())
snapshot=json.loads((ROOT/'report/src/data.json').read_text())
assert {e['id'] for e in snapshot['queries']['events']['rows']}=={e['id'] for e in events if e['category'] in ('core','expanded')}
assert not set(e['id'] for e in snapshot['queries']['events']['rows'])&set(e['id'] for e in snapshot['queries']['candidates']['rows'])
assert len(snapshot['queries']['domains']['rows'])==31*9
# Read cached Excel values and errors independently of the authoring library.
book=ROOT/'exports/中国大陆随机伤人事件_2018-2026.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(book) as z:
 errors=[];formula_count=0
 for name in z.namelist():
  if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
   tree=ET.fromstring(z.read(name))
   errors += [(name,c.attrib['r'],c.findtext('s:v',namespaces=ns)) for c in tree.findall('.//s:c',ns) if c.attrib.get('t')=='e']
   formula_count+=len(tree.findall('.//s:f',ns))
 assert not errors,errors
 sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
 cells={c.attrib['r']:c.findtext('s:v',namespaces=ns) for c in sheet.findall('.//s:c',ns)}
 for cell,val in [('B18',analysis['core']['events']),('C18',analysis['expanded']['events']),('D18',analysis['core']['deaths_lower_total']),('E18',analysis['core']['injured_lower_total'])]:assert float(cells[cell])==val,(cell,cells[cell],val)
 assert formula_count>=500
assert not any(e['date']>'2026-09-16' or e['date']<'2018-01-01' for e in events)
report={'status':'passed','independent_annual_checks':len(checks),'province_year_checks':len(context),'xlsx_formula_count':formula_count,'xlsx_formula_errors':0,'core_events':analysis['core']['events'],'expanded_events':analysis['expanded']['events'],'core_deaths_min':analysis['core']['deaths_lower_total'],'core_injured_min':analysis['core']['injured_lower_total'],'event_source_integrity':'passed','date_range':'passed','note':'这些检查验证计算与结构一致性；不能证明公开来源无误或检索穷尽。浏览器与逐案抽核另有记录。'}
(ROOT/'validation/independent_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
