# Phương án quản lý Git và CI/CD

> **Trạng thái:** ĐỀ XUẤT, các mục đánh dấu **[CHỜ QUYẾT ĐỊNH]** chưa được nhóm chốt. Theo quy tắc #1 của dự án, không tự chọn thay; chốt xong thì ghi vào `tracking/DECISIONS_LOG.md` (lưu máy) và tạo `tracking/feature-plans/ci-cd-pipeline.md`.
> **Mốc thời gian:** soạn ngày 2026-10-02 (Tuần 3/12). Còn khoảng 9 tuần để tích lũy số liệu.
> **Đối chiếu rubric:** TC2.4 (Git, chất lượng mã, secret), TC2.6 (CI/CD). Chỉ tiêu cụ thể nằm ở Mục 1.

---

## 1. Chỉ tiêu rubric cần đạt

### 1.1 Git và chất lượng mã (TC2.4)

| Chỉ tiêu | Mức 5 |
|---|---|
| Lỗi lint / 1000 dòng | 0 |
| Issue Blocker/Critical (phân tích tĩnh) | 0 |
| Tỉ lệ mã trùng lặp | ≤ 3% |
| Tỉ lệ tuần có commit | ≥ 90% |
| Tỉ lệ thay đổi qua PR có review | ≥ 90% |
| Secret lộ trong repo | 0 |
| Danh mục nợ kỹ thuật kèm kế hoạch xử lý | Có |

### 1.2 CI/CD (TC2.6)

- Pipeline có ≥ 6 chặng: build, lint/phân tích tĩnh, test, quét bảo mật/phụ thuộc, đóng gói Docker, triển khai tự động.
- Tỉ lệ build xanh ≥ 90%.
- ≥ 10 lần triển khai tự động trong kỳ, trải đều theo tiến độ.
- Thời gian từ commit đến staging ≤ 15 phút.
- Secret quản lý qua cơ chế của nền tảng; có đánh phiên bản và khả năng rollback.
- Có giám sát sau triển khai: health check, log tập trung, cảnh báo (alert).

---

## 2. Quản lý Git

### 2.1 Hiện trạng (đã có trong `devkit/`, Quyết định #36)

Không xây lại, chỉ áp dụng cho cả 3 repo (`docs`, `backend`, `frontend`).

```
feat|fix|docs|chore|test|refactor/<ten-chuc-nang> ──PR (squash)──▶ develop ──PR (merge commit)──▶ main
hotfix/<ten> ──PR (merge commit)──▶ main   (sau đó merge ngược main vào develop)
```

| Lớp | Chạy ở | Vai trò |
|---|---|---|
| Git hook (`.githooks/`) | Máy thành viên | Phát hiện sớm: commit thẳng vào `main`/`develop`, tên nhánh sai, commit message sai, `.env`, file > 5 MB, secret |
| CI + ruleset (`.github/`) | GitHub | Chặn thật khi merge: tên nhánh, tiêu đề PR, checklist PR, secret, đủ 1 approval |

Chỉ lớp CI + ruleset đảm bảo chỉ tiêu "≥ 90% thay đổi qua PR có review". Hook có thể bị bỏ qua bằng `--no-verify`.

### 2.2 Quy tắc làm việc hằng ngày

1. Mỗi việc là một nhánh `loại/ten-viet-thuong-gach-ngang` tách từ `develop`.
2. Commit theo Conventional Commits: `loại(phạm-vi): mô tả` (mô tả ≥ 10 ký tự, tiêu đề ≤ 72 ký tự, không dùng "update", "fix bug").
3. Mở PR vào `develop`, điền đủ checklist (mục không áp dụng thì tick và ghi `N/A: lý do`), người còn lại review. **Review chéo 100%** vì nhóm 2 người.
4. Merge squash vào `develop`; tích lũy xong một cột mốc thì PR merge commit từ `develop` vào `main`.
5. Mỗi thành viên có commit thực chất ít nhất 1 lần mỗi tuần, kể cả tuần chỉ làm tài liệu.
6. Không commit `.env` thật; chỉ `.env.example`.

### 2.3 Bằng chứng cho hội đồng

| Chỉ tiêu | Nguồn bằng chứng |
|---|---|
| Tuần có commit | `git log` theo tuần, ảnh chụp Insights của GitHub |
| PR có review | Danh sách PR đã merge kèm approval |
| Secret = 0 | Kết quả `gitleaks` trong CI |
| Nợ kỹ thuật | Issue label `tech-debt` (template `.github/ISSUE_TEMPLATE/tech-debt.md`) |

### 2.4 Việc còn thiếu **[CHỜ QUYẾT ĐỊNH]**

- Cấu trúc repo: **monorepo** hay **tách backend/frontend**. Xem Mục 4.3.
- Có dùng `CODEOWNERS` để tự gán reviewer không (nhóm 2 người, lợi ích nhỏ).

---

## 3. Kiến trúc pipeline CI/CD

