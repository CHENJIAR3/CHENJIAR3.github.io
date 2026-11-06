# Get Citation Data 故障诊断与修复

核验日期：2026-11-06。**本地代码已修复并真实抓取成功；GitHub 线上仍是旧代码，需要上传本目录的修改并启用新的发布方式。**

## 1. 已核验的事实

- 公开仓库最新任务 [#821](https://github.com/CHENJIAR3/CHENJIAR3.github.io/actions/runs/42063208235) 失败，运行的是提交 `d862f1b88eb0f058d7f84b7240cfcee13ae80c9d`。安装依赖和执行爬虫混在 `Run` 步骤中，该步骤约 10 秒后失败。
- 线上代码仍先导入 `scholarly`，再调用 `FreeProxies()`，成功后才创建 `results/`；与本地修复版不同。
- 用本地原 requirements 全新安装，实际得到 `bibtexparser==2.1.0`。执行 `from scholarly import scholarly`，可稳定复现：

```text
from bibtexparser.bibdatabase import BibDatabase
ModuleNotFoundError: No module named 'bibtexparser.bibdatabase'
```

这发生在任何 Scholar 请求、代理初始化、JSON 输出之前。`scholarly==1.7.11` 需要 bibtexparser 的 1.x API，但没有为它声明 `<2` 上限。

历史任务完整日志需要 GitHub 登录才能下载，因此不能断言过去每一次失败都来自同一异常。此前仅凭耗时认定“免费代理网站失效”的说法证据不足，也不能把“free-proxy 自 2019 年不维护”作为结论。

- OpenAlex 作者单条查询可以返回数据，但论文列表查询实测返回 **HTTP 429 / Insufficient budget**：匿名共享 IP 的每日额度已经用尽。之前“免费、无需 key、不封 IP，所以一定可用”的表述不成立。[官方认证与额度说明](https://help.openalex.org/api/authentication/)
- GitHub 明确说明：`GITHUB_TOKEN` 推送的提交不会触发分支式 Pages 构建。仅把 JSON 提交到 main，不能保证页面更新。[官方 Pages 文档](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 2. 已完成的修复

| 文件 | 修复 |
| --- | --- |
| `google_scholar_crawler/requirements.txt` | 新增 `bibtexparser==1.4.3`，保留 scholarly/httpx 的兼容版本 |
| `google_scholar_crawler/main.py` | 用独立子进程限制 Scholar 总耗时，覆盖导入、代理、抓取与填充；Windows 和 Linux 均适用 |
| 同上 | 配置代理时同时传给 scholarly 的主、备用连接，避免其隐式再次调用 FreeProxies |
| 同上 | 只填充 basics/indices/counts/publications，减少无关网络请求 |
| 同上 | 支持 `OPENALEX_API_KEY` Bearer 认证；使用作者 ID、每页 100 条、基本分页；重试短暂网络/服务错误，配额耗尽立即给出明确提示 |
| 同上 | 校验作者身份、指标与论文列表；缺字段不再当成 0；两路失败退出 1，并保留旧数据 |
| 同上 | 深拷贝旧论文数据，修正单篇引用变化被漏检的问题；记录各篇引用的数据源；缺失的 badge JSON 可以自动修复 |
| `.github/workflows/google_scholar_crawler.yaml` | 安装后检查依赖并运行回归测试；传入备用源 Key；安全提交数据，推送竞争时有限重试；保留失败日志 |
| `.github/workflows/pages.yaml` | 在 main 推送和爬虫成功后显式构建、发布 Pages，补齐机器人提交不触发构建的问题 |
| `_pages/about.md`、`assets/css/main.scss` | 徽章直接显示本地构建的数据及真实来源，不再依赖 Shields.io 图片 |
| `_includes/fetch_google_scholar_stats.html` | 保留空元素/缺失论文保护，标明单篇引用来源，并转义内联 JSON 的结束标签 |
| `_data/gs_data*.json` | 已以真实 Scholar 抓取结果更新：总引用 164，h-index 7，i10-index 5 |

## 3. 已执行的验证

- 原始依赖环境：复现 bibtexparser 导入异常。
- 修复依赖后：`pip check` 通过；scholarly 与旧版 BibDatabase API 均可导入。
- 真实 Scholar 抓取成功，约 7 秒完成。实际 `_data` 快照时间为 `2026-11-06 19:18:41`（北京时间），来源 `google_scholar`，总引用 **164**。
- 23 项离线回归测试通过，覆盖两路失败保留原文件、缺失指标、错误身份、禁止回退、单篇引用变化、代理双连接、真实子进程超时、认证、分页、配额错误、重试和敏感信息隐藏。
- OpenAlex 无 Key 的真实请求验证：退出码 1，明确提示配置 `OPENALEX_API_KEY`，未写入伪造的 0 或替换 Scholar 快照。
- 两份 GitHub Actions 工作流通过 actionlint；Python 语法、YAML 触发关系检查通过。
- Scholar/OpenAlex 两种 Liquid 徽章模板渲染通过；全站 SCSS 编译通过；引用显示 JavaScript 在 DOM 已加载/未加载、缺失总引用元素和未知论文 ID 场景通过；内联 JSON 结束标签转义通过。
- 本机没有可用 Ruby/Jekyll 环境，Docker 引擎也未运行；完整 Jekyll 构建和真实 Pages 部署需在上传后由工作流验证，不能把本地测试通过等同于线上已修复。

## 4. 上线步骤

这个目录是下载的源码副本，没有 `.git` 元数据，因此本次没有直接推送到 GitHub。

1. 将本目录的修改上传到仓库 **main**：特别注意隐藏目录 `.github/workflows/` 的两个 YAML，以及 `google_scholar_crawler/`、`_data/`、`_includes/fetch_google_scholar_stats.html`、`_pages/about.md`、`assets/css/main.scss` 和文档。不要上传 `.venv/` 或 `.citation-check/`。
2. 仓库 `Settings → Pages → Build and deployment → Source` 选择 **GitHub Actions**，让新建的 Deploy Pages 工作流负责发布。
3. 在 `Settings → Secrets and variables → Actions` 配置：
   - `GOOGLE_SCHOLAR_ID`（Secret，可省略，默认 `40KXmRMAAAAJ`）。
   - `GOOGLE_SCHOLAR_PROXY`（Secret，可选）：需要一个实际可用且能访问 Scholar 的代理。
   - `OPENALEX_API_KEY`（Secret，启用备用源时建议配置）：从 [OpenAlex 设置](https://openalex.org/settings/api) 获取，避免匿名共享额度耗尽。不要把 Key 写进源码。
   - `ORCID_ID`（Variable，可省略，默认 `0000-0002-7150-5239`）。
   - 若只允许 Scholar 数字，设 Variable `CITATION_OPENALEX_FALLBACK=false`。
4. 确保 Actions 已启用且仓库策略允许工作流写入代码。YAML 已声明 `contents: write`；如果 main 有保护规则，需要允许机器人更新数据，或按仓库要求走 PR。
5. `Actions → Get Citation Data → Run workflow`，先选 `scholar` 验证目标来源；需要回退时选 `auto`。成功后应自动出现 `Deploy Pages` 并完成 build/deploy。
6. 验收：`_data/gs_data.json` 有真实来源和时间，页面徽章显示对应来源和数字，后续每天北京时间 16:00 左右自动运行（GitHub 定时任务可能延迟）。

旧 `google-scholar-stats` 分支可保留作备份，新代码无需依赖它。

## 5. 本地复查

当前目录已创建隔离环境，可在 PowerShell 执行：

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s google_scholar_crawler -p 'test_*.py' -v
.\.venv\Scripts\python.exe google_scholar_crawler/main.py --source scholar --out _data
```

重新安装环境时，使用 Python 3.11 或 3.12 创建 `.venv`，再安装 requirements。工作流固定为 Python 3.11。

默认 `auto` 会先抓 Scholar，失败才尝试 OpenAlex。二者覆盖范围和计数口径不同，不能把 OpenAlex 的 268 当成 Scholar 的 164；切换来源时，页面标签和链接会随之切换。未在 OpenAlex 匹配到的旧论文保留原数值及来源。
