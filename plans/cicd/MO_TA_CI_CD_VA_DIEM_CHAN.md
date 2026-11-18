# Mô tả CI/CD của dự án và các điểm chặn cần quyết định

> **Ngày lập:** 2026-10-10 (Tuần 4/12). **Người đọc:** thành viên còn lại của nhóm và giảng viên hướng dẫn.
> **Mục đích:** (1) giúp người chưa tham gia hiểu CI/CD của dự án làm gì và chạy theo luồng nào; (2) nêu rõ các **điểm đang chặn** để người đọc quyết định (Mục 7).
> **Cách đọc nhãn trạng thái:** ✅ đã làm và đã kiểm chứng · 🟡 đã soạn, chưa chạy thật · ⛔ chưa làm.
> File này **không chứa** mật khẩu, khóa, token hay địa chỉ IP server. Các thông tin đó lưu trong GitHub Secrets hoặc trên server.

---

## 1. Tóm tắt trong 30 giây

Dự án có hai kho mã: **backend** (NestJS) và **frontend** (Next.js). Mỗi lần có thay đổi được gộp vào nhánh `develop`, GitHub **tự động** kiểm tra mã (build, lint, test, bảo mật, trùng lặp), đóng gói thành image Docker, đưa lên server **staging** và kiểm tra xem ứng dụng có chạy không. Một dịch vụ bên ngoài (Better Stack) theo dõi staging và gửi email nếu nó chết. Nếu bản mới hỏng có thể quay về bản cũ bằng một workflow.

**Hiện trạng:** hạ tầng và mã cấu hình đã sẵn sàng và đã được chạy thử ở máy bằng Docker; **chưa đẩy mã lên GitHub nên pipeline chưa chạy lần nào trên GitHub, và staging chưa được khởi động**. Có một điểm chặn nghiêm trọng về cơ sở dữ liệu (Mục 7, Q1).

**Vì sao làm:** rubric đồ án (TC2.4 chất lượng mã, TC2.5 kiểm thử, TC2.6 CI/CD, và quy tắc chặn điểm G6/G8) yêu cầu có pipeline chạy được, deploy tự động, rollback và giám sát. Chi tiết đối chiếu ở Mục 8.

---

## 2. Các khái niệm cần biết

| Từ | Nghĩa |
|---|---|
| **CI** (tích hợp liên tục) | Mỗi khi có thay đổi, máy của GitHub tự build và kiểm tra để phát hiện lỗi sớm |
| **CD** (triển khai liên tục) | Sau khi kiểm tra xanh, tự đóng gói và đưa bản mới lên môi trường |
| **Pull Request (PR)** | Đề nghị gộp một nhánh vào nhánh khác; người còn lại xem xét (review) trước khi gộp |
| **Image / Docker** | Gói ứng dụng đóng sẵn để chạy giống nhau ở mọi nơi |
| **GHCR** | Kho chứa image của GitHub |
| **Staging** | Bản chạy thật trên server để thử và demo trước khi dùng thật; ở đây là **môi trường duy nhất** |
| **Smoke test** | Kiểm tra nhanh sau deploy: ứng dụng có trả lời không |
| **Rollback** | Quay về phiên bản trước khi bản mới hỏng |
| **Health check** | Địa chỉ riêng cho biết ứng dụng "khỏe" hay không |

---

## 3. Kiến trúc tổng thể

```
 Máy lập trình viên          GitHub (Actions)                            Server staging
 ──────────────────          ─────────────────                           ──────────────────────────────
  commit + push     ──►  Pull Request vào develop                        Docker Compose gồm:
  (hook cục bộ chặn          │  CI: build, lint, trùng lặp, test,            • nginx   (cổng 8443, HTTPS)
   lỗi sơ đẳng)              │      bảo mật                                  • frontend (Next.js)
                             ▼                                               • backend  (NestJS)
                      Người kia review + approve                             • postgres, redis
                             │ merge vào develop                             • vector (gửi log)
                             ▼
                      CD: đóng gói Docker ──► GHCR (kho image)
                             │
                             ▼
                      deploy qua SSH ───────────────────────────────►  kéo image mới, migration, khởi động lại
                             │                                          rồi smoke test
                             ▼
                      (hỏng ⇒ job đỏ; quay lại bản cũ bằng workflow rollback)

 Giám sát ngoài: Better Stack gọi /api/health mỗi 5 phút ⇒ email cảnh báo; gom log của các container.
```

