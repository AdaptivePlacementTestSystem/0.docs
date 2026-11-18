# Hướng dẫn setup CI/CD cho repo Backend (đối chiếu rubric)

> **Ngày lập:** 2026-10-29 (Tuần 7/12). **Trạng thái:** BẢN NHÁP, chờ nhóm xác nhận (xem Mục 10).
> **Người đọc:** thành viên phụ trách Backend. **Mục tiêu:** làm theo từng bước để repo `backend` có CI/CD xanh giống `frontend`, đạt các tiêu chí rubric TC2.4, TC2.5, TC2.6 và tránh bẫy G6, G8.
> **Cách đọc nhãn:** ✅ đã chạy thật trên repo `frontend` (organization `AdaptivePlacementTestSystem`) · 🟡 mẫu dựa trên `frontend`, **chưa chạy thử trên backend** · ⛔ backend chưa có.
> File này không chứa mật khẩu, khoá hay IP server. Số liệu rubric lấy từ `0.docs/tracking/GIT_CONVENTIONS.md` và `docs-repo/plans/cicd/*`; **chưa đối chiếu lại với file `.docx` gốc của Khoa**.

---

## 1. Tóm tắt 1 phút

1. Repo `frontend` đã có CI/CD chạy xanh: `build-test`, `security`, `package` (đẩy ảnh Docker lên GHCR), `codeql` đều đạt; `deploy-staging` được bỏ qua có cảnh báo vì chưa có secret server.
2. Repo `backend` hiện **chưa có git, chưa có workflow, chưa có Dockerfile, chưa có migration, chưa có health endpoint**. Mục 5 liệt kê đủ việc cần làm theo thứ tự.
3. Backend có thể **sao chép gần như nguyên** bộ cấu hình của frontend (hook git, workflow `devkit-checks`, ruleset, template PR), chỉ khác phần lint, test cần Postgres/Redis, Prisma, Dockerfile.
4. Bẫy lớn nhất đã gặp ở frontend và sẽ lặp lại ở backend: **`@apt/shared-types` nằm ngoài repo**, **`.gitignore` chặn nhầm thư mục `reports`**, **tên image Docker phải viết thường**. Xem Mục 8.

---

## 2. Bản đồ repo và organization

| Thành phần | Địa chỉ | Trạng thái |
|---|---|---|
| Organization | `https://github.com/AdaptivePlacementTestSystem` | ✅ |
| Tài liệu | `AdaptivePlacementTestSystem/0.docs` (từ thư mục `docs-repo`) | ✅ đã push |
| Gói dùng chung | `AdaptivePlacementTestSystem/shared-types`, tag `v3.0.0` | ✅ đã push |
| Frontend | `AdaptivePlacementTestSystem/frontend` | ✅ CI xanh |
| **Backend** | `AdaptivePlacementTestSystem/backend` | ⛔ **chưa tạo** |

Mẫu tham chiếu để sao chép: thư mục local `D:\TLCN\frontend\frontend` (các file `.githooks/`, `.github/`, `.jscpd.json`, `Dockerfile`, `sonar-project.properties`).

---

## 3. Đối chiếu rubric: yêu cầu và cách đáp ứng

