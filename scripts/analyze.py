#!/usr/bin/env python3
"""Merge reviewed factual records and reproduce statistics (Python standard library)."""
import csv, json, math, statistics, copy
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUTOFF = '2026-09-16'
PROVINCES = '北京 天津 河北 山西 内蒙古 辽宁 吉林 黑龙江 上海 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 广西 海南 重庆 四川 贵州 云南 西藏 陕西 甘肃 青海 宁夏 新疆'.split()
CATEGORIES = {'core':'核心', 'expanded':'纠纷扩大', 'pending':'待核实', 'excluded':'排除', 'organized_terror':'有组织恐怖袭击'}
FIELDS = dict(id='事件编号',date='案发日期',date_precision='日期精度',title='事件名称',province='省级地区',city='城市',district='区县',urban_rural='城乡属性',scene='场景',method='方式',category='分类代码',classification_reason='分类依据',deaths='受害者死亡',injured='受害者受伤',injured_reported='受伤原口径',injured_lower_bound='受伤保守下限',deaths_lower_bound='死亡保守下限',serious_injuries='重伤',attacker_deaths='作案者死亡',attacker_injured='作案者受伤',casualty_asof='伤亡口径日期',casualty_note='伤亡修订说明',involves_children='涉及儿童',victim_relation='受害者关系',age='作案者年龄',sex='性别',occupation='职业状态',motive_summary='动机摘要',motive_tags='动机标签',motive_basis='动机证据层级',mental_health='精神健康证据',prior_violence='既往暴力记录',warning_signals='事前威胁线索',intervention='干预与现场处置',outcome='司法及处置结果',judgment_date='判决日期',execution_date='执行日期',last_source_date='最后来源日期',evidence_level='事件证据等级',source_ids='来源编号',field_sources='分字段来源',series_id='关联系列',notes='补充说明')
FIELDS.update(additional_collision_injured='故意性未明的碰撞伤者',response_injured='警方处置伤者',event_total_injured_reported='事件总伤者原口径',motive_attribution='动机归因说明')
FIELDS.update(date_time='已核实案发时间',continuous_attack='连续袭击过程',official_occurrence='发生获官方确认',official_classification='官方材料直接支持分类',classification_evidence='分类证据分层说明',motive_themes='动机归并主题')

def read(path):
    return json.loads((ROOT/path).read_text())
def write(path, obj):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvwrite(path, rows):
    if not rows: return
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT/path).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def known(x):return x is not None and x != '' and x != '未知'
def count_stats(events):
    result={'events':len(events)}
    for field in ['deaths','injured']:
        result[field+'_known_total']=sum(e[field] for e in events if e.get(field) is not None)
        result[field+'_lower_total']=sum(e[field] if e.get(field) is not None else (e.get(field+'_lower_bound') or 0) for e in events)
        result[field+'_unknown_events']=sum(e.get(field) is None for e in events)
    return result
def groups(rows,key):
    return [{key:k,**count_stats([e for e in rows if (e.get(key) or '未披露')==k])} for k in sorted({e.get(key) or '未披露' for e in rows})]
def corr(pairs):
    if len(pairs)<3:return None
    x,y=zip(*pairs); mx,my=statistics.mean(x),statistics.mean(y)
    den=math.sqrt(sum((v-mx)**2 for v in x)*sum((v-my)**2 for v in y))
    return sum((a-mx)*(b-my) for a,b in pairs)/den if den else None

