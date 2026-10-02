#!/usr/bin/env bash
# Áp ruleset vào 1 repo GitHub. Cần: gh đã đăng nhập (gh auth login), quyền Admin repo.
# Dùng:  ./apply-rulesets.sh <owner>/<repo>
# CHẠY SAU khi: (1) đã push main + develop lần đầu, (2) workflow devkit-checks đã chạy ít nhất 1 lần
# (status check chưa từng chạy thì ruleset sẽ chặn mọi PR vì chờ check không tồn tại).
set -euo pipefail
repo="${1:?Dung: $0 <owner>/<repo>}"
here="$(cd "$(dirname "$0")" && pwd)"
for f in "$here"/rulesets/protect-*.json; do
  echo "Ap $(basename "$f") vao $repo"
  gh api -X POST "repos/$repo/rulesets" --input "$f" >/dev/null
done
echo "Xong. Kiem tra: Settings > Rules > Rulesets. Them lint/test/build/codeql vao required checks khi pipeline co."
