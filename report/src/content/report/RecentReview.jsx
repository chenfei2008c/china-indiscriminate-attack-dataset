import React from 'react';
import {DataComponent,Filters,RichNarrative,useSectionFilters} from '../../data-app-public.jsx';

const filterDefinitions=[
  {id:'month',label:'案发月份',field:'month',defaultValue:'all',queryIds:['recent']},
  {id:'status',label:'核验分类',field:'category_label',defaultValue:'all',queryIds:['recent']},
  {id:'province',label:'省级地区',field:'province',defaultValue:'all',queryIds:['recent']},
];
const labels={core:'核心事件',expanded:'纠纷扩大',pending:'待核线索',excluded:'排除记录'};
const known=(e,key)=>e[key]!=null?String(e[key]):e[key+'_lower_bound']!=null?'至少 '+e[key+'_lower_bound']:'未明确';

export default function RecentReview({snapshot,onSelect}){
  const scope=useSectionFilters(filterDefinitions,{}, {id:'review-2026'});
  const props=scope.componentProps('recent',['id','date','month','category_label','province']);
  const rows=[...(props.displayRows||[])].sort((a,b)=>(b.date||'').localeCompare(a.date||'')||a.id.localeCompare(b.id));
  const s=snapshot.researchSummary.update_2026;
  const all=snapshot.queries.recent.rows;
  const counts=Object.fromEntries(['core','expanded','pending','excluded'].map(k=>[k,rows.filter(e=>e.category===k).length]));
  const narrative=`上一版收录了 ${s.previous_records} 条 2026 年线索。本轮以李老师的 X 账号 **@whyyoutouzhele** 为补漏入口，结合警方、法院、见义勇为材料与媒体采访，新增 ${s.new_records.length} 条，当前共 ${s.current_records} 条。案发日期尚不明确、但在 2026 年发现的投稿也单列于此，不能据发帖日归入年度或月份趋势。\n\n**线索数与已核实事件数分开展示。** 帖文及镜像可以帮助发现遗漏；同源转载不增加独立证据。事件确已发生，也可能仍缺攻击对象关系或故意性的证据。以下清单包含待核与排除项，它们不会计入后面的核心趋势。`;
  return <section id="review-2026" className="chapter recent-review">
    <div className="section-heading"><span className="section-number">01</span><div><div className="section-kicker">2026 年专项补查</div><h2>把遗漏的线索放回视野</h2></div></div>
    <DataComponent id="recent-review-intro" queryId="recent" sourceRows={all} displayRows={all} title="2026补查说明" kind="narrative"><RichNarrative id="recent-review-summary" value={narrative}/>
    </DataComponent>
    <div className="review-filter-bar"><Filters {...scope.filterProps}/></div>
    <DataComponent id="recent-register" queryId="recent" {...props} displayRows={rows} sourceRows={rows} title="2026事件与线索清单" kind="table">
      <div className="review-counts" data-reviewed-rows>{Object.entries(labels).map(([key,label])=><div className={'review-count '+key} key={key}><strong>{counts[key]}</strong><span>{label}</span></div>)}
      </div>
      <p className="review-result-label">当前筛选 {rows.length} 条 · 已知案发日期倒序，日期待核列后 · 点击查看分类、修订和原帖依据</p>
      {!rows.length?<div className="empty-state" role="status">此组筛选未检出线索；请恢复为 All 查看其他记录。</div>:<div className="case-grid" data-reviewed-rows>{rows.map(e=><article key={e.id} className={'case-card '+e.category}>
        <div className="case-meta"><time dateTime={e.date||undefined}>{e.date||'案发日期待核'}</time><span className={'status-tag '+e.category}>{labels[e.category]||e.category_label}</span></div>
        <h3>{e.title.replace(/（排除）$/, '')}</h3>
        <div className="case-location">{e.province} · {e.city||'城市待核'} · {e.method}</div>
        <p className="case-reason">{e.classification_reason}</p>
        <div className="case-facts"><span>受害者死亡 <b>{known(e,'deaths')}</b></span><span>受伤 <b>{known(e,'injured')}</b></span></div>
        <div className="case-evidence">{e.official_occurrence?'事件发生有官方确认':e.evidence_level==='多源媒体'?'有独立媒体材料':'公开线索，证据尚有限'}{e.category==='pending'?' · 分类待核':''}</div>
        <button className="case-open" onClick={()=>onSelect(e)} aria-label={'查看'+e.title+'的补查依据'}><span>{e.id} · 查看证据</span><span aria-hidden="true">↗</span></button>
      </article>)}</div>}
    </DataComponent>
  </section>;
}