def main():
    events=[];sources=[];coverage=[];notes=[];loaded=[]
    for name in ['group_a','group_b','group_c']:
        path=ROOT/f'work/{name}.json'
        if path.exists():
            d=json.loads(path.read_text());events+=d['events'];sources+=d['sources'];coverage+=d.get('coverage',[]);notes+=d.get('notes',[]);loaded.append(name)
    sources+=read('work/context_sources.json')+read('work/root_sources.json')+read('work/root_additional_sources.json')
    splits=read('work/event_splits.json')
    expanded_events=[]
    for e in events:
        if e['id'] not in splits:expanded_events.append(e);continue
        for fragment in splits[e['id']]:
            child=copy.deepcopy(e);child.update(fragment);child['source_ids'].append('RS002')
            for f in ['date','location','casualties','classification']:child['field_sources'][f].append('RS002')
            expanded_events.append(child)
    events=expanded_events
    for s in sources:
        s['supports']=[kid['id'] for eid in s['supports'] for kid in (splits[eid] if eid in splits else [{'id':eid}])]
    for path in ['work/review_sources.json','work/review_c_sources.json','work/review_demographics_sources.json']:
        if (ROOT/path).exists():
            extra=read(path); sources+=extra if isinstance(extra,list) else extra['sources']
            if isinstance(extra,dict):
                for patch in extra.get('source_updates',[]):
                    for s in sources:
                        if s['id']==patch['id']:s.update(patch)
    if (ROOT/'work/review_findings.json').exists():
        patches=read('work/review_findings.json').get('source_metadata_suggested_overrides',{})
        for s in sources:s.update(patches.get(s['id'],{}))
    coverage+=read('work/root_coverage.json')
    # Corrections are explicit, versioned and never overwrite the researchers' raw records.
    overrides={}
    def merge_changes(eid, changes, path):
        dest=overrides.setdefault(eid,{})
        for key,val in changes.items():
            if key=='source_ids':dest[key]=list(dict.fromkeys(dest.get(key,[])+val))
            elif key=='field_sources':
                if 'demographics' in path:val={k:v for k,v in val.items() if k=='demographics'}
                dest.setdefault(key,{}).update(val)
            else:dest[key]=val
    for path in ['work/review_overrides.json','work/review_c_overrides.json','work/review_a_classification.json','work/review_demographics.json','work/overrides.json']:
        if (ROOT/path).exists():
            patch=read(path)
            if 'overrides' in patch:
                for item in patch['overrides']:merge_changes(item['event_id'],item['set'],path)
            else:
                for eid,changes in patch.items():merge_changes(eid,changes,path)
    for e in events:
        patch=overrides.get(e['id'],{})
        for key,val in patch.items():
            if key=='source_ids':e[key]=list(dict.fromkeys(e.get(key,[])+val))
            elif key=='field_sources':e[key].update(val)
            else:e[key]=val
        if e.get('basis'):e['classification_evidence']=e.get('classification_evidence','')+'；'+e.pop('basis')
        e.pop('category_unchanged',None);e.pop('review_scope',None)
        for f in FIELDS:e.setdefault(f,None)
        e['year']=int(e['date'][:4]) if e['date'] else None
        e['quarter']=e['date'][:4]+'-Q'+str((int(e['date'][5:7])-1)//3+1) if e['date'] and len(e['date'])>=7 else None
        e['category_label']=CATEGORIES[e['category']]
        e['official_occurrence']=e['evidence_level'] in ['官方原文','官方转载']
        if e['official_classification'] is None:e['official_classification']=e['official_occurrence'] and e['category'] in ['core','expanded']
        if e['classification_evidence'] is None:e['classification_evidence']=e.get('classification_evidence_basis') or ('官方事实直接支持' if e['official_classification'] else '媒体调查／研究推断')
        e['official']=e['official_classification']
        e['same_period']=len(e['date'] or '')==10 and e['date'][5:]<='09-16'
        e['motive_known']=known(e['motive_summary']) and e['motive_basis'] in ['法院认定','警方初步通报','媒体调查','检方指控','外交渠道转述法院']
        e['deaths_min']=e['deaths'] if e['deaths'] is not None else e.get('deaths_lower_bound') or 0
        e['injured_min']=e['injured'] if e['injured'] is not None else e.get('injured_lower_bound') or 0
        e['motive_tags']=e.get('motive_tags') or []
        taxonomy=read('work/motive_taxonomy.json')
        e['motive_themes']=sorted(set(taxonomy.get(t,'其他已披露背景') for t in e['motive_tags'])) if e['motive_known'] else []
        for f in ['date','location','casualties','classification','motive','outcome']:e['field_sources'].setdefault(f,[])
    events.sort(key=lambda e:(e['date'] or '',e['id']))
    assert len({s['id'] for s in sources})==len(sources),'Duplicate source IDs'
    sourceids={s['id'] for s in sources}
    issues=[]
    assert len({e['id'] for e in events})==len(events),'Duplicate event IDs'
    assert all(e['province'] in PROVINCES for e in events),'Invalid province'
    for e in events:
        assert e['date'] and '2018-01-01'<=e['date']<=CUTOFF, e['id']+' event date outside scope'
        assert e['source_ids'] and all(s in sourceids for s in e['source_ids']),e['id']+' missing source'
        assert all(s in sourceids for ids in e['field_sources'].values() for s in ids), e['id']+' field source missing'
        assert all(set(ids)<=set(e['source_ids']) for ids in e['field_sources'].values()), e['id']+' field source not linked to event'
        for f in ['deaths','injured','serious_injuries','attacker_deaths','attacker_injured','injured_lower_bound','deaths_lower_bound']:
            assert e[f] is None or isinstance(e[f],(int,float)) and math.isfinite(e[f]) and e[f]>=0 and int(e[f])==e[f],(e['id'],f,e[f])
        for f in ['deaths','injured']:
            assert e[f] is None or e.get(f+'_lower_bound') is None or e[f]>=e[f+'_lower_bound'],e['id']+' lower bound exceeds precise count'
        assert e['serious_injuries'] is None or e['injured'] is None or e['serious_injuries']<=e['injured'],e['id']+' serious > injured'
        if e['category'] in ['core','expanded']:
            assert e['classification_reason'] and e['field_sources']['classification'],e['id']+' no classification support'
            if not e['official_occurrence'] and e['evidence_level']!='多源媒体':issues.append({'id':e['id'],'issue':'纳入事件未标记官方发生或多源媒体，需复核'})
    duplicates=Counter((e['date'],e['province'],e['city']) for e in events)
    for (d,p,c),n in duplicates.items():
        same=[e for e in events if (e['date'],e['province'],e['city'])==(d,p,c)]
        if n>1 and not (all(e.get('series_id') and e.get('date_time') for e in same) and len({e['date_time'] for e in same})==n):
            issues.append({'id':f'{d}|{p}|{c}','issue':'同日同城市候选重复，人工复核'})
    verified=[e for e in events if e['category'] in ['core','expanded']]
    core=[e for e in events if e['category']=='core']
    annual=[];quarterly=[];sens=[]
    for year in range(2018,2027):
        for scope,select in [('核心',core),('扩展',verified)]:
            r=[e for e in select if e['year']==year]
            annual.append({'year':year,'scope':scope,'period':'全年' if year<2026 else '截至09-16',**count_stats(r)})
            annual.append({'year':year,'scope':scope,'period':'01-01至09-16',**count_stats([e for e in r if e['same_period']])})
            largest=max(r,key=lambda e:e['deaths_min'],default=None)
            sens.append({'year':year,'scope':scope,'official_events':sum(e['official'] for e in r),'all_verified_events':len(r),'largest_event_id':largest['id'] if largest else None,'deaths_lower_total':sum(e['deaths_min'] for e in r),'deaths_without_largest':sum(e['deaths_min'] for e in r if e is not largest)})
        for q in range(1,5):
            if year==2026 and q==4:continue
            quarterly.append({'quarter':str(year)+'-Q'+str(q),**count_stats([e for e in core if e['quarter']==str(year)+'-Q'+str(q)])})
    context=read('data/provincial_context.json');panel=[]
    for b in context:
        r=[e for e in core if e['province']==b['province'] and e['year']==b['year']]
        panel.append({**b,**count_stats(r),'records_per_million':len(r)/(b['population_10k']/100) if b.get('population_10k') else None,'no_record_means':'未检出，不代表实际零发生' if not r else '公开核实记录'})
    correlations=[]
    for year in range(2018,2025):
        for field in ['population_10k','urbanization_pct','income_yuan']:
            rows=[b for b in panel if b['year']==year and b.get(field) is not None]
            for metric in ['events','records_per_million']:
                correlations.append({'year':year,'background':field,'metric':metric,'n':len(rows),'pearson_r':corr([(b[field],b[metric]) for b in rows]),'interpretation':'描述性地区关联；检索未检出按记录数0计算；不能解释个人动机或实际犯罪率'})
    motive=[]
    for e in events:
        for tag in e['motive_tags']:motive.append({'event_id':e['id'],'category':e['category'],'tag':tag,'theme':taxonomy.get(tag,'其他已披露背景'),'basis':e['motive_basis'],'summary':e['motive_summary'],'source_ids':e['field_sources']['motive']})
    missing=[{'field':FIELDS[f],'missing':sum(not known(e.get(f)) for e in core),'n':len(core)} for f in ['motive_summary','age','sex','occupation','mental_health','prior_violence','warning_signals','intervention','serious_injuries']]
    summary={'cutoff':CUTOFF,'loaded_groups':loaded,'categories':dict(Counter(e['category'] for e in events)),'core':count_stats(core),'expanded':count_stats(verified),'annual':annual,'quarterly':quarterly,'sensitivity':sens,'geography':groups(core,'province'),'scenes':groups(core,'scene'),'methods':groups(core,'method'),'missingness':missing,'motive_known':sum(e['motive_known'] for e in core),'correlations':correlations}
    explanations={'category':'核心core；扩展新增expanded；待核pending；排除excluded；恐袭organized_terror另列。','injured':'受害者受伤人数，尽可能采用最新结局；作案者另列；不含已转死亡者；若来源不能证明去重则详见casualty_note。','deaths':'公开可核实的受害者死亡人数，作案者死亡另列。','official_occurrence':'事件发生是否获官方原文或可靠完整转载支持，不代表官方确认随机性。','official_classification':'严格敏感性标记：官方材料的事实直接支持随机/扩大关系。媒体采集、外交渠道转述及研究推断另层，不计此子集。','motive_themes':'研究编码，按work/motive_taxonomy.json归并原始标签；允许多标签，非独立新增事实。','field_sources':'日期、地点、伤亡、分类、动机、处置及人口特征分别对应来源ID；应回查来源正文与关键事实摘要。','date_time':'少数案件可核实到时间，ISO8601含中国时区+08:00；未知为空，不以报道时间填补。','continuous_attack':'明确为同一连续过程时为true；未核实为空。跨时段重新启动的袭击独立计件，即使在同一天。','motive_basis':'法院认定/警方初步通报/检方指控/外交渠道转述法院/媒体调查/未知；不同层级不互换。','series_id':'同一作案系列的关联编号；件数不等于独立作案者人数。','classification_evidence':'分类所依赖的事实层与研究解释，避免将媒体判断误写成官方定性。'}
    dictionary=[{'field':k,'label':v,'definition':explanations.get(k,'空值表示未查得/无法确定，不能按0解释。')} for k,v in FIELDS.items()]
    outputs={'events':events,'sources':sources,'search_coverage':coverage,'motive_tags':motive,'field_dictionary':dictionary,'analysis':summary,'province_year_panel':panel,'excluded_pending':[e for e in events if e['category'] not in ['core','expanded']]}
    for name,obj in outputs.items():
        write('data/'+name+'.json',obj)
        if isinstance(obj,list):csvwrite('data/'+name+'.csv',obj)
    write('validation/data_checks.json',{'status':'needs_review' if issues else 'passed','event_count':len(events),'source_count':len(sources),'coverage_count':len(coverage),'issues':issues,'notes':notes})
    # Content-addressed runtime build will preserve all source rows.
    snapshot=read('report/src/data.json')
    def query(rows,label,ids=None):
        selected=[s for s in sources if ids is None or s['id'] in ids]
        return {'rows':rows,'source':{'label':label,'links':[{'label':s['title'],'url':s['url']} for s in selected], 'filters':['案发日期2018-01-01至2026-09-16','中国大陆31省级地区'], 'caveats':['这是公开信息可核实事件库，记录密度不等于实际发生率。','未知数保持空值；伤亡合计使用已知值或明确下限。']}}
    snapshot['queries']={'events':query(verified,'逐案核验的核心与扩展事件',set(s for e in verified for s in e['source_ids'])),'candidates':query(outputs['excluded_pending'],'待核实与排除记录'),'sources':query(sources,'逐字段可追溯来源'),'context':query(panel,'国家统计局2018—2024同版资料及2025省级人口披露汇总',set(s['id'] for s in read('work/context_sources.json'))),'prevention':query([s for s in sources if s['id'].startswith('R_SAFETY') or s['id']=='R_NTAC2024'],'公共安全原始指引'),'coverage':query(coverage,'实际检索与访问记录'),'geography':query(read('data/provinces.geojson')['features'],'地理边界，仅大陆31省着色',{'R_GEO'})}
    snapshot['researchSummary']=summary
    snapshot['queries']['domains']=query([{'year':y,'province':p} for y in range(2018,2027) for p in PROVINCES],'用户指定的观察范围；只用于筛选选项，不是事件记录',set())
    write('report/src/data.json',snapshot)
    print(json.dumps({'events':len(events),'sources':len(sources),'categories':summary['categories'],'issues':issues},ensure_ascii=False))

if __name__=='__main__':main()
