# 本项目的开发约定

本仓库是 Minghao Zhu 的个人网站，基于 al-folio v1，已从完整演示模板精简。它不是 al-folio 上游 starter 的开发仓库。用户已有的个人内容和本地主题覆盖应保留。

## 修改范围

- 页面与内容：`_pages`、`_news`、`_data`、`_bibliography`、`assets/img`。
- 个人主题覆盖：`_layouts`、`_includes`、`_sass`、`assets/css`。修改时保持 al-folio 样式，并检查 `.al-folio-overrides.yml`。
- 新增或删除运行时插件，需要同时修改 `Gemfile`、`Gemfile.lock` 和 `_config.yml`，确认页面实际需要该插件。
- 基础布局、导航、Sass 与默认仓库卡片来自 `al_folio_core`；图标、引用、图片和升级审计由锁文件中的插件提供。不要为了修改少量个人内容复制完整主题运行时，也不要修改 `.local/bundle` 中的 gem 文件。
- 不改写用户已有的未提交内容；清理前做可恢复备份，不把旧依赖目录当源码。

## 环境与验证

安装与使用方式见 [README.md](README.md)。Apple Silicon 本地工具在 `.local`，不要依赖系统 Ruby、旧 `.bundle` 或 Python 虚拟环境。实际 baseurl 为空，预览地址是 `http://127.0.0.1:4000/`。

```sh
bin/site build
bin/site check
bin/site format-check
bin/site audit
bin/al-folio upgrade audit
bin/site serve
```

全新机器先执行 `python3 bin/setup-local.py`。修改页面后检查本地预览；外部 GitHub 卡片服务的故障需与本地构建结果分开报告。配置文件变更需重启 Jekyll。

此次清理已归档上游演示集成测试、Docker 流程和截图工具，不要运行文档旧版本里的已删除命令，也不要恢复 `/al-folio` baseurl。实际保留的 CI 是页面构建及内部链接检查、格式检查、升级审计。

## 布局与主题覆盖

- 首页由 `_pages/about.md`、`_data/homepage.yml` 和 `_layouts/home.liquid` 渲染；论文使用 `_bibliography/home-papers.bib` 和 `_layouts/home_publication.liquid`。
- 新闻由 `_news` 和 `_includes/personal_news_row.liquid` 渲染；仓库由 `_data/repositories.yml`、`_pages/repositories.md` 和 `_includes/repository/` 渲染。
- `assets/css/main.scss` 导入主题 Sass 与 `_sass/_personal.scss`，个人样式集中在后者。
- 当前登记五个主题覆盖：`_includes/head.liquid`、`_includes/header.liquid`、`_includes/repository/repo.liquid`、`_includes/repository/repo_user.liquid`、`assets/css/main.scss`。修改后核对 `.al-folio-overrides.yml`，升级前运行升级审计，保留个人定制。

仓库内只保留 README、开发约定及页面和新闻所需的 Markdown。重复工具说明、内部审计和清理记录放在仓库外；不要恢复已归档的上游演示或迁移说明。
