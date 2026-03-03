# create-djl-django

`django-admin startproject --template` 的 Django 项目模板仓库。

仓库地址：<https://github.com/App1ePine/create-djl-django>

## 使用方式

先统一三个概念：

- `PROJECT_PATH`：项目落盘路径（`startproject` 第二个参数）
- `PROJECT_NAME`：项目包名/管理目录名（`startproject` 第一个参数）
- `APP_NAME`：应用目录名（模板里默认占位为 `app_name`）

### 1. 最简单：使用指定模板版本 + 不通过脚本调整占位应用名

```bash
PROJECT_PATH=./mysite
PROJECT_NAME=mysite

mkdir -p "${PROJECT_PATH}"
django-admin startproject "${PROJECT_NAME}" "${PROJECT_PATH}" \
  --template=https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/v0.1.4
```

说明：

- `PROJECT_PATH` 和 `PROJECT_NAME` 可以不同（例如路径是 `./backend`，项目包名是 `application`）；
- 默认会生成占位 app 目录 `app_name/`；
- 若你不想使用占位名，可在创建后手动重命名并同步修改 `INSTALLED_APPS`、`urls.py`、`apps.py`。

### 2. 使用最新模板版本 + 不通过脚本调整占位应用名

```bash
TAG=$(git ls-remote --tags --sort='v:refname' https://github.com/App1ePine/create-djl-django.git \
  | awk -F/ '{print $3}' \
  | grep -E '^v?[0-9]+(\.[0-9]+)*$' \
  | tail -n1)

PROJECT_PATH=./mysite
PROJECT_NAME=mysite

mkdir -p "${PROJECT_PATH}"
django-admin startproject "${PROJECT_NAME}" "${PROJECT_PATH}" \
  --template="https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/${TAG}"
```

### 3. 通过脚本调整占位应用名（在 1 或 2 的基础上再执行）

```bash
PROJECT_PATH=./mysite
APP_NAME=demo

python "${PROJECT_PATH}/scripts/update_placeholder_app_name.py" "${APP_NAME}"

# 或者使用单行命令
PROJECT_PATH=./mysite APP_NAME=demo python "${PROJECT_PATH}/scripts/update_placeholder_app_name.py" "${APP_NAME}"
```

说明：

- `django-admin startproject` 原生命令只支持 `project_name`；
- `app_name` 通过 `scripts/update_placeholder_app_name.py` 对占位目录 `app_name/` 做二次替换。

### 4. 在 Shell 中封装一条命令（兼容 zsh/bash，__推荐__）

说明：

- 同一份函数可用于 `zsh` 与 `bash`；
- `zsh` 用户写入 `~/.zshrc`，`bash` 用户写入 `~/.bashrc`；
- `python_path` 改成你本机 Python 绝对路径。

```bash
my-django-admin() {
  local debug=0

  if [[ "$1" == "--debug" ]]; then
    debug=1
    shift
  fi

  local cmd="$1"
  local project_name="$2"
  local app_name="$3"
  local project_path="$4"

  local python_path="/Users/dengjianlong/miniforge3/envs/work/bin/python"

  log() {
    if [[ "$debug" -eq 1 ]]; then
      echo "$@"
    fi
  }

  info() {
    echo "$@"
  }

  if [[ "$cmd" != "startproject" ]]; then
    info "用法: my-django-admin [--debug] startproject <project_name> <app_name> <project_path>"
    return 1
  fi

  if [[ -z "$project_name" || -z "$app_name" || -z "$project_path" ]]; then
    info "用法: my-django-admin [--debug] startproject <project_name> <app_name> <project_path>"
    return 1
  fi

  if [[ ! -x "$python_path" ]]; then
    info "错误: python_path 不存在或不可执行: $python_path"
    return 1
  fi

  if ! "$python_path" -m django --version >/dev/null 2>&1; then
    info "错误: 该 python 环境未安装 Django: $python_path"
    return 1
  fi

  local repo_url="https://github.com/App1ePine/create-djl-django.git"
  local tag
  tag=$(git ls-remote --tags --sort='v:refname' "$repo_url" \
    | awk -F/ '{print $3}' \
    | grep -E '^v?[0-9]+(\.[0-9]+)*$' \
    | tail -n1)

  if [[ -z "$tag" ]]; then
    info "错误: 无法获取最新 tag"
    return 1
  fi

  local template_url="https://codeload.github.com/App1ePine/create-djl-django/zip/refs/tags/${tag}"

  mkdir -p "$project_path" || return 1

  log "正在创建项目: project_name=$project_name app_name=$app_name path=$project_path tag=$tag"
  "$python_path" -m django startproject "$project_name" "$project_path" \
    --template="$template_url" || return 1

  "$python_path" "$project_path/scripts/update_placeholder_app_name.py" "$app_name" || return 1

  info "创建完成: project_name=$project_name app_name=$app_name project_path=$project_path tag=$tag"
}
```

加载配置后使用：

```bash
source ~/.zshrc   # bash 用户改为 source ~/.bashrc
my-django-admin startproject application demo_app ./test01
my-django-admin --debug startproject application demo_app ./test01
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
- 示例应用占位目录：`app_name/`（创建后通过脚本替换）
- Python 包路径占位变量：`{{ project_name }}`
- 注意：文件内容里要使用 `{{ project_name }}`，不要写裸字符串 `project_name`
- `django-admin startproject` 原生命令只支持 `project_name`，`app_name` 通过 `scripts/update_placeholder_app_name.py` 二次设置

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
