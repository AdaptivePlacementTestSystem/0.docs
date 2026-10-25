# Kế hoạch: Triển khai Frontend (Next.js) cho Adaptive Placement Test CAT-Rasch

> **Phạm vi đọc:** `SRS_TLCN_v2.6_Final.docx` (Mục III, IX, X, XI, XII, XV), `20260922_MoHinhHoaYeuCau.docx` (24 Use Case), `Mo_ta_So_do_Lop_ClassDiagram.md`, `DECISIONS_LOG.md` (#12, #34 và các quyết định liên quan), và **hợp đồng API thật** của `D:\TLCN\backend\backend\src\modules\*\presentation\*.controller.ts`, `auth/application/dto/login.dto.ts`, `shared/decorators/current-user.decorator.ts`, `shared/filters/http-exception.filter.ts`, `prisma/schema.prisma`.
> **Ngày lập:** 2026-10-07 (Tuần 4/12). **Vai trò người lập:** Senior Engineer + PM.
> **Trạng thái:** ✅ **Mục 3 đã được bạn chốt ngày 2026-10-07 (xem 3.3)** — đã chốt thêm Q-F23/24/26/28 về "Đợt thi" (Mục 3.4); **Q-F25 và Q-F27 cũng đã chốt — không còn câu hỏi mở nào ở Mục 3.** Chưa tạo repo, chưa chạy `create-next-app`, chưa có dòng code nào. File theo dõi đi kèm: [`TRACKING_TRIEN_KHAI_FRONTEND.md`](./TRACKING_TRIEN_KHAI_FRONTEND.md).
> **Cập nhật 2026-10-08 (quyết định #58–#61, xem `DECISIONS_LOG.md`):** (1) **#59 cắt hẳn ExamRound** ⇒ **hủy** FE4.13, FE6.11–6.13, phần chọn đợt ở FE4.1 và Q-F23…Q-F28 / BE-X19; thay thế một phần #55. Sau `COMPLETED` SV luôn xem được đáp án + giải thích qua FE5.5 (`/sessions/:id/review`). (2) **#58:** `POST /sessions` trả **409** kèm `sessionId` khi đã có phiên dở (FE4.2 giữ giả định này; điều hướng sang 'Tiếp tục'). (3) **#60:** giải thích do AI sinh lúc sinh câu hỏi và GV duyệt, lưu sẵn trong Item Bank ⇒ FE5.5/5.6 chỉ đọc, không chờ AI. (4) **#61:** BE phải có sớm BE-X8, X9, X14, X16, X4 (`result`) và X10 (`review`). Các mục Mục 3.4, bảng task và ước lượng bên dưới **chưa được viết lại**; đọc kèm ghi chú này.
>
> **Quan hệ với kế hoạch Backend:** [`KE_HOACH_RA_SOAT_VA_HOAN_THIEN_BACKEND.md`](./KE_HOACH_RA_SOAT_VA_HOAN_THIEN_BACKEND.md). Frontend **phụ thuộc** một số task Backend (Mục 5); nhiều chỗ hợp đồng API hiện còn thiếu — xem Mục 2.
>
> **Cách hiểu "bảng nhận xét":** Frontend **chưa tồn tại** (không có thư mục, không có repo — đúng `CLAUDE.md`). Vì vậy bảng nhận xét ở Mục 2 **không phải rà soát code**, mà là *phân tích khoảng trống & rủi ro*: yêu cầu SRS/Use Case nào Frontend phải đáp ứng, hợp đồng API Backend hiện có đáp ứng được hay không, và phải quyết định gì trước khi code. Nếu bạn muốn hiểu khác, báo tôi.

---

## 0. Tóm tắt điều hành

**Kết luận một câu:** Frontend là phần có nhiều Use Case nhất (UCSV01–07, UCGV01–10, UCADM01–07 = 24 UC) nhưng SRS chỉ xếp lịch rất ngắn (Tuần 9–10: giao diện làm bài + Result Dashboard; Tuần 10–11: Class Report). Với Backend đang ở trạng thái "scaffold chưa đúng", **rủi ro lớn nhất không nằm ở việc vẽ giao diện mà ở hợp đồng API còn thiếu/lệch** — nếu bắt đầu code UI sớm mà không khóa hợp đồng, sẽ phải làm lại.

| Nhóm | Số mục | 🔴 | 🟠 | 🟡 | 🟢 |
|---|---|---|---|---|---|
| G. Hợp đồng API Frontend↔Backend (thiếu/lệch) | 14 | 3 | 7 | 4 | 0 |
| S. Bảo mật phía client | 5 | 2 | 2 | 1 | 0 |
| U. Luồng làm bài thi & độ tin cậy giao diện | 6 | 1 | 4 | 1 | 0 |
| P. Phạm vi, tiến độ & quy trình | 6 | 0 | 3 | 3 | 0 |
| **Tổng** | **31** | **6** | **16** | **9** | **0** |

**Năm điểm cần đọc trước:**
1. **G-01 — Không có cách nào để Frontend biết "phiên dở dang" (UCSV07).** `POST /sessions` luôn tạo phiên mới; `GET /sessions/:id/resume` cần biết `id` trước. Không có `GET /sessions/active`. Lưu `sessionId` ở `localStorage` sẽ hỏng khi đổi thiết bị/xóa trình duyệt.
2. **G-02 — Frontend không biết MSSV của chính mình.** JWT/`/auth/me` chỉ có `sub, role, institutionId, email`; nhưng route hồ sơ là `GET /placement-profiles/:studentCode` (theo MSSV). Sinh viên không thể mở hồ sơ của chính mình nếu không tra được `studentCode`.
3. **G-03 — Không có `GET /sessions/:id/result`** (SRS X), cũng không có `history`, `class-distribution`, `error-patterns`, `GET/PUT/DELETE /items/:id`. Màn "Kết quả" (UCSV04) và "Lịch sử" (UCSV06) chưa có nguồn dữ liệu. (Đã nằm trong kế hoạch Backend P4.11, P6.x — nhưng Frontend phải chờ hoặc dùng mock.)
4. **S-01 — Token để đâu?** Backend hiện trả `accessToken` trong body, chưa có refresh, `CORS origin: true`. Nếu để `localStorage` thì một lỗi XSS lấy được toàn bộ phiên (kể cả ADMIN). Cần chốt kiến trúc lưu token (Q-F3) **trước** khi viết màn đăng nhập.
5. **U-01 — Đồng hồ 45 phút.** SRS quy định timeout 45 phút nhưng không API nào trả thời điểm hết hạn. Nếu đồng hồ chạy ở client, đóng/mở lại tab hoặc đổi máy là đồng hồ sai; cần `expiresAt` do server quyết định.

**Có thay đổi tính năng cốt lõi không?** **Không.** Frontend chỉ *hiển thị và thu thập*; mọi tính toán (EAP, chọn câu, điều kiện dừng, CEFR) vẫn ở Backend. Chi tiết ở Mục 6.

---

## 1. Kiểm chứng nguồn (bằng chứng đã đọc)

| # | Điều đã kiểm | Nguồn | Kết quả |
|---|---|---|---|
| V1 | Không có thư mục frontend | `ls D:\TLCN` | Không có `frontend/`; chỉ `backend/backend`. Đúng `CLAUDE.md` "CHƯA CÓ CODE" ở phía FE. |
| V2 | Quyết định cấu trúc repo | `DECISIONS_LOG` #34 | **Tách repo backend/frontend/docs**, Free + public. ⇒ #12 (pnpm workspaces + `shared-types`) **bị thay thế một phần**: không thể chia sẻ gói `shared-types` trực tiếp giữa 2 repo. |
| V3 | Công nghệ FE chốt trong SRS | SRS XI, III | Next.js (React/TypeScript), "SSR"; Nginx ở phía trước; Docker Compose. |
| V4 | Lịch FE theo SRS | SRS XII | Tuần 9–10: giao diện làm bài thi; Tuần 10: Student Result Dashboard + Radar; Tuần 11: Teacher Class Report. Hiện Tuần 4. |
| V5 | Phạm vi UI theo F-ID | SRS IX | Chỉ **F-08 (P1)** Student Result Dashboard và **F-09 (P1)** Teacher Class Report được ghi là FE; F-02 (Item Bank CRUD, P0) cần UI theo UCGV02–06; **F-16 (chống gian lận), F-11 (AI Question Generator) là Khóa luận**. |
| V6 | 24 Use Case | `20260922_MoHinhHoaYeuCau.docx` | SV 7, GV 10, Admin 7. |
| V7 | Endpoint Backend thực có | `*.controller.ts` | `auth/login`, `auth/me`; `sessions` (POST, GET next-item, POST responses, GET resume); `items` (GET danh sách chỉ lọc `status`,`skill`; POST; POST `:id/approve`; POST `:id/reject` **không nhận lý do**); `placement-profiles/:studentCode`; `reports/distribution`, `reports/export-csv`; `explanations/items/:itemId`. |
| V8 | JWT payload | `current-user.decorator.ts` | `{ sub, role, institutionId, email }` — **không có `studentCode`, `fullName`**. Login trả thêm `user.fullName`. |
| V9 | Định dạng lỗi | `http-exception.filter.ts` | `{ statusCode, message: string \| string[], error, timestamp, path }` — không có mã lỗi nghiệp vụ ổn định. |
| V10 | `next-item` khi hết câu | `test-session.controller.ts` | Trả **HTTP 200** `{ message: '...' }` thay vì lỗi/trạng thái riêng. |
| V11 | Câu hỏi gửi sang SV | `formatItemForStudent` | `{ id, content, options, skill, cefrTarget }` — **có** `cefrTarget` (lộ độ khó danh nghĩa; xem U-05). Không có số thứ tự câu, tổng câu, thời gian còn lại. |
| V12 | Submit trả gì | `submit-response.use-case.ts` | `{ isCorrect, thetaAfter, seAfter, shouldStop, stoppingReason }` — **lộ `isCorrect`, `thetaAfter`, `seAfter` ngay khi nộp** (xem U-04). |
| V13 | Enum trạng thái/lý do | `schema.prisma` | `SessionStatus`, `StoppingReason {MAX_ITEMS_REACHED, SE_THRESHOLD, ITEM_BANK_BOUNDARY, TIMEOUT}`, `Skill {VOCABULARY, GRAMMAR}`, `CEFRLevel`, `CEFRConfidence`, `ItemStatus`. |
| V14 | Swagger/OpenAPI | `grep` trong Backend & kế hoạch BE | **Chưa có** `@nestjs/swagger`; SRS Tuần 10 nhắc "Swagger". Kế hoạch Backend **chưa có task** này. |

> ⚠️ **Giới hạn:** các phát hiện dưới đây đến từ đọc tài liệu và mã controller, **chưa chạy Backend** (chưa có DB/Redis dựng sẵn trong phiên này). Mọi hình dạng JSON ở Mục 2 là *theo mã*, Agent phải xác minh lại bằng cách gọi thật ở task FE2.1.

---

## 2. Bảng nhận xét chi tiết (phân tích khoảng trống & rủi ro)

Quy ước: 🔴 chặn làm đúng/an toàn · 🟠 sẽ gây làm lại hoặc UX sai · 🟡 nên làm · "Tác động" = hệ thống của bạn bị ảnh hưởng gì nếu xử lý như đề xuất.

### 2.G. Hợp đồng API Frontend ↔ Backend

| Mã | Mức | Phát hiện | Giải pháp đề xuất & lý do | Tác động hệ thống | Task |
|---|---|---|---|---|---|
| G-01 | 🔴 | Không có API tìm phiên đang dở (UCSV07 bước 1–2: "hiển thị nút Tiếp tục bài thi dở dang" khi đăng nhập lại) | Thêm `GET /sessions/active` (trả phiên `IN_PROGRESS` của chính mình hoặc `null`) — theo **Q-F11**. Lý do: nguồn sự thật phải ở server (đúng SRS 15.2 "khôi phục phiên"), không dựa `localStorage` | Backend thêm 1 endpoint + use case; liên quan **Q5** (nhiều phiên IN_PROGRESS) của kế hoạch BE | BE-X8, FE4.9 |
| G-02 | 🔴 | Frontend không biết `studentCode` (MSSV) để gọi `GET /placement-profiles/:studentCode`; `/auth/me` chỉ trả JWT payload | Mở rộng `login`/`me` trả `user.studentCode` (SV) — hoặc thêm `GET /placement-profiles/me`. Mặc định: **thêm `studentCode` + `fullName` vào `/auth/me` và `login.user`** (rẻ, không đổi route) | Backend sửa DTO; không đổi schema (MSSV đã có ở `StudentProfile`) | BE-X14, FE3.4 |
| G-03 | 🔴 | Thiếu các endpoint SRS X mà màn hình cần: `GET /sessions/:id/result`, `GET /placement-profiles/:code/history`, `GET /reports/class-distribution`, `GET /reports/error-patterns`, `GET/PUT/DELETE /items/:id`, `POST /auth/refresh`, `POST /auth/logout` | Đã có trong kế hoạch BE (P4.11, P6.8, P6.10–11, P6.1–3, P5.6). FE dùng **mock theo hợp đồng** (MSW) cho tới khi BE xong; **không** tự bịa endpoint khác | Cho phép FE chạy song song BE (Q-F13) | BE-X3..X7, FE2.x |
| G-04 | 🟠 | Phiên thi thiếu siêu dữ liệu để vẽ UI: số thứ tự câu, tối đa 25, thời gian còn lại/`expiresAt`, `itemCount` | Trả thêm `session: { id, itemCount, maxItems, expiresAt, state }` ở `POST /sessions`, `next-item`, `resume` — theo **Q-F10** | Đồng hồ đúng khi đổi tab/máy; thanh tiến độ "câu n/25" hiển thị được. Lưu ý: *không* hiển thị "còn bao nhiêu câu nữa" vì CAT có thể dừng sớm (SE<0.35) | BE-X9, FE4.3 |
| G-05 | 🟠 | `GET /items` chỉ lọc `status`, `skill`; UCGV02 yêu cầu lọc theo CEFR, nguồn, tìm theo từ khóa; chưa có phân trang | Thêm `cefr`, `source`, `q`, `page`, `limit`, trả `{ data, total }` | Danh sách lớn (250+ câu, SRS Tuần 4) không tải một lần; lọc "theo thời gian thực" làm phía server | BE-X17, FE6.2 |
| G-06 | 🟠 | `POST /items/:id/reject` không nhận lý do, trong khi UCGV05 bước 4b ghi "nhập lý do" | **Đã chốt (quyết định #56): không ghi lý do.** FE không có ô nhập lý do; nút "Từ chối" chỉ có hộp xác nhận. Không đổi schema, không cần BE-X18 | UCGV05 4b lệch đặc tả Use Case ⇒ ghi vào đề xuất SRS v2.7 (FE9.5). GV khác sẽ không biết vì sao câu bị loại | FE6.6, FE6.7 |
| G-07 | 🟠 | UCSV05 (xem giải thích): cần danh sách câu đã làm kèm đáp án SV chọn, đáp án đúng, giải thích — **chỉ sau khi `COMPLETED`**. `GET /explanations/items/:itemId` hiện không gắn phiên (đã là lỗi A-04 phía BE) | Thêm `GET /sessions/:id/review` (chỉ phiên của mình và đã hoàn thành) trả `[{ item, chosen, correct, isCorrect, explanation }]`; FE không gọi `/explanations/items/:id` trực tiếp | Đóng lỗ rò đáp án (A-04) và cho FE đúng một luồng | BE-X10, FE5.5 |
| G-08 | 🟠 | Lỗi không có mã ổn định: FE không phân biệt được "item không khớp state" (409), "phiên hết hạn", "hết quyền" ngoài chuỗi tiếng Việt | Chuẩn hóa `{ code: 'SESSION_ITEM_MISMATCH' \| 'SESSION_EXPIRED' \| ..., message }`; FE chỉ `switch(code)` | Nếu không, FE phải so chuỗi — dễ vỡ khi đổi thông báo | BE-X11, FE2.4 |
| G-09 | 🟠 | `next-item` hết câu ⇒ HTTP 200 `{message}` (V10) — FE sẽ render `undefined` thành câu hỏi | Theo **Q10** của kế hoạch BE (kết thúc phiên có lý do rõ ràng); FE xử lý bằng discriminated union `{ kind: 'item' } \| { kind: 'finished', reason }` | Không còn "màn trắng" giữa bài thi | BE-X12, FE4.4 |
| G-10 | 🟠 | Submit trả `isCorrect/thetaAfter/seAfter` ngay | Xem **U-04**: BE **không** trả `theta/se` trong lúc thi; `isCorrect` **chỉ trả khi đợt thi bật phản hồi** (Q-F12(a), 3.3–3.4); mặc định `{ accepted, shouldStop }` | Tránh SV đoán đáp án đúng/sai theo từng câu (CAT test phải "kín" đến lúc xong); đồng thời giảm dữ liệu lộ | BE-X16, FE4.5 |
| G-11 | 🟡 | Tên route lệch SRS: code `reports/distribution` vs SRS `reports/class-distribution`; `:studentCode` vs SRS `:student_id` | FE gọi qua **một** lớp `api/endpoints.ts`; đổi route chỉ sửa 1 chỗ | Giảm chi phí khi BE đổi tên (E-01/E-03 của kế hoạch BE) | FE2.2 |
| G-12 | 🟡 | Chưa có OpenAPI ⇒ kiểu dữ liệu FE phải tự viết tay, dễ lệch (rủi ro đã cảnh báo ở `Tuan2/KE_HOACH_CAU_TRUC_DU_AN.md`) | Theo **Q-F4**: thêm `@nestjs/swagger` ở BE, FE sinh kiểu bằng `openapi-typescript` | Không còn gói `shared-types` (do #34 tách repo) nhưng vẫn một nguồn sự thật | BE-X2, FE2.3 |
| G-13 | 🟡 | CORS BE: `origin: true` | Allowlist theo ENV (đã có trong kế hoạch BE, phase P1) | Cần cho cookie `credentials` nếu chọn phương án BFF khác | BE-X1 |
| G-14 | 🟡 | `GET /reports/*` của Admin gán `'default-institution'` (E-05 phía BE) ⇒ lỗi | Chờ BE sửa; FE không xử lý lỗi này (không "chữa cháy" ở client) | — | BE P6.10 |

### 2.S. Bảo mật phía client

| Mã | Mức | Phát hiện | Giải pháp & lý do | Tác động | Task |
|---|---|---|---|---|---|
| S-01 | 🔴 | Lưu token ở đâu (V7: BE trả token trong body) | **Q-F3.** Mặc định: Next.js đóng vai trò BFF — route handler nhận `login`, đặt token vào **cookie `httpOnly; Secure; SameSite=Lax`**, FE gọi qua `/api/proxy/*`. Lý do: JS trong trình duyệt không đọc được token ⇒ XSS không lấy được phiên; `middleware.ts` đọc cookie để chặn route theo vai trò ngay ở SSR | Thêm một lớp proxy (≈ +1 hop; ngân sách NFR 300 ms p95 cho submit+next vẫn dư vì cùng host). Hệ quả: CORS gần như không cần | FE3.2–3.3 |
| S-02 | 🔴 | Rò đáp án qua giao diện/DevTools: SRS 15.3 "đáp án đúng không bao giờ trả về client trước khi nộp" | Chủ yếu là việc của BE (A-04, G-10). FE: kiểu dữ liệu `ExamItem` **không có** trường đáp án; test e2e khẳng định response của `next-item` không chứa `correct*` | Một test chặn hồi quy | FE4.12 |
| S-03 | 🟠 | Hiển thị nội dung câu hỏi: nội dung do GV nhập (`items.content`, có `____`) ⇒ nguy cơ XSS nếu render HTML | Mặc định render **văn bản thuần** (`white-space: pre-wrap`), không `dangerouslySetInnerHTML` (**Q-F16**) | GV không dùng được in đậm/gạch chân trong đề; đủ cho Vocabulary/Grammar | FE1.7, FE4.3 |
| S-04 | 🟠 | Phân quyền chỉ ở UI là vô nghĩa nếu BE hở (A-03) | FE vẫn chặn theo vai trò (`middleware.ts` + ẩn menu) để UX đúng, nhưng **tài liệu hóa rõ: đây không phải lớp bảo mật** | Tránh ảo giác an toàn khi báo cáo | FE3.6 |
| S-05 | 🟡 | Header bảo mật (CSP, `X-Content-Type-Options`, `Referrer-Policy`), không để lộ biến môi trường | `next.config` headers; chỉ biến `NEXT_PUBLIC_*` cho giá trị công khai; repo **public** (#34) ⇒ `.env*` vào `.gitignore` ngay từ task đầu | Tránh lặp lại A-09 (BE không có `.gitignore`) | FE1.1, FE8.4 |

### 2.U. Luồng làm bài thi & độ tin cậy giao diện

| Mã | Mức | Phát hiện | Giải pháp & lý do | Tác động | Task |
|---|---|---|---|---|---|
| U-01 | 🔴 | Đồng hồ 45 phút phải do server quyết định (G-04) | Hiển thị đếm ngược dựa `expiresAt` − (giờ server ước lượng bằng độ lệch đo ở lần gọi đầu); hết giờ ⇒ gọi `next-item`/`result` để server tự kết thúc (`TIMEOUT`) | Đúng khi F5/đổi máy; không tin đồng hồ máy khách | FE4.6 |
| U-02 | 🟠 | Double-submit / spam (SRS 15.5): bấm "Nộp" hai lần, mạng chậm | Khóa nút ngay khi gửi, giữ `AbortController`; nếu BE trả 409 `SESSION_ITEM_MISMATCH` ⇒ **không báo lỗi**, tự `refetch next-item` (idempotent theo state machine) | Trải nghiệm không "vỡ" khi mạng chập chờn | FE4.5 |
| U-03 | 🟠 | Tải lại trang giữa câu (F5) ⇒ phải thấy **đúng câu cũ** | `next-item` đã idempotent khi `WAITING_FOR_ANSWER` (SRS 15.5) ⇒ trang thi luôn khởi tạo bằng `next-item`; không lưu câu hỏi ở `localStorage` | Không cần đồng bộ thêm; câu đã chọn nhưng chưa nộp thì mất (chấp nhận, ghi chú UI) | FE4.4 |
| U-04 | 🟠 | Hiển thị đúng/sai theo từng câu trong lúc thi | **Đã chốt: GV bật/tắt theo từng đợt thi** (Mục 3.3–3.4). UI chỉ hiện phản hồi khi phiên có cờ bật; ngược lại **bỏ qua** `isCorrect/theta/se` kể cả nếu BE lỡ trả. θ/SE **không bao giờ** hiện trong lúc thi | Giữ CAT "kín"; nếu bạn muốn phản hồi từng câu (kiểu luyện tập) thì khác SRS UCSV03 | FE4.5 |
| U-05 | 🟠 | `cefrTarget` đi kèm câu hỏi (V11) cho SV biết độ khó danh nghĩa ⇒ SV đoán được θ | Không hiển thị `cefrTarget` cho SV; đề xuất BE bỏ khỏi payload SV (cùng G-10) | Nhỏ; tránh thông tin dư | FE4.3 |
| U-06 | 🟡 | Mất mạng giữa chừng | Thanh trạng thái "Mất kết nối – đang thử lại", `retry` có backoff cho GET; **POST không tự retry mù** (phụ thuộc idempotency, xem U-02) | Không gửi trùng đáp án | FE4.7 |

### 2.P. Phạm vi, tiến độ & quy trình

| Mã | Mức | Phát hiện | Giải pháp & lý do | Tác động | Task |
|---|---|---|---|---|---|
| P-01 | 🟠 | SRS xếp FE vào Tuần 9–10, nhưng hiện Tuần 4 và BE còn lỗi; nếu đợi BE xong mới làm, FE bị dồn vào 2–3 tuần cuối | **Q-F13** (mặc định): bắt đầu FE từ Tuần 5 với **mock theo hợp đồng** (MSW), tích hợp BE thật khi P4/P5/P6 của BE xong | Trải đều công việc; rủi ro: mock lệch thật ⇒ có task "đối chiếu hợp đồng" (FE2.6, FE8.1) | Toàn kế hoạch |
| P-02 | 🟠 | Use Case Admin (UCADM02/03/07: quản lý tài khoản, phân quyền, cấu hình) và UCGV10 (gán chủ đề bằng AI): **không có endpoint Backend** và không có trong kế hoạch BE | **Q-F12** (mặc định): *không làm* ở TL; Admin dùng chung giao diện Giảng viên (+ xem toàn hệ thống: UCADM04/05/06). Ghi vào "Phạm vi bị cắt" của báo cáo | Nếu bạn muốn làm thì kéo thêm cả BE ⇒ ≥ 1,5 tuần/người | FE0.1, FE9.6 |
| P-03 | 🟠 | #12 (pnpm workspaces + `shared-types`) mâu thuẫn #34 (tách repo) | Ghi nhận #12 đã bị thay thế; **Q-F18**: dùng `npm` như BE, kiểu dữ liệu sinh từ OpenAPI | Cần cập nhật `DECISIONS_LOG` (không sửa dòng cũ, thêm dòng mới) | FE0.4 |
| P-04 | 🟡 | CI chưa có ở BE; repo FE public ⇒ phải có `.gitignore`, lint, test trước khi nhiều commit | FE1 dựng sẵn `lint`, `typecheck`, `test`; **CI để ở Mục 11** (chưa quyết) | Số liệu TC2.4/2.5 phải đo thật ở repo FE | FE1.x |
| P-05 | 🟡 | Phân công (2 người) không có trong tài liệu | **Không tự phân công.** Cột "Người" trong tracking để trống cho bạn điền | — | — |
| P-06 | 🟡 | UI tiếng gì? SRS không nói | **Q-F9** | Chi phí i18n nếu đổi về sau | FE1.6 |

---

## 3. Các điểm CẦN BẠN CHỐT (đã chốt hết — xem 3.3)

> Cách chốt: đánh dấu `☑` vào **một** phương án mỗi câu, hoặc ghi ở Mục 3.3 "duyệt hết mặc định" / liệt kê mã khác mặc định. **Task nào phụ thuộc câu chưa chốt thì Agent không làm** (Mục 10.3). Phương án ★ là khuyến nghị của tôi, không phải quyết định.

### 3.1. Nhóm I — ảnh hưởng thiết kế (chốt trước khi làm task liên quan)

| Mã | Câu hỏi | Phương án (★ = khuyến nghị) | Đánh đổi |
|---|---|---|---|
| ☑ **Q-F1** | Vị trí & tên repo FE (theo #34 đã tách repo) | ★ **A.** `D:\TLCN\frontend`, repo riêng `…/placement-test-frontend` · **B.** đặt trong `D:\TLCN\backend\` (không khuyến khích: trái #34) · **C.** tên khác (ghi rõ) | A giữ ranh giới rõ & CI riêng; số liệu commit/PR rải nhiều repo (đã chấp nhận ở #34) |
| ☑ **Q-F2** | Kiểu render | ★ **A.** Next.js **App Router** + TypeScript `strict`; trang đọc dữ liệu dùng Server Component, trang thi/biểu mẫu dùng Client Component · **B.** Pages Router · **C.** Toàn bộ client-side (SPA) | A khớp SRS "SSR" và hướng chính thức của Next; C đơn giản nhất nhưng bỏ SSR và khó bảo vệ cookie/`middleware` |
| ☑ **Q-F3** | Lưu & gửi token | ★ **A.** BFF: route handler Next đặt cookie `httpOnly`, FE gọi qua proxy · **B.** `accessToken` trong bộ nhớ + refresh token cookie do **Backend** đặt (cần cấu hình CORS/cookie chéo origin) · **C.** `localStorage` | A an toàn, không phụ thuộc cấu hình cookie của BE, thêm 1 lớp proxy; B ít code FE nhưng buộc BE đổi; C đơn giản nhất nhưng XSS lấy được token (đặc biệt Admin) — **không khuyến nghị** |
| ☑ **Q-F4** | Nguồn kiểu dữ liệu API | ★ **A.** BE thêm Swagger; FE sinh kiểu bằng `openapi-typescript` (+ `zod` cho vài response trọng yếu) · **B.** FE tự viết `zod` schema tay · **C.** Copy DTO thủ công | A một nguồn sự thật nhưng cần task BE-X2; B chạy ngay không chờ BE, nhưng dễ lệch |
| ☑ **Q-F5** | Bộ UI | ★ **A.** Tailwind CSS + **shadcn/ui** (Radix) · **B.** MUI · **C.** Ant Design | A nhẹ, tùy biến, a11y tốt, nhưng tự ráp bảng/biểu mẫu; B/C có sẵn bảng/biểu mẫu nhưng nặng và "kiểu mặc định" khó khác biệt |
| ☑ **Q-F6** | Thư viện biểu đồ | ★ **A.** **Recharts** (Radar, Bar) · **B.** Chart.js · **C.** ECharts | A tích hợp React gọn, đủ Radar/Bar cho UCSV04/GV07; C mạnh hơn nhưng nặng |
| ☑ **Q-F7** | Quản lý dữ liệu từ server | ★ **A.** **TanStack Query** (client) + fetch trong Server Component cho trang đọc · **B.** SWR · **C.** Chỉ Server Actions/`fetch` | A có cache/retry/invalidate cho danh sách Item Bank; C ít thư viện nhưng tự viết retry/refetch |
| ☑ **Q-F9** | Ngôn ngữ giao diện | ★ **A.** Chỉ tiếng Việt; chuỗi gom vào `src/messages/vi.ts` để sau dễ i18n · **B.** `next-intl` có vi + en ngay · **C.** Chuỗi rải trong component | A rẻ, khớp đối tượng SV TDTU; B +1–2 ngày; C khó đổi về sau |
| ☑ **Q-F10** | Nguồn thời gian còn lại của bài thi | ★ **A.** Server trả `expiresAt` (+ `serverTime`) mỗi lần gọi; FE đếm ngược · **B.** FE tự đếm từ lúc bắt đầu | A đúng khi F5/đổi máy, cần BE-X9; B không cần BE nhưng sai khi tải lại |
| ☑ **Q-F11** | Cách tìm phiên dở dang (UCSV07) | ★ **A.** BE thêm `GET /sessions/active` · **B.** `POST /sessions` trả luôn phiên `IN_PROGRESS` nếu có (gắn **Q5** của BE) · **C.** FE lưu `sessionId` ở `localStorage` | A rõ ràng, tách tạo/tra cứu; B ít endpoint nhưng hành vi `POST` "ẩn"; C hỏng khi đổi máy/xóa dữ liệu |
| ☑ **Q-F12** | Phản hồi trong lúc thi & phạm vi Admin/AI-tag | **(a) Phản hồi từng câu:** ★ không hiển thị đúng/sai trong lúc thi (kín đến khi xong) · hiển thị ngay (kiểu luyện tập, lệch UCSV03). **(b) Phạm vi:** ★ bỏ UCADM02/03/07 và UCGV10 khỏi TL; Admin dùng chung giao diện GV · làm cả (kéo theo BE) | Bỏ giúp kịp tiến độ; làm đủ sẽ vượt khối lượng 2 người/12 tuần |
| ☑ **Q-F13** | Tiến độ bắt đầu FE | ★ **A.** Bắt đầu Tuần 5 với mock (MSW) song song BE · **B.** Chờ BE xong P4–P6 rồi mới làm (đúng lịch SRS Tuần 9–10) | A giảm rủi ro dồn việc, nhưng phải có bước đối chiếu hợp đồng; B an toàn về hợp đồng, rủi ro trễ cuối kỳ |
| ☑ **Q-F14** | Bộ test | ★ **A.** Vitest + React Testing Library + MSW (đơn vị/thành phần) + **Playwright** (E2E) · **B.** Jest + Cypress | A cùng Vitest với BE (một cách viết test), Playwright chạy được trên môi trường này; B quen thuộc nhưng thêm công cụ |

### 3.2. Nhóm II — xác nhận mặc định (nếu không phản đối thì Agent làm theo ★)

| Mã | Nội dung mặc định ★ | Phương án khác |
|---|---|---|
| ☑ Q-F8 | `react-hook-form` + `zod` cho biểu mẫu (đăng nhập, câu hỏi) | Formik |
| ☑ Q-F15 | Triển khai: `output: 'standalone'` + Dockerfile, chạy sau Nginx cùng `docker-compose` của BE (khớp SRS XI) | Vercel (ngoài stack SRS) |
| ☑ Q-F16 | Nội dung câu hỏi hiển thị **văn bản thuần**; chỗ trống `____` (quyết định #42) tô bằng CSS | Markdown có làm sạch (sanitize) |
| ☑ Q-F17 | Xuất CSV: tải qua proxy BFF (giữ cookie), tên file do BE đặt | Gọi thẳng BE |
| ☑ Q-F18 | Trình quản lý gói: `npm` (như BE); #12 coi là đã bị #34 thay thế | `pnpm` |
| ☑ Q-F19 | Responsive: trang làm bài thi **mobile-first** (SV có thể thi trên điện thoại); trang GV/Admin **desktop-first** | Chỉ desktop |
| ☑ Q-F20 | Không làm chống gian lận (F-16 là Khóa luận): không chặn copy/paste, không phát hiện chuyển tab | Có ghi nhận chuyển tab (cần BE) |
| ☑ Q-F21 | Mục tiêu a11y: WCAG 2.1 AA ở mức cơ bản (nhãn, tương phản, điều hướng bằng bàn phím, `aria-live` cho đồng hồ/lỗi); kiểm bằng axe | Không đặt mục tiêu |
| ☑ Q-F22 | Tên thương hiệu/logo: tạm dùng chữ "Adaptive Placement Test"; không dùng logo trường/EduZ khi chưa được phép | Dùng logo thật |

### 3.3. Phản hồi của bạn (đã điền ngày 2026-10-07, qua hội thoại)

```
Duyệt: ☑ hết mặc định ★ cho các mục không liệt kê bên dưới; ☑ có mục khác/bổ sung (liệt kê)
Q-F1:  A  (D:\TLCN\frontend, repo riêng)
Q-F2:  A  (App Router, mặc định)
Q-F3:  A  (BFF + cookie httpOnly)
Q-F4:  A  (Swagger ở BE + openapi-typescript)
Q-F5:  A  (Tailwind + shadcn/ui)
Q-F6:  Recharts      Q-F7: TanStack Query      Q-F9: chỉ tiếng Việt      Q-F14: Vitest+RTL+MSW+Playwright
Q-F10: A  (server trả expiresAt)
Q-F11: A  (BE thêm GET /sessions/active)
Q-F12(a): KHÁC MẶC ĐỊNH — "Cho GV có quyền lựa chọn" hiện đúng/sai từng câu; áp dụng THEO TỪNG ĐỢT THI,
          làm bằng bảng ExamRound mới (chi tiết còn mở ở Mục 3.4).
Q-F12(b): bỏ UCADM02/03/07 và UCGV10 khỏi Tiểu luận (mặc định)
Q-F13: A  (bắt đầu Tuần 5 với mock MSW)
Nhóm II (Q-F8, Q-F15…Q-F22): mặc định ★
Người phụ trách FE: (chưa điền)
```

> Ghi chú của tôi: "mặc định của đợt là kín (tắt phản hồi)" là suy luận của tôi từ SRS UCSV03, bạn chưa nói rõ. Nếu bạn muốn mặc định là hiện, báo tôi.

### 3.4. Câu hỏi còn mở — hệ quả của quyết định "Đợt thi" (ExamRound)

Quyết định Q-F12(a) đưa vào khái niệm **đợt thi** chưa có trong SRS/Class Diagram/schema. Đây là **thay đổi phạm vi và đổi schema**. Agent **không được** thiết kế chi tiết khi bạn chưa trả lời các ô dưới đây:

| Mã | Câu hỏi | Phương án (★ = khuyến nghị) | Đánh đổi |
|---|---|---|---|
| ☑ **Q-F23** (chốt A) | Trường của `ExamRound` | ★ **A.** Tối thiểu: `id, institution_id, name, created_by, opens_at, closes_at, show_item_feedback (bool, mặc định false), created_at` · **B.** A + `max_attempts`, `access_code` · **C.** Khác (ghi rõ) | A đủ cho nhu cầu (bật/tắt phản hồi + lọc báo cáo theo đợt); B thêm kiểm soát nhưng tăng UI/BE |
| ☑ **Q-F24** (chốt A) | Sinh viên vào đợt nào? | ★ **A.** Chọn từ danh sách đợt đang mở của đơn vị mình (`GET /exam-rounds/open`) · **B.** Nhập mã tham gia (cần `access_code`) · **C.** Một đợt "mặc định" của đơn vị, SV không chọn | A đơn giản, không cần mã; B chặn người ngoài đợt nhưng thêm bước; C ít UI nhất nhưng GV không tách được nhiều đợt cùng lúc |
| ☑ **Q-F25** (chốt A: có) | Phiên thi hiện có (không thuộc đợt nào) | ★ **A.** `exam_round_id` cho phép NULL = hành vi kín như hiện nay · **B.** Bắt buộc có đợt, tạo đợt "mặc định" cho dữ liệu cũ | A không phá dữ liệu cũ/seed; B sạch hơn nhưng cần migration dữ liệu |
| ☑ **Q-F26** (chốt **C**, khác ★) | Phản hồi hiển thị gồm gì khi bật | ★ **A.** Chỉ "đúng/sai" sau mỗi câu · **B.** Kèm đáp án đúng · **C.** Kèm cả giải thích AI | A lộ ít nhất; B/C lộ đáp án đúng giữa bài ⇒ SV có thể truyền đáp án cho bạn cùng thi, làm yếu tính "kín" ở SRS 15.3 |
| ☑ **Q-F27** (chốt A, mặc định ★) | Ai được tạo/sửa đợt thi? | ★ **A.** Teacher (đơn vị mình) và Admin · **B.** Chỉ Admin | A đúng tinh thần "cho GV quyền lựa chọn" |
| ☑ **Q-F28** (chốt A) | Sửa cờ phản hồi khi đợt đang có phiên `IN_PROGRESS` | ★ **A.** Cờ được **chụp lại vào phiên lúc bắt đầu** (đổi cờ không ảnh hưởng phiên đang thi) · **B.** Đọc cờ mới mỗi lần | A nhất quán trong một phiên; B có thể đổi luật giữa bài |

**Hệ quả của lựa chọn Q-F26 = C (kèm đáp án đúng + giải thích AI sau mỗi câu, khi GV bật):** đây là lựa chọn *khác* khuyến nghị của tôi, nên ghi rõ các hệ quả để bạn biết:
- **Lộ đáp án giữa bài:** SV thấy đáp án đúng ngay sau mỗi câu ⇒ có thể truyền cho bạn cùng thi. Đây là lý do mặc định của đợt phải là **tắt**, và công tắc ở FE6.12 phải có chú thích cảnh báo.
- **Quy tắc bảo mật BE (A-04) phải đổi dạng:** `GET /explanations/items/:id` không còn "chỉ sau khi hoàn thành" mà là "câu đã được **chính phiên này** trả lời **và** phiên có cờ bật". Phải làm ở BE, FE không tự quyết (xem BE-X19, BE-X10).
- **Độ trễ:** giải thích sinh *lười* bằng Gemini, lần đầu cho mỗi câu có thể chậm (NFR submit+next < 300 ms p95 là cho đường nộp, không gồm AI). Vì vậy FE4.13 hiển thị giải thích **không chặn** nút sang câu kế (skeleton, tải bất đồng bộ); nếu giải thích lỗi/chậm thì vẫn cho đi tiếp.
- **Provider Gemini hiện là stub** (kế hoạch BE, nhóm AI) ⇒ giải thích thật chỉ có khi AI gateway làm xong (đang ngoài phạm vi kế hoạch BE). Tới lúc đó FE chỉ hiển thị đáp án đúng + trạng thái "chưa có giải thích".
- Tác động User Study mạnh hơn phương án A/B (SV học ngay từ đáp án trong lúc thi).

**Rủi ro học thuật cần báo GVHD (không phải quyết định kỹ thuật):** hiển thị đúng/sai từng câu có thể làm thay đổi hành vi trả lời của SV trong CAT. Khóa luận có User Study "CAT vs Linear" (RQ1–RQ3, SRS XII); khi dùng dữ liệu từ đợt có bật phản hồi, **phải ghi cờ này** để không trộn với dữ liệu thi kín. Tôi không đánh giá được mức ảnh hưởng; cần ý kiến GVHD.

**Q-F25 và Q-F27 đã chốt (2026-10-07):** phiên cũ để `exam_round_id` NULL = thi kín; Teacher (đơn vị mình) và Admin tạo được đợt. **Toàn bộ Q-F23…Q-F28 đã chốt**; BE-X19, FE4.13, FE6.11–6.13 không còn bị chặn bởi câu hỏi mở (vẫn phụ thuộc thứ tự phase).

**Tác động lên các thành phần khác (theo các lựa chọn đã chốt + ★ cho Q-F25/27):**
- Backend: bảng mới `exam_rounds`; cột `test_sessions.exam_round_id` (NULL được) và cột chụp cờ phản hồi; `POST /sessions` nhận `examRoundId`; response `responses` trả `isCorrect` **chỉ khi** cờ của phiên bật; CRUD `exam-rounds` cho GV; `GET /exam-rounds/open` cho SV ⇒ **BE-X19** (Mục 5), **chạm schema ⇒ cần task migration riêng và `DECISIONS_LOG`**.
- Frontend: thêm FE4.13 (hiển thị phản hồi có điều kiện), FE6.11–FE6.13 (quản lý đợt thi), và FE4.1 chọn đợt.
- Báo cáo (UCGV07 "lọc theo kỳ học/nhóm") có thể lọc theo đợt: lợi ích phụ, nhưng cần BE-X6 hỗ trợ tham số `examRoundId`; chưa nằm trong phạm vi nếu bạn không yêu cầu.

---

## 4. Ánh xạ Use Case → Màn hình → API (cho Agent đọc)

| UC | Màn hình (route) | API dùng | Trạng thái API |
|---|---|---|---|
| UCSV01/GV01/ADM01 | `/login` | `POST /auth/login`, `GET /auth/me` | ✅ có (cần G-02) |
| UCSV02 | `/exam/start` (giới thiệu: 25 câu, 45 phút) | `POST /sessions` | ✅ (cần G-04) |
| UCSV03 | `/exam/[sessionId]` | `GET next-item`, `POST responses` | ✅ (cần G-04/08/09/10) |
| UCSV04 | `/results/[sessionId]` | `GET /sessions/:id/result` hoặc `GET /placement-profiles/:code` | ⏳ BE P4.11 |
| UCSV05 | `/results/[sessionId]/review` | `GET /sessions/:id/review` | ⏳ BE-X10 (mới) |
| UCSV06 | `/history` | `GET /placement-profiles/:code/history` | ⏳ BE P6.8 |
| UCSV07 | Banner ở `/` + `/exam/[sessionId]` | `GET /sessions/active`, `GET resume` | ⏳ BE-X8 (mới) |
| UCGV02 | `/teacher/items` | `GET /items` (lọc/tìm/phân trang) | ⚠️ cần G-05 |
| UCGV03/04 | `/teacher/items/new`, `/teacher/items/[id]` | `POST/GET/PUT /items` | ⏳ BE P6.1–2 |
| UCGV05 | `/teacher/items/review` | `POST approve`, `POST reject` (không có lý do — #56) | ✅ có |
| UCGV06 | nút xóa trong danh sách | `DELETE /items/:id` | ⏳ BE P6.3 |
| UCGV07 | `/teacher/reports` | `GET /reports/class-distribution`, `/error-patterns` | ⏳ BE P6.10–11 |
| UCGV08 | nút "Xuất CSV" | `GET /reports/export-csv` | ✅ (kiểm tên tham số) |
| UCGV09/ADM04 | `/teacher/students/[code]` | `GET /placement-profiles/:code` | ✅ (kiểm tra quyền cùng `institution_id`) |
| UCADM05/06 | dùng lại `/teacher/reports`, `/teacher/items` với phạm vi toàn hệ thống | như trên (+ `?institutionId=`) | ⏳ BE P6.10 |
| UCADM02/03/07, UCGV10 | **Không làm** (Q-F12b mặc định) | — | — |

**Cấu trúc thư mục đề xuất (đã gộp vào task FE1.5; không tạo trước):**
```
frontend/
  src/
    app/                      # App Router: (public)/login, (student)/..., (teacher)/..., api/proxy/[...path]
    components/ui/            # shadcn/ui
    features/{auth,exam,result,history,items,reports}/   # components + hooks + schema của từng tính năng
    lib/api/{client.ts,endpoints.ts,errors.ts,types.gen.ts}
    lib/auth/{session.ts,roles.ts}
    messages/vi.ts
    mocks/{handlers.ts,fixtures/}   # MSW
  tests/{unit,e2e}/
```

---

## 5. Yêu cầu đối với Backend (hợp đồng) — ánh xạ vào kế hoạch BE

> Các dòng "mới" **chưa có** trong 87 task của kế hoạch Backend. Khi bạn duyệt kế hoạch này, Agent sẽ **thêm vào** bảng tracking BE một phase `PX` (không sửa task cũ) — xem FE0.5. Một dòng đổi schema: BE-X19 (BE-X18 đã hủy theo #56).

| Mã | Yêu cầu | Task BE sẵn có | Ghi chú |
|---|---|---|---|
| BE-X1 | CORS allowlist theo ENV | P1 (CORS) | Cần nếu Q-F3 = B |
| BE-X2 | `@nestjs/swagger` + `openapi.json` | **mới** | Cần nếu Q-F4 = A |
| BE-X3 | `POST /auth/refresh`, `/auth/logout` | P5.6 | Hình dạng token/cookie theo Q-F3 |
| BE-X4 | `GET /sessions/:id/result` | P4.11 | |
| BE-X5 | `GET /placement-profiles/:code/history` | P6.8 | |
| BE-X6 | `GET /reports/class-distribution`, `/error-patterns` | P6.10, P6.11 | |
| BE-X7 | `GET/PUT/DELETE /items/:id` | P6.1–P6.3 | |
| BE-X8 | `GET /sessions/active` | **mới** | Q-F11 |
| BE-X9 | Siêu dữ liệu phiên: `itemCount`, `maxItems`, `expiresAt`, `serverTime` | **mới** | Q-F10 |
| BE-X10 | `GET /sessions/:id/review` | **mới** (thay `/explanations/items/:id` cho SV; liên quan P6.9) | G-07 |
| BE-X11 | Mã lỗi nghiệp vụ ổn định | **mới** (mở rộng `HttpExceptionFilter`) | G-08 |
| BE-X12 | `next-item` khi hết câu: trạng thái rõ ràng | Q10 của BE | G-09 |
| BE-X14 | `studentCode`, `fullName` trong `/auth/me` & `login.user` | **mới** | G-02 |
| BE-X16 | Submit không trả `isCorrect/theta/se`; `next-item` không trả `cefrTarget` | **mới** (đổi hợp đồng — hỏi lại nếu bạn muốn giữ) | G-10, U-05 |
| BE-X17 | `GET /items` thêm `cefr`, `source`, `q`, phân trang `{data,total}` | **mới** | G-05 |
| ~~BE-X18~~ | ~~`reject` nhận & lưu `reason`~~ — **hủy theo quyết định #56 (không ghi lý do)** | — | G-06 |
| BE-X19 | `ExamRound`: bảng `exam_rounds`, cột `test_sessions.exam_round_id` + cờ phản hồi chụp lại, CRUD cho GV, `GET /exam-rounds/open` cho SV, `POST /sessions` nhận `examRoundId`, `responses` trả `isCorrect` + đáp án đúng + giải thích **chỉ khi** cờ phiên bật | **mới** — **đổi schema (Q-F23…28 đã chốt)**; kèm đổi quy tắc truy cập giải thích (Q-F26 = C) | Q-F12(a) |

---

## 6. Phân tích: có thay đổi tính năng cốt lõi của hệ thống không?

**Kết luận: Không.**

- **Thuật toán/đặc tả không đổi:** Rasch 1PL, EAP 41 điểm, Top-5, thứ tự dừng, θ₀=−0.5… vẫn hoàn toàn ở Backend. Frontend không tính θ, không chọn câu, không quyết định dừng.
- **Frontend là lớp trình bày + thu thập** theo đúng 24 Use Case đã duyệt (trừ phần cắt ở Q-F12b: UCADM02/03/07, UCGV10).
- **Những thay đổi quan sát được (đều là hợp đồng API, không phải tính năng):**
  1. **Thay đổi sản phẩm do bạn quyết định (Q-F12(a)):** GV có thể bật phản hồi đúng/sai từng câu theo **đợt thi**. Mặc định vẫn kín như SRS UCSV03; tính năng này **mới, ngoài SRS v2.6** ⇒ ghi vào danh sách đề xuất SRS v2.7 (FE9.5) và `DECISIONS_LOG`. Nó đổi schema (BE-X19) và có rủi ro học thuật cho User Study (Mục 3.4).
  1b. Dù bật hay tắt, θ/SE và `cefrTarget` không hiện trong lúc thi (đóng chỗ rò).
  2. Thêm vài endpoint đọc (`active`, `review`) và trường siêu dữ liệu — **bổ sung**, không phá hợp đồng cũ (trừ BE-X16 đổi nội dung response của `responses`/`next-item`).
  3. Từ chối câu hỏi **không** lưu lý do (quyết định #56) — lệch UCGV05 bước 4b, không đổi schema.
- **Tác động tới NFR:** đường nộp đáp án có thêm 1 hop proxy (nếu Q-F3 = A); mục tiêu < 300 ms p95 là cho **Backend** (SRS 15.1) — tôi sẽ đo riêng và **không** ghi con số nào vào `TRACKING.md` cho tới khi đo thật.
- **Tác động tới quy trình:** thêm một repo (đã chấp nhận ở #34) ⇒ số liệu commit/PR/coverage phải gom từ 2 repo (TC2.4/2.5).

---

## 7. Phụ thuộc giữa các phase

```
FE0 (cổng: bạn duyệt Mục 3, đọc tài liệu, feature-plan, ghi DECISIONS_LOG, mở phase PX ở tracking BE)
  └─► FE1 (Scaffold & tooling)
        └─► FE2 (Hợp đồng API, client, mock)  ── đối chiếu BE ─► BE-X*
              └─► FE3 (Auth, layout, RBAC)
                    ├─► FE4 (Làm bài thi)         ┐
                    ├─► FE5 (Kết quả/Giải thích/Lịch sử) ├─ song song được
                    ├─► FE6 (Item Bank GV)        │  (khác nhau thư mục `features/*`)
                    └─► FE7 (Báo cáo/Hồ sơ/CSV)   ┘
                          └─► FE8 (Chất lượng: a11y, bảo mật, E2E, đối chiếu BE thật)
                                └─► FE9 (Docker, tài liệu, minh chứng)
```
- FE5 điều hướng từ FE4 sang `/results/[id]`: dùng route cố định, không cần FE4 xong.
- Tích hợp BE thật (FE8.1) chỉ làm khi **BE P4, P5, P6** đã ✅ ở tracking BE.

---

## 8. Kế hoạch triển khai chi tiết (cho AI Agent)

Quy ước cột: **Loại** 🤖 Agent · 👤 Người · ⛔ Cổng · `∥` song song được. **Xác minh** = lệnh/hành vi phải đúng *trước khi* đánh ✅.

### FE0 — Cổng vào (tuần tự)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE0.1 | ⛔ Bạn điền Mục 3.3 và nói "duyệt" | 👤 | Mục 3.3 có nội dung |
| FE0.2 | Kiểm trạng thái: `D:\TLCN\frontend` (hoặc đường dẫn Q-F1) có tồn tại không; `git status` nếu có; nếu thư mục đã có nội dung ⇒ **dừng hỏi** | 🤖 | Ghi kết quả vào tracking |
| FE0.3 | Đọc theo Mục 10.2; đọc lại hợp đồng BE thực tế (controller + DTO) | 🤖 | Ghi vào tracking: danh sách khác biệt với Mục 1 (nếu có) |
| FE0.4 | Tạo `0.docs/tracking/feature-plans/frontend-ui.md` từ `_template.md` (điền Mục 1–3 từ kế hoạch này); thêm dòng mới vào `DECISIONS_LOG.md` (số tiếp theo sau dòng cuối) cho các Q-F đã chốt, kèm ghi chú "#12 bị thay thế một phần bởi #34" | 🤖 | File tồn tại; mỗi Q-F nhóm I có đúng 1 dòng |
| FE0.5 | Thêm phase `PX` (BE-X1…X19, trừ X18 đã hủy) vào **cuối** `Tuan4/TRACKING_RA_SOAT_VA_HOAN_THIEN_BACKEND.md` + mục tương ứng trong kế hoạch BE (chỉ thêm, không sửa task cũ); báo bạn những BE-X cần đổi schema (X18) để bạn chốt riêng | 🤖 | Tracking BE có phase `PX`; không task cũ bị đổi |

### FE1 — Scaffold & tooling (sau FE0; `∥` nội bộ ở FE1.6–1.8)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE1.1 | Tạo repo thư mục theo Q-F1; **tạo `.gitignore` (gồm `.env*`, `.next`, `node_modules`, `coverage`, `playwright-report`) TRƯỚC mọi file khác**; không `git init`/commit giùm (nhắc bạn lệnh) | 🤖 | `.gitignore` là file đầu tiên; liệt kê file tạo ra |
| FE1.2 | `create-next-app` (App Router, TypeScript, ESLint/oxlint theo BE nếu khả thi, `src/`, import alias `@/*`); bật `strict`, `noUncheckedIndexedAccess` | 🤖 | `npm run build` xanh |
| FE1.3 | Tailwind + shadcn/ui (theo Q-F5); thêm Button, Input, Card, Table, Dialog, Toast, Tabs, Badge, Skeleton | 🤖 | Trang `/` render, không lỗi console |
| FE1.4 | Cấu hình test: Vitest + RTL + MSW; script `test`, `test:cov`; một test mẫu | 🤖 | `npm test` xanh |
| FE1.5 | Dựng cây thư mục như Mục 4; `README.md` ngắn (cách chạy, biến môi trường) | 🤖 | Cây đúng; README không chứa secret |
| FE1.6 | `∥` Kiểu env có kiểm tra khi khởi động (zod): `API_BASE_URL`, `NEXT_PUBLIC_APP_NAME`; `.env.example` (không có giá trị bí mật) | 🤖 | Thiếu biến ⇒ lỗi rõ khi `build`/`start` |
| FE1.7 | `∥` `src/messages/vi.ts` (Q-F9) + helper hiển thị `CEFRLevel`/`StoppingReason`/`ItemStatus` sang chuỗi tiếng Việt | 🤖 | Test thuần cho map enum (không enum nào thiếu) |
| FE1.8 | `∥` Prettier/format, `typecheck` script, `lint` script; hook không bắt buộc | 🤖 | `npm run lint`, `npm run typecheck` xanh |
| FE1.9 | Playwright cài & cấu hình cơ bản (`playwright.config.ts`, 1 test khởi động trang) | 🤖 | `npx playwright test` xanh |

### FE2 — Hợp đồng API & lớp truy cập dữ liệu (sau FE1)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE2.1 | Xác minh hợp đồng BE **bằng gọi thật** nếu BE chạy được (login → start → next-item → responses → resume); nếu không chạy được ⇒ ghi "chưa xác minh" và dựa vào mã | 🤖 | Ghi JSON thật vào tracking (cắt gọn, không chứa token) |
| FE2.2 | `lib/api/endpoints.ts` (một nơi duy nhất liệt kê route) + `lib/api/client.ts` (fetch wrapper: timeout, `AbortController`, parse lỗi) | 🤖 | Test: lỗi 4xx/5xx/timeout ánh xạ đúng |
| FE2.3 | Sinh kiểu: Q-F4=A ⇒ script `npm run gen:api` từ `openapi.json` (nếu BE chưa có thì dùng kiểu viết tay trong `types.manual.ts` và ghi TODO); Q-F4=B ⇒ `zod` schema | 🤖 | `typecheck` xanh |
| FE2.4 | `lib/api/errors.ts`: `ApiError { status, code?, message }`; map `code` (BE-X11) → hành vi; trước khi BE có `code` ⇒ ánh xạ theo `statusCode` | 🤖 | Test các nhánh |
| FE2.5 | Discriminated union cho `next-item`: `{kind:'item'} \| {kind:'finished'} \| {kind:'error'}`; adapter chịu được dạng `{message}` hiện tại (G-09) | 🤖 | Test với cả hai dạng response |
| FE2.6 | MSW `mocks/handlers.ts` + fixtures **đúng Mục 4** (kịch bản: thi trơn, dừng sớm, hết thời gian, 409, mất mạng, hết quyền) | 🤖 | Gắn nhãn "mock — không phải dữ liệu thật" trong fixture |
| FE2.7 | Hooks TanStack Query cho từng tài nguyên (Q-F7), khóa cache thống nhất | 🤖 | Test hook với MSW |
| FE2.8 | Bảng "đối chiếu hợp đồng" trong tracking: mỗi endpoint — mock có / BE thật có / khớp? | 🤖 | Bảng đủ dòng Mục 4 |

### FE3 — Auth, layout, RBAC (sau FE2)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE3.1 | Trang `/login` (react-hook-form + zod; thông báo lỗi tiếng Việt; không tiết lộ email có tồn tại hay không) | 🤖 | Test: sai mật khẩu, thiếu trường |
| FE3.2 | Route handler `api/proxy/[...path]` (Q-F3=A): chuyển tiếp, gắn `Authorization` từ cookie, **không** chuyển tiếp header nhạy cảm thừa, giới hạn path cho phép | 🤖 | Test: path ngoài allowlist bị 404/403 |
| FE3.3 | Đăng nhập → đặt cookie `httpOnly; Secure(prod); SameSite=Lax`; đăng xuất xóa cookie; (khi BE-X3 xong) làm mới token khi 401 một lần rồi mới đẩy về `/login` | 🤖 | Test; kiểm tay: `document.cookie` không thấy token |
| FE3.4 | `lib/auth/session.ts`: đọc người dùng hiện tại ở server (`/auth/me`), kiểu `CurrentUser {id, role, institutionId, studentCode?, fullName}` | 🤖 | Test; lệch G-02 ⇒ ghi vào tracking |
| FE3.5 | Layout theo vai trò: `(student)`, `(teacher)` (Admin dùng chung), thanh điều hướng, trang 403/404/lỗi chung | 🤖 | Render theo 3 vai trò |
| FE3.6 | `middleware.ts`: chuyển hướng theo vai trò; ghi chú rõ trong README "không phải lớp bảo mật" (S-04) | 🤖 | Test: SV vào `/teacher/*` bị chuyển hướng |
| FE3.7 | Trang chủ SV (`/`): nút "Bắt đầu bài thi", banner phiên dở dang (nối FE4.9), liên kết lịch sử | 🤖 | Test với mock |
| FE3.8 | Trang chủ GV: lối vào Item Bank, Duyệt, Báo cáo | 🤖 | Test |
| FE3.9 | Toast/Error boundary toàn cục, trang `error.tsx`/`not-found.tsx` | 🤖 | Test |

### FE4 — Làm bài thi (UCSV02, 03, 07) (`∥ FE5, FE6, FE7`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE4.1 | `/exam/start`: quy tắc bài thi, 25 câu tối đa, 45 phút (đọc từ cấu hình/BE, không hardcode — C-07 phía BE), nút xác nhận; **(sau Q-F24)** chọn đợt thi đang mở | 🤖 | Test hiển thị đúng số từ mock |
| FE4.2 | Gọi `POST /sessions` ⇒ chuyển `/exam/[sessionId]`; xử lý lỗi (403 sai vai trò, đã có phiên dở) | 🤖 | Test |
| FE4.3 | Thành phần `QuestionCard`: nội dung văn bản thuần, 4 lựa chọn A–D (radio, truy cập bàn phím), chỗ trống `____`; **không** hiển thị `cefrTarget`/đúng-sai | 🤖 | Test; kiểu `ExamItem` không có trường đáp án |
| FE4.4 | Khởi tạo trang thi bằng `next-item` (idempotent, U-03); xử lý `finished` ⇒ `/results/[id]` | 🤖 | Test: F5 giữa câu vẫn cùng câu |
| FE4.5 | Nộp đáp án: khóa nút, `responseTimeMs` đo bằng `performance.now()`, xử lý 409 ⇒ refetch im lặng, `shouldStop` ⇒ sang kết quả; bỏ qua `isCorrect/theta/se` | 🤖 | Test: double-click gửi 1 request; 409 không hiện lỗi |
| FE4.6 | Đồng hồ đếm ngược theo `expiresAt` (Q-F10), cảnh báo còn 5 phút (`aria-live`), hết giờ ⇒ báo server | 🤖 | Test với fake timers |
| FE4.7 | Mất mạng: banner, GET retry có backoff, POST không tự retry; nút "Thử lại" thủ công | 🤖 | Test với MSW (network error) |
| FE4.8 | Thanh tiến độ "Câu n" (không hiển thị "n/25 chắc chắn" vì có thể dừng sớm — chỉ "tối đa 25") | 🤖 | Test |
| FE4.9 | UCSV07: gọi `GET /sessions/active` ở trang chủ; nút "Tiếp tục bài thi" ⇒ `resume` ⇒ vào `/exam/[id]` | 🤖 | Test (cần BE-X8; trước đó dùng mock) |
| FE4.10 | Chặn rời trang vô ý (`beforeunload` chỉ cảnh báo, không chặn cứng); không có nút "Quay lại câu trước" | 🤖 | Test |
| FE4.11 | Responsive mobile-first cho toàn bộ luồng thi (Q-F19), kiểm ở 360 px và 1280 px | 🤖 | Ảnh chụp Playwright 2 kích thước (lưu vào `tests/e2e/__screens__`, không commit nếu lớn) |
| FE4.12 | Test chặn hồi quy rò đáp án: mọi response mock của `next-item` không chứa khóa `correct*`; (khi BE thật) cùng kiểm với BE | 🤖 | Test đỏ-xanh |
| FE4.13 | **(Q-F23…28 đã chốt)** Phản hồi từng câu có điều kiện: chỉ khi phiên có cờ bật hiện "đúng/sai" + đáp án đúng + giải thích AI (Q-F26 = C); giải thích tải bất đồng bộ, không chặn nút sang câu kế; tắt ⇒ DOM không có đúng/sai, đáp án, giải thích; không bao giờ hiện θ/SE | 🤖 | Test hai chế độ; test giải thích chậm/lỗi vẫn đi tiếp được |

### FE5 — Kết quả, giải thích, lịch sử (UCSV04–06) (`∥ FE4, FE6, FE7`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE5.1 | `/results/[sessionId]`: CEFR tổng thể, θ, SE, khoảng tin cậy 95% (định dạng số thống nhất, làm tròn 2 chữ số) | 🤖 | Test với fixture |
| FE5.2 | Radar chart kỹ năng (Recharts; fallback bảng cho trình đọc màn hình); xử lý trường hợp `skillProfiles` rỗng (BE C-10 chưa xong) bằng trạng thái "đang cập nhật", **không bịa số** | 🤖 | Test: rỗng/đủ |
| FE5.3 | Khối Error Patterns (chủ đề yếu, độ chính xác, mức nghiêm trọng) | 🤖 | Test |
| FE5.4 | Khối gợi ý cải thiện (`aiRecommendations`) + cảnh báo `boundary_effect` / độ tin cậy `cefr_confidence` (chuỗi theo SRS 4.5) | 🤖 | Test: có/không `boundary_effect` |
| FE5.5 | `/results/[sessionId]/review`: danh sách câu đã làm (đúng/sai), xem chi tiết: câu hỏi, đáp án đã chọn, đáp án đúng, giải thích; chuyển câu | 🤖 | Test (cần BE-X10; trước đó mock) |
| FE5.6 | Xử lý giải thích chưa sẵn sàng (sinh lười — lần đầu có thể chậm): skeleton + thông báo, không chặn danh sách | 🤖 | Test |
| FE5.7 | `/history`: bảng phiên đã hoàn thành (ngày, số câu, CEFR, θ, SE) + mở lại kết quả (UCSV06 bước 4) | 🤖 | Test |
| FE5.8 | Trạng thái rỗng/lỗi/đang tải cho cả 3 trang | 🤖 | Test |
| FE5.9 | In kết quả / xuất PDF: **ngoài phạm vi** (ghi Mục 11) | 🤖 | — (không làm) |

### FE6 — Item Bank cho Giảng viên (UCGV02–06) (`∥ FE4, FE5, FE7`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE6.1 | `/teacher/items`: bảng, phân trang phía server, trạng thái chip (DRAFT/PENDING_REVIEW/APPROVED/REJECTED) | 🤖 | Test |
| FE6.2 | Bộ lọc kỹ năng, CEFR, trạng thái, nguồn + ô tìm kiếm (debounce); lưu bộ lọc ở URL | 🤖 | Test; (cần BE-X17, trước đó lọc phía mock) |
| FE6.3 | Biểu mẫu tạo câu (UCGV03): nội dung, 4 đáp án, đáp án đúng, kỹ năng, CEFR, `topic_tag`, `irt_b`; kiểm tra khoảng `irt_b` theo biên Item Bank lấy từ cấu hình (không hardcode) | 🤖 | Test các ràng buộc |
| FE6.4 | Hai nút "Lưu nháp" / "Lưu và gửi duyệt" | 🤖 | Test |
| FE6.5 | Sửa câu (UCGV04): nạp dữ liệu, cảnh báo "câu đã duyệt sẽ quay về Chờ duyệt" (theo Q6 của BE đã chốt) | 🤖 | Test (cần BE P6.2) |
| FE6.6 | Hàng đợi Duyệt (UCGV05): xem nội dung, nút Phê duyệt, nút Từ chối (chỉ hộp xác nhận, **không** nhập lý do — #56) rồi tự chuyển câu kế | 🤖 | Test |
| FE6.7 | ~~Gửi `reason` khi từ chối~~ — **bỏ theo #56**; thay bằng: chặn duyệt/từ chối câu sai trạng thái (hiển thị lỗi 409 từ máy trạng thái BE) | 🤖 | Test |
| FE6.8 | Xóa (UCGV06): chỉ cho `DRAFT/REJECTED`; hộp thoại xác nhận; xử lý 409 nếu BE từ chối | 🤖 | Test |
| FE6.9 | Hiển thị `irt_b` có/không `calibrated`; câu `APPROVED` có cảnh báo khi sửa | 🤖 | Test |
| FE6.10 | Phân quyền hiển thị: Teacher chỉ thấy nội dung hợp lệ theo BE; Admin xem toàn bộ | 🤖 | Test theo vai trò |
| FE6.11 | **(Q-F23…28 đã chốt)** `/teacher/exam-rounds`: danh sách đợt thi (tên, thời gian mở/đóng, cờ phản hồi) | 🤖 | Test với mock |
| FE6.12 | **(Q-F23…28 đã chốt)** Biểu mẫu tạo/sửa đợt thi, công tắc "Hiện đúng/sai từng câu" (mặc định tắt, chú thích rủi ro lộ đáp án); cảnh báo khi đợt đang có phiên đang thi (Q-F28) | 🤖 | Test |
| FE6.13 | **(Q-F23…28 đã chốt)** Xóa/đóng đợt thi; xử lý khi đợt đã có phiên (409) | 🤖 | Test |

### FE7 — Báo cáo, hồ sơ, CSV (UCGV07–09, ADM04–06) (`∥ FE4, FE5, FE6`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE7.1 | `/teacher/reports`: biểu đồ cột phân phối CEFR (A1–B2) | 🤖 | Test |
| FE7.2 | Bảng Error Patterns toàn lớp (chủ đề hay sai, tỷ lệ lỗi) | 🤖 | Test (cần BE P6.11; trước đó trạng thái rỗng) |
| FE7.3 | Bộ lọc theo kỳ học/nhóm: **chỉ làm phần mà BE hỗ trợ**; phần chưa có ⇒ ghi Mục 11, không giả lập | 🤖 | Ghi rõ trong tracking |
| FE7.4 | Nút "Xuất CSV" (UCGV08): hộp thoại loại xuất + phạm vi, tải file qua proxy, thông báo lỗi nếu rỗng | 🤖 | Test; kiểm tay: file mở được bằng Excel (UTF-8 BOM nếu BE gửi) |
| FE7.5 | `/teacher/students/[code]`: hồ sơ SV (UCGV09/ADM04), dùng lại các khối của FE5 | 🤖 | Test: 403 khi khác `institution_id` hiển thị trang 403 |
| FE7.6 | Chọn đơn vị cho Admin (`?institutionId=`), mặc định "tất cả" | 🤖 | Test (cần BE P6.10) |
| FE7.7 | Tìm sinh viên theo MSSV (nhập mã → mở hồ sơ) | 🤖 | Test |
| FE7.8 | Trạng thái rỗng/lỗi/đang tải | 🤖 | Test |

### FE8 — Chất lượng (sau FE4–FE7)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE8.1 | **Đối chiếu BE thật** (khi BE P4/P5/P6 ✅): chạy lại FE2.1; cập nhật bảng FE2.8; sửa chỗ lệch; chuyển E2E sang BE thật | 🤖 | Bảng không còn dòng "lệch" chưa xử lý |
| FE8.2 | E2E Playwright: SV đăng nhập → thi đến khi dừng → kết quả → giải thích → lịch sử | 🤖 | Xanh trên mock; xanh trên BE thật (nếu có) |
| FE8.3 | E2E: F5 giữa câu, đóng tab rồi "Tiếp tục", hết giờ, mất mạng | 🤖 | Xanh |
| FE8.4 | Header bảo mật (CSP, nosniff, referrer), rà `NEXT_PUBLIC_*`, `npm audit` (ghi kết quả thật) | 🤖 | Báo cáo lệnh + kết quả |
| FE8.5 | a11y: axe (qua Playwright) trên 6 trang chính + kiểm bàn phím trang thi (Q-F21) | 🤖 | Số lỗi nghiêm trọng = 0 hoặc liệt kê |
| FE8.6 | Hiệu năng: Lighthouse ở trang thi/kết quả (ghi số thật, gắn môi trường đo; **không** ghi vào TRACKING.md nếu chưa đo ổn định) | 🤖 | Kết quả đính kèm |
| FE8.7 | Độ phủ test: `npm run test:cov`; ghi số thật hoặc "N/A" | 🤖 | Số có nguồn |
| FE8.8 | Rà "mọi chuỗi nhìn thấy được" tiếng Việt, không rò thông báo kỹ thuật/stack ra người dùng | 🤖 | Danh sách đã rà |

### FE9 — Đóng gói & khép sổ (bắt buộc theo `rubric-tracker`)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| FE9.1 | Ghi `AI_USAGE_LOG.md` **sau mỗi phiên** (không dồn cuối): ngày, thành viên (hỏi), phạm vi, phần AI sinh, phần người phải kiểm | 🤖 | Có dòng mới |
| FE9.2 | `weekly-log/Tuan-XX.md`: tạo/cập nhật mục "Thay đổi thiết kế & lý do" (TC2.1) | 🤖 | File cập nhật |
| FE9.3 | Dockerfile (`standalone`), thêm service vào `docker-compose` (nếu repo `docs`/BE giữ compose ⇒ **chỉ đề xuất đoạn cấu hình**, không sửa repo khác) | 🤖 | `docker build` chạy được (nếu có Docker); nếu không ⇒ ghi "chưa kiểm" |
| FE9.4 | Tài liệu: sơ đồ màn hình, bảng UC→route→API (Mục 4) cập nhật thực tế; hướng dẫn demo | 🤖 | Khớp mã |
| FE9.5 | Danh sách đề xuất **cập nhật SRS v2.7** (API `active`, `review`, siêu dữ liệu phiên…) — không sửa `.docx` | 🤖 | Danh sách có |
| FE9.6 | "Phạm vi bị cắt & lý do" (UCADM02/03/07, UCGV10, PDF…) cho báo cáo/demo | 🤖 | Danh sách có |
| FE9.7 | Cập nhật `TRACKING.md` chỉ bằng số **đo thật** hoặc N/A; nhắc bạn chạy `git add/commit` theo `GIT_CONVENTIONS.md` | 🤖 | Không có số bịa |

**Tổng sau #59 (cắt ExamRound): 85 task** (FE5.9 là "ghi nhận không làm"; FE4.13, FE6.11–6.13 đã hủy). Ghi chú 2026-10-10: Next.js 16 dùng `proxy.ts` thay cho `middleware.ts` (FE3.6).

---

## 9. Ước lượng khối lượng

> Ước lượng thô để PM cân đối, **không phải cam kết** (chưa biết tốc độ thực tế của nhóm). Đơn vị: ngày-người.

| Phase | Ước lượng | Ghi chú |
|---|---|---|
| FE0–FE1 | 1,5–2 | gồm quyết định & scaffold |
| FE2 | 2–3 | mock là phần tốn nhất |
| FE3 | 2–3 | BFF + RBAC |
| FE4 | 4–5,5 | phần quan trọng & khó nhất (+0,5 cho FE4.13) |
| FE5 | 3–4 | biểu đồ + review |
| FE6 | 5,5–7 | biểu mẫu + hàng đợi duyệt (+1,5–2 cho quản lý đợt thi) |
| FE7 | 2–3 | |
| FE8 | 3–4 | tùy BE sẵn sàng |
| FE9 | 1–2 | |
| **Tổng** | **~24–34** | ≈ 2 người × 2–3 tuần nếu song song được FE4–FE7 |

**Mức ưu tiên tối thiểu (nếu thiếu thời gian):** FE0–FE4 + FE5.1–5.4 + FE8.2 ⇒ SV thi được và xem kết quả (F-08). Sau đó FE6 (F-02 cần cho GV nhập đề), rồi FE7 (F-09).

---

## 10. Hướng dẫn dành cho AI Agent thực thi kế hoạch này

### 10.1. Quy tắc bất biến
1. Kế hoạch được duyệt khi Mục 3.3 có phản hồi. Làm đúng nội dung đã duyệt; **không "cải tiến"** thêm, không thêm thư viện ngoài danh sách đã chốt.
2. **Chỉ tạo/sửa file được liệt kê trong task** (trừ file test và file mà task nêu rõ). Không tạo tài liệu thừa.
3. **Frontend không tính toán nghiệp vụ CAT** (EAP, chọn câu, ngưỡng dừng, ánh xạ CEFR). Nếu thấy mình viết công thức θ/SE/CEFR ở FE ⇒ dừng, đó là sai lớp.
4. **Không bao giờ** đặt token ở `localStorage`/`sessionStorage`/biến toàn cục (nếu Q-F3 = A/B). Không `dangerouslySetInnerHTML` với nội dung do người dùng nhập.
5. Không hardcode: số câu tối đa, thời gian, biên `irt_b`, ngưỡng độ tin cậy, URL API ⇒ lấy từ cấu hình/BE/ENV.
6. Ngôn ngữ: giao diện & tài liệu/tracking **tiếng Việt**; định danh code, tên file, UML **tiếng Anh**.
7. Không bịa số liệu (coverage, Lighthouse, thời gian phản hồi, KPI). Chưa đo ⇒ "N/A". Dữ liệu mock phải gắn nhãn mock.
8. Không tự `git init`/commit/push/tạo PR (bộ nhớ dự án: chỉ đưa lệnh cho bạn chạy); không ký `COMMITMENT_BASELINE.md`; không sửa `.docx` SRS.
9. Không sửa mã Backend từ kế hoạch này. Chỗ cần Backend ⇒ ghi vào phase `PX` của tracking BE (FE0.5) và dùng mock.
10. Test đi kèm mỗi task ghi "Test"; chứng minh test đỏ trước (với lỗi đã biết) rồi mới sửa.
11. Sau **mỗi** phiên có AI sinh/sửa: ghi `AI_USAGE_LOG.md` (FE9.1).
12. Quy tắc `rubric-tracker`: trước khi code một F-ID/UC không tầm thường ⇒ đã có `feature-plans/frontend-ui.md` (FE0.4).

### 10.2. Thứ tự đọc bắt buộc (FE0.3)
`CLAUDE.md` → `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md` → **kế hoạch này** → `DECISIONS_LOG.md` (#12, #34, #42 và các dòng liên quan) → kế hoạch Backend (Mục 3, 8: P4–P6) → SRS v2.6 (Mục IX, X, XV) → đặc tả Use Case (UCSV/UCGV).

### 10.3. Điều kiện phải DỪNG và hỏi qua `AskUserQuestion` (≥ 2 phương án + trade-off)
- Bất kỳ Q-F nhóm I còn trống mà task cần.
- Thư mục đích đã có nội dung (FE0.2).
- Hợp đồng BE thật khác hợp đồng trong kế hoạch này theo cách đổi hình dạng dữ liệu (FE2.1, FE8.1).
- Cần thêm thư viện ngoài danh sách đã chốt, hoặc đổi phiên bản chính (major) của Next/React.
- Muốn thêm màn hình/chức năng không có trong Mục 4.
- Chỗ BE-X19 (đổi schema) hay bất kỳ yêu cầu BE làm đổi hành vi cốt lõi. **BE-X19 đổi schema: vẫn phải có task migration riêng và dòng `DECISIONS_LOG` trước khi code.**
- Phát hiện lỗi 🔴 mới ở BE khi tích hợp ⇒ **báo ngay**, thêm tracking "Phát hiện mới", không tự sửa BE.
- **Bất kỳ** lựa chọn ảnh hưởng khả năng mở rộng/bảo trì mà SRS/Class Diagram/kế hoạch này không quy định.

### 10.4. Cách cập nhật file theo dõi (sau **mỗi** task hoàn thành)
Mở `Tuan4/TRACKING_TRIEN_KHAI_FRONTEND.md` và:
1. Ô trạng thái: ⬜ → 🔄 khi bắt đầu → ✅ **chỉ khi đã chạy xong bước Xác minh**, hoặc 🚫 kèm câu hỏi dừng.
2. Cột "Bằng chứng": lệnh + kết quả tóm tắt + đường dẫn file tạo/sửa. Không dán log dài, **không dán token/secret**.
3. Tính lại % của phase và bảng tổng quan (= số ✅ / tổng task).
4. **Thêm một dòng** vào "Nhật ký cập nhật" cuối file (append-only).
5. Bị chặn ⇒ đặt 🚫, **không** chuyển sang task phụ thuộc.
6. Task song song (FE4–FE7) chỉ cập nhật đúng **hàng của mình**. File dễ xung đột: `package.json`, `package-lock.json`, `src/messages/vi.ts`, `src/mocks/handlers.ts`, `src/lib/api/endpoints.ts`, `src/app/layout.tsx` — chỉ **một** nhánh sửa tại một thời điểm.
7. Task mô tả sai thực tế (đường dẫn, tên endpoint…) ⇒ sửa cột "Ghi chú" ngay, không âm thầm làm khác.

### 10.5. Định nghĩa "xong" (DoD) cho cả kế hoạch
- [ ] 24 UC: mỗi UC trong phạm vi có màn hình + test; UC bị cắt có ghi lý do (FE9.6).
- [ ] `npm run build`, `lint`, `typecheck`, `test` xanh; E2E luồng chính xanh (mock; và BE thật nếu BE đã sẵn sàng).
- [ ] Không còn token trong `localStorage`/`sessionStorage`; không `dangerouslySetInnerHTML`; không khóa đáp án đúng trong kiểu dữ liệu của câu hỏi lúc thi.
- [ ] Bảng đối chiếu hợp đồng (FE2.8) không còn dòng "lệch" chưa xử lý.
- [ ] `DECISIONS_LOG.md`, `AI_USAGE_LOG.md`, `weekly-log`, `feature-plans/frontend-ui.md` đã cập nhật; có danh sách đề xuất SRS v2.7.
- [ ] `TRACKING.md` chỉ chứa số đo thật hoặc N/A.

### 10.6. Lệnh tham chiếu nhanh (PowerShell, trong thư mục repo FE)
```powershell
npm run dev ; npm run build ; npm run lint ; npm run typecheck
npm test ; npm run test:cov
npx playwright test ; npx playwright test --ui
npm run gen:api            # sinh kiểu từ openapi.json (khi Q-F4 = A và BE đã có)
npm audit
```
> Tên script là *dự kiến*, Agent kiểm `package.json` thực tế ở FE1 và cập nhật Mục này nếu khác. Phiên bản Next/React/Tailwind/shadcn đổi cú pháp nhanh — Agent đối chiếu tài liệu chính thức (context7) trước khi dùng cú pháp từ trí nhớ.

---

## 11. Rủi ro & câu hỏi mở (Agent **không** tự trả lời)

- **Ai làm FE?** Chưa phân công (P-05). Cột "Người" trong tracking để bạn điền.
- **SSO Google/Microsoft** (SRS mô tả Adapter Pattern): ngoài phạm vi kế hoạch BE ⇒ FE chỉ có đăng nhập email/mật khẩu.
- **Bộ lọc theo "kỳ học/nhóm sinh viên"** (UCGV07 bước 5): schema hiện không có khái niệm lớp/kỳ; chưa biết BE sẽ hỗ trợ không ⇒ FE7.3 chỉ làm phần BE có.
- **Xuất PDF/in kết quả:** chưa có trong UC ⇒ không làm.
- **CI cho repo FE:** chưa quyết (BE cũng chưa có); TC2.4/2.5 sẽ cần số liệu từ CI hoặc lệnh chạy tay có ghi lại.
- **Màn hình quản trị người dùng/cấu hình** (UCADM02/03/07): xem Q-F12(b).
- **Gauss–Hermite vs lưới đều** (rủi ro đã nêu ở kế hoạch BE) không ảnh hưởng FE, nhưng nếu kết quả θ thay đổi sau khi sửa BE thì **ảnh chụp/số liệu demo** cũ không dùng được.
- **Nội dung CLOTH có giấy phép chưa rõ** (#26) và repo **public** ⇒ fixture/mock **không** được chứa câu hỏi thật từ CLOTH; dùng câu tự soạn hoặc câu giả rõ ràng.
- **Hiển thị `cefr_confidence`:** SRS 4.5 mô tả cảnh báo biên nhưng chưa cho chuỗi hiển thị cụ thể ⇒ chuỗi tiếng Việt do tôi soạn ở FE5.4 là *đề xuất*, bạn/GVHD cần duyệt.
