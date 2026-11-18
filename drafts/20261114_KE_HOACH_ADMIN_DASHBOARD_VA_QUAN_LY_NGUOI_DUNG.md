# Kế hoạch (BẢN NHÁP, chưa chốt): Admin Dashboard (S36) và Quản lý người dùng (S24, S19)

- Ngày: 2026-11-14 · Trạng thái: **nháp**, nằm ở `drafts/` theo quy tắc 7 của CLAUDE.md. Chưa sửa SRS, Class Diagram, SD hay schema.
- Nguồn đã đọc: `design/ui/20261017_MO_TA_…` (S36, S24, S19, R-5, BR-13), `DANH_SACH_MAN_HINH_THEO_ROLE.md`, SRS v3.0 (UCADM05/08/09, BR-03…BR-05, BR-16…BR-19, API mục X), `design/class/*`, `backend/backend/prisma/schema.prisma`, mã backend `reporting`, `user-admin`, mã frontend `(admin)/admin/…`.
- **Chưa đọc được:** hai màn Stitch (Admin/Dashboard `2beaef86…`, Admin/Danh Sách Lô Câu Hỏi `48ef6cc5…`). Phiên này không có công cụ Stitch, và đoạn dán không kèm URL tải. Mục C bên dưới chỉ là danh sách việc đối chiếu cần làm khi có mã/ảnh. Lưu ý: màn "Danh Sách Lô Câu Hỏi" là S28, không thuộc phạm vi dashboard/người dùng.

## A. Hiện trạng mã (đã kiểm)

| Phần | Hiện trạng |
|---|---|
| FE `/admin/dashboard`, `/admin/users/{students,teachers,import}` | Chỉ là trang rỗng 7 dòng (`<h1>dashboard</h1>`). Chưa có feature folder `admin`/`users` trong `src/features` (hiện có auth, exam, history, items, reports, result). |
| BE `user-admin` | Chỉ có `user-admin.module.ts` rỗng (`@Module({})`). Không có controller, use-case, repository. |
| BE `reporting` | Chỉ có `GET /reports/class-distribution`, `GET /reports/export-csv` (TEACHER, ADMIN). **Không có** endpoint thống kê hệ thống cho dashboard. |
| Prisma (backend) | `User` có `isActive`, `mustChangePassword`, `passwordChangedAt`, `StudentProfile.studentCode`, `TeacherProfile.teacherCode`. **Không có** bảng nhật ký kiểm toán, **không có** cột trạng thái gửi email, **không có** `lastLoginAt`. |

## B. Mâu thuẫn và điểm lệch giữa các tài liệu (cần chốt)

