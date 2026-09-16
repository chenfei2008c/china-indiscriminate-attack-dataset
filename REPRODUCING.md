# 复现、检查与更新

## 1. 直接阅读

下载 `exports/互动报告.html` 后用浏览器打开，或在仓库根目录运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

访问 http://127.0.0.1:8000 。`docs/index.html` 与同目录 `snapshot.*.json` 必须一起保存。Excel、JSON、CSV 均可独立读取；本地服务只监听本机。

## 2. 分析复算

Python 3 标准库即可：

```bash
python3 scripts/build_context.py
python3 scripts/analyze.py
python3 scripts/validate.py
```

- `build_context.py` 保存按来源人工转录的同版年鉴数据和 2025 年人口汇总，生成 248 行省年背景表；不是在线自动抓取器。
- `analyze.py` 合并三组研究输入、补充来源、分类复核和事件拆分；重建 JSON、CSV、分析汇总及 `report/src/data.json`。
- `validate.py` 用 SQLite 独立重算 36 组年度/同期汇总和 248 个省年观测，核对来源关联，并读取 Excel 的公式缓存及错误单元格。

当前快照验收值：核心 51，扩展合计 63，核心受害者已知死亡 162、受伤明确值和下限合计 511。更改原始输入后，不应为维持这些计数而调整分类；需更新研究说明和导出文件。

## 3. 重建 Excel

使用带 `@oai/artifact-tool` 的 Codex 工作区 Node.js 环境，使该包可被 `scripts/build_workbook.mjs` 正常解析，再运行：

```bash
node scripts/build_workbook.mjs
python3 scripts/validate.py
```

该依赖不是 Python 标准库。仓库不包含本机运行时、`node_modules` 或私有路径。脚本输出工作簿、公式核对结果和各工作表预览；新增事件时重新建表，以扩展公式范围。`敏感性`、`季度统计` 和 `描述性关联` 是分析脚本生成的快照，不能只修改工作簿而期待这些表自动重算。

## 4. 重建互动报告

报告由 OpenAI Data 插件 1.0.8 的受保护共享运行时构建。编辑范围和契约见 `report/AGENTS.md`，项目内容主要在 `report/src/content/report/`、`report/src/data.json` 与主题文件。

在安装 Data 插件的 Codex 环境中，使用已配置的 Node.js 和插件 CLI 路径：

```bash
"$CODEX_NODE" "$DATA_APP_CLI" build --project-dir report --separate-data
"$CODEX_NODE" "$DATA_APP_CLI" export-offline --project-dir report \
  --output "$PWD/report/.data-app-offline/exports/report.html"
```

`CODEX_NODE` 是 Node 可执行文件路径，`DATA_APP_CLI` 是插件 `scripts/data-app.mjs` 路径。它们由使用者环境提供，不在仓库中硬编码。完成数据和内容更新后，将 `report/src/data.json` 的 `buildStatus` 设为 `complete` 再构建。验证后把 `report/dist/` 整体复制到 `docs/`，将离线导出复制为 `exports/互动报告.html`。

静态文件可供普通浏览器读取。编辑、提问、发布等共享运行时功能依赖支持它们的宿主；本项目交付的本地浏览、筛选、图表和来源功能不需要登录。

## 5. 更新证据

1. 新线索先核实发生、故意性和目标关系，分别记录证据。
2. 保存官方原文或完整可靠转载；两个媒体源须独立采集，不能按转载网站数计算。
3. 在研究输入和显式修订中注明修改字段、依据与原因。重复报道连接原事件；新的独立袭击才新增事件。
4. 未知保持 `null`，模糊人数记录原文与可证明下限；作案者伤亡单列。
5. 重算分析、工作簿和报告，检查完整年度、同期、空筛选、未知值、来源弹窗及窄屏。
6. 更新 README、研究解读、修订记录与验证记录，检查生成产物一致后提交。

本库没有稳定捕获率，也没有完整全国事件登记作为漏报基准；技术复现不能证明来源无误或检索穷尽。