| Tiêu chí | Yêu cầu (mức cao nhất) | Cách đáp ứng ở backend | Công cụ / file |
|---|---|---|---|
| **TC2.4** Lỗi lint | 0 lỗi lint / 1000 dòng | Chạy `npm run lint` trong CI, fail nếu có lỗi | `oxlint --type-aware` (đã có sẵn) |
| TC2.4 Trùng lặp mã | ≤ 3% | Thêm `jscpd`, ngưỡng 3% | `.jscpd.json`, `npm run dup` |
| TC2.4 Issue Blocker/Critical | 0 | CodeQL (bắt buộc), SonarCloud (tuỳ chọn) | `codeql.yml` |
| TC2.4 Tuần có commit | ≥ 90% | Mỗi người commit thực chất mỗi tuần | `GIT_CONVENTIONS.md` |
| TC2.4 Thay đổi qua PR có review | ≥ 90% | Ruleset bắt buộc PR và 1 approval, **không ai bypass** | `rulesets/protect-main.json` |
| TC2.4 Secret lộ trong repo | 0 | gitleaks ở hook cục bộ và CI; không commit `.env` | `devkit-checks.yml`, `pipeline.yml` |
| TC2.4 Tài liệu | README, sơ đồ triển khai, nợ kỹ thuật, quy ước mã | `README.md`, `TECH_DEBT.md`, `CODING_CONVENTION.md` | có ở frontend, sao chép sang |
| **TC2.5** Kiểm thử | ≥ 4 tầng test; coverage ≥ 70%; 100% test qua | `npm run test:cov` trong CI; thêm test tích hợp và e2e | `vitest` |
| **TC2.6** Pipeline | ≥ 6 chặng | build · lint/dup · test · bảo mật · đóng gói · deploy + smoke test | `pipeline.yml` |
| TC2.6 Ổn định | Build xanh ≥ 90%; ≥ 10 deploy tự động trải đều; commit → staging ≤ 15 phút | Cần **đo thật** sau khi chạy | tab Actions, Deployments |
| TC2.6 Bí mật & phiên bản | Secret qua nền tảng; tag theo commit; rollback | GitHub Secrets/Environment `staging`; tag `sha-xxxxxxx`; `rollback.yml` | |
| TC2.6 Giám sát | Health check + log tập trung + cảnh báo | `/health`, `/ready` (⛔ chưa có ở backend) | Better Stack |
| **G6** | Không có pipeline chạy được lúc bảo vệ ⇒ TC2.6 tối đa Mức 2 | Phải có pipeline chạy thật và staging chạy lúc bảo vệ | |
| **G8** | Repo không cấp quyền / không build được từ bản sạch ⇒ bị phạt | CI build từ bản clone sạch; README đầy đủ; **gói `shared-types` phải lấy được từ GitHub** | |

**Hiện trạng số đo (từ tài liệu và lần kiểm gần nhất):** backend trùng lặp 0,55%, coverage khoảng 2,8% (còn rất thấp so với mức 70%), chỉ có 2 file test; thư mục `test/e2e` và `test/integration` rỗng.

---

## 4. Quy tắc bắt buộc (vi phạm là CI hoặc hook chặn)

### 4.1. Nhánh và PR

| Quy tắc | Chi tiết |
|---|---|
| **Không commit/push thẳng vào `main` và `develop`** | Hook `pre-commit` và `pre-push` chặn; ruleset chặn phía GitHub |
| Tên nhánh | `feat\|fix\|docs\|test\|chore\|refactor/<ten-viet-thuong-gach-ngang>`, ví dụ `feat/health-endpoint`; `hotfix/<ten>` chỉ vào `main` |
| Luồng | nhánh con → PR (**squash**) → `develop` → PR (**merge commit**) → `main` |
| Vào `main` chỉ nhận | `develop` hoặc `hotfix/*` |
| Review | **1 approval**, người còn lại duyệt (nhóm 2 người: review chéo 100%); dismiss review khi có commit mới |
| Mọi cuộc thảo luận trong PR phải được resolve | ruleset `required_review_thread_resolution` |
| Merge phải cập nhật với nhánh đích | `strict_required_status_checks_policy` |

### 4.2. Commit và tiêu đề PR

- Định dạng: `<loại>(<phạm-vi>): <mô tả>`; loại ∈ `feat, fix, docs, test, chore, refactor`; phạm vi tuỳ chọn, chữ thường, không dấu cách.
- **Tiêu đề ≤ 72 ký tự**, mô tả **≥ 10 ký tự**, **không** dùng từ chung chung (`update`, `fix bug`, `wip`, `misc`, `minor`…).
- PR vào `develop` được squash nên **tiêu đề PR cũng phải theo định dạng trên** và bị kiểm.
- Không thêm dòng `Co-Authored-By` nếu không được yêu cầu.

