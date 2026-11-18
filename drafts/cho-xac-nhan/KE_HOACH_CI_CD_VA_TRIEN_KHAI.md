# Kế hoạch: CI/CD và triển khai — nhắm điểm tối đa TC2.4 (phần Git/CI), TC2.5 (phần CI), TC2.6, tránh G6 và G8

> **Phạm vi đọc:** `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (TC2.4, TC2.5, TC2.6, Mục 5 bảng metric, Mục 7 quy tắc chặn G1–G9, Mục 8 minh chứng), `0.docs/tracking/feature-plans/ke-hoach-tao-repo.md`, `GIT_CONVENTIONS.md`, `docs-repo/devkit/*` (README, `devkit-checks.yml`, `protect-main.json`), `DECISIONS_LOG.md` (#34, #36, #37, #39, #49–#64), `feature-plans/ai-llm-gateway.md`, mã `backend/backend` và `frontend` hiện có.
> **Ngày lập:** 2026-10-09 (Tuần 4/12). **Vai trò người lập:** Senior Engineer + PM.
> **Trạng thái:** 🔄 **Đã có server staging (cập nhật 2026-10-09, sau bản "chỉ GitHub")** — các task trước đó bị hoãn nay được mở lại, nhưng **chưa xác minh được server** (chưa SSH, chưa biết OS/Docker/RAM/cổng). Q-CD1…Q-CD4 đã chốt. Các Q-CD đã chốt (xem Mục 5; DECISIONS_LOG #65–#70); chưa hỏi Q-CD8, Q-CD2b (dùng mặc định ★). Còn CD0.2 (hỏi GVHD) và CD0.3 (xác minh server). Địa chỉ server **không ghi vào repo hay tài liệu**; lưu ở GitHub Secret `STAGING_HOST`. Chưa tạo workflow, Dockerfile, repo hay cấu hình server nào. File theo dõi đi kèm: [`TRACKING_CI_CD_VA_TRIEN_KHAI.md`](./TRACKING_CI_CD_VA_TRIEN_KHAI.md).
>
> ⚠️ **Giới hạn nói thẳng:** (1) mọi giới hạn dịch vụ bên thứ ba (số phút GitHub Actions, GHCR, SonarCloud, gói miễn phí Grafana/BetterStack/UptimeRobot, ruleset gói Free) là **từ hiểu biết chung, chưa kiểm chứng trên tài khoản của nhóm** — task CD0.3 kiểm; (2) tôi **chưa truy cập server** nên mọi nhận định về RAM/CPU/Docker trên server chỉ dựa vào dòng "Ubuntu, 2 vCPU, 2 GB RAM (ảnh nhóm cung cấp 2026-10-02)" trong `ai-llm-gateway.md`; (3) không có con số thời gian pipeline nào đã đo — mọi mục tiêu ≤15 phút là *mục tiêu thiết kế*, đo ở CD8.

---

## 0. Tóm tắt điều hành

**Điểm tối đa cần đạt ở phần CI/CD** (theo bảng metric Mục 5 rubric):

| Tiêu chí | Ngưỡng Mức 5 | Hiện trạng | Mức khó |
|---|---|---|---|
| **TC2.6** số chặng pipeline | ≥ 6: build → lint/phân tích tĩnh → test → quét bảo mật/phụ thuộc → đóng gói Docker → deploy tự động | Chưa có pipeline nào chạy (devkit có 4 check *vệ sinh PR*, chưa chạy trên GitHub) | Trung bình |
| TC2.6 tỉ lệ build xanh | ≥ 90% | — | **Cao** (mọi lần chạy đỏ, kể cả trên PR, đều có thể bị tính) |
| TC2.6 số lần deploy tự động | ≥ 10, **trải đều** theo tiến độ | 0 | Trung bình (cần deploy chạy được sớm, ~Tuần 5–6) |
| TC2.6 commit → staging | ≤ 15 phút | — | Trung bình (cần build image trên Actions, không build trên server 2 GB) |
| TC2.6 giám sát | health check + log tập trung + cảnh báo; secret qua nền tảng; phiên bản + rollback | Không có endpoint health, không Dockerfile | Trung bình |
| **TC2.4** (phần CI) | 0 lỗi lint, 0 Blocker/Critical, trùng lặp ≤ 3%, 0 secret (gitleaks/truffleHog), README + sơ đồ triển khai + nợ kỹ thuật | Chưa có SonarCloud/CodeQL/gitleaks chạy; backend chưa có `.gitignore` | Trung bình |
| **TC2.4** (phần Git) | ≥ 90% tuần có commit; ≥ 90% thay đổi qua PR có review | **Chưa có git**; đang Tuần 4 | **Cao** (không bù được tuần đã qua) |
| **TC2.5** (phần CI) | 100% test pass ở lần chạy CI cuối; coverage mô-đun cốt lõi ≥ 70% có báo cáo; ≥ 4 tầng test | 0 test ở BE; FE có 12 unit + 1 E2E | Cao với BE |
| **G6** | Không có pipeline chạy được lúc bảo vệ ⇒ TC2.6 tối đa Mức 2 | — | **Phải tránh** |
| **G8** | Repo không cấp quyền hội đồng/không build được ⇒ TC2.2 và TC2.4 mỗi tiêu chí −1 mức | — | Tránh bằng CI build từ sạch mỗi lần |

### 0.1. Phạm vi giai đoạn 1 — chỉ GitHub, chưa có server (chốt 2026-10-09)

> **CẬP NHẬT cùng ngày — mục này đã bị thay thế một phần:** bạn cung cấp một server staging, nên 17 task ⏸ ở dưới **được mở lại** và danh sách "hoãn" không còn hiệu lực. Nội dung bên dưới giữ lại để truy vết lý do ban đầu (nhiều đoạn vẫn đúng cho thứ tự thực hiện: CI trước, deploy sau). Điều kiện để deploy chạy thật: CD0.3 xác minh được server (SSH, Docker, RAM, cổng 80/443) và có HTTPS (Q-CD5).

**Làm ngay (không cần server):** CD0, CD1, CD2, CD3, CD4 (Dockerfile + build + đẩy GHCR), CD6.7 (tag + GitHub Release), CD7.1–7.2 (endpoint health), CD7.6 (runbook), CD8 (phần đo CI), CD9.
**Hoãn tới khi có server:** CD5 (toàn bộ hạ tầng staging), CD6.1–6.6, CD6.8, CD6.9 (deploy tự động, smoke trên staging, rollback, thông báo deploy), CD7.3–7.5 (monitor ngoài, log tập trung, cảnh báo), CD8.1/CD8.2 (đo commit→staging; thay bằng đo commit→image đã đẩy lên GHCR).
**Thêm để bù chỗ thiếu server:** CD4.7 *smoke test ngay trong runner* (dựng BE+FE+Postgres+Redis bằng `docker compose` tạm trong job, gọi `/health` và trang chủ, rồi hủy) và CD6.10 *job `deploy` có điều kiện* (`if: vars.DEPLOY_ENABLED == 'true'`, mặc định **bị bỏ qua**, bật khi có server).

**Hệ quả điểm số — nói thẳng:**
- Không có server ⇒ **chưa có deploy tự động thật**. Theo rubric TC2.6, "CI tự động nhưng triển khai còn thủ công" = **Mức 3** (≥2 chặng, ≥1 lần deploy tự động *nếu* có). Muốn Mức 4/5 và tránh **G6** (cần pipeline CI/CD *chạy được* lúc bảo vệ, với "sản phẩm chỉ chạy trên máy cá nhân" là Mức 1) thì cuối cùng **vẫn phải có một môi trường đã triển khai**.
- **Không tạo "deploy giả"** (ví dụ ghi một Deployment rỗng) để tăng số lần deploy: đó là số liệu không thật, hội đồng đối chiếu log sẽ lộ.
- Tiêu chí "≥10 lần deploy, trải đều" chỉ tính từ khi server sẵn sàng. **Server càng muộn, 10 lần càng khó trải đều** (hiện Tuần 4; 8 tuần còn lại). Mốc cần nhớ: có staging chạy được **chậm nhất đầu Tuần 7** để còn đủ thời gian cho ≥10 lần deploy trước Tuần 11 (mốc này là ước lượng của tôi, không phải quy định rubric).
- Chuỗi build → lint → test → bảo mật → Docker vẫn hoàn toàn đạt được và là nền cho TC2.4, TC2.5.

**Chiến lược một câu:** dựng **"khung xương đi bộ" (walking skeleton)** — một pipeline đủ 6 chặng deploy được bản BE/FE tối thiểu lên staging **trước cuối Tuần 5**, rồi mọi PR sau đó tự động đi qua nó. Điều này vừa giải bài toán "≥10 lần deploy trải đều", vừa biến CI thành bằng chứng sống cho TC2.4/2.5/2.6 thay vì dồn làm cuối kỳ.

**Ba rủi ro lớn nhất (đọc trước):**
1. **Tỉ lệ tuần có commit (TC2.4):** `ke-hoach-tao-repo.md` đã tính: repo chỉ có từ Tuần 3–4 ⇒ tối đa ~83% (Mức 4) nếu mẫu số 12 tuần; hiện nay (Tuần 4, chưa có git) còn thấp hơn. **Không bù bằng commit lùi ngày.** Cần hỏi GVHD cách Khoa đếm (CD0.2).
2. **Build xanh ≥ 90%:** chưa rõ Khoa đếm cả run trên PR hay chỉ nhánh chính. Thiết kế để *mọi* run đỏ đều hiếm: kiểm cục bộ bằng hook trước khi push, `actionlint`, không đưa bước dễ flaky (E2E) vào required check ở giai đoạn đầu.
3. **Server 2 GB + Cookie `Secure`:** build image trên server là không khả thi; và cookie `httpOnly; Secure` của BFF (quyết định #50) **không hoạt động trên HTTP thường** ⇒ staging bắt buộc có HTTPS ⇒ cần tên miền (Q-CD5).

---

## 1. Kiểm chứng nguồn (bằng chứng đã đọc)

| # | Điều đã kiểm | Nguồn | Kết quả |
|---|---|---|---|
| V1 | Ngưỡng TC2.4/2.5/2.6, G6, G8, danh mục minh chứng | Rubric Mục 4, 5, 7, 8 | Đã trích ở Mục 0; Mức 5 TC2.6 còn đòi **đánh phiên bản + rollback + secret qua nền tảng + giám sát sau deploy** |
| V2 | Quy ước Git đã chốt | `GIT_CONVENTIONS.md`, #36 | `feat/*`→`develop` (squash)→`main` (merge commit); Conventional Commits; review chéo 100% |
| V3 | Devkit hiện có | `docs-repo/devkit` | Git hook cục bộ + workflow `devkit-checks` (4 job: `branch-policy`, `commit-lint`, `pr-checklist`, `secret-scan`) + ruleset `protect-main/develop` (1 approval, bypass rỗng). **Chưa có** build/lint/test/CodeQL/Docker/deploy. README tự ghi "chưa chạy trên GitHub thật" |
| V4 | Quyết định về repo | #34 | 3 repo `backend`/`frontend`/`docs`, Free + **public**; ruleset org-level; SonarCloud/CodeQL miễn phí cho repo public (cần xác nhận) |
| V5 | Dockerfile/compose/Nginx/health ở BE | `ls backend/backend`, `grep -il health src` | **Không có** Dockerfile, `docker-compose`, cấu hình Nginx; **không có** endpoint health |
| V6 | FE | `frontend/` | `output: "standalone"` đã bật; scripts `lint`, `typecheck`, `format:check`, `test`, `test:cov`, `test:e2e`, `build`; 12 test đơn vị + 1 E2E; chưa có Dockerfile (FE9.3) |
| V7 | BE scripts | `package.json` BE | `lint` = `oxlint --type-aware`, `test` = `vitest run`, `test:cov`, `test:e2e`, `db:migrate`; tracking BE Q-01: 0 test |
| V8 | Server | `ai-llm-gateway.md` | "Ubuntu, 2 vCPU, 2 GB RAM (ảnh nhóm cung cấp 2026-10-02)"; #39: chuyển Postgres sang dịch vụ quản lý để dành RAM cho LiteLLM (câu 5, 6 **chưa chốt**); K4a (file `20261009_...`) đề xuất bỏ LiteLLM ở giai đoạn TL |
| V9 | Stack triển khai SRS | SRS III, XI | Docker + Docker Compose + Nginx (gateway), TLS 1.2+ qua Nginx (XV.3) |
| V10 | Trạng thái git | `AI_USAGE_LOG`, thư mục | `D:\TLCN`, `D:\TLCN\frontend`: **chưa `git init`** |

---

## 2. Phân tích: từng metric → cách đạt → rủi ro

### 2.1. TC2.6 — CI/CD và vận hành (5 điểm)

| Yêu cầu Mức 5 | Thiết kế để đạt | Rủi ro / bẫy | Task |
|---|---|---|---|
| **≥ 6 chặng** | `build` → `lint+typecheck+static` → `test` (unit+integration) → `security` (gitleaks, `npm audit`, dependency-review, CodeQL, Trivy) → `package` (Docker→GHCR) → `deploy` (staging) + `smoke` | Gộp chặng làm "6 job" nhưng thật ra chạy rời rạc: để hội đồng thấy rõ, vẽ pipeline thành **một workflow có `needs:` nối tiếp** (ảnh chụp cho slide) | CD2–CD6 |
| **Build xanh ≥ 90%** | Kiểm cục bộ trước push (hook `pre-push` chạy `lint`+`typecheck`+`test`); dùng `actionlint` trước khi đẩy file workflow; cache phụ thuộc; không đặt E2E/Sonar mới vào required cho tới khi ổn định; `concurrency` hủy run cũ để không sinh run "cancelled" gây nhiễu | **Run lỗi cấu hình ở giai đoạn đầu kéo tụt tỉ lệ.** Giảm bằng cách thử workflow trên nhánh `chore/ci-*` ngay từ Tuần 4–5 (khi tổng số run còn ít, mỗi run đỏ tốn nhiều) — thực ra *tổng* run càng nhiều càng pha loãng: đẩy tần suất merge đều | CD2.8, CD8 |
| **≥ 10 deploy tự động, trải đều** | Mỗi merge vào `develop` ⇒ deploy staging (dùng `environment: staging` để GitHub ghi **Deployments**; đây là nguồn đếm sạch nhất) | Nếu deploy chỉ chạy được từ Tuần 9 thì "trải đều" thất bại. Mục tiêu: lần deploy đầu **≤ cuối Tuần 5**, ≥ 1 lần/tuần sau đó | CD6 |
| **commit → staging ≤ 15 phút** | Build image **trên Actions** (không trên server), `buildx` + cache GHA, các job song song, server chỉ `pull` + `up -d`; ngân sách: CI ≤ 8 phút, package ≤ 4, deploy+smoke ≤ 3 *(mục tiêu thiết kế, chưa đo)* | Next build + Docker build có thể vượt nếu không cache; migration dài | CD4, CD8.1 |
| **Secret qua cơ chế nền tảng** | GitHub Environments secrets (`staging`) cho SSH key/URL; file `.env` trên server nằm ngoài repo (quyền 600) | Secret để trong workflow/`docker-compose.yml` commit vào repo = vừa mất điểm TC2.6 vừa vi phạm TC2.4 | CD5, CD6 |
| **Đánh phiên bản + rollback** | Image tag = `git sha` (+ `vX.Y.Z` khi tag `main`); workflow `rollback` (`workflow_dispatch` nhận tag) deploy lại tag cũ; giữ N image gần nhất | **Prisma không có migration "down"** ⇒ rollback chỉ an toàn nếu migration tương thích ngược (chính sách *expand/contract*, Q-CD11) | CD6.5, CD6.6 |
| **Giám sát: health check + log tập trung + cảnh báo** | `GET /health` (liveness) và `/ready` (DB+Redis) ở BE; `/api/health` ở FE; `HEALTHCHECK` trong Dockerfile; monitor ngoài ping + báo qua email/Discord/Telegram; log gom về dịch vụ ngoài (không tự dựng Loki trên 2 GB); pipeline fail cũng báo | Dựng Grafana/Loki trên server 2 GB sẽ ăn hết RAM (Q-CD7) | CD7 |

### 2.2. TC2.4 — phần CI và Git

| Yêu cầu | Thiết kế | Ghi chú |
|---|---|---|
| 0 lỗi lint, 0 Blocker/Critical, trùng lặp ≤ 3% | Lint **fail CI** nếu còn lỗi; SonarCloud với Quality Gate (hoặc CodeQL + `jscpd`, Q-CD6); loại trừ file sinh tự động (`components/ui/**` của shadcn, `prisma/migrations`, `dist`) khỏi tính trùng lặp *một cách minh bạch* (ghi cấu hình) | Không "giấu" mã trùng bằng loại trừ tùy tiện — hội đồng có thể hỏi |
| 0 secret (gitleaks/truffleHog) | gitleaks ở hook, ở CI (**quét toàn bộ lịch sử** ít nhất một lần trước push đầu), bật GitHub secret scanning + push protection | Backend hiện có `.env` thật, **chưa có `.gitignore`** (A-09): quét *trước* `git add`, không sau |
| ≥ 90% tuần có commit | Mỗi người ≥ 1 commit thực chất/tuần (đã là quy tắc #2 GIT_CONVENTIONS); báo cáo tự động số tuần có commit từ `git log` (CD8.4) | **Không tạo commit lùi ngày/commit rỗng** |
| ≥ 90% thay đổi qua PR có review | Ruleset đã soạn (1 approval, bypass rỗng) + quy ước khi một người vắng (Q4 của `ke-hoach-tao-repo`) | Nhóm 2 người: PR kẹt khi một người vắng — ghi quy ước trước |
| README + hướng dẫn cài + sơ đồ triển khai + nợ kỹ thuật | README mỗi repo (FE đã có); sơ đồ triển khai (Mục 3); `TECH_DEBT.md` | Task CD9 |

### 2.3. TC2.5 — phần CI

- Pipeline phải **chạy và công bố** coverage (artifact + tóm tắt trong job summary) và để lần chạy cuối trên `main` xanh 100%.
- Tầng kiểm thử trong CI: (1) unit, (2) integration (Postgres + Redis bằng `services:`), (3) API (supertest), (4) E2E (Playwright), (5) phi chức năng (k6 nhẹ trên staging, ví dụ ngưỡng SRS 15.1) — Mức 5 cần ≥ 4 tầng.
- **Ngưỡng coverage đặt theo số đo thật**, nâng dần; không đặt 70% khi chưa đạt (sẽ làm CI đỏ liên tục, kéo tụt tỉ lệ xanh).

---

## 3. Kiến trúc pipeline và môi trường đề xuất

```
 feat/* ──PR──► develop ──PR──► main                (devkit: branch-policy, commit-lint, pr-checklist)
   │              │                │
   ▼              ▼                ▼
 [PR CI]        [CI + CD]        [Release]
 1 build         1 build          tag vX.Y.Z + GitHub Release
 2 lint/static   2 lint/static    (không deploy riêng — Q-CD3)
 3 test (unit+   3 test
   integration)  4 security (gitleaks, audit, dependency-review, CodeQL, Sonar)
 4 security      5 package: docker buildx → GHCR (tag = sha)   ← Trivy scan
                 6 deploy staging (environment: staging) → migrate → pull/up -d → smoke → (fail ⇒ rollback tag trước)
                         │
                         ▼
        Staging (Ubuntu 2 vCPU/2 GB) — Nginx(TLS) ─► frontend (Next standalone)
                                                   └► backend (NestJS) ─► Redis, Postgres (container hoặc managed — Q-CD4)
        Giám sát ngoài: uptime monitor ─ ping /health ─► cảnh báo;  log shipper ─► dịch vụ log;  Actions fail ─► webhook
```

**Phân chia repo:** `backend` và `frontend` mỗi repo một pipeline riêng; cả hai đẩy image lên GHCR. Nơi giữ `docker-compose.yml` + `nginx.conf` của staging là quyết định Q-CD2b (không nằm ngoài kế hoạch #34 3 repo nếu đặt trong `backend/deploy/` hoặc `docs/deploy/`).

**Ràng buộc bảo mật cho repo public (bắt buộc):** dùng `pull_request` (không dùng `pull_request_target`) cho mã từ nhánh; secret **chỉ** hiện cho workflow chạy trên `develop`/`main` qua `environment`; `permissions:` tối thiểu ở từng job; ghim action theo SHA hoặc tag chính thức; **không** chạy self-hosted runner trên repo public (PR từ fork có thể chạy mã tùy ý trên server).

---

## 4. Các "bẫy mất điểm" đã nhận diện

| # | Bẫy | Hậu quả rubric | Phòng tránh |
|---|---|---|---|
| T1 | Push đầu có `.env` hoặc khóa API (BE chưa có `.gitignore`) | TC2.4 secret ≥ 1; lịch sử Git giữ vĩnh viễn | Quét gitleaks toàn lịch sử trước push; `.gitignore` là file đầu tiên (FE đã làm đúng) |
| T2 | Pipeline chỉ chạy `build` mà bỏ test/lint | TC2.6 chỉ Mức 3 | Chặng test là điều kiện cứng của `package`/`deploy` (`needs`) |
| T3 | Deploy lần đầu quá muộn | "≥10 lần, trải đều" thất bại | Walking skeleton cuối Tuần 5 |
| T4 | Build image trên server 2 GB | Chậm/OOM, vượt 15 phút | Build trên Actions, server chỉ pull |
| T5 | Staging HTTP thường + cookie `Secure` | Đăng nhập hỏng; vi phạm SRS TLS | HTTPS ngay từ đầu (Q-CD5) |
| T6 | Migration không tương thích ngược | Rollback hỏng dữ liệu | Expand/contract; kiểm drift ở CI (BE P7.4) |
| T7 | Quality Gate Sonar đỏ vì mã sinh tự động / mã BE scaffold lỗi | Build xanh thấp | Cấu hình loại trừ có ghi chép; sửa lỗi 🔴 BE (kế hoạch BE) trước khi bật gate "required" |
| T8 | CI phụ thuộc DB/Redis ngoài | Flaky, đỏ ngẫu nhiên | `services:` container trong job; không gọi dịch vụ ngoài (Gemini) trong test — dùng provider giả |
| T9 | Lần chạy CI cuối trên `main` đỏ vào ngày bảo vệ | TC2.5 pass-rate, G6 | **Đóng băng** `main` từ Tuần 11 (chỉ hotfix); chạy lại lần cuối + chụp màn hình |
| T10 | Secret cho PR từ fork | Lộ khóa | Xem ràng buộc Mục 3 |
| T11 | Dữ liệu CLOTH (giấy phép chưa rõ #26) vào seed/staging công khai | Rủi ro bản quyền | Staging chỉ dùng dữ liệu tổng hợp; gắn nhãn |
| T12 | Hội đồng không build được repo (G8) | −1 mức TC2.2 và TC2.4 | CI `build` từ checkout sạch mỗi lần (`npm ci`), README đầy đủ, cấp quyền Read cho hội đồng |

---

## 5. Các điểm CẦN BẠN CHỐT (điền ô `☐`)

| Mã | Câu hỏi | Phương án (★ = khuyến nghị) | Đánh đổi |
|---|---|---|---|
| ☑ **Q-CD1** (chốt A — *server đã có*) | Staging chạy ở đâu? | ★ **A.** Server Ubuntu 2 vCPU/2 GB hiện có (CD0.3 xác minh) · **B.** VPS lớn hơn (trả phí) · **C.** PaaS (Render/Railway/Fly) | A giữ đúng stack Docker+Nginx của SRS, rẻ, nhưng RAM sát. B thoải mái, tốn tiền. C dễ nhưng lệch SRS/Nginx và có giới hạn gói miễn phí |
| ☑ **Q-CD2** (chốt A — *server đã có*) | Cơ chế deploy | ★ **A.** Actions build → GHCR; deploy bằng SSH `docker compose pull && up -d` · **B.** Self-hosted runner trên server · **C.** Watchtower tự kéo image | A an toàn cho repo public, rõ ràng, có `environment`. B **không dùng cho repo public** (chạy mã tùy ý). C khó kiểm soát thứ tự migrate và smoke test |
| ☐ **Q-CD2b** | `docker-compose.yml` + `nginx.conf` staging nằm ở đâu? | ★ **A.** `backend/deploy/` (BE deploy copy sang server) · **B.** `docs/deploy/` · **C.** repo thứ tư `deploy` | A đơn giản nhất; FE chỉ cần `pull frontend`. C trái #34 (3 repo) nhưng tách trách nhiệm tốt |
| ☑ **Q-CD3** (chốt A — *server đã có*) | Số môi trường | ★ **A.** Một môi trường `staging` tự động từ `develop`; `main` chỉ gắn tag + GitHub Release (cùng image) · **B.** staging + production trên cùng host (2 compose project) · **C.** hai host | A đủ Mức 5 (rubric nói "staging"); B tốn RAM; C tốn tiền |
| ☑ **Q-CD4** (chốt A — *server đã có*) | Postgres của staging | ★ **A.** Container trong compose + volume + `pg_dump` định kỳ · **B.** Dịch vụ quản lý (Neon/Supabase; xem #39 câu 5) | A tiết kiệm phụ thuộc ngoài, nhưng ăn RAM server 2 GB. B giải phóng RAM (lý do #39) nhưng DB miễn phí có thể ngủ/dừng (đã nêu ở `ai-llm-gateway.md`). *Phụ thuộc K4a: nếu không dùng LiteLLM thì lý do của B yếu đi* |
| ☑ **Q-CD5** (chốt lại: tên miền `adaptiveplacementtest.id.vn`, DNS-01 bằng **TXT thủ công** mỗi ≤ 90 ngày, cổng 8443 — #74) | Tên miền và HTTPS | ★ **A.** Tên miền riêng/DDNS + Let's Encrypt · **B.** Hostname dạng `<ip>.sslip.io` + Let's Encrypt · **C.** HTTP thường | A/B cho TLS thật, cookie `Secure` hoạt động. C **làm hỏng đăng nhập BFF** — không khuyến nghị |
| ☑ **Q-CD6** (chốt B: SonarCloud + CodeQL, khác ★) | Phân tích tĩnh/trùng lặp | ★ **A.** SonarCloud + CodeQL · **B.** CodeQL + `jscpd` (khớp Q2 `ke-hoach-tao-repo`) | A cho báo cáo trực quan, Quality Gate, cần kiểm gói miễn phí. B không cần tài khoản ngoài nhưng không có dashboard đẹp |
| ☑ **Q-CD7** (chốt A: monitor ngoài + log hosted) | Log tập trung + cảnh báo | ★ **A.** Monitor ngoài (UptimeRobot/BetterStack…) + dịch vụ log hosted (gói miễn phí) + webhook Discord/Telegram/email · **B.** Tự dựng Loki+Grafana · **C.** Chỉ `docker logs` | A nhẹ RAM, đủ "tập trung + alert" nếu gói miễn phí đáp ứng. B ăn RAM server 2 GB. C **không đạt** "log tập trung" |
| ☐ **Q-CD8** | Registry | ★ **A.** GHCR · **B.** Docker Hub | A gắn sẵn với GitHub, quyền theo repo |
| ☑ **Q-CD9** (chốt A) | Required checks và E2E | ★ **A.** Required = `lint`, `typecheck`, `test`, `build`, `security`, (`sonar` khi ổn định); E2E chạy nhưng **chưa required** tới khi ổn định · **B.** Mọi thứ required ngay | A giữ tỉ lệ xanh cao, rủi ro lọt lỗi UI. B nghiêm ngặt nhưng dễ đỏ vì flaky |
| ☑ **Q-CD10** (chốt A) | Chính sách rollback và migration | ★ **A.** Rollback = deploy lại image tag cũ; migration theo *expand/contract* (tương thích ngược), không có migration down · **B.** Viết migration down thủ công | A phù hợp Prisma, cần kỷ luật khi viết migration. B tốn công, dễ sai |
| ☑ **Q-CD11** (chốt: KHÔNG sao lưu, khác ★) | Sao lưu DB staging | ★ **A.** `pg_dump` hằng ngày, giữ 7 bản, lưu ngoài server · **B.** Không sao lưu | A rẻ; B rủi ro mất dữ liệu demo |
| ☑ **Q-CD12** (chốt B': cùng server, Docker + cổng 8443, KHÔNG đụng farmnongviet — #71) | Dùng chung server với dự án `farmnongviet` (Nginx host giữ 80/443, UFW chỉ mở 22/80/443/8080) | **A'.** VPS/server riêng cho staging (cách ly hoàn toàn) · **B'.** Cùng server nhưng Docker + Nginx container trên cổng khác (ví dụ 8443), HTTPS bằng chứng chỉ tự ký hoặc tên miền riêng + DNS-01; phải mở thêm cổng UFW; vẫn dùng chung RAM/CPU · **C'.** Không dùng server này; chỉ CI trên GitHub tới khi có hạ tầng | A' sạch nhất, tốn tiền. B' không sửa gì của dự án kia nhưng Let's Encrypt kiểu HTTP-01/sslip.io **không dùng được** (cần cổng 80/443), RAM khả dụng ~944 MB và swap đã dùng nên có thể làm chậm dự án kia. C' an toàn nhưng chưa có deploy (TC2.6 ≤ Mức 3, nguy cơ G6) |
| ☐ **Q-CD13** | Cài Docker bằng gì và khi nào được khởi động lại server | ★ **A.** Kho chính thức Docker (`docker-ce` + plugin compose), khởi động lại vào khung giờ ít người dùng · **B.** `docker.io` từ Ubuntu (29.1.3) + `docker-compose-v2` · **C.** snap (không khuyến nghị) | A cho bản mới và plugin compose đúng, thêm một kho apt. B đơn giản, có thể thiếu/lệch plugin compose. Khởi động lại làm gián đoạn dự án kia, cần báo chủ dự án đó |
| **Hỏi GVHD (không phải quyết định kỹ thuật)** | (1) Khoa đếm "tuần có commit" từ ngày bắt đầu đồ án hay từ ngày tạo repo? (2) "Build xanh" tính cả run PR hay chỉ nhánh chính? (3) Staging trên server của nhóm có được chấp nhận làm "môi trường đã triển khai"? (4) Hội đồng cần quyền gì để truy cập repo/staging? | | Nếu không hỏi sẽ phải đoán và có thể sai ngưỡng |
| **Người phụ trách hạ tầng CI/CD** | _(điền tên)_ | | Hiện chưa ai |

### 5.1. Phản hồi của bạn (điền khi duyệt)

```
Duyệt: ☐ hết mặc định ★   ☐ có khác mặc định (liệt kê)
Q-CD1:   Q-CD2:   Q-CD2b:  Q-CD3:   Q-CD4:   Q-CD5:
Q-CD6:   Q-CD7:   Q-CD8:   Q-CD9:   Q-CD10:  Q-CD11:
Người phụ trách:            Ghi chú:
```

---

## 6. Phụ thuộc và tiến độ đề xuất

```
CD0 (cổng) ─► CD1 (repo + devkit chạy thật) ─► CD2 (CI chặng 1–3) ─► CD3 (bảo mật/chất lượng) ─► CD4 (Docker)
                                                                                    │
CD5 (hạ tầng staging, ∥ từ sau CD0) ───────────────────────────────────────────────┤
                                                                                    ▼
                                                  CD6 (deploy tự động) ─► CD7 (giám sát) ─► CD8 (đo + tối ưu) ─► CD9 (khép sổ)
```

| Tuần | Mục tiêu CD | Ghi chú |
|---|---|---|
| **4 (hiện tại)** | CD0, CD1: chốt quyết định, hỏi GVHD, tạo org/repo/git, devkit chạy thật | Phụ thuộc `ke-hoach-tao-repo.md` bước 1–10 |
| **5** | CD2, CD3 (phần cốt lõi), CD4, CD5, CD6 *skeleton* | **Mốc then chốt: deploy tự động lần đầu** (BE `/health` + FE trang chủ) |
| **6** | CD3 hoàn thiện, CD7, rollback | Trước gate G1 (cuối Tuần 6): có ảnh chụp pipeline xanh đủ chặng |
| 7–10 | Duy trì, tối ưu thời gian, E2E/k6, nâng ngưỡng coverage | ≥ 1 deploy/tuần |
| 11 | **Đóng băng `main`**; kiểm tra G6/G8; thu minh chứng | CD9 |
| 12 | Chỉ hotfix | |

**Phụ thuộc vào kế hoạch BE/FE (không sửa chúng ở đây):** BE P1.1 (`.gitignore`), P1.2 (ENV fail-fast), P1.x (lint/strict) nên xong **trước** CD2 BE; BE test tối thiểu (P2/P8) để CI không chạy "0 test"; FE9.3 (Dockerfile) được gộp vào CD4.3; PX/health nằm ở CD7.1. Các file dễ xung đột: `package.json`, `main.ts`, `app.module.ts` — mỗi lần chỉ một nhánh sửa.

---

## 7. Kế hoạch triển khai chi tiết (cho AI Agent)

Quy ước: **Loại** 🤖 Agent · 👤 Người · ⛔ Cổng · `∥` song song. **Xác minh** = điều phải đúng trước khi đánh ✅. "BE"/"FE"/"DOCS" = repo.

### CD0 — Cổng vào (tuần tự)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD0.1 | ⛔ Bạn điền Mục 5.1 | 👤 | Mục 5.1 có nội dung |
| CD0.2 | Hỏi GVHD 4 câu ở Mục 5; ghi câu trả lời vào tracking | 👤 | Có trả lời bằng văn bản (email/ghi chú) |
| CD0.3 | Xác minh tiền đề: (a) server — SSH được không, `docker`/`docker compose` bản nào, RAM trống (`free -m`), disk; (b) tên miền; (c) gói miễn phí GitHub Actions/GHCR/ruleset cho repo public, SonarCloud, dịch vụ log/monitor đã chọn | 🤖+👤 | Ghi kết quả **thật** vào tracking; mục nào không kiểm được ⇒ "chưa kiểm chứng" |
| CD0.4 | Tạo `0.docs/tracking/feature-plans/ci-cd.md` từ `_template.md`; thêm dòng `DECISIONS_LOG` (số kế tiếp, **không** sửa dòng cũ) cho mỗi Q-CD đã chốt | 🤖 | File tồn tại; mỗi Q có đúng 1 dòng hoặc gộp có chủ đề |
| CD0.5 | Đối chiếu bảng metric Mục 0 với rubric gốc một lần nữa; lập bảng "bằng chứng cần thu" (Mục 8) | 🤖 | Bảng khớp rubric Mục 5 và 8 |

### CD1 — Repo, devkit chạy thật (tiền đề; thực hiện theo `ke-hoach-tao-repo.md` bước 4–10)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD1.1 | Tạo GitHub Org (bật 2FA), 3 repo; mời GVHD quyền Read | 👤 | Org/repo tồn tại; quyền hội đồng kiểm được |
| CD1.2 | **Quét gitleaks toàn bộ cây thư mục BE/FE/DOCS trước `git add`** (đặc biệt `.env` của BE); BE: tạo `.gitignore` (P1.1) trước | 🤖 | `gitleaks detect --no-git` = 0 phát hiện thật; ghi báo cáo |
| CD1.3 | `git init -b main`, `devkit/install.sh` cho từng repo, commit khởi tạo **tối thiểu**; Agent **chỉ đưa lệnh**, bạn chạy (không tự commit/push) | 👤 | `git log` có commit đầu; hook hoạt động (`bash devkit/tests/test-hooks.sh` xanh) |
| CD1.4 | Đẩy `main`+`develop` (`DEVKIT_BOOTSTRAP=1`), mở 1 PR thử để `devkit-checks` chạy lần đầu trên GitHub, rồi `apply-rulesets.sh` | 👤 | Ruleset hiển thị trong Settings; PR sai quy ước bị chặn |
| CD1.5 | Bật secret scanning + push protection, Dependabot (alerts + version updates), `GITHUB_TOKEN` mặc định read-only | 👤 | Ảnh chụp Settings |
| CD1.6 | Cài `actionlint` cục bộ; thêm vào `local-checks.sh` kiểm các file workflow | 🤖 | Workflow lỗi cú pháp bị hook chặn |

### CD2 — CI chặng 1–3: build, lint/static, test (sau CD1; BE ∥ FE)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD2.1 | FE `ci.yml`: `npm ci` (cache), `lint`, `typecheck`, `format:check`, `build` (với `API_BASE_URL` giả) | 🤖 | Chạy xanh trên nhánh thử; thời gian ghi vào tracking |
| CD2.2 | FE: `test:cov` (Vitest), đẩy coverage làm artifact + tóm tắt vào job summary | 🤖 | Artifact có; số coverage là số thật |
| CD2.3 | BE `ci.yml`: `npm ci`, `lint` (oxlint), `build`; `prisma validate` | 🤖 | Xanh |
| CD2.4 | BE: unit test + coverage (artifact). Nếu 0 test ⇒ **không** dùng `--passWithNoTests` để che; chờ test tối thiểu (BE P2) rồi mới đưa vào required | 🤖 | Không có bước test "giả" xanh |
| CD2.5 | BE: integration test với `services: postgres, redis`; chạy `prisma migrate deploy` + kiểm drift (`migrate diff --exit-code`, khớp BE P7.4) | 🤖 | Xanh trên DB rỗng |
| CD2.6 | `concurrency` hủy run cũ cùng nhánh; `timeout-minutes` mỗi job; `permissions:` tối thiểu | 🤖 | Xem `actionlint` |
| CD2.7 | Đặt `needs:` đúng thứ tự để tạo **một** workflow nối chặng (cho ảnh chụp pipeline) | 🤖 | Đồ thị Actions hiển thị đủ chặng |
| CD2.8 | Thử workflow trên nhánh `chore/ci-*` + PR nháp; sửa đến khi ổn rồi mới thêm vào required | 🤖+👤 | Ghi số run đỏ/xanh trong giai đoạn thử |
| CD2.9 | Thêm `lint`, `typecheck`, `test`, `build` vào required checks của ruleset (`protect-develop`, `protect-main`) theo Q-CD9 | 👤 | Ruleset cập nhật (`apply-rulesets.sh`) |

### CD3 — Chặng bảo mật và chất lượng (`∥` với CD4)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD3.1 | gitleaks **toàn lịch sử** trong CI (artifact báo cáo); đã có `secret-scan` của devkit — thống nhất để không chạy trùng | 🤖 | Báo cáo 0 secret |
| CD3.2 | `npm audit --omit=dev --audit-level=high` làm chặng bắt buộc; devDependencies: ghi nhận, xử lý theo kế hoạch (FE hiện còn cảnh báo ở devDependencies) | 🤖 | Quy tắc rõ trong workflow; ngoại lệ có ghi chép |
| CD3.3 | `actions/dependency-review-action` trên PR | 🤖 | Chạy trên PR có đổi `package.json` |
| CD3.4 | CodeQL (JavaScript/TypeScript) hàng tuần + trên PR | 🤖 | Có kết quả trong tab Security |
| CD3.5 | SonarCloud (Q-CD6): tạo project, cấu hình loại trừ (`components/ui/**`, migrations, `dist`, file test khỏi tính duplication nếu hợp lý), Quality Gate; **chưa required** cho tới khi xanh 2 tuần liên tiếp | 🤖+👤 | Dashboard hiện coverage + duplication; ghi cấu hình loại trừ vào README |
| CD3.6 | Trivy quét image (sau CD4) — fail ở mức HIGH/CRITICAL có bản vá | 🤖 | Báo cáo đính kèm |
| CD3.7 | Hạ ngưỡng nợ kỹ thuật: file `TECH_DEBT.md` + label `tech-debt`; mỗi cảnh báo được hoãn phải có dòng | 🤖 | File tồn tại, mỗi dòng có kế hoạch xử lý |

### CD4 — Đóng gói Docker (`∥` CD3)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD4.1 | BE `Dockerfile` đa giai đoạn (build → runtime mỏng, user không root, `HEALTHCHECK`), `.dockerignore` | 🤖 | `docker build` chạy; image chạy với env giả |
| CD4.2 | BE: bước `prisma migrate deploy` chạy bằng container tạm trước khi khởi động app (không trong `CMD` chính) | 🤖 | Tài liệu hóa trong README |
| CD4.3 | FE `Dockerfile` dựa `output: "standalone"` (gộp FE9.3), `HEALTHCHECK`, `.dockerignore` | 🤖 | Image chạy, `/` trả 200 |
| CD4.4 | Workflow `package`: `docker/build-push-action` + cache GHA; tag `sha-<7>`, `develop`, và `vX.Y.Z` khi tag; đẩy GHCR (Q-CD8) | 🤖 | Image xuất hiện trong GHCR; tag đúng |
| CD4.5 | Kiểm kích thước image và thời gian build; ghi vào tracking | 🤖 | Số thật |
| CD4.6 | Chỉ job chạy trên `develop`/`main` mới có quyền `packages: write` | 🤖 | `permissions` đúng |
| CD4.7 | **Smoke test trong runner:** dựng tạm BE+FE+Postgres+Redis bằng `docker compose` (image vừa build), chờ `healthy`, gọi `/health`, `/ready` và trang chủ FE, rồi hủy; job đỏ nếu lỗi | 🤖 | Chạy xanh; cố ý làm hỏng một lần để thấy đỏ |

### CD5 — Hạ tầng staging (`∥` sau CD0; làm trước CD6)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD5.1 | Chuẩn bị server: user `deploy` (không root, chỉ quyền docker), khóa SSH riêng cho CI, tắt đăng nhập mật khẩu, tường lửa chỉ mở 22/80/443 | 👤 (+Agent soạn lệnh) | Kiểm bằng `ss -tlnp` và thử đăng nhập |
| CD5.2 | `docker-compose.yml` (vị trí theo Q-CD2b): nginx, frontend, backend, redis, (postgres theo Q-CD4); `restart: unless-stopped`, giới hạn bộ nhớ từng service, log rotation `json-file` (`max-size`, `max-file`) | 🤖 | `docker compose config` hợp lệ; `docker stats` đo RAM thật khi chạy (không đoán) |
| CD5.3 | `nginx.conf`: reverse proxy `/api/` → backend, `/` → frontend, header bảo mật; HTTPS bằng Let's Encrypt (Q-CD5) | 🤖+👤 | `curl -I https://...` 200; chứng chỉ hợp lệ |
| CD5.4 | File `.env` runtime trên server (quyền 600, **ngoài repo**); danh sách biến ghi ở `.env.example` | 👤 | Không có secret trong repo (gitleaks) |
| CD5.5 | Sao lưu DB (Q-CD11): cron `pg_dump`, giữ 7 bản, kiểm khôi phục thử một lần | 🤖+👤 | Khôi phục thử thành công |
| CD5.6 | Đo RAM/CPU thật khi chạy đủ stack; nếu thiếu ⇒ **dừng hỏi** (đổi Q-CD1/Q-CD4) | 🤖 | Ghi `free -m` + `docker stats` vào tracking |
| CD5.7 | **Nhắc gia hạn chứng chỉ** (theo #74): cấp lần đầu bằng DNS-01 thủ công; đặt lịch nhắc ở ngày 60, ghi hạn chứng chỉ vào runbook; thêm kiểm hạn chứng chỉ trong monitor (nếu dịch vụ hỗ trợ) hoặc job `cert-expiry` cảnh báo khi còn < 20 ngày | 🤖+👤 | Lệnh `openssl s_client` cho ra ngày hết hạn; cảnh báo thử hoạt động |

### CD6 — Triển khai tự động (sau CD4, CD5)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD6.1 | Secret của Environment `staging` (SSH key, host, user); không in ra log | 👤 | Settings → Environments |
| CD6.2 | Workflow `deploy`: kích hoạt sau `package` thành công trên `develop`; `environment: staging` (để GitHub ghi **Deployments**); `concurrency` không chạy hai deploy song song | 🤖 | Deployment hiện trong tab Deployments |
| CD6.3 | Bước deploy: SSH → `docker compose pull <service>` → chạy migration (CD4.2) → `up -d <service>` | 🤖 | Chạy được trên staging thật |
| CD6.4 | **Smoke test** sau deploy: gọi `/health`, `/ready`, trang chủ FE, một luồng đọc; fail ⇒ job đỏ | 🤖 | Cố ý làm hỏng 1 lần để thấy job đỏ |
| CD6.5 | **Rollback tự động**: smoke fail ⇒ deploy lại tag trước (lưu trong file trạng thái trên server) | 🤖 | Diễn tập: deploy bản hỏng ⇒ tự quay lại |
| CD6.6 | Workflow `rollback` (`workflow_dispatch`, nhập tag) + tài liệu cách dùng | 🤖 | Diễn tập một lần, ghi thời gian |
| CD6.7 | Tag `vX.Y.Z` trên `main` ⇒ tạo GitHub Release với ghi chú; image tag tương ứng | 🤖 | Release xuất hiện |
| CD6.8 | **Mốc then chốt:** deploy tự động lần đầu (BE `/health` + FE trang chủ) — mục tiêu **cuối Tuần 5** | 🤖+👤 | Deployment đầu tiên xanh; ảnh chụp |
| CD6.9 | Thông báo kết quả deploy/pipeline fail qua webhook (Q-CD7) | 🤖 | Nhận được tin báo thử |
| CD6.10 | Job `deploy` có điều kiện `if: vars.DEPLOY_ENABLED == 'true'` (mặc định bỏ qua; **không** ghi Deployment khi bỏ qua); bật khi có server | 🤖 | Run hiện job "skipped", không phải "success" |

### CD7 — Giám sát và vận hành
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD7.1 | **BE:** endpoint `GET /health` (liveness) và `GET /ready` (kiểm DB + Redis, ví dụ `@nestjs/terminus`) — ngoài prefix hoặc không cần JWT, không lộ thông tin nhạy cảm; test | 🤖 | Test; không trả chi tiết lỗi nội bộ |
| CD7.2 | **FE:** `GET /api/health` (Route Handler) | 🤖 | Test |
| CD7.3 | Monitor ngoài ping `/health` mỗi vài phút + cảnh báo email/Discord/Telegram (Q-CD7) | 👤 (+Agent soạn hướng dẫn) | Gây lỗi có chủ đích ⇒ nhận cảnh báo |
| CD7.4 | Log tập trung: shipper nhẹ (RAM thấp) từ Docker lên dịch vụ log đã chọn; log có `requestId`, **không** ghi token/mật khẩu/đáp án | 🤖+👤 | Tìm được log của một request thử |
| CD7.5 | Cảnh báo khi: dịch vụ down, tỉ lệ lỗi 5xx tăng, disk > ngưỡng, backup thất bại | 🤖+👤 | Ghi quy tắc cảnh báo; thử kích hoạt ≥ 1 quy tắc |
| CD7.6 | Runbook ngắn (`RUNBOOK.md` hoặc mục trong README): triển khai, rollback, đọc log, khôi phục DB | 🤖 | Một người khác làm theo được |

### CD8 — Đo, tối ưu, kiểm thử pipeline
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD8.1 | Đo thời gian commit → staging (từ thời điểm push `develop` tới smoke xanh) **5 lần**; ghi trung bình, lớn nhất | 🤖 | Số thật từ log Actions |
| CD8.2 | Tối ưu nếu > 15 phút: cache, chạy song song, bỏ bước thừa, `--frozen-lockfile`-tương đương | 🤖 | Đo lại |
| CD8.3 | Script `scripts/ci-metrics` (mỗi repo, `gh run list --json` + `gh api .../deployments`) tính: tỉ lệ run xanh, số deploy, thời gian trung bình | 🤖 | Chạy ra số; khớp với giao diện GitHub |
| CD8.4 | Script đếm "tuần có commit" và tỉ lệ PR có review từ `git log`/`gh pr list` | 🤖 | Số thật |
| CD8.5 | **Diễn tập vi phạm:** PR chứa secret giả, PR sai tên nhánh, PR làm hỏng test ⇒ phải bị chặn | 🤖+👤 | Ảnh chụp chặn |
| CD8.6 | Chính sách flaky: test bất ổn bị cách ly có ghi chép, **không** `retry` che lỗi thật | 🤖 | Danh sách flaky (có thể rỗng) |
| CD8.7 | E2E Playwright chạy trong CI (mock) và smoke trên staging; chuyển thành required khi ổn định (Q-CD9) | 🤖 | Xanh ≥ 2 tuần liên tiếp mới nâng |
| CD8.8 | Kiểm tải nhẹ (k6) trên staging theo SRS 15.1 (ghi môi trường đo; không so với "100 user" nếu hạ tầng không tương đương) | 🤖 | Báo cáo kèm điều kiện đo |

### CD9 — Khép sổ và minh chứng (bắt buộc theo `rubric-tracker`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| CD9.1 | `AI_USAGE_LOG.md` **sau mỗi phiên** có AI sinh/sửa workflow/Dockerfile/cấu hình | 🤖 | Có dòng mới |
| CD9.2 | `weekly-log/Tuan-XX.md`: ghi mọi thay đổi thiết kế hạ tầng và lý do (TC2.1) | 🤖 | File cập nhật |
| CD9.3 | README BE/FE/DOCS: cài đặt, chạy, test, biến môi trường, **sơ đồ triển khai** (Mục 3), cách rollback | 🤖 | Người ngoài build được từ README (G8) |
| CD9.4 | `CODING_CONVENTION.md` đã công bố; `TECH_DEBT.md` cập nhật | 🤖 | File có |
| CD9.5 | **Đóng băng `main` từ Tuần 11:** chỉ hotfix; chạy lại toàn bộ pipeline lần cuối | 👤 | Lần chạy cuối xanh 100% |
| CD9.6 | Gói minh chứng (Mục 8): ảnh chụp pipeline, lịch sử run, Deployments, báo cáo coverage/Sonar/gitleaks, cấu hình health/log/alert | 🤖+👤 | Đủ 100% mục Mục 8 |
| CD9.7 | Cập nhật `TRACKING.md` **chỉ bằng số đo thật** hoặc N/A | 🤖 | Không số bịa |
| CD9.8 | Nhắc bạn cấp quyền Read repo cho hội đồng; kiểm checkout sạch → `npm ci && npm run build` xanh | 👤 | Ghi lại lệnh và kết quả |

**Tổng: CD0 5 · CD1 6 · CD2 9 · CD3 7 · CD4 7 · CD5 7 · CD6 10 · CD7 6 · CD8 8 · CD9 8 = 73 task; toàn bộ 73 task được mở (17 task phụ thuộc server từng bị hoãn nay đã mở lại, vẫn cần CD0.3 xác minh server trước).**

---

## 8. Gói minh chứng cần thu và cách đo (không bịa số)

| Tiêu chí | Minh chứng (theo Mục 8 rubric) | Cách lấy |
|---|---|---|
| TC2.6 chặng | Tệp cấu hình pipeline; ảnh đồ thị Actions đủ chặng | `.github/workflows/*.yml` + ảnh chụp |
| TC2.6 build xanh | Lịch sử run | `gh run list --json conclusion,createdAt,event,headBranch` → script CD8.3 |
| TC2.6 deploy | Lịch sử deploy | `gh api repos/<org>/<repo>/deployments` (do dùng `environment`) |
| TC2.6 thời gian | Log pipeline | Chênh lệch `createdAt` → smoke xanh (CD8.1) |
| TC2.6 giám sát | Cấu hình health/log/alert + ảnh cảnh báo thật | Ảnh monitor, ảnh nhận cảnh báo, ảnh log |
| TC2.4 lint/static | Báo cáo linter + Sonar/CodeQL | Artifact CI |
| TC2.4 secret | Báo cáo gitleaks (toàn lịch sử) | Artifact CI |
| TC2.4 git | Tỉ lệ tuần có commit, PR có review | Script CD8.4 |
| TC2.5 | Coverage report, % test pass ở run cuối, danh sách defect | Artifact CI + bug tracker (GitHub Issues) |
| G8 | Link repo + quyền hội đồng + build sạch | CD9.8 |

---

## 9. Hướng dẫn dành cho AI Agent thực thi kế hoạch này

### 9.1. Quy tắc bất biến
1. Chỉ làm khi Mục 5.1 có phản hồi. Làm đúng nội dung đã duyệt, **không thêm công cụ ngoài danh sách** (ví dụ thêm SonarCloud khi Q-CD6 chọn B).
2. **Không bao giờ** đặt secret/khóa/IP nhạy cảm vào repo, workflow, compose hay log. Không in secret ra log Actions. Dùng GitHub Environments và `.env` trên server.
3. Với repo public: chỉ `pull_request`; không `pull_request_target`; không self-hosted runner; `permissions` tối thiểu; ghim action theo SHA/tag chính thức.
4. **Không tự `git init`/commit/push/tạo PR/áp ruleset** (bộ nhớ dự án): Agent soạn nội dung và đưa lệnh cho bạn chạy. Không ký `COMMITMENT_BASELINE.md`; không sửa `.docx` SRS.
5. **Không tạo commit lùi ngày hoặc commit rỗng** để tăng số tuần có commit. **Không tắt/bỏ qua** bước test, lint hay quét để làm xanh pipeline; không `continue-on-error` che lỗi thật; không `--passWithNoTests`/`retry` che lỗi (CD2.4, CD8.6).
6. Không bịa số liệu (thời gian pipeline, % xanh, coverage, RAM). Chưa đo ⇒ "N/A". Mọi con số phải có lệnh/đường dẫn gốc.
7. Không chạy lệnh phá hoại trên server (`rm -rf`, `docker system prune -a`, đổi tường lửa) khi chưa được bạn đồng ý; chỉ thao tác server qua kênh bạn cấp.
8. Ngôn ngữ: tài liệu/tracking tiếng Việt; tên file, định danh, workflow tiếng Anh.
9. Sau **mỗi** phiên: `AI_USAGE_LOG.md` (CD9.1).

### 9.2. Thứ tự đọc (CD0)
`CLAUDE.md` → `HUONG_DAN_RUBRIC_VA_TRACKING.md` → **kế hoạch này** → `ke-hoach-tao-repo.md` → `docs-repo/devkit/README.md` + `devkit-checks.yml` → `DECISIONS_LOG.md` (#34, #36, #37, #39, #49–#64) → rubric Mục 4 (TC2.4–2.6), Mục 5, 7, 8 → `ai-llm-gateway.md`.

### 9.3. Điều kiện phải DỪNG và hỏi (`AskUserQuestion`, ≥2 phương án + đánh đổi)
- Ô Q-CD còn trống mà task cần.
- Server không đủ RAM/disk hoặc không SSH được (CD0.3, CD5.6).
- Gói miễn phí của một dịch vụ không đủ (Actions, GHCR, Sonar, log/monitor) ⇒ phương án thay thế.
- Muốn thêm công cụ/dịch vụ ngoài danh sách, hoặc dịch vụ trả phí.
- Cần đổi `ruleset` ngoài việc thêm required checks.
- Cần đổi schema/migration để rollback an toàn (Q-CD10).
- Lỗi 🔴 mới ở BE/FE khi bật CI (chuyển sang "Phát hiện mới" trong tracking, không tự sửa ngoài phạm vi).
- **Mọi** lựa chọn ảnh hưởng khả năng mở rộng/bảo trì mà kế hoạch này không quy định.

### 9.4. Cách cập nhật file theo dõi
Như kế hoạch BE/FE: ô trạng thái ⬜→🔄→✅ (**chỉ ✅ khi đã chạy bước Xác minh**), cột "Bằng chứng" (lệnh + kết quả tóm tắt, không dán token), tính lại %, thêm dòng "Nhật ký cập nhật" (append-only), 🚫 khi bị chặn và **không** chuyển sang task phụ thuộc. File dễ xung đột giữa các nhánh: `.github/workflows/*`, `Dockerfile`, `docker-compose.yml`, `package.json`.

### 9.5. Định nghĩa "xong" (DoD)
- [ ] Pipeline có ≥ 6 chặng, chạy đủ trên `develop`; ≥ 10 deploy tự động ghi trong Deployments, trải theo tuần.
- [ ] Tỉ lệ run xanh, thời gian commit→staging, số deploy: **đo bằng script**, kết quả ghi trong tracking.
- [ ] Health + log tập trung + cảnh báo có ảnh chứng minh đã kích hoạt thật; rollback đã diễn tập.
- [ ] 0 secret (gitleaks toàn lịch sử), 0 lỗi lint, Sonar/CodeQL không còn Blocker/Critical, trùng lặp ≤ 3% *hoặc* số thật kèm kế hoạch.
- [ ] Lần chạy CI cuối trên `main` xanh 100%; coverage và số tầng test là số đo thật.
- [ ] README + sơ đồ triển khai + `TECH_DEBT.md` + `CODING_CONVENTION.md`; checkout sạch build được; hội đồng có quyền truy cập.
- [ ] `DECISIONS_LOG`, `AI_USAGE_LOG`, `weekly-log`, `feature-plans/ci-cd.md` đã cập nhật.

### 9.6. Lệnh tham chiếu (PowerShell/Git Bash; kiểm tên thực tế trước khi chạy)
```bash
gitleaks detect --no-git --redact --report-path gitleaks-report.json     # trước khi git add
actionlint                                                                 # kiểm file workflow
gh run list --limit 50 --json conclusion,createdAt,event,headBranch
gh api repos/<org>/<repo>/deployments
docker compose config ; docker stats --no-stream ; free -m
```

---

## 10. Rủi ro và câu hỏi mở (Agent **không** tự trả lời)

- **Số tuần có commit** có thể không đạt Mức 5 bất kể làm tốt đến đâu (xem Mục 0). Chỉ GVHD trả lời được cách đếm.
- **RAM server:** nếu Q-CD4 = A (Postgres trong compose) và có thêm LiteLLM, 2 GB gần như chắc chắn thiếu; phải đo (CD5.6) trước khi cam kết.
- **Gói miễn phí:** SonarCloud, log/monitor hosted, ruleset gói Free cho repo public — chưa kiểm chứng; có thể buộc đổi phương án giữa chừng.
- **Tỉ lệ xanh khi mới khởi động CI:** số run ít ⇒ vài lần đỏ ban đầu gây ảnh hưởng lớn; Khoa có thể không tính run trên nhánh thử — chưa biết.
- **Dữ liệu CLOTH/giấy phép (#26) và AI bên ngoài:** staging công khai không được chứa nội dung chưa rõ giấy phép; gửi dữ liệu tới nhà cung cấp AI ngoài còn phụ thuộc câu 6 của `ai-llm-gateway.md`.
- **Backend hiện còn nhiều lỗi 🔴** (kế hoạch BE): bật Quality Gate/required test quá sớm sẽ làm pipeline đỏ liên tục; nên đồng bộ thứ tự với BE P1–P2.
- **Bảo trì sau bảo vệ:** staging chạy trên server nhóm cần có người chịu trách nhiệm; chưa ai được giao.
