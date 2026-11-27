# Kế hoạch OpenAPI/Swagger cho backend và sinh kiểu cho frontend (BE-X2)

- Slug: `be-x2-openapi`
- Trạng thái: **đã triển khai một phần trên nhánh riêng; chưa tích hợp vào nhánh source hiện hành, chưa hoàn tất BE-X2**
- Phạm vi: Tiểu luận (TL). Nợ kỹ thuật từ quyết định #51; bổ sung cho #122.
- Quyết định liên quan: #34 (tách repo), #48 (FE repo riêng), #51 (Swagger + `openapi-typescript`), #122 (`@apt/shared-types`), **#138** (chốt phương án ở file này).
- Cập nhật kiểm tra 27/11/2026: backend OpenAPI branch `feat/be-x2-openapi`, commit `944f1132a4fe525f7bf681f780fb7156e7bfd542`; frontend OpenAPI branch `feat/be-x2-openapi`, commit `7a1a15b`. Cả hai worktree sạch tại thời điểm kiểm tra, nhưng đây là nhánh riêng, chưa merge vào source branch hiện hành. Backend spec tại commit này ghi 45 operation có schema thành công/status không body; mốc 47 thuộc snapshot lịch sử commit 0dac52b trên nhánh khác; coverage có inventory và một số breaking-change checks. Shared types local trên `main` có `ItemBatchStatus.PARTIALLY_IMPORTED` và `ReviewAction.UPDATE_DUE_DATE`, chưa commit/tag; BE/FE package hiện hành vẫn pin Git tag `v3.0.0`, nên các enum local chưa tự đến consumer.
- Giới hạn: OpenAPI branch được dựng từ base backend `9b41f7b`, không bao gồm workflow Q1–Q8 mới trong item-generation; không coi 45 operation tại commit 944f113 là coverage của item-generation hoặc bằng chứng runtime. CI GitHub chưa xác minh.

## 1. Vấn đề

FE và BE lệch định dạng response (đã gặp 2 lần). #122 chỉ dùng chung Enum, ErrorCode, ApiError qua `@apt/shared-types`, còn DTO response vẫn đồng bộ bằng tay vì BE chưa có Swagger (nợ từ #51). Giải pháp là một nguồn sự thật cho hợp đồng API, sinh từ mã backend, và FE sinh kiểu từ đó để lệch thì **lỗi biên dịch**, không giữ nguyên hai repo riêng.

## 2. Baseline lịch sử backend (19/11/2026, nhánh `develop`, HEAD `9b41f7b`)

Mục này ghi lại thời điểm lập kế hoạch; không mô tả trạng thái hiện nay. Repo frontend và nhánh OpenAPI riêng đã tồn tại; xem trạng thái kiểm chứng 27/11 ở đầu tài liệu và Mục 8.

- Chưa có `@nestjs/swagger`; `nest-cli.json` không có plugin; `main.ts` không có `SwaggerModule`.
- Lỗi đã chuẩn hóa qua `src/shared/filters/http-exception.filter.ts`: `{ statusCode, message, error, code?, details?, timestamp, path }`; kiểu này chưa được xuất ra cho FE.
- Response thành công không thống nhất: DTO class (`AuthResponseDto`, `AccountView`), `Paged<AccountView>`, object literal (`{ success }`, `{ grid }`, `{ total }`), `void`, và 7 chỗ `return {…}` chưa có kiểu ở `test-session.controller.ts`.
- 11 controller; DTO đầu vào dùng `class-validator` nên plugin Swagger đọc được.
- Frontend: `apt-workspace/frontend` chưa phải git repo; phần FE chờ URL repo.

## 3. Quyết định đã chốt

### 3.1 Envelope response thành công

| Phương án | Ưu | Nhược | Kết quả |
|---|---|---|---|
| A. Giữ nguyên, không bọc | Ít sửa nhất | Phân trang vẫn mỗi nơi một kiểu | |
| B. Bọc `{ data, meta }` toàn cục | Một hình dạng duy nhất | Đổi hợp đồng mọi endpoint, FE và SRS phải sửa | |
| **C. Chỉ chuẩn hóa phân trang** | Rẻ; Swagger vẫn bắt lệch theo từng endpoint | Không thống nhất toàn bộ | **Chọn** |

### 3.2 Cách FE nhận `openapi.json`

| Phương án | Ưu | Nhược | Kết quả |
|---|---|---|---|
| A. Commit sang `docs-repo` | Có lịch sử riêng | Thêm bước thủ công hoặc CI chéo repo | |
| B. Artifact/release của CI | Tự động theo tag | Cần token GitHub chéo repo | |
| C. Đọc URL staging | Đơn giản | CI frontend phụ thuộc server staging | |
| **D. Commit `openapi.json` trong repo backend** | Ít hạ tầng nhất; repo public nên FE tải raw được | FE phải tải từ GitHub raw | **Chọn** |

## 4. Cách áp dụng

### Backend (nhánh mới từ `develop`, ví dụ `feat/openapi-spec`)