### 3.1 Sáu chặng

| # | Chặng | Việc làm | Công cụ đề xuất | Điều kiện đạt |
|---|---|---|---|---|
| 1 | Build | `npm ci`, `nest build`, `next build` | GitHub Actions, cache npm | Build không lỗi |
| 2 | Lint/phân tích tĩnh | ESLint, Prettier check, phân tích Sonar | ESLint, SonarCloud | 0 Blocker/Critical, trùng lặp ≤ 3% |
| 3 | Test | Unit test, đo coverage | Jest | Test pass; `cat-engine` có ≥ 3 case bắt buộc |
| 4 | Quét bảo mật/phụ thuộc | Secret, thư viện lỗi thời, lỗ hổng image | gitleaks (đã có), `npm audit` hoặc Dependabot, Trivy | Không có lỗ hổng mức cao chưa xử lý |
| 5 | Đóng gói | Build Docker image, gắn tag | Docker multi-stage, GHCR | Image build được, gắn tag version và SHA |
| 6 | Triển khai tự động | Deploy staging, chạy smoke test | GitHub Actions + SSH/API nền tảng | `/health` trả OK sau deploy |

Mỗi chặng là một job riêng để báo cáo hiển thị đủ 6 chặng.

### 3.2 Luồng kích hoạt

| Sự kiện | Chạy |
|---|---|
| Mở/cập nhật PR | Chặng 1 đến 4 (chặn merge nếu đỏ) |
| Merge vào `develop` | Chặng 1 đến 6, deploy **staging** |
| Merge vào `main` hoặc tag `vX.Y.Z` | Đóng gói bản phát hành, gắn version |
| Chạy tay (`workflow_dispatch`) | Rollback về tag cũ |

### 3.3 Ngân sách thời gian (mục tiêu commit đến staging ≤ 15 phút)

| Chặng | Ngân sách |
|---|---|
| Build | 3 phút |
| Lint + Test + Quét (chạy song song) | 4 phút |
| Đóng gói | 3 phút |
| Deploy + smoke test | 2 phút |
| **Tổng** | **≈ 12 phút** (dư 3 phút) |

Giữ dưới ngưỡng bằng: chạy song song, cache npm và Docker layer, multi-stage build. Dịch vụ calibration (py-irt/catR) chạy offline, **không** nằm trong pipeline chính, build riêng.

Các con số trên là ngân sách ước tính, **phải đo lại** bằng lần chạy thật rồi ghi vào `TRACKING.md`, không điền số bịa.

---

## 4. Quyết định cần chốt

### 4.1 Nơi chạy staging **[CHỜ QUYẾT ĐỊNH]**

| Phương án | Ưu | Nhược |
|---|---|---|
| **A1. VPS + Docker Compose** (Nginx, NestJS, Next, Postgres, Redis) | Khớp stack đã chốt (Nginx gateway), chủ động, rẻ | Tự vá, tự bảo mật server; tốn công setup |
| **A2. PaaS** (Render/Railway/Fly.io) | Setup nhanh, có sẵn log, secret, rollback | Tốn phí khi có DB và Redis; Nginx và sidecar kém tự nhiên |
| **A3. Cloud Run + Cloud SQL** | Gần thực tế doanh nghiệp, rollback theo revision | Cấu hình phức tạp, dễ vượt ngân sách |

Nghiêng về A1 nếu có VPS rẻ hoặc credit sinh viên; A2 nếu cần nhanh và ít kinh nghiệm DevOps.

### 4.2 Log và giám sát **[CHỜ QUYẾT ĐỊNH]**

| Phương án | Ưu | Nhược |
|---|---|---|
| **B1. Loki + Grafana tự dựng** | Đủ log tập trung, dashboard, alert; miễn phí | Tốn RAM VPS, tốn công cấu hình |
| **B2. SaaS** (Better Stack, Grafana Cloud free) | Setup nhanh, free tier đủ | Phụ thuộc dịch vụ ngoài |

### 4.3 Cấu trúc repo **[CHỜ QUYẾT ĐỊNH]**

| Phương án | Ưu | Nhược |
|---|---|---|
| **C1. Monorepo** | Một pipeline, một bộ hook, dễ theo dõi | Pipeline lớn hơn, cần lọc theo thư mục |
| **C2. Tách backend/frontend** | Pipeline đơn giản mỗi repo, đúng cách `devkit` đang giả định (3 repo) | Dựng CI 2 lần, số liệu rải 2 nơi |

### 4.4 Công cụ phân tích tĩnh **[CHỜ QUYẾT ĐỊNH]**

| Phương án | Ưu | Nhược |
|---|---|---|
| **D1. SonarCloud** | Đo cả Blocker/Critical lẫn trùng lặp, có dashboard làm bằng chứng | Cần tài khoản và token, repo public mới miễn phí |
| **D2. CodeQL + `jscpd`** | Chạy ngay trên GitHub, không cần dịch vụ ngoài | Hai công cụ riêng, báo cáo trùng lặp kém trực quan |

