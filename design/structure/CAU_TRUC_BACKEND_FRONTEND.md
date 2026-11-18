# Sơ đồ cấu trúc `backend/backend` và `frontend`

Cập nhật: 2026-10-19 (sau đợt đồng bộ với thiết kế v3.0 — xem `0.docs/tracking/feature-plans/dong-bo-code-voi-thiet-ke-v3.md`).
Chú thích trạng thái: ✅ đã có mã · 🟡 có nhưng còn theo mô hình cũ / chưa đủ · ⬜ module rỗng (`@Module({})`) · 🗄️ giữ làm tham khảo, không biên dịch.

---

## 1. Backend — `D:\TLCN\backend\backend` (NestJS, Clean Architecture)

### 1.1 Gốc

| Đường dẫn | Vai trò |
|---|---|
| `prisma/schema.prisma` | Nguồn chân lý DB (v3.0: lô/gói duyệt đề, kỳ thi, 6 trạng thái Item) |
| `prisma/custom_migrations.sql` | Partial index, CHECK (FINAL_APPROVED, kỳ thi 5–180 phút, giao việc ≥ 1 ngày, `content_hash`) |
| `prisma/seed.ts` | Dữ liệu giả: Admin/GV/SV, kỳ thi mẫu, lô seed, 30 câu (mật khẩu từ env, argon2) |
| `src/main.ts`, `src/app.module.ts` | Khởi động, prefix `api/v1`, ValidationPipe, filter, nối module |
| `src/config/` | `configuration.ts` (tham số CAT đọc từ env), `validation.schema.ts` (Joi) |
| `src/shared/` | `decorators` (`@CurrentUser`, `@Roles`), `guards` (JWT, Roles), `filters`, `prisma` (global), `interceptors` (trống) |
| `test/` | `app.e2e-spec.ts`, thư mục `e2e/`, `integration/` (trống) |
| `.env`, `.env.example`, `package.json`, `tsconfig*.json`, `vitest.config*.ts`, `nest-cli.json`, `.oxlintrc.json` | Cấu hình dự án |
| `TRACKING_BACKEND_SCAFFOLD.md` | Lịch sử scaffold (theo SRS v2.6, đã lỗi thời) |
| `dist/`, `node_modules/` | Sinh tự động |

### 1.2 Module nghiệp vụ `src/modules/*`

| Module | Presentation | Application | Domain | Infrastructure | Trạng thái |
|---|---|---|---|---|---|
| `auth` | `auth.controller` (`POST /auth/login`, `GET /auth/me`) | `login`, `verify-token` use case; `login.dto` | `user.entity`, enum `UserRole`, `AuthProviderType`; `IUserRepository` | `prisma-user.repository`, `jwt.provider`, `jwt.strategy` | ✅ argon2, `isActive`, `mustChangePassword`; ⬜ chưa có đổi/quên mật khẩu |
| `item-bank` | `item-bank.controller` (chỉ `GET /items`, `GET /items/:id`, `POST /items/generate-explanation`) | `item.service` (facade), `list-items`, `get-item`, `generate-explanation` | `item.entity`; enum `ItemStatus` (6), `ItemBatchSource`, `Skill`, `CEFRLevel`; `IItemRepository` | `prisma-item.repository` (CAT lọc `FINAL_APPROVED`) | ✅ chỉ xem |
| `item-bank/…/_legacy` | — | `create/update/delete/clone/approve/reject-item`, `item-lifecycle.spec`, `item-source.enum` | — | — | 🗄️ CRUD form đã bỏ (DC-32) |
| `cat-engine` | — | `cat-engine.service` (facade); use case `pick-next-skill`, `select-next-item`, `compute-eap`, `check-stopping-criterion`; `cat-engine.service.spec` | `ability-estimate`, `eap-computation-state`; `cat-engine.domain-service` | (trống) | ✅ timeout theo `expiresAt` |
| `test-session` | `test-session.controller` (`POST /sessions` nhận `examRoundId`, `GET active`, `next-item`, `responses`, `resume`, `result`, `review`) | `start-session`, `submit-response`, `resume-session`, `get-active-session`, `get-session-result`, `get-session-review`, `compute-result` | `test-session.entity` (`examRoundId`, `expiresAt`), `session-response.entity` | `prisma-test-session.repository`, `redis-session-cache.service` | ✅ gắn kỳ thi |
| `language-profile` | `language-profile.controller`; guard `profile-access`, `eduz-api-key` | `get-profile`, `export-for-eduz` | `language-profile.entity`, `profile-access.policy` | `prisma-language-profile.repository`, `prisma-profile-target.lookup` | ✅ đơn trường |
| `reporting` | `reporting.controller` (`GET /reports/class-distribution`, `/export-csv`, lọc `?examRoundId=`) | `generate-class-report`, `export-csv` | `class-report.entity` | (trống) | 🟡 chưa có `error-patterns` |
| `ai-explainer` | `ai-explainer.controller` (`GET /explanations/items/:itemId`) | `explain-item` | `explanation.entity` | `gemini-flash.provider` | 🟡 vẫn sinh theo yêu cầu, chưa chuyển sang sinh cùng lô |
| `exam-round` | — | — | — | — | ⬜ rỗng |
| `user-import` | — | — | — | — | ⬜ rỗng |
| `user-admin` | — | — | — | — | ⬜ rỗng |
| `mail` | — | — | — | — | ⬜ rỗng |
| `item-generation` | — | — | — | — | ⬜ rỗng (lô, gói, duyệt A/B, C1–C3) |
| `llm-gateway` | — | — | — | — | ⬜ rỗng |