1. Cài `@nestjs/swagger`. Bật plugin trong `nest-cli.json` (`introspectComments: true`).
2. `main.ts`: `SwaggerModule.setup('docs', …)` có `addBearerAuth()`; chỉ mở UI ngoài production.
3. Script `npm run openapi:generate` dựng app bằng module test (mock Prisma/Redis) và ghi `openapi.json` ở gốc repo. **Đây là rủi ro lớn nhất** vì module thật cần Postgres/Redis.
4. Khai báo response tường minh cho từng endpoint (`@ApiOkResponse({ type })`); tách mọi `return {…}` literal và kiểu inline thành response DTO có tên. Đây là phần trực tiếp ngăn lệch định dạng, không phải bản thân việc cài Swagger.
5. `ErrorResponseDto` (class) khớp `HttpExceptionFilter`, đồng bộ với `ApiError` trong `@apt/shared-types`; dùng chung cho các response lỗi.
6. `PagedDto<T>` thống nhất `{ items, total, page, pageSize }` (khớp `Paged<T>` hiện có).
7. CI backend: chạy `openapi:generate` rồi `git diff --exit-code openapi.json` để buộc commit spec cùng thay đổi API.

### Frontend (khi có repo)

8. Cài `openapi-typescript` và `openapi-fetch`. Script `gen:api` tải `openapi.json` từ nhánh `develop` của backend (GitHub raw) rồi sinh `src/lib/api/schema.d.ts`.
9. Thay dần các kiểu viết tay bằng kiểu sinh; chạy `gen:api` và `tsc` trong CI để build đỏ khi API lệch.

### Tài liệu cần đồng bộ

10. `backend/TECH_DEBT.md` (thêm mục BE-X2); `KE_HOACH_CAU_TRUC_DU_AN.md` (nguồn kiểu API); `plans/cicd/HUONG_DAN_CI_CD_TU_A_DEN_Z.md` (bước CI spec); SRS Mục API nếu `PagedDto` đổi tên trường; `weekly-log` tuần hiện tại.

## 5. Rủi ro

| Rủi ro | Cách phòng |
|---|---|
| Sinh spec cần dựng app, module phụ thuộc Prisma/Redis | Dùng module test với provider giả; không kết nối DB/Redis khi sinh |
| Plugin bỏ sót kiểu generic/union | Khai báo `@ApiOkResponse` tường minh cho các endpoint đó |
| Quên commit spec sau khi đổi API | CI `git diff --exit-code openapi.json` chặn merge |
| Repo public nên spec công khai | Không đặt dữ liệu thật hay endpoint nội bộ vào ví dụ; kiểm tra trước khi commit (xem #26, #34) |
| Giữ hai cơ chế chung kiểu (#122: shared-types và OpenAPI) | Phân vai rõ: shared-types chỉ Enum/ErrorCode/ApiError; DTO chỉ từ OpenAPI |

## 6. Kế hoạch test

- Unit: response DTO mới, `PagedDto`, `ErrorResponseDto` khớp filter.
- Hợp đồng: dựng app, so spec sinh ra với `openapi.json` đã commit; mọi route có response 2xx và lỗi được khai báo.
- Case đặc biệt: `void`/204, upload multipart (`user-import`), `@AllowWhenMustChangePassword`, phân trang rỗng.
- FE: tạo thử một thay đổi response giả ở BE để chứng minh `tsc` báo đỏ.

## 8. Trạng thái kiểm chứng 27/11/2026

| Thành phần | Bằng chứng | Trạng thái |
|---|---|---|
| Backend OpenAPI | Nhánh `feat/be-x2-openapi`, commit `944f1132a4fe525f7bf681f780fb7156e7bfd542`; có Swagger setup, `openapi.json`, inventory 45 operation, coverage/breaking checks và test scripts | Đã triển khai trên nhánh riêng; chưa merge vào nhánh source hiện hành |
| Frontend types | Nhánh `feat/be-x2-openapi`, commit `7a1a15b`; `schema.d.ts` được sinh từ spec; workflow tương thích theo SHA và cảnh báo drift | Đã triển khai trên nhánh riêng; chưa merge vào nhánh source hiện hành |
| Shared types | Local `main` có `PARTIALLY_IMPORTED` và `UPDATE_DUE_DATE`; diff chưa commit; BE/FE package hiện hành vẫn pin tag `v3.0.0` | Chưa phát hành; consumer chưa nhận được các giá trị local |
| Q1–Q8 item-generation | Controller/use case đang được phát triển trên source branch hiện hành; spec OpenAPI của nhánh riêng lấy base `9b41f7b` và không chứa item-generation contract | Chưa có OpenAPI cho item-generation; không khai báo hoàn tất coverage |
| Runtime / CI | Unit/typecheck/HTTP mock checks có ghi nhận trong feature plan; GitHub CI chưa xác minh | Chưa xác nhận runtime thật hoặc CI GitHub |

Không chép `openapi.json` từ worktree riêng vào source repo hiện hành nếu chưa tích hợp nhánh code tương ứng; việc đó sẽ tạo contract không sinh ra từ mã nguồn đang dùng. Shared types chỉ được xem là đồng bộ consumer sau khi có release/tag mới và dependency được cập nhật theo quy trình repo.

### Nợ tài liệu/contract còn lại

- Đồng bộ DOCX/OpenAPI cho các endpoint item-generation sau khi backend đưa Swagger metadata và routes Q1–Q8 vào nhánh tích hợp.
- Kiểm thử runtime so response schema và security cho các operation ngoài lát Auth/Test Session.
- CI backend/frontend và workflow drift/compatibility chưa chạy trên GitHub.
- API contract vẫn là code-first sinh từ backend, không phải contract-first; OpenAPI không tự chứng minh runtime.

