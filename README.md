# Minghao Zhu 的个人网站

基于 Jekyll / al-folio。导航为 Home、News、Publications 和 Repositories；个人 CV 页面保留在 `/cv/`。

## 本地使用

全新 Apple Silicon Mac 需要 Apple Command Line Tools 和 Python 3。在仓库根目录执行：

```sh
python3 bin/setup-local.py
bin/site serve
```

安装脚本下载固定版本的 Ruby 3.3.11、Bundler 4.0.6、Node 24.19.0，并验证下载文件的 SHA-256。已有环境只需运行 `bin/site serve`。

打开 `http://127.0.0.1:4000/`。页面修改后自动构建，刷新查看；修改 `_config.yml` 后重启服务。按 Ctrl-C 停止。实际 `baseurl` 为空。

```sh
bin/site build
bin/site check
bin/site format-check
bin/site audit
bin/al-folio upgrade audit
```

`check` 检查生成 HTML 的本地链接和资源，不请求外部服务。其他平台安装匹配版本的 Ruby、Bundler 和 Node 后，执行 `bundle install`、`npm ci`、`bundle exec jekyll build` 和 `bundle exec ruby bin/check-site.rb`；格式检查使用 `npm run lint:prettier`。

移动项目后，先将 `.local` 移到仓库外备份，再执行安装脚本，避免复用旧的 Ruby 前缀和动态库路径。日常构建通过 `bin/site` 使用隔离的本地环境。

## 文件入口

- `_pages`、`_news`：页面和个人动态。
- `_data`：个人经历、联系方式、仓库配置。
- `_bibliography/home-papers.bib`：论文信息。
- `assets/img`：当前展示的照片和论文图片。
- `_layouts`、`_includes`、`_sass`、`assets/css`：个人布局及主题覆盖。
- `bin`：本地环境、构建和检查入口。
- `.github/workflows`：部署、格式检查和升级审计。

首页展示 `selected=true` 的论文和 `featured=true` 的动态；Publications 展示完整论文列表。个人样式集中在 `_sass/_personal.scss`，有意覆盖的主题文件登记在 `.al-folio-overrides.yml`。

主题运行时由锁定的 gems 提供。`.local` 和 `node_modules` 是本地依赖，`_site`、`.jekyll-cache` 是生成输出与缓存，均不提交。清空 `.local/downloads` 和 `.local/npm-cache` 不影响已有环境的构建。

## 远程资源与发布

GitHub 卡片直接加载 `_config.yml` 中 `external_services.github_readme_stats_url` 指定的远程服务，没有本地快照或超时回退。CDN 字体与卡片依赖访问者的网络和服务可用性。

`_data/repositories.yml` 控制展示仓库和统计角色，包含 `OWNER`、`ORGANIZATION_MEMBER`、`COLLABORATOR`；统计卡片纳入自有贡献仓库。展示列表不会自动改变统计范围，缓存版本参数不能调整公共服务的缓存策略。

GitHub Pages 的发布源需要在仓库设置中配置；本地构建成功不代表公网已发布。项目修改约定见 [AGENTS.md](AGENTS.md)。

基于 [al-folio](https://github.com/alshedivat/al-folio)，许可证见 [LICENSE](LICENSE)。
