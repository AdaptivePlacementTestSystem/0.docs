#!/usr/bin/env bash
# Chạy lại TOÀN BỘ kiểm tra CI/CD ở máy (không cần GitHub, không đụng server).
# Dùng (Git Bash):  bash /d/TLCN/CI-CD/verify-local.sh
# Có thể đổi đường dẫn:  BE_DIR=... FE_DIR=... bash verify-local.sh
# Công cụ tùy chọn: actionlint, gitleaks (không có thì bước đó được ghi "BỎ QUA", không tính là đạt).
# Script này CHỈ ĐỌC/chạy kiểm tra; chỉ ghi vào thư mục coverage/, reports/, dist/, .next/ của repo.
set -u

BE_DIR="${BE_DIR:-/d/TLCN/backend/backend}"
FE_DIR="${FE_DIR:-/d/TLCN/frontend}"
API_BASE_URL="${API_BASE_URL:-http://localhost:3001/api/v1}"

PASS=0; FAIL=0; SKIP=0
declare -a RESULTS

run() { # run "<tên>" "<thư mục>" <lệnh...>
  local name="$1" dir="$2"; shift 2
  local out
  if out=$(cd "$dir" && "$@" 2>&1); then
    RESULTS+=("ĐẠT     | $name"); PASS=$((PASS+1))
  else
    RESULTS+=("KHÔNG ĐẠT | $name"); FAIL=$((FAIL+1))
    echo "----- $name (cuối log) -----"; echo "$out" | tail -15
  fi
}
skip() { RESULTS+=("BỎ QUA  | $1 ($2)"); SKIP=$((SKIP+1)); }

echo "== Backend: $BE_DIR"
run "BE lint (oxlint)"                 "$BE_DIR" npm run lint
run "BE trùng lặp mã (jscpd ≤ 3%)"     "$BE_DIR" npm run dup
run "BE build"                         "$BE_DIR" npm run build
run "BE test + coverage"               "$BE_DIR" npm run test:cov
run "BE lỗ hổng thư viện (prod, high)" "$BE_DIR" npm audit --omit=dev --audit-level=high
run "BE prisma validate"               "$BE_DIR" env DATABASE_URL=postgresql://u:p@localhost:5432/db npx prisma validate
# compose cần file .env (env_file) — kiểm trong thư mục tạm, dùng file mẫu làm .env, không đụng thư mục deploy thật
if command -v docker >/dev/null 2>&1; then
  TMP_DEPLOY="$(mktemp -d)"; cp -r "$BE_DIR/deploy/." "$TMP_DEPLOY/"; cp "$BE_DIR/deploy/.env.staging.example" "$TMP_DEPLOY/.env"
  run "BE docker compose config"         "$TMP_DEPLOY" docker compose config -q
  rm -rf "$TMP_DEPLOY"
else
  skip "BE docker compose config" "chưa cài Docker"
fi

echo "== Frontend: $FE_DIR"
run "FE lint (ESLint)"                 "$FE_DIR" npm run lint
run "FE typecheck"                     "$FE_DIR" npm run typecheck
run "FE định dạng (Prettier)"          "$FE_DIR" npm run format:check
run "FE trùng lặp mã (jscpd ≤ 3%)"     "$FE_DIR" npm run dup
run "FE test + coverage"               "$FE_DIR" npm run test:cov
run "FE build"                         "$FE_DIR" env API_BASE_URL="$API_BASE_URL" npm run build
run "FE lỗ hổng thư viện (prod, high)" "$FE_DIR" npm audit --omit=dev --audit-level=high

echo "== Workflow GitHub Actions"
if command -v actionlint >/dev/null 2>&1; then
  run "actionlint BE" "$BE_DIR" sh -c 'actionlint .github/workflows/*.yml'
  run "actionlint FE" "$FE_DIR" sh -c 'actionlint .github/workflows/*.yml'
else
  skip "actionlint" "chưa cài; tải từ github.com/rhysd/actionlint/releases"
fi

echo "== Secret (gitleaks, quét thư mục hiện tại — LƯU Ý: sẽ báo cả .env thật nếu có)"
if command -v gitleaks >/dev/null 2>&1; then
  echo "   (Nên quét sau khi git add: gitleaks detect --source . ; hoặc quét bản sao đã loại .env)"
  skip "gitleaks" "đã cài nhưng cần quét đúng phần SẼ commit; xem hướng dẫn trong README.md của thư mục CI-CD"
else
  skip "gitleaks" "chưa cài; winget install gitleaks.gitleaks"
fi

echo; echo "================ TỔNG KẾT ================"
for r in "${RESULTS[@]}"; do echo "$r"; done
echo "------------------------------------------"
echo "Đạt: $PASS   Không đạt: $FAIL   Bỏ qua: $SKIP"
[ "$FAIL" -eq 0 ]