**Địa chỉ staging:** `https://staging.adaptiveplacementtest.id.vn:8443`.

**Điểm đặc biệt cần hiểu:** server staging **dùng chung với một dự án khác đang chạy thật** (website `farmnongviet`). Vì vậy: (a) cổng 80/443 thuộc dự án kia nên ta dùng cổng **8443**; (b) ta **không được sửa** bất kỳ cấu hình nào của dự án kia; (c) staging chỉ được dùng phần RAM dư. Đây là nguồn gốc của nhiều ràng buộc dưới đây.

---

## 4. Luồng làm việc (từng bước)

### 4.1. Một thay đổi đi từ máy đến staging

| # | Việc | Ai/Cái gì | Kết quả |
|---|---|---|---|
| 1 | Tạo nhánh `feat/ten-chuc-nang`, viết mã | Thành viên | |
| 2 | `git commit` | Hook cục bộ (devkit) | Chặn: message sai quy ước, có file `.env`, có secret |
| 3 | `git push` | Hook cục bộ | Chạy lint và test ở máy trước khi đẩy |
| 4 | Mở **Pull Request** vào `develop` | Thành viên | Kích hoạt CI |
| 5 | **CI** chạy (xem 4.2) | GitHub Actions | Xanh hoặc đỏ |
| 6 | Người còn lại **review và approve** | Thành viên khác | Quy tắc nhánh bắt buộc 1 approval |
| 7 | **Squash merge** vào `develop` | Thành viên | Kích hoạt CD |
| 8 | **Đóng gói**: build image, đẩy GHCR, gắn tag theo mã commit | GitHub Actions | Image `sha-xxxxxxx` |
| 9 | **Deploy**: SSH vào server, chạy `deploy.sh` | GitHub Actions | Kéo image, migration (backend), khởi động lại đúng dịch vụ |
| 10 | **Smoke test** | `deploy.sh` | Gọi health bên trong container; không khỏe sau 150 giây thì job đỏ |
| 11 | Ghi nhận lần deploy | GitHub Environment `staging` | Hiện ở mục Deployments (bằng chứng đếm số lần deploy) |
| 12 | Phát hành: PR `develop → main`, gắn tag `vX.Y.Z` | Thành viên | GitHub Release dùng đúng image đã chạy ở staging |

### 4.2. CI gồm những chặng nào (mỗi repo có pipeline riêng)

| Chặng | Việc | Công cụ | Điều kiện đạt |
|---|---|---|---|
| 1. Build | `npm ci` rồi build từ bản sạch | npm, Next/Nest | Build thành công |
| 2. Lint / phân tích tĩnh | Kiểm lỗi, kiểu, định dạng, **trùng lặp mã** | oxlint (BE), ESLint (FE), `tsc`, Prettier, jscpd | 0 lỗi lint; trùng lặp ≤ 3% |
| 3. Test | Test đơn vị + báo cáo coverage | Vitest | Toàn bộ test qua |
| 4. Bảo mật | Quét secret toàn lịch sử; lỗ hổng thư viện chạy thật; review phụ thuộc trên PR | gitleaks, `npm audit`, dependency-review | 0 secret; 0 lỗ hổng mức high |
| (tùy chọn) | Phân tích tĩnh trên dashboard (Blocker/High, trùng lặp, coverage) | SonarCloud | Chỉ chạy khi có token; **không bắt buộc để merge** |
| 5. Đóng gói | Build image, đẩy GHCR | Docker Buildx | Chỉ chạy khi push vào `develop` |
| 6. Triển khai | Deploy + smoke test | SSH, Docker Compose | Chỉ chạy khi push vào `develop` |

Chặng 5–6 chỉ chạy khi chặng 1–4 xanh.

### 4.3. Quay lại bản cũ (rollback)

Workflow `rollback` nhận tên một image cũ (ví dụ `…:sha-abc1234`) và chạy lại đúng bước deploy với image đó. Chỉ an toàn nếu migration cơ sở dữ liệu **tương thích ngược** (chính sách: migration chỉ thêm, không xóa; Prisma không có migration "down").

### 4.4. Giám sát sau triển khai