### 4.3. Checklist PR (`pr-checklist` bắt buộc)

- Dùng `.github/pull_request_template.md`. **Phải có ít nhất một ô `- [x]` và không còn ô `- [ ]` nào.** Mục không áp dụng thì tick và ghi `N/A: lý do`.
- Mục thường gặp: đã đối chiếu công thức CAT/EAP/Rasch với SRS; có unit test đi kèm; không có secret; đã ghi `AI_USAGE_LOG.md` nếu có phần AI sinh; lint pass.

### 4.4. Bí mật

- **Không bao giờ commit `.env`**; chỉ commit `.env.example` (đã có trong `.gitignore`: `.env`, `.env.*`, `!.env.example`).
- Khoá, mật khẩu, token chỉ nằm trong **GitHub Secrets** (Environment `staging`) hoặc file `.env` quyền 600 trên server.
- Trong workflow, secret đọc qua `env:`, **không nội suy thẳng vào dòng lệnh**.
- Repo công khai: dùng `pull_request`, **không** dùng `pull_request_target`, không dùng self-hosted runner, quyền token tối thiểu cho từng job.

### 4.5. Chất lượng mã

- Lint 0 lỗi; trùng lặp ≤ 3%; Prettier sạch (`format:check`); typecheck sạch; `npm audit --omit=dev --audit-level=high` = 0.
- Các tham số thuật toán CAT (`CAT_*`) **không hardcode**, lấy từ `ConfigService`/env (xem `CLAUDE.md`).

---

## 5. Các bước setup theo thứ tự

> Làm tuần tự. Mỗi bước có cách kiểm. Với backend chưa có git, bắt đầu từ bước 0.

### Bước 0. Chuẩn bị trên GitHub

1. Tạo repo **trống** `AdaptivePlacementTestSystem/backend`, **không tích** README, LICENSE hay `.gitignore`.
2. Đặt **Public**. Repo private cần GitHub Advanced Security mới chạy được CodeQL (lỗi "Advanced Security must be enabled").
3. Settings → General → Pull Requests: bật **Automatically delete head branches**; chỉ cho squash và merge commit (tắt rebase).
4. **Chưa import ruleset** (xem Bước 8, nếu import sớm sẽ chặn cả lần push đầu).

### Bước 1. Khởi tạo git và hook

```
cd D:\TLCN\backend\backend
git init -b main
git config core.hooksPath .githooks
```

Sao chép từ `D:\TLCN\frontend\frontend` sang backend:

| Từ frontend | Sao chép? | Ghi chú |
|---|---|---|
| `.githooks/` (`_lib.sh`, `commit-msg`, `pre-commit`, `pre-push`, `local-checks.sh`) | ✅ nguyên bản | `local-checks.sh` chạy `npm run lint` và `npm test` trước khi push |
| `.gitattributes` | ✅ | ép `.githooks/*` và `*.sh` dùng LF |
| `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/` | ✅ | |
| `.github/workflows/devkit-checks.yml` | ✅ nguyên bản | kiểm nhánh, commit, checklist, secret |
| `.github/workflows/codeql.yml` | ✅ nguyên bản | |
| `.github/workflows/rollback.yml` | ✅ | đổi ví dụ tên image |
| `.github/workflows/pipeline.yml` | ⚠️ sao chép **rồi sửa** (Mục 6) | khác ở test, Prisma, Docker |
| `.jscpd.json` | ✅ | |
| `TECH_DEBT.md`, `CODING_CONVENTION.md`, `README.md` | ✅ sao chép rồi sửa nội dung | bắt buộc cho TC2.4 |

`.gitignore` của backend: **không dùng dòng `reports/`** mà dùng `/reports/` (xem Mục 8, lỗi số 2).

### Bước 2. Nối `@apt/shared-types`

`package.json` của backend đang là `"file:../../packages/shared-types"` ⇒ CI **chắc chắn lỗi** vì runner chỉ checkout repo backend. Đổi thành:

