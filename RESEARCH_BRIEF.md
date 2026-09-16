# 中国大陆随机伤人事件研究：执行约定

截至日期：2026-09-16；案发范围：2018-01-01至2026-09-16，中国大陆31省级地区。用户批准完整公开信息研究、互动报告、Excel明细。新项目独立保存，不改变既有项目。

## 分类
core：对不特定/与原纠纷无关的人实施主动袭击；包括针对学校等群体中无关个体。
expanded：原本针对特定对象的纠纷扩大到无关人员。
pending：事件发生、故意性或无差别特征未得到充分证实。
excluded：仅私人定向纠纷、交通事故、未实施威胁或区间外；保留具体理由。
organized_terror：已认定的有组织恐怖袭击另列。
核心必须有支持随机性的证据，不能只凭受害者多。精神疾病和刑责能力另列，不自动等同动机。
官方通报/法院材料（包括可靠完整转载）可以建立事件事实；否则需两个独立采集的可靠媒体。转载同一稿不能算多源。没有材料的字段null，不臆造零伤亡或动机。

## 各组交付
在 work/group_NAME.json 写 JSON：{events:[],sources:[],coverage:[],notes:[]}，记录事实用自己的简明措辞；仅保留必要短引文。务必保存成功查询和未检出记录。

事件字段：id（组名前缀）, date(YYYY-MM-DD或YYYY-MM/null), date_precision(day/month/year), title, province（北京/天津/河北/山西/内蒙古/辽宁/吉林/黑龙江/上海/江苏/浙江/安徽/福建/江西/山东/河南/湖北/湖南/广东/广西/海南/重庆/四川/贵州/云南/西藏/陕西/甘肃/青海/宁夏/新疆）, city, district, urban_rural, scene(街道交通/校园及周边/商业场所/公园广场/医疗机构/社区住宅/机关单位/公共交通/其他), method(持械/驾车/纵火/爆炸/复合/其他), category(core/expanded/pending/excluded/organized_terror), classification_reason, deaths(number|null), injured(number|null), serious_injuries(number|null), attacker_deaths(number|null), attacker_injured(number|null), casualty_asof, casualty_note, involves_children(boolean|null), victim_relation, age(number|null), sex, occupation, motive_summary, motive_tags(array), motive_basis(法院认定/警方初步通报/媒体调查/未知), mental_health, prior_violence, warning_signals, intervention, outcome, judgment_date, execution_date, last_source_date, evidence_level(官方原文/官方转载/多源媒体/单一媒体/网传待核), source_ids(array), field_sources(object，date/location/casualties/classification/motive/outcome各对应source id数组), notes。

来源字段：id, url, title, publisher, published_date, accessed_date（2026-09-16）, type（法院/检察院/公安/官方媒体/独立媒体/汇编线索/研究/统计）, independence_group（同源转载用同组）, supports（涉及event id数组）, key_facts（简明转述）。不保存血腥影像、个人住址和受害者姓名。

coverage条目：query, scope_years, scope_regions, status(已检索/访问失败/待核), candidate_count（可null）, notes。需要网上实际搜索，不能记忆编数。正文必须打开核对；仅摘要可见时注明。后续法院裁判比初报更完整时保留修订依据。所有事件按案发日去重。

## 审查要点
1. 不把重大暴力犯罪总体统计替代随机伤人趋势。
2. 2026不年化；不同年份报告可见性不一致，不声称真实发生率。
3. 已核实范围不等于随机性已证实。两者分开。
4. 不设事件数目标，不为凑数纳入不确定案例。

## 执行记录
- 任务A：2018—2020逐案研究。
- 任务B：2021—2023逐案研究。
- 任务C：2024—2026逐案研究。
- 主任务：全国地区补漏、统计背景、防范文献、统一复核、分析和交付。
- Ruling：本工作是新建研究产物，独立outputs目录隔离；不修改既有应用；用户后续明确授权将最终研究、报告和README推送至 https://github.com/chenfei2008c/china-indiscriminate-attack-dataset.git 。
