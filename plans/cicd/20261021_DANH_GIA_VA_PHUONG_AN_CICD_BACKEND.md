# Đánh giá CI/CD backend và các phương án cần chốt

> Ngày: 21/10/2026 (Tuần 5/12). Phạm vi: repo `backend` (NestJS) và phần dùng chung với `frontend`.
> Đã đối chiếu với: `CI-CD/MO_TA_CI_CD_VA_DIEM_CHAN.md`, `work/week-04/*CI_CD*`, SRS v3.0 (Mục III, XV), `DECISIONS_LOG` (#65–#81, #122), mã thật trong `D:\TLCN\backend\backend`.
> Rubric: đọc qua `HUONG_DAN_RUBRIC_VA_TRACKING.md` (TC2.4, TC2.5, TC2.6, G6, G8). **Chưa có bản `.docx` gốc lúc soạn**, nên các con số điểm cụ thể ghi "chưa kiểm chứng".
> Cách đọc: ✅ đã kiểm trên mã · ❓ chưa kiểm được · ★ khuyến nghị của người soạn, **không phải quyết định**. Mỗi mục "Quyết định" cần hai người đánh dấu ☑ một phương án.

---

## 1. Kết luận ngắn

1. Thiết kế CI/CD trên giấy đủ để hướng tới Mức 5 ở TC2.6, nhưng **chưa có bằng chứng chạy thật**: chưa có git, pipeline chưa chạy lần nào, 0 lần deploy.
2. Phía **backend thiếu mã** mà tài liệu mô tả như đã có: Dockerfile, workflow, module health, migration. (Frontend đã có Dockerfile và 3 workflow.)
3. Có **một lỗi thiết kế sẽ làm CI gãy ngay lần đầu**: backend phụ thuộc `@apt/shared-types` qua đường dẫn `file:` nằm ngoài repo.
4. Việc cấp bách nhất là tạo bằng chứng chạy thật (G6), không phải tối ưu hạ tầng.

---

## 2. Hiện trạng đã kiểm trên mã

| Mục | Tài liệu nói | Mã thật (`D:\TLCN\backend\backend`) | Trạng thái |
|---|---|---|---|
| Workflow GitHub Actions | Pipeline 6 chặng | Không có `.github/` | ✅ thiếu |
| Dockerfile / `deploy/` | Có, image 847 MB | Không có | ✅ thiếu |
| Module health (`/health`, `/ready`) | "✅ code và test" | Không có trong 13 module | ✅ thiếu |
| Prisma migrations | Cần cho `migrate deploy` | Thư mục rỗng; có `custom_migrations.sql` tách rời | ✅ thiếu (đúng Q1) |
| Phụ thuộc `@apt/shared-types` | Hai repo riêng (#48) | `"file:../../packages/shared-types"` | ✅ sẽ gãy khi tách repo |
| Test | Cần ≥ 4 tầng, coverage ≥ 70% | 2 file spec; `test/e2e` và `test/integration` rỗng | ✅ thiếu |
| `.env` | Không commit | Có file `.env`, đã nằm trong `.gitignore`; chưa có git | ✅ an toàn hiện tại |
| Git | Cần từ sớm | Chưa `git init` | ✅ thiếu |

**Chưa rõ nguồn gốc chênh lệch.** Mô tả CI/CD ghi backend đã có health và Dockerfile chạy thử, nhưng cả bản hiện tại lẫn bản sao lưu `D:\TLCN_ARCHIVE_cu` đều không có. Có thể mã nằm ở máy khác hoặc bị mất khi đồng bộ bản đồng đội ngày 21/10. Người phụ trách hạ tầng cần xác nhận trước khi cho là tài liệu sai.

---

## 3. Đối chiếu rubric

| Tiêu chí | Yêu cầu Mức 5 | Hiện trạng | Rủi ro |
|---|---|---|---|
| TC2.6 | ≥ 6 chặng; xanh ≥ 90%; ≥ 10 deploy trải đều; commit→staging ≤ 15 phút; secret qua nền tảng; rollback; health + log + cảnh báo | Có thiết kế; 0 lần chạy | Cao |
| G6 | Không có pipeline chạy được lúc bảo vệ ⇒ TC2.6 trần Mức 2 | Đang trượt mốc deploy đầu (cuối Tuần 5) | Cao |
| TC2.4 | 0 lỗi lint; trùng lặp ≤ 3%; ≥ 90% tuần có commit; ≥ 90% PR có review; 0 secret | Lint sạch, trùng lặp 0,55% (đo cục bộ, chưa trong CI); chưa có commit | Cao (phần commit) |
| TC2.5 | ≥ 4 tầng; coverage ≥ 70%; 100% test qua | ~2,8% coverage BE; thiếu tầng | Cao |
| G8 | Repo không build được từ bản sạch | `shared-types` ngoài repo ⇒ có nguy cơ | Trung bình–cao ❓ mức phạt cụ thể chưa kiểm |

---

## 4. Các quyết định cần chốt

### Quyết định 1 — Nối `@apt/shared-types` vào CI (chặn mọi thứ khác) 🔴

**Vấn đề:** `file:../../packages/shared-types` nằm ngoài repo backend. Runner chỉ checkout backend nên `npm ci` báo thiếu package. Đã chốt #122 mô hình C, nhưng chưa chốt cách CI lấy gói.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. CI checkout thêm repo chứa `packages/shared-types` (hiện ở `docs-repo`), build `dist/`, rồi trỏ `file:` vào bản đó** | Ít việc nhất; giữ #122; không thêm dịch vụ | Pipeline thêm bước checkout/build; cần trỏ lại đường dẫn `file:` trong CI mà không đổi `package.json` thường; `docs-repo` phải đọc được từ CI |
| B. Đẩy `@apt/shared-types` lên GitHub Packages, BE và FE cài như gói thường | Chuẩn nhất, không phụ thuộc cấu trúc thư mục | Thêm quy trình phát hành phiên bản và token; nhiều việc cho nhóm 2 người |
| C. Đưa `shared-types` vào từng repo (sao chép) hoặc gom monorepo | CI đơn giản | Trái #48/#122 (lệch bản, hoặc đảo quyết định tách repo) |

☐ A ☐ B ☐ C

### Quyết định 2 — Migration khởi tạo Prisma (Q1) 🔴

**Vấn đề:** `prisma/migrations` rỗng nên `prisma migrate deploy` không tạo bảng; `custom_migrations.sql` (chỉ mục một phần, CHECK) tách rời.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. Sinh migration baseline từ `schema.prisma`, nối nội dung `custom_migrations.sql`, mọi thay đổi sau đi qua migration** | Đúng chuẩn Prisma; deploy lặp lại được | Phải kiểm drift (đặc biệt chỉ mục `idx_items_cat`); schema còn đổi nhiều nên baseline có thể phải làm lại |
| B. `prisma db push` khi deploy | Nhanh | Không có lịch sử; không rollback; không áp được SQL tùy biến; không khuyến nghị |
| C. Chạy SQL tay một lần | Không đổi mã | Không lặp lại, không minh chứng được |

☐ A ☐ B ☐ C

### Quyết định 3 — Cấu trúc pipeline backend (rubric đếm ≥ 6 chặng)

**Lưu ý:** bản mẫu trong báo cáo cũ chỉ có 5 job vì gộp build và lint. Nếu hội đồng đếm theo job thì thiếu một chặng.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. 6 job tách riêng: build · lint/trùng lặp · test (kèm Postgres, Redis) · bảo mật · đóng gói · deploy + smoke test; bám pipeline frontend** | Rõ ràng đủ ≥ 6; thống nhất hai repo | Mỗi job cài lại phụ thuộc (dùng cache để bù) |
| B. Giữ 5 job, mỗi job nhiều bước | Ít chạy lại | Rủi ro bị đếm thiếu chặng |

Điểm cần có trong cả hai phương án: bước migrate trước test tích hợp (phụ thuộc Quyết định 2); `dependency-review` trên PR; smoke test sau deploy; `rollback.yml`; secret đọc qua `env`, không nội suy thẳng vào lệnh.
Quét secret: `gitleaks-action` cần license nếu repo thuộc tổ chức; nếu vậy dùng gitleaks CLI hoặc xác nhận loại tài khoản ❓.

☐ A ☐ B

### Quyết định 4 — Phát hành trên máy chủ dùng chung (Q2, Q5)

Báo cáo cũ đề xuất cấu hình Nginx của server và chạy `certbot` để dùng cổng 80/443 và tự gia hạn chứng chỉ. **Cách này trái Quyết định #71** (không sửa/reload Nginx host, không chạy certbot, không đổi UFW của `farmnongviet`), nên chỉ làm nếu chủ server đồng ý rõ ràng.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. Giữ nguyên (Docker + Nginx container, cổng 8443, chứng chỉ thủ công), đặt lịch nhắc, đo RAM bằng `docker stats`, có tiêu chí dừng** | Không đụng dự án kia; không phụ thuộc dịch vụ ngoài | Gia hạn thủ công ≤ 90 ngày (hết hạn 2027-01-07, nhắc 2026-12-08); rubric không bắt buộc tự động |
| B. Xin phép chủ server dùng Nginx host làm reverse proxy + certbot HTTP-01 | Cổng chuẩn; chứng chỉ tự động | Chạm vào dự án đang chạy thật; cần chấp thuận bằng lời |
| C. Tự động hóa DNS-01 (chuyển DNS sang nhà cung cấp có API, hoặc ủy quyền `_acme-challenge`) | Tự động mà không đụng host | Đổi DNS; chưa kiểm chứng với tên miền `.id.vn` |
| D. Thuê VPS riêng cho staging | Cách ly hoàn toàn | Tốn tiền; cấu hình lại tên miền, chứng chỉ, secret |

☐ A ☐ B ☐ C ☐ D

### Quyết định 5 — Sao lưu cơ sở dữ liệu staging (#70)

Rubric không yêu cầu. Chỉ cân nhắc lại nếu thực nghiệm người dùng (TC2.7) lưu dữ liệu thật trên staging.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. Giữ #70: không sao lưu**, dữ liệu staging là seed tạo lại được | Ít việc | Mất dữ liệu nếu ổ hỏng hoặc migration lỗi |
| B. `pg_dump` hằng ngày, giữ 7 bản | An toàn dữ liệu thực nghiệm | Phải ghi lên server (cần chủ server đồng ý); chưa xác minh tên container; thêm dung lượng |
| C. Chỉ dump trước mỗi lần deploy có migration | Rẻ, đúng chỗ rủi ro nhất | Gắn vào `deploy.sh`; bản dump nằm cùng đĩa server |

☐ A ☐ B ☐ C

### Quyết định 6 — Kích thước image backend (Q4)

847 MB là số đã đo; mốc "150–220 MB" của báo cáo cũ chỉ là ước tính. Rubric chỉ yêu cầu commit→staging ≤ 15 phút.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. Chấp nhận lúc này; đo commit→staging ở lần deploy đầu; tối ưu nếu vượt ngưỡng** | Không tốn công khi chưa cần | Có thể phải làm gấp nếu chậm |
| B. Tối ưu ngay (multi-stage, tách Prisma CLI, loại phụ thuộc phát triển) | Image nhỏ hơn (chưa đo) | Thêm việc; rủi ro lỗi migration trong image |

☐ A ☐ B

### Quyết định 7 — Phụ thuộc deploy giữa frontend và backend

**Vấn đề:** compose, nginx, `deploy.sh` do pipeline backend chép lên server; frontend phải chờ backend deploy lần đầu.

| Phương án | Lợi | Đánh đổi |
|---|---|---|
| **A ★. Chấp nhận, ghi vào `TECH_DEBT.md`, ghi rõ thứ tự deploy lần đầu** | Không đổi cấu trúc khi sắp tới hạn | Còn phụ thuộc ngầm |
| B. Đưa cấu hình dùng chung vào một chỗ riêng (repo hạ tầng nhỏ hoặc thư mục trong `docs-repo`) | Hai pipeline độc lập | Thêm một nơi quản lý; cần đồng bộ quyền truy cập |

☐ A ☐ B

---

## 5. Việc không cần quyết định (làm ngay)

| # | Việc | Ghi chú |
|---|---|---|
| 1 | Thêm module Health (`/api/v1/health` liveness, `/ready` kiểm Postgres và Redis, 503 khi hỏng) + test | Dockerfile và workflow dùng nó |
| 2 | Chạy `gitleaks` trên cây mã, xác nhận `.env` không vào commit đầu tiên | `.env` đã trong `.gitignore` |
| 3 | `git init`, đẩy `backend` và `frontend`, bật ruleset 1 approval | Cần workflow chạy một lần trước khi bật ruleset |
| 4 | Hỏi GVHD: tuần commit tính từ ngày bắt đầu đồ án hay từ ngày tạo repo (G1) | Quyết định điểm TC2.4 |
| 5 | Viết test cho backend (hiện ~2,8%): unit, integration, API | TC2.5 cần ≥ 4 tầng |
| 6 | Ghi chú rollback: chỉ an toàn nếu không có migration phá vỡ tương thích kể từ bản đích | Chỉ là tài liệu |

## 6. Thứ tự đề xuất

Quyết định 1 → Quyết định 2 → Health → Dockerfile + pipeline (Quyết định 3, 6) → `git init` và đẩy mã → deploy đầu tiên → đo (tỉ lệ xanh, số lần deploy, thời gian). Quyết định 4, 5, 7 làm sau khi pipeline chạy được.

## 7. Điều chưa kiểm chứng

- Con số điểm và mức phạt cụ thể của G6/G8 (thiếu rubric gốc).
- Backend có chạy `npm test` được không sau khi sửa đường dẫn `shared-types`.
- Trạng thái server staging (container có chạy không, RAM thật).
- Mã backend có Dockerfile/health ở máy nào khác hay không.