```json
"@apt/shared-types": "git+https://github.com/AdaptivePlacementTestSystem/shared-types.git#v3.0.0"
```

Sau đó: xoá `package-lock.json` và `node_modules`, chạy `npm install`, rồi **đổi mọi `git+ssh://git@github.com/` trong `package-lock.json` thành `git+https://github.com/`** (CI không có khoá SSH). Kiểm: `npm ci` trên clone sạch phải cài được gói và có thư mục `node_modules/@apt/shared-types/dist`.

### Bước 3. Bổ sung script và cấu hình còn thiếu cho backend

Backend hiện **thiếu** các script mà pipeline cần (frontend có sẵn):

| Cần thêm vào `package.json` | Giá trị gợi ý |
|---|---|
| `"typecheck"` | `tsc --noEmit -p tsconfig.json` |
| `"format:check"` | `prettier --check "src/**/*.ts" "test/**/*.ts"` |
| `"dup"` | `jscpd` (thêm `jscpd` vào devDependencies; dùng `.jscpd.json`) |
| `"test:cov"` | đã có; **cần cấu hình coverage** trong `vitest.config.ts` |

Thêm vào `vitest.config.ts` (mẫu):

```ts
test: {
  // ...giữ cấu hình hiện có
  coverage: {
    provider: 'v8',
    reporter: ['text-summary', 'html', 'lcov'],
    include: ['src/**/*.ts'],
    exclude: ['src/**/*.spec.ts', 'src/main.ts'],
  },
},
```

Với `.jscpd.json` đổi `"path": ["src"]` giữ nguyên, `"format": ["typescript"]`.

### Bước 4. Việc code bắt buộc để deploy và smoke test có ý nghĩa

| Việc | Vì sao | Trạng thái |
|---|---|---|
| Module health: `GET /api/v1/health` (còn sống) và `/ready` (kiểm Postgres + Redis, 503 nếu hỏng) | smoke test sau deploy, Better Stack, `HEALTHCHECK` Docker | ⛔ chưa có trong 13 module |
| **Migration khởi tạo Prisma** (`prisma/migrations` đang rỗng) | `prisma migrate deploy` không tạo bảng nào ⇒ staging chạy nhưng vô dụng | ⛔ cần nhóm chốt (mục Q1 trong `MO_TA_CI_CD_VA_DIEM_CHAN.md`, phương án A khuyến nghị: sinh baseline từ `schema.prisma`, nối `custom_migrations.sql`) |
| `Dockerfile` backend (xem Mục 7) | bước `package` | ⛔ chưa có |
| Test tích hợp và e2e | TC2.5 cần ≥ 4 tầng và coverage ≥ 70% | ⛔ hiện 2 file spec |

### Bước 5. Sửa `pipeline.yml` cho backend (xem Mục 6)

### Bước 6. Kiểm chứng cục bộ trước khi push (bắt buộc)

Mô phỏng CI trên **bản clone sạch** (xuống dòng LF như CI). Chạy lần lượt, mọi bước phải qua:

```
git clone <đường-dẫn-repo-local> ..\backend-ci-check    # bản sạch, không có node_modules
cd ..\backend-ci-check
npm ci
npx prisma generate
npm run lint; npm run dup; npm run typecheck; npm run format:check
npm run test:cov
npm run build
npm audit --omit=dev --audit-level=high
gitleaks detect --source . --redact        # gitleaks 8.18.4
```

Mẹo trên Windows: cây làm việc có thể bị đổi sang CRLF nên `format:check` báo sai; nội dung đã commit mới là LF (CI Linux sẽ thấy LF). Kiểm tương đương bằng `npx prettier --check --end-of-line auto .`.

### Bước 7. Push lần đầu (đúng thứ tự)

```
$env:DEVKIT_BOOTSTRAP=1
git push -u origin main          # commit khởi tạo duy nhất
git push -u origin develop       # develop tách từ main
Remove-Item Env:DEVKIT_BOOTSTRAP
git push -u origin feat/<ten-chuc-nang>
```

