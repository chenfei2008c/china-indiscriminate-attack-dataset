import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=async n=>JSON.parse(await fs.readFile(path.join(root,'data',n+'.json'),'utf8'));
const [events,sources,tags,panel,coverage,dict,analysis]=await Promise.all(['events','sources','motive_tags','province_year_panel','search_coverage','field_dictionary','analysis'].map(read));
const out=path.join(root,'exports'),validation=path.join(root,'validation');
await fs.mkdir(out,{recursive:true});await fs.mkdir(validation,{recursive:true});
const wb=Workbook.create();
const names=['统计汇总','事件主表','来源证据','动机与背景标签','省年背景','敏感性','季度统计','描述性关联','2026补查','待核实与排除','检索覆盖','字段字典','使用说明'];
const sh=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s};
const value=v=>v==null?null:typeof v==='boolean'?(v?'是':'否'):Array.isArray(v)?v.join('；'):typeof v==='object'?JSON.stringify(v):v;
let tableId=0;
function table(name,rows,fields,labels={},start=1){
 const s=sh[name],last=col(fields.length-1),end=start+rows.length;
 const matrix=[fields.map(k=>labels[k]||k),...rows.map(r=>fields.map(k=>value(r[k])))];
 s.getRange(`A${start}:${last}${end}`).values=matrix;
 s.showGridLines=false;s.freezePanes.freezeRows(start);s.tabColor=name==='统计汇总'?'#245D72':'#92AAB5';
 const area=s.getRange(`A${start}:${last}${end}`);area.format.font.name='Aptos';area.format.font.size=11;area.format.verticalAlignment='top';area.format.rowHeight=38;area.format.columnWidth=19;
 s.getRange(`A${start}:${last}${start}`).format.fill='#245D72';s.getRange(`A${start}:${last}${start}`).format.font.color='#FFFFFF';s.getRange(`A${start}:${last}${start}`).format.font.bold=true;s.getRange(`A${start}:${last}${start}`).format.rowHeight=42;s.getRange(`A${start}:${last}${start}`).format.wrapText=true;
 s.tables.add(`A${start}:${last}${end}`,true,`ResearchTable${++tableId}`);
 fields.forEach((f,i)=>{
   const range=s.getRange(`${col(i)}${start+1}:${col(i)}${end}`);
   if(/date$|^date$|_asof$/.test(f)&&rows.every(r=>r[f]==null||/^\d{4}-\d{2}-\d{2}$/.test(r[f]))){range.values=rows.map(r=>[r[f]?new Date(r[f]+'T00:00:00Z'):null]);range.setNumberFormat('yyyy-mm-dd');}
   if(f==='publisher'){range.format.columnWidth=30;range.format.wrapText=true;}
   if(['title','classification_reason','key_facts','notes','casualty_note','motive_summary','query','definition','说明','dating_note','verification_gaps'].includes(f)){range.format.columnWidth=55;range.format.wrapText=true;}
   if(['url','original_url','social_source_urls','field_sources','source_ids','scope_years','scope_regions','supports'].includes(f)){range.format.columnWidth=f==='url'?64:30;range.format.wrapText=true;}
   if(rows.some(r=>typeof r[f]==='number')){range.setNumberFormat(/pct|per_million|pearson_r/.test(f)?'0.0000':'0');range.format.horizontalAlignment='right';}
 });
 return {sheet:s,fields,start,end};
}
const labels=Object.fromEntries(dict.map(d=>[d.field,d.label]));
const fields=['id','date','title','province','city','category','scene','method','deaths','injured','injured_reported','injured_lower_bound','deaths_lower_bound','casualty_asof','casualty_note','classification_reason','district','urban_rural','date_precision','date_time','continuous_attack','serious_injuries','attacker_deaths','attacker_injured','involves_children','victim_relation','age','sex','occupation','motive_summary','motive_tags','motive_basis','mental_health','prior_violence','warning_signals','intervention','outcome','judgment_date','execution_date','last_source_date','evidence_level','source_ids','field_sources','series_id','additional_collision_injured','response_injured','event_total_injured_reported','motive_attribution','review_batch','review_year','reported_date','dating_note','verification_gaps','social_source_urls','notes','official_occurrence','official_classification','classification_evidence','motive_themes','year','deaths_min','injured_min','official_number','motive_known_number','same_period_number','deaths_unknown','injured_unknown'];
Object.assign(labels,{official_occurrence:'发生获官方确认',official_classification:'官方材料直接支持分类',classification_evidence:'分类证据分层说明',motive_themes:'动机归并主题',year:'案发年（汇总辅助）',deaths_min:'死亡已知数或下限',injured_min:'受伤已知数或下限',official_number:'官方来源标记1/0',motive_known_number:'动机有证据1/0',same_period_number:'1月1日至9月16日1/0',deaths_unknown:'死亡数不明1/0',injured_unknown:'受伤数不明1/0'});
const master=table('事件主表',events.map(e=>({...e,official_number:e.official?1:0,motive_known_number:e.motive_known?1:0,same_period_number:e.same_period?1:0,deaths_unknown:e.deaths==null?1:0,injured_unknown:e.injured==null?1:0})),fields,labels);
const ref=f=>`'事件主表'!$${col(fields.indexOf(f))}$2:$${col(fields.indexOf(f))}$${master.end}`;
const sf=sh['统计汇总'];sf.showGridLines=false;sf.tabColor='#245D72';sf.freezePanes.freezeRows(7);
sf.getRange('A1:K20').format.font.name='Aptos';sf.getRange('A1:K20').format.font.size=11;sf.getRange('A1:K20').format.columnWidth=18;sf.getRange('A1:K20').format.rowHeight=25;
sf.getRange('A1:K1').merge();sf.getRange('A1').values=[['中国大陆随机伤人事件公开信息研究']];sf.getRange('A1:K1').format.font.size=22;sf.getRange('A1:K1').format.font.bold=true;sf.getRange('A1:K1').format.rowHeight=42;
sf.getRange('A2:K2').merge();sf.getRange('A2').values=[['2018-01-01 — 2026-09-16 ｜ 31省级地区 ｜ 公开可核实记录，不是全部实际案件']];
sf.getRange('A3:K3').merge();sf.getRange('A3').values=[['核心：不特定或与纠纷无关人员；扩展：核心 + 定向纠纷扩大。待核与排除不计入汇总。']];
sf.getRange('A4:K4').merge();sf.getRange('A4').values=[['伤亡为受害者已知合计/明确下限；作案者另列。2026仅截至9月16日，不折算全年。']];
sf.getRange('A5:K5').merge();sf.getRange('A5').values=[['所有空值代表未知。年度公式可随主表现有范围内修改更新；新增记录后请重跑分析和建表脚本。']];
const heads=['案发年','核心件数','扩展件数','核心死亡下限','核心受伤下限','官方直接支持分类件数','动机未知件数','同期核心件数','死亡人数未知','受伤人数未知','备注'];
sf.getRange('A7:K7').values=[heads];sf.getRange('A7:K7').format.fill='#245D72';sf.getRange('A7:K7').format.font.color='#FFFFFF';sf.getRange('A7:K7').format.font.bold=true;sf.getRange('A7:K7').format.rowHeight=48;sf.getRange('A7:K7').format.wrapText=true;
for(let y=2018;y<=2026;y++){
 const row=y-2018+8,base=`${ref('year')},$A${row},${ref('category')},"core"`;
 sf.getRange(`A${row}`).values=[[y]];
 sf.getRange(`B${row}:J${row}`).formulas=[[
 `=COUNTIFS(${base})`,`=B${row}+COUNTIFS(${ref('year')},$A${row},${ref('category')},"expanded")`,
 `=SUMIFS(${ref('deaths_min')},${base})`,`=SUMIFS(${ref('injured_min')},${base})`,
 `=SUMIFS(${ref('official_number')},${base})`,`=B${row}-SUMIFS(${ref('motive_known_number')},${base})`,
 `=SUMIFS(${ref('same_period_number')},${base})`,`=SUMIFS(${ref('deaths_unknown')},${base})`,`=SUMIFS(${ref('injured_unknown')},${base})`]];
 sf.getRange(`K${row}`).values=[[y===2026?'截至09-16':'全年']];
}
sf.getRange('A18').values=[['全期合计']];sf.getRange('B18:J18').formulas=[Array.from({length:9},(_,i)=>`=SUM(${col(i+1)}8:${col(i+1)}16)`)];sf.getRange('A18:K18').format.fill='#DCEAF0';sf.getRange('A18:J18').format.font.bold=true;sf.getRange('B8:J18').setNumberFormat('0');
sf.getRange('A21:K21').merge();sf.getRange('A21').values=[['趋势解读：数字反映本次公开检索覆盖；不能用2025/2026的少量核实记录证明真实发生率下降。']];
sf.getRange('A23:E23').values=[['口径','件数','已知死亡/下限','已知受伤/下限','精确伤数不明案件']];
sf.getRange('A24:E25').values=[['核心',analysis.core.events,analysis.core.deaths_lower_total,analysis.core.injured_lower_total,analysis.core.injured_unknown_events],['扩展',analysis.expanded.events,analysis.expanded.deaths_lower_total,analysis.expanded.injured_lower_total,analysis.expanded.injured_unknown_events]];
sf.getRange('A27:K27').merge();sf.getRange('A27').values=[['以下为按分析脚本生成的快照；全量趋势、季度及敏感性见同名工作表和互动报告。']];
table('来源证据',sources,['id','title','publisher','published_date','url','original_url','access_status','type','independence_group','supports','key_facts','accessed_date'],{id:'来源编号',title:'来源标题',publisher:'发布机构',published_date:'发布日期',url:'核读链接',original_url:'原始社媒链接',access_status:'访问状态',type:'来源类型',independence_group:'同源组',supports:'支持事件/用途',key_facts:'核读事实与限制',accessed_date:'查阅日期'});
table('动机与背景标签',tags,['event_id','category','tag','theme','basis','summary','source_ids'],{event_id:'事件编号',category:'分类',tag:'原始标签',theme:'归并主题（解释层）',basis:'证据层级',summary:'动机摘要',source_ids:'支持来源'});
const pFields=['province','year','events','population_10k','records_per_million','urbanization_pct','income_yuan','unemployment_pct','employed_10k','tertiary_employed_10k','tertiary_employment_pct','population_source','urbanization_source','income_source','employment_source','unemployment_note','no_record_means'];
const p=table('省年背景',panel,pFields,{province:'省级地区',year:'年份',events:'核心记录件数',population_10k:'常住人口_万人',records_per_million:'每百万人公开记录数',urbanization_pct:'城镇化率_%',income_yuan:'居民人均可支配收入_元',unemployment_pct:'调查失业率_缺失',employed_10k:'就业人员_万人',tertiary_employed_10k:'第三产业就业_万人',tertiary_employment_pct:'第三产业就业占比_%',population_source:'人口来源',urbanization_source:'城镇化来源',income_source:'收入来源',employment_source:'就业来源',unemployment_note:'失业指标缺口',no_record_means:'未检出解释'});
for(let i=0;i<panel.length;i++){let r=i+2;p.sheet.getRange(`C${r}`).formulas=[[`=COUNTIFS(${ref('province')},A${r},${ref('year')},B${r},${ref('category')},"core")`]];p.sheet.getRange(`E${r}`).formulas=[[`=C${r}/(D${r}/100)`]];}
table('敏感性',analysis.sensitivity,Object.keys(analysis.sensitivity[0]),{year:'年份',scope:'统计口径',official_events:'官方直接支持分类件数',all_verified_events:'全部核实件数',largest_event_id:'当年最大死亡事件',deaths_lower_total:'死亡下限',deaths_without_largest:'移除最大事件后死亡下限'});
table('季度统计',analysis.quarterly,Object.keys(analysis.quarterly[0]),{quarter:'案发季度',events:'核心件数',deaths_known_total:'精确死亡已知合计',deaths_lower_total:'死亡含下限合计',deaths_unknown_events:'死亡不明案件',injured_known_total:'精确受伤已知合计',injured_lower_total:'受伤含下限合计',injured_unknown_events:'受伤不明案件'});
table('描述性关联',analysis.correlations,Object.keys(analysis.correlations[0]),{year:'年份',background:'背景指标代码',metric:'记录指标',n:'省级样本量',pearson_r:'Pearson相关系数',interpretation:'解释边界'});
table('2026补查',events.filter(e=>e.year===2026||e.review_year===2026),['id','date','date_precision','reported_date','title','province','city','category','classification_reason','deaths','deaths_lower_bound','injured','injured_lower_bound','casualty_note','dating_note','verification_gaps','source_ids','social_source_urls'],labels);
table('待核实与排除',events.filter(e=>!['core','expanded'].includes(e.category)),['id','date','title','province','category','classification_reason','deaths','injured','casualty_note','evidence_level','source_ids','notes'],labels);
table('检索覆盖',coverage,['query','scope_years','scope_regions','status','candidate_count','notes'],{query:'实际查询或访问项',scope_years:'年份范围',scope_regions:'地区范围',status:'状态',candidate_count:'候选数（未统计为空）',notes:'检出/失败与限制'});
table('字段字典',[...dict,...Object.entries(labels).filter(([k])=>!dict.some(d=>d.field===k)).map(([field,label])=>({field,label,definition:'汇总辅助值；根据原始字段派生。空值在下限加总中贡献0不代表实际为0。'}))],['field','label','definition'],{field:'字段代码',label:'中文标签',definition:'含义与空值规则'});
table('使用说明',[
 {主题:'研究定位',说明:'公开信息可核实事件库。2018-01-01至2026-09-16，中国大陆31省级地区。不是全部实际案件普查。'},
 {主题:'分类',说明:'core核心；expanded为纠纷扩大新增部分；核心+expanded为扩展口径；pending待核；excluded排除；organized_terror另列。当前未检出可核实的区间内有组织恐袭，不表示不存在。'},
 {主题:'核验',说明:'官方原文或可追溯完整转载，或两家独立采集可靠媒体。多次转载同一通报不算独立来源。field_sources分别标记事件/分类/伤亡/动机/结果。'},
 {主题:'未知与伤亡',说明:'空白保持未知，不自动按0。统计合计是已知值与明确下限相加；精确人数不明案件另列。作案者伤亡独立；警方处置、故意性未明碰撞附加人数不混入主动袭击合计。'},
 {主题:'动机',说明:'原始多标签保留；归并主题是分析编码，不是额外事实。精神健康单独记录证据，不自动作为动机。'},
 {主题:'时间',说明:'按案发日归年；同一连续过程计一件；跨日袭击用series_id关联；判决和执行不是新事件。2026只与历年1月1日至9月16日比较，不年化。'},
 {主题:'地区背景',说明:'2018—2024人口/城镇化/收入来自国家统计局2025年鉴同版序列；2025人口为一财汇总各省披露的二手表。人口修订不可当真实增减。省年关联使用31省记录数，未检出记0仅指记录数。'},
 {主题:'就业缺口',说明:'2024就业人数和第三产业就业仅描述结构。未取得省级连续同口径调查失业率，保留空白，不能用登记失业率替代。'},
 {主题:'解释',说明:'记录数和密度均受报道、可访问性、检索深度影响。相关不等于因果，地区关系不能推断个人动机。新增发现旧记录属于检索补漏，不能解释为当天风险上升。'},
 {主题:'更新',说明:'先补来源，再更新raw研究分组JSON与显式修订overrides，运行scripts/analyze.py后build_workbook.mjs及报告build。JSON/CSV是可复现数据主格式，Excel为发行快照。'},
 {主题:'来源与权利',说明:'所有链接保留；仅发布结构化事实和简要转述。外部新闻、原图、PDF及地理数据权利属于原发布者。本库不复制血腥图像或受害者住址。'},
 {主题:'复核',说明:'统计汇总B8:J18和省年记录密度使用Excel公式；季度、敏感性和描述性关联由Python复现脚本计算，修改数据后须重跑。'}
],['主题','说明']);
sh['使用说明'].getRange('A1:A13').format.columnWidth=18;sh['使用说明'].getRange('B1:B13').format.columnWidth=110;sh['使用说明'].getRange('B2:B13').format.wrapText=true;sh['使用说明'].getRange('A2:B13').format.rowHeight=55;
await wb.recalculate();
const actual=sf.getRange('B18:J18').values[0];
if(actual[0]!==analysis.core.events||actual[1]!==analysis.expanded.events||actual[2]!==analysis.core.deaths_lower_total||actual[3]!==analysis.core.injured_lower_total)throw new Error('Excel totals do not reconcile: '+JSON.stringify(actual));
console.log(await wb.inspect({kind:'region',sheetId:'统计汇总',range:'A7:K18',maxChars:1800,tableMaxRows:12,tableMaxCols:11}));
await fs.writeFile(path.join(validation,'xlsx_totals.json'),JSON.stringify({status:'passed',core:actual[0],expanded:actual[1],deaths_min:actual[2],injured_min:actual[3],sheets:names},null,2));
console.log(wb.help('workbook.render',{include:'index,examples,notes',maxChars:2800}).ndjson);
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(out,'中国大陆随机伤人事件_2018-2026.xlsx'));
for(const name of names){
 try{const png=await wb.render({sheetName:name,range:name==='统计汇总'?'A1:K27':name==='使用说明'?'A1:B5':'A1:F8',scale:1,format:'png'});await fs.writeFile(path.join(validation,`sheet_${name}.png`),new Uint8Array(await png.arrayBuffer()));}catch(e){console.log('Render failed '+name+': '+e.message);}
}
console.log('Saved workbook '+out);