---

## 5. Triển khai, secret, phiên bản, rollback

- **Secret:** GitHub Environments/Secrets cho CI; biến môi trường của nền tảng cho runtime. Không hardcode, chỉ commit `.env.example`. Khóa API Gemini và thông tin DB thuộc nhóm này.
- **Phiên bản:** semver `v0.x.y` (tag Git). Image Docker gắn hai tag: `v0.x.y` và `sha-<7 ký tự>`.
- **Rollback:** workflow `rollback` nhận tag cũ làm tham số rồi deploy lại image đó. **Diễn tập ít nhất một lần và lưu bằng chứng** (ảnh chụp, log chạy).
- **Môi trường:** tối thiểu `staging`. `production` chỉ thêm nếu còn thời gian, không bắt buộc cho rubric.

## 6. Giám sát sau triển khai

| Hạng mục | Cách làm |
|---|---|
| Health check | Endpoint `/health` (NestJS Terminus, kiểm tra Postgres và Redis); chặng 6 gọi và fail nếu không OK |
| Log tập trung | Log JSON ra stdout, gom về một nơi theo Mục 4.2 |
| Alert | Uptime check ngoài mỗi 5 phút, gửi Telegram hoặc Discord khi down hoặc health lỗi |

---

## 7. Chỉ tiêu CI/CD và cách đo

| Chỉ tiêu | Cách đáp ứng | Cách đo |
|---|---|---|
| Build xanh ≥ 90% | Ruleset chặn merge khi CI đỏ; hook `pre-push` chạy lint/test cục bộ | Tỉ lệ run thành công trên `develop` và `main` từ lịch sử Actions |
| ≥ 10 lần deploy, trải đều | Mỗi PR squash vào `develop` là một lần deploy; mục tiêu 12 đến 14 lần, ≥ 1 lần mỗi tuần từ Tuần 4 | Lịch sử GitHub Deployments |
| Commit đến staging ≤ 15 phút | Mục 3.3 | Thời gian chạy workflow, ghi vài lần đại diện |
| Secret, phiên bản, rollback | Mục 5 | Ảnh chụp cấu hình, danh sách tag, log rollback |
| Giám sát | Mục 6 | Ảnh chụp dashboard và alert thử nghiệm |

---

## 8. Lộ trình theo tuần

| Tuần | Mốc | Sản phẩm |
|---|---|---|
| 3 đến 4 | Chốt Mục 4; tạo repo code, skeleton NestJS có `/health`; dựng pipeline 6 chặng; deploy staging lần đầu | Pipeline chạy xanh, lần deploy #1 |
| 5 đến 6 | Thêm ESLint, Sonar, Jest vào CI; log JSON; uptime alert | ≥ 4 lần deploy lũy kế |
| 7 | Diễn tập rollback; đo thời gian pipeline | Bằng chứng rollback, số liệu ≤ 15 phút |
| 8 đến 11 | Giữ nhịp deploy; theo dõi tỉ lệ build xanh; xử lý nợ kỹ thuật | ≥ 1 deploy mỗi tuần |
| 12 | Chốt số liệu và bằng chứng cho báo cáo | `TRACKING.md` cập nhật số đo thật |

**Mốc kiểm soát:** hết Tuần 6 phải có ≥ 4 lần deploy. Nếu chưa, coi là tín hiệu đỏ và họp điều chỉnh. Tiêu chí "trải đều" không thể bù vào cuối kỳ.

## 9. Rủi ro

| Rủi ro | Cách giảm |
|---|---|
| Có code muộn nên thiếu số lần deploy | Deploy skeleton ngay khi có code đầu tiên |
| Vài lần build đỏ kéo tỉ lệ dưới 90% | PR nhỏ, ruleset chặn merge khi đỏ, hook `pre-push` |
| Pipeline vượt 15 phút | Chạy song song, cache, image nhỏ, tách calibration khỏi pipeline |
| Chi phí hạ tầng | Chốt Mục 4.1 sớm, dùng credit sinh viên hoặc free tier |
| Chỉ một người hiểu CI/CD | Cả hai review workflow; viết hướng dẫn vận hành trong README repo |
| Admin bypass ruleset làm mất bằng chứng review | Giữ ruleset không cho bypass, kể cả admin |

## 10. Việc cần làm ngay sau khi chốt

1. Ghi quyết định Mục 4 vào `tracking/DECISIONS_LOG.md`.
2. Tạo `tracking/feature-plans/ci-cd-pipeline.md` từ `_template.md`.
3. Tạo repo code (theo Mục 4.3), chạy `devkit/install.sh`, áp ruleset bằng `devkit/apply-rulesets.sh`.
4. Dựng workflow 6 chặng và deploy lần đầu.
5. Ghi `tracking/AI_USAGE_LOG.md` cho phần AI hỗ trợ soạn tài liệu này.