| Việc | Cách làm | Trạng thái |
|---|---|---|
| Health check | Backend `GET /api/v1/health` (còn sống) và `/ready` (kiểm Postgres + Redis, 503 nếu hỏng); frontend `GET /api/health` (sâu: 503 nếu backend không sẵn sàng) và `/api/health/live` | ✅ code và test; ✅ chạy thử bằng Docker ở máy (tắt/bật Redis và Postgres) |
| Cảnh báo | Better Stack gọi `/api/health` mỗi **5 phút**, gửi email khi không phản hồi | 🟡 monitor đã tạo, đang tạm dừng |
| Log tập trung | Container `vector` gửi log Docker lên Better Stack | 🟡 cấu hình đã qua `vector validate`; chưa gửi log thật |

---

## 5. Bảo mật và bí mật

- **Không có bí mật trong mã.** Khóa SSH, địa chỉ server, token lưu trong **GitHub Secrets** (Environment `staging`). Trên server, file `.env` (quyền 600) chứa mật khẩu cơ sở dữ liệu và JWT, **sinh ngẫu nhiên ngay trên server**.
- **Quét secret** bằng gitleaks cục bộ trên phần sẽ commit: 0 phát hiện (sau khi sửa 2 dương tính giả).
- **Lỗ hổng thư viện chạy thật** (`npm audit --omit=dev`, mức high): 0 ở cả hai repo.
- Repo **công khai**: workflow dùng `pull_request` (không `pull_request_target`), không dùng self-hosted runner, quyền token tối thiểu cho từng job.
- Chỉ **một cổng (8443)** mở ra Internet; backend, Postgres, Redis không có cổng nào mở ra ngoài.
- Docker xuất bản cổng **bỏ qua tường lửa UFW**, nên chỉ được khai báo đúng cổng 8443.

---

## 6. Những gì đã kiểm chứng và chưa

### 6.1. Đã chạy thật (ở máy bằng Docker)

| Kiểm | Kết quả |
|---|---|
| `docker build` backend / frontend | Thành công; **847 MB / 296 MB** |
| Chạy Postgres + Redis + backend + frontend | Cả bốn `healthy`; RAM lúc rảnh ~26–36 MB mỗi dịch vụ |
| Mất/hồi phục Redis và Postgres | `/ready` báo 503 rồi **tự về 200** |
| `nginx -t` cấu hình thật | Thành công (chứng chỉ tự ký tạm) |
| `vector validate` | Thành công |
| Bộ kiểm cục bộ (`verify-local.sh`) | **16/16 đạt** (lint, trùng lặp, build, test + coverage, lỗ hổng thư viện, prisma validate, compose, `actionlint`) |
| `actionlint` các workflow | Sạch |
| Số đo hiện tại | Trùng lặp: BE **0,55%**, FE **0,00%**; coverage: BE **~2,8% dòng**, FE **~81%** (không tính mã shadcn sinh sẵn) |

### 6.2. Đã làm trên server (chỉ trong thư mục của user `deploy`)

Cài Docker; chép cấu hình compose, Nginx, vector, `deploy.sh` vào `~/placement`; tạo `.env` với khóa ngẫu nhiên; cấp chứng chỉ HTTPS thật (hết hạn **2027-01-07**). **Chưa khởi động container nào.** Không đụng dự án `farmnongviet`.

### 6.3. Chưa làm

- Chạy pipeline lần nào trên GitHub (mã chưa đẩy lên; repo `backend`, `frontend` chưa `git init`).
- Deploy thật lên staging; chạy `deploy.sh` trên server.
- Gửi thử log thật, điền token Better Stack vào `.env` trên server.
- Chạy SonarCloud (có tổ chức, project và token nhưng chưa có lần phân tích nào).
- Đo các số liệu rubric từ GitHub (`ci-metrics.sh`): tỉ lệ xanh, số lần deploy, thời gian.

---

## 7. ĐIỂM CHẶN CẦN QUYẾT ĐỊNH

> Ghi chú: ★ là khuyến nghị của người soạn, **không phải quyết định**. Đánh dấu `☑` một phương án mỗi mục.

### 7.1. Quyết định thiết kế / kỹ thuật

#### ☐ Q1 — Cơ sở dữ liệu staging sẽ trống: tạo migration khởi tạo thế nào? 🔴

