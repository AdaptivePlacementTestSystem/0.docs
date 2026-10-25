# Thư mục CI/CD — mục lục

> Thư mục này **không chứa mã chạy thật**; nó chỉ trỏ tới nơi mọi thứ nằm và giúp bạn kiểm tra nhanh. Bản gốc của từng file ở các repo bên dưới.

## 1. Mọi thứ nằm ở đâu

| Thứ | Vị trí |
|---|---|
| **Mô tả CI/CD và các điểm chặn cần quyết định (đọc trước)** | `D:\TLCN\docs-repo\plans\cicd\MO_TA_CI_CD_VA_DIEM_CHAN.md` |
| Pipeline CI/CD backend | `D:\TLCN\backend\backend\.github\workflows\pipeline.yml`, `rollback.yml` |
| Pipeline CI/CD frontend | `D:\TLCN\frontend\.github\workflows\pipeline.yml`, `rollback.yml` |
| Dockerfile | `backend\backend\Dockerfile`, `frontend\Dockerfile` |
| Cấu hình staging (compose, Nginx, gửi log, deploy) | `D:\TLCN\backend\backend\deploy\` (`docker-compose.yml`, `nginx\`, `vector\`, `deploy.sh`, `.env.staging.example`) |
| Endpoint health | BE: `src/modules/health/`; FE: `src/app/api/health/` |
| Đo trùng lặp | `.jscpd.json` + `npm run dup` (mỗi repo) |
| SonarCloud (tùy chọn) | `sonar-project.properties` (mỗi repo) |
| Quy ước mã, nợ kỹ thuật | `CODING_CONVENTION.md`, `TECH_DEBT.md` (mỗi repo) |
| Đo số liệu từ GitHub | `backend\backend\scripts\ci-metrics.sh` |
| Hướng dẫn A–Z | `D:\TLCN\Tuan4\HUONG_DAN_CI_CD_TU_A_DEN_Z.md` |
| Kế hoạch / theo dõi | `D:\TLCN\Tuan4\KE_HOACH_CI_CD_VA_TRIEN_KHAI.md`, `TRACKING_CI_CD_VA_TRIEN_KHAI.md` |
| Quyết định | `D:\TLCN\0.docs\tracking\DECISIONS_LOG.md` (#65–#74 và #79–#81) |

## 2. Kiểm tra nhanh ở máy

```bash
bash /d/TLCN/CI-CD/verify-local.sh
```

Chạy lint, đo trùng lặp, build, test + coverage, kiểm lỗ hổng thư viện, `prisma validate`, kiểm compose, `actionlint` (nếu cài). In bảng tổng kết ĐẠT / KHÔNG ĐẠT / BỎ QUA. Mục BỎ QUA **không** được tính là đạt.

Quét secret (gitleaks) cần làm đúng phần **sẽ commit**: sau khi `git add`, chạy `gitleaks detect --source .`; hoặc quét bản sao đã loại `.env`, `node_modules`, `dist`.

## 3. Thứ tự đưa lên GitHub (khi sẵn sàng)

1. Quét gitleaks → `git init -b main` → cài devkit → commit khởi tạo tối thiểu → `git branch develop` → push `main`/`develop` (`DEVKIT_BOOTSTRAP=1`).
2. Đưa mã vào bằng Pull Request (`feat/...` → `develop`), người còn lại review.
3. Sau khi workflow `devkit-checks` đã chạy một lần, chạy `apply-rulesets.sh`.
4. Trên GitHub thêm Environment `staging` + Secrets (`STAGING_HOST`, `STAGING_USER`, `STAGING_SSH_KEY`, `STAGING_KNOWN_HOSTS`), Variable `STAGING_DOMAIN`, và Secret `SONAR_TOKEN` (cấp repo).
5. Deploy **backend trước** (nó chép compose/nginx/vector/deploy.sh lên server), rồi frontend.

## 4. Trạng thái (cập nhật 2026-10-10)

| Hạng mục | Tình trạng |
|---|---|
| Server (Docker, user `deploy`, tên miền, chứng chỉ HTTPS) | Xong, đã kiểm |
| `docker build` backend, frontend | **Đã chạy thật, thành công** (BE 847 MB, FE 296 MB) |
| Chạy stack (Postgres, Redis, backend, frontend) bằng Docker ở máy | Chạy, health `healthy`; kịch bản tắt/bật Redis và Postgres: `/ready` báo 503 rồi tự về 200 |
| Cấu hình Nginx | `nginx -t` thành công (chứng chỉ giả lập) |
| Cấu hình gửi log (vector) | `vector validate` thành công; chưa gửi thử log thật |
| Workflow GitHub | `actionlint` sạch; **chưa chạy trên GitHub** |
| Migration cơ sở dữ liệu | **Thiếu**: `prisma/migrations` trống ⇒ DB staging sẽ không có bảng (cần quyết định) |
| Deploy lên staging | **Chưa** |

## 5. Minh chứng cần chụp (TC2.4, TC2.5, TC2.6, TC3)

- Đồ thị pipeline đủ chặng xanh; lịch sử run (tab Actions); mục Deployments.
- Dashboard SonarCloud (nếu dùng): issue, trùng lặp, coverage, Quality Gate.
- Báo cáo `jscpd` HTML (artifact), báo cáo coverage, báo cáo gitleaks.
- Cấu hình monitor Better Stack + **email cảnh báo thật** (tắt frontend có chủ đích) + trang Logs có dòng log của một request.
- Thử rollback một lần (ảnh log workflow `rollback`).
- Số đo từ `ci-metrics.sh` (tỉ lệ xanh, số deploy, thời gian). Chưa đo ⇒ ghi "N/A".
