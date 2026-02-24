# Django 项目模板

## 模板目录

`/path-to/create-djl-django`

## 本地使用

```bash
django-admin startproject mysite ./mysite \
  --template=/path-to/create-djl-django
```

## 远程仓库使用（推荐）

```bash
django-admin startproject mysite ./mysite \
  --template=https://codeload.github.com/<user>/<repo>/zip/refs/tags/v1.0.0
```

## 说明

- 项目包目录使用 `project_name` 作为占位目录名。
- Python 文件中包路径使用 `{{ project_name }}` 作为占位变量。
