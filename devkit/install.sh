#!/usr/bin/env bash
# Cài devkit vào repo hiện tại: chép .githooks và .github, bật core.hooksPath.
# Dùng (trong Git Bash, đứng trong repo đích):  bash /duong/dan/devkit/install.sh [--force]
set -euo pipefail
src="$(cd "$(dirname "$0")/template" && pwd)"
root="$(git rev-parse --show-toplevel)"
force="${1:-}"

copy() {
  local rel="$1" dst="$root/$1"
  if [ -e "$dst" ] && [ "$force" != "--force" ] && ! cmp -s "$src/$rel" "$dst"; then
    echo "  bo qua (da ton tai, khac noi dung): $rel   (dung --force de ghi de)"; return
  fi
  mkdir -p "$(dirname "$dst")"; cp "$src/$rel" "$dst"; echo "  chep: $rel"
}

echo "Cai devkit vao $root"
while read -r rel; do copy "$rel"; done < <(cd "$src" && find . -type f | sed 's|^\./||')
chmod +x "$root"/.githooks/* 2>/dev/null || true
git -C "$root" config core.hooksPath .githooks
echo "Da bat core.hooksPath=.githooks"

# Windows autocrlf co the doi hook sang CRLF -> bash bao loi '\r'. Ep LF cho hook va script.
ga="$root/.gitattributes"
for rule in '.githooks/* text eol=lf' '*.sh text eol=lf'; do
  grep -qxF "$rule" "$ga" 2>/dev/null || { echo "$rule" >> "$ga"; echo "  them vao .gitattributes: $rule"; }
done
echo "Sau khi 'git add .githooks', chay:  git update-index --chmod=+x .githooks/*   (Windows khong luu co thuc thi)"

if command -v gitleaks >/dev/null 2>&1; then
  echo "gitleaks: $(gitleaks version)"
else
  echo "CANH BAO: chua cai gitleaks (https://github.com/gitleaks/gitleaks#installing). Hook chi canh bao, CI se chan."
fi
echo "Moi thanh vien clone repo phai chay lai install.sh (git khong luu core.hooksPath)."
