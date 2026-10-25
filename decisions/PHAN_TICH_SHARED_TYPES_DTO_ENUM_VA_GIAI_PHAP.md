# Phân tích `shared-types` (DTO và Enum), giải pháp và đánh đổi

> **Cập nhật 20/10/2026:** đã chốt mô hình C (Quyết định #122) và thực hiện bước 1–3 của lộ trình; xem `0.docs/tracking/feature-plans/shared-types.md`. Các mục bên dưới giữ nguyên làm hồ sơ phân tích.

- **Ngày:** 2026-10-19
- **Đối tượng rà soát:** `D:\TLCN\packages\packages\shared-types` (11 file enum, `index.ts`, `package.json`)
- **Đối chiếu với:** `Update/KE_HOACH_CAU_TRUC_DU_AN.md` (Mục `packages/shared-types`), `backend/backend/prisma/schema.prisma`, `Update/SRS_TLCN_v3.0.md`, `Tuan5/DANH_SACH_MAN_HINH_THEO_ROLE.md`, `0.docs/tracking/DECISIONS_LOG.md` (#12, #34, #48, #51), mã `backend/backend` và `frontend`.
- **Trạng thái:** chỉ là phân tích. Chưa sửa mã. Các mục "Cần quyết định" phải được chọn phương án trước khi làm (quy tắc dự án số 1).

---

## 1. Kết luận ngắn

| # | Phát hiện | Mức |
|---|---|---|
| F1 | **Mâu thuẫn quyết định:** gói `shared-types` đã bị #48 coi là bỏ ("không còn gói `shared-types`; kiểu dữ liệu sinh từ OpenAPI — #51"). Kế hoạch cấu trúc 16/10 lại đưa nó vào và nói "Đã chốt (#12)". Không có quyết định nào sau #48 khôi phục nó | 🔴 |
| F2 | 11 enum hiện có **đúng giá trị** so với schema và kế hoạch | ✅ |
| F3 | Thiếu 4 enum so với schema: `ReviewAction`, `CheckPoint`, `CEFRConfidence`, `AuthProviderType` | 🟠 |
| F4 | Thiếu hẳn thư mục `dto/` (kế hoạch ghi 6 file); 6 file đó cũng chưa phủ hết các màn | 🟠 |
| F5 | Thiếu enum **mã lỗi API** (~19 mã trong tài liệu màn hình, FE cần để điều hướng) | 🟠 |
| F6 | Gói chưa build được (không có `tsconfig.json`; `main` trỏ `dist/` chưa có) và không có hạ tầng monorepo (`pnpm-workspace.yaml`, `package.json` gốc, `tsconfig.base.json`) | 🟠 |
| F7 | Không ứng dụng nào dùng gói: BE và FE đều không khai báo `@apt/shared-types`; hiện có **ba bản enum** (BE enum TS, FE mảng `as const`, gói) | 🟠 |
| F8 | Vị trí `packages/packages/shared-types` lệch với đích `packages/shared-types` | 🟡 |
| F9 | Mã lỗi phiên đang mở: SRS ghi `SESSION_IN_PROGRESS`, backend đang dùng `ACTIVE_SESSION_EXISTS` | 🟡 |

---

## 2. Chi tiết từng phát hiện

### F1. Gói này có còn nằm trong thiết kế không?
- **#12 (25/9):** chọn monorepo pnpm + `shared-types`.
- **#34 (2/10):** tách repo (backend/frontend/docs).
- **#48 (7/10):** frontend là repo riêng `D:\TLCN\frontend`, quản lý gói bằng **npm**; #12 "đã bị #34 thay thế một phần", không còn `shared-types`.
- **#51 (7/10):** nguồn kiểu API cho FE là **OpenAPI** (BE thêm Swagger, FE sinh kiểu bằng `openapi-typescript`), tạm viết tay tới khi có task BE-X2.
- **16/10:** `KE_HOACH_CAU_TRUC_DU_AN.md` quay lại monorepo `apps/backend`, `apps/frontend`, `packages/shared-types` và ghi "✅ Đã chốt (#12)". Cấu trúc thực tế trong `D:\TLCN` vẫn là hai thư mục riêng, đúng #48.
- **Hệ quả:** tài liệu đang tự mâu thuẫn. Phải chốt lại trước khi đầu tư vào `shared-types` (xem Quyết định Q1).

### F2. Enum đã có: đúng
`UserRole`, `ExamRoundStatus`, `ItemStatus` (6), `Skill` (2), `CEFRLevel` (6), `SessionStatus` (3), `StoppingReason` (4), `ItemBatchStatus` (10), `ItemBatchSource` (2), `PackageStatus` (3), `CheckLevel` (3) khớp từng giá trị với `schema.prisma`. `ItemSource` đã bỏ đúng.

### F3. Enum còn thiếu
| Enum | Giá trị (theo schema) | Ai cần | Nên đặt trong shared? |
|---|---|---|---|
| `ReviewAction` | APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG | FE hiển thị lịch sử sự kiện (S10, S29) | Có |
| `CheckPoint` | C1, C2, C3 | FE hiển thị kết quả AI kiểm (S10, S32) | Có |
| `CEFRConfidence` | LOW, MEDIUM, HIGH | FE hiển thị độ tin cậy ở S05 | Có |
| `AuthProviderType` | LOCAL, GOOGLE, MICROSOFT | Chỉ BE; Tiểu luận chỉ có LOCAL, SSO thuộc Khóa luận | Không (giữ ở BE) |

Kế hoạch cấu trúc cũng liệt kê thiếu 3 enum đầu, nên đó là thiếu sót từ thiết kế, không chỉ ở mã.

### F4. DTO
Kế hoạch ghi 6 file: `auth`, `user-import-grid`, `exam-round`, `item-batch`, `item-review`, `test-session`. Còn thiếu so với các màn và API trong `DANH_SACH_MAN_HINH_THEO_ROLE.md`:
- Hồ sơ năng lực / kết quả (S05, S14) và lịch sử (S07).
- Báo cáo lớp (S12): phân phối CEFR, chủ đề sai.
- Kết quả AI kiểm (`ItemCheckResult`) và gói duyệt (`ItemPackage`).
- Hộp việc GV (`GET /me/review-tasks`, `/me/confirm-packages`).
- Phân trang và định dạng lỗi chung (`Paged<T>`, `ApiError`).

### F5. Mã lỗi API
Tài liệu màn hình dùng, ví dụ: `NOT_IN_ROUND`, `ROUND_NOT_OPEN`, `ROUND_ALREADY_COMPLETED`, `SESSION_IN_PROGRESS`, `PASSWORD_CHANGE_REQUIRED`, `RATE_LIMITED`, `INVALID_RESET_OTP`, `IMPORT_GRID_EMPTY`, `IMPORT_GRID_EXPIRED`, `IMPORT_FILE_INVALID`, `NOT_ASSIGNED`, `PACKAGE_INCOMPLETE`, `CONFIRMER_IN_REVIEW_GROUP`, `DUPLICATE_AFTER_EDIT`, `INVALID_AFTER_EDIT`, `FINAL_CHECK_REQUIRED`, `FINAL_CHECK_STALE`, `BATCH_NOT_READY_TO_FINALIZE`, `BATCH_BUDGET_EXCEEDED`. Frontend phụ thuộc vào chúng (ví dụ `PASSWORD_CHANGE_REQUIRED` đưa về S16) nên nên có một nguồn duy nhất, hiện chưa có.

### F6–F8. Hạ tầng gói
Không `tsconfig.json`, không `dist/`, không workspace; nằm ở `packages/packages/shared-types`. `npm run build` trong gói sẽ lỗi.

### F7. Ba bản enum
- BE: `item-bank/domain/enums/*`, `auth/domain/enums/*`, `test-session/domain/entities/test-session.entity.ts`, v.v.
- FE: `src/lib/enums.ts` (mảng `as const`, tự ghi "bản sao thủ công, TẠM THỜI").
- Gói: enum TS.
- Mỗi lần đổi enum phải sửa ba nơi; đã từng lệch một lần (FE còn `PENDING_REVIEW` sau khi schema đổi).

### F9. Mã lỗi phiên đang mở
SRS Mục L4 và bảng mã lỗi ghi `SESSION_IN_PROGRESS` (409, kèm `sessionId`). Backend đang trả `ACTIVE_SESSION_EXISTS`. Nên đổi theo SRS ở BE và FE khi làm đợt này.

---

## 3. Các quyết định cần chốt

### Q1. Nguồn kiểu dùng chung giữa FE và BE (quyết định gốc)

| Phương án | Mô tả | Ưu điểm | Nhược điểm / đánh đổi |
|---|---|---|---|
| **A. OpenAPI (đúng #51, không dùng `shared-types`)** | BE thêm Swagger; FE sinh kiểu bằng `openapi-typescript`; enum lấy từ spec | Đã chốt, khớp tách repo; không cần chia sẻ mã; kiểu sinh tự động theo controller thật | Phải làm task BE-X2; enum của Prisma phải được mô tả bằng `@ApiProperty({ enum })` ở mọi DTO; kiểu sinh có thể lỏng nếu quên decorator; không giúp BE kiểm DTO |
| **B. Khôi phục `shared-types` (đúng kế hoạch 16/10)** | Giữ gói enum + DTO dùng chung | Một nguồn thật, kiểm lỗi lúc biên dịch ở cả hai phía; không cần Swagger để có kiểu | Đảo #48/#51, phải ghi quyết định mới; cần hạ tầng monorepo hoặc cơ chế chia sẻ gói (Q3); phải giữ gói đồng bộ với schema bằng tay |
| **C. Kết hợp** | `shared-types` chỉ chứa **enum + mã lỗi + vài kiểu nền** (`Paged`, `ApiError`); DTO request/response sinh từ OpenAPI | Phần dễ lệch nhất (enum, mã lỗi) có nguồn chung; không phải duy trì tay hàng chục DTO | Hai cơ chế chạy song song, phức tạp hơn để giải thích; vẫn cần Swagger và gói |
| **D. Giữ nguyên ba bản, đồng bộ bằng tay** | Không làm gì | Không tốn công | Lặp lại đúng lỗi lệch đã xảy ra; không chấp nhận được khi số enum, DTO tăng nhanh ở các tuần tới |

**Đề xuất (chờ chốt): C.** Lý do: tuần 5/12, repo còn tách và chưa có git; enum và mã lỗi là phần hay lệch nhất và rẻ nhất để chia sẻ; DTO sinh từ OpenAPI không buộc phải đổi hạ tầng. Nếu nhóm muốn ít thay đổi nhất, chọn A và coi thư mục `packages` là bản nháp bỏ đi; nếu muốn đúng kế hoạch 16/10, chọn B và cập nhật DECISIONS_LOG (đảo #48).

### Q2. Kiểu DTO chia sẻ (chỉ cần nếu chọn B hoặc C có DTO)

| Phương án | Mô tả | Ưu điểm | Nhược điểm / đánh đổi |
|---|---|---|---|
| **A. Interface TS thuần** | Gói chỉ chứa `interface`/`type`; BE tự viết class DTO có `class-validator` và `implements` interface đó | FE nhẹ, không kéo thư viện; BE vẫn được kiểm tra khi `implements` | Quy tắc validate nằm riêng ở BE, có thể lệch với form FE |
| **B. Class có `class-validator`** | Gói chứa class DTO có decorator, dùng ở cả BE (ValidationPipe) và FE | Một nguồn cho cả kiểu lẫn validate | FE phải kéo `class-validator`, `class-transformer`, `reflect-metadata` vào bundle; Next.js và decorator dễ gặp lỗi cấu hình |
| **C. Zod schema** | Gói chứa schema zod, kiểu suy ra bằng `z.infer`; BE dùng pipe zod | FE đã dùng zod + react-hook-form; một nguồn cho kiểu và validate | BE đang dùng class-validator, phải đổi hoặc chạy hai kiểu; thêm phụ thuộc cho BE |

**Đề xuất (chờ chốt): A.** Ít rủi ro nhất với tiến độ hiện tại; có thể nâng lên C sau khi Tuần 6 ổn định phạm vi.

### Q3. Cách chia sẻ gói giữa hai repo (nếu chọn B hoặc C)

| Phương án | Mô tả | Ưu điểm | Nhược điểm / đánh đổi |
|---|---|---|---|
| **A. Monorepo pnpm** (kế hoạch 16/10) | Gộp `apps/backend`, `apps/frontend`, `packages/shared-types` | Chia sẻ tức thì, một CI, đúng kế hoạch cấu trúc | Đảo #34/#48 (đã tách repo); phải di chuyển cả hai ứng dụng và CI/CD; chưa có git nên chi phí chuyển còn rẻ, nhưng đây là thay đổi lớn nhất |
| **B. Giữ hai repo, gói riêng, cài qua `file:` hoặc `npm link`** | `shared-types` là thư mục độc lập; mỗi app khai báo `"@apt/shared-types": "file:../packages/shared-types"` | Không đổi cấu trúc repo; đúng #34/#48 | Phải build gói trước khi build app; CI mỗi repo phải checkout được gói; dễ quên cập nhật |
| **C. Xuất gói lên registry riêng (GitHub Packages)** | Phát hành phiên bản `@apt/shared-types` | Chuẩn, có version, hợp CI tách | Thêm quy trình phát hành, quá nặng cho 12 tuần |
| **D. Sao chép tệp sinh tự động** | Script sinh enum/mã lỗi từ `schema.prisma` ra FE | Nhẹ, một nguồn là schema | Chỉ phủ enum, không phủ mã lỗi/DTO; cần viết và bảo trì script |

**Đề xuất (chờ chốt):** nếu chọn Q1 = C thì **Q3 = B hoặc D** (không đảo #34). D phủ tốt nhất phần enum vì `schema.prisma` đã là nguồn chân lý; mã lỗi thì để trong gói nhỏ ở BE xuất qua OpenAPI.

### Q4. Danh sách enum và mã lỗi đưa vào gói
- **Đề xuất:** thêm `ReviewAction`, `CheckPoint`, `CEFRConfidence`; không đưa `AuthProviderType`; thêm `ErrorCode` (19 mã ở F5) với cấu trúc `ApiError { code, message, details? }`.
- Phương án khác: để mã lỗi là chuỗi tự do (đơn giản hơn, nhưng FE mất kiểm lỗi chính tả).

---

## 4. Lộ trình đề xuất (sau khi chốt Q1–Q4)

| Bước | Việc | Phụ thuộc |
|---|---|---|
| 1 | Ghi quyết định mới vào `DECISIONS_LOG` (vai trò `shared-types` sau #48/#51), cập nhật `KE_HOACH_CAU_TRUC_DU_AN.md` (3 enum thiếu, đường dẫn gói, ghi chú #48) và `CLAUDE.md` nếu đổi | Q1 |
| 2 | Bổ sung `ReviewAction`, `CheckPoint`, `CEFRConfidence`, `ErrorCode`; thêm `tsconfig.json`; đưa `packages/packages/shared-types` về `packages/shared-types` | Q1, Q4 |
| 3 | Nối gói vào BE và FE theo cách đã chọn; thay các enum cục bộ (BE enum, FE `lib/enums.ts`) bằng import từ gói; cùng đợt đổi `ACTIVE_SESSION_EXISTS` thành `SESSION_IN_PROGRESS` | Q3 |
| 4 | Thêm DTO theo từng màn khi triển khai màn đó (không viết hết trước) | Q2 |
| 5 | Thêm kiểm tra tự động: script so sánh giá trị enum của gói với `schema.prisma` (chạy trong CI hoặc vitest) để ngăn lệch lại | Bước 2 |
| 6 | Ghi `AI_USAGE_LOG.md`, tạo `feature-plans/shared-types.md` trước khi code | — |

## 5. Rủi ro nếu không xử lý
- Lệch enum giữa FE và BE tái diễn, lỗi chỉ lộ khi chạy thật (như `PENDING_REVIEW` còn sót ở FE).
- Hội đồng hỏi về tổ chức mã nguồn (TC2.4): tài liệu đang nói hai điều khác nhau về cùng một gói.
- Thư mục `packages/` hiện hoạt động như mã chết nhưng nằm trong repo, gây hiểu nhầm là đã dùng.

## 6. Việc nhỏ không cần chờ quyết định
- Đổi `ACTIVE_SESSION_EXISTS` thành `SESSION_IN_PROGRESS` ở BE và FE (SRS đã ghi rõ).
- Sửa Mục `shared-types` trong `KE_HOACH_CAU_TRUC_DU_AN.md`: thêm 3 enum còn thiếu, ghi chú mâu thuẫn với #48.