**Vấn đề (đã kiểm bằng Docker):** thư mục `prisma/migrations` của backend **không có migration nào**. Khi deploy, `prisma migrate deploy` báo "No pending migrations" và database chỉ có bảng hệ thống, **không có bảng nghiệp vụ**. Mọi chức năng cần DB sẽ lỗi. Ngoài ra còn tệp `custom_migrations.sql` (chỉ mục một phần, ràng buộc CHECK) mà Prisma không tự sinh được.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Sinh migration khởi tạo từ `schema.prisma`, nối thêm phần SQL tùy biến; từ đó mọi thay đổi schema đi qua migration | Đúng chuẩn Prisma, deploy lặp lại được, rollback có chính sách | Chạm thiết kế CSDL: phải kiểm drift giữa schema và SQL tùy biến (đặc biệt chỉ mục `idx_items_cat`); cần người quyết định về nội dung |
| B. Dùng `prisma db push` khi deploy | Nhanh nhất | Không có lịch sử migration, có thể xóa dữ liệu khi schema đổi, không dùng được cho rollback; **không khuyến nghị** |
| C. Chạy SQL bằng tay một lần trên server | Không đổi mã | Không lặp lại được, không minh chứng được, dễ sai |

**Ảnh hưởng nếu chưa quyết:** staging có thể chạy nhưng vô dụng; deploy backend đầu tiên sẽ qua health nhưng không có dữ liệu.
**Người quyết:** cả nhóm (liên quan thiết kế CSDL).

#### ☐ Q2 — Dùng chung server với dự án `farmnongviet`: tiếp tục hay tách? 🟠

**Vấn đề:** server có ~1 GB RAM khả dụng, đang chạy một ứng dụng thật của dự án khác. Staging thêm tải; nếu thiếu RAM, **dự án kia có thể bị chậm**. Chưa đo RAM khi staging chạy thật và có người dùng.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Tiếp tục, giữ giới hạn bộ nhớ từng container, **đo bằng `docker stats` ở lần chạy đầu**, có tiêu chí dừng (RAM khả dụng < ~200 MB hoặc swap tăng nhanh ⇒ `docker compose down`) | Không tốn tiền, đúng stack Docker + Nginx | Rủi ro ảnh hưởng dự án kia; HTTPS bị ràng buộc ở cổng 8443 |
| B. Thuê VPS riêng cho staging | Cách ly hoàn toàn, dùng được cổng 80/443 | Tốn tiền, phải cấu hình lại tên miền, chứng chỉ, secret |
| C. Chưa dùng server, chỉ CI trên GitHub | An toàn tuyệt đối cho dự án kia | Không có deploy tự động ⇒ TC2.6 tối đa **Mức 3**; nguy cơ **G6** (không có pipeline chạy được lúc bảo vệ) |

**Người quyết:** cả nhóm + chủ dự án `farmnongviet` (cho phép dùng chung).

#### ☐ Q3 — Gói ảnh Docker (GHCR) để công khai hay riêng tư?

**Vấn đề:** image đẩy lên GHCR có thể ở chế độ riêng tư; server cần quyền kéo. Pipeline hiện đăng nhập GHCR trên server bằng token tạm của lần chạy rồi đăng xuất (**chưa chạy thật**).

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Giữ riêng tư, đăng nhập bằng token tạm của lần chạy | Không lộ image | Có thể lỗi quyền lần đầu; cần liên kết package với repo (đã thêm nhãn nguồn) |
| B. Đặt package công khai | Đơn giản, server kéo không cần đăng nhập | Ai cũng tải được image (không chứa bí mật, nhưng chứa mã đã build) |

#### ☐ Q4 — Kích thước image backend 847 MB: tối ưu hay chấp nhận?

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Chấp nhận lúc này, ghi vào nợ kỹ thuật | Không tốn công; tập trung việc chính | Tải chậm, tốn đĩa server (còn ~13 GB), có thể ảnh hưởng mục tiêu ≤ 15 phút |
| B. Tách giai đoạn: cài riêng Prisma CLI, loại thư viện phát triển | Image nhỏ hơn đáng kể (chưa đo) | Thêm việc và rủi ro lỗi migration |

#### ☐ Q5 — Gia hạn chứng chỉ HTTPS thủ công: chấp nhận hay tự động hóa?