| # | Mâu thuẫn | Bằng chứng | Ảnh hưởng | Phương án (cần chốt) |
|---|---|---|---|---|
| X1 | **Nhật ký kiểm toán không có nơi lưu.** BR-18 bắt buộc ghi nhật ký khi nâng/thu hồi Admin; BR-05 ghi nhật ký gửi email thất bại; nhưng schema không có bảng `audit_logs`, chỉ có `ItemReviewEvent` (riêng cho câu hỏi). | SRS BR-05, BR-18, L0; schema | Không thể code `PATCH /users/:id/role` đúng BR-18 | **ĐỀ XUẤT của AI (chờ chốt, người dùng đã nhờ đề xuất): (a)** bảng chung `AuditLog` (`id`, `actorId`→User, `action` enum, `targetType`, `targetId`, `metadata Json`, `createdAt`; index `(targetType,targetId)`, `(actorId,createdAt)`), ghi qua `AuditPort` để đổi nơi lưu sau này. Lý do: BR-18 đòi "nhật ký kiểm toán", dùng lại cho khóa tài khoản, kỳ thi, gửi lại mật khẩu; chi phí là 1 migration + sửa SRS mục 6.2, Class Diagram, schema tham chiếu. Phương án khác: (b) chỉ log pino, không đổi schema nhưng không truy vấn được và phải sửa BR-18; (c) mở rộng `ItemReviewEvent`: không hợp vì gắn `Item` |
| X2 | **Trạng thái gửi email.** SRS BR-05 nói ghi trạng thái "chưa gửi" để Admin xem được; UI S24 và Quyết định #120 (P18-2) nói **không** có cột trạng thái email, chỉ có "Gửi lại mật khẩu tạm" từng tài khoản. | SRS BR-05 vs UI S24, P18-2 | SRS và UI tự mâu thuẫn; S19 vẫn cần "kết quả: số tạo, số email đã xếp hàng" | **ĐÃ CHỌN (người dùng, 14/11/2026): (a)** theo #120: không đổi schema; sửa SRS BR-05 và UCADM08 ngoại lệ 10a cho khớp (chỉ ghi `AuditLog`/log và báo số email đã xếp hàng); chưa ghi Quyết định chính thức vào `DECISIONS_LOG` |
| X3 | **Dashboard S36 đang `🔶 R-5` (chưa xác nhận giữ)**; UI ghi "Số liệu là mock", API chỉ ghi chung `GET /reports/…`. SRS chỉ có dòng "Tổng quan hệ thống, cấu hình (UCADM05)" trong ma trận quyền (mục 8) và BR-13; **không có F-ID riêng** cho dashboard Admin, không có API tương ứng ở mục X. | UI S36, R-5; SRS 803, 873, 1172 | Thiếu hợp đồng API (đường dẫn, JSON, quyền) | Chốt giữ S36; thêm vào SRS mục X: ví dụ `GET /reports/overview` (đề xuất tên), hoặc chia nhỏ. Tên endpoint thuộc quy tắc "không tự quyết" |
| X4 | **UCADM05 gắn hai màn:** UC "Báo cáo tổng thể" trỏ tới cả S36 và S12; còn UI nói Admin dùng chung S12 (`/teacher/reports`, R-2). Dashboard trùng một phần với S12 (phân phối CEFR, thống kê trạng thái câu). | UI dòng 1229, R-2; S12 mục 6 (thẻ trạng thái câu chỉ Admin) | Có thể trùng nghiệp vụ/endpoint giữa S36 và S12 | Chốt ranh giới: S36 = số tổng hợp toàn hệ thống; S12 = báo cáo lớp theo kỳ. Tái dùng `item-status-chart` |
| X5 | **Chỉ số "SV đã thi" và "câu vào ngân hàng" chưa có định nghĩa.** "SV đã thi" = SV có ≥1 phiên `COMPLETED`? tính cả `TIMEOUT`? "Câu vào ngân hàng" = số `FINAL_APPROVED`? Có nghĩa theo lọc kỳ (BR-13, mặc định toàn hệ thống) không? | UI S36 `stat-students`, `stat-final-approved` | Số liệu hai nơi có thể lệch | Cần định nghĩa trong SRS khi chốt X3 |
| X6 | **Tên endpoint tạo tài khoản lệch phạm vi quyền:** `GET/POST /students`, `/teachers` (SRS 1183–1187) đặt ở nhóm Admin nhưng URL không có tiền tố `admin`; đổi role dùng `/users/:id/role`. Tên module backend `user-admin` vẫn là "tên chờ duyệt". | SRS X; CLAUDE.md | Đặt tên module và route ảnh hưởng mở rộng | Chốt tên module (`user-admin` hay tách `user-import`), giữ route theo SRS |
| X7 | **`POST /students/:id/lock\|unlock\|resend-temporary-password` chỉ có đường `/students`**; SRS ghi rút gọn, UI S24 dùng cho cả GV (`/teachers/:id/...`). | SRS 1186 vs UI S24 | Thiếu đường dẫn cho GV | Sửa SRS cho đối xứng (ghi rõ `/teachers/:id/...`) |
| X8 | Khóa tài khoản giữa lúc thi: **không cần thêm cơ chế** (mục G.5). | | | |
| X9 | ~~Token không tra DB~~ **SAI, đã rút lại (mục G.1):** dựa trên bản cũ `backend/backend`. | | | |
| X10 | **Sequence Diagram thiếu.** SD_06 chỉ phủ import tài khoản. Không có SD cho: tạo từng người (L1b), sửa/khóa/gửi lại mật khẩu, nâng/thu hồi Admin (L0), dashboard Admin. SD_05 là báo cáo lớp. | `design/sequence/SD_01…12` | Nợ đồng bộ tài liệu | Bổ sung SD mới hoặc mở rộng SD_06 (đề xuất, chờ chốt số/tên) |
| X11 | ~~schema backend còn ItemPackage~~ **chỉ đúng với bản cũ `backend/backend`**, nhánh mới nhất đã bỏ (mục G.8). | | | |
| X12 | **Mã CEFR trên dashboard:** UI nói "6 màu CEFR", SRS thang A1–C2 là 6 mức; kiểm tra `CEFRLevel` trong schema có đủ 6 giá trị khớp. | UI S36 | **Lệch thật:** enum `CEFRLevel` trong schema là `PRE_A1, A1, A2, B1, B2, C1_PLUS` (6 giá trị), không phải A1–C2. Biểu đồ dashboard "6 màu" phải dùng đúng 6 nhãn này; kiểm SRS/UI dùng thang nào để thống nhất nhãn | Chốt nhãn hiển thị (ví dụ `C1_PLUS` hiển thị "C1+") rồi ghi vào UI |

