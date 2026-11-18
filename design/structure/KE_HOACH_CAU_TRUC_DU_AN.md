# Kế hoạch chốt cấu trúc dự án (NestJS + Next.js + PostgreSQL) — v3.0

- Phạm vi: Tiểu luận (TL) — Hệ thống Adaptive Placement Test (CAT-Rasch) tích hợp AI
- Ngày lập: 2026-09-25 | Cập nhật v3.0: 2026-10-15 (Đồng bộ theo SRS v3.0, Kế hoạch Import Lưới tạm và Kế hoạch Sinh & Duyệt đề AI hai chặng)
- Người soạn: Claude Code (Sonnet 5) & Antigravity (Senior SE / Lead Architect)
- Trạng thái phê duyệt: **Đã chốt các quyết định kiến trúc**:
  1. **Hai repo riêng (#34, #48, #51) + gói `packages/shared-types` chỉ chứa Enum + `ErrorCode` + `ApiError` (mô hình C, Quyết định #122)**; nối vào BE và FE bằng `"@apt/shared-types": "file:..."`; DTO request/response sinh từ OpenAPI (BE-X2). *Thay cho dòng "Monorepo pnpm (#12)" trước đây — #12 đã bị #48 thay thế.*
  2. Prisma ORM bọc qua Repository pattern (Quyết định #13) để đảm bảo Clean Architecture và nguyên tắc Dependency Inversion.
  3. Single-tenant (DC-19): Bỏ hoàn toàn `Institution` và các trường `institution_id`; 3 role người dùng chính: `STUDENT`, `TEACHER`, `ADMIN`.
  4. Xác thực & Tài khoản (DC-02, DC-03, DC-21, DC-23, DC-24): Đăng nhập Email + Mật khẩu (argon2), đổi mật khẩu lần đầu (`mustChangePassword`), quên mật khẩu OTP 6 số qua email (`MailPort` + BullMQ + Redis TTL 10m), khóa tài khoản `isActive`. Import tài khoản SV/GV theo cơ chế "lưới tạm" (Import Grid Redis TTL 30m).
  5. Kỳ thi & Phiên thi (DC-07..DC-10, DC-20): Bổ sung `ExamRound` (`DRAFT`, `SCHEDULED`, `OPEN`, `CLOSED`), import danh sách thi theo lưới tạm; thời hạn phiên thi `expires_at = min(startedAt + durationMinutes, closesAt)`.
  6. Sinh & Duyệt đề AI (DC-27..DC-45): Kéo `item-generation` và `llm-gateway` từ Khóa luận vào Tiểu luận (F-23..F-28); quy trình duyệt 2 chặng: GV vai A (sửa/duyệt/từ chối, gửi gói) $\rightarrow$ GV vai B (confirm gói); kiểm tra AI 3 checkpoint (C1, C2, C3) với lọc trùng 3 tầng (T1 băm, T2 pg_trgm, T3 embedding) + G5 kiểm tra đáp án độc lập.
  7. Lược bỏ `ItemSource` khỏi thực thể `Item` (nguồn gốc được quản lý theo Lô `ItemBatch.source`, enum đổi tên thành `ItemBatchSource`; `Item.batchId` bắt buộc, câu seed thuộc các lô seed); bỏ `WRITING` khỏi `Skill`.
  8. Mã hóa Use Case Kỳ thi: Đổi tiền tố thành `UCADM15` (Quản lý kỳ thi), `UCADM16` (Import danh sách thi), `UCADM17` (Theo dõi dự thi).
- File theo dõi tiến độ đi kèm: `TRACKING_CAU_TRUC_DU_AN.md`.
- Nguồn đã đối chiếu: `SRS_TLCN_v3.0.md`, `20261014_KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md`, `20261014_KE_HOACH_SINH_VA_DUYET_DE_AI.md`, `Mo_ta_So_do_Lop_ClassDiagram.md`, `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx`.

---

## 0. Tóm tắt điều hành

Cấu trúc dự án được thiết kế tuân thủ nghiêm ngặt **Clean Architecture** (phân tách rõ 4 tầng: Domain, Application, Infrastructure, Presentation) bên trong từng module nghiệp vụ của NestJS, kết hợp với cấu trúc phân trang theo vai trò người dùng (Route Groups) của Next.js App Router và gói dùng chung `shared-types`.

**Các điểm điều chỉnh quan trọng trong phiên bản v3.0:**
1. **Bổ sung các module nghiệp vụ Backend mới:**
   - `user-import`: Xử lý import tài khoản SV/GV theo cơ chế lưới tạm trên Redis (UCADM08).
   - `user-admin`: Quản lý tài khoản SV/GV, tạo lẻ, khóa/mở khóa, cấp lại mật khẩu tạm, nâng/thu hồi quyền Admin (UCADM09).
   - `exam-round`: Quản lý kỳ thi, import danh sách thí sinh dự thi theo lưới tạm, theo dõi tiến độ thi thời gian thực (UCADM15, UCADM16, UCADM17).
   - `mail`: Module gửi email bất đồng bộ qua hàng đợi BullMQ, giao tiếp qua port `MailPort` và adapter `SmtpMailAdapter`.
   - `item-generation`: Kéo từ Khóa luận vào Tiểu luận — điều phối tạo lô câu hỏi (AI sinh hoặc file import), bộ lọc AI 3 chặng C1/C2/C3, thuật toán chia đều câu hỏi cho nhóm GV A, quản lý đóng gói gửi GV B, nhắc hạn 24h, kiểm tra delta C3 và import vào ngân hàng (UCADM11..14, UCGV14..15).
   - `llm-gateway`: Cổng gọi LLM dùng chung có dự phòng nhà cung cấp, ghi nhận token/mô hình, cache prompt.
2. **Loại bỏ hoàn toàn multi-tenant:**
   - Xóa bỏ mọi tham chiếu tới `Institution`, `institution_id`, `resolveScope`.
   - `RolesGuard` tinh giản thành bộ lọc theo role duy nhất: `STUDENT`, `TEACHER`, `ADMIN`.
3. **Lược bỏ `ItemSource`:**
   - Thực thể `Item` không chứa trường `source`. Việc truy vết nguồn gốc câu hỏi được liên kết qua `ItemBatch` (`item_batches.source`, enum `ItemBatchSource` = `AI_GENERATED | IMPORTED`).
   - `Item.batchId` bắt buộc (NOT NULL). Câu seed thuộc các lô seed (`source = IMPORTED`, `status = DONE`, `created_by` = Admin hệ thống tạo trước trong script cài đặt); mỗi bộ nguồn một lô, phân biệt bằng `ItemBatch.name` (CEFR-J, CLOTH, GV tự soạn). Quyết định 16/10/2026.
4. **Cấu trúc Frontend Next.js App Router hoàn chỉnh theo 3 vai trò:**
   - Sinh viên: Trang làm bài có đồng hồ đếm ngược theo `expiresAt`, xem giải thích AI theo từng câu.
   - Giảng viên: Hộp việc duyệt câu hỏi (vai A) và hộp việc xác nhận gói câu hỏi (vai B), tra cứu báo cáo lớp lọc theo kỳ thi.
   - Quản trị viên: Bộ màn hình quản lý tài khoản, quản lý kỳ thi (kèm import danh sách thí sinh), và quản lý các lô câu hỏi AI.

---

## 1. Đánh giá công nghệ chi tiết

| Công nghệ | Đánh giá kiến trúc | Vai trò trong hệ thống v3.0 | Kết luận |
|---|---|---|---|
| **NestJS** (Backend) | Dependency Injection qua constructor bằng decorator; module hóa Clean Architecture; phân tách Domain (pure TypeScript, zero-dependency) khỏi Framework | Khung ứng dụng chính, quản lý toàn bộ các module nghiệp vụ API và worker nền | ✅ **Giữ nguyên** |
| **Next.js (App Router)** (Frontend) | SSR kết hợp Client Components (`"use client"`), Route Groups `(auth)`, `(student)`, `(teacher)`, `(admin)` phân quyền trực quan; layout lồng nhau | Giao diện người dùng cho cả 3 vai trò; quản lý cookie `httpOnly`, đồng hồ đếm ngược realtime | ✅ **Giữ nguyên** |
| **PostgreSQL 16** | Nguồn sự thật duy nhất (Single Source of Truth), đảm bảo ACID khi nộp bài thi, lưu trữ User, Item, ExamRound, TestSession, LanguageProfile; hỗ trợ extension `pg_trgm` lọc trùng câu hỏi | Cơ sở dữ liệu quan hệ chính | ✅ **Giữ nguyên** |
| **Redis 7 + BullMQ** | Bộ nhớ đệm tốc độ cao và hàng đợi xử lý nền: (1) State Machine phiên thi CAT, (2) Lưới tạm Import tài khoản và danh sách thi (TTL 30m), (3) Hash mã OTP quên mật khẩu (TTL 10m), (4) BullMQ queue gửi email retry, sinh đề AI, nhắc hạn | Tầng Cache L1, State Machine và Message Broker | ✅ **Giữ nguyên & Mở rộng** |
| **Gói `@apt/shared-types` (mô hình C)** | Gói TS thuần ở `packages/shared-types`, chỉ chứa enum, `ErrorCode`, `ApiError`; BE và FE khai báo `file:` trong `package.json`. DTO API sinh từ OpenAPI. Hai repo riêng vẫn giữ (#48) | Chiến lược chia sẻ kiểu dữ liệu | ✅ **Đã chốt (#122)**; thay #12 |
| **Prisma ORM** | Schema định nghĩa tập trung, hỗ trợ type-safe client, bọc qua Repository pattern ở tầng Domain để đảm bảo Clean Architecture | Tầng Persistence Adapter | ✅ **Đã chốt (#13)** |

---

## 2. Bảng nhận xét — Lỗi cấu trúc thường gặp và cách sơ đồ này xử lý

| # | Lỗi cấu trúc thường gặp | Hậu quả | Cách giải quyết trong thiết kế v3.0 |
|---|---|---|---|
| 1 | Trộn lẫn logic kiểm tra kỳ thi và chấm điểm CAT vào Controller | Không test đơn vị được thuật toán, vi phạm Single Responsibility | Tách bạch: `ExamRoundModule` quản lý điều kiện vào thi; `TestSessionModule` điều phối phiên; `CatEngineModule` là domain service thuần tính toán EAP/Rasch |
| 2 | Hardcode thuật toán và tham số CAT trong source code | Khó tinh chỉnh theta0, ngưỡng dừng SE, danh sách điểm quadrature | Đưa toàn bộ tham số thuật toán vào `config/cat.config.ts`, truy xuất qua `ConfigService` |
| 3 | Domain Model phụ thuộc trực tiếp vào Prisma Client (`@prisma/client`) | Vi phạm Dependency Inversion, không thay thế được tầng lưu trữ | `domain/entities/*.entity.ts` là pure TypeScript class; `domain/repositories/*.interface.ts` định nghĩa hợp đồng; `infrastructure/persistence/prisma-*.repository.ts` hiện thực hóa interface |
| 4 | Gọi API AI trực tiếp rải rác trong các use case | Không kiểm soát được chi phí token, không có cơ chế dự phòng nhà cung cấp | Tập trung qua `llm-gateway/` — quản lý prompt hash cache, token logging, rate limit và fallback |
| 5 | Gộp chung chức năng import và lưu thẳng vào Database mà không có bước đệm | Gặp lỗi giữa chừng làm bẩn database, khó sửa lỗi theo dòng | Cơ chế "Lưới tạm" (Import Grid) trên Redis: tải nhiều file gộp vào lưới, popup lọc lỗi, bấm Lưu mới ghi DB trong 1 transaction duy nhất |

---

## 3. Sơ đồ cấu trúc thư mục chi tiết (cấu trúc đích dạng monorepo; thực tế từ #48/#122: hai repo riêng `backend`, `frontend` + gói `packages/shared-types` nối bằng `file:`)

```
adaptive-placement-test/
├── apps/
│   ├── backend/                                # NestJS — Clean Architecture
│   │   ├── src/
│   │   │   ├── main.ts
│   │   │   ├── app.module.ts
│   │   │   ├── config/
│   │   │   │   ├── configuration.ts            # Đọc .env -> ConfigService
│   │   │   │   ├── cat.config.ts               # Tham số CAT: theta0 (-0.5), SE (<0.35), 41 điểm EAP
│   │   │   │   └── validation.schema.ts        # Joi/Zod validate môi trường
│   │   │   ├── shared/                         # Cross-cutting concerns dùng chung
│   │   │   │   ├── guards/
│   │   │   │   │   ├── jwt-auth.guard.ts       # Xác thực JWT Access Token
│   │   │   │   │   ├── roles.guard.ts          # Phân quyền: STUDENT, TEACHER, ADMIN
│   │   │   │   │   └── must-change-password.guard.ts # Chặn truy cập nếu mustChangePassword=true
│   │   │   │   ├── decorators/
│   │   │   │   │   ├── current-user.decorator.ts
│   │   │   │   │   └── roles.decorator.ts
│   │   │   │   ├── filters/
│   │   │   │   │   └── http-exception.filter.ts
│   │   │   │   └── interceptors/
│   │   │   │       └── logging.interceptor.ts
│   │   │   │
│   │   │   ├── modules/
│   │   │   │   ├── auth/                       # UCSV01, UCGV01, UCADM01, UCSV08, UCSV09
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   ├── entities/user.entity.ts
│   │   │   │   │   │   ├── enums/user-role.enum.ts
│   │   │   │   │   │   └── repositories/user.repository.interface.ts
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── use-cases/
│   │   │   │   │   │   │   ├── login.use-case.ts
│   │   │   │   │   │   │   ├── change-password.use-case.ts
│   │   │   │   │   │   │   ├── forgot-password-otp.use-case.ts
│   │   │   │   │   │   │   ├── reset-password.use-case.ts
│   │   │   │   │   │   │   └── verify-token.use-case.ts
│   │   │   │   │   │   └── dto/{login,change-password,forgot-password,reset-password}.dto.ts
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── persistence/prisma-user.repository.ts
│   │   │   │   │   │   ├── hashing/argon2-password-hasher.ts
│   │   │   │   │   │   ├── cache/redis-otp-cache.service.ts # Lưu OTP 6 số (TTL 10m, tối đa 5 lần sai)
│   │   │   │   │   │   └── providers/jwt.provider.ts
│   │   │   │   │   ├── presentation/auth.controller.ts
│   │   │   │   │   └── auth.module.ts
│   │   │   │   │
│   │   │   │   ├── user-import/                # UCADM08 — Import tài khoản SV/GV qua lưới tạm
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   └── value-objects/{import-report,import-row-result,import-row-status}.ts
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── use-cases/
│   │   │   │   │   │   │   ├── upload-user-import-grid.use-case.ts
│   │   │   │   │   │   │   ├── get-user-import-grid.use-case.ts
│   │   │   │   │   │   │   ├── delete-grid-row.use-case.ts
│   │   │   │   │   │   │   ├── clear-user-import-grid.use-case.ts
│   │   │   │   │   │   │   └── save-imported-users.use-case.ts
│   │   │   │   │   │   └── services/user-import.service.ts
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── excel/xlsx-user-parser.service.ts
│   │   │   │   │   │   └── cache/redis-user-import-grid.repository.ts # Khóa theo adminId + kind (TTL 30m)
│   │   │   │   │   ├── presentation/user-import.controller.ts
│   │   │   │   │   └── user-import.module.ts
│   │   │   │   │
│   │   │   │   ├── user-admin/                 # UCADM09 — Quản lý tài khoản SV/GV, phân quyền
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── use-cases/
│   │   │   │   │   │   │   ├── create-individual-student.use-case.ts
│   │   │   │   │   │   │   ├── create-individual-teacher.use-case.ts
│   │   │   │   │   │   │   ├── toggle-user-active.use-case.ts
│   │   │   │   │   │   │   ├── reset-user-temporary-password.use-case.ts
│   │   │   │   │   │   │   └── update-admin-role.use-case.ts # Nâng/thu hồi quyền Admin
│   │   │   │   │   │   └── dto/{create-user,update-role}.dto.ts
│   │   │   │   │   ├── presentation/user-admin.controller.ts
│   │   │   │   │   └── user-admin.module.ts
│   │   │   │   │
│   │   │   │   ├── exam-round/                 # UCADM15, UCADM16, UCADM17 — Quản lý kỳ thi & Danh sách thi
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   ├── entities/exam-round.entity.ts # isOpen(), effectiveStatus(), includes()
│   │   │   │   │   │   ├── enums/exam-round-status.enum.ts # DRAFT, SCHEDULED, OPEN, CLOSED
│   │   │   │   │   │   └── repositories/exam-round.repository.interface.ts
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── use-cases/
│   │   │   │   │   │   │   ├── create-exam-round.use-case.ts
│   │   │   │   │   │   │   ├── update-exam-round.use-case.ts
│   │   │   │   │   │   │   ├── publish-exam-round.use-case.ts
│   │   │   │   │   │   │   ├── close-exam-round.use-case.ts
│   │   │   │   │   │   │   ├── upload-roster-grid.use-case.ts
│   │   │   │   │   │   │   ├── get-roster-grid.use-case.ts
│   │   │   │   │   │   │   ├── save-exam-roster.use-case.ts
│   │   │   │   │   │   │   ├── get-student-active-rounds.use-case.ts
│   │   │   │   │   │   │   └── monitor-exam-round.use-case.ts
│   │   │   │   │   │   └── services/roster-import.service.ts
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── persistence/prisma-exam-round.repository.ts
│   │   │   │   │   │   ├── excel/xlsx-roster-parser.service.ts
│   │   │   │   │   │   └── cache/redis-roster-grid.repository.ts
│   │   │   │   │   ├── presentation/exam-round.controller.ts
│   │   │   │   │   └── exam-round.module.ts
│   │   │   │   │
│   │   │   │   ├── mail/                       # Tầng gửi email bất đồng bộ
│   │   │   │   │   ├── domain/ports/mail.port.ts # Interface MailPort
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── adapters/smtp-mail.adapter.ts # Nodemailer SMTP
│   │   │   │   │   │   ├── processors/mail.processor.ts  # BullMQ Worker gửi email có retry
│   │   │   │   │   │   └── templates/{welcome-temp-password,otp-reset-password,review-reminder}.hbs
│   │   │   │   │   └── mail.module.ts
│   │   │   │   │
│   │   │   │   ├── item-bank/                  # UCGV02, UCADM06 — Ngân hàng câu hỏi, chỉ xem (GV: câu được giao; Admin: mọi câu)
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   ├── entities/item.entity.ts # Không có source (nguồn ở ItemBatch.source), batchId bắt buộc, status ItemStatus
│   │   │   │   │   │   ├── enums/{skill,cefr-level,item-status}.enum.ts # Đã bỏ ItemSource; nguồn lô là ItemBatchSource (item-generation)
│   │   │   │   │   │   └── repositories/item.repository.interface.ts
│   │   │   │   │   ├── application/use-cases/{get-item-details,list-items-for-cat,list-items-admin}.use-case.ts
│   │   │   │   │   ├── infrastructure/persistence/prisma-item.repository.ts
│   │   │   │   │   ├── presentation/item-bank.controller.ts
│   │   │   │   │   └── item-bank.module.ts
│   │   │   │   │
│   │   │   │   ├── item-generation/            # UCADM11..14, UCGV14..15 — Sinh đề AI & Duyệt hai chặng A/B
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   ├── entities/{item-batch,item-package,item-review-assignment,item-check-result}.entity.ts
│   │   │   │   │   │   ├── enums/{item-batch-status,package-status,checkpoint,check-level}.enum.ts
│   │   │   │   │   │   ├── strategies/duplicate-check/{hash-t1,trgm-t2,embedding-t3}.strategy.ts
│   │   │   │   │   │   └── repositories/{item-batch,item-package}.repository.interface.ts
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── use-cases/
│   │   │   │   │   │   │   ├── create-ai-item-batch.use-case.ts       # UCADM11 (Admin)
│   │   │   │   │   │   │   ├── upload-item-import-grid.use-case.ts    # UCADM12 (Admin)
│   │   │   │   │   │   │   ├── save-imported-item-batch.use-case.ts   # UCADM12 (Admin)
│   │   │   │   │   │   │   ├── assign-review-batch.use-case.ts        # UCADM13 (Admin chia đều nhóm A, chỉ định B)
│   │   │   │   │   │   │   ├── reassign-review.use-case.ts            # UCADM13 (Admin giao lại)
│   │   │   │   │   │   │   ├── update-deadlines.use-case.ts           # UCADM13 (Admin chỉnh hạn)
│   │   │   │   │   │   │   ├── force-send-package.use-case.ts         # UCADM13 (Admin ép gửi gói OPEN → SENT, ghi FORCE_SEND)
│   │   │   │   │   │   │   ├── get-teacher-review-tasks.use-case.ts   # UCGV14 (GV vai A)
│   │   │   │   │   │   │   ├── update-item-review-content.use-case.ts # UCGV14 (GV vai A sửa câu)
│   │   │   │   │   │   │   ├── approve-item-step-a.use-case.ts        # UCGV14 (GV vai A duyệt)
│   │   │   │   │   │   │   ├── reject-item-step-a.use-case.ts         # UCGV14 (GV vai A từ chối)
│   │   │   │   │   │   │   ├── send-package-to-b.use-case.ts          # UCGV14 (GV vai A đóng gói gửi B)
│   │   │   │   │   │   │   ├── get-teacher-confirm-packages.use-case.ts # UCGV15 (GV vai B)
│   │   │   │   │   │   │   ├── confirm-item-step-b.use-case.ts        # UCGV15 (GV vai B xác nhận)
│   │   │   │   │   │   │   ├── remove-item-step-b.use-case.ts         # UCGV15 (GV vai B loại bỏ)
│   │   │   │   │   │   │   ├── confirm-all-remaining-step-b.use-case.ts # UCGV15 (GV vai B xác nhận tất cả)
│   │   │   │   │   │   │   ├── run-final-check-c3.use-case.ts         # UCADM14 (Admin chạy C3)
│   │   │   │   │   │   │   ├── decide-soft-flag-item.use-case.ts      # UCADM14 (Admin quyết lỗi mềm)
│   │   │   │   │   │   │   └── import-batch-to-bank.use-case.ts       # UCADM14 (Admin import FINAL_APPROVED)
│   │   │   │   │   │   └── services/
│   │   │   │   │   │       ├── item-generation.service.ts             # Điều phối sinh dư N', bù thiếu G6
│   │   │   │   │   │       ├── item-check.service.ts                  # Checkpoint C1, C2, C3
│   │   │   │   │   │       ├── item-duplicate-checker.service.ts      # Lọc trùng 3 tầng T1, T2, T3
│   │   │   │   │   │       ├── review-distribution.service.ts         # Thuật toán chia đều câu hỏi nhóm A
│   │   │   │   │   │       └── deadline-reminder.service.ts           # Đặt lịch nhắc trước 24h
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── persistence/
│   │   │   │   │   │   │   ├── prisma-item-batch.repository.ts
│   │   │   │   │   │   │   ├── prisma-item-package.repository.ts
│   │   │   │   │   │   │   └── prisma-review-assignment.repository.ts
│   │   │   │   │   │   └── processors/
│   │   │   │   │   │       ├── batch-generation.processor.ts          # BullMQ sinh câu hỏi AI nền
│   │   │   │   │   │       └── deadline-reminder.processor.ts         # BullMQ nhắc hạn
│   │   │   │   │   ├── presentation/
│   │   │   │   │   │   ├── item-batch-admin.controller.ts         # API Admin
│   │   │   │   │   │   ├── teacher-review-a.controller.ts         # API GV vai A
│   │   │   │   │   │   └── teacher-confirm-b.controller.ts        # API GV vai B
│   │   │   │   │   └── item-generation.module.ts
│   │   │   │   │
│   │   │   │   ├── llm-gateway/                # Cổng gọi LLM dự phòng nhà cung cấp & quản lý token
│   │   │   │   │   ├── domain/ports/llm-provider.port.ts
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── providers/{gemini,openai-fallback}.provider.ts
│   │   │   │   │   │   ├── cache/redis-prompt-cache.service.ts
│   │   │   │   │   │   └── logging/token-usage-logger.service.ts
│   │   │   │   │   └── llm-gateway.module.ts
│   │   │   │   │
│   │   │   │   ├── cat-engine/                 # ⭐ Thuật toán CAT (Rasch 1PL + EAP 41 điểm)
│   │   │   │   │   ├── domain/
│   │   │   │   │   │   ├── entities/{ability-estimate,eap-computation-state}.entity.ts
│   │   │   │   │   │   └── services/cat-engine.domain-service.ts  # Contract thuần TypeScript
│   │   │   │   │   ├── application/
│   │   │   │   │   │   ├── services/cat-engine.service.ts         # Facade điều phối thuật toán
│   │   │   │   │   │   └── use-cases/
│   │   │   │   │   │       ├── pick-next-skill.use-case.ts
│   │   │   │   │   │       ├── select-next-item.use-case.ts       # Randomized Top-5 (status=FINAL_APPROVED)
│   │   │   │   │   │       ├── compute-eap.use-case.ts            # Lưới đều 41 điểm [-4, +4], bước 0.2
│   │   │   │   │   │       └── check-stopping-criterion.use-case.ts # Max 25, SE<0.35, Timeout, Outlier Stop
│   │   │   │   │   └── cat-engine.module.ts
│   │   │   │   │
│   │   │   │   ├── test-session/               # UCSV02, UCSV03, UCSV07 — Điều phối phiên thi
│   │   │   │   │   ├── domain/entities/{test-session,session-response}.entity.ts
│   │   │   │   │   ├── application/use-cases/
│   │   │   │   │   │   ├── start-session.use-case.ts          # BR-10: kiểm tra kỳ OPEN, thuộc roster, tính expires_at
│   │   │   │   │   │   ├── submit-response.use-case.ts
│   │   │   │   │   │   ├── resume-session.use-case.ts         # Kiểm tra còn hạn expires_at
│   │   │   │   │   │   └── compute-result.use-case.ts
│   │   │   │   │   ├── infrastructure/
│   │   │   │   │   │   ├── persistence/prisma-test-session.repository.ts
│   │   │   │   │   │   └── cache/redis-session-cache.service.ts # State machine lưu Redis
│   │   │   │   │   ├── presentation/test-session.controller.ts
│   │   │   │   │   └── test-session.module.ts
│   │   │   │   │
│   │   │   │   ├── language-profile/           # UCSV04, UCGV09, UCADM04 — Hồ sơ năng lực ngôn ngữ
│   │   │   │   │   ├── domain/entities/language-profile.entity.ts # Aggregate root
│   │   │   │   │   ├── application/use-cases/{get-profile,export-for-eduz}.use-case.ts
│   │   │   │   │   ├── infrastructure/persistence/prisma-language-profile.repository.ts
│   │   │   │   │   ├── presentation/language-profile.controller.ts
│   │   │   │   │   └── language-profile.module.ts
│   │   │   │   │
│   │   │   │   ├── ai-explainer/               # UCSV05 — Giải thích AI đúng/sai (gắn theo Item)
│   │   │   │   │   ├── domain/entities/explanation.entity.ts
│   │   │   │   │   ├── application/use-cases/get-item-explanation.use-case.ts
│   │   │   │   │   ├── infrastructure/persistence/prisma-explanation.repository.ts
│   │   │   │   │   ├── presentation/ai-explainer.controller.ts
│   │   │   │   │   └── ai-explainer.module.ts
│   │   │   │   │
│   │   │   │   └── reporting/                  # UCGV07, UCGV08, UCADM05 — Báo cáo lớp & toàn trường
│   │   │   │       ├── domain/entities/class-report.entity.ts
│   │   │   │       ├── application/use-cases/{generate-class-report,export-class-csv}.use-case.ts # Lọc theo examRoundId
│   │   │   │       ├── presentation/reporting.controller.ts
│   │   │   │       └── reporting.module.ts
│   │   │   │
│   │   │   └── jobs/
│   │   │       └── mmle-recalibration.processor.ts # Recalibrate irt_b nền
│   │   │
│   │   ├── prisma/
│   │   │   ├── schema.prisma                   # Single-tenant, bảng users, items, exam_rounds, item_batches...
│   │   │   └── migrations/
│   │   ├── test/{unit,e2e}/
│   │   ├── .env.example
│   │   ├── nest-cli.json
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   └── frontend/                               # Next.js App Router (TypeScript)
│       ├── app/
│       │   ├── (auth)/                         # Màn hình xác thực
│       │   │   ├── login/page.tsx              # Đăng nhập email + mật khẩu
│       │   │   ├── forgot-password/page.tsx    # Nhập email nhận OTP 6 số
│       │   │   ├── reset-password/page.tsx     # Nhập OTP và mật khẩu mới
│       │   │   └── change-password/page.tsx    # Bắt buộc đổi mật khẩu lần đầu (mustChangePassword)
│       │   │
│       │   ├── (student)/                      # Màn hình dành cho Sinh viên
│       │   │   ├── dashboard/page.tsx          # Trang chủ: danh sách kỳ thi đang mở của SV
│       │   │   ├── exams/[roundId]/take/page.tsx # Làm bài thi thích ứng (Timer đếm ngược expiresAt)
│       │   │   ├── results/[sessionId]/page.tsx # Xem kết quả CEFR, hồ sơ năng lực & giải thích AI
│       │   │   └── history/page.tsx            # Lịch sử các đợt thi đã hoàn thành
│       │   │
│       │   ├── (teacher)/                      # Màn hình dành cho Giảng viên
│       │   │   ├── dashboard/page.tsx          # Dashboard tổng quan
│       │   │   ├── reports/page.tsx            # Báo cáo lớp học (bộ lọc theo kỳ thi examRoundId, xuất CSV)
│       │   │   ├── students/[studentId]/page.tsx # Tra cứu hồ sơ năng lực chi tiết sinh viên
│       │   │   ├── item-bank/page.tsx          # UCGV02: Ngân hàng câu hỏi chế độ chỉ xem (câu được giao); chi tiết item-bank/[id]/page.tsx
│       │   │   ├── tasks/
│       │   │   │   ├── reviews/page.tsx        # Hộp việc GV vai A: danh sách câu hỏi được giao
│       │   │   │   ├── reviews/[packageId]/page.tsx # Màn hình duyệt gói của GV A: sửa câu, Duyệt (FIRST_APPROVED), Từ chối, Gửi cho B
│       │   │   │   ├── confirms/page.tsx       # Hộp việc GV vai B: danh sách các gói từ GV A
│       │   │   │   └── confirms/[packageId]/page.tsx # Màn hình xem gói, Xác nhận / Loại từng câu hoặc Confirm-All
│       │   │
│       │   ├── (admin)/                        # Màn hình dành cho Quản trị viên
│       │   │   ├── dashboard/page.tsx          # Thống kê tổng quan hệ thống
│       │   │   ├── users/
│       │   │   │   ├── students/page.tsx       # Quản lý tài khoản SV: danh sách, tạo lẻ, khóa/mở, cấp lại MK
│       │   │   │   ├── teachers/page.tsx       # Quản lý tài khoản GV: danh sách, tạo lẻ, nâng/thu hồi Admin
│       │   │   │   └── import/page.tsx         # Import tài khoản SV/GV theo lưới tạm Redis (popup báo lỗi, Lưu ghi DB)
│       │   │   ├── exam-rounds/
│       │   │   │   ├── page.tsx                # Danh sách các kỳ thi
│       │   │   │   ├── new/page.tsx            # Tạo kỳ thi mới (opensAt, closesAt, durationMinutes = 45)
│       │   │   │   ├── [roundId]/edit/page.tsx # Chỉnh sửa kỳ thi
│       │   │   │   ├── [roundId]/page.tsx      # Chi tiết kỳ thi & giám sát dự thi thời gian thực
│       │   │   │   └── [roundId]/import/page.tsx # Import danh sách sinh viên thi theo lưới tạm Redis
│       │   │   ├── item-batches/
│       │   │   │   ├── page.tsx                # Danh sách các lô câu hỏi, tiến độ, tab "AI đã loại"
│       │   │   │   ├── generate/page.tsx       # Form yêu cầu AI sinh lô (skill, CEFR, topic, N câu)
│       │   │   │   ├── import/page.tsx         # Import đề thi từ file Excel vào lưới tạm
│       │   │   │   ├── [batchId]/assign/page.tsx # Giao việc: chọn nhóm GV A, chỉ định GV B, đặt hạn review/confirm
│       │   │   │   └── [batchId]/final-check/page.tsx # Kết quả C3 delta check, quyết định cờ mềm, nút Import
│       │   │   └── item-bank/page.tsx          # Ngân hàng câu hỏi (Admin, chỉ xem, mọi câu; chi tiết [id])
│       │   │
│       │   ├── layout.tsx
│       │   └── globals.css
│       ├── components/
│       │   ├── ui/                             # Button, Input, Modal, Table, Badge...
│       │   └── features/
│       │       ├── auth/                       # Form đăng nhập, đổi mật khẩu, OTP
│       │       ├── test-taking/                # QuestionCard, CountdownTimer, ProgressBar
│       │       ├── reports/                    # AbilityChart, CEFRRadar, ErrorPatternTable
│       │       ├── import-grid/                # Bảng lưới tạm Redis, popup lỗi, nút Tải thêm & Lưu
│       │       └── item-review/                # DiffViewer (so sánh bản sửa của A), CheckFlagBadge
│       ├── lib/
│       │   ├── api-client.ts                   # Gọi backend NestJS dùng type từ shared-types
│       │   └── auth.ts                         # Quản lý session / token
│       ├── hooks/
│       ├── public/
│       │   └── templates/                      # File Excel mẫu tĩnh: import-students.xlsx, import-teachers.xlsx, import-roster.xlsx, import-items.xlsx
│       ├── next.config.ts
│       ├── tsconfig.json
│       └── package.json
│
├── packages/
│   └── shared-types/                          # DTO & Enum dùng chung FE + BE
│       ├── src/
│       │   ├── enums/
│       │   │   ├── user-role.enum.ts          # STUDENT, TEACHER, ADMIN, EDUZ_SERVICE
│       │   │   ├── exam-round-status.enum.ts  # DRAFT, SCHEDULED, OPEN, CLOSED
│       │   │   ├── item-status.enum.ts        # DRAFT, FIRST_APPROVED, SECOND_APPROVED, FINAL_APPROVED, REJECTED, AI_REJECTED
│       │   │   ├── skill.enum.ts              # VOCABULARY, GRAMMAR (bỏ WRITING)
│       │   │   ├── cefr-level.enum.ts         # PRE_A1, A1, A2, B1, B2, C1_PLUS
│       │   │   ├── session-status.enum.ts     # IN_PROGRESS, COMPLETED, ABANDONED
│       │   │   ├── stopping-reason.enum.ts    # MAX_ITEMS_REACHED, SE_THRESHOLD, ITEM_BANK_BOUNDARY, TIMEOUT
│       │   │   ├── item-batch-status.enum.ts  # GENERATING, IMPORTING, CHECKING, READY_TO_ASSIGN, IN_REVIEW, READY_TO_FINALIZE, FINAL_CHECKED, DONE, FAILED, PARTIAL
│       │   │   ├── item-batch-source.enum.ts  # AI_GENERATED, IMPORTED (thay item-source.enum.ts)
│       │   │   ├── package-status.enum.ts     # OPEN, SENT, DONE
│       │   │   ├── check-level.enum.ts        # PASS, SOFT, HARD
│       │   │   ├── check-point.enum.ts        # C1, C2, C3
│       │   │   ├── review-action.enum.ts      # APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG
│       │   │   └── cefr-confidence.enum.ts    # LOW, MEDIUM, HIGH
│       │   │   # ĐÃ LOẠI BỎ item-source.enum.ts (Item không còn source)
│       │   ├── errors/
│       │   │   ├── error-code.ts              # enum ErrorCode (31 mã: chung, tài khoản, kỳ thi/phiên, import, lô/duyệt)
│       │   │   └── api-error.ts               # interface ApiError { code, message, details? }, SessionInProgressDetails
│       │   ├── values.ts                      # USER_ROLES, ITEM_STATUSES… + kiểu literal (UserRoleValue…) cho FE/zod
│       │   └── index.ts
│       │   # KHÔNG có dto/: DTO request/response sinh từ OpenAPI (#122, #51)
│       ├── tsconfig.json                      # build ra dist/ (CommonJS + .d.ts)
│       └── package.json                       # @apt/shared-types
│
├── infra/
│   ├── docker-compose.yml                      # PostgreSQL 16 + Redis 7 + Mailpit (dev)
│   ├── nginx/nginx.conf                        # API Gateway reverse proxy
│   └── docker/{backend,frontend}.Dockerfile
│
├── .github/workflows/                          # CI/CD: lint, test, build, security scan
├── pnpm-workspace.yaml
├── package.json
├── tsconfig.base.json
├── .gitignore
├── CLAUDE.md
└── README.md
```

---

## 3b. Module Dependency Graph (NestJS import/export)

Đồ thị phụ thuộc module tuân thủ nguyên tắc một chiều của Clean Architecture:

```
                  ┌────────────────────────────────────────┐
                  │               AppModule                │
                  └───────────────────┬────────────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│  AuthModule  │ (Global Guard)│  MailModule  │               │LlmGatewayMod.│
└──────┬───────┘               └──────┬───────┘               └──────┬───────┘
       │                              │                              │
       │                              ▼                              ▼
       │                       ┌──────────────┐               ┌──────────────┐
       │                       │UserImportMod.│               │ItemGenModule │
       │                       └──────┬───────┘               └──────┬───────┘
       │                              │                              │
       │                              ▼                              ▼
       │                       ┌──────────────┐               ┌──────────────┐
       │                       │UserAdminMod. │               │ItemBankModule│
       │                       └──────────────┘               └──────┬───────┘
       │                                                             │
       ▼                                                             ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│ExamRoundMod. │──────────────►│TestSessionMod│◄──────────────│CatEngineMod. │
└──────────────┘               └──────┬───────┘               └──────────────┘
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
                ┌──────────────┐              ┌──────────────┐
                │LangProfileMod│              │ ReportingMod │
                └──────────────┘              └──────────────┘
```

**Quy tắc liên kết giữa các module:**
1. `ItemBankModule` là kho dữ liệu câu hỏi đã duyệt (`FINAL_APPROVED`), được `CatEngineModule` import để chọn câu.
2. `ItemGenerationModule` phụ thuộc `LlmGatewayModule` để gọi AI sinh câu, embedding và kiểm đáp án G5; phụ thuộc `MailModule` để gửi thông báo nhắc việc; khi bấm Import thành công sẽ ghi câu hỏi vào `ItemBankModule`.
3. `ExamRoundModule` cung cấp thông tin kiểm tra tính hợp lệ của kỳ thi và danh sách thí sinh cho `TestSessionModule` khi khởi tạo bài thi.
4. `TestSessionModule` phụ thuộc `CatEngineModule` để cập nhật $\theta$ (EAP) và chọn câu hỏi tiếp theo; khi hoàn thành bài thi sẽ kích hoạt `LanguageProfileModule`.
5. `ReportingModule` tổng hợp dữ liệu từ `LanguageProfileModule` và lọc theo `examRoundId` từ `ExamRoundModule`.

---

## 4. Bảng ánh xạ Truy vết Yêu cầu (Traceability Matrix): F-ID ↔ UC-ID ↔ Thư mục Code

| F-ID (SRS v3.0) | Mã Use Case | Tên Chức năng | Vai trò | Thư mục Backend tương ứng | Đường dẫn Frontend |
|---|---|---|---|---|---|
| F-01 | UCSV01, UCGV01, UCADM01 | Đăng nhập hệ thống (Email + MK) | SV, GV, Admin | `src/modules/auth/` | `/login` |
| F-21 | UCSV08 | Đổi mật khẩu | SV, GV, Admin | `src/modules/auth/` | `/change-password` |
| F-21 | UCSV09 | Quên mật khẩu (OTP qua email) | SV, GV, Admin | `src/modules/auth/`, `src/modules/mail/` | `/forgot-password`, `/reset-password` |
| F-18 | UCADM08 | Import tài khoản người dùng (SV/GV) | Admin | `src/modules/user-import/` | `/admin/users/import` |
| F-22 | UCADM09 | Quản lý tài khoản người dùng (SV/GV) | Admin | `src/modules/user-admin/` | `/admin/users/students`, `.../teachers` |
| F-19 | **UCADM15** | Quản lý kỳ thi (Exam Round) | Admin | `src/modules/exam-round/` | `/admin/exam-rounds` |
| F-20 | **UCADM16** | Import danh sách sinh viên thi | Admin | `src/modules/exam-round/` | `/admin/exam-rounds/[id]/import` |
| F-19 | **UCADM17** | Theo dõi dự thi của kỳ thi | Admin | `src/modules/exam-round/` | `/admin/exam-rounds/[id]` |
| F-23 | UCADM11 | Tạo lô câu hỏi bằng AI | Admin | `src/modules/item-generation/` | `/admin/item-batches/generate` |
| F-24 | UCADM12 | Import đề thi từ file Excel | Admin | `src/modules/item-generation/` | `/admin/item-batches/import` |
| F-25 | UCADM13 | Giao việc duyệt câu hỏi và theo dõi lô | Admin | `src/modules/item-generation/` | `/admin/item-batches/[id]/assign` |
| F-26 | UCGV14 | Duyệt và gửi gói câu hỏi (GV vai A) | GV vai A | `src/modules/item-generation/` | `/teacher/tasks/reviews` |
| F-27 | UCGV15 | Xác nhận gói câu hỏi (GV vai B) | GV vai B | `src/modules/item-generation/` | `/teacher/tasks/confirms` |
| F-28 | UCADM14 | Kiểm tra C3 và Import vào ngân hàng | Admin | `src/modules/item-generation/` | `/admin/item-batches/[id]/final-check` |
| F-03 | UCSV02, UCSV03, UCSV07 | Làm bài thi thích ứng (CAT) | Sinh viên | `src/modules/test-session/`, `cat-engine/` | `/student/exams/[roundId]/take` |
| F-05 | UCSV04, UCGV09, UCADM04 | Xem kết quả & Hồ sơ năng lực | SV, GV, Admin | `src/modules/language-profile/` | `/student/results/[id]`, `/teacher/students/[id]` |
| F-06 | UCSV05 | Xem giải thích AI | Sinh viên | `src/modules/ai-explainer/` | `/student/results/[id]` |
| F-09 | UCGV07, UCGV08, UCADM05 | Báo cáo lớp học & Tổng thể (lọc kỳ) | GV, Admin | `src/modules/reporting/` | `/teacher/reports`, `/admin/dashboard` |
| F-02 | UCGV02, UCADM06 | Xem ngân hàng câu hỏi (chỉ xem) | GV (câu được giao), Admin (mọi câu) | `src/modules/item-bank/` | `/teacher/item-bank`, `/admin/item-bank` |
| F-08 | UCSV06 | Xem lịch sử bài thi | Sinh viên | `src/modules/language-profile/` | `/history` |
| F-26 | UCGV04 | Chỉnh sửa câu hỏi (bước con của UCGV14, chỉ GV vai A, câu DRAFT) | GV vai A | `src/modules/item-generation/` | `/teacher/tasks/reviews/[packageId]` |

---

## 5. Kết luận phân tích & Đảm bảo tiêu chí đánh giá (Rubric)

1. **Chuẩn OOP & Clean Architecture (TC2.1 Mức 5):**
   - Tầng Domain độc lập hoàn toàn khỏi Framework và ORM, giúp viết unit test cho các Use Case và Domain Service đạt độ bao phủ cao (TC2.5) mà không cần mock HTTP Server hay kết nối Database thật.
   - Các nguyên tắc SOLID được thực thi triệt để: Single Responsibility theo từng use case file, Open/Closed thông qua strategy pattern lọc trùng và port/adapter, Dependency Inversion qua repository interfaces.
2. **Khớp 100% giữa Thiết kế và Mã nguồn:**
   - Mọi Use Case trong bảng đặc tả (bao gồm tiền tố mới `UCADM15..17` và bỏ `ItemSource`) đều ánh xạ 1-1 với Use Case Class và Controller Endpoint trong cấu trúc thư mục.
   - Sơ đồ đường dẫn thư mục phản ánh chính xác cấu trúc module đã cam kết trong `SRS_TLCN_v3.0.md` Mục III.
