#!/usr/bin/env bash
set -euo pipefail

TAG="${1:?用法: ./scripts/update-readme-tag.sh v1.0.2}"
README="README.md"

# macOS sed 需要 -i ''
sed -E -i '' "s#(refs/tags/)v[0-9]+(\.[0-9]+)*#\1${TAG}#g" "$README"

echo "README tag 已更新为: $TAG"