## C. Việc đối chiếu màn Stitch (chờ có dữ liệu)

Khi có mã HTML/ảnh của "Admin/Dashboard", đối chiếu với S36: 4 thẻ số (`stat-students`, `stat-final-approved`, `stat-batches-open`, `stat-open-rounds`), biểu đồ phân phối CEFR, biểu đồ 6 trạng thái câu, chuyển Biểu đồ|Bảng, câu rỗng "Chưa có sinh viên nào hoàn thành bài thi.", mục sidebar Admin (L-SIDEBAR, mục 2.4), nhãn tiếng Việt, và xem Stitch có thêm thành phần nằm ngoài đặc tả (ví dụ biểu đồ xu hướng, thông báo chuông; **TL không làm chuông thời gian thực**, CLAUDE.md). Màn quản lý người dùng (S24) chưa có bản Stitch nào được nhắc; cần xác nhận có hay không.

## D. Đề xuất thứ tự thực hiện (sau khi chốt mục B)

1. Chốt X1, X2, X3 (quyết định thiết kế) → ghi `DECISIONS_LOG` (#136+) và `feature-plans/admin-dashboard-user-mgmt.md` (tạo từ `_template.md`).
2. Đồng bộ tài liệu (SRS .md/.docx, UI, SD mới, CD nếu có `AuditLog`, schema.prisma + migration).
3. Backend `user-admin`: use-case tạo từng người, sửa, khóa/mở khóa, gửi lại mật khẩu tạm, đổi role (Strategy/Port: `MailPort`, `PasswordGenerator`, `AuditPort`); controller + guard `ADMIN`; test: trùng email/MSSV/mã GV, không thu hồi Admin cuối, Admin không tự thu hồi mình, khóa chặn đăng nhập.
4. Backend `reporting`: endpoint tổng quan (theo định nghĩa X5) + test.
5. Frontend: feature folder `admin-users`, `admin-overview`; trang S24, S19, S36 theo mã Stitch đã chốt.
6. Import lưới tạm (S19) là đợt sau, vì cần Redis + hàng đợi mail (`mail` module, Q-5 SMTP chưa chốt).

## E. Kế hoạch xây dựng (đề xuất, chờ chốt mục B)

| Pha | Việc | Phụ thuộc | Đầu ra / kiểm chứng |
|---|---|---|---|
| P0 | Cung cấp mã/ảnh Stitch (hiện chưa có) và chốt G.3, G.4, G.7, G.8 (X1 hoãn) | Người dùng | Ghi `DECISIONS_LOG` #136+ và `feature-plans/admin-dashboard-user-mgmt.md` |
| P1 | Đồng bộ tài liệu: SRS `.md`+`.docx` (BR-05, BR-18, API tổng quan, định nghĩa chỉ số), UI S36/S24, SD mới cho L0/L1b/khóa/dashboard, Class Diagram + `schema.prisma` tham chiếu (`AuditLog` nếu chọn) | P0 | Bảng tài liệu ☑/☐ theo mục 4b |
| P2 | Schema backend (trên nhánh mới nhất): chỉ khi G.3 chọn (b) hoặc X1 được mở lại; mặc định không có migration | G.3, X1 | Migration chạy được trên Postgres thật (nếu có) |
| P3 | ~~Sửa `auth`~~ **Bỏ** (G.1: nhánh `feat/auth-module` đã tra DB mỗi request). Thay bằng: xác nhận nhánh làm việc chính, rồi chỉ viết test tích hợp khóa/đổi role | G.8 | Test: khóa → 401; thu hồi Admin → 403 |
| P4 | `user-admin` (Clean Architecture): use-case tạo SV/GV, sửa, khóa/mở, gửi lại mật khẩu tạm, đổi role; cổng `MailPort`, `PasswordGenerator`, `AuditPort`; controller `/students`, `/teachers`, `/users/:id/role`, guard `ADMIN` | P2, P3, module `mail` | Test: trùng email/MSSV/mã GV (409), không thu hồi Admin cuối, Admin không tự thu hồi mình, mật khẩu tạm 12 ký tự không lộ trong response/log |
| P5 | `reporting`: `GET` tổng quan (4 số + phân phối CEFR + 6 trạng thái câu, lọc `examRoundId` theo BR-13), tái dùng truy vấn S12 | X3, X5 | Test số liệu với dữ liệu seed; `AI_REJECTED` chỉ Admin |
| P6 | Frontend: `features/admin-users`, `features/admin-overview`; trang S24 (2 tab, modal tạo/sửa, khóa, gửi lại, nâng/thu hồi), S36; i18n `messages/vi.ts`; chuyển Biểu đồ/Bảng | P4, P5, mã Stitch | Test thành phần + testid theo UI |
| P7 (đợt sau) | S19 import lưới tạm (Redis, BullMQ, `mail`, SMTP Q-5) | Q-5 | SD_06 đã có |

Ghi chú tuân thủ: trước P2 phải hỏi lại người dùng đã chốt gì ở X1/X9 (quy tắc "không tự quyết định"); sau mỗi pha ghi `AI_USAGE_LOG.md`; cập nhật weekly-log tuần hiện tại (Nợ đồng bộ tài liệu nếu hoãn).

## F. Việc cần người dùng

1. Cung cấp URL tải hoặc file HTML/PNG của hai màn Stitch (câu trả lời vừa gửi chỉ lặp lại đoạn hướng dẫn, không có URL).
2. Chốt: X1 (đề xuất AuditLog), X3, X5, X8, X9, X12, X6.


## G. Cập nhật sau phản hồi ngày 14/11/2026 (thay thế các ý tương ứng ở mục B)

### G.1 Token sau khi khóa/thu hồi quyền (X9): nhận định cũ SAI, đã rút lại
- Mã trong `D:\TLCN\backend\backend` là **bản cũ**. Nhánh mới nhất là `feat/auth-module` (clone `D:\TLCN\backend-auth-fix`, commit `c12c98c`, 10/11/2026; chỉ kiểm bản đã clone, chưa `git fetch` nên remote có thể mới hơn). `JwtStrategy.validate()` ở nhánh này **tra DB mỗi request**: không có user hoặc `isActive = false` → 401; `role` trả về lấy từ DB (không lấy từ payload) nên `RolesGuard` thấy role mới ngay; token cấp trước `passwordChangedAt` → 401.
- Vậy **BR-18 (token cũ mất quyền cũ) và BR-19 (khóa thì không dùng được) đã được đáp ứng ở tầng access token**; không cần `tokenVersion`, blacklist hay sửa module `auth`. Khi làm `user-admin`, use-case khóa/đổi role chỉ cần ghi DB, kèm test tích hợp "khóa → request kế tiếp 401", "thu hồi Admin → 403".
- Ghi nhận (không phải lỗi): (a) mỗi request một truy vấn user, chấp nhận ở quy mô TL, **không** cache Redis vì cache làm trễ hiệu lực khóa; (b) `configuration.ts` có `refreshExpiresIn` nhưng chưa có use-case refresh, nên chưa có đường làm mới token cần chặn; nếu sau này thêm refresh phải kiểm `isActive` và role ở đó; (c) SRS cần ghi rõ cơ chế "tra DB mỗi request" ở BR-18/BR-19.
- Hệ quả tài liệu: `CLAUDE.md` ghi "bản thật ở `backend/backend/prisma`" đang trỏ vào bản cũ (xem G.8).

### G.2 Nhật ký kiểm toán (X1): hoãn
Để sau, theo yêu cầu. Nợ cần ghi: BR-18 ("ghi nhật ký kiểm toán khi nâng/thu hồi Admin") chưa đạt khi code `PATCH /users/:id/role`; tạm chỉ ghi log ứng dụng và ghi vào weekly-log mục "Nợ đồng bộ tài liệu". Đề xuất `AuditLog` ở mục B giữ làm phương án khi quay lại.

### G.3 Trạng thái gửi email (X2): xem xét thêm
Bạn đã chọn theo #120 nhưng nay muốn xem xét thêm. Ba cách:

| Cách | Nội dung | Được | Mất |
|---|---|---|---|
| (a) Giữ #120 | Không lưu trạng thái; chỉ nút "Gửi lại mật khẩu tạm" từng tài khoản; BullMQ retry + log | Không đổi schema, đơn giản | Admin không thấy ai chưa nhận thư; phải sửa SRS BR-05 |
| (b) Cột trên `User` | Ví dụ trạng thái NOT_SENT/QUEUED/SENT/FAILED + thời điểm; S24 hiện huy hiệu và lọc được | Đúng BR-05 của SRS | Đảo #120 (P18-2); đổi schema + Class Diagram; worker mail phải ghi ngược vào `User` (tăng coupling `mail` ↔ `user-admin`, cần port/sự kiện) |
| (c) Chỉ trạng thái job BullMQ | Không đổi schema | Nhẹ | Job xong bị dọn sau một thời gian, không bền, khó lọc |

Đề xuất của AI: (a) cho TL; (b) nếu GVHD cần chứng minh không bỏ sót SV. **Chưa chọn.**

### G.4 Dashboard S36 vào SRS (X3, X4, X5): nội dung đề xuất đưa vào SRS
Tên endpoint và F-ID do bạn đặt (quy tắc không tự quyết); dưới đây dùng tên tạm.
- **F-ID mới** (số do bạn đặt): "Tổng quan hệ thống cho Admin". UCADM05 chỉ gắn **S36**; S12 vẫn là UCGV07/08 (Admin xem chung theo R-2). Ranh giới: S36 = số liệu toàn hệ thống; S12 = báo cáo lớp theo kỳ.
- **API tạm:** `GET /api/v1/reports/overview?examRoundId=` (ADMIN). Trả: `studentsCompleted`, `finalApprovedItems`, `batchesNeedingAction`, `openExamRounds`, `cefrDistribution[6]` (khóa theo enum `CEFRLevel`), `itemStatusCounts[6]` (theo `ItemStatus`, `AI_REJECTED` chỉ Admin). Lọc `examRoundId` (BR-13) chỉ áp cho `studentsCompleted` và `cefrDistribution`; các số về ngân hàng câu, lô, kỳ đang mở luôn là toàn hệ thống.
- **Định nghĩa chỉ số (chờ chốt):**
  - SV đã thi = số SV khác nhau có ít nhất một `TestSession` `COMPLETED` (gồm `TIMEOUT`, không gồm `ABANDONED`).
  - Câu vào ngân hàng = số `Item` `FINAL_APPROVED`.
  - Lô cần xử lý = số `ItemBatch` ở `READY_TO_ASSIGN`, `READY_TO_FINALIZE`, `FAILED`, `PARTIAL` (đang chờ Admin hành động; `IN_REVIEW` chờ GV nên không tính).
  - Kỳ đang mở = `effectiveStatus = OPEN` (BR-10, không đọc cột `status`).
  - Phân phối CEFR = mức của hồ sơ mới nhất mỗi SV.
- Thay số "mock" trong UI S36 bằng dữ liệu thật; thêm `GetSystemOverviewUseCase` trong `reporting`, tái dùng truy vấn của `GenerateClassReportUseCase` nếu cùng nguồn.

### G.5 Khóa tài khoản giữa lúc thi (X8): có cần không?
**Không cần thêm cơ chế.** Vì `JwtStrategy` tra DB mỗi request, SV bị khóa nhận 401 ở mọi request kế tiếp. Phiên `IN_PROGRESS` đứng yên tới `expires_at` rồi bị xử lý lười theo K5, giống khi SV đóng tab. Chỉ cần sửa câu chữ BR-19: "khóa ⇒ mọi request bị 401; phiên đang làm không xử lý riêng, quá `expires_at` thì áp dụng K5; mở khóa khi phiên còn hạn thì SV làm tiếp được". Không thêm mã lỗi hay use-case. Khi code cần kiểm một điều: bắt đầu phiên không tạo phiên thứ hai cho SV còn phiên `IN_PROGRESS`.

### G.6 Nhãn CEFR (X12): chuẩn hóa theo enum
Enum là nguồn chân lý (`schema.prisma` và `@apt/shared-types`): `PRE_A1, A1, A2, B1, B2, C1_PLUS`. SRS và UI đang dùng nhãn hiển thị `Pre-A1 … C1+` (cùng ý, khác hình thức). Đề xuất: mọi tài liệu và mã gọi **giá trị** bằng tên enum; **nhãn hiển thị** lấy từ một bảng ánh xạ duy nhất `CEFR_LABELS` (`PRE_A1` → "Pre-A1", `C1_PLUS` → "C1+") đặt trong `@apt/shared-types` hoặc FE `messages/vi.ts`, kèm màu huy hiệu của UI. Việc cần làm: thêm bảng ánh xạ vào SRS (mục thang CEFR) và UI (mục huy hiệu), đổi mô tả dashboard dùng tên enum, kiểm Class Diagram dùng `CEFRLevel` đủ 6 giá trị.

### G.7 Route đầy đủ cho quản lý tài khoản (X6, X7): đề xuất hoàn chỉnh
SRS hiện có `GET/POST/PATCH` cho `/students` và `/teachers`, nhưng `lock|unlock|resend-temporary-password` chỉ ghi cho `/students`. Đề xuất tách "dữ liệu hồ sơ" và "thao tác trên tài khoản" để không nhân đôi use-case:

| Nhóm | Route | Ghi chú |
|---|---|---|
| Danh sách, tạo, sửa (có trường riêng MSSV / mã GV) | `GET` và `POST /students`, `PATCH /students/:id`; `GET` và `POST /teachers`, `PATCH /teachers/:id` | Giữ theo SRS; `?q=` tìm theo MSSV/mã GV/email, có phân trang |
| Thao tác tài khoản dùng chung | `POST /users/:id/lock`, `POST /users/:id/unlock`, `POST /users/:id/resend-temporary-password`, `PATCH /users/:id/role` | Một use-case, một chỗ kiểm quy tắc |

Phương án thay thế: đối xứng `/students/:id/lock` và `/teachers/:id/lock` (khớp SRS từng chữ nhưng nhân đôi route). Quy tắc cần ghi thêm: SRS chỉ cấm Admin **tự thu hồi** mình, chưa cấm **tự khóa** (đề xuất cấm; chờ chốt); khóa Admin khác có được không; mã lỗi 403/404/409. Chờ bạn chọn một trong hai.

### G.8 Còn `ItemPackage` trong backend không? Kết quả kiểm
- Nhánh mới nhất `feat/auth-module` (`backend-auth-fix`), cùng `develop` ở `backend-develop` và `backend-latest`: `schema.prisma` **không còn** model/quan hệ `ItemPackage`, `ItemBatchAssignment`, `ItemReviewAssignment`; chỉ còn **một dòng chú thích** (dòng 190) ghi quyết định 03/11/2026. Mã `src` không tham chiếu các tên này. **Không có gì phải bỏ** ở nhánh mới nhất.
- Chỗ còn sót là thư mục **cũ** `D:\TLCN\backend\backend` (không có `.git`; schema còn 5 chỗ `ItemPackage`; `JwtStrategy` chưa tra DB). Tôi **chưa xóa hay sửa** vì không rõ có ai còn dùng. Đề xuất: nén vào `_ARCHIVE_20261114` hoặc xóa khi bạn xác nhận, và sửa `CLAUDE.md` trỏ tới clone đúng.

### G.9 Sequence Diagram cần thêm (đề xuất, chưa dựng XMI)
File SD là XMI Enterprise Architect rất dài (60–190 KB mỗi file, ảnh dựng bằng `render_sd.py`). Vì G.3 và G.7 chưa chốt (ảnh hưởng thông điệp), tôi lập nội dung trước, chốt xong mới dựng XML và ảnh để không phải làm lại. Ba SD, tạm đặt tên `SD_13` đến `SD_15` (số và tên do bạn duyệt):
1. **SD_13 Quản lý tài khoản (UCADM09):** Admin → Trang Tài khoản → `UserAdminController` → `CreateAccountUseCase` (kiểm trùng email/MSSV/mã GV, 409) → `PasswordGenerator` → `IUserRepository` (transaction `users` + profile) → `MailPort` (xếp hàng BullMQ). Nhánh sửa họ tên/email, khóa/mở khóa, gửi lại mật khẩu tạm (sinh mới, `mustChangePassword = true`).
2. **SD_14 Nâng/thu hồi Admin (L0, BR-17/18):** Admin → `PATCH /users/:id/role` → kiểm không tự thu hồi, không phải Admin cuối → đổi role → (ghi nhật ký: chờ X1) → request kế tiếp của người bị đổi quyền qua `JwtStrategy` tra DB nên mất quyền ngay.
3. **SD_15 Tổng quan hệ thống (UCADM05, S36):** Admin → Trang Tổng quan → `ReportingController.overview` → `GetSystemOverviewUseCase` → các repository (phiên, câu hỏi, lô, kỳ thi, hồ sơ) → trả số liệu và hai biểu đồ.

Cũng cần cập nhật **SD_01** (xác thực mỗi request tra DB) và ghi chú kết quả Lưu ở SD_06.

### G.10 Việc cần bạn chốt lại
1. G.3: chọn (a), (b) hay (c) cho trạng thái email.
2. G.4: duyệt định nghĩa chỉ số, tên endpoint tạm, F-ID.
3. G.7: nhóm route `/users/:id/...` hay đối xứng; có cấm Admin tự khóa mình.
4. G.8: xử lý thư mục `backend/backend` cũ và sửa `CLAUDE.md`.
5. Vẫn thiếu mã/ảnh hai màn Stitch.


## H. Quyết định ngày 14/11/2026 (người dùng chốt qua hỏi đáp)
- **Nơi làm việc:** `D:\TLCNpt-workspaceackend` (clone mới). Nhánh làm việc `feat/user-admin` tạo từ `origin/feat/auth-module` (commit `c12c98c`), chưa push, đã bỏ upstream để tránh push nhầm.
- **Trạng thái email (G.3): giữ #120**, không lưu trạng thái, không đổi schema; sửa SRS BR-05 và UCADM08 ngoại lệ 10a cho khớp.
- **Dọn bản cũ:** đã nén `D:\TLCNackend` (bản cũ, bỏ `node_modules`, `dist`) vào `D:\TLCN\_ARCHIVE_20261114ackend_backend_cu.tar.gz`; **chưa xóa** thư mục gốc. Ba clone `backend-develop`, `backend-latest`, `backend-auth-fix` sạch, không có commit chưa push; chưa đụng.
- **Còn mở:** route tài khoản (G.7), cấm Admin tự khóa, tên endpoint dashboard và định nghĩa chỉ số (G.4), sửa `CLAUDE.md`, mã/ảnh Stitch.

## I. Đối chiếu màn Stitch "Admin/Dashboard" với S36 (đã đọc mã HTML, 14/11/2026)

Đã xóa thư mục cũ `D:\TLCN\backend` theo yêu cầu (đã có bản nén `_ARCHIVE_20261114/backend_backend_cu.tar.gz`, kiểm có `prisma/schema.prisma` trong đó). Ba clone `backend-*` chưa đụng.

| # | Chỗ lệch | Stitch | Tài liệu | Mức |
|---|---|---|---|---|
| D1 | **Ngưỡng θ→CEFR sai so với SRS** | B1 `0 ≤ θ < 1.2`, B2 `1.2 ≤ θ < 2.2`, C1+ `θ ≥ 2.2` | SRS mục 4.6: B1 `[0,1)`, B2 `[1,2)`, C1+ `θ ≥ 2.0` (Pre-A1 và A1, A2 khớp) | Cao: sửa Stitch theo SRS, không đổi SRS |
| D2 | **Bộ lọc kỳ thi (BR-13) bị thiếu** | Không có | S36 phải có chip "Kỳ thi" gửi `examRoundId` | Cao |
| D3 | **Khái niệm "Học kỳ 1 • 2024-2025", "Kỳ 1 2024-2025"** ở đầu trang và huy hiệu | Có | Hệ thống không có thực thể học kỳ/năm học; chỉ có `ExamRound` | Cao: bỏ hoặc thay bằng tên kỳ thi/bộ lọc |
| D4 | **Mã ca thi** (`CAT-2024-K1-A`), **"Phòng máy A1"** | Có trong bảng kỳ thi và thẻ "Kỳ thi đang mở" | `ExamRound` không có mã ca/phòng máy | Cao: bỏ |
| D5 | **Thẻ "Ngân hàng câu hỏi: Đã kiểm định & hiệu chuẩn Rasch"** | Ghi hiệu chuẩn | `FINAL_APPROVED` chưa chắc đã calibrate (`Item.calibrated` riêng) | Trung: đổi nhãn thành "Đã vào ngân hàng chính thức" |
| D6 | **Thẻ "+14% so với kỳ trước"** | Có | Không có API/định nghĩa so sánh kỳ | Trung: bỏ hoặc cần quyết định riêng |
| D7 | **Nút "Làm mới chỉ số", "Xuất báo cáo tổng quan (PDF/Excel)"**, "Hỗ trợ kỹ thuật", "Phiên bản CAT-Rasch v2.4" | Có | Không có trong S36; không có API xuất tổng quan (chỉ có xuất CSV báo cáo lớp và xuất kết quả kỳ ở S22) | Trung: bỏ hoặc đề xuất UC mới |
| D8 | **Dòng nhận xét "Điểm chuẩn trung vị đạt B1, phân bổ chuẩn Gaussian", "Độ tin cậy SEM < 0.32"** | Có | Là nội dung tự bịa; ngưỡng SE của hệ thống là 0.35 | Cao: bỏ |
| D9 | **Biểu đồ 6 trạng thái câu dùng vòng tròn (donut)** | Donut 3 cung (mã SVG chỉ gom 3 nhóm), có bảng 6 dòng bên dưới | S36: 6 thanh ngang màu trạng thái + chuyển Biểu đồ/Bảng | Trung: đổi biểu đồ, thêm chuyển Biểu đồ/Bảng cho cả biểu đồ trạng thái (Stitch chỉ có ở CEFR) |
| D10 | **Nhãn 6 trạng thái** khớp (Đã vào ngân hàng chính thức, Đã xác nhận vòng 2, Đã duyệt vòng 1, Chờ duyệt vòng 1, Đã loại bởi GV, AI đã loại) | Có; tổng 693 = cộng đúng | UI mục 2.2 nhãn: `DRAFT` = "Chờ duyệt vòng 1" ... | OK, chỉ cần thống nhất chữ "chính thức" |
| D11 | **Nhãn CEFR có hậu tố** ("A1 - Beginner", "B2 - Upper-Intermediate") | Có | UI/SRS: nhãn "Pre-A1…C1+" qua `CEFR_LABELS` | Trung: dùng nhãn ngắn |
| D12 | **Màu thanh CEFR** không theo bảng màu huy hiệu (nhiều thanh dùng chung `#0284C7`) | Có | UI mục 2.1: 6 màu riêng | Thấp |
| D13 | **Thẻ không bấm được** (sinh viên, kỳ thi) và thẻ "Lô cần xử lý" có liên kết | Chỉ thẻ lô có link | S36: `stat-batches-open` → S28, `stat-open-rounds` → S20 | Thấp: thêm link thẻ kỳ thi |
| D14 | **Bảng "Các kỳ thi đang diễn ra"**: khung giờ chỉ trong một ngày, "142 đang làm bài / 518 đã hoàn thành", "Cập nhật tự động mỗi 30s" | Có | `ExamRound` có `opensAt/closesAt` (có thể nhiều ngày), số đang làm/hoàn thành tính từ phiên; **polling 30 giây** chưa có trong đặc tả (TL không làm thông báo thời gian thực, polling thì chưa quyết định) | Trung: cần quyết định có bảng này và có tự cập nhật không |
| D15 | **Trạng thái rỗng, lỗi, đang tải, 403** | Không có | S36 mục (e): "Chưa có sinh viên nào hoàn thành bài thi." | Trung: bổ sung |
| D16 | **Thanh bên khác nhau giữa hai màn**: màn Dashboard chỉ có 5 mục; màn "Danh sách lô" thêm nhóm "Khảo thí & Tra cứu" (Báo cáo lớp học, Hồ sơ sinh viên) | Lệch | L-SIDEBAR Admin có 7 mục (cả Báo cáo lớp học, Hồ sơ SV) | Trung: dùng bản 7 mục ở mọi màn |
| D17 | **Số liệu mẫu mâu thuẫn**: dashboard 2024-2025, lô 2026; card "Chờ giao GV 02" mà bảng chỉ có 1 lô chờ giao | Có | — | Thấp (chỉ là dữ liệu mẫu) |

Màn "Admin/Danh Sách Lô Câu Hỏi" thuộc S28 (không phải phạm vi đợt này), nhưng đã thấy các chỗ lệch cần ghi để khỏi quên:
- **Cột "Tiến độ C1-C3"** thực ra hiển thị tiến độ duyệt/xác nhận của GV; C1–C3 là ba điểm AI kiểm, nên tên cột sai.
- **Nhãn nguồn "AI sinh (C1)"**: nguồn chỉ là `AI_GENERATED` hoặc `IMPORTED`; "(C1)" gây hiểu nhầm.
- **"Mã đợt" (BATCH-2026-VOCAB-01)**: `ItemBatch` chỉ có `name` tùy chọn, không có mã đợt.
- Hạn chót "Quá hạn", thẻ "Tỉ lệ duyệt đạt chuẩn 88.4%", nút "Bộ lọc nâng cao", "Xuất báo cáo" không có trong S28; ngược lại các tab trạng thái bỏ sót `FINAL_CHECKED`, `FAILED`, `PARTIAL`.

Màn quản lý tài khoản (S24) và import tài khoản (S19): vẫn chưa có bản Stitch nào.

## J. Quyết định đã chốt ngày 14/11/2026 (hỏi đáp, đợt 2)
1. **Route (G.7):** gộp thao tác tài khoản về `POST /users/:id/lock`, `POST /users/:id/unlock`, `POST /users/:id/resend-temporary-password`, `PATCH /users/:id/role`. `/students` và `/teachers` chỉ cho danh sách, tạo, sửa.
2. **Cấm Admin tự khóa mình** (thêm vào BR-17/19, cùng quy tắc cấm tự thu hồi quyền và không thu hồi/khóa Admin cuối cùng nếu áp dụng).
3. **Endpoint tổng quan:** `GET /reports/overview` (ADMIN, `examRoundId` tùy chọn).
4. **Thành phần Stitch ngoài S36 (D6, D7, D14):** bỏ "+% so kỳ trước", nút "Xuất báo cáo tổng quan"; bảng kỳ thi đang mở giữ nhưng không tự cập nhật (chỉ làm mới khi tải trang hoặc bấm nút). Không tăng phạm vi, nên chưa cần sửa `COMMITMENT_BASELINE.md`.
5. **Đã dọn:** xóa `D:\TLCN\backend` cũ (có bản nén).
6. **Còn mở:** số F-ID cho "Tổng quan hệ thống"; định nghĩa 5 chỉ số (G.4); danh sách sửa Stitch D1–D17 (mục I) chờ bạn duyệt; nhật ký kiểm toán (G.2, hoãn).