### 1.3 Cây rút gọn

```text
backend/backend
├─ prisma/            schema.prisma · custom_migrations.sql · seed.ts
├─ src/
│  ├─ main.ts · app.module.ts
│  ├─ config/         configuration.ts · validation.schema.ts
│  ├─ shared/         decorators · guards · filters · interceptors · prisma
│  └─ modules/
│     ├─ auth/ · item-bank/ (+ _legacy) · cat-engine/ · test-session/
│     ├─ language-profile/ · reporting/ · ai-explainer/
│     └─ exam-round/ · user-import/ · user-admin/ · mail/ · item-generation/ · llm-gateway/   (rỗng)
└─ test/              app.e2e-spec.ts · e2e/ · integration/
```

Mỗi module đầy đủ theo 4 tầng: `presentation/` → `application/` (use-cases, services, dto) → `domain/` (entities, enums, repositories, services, policies) → `infrastructure/` (persistence, providers, cache).

---

## 2. Frontend — `D:\TLCN\frontend` (Next.js App Router, TypeScript)

### 2.1 Gốc

| Đường dẫn | Vai trò |
|---|---|
| `src/` | Mã nguồn (xem 2.2) |
| `tests/` | `unit/` (button, env, health-route, lib, messages, mock-api), `e2e/flows.spec.ts` (Playwright), `setup.ts` |
| `public/` | Tài nguyên tĩnh |
| `package.json`, `tsconfig.json`, `next.config.ts`, `eslint.config.mjs`, `vitest.config.mts`, `playwright.config.ts`, `components.json` | Cấu hình |
| `Dockerfile`, `.dockerignore`, `.github/`, `sonar-project.properties`, `.jscpd.json` | CI/CD, chất lượng mã |
| `README.md`, `AGENTS.md`, `CODING_CONVENTION.md`, `TECH_DEBT.md` | Tài liệu dự án |
| `frontend/` | ⚠️ Bản sao cũ của cả frontend (còn `institutionId`, `PENDING_REVIEW`); nên xóa |
| `.next/`, `coverage/`, `playwright-report/`, `reports/`, `test-results/`, `node_modules/` | Sinh tự động |

### 2.2 Route `src/app` (App Router)