`DEVKIT_BOOTSTRAP=1` là **ngoại lệ duy nhất** của hook `pre-push`, chỉ dùng cho lần khởi tạo `main`/`develop`. Sau đó mở PR vào `develop`.

### Bước 8. Import ruleset (SAU khi pipeline đã chạy ít nhất một lần)

1. Mở một PR thử để `devkit-checks` và `pipeline` chạy; xem tên các check hiện ra.
2. Settings → Rules → Rulesets → New → **Import a ruleset** → chọn `protect-main.json` (đặt ở `.github/rulesets/` hoặc `docs-repo/devkit/rulesets/`).
3. Đối chiếu tên 7 check bắt buộc với tên thực tế: `branch-policy`, `commit-lint`, `pr-checklist`, `secret-scan`, `build-test`, `security`, `analyze`. Sai tên ⇒ PR bị treo mãi ở trạng thái "Expected".
4. Tuỳ chọn: import `protect-develop.json` (4 check, chỉ squash).
5. Nếu cần push lại lịch sử khởi tạo: đặt ruleset về **Disabled**, push, rồi bật lại **Active**. Ruleset để `bypass_actors: []` nên ngay cả admin cũng bị chặn.

### Bước 9. Secret và deploy staging

| Secret (Environment `staging`) | Ý nghĩa |
|---|---|
| `STAGING_SSH_KEY` | khoá SSH riêng của user deploy |
| `STAGING_KNOWN_HOSTS` | dòng `known_hosts` của server |
| `STAGING_HOST` | địa chỉ server |
| `STAGING_USER` | user SSH |

- Pipeline có **bước kiểm tra secret**: thiếu secret thì 4 bước deploy bị bỏ qua kèm cảnh báo, job vẫn xanh. **Cẩn thận:** job xanh nhưng **chưa deploy thật**, nên không tính là bằng chứng deploy cho rubric TC2.6.
- Server staging dùng chung với một dự án khác (`farmnongviet`): **không sửa Nginx/UFW/certbot của dự án kia**, chỉ ghi trong thư mục của user `deploy`. Chi tiết trong `MO_TA_CI_CD_VA_DIEM_CHAN.md`.
- Không dùng dữ liệu thật trên staging cho đến khi sửa các lỗi nghiêm trọng của backend (mục T6 trong tài liệu đó).

---

## 6. Mẫu `pipeline.yml` cho backend 🟡

Dựa trên bản **đã chạy xanh** của frontend; phần in đậm trong chú thích là chỗ khác. **Chưa chạy thử trên backend**: kiểm bằng `actionlint` và thử trên nhánh `chore/ci-*` trước khi bật bắt buộc.

