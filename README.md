# 中国大陆随机伤人事件公开资料库

2018—2026 年中国大陆随机伤人事件的公开资料检索、逐案核验和描述性分析。

仓库：[chenfei2008c/china-indiscriminate-attack-dataset](https://github.com/chenfei2008c/china-indiscriminate-attack-dataset)

> **资料截至 2026-09-16。** 案发范围为 **2018-01-01 至 2026-09-16**，覆盖中国大陆 31 个省级地区，不含港澳台。2026 年只统计截至 9 月 16 日的记录，不年化。

## 先看成果

- **[研究解读](RESEARCH.md)**：趋势、地域分布、共同因素、经济社会背景与分层防范建议。
- **[Excel 明细](exports/中国大陆随机伤人事件_2018-2026.xlsx)**：12 张工作表，含事件、逐字段来源、标签、汇总、背景和检索记录。点击 GitHub 文件页的下载按钮即可保存。
- **[互动报告下载](exports/互动报告.html)**：下载完整 HTML 后用浏览器打开，支持筛选、地图、同期比较及逐案来源查看。数据已包含在文件内，阅读外部来源需要联网。

也可在仓库根目录运行以下命令，再打开 **http://127.0.0.1:8000**：

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

报告的时间窗口、类别、年份、地区、场景、方式和证据筛选会同步作用于统计卡、图表与事件明细；表内搜索仅定位行。页面顶部的研究结论使用全库口径。仓库保存静态站点文件，未预设公开网站部署。

**主要发现：** 2018—2024 年核心记录为 13、7、6、5、3、6、10 起，呈下降后回升的变化；2024 年死亡合计受珠海单案显著影响。来源与分类标准的敏感性较大，2025—2026 年证据缺口尤其明显，现有记录不能判定全国实际发生率如何变化。

## 这个项目提供什么

- 逐案列出日期、地点、袭击方式、伤亡、受害关系、分类依据、已披露动机及司法进展。
- 将事件与来源逐字段关联，保留同源转载标识、伤亡修订说明和查询覆盖记录。
- 提供核心、扩展、待核、排除四类记录，支持复核不同定义对结论的影响。
- 提供年表、地域与场景汇总、去除最大单案后的敏感性，以及省级背景的描述性关联。

本库记录的是**能够检索并按统一标准核实的公开事件**，不能代表全部实际发生事件。记录密度不是犯罪发生率；资料缺失、来源失效、报道与裁判滞后都可能影响结果。

## 当前版本概况

| 分类 | 记录数 | 含义 |
| --- | ---: | --- |
| 核心 `core` | 51 | 主动袭击不特定或与原纠纷无关的人，包括针对学校等群体中的无关个体 |
| 扩展新增 `expanded` | 12 | 原本针对特定对象的纠纷，伤害扩大至原纠纷之外人员 |
| 待核 `pending` | 72 | 事件发生、故意性或随机性尚有至少一项证据不足 |
| 排除 `excluded` | 12 | 未满足范围或定义，如特定私人纠纷、事故、未实施威胁；逐案说明理由 |

当前候选共 147 条，来源 194 条，检索覆盖 345 条。汇总中的“扩展合计”＝核心＋扩展新增，为 63 起。`analysis.json` 的顶层 `expanded` 使用这一合并口径，不能再加一次核心数。

核心已明确受害者死亡合计 162 人，另有 1 起死亡人数未明确；受伤精确值合计 455 人，加入明确下限后至少 511 人。仍有 6 起没有完整精确伤者数，请同时阅读伤亡说明。

### 两个容易误读的地方

**待核不等于事件虚假。** 有的事件已经警方确认，但公开材料未说明受害者与作案者关系；有的候选则连发生细节也未可靠核实。例如，武汉青松路 2026-03-31 事件有警方确认的伤者信息，当前缺少随机性证据，因此暂列待核。请查看每条记录的 `classification_reason`，不要把所有待核记录视为同一种证据状态。

**2026 年核心为 0，不等于没有袭击。** 0 表示截至当前检索日，没有记录通过本库全部核心纳入条件。待核、排除与未被检出的事件仍可能存在；也不能用这一结果推断全国风险已下降。

## 文件导航

仓库根目录包含 `data/`、`scripts/`、`work/`、`report/` 和 `exports/`。

| 文件或目录 | 用途 |
| --- | --- |
| [data/events.json](data/events.json) / [CSV](data/events.csv) | 全部候选事件，含核心、扩展、待核和排除 |
| [data/sources.json](data/sources.json) / [CSV](data/sources.csv) | 来源、访问时间、同源转载组及支持的事件 |
| [data/excluded_pending.json](data/excluded_pending.json) / [CSV](data/excluded_pending.csv) | 待核与排除记录及理由 |
| [data/search_coverage.json](data/search_coverage.json) / [CSV](data/search_coverage.csv) | 实际查询、覆盖范围、访问失败和待核说明 |
| [data/analysis.json](data/analysis.json) | 年度、季度、地域、方式、缺失度、敏感性和相关分析 |
| [data/province_year_panel.json](data/province_year_panel.json) / [CSV](data/province_year_panel.csv) | 省年事件汇总与背景数据 |
| [data/provincial_context.json](data/provincial_context.json) | 省级人口、城镇化、收入及来源标识 |
| [data/motive_tags.json](data/motive_tags.json) / [CSV](data/motive_tags.csv) | 动机与背景标签，多标签可重叠 |
| [data/field_dictionary.json](data/field_dictionary.json) / [CSV](data/field_dictionary.csv) | 字段说明 |
| [scripts/](scripts/) | 数据整理、汇总与工作簿生成脚本 |
| [work/](work/) | 研究输入、分类复核与中文解读 |
| [report/](report/) | 互动报告及其源文件 |
| [exports/](exports/) | 可直接打开的报告、表格等交付文件 |
| [RESEARCH.md](RESEARCH.md) | 中文研究解读：趋势、地域、背景与防范 |
| [docs/](docs/) | 可用本地 HTTP 服务打开的静态报告 |
| [validation/](validation/) | 数据、公式、独立复算及浏览器验收记录 |

JSON 适合保留嵌套来源与标签；CSV 采用带 BOM 的 UTF-8，数组或对象字段保存为 JSON 文本，便于常见表格软件读取。

## 核验方法

1. 按年份、地区和袭击方式检索公开资料，用汇编发现线索，再回查法院、检察院、公安通报或可靠媒体正文。
2. 官方材料及可靠完整转载可以支持事件事实；无官方材料时，要求两个独立采集的可靠媒体来源。多个网站转载同一稿件只算同一证据来源。
3. 分别核实“发生了什么”和“是否符合随机/无关对象的定义”。多人伤亡、公共场所、受害者国籍、精神健康信息都不能单独证明随机性。
4. 按独立连续袭击过程去重，后续起诉、判决、执行公告归入原事件；同一作案者中断后重新实施的袭击可分案记录，即使在同一天发生，并用 `series_id` 关联。长春系列 B40a、B40b、B41 共三次，伤亡不重复累计。
5. 优先追踪较完整的后续伤亡和司法信息，保存修订依据。初报、起诉指控、法院认定与未证实说法保持区别。

“随机伤人”是本研究的操作性分类，不是统一的法律罪名。核心与扩展之间可能存在边界争议，详见逐案分类依据。有组织恐怖袭击若得到确认，按单独类别处理，不混入核心趋势。

## 读取数据前，请了解这些字段

| 字段 | 阅读方式 |
| --- | --- |
| `id` | 稳定事件编号，用于连接来源与修订记录 |
| `category`、`classification_reason` | 当前分类及证据理由；筛选统计前必须先明确口径 |
| `official_occurrence`、`official_classification` | 分别表示发生获官方确认、官方材料直接支持本库分类，两者不能混为一谈 |
| `deaths`、`injured` | 尽可能采用最新可核实口径的受害者死亡、受伤数字；未知为 `null` |
| `injured_reported`、`injured_lower_bound` | 保留“多人”“20余人”等原口径与可确认下限，不强行精确化 |
| `attacker_deaths`、`attacker_injured` | 作案者伤亡单列，不混入受害者合计 |
| `casualty_asof`、`casualty_note` | 伤亡口径截至何时、是否有修订或冲突 |
| `additional_collision_injured`、`response_injured` | 故意性未明的碰撞伤者、警方处置伤者等特殊边界，须结合说明阅读 |
| `motive_summary`、`motive_basis` | 已披露动机及证据层级；检方指控或警方初查不等于法院最终认定 |
| `source_ids`、`field_sources` | 整案及日期、地点、伤亡、分类、动机、结局各字段的来源编号 |
| `last_source_date` | 当前收录的最后来源日期，不保证其后没有新进展 |

`null` 与 0 不同：前者未知，后者须有证据支持。精确值合计、保守下限合计、未知项数量应同时报告，不能将空值补零后声称得到完整伤亡。标签一案可多项，也不能把标签计数相加为互斥总数。

## 复现与使用示例

在包含 `data/` 的仓库根目录，用 Python 标准库读取当前分类：

```bash
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

events = json.loads(Path('data/events.json').read_text(encoding='utf-8'))
print(Counter(event['category'] for event in events))
core = [event for event in events if event['category'] == 'core']
print('核心记录:', len(core))
print('已知死亡合计:', sum(event['deaths'] for event in core if event['deaths'] is not None))
print('死亡未明确事件:', sum(event['deaths'] is None for event in core))
PY
```

维护者可用 `python3 scripts/build_context.py` 生成省级背景表，再运行 `python3 scripts/analyze.py` 重建汇总。完整重算依赖 `work/` 中的研究输入、来源和分类文件，以及当前报告快照 `report/src/data.json`；脚本会写入数据、检查结果和报告快照。仅分析已发布数据时无需重算。

```bash
python3 scripts/build_context.py
python3 scripts/analyze.py
python3 scripts/validate.py
```

上述分析和验证使用 Python 标准库。`validate.py` 以独立 SQLite 查询核对年度、同期和省年统计，并读取已发布 Excel 的公式缓存；更改数据后须先重建工作簿，再运行完整验证。

工作簿由 `scripts/build_workbook.mjs` 使用 `@oai/artifact-tool` 生成，依赖支持该库的 Codex 工作区 Node.js 环境。互动报告使用 Data 插件的受保护运行时；在安装相应插件的环境中，用其 `data-app.mjs build --project-dir report --separate-data` 重建，再通过 `export-offline` 导出。详见 [复现说明](REPRODUCING.md)。普通读者查看已生成的 HTML、Excel 和 JSON 无需这些创作依赖。

省级关联使用 2018—2024 年同版年鉴数据，每年分别计算 31 省的 Pearson 相关系数。未检出地区在“公开记录数”中为零，不能理解为真实零发生。现有资料缺少同口径的省级调查失业率连续面板，不用登记失业率或产业就业结构代替，也不据省级关联推断个人原因。

## 更正与更新

可通过 [Issues](https://github.com/chenfei2008c/china-indiscriminate-attack-dataset/issues) 或 Pull Request 提交更正。建议提供：

- 事件编号，或新候选的案发日期、地点与事件名称；
- 拟修改的字段、当前值、建议值；
- 可打开的来源链接、发布机构与发布日期；
- 支持该字段的必要短摘录或简明说明；
- 来源是独立采集还是转载，以及是否存在相反证据。

后续更新按“补来源 → 核查字段 → 记录修订原因 → 重算汇总 → 检查报告和导出文件”的顺序进行。新增通报可能使待核转入核心或扩展，也可能支持排除；伤亡与动机可随司法进展更新。没有新证据时不因转载增多自动提高等级。当前为一次检索快照，未承诺固定更新频率或持续实时监控。

提交材料请保留必要事实与公开来源，不上传血腥影像、私人住址或不必要的受害者个人信息。来源网页与文献保留原机构版权。

## 如何引用

请固定到使用时的 commit 或发布版本，并同时注明资料截止日、统计口径和访问日期。例如：

> 中国大陆随机伤人事件公开资料库（2018-01-01—2026-09-16），chenfei2008c/china-indiscriminate-attack-dataset，commit `<实际提交哈希>`，访问日期 `<YYYY-MM-DD>`。使用核心口径；伤亡为已知值及明确下限。

引用个案时，加上事件编号和原始来源。引用趋势时说明是否包含扩展事件、2026 年仅到 9 月 16 日，以及未知项如何处理。请勿把本库计数写成“中国实际发生总数”，也勿把未检出或待核写成已证伪。
