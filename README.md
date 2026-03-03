# create-djl-django

`django-admin startproject --template` 的 Django 项目模板仓库。

仓库地址：<https://github.com/App1ePine/create-djl-django>

## 使用方式

### 方式 A：固定版本

```bash
django-admin startproject mysite ./mysite \
  --template=https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/v0.1.3
```

### 方式 B：使用最新版本

```bash
TAG=$(git ls-remote --tags --sort='v:refname' https://github.com/App1ePine/create-djl-django.git \
  | awk -F/ '{print $3}' \
  | grep -E '^v?[0-9]+(\.[0-9]+)*$' \
  | tail -n1)

django-admin startproject mysite ./mysite \
  --template="https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/${TAG}"
```

## 依赖安装

项目创建后，至少安装以下依赖：

```bash
pip install django djangorestframework drf-spectacular
```

接口文档地址：

- Swagger UI: `/`
- OpenAPI Schema: `/api/schema/`

## 模板目录

- 模板根目录：`create-djl-django/`
- 项目包占位目录：`project_name/`
- Python 包路径占位变量：`{{ project_name }}`

## 首次初始化 GitHub 仓库

在本项目目录执行：

```bash
cd /path-to/create-djl-django

git init
git branch -M main
git add .
git commit -m "feat: init django template"
```

### 方式 A：使用 GitHub CLI（推荐）

```bash
gh auth login
gh repo create create-djl-django --public --source=. --remote=origin --push
```

### 方式 B：网页创建后手动绑定 remote

```bash
git remote add origin xxx
git push -u origin main
```

## 日常迭代流程（推荐）

1. 修改模板内容并提交到 `main`。
2. 发版前自动更新 README 中的示例 tag（例如 `v1.0.2`）。
3. 打版本标签并推送（例如 `v1.0.2`）。
4. 创建新项目时，`--template` 使用对应 tag 的链接（推荐）或使用上文“自动最新 tag”命令。

```bash
git add .
git commit -m "feat: update template"
git push origin main

./scripts/update-readme-tag.sh v1.0.2
git add README.md
git commit -m "docs: bump template tag to v1.0.2"

git tag v1.0.2
git push origin v1.0.2
```