```yaml
name: pipeline
on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop]
  workflow_dispatch:
concurrency:
  group: pipeline-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
permissions:
  contents: read
jobs:
  build-test:
    name: build-test
    runs-on: ubuntu-latest
    timeout-minutes: 20
    env:
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      # Biến tối thiểu để test/e2e chạy; giá trị giả, không phải secret thật
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/apt_test
      REDIS_HOST: localhost
      REDIS_PORT: "6379"
      JWT_SECRET: ci-only-secret-khong-dung-that
      NODE_ENV: test
    services:               # KHÁC FRONTEND: test tích hợp cần Postgres và Redis
      postgres:
        image: postgres:16-alpine
        env: { POSTGRES_PASSWORD: postgres, POSTGRES_DB: apt_test }
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U postgres" --health-interval 5s
          --health-timeout 5s --health-retries 10
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
        options: >-
          --health-cmd "redis-cli ping" --health-interval 5s
          --health-timeout 5s --health-retries 10
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: 24, cache: npm }
      - run: npm ci
      - run: npx prisma generate            # KHÁC FRONTEND
      # - run: npx prisma migrate deploy    # BẬT sau khi có migration (Q1)
      - run: npm run lint
      - run: npm run dup
      - run: npm run typecheck
      - run: npm run format:check
      - run: npm run test:cov
      - run: npm run build
      - name: Báo cáo coverage
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: coverage-backend, path: coverage, if-no-files-found: ignore }
      - name: SonarCloud
        if: env.SONAR_TOKEN != ''
        uses: SonarSource/sonarqube-scan-action@v7

  security:
    name: security
    runs-on: ubuntu-latest
    timeout-minutes: 10
    env:
      GITLEAKS_VERSION: "8.18.4"
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: 24, cache: npm }
      - name: Quét secret toàn lịch sử (gitleaks)
        run: |
          curl -sSfL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" | tar -xz gitleaks
          ./gitleaks detect --source . --redact --verbose
      - run: npm audit --omit=dev --audit-level=high
      - name: Review phụ thuộc trên PR
        if: github.event_name == 'pull_request'
        uses: actions/dependency-review-action@v4

  package:
    name: package
    needs: [build-test, security]
    if: github.event_name == 'push' && github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions: { contents: read, packages: write }
    outputs:
      image: ${{ steps.meta.outputs.image }}
    steps:
      - uses: actions/checkout@v4
      - name: Tên image (chữ thường)
        id: meta
        run: |
          IMAGE="ghcr.io/${GITHUB_REPOSITORY,,}"
          echo "image=${IMAGE}:sha-${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"
          echo "repo=${IMAGE}" >> "$GITHUB_OUTPUT"
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ${{ steps.meta.outputs.image }}
            ${{ steps.meta.outputs.repo }}:develop      # PHẢI dùng biến chữ thường, không dùng github.repository
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: deploy-staging
    needs: package
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: staging
    permissions: { contents: read, packages: read }
    steps:
      - name: Kiểm tra secret staging
        id: guard
        env:
          READY: ${{ secrets.STAGING_SSH_KEY != '' && secrets.STAGING_KNOWN_HOSTS != '' && secrets.STAGING_HOST != '' && secrets.STAGING_USER != '' }}
        run: |
          echo "ready=${READY}" >> "$GITHUB_OUTPUT"
          [ "$READY" = "true" ] || echo "::warning::Thiếu secret staging nên bỏ qua deploy."
      # Các bước dưới đều cần: if: steps.guard.outputs.ready == 'true'
      #   Cấu hình SSH · Đăng nhập GHCR trên server · Deploy (deploy.sh backend IMAGE) · Đăng xuất GHCR (if: always() && ...)
      # Backend: deploy.sh chạy migrate trước khi khởi động lại dịch vụ rồi smoke test /ready.
```

Giữ nguyên đúng 4 tên job `build-test`, `security`, `package`, `deploy-staging` và job CodeQL tên `analyze`: ruleset bắt buộc đúng các tên này.

---

## 7. Dockerfile backend: các điểm bắt buộc 🟡

| Điểm | Lý do |
|---|---|
| Ảnh nền `node:24-alpine` **phải `apk add --no-cache git`** trước `npm ci` | `@apt/shared-types` cài từ GitHub; ảnh alpine không có git (đã xử lý ở Dockerfile frontend) |
| `npx prisma generate` trong giai đoạn build; ảnh chạy cần Prisma Client và (nếu `migrate deploy` chạy trong ảnh) Prisma CLI | tránh lỗi thiếu client lúc chạy |
| Chạy bằng user `node`, không root | bảo mật |
| `HEALTHCHECK` gọi `/api/v1/health` (liveness, không phụ thuộc DB) | Docker biết container sống |
| Ghi nhớ kích thước | bản cũ đo 847 MB; mục tiêu commit → staging ≤ 15 phút |
| Có thể kiểm bằng Docker Desktop trước khi push | đã làm ở frontend: build, chạy, `/api/health/live` trả 200 |

Tên image lên GHCR luôn **chữ thường**: `ghcr.io/adaptiveplacementtestsystem/backend:sha-xxxxxxx`.

