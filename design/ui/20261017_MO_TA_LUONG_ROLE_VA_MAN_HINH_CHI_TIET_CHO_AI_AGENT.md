# MÔ TẢ LUỒNG HOẠT ĐỘNG THEO ROLE, NGHIỆP VỤ VÀ MÀN HÌNH CHI TIẾT — DÀNH CHO AI AGENT SINH GIAO DIỆN

> **Ngày lập:** 2026-10-17 (Tuần 5/12). **Phiên bản:** 1.1 (19/10/2026; bản tổng hợp, thay thế vai trò "nguồn mô tả UI" của 3 file Tuan4 và `Tuan5/DANH_SACH_MAN_HINH_THEO_ROLE.md`; các file đó vẫn giữ làm lịch sử/đối chiếu).
> **Trạng thái:** ⚠️ Bản làm việc, **chưa có người review**. Soạn có hỗ trợ AI, cần thành viên rà soát trước khi dùng làm đầu vào chính thức cho sinh mã.
> **Mục tiêu:** một file duy nhất để AI Agent (v0, Claude, Cursor, Figma Make…) đọc là sinh được đúng giao diện: luồng từng role, nghiệp vụ, và từng màn hình đến mức từng thành phần (nhãn, ô nhập, quy tắc bật/tắt nút, thông báo, trạng thái).
> **Nguồn tổng hợp (theo thứ tự ưu tiên khi mâu thuẫn):**
> 1. `Update/20261016_BAN_CHOT_QUYET_DINH_DONG_BO_TOAN_DIEN_GUI_TEAMMATE.md` (+ Phụ lục của Phương) — quyết định chính thức 16/10/2026.
> 2. `Update/SRS_TLCN_v3.0.md` (Mục IXb: BR-01…BR-30, mã lỗi; Mục X: API) và `Update/20261016_MoHinhHoaYeuCau.docx` (UC).
> 3. `Update/KE_HOACH_CAU_TRUC_DU_AN.md` (cấu trúc FE đích, ma trận UC ↔ F-ID ↔ route).
> 4. `Tuan5/KE_HOACH_SINH_VA_DUYET_DE_AI.md` (luồng lô/gói/duyệt), `Tuan5/DANH_SACH_MAN_HINH_THEO_ROLE.md` (S01–S35), `Tuan4/20261010_MO_TA_MAN_HINH_TOI_GIAN_THEO_ROLE.md` (bố cục, copy, ID kiểm thử).
> **Cập nhật 2026-10-18 (đồng bộ #119–#121):** S22 (Gỡ SV chỉ "Chưa thi", lọc, tick, xuất CSV/Excel), S24 (bỏ cột trạng thái email), S32 và Mục 4.5-F (bỏ luồng "câu tồn đọng"), S34/S35 (hiện tên GV A), P25-1 và P25-4 đã chốt. Backup: `Update/_BACKUP_20261018/`.
> **Cập nhật 2026-10-19 (v1.1, đồng bộ lại với SRS v3.0, đặc tả UC 30 bảng, `schema.prisma`, #115–#121):** sửa 6 chỗ lệch (Mục 4.1-b, 4.2, 4.5-A/B/D, menu GV đã chốt, S10); thêm bổ sung chi tiết cho S05, S06, S07, S12; **thêm Mục 4.7** (quy tắc BR-01…BR-30 → hành vi giao diện), **Mục 4.8** (tình huống ngoại lệ và biên theo role), **Phụ lục E** (30 UC ↔ màn ↔ API ↔ BR), **Phụ lục F** (trường hiển thị ↔ cột schema). Điểm mới cần chốt: BR-05 (Mục 9). Backup: `Update/_BACKUP_20261019/`.
> **Giới hạn trung thực:** chưa chạy FE; chưa sinh thử UI từ file này; mọi số liệu trong ví dụ là **dữ liệu mẫu (mock)**; tên màn/route/nhãn tiếng Việt mới là đề xuất cho tới khi nhóm duyệt W0.1.

---

## 0. CÁCH ĐỌC FILE NÀY (DÀNH CHO AI AGENT)

### 0.1. Quy tắc bắt buộc khi sinh giao diện
1. **Chỉ sinh các màn có trong Mục 5–7.** Không thêm: đăng ký tự do, đăng nhập Google/SSO/mạng xã hội, thanh toán, chat, bảng xếp hạng, chế độ luyện tập, cấu hình hệ thống, chuông thông báo thời gian thực, bộ chọn Đơn vị/trường (hệ thống **một trường**), chế độ tối.
2. **Điểm chưa chốt (thẻ `⚠️` / `TODO-CONFIRM`, tổng hợp ở Mục 9): Agent KHÔNG tự quyết.** Dùng đúng giá trị mặc định đã ghi, thêm comment `// TODO-CONFIRM <mã>` trong mã (không hiển thị cho người dùng cuối), và báo lại danh sách điểm đó khi bàn giao.
3. **Không bịa dữ liệu thật.** Dùng dữ liệu mẫu (mock) trong từng màn; gắn cờ `MOCK` ở nơi tập dữ liệu được định nghĩa. Mật khẩu tạm **không bao giờ hiển thị** trên màn hình, trong ví dụ, hay trong log.
4. **Mọi màn có đủ 5 trạng thái** (Mục 2.6): đang tải (skeleton), có dữ liệu, rỗng, lỗi (có nút "Thử lại"), mất kết nối. Mỗi màn dưới đây chỉ liệt kê **phần khác/đặc thù**.
5. **Mỗi màn tối đa 1 nút hành động chính** (màu xanh đặc). Nút nguy hiểm (Từ chối, Loại bỏ, Khóa, Xóa lưới) dùng viền/chữ đỏ, luôn có hộp xác nhận.
6. **Không dùng màu làm tín hiệu duy nhất:** mọi huy hiệu trạng thái/CEFR/đúng–sai luôn kèm chữ hoặc biểu tượng.
7. **Quyền truy cập do route guard + API quyết định, UI chỉ phản ánh.** Vào route sai vai trò/việc không giao cho mình → trang 403 (S15). UI không được là lớp bảo vệ duy nhất.
8. **Thứ tự sinh đề xuất:** làm khối nền (Mục 2) trước, rồi mỗi lần 2–3 màn theo Mục 8; sau mỗi lượt đối chiếu AC của màn.

### 0.2. Ký hiệu trạng thái trong file
| Ký hiệu | Nghĩa |
|---|---|
| (không thẻ) | Đã chốt theo SRS v3.0 / bản chốt 16/10 / kế hoạch Tuần 5 |
| `⚠️ ĐX` | **Đề xuất** của AI hoặc tên/route/nhãn mới chưa được nhóm duyệt (W0.1, MD-12, MD-13); dùng được nhưng có thể đổi |
| `🔶 TODO-CONFIRM <mã>` | Điểm **mở** thật sự, chưa có quyết định; xem Mục 9 để biết mặc định tạm dùng |
| `[D]` | Chi tiết giao diện do file này **suy ra** để đủ sinh UI (cỡ, thứ tự, vi mô); không phải quy tắc nghiệp vụ, đổi được mà không ảnh hưởng SRS |

### 0.3. Cách đọc đặc tả một màn (Mục 6–7)
Mỗi màn có cùng khuôn: **(a) Thông tin chung** (route, file Next.js, guard, layout, API, UC) → **(b) Bố cục** (ASCII) → **(c) Bảng thành phần** (từ trên xuống, từng ô/nút: `testid`, nhãn, quy tắc) → **(d) Hành động** (nút → API → thành công/lỗi) → **(e) Trạng thái đặc thù** → **(f) Dữ liệu mẫu** → **(g) Tiêu chí chấp nhận (AC)**.

---

## 1. TỔNG QUAN HỆ THỐNG, ROLE VÀ PHÂN QUYỀN

### 1.1. Hệ thống
**Adaptive Placement Test** — kiểm tra xếp lớp tiếng Anh thích ứng (CAT, mô hình Rasch), xếp mức theo thang **CEFR: Pre-A1, A1, A2, B1, B2, C1+**. Hai kỹ năng: **Từ vựng (Vocabulary)** và **Ngữ pháp (Grammar)** (không có Writing trong Tiểu luận). Mỗi bài thi: tối đa 25 câu, có thể dừng sớm; thời lượng do **kỳ thi** quy định (`durationMinutes`, mặc định 45, 5–180). Hệ thống **đơn trường**; không có đăng ký tự do — **tài khoản do Admin tạo** (từng người hoặc import).

### 1.2. Ba role (không có role "Trưởng bộ môn", không có `/hod/`)
| Role | Là ai | Làm được gì (tóm tắt) | Điều hướng |
|---|---|---|---|
| **STUDENT** | Sinh viên | Chỉ dữ liệu của chính mình; chỉ thi trong kỳ mình thuộc; xem kết quả, đáp án, lịch sử; đổi/quên mật khẩu | Thanh trên (ẩn khi đang làm bài) |
| **TEACHER** (GV) | Giảng viên | **Luôn:** xem báo cáo lớp (lọc kỳ), tra cứu hồ sơ SV (nhập MSSV chính xác). **Khi Admin giao việc:** làm **GV A** (sửa, duyệt/từ chối câu được giao, gửi gói cho B) và/hoặc **GV B** (xác nhận/loại bỏ câu trong gói; không sửa; không trả về A). Xem ngân hàng câu hỏi **chỉ đọc** (câu được giao) | Thanh bên trái |
| **ADMIN** | Quản trị của trường (siêu tập của Teacher) | Tạo lô câu hỏi (AI sinh hoặc import file), giao việc/giao lại/chỉnh hạn/ép gửi gói, Kiểm tra (C3) + Import cuối, xem câu `AI_REJECTED` và thống kê; tạo/công bố/đóng kỳ thi, import danh sách thi, theo dõi dự thi; tạo + import + quản lý tài khoản SV và GV, nâng/thu hồi Admin; xem báo cáo, hồ sơ SV, ngân hàng (chỉ đọc). **Không sửa nội dung câu, không gõ câu bằng form, không duyệt nội dung.** | Thanh bên trái |
| EduZ (M2M) | Hệ thống ngoài | Chỉ gọi API bằng API Key — **không có giao diện**. Không phải dòng trong bảng `users` | — |

**Vai A / B không phải role**: là *phân công theo lô* do Admin chọn lúc "Giao việc". GV B của lô **không được nằm** trong nhóm A của cùng lô. Một GV có thể là A ở lô này và B ở lô khác. Một GV có thể chưa được giao gì (Hộp việc rỗng).

### 1.3. Ma trận quyền theo nhóm màn hình
| Nhóm | STUDENT | TEACHER (không phân công) | TEACHER vai A | TEACHER vai B | ADMIN |
|---|---|---|---|---|---|
| Đăng nhập / đổi / quên / đặt lại mật khẩu (S01, S16–S18) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kỳ thi của tôi, làm bài, kết quả, đáp án, lịch sử (S02–S07) | ✅ (của mình) | ❌ 403 | ❌ | ❌ | ❌ 403 |
| Báo cáo lớp, tra cứu/hồ sơ SV (S12–S14) | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ngân hàng câu hỏi chỉ đọc (S08, S10) | ❌ | ✅ chỉ câu **được giao** (có thể rỗng) | ✅ | ✅ | ✅ mọi câu (kể cả `AI_REJECTED` ở tab của lô) |
| Hộp việc "Cần duyệt" + duyệt từng câu + Gửi gói (S33, S11) | ❌ | ❌ | ✅ **đúng người** | ❌ | ❌ |
| Hộp việc "Cần xác nhận" + màn gói (S34, S35) | ❌ | ❌ | ❌ | ✅ **gói gửi cho mình** | ❌ |
| Tạo lô AI/import, danh sách & chi tiết lô, giao việc, giao lại, chỉnh hạn, ép gửi gói, Kiểm tra C3, Import (S26–S32) | ❌ 403 | ❌ 403 | ❌ | ❌ | ✅ |
| Kỳ thi: danh sách/tạo/sửa/chi tiết/import danh sách thi (S20–S23) | ❌ | ❌ 403 | ❌ | ❌ | ✅ |
| Tài khoản: danh sách, tạo lẻ, import, khóa, đổi role (S19, S24) | ❌ | ❌ 403 | ❌ | ❌ | ✅ |
| Tổng quan hệ thống (S36) | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 2. KHỐI NỀN GIAO DIỆN (ÁP DỤNG CHO MỌI MÀN)

### 2.1. Phong cách và token thiết kế
**TỐI GIẢN, SÁNG, ÍT THÀNH PHẦN.** Mỗi màn một việc chính. Nhiều khoảng trắng, **bo góc 12 px**, bóng đổ rất nhẹ, không ảnh nền, không minh họa phức tạp, không gradient nặng, **không có chế độ tối**. Web app **tiếng Việt**, font **"Be Vietnam Pro"** (dự phòng Inter).

| Token | Giá trị |
|---|---|
| `--primary` / nhạt / đậm | `#2563EB` / `#DBEAFE` / `#1D4ED8` |
| `--accent` | `#14B8A6` |
| `--bg` / `--card` / `--border` | `#F8FAFC` / `#FFFFFF` / `#E2E8F0` |
| `--text` / `--text-muted` | `#0F172A` / `#64748B` |
| `--success` / `--warning` / `--danger` | `#16A34A` / `#F59E0B` / `#DC2626` |
| Cỡ chữ | tiêu đề trang 24 px; tiêu đề thẻ 18 px; nội dung 16 px; chữ phụ 14 px; **nội dung câu hỏi thi ≥ 18 px (màn làm bài 20 px)** |
| Khoảng cách | bội số 8 px; vùng chạm ≥ 44 px (nút chính cao 48 px) |
| Responsive | mobile-first 360 → 768 → 1280 px; không cuộn ngang ở 360 px; nội dung tối đa rộng 1120 px, căn giữa |
| Logo `[D]` | ô vuông bo `#2563EB` chứa đường cong chữ S đi lên kết thúc bằng dấu tích trắng + chữ "**Adaptive** Placement Test" + dòng nhỏ "Kiểm tra xếp lớp tiếng Anh thích ứng"; có bản chỉ biểu tượng |

**Huy hiệu CEFR (luôn kèm chữ):** Pre-A1 `#E0F2FE`, A1 `#BAE6FD`, A2 `#7DD3FC`, B1 `#38BDF8`, B2 `#0EA5E9`, C1+ `#0369A1` (chữ trắng ở B2, C1+).

### 2.2. Từ điển nhãn tiếng Việt cho enum (dùng thống nhất ở MỌI màn)
**Trạng thái câu hỏi `ItemStatus`** (nhãn và màu là đề xuất `⚠️ ĐX`):
| Giá trị | Nhãn | Màu | Ai thấy |
|---|---|---|---|
| `DRAFT` | Chờ duyệt vòng 1 | `#94A3B8` | Admin, GV A (câu mình) |
| `FIRST_APPROVED` | Đã duyệt vòng 1 | `#F59E0B` | Admin, GV A, GV B (trong gói) |
| `SECOND_APPROVED` | Đã xác nhận vòng 2 | `#14B8A6` | Admin, GV B |
| `FINAL_APPROVED` | Đã vào ngân hàng | `#16A34A` | Mọi người có quyền xem ngân hàng |
| `REJECTED` | Đã loại | `#DC2626` | Admin (kèm thống kê theo GV); GV thấy câu mình/gói mình loại |
| `AI_REJECTED` | AI đã loại | `#7C3AED` | **Chỉ Admin** (tab "AI đã loại" của lô). Không bao giờ hiện cho GV/SV, không có trong bộ lọc ngân hàng |

**Trạng thái lô `ItemBatchStatus`:** `GENERATING` Đang sinh · `IMPORTING` Đang nhập · `CHECKING` AI đang kiểm tra · `READY_TO_ASSIGN` Chờ giao việc · `IN_REVIEW` Đang duyệt · `READY_TO_FINALIZE` Chờ kiểm tra cuối · `FINAL_CHECKED` Đã kiểm tra, chờ import · `DONE` Hoàn tất · `FAILED` Lỗi · `PARTIAL` Thiếu câu. **Nguồn lô `ItemBatchSource`:** `AI_GENERATED` "AI sinh" · `IMPORTED` "Import file" (câu seed cũ thuộc các lô seed `IMPORTED`/`DONE`, tên lô phân biệt bộ nguồn qua `ItemBatch.name`). **`Item` không có trường `source`**: cột "Nguồn" ở mọi bảng câu hỏi lấy từ lô.

**Trạng thái gói `PackageStatus` (đúng 3 giá trị):** `OPEN` "Chưa gửi" (tạo ngay lúc Admin giao việc) → `SENT` "Đã gửi" → `DONE` "Đã xong". GV B chỉ thấy gói `SENT`/`DONE` gửi cho mình.

**Trạng thái kỳ thi hiệu lực `effectiveStatus`:** `DRAFT` Nháp · `SCHEDULED` Đã lên lịch · `OPEN` Đang mở · `CLOSED` Đã đóng. Ở góc nhìn SV thêm: "Chưa mở" (SCHEDULED), "Đang mở" (OPEN), "Đã đóng" (CLOSED), "Đã thi" (SV đã `COMPLETED` trong kỳ). **Trạng thái dự thi của SV trong kỳ (Admin xem):** Chưa thi · Đang thi · Hoàn thành · Bỏ dở.

**Mức kiểm AI `CheckLevel`:** `PASS` Qua · `SOFT` Cờ mềm · `HARD` Lỗi cứng. **Điểm kiểm `CheckPoint`:** C1 (sau khi AI sinh), C2 (sau import file), C3 (Kiểm tra cuối trước Import).

**Hành động kiểm toán `ReviewAction`** (hiển thị ở "Lịch sử" câu): `APPROVE` Duyệt · `REJECT` Từ chối · `CONFIRM` Xác nhận · `REMOVE` Loại bỏ · `CONFIRM_ALL` Xác nhận hàng loạt · `IMPORT` Import · `REASSIGN` Giao lại · `EXTEND` Chỉnh hạn · `FORCE_SEND` Ép gửi gói · `ACCEPT_FLAG` Admin chấp nhận cờ.

**Mức nghiêm trọng chủ đề sai:** Nhẹ · Trung bình · Nghiêm trọng. **Kỹ năng:** Từ vựng · Ngữ pháp. **Lý do dừng bài:** `MAX_ITEMS_REACHED` "Đã làm đủ số câu tối đa" · `SE_THRESHOLD` "Hệ thống đã đủ tin cậy về năng lực của bạn" · `ITEM_BANK_BOUNDARY` "Năng lực của bạn ở vùng biên của thang đánh giá" · `TIMEOUT` "Đã hết thời gian làm bài".

### 2.3. Bảng mã lỗi → thông điệp hiển thị
Định dạng lỗi hiện tại của BE: `{statusCode, message, error, timestamp, path}`; mã nghiệp vụ ổn định là việc của BE — FE ánh xạ theo bảng sau (theo `code` nếu có, hoặc theo `message`/HTTP).

| Mã / HTTP | Thông điệp hiển thị (tiếng Việt) | Hiển thị ở |
|---|---|---|
| 401 (đăng nhập sai) | Thông tin đăng nhập không chính xác. | Dải đỏ nhạt trên nút (S01) |
| Tài khoản `is_active=false` | Tài khoản đã bị khóa, vui lòng liên hệ quản trị viên. | S01 |
| `PASSWORD_CHANGE_REQUIRED` 403 | (không hiện) — FE tự chuyển về `/change-password` | Toàn cục |
| 401 token hết hạn | Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại. | Chuyển `/login` kèm toast |
| 403 sai role / không được giao | Bạn không có quyền truy cập trang này. | Trang S15 (403) |
| 404 | Không tìm thấy trang hoặc dữ liệu. | S15 (404) |
| 5xx | Có lỗi xảy ra, vui lòng thử lại. + nút "Thử lại" | Khối lỗi |
| Mất mạng | Dải cố định đầu trang: "Mất kết nối mạng. Đang thử kết nối lại…" | Toàn cục |
| `RATE_LIMITED` 429 | Bạn thao tác quá nhanh, vui lòng thử lại sau. | S17 |
| `INVALID_RESET_OTP` 400 | Mã không đúng hoặc đã hết hạn. | S18 |
| `NOT_IN_ROUND` 403 | Bạn không thuộc kỳ thi này. | S03 |
| `ROUND_NOT_OPEN` 409 | Kỳ thi chưa mở hoặc đã đóng. | S03 |
| `ROUND_ALREADY_COMPLETED` 409 | Bạn đã hoàn thành bài thi của kỳ này. | S03 |
| `SESSION_IN_PROGRESS` 409 | (mở hộp thoại "Bạn đang có một bài thi dở dang.") | S03 |
| `IMPORT_FILE_INVALID` 400/413 | File không hợp lệ: chỉ nhận .xlsx, tối đa 2 MB, tối đa 1000 dòng dữ liệu. | S19, S23, S27 |
| `IMPORT_GRID_EXPIRED` 410 | Lưới tạm đã hết hạn, vui lòng tải lại file. | S19, S23, S27 |
| `IMPORT_GRID_EMPTY` 422 | Lưới đang trống, hãy tải file trước khi lưu. | S19, S23, S27 |
| 409 trùng email/MSSV/Mã GV (tạo lẻ) | Email / MSSV / Mã GV đã tồn tại. (hiện ngay dưới ô trùng) | Form S24 |
| `NOT_ASSIGNED` 403 | Bạn không được giao việc này. | S15 (403) |
| `CONFIRMER_IN_REVIEW_GROUP` 409 | GV xác nhận không được nằm trong nhóm GV duyệt. | S30 |
| `PACKAGE_INCOMPLETE` 409 | Còn câu chưa quyết định, chưa thể gửi gói. | S33, S11 |
| `DUPLICATE_AFTER_EDIT` 422 | Bản sửa trùng một câu khác. | S11 |
| `INVALID_AFTER_EDIT` 422 | Bản sửa không hợp lệ (xem chi tiết bên dưới). | S11 |
| `BATCH_BUDGET_EXCEEDED` 409 | Lô vượt giới hạn gọi AI cho phép. | S26 |
| `FINAL_CHECK_REQUIRED` 409 | Cần chạy Kiểm tra trước khi Import. | S32 |
| `FINAL_CHECK_STALE` 409 | Dữ liệu đã thay đổi kể từ lần kiểm tra cuối. Vui lòng kiểm tra lại. | S32 |
| `BATCH_NOT_READY_TO_FINALIZE` 409 | Lô chưa sẵn sàng để kiểm tra cuối. | S32 |

### 2.4. Khung giao diện (layout) dùng chung
**L-AUTH — Khung xác thực** (`/login`, `/forgot-password`, `/reset-password`, `/change-password`)
- `/login`: **hai nửa**. Nửa trái 45% nền `#EFF6FF`: logo (góc trên trái), câu giá trị 24 px "Đo đúng năng lực, không mất thời gian vào câu quá dễ hay quá khó.", họa tiết SVG đường cong chữ S nét mảnh, mờ, ở dưới (**không ảnh chụp, không ảnh trường**). Nửa phải nền trắng: biểu mẫu rộng tối đa 360 px, căn giữa dọc. Điện thoại: bỏ nửa trái, chỉ còn logo căn giữa trên biểu mẫu.
- `/forgot-password`, `/reset-password`, `/change-password`: một thẻ trắng căn giữa, rộng tối đa **420 px**, nền `#F8FAFC`, logo nhỏ phía trên thẻ. `/change-password` khi bị buộc đổi (lần đầu): **không có thanh điều hướng**.

**L-STUDENT — Thanh trên Sinh viên** (S02, S05, S06, S07, S03)
- Thanh **trắng**, cao 64 px, viền dưới 1 px `--border`. Trái: logo (điện thoại: chỉ biểu tượng). Giữa (≥768 px): 2 tab chữ **"Trang chủ"** (`/student/dashboard`) và **"Lịch sử bài thi"** (`/student/history`); tab hiện tại gạch chân xanh 2 px. Phải: avatar chữ cái đầu tên trong vòng tròn `#DBEAFE`; bấm mở menu nhỏ: "Đổi mật khẩu" `⚠️ ĐX` (→ `/change-password`), "Đăng xuất". **Không vẽ chuông thông báo.** Điện thoại: 2 tab chuyển thành thanh dưới 2 mục.
- Nền nội dung `#F8FAFC`; nội dung tối đa 720 px (S02, S05) hoặc 1120 px (S07), căn giữa; các thẻ trắng xếp dọc cách nhau 24 px; **không có khung bọc lớn**.

**L-FOCUS — Chế độ tập trung** (S04 làm bài)
- **Ẩn toàn bộ điều hướng**: không logo, không menu, không avatar. Chỉ: số câu (trái), đồng hồ (phải), thẻ câu hỏi, 4 phương án, nút nộp. Gợi ý triển khai `[D]`: đặt route `take` trong route group `(exam)` (URL không đổi vì group không vào URL).

**L-SIDEBAR — Thanh bên Teacher/Admin** (mọi màn S08–S14, S19–S36)
- Thanh bên trái rộng **240 px**, nền trắng, viền phải mảnh (điện thoại: thu thành nút ☰ mở ngăn kéo). Đỉnh: logo. Các mục: biểu tượng nét mảnh + chữ; mục hiện tại nền `#DBEAFE` chữ xanh đậm. Đáy: avatar chữ cái + tên + nút chữ "Đăng xuất"; Admin có thêm huy hiệu nhỏ "Quản trị viên" cạnh tên. **Không thanh trên đậm**; ở đầu vùng nội dung: tiêu đề trang 24 px, nút hành động chính căn phải cùng hàng.
- **Menu dựng theo `role`** (BR-16):

| Role | Mục menu (thứ tự) → route |
|---|---|
| **TEACHER** | **Hộp việc** (huy hiệu số việc chưa xong = câu chưa quyết của vai A + câu chưa quyết trong gói vai B) → `/teacher/tasks/reviews` · **Báo cáo lớp học** → `/teacher/reports` · **Hồ sơ sinh viên** → `/teacher/students` · **Ngân hàng câu hỏi** (chỉ xem; chốt 16/10, #116) → `/teacher/item-bank` |
| **ADMIN** | **Tổng quan** → `/admin/dashboard` · **Ngân hàng câu hỏi** → `/admin/item-bank` · **Lô câu hỏi** (chấm vàng = số lô cần xử lý) → `/admin/item-batches` · **Kỳ thi** → `/admin/exam-rounds` · **Tài khoản** → `/admin/users/students` · **Báo cáo lớp học** → `/teacher/reports` `🔶 R-2` · **Hồ sơ sinh viên** → `/teacher/students` `🔶 R-2`. **Không có "Hộp việc"** (Admin không làm A/B; `🔶 P25-1`) |

- **Hộp việc có hai tab** hiển thị trên cả S33 và S34 (cùng khung tab ở đầu trang, mỗi tab là một route): "**Cần duyệt**" (`/teacher/tasks/reviews`) và "**Cần xác nhận**" (`/teacher/tasks/confirms`), kèm huy hiệu số. Tab không có việc: trạng thái rỗng "Bạn chưa có việc nào được giao." Mục "Hộp việc" ở menu mở tab "Cần duyệt" `⚠️ ĐX`.

### 2.5. Bộ thành phần dùng chung (component dictionary)
| Mã | Thành phần | Mô tả bắt buộc |
|---|---|---|
| C-BADGE | Huy hiệu trạng thái / CEFR | Viên thuốc (pill) bo tròn, chữ 14 px, nền theo bảng màu, **luôn có chữ**. |
| C-CHIP | Chip lọc | Pill bo tròn nằm **trực tiếp trên nền xám** (không bọc khung). Chip đang lọc: nền `#DBEAFE`, chữ xanh đậm. Điện thoại: gộp thành nút "Bộ lọc" mở ngăn kéo. |
| C-SEARCH | Ô tìm kiếm | Pill bo tròn, biểu tượng kính lúp **bên ngoài** nhãn, nhãn chữ phía trên hoặc placeholder rõ; debounce 300 ms `[D]`. |
| C-TABLE | Bảng dữ liệu | Trong thẻ trắng; hàng cao 56 px; hover nền xanh rất nhạt; phân trang "Hiển thị 1–20 / N ‹ 1 2 3 ›" (20 dòng/trang `[D]`); điện thoại: chuyển dạng **danh sách thẻ**. |
| C-FIELD | Ô nhập | **Nhãn chữ nằm phía trên** ô, không có biểu tượng trong ô; lỗi hiện dòng chữ đỏ ngay dưới ô + `aria-describedby`; trường bắt buộc có dấu `*` sau nhãn. |
| C-PASSWORD | Ô mật khẩu | Như C-FIELD + nút chữ "Hiện"/"Ẩn" bên trong phải. |
| C-BTN | Nút | Chính: nền `--primary`, chữ trắng, rộng theo nội dung (rộng đầy ở biểu mẫu hẹp), cao 48 px. Phụ: viền `--border`. Nguy hiểm: viền + chữ `--danger`. Vô hiệu: xám, `aria-disabled`, có `title` giải thích khi tắt. Đang gửi: khóa + spinner trong nút. |
| C-DIALOG | Hộp thoại xác nhận | Căn giữa, ≤ 440 px; tiêu đề + 1–2 câu nội dung + 2 nút (Hủy ở trái, hành động ở phải). **Hộp thoại Từ chối/Loại bỏ: chỉ "Hủy" và "Từ chối"/"Loại bỏ", KHÔNG có ô lý do** (#56). Đóng bằng Esc; trả focus về nút gọi. |
| C-TOAST | Thông báo nhỏ | Góc dưới phải, tự tắt sau 4 giây `[D]`; lỗi không tự tắt. |
| C-SKELETON | Khung chờ | Khối xám nhấp nháy đúng hình dạng nội dung. |
| C-OFFLINE | Dải mất kết nối | Cố định phía trên cùng: "Mất kết nối mạng. Đang thử kết nối lại…"; khóa các nút ghi. |
| C-EMPTY | Trạng thái rỗng | Chữ xám căn giữa trong thẻ + (nếu có) nút hành động liên quan. |
| C-ERROR | Khối lỗi | Dải đỏ nhạt `#FEE2E2` + thông điệp + nút "Thử lại". |
| C-IMPORT-GRID | Lưới tạm import (xem Mục 2.7) | Dùng chung cho S19, S23, S27. |
| C-DIFF | So sánh bản gốc/bản sửa | 2 cột "Bản gốc" | "Bản A đã sửa"; phần khác nhau: **gạch dưới/gạch ngang + nhãn chữ "đã đổi"**, không chỉ dùng màu. Dùng ở S10, S35, S32. |
| C-FLAG | Chip cờ mềm | Viên thuốc cam nhạt `#FEF3C7` + biểu tượng "!" + mã lý do dịch tiếng Việt + (nếu có) liên kết "xem câu nghi trùng". Bấm mở khung xem câu nghi trùng (chỉ đọc). |
| C-PROGRESS | Thanh tiến độ | Mảnh 6 px, kèm số "x / y" bằng chữ. |
| C-DUE | Huy hiệu hạn | "Còn N ngày" (xanh) / "Hôm nay" (cam) / "Quá hạn" (đỏ, kèm chữ). Quá hạn **chỉ cảnh báo, không khóa thao tác**. |
| C-STEPPER | Thanh tiến trình lô | 7 bước: Tạo → AI kiểm → Giao việc → A duyệt → B xác nhận → Kiểm tra → Import; bước hiện tại tô xanh, bước xong có dấu tích + chữ. |

### 2.6. Năm trạng thái giao diện (áp dụng mọi màn)
| Trạng thái | Quy tắc |
|---|---|
| Đang tải | Skeleton đúng hình dạng; riêng thao tác ghi: khóa nút + spinner. |
| Có dữ liệu | Hiển thị bình thường. |
| Rỗng | C-EMPTY với câu riêng của màn (ghi ở từng màn). |
| Lỗi | C-ERROR + "Thử lại"; **giữ nguyên dữ liệu người dùng đã nhập** (biểu mẫu, bản sửa câu). |
| Mất kết nối | C-OFFLINE; khóa nút ghi; tự gọi lại khi có mạng. |

### 2.7. Lưới tạm import (C-IMPORT-GRID) — cơ chế chung cho S19, S23, S27
**Hành vi (bắt buộc, SRS 9b.4):** không có bước "xem trước/xác nhận" riêng, không có chế độ "tất cả hoặc không", không trạng thái `SKIPPED`.
```
┌──── Kéo thả hoặc chọn file .xlsx (có thể chọn nhiều lần) ─────┐   ← dropzone
   [Tải file mẫu]                                                       
 Lưới tạm (N dòng)                                  [Xóa cả lưới]
 ┌──────────────────────────────────────────────────────────┐
 │ <các cột theo từng màn>                       [Xóa dòng]  │
 └──────────────────────────────────────────────────────────┘
                                   [  Lưu N …  ]  ← nút chính
```
1. **Tải file:** `.xlsx`, ≤ 2 MB, ≤ 1000 dòng dữ liệu, dòng đầu là tiêu đề; có thể tải **nhiều file liên tiếp, cộng dồn** vào cùng lưới. Dòng đã có trong lưới → **bỏ qua** (không tính lỗi).
2. **Dòng lỗi bị loại khỏi lưới**, không chặn việc Lưu. Sau **mỗi lần tải** hiện **popup** liệt kê các dòng bị loại: "Dòng <số dòng trong file> — <lý do>", nút "Đóng". Một số màn có **popup thứ hai** (ví dụ "Tài khoản đã tồn tại").
3. **Xóa dòng / Xóa cả lưới:** hộp xác nhận đối với "Xóa cả lưới".
4. **Lưới sống ~30 phút** từ lần thao tác cuối (làm mới mỗi lần thêm). Hết hạn → `IMPORT_GRID_EXPIRED`: banner vàng "Lưới tạm đã hết hạn, vui lòng tải lại file." và lưới trống.
5. **Nút Lưu** (chính): bật khi lưới không rỗng; bấm → ghi mọi dòng trong lưới trong **một transaction**; lưới rỗng → `IMPORT_GRID_EMPTY`.
6. Số dòng hiển thị trong nhãn nút: "Lưu 12 …". Dữ liệu lưới nằm ở server (Redis); FE chỉ hiển thị, tải lại trang vẫn lấy lại được lưới qua `GET …/grid` trong 30 phút.
7. **File mẫu** là file tĩnh trong `public/templates/` (chỉ dữ liệu giả): `import-students.xlsx`, `import-teachers.xlsx`, `import-roster.xlsx`, `import-items.xlsx`.

---

## 3. BẢN ĐỒ ROUTE CHUẨN (NGUỒN DUY NHẤT CHO FILE NÀY)

> **Quy ước route đã chốt cho file này (17/10/2026):** (1) Student/Teacher/Admin lấy **theo cấu trúc đích** `Update/KE_HOACH_CAU_TRUC_DU_AN.md` — mỗi role có **tiền tố URL riêng** `/student`, `/teacher`, `/admin` (cần thiết vì route group `(student)`, `(teacher)`, `(admin)` không xuất hiện trong URL; thiếu tiền tố sẽ trùng `/dashboard`); nhóm xác thực không tiền tố. (2) Bộ route của bản chốt 16/10 (reviews/confirms/item-batches/exam-rounds…) giữ nguyên. (3) **Nhóm tài khoản Admin dùng `/admin/users/*`** — lý do: SRS/Class Diagram gom import tài khoản vào **một** dịch vụ dùng chung (`UserImportService`, tham số `kind`; API `/users/import/*`), quản lý tài khoản vào `AccountAdminService`/module `user-admin`; mọi tài khoản cùng là `User` (một aggregate, role qua `UserRole`) nên gom dưới một thư mục tài nguyên `users`, cùng kiểu với `/admin/exam-rounds/[roundId]/import`; tên `/admin/import-users` (động từ + danh từ) và `/admin/students` rời khỏi cây `users` bị bỏ. (4) Mọi URL động dùng tham số theo bảng; khi khác tên với bản cũ xem Mục 10.2.

### 3.1. Xác thực (route group `(auth)`, không tiền tố)
| ID | URL | File Next.js | Ai vào | API chính | UC |
|---|---|---|---|---|---|
| S01 | `/login` | `app/(auth)/login/page.tsx` | Chưa đăng nhập (đã đăng nhập → tự chuyển về trang chủ theo role) | `POST /auth/login` | UCSV01/UCGV01/UCADM01 |
| S17 | `/forgot-password` | `app/(auth)/forgot-password/page.tsx` | Chưa đăng nhập | `POST /auth/forgot-password` | UCSV09 `⚠️ ĐX` |
| S18 | `/reset-password` | `app/(auth)/reset-password/page.tsx` | Chưa đăng nhập | `POST /auth/reset-password` | UCSV09 `⚠️ ĐX` |
| S16 | `/change-password` | `app/(auth)/change-password/page.tsx` | Đã đăng nhập (mọi role) | `POST /auth/change-password` | UCSV08 `⚠️ ĐX` |

Trang chủ theo role sau đăng nhập: STUDENT → `/student/dashboard`; TEACHER → `/teacher/tasks/reviews` nếu có việc, ngược lại `/teacher/reports` `🔶 R-1`; ADMIN → `/admin/dashboard` `🔶 R-5`. Route gốc `/` chỉ làm nhiệm vụ chuyển hướng theo role.

### 3.2. Sinh viên (`app/(student)/student/…`)
| ID | URL | File Next.js | API chính | UC |
|---|---|---|---|---|
| S02 | `/student/dashboard` | `(student)/student/dashboard/page.tsx` | `GET /exam-rounds/mine`, `GET /sessions/active` | UCSV02, UCSV07 |
| S03 | `/student/exams/[roundId]` `⚠️ ĐX` (màn giới thiệu bài thi) | `(student)/student/exams/[roundId]/page.tsx` | `POST /sessions` `{examRoundId}` | UCSV02 |
| S04 | `/student/exams/[roundId]/take` | `(exam)/student/exams/[roundId]/take/page.tsx` (nhóm `(exam)` = khung tập trung) | `GET /sessions/active`, `GET /sessions/:id/next-item`, `POST /sessions/:id/responses`, `GET /sessions/:id/resume` | UCSV03 |
| S05 | `/student/results/[sessionId]` | `(student)/student/results/[sessionId]/page.tsx` | `GET /sessions/:id/result` | UCSV04 |
| S06 | `/student/results/[sessionId]/review` | `(student)/student/results/[sessionId]/review/page.tsx` | `GET …/review` | UCSV05 |
| S07 | `/student/history` | `(student)/student/history/page.tsx` | `GET /placement-profiles/:id/history` | UCSV06 |

### 3.3. Giảng viên (`app/(teacher)/teacher/…`)
| ID | URL | File Next.js | API chính | UC |
|---|---|---|---|---|
| S33 | `/teacher/tasks/reviews` | `tasks/reviews/page.tsx` | `GET /me/review-tasks`, `POST /item-packages/mine/send` | UCGV14 |
| S11 | `/teacher/tasks/reviews/[packageId]` | `tasks/reviews/[packageId]/page.tsx` | `PATCH /items/:id`, `POST /items/:id/approve\|reject`, `POST /item-packages/mine/send` | UCGV14 (gồm UCGV04 sửa câu) |
| S34 | `/teacher/tasks/confirms` | `tasks/confirms/page.tsx` | `GET /me/confirm-packages` | UCGV15 |
| S35 | `/teacher/tasks/confirms/[packageId]` | `tasks/confirms/[packageId]/page.tsx` | `POST /items/:id/confirm\|remove`, `POST /item-packages/:id/confirm-all` | UCGV15 |
| S12 | `/teacher/reports` | `reports/page.tsx` | `GET /reports/class-distribution`, `…/error-patterns` (`?examRoundId=`) | UCGV07, UCGV08, UCADM05 |
| S13 | `/teacher/students` | `students/page.tsx` | (tra cứu theo MSSV) | UCGV09, UCADM04 |
| S14 | `/teacher/students/[studentId]` (giá trị tham số = **MSSV** `🔶 R-6`) | `students/[studentId]/page.tsx` | `GET /placement-profiles/:id`, `…/history` | UCGV09, UCADM04 |
| S08 | `/teacher/item-bank` | `item-bank/page.tsx` | `GET /items` (GV: chỉ câu được giao) | UCGV02 |
| S10 | `/teacher/item-bank/[id]` | `item-bank/[id]/page.tsx` | `GET /items/:id` | UCGV04 (xem), UCGV06 (xem) |
| — | `/teacher/dashboard` | (cấu trúc đích có, **chưa có đặc tả nội dung**) | — | `🔶 R-1` — không sinh trong đợt này |

### 3.4. Quản trị (`app/(admin)/admin/…`)
| ID | URL | File Next.js | API chính | UC |
|---|---|---|---|---|
| S36 (cũ E2) | `/admin/dashboard` `🔶 R-5` | `dashboard/page.tsx` | `GET /reports/…` | UCADM05 |
| S08 | `/admin/item-bank` | `item-bank/page.tsx` | `GET /items` (mọi câu) | UCADM06 |
| S10 | `/admin/item-bank/[id]` | `item-bank/[id]/page.tsx` | `GET /items/:id` | UCADM06 |
| S28 | `/admin/item-batches` | `item-batches/page.tsx` | `GET /item-batches` | UCADM13 |
| S26 | `/admin/item-batches/generate` | `item-batches/generate/page.tsx` | `POST /item-batches` | UCADM11 |
| S27 | `/admin/item-batches/import` | `item-batches/import/page.tsx` | `POST /item-imports/upload`, `GET\|DELETE /item-imports/grid[/:rowKey]`, `POST /item-imports/save` | UCADM12 |
| S29 (+ S31 là ngăn phải) | `/admin/item-batches/[batchId]` | `item-batches/[batchId]/page.tsx` | `GET /item-batches/:id`, `GET …/ai-rejected`, `PATCH …/deadlines`, `POST /item-packages/:id/force-send` | UCADM13 |
| S30 | `/admin/item-batches/[batchId]/assign` | `…/assign/page.tsx` | `GET …/assign-preview`, `POST …/assign`, `POST …/reassign` | UCADM13 |
| S32 | `/admin/item-batches/[batchId]/final-check` | `…/final-check/page.tsx` | `POST\|GET …/final-check`, `POST /items/:id/decision`, `POST …/import` | UCADM14 |
| S20 | `/admin/exam-rounds` | `exam-rounds/page.tsx` | `GET /exam-rounds` | UCADM15 |
| S21 | `/admin/exam-rounds/new`, `/admin/exam-rounds/[roundId]/edit` | `exam-rounds/new/page.tsx`, `[roundId]/edit/page.tsx` | `POST /exam-rounds`, `PATCH /exam-rounds/:id` | UCADM15 |
| S22 | `/admin/exam-rounds/[roundId]` | `[roundId]/page.tsx` | `GET /exam-rounds/:id`, `…/participants`, `POST …/publish\|close`, `DELETE …/participants/:studentId` | UCADM15, UCADM17 |
| S23 | `/admin/exam-rounds/[roundId]/import` | `[roundId]/import/page.tsx` | `…/participants/import/{upload,grid,save}` | UCADM16 |
| S24 | `/admin/users/students`, `/admin/users/teachers` (hai tab = hai route) | `users/students/page.tsx`, `users/teachers/page.tsx` | `GET\|POST\|PATCH /students`, `/teachers`, `POST /students/:id/lock\|unlock\|resend-temporary-password`, `PATCH /users/:id/role` | UCADM09 |
| S19 | `/admin/users/import` (tham số `?kind=STUDENT\|TEACHER`) | `users/import/page.tsx` | `/users/import/{upload,grid,save}?kind=` | UCADM08 |
| S12–S14 | Admin dùng chung `/teacher/reports`, `/teacher/students[/…]` `🔶 R-2` | — | như Teacher | UCADM04, UCADM05 |

### 3.5. Trang lỗi (S15)
`app/403/page.tsx` (đã có), `app/not-found.tsx` (404), `app/error.tsx` (500). Mọi route sai role/không được giao → 403.

### 3.6. Bảo vệ route (guard) — quy tắc cho FE
- Chưa đăng nhập → `/login` (giữ `?next=` đường dẫn cũ).
- `mustChangePassword=true` → mọi route (trừ `/change-password`, đăng xuất) chuyển về `/change-password`.
- Sai role → 403. TEACHER mở route Admin (`/admin/**`) → 403. STUDENT mở `/teacher/**`, `/admin/**` → 403. ADMIN mở `/student/**` → 403.
- TEACHER mở `/teacher/tasks/reviews/[packageId]` của người khác hoặc `…/confirms/[packageId]` không gửi cho mình → 403 (`NOT_ASSIGNED`).
- Token **không** lưu ở `localStorage` (cookie `httpOnly`).

---

## 4. LUỒNG HOẠT ĐỘNG VÀ NGHIỆP VỤ THEO ROLE

### 4.1. Máy trạng thái (nguồn chân lý cho nút bật/tắt trên UI)

**(a) Câu hỏi `Item` — một chiều, không quay lại**
```
        ┌─ rớt C1/C2 (máy) ───────────────────────────► AI_REJECTED   (lưu mã lý do; chỉ Admin thấy)
Tạo ────┤
        └─ qua ► DRAFT ──A Duyệt──► FIRST_APPROVED ──(A Gửi gói)──► [B Xác nhận] ► SECOND_APPROVED ──Admin Import──► FINAL_APPROVED
                  │                       │                                  │              │
                  └──A Từ chối────────────┘ (A không sửa lại sau khi gửi)     └─B Loại bỏ──► REJECTED
                  └──► REJECTED                                                       C3 lỗi cứng ► AI_REJECTED ; lỗi mềm ► Admin: Chấp nhận (ACCEPT_FLAG→Import) | Loại (REJECTED)
```
Chỉ `FINAL_APPROVED` được CAT chọn; `FINAL_APPROVED` **cấm sửa**.

**(b) Lô `ItemBatch`:** `GENERATING|IMPORTING` → `CHECKING` → `READY_TO_ASSIGN` → `IN_REVIEW` → `READY_TO_FINALIZE` (mọi gói `DONE` **hoặc** mọi hạn đã qua) → `FINAL_CHECKED` (sau khi Admin bấm Kiểm tra) → `DONE` (mọi câu ở trạng thái cuối: `FINAL_APPROVED`/`REJECTED`/`AI_REJECTED`). Ngoại lệ `FAILED`, `PARTIAL` (hết ngân sách AI, thiếu câu). Theo #121 không có luồng xử lý riêng cho câu chưa quyết định sau Import (xem Mục 4.5-F); lô sang `DONE` khi mọi câu đã ở trạng thái cuối.

**(c) Gói `ItemPackage`:** một gói **cho mỗi GV A trong một lô** (`UNIQUE(batchId, reviewerId)`), tạo **ngay lúc Admin giao việc**: `OPEN` → (A bấm Gửi cho B) `SENT` → (mọi câu trong gói có quyết định) `DONE`.

**(d) Kỳ thi `ExamRound`** (`effectiveStatus(round, now)` là nguồn duy nhất, chuyển *lazy*): `DRAFT` --Công bố (cần ≥1 SV)--> `SCHEDULED` --tới `opensAt`--> `OPEN` --tới `closesAt` hoặc Admin Đóng--> `CLOSED`; `DRAFT` --Hủy--> `CLOSED`. Không quay lui.

**(e) Phiên thi `TestSession`:** `IN_PROGRESS` → `COMPLETED` (đủ điều kiện dừng hoặc quá hạn khi ≥ 8 câu, `stoppingReason=TIMEOUT`) | `ABANDONED` (quá hạn khi < 8 câu). `expiresAt = min(startedAt + durationMinutes của kỳ, closesAt)`, tính **một lần** lúc bắt đầu.

### 4.2. Luồng chung — Xác thực và mật khẩu
1. **Đăng nhập (S01):** nhập Email + mật khẩu → `POST /auth/login`. Thành công: nếu `mustChangePassword=true` → S16 (bị chặn mọi route khác); ngược lại về trang chủ theo role (Mục 3.1). Sai → dải lỗi, giữ ô Email. Khóa (`is_active=false`) → không đăng nhập được.
2. **Mật khẩu tạm lần đầu:** tài khoản do Admin tạo nhận **email mật khẩu tạm** (12 ký tự; không hiển thị ở UI). Đăng nhập lần đầu bắt buộc đổi (S16). Sau thành công: `mustChangePassword=false`, cấp lại token, toast "Đã đổi mật khẩu." → trang chủ theo role.
3. **Quên mật khẩu:** S01 → "Quên mật khẩu?" → S17 (nhập email; **luôn 202, thông điệp trung tính**) → email có **OTP 6 số** (hiệu lực 10 phút, dùng 1 lần, sai tối đa 5 lần rồi hủy mã) → S18 (email + OTP + mật khẩu mới) → về S01 (**không tự đăng nhập**).
4. **Phiên đăng nhập:** access token + refresh token xoay vòng; FE giữ token qua cookie httpOnly (BFF, #50); khi access token hết hạn FE gọi `POST /auth/refresh`, hỏng → về S01 kèm toast "Phiên đăng nhập đã hết hạn…"; bấm **Đăng xuất** gọi `POST /auth/logout` rồi về S01. Sau khi **đổi mật khẩu** (S16) hoặc **đổi quyền** (S24) token cũ mất hiệu lực quyền cũ (UCSV08, BR-18). Đăng nhập sai liên tiếp vượt ngưỡng → 429 `RATE_LIMITED` (ngưỡng chưa chốt; UI không hiển thị con số).
5. **Chính sách mật khẩu:** mật khẩu mới ≠ mật khẩu hiện tại; độ dài tối thiểu **8** (`🔶 TODO-CONFIRM Q-4`, đề xuất).

### 4.3. Luồng Sinh viên (STUDENT)
**Tiền đề:** Admin đã tạo tài khoản SV (S24/S19), tạo kỳ thi (S21), thêm SV vào kỳ (S23) và **Công bố** kỳ (S22).
1. Đăng nhập → **S02**: thẻ "Kỳ thi của tôi" liệt kê các kỳ SV thuộc, kèm trạng thái hiệu lực. Nút "Bắt đầu bài thi" **chỉ bật ở kỳ Đang mở** và SV chưa có phiên hoàn thành trong kỳ đó.
2. Nếu có **bài dở** (phiên `IN_PROGRESS`): thẻ cam "Bạn đang có một bài thi dở dang." + nút "Tiếp tục bài thi" → thẳng S04 (không hiện nút Bắt đầu ở kỳ đó).
3. Bấm "Bắt đầu bài thi" → **S03** (giới thiệu, đã chọn sẵn kỳ) → "Tôi đã hiểu, bắt đầu làm bài" → `POST /sessions {examRoundId}` → S04. Điều kiện hợp lệ (BR-10): thuộc danh sách kỳ; kỳ đang `OPEN`; chưa có phiên `IN_PROGRESS`; chưa có phiên `COMPLETED` trong kỳ.
4. **S04 làm bài (CAT):** mỗi lượt: server chọn câu kế (`next-item`) theo **Randomized Top-5 b-matching** trên các câu `FINAL_APPROVED`, round-robin kỹ năng Từ vựng/Ngữ pháp; SV chọn 1 trong 4 đáp án → "Nộp đáp án" → `POST responses` → câu kế (không hiện đúng/sai, θ, SE, mức CEFR tạm tính; không quay lại/bỏ qua). Dừng khi: SE < 0,35, hoặc đủ 25 câu, hoặc Outlier Early Stop (sau ≥ 8 câu), hoặc hết `expiresAt`. **Tải lại trang (F5), mất mạng rồi vào lại hoặc mở từ S02 "Tiếp tục"** (trong vòng 7200 giây): FE gọi `GET /sessions/active` rồi `GET /sessions/:id/resume`; server đọc trạng thái từ Redis, nếu mất thì **dựng lại từ PostgreSQL** (các câu đã trả lời); trả về đúng câu chưa trả lời và thời gian còn lại theo `expiresAt` (**không cấp lại thời gian**); phiên đã quá hạn → áp luật K5; phiên đã `COMPLETED` → chuyển sang S05. Đáp án chọn dở được giữ tạm ở trình duyệt và gửi lại khi có mạng.
5. **Hết giờ** (`expiresAt`): ≥ 8 câu → `COMPLETED` + `TIMEOUT` → S05 kèm thông báo; < 8 câu → `ABANDONED` → về S02 với thông báo "Bài thi bị hủy do hết thời gian khi làm chưa đủ 8 câu."
6. **S05 kết quả:** CEFR, độ tin cậy, θ/SE/CI, 2 thanh kỹ năng, chủ đề cần cải thiện, gợi ý AI, banner vùng biên → "Xem giải thích chi tiết" → **S06** (đáp án đúng/đã chọn + giải thích AI **đã sinh sẵn cùng lúc sinh câu**, dùng chung mọi SV) → "Về kết quả"/"Về trang chủ".
7. **S07 lịch sử:** bảng các lần thi → bấm dòng → S05 của lần đó.
8. **Lỗi chặn vào thi** hiện tại S02/S03: không thuộc kỳ, kỳ chưa mở/đã đóng, đã thi xong kỳ, có phiên dở (Mục 2.3).

### 4.4. Luồng Giảng viên (TEACHER)
**4.4-A. Luồng luôn có (mọi GV):** Đăng nhập (S01) → (S16 nếu cần) → **S12 Báo cáo lớp** (lọc theo kỳ, xuất CSV) hoặc **S13 → S14** (nhập MSSV chính xác → hồ sơ SV). GV chỉ **xem**, không có thao tác ghi.

**4.4-B. GV vai A — duyệt câu (khi Admin đã giao việc cho mình; lô `IN_REVIEW`)**
1. Nhận **email nhắc việc** ("Bạn có x câu cần duyệt, hạn dd/mm") và thấy việc ở **Hộp việc → Cần duyệt (S33)**: mỗi thẻ là **một gói của mình trong một lô** (tên lô, "Đã quyết 12 / 20", hạn, tiến độ).
2. Bấm thẻ → **S11** (màn gói): danh sách câu trong gói + trình sửa/duyệt từng câu. Chỉ thấy **câu giao cho mình** (khác → 403).
3. Với mỗi câu (đang `DRAFT`): có thể **sửa** nội dung, 4 phương án, đáp án đúng, giải thích (kỹ năng/CEFR/chủ đề/`irt_b` chỉ đọc `🔶 P25-3`); bấm **Lưu sửa** → server chạy lại **luật cứng + trùng T1–T2** trên bản sửa; lỗi/trùng → **chặn nút Duyệt** (`INVALID_AFTER_EDIT`/`DUPLICATE_AFTER_EDIT`).
4. Chọn **Duyệt** (→ `FIRST_APPROVED`) hoặc **Từ chối** (→ `REJECTED`, **không có ô lý do**). Sau mỗi thao tác tự sang câu chưa quyết kế tiếp.
5. Khi **mọi câu đã có quyết định**, nút **"Gửi cho B"** bật; gửi **một lần** → gói `SENT` (câu A từ chối **không** vào gói; sau khi gửi, A **không sửa lại**, gói chỉ đọc). Còn câu chưa quyết → `PACKAGE_INCOMPLETE`.
6. Quá hạn chỉ hiện cảnh báo "Việc này đã quá hạn", **không khóa thao tác**. Admin có thể chỉnh hạn, giao lại, hoặc **ép gửi** gói thay A.

**4.4-C. GV vai B — xác nhận (khi một gói đã được A gửi cho mình)**
1. Nhận email nhắc, thấy **gói** ở **Hộp việc → Cần xác nhận (S34)** (mỗi A gửi một gói riêng, vào các thời điểm khác nhau; hạn của B tính từ **ngày gói được gửi**).
2. Bấm gói → **S35**: **chỉ đọc**. Mỗi câu hiện cờ mềm, dấu **"A đã sửa"** và **bản gốc so với bản đã sửa**.
3. Với mỗi câu: **Xác nhận** (→ `SECOND_APPROVED`) hoặc **Loại bỏ** (→ `REJECTED`, không ô lý do). Hoặc nút **"Xác nhận tất cả câu còn lại"** (chỉ tác động câu chưa quyết; ghi log `CONFIRM_ALL`).
4. B **không sửa, không trả về A**. Mọi câu có quyết định → gói `DONE`, màn hiện "Gói đã hoàn tất." và chỉ đọc.

### 4.5. Luồng Quản trị (ADMIN)
**A. Tài khoản**
1. **Tạo từng người** (S24 → "Thêm sinh viên"/"Thêm giảng viên" → form → Lưu) **hoặc import** (S24 → "Import" → S19: chọn loại SV/GV → tải 1..n file vào **lưới tạm** → popup dòng bị loại / "Tài khoản đã tồn tại" → **Lưu**).
2. Khi Lưu: tạo tài khoản (`role` = STUDENT/TEACHER, `mustChangePassword=true`), sinh mật khẩu tạm 12 ký tự (argon2), **xếp hàng email** (BullMQ + MailPort). Email gửi thất bại sau retry (BullMQ, 3 lần): **không rollback tài khoản**; hệ thống ghi nhật ký phía server (BR-05, BR-15). **UI không có cột hay bộ lọc trạng thái email** (#120); Admin dùng "Gửi lại mật khẩu tạm" từng tài khoản (`🔶 BR-05`, Mục 9).
3. Quản lý: sửa họ tên/email, **Khóa/Mở khóa** (`is_active`), **Gửi lại mật khẩu tạm** (SV), với GV: **Nâng lên Admin / Thu hồi Admin**. Không tự thu hồi mình; không thu hồi Admin cuối (`🔶 BR-18 đề xuất`). Không xóa cứng tài khoản đã có phiên/hồ sơ (chỉ khóa).

**B. Kỳ thi**
1. **S20** danh sách → "Tạo kỳ thi" → **S21** (tên, giờ mở, giờ đóng, **thời lượng bắt buộc điền sẵn 45**; 5–180; ≤ khoảng mở–đóng) → Lưu (kỳ ở `DRAFT`) → **S22**.
2. S22 → "Import danh sách" → **S23** (lưới tạm, cột MSSV/Ghi chú; MSSV không tồn tại/đã có trong kỳ → bị loại + popup) → Lưu → về S22.
3. S22 → **Công bố** (cần ≥ 1 SV; `DRAFT → SCHEDULED`) → tới giờ mở tự `OPEN` → tới giờ đóng tự `CLOSED`, hoặc **Đóng kỳ** thủ công (phiên đang chạy vẫn tiếp tục tới `expiresAt`, chỉ chặn phiên mới; `🔶 TODO-CONFIRM Q-2`). Theo dõi trạng thái dự thi từng SV; **Gỡ SV** chỉ ở dòng "Chưa thi" và khi kỳ chưa đóng (SV đã có phiên bị khóa ngoại `fk_session_participant` chặn).
4. Quy tắc sửa kỳ (BR-08, `🔶` đề xuất): `DRAFT` sửa tự do; `SCHEDULED` chỉ sửa tên và kéo dài giờ đóng; `CLOSED` không sửa.

**C. Tạo lô câu hỏi** (câu hỏi chỉ vào hệ thống qua lô; **không có form thêm từng câu**)
- **Bằng AI (S26):** nhập Kỹ năng, CEFR, Chủ đề (tùy chọn), Số câu N → "Tạo lô" → lô `GENERATING` (chạy nền) → S29 xem tiến độ. Hệ thống sinh dư, **kiểm C1** (luật cứng → trùng T1/T2/T3 → kiểm đáp án độc lập), bù thiếu, cắt về N; giải thích được sinh **cùng lúc** với câu. Không chọn GV ở bước này.
- **Bằng import file (S27):** tải 1..n file `.xlsx` vào lưới tạm (C2 tầng 1–4 chạy ngay khi tải: dòng lỗi/trùng bị loại + popup; trùng gần đúng = **cờ mềm** trên lưới) → **Lưu** → tạo lô `IMPORTED`, chạy C2 tầng 5 → S29. **GV không có chức năng này.**
- Kết quả: lô `READY_TO_ASSIGN` (hoặc `PARTIAL`/`FAILED`). Câu rớt tầng cứng → `AI_REJECTED` (tab "AI đã loại", chỉ Admin).

**D. Giao việc (S30)** — điều kiện: lô `READY_TO_ASSIGN`.
1. Chọn **nhóm A** (≥ 1 GV, khuyên ≥ 2), **GV B** (đúng 1, ∉ nhóm A, bắt buộc), `reviewDays` ≥ 1, `confirmDays` ≥ 1.
2. **Xem trước phân bổ:** chia đều theo (kỹ năng, CEFR, thứ tự sinh) vòng tròn cho từng A; chênh nhau tối đa 1 câu (100/5 = 20 mỗi người; 103 → 3 người 21, 2 người 20). Hạn A = cuối ngày (ngày giao + `reviewDays`) 23:59; hạn B = cuối ngày (ngày A gửi gói + `confirmDays`).
3. "Xác nhận giao" → tạo phân công theo từng câu, **tạo mỗi A một gói `OPEN`**, lô → `IN_REVIEW`, gửi email nhắc việc, đặt lịch nhắc **trước hạn 24 giờ** (mỗi nhóm một lần; hạn < 24 giờ lúc giao → nhắc ngay).
4. **Theo dõi (S29):** tiến độ theo GV/gói, "Quá hạn" (tính lazy, **chỉ cảnh báo**). **Chỉnh hạn (S31)** áp dụng cho việc chưa xử lý, tính lại hạn, đặt lại nhắc. **Giao lại**: chuyển câu chưa xử lý của một A sang A khác (hoặc đổi B của gói chưa gửi/chưa xử lý), vẫn B ∉ nhóm A. **Ép gửi gói** thay A (chỉ gói `OPEN`; hộp xác nhận nêu "đã duyệt X/Y câu"; chỉ mang theo câu A đã `FIRST_APPROVED`, câu chưa quyết nằm lại trong lô). Ba thao tác này là **biện pháp dự phòng** theo #121, không phải luồng thường.

**E. Kiểm tra cuối (C3) và Import (S32)** — điều kiện: lô `READY_TO_FINALIZE`.
1. Xem thống kê (Đã xác nhận vòng 2, Đã loại bởi A/B, AI đã loại, chưa xử lý/quá hạn).
2. Bấm **Kiểm tra** (C3, chạy theo thay đổi): báo cáo theo câu Qua/Cờ mềm/Lỗi cứng + mã lý do + câu nghi trùng + bản gốc so bản sửa; tổng hợp theo gói; số câu A sửa, tỉ lệ A/B loại. **Lỗi cứng → tự `AI_REJECTED`.** **Lỗi mềm → Admin quyết từng câu: "Chấp nhận (cho Import)" (ghi `ACCEPT_FLAG`) hoặc "Loại" (`REJECTED`).**
3. **Import** chỉ bật khi có báo cáo C3 **còn hiệu lực** (không câu nào đổi, ngân hàng không đổi kể từ lúc kiểm); nếu đổi → `FINAL_CHECK_STALE` → kiểm lại. Lúc Import, server vẫn chạy lại T1–T2 nhanh chống tranh chấp (hai Admin Import cùng lúc). Câu chưa xử lý (quá hạn) **không** được import.
4. Thành công: các câu qua → `FINAL_APPROVED` (ghi `approved_by`, `approved_at`, `calibrated=false`) → CAT dùng được.

**F. Hạn và dự phòng (chốt 18/10, #121):** đến hạn mọi GV phải hoàn thành việc được giao; **không có luồng riêng xử lý "câu tồn đọng" sau Import**. Chỉnh hạn, giao lại, ép gửi gói chỉ là biện pháp dự phòng của Admin trước khi chạy C3. Câu chưa quyết định không được import. (Đã gỡ hai đề xuất cũ: lô `FINAL_CHECKED` quay về `IN_REVIEW`; Admin loại câu chưa xử lý thành `REJECTED`.)

**G. Báo cáo / hồ sơ:** Admin xem S12–S14 như GV (mọi SV, không lỗi "không có quyền xem"), S12 thêm thẻ "Thống kê câu hỏi theo trạng thái".

### 4.6. Dòng thời gian liên role (ví dụ tổng — dữ liệu mẫu)
| Bước | Ai | Việc | Màn | Trạng thái sau |
|---|---|---|---|---|
| 1 | Admin | Tạo lô AI "Từ vựng B1", N = 100 | S26 → S29 | Lô `GENERATING` → `CHECKING` → `READY_TO_ASSIGN`; ~100 câu `DRAFT`, một số `AI_REJECTED` |
| 2 | Admin | Xem tab "AI đã loại", cờ mềm; **Giao việc**: A = {Lan, Hùng, Mai, Tú, Đức}, B = Bình, `reviewDays`=5, `confirmDays`=3 | S29 → S30 | Lô `IN_REVIEW`; 5 gói `OPEN` (20 câu mỗi gói); 5 email nhắc |
| 3 | GV A (Lan) | Duyệt 17 câu, sửa 3 câu, từ chối 3 câu → **Gửi cho B** | S33 → S11 | Gói của Lan `SENT` (17 câu `FIRST_APPROVED`); 3 câu `REJECTED` |
| 4 | GV B (Bình) | Mở gói của Lan, xác nhận 15, loại 2 | S34 → S35 | Gói `DONE`; 15 `SECOND_APPROVED`; 2 `REJECTED` |
| 5 | (hệ thống) | Mọi gói `DONE` hoặc mọi hạn qua | — | Lô `READY_TO_FINALIZE` |
| 6 | Admin | **Kiểm tra** (C3) → chấp nhận 1 cờ mềm → **Import** | S32 | Câu qua → `FINAL_APPROVED`; lô `DONE` nếu mọi câu ở trạng thái cuối |
| 7 | SV | Làm bài kỳ thi; CAT chọn từ các câu `FINAL_APPROVED` | S02–S04 | — |

### 4.7. Quy tắc nghiệp vụ (BR-01…BR-30) → hành vi trên giao diện
> Nguồn: SRS v3.0 Mục IXb (9b.6). Cột "Hành vi UI" là điều AI Agent phải thể hiện; quy tắc chỉ phía server ghi rõ "không có UI".

| BR | Tóm tắt quy tắc | Màn | Hành vi UI |
|---|---|---|---|
| BR-01 | Tài khoản chỉ do Admin tạo, không tự đăng ký | S01, S19, S24 | Không có nút/trang "Đăng ký"; tạo tài khoản chỉ ở S24 (form) và S19 (import) |
| BR-02 | Email duy nhất (không phân biệt hoa thường); MSSV, Mã GV duy nhất | S19, S24 | Form S24: lỗi ngay dưới ô trùng; S19: dòng trùng bị loại, popup "Tài khoản đã tồn tại" |
| BR-03 | Dòng import hợp lệ khi đủ cột bắt buộc, email đúng, không trùng lưới/CSDL | S19, S23, S27 | Dòng sai bị loại khỏi lưới + popup "Dòng {n} — {lý do}" |
| BR-04 | Lưu = một transaction mọi dòng trong lưới; lưới rỗng bị từ chối | S19, S23, S27 | Nút Lưu bật khi lưới không rỗng; `IMPORT_GRID_EMPTY` |
| BR-05 | Tài khoản mới có role, `mustChangePassword = true`; email gửi sau khi Lưu/tạo; gửi lỗi không rollback | S19, S24 | Sau Lưu: "Đã tạo {n} tài khoản, {m} email đã xếp hàng gửi"; không hiện mật khẩu; `🔶 BR-05` nơi hiển thị lỗi gửi (Mục 9) |
| BR-06 | Đổi mật khẩu: khác mật khẩu cũ, ≥ 8 ký tự (Q-4) | S16, S18 | Kiểm tra form; sau thành công cấp lại token |
| BR-07 | Chỉ Admin tạo/sửa/công bố/đóng kỳ và import danh sách thi | S20–S23 | Menu và route chỉ có ở Admin; GV/SV vào → 403 |
| BR-08 | `opensAt < closesAt`; DRAFT sửa tự do; SCHEDULED chỉ sửa tên và kéo dài giờ đóng; CLOSED không sửa `🔶` | S21 | Ô bị khóa theo trạng thái; CLOSED chỉ xem |
| BR-09 | Danh sách thi chỉ gồm tài khoản STUDENT đã tồn tại | S23 | MSSV không tồn tại → bị loại + popup |
| BR-10 | Bắt đầu phiên: thuộc kỳ, kỳ `OPEN`, chưa có phiên dở, chưa `COMPLETED` | S02, S03 | Nút Bắt đầu chỉ bật ở kỳ đang mở; lỗi `NOT_IN_ROUND`/`ROUND_NOT_OPEN`/`ROUND_ALREADY_COMPLETED`/`SESSION_IN_PROGRESS` |
| BR-11 | `expires_at` tính một lần; quá hạn: ≥ 8 câu → COMPLETED + TIMEOUT, ít hơn → ABANDONED | S04, S05, S07 | Đồng hồ đếm theo `expiresAt`; thông báo theo kết cục |
| BR-12 | Đóng kỳ thủ công: phiên đang chạy tiếp tục tới `expires_at` `🔶 Q-2` | S22 | Hộp xác nhận "Phiên đang làm bài vẫn tiếp tục…" |
| BR-13 | Báo cáo lọc theo kỳ, mặc định toàn hệ thống | S12, S36 | Chip lọc "Kỳ thi" gửi `examRoundId` |
| BR-14 | Quên mật khẩu: phản hồi luôn như nhau; OTP một lần, 10 phút, sai tối đa 5 lần | S17, S18 | Thông điệp trung tính; `INVALID_RESET_OTP`; `RATE_LIMITED` |
| BR-15 | Import ghi nhật ký kiểm toán (ai, khi nào, số dòng, kết quả) | — | **Không có UI** (chưa có màn nhật ký) |
| BR-16 | Phân quyền theo role và theo phân công; không đủ quyền → 403 | Mọi màn | Guard route + API; `NOT_ASSIGNED` → S15 (403) |
| BR-17 | Admin tạo/sửa/khóa GV; nâng/thu hồi Admin; không tự thu hồi mình | S24 | Nút "Nâng lên Admin"/"Thu hồi Admin" (tab GV), ẩn/khóa với chính mình |
| BR-18 | Ghi nhật ký nâng/thu hồi; không thu hồi Admin cuối `🔶`; token cũ mất quyền cũ | S24 | Thu hồi Admin cuối → bị từ chối, thông điệp rõ |
| BR-19 | Khóa tài khoản = không đăng nhập; không xóa cứng; gửi lại mật khẩu tạm | S24 | Nút Khóa/Mở khóa, Gửi lại mật khẩu tạm (hộp xác nhận); không có nút Xóa |
| BR-20 | Tạo từng người: nhập MSSV/Mã GV, họ tên, email; trùng → 409; import không cập nhật tài khoản có sẵn | S24, S19 | Form tạo lẻ; popup "đã tồn tại" |
| BR-21 | Câu hỏi chỉ vào qua lô; không form thêm câu; GV không import; Admin không sửa nội dung | S08, S10, S26, S27 | Không có nút Thêm/Sửa/Xóa; S26/S27 chỉ Admin |
| BR-22 | Giao việc: nhóm A ≥ 1, đúng một B ∉ A, hai số ngày ≥ 1, lô `READY_TO_ASSIGN` | S30 | Danh sách B loại trừ nhóm A; `CONFIRMER_IN_REVIEW_GROUP`; nút Xác nhận giao có điều kiện bật |
| BR-23 | Chia đều vòng tròn, chênh tối đa 1 câu | S30 | Bảng xem trước phân bổ |
| BR-24 | Hạn cuối ngày 23:59 giờ VN; nhắc trước 24 giờ; quá hạn chỉ cảnh báo | S31, S33–S35 | C-DUE; chỉnh hạn chỉ áp dụng việc chưa xử lý |
| BR-25 | A chỉ Gửi khi mọi câu đã quyết; gửi một lần; sau gửi không sửa | S11, S33 | Nút "Gửi cho B" tắt khi còn câu chưa quyết; `PACKAGE_INCOMPLETE`; sau gửi gói chỉ đọc |
| BR-26 | B chỉ đọc: Xác nhận/Loại từng câu hoặc "Xác nhận tất cả câu còn lại"; không trả về A | S35 | Không có ô sửa, không có nút trả về |
| BR-27 | Sửa xong chạy lại luật cứng và T1–T2; hỏng/trùng chặn Duyệt | S11 | `INVALID_AFTER_EDIT`/`DUPLICATE_AFTER_EDIT`; Duyệt bị khóa |
| BR-28 | Import khi lô `READY_TO_FINALIZE` và có báo cáo C3 còn hiệu lực | S32 | Nút Import khóa tới khi có báo cáo hợp lệ; `FINAL_CHECK_REQUIRED`/`STALE`/`BATCH_NOT_READY_TO_FINALIZE` |
| BR-29 | Người loại → REJECTED (không lý do); máy loại → AI_REJECTED (chỉ Admin thấy); lỗi mềm Admin quyết | S29, S32, S11, S35 | Hộp thoại Từ chối/Loại bỏ không có ô lý do; tab "AI đã loại" chỉ Admin; Chấp nhận/Loại lỗi mềm |
| BR-30 | Item một chiều; `FINAL_APPROVED` cấm sửa; `irt_b` ∈ [−4, +4]; câu mới `calibrated = false` | S10, S27 | Dải chỉ đọc ở S10; dòng import `irt_b` ngoài khoảng bị loại |

### 4.8. Tình huống ngoại lệ và biên theo role (nguồn: bảng đặc tả UC)
**Student**
- **Hết thời gian khi nộp (UCSV03 3a):** server kiểm `now > expiresAt` → áp K5 (≥ 8 câu `COMPLETED` + `TIMEOUT`; < 8 câu `ABANDONED`, cho thi lại nếu kỳ còn mở).
- **Mất mạng khi nộp (UCSV03 2a):** giữ đáp án tạm ở trình duyệt, tự gửi lại khi có mạng; dải C-OFFLINE khóa nút nộp trong lúc mất mạng.
- **Vào thi lúc kỳ sắp đóng (UCSV02 AC):** ví dụ kỳ 10:00–11:00, thời lượng 45 phút, vào 10:45 → `expiresAt` = 11:00 (còn 15 phút); S03 hiện đúng "thời gian làm bài còn lại" tính tới `closesAt`.
- **Đã có phiên dở (UCSV02 4a):** S03 nhận 409 `SESSION_IN_PROGRESS` kèm `sessionId` → hộp thoại "Bạn đang có một bài thi dở dang" với nút tiếp tục.
- **Quên mật khẩu (UCSV09):** email không tồn tại vẫn trả thông điệp trung tính; nhập sai OTP 5 lần → mã bị hủy, phải xin mã mới.
- **Xem lại đáp án tắt (UCSV05, K6):** hiện "Chức năng xem lại đáp án hiện đang tạm đóng."

**Teacher**
- **Không được giao việc:** Hộp việc rỗng ("Bạn chưa có việc nào được giao."); `/teacher/item-bank` rỗng.
- **Mở câu/gói không phải của mình:** 403 `NOT_ASSIGNED` → S15.
- **Sửa xong bị trùng (UCGV14 4a):** lưu bị từ chối, nội dung cũ giữ nguyên, Duyệt bị khóa.
- **Gửi gói khi còn câu chưa quyết (UCGV14 8a):** 409 `PACKAGE_INCOMPLETE`.
- **Hạn sắp hết (UCGV14 2a):** nhận email nhắc trước 24 giờ; việc vẫn hiện trong Hộp việc (không có chuông).
- **GV B cố sửa hoặc trả về A (UCGV15 3a):** không có thao tác tương ứng trên UI; gọi API → 403/400.
- **Tra cứu SV không tồn tại (UCGV09):** "Không tìm thấy sinh viên."; SV chưa có hồ sơ: "Sinh viên chưa có hồ sơ năng lực."

**Admin**
- **Import tài khoản (UCADM08):** file sai định dạng/quá 2 MB/quá 1000 dòng → `IMPORT_FILE_INVALID`; lưới hết hạn → 410; Lưu khi rỗng → 422; email gửi lỗi không rollback (`🔶 BR-05`).
- **Quản lý tài khoản (UCADM09):** trùng email/MSSV/Mã GV → 409 ngay dưới ô; tự thu hồi quyền mình → 400; thu hồi Admin cuối → bị chặn.
- **Kỳ thi (UCADM15):** `opensAt ≥ closesAt` hoặc thời lượng > khoảng mở–đóng → lỗi form; Công bố khi chưa có SV → bị khóa với `title`; sửa kỳ CLOSED → bị chặn.
- **Import danh sách thi (UCADM16):** MSSV chưa có tài khoản → bị loại, popup nhắc import tài khoản trước (S19); gỡ SV chỉ khi chưa có phiên.
- **Theo dõi dự thi (UCADM17):** dữ liệu cập nhật theo thời gian thực (làm mới định kỳ `[D]` 15 giây khi kỳ `OPEN`); xuất CSV/Excel `⚠️ ĐX`.
- **Tạo lô AI (UCADM11):** hết ngân sách hoặc hết vòng bù → lô `PARTIAL`; Gemini lỗi → tự chuyển nhà cung cấp dự phòng, thất bại hoàn toàn → lô `FAILED`.
- **Giao việc (UCADM13):** B trùng nhóm A → 409; nhóm A rỗng → lỗi form; lô không ở `READY_TO_ASSIGN` → dải thông báo.
- **Kiểm tra C3 và Import (UCADM14):** lô chưa `READY_TO_FINALIZE` → 409 `BATCH_NOT_READY_TO_FINALIZE` (nút Kiểm tra khóa); ngân hàng đổi trong lúc chờ → `FINAL_CHECK_STALE`; lỗi cứng ở C3 → tự `AI_REJECTED` và không được import.


---

## 5. ĐẶC TẢ MÀN HÌNH — XÁC THỰC VÀ SINH VIÊN

> Khuôn mỗi màn: (a) Thông tin chung · (b) Bố cục · (c) Thành phần · (d) Hành động · (e) Trạng thái đặc thù · (f) Dữ liệu mẫu · (g) AC. Trạng thái chung (tải/rỗng/lỗi/offline) xem Mục 2.6; chỉ ghi phần **đặc thù**.

### S01 — Đăng nhập
**(a)** Route `/login` · Layout L-AUTH (hai nửa) · Ai vào: chưa đăng nhập; đã đăng nhập → tự chuyển trang chủ theo role · API `POST /auth/login` · UC UCSV01/UCGV01/UCADM01.
**(b)**
```
┌───────────────────────────────┬───────────────────────────────┐
│  (nền #EFF6FF)                │  (nền trắng)                  │
│  [logo]                       │   Đăng nhập                   │
│  Đo đúng năng lực, không mất  │   Dùng tài khoản do trường    │
│  thời gian vào câu quá dễ     │   cấp để làm bài kiểm tra.    │
│  hay quá khó.                 │   Email *                     │
│  ~~~ đường cong chữ S ~~~     │   [____________________]      │
│                               │   Mật khẩu *                  │
│                               │   [______________] [Hiện]     │
│                               │   [dải lỗi — chỉ khi có lỗi]  │
│                               │   [      Đăng nhập      ]     │
│                               │   Quên mật khẩu?              │
└───────────────────────────────┴───────────────────────────────┘
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Tiêu đề "Đăng nhập" 24 px đậm; dòng phụ 14 px xám "Dùng tài khoản do trường cấp để làm bài kiểm tra." | — | — |
| 2 | Ô **Email** (type=email, autocomplete=username) | `login-id` | Bắt buộc; nhãn **"Email"** (không còn "Email hoặc MSSV"); cắt khoảng trắng đầu/cuối; so khớp không phân biệt hoa thường (server). Lỗi định dạng: "Email không hợp lệ." |
| 3 | Ô **Mật khẩu** (C-PASSWORD, autocomplete=current-password) | `login-password` | Bắt buộc; nút "Hiện/Ẩn" đổi `type` |
| 4 | Dải lỗi (đỏ nhạt, phía trên nút) | `login-error` | Chỉ hiện khi API lỗi; `role="alert"` |
| 5 | Nút chính **"Đăng nhập"** (rộng đầy, cao 48 px) | `login-submit` | Vô hiệu khi Email hoặc Mật khẩu trống; Enter trong ô = bấm |
| 6 | Liên kết chữ **"Quên mật khẩu?"** | `forgot-password-link` | → `/forgot-password` |
| — | **KHÔNG có:** nút Google/SSO, "Ghi nhớ đăng nhập", đăng ký, bộ chọn Đơn vị | | |
**(d)**
- Bấm Đăng nhập → khóa nút + spinner → `POST /auth/login`.
  - OK, `mustChangePassword=true` → `/change-password`. OK bình thường → trang chủ theo role (Mục 3.1) hoặc `?next=` nếu hợp lệ cùng role.
  - 401 → dải lỗi "Thông tin đăng nhập không chính xác." (giữ nguyên Email, xóa Mật khẩu, focus vào Mật khẩu).
  - Khóa → "Tài khoản đã bị khóa, vui lòng liên hệ quản trị viên."
  - Mạng → "Không kết nối được máy chủ, vui lòng thử lại."
**(e)** Điện thoại: bỏ nửa trái, chỉ logo căn giữa phía trên biểu mẫu. Đang gửi: khóa cả hai ô và nút.
**(f)** Mock: không cần dữ liệu; tài khoản thử `sv0001@example.edu.vn` (giả).
**(g)** AC: đúng thông tin → trang chủ; sai → giữ Email + hiện lỗi; token **không** ở `localStorage`; không có nút SSO.

---

### S16 — Đổi mật khẩu (dùng chung 3 role)
**(a)** Route `/change-password` · L-AUTH (thẻ ≤ 420 px) · Ai vào: mọi role đã đăng nhập · API `POST /auth/change-password {currentPassword,newPassword}` · UC UCSV08 `⚠️ ĐX`.
**(b)**
```
            [logo nhỏ]
┌──────────────────────────────────────┐
│ Đổi mật khẩu                          │
│ (chỉ lần đầu) Đây là lần đăng nhập    │
│ đầu tiên. Vui lòng đặt mật khẩu mới   │
│ để tiếp tục.                          │
│ Mật khẩu hiện tại *   [__________][Hiện]│
│ Mật khẩu mới *        [__________][Hiện]│
│   gợi ý: khác mật khẩu cũ; tối thiểu 8 │
│ Nhập lại mật khẩu mới *[_________][Hiện]│
│ [        Đổi mật khẩu        ]         │
└──────────────────────────────────────┘
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Dòng phụ lần đầu | `cp-first-login-note` | Chỉ hiện khi vào do `mustChangePassword=true`; khi đó **ẩn mọi điều hướng**, không có nút "Hủy" |
| 2 | Mật khẩu hiện tại (C-PASSWORD) | `cp-current` | Bắt buộc. Lần đầu: là mật khẩu tạm trong email |
| 3 | Mật khẩu mới (C-PASSWORD) + dòng gợi ý quy tắc | `cp-new` | Bắt buộc; ≠ mật khẩu hiện tại; độ dài tối thiểu **8** `🔶 Q-4` (đọc từ cấu hình, không hardcode) |
| 4 | Nhập lại mật khẩu mới | `cp-confirm` | Phải trùng ô 3: "Mật khẩu nhập lại không khớp." |
| 5 | Nút chính "Đổi mật khẩu" | `cp-submit` | Vô hiệu khi còn ô trống / không khớp |
| 6 | Nút chữ "Hủy" (chỉ khi đổi tự nguyện, không bị buộc) `⚠️ ĐX` | `cp-cancel` | Quay lại trang trước |
**(d)** Bấm → `POST /auth/change-password`: OK → toast "Đã đổi mật khẩu." → trang chủ theo role (token được cấp lại, `mustChangePassword=false`). Lỗi: "Mật khẩu hiện tại không đúng." · "Mật khẩu mới phải khác mật khẩu hiện tại." · "Mật khẩu mới chưa đạt yêu cầu (tối thiểu 8 ký tự)."
**(e)** Mọi route khác trả `403 PASSWORD_CHANGE_REQUIRED` → FE chuyển về đây.
**(g)** AC: không thể rời màn khi bị buộc (trừ Đăng xuất); sau đổi thành công không còn bị chặn.

---

### S17 — Quên mật khẩu
**(a)** Route `/forgot-password` · L-AUTH (thẻ ≤ 420 px) · API `POST /auth/forgot-password {email}` (**luôn 202**) · UC UCSV09 `⚠️ ĐX`.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Tiêu đề "Quên mật khẩu"; dòng phụ "Nhập email của bạn, chúng tôi sẽ gửi mã xác nhận 6 chữ số." | — | |
| 2 | Ô **Email** | `fp-email` | Bắt buộc, đúng định dạng |
| 3 | Nút chính "Gửi mã xác nhận" | `fp-submit` | Vô hiệu khi trống/sai định dạng; sau khi gửi khóa 30 giây `[D]` |
| 4 | Nút chữ "Quay lại đăng nhập" | `fp-back` | → `/login` |
| 5 | Khối kết quả (sau khi gửi) | `fp-sent` | Thông điệp **trung tính y hệt** dù email có tồn tại: "Nếu email tồn tại trong hệ thống, chúng tôi đã gửi mã xác nhận 6 chữ số (hiệu lực 10 phút)." + nút "Nhập mã xác nhận" → `/reset-password` (mang `?email=`) |
**(d/e)** 429 `RATE_LIMITED` → "Bạn thao tác quá nhanh, vui lòng thử lại sau." (giới hạn theo email + IP). Không bao giờ tiết lộ email có tồn tại hay không (BR-14).
**(g)** AC: thông điệp giống nhau với email tồn tại/không tồn tại.

---

### S18 — Đặt lại mật khẩu
**(a)** Route `/reset-password` · L-AUTH (thẻ ≤ 420 px) · API `POST /auth/reset-password {email,otp,newPassword}` · UC UCSV09 `⚠️ ĐX`.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Ô Email (điền sẵn nếu có `?email=`) | `rp-email` | Bắt buộc |
| 2 | Ô **Mã xác nhận (6 chữ số)** | `rp-otp` | `inputmode=numeric`, đúng 6 chữ số, tự bỏ ký tự không phải số |
| 3 | Ô Mật khẩu mới (C-PASSWORD) | `rp-new` | Chính sách như S16 (`🔶 Q-4`) |
| 4 | Ô Nhập lại mật khẩu mới | `rp-confirm` | Phải khớp |
| 5 | Nút chính "Đặt lại mật khẩu" | `rp-submit` | Vô hiệu khi thiếu/không hợp lệ |
| 6 | Liên kết "Chưa nhận được mã? Gửi lại" | `rp-resend` | → `/forgot-password` |
**(d)** OK → toast/dải xanh "Đã đặt lại mật khẩu. Vui lòng đăng nhập." → `/login` (**không tự đăng nhập**). `INVALID_RESET_OTP` → "Mã không đúng hoặc đã hết hạn." (mã nhập sai quá 5 lần bị hủy, phải xin mã mới).
**(g)** AC: OTP dùng một lần; thành công xóa `mustChangePassword`.

---

### S02 — Trang chủ sinh viên
**(a)** Route `/student/dashboard` · L-STUDENT (nội dung ≤ 720 px) · API `GET /exam-rounds/mine`, `GET /sessions/active` (trả thêm `expiresAt` + thông tin kỳ), kết quả gần nhất từ `GET /placement-profiles/:id/history` · UC UCSV02, UCSV07.
**(b)**
```
Xin chào, Minh Anh                                 (24 px đậm)
Chọn kỳ thi đang mở để làm bài kiểm tra xếp lớp.   (16 px xám)

Kỳ thi của tôi
┌───────────────────────────────────────────┐
│ XẾP LỚP ANH VĂN ĐẦU KHÓA        [Đang mở] │
│ 10:00–11:00 · 60 phút · tối đa 25 câu     │
│                          [ Bắt đầu bài thi ]│
├───────────────────────────────────────────┤
│ XẾP LỚP BỔ SUNG                  [Chưa mở]│
│ Mở lúc 14:00, 15/10/2026                  │
└───────────────────────────────────────────┘
Kết quả gần nhất
┌───────────────────────────────────────────┐
│ [ A2 ]   Ngày 10/10/2026 · 25 câu         │
│          Xem kết quả →   Lịch sử bài thi →│
└───────────────────────────────────────────┘
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Lời chào chữ thuần "Xin chào, {tên}" + dòng phụ hướng dẫn việc kế tiếp | — | Không biểu tượng cảm xúc |
| 2 | **Thẻ "Kỳ thi của tôi"** (danh sách) | `my-rounds` | Mỗi kỳ SV thuộc là một hàng `round-card-{id}`: tên kỳ (đậm), C-BADGE trạng thái (Chưa mở/Đang mở/Đã đóng/Đã thi), dòng phụ "giờ mở–đóng · {durationMinutes} phút · tối đa 25 câu" (kỳ chưa mở: "Mở lúc HH:mm, dd/MM/yyyy") |
| 3 | Nút chính **"Bắt đầu bài thi"** trong hàng kỳ | `start-exam` | **Chỉ bật khi kỳ Đang mở** và SV chưa có phiên hoàn thành trong kỳ và không có bài dở; bấm → `/student/exams/[roundId]`. Kỳ khác: không hiện nút (hoặc tắt kèm `title` lý do) |
| 4 | **Biến thể bài dở dang** (thay hàng kỳ tương ứng) | `resume-banner` | Viền cam nhạt `#FEF3C7`; tiêu đề "Bạn đang có một bài thi dở dang."; dòng "Đã làm {n} câu · còn {mm:ss}" (tính theo `expiresAt`); nút chính **"Tiếp tục bài thi"** `resume-btn` → `/student/exams/[roundId]/take`; **không hiện nút Bắt đầu** ở kỳ đó |
| 5 | Thẻ **"Kết quả gần nhất"** | `latest-result` | Chỉ hiện khi có kết quả: huy hiệu CEFR lớn, "Ngày dd/MM/yyyy · {n} câu", liên kết "Xem kết quả →" (S05), "Lịch sử bài thi →" (S07). Chưa thi: thay bằng dòng xám "Bạn chưa hoàn thành bài thi nào." |
**(e)** Rỗng (chưa thuộc kỳ nào): "Bạn chưa thuộc kỳ thi nào. Vui lòng liên hệ quản trị viên." · Lỗi tải trạng thái phiên: vẫn cho vào, dải cảnh báo nhỏ, **không chặn** · Bài bị hủy do hết giờ < 8 câu: dải thông tin đầu trang "Bài thi trước bị hủy do hết thời gian khi làm chưa đủ 8 câu." `[D]`.
**(f)** Mock: 2 kỳ (Đang mở, Chưa mở) + 1 kết quả A2.
**(g)** AC: nút Bắt đầu chỉ bật ở kỳ Đang mở; có bài dở → chỉ có "Tiếp tục"; số phút hiển thị = `durationMinutes` của kỳ (không cố định 45).

---

### S03 — Giới thiệu bài thi `⚠️ ĐX` (route mới)
**(a)** Route `/student/exams/[roundId]` · L-STUDENT (thẻ ≤ 600 px) · API `POST /sessions {examRoundId}` · UC UCSV02.
**(b)** Một thẻ trắng căn giữa: tiêu đề "Trước khi bắt đầu"; dưới tiêu đề: **tên kỳ** + "Kỳ đóng lúc HH:mm, dd/MM (còn {x})"; danh sách 6 dòng (biểu tượng tuyến nét mảnh + 1 câu); chân thẻ 2 nút.
**(c)**
| # | Thành phần | testid | Nội dung |
|---|---|---|---|
| 1 | Tiêu đề + tên kỳ + giờ còn lại tới `closesAt` | `intro-round` | |
| 2 | 6 dòng quy tắc | `intro-rules` | (1) Tối đa 25 câu. (2) Thời lượng {durationMinutes} phút và không vượt giờ đóng kỳ — vào muộn thì chỉ còn phần thời gian còn lại. (3) Mỗi người một đề vì câu hỏi thay đổi theo năng lực. (4) Không thể quay lại câu trước. (5) Không hiện đúng/sai trong lúc làm. (6) Có thể kết thúc sớm khi hệ thống đã đủ tin cậy — kết quả và đáp án xem được sau khi hoàn thành. |
| 3 | Nút chính **"Tôi đã hiểu, bắt đầu làm bài"** | `confirm-start` | Chỉ bấm một lần (khóa ngay khi bấm) |
| 4 | Nút chữ "Quay lại" | `intro-back` | → S02 |
**(d)** `POST /sessions {examRoundId}`: OK → `/student/exams/[roundId]/take`. Lỗi: `NOT_IN_ROUND` / `ROUND_NOT_OPEN` / `ROUND_ALREADY_COMPLETED` → dải lỗi trong thẻ (thông điệp ở Mục 2.3); `SESSION_IN_PROGRESS` → **hộp thoại** "Bạn đang có một bài thi dở dang." với nút chính "Tiếp tục bài thi" và nút chữ đỏ "Hủy bài cũ và bắt đầu lại" `🔶 O4` (**chưa có endpoint** → vẽ nút nhưng vô hiệu kèm `title` "Chưa hỗ trợ"); chưa có đề: "Hệ thống chưa sẵn sàng, vui lòng thử lại sau."
**(e)** Truy cập `/student/exams/[roundId]` của kỳ SV không thuộc → 403.
**(g)** AC: bấm hai lần chỉ tạo một phiên; lỗi theo mã hiển thị đúng thông điệp.

---

### S04 — Làm bài (khung tập trung)
**(a)** Route `/student/exams/[roundId]/take` · **L-FOCUS** · API `GET /sessions/active` (lấy phiên của kỳ), `GET /sessions/:id/next-item`, `POST /sessions/:id/responses`, `GET /sessions/:id/resume` · UC UCSV03. Không có phiên `IN_PROGRESS` → chuyển về `/student/exams/[roundId]`.
**(b)**
```
Câu 8  (tối đa 25)                                   ⏱ 18:42
─────────────────────────────────────────────────────────────
                         [Ngữ pháp]
            She ____ to school every day.

            ┌───────────────────────────────┐
            │ A   go                        │
            └───────────────────────────────┘
            ┌───────────────────────────────┐
            │ B   goes                      │   ← đang chọn (viền xanh 2px, nền #DBEAFE, dấu ✓)
            └───────────────────────────────┘
            │ C   going │   │ D   gone │
─────────────────────────────────────────────────────────────
                                      [   Nộp đáp án   ]
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Số câu "Câu {n} (tối đa 25)" (trái) | `question-index` | Không hiện thanh tiến độ tới 25 |
| 2 | Đồng hồ ⏱ mm:ss (phải) | `timer` | Đếm ngược theo **`expiresAt` của phiên** (= min(thời lượng kỳ, giờ đóng kỳ)), **không phải 45 cố định**; bình thường xám đậm; còn < 5 phút → cam + biểu tượng đồng hồ + thông báo cho trình đọc màn hình (`aria-live`); đồng bộ lại với server khi mở lại |
| 3 | Chip kỹ năng ("Từ vựng"/"Ngữ pháp") | `question-skill` | |
| 4 | Nội dung câu hỏi (20 px) | `question-content` | |
| 5 | 4 thẻ phương án A–D (radio, cao ≥ 56 px, chữ cái A–D trong ô vuông bên trái) | `option-A`…`option-D` | Chọn nhanh bằng phím A–D hoặc 1–4; chỉ chọn được 1 |
| 6 | Nút chính **"Nộp đáp án"** | `submit-answer` | Vô hiệu khi chưa chọn; cố định đáy màn hình trên điện thoại; nộp hai lần chỉ ghi một lần |
**KHÔNG hiển thị (tuyệt đối):** đúng/sai, điểm năng lực θ, SE, mức CEFR tạm tính, nút quay lại/bỏ qua/gợi ý, thanh tiến độ tới 25, logo/menu/avatar.
**(d)** Nộp → khóa tất cả + spinner → `POST responses` → tải câu kế (skeleton; quá 1 giây hiện "Đang chuẩn bị câu tiếp theo…") hoặc, nếu đã dừng, chuyển `/student/results/[sessionId]`. F5 → quay lại đúng câu cũ (`resume`).
**(e)** Trạng thái cần vẽ: chưa chọn · đã chọn · đang nộp · đang chuẩn bị câu kế · **lỗi mạng khi nộp** (giữ lựa chọn + "Thử lại") · mất kết nối (C-OFFLINE, khóa nút nộp) · còn 5 phút · **hết giờ**: "Đã hết thời gian, đang chuyển đến kết quả…" → S05 (≥ 8 câu) hoặc S02 kèm thông báo hủy (< 8 câu).
**(f)** Mock: 1 câu Ngữ pháp, 4 phương án, đồng hồ 18:42.
**(g)** AC: nút nộp tắt khi chưa chọn; nộp xong tự chuyển câu mà không hiện đúng/sai; F5 về đúng câu; hết giờ → màn kết quả/S02 đúng luật.

---

### S05 — Kết quả
**(a)** Route `/student/results/[sessionId]` · L-STUDENT (cột đơn ≤ 720 px) · API `GET /sessions/:id/result` · UC UCSV04. SV khác mở kết quả của mình → 403.
**(c)** Các khối là thẻ trắng xếp dọc, theo thứ tự:
| # | Khối | testid | Nội dung / quy tắc |
|---|---|---|---|
| 1 | **Tóm tắt** | `cefr-badge` | Huy hiệu CEFR rất lớn (nền theo thang CEFR) + "Độ tin cậy: Cao/Vừa/Thấp" + một câu lý do dừng (nhãn `stoppingReason`, Mục 2.2) |
| 2 | **Năng lực** | `theta-value`, `se-value`, `ci-value` | Dải ngang chia 6 đoạn Pre-A1…C1+ theo màu CEFR, một chấm đánh dấu vị trí; 3 số nhỏ: θ = -0,28 · SE = 0,31 · KTC 95% = [-0,89 ; 0,33]; biểu tượng (i): "θ là thước đo năng lực; càng cao càng giỏi." |
| 3 | **Theo kỹ năng** | `skill-vocab`, `skill-grammar` | **2 thanh ngang** (không radar): "Từ vựng 68% (ước lượng B1, 9/14 đúng)", "Ngữ pháp 52% (ước lượng A2, 6/11 đúng)". Thiếu dữ liệu → "Đang cập nhật" (không bịa số) |
| 4 | **Chủ đề cần cải thiện** | `error-patterns` | Bảng gọn: chủ đề, kỹ năng, đúng/đã làm, tỉ lệ, mức nghiêm trọng (Nhẹ/Trung bình/Nghiêm trọng, huy hiệu chữ); sắp nghiêm trọng nhất trước |
| 5 | **Gợi ý học tập (AI)** | `recommendations` | 2–3 gạch đầu dòng, ví dụ "Ưu tiên luyện Past Simple và Past Continuous trước."; rỗng → ẩn khối |
| 6 | **Thông tin bài thi** | `exam-info` | Số câu, thời gian làm |
| 7 | **Banner vùng biên** (vàng nhạt, chỉ khi có) | `boundary-notice` | C1+: "Năng lực của bạn vượt ngoài phạm vi đánh giá hiện tại (C1+). Vui lòng liên hệ Giảng viên để được tư vấn bổ sung." · Pre-A1: "Năng lực của bạn chưa đến mức A1. Vui lòng liên hệ Giảng viên để được hỗ trợ thêm." |
| 8 | Chân trang | `open-review` | Nút chính **"Xem giải thích chi tiết"** → S06; nút chữ "Về trang chủ" → S02 |
**(e)** Đang tổng hợp: "Đang tổng hợp kết quả…" · lỗi. **Không cuộn ngang ở 360 px.**
**(e2) Theo trạng thái phiên (UCSV04):** chỉ phiên `COMPLETED` của chính SV mới có kết quả. Phiên còn `IN_PROGRESS` → không trả kết quả, hiện thẻ "Bạn đang có bài thi dở dang" + nút "Tiếp tục bài thi" (S04). Phiên `ABANDONED` → "Bài thi này không có kết quả vì hết thời gian khi chưa đủ 8 câu." + (nếu kỳ còn mở) nút "Thi lại" → S02. Không tìm thấy phiên → 404; phiên của người khác → 403.
**(f)** Mock: A2, θ=-0,28, SE=0,31, KTC [-0,89; 0,33], Từ vựng 68%, Ngữ pháp 52%.
**(g)** AC: không cuộn ngang 360 px; chỉ 2 kỹ năng, không radar; SV khác → 403.

---

### S06 — Xem lại đáp án
**(a)** Route `/student/results/[sessionId]/review` · L-STUDENT · API `GET …/review` · UC UCSV05 · cờ `REVIEW_ENABLED` `🔶 K6`.
**(b)** Máy tính hai cột: trái (280 px) danh sách câu; phải chi tiết câu đang chọn. Điện thoại: thanh cuộn ngang các số câu (tròn, ✓/✕) ở trên, chi tiết ở dưới.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Danh sách câu | `review-list` | Mỗi dòng `review-item-{n}`: "3 · ✕ Sai · Ngữ pháp" / "4 · ✓ Đúng · Từ vựng" (biểu tượng **và** chữ) |
| 2 | Câu hỏi + 4 phương án | — | Phương án SV chọn có nhãn **"Bạn đã chọn"** (`chosen-mark`); đáp án đúng có nhãn **"Đáp án đúng"** (`correct-mark`) |
| 3 | Khối **Giải thích** | `explanation-general`, `explanation-option-A..D` | "Giải thích chung" rồi giải thích riêng từng phương án A–D. Giải thích do AI sinh **sẵn cùng lúc sinh câu**, dùng chung mọi SV |
| 4 | Chân | — | Nút "Câu trước", "Câu sau", "Về kết quả" |
**(e)** Không có giải thích: "Câu này chưa có giải thích." · lỗi: "Không thể tải giải thích lúc này, vui lòng thử lại sau." · tạm đóng (`REVIEW_ENABLED=false`): "Chức năng xem lại đáp án hiện đang tạm đóng." + nút về kết quả `🔶 K6` · danh sách rỗng. **Chặn đáp án:** phiên chưa `COMPLETED` → 409, không trả đáp án đúng của câu nào; phiên của người khác → 403 (SRS 15.3: đáp án đúng chỉ trả về sau khi nộp). Hai SV làm cùng một câu thấy **cùng một giải thích** (một bản gắn `Item`, không sinh lại).

---

### S07 — Lịch sử bài thi
**(a)** Route `/student/history` · L-STUDENT (≤ 1120 px) · API `GET /placement-profiles/:id/history` · UC UCSV06.
**(c)** Máy tính: bảng 5 cột (Ngày thi · Số câu · CEFR (huy hiệu) · θ · SE), hàng cao 56 px, mới nhất trên cùng, bấm hàng → S05 (`history-row-{sessionId}`). Có thể thêm cột **"Kỳ thi"** `⚠️ ĐX` (chưa duyệt). Điện thoại: danh sách thẻ (huy hiệu CEFR + ngày + "25 câu").
**(e)** Rỗng: "Bạn chưa hoàn thành bài thi nào." + nút chính "Bắt đầu bài thi" → S02.
**(e2) Dòng theo trạng thái (UCSV06):** `COMPLETED` → bấm xem S05; `IN_PROGRESS` còn hạn → nhãn "Đang làm dở" + nút "Tiếp tục" → S04; `ABANDONED` → nhãn "Bị hủy (hết giờ)", không bấm xem kết quả. Chỉ hiện phiên của chính SV; sửa `student_id` trên URL → 403.

---

### S15 — Trang lỗi chung
**(a)** `403`, `404`, `500` · căn giữa dọc: số lớn xám nhạt, một câu giải thích, nút "Về trang chủ" (theo role); 500/ngoại tuyến thêm "Thử lại". 403: "Bạn không có quyền truy cập trang này." Admin mở nhầm đường dẫn SV → 403, nút về `/admin/dashboard`.

---

## 6. ĐẶC TẢ MÀN HÌNH — GIẢNG VIÊN (TEACHER)

> Layout mọi màn: **L-SIDEBAR** (menu TEACHER, Mục 2.4). Màn S08/S10/S12–S14 Admin dùng chung (khác biệt nêu rõ ở từng màn). Khung tab "Hộp việc" (Cần duyệt | Cần xác nhận) đặt ở đầu S33 và S34.

### S33 — Hộp việc: Cần duyệt (GV vai A)
**(a)** Route `/teacher/tasks/reviews` · Guard TEACHER · API `GET /me/review-tasks`, `POST /item-packages/mine/send` · UC UCGV14 (thay UCGV05).
**(b)**
```
Hộp việc          [ Cần duyệt (2) ]  [ Cần xác nhận (1) ]
┌──────────────────────────────────────────────────────────┐
│ Lô "Từ vựng B1 – đợt 1"                       [Còn 5 ngày] │
│ Đã quyết 12 / 20   ███████████░░░░░░░                      │
│ Hạn: 25/10/2026 23:59                                      │
│ Còn 8 câu chưa quyết định                                  │
│                           [ Mở gói ]   [ Gửi cho B ] (tắt) │
└──────────────────────────────────────────────────────────┘
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Khung tab Hộp việc + huy hiệu số | `tasks-tabs` | Tab hiện tại gạch chân xanh |
| 2 | Danh sách thẻ — **mỗi thẻ = gói của GV này trong một lô** | `inbox-review-list`, `inbox-batch-{id}` | Tên lô; C-PROGRESS "Đã quyết x / y" (y = số câu giao cho mình); C-DUE theo `due_at` (cuối ngày giao + `reviewDays`, 23:59:59 giờ VN); dòng phụ "Còn k câu chưa quyết định" |
| 3 | Nút phụ **"Mở gói"** | `open-package-{id}` | → `/teacher/tasks/reviews/[packageId]` (mở tại câu đầu chưa quyết) |
| 4 | Nút chính **"Gửi cho B"** | `send-package-{batchId}` | **Tắt** cho tới khi mọi câu đã Duyệt hoặc Từ chối (`title`: "Còn x câu chưa quyết định"); gói `SENT`/`DONE` → ẩn nút, thẻ hiện huy hiệu "Đã gửi" và chỉ đọc |
**(d)** "Gửi cho B" → C-DIALOG: tiêu đề "Gửi cho giảng viên xác nhận?", nội dung "Sau khi gửi, bạn không thể sửa lại các câu trong gói. Câu bạn đã từ chối sẽ không được gửi đi." → [Hủy] [Gửi] → `POST /item-packages/mine/send` → OK: thẻ chuyển "Đã gửi", toast "Đã gửi gói cho giảng viên xác nhận." · `PACKAGE_INCOMPLETE` → "Còn câu chưa quyết định, chưa thể gửi gói." (làm mới tiến độ).
**(e)** Rỗng: "Bạn chưa có câu nào cần duyệt." · Quá hạn: C-DUE đỏ "Quá hạn" **nhưng vẫn thao tác được**.
**(f)** Mock: 2 thẻ (12/20 còn 5 ngày; 20/20 đã gửi).
**(g)** AC: nút Gửi chỉ bật khi mọi câu đã quyết; gửi một lần; câu A loại không vào gói.

---

### S11 — Duyệt gói và từng câu (GV vai A)
**(a)** Route `/teacher/tasks/reviews/[packageId]` (chọn câu bằng `?item={itemId}`) `[D]` · Guard: **chỉ GV A đúng người** (khác → 403 `NOT_ASSIGNED`) · API `GET /me/review-tasks`, `PATCH /items/:id`, `POST /items/:id/approve|reject`, `POST /item-packages/mine/send` · UC UCGV14 (gồm UCGV04 sửa câu).
**(b)** Bố cục chia đôi (điện thoại: danh sách trước, chạm câu mới sang chi tiết).
```
Lô "Từ vựng B1 – đợt 1"        Đã quyết 12 / 20      Hạn: 25/10 23:59   [Còn 5 ngày]
┌─ Danh sách câu ───────┬─ Câu 13/20 ─────────────────────────────────────────┐
│ 1 ✓ Đã duyệt          │ (!) Gần giống một câu trong ngân hàng [xem câu đó]   │ ← C-FLAG
│ 2 ✕ Đã từ chối        │ Nội dung *                                           │
│ …                     │ [_____________________________________________]    │
│ 13 • Chưa quyết  ◄    │ A [______]  B [______]  C [______]  D [______]      │
│ 14 • Chưa quyết (!)   │ Đáp án đúng *  (•)A ( )B ( )C ( )D                  │
│                       │ Giải thích chung [_______]  A[__] B[__] C[__] D[__] │
│                       │ Kỹ năng: Từ vựng · CEFR: B1 · Chủ đề: … · irt_b: …  │ ← chỉ đọc
│                       │ [Xem bản gốc]   (chỉ khi đã Lưu sửa)                 │
│                       │ [Câu trước] [Lưu sửa] [Từ chối] [ Duyệt ] [Câu sau] │
└───────────────────────┴─────────────────────────────────────────────────────┘
                                                    [ Gửi cho B ]  (cuối gói)
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Đầu trang: tên lô, "Đã quyết x / y", C-DUE | `review-progress` | |
| 2 | Danh sách câu (cột trái) | `review-list` | Mỗi dòng: số thứ tự, trạng thái chữ+biểu tượng (Chưa quyết • / Đã duyệt ✓ / Đã từ chối ✕), chấm "(!)" nếu có cờ mềm, dấu "đã sửa" nếu A đã Lưu sửa; câu đang mở đánh dấu ◄ |
| 3 | **Cờ mềm** (C-FLAG, 0..n) | `review-flags` | Hiện mã lý do (Phụ lục A) + liên kết "xem câu đó" cho nghi trùng. Cờ mềm là **gợi ý**, không chặn |
| 4 | **Nội dung** (textarea) | `review-content` | Sửa được khi câu `DRAFT` và gói `OPEN`; bắt buộc |
| 5 | **4 phương án** A–D (ô nhập) | `review-option-A`…`D` | Bắt buộc; 4 phương án khác nhau |
| 6 | **Đáp án đúng** (radio A–D) | `review-correct` | Đúng 1 đáp án |
| 7 | **Giải thích** chung + từng phương án A–D | `review-explanation` | Bắt buộc có giải thích |
| 8 | Thông tin chỉ đọc: Kỹ năng, CEFR, Chủ đề, `irt_b` | `review-meta` | A **không** sửa các trường này `🔶 P25-3` |
| 9 | Nút phụ "Xem bản gốc" | `review-view-original` | Mở C-DIFF (bản gốc | bản đã sửa) |
| 10 | Nút phụ **"Lưu sửa"** | `review-save` | Bật khi có thay đổi; không đổi gì: toast "Không có thay đổi nào để lưu." |
| 11 | Nút **"Từ chối"** (viền đỏ) | `review-reject` | → C-DIALOG "Từ chối câu này?" chỉ [Hủy] [Từ chối], **không ô lý do** → `REJECTED` |
| 12 | Nút chính **"Duyệt"** (xanh) | `review-approve` | **Khóa** khi: có thay đổi chưa Lưu sửa, hoặc lần Lưu sửa gần nhất trả `INVALID_AFTER_EDIT`/`DUPLICATE_AFTER_EDIT`. → `FIRST_APPROVED` |
| 13 | "Câu trước"/"Câu sau" | `review-prev`, `review-next` | Điều hướng trong gói (phím ←/→ `[D]`) |
| 14 | Nút "Gửi cho B" (cuối trang) | `send-package-{batchId}` | Cùng quy tắc và hộp thoại như S33 |
**(d)**
- **Lưu sửa** → `PATCH /items/:id` → server chạy lại **luật cứng + trùng T1–T2** trên bản sửa. OK: toast "Đã lưu bản sửa."; lỗi 422: dải đỏ nhạt dưới ô ("Bản sửa trùng một câu khác." / "Bản sửa không hợp lệ: <lý do theo Phụ lục A>"), **khóa Duyệt** cho tới khi sửa xong.
- **Duyệt/Từ chối** → API tương ứng → tự sang câu chưa quyết kế tiếp; hết câu → về S33 (hoặc hiện nút Gửi cho B nổi bật).
- Sau khi gói `SENT`: toàn bộ ô khóa, hiển thị "Gói đã gửi, chỉ đọc."
**(e)** Quá hạn: dải cam "Việc này đã quá hạn" **không khóa**; lỗi mạng: giữ nội dung đã nhập + "Thử lại"; rỗng: "Bạn chưa có câu nào cần duyệt."; không đúng người: 403.
**(f)** Mock: gói 20 câu, 12 đã quyết; câu 13 có 1 cờ mềm nghi trùng.
**(g)** AC: chỉ thấy câu của mình; sửa trùng/hỏng → nút Duyệt khóa; Từ chối không có ô lý do; sau gửi gói không sửa được.

---

### S34 — Hộp việc: Cần xác nhận (GV vai B)
**(a)** Route `/teacher/tasks/confirms` · Guard TEACHER · API `GET /me/confirm-packages` · UC UCGV15.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Khung tab Hộp việc | `tasks-tabs` | Như S33 |
| 2 | Danh sách **gói** (mỗi GV A đã gửi = một gói) | `inbox-confirm-list`, `package-row-{id}` | Cột: Lô · Ngày gửi · "Đã xử lý 7 / 15" (C-PROGRESS) · Hạn (C-DUE; **tính từ ngày gói được gửi** + `confirmDays`) · Trạng thái gói (C-BADGE "Đã gửi"/"Đã xong") |
| 3 | Bấm hàng | — | → `/teacher/tasks/confirms/[packageId]` |
**(e)** **Mỗi gói hiện nhãn "Gói do GV {Họ tên A} gửi ngày dd/mm"** (chốt P25-4; cũng hiện ở đầu màn S35). Chỉ hiện gói `SENT`/`DONE` gửi cho mình. Rỗng: "Bạn chưa có gói nào cần xác nhận."

---

### S35 — Màn gói (GV vai B)
**(a)** Route `/teacher/tasks/confirms/[packageId]` · Guard: **chỉ B của gói** (khác → 403) · API `POST /items/:id/confirm`, `POST /items/:id/remove`, `POST /item-packages/:id/confirm-all` · UC UCGV15.
**(b)**
```
Gói 2 – Lô "Từ vựng B1 – đợt 1"        Đã xử lý 7 / 15        Hạn: 28/10 23:59
                                                [ Xác nhận tất cả câu còn lại ]
┌─────────────────────────────────────────────────────────────────┐
│ She ____ to school…   [A đã sửa]  (!cờ)  Chưa quyết  [Xác nhận][Loại bỏ] │
│ …                                                                │
└─────────────────────────────────────────────────────────────────┘
Chi tiết câu đang chọn:  Bản gốc │ Bản A đã sửa      (khác biệt: gạch + chữ "đã đổi")
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Đầu gói: tên lô, "Đã xử lý x / y", C-DUE | `package-header` | |
| 2 | Nút phụ **"Xác nhận tất cả câu còn lại"** | `confirm-all` | Bật khi còn ≥ 1 câu chưa quyết; → C-DIALOG "Xác nhận tất cả {n} câu còn lại trong gói?" ([Hủy] [Xác nhận]), n = số câu chưa quyết; chỉ tác động câu chưa quyết; ghi log hàng loạt |
| 3 | Danh sách câu | `package-items` | Mỗi dòng: nội dung rút gọn; C-FLAG; dấu **"A đã sửa"** (`item-edited-flag-{id}`); trạng thái (Chưa quyết / Đã xác nhận vòng 2 / Đã loại); 2 nút |
| 4 | Nút **"Xác nhận"** | `confirm-item-{id}` | → `SECOND_APPROVED`; ẩn khi câu đã có quyết định |
| 5 | Nút **"Loại bỏ"** (viền đỏ) | `remove-item-{id}` | → C-DIALOG [Hủy] [Loại bỏ] **không ô lý do** → `REJECTED` |
| 6 | Khung chi tiết câu đang chọn | `diff-view` | Nội dung đầy đủ, **chỉ đọc**; nếu A đã sửa: C-DIFF bản gốc | bản sửa; giải thích |
| 7 | Dải hoàn tất | `package-done` | Khi mọi câu có quyết định: dải xanh "Gói đã hoàn tất." và cả màn chỉ đọc |
**KHÔNG có:** ô nhập sửa nội dung, nút "Trả về A", nút duyệt lại.
**(e)** Lỗi mạng khi xác nhận: giữ trạng thái, "Thử lại"; mất kết nối: khóa nút; tải: skeleton.
**(g)** AC: B không sửa được; "tất cả còn lại" chỉ ảnh hưởng câu chưa quyết; gói xong → chỉ đọc; GV khác → 403.

---

### S12 — Báo cáo lớp học (Teacher & Admin dùng chung)
**(a)** Route `/teacher/reports` · API `GET /reports/class-distribution?examRoundId=`, `GET /reports/error-patterns` · UC UCGV07, UCGV08, UCADM05.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Tiêu đề + **chip lọc "Kỳ thi"** (dropdown các kỳ; mặc định "Tất cả kỳ thi"; gửi `examRoundId`) | `filter-round` | BR-13 |
| 2 | Nút phụ **"Xuất CSV"** | `export-csv` | Mở hộp thoại chọn `export-type`: "Phân phối CEFR" hoặc "Hồ sơ từng sinh viên" `⚠️ ĐX` (UCGV08 chỉ nêu xuất dữ liệu của báo cáo đang xem; lựa chọn "Hồ sơ từng sinh viên" do file này đề xuất). Xuất đúng **bộ lọc kỳ thi đang áp dụng**; tên tệp có tên kỳ (nếu lọc) và ngày xuất; UTF-8; ô văn bản bắt đầu bằng `= + - @` được vô hiệu hóa (chống CSV injection, SRS 15.3); không có dữ liệu → tệp chỉ có dòng tiêu đề + toast "Không có dữ liệu để xuất"; STUDENT gọi API → 403 |
| 3 | Thẻ số "Sinh viên đã hoàn thành: 128" | `stat-completed` | |
| 4 | Thẻ **Phân phối CEFR**: cột 6 màu CEFR, trên mỗi cột số SV + % | `cefr-distribution` | Nút chuyển "Biểu đồ | Bảng" (bảng số liệu thay thế) |
| 5 | Thẻ **Chủ đề sai nhiều nhất của cả lớp** | `error-pattern-table` | Cột: chủ đề, kỹ năng, tỉ lệ sai, số SV |
| 6 | **Chỉ Admin:** thẻ "Thống kê câu hỏi theo trạng thái" (6 trạng thái, thanh ngang màu trạng thái, chuyển Biểu đồ|Bảng) | `item-status-chart` | UCADM05; `AI_REJECTED` chỉ Admin |
**(e)** Rỗng: "Chưa có sinh viên nào hoàn thành bài thi trong kỳ này." · Dữ liệu quá lớn: "Dữ liệu lớn, vui lòng thu hẹp phạm vi" `🔶 O7`. Teacher **chỉ xem**, không có thao tác ghi.

---

### S13 — Tra cứu sinh viên
**(a)** Route `/teacher/students` · UC UCGV09, UCADM04.
**(c)** Một thẻ căn giữa ≤ 560 px: nhãn "Mã số sinh viên", ô nhập (`student-code-input`, bắt buộc, khớp **chính xác**), nút chính "Tìm" (`student-search`). **Không vẽ danh sách đầy đủ** (chưa có endpoint, `🔶 O6`). Không thấy: "Không tìm thấy sinh viên." Tìm thấy → `/teacher/students/[studentId]`.

### S14 — Hồ sơ năng lực sinh viên
**(a)** Route `/teacher/students/[studentId]` (tham số = MSSV `🔶 R-6`) · API `GET /placement-profiles/:id`, `…/history`.
**(c)** Đầu trang: tên + MSSV. Tái dùng đúng các khối của **S05** (huy hiệu CEFR + độ tin cậy, θ/SE/KTC, 2 thanh kỹ năng, chủ đề cần cải thiện, gợi ý AI, banner vùng biên) + thẻ **"Lịch sử các lần thi"** (bảng: ngày, số câu, CEFR, θ, SE). Rỗng: "Sinh viên chưa có hồ sơ năng lực." · "Không tìm thấy sinh viên." Admin xem mọi SV; GV xem theo quyền của hệ thống (đơn trường).

---

### S08 — Ngân hàng câu hỏi (CHỈ XEM) — Teacher `/teacher/item-bank`, Admin `/admin/item-bank`
**(a)** API `GET /items` · UC UCGV02 (GV), UCADM06 (Admin). **Khác biệt theo role:**
| | Teacher | Admin |
|---|---|---|
| Phạm vi dữ liệu | Chỉ câu/gói **được giao cho mình**; có thể rỗng | Mọi câu |
| Nút trên đầu trang | **Không có** | "Tạo lô bằng AI" → S26 (`create-batch-ai`), "Import đề từ file" → S27 (`import-items`), liên kết "Lô cần xử lý (n) →" → S28 |
| Chip lọc trạng thái | 5 giá trị (không `AI_REJECTED`) | 5 giá trị (không `AI_REJECTED`; câu AI loại xem ở tab của lô, S29) |
| Chip "Lô" | Không | Có (`filter-batch`) |
**(b)**
```
Ngân hàng câu hỏi              [ Import đề từ file ]  [ Tạo lô bằng AI ]    ← chỉ Admin
Lô cần xử lý (3) →                                                           ← chỉ Admin
[🔍 Tìm trong nội dung…]  (Kỹ năng ▾)(CEFR ▾)(Trạng thái ▾)(Nguồn ▾)(Lô ▾)
┌─────────────────────────────────────────────────────────────────┐
│ Nội dung        Kỹ năng  CEFR  Chủ đề  Trạng thái        irt_b  │
│ She ____ to…    Ngữ pháp [A2]  past_s… (Đã vào ngân hàng) -0,4   │
└─────────────────────────────────────────────────────────────────┘
                              Hiển thị 1–20 / 280   ‹ 1 2 3 ›
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Ô tìm kiếm C-SEARCH | `search-input` | Tìm trong nội dung |
| 2 | Chip: Kỹ năng · CEFR · Trạng thái · Nguồn (**AI sinh / Import file**, lấy từ lô) · Lô | `filter-skill`, `filter-cefr`, `filter-status`, `filter-source`, `filter-batch` | Admin mặc định lọc "Đã vào ngân hàng"; Teacher mặc định "Tất cả" `[D]` |
| 3 | Bảng C-TABLE | `items-table` | Cột: Nội dung (cắt 1–2 dòng) · Kỹ năng · CEFR (huy hiệu) · Chủ đề · Trạng thái (C-BADGE) · Nguồn · Lô · `irt_b` · Cập nhật lần cuối. Bấm hàng → S10 |
**KHÔNG có:** nút Thêm câu hỏi, Xóa, Sửa, Nhân bản. **(e)** Rỗng: "Không tìm thấy câu hỏi phù hợp." · đang lọc: bảng cũ mờ.

### S10 — Chi tiết câu hỏi (CHỈ ĐỌC) — Teacher `/teacher/item-bank/[id]`, Admin `/admin/item-bank/[id]`
**(a)** API `GET /items/:id` · UC UCGV02 (GV), UCADM06 (Admin); UCGV04 là bước sửa câu nằm trong UCGV14 (S11), UCGV06 ngoài phạm vi.
**(c)** Một thẻ ≤ 720 px:
| # | Khối | testid | Nội dung / quy tắc |
|---|---|---|---|
| 1 | Thông tin câu | `item-detail` | Nội dung; 4 phương án (đáp án đúng đánh dấu biểu tượng + chữ "Đáp án đúng"); Kỹ năng, CEFR, Chủ đề, `irt_b`; giải thích chung + từng phương án; C-BADGE trạng thái (6 giá trị); Nguồn; Lô |
| 2 | Dải chỉ đọc | `readonly-banner` | `FINAL_APPROVED`: dải xanh nhạt "Câu hỏi đã vào ngân hàng nên không thể chỉnh sửa." + `approved_by`, `approved_at`. Ở mọi trạng thái **không** có Lưu/Sửa/Xóa/Nhân bản/Duyệt/Từ chối |
| 3 | **Kết quả AI kiểm** (**chỉ Admin**) | `check-results` | C1/C2/C3: mỗi lần Qua/Cờ mềm/Lỗi cứng + mã lý do + liên kết tới câu nghi trùng |
| 4 | **Lịch sử** (**chỉ Admin**) | `item-history` | `ReviewAction` ai/lúc nào (Duyệt, Từ chối, Xác nhận, Loại bỏ, Chấp nhận cờ, Import…) |
| 5 | Bản gốc so bản sửa | `diff-original-edited` | Chỉ khi A đã sửa (C-DIFF) |
**(e)** GV mở câu không được giao → 403.

---

## 7. ĐẶC TẢ MÀN HÌNH — QUẢN TRỊ VIÊN (ADMIN)

> Layout mọi màn: **L-SIDEBAR** (menu ADMIN, Mục 2.4). Guard: chỉ `ADMIN`; TEACHER/STUDENT → 403. Admin **không sửa nội dung câu**, **không gõ câu bằng form**. S08/S10/S12–S14 xem ở Mục 6.

### S36 — Tổng quan hệ thống `🔶 R-5` (màn từ Tuan4, chưa xác nhận giữ)
**(a)** Route `/admin/dashboard` · API `GET /reports/…` · UC UCADM05.
**(b)**
```
Tổng quan
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ 1.240  │ │  235   │ │   3    │ │   4    │   ← 4 số lớn, nhãn xám nhỏ
│ SV đã  │ │ Câu vào│ │ Lô cần │ │ Kỳ thi │
│ thi    │ │ ngân   │ │ xử lý →│ │ đang mở│
└────────┘ └────────┘ └────────┘ └────────┘
Phân phối CEFR toàn hệ thống        Câu hỏi theo trạng thái
[ biểu đồ cột 6 màu CEFR ]          [ 6 thanh ngang màu trạng thái ]
```
**(c)** `stat-students`, `stat-final-approved`, `stat-batches-open` (bấm → S28), `stat-open-rounds` (bấm → S20), `cefr-distribution`, `item-status-chart` (mỗi biểu đồ có chuyển "Biểu đồ | Bảng"). Rỗng: "Chưa có sinh viên nào hoàn thành bài thi." Số liệu là mock.

---

### S28 — Danh sách lô câu hỏi
**(a)** Route `/admin/item-batches` · API `GET /item-batches` · UC UCADM13.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Tiêu đề "Lô câu hỏi" + nút chính **"Tạo lô bằng AI"** (→ S26) + nút phụ **"Import đề từ file"** (→ S27) | `create-batch-ai`, `import-items` | |
| 2 | Chip lọc trạng thái lô | `filter-batch-status` | 10 giá trị (Mục 2.2) |
| 3 | Bảng | `batches-table` | Cột: Tên/ngày tạo (`ItemBatch.name` nếu có) · Nguồn (AI sinh / Import file) · Kỹ năng + CEFR · Số câu yêu cầu · **Trạng thái lô** (C-BADGE chữ) · Tiến độ (x/y) · Hạn gần nhất (C-DUE, "Quá hạn" nếu có). Bấm hàng → S29 |
**(e)** Rỗng: "Chưa có lô câu hỏi nào." · Lô seed (`IMPORTED`/`DONE`) hiển thị bình thường, lọc được.

### S26 — Tạo lô bằng AI
**(a)** Route `/admin/item-batches/generate` · API `POST /item-batches` · UC UCADM11.
**(c)** Thẻ ≤ 560 px, một cột:
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | **Kỹ năng \*** (select: Từ vựng / Ngữ pháp) | `batch-skill` | Bắt buộc |
| 2 | **Cấp CEFR \*** (select: A1, A2, B1, B2 `[D]`) | `batch-cefr` | Bắt buộc |
| 3 | **Chủ đề** (tùy chọn) | `batch-topic` | Văn bản ngắn |
| 4 | **Số câu cần \*** (số nguyên dương) | `batch-count` | Bắt buộc; > 0 |
| 5 | Dòng phụ | — | "AI sẽ sinh dư và lọc trùng; số câu cuối có thể thấp hơn nếu hết ngân sách." |
| 6 | Nút chính **"Tạo lô"**, nút chữ "Hủy" | `batch-create` | Vô hiệu khi thiếu trường. **Không chọn GV ở bước này.** |
**(d)** OK → tạo lô `GENERATING` → chuyển S29 (hiện tiến độ). Lỗi: `BATCH_BUDGET_EXCEEDED` → "Lô vượt giới hạn gọi AI cho phép."; thiếu trường; mạng.

### S27 — Import đề từ file (lưới tạm)
**(a)** Route `/admin/item-batches/import` · API `POST /item-imports/upload`, `GET|DELETE /item-imports/grid[/:rowKey]`, `POST /item-imports/save` · UC UCADM12. **GV không có màn này (403).**
**(b)** Dùng **C-IMPORT-GRID** (Mục 2.7). Cột lưới: `Skill · CEFR · Topic · Câu hỏi · A · B · C · D · Đáp án · Giải thích · irt_b` (Giải thích, irt_b tùy chọn; `irt_b` ∈ [−4, +4]).
**(c)** Khác biệt so với cơ chế chung:
| # | Điểm | Quy tắc |
|---|---|---|
| 1 | Popup dòng bị loại (`itemimport-rejected-popup`) | Lý do: thiếu cột bắt buộc; kiểu dữ liệu sai; Skill/CEFR không hợp lệ; `irt_b` ngoài [−4, +4]; trùng ngân hàng / lô khác / trong lưới (T1–T2 cứng) |
| 2 | **Cờ mềm** trên dòng lưới | Trùng gần đúng (T2 giữa hai ngưỡng, T3) **không bị loại**: dòng mang chip C-FLAG; vẫn Lưu được |
| 3 | Nút chính | **"Lưu {N} câu và kiểm tra bằng AI"** (`itemimport-save`) → tạo lô `IMPORTED`, chạy C2 tầng 5 → chuyển S29 |
| 4 | Testid | `itemimport-dropzone`, `itemimport-grid`, `itemimport-rejected-popup`, `itemimport-clear`, `itemimport-save`, `itemimport-template` |
**(e)** Lỗi: `IMPORT_FILE_INVALID`, `IMPORT_GRID_EXPIRED`, `IMPORT_GRID_EMPTY`.

---

### S29 — Chi tiết lô: tiến độ, câu, AI đã loại (+ S31 Chỉnh hạn)
**(a)** Route `/admin/item-batches/[batchId]` · API `GET /item-batches/:id`, `GET …/ai-rejected`, `PATCH …/deadlines`, `POST /item-packages/:id/force-send` · UC UCADM13.
**(b)**
```
Lô "Từ vựng B1 – đợt 1"  [Đang duyệt]                [Giao việc] [Chỉnh hạn] [Giao lại] [Kiểm tra]
Tạo ─ AI kiểm ─ Giao việc ─ A duyệt ─ B xác nhận ─ Kiểm tra ─ Import        ← C-STEPPER
[Chờ duyệt 40][Đã duyệt vòng1 30][Đã xác nhận 20][Đã vào NH 0][Đã loại 6][AI đã loại 4][Chưa xử lý 3]
 Tab:  Câu hỏi | Theo GV và gói | AI đã loại | Thống kê
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Đầu trang: tên lô, C-BADGE trạng thái lô | `batch-status` | |
| 2 | C-STEPPER 7 bước | `batch-progress` | Khi `GENERATING`/`IMPORTING`/`CHECKING`: hiện tiến độ, **tự làm mới** (polling 5 giây `[D]`) |
| 3 | Hàng thẻ đếm theo trạng thái câu | `batch-counts` | Chờ duyệt vòng 1 · Đã duyệt vòng 1 · Đã xác nhận vòng 2 · Đã vào ngân hàng · Đã loại (GV/Admin) · AI đã loại · Chưa xử lý |
| 4 | **Nút theo trạng thái lô** | `go-assign`, `go-finalize`, … | `READY_TO_ASSIGN` → **"Giao việc"** (→ S30); `IN_REVIEW` → "Chỉnh hạn" (mở S31), "Giao lại" (→ S30 tab Giao lại), "Ép gửi gói" (trên từng gói chưa gửi); `READY_TO_FINALIZE`/`FINAL_CHECKED` → **"Kiểm tra"** (→ S32). Nút không phù hợp trạng thái thì **ẩn** |
| 5 | Tab **Câu hỏi** | `tab-items` | Bảng câu của lô, cờ mềm; bấm hàng → S10 |
| 6 | Tab **Theo GV và gói** | `tab-assignees` | Theo GV A: số câu giao / đã quyết / hạn / "Quá hạn"; theo gói: A → B, trạng thái gói (Chưa gửi / Đã gửi / Đã xong), hạn của B; nút **"Ép gửi gói"** (`force-send-{packageId}`) chỉ ở gói `OPEN` → hộp xác nhận "Gửi gói thay cho {GV A}? Giảng viên sẽ không thể sửa các câu trong gói." `🔶` đề xuất |
| 7 | Tab **AI đã loại** (**chỉ Admin**) | `tab-ai-rejected` | Nội dung + mã lý do (Phụ lục A) + câu bị nghi trùng; rỗng: "Chưa có câu nào bị AI loại." |
| 8 | Tab **Thống kê** | `tab-stats` | Tỉ lệ loại theo tầng AI, theo từng GV A, theo GV B |
| 9 | **S31 Chỉnh hạn** (ngăn bên phải) | `deadline-review-days`, `deadline-confirm-days`, `deadline-save` | 2 ô số ≥ 1: `reviewDays`, `confirmDays`; chỉ áp dụng việc **chưa xử lý**; hiện trước hạn mới "dd/mm 23:59"; nút chính "Lưu hạn" → `PATCH …/deadlines` (đặt lại lịch nhắc 24 giờ trước hạn) → toast "Đã cập nhật hạn." |
**(e)** Lô `FAILED`: dải đỏ + lý do; lô `PARTIAL`: dải vàng "Thiếu {x} câu so với yêu cầu"; 404 lô không tồn tại.

### S30 — Giao việc (xem trước phân bổ) và Giao lại
**(a)** Route `/admin/item-batches/[batchId]/assign` · API `GET …/assign-preview`, `POST …/assign {reviewerIds,confirmerId,reviewDays,confirmDays}`, `POST …/reassign` · UC UCADM13 · Giao việc chỉ khi lô `READY_TO_ASSIGN`.
**(b)** Hai tab: **Giao việc** | **Giao lại**.
**(c)** Tab Giao việc (ba khối xếp dọc):
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | **Nhóm GV duyệt (A)** — danh sách chọn nhiều | `assign-reviewers` | Tối thiểu 1; gợi ý từ 2 người để chia việc. Chỉ liệt kê GV đang hoạt động |
| 2 | **GV xác nhận (B)** — chọn đúng một | `assign-confirmer` | **Bắt buộc**; GV đã chọn vào nhóm A bị **vô hiệu hóa** trong danh sách B và ngược lại; vi phạm → `CONFIRMER_IN_REVIEW_GROUP` "GV xác nhận không được nằm trong nhóm GV duyệt." Admin có được chọn làm A/B không: `🔶 P25-1` (mặc định: **không** liệt kê Admin) |
| 3 | **Số ngày để A duyệt** (`reviewDays` ≥ 1) | `assign-review-days` | Số nguyên |
| 4 | **Số ngày để B xác nhận sau khi nhận gói** (`confirmDays` ≥ 1) | `assign-confirm-days` | Số nguyên |
| 5 | Nút phụ **"Xem trước phân bổ"** | `assign-preview` | Bảng GV A – số câu theo kỹ năng/CEFR (chia đều, chênh ≤ 1 câu); hạn của A "dd/mm 23:59"; hạn của B "tính từ ngày A gửi gói" |
| 6 | Nút chính **"Xác nhận giao"** | `assign-submit` | Bật khi A ≥ 1, B đã chọn, hai số ≥ 1 và đã xem trước; → lô `IN_REVIEW`, toast "Đã giao việc" → S29 |
Tab **Giao lại**: chọn GV A còn câu chưa xử lý → chọn GV nhận (hoặc đổi B của gói chưa gửi/chưa xử lý, vẫn B ∉ nhóm A) → nút `reassign-submit`; hạn tính lại từ ngày giao lại; ghi kiểm toán `REASSIGN`.
**(e)** Rỗng: "Chưa có giảng viên nào để giao việc." · Đang tải danh sách GV / đang tạo phân bổ · lô không ở `READY_TO_ASSIGN` → dải "Lô này không ở trạng thái chờ giao việc." (chỉ còn tab Giao lại nếu `IN_REVIEW`).

### S32 — Kiểm tra (C3) và Import cuối
**(a)** Route `/admin/item-batches/[batchId]/final-check` · API `POST|GET …/final-check`, `POST /items/:id/decision`, `POST …/import` · UC UCADM14 · chỉ khi lô `READY_TO_FINALIZE` (hoặc đã `FINAL_CHECKED` để xem/kiểm lại); khác → `BATCH_NOT_READY_TO_FINALIZE`.
**(b)**
```
Kiểm tra cuối — Lô "Từ vựng B1 – đợt 1"
Đã xác nhận vòng 2: 20 · Đã loại bởi A/B: 6 · AI đã loại: 4 · Chưa xử lý/quá hạn: 3
[ Kiểm tra ]                                          (dải cảnh báo nếu báo cáo cũ)
Báo cáo theo câu:  Qua 17 · Cờ mềm 2 · Lỗi cứng 1
 Câu …  [Cờ mềm] NEAR_DUPLICATE_BANK  [xem câu nghi trùng]  [bản gốc|bản sửa]  [Chấp nhận (cho Import)] [Loại]
Câu chưa quyết định (không được import): 3
                                                     [   Import   ]
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Thống kê đầu trang | `finalize-stats` | Đã xác nhận vòng 2 · Đã loại bởi A/B · AI đã loại · Chưa xử lý/quá hạn |
| 2 | Nút **"Kiểm tra"** (spinner khi chạy) | `finalize-check` | → `POST …/final-check` (C3 chạy theo thay đổi) |
| 3 | **Báo cáo theo câu** | `finalize-report` | Mỗi câu: Qua / Cờ mềm / Lỗi cứng + mã lý do + câu nghi trùng + C-DIFF nếu A sửa; tổng hợp theo gói; số câu A sửa; tỉ lệ A/B loại. **Lỗi cứng ⇒ câu đã chuyển "AI đã loại"** (hiển thị, không có nút) |
| 4 | Với mỗi **cờ mềm** hai nút | `soft-accept-{itemId}`, `soft-reject-{itemId}` | "Chấp nhận (cho Import)" (ghi `ACCEPT_FLAG`) / "Loại" (`REJECTED`) → `POST /items/:id/decision` |
| 5 | Dải cảnh báo báo cáo cũ | `finalize-stale` | "Dữ liệu đã thay đổi kể từ lần kiểm tra cuối. Vui lòng kiểm tra lại." (`FINAL_CHECK_STALE`); khi đó Import bị khóa |
| 6 | Dòng thông tin **"Câu chưa quyết định"** | `finalize-unprocessed` | Chỉ hiển thị số lượng và danh sách câu **không được import**; **không có nút xử lý riêng** (#121: đến hạn mọi GV phải hoàn thành; dự phòng dùng S29) |
| 7 | Nút chính **"Import"** | `finalize-import` | **Tắt** tới khi có báo cáo C3 hợp lệ (còn hiệu lực) và mọi cờ mềm đã được quyết; `title` giải thích khi tắt (`FINAL_CHECK_REQUIRED`) |
**(d)** Import thành công: "Đã import {N} câu vào ngân hàng." (các câu → `FINAL_APPROVED`) → về S29. Hai Admin Import cùng lúc: người sau nhận lỗi tranh chấp (server chạy lại T1–T2) → "Một số câu vừa bị trùng với câu mới vào ngân hàng, vui lòng kiểm tra lại."
**(e)** Chưa có báo cáo: "Chưa có báo cáo kiểm tra. Bấm Kiểm tra để bắt đầu."

---

### S20 — Danh sách kỳ thi
**(a)** Route `/admin/exam-rounds` · API `GET /exam-rounds` · UC UCADM15.
**(c)** Tiêu đề "Kỳ thi" + nút chính **"Tạo kỳ thi"** (`create-round`, → S21); chip lọc trạng thái (Tất cả · Nháp · Đã lên lịch · Đang mở · Đã đóng; `filter-round-status`); bảng `rounds-table`: Tên kỳ · Giờ mở · Giờ đóng · Thời lượng (phút) · Trạng thái hiệu lực (C-BADGE) · Số SV; bấm hàng → S22. Rỗng: "Chưa có kỳ thi nào." + nút "Tạo kỳ thi". Trạng thái hiển thị = `effectiveStatus`.

### S21 — Tạo / sửa kỳ thi
**(a)** Route `/admin/exam-rounds/new`, `/admin/exam-rounds/[roundId]/edit` · API `POST /exam-rounds`, `PATCH /exam-rounds/:id` · UC UCADM15.
**(c)** Thẻ ≤ 560 px, một cột:
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | **Tên kỳ thi \*** | `round-name` | Bắt buộc |
| 2 | **Giờ mở \*** (date-time) | `round-opens` | Bắt buộc |
| 3 | **Giờ đóng \*** (date-time) | `round-closes` | Bắt buộc; phải **> Giờ mở** ("Giờ đóng phải sau giờ mở.") |
| 4 | **Thời lượng làm bài (phút) \*** | `round-duration` | **Bắt buộc, điền sẵn 45**; số nguyên 5–180; không lớn hơn khoảng từ giờ mở đến giờ đóng; lỗi: "Thời lượng phải từ 5 đến 180 phút và không vượt khoảng mở–đóng." |
| 5 | Dòng phụ | — | "Sinh viên vào muộn chỉ còn phần thời gian còn lại tới giờ đóng." |
| 6 | Nút chính **"Lưu"** (kỳ `DRAFT`), nút chữ "Hủy" | `save-round` | Vô hiệu khi thiếu/không hợp lệ |
**(d)** OK → toast, về S22. **Quy tắc sửa theo trạng thái (BR-08, `🔶` đề xuất):** `DRAFT` sửa tự do · `SCHEDULED` chỉ sửa tên và kéo dài giờ đóng (các ô khác khóa kèm chú thích) · `CLOSED` chỉ xem (không vào được `/edit` → chuyển S22).

### S22 — Chi tiết kỳ thi / Theo dõi dự thi
**(a)** Route `/admin/exam-rounds/[roundId]` · API `GET /exam-rounds/:id`, `…/participants`, `POST …/publish|close`, `DELETE …/participants/:studentId`, `GET …/participants/export?format=csv|xlsx&status=&q=&studentIds=` `⚠️ ĐX` · UC UCADM15, UCADM17.
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Đầu trang: tên, trạng thái, giờ mở/đóng, thời lượng | — | |
| 2 | Nút **"Công bố"** (chính) | `publish-round` | Hiện khi `DRAFT`; **bật khi có ≥ 1 SV** (`title`: "Cần ít nhất 1 sinh viên"); → `DRAFT → SCHEDULED` |
| 3 | Nút **"Đóng kỳ"** | `close-round` | Hiện khi `SCHEDULED`/`OPEN`; hộp xác nhận ghi rõ: "Phiên đang làm bài vẫn tiếp tục tới hết thời gian của phiên; chỉ chặn sinh viên bắt đầu phiên mới." `🔶 Q-2` |
| 4 | Nút phụ "Import danh sách" (→ S23), "Sửa" (→ S21) | `import-roster` | "Import" ẩn khi `CLOSED` |
| 5 | Bảng SV | `participants-table` | Cột: ô tick · MSSV · Họ tên · Ghi chú · Trạng thái dự thi (Chưa thi / Đang thi / Hoàn thành / Bỏ dở) · nút chữ **"Gỡ"** (`remove-participant-{id}`; **chỉ bật ở dòng "Chưa thi"** và khi kỳ chưa đóng; dòng Đang thi/Hoàn thành/Bỏ dở ẩn nút hoặc vô hiệu kèm `title` giải thích — khóa ngoại phiên thi chặn xóa) |
| 6 | Bộ lọc trạng thái và ô tìm MSSV/Họ tên | `participants-filter`, `participants-search` | Lọc bảng; "chọn tất cả theo bộ lọc" ở ô tick đầu cột |
| 7 | Nút **"Xuất CSV"** và **"Xuất Excel"** (`#120`, `⚠️ ĐX` UC/API) | `export-csv`, `export-xlsx` | Có dòng được tick: chỉ xuất các dòng đó (một hoặc nhiều SV); không tick: xuất toàn bộ danh sách đang lọc. Tải file ngay (đồng bộ). Cột: MSSV · Họ tên · Trạng thái · Mức CEFR · θ · SE · Thời điểm bắt đầu · Thời điểm nộp. Chống CSV injection (ô bắt đầu bằng `= + - @`). Không có dòng khớp: toast "Không có dữ liệu để xuất" |
**(e)** Rỗng: "Chưa có sinh viên trong kỳ." · thao tác sai trạng thái: lỗi 409 hiển thị toast.

### S23 — Import danh sách thi (lưới tạm)
**(a)** Route `/admin/exam-rounds/[roundId]/import` · API `…/participants/import/{upload,grid,save}` · UC UCADM16.
**(b/c)** Dùng **C-IMPORT-GRID**. Tiêu đề "Import danh sách sinh viên cho \"{tên kỳ}\"". Cột lưới: **MSSV · Ghi chú** (A = MSSV, B = Ghi chú tùy chọn ≤ 255 ký tự). Popup dòng bị loại (`roster-rejected-popup`): thiếu cột · sai định dạng · trùng trong file · **"MSSV không tồn tại"** (hoặc không phải sinh viên) · **"Đã có trong kỳ"**. Nút chính **"Lưu {N} sinh viên vào kỳ"** (`roster-save`) → một transaction → về S22. Testid: `roster-dropzone`, `roster-grid`, `roster-clear`.

---

### S24 — Quản lý tài khoản (Sinh viên | Giảng viên)
**(a)** Route `/admin/users/students` và `/admin/users/teachers` (hai tab = hai route, dùng chung một component) · API `GET|POST|PATCH /students`, `/teachers`; `POST /students/:id/lock|unlock|resend-temporary-password`; `PATCH /users/:id/role` · UC UCADM09.
**(b)**
```
Tài khoản     [ Sinh viên ]  [ Giảng viên ]            [ Thêm sinh viên ]  [ Import ]
[🔍 Tìm theo MSSV hoặc email]
┌──────────────────────────────────────────────────────────────────────────────┐
│ Họ tên  MSSV  Email  Trạng thái  Đã đổi MK   Hành động     │
└──────────────────────────────────────────────────────────────────────────────┘
```
**(c)**
| # | Thành phần | testid | Quy tắc |
|---|---|---|---|
| 1 | Hai tab | `accounts-tab-students`, `accounts-tab-teachers` | |
| 2 | Ô tìm theo MSSV/email (SV) hoặc Mã GV/email (GV) | `account-search` | |
| 3 | Nút **"Thêm sinh viên"** (tab SV) / **"Thêm giảng viên"** (tab GV) | `add-student` / `add-teacher` | Mở **form tạo từng người** (dưới) |
| 4 | Nút phụ **"Import"** | `import-accounts` | → `/admin/users/import?kind=STUDENT|TEACHER` (chọn sẵn loại theo tab) |
| 5 | Bảng (C-TABLE, phân trang) | `accounts-table` | Cột: Họ tên · MSSV (SV) / Mã GV (GV) · Email · **Trạng thái** (Hoạt động / Đã khóa) · **Đã đổi mật khẩu** (Rồi / Chưa) · *(không có cột trạng thái email: #120 — schema chưa lưu trạng thái gửi; chỉ có nút "Gửi lại mật khẩu tạm" từng tài khoản)* |
| 6 | Hành động cuối hàng (nút chữ) | — | "Sửa" (họ tên, email; modal); `lock-{id}` "Khóa"/"Mở khóa" (`is_active`); `resend-temp-{id}` "Gửi lại mật khẩu tạm" (sinh mật khẩu mới, buộc đổi lại; xác nhận); **tab GV:** `grant-admin-{id}` "Nâng lên Admin" / "Thu hồi Admin" (xác nhận) |
**Form tạo từng người** (`account-form`, modal ≤ 480 px): SV: **MSSV \*, Họ tên \*, Email \***; GV: **Mã GV \*, Họ tên \*, Email \***. Nút chính "Lưu", chữ "Hủy". Trùng email/MSSV/Mã GV → lỗi ngay dưới ô trùng ("Email đã tồn tại.", "MSSV đã tồn tại.", "Mã GV đã tồn tại."). Lưu OK: sinh mật khẩu tạm 12 ký tự, xếp hàng email (**không hiển thị mật khẩu**), toast "Đã tạo tài khoản. Mật khẩu tạm đã được gửi qua email.", làm mới danh sách.
**Quy tắc (BR-17/18/19):** Admin không tự thu hồi quyền của mình (nút ẩn/tắt ở hàng của mình, `title` giải thích); không thu hồi Admin cuối cùng (lỗi: "Không thể thu hồi quyền của quản trị viên cuối cùng."); tài khoản bị khóa không đăng nhập được; **không có nút Xóa** (chỉ khóa). Đổi role → token cũ mất quyền cũ.
**(e)** Rỗng: "Chưa có sinh viên." / "Chưa có giảng viên." · 403 nếu TEACHER mở · lỗi tải.

### S19 — Import tài khoản (SV, GV) — lưới tạm
**(a)** Route `/admin/users/import` (`?kind=STUDENT|TEACHER`) · API `POST /users/import/upload?kind=`, `GET /users/import/grid?kind=`, `DELETE /users/import/grid[/:rowKey]?kind=`, `DELETE /users/import/grid`, `POST /users/import/save?kind=` · UC UCADM08.
**(b/c)** Dùng **C-IMPORT-GRID**; khác biệt:
| # | Điểm | Quy tắc |
|---|---|---|
| 1 | Ô chọn **"Loại tài khoản"** (Sinh viên | Giảng viên) | `import-kind`; **mỗi loại một lưới riêng** (khóa theo adminId + kind); đổi loại không mất lưới loại kia |
| 2 | Cột lưới | SV: **MSSV · Họ tên · Email**; GV: **Mã GV · Họ tên · Email** |
| 3 | Popup dòng bị loại | `import-rejected-popup`: thiếu cột/trống · email sai định dạng · trùng trong file |
| 4 | **Popup riêng "Tài khoản đã tồn tại"** | `import-existing-popup`: email, MSSV hoặc Mã GV đã có trong hệ thống. Dòng này **không vào lưới** nên không chặn Lưu. **Chỉ tạo mới; không cập nhật tài khoản có sẵn** |
| 5 | Hai liên kết tải mẫu | `import-template-student`, `import-template-teacher` (file giả) |
| 6 | Nút chính **"Lưu"** | `import-save`: tạo tài khoản (theo loại), sinh mật khẩu tạm, **chỉ sau Lưu mới xếp hàng email**; kết quả: "Đã tạo {N} tài khoản, {N} email đã xếp hàng." |
**(e)** Email gửi thất bại sau retry → **không rollback tài khoản**; UI **không** hiển thị trạng thái gửi (#120) `🔶 BR-05` (Mục 9), SMTP chưa chọn (Q-5); sau Lưu chỉ hiện "Đã tạo {n} tài khoản, {m} email đã xếp hàng gửi"; lưới rỗng → `IMPORT_GRID_EMPTY`; hết TTL → `IMPORT_GRID_EXPIRED`.

---

## 8. THỨ TỰ SINH ĐỀ XUẤT (MỖI LƯỢT 2–4 MÀN)

| Lượt | Nội dung | Điều kiện hoàn thành |
|---|---|---|
| 0 | **Khối nền:** token (Mục 2.1), 5 layout (Mục 2.4), bộ C-* (Mục 2.5), từ điển nhãn/mã lỗi (Mục 2.2–2.3), route guard (Mục 3.6), API client + dữ liệu mock | Trang mẫu hiển thị đủ huy hiệu CEFR/trạng thái/dialog/skeleton ở 360 và 1280 px |
| 1 | S01, S16, S17, S18 | AC Mục 5; luồng quên mật khẩu chạy trọn với mock |
| 2 | S02, S03, S04 | Bắt đầu → làm bài → hết giờ đúng luật (mock) |
| 3 | S05, S06, S07, S15 | Không cuộn ngang 360 px |
| 4 | S12, S13, S14, S08, S10 | Bản Teacher và Admin của S08/S10 khác đúng bảng Mục 6 |
| 5 | S20, S21, S22, S23 | Máy trạng thái kỳ thi; lưới tạm dùng C-IMPORT-GRID |
| 6 | S24, S19 | Form tạo lẻ + import dùng lại C-IMPORT-GRID |
| 7 | S26, S27, S28, S29 (+S31) | Nút theo trạng thái lô hiện/ẩn đúng |
| 8 | S30, S32, S36 | Chặn B ∈ nhóm A; Import khóa/mở đúng |
| 9 | S33, S11, S34, S35 | Gửi gói chỉ bật khi đủ quyết định; B chỉ đọc |

Sau mỗi lượt: đối chiếu AC (g) từng màn, đối chiếu "KHÔNG hiển thị/KHÔNG có" trong Mục 0.1, ghi `0.docs/tracking/AI_USAGE_LOG.md` (công cụ, prompt, phần sửa tay) — bắt buộc cho TC2.3.

---

## 9. ĐIỂM CHƯA CHỐT — AGENT KHÔNG TỰ QUYẾT, DÙNG MẶC ĐỊNH VÀ GẮN `TODO-CONFIRM`

| Mã | Nội dung | Mặc định tạm dùng trong file này | Ảnh hưởng |
|---|---|---|---|
| Q-2 | Đóng kỳ thủ công khi còn phiên đang chạy: cắt ngay hay để chạy tới `expiresAt` (BR-12) | **Để chạy**, chỉ chặn phiên mới | S22 |
| Q-4 | Chính sách mật khẩu (độ dài tối thiểu) | ≥ 8, đọc từ cấu hình | S16, S18 |
| Q-5 | Nhà cung cấp SMTP | Không hiển thị gì phụ thuộc nhà cung cấp | S19, S24 |
| 🔶 BR-05 | BR-05 (SRS) yêu cầu ghi trạng thái "chưa gửi" **để Admin xem được**; nhưng #120 chọn không đổi schema và không có màn nhật ký kiểm toán → **chưa có nơi hiển thị**. Cần chốt: (1) thêm cột trạng thái trên `User` hoặc bảng nhật ký gửi email + hiển thị ở S24, hay (2) chấp nhận Admin không thấy lỗi gửi | **Mặc định: UI không hiển thị**; chỉ có "Gửi lại mật khẩu tạm" từng tài khoản | S19, S24 |
| BR-08 | Quy tắc sửa kỳ thi theo trạng thái | `DRAFT` tự do; `SCHEDULED` chỉ tên + kéo dài giờ đóng; `CLOSED` không sửa | S21 |
| BR-18 | Không thu hồi Admin cuối | Có chặn | S24 |
| ✅ P25-1 | Admin có được chọn làm GV A/B? Admin có Hộp việc? | **Đã chốt 18/10: Không** (S30 chỉ liệt kê `role = TEACHER`; menu Admin không có Hộp việc) | S30, menu |
| P25-2 | Admin có xóa được câu `REJECTED`/lô? | **Không có nút Xóa** | S08, S29 |
| P25-3 | GV A có sửa được kỹ năng/CEFR/chủ đề/`irt_b`? | **Không** (chỉ nội dung, đáp án, giải thích) | S11 |
| ✅ P25-4 | GV B có thấy tên GV A trên gói? | **Đã chốt: Có** (UCGV15 bước 2): nhãn "Gói do GV {Họ tên A} gửi ngày dd/mm" ở danh sách gói (S34) và đầu màn gói (S35) | S34, S35 |
| O4 | "Hủy bài cũ và bắt đầu lại" (SV) chưa có endpoint | Nút vẽ nhưng vô hiệu | S03 |
| O6 | Danh sách đầy đủ SV cho GV | Không vẽ, chỉ tra MSSV | S13 |
| O7 | Báo cáo dữ liệu quá lớn | Hiện thông điệp "thu hẹp phạm vi" | S12 |
| K6 | Cờ `REVIEW_ENABLED` xem lại đáp án | Hỗ trợ cả hai nhánh bật/tắt | S06 |
| Q-7…Q-10 | Ngưỡng/tham số AI, bản quyền, mô hình embedding, `pg_trgm` | **UI không hiển thị con số ngưỡng nào** | S26, S27, S29, S32 |
| — | "Ép gửi gói" (Admin gửi thay A): **giữ làm dự phòng** theo #121 (người dùng chưa xác nhận có bỏ hẳn hay không) | Như Mục 4.5-D/F | S29 |
| R-1 | Cấu trúc đích có `/teacher/dashboard` nhưng **chưa có nội dung đặc tả** | Không sinh; GV vào `/teacher/tasks/reviews` (nếu có việc) hoặc `/teacher/reports` | Mục 3.1 |
| R-2 | Admin xem báo cáo/hồ sơ SV ở đâu: cấu trúc đích chỉ ghi `/teacher/reports` và `/admin/dashboard` | Admin dùng chung `/teacher/reports`, `/teacher/students[/…]` (guard cho phép ADMIN; sidebar dựng theo role) | S12–S14 |
| ✅ R-3 | Menu GV 4 mục, có "Ngân hàng câu hỏi" → `/teacher/item-bank` | **Đã chốt 16/10 (#116)**; S08 với Teacher không có nút tạo lô/import | Mục 2.4, S08 |
| R-4 | "Đổi mật khẩu" tự nguyện có mục trong menu avatar? | Có (SV) / đáy sidebar (GV, Admin) `⚠️ ĐX` | S16 |
| R-5 | Giữ hay bỏ màn Tổng quan Admin (S36, cũ E2) | Giữ làm trang chủ Admin | S36 |
| R-6 | Tham số `[studentId]` của S14 là MSSV hay UUID user (API hiện tra theo MSSV) | MSSV | S13, S14 |
| R-7 | S03 là route riêng `/student/exams/[roundId]` (cấu trúc đích chỉ có `take`) | Có route riêng | S02, S03, S04 |
| P18-1 | Giới hạn số dòng tối đa khi xuất kết quả kỳ thi (S22) | Chưa đặt; không hiển thị con số | S22 |
| P18-3 | S04 route theo `roundId` nhưng API/UCSV07 theo `sessionId` | FE tra phiên đang mở của kỳ (`GET /sessions/active`) rồi `GET /sessions/:id/resume` | S02, S04 |

**Nợ đồng bộ tài liệu liên quan file này (ghi nhận, chưa sửa):** (1) `Update/KE_HOACH_CAU_TRUC_DU_AN.md` có hai bộ route tự mâu thuẫn — cây thư mục để `(student)/dashboard`, `(teacher)/dashboard`, `(admin)/dashboard` (trùng URL `/dashboard` vì route group không vào URL) còn bảng F-ID dùng `/student/...`, `/teacher/...`, `/admin/...`; file này theo bảng F-ID và cần cập nhật cây thư mục cho khớp (thêm thư mục tiền tố `student/`, `teacher/`, `admin/` bên trong từng route group) và thêm `users/` cho nhóm tài khoản (đã đúng). (2) `Tuan4/` 3 file mô tả giao diện vẫn dùng route cũ (`/`, `/exam/[sessionId]`, `/admin/students`…). (3) Mã FE hiện có (`frontend/src/app`) còn `teacher/items/new`, `items/[id]/edit`, `review-queue`, `(student)/page.tsx` ở gốc — là mô hình cũ, không sửa trong phiên này.

---

## 10. PHỤ LỤC

### 10.1. Phụ lục A — Từ điển mã lý do kiểm AI `⚠️ ĐX` (nhãn tiếng Việt cho C-FLAG, S10, S11, S29, S32)
> BE chưa chốt tên mã; FE ánh xạ theo bảng này, **mã lạ → hiển thị "Lý do khác ({mã})"**. Mức: **Cứng** = `HARD` (tự `AI_REJECTED`), **Mềm** = `SOFT` (cờ cho người xem).
| Mã (đề xuất) | Mức | Nhãn hiển thị |
|---|---|---|
| `OPTIONS_INVALID` | Cứng | Phương án không đủ 4 hoặc có phương án trùng nhau |
| `CORRECT_ANSWER_INVALID` | Cứng | Không có đúng một đáp án đúng |
| `LENGTH_INVALID` | Cứng | Độ dài nội dung/phương án không hợp lệ |
| `IRT_B_OUT_OF_RANGE` | Cứng | Độ khó (irt_b) ngoài khoảng cho phép [−4, +4] |
| `SKILL_CEFR_MISMATCH` | Cứng | Kỹ năng hoặc mức CEFR không hợp lệ |
| `MISSING_EXPLANATION` | Cứng | Thiếu giải thích |
| `DUPLICATE_EXACT` | Cứng | Trùng hệt một câu khác (ngân hàng / lô khác / cùng lô) |
| `DUPLICATE_NEAR_HIGH` | Cứng | Gần như giống hệt một câu khác |
| `WORKFLOW_INTEGRITY` | Cứng | Quy trình duyệt không toàn vẹn (ví dụ thiếu người duyệt/xác nhận) |
| `DUPLICATE_NEAR_MID` | Mềm | Gần giống một câu khác |
| `DUPLICATE_SEMANTIC` | Mềm | Có thể là diễn đạt lại của một câu khác |
| `ANSWER_MISMATCH` | Mềm | AI chọn đáp án khác đáp án đang đặt |
| `EXPLANATION_MISMATCH` | Mềm | Giải thích có thể không khớp đáp án |

### 10.2. Phụ lục B — Đối chiếu ID/route cũ ↔ mới (để đọc các file Tuan4/Tuan5 cũ)
| Mã Tuan4 | Mã S | Route cũ | Route chuẩn của file này |
|---|---|---|---|
| C1 / D1 / E1 | S01 | `/login` | `/login` |
| C2 | S02 | `/` | `/student/dashboard` |
| C3 | S03 | `/exam/start` | `/student/exams/[roundId]` |
| C4 | S04 | `/exam/[sessionId]` | `/student/exams/[roundId]/take` |
| C5 | S05 | `/results/[sessionId]` | `/student/results/[sessionId]` |
| C6 | S06 | `/results/[sessionId]/review` | `/student/results/[sessionId]/review` |
| C7 | S07 | `/history` | `/student/history` |
| C9–C11 | S16–S18 | `/change-password`, `/forgot-password`, `/reset-password` | không đổi |
| D2 / E3 | S08 | `/teacher/items`, `/teacher/item-bank` | `/teacher/item-bank`, `/admin/item-bank` |
| D4 / E4 | S10 | `/teacher/items/[id]` | `/teacher/item-bank/[id]`, `/admin/item-bank/[id]` |
| D5 | S11 | `/teacher/review-queue`, `/teacher/items/review` | `/teacher/tasks/reviews/[packageId]` |
| D6 / E5 | S12 | `/teacher/reports` | không đổi |
| D7 / E6 | S13 | `/teacher/students` | không đổi |
| D8 | S14 | `/teacher/students/[code]` | `/teacher/students/[studentId]` |
| D10 / D11 / D12 | S33 / S34 / S35 | `/teacher/inbox/…`, `/me/review-tasks`, `/hod/…` | `/teacher/tasks/reviews`, `/teacher/tasks/confirms`, `/teacher/tasks/confirms/[packageId]` |
| E2 | S36 | — | `/admin/dashboard` |
| E8 | S20 | `/admin/exam-rounds` | không đổi |
| E9 | S21 | `/admin/exam-rounds/new`, `/[id]/edit` | `…/new`, `/[roundId]/edit` |
| E10 | S22 | `/admin/exam-rounds/[id]` | `/admin/exam-rounds/[roundId]` |
| E11 | S23 | `…/[id]/import`, `…/roster` | `/admin/exam-rounds/[roundId]/import` |
| E12 | S19 | `/admin/import-users` | `/admin/users/import` |
| E13 | S24 | `/admin/students`, `/admin/teachers` | `/admin/users/students`, `/admin/users/teachers` |
| E14 / E15 | S26 / S27 | `/admin/item-batches/generate|import` | không đổi |
| E16 / E17 | S28 / S29 | `/admin/item-batches`, `/[id]` | `/admin/item-batches`, `/[batchId]` |
| E18 | S30 | `…/[id]/assign` | `…/[batchId]/assign` |
| E19 | S31 | ngăn trong S29 | không đổi |
| E20 | S32 | `…/[id]/final-check` | `…/[batchId]/final-check` |
| ~~D3/S09~~ | — | `/teacher/items/new` | **Đã bỏ** (không ai thêm câu bằng form) |
| ~~S25~~ | — | Gán QTV đơn vị | **Đã bỏ** (đơn trường) |

### 10.3. Phụ lục C — Tiêu chí chấp nhận chung (áp dụng mọi màn)
1. **Không cuộn ngang** ở 360 px; không có phần tử bị che bởi thanh dưới cố định.
2. Mọi ô nhập có **nhãn chữ phía trên**; lỗi hiện dưới ô, liên kết `aria-describedby`; thứ tự Tab theo thứ tự thị giác; focus nhìn thấy rõ.
3. Mọi huy hiệu/đúng–sai/trạng thái có **chữ hoặc biểu tượng**, không chỉ màu; tương phản đủ.
4. Mỗi biểu đồ có **bảng số liệu thay thế** (nút "Biểu đồ | Bảng").
5. Nút nguy hiểm luôn có hộp xác nhận; hộp Từ chối/Loại bỏ **không có ô lý do**.
6. Mọi nút ghi bị **khóa khi đang gửi** và khi mất kết nối; không thể bấm hai lần tạo hai bản ghi.
7. Mọi `testid` trong file tồn tại đúng tên để viết test E2E.
8. Không có phần tử thuộc danh sách cấm ở Mục 0.1 (SSO, chuông, Đơn vị, chế độ tối, form thêm câu, nút Trả về A).
9. Nhãn hiển thị **tiếng Việt có dấu**, dùng đúng từ điển Mục 2.2; số liệu hiển thị dùng dấu phẩy thập phân kiểu Việt ("-0,28").
10. Mật khẩu tạm không xuất hiện ở bất kỳ đâu trên UI hay trong dữ liệu mẫu.

### 10.4. Phụ lục D — Mẫu prompt gửi cho AI Agent
```
Bạn là kỹ sư frontend. Đọc kỹ file "Tuan5/20261017_MO_TA_LUONG_ROLE_VA_MAN_HINH_CHI_TIET_CHO_AI_AGENT.md".
Nhiệm vụ lượt này: sinh các màn <S02, S03, S04> bằng Next.js App Router (TypeScript) + Tailwind,
dùng dữ liệu mock, đặt file đúng đường dẫn ở Mục 3.
Bắt buộc: (1) làm theo Mục 0.1; (2) dùng khối nền Mục 2 (token, layout, component, từ điển nhãn);
(3) đủ 5 trạng thái giao diện; (4) mọi testid như đặc tả; (5) điểm 🔶 TODO-CONFIRM dùng mặc định ở Mục 9
và chú thích // TODO-CONFIRM <mã>; (6) KHÔNG thêm màn/tính năng ngoài đặc tả.
Cuối cùng liệt kê: các điểm TODO-CONFIRM đã dùng mặc định, các chỗ bạn phải suy đoán, và đối chiếu AC (g) từng màn.
```

### 10.5. Phụ lục E — Ma trận 30 Use Case ↔ màn ↔ API ↔ BR
| UC | Tên | Màn | API chính | BR |
|---|---|---|---|---|
| UCSV01 / UCGV01 / UCADM01 | Đăng nhập | S01 | `POST /auth/login`, `/auth/refresh`, `/auth/logout` | BR-02, 05, 06, 19 |
| UCSV02 | Bắt đầu bài thi | S02, S03 | `GET /exam-rounds/mine`, `POST /sessions` | BR-07…11 |
| UCSV03 | Làm bài | S04 | `GET /sessions/:id/next-item`, `POST /sessions/:id/responses` | BR-10, 11 |
| UCSV04 | Xem kết quả | S05 | `GET /sessions/:id/result` | BR-16 |
| UCSV05 | Xem giải thích AI | S06 | `GET /sessions/:id/review` `⚠️ ĐX` | BR-16, 30 |
| UCSV06 | Lịch sử bài thi | S07 | `GET /placement-profiles/:id/history` | BR-16 |
| UCSV07 | Tiếp tục bài thi | S02, S04 | `GET /sessions/active`, `GET /sessions/:id/resume` | BR-10, 11 |
| UCSV08 | Đổi mật khẩu | S16 | `POST /auth/change-password` | BR-06 |
| UCSV09 | Quên mật khẩu (OTP) | S17, S18 | `POST /auth/forgot-password`, `/auth/reset-password` | BR-14 |
| UCGV02 | Xem ngân hàng (GV) | S08, S10 | `GET /items`, `GET /items/:id` | BR-16, 21, 29, 30 |
| UCGV04 | Sửa câu (bước con của UCGV14) | S11 | `PATCH /items/:id` | BR-27, 30 |
| UCGV07 | Xem báo cáo lớp | S12 | `GET /reports/class-distribution`, `/reports/error-patterns` | BR-13 |
| UCGV08 | Xuất báo cáo CSV | S12 | (chưa có endpoint riêng trong API Contract) `⚠️ ĐX` | BR-13 |
| UCGV09 | Xem hồ sơ SV | S13, S14 | `GET /placement-profiles/:id`, `…/history` | BR-16 |
| UCGV14 | Duyệt và gửi gói (GV A) | S33, S11 | `GET /me/review-tasks`, `PATCH /items/:id`, `POST /items/:id/approve|reject`, `POST /item-packages/mine/send` | BR-16, 22, 24, 25, 27 |
| UCGV15 | Xác nhận gói (GV B) | S34, S35 | `GET /me/confirm-packages`, `POST /items/:id/confirm|remove`, `POST /item-packages/:id/confirm-all` | BR-16, 24, 26 |
| UCADM04 | Xem hồ sơ SV (Admin) | S13, S14 | như UCGV09 | BR-16 |
| UCADM05 | Báo cáo tổng thể | S36, S12 | `GET /reports/…?examRoundId=` | BR-13 |
| UCADM06 | Quản lý/giám sát ngân hàng | S08, S10 | `GET /items`, `GET /item-batches/:id/ai-rejected` | BR-16, 21, 29, 30 |
| UCADM08 | Import tài khoản SV/GV | S19 | `POST /users/import/upload|save?kind=`, `GET|DELETE /users/import/grid` | BR-01…05, 15 |
| UCADM09 | Quản lý tài khoản | S24 | `GET|POST|PATCH /students`, `/teachers`, `POST …/lock|unlock|resend-temporary-password`, `PATCH /users/:id/role` | BR-01, 02, 16…20 |
| UCADM11 | Tạo lô bằng AI | S26, S29 | `POST /item-batches`, `GET /item-batches/:id` | BR-21, 29, 30 |
| UCADM12 | Import đề từ file | S27, S29 | `POST /item-imports/upload|save`, `GET|DELETE /item-imports/grid` | BR-21, 29, 30 |
| UCADM13 | Giao việc và theo dõi lô | S28, S29, S30, S31 | `GET …/assign-preview`, `POST …/assign|reassign`, `PATCH …/deadlines`, `POST /item-packages/:id/force-send` | BR-22…25 |
| UCADM14 | Kiểm tra C3 và Import | S32 | `POST|GET …/final-check`, `POST /items/:id/decision`, `POST …/import` | BR-28, 29, 30 |
| UCADM15 | Quản lý kỳ thi | S20, S21, S22 | `POST|GET|PATCH /exam-rounds`, `POST …/publish|close` | BR-07, 08, 12 |
| UCADM16 | Import danh sách thi | S23 | `POST …/participants/import/upload|save`, `GET|DELETE …/import/grid`, `DELETE …/participants/:studentId` | BR-03, 04, 07, 09 |
| UCADM17 | Theo dõi dự thi | S22 | `GET /exam-rounds/:id/participants`, `GET …/participants/export` `⚠️ ĐX` | BR-07, 10, 11 |

Ghi chú: UC `UCADM02/03/07`, `UCGV03/05/06/10` đã bỏ hoặc ngoài phạm vi, không có màn hình.

### 10.6. Phụ lục F — Trường hiển thị ↔ cột trong `schema.prisma`
> Dùng để định kiểu dữ liệu và dựng mock. **Không bao giờ hiển thị:** `passwordHash`, `externalId`, `contentHash`, `vector` (embedding), `irtA`, `irtC`; `correctAnswer` và giải thích **không** trả về SV trước khi nộp bài.

| Bảng | Trường chính (kiểu) | Hiển thị ở |
|---|---|---|
| `User` | `id`, `email`, `fullName`, `role` (STUDENT/TEACHER/ADMIN), `isActive`, `mustChangePassword`, `passwordChangedAt` | S01, S16, S24, menu |
| `StudentProfile` / `TeacherProfile` | `studentCode` / `teacherCode` (duy nhất) | S13, S14, S22, S24 |
| `ExamRound` | `name`, `opensAt`, `closesAt`, `durationMinutes` (mặc định 45), `status` (DRAFT/SCHEDULED/OPEN/CLOSED; hiển thị = `effectiveStatus`) | S02, S03, S20–S22 |
| `ExamRoundParticipant` | `(roundId, studentId)`, `note` (≤ 255), `addedAt` | S22, S23 |
| `TestSession` | `status`, `thetaFinal`, `seFinal`, `startedAt`, `completedAt`, `expiresAt`, `stoppingReason` | S04, S05, S07, S22 |
| `SessionResponse` | `itemId`, `response` (A–D), `isCorrect`, `thetaAfter`, `seAfter`, `responseTimeMs` | S06 (đáp án chọn, đúng/sai) |
| `LanguageProfile` | `cefrLevel`, `cefrConfidence`, `theta`, `standardError`, `confidenceInterval95`, `boundaryEffect`, `skillProfiles` (JSON), `errorPatterns` (JSON), `aiRecommendations`, `testMetadata` | S05, S14 |
| `Item` | `content`, `options` (JSON), `correctAnswer`, `skill`, `topicTag`, `cefrTarget`, `irtB` (∈ [−4, +4]), `status`, `approvedBy`/`approvedAt` (Admin Import), `batchId` (bắt buộc), `packageId` (sau khi A gửi) | S08, S10, S11, S35 |
| `Explanation` | `content` (một bản cho mỗi `Item`) | S06, S10, S11 |
| `ItemBatch` | `source` (`ItemBatchSource`), `name?`, `status`, `skill?`, `cefrTarget?`, `topicTag?`, `requestedCount?` (chỉ lô AI), `createdBy` | S28, S29 |
| `ItemBatchAssignment` | `confirmerId` (GV B), `assignedBy`, `reviewDays`, `confirmDays` | S29, S30 |
| `ItemPackage` | `reviewerId` (GV A), `confirmerId` (GV B), `status` (OPEN/SENT/DONE), `sentAt?`, `dueAt?` | S29, S33–S35 |
| `ItemReviewAssignment` | `itemId` (duy nhất), `assigneeId`, `dueAt`, `reminderSent` | S33, S11, C-DUE |
| `ItemCheckResult` | `checkpoint` (C1/C2/C3), `level` (PASS/SOFT/HARD), `reasonCodes[]`, `suspectedDuplicateId?` | S10, S27, S29, S32 (chỉ Admin) |
| `ItemReviewEvent` | `action` (`ReviewAction`), `actorId`, `itemId`, `createdAt` | S10 "Lịch sử" (chỉ Admin) |

### 10.7. Việc còn lại với file này
- **Người review (W4.4):** rà từng màn với SRS v3.0 và UC spec; duyệt hoặc đổi các mục `⚠️ ĐX` và `🔶` ở Mục 9.
- **Đồng bộ:** cập nhật `Update/KE_HOACH_CAU_TRUC_DU_AN.md` (cây thư mục, Mục 9 "Nợ đồng bộ") và 3 file mô tả giao diện `Tuan4/` theo route chuẩn của file này.
- **Đã đồng bộ 19/10 (v1.1):** #119–#121; quy tắc BR-01…BR-30 (Mục 4.7); ngoại lệ theo UC (Mục 4.8); ma trận 30 UC (Phụ lục E); trường dữ liệu theo schema (Phụ lục F). **Đã sửa 19/10:** route trong UC spec (UCSV02, 04–07) đã có tiền tố `/student`. **Còn lệch:** S04 theo `roundId` nhưng API theo `sessionId` (P18-3), và `GET /sessions/:id/review`, endpoint xuất báo cáo CSV, endpoint xuất kết quả kỳ thi chưa có trong API Contract của SRS (đề xuất).
- **Kiểm chứng:** chạy sinh thử 1 lượt (Mục 8, lượt 1) để xem đặc tả đã đủ chưa; bổ sung chỗ Agent phải suy đoán.