| Nhóm | Route | File | Màn hình (theo `DANH_SACH_MAN_HINH_THEO_ROLE.md`) | Trạng thái |
|---|---|---|---|---|
| `(auth)` | `/login` | `login/page.tsx` | S01 Đăng nhập | ✅ (đã có link Quên mật khẩu; chuyển từ `(public)` ngày 29/10/2026) |
| `(student)` | `/` | `page.tsx` | S02 Trang chủ SV | 🟡 chưa có "Kỳ thi của tôi", chưa gửi `examRoundId` |
| `(student)` | `/history` | `history/page.tsx` | S07 Lịch sử | ✅ |
| `(student)` | `/results/[sessionId]` | `results/[sessionId]/page.tsx` | S05 Kết quả | ✅ |
| `(student)` | `/results/[sessionId]/review` | `…/review/page.tsx` | S06 Xem lại đáp án | ✅ |
| `(exam)` | `/exam/[sessionId]` | `exam/[sessionId]/page.tsx` | S04 Làm bài | 🟡 route cũ (đích: theo `roundId`) |
| `(teacher)` | `/teacher` | `teacher/page.tsx` | Trang chủ GV | ✅ |
| `(teacher)` | `/teacher/items`, `/teacher/items/[id]` | `items/page.tsx`, `items/[id]/page.tsx` | S08, S10 (chỉ xem) | 🟡 route cũ (đích: `/teacher/item-bank`) |
| `(teacher)` | `/teacher/items/new`, `/teacher/items/[id]/edit` | `new/page.tsx`, `edit/page.tsx` | S09 (đã bỏ) | 🗄️ chỉ redirect |
| `(teacher)` | `/teacher/review-queue` | `review-queue/page.tsx` | S11 (cũ) | 🟡 chỉ xem, chờ làm Hộp việc A/B |
| `(teacher)` | `/teacher/reports` | `reports/page.tsx` | S12 Báo cáo lớp | ✅ (chưa có bộ lọc kỳ trên UI) |
| `(teacher)` | `/teacher/students` | `students/page.tsx` | S13 Tìm SV | ✅ |
| (gốc) | `/403`, `error.tsx`, `not-found.tsx` | — | S15 Lỗi chung | ✅ |
| `api/` | `/api/auth/login`, `/api/auth/logout`, `/api/proxy/[...path]`, `/api/health`, `/api/health/live` | `route.ts` | BFF: đặt cookie JWT, proxy sang backend | ✅ |
| — | `/admin/*`, `/change-password`, `/forgot-password`, `/reset-password`, `/teacher/tasks/*`, `/teacher/students/[studentId]` | — | S14, S16–S24, S26–S36 | ⬜ chưa có |

### 2.3 Phần còn lại của `src`

| Thư mục | Nội dung |
|---|---|
| `features/auth` | `login-form.tsx` |
| `features/exam` | `exam-runner.tsx`, `student-home.tsx`, `use-countdown.ts` |
| `features/result` | `result-card.tsx`, `result-view.tsx`, `review-view.tsx` |
| `features/history` | `history-view.tsx` |
| `features/items` | `item-list.tsx`, `item-detail.tsx`, `review-queue.tsx`, `item-form.tsx` (🗄️ không còn route dùng) |
| `features/reports` | `reports-view.tsx`, `student-lookup.tsx` |
| `components/layout` | `app-header`, `confirm-dialog`, `logout-button`, `native-select`, `states` |
| `components/ui` | shadcn/ui: alert, badge, button, card, dialog, input, label, radio-group, select, skeleton, sonner, table, tabs, textarea |
| `components/providers.tsx` | React Query, theme, toaster |
| `lib/api` | `client`, `endpoints` (một nơi liệt kê route API), `types`, `normalize`, `errors`, `error-message`, `proxy-policy` |
| `lib/auth` | `jwt`, `session`, `user`, `roles` (điều hướng theo role) |
| `lib/` khác | ~~`enums.ts`~~ (đã xóa 20/10, dùng `@apt/shared-types`), `env.ts`, `env-schema.ts`, `explanation.ts`, `utils.ts` |
| `messages/vi.ts` | Chuỗi giao diện tiếng Việt |
| `mocks/` | `db.ts`, `handlers.ts`, `server.ts` (MSW), `fixtures/` |
| `proxy.ts`, `instrumentation.ts` | Middleware điều hướng/xác thực, khởi tạo |

### 2.4 Cây rút gọn

```text
frontend
├─ src/
│  ├─ app/           (auth) · (student) · (exam) · (teacher)/teacher · api/ · 403 · error · not-found
│  ├─ features/      auth · exam · result · history · items · reports
│  ├─ components/    layout · ui · providers.tsx
│  ├─ lib/           api · auth · env*.ts · utils.ts
│  ├─ messages/vi.ts · mocks/ · proxy.ts · instrumentation.ts
├─ tests/            unit/ · e2e/ · setup.ts
├─ public/ · .github/ · Dockerfile · cấu hình
└─ frontend/         (bản sao cũ — nên xóa)
```

---

## 3. Đối chiếu nhanh với cấu trúc đích

Cấu trúc đích: `Update/KE_HOACH_CAU_TRUC_DU_AN.md`. Phần còn thiếu so với đích: các module backend rỗng (mục 1.2), toàn bộ nhóm route `/admin/*`, Hộp việc GV A/B, đổi/quên mật khẩu, và route làm bài theo `roundId` ở frontend.