---

## 8. Lỗi thường gặp (đã gặp thật ở frontend)

| # | Triệu chứng trong CI/Git | Nguyên nhân | Cách sửa |
|---|---|---|---|
| 1 | `Cannot find module '@apt/shared-types'` ở typecheck; kéo theo hàng chục lỗi `TS7053` | Dependency `file:../../packages/shared-types` nằm ngoài repo | Mục Bước 2: dùng git URL kèm tag `v3.0.0`, lockfile dùng `git+https` |
| 2 | `Cannot find module '@/features/reports/...'` dù chạy local được | `.gitignore` có dòng `reports/` (để chặn báo cáo jscpd) nên chặn luôn mọi thư mục tên `reports` trong `src/`; file **chưa từng lên git** | Đổi thành `/reports/` (chỉ thư mục gốc). Kiểm: `git status --ignored` xem file nguồn nào bị ignore |
| 3 | `invalid tag "ghcr.io/AdaptivePlacementTest/...": repository name must be lowercase` | Dùng thẳng `github.repository` (có chữ hoa) làm tag | Dùng `steps.meta.outputs.repo` đã hạ chữ thường |
| 4 | `denied: permission_denied: read_package` khi đẩy ảnh | Package GHCR cùng tên đã tồn tại, gắn với repo cũ (đã xoá repo nhưng package vẫn còn) | Xoá package cũ hoặc cấp quyền Write cho repo mới ở Package settings → Manage Actions access |
| 5 | CodeQL: `Advanced Security must be enabled for this repository` | Repo private, chưa bật Advanced Security | Chuyển repo sang Public (hoặc bật GHAS); chạy lại job |
| 6 | `npm audit` đỏ: `next`, `zod`, `fast-uri` | Phụ thuộc có lỗ hổng mức high/critical | Nâng phiên bản (`npm audit fix`); kiểm `npm audit --omit=dev --audit-level=high` = 0 |
| 7 | `format:check` đỏ ở vài file | Chưa chạy Prettier; hoặc cây Windows bị CRLF | `npx prettier --write --end-of-line lf .`; trên máy Windows kiểm bằng `--end-of-line auto` |
| 8 | `build` lỗi: `two parallel pages that resolve to the same path` | Hai route cùng đường dẫn (file cũ chưa xoá khi chuyển nhóm route) | Xoá file thừa, kiểm bằng `next build` |
| 9 | `ssh: usage ...` ở bước deploy; log ghi `TARGET: @` | Secret `STAGING_USER`/`STAGING_HOST` trống | Thêm secret hoặc dùng bước guard để bỏ qua |
| 10 | `GH013 ... 7 of 7 required status checks are expected` khi push `main` | Ruleset đang Active chặn cả lần push khởi tạo | Đặt ruleset Disabled, push, bật lại Active |
| 11 | `[rejected] main -> main (non-fast-forward)` | Lịch sử local khác remote (ví dụ viết lại commit) | **Không force-push**; tạo lại repo trống và push lại, hoặc xin phép rõ ràng |
| 12 | `commit-lint` đỏ | Tiêu đề > 72 ký tự, sai định dạng, hoặc mô tả quá chung chung | Sửa theo Mục 4.2; tiêu đề PR cũng kiểm |
| 13 | `pr-checklist` đỏ | Còn ô `- [ ]` hoặc không có ô `- [x]` nào | Tick hết, mục không áp dụng ghi `N/A: lý do` |
| 14 | Lỗi mạng `Connection was reset` / `Failed to connect ... 443` khi push | Mạng chập chờn | Thử lại, kiểm `git ls-remote origin` trước khi kết luận |

---

## 9. Danh mục nghiệm thu (Definition of Done) cho backend

