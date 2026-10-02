# devkit — chặn push sai chuẩn rubric

Bộ file dùng chung cho cả 3 repo (`backend`, `frontend`, `docs`). Nguồn quyết định: Quyết định #36 (log thật lưu máy của nhóm). Chuẩn đối chiếu: rubric TC2.4 (Git, secret, chất lượng) và TC2.6 (CI), `tracking/GIT_CONVENTIONS.md`.

## Mô hình nhánh

```
feat|fix|docs|chore|test|refactor/<ten-chuc-nang>  ──PR (squash)──▶  develop  ──PR (merge commit)──▶  main
hotfix/<ten>  ──PR (merge commit)──▶  main   (sau đó merge ngược main vào develop)
```

`<ten-chuc-nang>`: chữ thường, số, gạch ngang. Ví dụ `feat/cat-engine-eap`, `docs/cap-nhat-srs`.
Squash vào `develop` để mỗi tính năng là 1 commit sạch. Merge commit vào `main` để `develop` không bị lệch lịch sử.

## Hai lớp bảo vệ

| Lớp | Chạy ở | Chặn | Bỏ qua được không |
|---|---|---|---|
| **Git hook** (`template/.githooks`) | Máy thành viên | commit/push thẳng vào `main`/`develop`; tên nhánh sai; commit message sai hoặc chung chung (`update`, `fix bug`); `.env` thật; file > 5 MB; secret (nếu cài gitleaks); lint/test cục bộ khi push | **Được** (`--no-verify`). Hook chỉ giúp phát hiện sớm |
| **CI + ruleset** (`template/.github`, `rulesets/`) | GitHub | Merge khi: sai tên nhánh/hướng merge, sai commit/tiêu đề PR, checklist PR chưa tick hết, có secret, chưa đủ 1 approval | **Không** (admin cũng không bypass). Đây là lớp tạo bằng chứng cho rubric |

Chỉ lớp CI + ruleset mới đảm bảo "≥90% thay đổi qua PR có review". Hook không thay được.

## Cài đặt (mỗi repo, mỗi máy)

```bash
# Trong Git Bash, đứng trong repo đích
bash /duong/dan/docs/devkit/install.sh
git add .githooks .github .gitattributes
git update-index --chmod=+x .githooks/*
```

- Chép `.githooks/` và `.github/` vào repo, bật `core.hooksPath`, ép `eol=lf` cho hook.
- **Mỗi thành viên sau khi clone phải chạy lại `install.sh`** (git không lưu `core.hooksPath` trong repo).
- Cài [gitleaks](https://github.com/gitleaks/gitleaks#installing) để quét secret ở máy. Chưa cài thì hook chỉ cảnh báo.
- Repo backend/frontend: sửa `.githooks/local-checks.sh` cho đúng lệnh lint/test. Mặc định chạy `npm run lint` và `npm test` nếu có `package.json`.

## Khởi tạo repo mới (thứ tự quan trọng)

1. `git init -b main`, chạy `install.sh`, commit đầu tiên (hook cho phép commit đầu tiên trên `main`).
2. `git branch develop`, rồi push cả hai: `DEVKIT_BOOTSTRAP=1 git push -u origin main develop`. Đây là ngoại lệ duy nhất cho push thẳng.
3. Tạo 1 PR thử để workflow `devkit-checks` chạy ít nhất một lần. Nếu không, ruleset sẽ chờ check chưa từng tồn tại và chặn mọi PR.
4. `devkit/apply-rulesets.sh <owner>/<repo>` (cần `gh auth login`, quyền Admin).
5. Sau khi có pipeline thật, thêm `lint`, `test`, `build`, `codeql` vào required checks của ruleset.

## Kiểm thử hook

```bash
bash devkit/tests/test-hooks.sh     # 22 ca: chặn và cho phép, trên repo tạm
```

## Chưa kiểm chứng (cần thử trên GitHub thật)

- Workflow `devkit-checks.yml` mới chỉ kiểm cú pháp YAML, chưa chạy trên GitHub Actions.
- Ruleset JSON chưa import thật. Tham số `allowed_merge_methods` và việc gói Free áp ruleset cho repo public cần xác nhận khi chạy `apply-rulesets.sh`.
- `GITLEAKS_VERSION` 8.18.4 và tên file tải về chưa kiểm tra lại với trang release.
- Chưa có gitleaks trên máy phát triển nên nhánh quét secret của hook chưa được chạy.
