# create-djl-django

`django-admin startproject --template` 的 Django 项目模板仓库。

仓库地址：<https://github.com/App1ePine/create-djl-django>

## 使用方式

```bash
django-admin startproject mysite ./mysite \
  --template=https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/v1.0.0
```

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
2. 打版本标签并推送（例如 `v1.0.1`）。
3. 创建新项目时，`--template` 使用对应 tag 的链接。

```bash
git add .
git commit -m "feat: update template"
git push origin main

git tag v1.0.1
git push origin v1.0.1
```
