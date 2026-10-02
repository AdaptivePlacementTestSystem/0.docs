#!/usr/bin/env bash
# Kiểm thử hook devkit trong repo tạm. Chạy: bash devkit/tests/test-hooks.sh
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
pass=0; failn=0

ok()   { pass=$((pass+1)); echo "  PASS  $1"; }
bad()  { failn=$((failn+1)); echo "  FAIL  $1"; }
expect_ok()   { local name="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$name"; else bad "$name (mong doi thanh cong)"; fi; }
expect_fail() { local name="$1"; shift; if "$@" >/dev/null 2>&1; then bad "$name (mong doi bi chan)"; else ok "$name"; fi; }

cd "$tmp" && git init -q -b main && git config user.email t@t && git config user.name t
bash "$here/install.sh" >/dev/null 2>&1
echo a > a.txt && git add .

echo "== commit-msg / pre-commit =="
expect_fail "commit dau tien: message 'update' bi chan"            git commit -q -m "update"
expect_ok   "commit dau tien tren main duoc phep (khoi tao repo)"  git commit -q -m "chore: khoi tao repo docs va devkit"
echo b > b.txt && git add b.txt
expect_fail "commit thang vao main bi chan"                         git commit -q -m "docs: them file b vao thu muc goc"
git branch develop
git switch -q develop
expect_fail "commit thang vao develop bi chan"                      git commit -q -m "docs: them file b vao thu muc goc"
git switch -q -c Feature/Foo
expect_fail "ten nhanh 'Feature/Foo' bi chan"                       git commit -q -m "feat: them module cat engine co ban"
git branch -m feat/cat-engine
expect_fail "message 'fix bug' bi chan"                             git commit -q -m "fix bug"
expect_fail "message khong co loai bi chan"                         git commit -q -m "them module cat engine co ban"
expect_fail "mo ta qua ngan bi chan"                                git commit -q -m "feat: abc"
expect_fail "mo ta chung chung bi chan"                             git commit -q -m "feat: changes"
echo SECRET=1 > .env && git add .env
expect_fail ".env that bi chan"                                     git commit -q -m "feat: them cau hinh moi truong"
git rm -q --cached .env; echo SECRET=changeme > .env.example; git add .env.example
expect_ok   ".env.example duoc phep + message dung"                 git commit -q -m "feat(cat-engine): them chon cau hoi top-5 theo b"
head -c 6000000 /dev/zero > big.bin && git add big.bin
expect_fail "file > 5 MB bi chan"                                   git commit -q -m "chore: them file nhi phan lon"
git rm -q --cached big.bin; rm big.bin

echo "== pre-push =="
sha=$(git rev-parse HEAD); zero=0000000000000000000000000000000000000000
push() { printf '%s\n' "$1" | bash .githooks/pre-push origin url; }
expect_ok   "push feat/cat-engine hop le"                           push "refs/heads/feat/cat-engine $sha refs/heads/feat/cat-engine $zero"
expect_fail "push thang vao main bi chan"                           push "refs/heads/feat/cat-engine $sha refs/heads/main $zero"
expect_fail "push thang vao develop bi chan"                        push "refs/heads/feat/cat-engine $sha refs/heads/develop $zero"
expect_fail "xoa develop bi chan"                                   push "(delete) $zero refs/heads/develop $sha"
expect_ok   "xoa nhanh feat duoc phep"                              push "(delete) $zero refs/heads/feat/cat-engine $sha"
expect_fail "push len ten nhanh sai (wip)"                          push "refs/heads/feat/cat-engine $sha refs/heads/wip $zero"
expect_fail "push len ten nhanh sai (feat/Foo_Bar)"                 push "refs/heads/feat/cat-engine $sha refs/heads/feat/Foo_Bar $zero"
expect_ok   "hotfix/sua-loi-eap hop le"                             push "refs/heads/feat/cat-engine $sha refs/heads/hotfix/sua-loi-eap $zero"
expect_ok   "bootstrap push main (DEVKIT_BOOTSTRAP=1)"              env DEVKIT_BOOTSTRAP=1 bash -c "printf '%s\n' 'refs/heads/main $sha refs/heads/main $zero' | bash .githooks/pre-push origin url"
# commit message sai da lot vao lich su (bo qua hook) -> pre-push phai bat
git -c core.hooksPath=/dev/null commit -q --allow-empty -m "update stuff"
bad_sha=$(git rev-parse HEAD)
expect_fail "pre-push bat commit message sai trong lich su"         push "refs/heads/feat/cat-engine $bad_sha refs/heads/feat/cat-engine $sha"

echo
echo "Ket qua: $pass dat, $failn that bai"
[ "$failn" -eq 0 ]