- [ ] Repo `backend` public, có README, `TECH_DEBT.md`, `CODING_CONVENTION.md`.
- [ ] `main` chỉ có commit khởi tạo; `develop` tách từ `main`; mọi thay đổi sau đó qua PR.
- [ ] Hook cục bộ bật (`git config core.hooksPath .githooks`); gitleaks đã cài.
- [ ] `npm ci` trên **clone sạch** thành công (gồm `@apt/shared-types` từ GitHub).
- [ ] Lint, dup, typecheck, format, test:cov, build, audit, gitleaks đều qua trên clone sạch.
- [ ] Workflow `pipeline`, `codeql`, `devkit-checks` xanh trên `develop` và trên một PR thử.
- [ ] Ruleset đã import, tên 7 check khớp thực tế, một PR thử đã bị chặn khi thiếu review/check.
- [ ] Ảnh Docker lên GHCR với tag `sha-xxxxxxx` (chữ thường); `rollback.yml` thử được.
- [ ] Secret staging đã thêm; `deploy-staging` **deploy thật** và smoke test qua (không chỉ "bỏ qua").
- [ ] Mỗi thành viên có commit thực chất mỗi tuần; mọi thay đổi vào `develop` qua PR có review.
- [ ] Đã ghi `AI_USAGE_LOG.md` cho phần do AI sinh (TC2.3).

---

## 10. Việc còn mở và cần nhóm xác nhận

| # | Việc | Ghi chú |
|---|---|---|
| 1 | **Quyết định gói dùng chung:** hiện thực tế là repo riêng `shared-types` cài qua git URL (không phải `file:` hay copy) | Phiên làm việc này đã làm vậy cho frontend; **chưa ghi vào `DECISIONS_LOG.md`**, cần nhóm xác nhận và ghi |
| 2 | Migration khởi tạo Prisma (Q1) | Chặn deploy có ý nghĩa; chạm thiết kế CSDL nên nhóm quyết |
| 3 | Module health và Dockerfile backend | Chưa có; cần người phụ trách BE |
| 4 | Test: coverage khoảng 2,8% so với yêu cầu 70% và thiếu tầng test | Ảnh hưởng TC2.5; nên lên kế hoạch theo tuần |
| 5 | SonarCloud: `sonar.organization` và `sonar.projectKey` vẫn là khoá của organization cũ | Bước Sonar tự bỏ qua khi thiếu `SONAR_TOKEN`; sửa khi tạo project mới |
| 6 | Server staging: có `~/placement/deploy.sh` và đủ secret chưa | Chưa xác minh trong phiên này; không đụng dự án `farmnongviet` |
| 7 | Cần giảng viên xác nhận cách đếm "tuần có commit", "build xanh" (G1, G2) | Xem Mục 7.2 trong `MO_TA_CI_CD_VA_DIEM_CHAN.md` |
| 8 | Tài liệu cũ `MO_TA_CI_CD_VA_DIEM_CHAN.md` và `20261021_DANH_GIA...` còn nhắc organization cũ và trạng thái "chưa chạy pipeline" | Cần cập nhật theo kết quả mới (đồng bộ tài liệu, quy tắc dự án số 7) |

---

## 11. Tham khảo

| Tệp | Nội dung |
|---|---|
| `D:\TLCN\frontend\frontend\.github\workflows\*.yml` | Workflow thật đã chạy xanh |
| `D:\TLCN\frontend\frontend\.githooks\` | Hook cục bộ |
| `D:\TLCN\docs-repo\devkit\rulesets\protect-main.json`, `protect-develop.json` | Ruleset gốc (bản `protect-main` cho frontend có thêm 3 check của pipeline ở `.github/rulesets/`) |
| `D:\TLCN\0.docs\tracking\GIT_CONVENTIONS.md` | Quy ước Git và ngưỡng TC2.4 |
| `docs-repo\plans\cicd\MO_TA_CI_CD_VA_DIEM_CHAN.md` | Kiến trúc staging, điểm chặn, đối chiếu rubric |
| `docs-repo\plans\cicd\20261021_DANH_GIA_VA_PHUONG_AN_CICD_BACKEND.md` | Đánh giá riêng cho backend |
