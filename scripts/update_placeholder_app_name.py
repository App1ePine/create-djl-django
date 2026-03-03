#!/usr/bin/env python
"""Configure app_name placeholder in a generated project."""

from __future__ import annotations

import argparse
import keyword
import re
from pathlib import Path

PLACEHOLDER_APP_NAME = "app_name"


def validate_app_name(app_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", app_name):
        raise ValueError("app_name 只能包含字母、数字、下划线，且不能以数字开头。")
    if keyword.iskeyword(app_name):
        raise ValueError("app_name 不能是 Python 关键字。")


def camel_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"{path} 中未找到预期内容: {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def find_project_package(project_root: Path) -> Path:
    candidates = [
        item
        for item in project_root.iterdir()
        if item.is_dir() and (item / "settings.py").exists() and (item / "urls.py").exists()
    ]
    if len(candidates) != 1:
        raise RuntimeError("无法唯一定位项目包目录，请确认项目根目录下只存在一个包含 settings.py 和 urls.py 的包目录。")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="为模板项目设置 app_name。")
    parser.add_argument("app_name", help="目标 Django app 名称，例如 demo 或 user_center")
    args = parser.parse_args()

    app_name = args.app_name.strip()
    validate_app_name(app_name)

    if app_name == PLACEHOLDER_APP_NAME:
        print("app_name 与占位名相同，无需变更。")
        return

    project_root = Path(__file__).resolve().parent.parent
    placeholder_dir = project_root / PLACEHOLDER_APP_NAME
    target_dir = project_root / app_name

    if not placeholder_dir.exists():
        if target_dir.exists():
            print(f"检测到目录 {app_name}/ 已存在，推测你已经设置过 app_name。")
            return
        raise RuntimeError(f"未找到占位目录 {PLACEHOLDER_APP_NAME}/。")
    if target_dir.exists():
        raise RuntimeError(f"目标目录 {target_dir} 已存在，无法覆盖。")

    placeholder_dir.rename(target_dir)

    project_package_dir = find_project_package(project_root)
    replace_once(project_package_dir / "settings.py", '"app_name"', f'"{app_name}"')
    replace_once(
        project_package_dir / "urls.py",
        'include("app_name.urls")',
        f'include("{app_name}.urls")',
    )
    replace_once(
        project_package_dir / "urls.py",
        'path("api/app_name/",',
        f'path("api/{app_name}/",',
    )

    apps_py = target_dir / "apps.py"
    replace_once(apps_py, "class AppNameConfig(AppConfig):", f"class {camel_case(app_name)}Config(AppConfig):")
    replace_once(apps_py, 'name = "app_name"', f'name = "{app_name}"')
    replace_once(target_dir / "urls.py", 'app_name = "app_name"', f'app_name = "{app_name}"')

    print(f"已完成 app_name 设置: {app_name}")


if __name__ == "__main__":
    main()