**Hiện tại (quyết định #74):** chứng chỉ gia hạn **thủ công** tối đa mỗi 90 ngày (hết hạn **2027-01-07**, nhắc lịch **2026-12-08**), vì nhà đăng ký tên miền (BKNS) không có công cụ cấp tự động tương thích.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Giữ thủ công, nhắc lịch | Không phụ thuộc dịch vụ ngoài | Dễ quên; rubric ưa quy trình tự động |
| B. Chuyển DNS sang Cloudflare (có API) hoặc ủy quyền bản ghi xác thực | Cấp và gia hạn tự động | Đổi nameserver (ảnh hưởng toàn bộ DNS), chưa kiểm chứng Cloudflare nhận tên miền `.id.vn` |

#### ☐ Q6 — Sao lưu cơ sở dữ liệu staging

**Hiện tại (quyết định #70):** không sao lưu.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Không sao lưu khi dữ liệu chỉ là seed tạo lại được | Ít việc | Mất dữ liệu nếu ổ đĩa hỏng hoặc migration lỗi |
| B. `pg_dump` hằng ngày, giữ 7 bản, lưu ngoài server | An toàn dữ liệu | Thêm việc và dung lượng; cần nếu có dữ liệu thực nghiệm người dùng (TC2.7) |

#### ☐ Q7 — SonarCloud: bắt buộc để merge hay chỉ tham khảo?

**Vấn đề:** Sonar cho báo cáo Blocker/High, trùng lặp, coverage (cần cho minh chứng TC2.4 nếu hội đồng đòi). Nhưng coverage backend rất thấp (~2,8%) nên **Quality Gate nhiều khả năng đỏ**. Một số loại token (phạm vi tổ chức) thuộc gói trả phí; gói Free của tổ chức có thể đổi sau thời gian dùng thử.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★.** Chạy như báo cáo tham khảo, **không bắt buộc**; đưa vào bắt buộc khi xanh ổn định | Không làm đỏ pipeline vô lý | Mất chức năng "chặn" ở giai đoạn đầu |
| B. Bắt buộc ngay | Cổng chất lượng nghiêm | Pipeline đỏ liên tục đến khi coverage đủ ⇒ kéo tụt tỉ lệ build xanh |

### 7.2. Cần giảng viên hướng dẫn xác nhận (rubric không định nghĩa rõ)

| # | Câu hỏi | Vì sao quan trọng |
|---|---|---|
| ☐ G1 | Khoa đếm **"tuần có commit"** từ ngày bắt đầu đồ án hay từ ngày tạo repo? | Git bắt đầu muộn (đang Tuần 4); nếu mẫu số là 12 tuần thì TC2.4 khó đạt Mức 5 (≥ 90% tuần có commit). Không tạo commit lùi ngày |
| ☐ G2 | **"Build xanh ≥ 90%"** tính cả run trên Pull Request hay chỉ nhánh chính? | Những lần đỏ khi mới dựng pipeline có thể kéo tụt tỉ lệ |
| ☐ G3 | **Staging trên server của nhóm** (dùng chung, cổng 8443) có được chấp nhận làm "môi trường đã triển khai"? | Quyết định TC2.6, G6 và phần demo của TC3 |
| ☐ G4 | **"≥ 10 lần deploy tự động, trải đều"** — đếm theo tuần thế nào? | Deploy chỉ tính từ khi chạy được; càng muộn càng khó trải đều |
| ☐ G5 | Hội đồng cần **quyền gì** để xem repo và staging? (quy tắc G8) | Repo phải cấp quyền cho hội đồng |
| ☐ G6 | Chấp nhận **gia hạn chứng chỉ thủ công** và **không sao lưu DB** như điểm yếu đã biết? | Ảnh hưởng đánh giá "quy trình tự động" |

### 7.3. Việc cần người thực hiện (không phải quyết định, nhưng đang chặn)

| # | Việc | Người |
|---|---|---|
| ☐ T1 | **Phân công người phụ trách hạ tầng CI/CD** (hiện chưa có tên); quyền truy cập server, GitHub Secrets chỉ nên nằm ở người đáng tin, có phương án khi người đó vắng | Cả nhóm |
| ☐ T2 | **Siết bảo mật SSH của server** (đổi thông tin đăng nhập quản trị, tắt đăng nhập mật khẩu nếu chủ server đồng ý) | Chủ server |
| ☐ T3 | **Khởi tạo git và đẩy mã** `backend`, `frontend` lên GitHub; bật quy tắc bảo vệ nhánh (cần workflow chạy ít nhất một lần trước khi bật) | Thành viên |
| ☐ T4 | Điền token của Better Stack vào `~/placement/.env` trên server; tạo bản ghi **Heartbeat** nếu cần | Thành viên |
| ☐ T5 | Quy ước khi một người vắng và Pull Request chờ review (quy tắc nhánh không cho bỏ qua review, kể cả quản trị) | Cả nhóm |
| ☐ T6 | Backend còn **lỗi nghiêm trọng về nghiệp vụ/bảo mật** (đăng nhập, ước lượng θ, kiểm quyền phiên thi, lộ đáp án): **không dùng dữ liệu thật trên staging** cho đến khi sửa (kế hoạch rà soát backend) | Thành viên phụ trách BE |
| ☐ T7 | Viết test cho backend: coverage hiện ~2,8% và chưa đủ số tầng kiểm thử (TC2.5 Mức 5 cần ≥ 4 tầng) | Thành viên phụ trách BE |

---

## 8. Đối chiếu nhanh với rubric (chỉ phần liên quan CI/CD)

| Yêu cầu | Đáp ứng trong thiết kế | Trạng thái |
|---|---|---|
| TC2.6: ≥ 6 chặng pipeline | Có (Mục 4.2) | 🟡 chưa chạy trên GitHub |
| TC2.6: build xanh ≥ 90%; ≥ 10 deploy tự động trải đều; commit → staging ≤ 15 phút | Thiết kế đã hướng tới; cần **đo thật** sau khi chạy | ⛔ chưa có số đo (hiện 0 lần deploy) |
| TC2.6: secret qua nền tảng; phiên bản + rollback | GitHub Environment; tag theo commit; workflow rollback | 🟡 |
| TC2.6: health check + log tập trung + cảnh báo | Mục 4.4 | 🟡 / ✅ (phần health) |
| TC2.4: 0 lỗi lint, trùng lặp ≤ 3%, 0 secret | Đo cục bộ: lint sạch, BE 0,55%, FE 0,00%, gitleaks 0 | ✅ cục bộ; 🟡 trong CI |
| TC2.4: ≥ 90% tuần có commit, ≥ 90% PR có review | Quy tắc nhánh + review chéo | ⛔ phụ thuộc G1 và thời điểm bắt đầu có git |
| TC2.4: README, sơ đồ triển khai, nợ kỹ thuật, quy ước mã | `README.md`, `TECH_DEBT.md`, `CODING_CONVENTION.md`, file này | ✅ |
| TC2.5: coverage, % test pass ở CI cuối, ≥ 4 tầng test | Báo cáo coverage trong CI | ⛔ BE ~2,8%; chưa đủ tầng test |
| G6 (không có pipeline chạy được lúc bảo vệ ⇒ TC2.6 ≤ Mức 2) | Cần pipeline chạy thật và staging chạy lúc bảo vệ | ⛔ cần giải quyết Q1, Q2, T3 |
| G8 (repo không cấp quyền hội đồng / không build được) | CI build từ bản sạch; README đầy đủ | 🟡 cần G5 |

**Kết luận cho người quyết định:** thiết kế bao phủ đầy đủ các yêu cầu CI/CD Mức 5 của rubric, nhưng **chưa có bằng chứng chạy thật trên GitHub** và có **một điểm chặn kỹ thuật nghiêm trọng (Q1, migration)**. Hai việc ưu tiên: (1) quyết Q1 và Q2; (2) đẩy mã lên GitHub để có số đo thật đầu tiên.

---

## 9. Tệp liên quan

| Tệp | Nội dung |
|---|---|
| `D:\TLCN\CI-CD\README.md`, `verify-local.sh` | Mục lục và bộ kiểm tra nhanh |
| `D:\TLCN\Tuan4\HUONG_DAN_CI_CD_TU_A_DEN_Z.md` | Hướng dẫn chi tiết từng bước và giải thích công cụ |
| `D:\TLCN\Tuan4\KE_HOACH_CI_CD_VA_TRIEN_KHAI.md`, `TRACKING_CI_CD_VA_TRIEN_KHAI.md` | Kế hoạch và theo dõi tiến độ |
| `D:\TLCN\0.docs\tracking\DECISIONS_LOG.md` (#65–#74 và #79–#81) | Lịch sử các quyết định CI/CD |
| Repo `backend`: `.github/workflows/`, `Dockerfile`, `deploy/`, `TECH_DEBT.md`, `CODING_CONVENTION.md` | Mã cấu hình thật |
| Repo `frontend`: `.github/workflows/`, `Dockerfile`, `TECH_DEBT.md`, `CODING_CONVENTION.md` | Mã cấu hình thật |
