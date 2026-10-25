# Danh sách màn hình theo role — luồng và chức năng

> **Ngày lập:** 2026-10-13 (Tuần 5). **Task:** W4.2 của `KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md`.
> **Trạng thái tài liệu:** ⚠️ Bản làm việc. Kế hoạch Tuần 5 **chưa ghi nhận duyệt W0.1** nên ID/route màn mới (MD-13) và ID UC mới (MD-12) vẫn là đề xuất của AI. Các điểm đã có DC-xx/Quyết định thì không gắn ⚠️.
> **Nguồn:** `Tuan4/20261010_MO_TA_MAN_HINH_TOI_GIAN_THEO_ROLE.md` (S01–S15), kế hoạch Tuần 5 (S16–S24), `frontend/src/app` (route thật, đã liệt kê bằng `find`), `20260922_MoHinhHoaYeuCau.docx` (UC).
> **Cập nhật 2026-10-13 (đồng bộ DC-15…17, Quyết định #95):** phân biệt 3 cấp GV thường / GV-QTV / QTV hệ thống (đã bị DC-19 thay). Backup: `_BACKUP_20261013_DANH_SACH_MAN_HINH_THEO_ROLE_ORIGINAL.md`.
> **Cập nhật 2026-10-13 (phiên 20, DC-18 / #96):** **GV thường chỉ xem kết quả** (S12, S13, S14 + mật khẩu). S08–S11 và S20–S23 chuyển sang Admin.
> **Cập nhật 2026-10-13 (phiên 21, DC-19 / #97): HỆ THỐNG ĐƠN TRƯỜNG** — còn **Student / Teacher / Admin (của trường)**; bỏ S25, bỏ bộ chọn Đơn vị.
> **Cập nhật 2026-10-13 (phiên 22, DC-20…DC-23 / #93, #94, #98):** D-T = T2 (`durationMinutes` theo kỳ, `expiresAt`); D-FP = C (OTP 6 số); Q-1 và Q-8 đã chốt (`users.is_active`); **import theo lưới tạm** (S19, S23: tải nhiều file cộng dồn, popup dòng bị loại, bấm Lưu mới ghi DB; không còn preview/confirm, all-or-nothing, `SKIPPED`). Backup: `_BACKUP_20261013_PHIEN22_DANH_SACH_MAN_HINH_THEO_ROLE_ORIGINAL.md`.
> **Cập nhật 2026-10-13 (phiên 23, DC-24…DC-26 / #99–#101):** Admin tạo tài khoản **SV và GV** bằng **form từng người (S24: nút "Thêm sinh viên"/"Thêm giảng viên")** hoặc **import (S19: chọn loại SV/GV, hai file mẫu)**; thời lượng kỳ thi (S21) **bắt buộc, điền sẵn 45**. API `POST /students`, `POST /teachers`, `kind` ở import là **đề xuất**. Backup: `_BACKUP_20261013_PHIEN23_DANH_SACH_MAN_HINH_THEO_ROLE_ORIGINAL.md`.
> **Cập nhật 2026-10-14 (phiên 25, DC-27…DC-45 / #102–#113, nguồn `KE_HOACH_SINH_VA_DUYET_DE_AI.md`):** luồng câu hỏi mới: Admin tạo lô (AI hoặc import file lưới tạm) → AI kiểm → giao việc → **GV A** duyệt và gửi gói → **GV B** xác nhận → Admin Kiểm tra (C3) và Import → `FINAL_APPROVED`. **Bỏ** màn thêm câu thủ công (S09) và UC GV import; **S08–S11 viết lại theo vai mới** (S08, S10 Admin chỉ xem; S11 là màn duyệt từng câu của GV A); **thêm S26–S35** (Admin S26–S32, GV S33–S35); menu GV thường có thêm **Hộp việc**; mọi `APPROVED` → `FINAL_APPROVED`; 6 trạng thái câu có nhãn tiếng Việt. **Toàn bộ ID màn S26–S35, route, ID UC (UCADM11–14, UCGV14–15) và nhãn là đề xuất của AI** (chờ duyệt, như MD-12/MD-13). Q-7…Q-10 của kế hoạch AI (ngưỡng, bản quyền, mô hình embedding, `pg_trgm`) **chờ chốt**. Backup: `_BACKUP_20261014_DANH_SACH_MAN_HINH_THEO_ROLE_ORIGINAL.md`.
> **Cập nhật 2026-10-17 (đồng bộ bản chốt 16/10 và cấu trúc đích, DECISIONS_LOG #118):** cột "Tên / Route" các màn S02–S07, S14, S19, S24 đổi sang **route chuẩn mới** (tiền tố `/student`, `/teacher`, `/admin`; tài khoản Admin `/admin/users/*`); các mô tả "Route thật" cũ chuyển thành cột "Mã nguồn hiện có" (mô hình cũ, chưa refactor). **Mô tả đầy đủ luồng từng role, nghiệp vụ và từng thành phần màn hình nay ở `Tuan5/20261017_MO_TA_LUONG_ROLE_VA_MAN_HINH_CHI_TIET_CHO_AI_AGENT.md`** (file đó là nguồn cho AI Agent sinh UI; file này giữ vai trò danh mục + ma trận UC/API). Thêm S36 (Tổng quan Admin, cũ E2). Backup: `_BACKUP_20261017_DANH_SACH_MAN_HINH_THEO_ROLE_ORIGINAL.md`.
> **Cập nhật 2026-10-18 (xem xét nhận xét đồng đội `20261018_DOI_CHIEU_MAN_HINH_THEO_ROLE_VA_SRS_V3.md`):** chấp nhận 8/11 điểm, chấp nhận có điều chỉnh 1, **bác 2** (xuất kết quả kỳ thi ở S22; lọc trạng thái email và gửi lại hàng loạt ở S24 — chuyển thành điểm mở P18-1, P18-2, mục 8). Sửa: menu Teacher 4 mục có S08; S20–S23 chuyển sang mục Admin; S08 ẩn nút quản trị với Teacher; S22 Gỡ SV chỉ bật khi "Chưa thi"; S23, S27 nút Tải file mẫu; S29 Ép gửi gói theo từng gói; S30 luồng Giao lại; S04 tự khôi phục phiên khi tải lại; S34, S35 hiện tên GV A. Backup: `Update/_BACKUP_20261018/`.
> **Giới hạn:** chưa chạy FE; cột "Mã nguồn" chỉ dựa vào việc file `page.tsx` có tồn tại, **chưa kiểm nội dung**; chưa đối chiếu với 3 file Tuan4 bằng script (W4.3); chưa có người review (W4.4).

## 0. Chú giải thẻ trạng thái

| Thẻ | Nghĩa |
|---|---|
| ✅ | Đã chốt (có Quyết định #84–#98 hoặc DC-xx trong kế hoạch) |
| ⚠️ | Còn mở hoặc đề xuất AI chưa duyệt: Q-2, Q-4, Q-5, và ID/route/UC mới chờ duyệt W0.1 (MD-12, MD-13) |
| 🔶 TODO-CONFIRM | Điểm mở kế thừa từ Tuan4 (O2, O3, O6, O7, O8, K6…) |
| Mã nguồn | **Có** = tìm thấy `page.tsx` tương ứng; **Chưa có** = chưa thấy route; **Lệch** = route thật khác mô tả Tuan4 |

Đã gỡ thẻ ⛔: D-T (chốt T2, DC-20) và D-FP (chốt OTP, DC-21). Đã gỡ ⚠️ ở: Q-1 (DC-22), Q-8 (DC-23).

## 1. Tổng quan role và quyền

| Role | Điều hướng | Phạm vi dữ liệu |
|---|---|---|
| **Student** | Thanh trên (ẩn khi làm bài) | Chỉ dữ liệu của chính mình; chỉ thi trong kỳ mình thuộc ✅ |
| **Teacher** (GV thường) | Thanh bên trái, **4 mục**: **Hộp việc** (S33, S34), **Ngân hàng câu hỏi** (S08, chỉ xem câu được giao, UCGV02), Báo cáo (S12), Tra cứu SV (S13, S14) ✅ DC-18/DC-27, #13 ngày 16/10 | **Xem** kết quả; **khi được Admin giao**: làm GV A (sửa, duyệt/từ chối, gửi gói) hoặc GV B (xác nhận/loại bỏ, không sửa). **Không** import đề, không tạo lô, không tạo kỳ thi, không thêm câu bằng form |
| **Admin** (của trường) ✅ DC-19 | Thanh bên trái, **7 mục**: Tổng quan, Ngân hàng câu hỏi (chỉ xem), **Lô câu hỏi**, Kỳ thi, Tài khoản (SV, GV), Báo cáo, Hồ sơ SV. Không có Hộp việc | `role=ADMIN`: tạo lô câu hỏi (AI hoặc import file lưới tạm), giao việc/giao lại/chỉnh hạn, theo dõi, Kiểm tra (C3) + Import cuối, xem câu AI đã loại; **không** sửa nội dung và **không** gõ câu bằng form (DC-29); tạo kỳ thi + import danh sách thi, import/tạo từng tài khoản SV và GV, quản lý tài khoản, nâng/thu hồi Admin |
| ~~QTV hệ thống~~ | — | **Đã bỏ (DC-19)** |
| EduZ (M2M) | Không có giao diện | `GET placement-profiles` bằng API Key |

Admin dùng chung giao diện GV (#53). Menu dựng theo `role` (BR-16, MD-15 mới). Các UC cũ UCADM02/03/07 vẫn ngoài phạm vi TL; màn quản trị mới của TL là **S19, S24**.

## 2. Bản đồ luồng theo role

**Student**
```
S01 Đăng nhập ──(mustChangePassword=true)──► S16 Đổi mật khẩu ──► S02
   │  └─ "Quên mật khẩu" ✅ ─► S17 (nhập email) ─► (email có OTP 6 số) ─► S18 (email + mã + mật khẩu mới) ──► S01
   └─(bình thường)──► S02 Trang chủ
S02 ─ có bài dở ─► [Tiếp tục] ─► S04
S04 ─ tải lại trang (F5) / mất mạng rồi mở lại, còn hạn ─► tự khôi phục tại chỗ (`GET /sessions/active` ─► `GET /sessions/:id/resume`), không về S02
S02 ─ "Kỳ thi của tôi" ✅ ─ chọn kỳ đang mở ─► S03 ─► S04 ⇄ (nộp/câu kế) ─► S05 ─► S06
S02 / tab ─► S07 Lịch sử ─► S05
Lỗi chặn vào thi: không thuộc kỳ / kỳ chưa mở / đã thi xong kỳ / có phiên dở ─► thông báo tại S02 hoặc S03
Hết giờ (theo expiresAt của phiên) ─► S05 (≥8 câu) hoặc S02 kèm thông báo (<8 câu, ABANDONED)
```
**Teacher (GV thường: xem kết quả + Hộp việc khi được giao)**
```
S01 ─► (S16 nếu cần) ─► S12 Báo cáo (lọc kỳ) ; S13 ─► S14 Hồ sơ SV
Hộp việc GV A: S33 (Cần duyệt) ─► S11 duyệt/sửa từng câu ─► S33 ─► [Gửi cho B]
Hộp việc GV B: S34 (Cần xác nhận, theo gói) ─► S35 màn gói (Xác nhận/Loại bỏ/“Xác nhận tất cả câu còn lại”)
Ngân hàng câu hỏi (chỉ xem): S08 ─► S10 (chỉ câu được giao; không có nút tạo lô/import)
```
**Luồng câu hỏi (Admin điều phối, DC-27…DC-45)**
```
Tạo lô: S26 (AI sinh)  hoặc  S27 (import file, lưới tạm) ─► AI kiểm C1/C2 ─► S29 Chi tiết lô (READY_TO_ASSIGN; tab “AI đã loại”)
S29 ─► S30 Giao việc (nhóm A, GV B, reviewDays, confirmDays; xem trước phân bổ) ─► lô IN_REVIEW ─► [GV A: S33/S11] ─► [GV B: S34/S35]
S29 ─► S31 Chỉnh hạn ; S30 tab Giao lại ; “Ép gửi gói” (từng dòng gói ở tab Theo GV và gói của S29)   (lô theo dõi tại S28 Danh sách lô)
Lô READY_TO_FINALIZE ─► S32 Kiểm tra (C3) ─► quyết lỗi mềm ─► Import ─► FINAL_APPROVED
Xem ngân hàng: S08 ─► S10 (chỉ đọc)
```
**Luồng Admin — các màn S20–S24, S26–S32 chỉ hiện cho Admin (S08, S10 dùng chung: GV xem câu được giao, Admin xem mọi câu)**
```
S01 ─► (S16 nếu cần) ─► S08 Ngân hàng câu hỏi (chỉ xem) ─► “Tạo lô bằng AI” S26 / “Import đề từ file” S27 ─► S29
Kỳ thi: S20 Danh sách ─► S21 Tạo/sửa ─► S22 Chi tiết ─► S23 Import danh sách (lưới tạm: tải file ─► popup dòng loại ─► Lưu) ─► S22 ─► Công bố
Báo cáo: S12 (lọc theo kỳ)   Hồ sơ: S13 ─► S14
```
**Admin (của trường)**
```
S01 ─► (S16 nếu cần) ─► S08, S10, S12–S14, S20–S23, S26–S32
Tài khoản: S24 Danh sách/quản lý SV + GV (nâng/thu hồi Admin) ─► nút "Thêm sinh viên"/"Thêm giảng viên" (form tạo từng người, đề xuất DC-24) ─► S24; hoặc ─► "Import" S19 (chọn loại SV/GV, tải 1..n file vào lưới tạm ─► popup dòng bị loại / tài khoản đã tồn tại ─► Lưu ─► kết quả) ─► S24
```

## 3. Màn hình — Student

| ID | Tên / Route thật | Mục đích và chức năng chính | UC | API chính | Mã nguồn | Ghi chú |
|---|---|---|---|---|---|---|
| S01 | Đăng nhập `/login` | Nhập **Email** + mật khẩu; chuyển trang theo role; chuyển S16 nếu `mustChangePassword`; liên kết "Quên mật khẩu" sang S17 | UCSV01 | `POST /auth/login` | Có `(public)/login` | ✅ Nhãn đổi "Email hoặc MSSV" → "Email" (#85, DC-14). ✅ Thêm liên kết "Quên mật khẩu" (DC-11, DC-21; Tuan4 ghi *không có*). ✅ Bỏ mọi nút Google/SSO. Tài khoản bị khóa (`is_active=false`) không đăng nhập được (DC-23) |
| S02 | Trang chủ `/student/dashboard` (route gốc `/` chỉ chuyển hướng theo role; mã hiện có ở `/`) | Chào; thẻ "Bắt đầu bài thi"; biến thể bài dở "Tiếp tục"; kết quả gần nhất | UCSV02, UCSV07 | `GET /sessions/active`, `GET /exam-rounds/mine` | Có `(student)/page.tsx` | ✅ **Thẻ "Kỳ thi của tôi"** (DC-07, MD-05): liệt kê kỳ SV thuộc + trạng thái hiệu lực (chưa mở / đang mở / đã đóng / đã thi). Nút Bắt đầu chỉ bật cho kỳ đang mở. ✅ Văn bản hiển thị "Tối đa 25 câu · tối đa `durationMinutes` của kỳ phút" (T2, DC-20; mặc định hiển thị 45) |
| S03 | Giới thiệu bài thi `/student/exams/[roundId]` ⚠️ (route đề xuất; cũ `/exam/start`) | Quy tắc bài thi; chọn kỳ; xác nhận bắt đầu | UCSV02 | `POST /sessions` | **Lệch/Chưa có**: không thấy `exam/start/page.tsx` (chỉ có `exam/[sessionId]`) | ✅ `POST /sessions` nhận **`examRoundId` bắt buộc** (MD-05, DC-07). Hiện tên kỳ, thời lượng và giờ còn lại tới `closesAt`. Lỗi: `NOT_IN_ROUND`, `ROUND_NOT_OPEN`, `ROUND_ALREADY_COMPLETED`, `SESSION_IN_PROGRESS` ✅. 🔶 Nút "Hủy bài cũ và bắt đầu lại" chưa có endpoint (O4) |
| S04 | Làm bài `/student/exams/[roundId]/take` (cũ `/exam/[sessionId]`) | Câu hỏi, 4 phương án, đồng hồ, nộp | UCSV03 | `GET /sessions/:id/next-item`, `POST /sessions/:id/responses` | Có `(exam)/exam/[sessionId]` | ✅ Đồng hồ đếm theo `expiresAt` = `min(startedAt + durationMinutes, closesAt)`, lưu lúc bắt đầu phiên (DC-09, DC-20). Hết hạn theo luật K5 (≥8 câu → kết quả; <8 → bỏ dở). Không hiện đúng/sai, θ, SE. **Tải lại trang (F5) hoặc mở lại khi còn hạn**: FE tự gọi `GET /sessions/active` rồi `GET /sessions/:id/resume` (cache Redis, nếu mất thì dựng lại từ PostgreSQL), hiện lại đúng câu chưa trả lời, đồng hồ tiếp tục theo `expiresAt`, không về S02; quá hạn áp luật K5. ⚠️ Route theo `roundId` nhưng API theo `sessionId`: FE tra phiên đang mở của kỳ (P18-3) |
| S05 | Kết quả `/student/results/[sessionId]` | CEFR, θ/SE/CI, 2 kỹ năng, chủ đề yếu, gợi ý AI, banner vùng biên | UCSV04 | `GET /sessions/:id/result` | Có `(student)/results/[sessionId]` | Không đổi |
| S06 | Xem lại đáp án `/student/results/[sessionId]/review` | Đáp án đúng/đã chọn + giải thích | UCSV05 | `GET …/review` | Có `…/review/page.tsx` | 🔶 K6 (`REVIEW_ENABLED`) |
| S07 | Lịch sử `/student/history` | Bảng các lần thi | UCSV06 | `GET /placement-profiles/…/history` | Có `(student)/history` | ⚠️ Có thể thêm cột "Kỳ thi" (chưa đề xuất chính thức, nêu để duyệt) |
| S15 | Lỗi chung | 403/404/500 | — | — | Có `403/page.tsx` (chỉ 403 thấy ở đây) | |
| S16 | **Đổi mật khẩu** `/change-password` | Nhập mật khẩu hiện tại + mới; **bắt buộc ở lần đăng nhập đầu**, chặn mọi route khác tới khi đổi | UCSV08 ⚠️ | `POST /auth/change-password` | **Chưa có** | ⚠️ ID, route (MD-13) và ID UC (MD-12) chờ duyệt. ⚠️ Chính sách độ dài mật khẩu: **Q-4 còn mở** (đề xuất ≥8). Dùng chung Student/Teacher/Admin. Lỗi `PASSWORD_CHANGE_REQUIRED` làm FE chuyển về đây |
| S17 | **Quên mật khẩu** `/forgot-password` | Nhập email → luôn báo "Nếu email tồn tại, chúng tôi đã gửi mã xác nhận" (202); chuyển sang S18 | UCSV09 ⚠️ | `POST /auth/forgot-password` | **Chưa có** | ✅ Theo **OTP 6 số** (DC-21): mã gửi email, TTL 10 phút. Có rate limit theo email + IP (`RATE_LIMITED`). Phản hồi y hệt dù email có tồn tại hay không (BR-14) |
| S18 | **Đặt lại mật khẩu** `/reset-password` | Nhập **email + mã OTP 6 số + mật khẩu mới**; xong về S01 (không tự đăng nhập) | UCSV09 ⚠️ | `POST /auth/reset-password` `{email,otp,newPassword}` | **Chưa có** | ✅ OTP dùng 1 lần, tối đa 5 lần nhập sai rồi hủy mã; lỗi `INVALID_RESET_OTP` (hết hạn/sai/đã hủy). Thành công xóa `mustChangePassword`. ⚠️ Độ dài mật khẩu mới: Q-4 |

## 4. Màn hình — Teacher (GV thường: S08, S10, S12–S14 chỉ xem; S11 và S33–S35 Hộp việc khi được giao)

| ID | Tên / Route thật | Mục đích và chức năng chính | UC | API chính | Mã nguồn | Ghi chú |
|---|---|---|---|---|---|---|
| S01 | Đăng nhập | Như Student | UCGV01 | `POST /auth/login` | Có | Như trên |
| S08 | Ngân hàng câu hỏi `/teacher/item-bank` (GV) và `/admin/item-bank` (Admin) | **Chỉ xem.** GV: chỉ câu/gói được giao cho mình (UCGV02); Admin: mọi câu (UCADM06). Danh sách, lọc (kỹ năng, CEFR, trạng thái 6 giá trị trừ `AI_REJECTED`, nguồn **AI sinh/Import file**, lô), tìm; **chỉ Admin** (`/admin/item-bank`) thấy nút "Tạo lô bằng AI" (S26), "Import đề từ file" (S27), liên kết "Lô cần xử lý" (S28); **GV (`/teacher/item-bank`) không thấy các nút/liên kết này**, chỉ có tìm kiếm, bộ lọc và danh sách câu được giao (BR-21). **Không** có Thêm/Xóa/Sửa/Nhân bản | UCGV02, UCADM06 | `GET /items` | Có (route cũ `/teacher/items`) | ⚠️ Đề xuất phiên 25 (DC-29, DC-32). 🔶 O7. Bỏ nút Xóa vì kế hoạch bản 5 không nêu (P25-2, chờ chốt) |
| ~~S09~~ | ~~Thêm câu hỏi `/teacher/items/new`~~ | **Đã bỏ** — không ai thêm từng câu bằng form (DC-32, #106) | ~~UCGV03~~ | — | (route cũ có trong mã) | ⛔ Bỏ theo DC-32; câu hỏi chỉ vào hệ thống qua S26/S27. Mã FE cũ cần xóa/vô hiệu (ngoài phạm vi file này) |
| S10 | Chi tiết câu hỏi (chỉ đọc) `/teacher/item-bank/[id]` (GV), `/admin/item-bank/[id]` (Admin) | **Chỉ đọc** (GV: câu được giao; mục kết quả AI C1/C2/C3 và lịch sử sự kiện chỉ Admin xem): nội dung, đáp án, giải thích, trạng thái (6), nguồn, lô, kết quả AI kiểm C1/C2/C3 (mã lý do, câu nghi trùng), lịch sử sự kiện, bản gốc so bản sửa, người duyệt/xác nhận/import. **Không** có Lưu/Sửa/Xóa/Nhân bản | UCGV02, UCADM06 | `GET /items/:id` | Có `[id]` (bản cũ có `/edit`) | ⚠️ Đề xuất phiên 25. `FINAL_APPROVED` cấm sửa (#64). "Nhân bản để sửa" bị bỏ vì kế hoạch bản 5 không nêu (muốn thay câu thì tạo lô mới) |
| S11 | **Duyệt từng câu trong gói (GV A)** `/teacher/tasks/reviews/[packageId]` | **GV A đúng người.** Hiện cờ mềm; **sửa** nội dung/đáp án/giải thích; `Lưu sửa` (kiểm lại luật cứng + trùng T1–T2); `Duyệt` (`FIRST_APPROVED`) / `Từ chối` (`REJECTED`, không lý do #56); trước/sau; quá hạn chỉ cảnh báo | UCGV14 (thay UCGV05) | `GET /me/review-tasks`, `PATCH /items/:id`, `POST /items/:id/approve` hoặc `reject` | **Lệch**: route thật `/teacher/review-queue` (cũ), mô tả cũ `/teacher/items/review` | ⚠️ Đề xuất phiên 25 (DC-33, DC-40…43). Lỗi: `NOT_ASSIGNED`, `DUPLICATE_AFTER_EDIT`, `INVALID_AFTER_EDIT`. Chỉ A sửa; B không sửa. Cần chốt một route (W4.3) |
| S12 | Báo cáo lớp `/teacher/reports` (Admin dùng chung, chờ chốt R-2) | Phân phối CEFR, chủ đề sai, xuất CSV; Teacher chỉ xem | UCGV07, UCGV08 | `GET /reports/class-distribution`, `…/error-patterns` | Có | ✅ **Bộ lọc "Kỳ thi"** (BR-13): `?examRoundId=`, mặc định toàn hệ thống. Tuan4 ghi "không có lọc theo kỳ" — **đảo theo #84** |
| S13 | Tìm sinh viên `/teacher/students` | Nhập MSSV chính xác | UCGV09 | `GET /placement-profiles/:code` | Có | 🔶 O6 |
| S14 | Hồ sơ sinh viên `/teacher/students/[studentId]` (tham số = MSSV, chờ chốt R-6; Admin dùng chung) | Hồ sơ + lịch sử | UCGV09 | như trên | **Chưa có** (chỉ thấy `students/page.tsx`) | |
| S33 | **Hộp việc — Cần duyệt (GV A)** `/teacher/tasks/reviews` | Danh sách lô được giao: số câu, đã quyết, hạn ("Quá hạn"), tiến độ; vào S11; nút **"Gửi cho B"** theo lô (tắt khi còn câu chưa quyết; gửi một lần; sau gửi chỉ đọc) | UCGV14 | `GET /me/review-tasks`, `POST /item-packages/mine/send` | **Chưa có** | ⚠️ Đề xuất. Lỗi `PACKAGE_INCOMPLETE`, `NOT_ASSIGNED`. Menu GV thường nay có mục **Hộp việc** |
| S34 | **Hộp việc — Cần xác nhận theo gói (GV B)** `/teacher/tasks/confirms` | Danh sách **gói** (mỗi GV A gửi một gói): lô, ngày gửi, đã xử lý x/y, hạn (từ ngày gửi gói), trạng thái gói | UCGV15 | `GET /me/confirm-packages` | **Chưa có** | ⚠️ Đề xuất. ✅ Hiển thị nhãn "Gói do GV [Họ tên A] gửi ngày dd/mm" (UCGV15 bước 2 đã ghi "kèm thông tin GV A"; P25-4 chốt có) |
| S35 | **Màn gói (GV B)** `/teacher/tasks/confirms/[packageId]` | Chỉ đọc; danh sách câu + cờ + dấu "A đã sửa"; **bản gốc so bản sửa**; `Xác nhận` (`SECOND_APPROVED`) / `Loại bỏ` (`REJECTED`, không lý do); **"Xác nhận tất cả câu còn lại"** (chỉ câu chưa quyết; ghi log hàng loạt). **Không sửa, không trả về A** | UCGV15 | `POST /items/:id/confirm` hoặc `remove`, `POST /item-packages/:id/confirm-all` | **Chưa có** | ⚠️ Đề xuất (DC-33, DC-42). Lỗi `NOT_ASSIGNED` |
| S16–S18 | Đổi / Quên / Đặt lại mật khẩu | Như Student (dùng chung) | UCSV08/09 ⚠️ | như trên | Chưa có | MD-12 |

## 5. Màn hình — Admin (của trường)

Ghi chú phạm vi: hệ thống chỉ có **một trường** (DC-19), nên không còn phạm vi theo đơn vị.

| ID | Tên / Route | Chức năng | UC | API | Mã nguồn | Ghi chú |
|---|---|---|---|---|---|---|
| S01 | Đăng nhập | Như trên | UCADM01 | `POST /auth/login` | Có | |
| S36 (cũ E2) | Tổng quan hệ thống `/admin/dashboard` | 4 số, phân phối CEFR, trạng thái câu hỏi | UCADM05 | `GET /reports/…` | Chưa thấy | 🔶 Màn mới từ Tuan4 (chưa xác nhận giữ) |
| E3–E7 | Bản Admin của S08, S10, S12–S14 (S08, S10 chỉ Admin có, chỉ xem) | Như Teacher (không còn bộ chọn/cột Đơn vị) | UCADM04–06 | như Teacher | Dùng chung | ✅ DC-19. Duyệt/xác nhận câu **không còn** là việc của Admin (DC-29) |
| S20 | **Danh sách kỳ thi** `/admin/exam-rounds` | Liệt kê kỳ thi: tên, giờ mở/đóng, thời lượng, trạng thái, số SV; nút "Tạo kỳ thi" | UCADM15 ⚠️ | `GET /exam-rounds` | **Chưa có** | ⚠️ ID/route/UC (MD-12, MD-13). Trạng thái hiển thị = `effectiveStatus` (DRAFT/SCHEDULED/OPEN/CLOSED) ✅ DC-10. Thêm mục "Kỳ thi" ở thanh bên (chỉ Admin) |
| S21 | **Tạo / sửa kỳ thi** `/admin/exam-rounds/new`, `/[id]/edit` | Nhập tên, giờ mở, giờ đóng, **thời lượng làm bài `durationMinutes`** (bắt buộc, điền sẵn 45; 5..180; không vượt closes − opens; cột DB `NOT NULL DEFAULT 45`) | UCADM15 ⚠️ | `POST/PATCH /exam-rounds` | **Chưa có** | ✅ Thời lượng theo kỳ (T2, DC-20). Quy tắc sửa theo trạng thái (BR-08, chốt ở W1.5): DRAFT sửa tự do; SCHEDULED chỉ sửa tên và kéo dài giờ đóng; CLOSED không sửa. Lỗi: giờ đóng ≤ giờ mở; thời lượng ngoài khoảng |
| S22 | **Chi tiết kỳ thi / Theo dõi dự thi** `/admin/exam-rounds/[id]` | Thông tin kỳ; bảng SV (MSSV, tên, trạng thái: chưa thi / đang thi / hoàn thành / bỏ dở); nút Công bố, Đóng kỳ, Import danh sách (S23); **"Gỡ SV" chỉ bật ở dòng trạng thái "Chưa thi"**; bộ lọc trạng thái và ô tìm theo MSSV/tên; ô tick từng dòng và "chọn tất cả theo bộ lọc"; nút **"Xuất CSV"** và **"Xuất Excel"**: có dòng được tick thì chỉ xuất các dòng đó (một hoặc nhiều sinh viên), không tick thì xuất toàn bộ danh sách đang lọc; cột MSSV, Họ tên, Trạng thái dự thi, Mức CEFR, θ, SE, Thời điểm bắt đầu, Thời điểm nộp; chỉ Admin; ⚠️ UC/API xuất là đề xuất 18/10 (SV đã có phiên thì khóa ngoại `fk_session_participant` chặn xóa; dòng "Đang thi/Hoàn thành/Bỏ dở" ẩn nút hoặc vô hiệu kèm tooltip; ẩn hết khi kỳ CLOSED) | UCADM15, UCADM17 ⚠️ | `GET /exam-rounds/:id`, `…/participants`, `POST …/publish|close`, `DELETE …/participants/:studentId` | **Chưa có** | ✅ Gỡ SV (MD-07). ⚠️ **Q-2 còn mở:** đóng kỳ thủ công khi có phiên đang chạy — cắt ngay hay chạy tới `expires_at` (đề xuất: để chạy). Công bố cần ≥1 SV |
| S23 | **Import danh sách thi (lưới tạm)** `/admin/exam-rounds/[id]/import` | Nút **Tải file mẫu** (`import-roster.xlsx`: MSSV, Ghi chú); tải **một hoặc nhiều** file `.xlsx` (cột MSSV, Ghi chú) cộng dồn vào lưới tạm; xem lưới; xóa dòng / xóa cả lưới; **popup** liệt kê dòng bị loại (số dòng + lý do); bấm **Lưu** mới ghi DB | UCADM16 ⚠️ | `POST …/participants/import/upload`, `GET …/import/grid`, `DELETE …/import/grid[/:rowKey]`, `POST …/import/save` | **Chưa có** | ✅ DC-22: dòng lỗi (thiếu cột, sai định dạng, trùng trong file) bị loại khỏi lưới; **MSSV không tồn tại** bị loại + popup; **MSSV đã có trong kỳ** bị loại + popup "đã có trong kỳ"; dòng đã có trong lưới thì bỏ qua khi tải thêm file. Lưu = một transaction; lưới rỗng thì từ chối (`IMPORT_GRID_EMPTY`); hết TTL ~30' → `IMPORT_GRID_EXPIRED` (410), tải lại. Giới hạn `.xlsx` ≤2 MB, ≤1000 dòng (MD-08; lỗi `IMPORT_FILE_INVALID`) |
| S19 | **Import tài khoản (SV, GV) (lưới tạm)** `/admin/users/import` (`?kind=STUDENT\|TEACHER`; cũ `/admin/import-users`) | **Chọn loại tài khoản (Sinh viên / Giảng viên)**, rồi tải **một hoặc nhiều** file `.xlsx` (file SV: MSSV, Họ tên, Email; file GV: Mã GV (`teacherCode`), Họ tên, Email) cộng dồn vào lưới tạm của loại đó (mỗi loại một lưới riêng); xem lưới; xóa dòng / xóa cả lưới; **popup** dòng bị loại (số dòng + lý do) và popup "tài khoản đã tồn tại" (email/MSSV/`teacherCode` trùng DB); bấm **Lưu** → tạo tài khoản + xếp hàng email mật khẩu tạm; kết quả (số tạo, số email đã xếp hàng); tải file mẫu (**hai file mẫu: SV và GV**) | UCADM08 ⚠️ | `POST /users/import/upload` (thêm `kind=STUDENT\|TEACHER`), `GET /users/import/grid`, `DELETE /users/import/grid[/:rowKey]`, `POST /users/import/save` (đề xuất; lưới khóa theo adminId + kind) | **Chưa có** | ✅ DC-22, DC-24 (#99): chỉ **tạo mới SV hoặc GV** (đảo "không import giảng viên" của DC-05), không cập nhật tài khoản có sẵn; dòng lỗi/đã tồn tại không vào lưới nên không chặn Lưu (BR-04 mới); dòng đã có trong lưới thì bỏ qua khi tải thêm. ✅ Email mật khẩu tạm **chỉ xếp hàng sau Lưu**. Lưới rỗng → `IMPORT_GRID_EMPTY`; hết TTL → `IMPORT_GRID_EXPIRED`. ⚠️ Hiển thị trạng thái gửi email thất bại cho Admin (BR-05) — chi tiết chốt ở UI. ⚠️ SMTP: Q-5 còn mở |
| S24 | **Quản lý tài khoản** `/admin/users/students`, `/admin/users/teachers` (cũ `/admin/students`, `/admin/teachers`) | Tab Sinh viên / Giảng viên: danh sách, tìm theo MSSV hoặc email; sửa họ tên/email; khóa/mở khóa (`is_active`); gửi lại mật khẩu tạm; với GV: **Nâng lên Admin / Thu hồi Admin**; nút **"Thêm sinh viên"** (tab SV) và **"Thêm giảng viên"** (tab GV) mở **form tạo từng người** (SV: MSSV, họ tên, email; GV: mã GV, họ tên, email; trùng email/MSSV/mã GV ⇒ báo lỗi tại form; sau lưu sinh mật khẩu tạm, xếp hàng email); nút "Import" sang S19 (cả hai tab, chọn sẵn loại theo tab); hiện trạng thái email và đã đổi mật khẩu | UCADM09 ⚠️ | `GET /students`, `GET /teachers`, `POST /students`, `POST /teachers` (tạo từng người, đề xuất DC-24), `PATCH …/:id`, `POST …/lock\|unlock\|resend-temporary-password`, `PATCH /users/:id/role` | **Chưa có** | ✅ DC-19, BR-17/18/19. ✅ Khóa = `users.is_active` (Q-8, DC-23). Không thu hồi được Admin cuối; Admin không tự thu hồi mình |
| ~~S25~~ | ~~Gán QTV đơn vị~~ | — | UCADM10 đã bỏ | — | — | ⛔ **Bỏ theo DC-19**; nâng/thu hồi Admin nằm ở S24 |
| S26 | **Tạo lô bằng AI** `/admin/item-batches/generate` | Nhập kỹ năng, CEFR, chủ đề (tùy chọn), số câu N; "Tạo lô" → lô `GENERATING` → S29. Không chọn GV ở bước này | UCADM11 ⚠️ | `POST /item-batches` | **Chưa có** | ⚠️ Đề xuất. Lỗi `BATCH_BUDGET_EXCEEDED`. Mọi ngưỡng AI chờ chốt (Q-7) |
| S27 | **Import đề từ file (lưới tạm)** `/admin/item-batches/import` | Nút **Tải file mẫu** (`import-items.xlsx`: Skill, CEFR, Topic, Câu hỏi, A, B, C, D, Đáp án, Giải thích (tùy chọn), irt_b (tùy chọn); tên cột là đề xuất); tải nhiều file `.xlsx` cộng dồn; kiểm C2 tầng 1–4 ngay khi tải (dòng lỗi/trùng bị loại + popup; trùng gần đúng = cờ mềm); `Lưu` → tạo lô `IMPORTED`, chạy C2 tầng 5 → S29. **GV không có màn này** | UCADM12 ⚠️ | `POST /item-imports/upload`, `GET`/`DELETE /item-imports/grid[/:rowKey]`, `POST /item-imports/save` | **Chưa có** | ⚠️ Đề xuất (DC-28). Lỗi `IMPORT_FILE_INVALID`, `IMPORT_GRID_EXPIRED`, `IMPORT_GRID_EMPTY`. `irt_b` ngoài [−4, +4] bị loại (DC-34) |
| S28 | **Danh sách lô** `/admin/item-batches` | Bảng lô: nguồn, kỹ năng + CEFR, số câu, trạng thái lô, tiến độ, hạn gần nhất ("Quá hạn"); lọc trạng thái | UCADM13 ⚠️ | `GET /item-batches` | **Chưa có** | ⚠️ Đề xuất. Menu Admin mục "Lô câu hỏi" |
| S29 | **Chi tiết lô: tiến độ, câu, AI đã loại** `/admin/item-batches/[id]` | Thanh tiến trình; đếm theo trạng thái câu; tab Câu hỏi / Theo GV và gói / **AI đã loại** (chỉ Admin) / Thống kê (tỉ lệ loại theo tầng AI, theo A, theo B); nút Giao việc, Chỉnh hạn, Giao lại, Kiểm tra; **"Ép gửi gói" đặt trên từng dòng gói** của tab Theo GV và gói (không phải nút cấp lô), kèm modal xác nhận "GV A mới duyệt X/Y câu: ép gửi sẽ chuyển X câu đã duyệt sang GV B, Y câu chưa quyết nằm lại trong lô" | UCADM13 ⚠️ | `GET /item-batches/:id`, `GET …/ai-rejected` | **Chưa có** | ⚠️ Đề xuất. "Ép gửi gói" (`POST /item-packages/:id/force-send`) là đề xuất Q-2 của kế hoạch AI |
| S30 | **Giao việc (xem trước phân bổ) và giao lại** `/admin/item-batches/[id]/assign` | Chọn nhóm A (nhiều GV), một GV B (∉ nhóm A, bắt buộc), `reviewDays`, `confirmDays`; **xem trước phân bổ** (chia đều, chênh ≤ 1 câu; hạn A cuối ngày giao + reviewDays, hạn B tính từ ngày gửi gói); `Xác nhận giao`; tab Giao lại (chọn GV A bị thu hồi việc ─► hệ thống liệt kê số câu chưa xử lý ─► chọn GV A thay thế hoặc đổi GV B của gói chưa gửi (B ∉ nhóm A) ─► đặt lại `reviewDays`/`confirmDays` ─► xác nhận; hạn tính lại từ ngày giao lại, gửi email mới, ghi REASSIGN). Danh sách chọn GV A và GV B chỉ gồm tài khoản `role = TEACHER` ✅ P25-1 (chốt 18/10: Admin không làm A/B) | UCADM13 ⚠️ | `GET …/assign-preview`, `POST …/assign`, `POST …/reassign` | **Chưa có** | ⚠️ Đề xuất (DC-40, DC-41). Lỗi `CONFIRMER_IN_REVIEW_GROUP`. Admin có được chọn làm A/B không: chưa quy định (P25-1) |
| S31 | **Chỉnh hạn** (ngăn bên trong S29) | `reviewDays`/`confirmDays` mới, chỉ áp dụng việc chưa xử lý; tính lại `due_at`, đặt lại lịch nhắc 24 giờ | UCADM13 ⚠️ | `PATCH /item-batches/:id/deadlines` | **Chưa có** | ⚠️ Đề xuất (DC-37, DC-38) |
| S32 | **Kiểm tra (C3) và Import cuối** `/admin/item-batches/[id]/final-check` | Chỉ khi `READY_TO_FINALIZE`; `Kiểm tra` → báo cáo theo câu (Qua/Cờ mềm/Lỗi cứng, mã lý do, câu nghi trùng, bản gốc so bản sửa), theo gói, thống kê; lỗi mềm: `Chấp nhận`/`Loại`; `Import` khóa tới khi có báo cáo còn hiệu lực; câu chưa xử lý không được import | UCADM14 ⚠️ | `POST`/`GET …/final-check`, `POST /items/:id/decision`, `POST …/import` | **Chưa có** | ⚠️ Đề xuất (DC-44, DC-45). Lỗi `FINAL_CHECK_REQUIRED`, `FINAL_CHECK_STALE`, `BATCH_NOT_READY_TO_FINALIZE`. O2 (lỗi cứng tự `AI_REJECTED`, lỗi mềm Admin quyết) đã chấp nhận (Q-1) |

## 6. Trạng thái giao diện cần có cho màn mới (để sinh UI và viết test)

| Màn | Rỗng | Đang tải | Lỗi | Thành công |
|---|---|---|---|---|
| S16 | — | Đang gửi | Mật khẩu hiện tại sai; mật khẩu mới trùng cũ; không đạt chính sách ⚠️ Q-4 | Chuyển trang chủ, cấp lại token |
| S17 | — | Đang gửi | Quá nhiều yêu cầu (`RATE_LIMITED`) | Thông báo trung tính, chuyển S18 |
| S18 | — | Đang gửi | Mã sai/hết hạn/đã hủy (`INVALID_RESET_OTP`); mật khẩu mới không đạt chính sách ⚠️ Q-4 | Về S01 |
| S19 | Lưới trống (chưa tải file; mỗi loại SV/GV một lưới) | Đang phân tích file | File sai định dạng/quá cỡ/quá dòng (`IMPORT_FILE_INVALID`); lưới hết hạn (`IMPORT_GRID_EXPIRED`); Lưu khi lưới rỗng (`IMPORT_GRID_EMPTY`); có dòng bị loại → popup | Lưới cập nhật; sau Lưu hiện kết quả (số tạo, số email xếp hàng) |
| S20 | "Chưa có kỳ thi nào" | Skeleton | Lỗi tải | Danh sách |
| S21 | — | Đang lưu | Giờ không hợp lệ; thời lượng để trống, ngoài 5..180 hoặc vượt khoảng mở–đóng | Toast, về S22 |
| S22 | "Chưa có sinh viên trong kỳ" | Skeleton | Lỗi tải; thao tác sai trạng thái | Cập nhật bảng |
| S23 | Lưới trống (chưa tải file) | Đang phân tích file | Như S19; popup MSSV không tồn tại / đã có trong kỳ | Lưới cập nhật; sau Lưu quay S22 |
| S24 (tab SV) | "Chưa có sinh viên" | Skeleton | 403 (TEACHER); lỗi tải; form Thêm sinh viên: thiếu trường, email/MSSV đã tồn tại | Cập nhật danh sách |
| S24 (tab GV) | "Chưa có giảng viên" | Skeleton | 403 (TEACHER); thu hồi Admin cuối bị từ chối; form Thêm giảng viên: thiếu trường, email/mã GV đã tồn tại | Cập nhật danh sách |
| S11 | "Bạn chưa có câu nào cần duyệt." | Skeleton | Không đúng người (`NOT_ASSIGNED` → 403); lưu sửa lỗi (`INVALID_AFTER_EDIT`, `DUPLICATE_AFTER_EDIT`: chặn Duyệt); lỗi mạng | Chuyển câu chưa quyết kế tiếp; hết câu về S33 |
| S26 | — | Đang tạo lô | Thiếu trường; `BATCH_BUDGET_EXCEEDED`; lỗi mạng | Chuyển S29, lô "Đang sinh" |
| S27 | Lưới trống (chưa tải file) | Đang phân tích file | `IMPORT_FILE_INVALID`; `IMPORT_GRID_EXPIRED`; `IMPORT_GRID_EMPTY`; popup dòng bị loại | Lưới cập nhật; sau Lưu chuyển S29 |
| S28 | "Chưa có lô câu hỏi nào." | Skeleton | Lỗi tải | Danh sách |
| S29 | Tab AI đã loại: "Chưa có câu nào bị AI loại."; tab Câu hỏi rỗng | Skeleton; lô đang sinh/kiểm hiện tiến độ | Lô lỗi (`FAILED`), lô thiếu câu (`PARTIAL`); lỗi tải; 404 | Cập nhật số đếm |
| S30 | "Chưa có giảng viên nào để giao việc." | Đang tải danh sách GV; đang tạo phân bổ | `CONFIRMER_IN_REVIEW_GROUP`; thiếu GV B; số ngày không hợp lệ | Toast "Đã giao việc", lô `IN_REVIEW` |
| S31 | — | Đang lưu | Số ngày không hợp lệ | Toast "Đã cập nhật hạn." |
| S32 | Chưa có báo cáo C3 | Đang kiểm tra (spinner) | `BATCH_NOT_READY_TO_FINALIZE`; `FINAL_CHECK_REQUIRED`; `FINAL_CHECK_STALE`; tranh chấp Import | Báo cáo hiển thị; "Đã import N câu vào ngân hàng." |
| S33 | "Bạn chưa có câu nào cần duyệt." | Skeleton | `PACKAGE_INCOMPLETE` khi Gửi; lỗi tải | Thẻ lô chuyển "Đã gửi" |
| S34 | "Bạn chưa có gói nào cần xác nhận." | Skeleton | Lỗi tải | Danh sách gói |
| S35 | — | Skeleton | `NOT_ASSIGNED` (403); lỗi mạng khi xác nhận | Dòng chuyển trạng thái; "Gói đã hoàn tất." |

## 7. Ma trận UC ↔ màn ↔ API ↔ role

| UC | Màn | API | Role | Thẻ |
|---|---|---|---|---|
| UCSV01/UCGV01/UCADM01 | S01 | `POST /auth/login` | Cả 3 | ✅ (sửa theo #85) |
| UCSV08 | S16 | `POST /auth/change-password` | Cả 3 | ⚠️ ID UC (MD-12) |
| UCSV09 | S17, S18 | `POST /auth/forgot-password`, `/reset-password` | Cả 3 | ✅ OTP (DC-21); ⚠️ ID UC (MD-12) |
| UCSV02, UCSV07 | S02, S03 | `GET /exam-rounds/mine`, `POST /sessions`, `GET /sessions/active` | Student | ✅ (DC-07) |
| UCSV03 | S04 | `GET next-item`, `POST responses` | Student | ✅ (T2, DC-20) |
| UCSV04–06 | S05–S07 | result / review / history | Student | ✅ |
| UCGV02, UCADM06 (UCGV04 là bước con của UCGV14; UCGV06 ngoài phạm vi) | S08, S10 | `GET /items…` (chỉ xem) | Teacher (câu được giao), Admin (mọi câu) | ✅ đã sửa theo quyền mới (không sửa/xóa/nhân bản) |
| ~~UCGV03~~ | ~~S09~~ | — | — | ⛔ bỏ (DC-32) |
| UCGV14 (thay UCGV05) | S11, S33 | `/me/review-tasks`, `PATCH /items/:id`, `…/approve` hoặc `reject`, `/item-packages/mine/send` | GV A | ⚠️ ID UC đề xuất |
| UCGV15 | S34, S35 | `/me/confirm-packages`, `…/confirm` hoặc `remove`, `…/confirm-all` | GV B | ⚠️ ID UC đề xuất |
| UCADM11 | S26 | `POST /item-batches` | Admin | ⚠️ ID UC đề xuất |
| UCADM12 | S27 | `/item-imports/{upload,grid,save}` | Admin | ✅ DC-22, DC-28; ⚠️ ID UC đề xuất |
| UCADM13 | S28, S29, S30, S31 | `/item-batches/:id/{assign-preview,assign,reassign,deadlines}`, `/item-packages/:id/force-send` | Admin | ⚠️ ID UC đề xuất |
| UCADM14 | S32 | `/item-batches/:id/{final-check,import}`, `/items/:id/decision` | Admin | ⚠️ ID UC đề xuất |
| UCGV07–08, UCADM05 | S12 (E2/E5) | `/reports/…?examRoundId=` | Teacher, Admin | ✅ lọc theo kỳ (BR-13) |
| UCGV09, UCADM04 | S13, S14 | `/placement-profiles/…` | Teacher, Admin | ✅ |
| UCADM15 | S20, S21, S22 | `/exam-rounds…` | **Admin** (DC-18) | ⚠️ ID UC/route |
| UCADM16 | S23 | `…/participants/import/{upload,grid,save}` | **Admin** (DC-18) | ✅ DC-22; ⚠️ ID UC/route |
| UCADM17 | S22 | `…/participants` | **Admin** (DC-18) | ⚠️ ID UC/route |
| UCADM08 (import SV, GV) | S19 | `/users/import/{upload,grid,save}` (+ `kind`) | Admin | ✅ DC-22; ⚠️ ID UC/route |
| UCADM09 (gồm tạo từng người, đề xuất) | S24 | `/students…`, `/teachers…` (gồm `POST`), `PATCH /users/:id/role` | Admin | ✅ Q-8 chốt; ⚠️ ID UC/route |
| ~~UCADM10~~ | ~~S25~~ | — | — | ⛔ bỏ (DC-19) |

## 8. Danh sách điểm chưa duyệt / cần xác nhận (tổng hợp)

| Mã | Nội dung | Ảnh hưởng màn |
|---|---|---|
| W0.1 | Duyệt kế hoạch (chưa ghi nhận trong kế hoạch); các MD còn lại | ID/route/UC mới trên S16–S24 |
| MD-12 | ID UC mới: UCADM08–09, UCADM15–17, UCSV08–09 (UCADM10 đã bỏ, DC-19) | S16–S24 |
| MD-13 | ID/route màn mới S16–S24 (S25 đã bỏ) | S16–S24 |
| Q-2 | Đóng kỳ thủ công khi có phiên đang chạy (đề xuất: để chạy tới `expires_at`) | S22 |
| Q-4 | Chính sách độ dài mật khẩu (đề xuất ≥8) | S16, S18 |
| Q-5 | Nhà cung cấp SMTP (hạn mức chưa kiểm chứng) | S19 (gửi email), S17 |
| Lệch route | S03 (`/exam/start` chưa có), S11 (`review-queue` vs `items/review`), S14 (chưa có) | S03, S11, S14 |
| DC-18/19 (bị DC-27…DC-45 thay phần duyệt câu) | ~~Admin tự duyệt~~ → từ phiên 25: Admin không soạn/duyệt nội dung, GV A duyệt và GV B xác nhận; BE chặn `TEACHER` ở `/exam-rounds` và API Admin của lô; hệ thống đơn trường | S08, S10, S11, S20–S24, S26–S35 |
| Tuan4 | Các 🔶 O2, O3, O4, O6, O7, O8, K6; màn E2 giữ hay bỏ | Như trên |
| Q-7…Q-10 (kế hoạch AI) | Ngưỡng/tham số AI kiểm; nguồn ngân hàng tham chiếu + bản quyền; mô hình embedding; `pg_trgm` trên staging | S26, S27, S29, S32 (UI không hiển thị con số cứng) |
| ✅ Quy tắc hạn (18/10) | Đến hạn mọi GV phải hoàn thành, **không có "câu tồn đọng" cần màn/luồng xử lý riêng sau Import**; chỉnh hạn, giao lại, ép gửi gói chỉ là biện pháp dự phòng trước khi chạy C3. Đã gỡ banner "Giao lại / Loại các câu còn lại" khỏi S29, S32 | S29, S32 |
| ~~P25-1~~ | ~~Admin có được chọn làm GV A/B không; Admin có mục Hộp việc không~~. → **Đã chốt 18/10: không** (khớp ma trận quyền 9b.16; danh sách chọn A và B chỉ `role = TEACHER`; Admin không có Hộp việc) | S30, menu Admin |
| P25-2 | Admin có xóa được câu `REJECTED`/lô không (bản 5 không nêu) | S08, S29 |
| P25-3 | A có sửa được kỹ năng/CEFR/chủ đề/`irt_b` không (bản 5: chỉ nội dung, đáp án, giải thích) | S11 |
| P25-4 | ~~B có thấy tên GV A trên gói không~~ → **chốt có** (UCGV15 bước 2) | S34, S35 |
| ✅ P18-1 | **Xuất kết quả dự thi của một kỳ ở S22**: **đã quyết 18/10: có thêm.** Cách làm: **đồng bộ** (tải file ngay), xuất theo bộ lọc hoặc theo các dòng được tick (một hoặc nhiều sinh viên), định dạng **CSV và Excel (.xlsx)**. Đã thêm vào S22, UCADM17 (luồng thay thế và tiêu chí chấp nhận) và SRS (API `GET /exam-rounds/:id/participants/export`, đề xuất). Còn lại: chống CSV injection (SRS 15.3) áp cho cả hai định dạng; giới hạn số dòng tối đa chờ chốt | S22, S12 |
| ~~P18-2~~ | **Lọc trạng thái gửi email mật khẩu tạm và nút "Gửi lại hàng loạt" ở S24**: SRS chỉ có "ghi nhật ký kiểm toán" (BR-05, UCADM08 ngoại lệ 10a), schema `User` **không có** cột trạng thái email, chưa có bảng nhật ký; gửi lại hàng loạt đổi mật khẩu tạm của nhiều tài khoản. **Đã chốt 18/10: chỉ giữ "Gửi lại mật khẩu tạm" từng tài khoản**, không thêm lọc trạng thái email và gửi hàng loạt, không đổi schema | S24, S19 |
| P18-3 | Route S04 `/student/exams/[roundId]/take` nhưng API và UCSV07 dùng `sessionId`; **Đã sửa 19/10:** bảng UC spec UCSV02, UCSV04–07 đã dùng `/student/...`; còn lại việc S04 theo `roundId`, API theo `sessionId` | S02–S07 |
| Mã FE cũ | Route/mã FE `teacher/items/new`, `items/[id]/edit`, `review-queue` tương ứng màn đã bỏ/đổi; **không sửa mã trong phiên này** | S09, S10, S11 |

**Đã chốt, gỡ khỏi danh sách:** D-T = T2 (DC-20, #93), D-FP = OTP 6 số (DC-21, #94), Q-1 = lưới tạm (DC-22, #98), Q-8 = `users.is_active` (DC-23, #98), MD-06 (`SKIPPED`) bị DC-22 thay, Q-6/Q-7/Q-9 đóng theo DC-19. Q-3 (định dạng sơ đồ mới) không ảnh hưởng màn hình.

## 9. Việc còn lại với file này
- **W4.3:** đối chiếu ID/route với 3 file Tuan4 bằng script, chốt route S03/S11/S14.
- **W1.16:** 3 file mô tả giao diện Tuan4 đã cập nhật ở phiên 22 (S01–S04, S12; S16–S24); cần chạy đối chiếu W4.3.
- **W4.4 người:** review. Sau khi duyệt W0.1 và chốt Q-2/Q-4/Q-5, gỡ các thẻ ⚠️ còn lại.
