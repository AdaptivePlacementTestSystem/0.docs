# Kế hoạch: Rà soát backend scaffold → sửa lỗi, đồng bộ SRS/Class Diagram, hoàn thiện để code thật

> **Phạm vi đọc:** `D:\TLCN\backend\backend` (NestJS 12 + Prisma 6.4.1 + Redis; ~80 file `.ts`, `prisma/schema.prisma`, `custom_migrations.sql`, `seed.ts`) — đối chiếu với `SRS_TLCN_v2.6_Final.docx`, `Mo_ta_So_do_Lop_ClassDiagram.md`, `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx`, `DECISIONS_LOG.md` (#1–#47), kế hoạch Tuần 3.
> **Ngày lập:** 2026-10-07 (Tuần 4/12). **Vai trò người lập:** Senior Engineer + PM.
> **Trạng thái:** ⏳ **CHỜ BẠN CHỐT Mục 3** (các ô `☐`). Chưa có dòng code nào được sửa. File theo dõi đi kèm: [`TRACKING_RA_SOAT_VA_HOAN_THIEN_BACKEND.md`](./TRACKING_RA_SOAT_VA_HOAN_THIEN_BACKEND.md).
>
> **Cập nhật 2026-10-08 (quyết định #58–#61, xem `DECISIONS_LOG.md`):** (1) **#58 (Q5 = C):** `POST /sessions` trả **409** kèm `sessionId` khi đã có phiên `IN_PROGRESS` (thay mặc định A bên dưới); P4.10 và P7.7 làm theo hướng này. (2) **#59 cắt ExamRound:** **hủy PX.16, PX.17 (BE-X19)**; PX.14 chỉ cần ẩn hẳn `isCorrect/thetaAfter/seAfter/cefrTarget` trong lúc thi (không cờ); PX.10 (`review`, chỉ phiên `COMPLETED` của chính mình) là đường duy nhất lộ đáp án + giải thích; sửa tham chiếu 'PX.16' ở PX.10/PX.14 thành 'không áp dụng'. Quy tắc A-04 giữ nguyên dạng ban đầu (không có ngoại lệ trong lúc thi). (3) **#60:** giải thích do AI sinh lúc sinh câu hỏi và được GV duyệt (hướng `Tuan2/Phuong_an_sua_doi_AI.md`); P6.9/AI-01/Q-G1 cần viết lại (chưa chốt cơ chế). (4) **#61:** tập tối thiểu đến Tuần 6 bổ sung PX.8, PX.9, PX.10, PX.13, PX.14, P4.11. Số task, Mục 6 và DoD bên dưới **chưa được viết lại**; đọc kèm ghi chú này.
>
> **Cách hiểu "Lược đồ trên"** trong yêu cầu: tôi hiểu là **toàn bộ thiết kế backend bạn chuẩn bị** — lược đồ CSDL (`schema.prisma`), kiến trúc module và các luồng chạy được dựng từ Class Diagram. Nếu bạn chỉ muốn rà riêng Class Diagram thì Mục 2.F (Schema) và Mục 5 là phần liên quan; phần còn lại vẫn cần vì nó là lý do kế hoạch tồn tại.

---

## 0. Tóm tắt điều hành

**Kết luận một câu:** scaffold có bộ khung tốt (Clean Architecture 4 tầng, Repository cho Item/User, Policy thuần cho RBAC, cấu hình CAT qua ENV, schema Prisma khớp quyết định #15–#33), nhưng **chưa thể coi là "đã xong" như `TRACKING_BACKEND_SCAFFOLD.md` ghi (100%)**: build/lint xanh chỉ chứng minh code *biên dịch được*, không chứng minh *chạy đúng*. Có **10 phát hiện mức Nghiêm trọng** (5 lỗi đáng sợ nhất ở dưới) có thể làm hỏng kết quả đo hoặc lộ đề, và **0 test**.

| Nhóm | Số phát hiện | 🔴 Nghiêm trọng | 🟠 Cao | 🟡 Vừa | 🟢 Thấp |
|---|---|---|---|---|---|
| A. Bảo mật & xác thực | 11 | 5 | 4 | 2 | 0 |
| B. Đúng đắn của CAT / phiên thi | 11 | 4 | 5 | 2 | 0 |
| C. Kiến trúc & OOP | 9 | 0 | 4 | 5 | 0 |
| D. Hợp đồng API so với SRS | 6 | 0 | 5 | 1 | 0 |
| E. Chất lượng & quy trình (TC2.4/2.5) | 6 | 1 | 1 | 3 | 1 |
| F. Lược đồ CSDL | 9 | 0 | 1 | 5 | 3 |
| G. AI | 3 | 0 | 1 | 0 | 2 |
| **Tổng** | **55** | **10** | **21** | **18** | **6** |

**Năm lỗi đáng sợ nhất (đọc trước):**
1. **B-01 — Đăng nhập chấp nhận mọi mật khẩu.** `login.use-case.ts:20`: `dto.password === user.passwordHash || user.passwordHash.length > 0` — luôn đúng khi có hash. Ai biết email là vào được (kể cả ADMIN).
2. **C-01 — EAP tính sai.** `submit-response.use-case.ts:1108`: mọi câu trước đó được gán `irtB: 0`; chỉ câu hiện tại dùng `irtB` thật. θ, SE, điều kiện dừng đều sai từ câu thứ 2 trở đi → toàn bộ giá trị đo của đồ án (KPI "số câu trung bình", "SE cuối bài") vô nghĩa.
3. **A-03 — Không kiểm quyền sở hữu phiên thi** (IDOR): bất kỳ người đăng nhập nào gọi `/sessions/:id/next-item|responses|resume` bằng id của người khác đều được; `POST /sessions` không kiểm role (giáo viên cũng tạo phiên).
4. **A-04 — `GET /explanations/items/:itemId` mở cho mọi user đã đăng nhập, không cần làm bài**: trả đáp án đúng *trước khi nộp* → vi phạm SRS 15.3 "Item protection" và vô hiệu hóa cơ chế chống lộ đề; còn cho phép bất kỳ ai kích hoạt gọi Gemini (tốn tiền).
5. **C-02 — Nộp đáp án cho `itemId` tùy ý** khi state là `READY_FOR_NEXT` hoặc Redis mất: SV có thể tự chọn câu dễ để trả lời, phá tính thích ứng. Kèm **C-10**: hồ sơ năng lực sinh ra chỉ có θ/SE — `skillProfiles`, `errorPatterns`, `aiRecommendations` đều rỗng, `testMetadata` thiếu trường SRS Mục VII → **F-06 chưa đạt**.

**Có thay đổi tính năng cốt lõi không?** **Không đổi đặc tả** (Rasch 1PL, EAP 41 điểm, Top-5, 4 điều kiện dừng giữ nguyên). Kế hoạch **đưa code về đúng đặc tả đã duyệt**; chi tiết và 3 chỗ hành vi quan sát được sẽ khác ở Mục 6.

---

## 1. Kiểm chứng nguồn (bằng chứng, không suy đoán)

| # | Điều đã kiểm | Kết quả |
|---|---|---|
| V1 | `Glob/ls` thư mục `backend` | Chỉ có `backend/backend/` (thư mục lồng nhau). **Không có `.gitignore`**, không có `.git`, **không có thư mục `prisma/migrations`**; có `.env` thật, `dist/`, `tsconfig.build.tsbuildinfo`. `TRACKING_BACKEND_SCAFFOLD.md` ghi "đã cấu hình `.gitignore`" → **không khớp thực tế** |
| V2 | Số file test | **0** file `*.spec.ts`. `test/app.e2e-spec.ts` là mẫu mặc định (`GET /` → "Hello World!") — không có route đó, sẽ đỏ nếu chạy. `vitest.config.ts` chỉ `include: **/*.spec.ts` |
| V3 | `tsconfig.json` | `strict: false` (chỉ `strictNullChecks`). Đếm `as any`/`: any` trong `src/` ≈ **40**. `oxlint` báo 0 lỗi vì không bắt các trường hợp này |
| V4 | Thư viện băm mật khẩu | **Không có** (`bcrypt`/`argon2` đều không có trong `package.json`); `zod` được cài nhưng **không file nào import** |
| V5 | SRS Mục 4.5 | Outlier Early Stop = θ ngoài [-2.5, 1.5] **VÀ** ΔSE<0.01 trong 3 câu **VÀ** ≥8 câu (pseudocode `dSE1`, `dSE2`). Code chỉ kiểm θ + ≥8 câu |
| V6 | SRS 4.5/Class Diagram VI.f (thứ tự ưu tiên) | SE → Boundary → 25 câu → Timeout. **Code khớp SRS**; **`CLAUDE.md` ghi sai thứ tự** (SE → 25 câu → Outlier → Timeout) và bỏ ΔSE → cần sửa `CLAUDE.md`, không sửa code theo `CLAUDE.md` |
| V7 | SRS Mục VII (JSON Profile v1) | Khóa: `ability_estimate`, `skill_profiles`, `test_metadata`, `$schema`. Code `ExportForEduZUseCase` xuất: `overall`, `skills`, `metadata`, `schema_version` → **lệch hợp đồng** |
| V8 | Quyết định #32 (404 cho cả "không tồn tại" và "không có quyền") | `ProfileAccessGuard` ném `ForbiddenException` (403) → **lệch quyết định đã chốt** |
| V9 | Quyết định #33 (LOCAL chỉ ADMIN seed) | `seed.ts` cho cả TEACHER mật khẩu LOCAL, mật khẩu seed **plaintext** (`'admin_password_hash_123'`) |
| V10 | `GeminiFlashProvider.generateExplanation` | **Không gọi API thật**: có key thì trả chuỗi cứng `"[Gemini …]: Đáp án đúng là X…"`, không có key trả chuỗi giả khác. Không phải lỗi scaffold nhưng **không được báo "đã xong F-05"** |
| V11 | `@Catch(HttpException)` | Lỗi Prisma (ví dụ `P2002` khi double-submit) **không** thuộc `HttpException` → trả 500 mặc định, lộ stack khi dev |
| V12 | Phiên bản công cụ | Nest 12, TS 6, ioredis 6, Prisma 6.4.1 (ghim), vitest 4, oxlint. Tuần 3 lập kế hoạch cho Prisma 7 + pnpm + jest + monorepo → **thực tế đã lệch** (Quyết định #34 tách repo). Tôi **chưa tra** tài liệu phiên bản mới nhất; Agent phải tra Context7 trước khi nâng/đổi bất cứ gì (task P1.9) |

---

## 2. Bảng nhận xét chi tiết

Ký hiệu mức: 🔴 Nghiêm trọng (sai kết quả/lộ dữ liệu/bypass) · 🟠 Cao (lệch SRS/quyết định, rủi ro khi demo) · 🟡 Vừa · 🟢 Thấp. Cột "Task" trỏ Mục 8–9. "ẢH" = ảnh hưởng tới hệ thống nếu sửa.

### 2.A. Bảo mật & xác thực

| ID | Mức | Phát hiện (bằng chứng) | Đối chiếu | Giải pháp & vì sao | ẢH khi sửa | Task |
|---|---|---|---|---|---|---|
| A-01 | 🔴 | `login.use-case.ts:20` — kiểm mật khẩu luôn đúng; chưa băm (V4) | SRS 15.3 JWT; TC2.4 secret/OWASP | Băm bằng thư viện chốt ở **Q3**; `verify(hash, password)`; so sánh thời gian hằng; thông báo lỗi chung. Vì sao: đây là cổng duy nhất bảo vệ mọi API | Phải seed lại mật khẩu băm; `Login` cần test (đúng/sai/không có hash) | P5.1–P5.3 |
| A-02 | 🔴 | `auth.module.ts`, `jwt.strategy.ts`, `eduz-api-key.guard.ts` có **giá trị mặc định cứng** cho JWT secret và EduZ API key trùng với `.env.example` | CLAUDE.md "không hardcode"; repo sẽ **public** (#34) | Bỏ fallback; thiếu biến ⇒ app **không khởi động** (Joi đã `JWT_SECRET required`; thêm `EDUZ_API_KEY` bắt buộc ở `production`). `EduZApiKeyGuard` dùng `timingSafeEqual`. Vì sao: key mặc định công khai trên GitHub = ai cũng gọi được M2M | Dev phải có `.env`; CI cần secret | P1.2, P5.4 |
| A-03 | 🔴 | `test-session.controller.ts`: không so `session.studentId` với `user.sub`; `startSession` không kiểm role | SRS 15.4 "STUDENT chỉ thao tác trên dữ liệu của mình" | `SessionOwnershipGuard` (hoặc kiểm trong use-case) + `@Roles(STUDENT)` cho `POST /sessions`; trả **404** khi không phải chủ (cùng tinh thần #32). Vì sao: chặn thi hộ/đọc state người khác | Test mới; Admin/Teacher bị chặn tạo phiên (đúng nghiệp vụ) | P4.1, P4.2 |
| A-04 | 🔴 | `ai-explainer.controller.ts` chỉ `JwtAuthGuard`; `explain-item` trả nội dung nêu đáp án đúng | SRS 15.3; Class Diagram: giải thích chạy khi SV *xem kết quả* | Quy tắc truy cập: STUDENT chỉ khi item đó nằm trong **phiên COMPLETED của chính mình**; TEACHER/ADMIN tự do; thêm giới hạn tốc độ. Vì sao: bảo vệ ngân hàng đề + chi phí AI | Cần lookup `session_responses`; thay đổi hợp đồng lỗi (403/404) | P6.9 |
| A-05 | 🟠 | `seed.ts`: mật khẩu plaintext; TEACHER có LOCAL | #33 | Seed băm mật khẩu; chỉ ADMIN LOCAL (đọc mật khẩu từ ENV, không cứng); giáo viên/SV `authProvider=null` đợi SSO. Chặn chạy seed khi `NODE_ENV=production` | Đổi dữ liệu seed, test đăng nhập dùng tài khoản khác | P5.5 |
| A-06 | 🟠 | Chỉ có `POST /auth/login`, `GET /auth/me` | SRS X, 15.3: `refresh` (rotation), `logout` | Triển khai theo **Q-A6** (xem Mục 3, mục kế thừa): refresh token lưu băm ở Redis, rotation, logout thu hồi. Chưa chốt ⇒ **dừng hỏi** khi tới P5.6 | Thêm bảng/khóa Redis; FE phải xử lý 401 → refresh | P5.6 |
| A-07 | 🟠 | Không giới hạn số lần đăng nhập sai/không rate-limit | TC2.4 (OWASP) | `@nestjs/throttler` cho `/auth/login`, `/explanations/*`, `/sessions/*`. Thư viện mới ⇒ ghi quyết định nhỏ vào DECISIONS_LOG | Thêm phụ thuộc | P5.7 |
| A-08 | 🟠 | `main.ts`: `enableCors({ origin: true, credentials: true })` | OWASP | Danh sách origin từ ENV (`CORS_ORIGINS`) | FE phải khai báo origin | P1.3 |
| A-09 | 🔴 | **Không có `.gitignore`** (V1) trong khi có `.env`, `dist/`, `node_modules/` và repo sẽ public | #34, G8, TC2.4 | Tạo `.gitignore` **trước `git init`**; thêm `gitleaks` ở bước CI sau. Vì sao: lộ secret = trừ điểm nặng (TC2.4, G8) | Không | P1.1 |
| A-10 | 🟡 | `export-csv`: nối chuỗi thô; tên `"..."` không thoát dấu `"`; ô bắt đầu `= + - @` thành công thức Excel | OWASP CSV injection | Thoát dấu nháy, tiền tố `'` cho ô nguy hiểm; thêm BOM UTF-8 để Excel đọc tiếng Việt | CSV đổi nhẹ | P6.12 |
| A-11 | 🟡 | Quyết định #24/#28: SSO Google/Microsoft + import danh sách; backend chưa có controller/strategy SSO dù có biến ENV | #24, #28 | **Ngoài phạm vi kế hoạch này** — cần feature-plan riêng `sso-google-microsoft.md`. Kế hoạch này chỉ dọn ENV rỗng nghĩa | — | Ghi nhận ở Mục 11 |

### 2.B. Đúng đắn của CAT & phiên thi

| ID | Mức | Phát hiện | Đối chiếu | Giải pháp & vì sao | ẢH | Task |
|---|---|---|---|---|---|---|
| C-01 | 🔴 | `submit-response.use-case.ts:1108–1111` — `irtB: 0` cho lịch sử | SRS 4.3 (EAP trên toàn bộ phản hồi) | Cung cấp `irtB` của từng câu cũ theo **Q1** (mặc định: JOIN `items`). Viết test **trước** (toàn đúng/toàn sai/xen kẽ + giá trị chuẩn tính độc lập) | θ/SE thay đổi so với hiện tại — **đây là sửa lỗi, không phải đổi đặc tả** | P2.1, P4.6 |
| C-02 | 🔴 | `submit-response`: chỉ kiểm `currentItemId` khi `WAITING_FOR_ANSWER`; không kiểm item đã được phục vụ/APPROVED/chưa trả lời | SRS 15.5 "payload phải chứa item_id trùng current_item_id" | Chấp nhận nộp **chỉ khi** `state=WAITING_FOR_ANSWER` và `itemId===currentItemId`; nếu Redis mất ⇒ reconstruct trước, rồi `READY_FOR_NEXT` ⇒ từ chối (409) | SV không còn tự chọn câu; test double-submit | P4.5 |
| C-03 | 🟠 | `RedisSessionCacheService`: get→set không nguyên tử; lỗi trùng `UNIQUE(session_id,item_id)` thành 500 | SRS 15.5; NFR độ tin cậy | Chuyển trạng thái nguyên tử theo **Q4** (mặc định Lua CAS) + bắt `P2002` ⇒ **409 Conflict** | Thêm script Lua + test song song (2 request đồng thời) | P4.4 |
| C-04 | 🔴 | Chỉ `resume` có dựng lại từ DB; `next-item`/`submit` khi Redis mất dùng `usedIds=[]`, `theta=-0.5` ⇒ **lặp câu, sai θ**. `resume` đặt `lastSkillPicked:null` (random lại, phá xen kẽ) và lấy θ của câu cuối thay vì tính lại | SRS VIII, 15.2, 15.5; Class Diagram III.10 | `SessionStateReconstructor` dùng chung cho cả 3 luồng: `itemsAdministered` từ responses; **tính lại EAP** (theo SRS) từ responses+irtB; `lastSkillPicked` suy ra từ kỹ năng của **câu đã trả lời cuối** (không cần đổi schema); `state=READY_FOR_NEXT`, `currentItemId=null` | Test mô phỏng xóa key Redis giữa bài | P4.3 |
| C-05 | 🟠 | `check-stopping-criterion`: thiếu ΔSE<0.01 ×3 câu; interface khai `recentThetaDelta` không dùng | SRS 4.5 | Theo **Q2** (mặc định: đủ SRS). Truyền 3 giá trị SE gần nhất từ `session_responses.seAfter` | Dừng sớm ít hơn hiện tại ở vùng biên | P2.4 |
| C-06 | 🟡 | `compute-eap`: `max(0.1, se)` (sàn tùy ý, không có trong SRS); `EAPComputationState` không dùng ở đâu; không có guard N(0,0.5)/MLE dù `CLAUDE.md` nói "có MLE fallback guard" | SRS 4.3, R10 | Theo **Q-C6** (Mục 3): mặc định EAP thuần, bỏ sàn SE, giữ clip [-4,4]; sửa `CLAUDE.md` thành "không dùng MLE ⇒ guard không áp dụng"; test hữu hạn khi toàn đúng/toàn sai | SE hiển thị nhỏ hơn sàn 0.1 (không ảnh hưởng ngưỡng 0.35) | P2.2, P2.3 |
| C-07 | 🟠 | Giá trị **cứng** rải rác: ngưỡng CEFR (`compute-result`), 0.35/0.5 độ tin cậy, `±1.5/−2.5` biên, `5` Top-N ở controller, `-0.5` ở controller/resume, `?? 0.35` trùng cấu hình | CLAUDE.md "KHÔNG hardcode"; Class Diagram | `ThetaCefrMapper` (Value Object, dải lấy từ cấu hình/hằng domain có tên), `CefrConfidencePolicy` theo **Q9**, `CAT_TOP_N_ITEMS` thực sự được dùng, một nguồn duy nhất `CatConfig` typed inject vào mọi use-case | Đổi chữ ký constructor ⇒ cập nhật test | P2.5–P2.7 |
| C-08 | 🟠 | `next-item` khi hết câu trong kỹ năng: trả **200** + `{message}`, phiên kẹt | SRS (không nêu); R7 | Theo **Q10** (mặc định: thử kỹ năng còn lại; hết cả hai ⇒ kết thúc phiên với lý do `ITEM_BANK_BOUNDARY`). Không đổi enum | Cần test pool cạn | P4.8 |
| C-09 | 🟠 | `next-item` không kiểm phiên đã `COMPLETED`/quá 45 phút; `TIMEOUT` chỉ xét lúc nộp; `ABANDONED` không bao giờ được set | SRS 4.5 timeout hard stop | Theo **Q11** (mặc định kiểm lười biếng ở mọi request): hết giờ ⇒ hoàn tất với `TIMEOUT` nếu ≥1 câu trả lời, ngược lại `ABANDONED` | Thêm nhánh; test đồng hồ giả | P4.7 |
| C-10 | 🔴 | `compute-result`: tạo hồ sơ **không trong transaction** với việc `complete` phiên, **không idempotent**; `skillProfiles=[]`, `errorPatterns=[]`, `aiRecommendations=[]`; `testMetadata` thiếu `test_duration_seconds, theta_init, quadrature_points, prior, item_bank_version, stopping_reason` (đang là camelCase khác SRS); `boundaryEffect` chỉ theo θ | SRS VII, F-06 (P0), 4.5 | `LanguageProfile.generateFromSession()` (đúng Class Diagram) tính **SkillProfile** (điểm %, `cefr_estimate`, số câu), **ErrorPattern** theo `topic_tag` (accuracy, severity, ngưỡng cấu hình), `TestMetadata` đủ khóa; `boundary_effect = (stopReason===ITEM_BANK_BOUNDARY) \|\| θ ngoài biên`; ghi trong **một transaction**, idempotent theo `testSessionId`. `aiRecommendations`: Q-C10 | Là phần lớn công việc của F-06; cần test số liệu | P3.4, P4.9 |
| C-11 | 🟡 | `POST /sessions` luôn tạo phiên mới; không có ràng buộc "1 phiên đang làm/SV" | SRS (không nêu) | Theo **Q5** (mặc định: trả lại phiên `IN_PROGRESS` đang có) | Hợp đồng `POST /sessions` idempotent | P4.10 |

### 2.C. Kiến trúc & OOP

| ID | Mức | Phát hiện | Giải pháp & vì sao | Task |
|---|---|---|---|---|
| D-01 | 🟠 | **Domain** import `@prisma/client`: `language-profile.entity.ts`, `class-report.entity.ts` | Dùng enum domain (`CefrLevel`, `CefrConfidence` đã có kiểu tương đương) — vi phạm quyết định #13 (Prisma bọc sau Repository) và quy tắc kế hoạch Tuần 3 mục 10.1(3) | P3.1 |
| D-02 | 🟠 | **Application** dùng `PrismaService`: `start-session`, `compute-result`, `explain-item`, `generate-class-report`, `export-csv` | Tạo cổng (port) trong `domain/`: `ITestSessionRepository`, `ILanguageProfileRepository`, `IExplanationRepository`, `IStudentLookup`, `IClassReportQuery`; Prisma chỉ ở `infrastructure/` (theo **Q14**) | P3.2 |
| D-03 | 🟠 | `TestSessionController.getNextItem` chứa cả luồng nghiệp vụ (chọn kỹ năng → `findForCAT` → chọn → ghi cache), inject trực tiếp `CatEngineService` + cache + repo | Tách `GetNextItemUseCase`; controller chỉ gọi use-case + định dạng đầu ra (che `correctAnswer`) | P3.3 |
| D-04 | 🟠 | `test-session` ghi thẳng bảng `language_profiles` (không qua module `language-profile`) | Theo **Q13**: `test-session` gọi `GenerateProfileUseCase` của `language-profile` (mặc định) — aggregate root có một chủ | P3.4 |
| D-05 | 🟡 | `PrismaTestSessionRepository`, `PrismaLanguageProfileRepository`, `PrismaProfileTargetLookup` không có interface; `ProfileAccessGuard` phụ thuộc lớp Prisma cụ thể | Token DI (`'ITestSessionRepository'`…) giống `IItemRepository` | P3.2 |
| D-06 | 🟡 | `ICATEngineDomainService` ≠ chữ ký thực + ≠ Class Diagram (`pickNextSkill(session)`, `selectNextItem(session,pool)`) | Đồng bộ interface ↔ impl; ghi rõ lệch Diagram (tham số là giá trị, không phải `session`) vào Quyết định nếu giữ | P3.5 |
| D-07 | 🟡 | `SessionCacheState` phẳng `theta/se`; Diagram: `eapState: EAPComputationState` (+ `ttlSeconds`); entity có nhưng **không dùng** | Dùng `EAPComputationState` trong cache (tùy **Q1** phương án 3); hoặc ghi lệch vào Quyết định | P3.6 |
| D-08 | 🟡 | `ItemSelectionStrategy` (Sympson-Hetter ở KL) chưa có — câu hỏi mở trong `DECISIONS_LOG` mục "Ví dụ" | Theo **Q-D8** (Mục 3, kế thừa): interface mỏng nay, hiện thực `RandomizedTopNStrategy` | P3.7 |
| D-09 | 🟡 | `any` ×40, `strict:false` | Theo **Q12**: bật `noImplicitAny` rồi `strict` theo đợt | P1.4, P3.8 |

### 2.D. Hợp đồng API so với SRS Mục X

| ID | Mức | Phát hiện | Giải pháp | Task |
|---|---|---|---|---|
| E-01 | 🟠 | **Thiếu** endpoint: `POST /auth/refresh`, `/auth/logout`; `GET/PUT/DELETE /items/:id`, `POST /items/bulk-import`; `GET /sessions/:id/result`; `GET /placement-profiles/:id/history`; `GET /reports/class-distribution`, `/reports/error-patterns` (code: `/reports/distribution`) | Làm theo từng task; `bulk-import` (Excel/CSV theo #40) **ngoài phạm vi** → feature-plan riêng; đổi `distribution` → `class-distribution` (hoặc giữ alias) | P5.6, P6.x |
| E-02 | 🟠 | JSON hồ sơ lệch SRS VII (V7) | `LanguageProfileJsonMapper` (phiên bản `schema v1`) xuất đúng khóa SRS; theo **Q8** | P6.5 |
| E-03 | 🟠 | EduZ gọi được route nào? SRS: `GET /placement-profiles/:student_id` bằng API key; code: route chính chỉ JWT, route M2M riêng `…/eduz-export` | Theo **Q7** (mặc định: một route, guard chấp nhận **JWT hoặc API Key**) | P6.6 |
| E-04 | 🟠 | Item Bank: `CreateItemDto` là `interface` ⇒ `ValidationPipe` **không chạy**; body `response` của submit nhập inline không kiểm ('Z' làm vi phạm CHECK ⇒ 500); chuyển trạng thái tùy ý (duyệt cả câu `REJECTED`, từ chối câu `APPROVED`); không có sửa nội dung (F-02) | DTO là `class` + `class-validator` (khoảng `irtB` theo biên Item Bank, A–D, độ dài); máy trạng thái trong `ItemEntity` (`DRAFT→PENDING_REVIEW→APPROVED/REJECTED`, quy tắc sửa-sau-duyệt theo **Q6**) | P6.1–P6.4 |
| E-05 | 🟠 | `reporting.controller`: Admin (`institutionId=null`) bị gán chuỗi `'default-institution'` ⇒ truy vấn UUID sai ⇒ lỗi | Admin: tham số tùy chọn `?institutionId=` (mặc định gộp tất cả, đúng "Admin không giới hạn institution"); Teacher: luôn ép `institutionId` của mình | P6.10 |
| E-06 | 🟡 | `ErrorPattern` toàn lớp (F-09, SRS X) chưa có; hồ sơ `errorPatterns` đang rỗng | Làm sau khi C-10 xong (có dữ liệu) | P6.11 |

### 2.E. Chất lượng & quy trình (TC2.4 / TC2.5 / TC2.3)

| ID | Mức | Phát hiện | Vì sao quan trọng | Giải pháp | Task |
|---|---|---|---|---|---|
| Q-01 | 🔴 | **0 test** (V2); lõi thuật toán chưa có đối chiếu | G5 (TC2.5 trần Mức 1); SRS 4.3 bắt buộc ≥3 case; TC2.3 cần bằng chứng "bắt được lỗi AI" | Test-first cho EAP, stopping, skill, policy, mapper; sau đó integration (DB thật) + API | P2.x, P8.x |
| Q-02 | 🟠 | Chưa `git init`, chưa CI, chưa hook | TC2.4/2.6; Quyết định #36 | **Việc của người** (agent không tự `git init`, xem 10.3). Agent chuẩn bị `.gitignore`, script `npm run lint/test/test:cov` | P1.1, P0.2 |
| Q-03 | 🟡 | `TRACKING_BACKEND_SCAFFOLD.md` ghi "Hoàn thành 100%", "Phase 5 build/lint" | Nhật ký báo cáo vượt mức thật ⇒ rủi ro khi hội đồng đối chiếu (TC2.3) | Thêm mục "Trạng thái thực" + trỏ sang tracking mới; **không xóa** nội dung cũ | P9.2 |
| Q-04 | 🟡 | `README.md` là bản mẫu Nest; chưa có hướng dẫn chạy/biến môi trường/kiến trúc | TC2.4 (tài liệu kỹ thuật) | Viết README thật (cài, ENV, migrate, seed, chạy test, sơ đồ module) | P9.4 |
| Q-05 | 🟡 | `CLAUDE.md` mô tả sai thứ tự dừng, bỏ ΔSE, nói có MLE guard | Agent đọc `CLAUDE.md` đầu tiên ⇒ có thể "sửa code theo tài liệu sai" | Sửa đoạn "CATEngine — 4 hành vi lõi" cho khớp SRS sau khi bạn chốt Q2/Q-C6 | P9.5 |
| Q-06 | 🟢 | `zod`, `@types/ioredis` (ioredis có sẵn type), `@nestjs/mau`, 3 thư viện validate (joi/zod/class-validator) | Giảm bề mặt phụ thuộc | Gỡ thư viện không dùng sau khi kiểm `grep` | P1.8 |

### 2.F. Lược đồ CSDL (`schema.prisma`, `custom_migrations.sql`, `seed.ts`)

Phần khớp (ghi nhận để không sửa nhầm): 9 bảng/9 enum khớp #15–#18, #21 (có `calibrated`, `times_used`), #22 (ADMIN `institution_id` null kèm CHECK, bỏ `WRITING`), composite FK tenant, `UNIQUE(session_id,item_id)`, `UNIQUE(item_id)` cho `explanations`, partial index và CHECK trong SQL.

| ID | Mức | Phát hiện | Giải pháp & vì sao | Task |
|---|---|---|---|---|
| S-01 | 🟠 | **Chưa có `prisma/migrations`**; SQL tay nằm riêng `custom_migrations.sql`; hướng dẫn chạy `migrate dev` rồi *dán SQL vào pgAdmin* ⇒ lần sau `migrate dev` có thể sinh migration **xóa** `idx_items_cat` (drift, đã cảnh báo ở kế hoạch Tuần 3 mục 6) | `migrate dev --create-only --name init` → apply → `--create-only --name cat_partial_index_and_checks` dán SQL → apply → kiểm drift (`migrate diff … --exit-code`) | P7.1–P7.4 |
| S-02 | 🟡 | Không có ràng buộc cho "`studentId` phải là user có role STUDENT" (có thể là TEACHER) | Chặn ở use-case (A-03) + tùy chọn trigger/`CHECK` qua bảng `student_profiles` (composite FK tới `student_profiles(user_id)` cần đổi schema ⇒ hỏi) | P7.5 |
| S-03 | 🟡 | `session_responses` không giữ `irt_b` lúc trả lời | **Q1** (phương án 2 thêm cột `item_irt_b`) | P7.6 (có điều kiện) |
| S-04 | 🟡 | Không có ràng buộc "1 phiên `IN_PROGRESS`/SV" | **Q5**: partial unique index `(student_id) WHERE status='IN_PROGRESS'` (nếu chọn A/C) | P7.7 (có điều kiện) |
| S-05 | 🟡 | Cột JSON `skill_profiles`, `error_patterns`, `test_metadata` không có kiểm cấu trúc, chỉ `schemaVersion` | Schema kiểm bằng `zod` (nay `zod` đang không dùng — đáng dùng) hoặc `class-validator`, **ở tầng domain mapper**, chọn theo Q-S5 | P3.9 |
| S-06 | 🟡 | Đồng bộ tài liệu: `Mo_ta_So_do_Lop_ClassDiagram.md` + diagram chưa phản ánh #21 (`calibrated`, `timesUsed`), #22 (`institution` `0..1`, bỏ `WRITING`), `AuthProviderType` | Cập nhật `Mo_ta` (md); diagram `.drawio` do người xuất lại (Q1 Tuần 3) | P9.6 |
| S-07 | 🟢 | Bảng `reference_items`, `item_label_evidence` (#29, #31 D4) chưa có trong schema | **Ngoài phạm vi** — thuộc kế hoạch Item Bank (Tuần 3); ghi nhận để không quên | Mục 11 |
| S-08 | 🟢 | Lệch công cụ so với kế hoạch Tuần 3: Prisma 6.4.1 (kế hoạch 7 + `adapter-pg`), npm (kế hoạch pnpm), vitest (kế hoạch jest), 1 repo `backend` (kế hoạch `apps/backend`) | Xác nhận giữ nguyên ở **Q15–Q18** và ghi vào DECISIONS_LOG | P0.5 |
| S-09 | 🟢 | `seed.ts` nạp 30 item mẫu (kế hoạch Tuần 3: *không seed Item*); `Item.status` mặc định `DRAFT` nhưng `CreateItemUseCase` đặt `PENDING_REVIEW` | Giữ cho dev nhưng đánh dấu rõ "dữ liệu mẫu, không phải Item Bank thật" + chặn `production`; ghi quyết định `PENDING_REVIEW` | P5.5 |

### 2.G. AI

| ID | Mức | Phát hiện | Giải pháp | Task |
|---|---|---|---|---|
| AI-01 | 🟠 | Provider là **stub** (V10); quyết định #39/#40 đã chọn LiteLLM gateway, kế hoạch riêng `ai-llm-gateway.md` | **Không làm trong kế hoạch này** (**Q-G1** mặc định). Chỉ: đổi tên/ghi chú "STUB", log cảnh báo khi chạy `production`, test hợp đồng use-case với provider giả. Không báo "xong F-05" | P6.9, P9.3 |
| AI-02 | 🟢 | Mặc định `gemini-1.5-flash` — tôi **chưa kiểm chứng** còn dùng được | Agent tra tài liệu Gemini hiện hành khi làm gateway; đừng sửa ở đây | Mục 11 |
| AI-03 | 🟢 | Prompt chỉ yêu cầu giải thích đáp án đúng; không có kiểm tra đầu ra | Thuộc gateway plan | Mục 11 |

---

## 3. Các điểm CẦN BẠN CHỐT (điền ô `☐` rồi báo "duyệt")

> **Quy tắc:** Agent **không** bắt đầu task phụ thuộc một câu hỏi khi ô chốt còn trống. Nếu bạn nói **"duyệt hết mặc định"**, mọi câu lấy phương án **(★)**. Agent ghi mỗi quyết định vào `DECISIONS_LOG.md` (số tiếp theo #48+) và `feature-plans/backend-hardening.md` Mục 3.

### 3.1. Nhóm I — ảnh hưởng thiết kế (bắt buộc chốt trước khi làm task liên quan)

**Q1 — Lấy `irtB` của các câu đã trả lời để tính lại EAP thế nào?** *(C-01, C-04, S-03, D-07)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | JOIN `items` khi nạp phiên | Không đổi schema; đơn giản | Nếu sau này `irt_b` đổi (calibration KL) thì dựng lại phiên cũ sẽ ra θ khác lúc thi |
| ☐ B | Thêm cột `session_responses.item_irt_b` (snapshot) | Dựng lại bất biến; nền cho F-12 | Đổi schema + migration, lệch SRS 6.2 (cần ghi đề xuất v2.7); sửa seed/test |
| ☐ C | Lưu `EAPComputationState`/`posteriorWeights` thay vì replay | Khớp đúng Class Diagram | Phức tạp nhất; khi Redis mất vẫn cần `irt_b` |

**Q2 — Outlier Early Stop: có điều kiện ΔSE<0.01 trong 3 câu không?** *(C-05)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Đủ theo SRS 4.5 (θ ngoài biên **và** ΔSE ×3 **và** ≥8 câu) | Đúng đặc tả được duyệt, đúng Class Diagram md, không dừng khi SE còn đang giảm | Cần đọc 3 `seAfter` gần nhất |
| ☐ B | Rút gọn (θ + ≥8 câu) như `CLAUDE.md`/code hiện tại | Đơn giản | Lệch SRS; có thể dừng khi kết quả còn kém chắc; phải ghi quyết định lệch SRS + đề xuất v2.7 |

**Q3 — Thư viện băm mật khẩu?** *(A-01, A-05)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | `argon2` | Khuyến nghị OWASP hiện nay | Native module; có thể vướng build trên Windows/Docker alpine (kiểm ở P5.1) |
| ☐ B | `bcryptjs` | Thuần JS, cài dễ | Chậm hơn, giới hạn 72 byte, ít hiện đại |
| ☐ C | `bcrypt` (native) | Nhanh, phổ biến | Native build như A, không hơn A về an toàn |

**Q4 — Chống race-condition state machine Redis?** *(C-03)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Lua script CAS (kiểm `state`+`currentItemId` rồi đổi, nguyên tử) + `P2002`→409 | Không khóa phân tán (đúng tinh thần SRS 15.5), nguyên tử thật | Phải viết/test Lua |
| ☐ B | Chỉ bắt `P2002`→409 | Ít việc nhất | Vẫn tính EAP thừa; còn cửa sổ ghi đè state |
| ☐ C | `SET NX` khóa ngắn theo session | Đơn giản hơn Lua | Rủi ro khóa mồ côi; SRS từng bỏ phương án khóa |

**Q5 — Nhiều phiên `IN_PROGRESS` của cùng một SV?** *(C-11, S-04)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | `POST /sessions` trả lại phiên đang làm (idempotent) + partial unique index | Chống mở nhiều phiên lấy "kết quả đẹp"; F-04 resume tự nhiên | Muốn thi lại phải kết thúc/hết hạn phiên cũ |
| ☐ B | Cho phép nhiều phiên | Linh hoạt | SV mở nhiều phiên, Redis/DB phình, kết quả khó hiểu |
| ☐ C | Trả 409 nếu đang có phiên | Rõ ràng | FE phải xử lý thêm; trải nghiệm kém hơn A |

**Q6 — Giáo viên sửa `Item` đã `APPROVED`: xử lý thế nào?** *(E-04; đồng thời trả lời câu mở Q4 Tuần 3 về `Explanation`)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Cho sửa nhưng **trở về `PENDING_REVIEW`** và **xóa `Explanation` cũ** | Không bao giờ có câu đã sửa mà chưa duyệt vào CAT; giải thích luôn khớp nội dung | Câu tạm ra khỏi CAT; mất giải thích (sinh lại lazy) |
| ☐ B | Cấm sửa khi `APPROVED` (phải sao chép câu mới) | Lịch sử sạch | Thao tác vòng vèo; không đúng F-02 "sửa tự do" |
| ☐ C | Sửa tại chỗ, giữ `APPROVED` | Nhanh | Lọt câu chưa kiểm vào bài thi; giải thích cũ sai nội dung |

**Q-C6 — Guard "EAP prior mạnh N(0,0.5) / MLE" của SRS 4.3 áp dụng thế nào?** *(C-06)*
SRS đặt guard ở mục *"MLE Fallback Guard (nếu EAP bị bug)"*; runtime hiện chỉ dùng EAP.
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | EAP thuần (không MLE), clip [-4,4], bỏ sàn SE; ghi "guard N/A vì không dùng MLE"; test toàn đúng/toàn sai ra θ hữu hạn | Đúng cách đọc "nếu dùng MLE"; không đổi hành vi | Phải sửa `CLAUDE.md`; giải trình trước hội đồng |
| ☐ B | Dùng prior N(0,0.5) khi toàn đúng/toàn sai | Đúng cách đọc khác của SRS | **Đổi quỹ đạo θ ở các câu đầu** ⇒ đổi số câu dừng |
| ☐ C | Cài thêm MLE fallback thật | Đủ mọi chữ trong SRS | Thêm code dễ lỗi, không có lợi ích đo được |

**Q7 — EduZ (M2M) gọi route nào?** *(E-03)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Một route `GET /placement-profiles/:studentCode`, guard chấp nhận **JWT hoặc API Key** (API Key chỉ GET) | Đúng hợp đồng SRS 15.4, bỏ route trùng | Guard hợp nhất phức tạp hơn một chút |
| ☐ B | Giữ route riêng `…/eduz-export`, đề xuất SRS v2.7 ghi nhận | Ít việc | Lệch SRS; hai route cần giữ đồng bộ |

**Q8 — Chuyển `LanguageProfile` → JSON (`exportForEduZ()`/`toJSON()`) đặt ở đâu?** *(E-02; câu mở trong DECISIONS_LOG)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A | `LanguageProfileJsonMapper` versioned (v1 nay, v2 ở KL) | Dễ thêm Schema v2 (F-13), domain thuần | Class Diagram có `exportForEduZ()` trên aggregate ⇒ lệch Diagram |
| ☐ B | Method trên aggregate | Khớp Diagram | Khó thêm v2, aggregate biết cấu trúc xuất |
| ☐ C ★ | Lai: aggregate có `exportForEduZ()` **mỏng** ủy quyền cho Mapper theo `schemaVersion` | Khớp Diagram và vẫn mở rộng được | Thêm một lớp gián tiếp |

**Q9 — Ngưỡng độ tin cậy CEFR (`cefr_confidence`)**: SRS **không** quy định; code hardcode HIGH<0.35, MEDIUM<0.5. *(C-07)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Giữ giá trị hiện tại, **đưa ra cấu hình** (`CAT_CONFIDENCE_MEDIUM_SE=0.5`), ghi đề xuất SRS v2.7 | Không đổi kết quả, hết hardcode | Số 0.5 vẫn là đề xuất chưa tra nguồn |
| ☐ B | Suy ra từ SE, `boundary_effect` và số câu (HIGH chỉ khi SE<0.35 **và** không biên) | Hợp lý hơn về nghiệp vụ | Tự đặt luật mới; cần bạn duyệt công thức |

**Q10 — Hết câu trong một kỹ năng?** *(C-08)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Thử kỹ năng còn lại; hết cả hai ⇒ kết thúc phiên với `ITEM_BANK_BOUNDARY` | Không kẹt phiên, không đổi enum/schema | Phá nhẹ quy tắc xen kẽ khi cạn câu |
| ☐ B | Trả 409 và dừng | Không phá xen kẽ | SV kẹt giữa bài |
| ☐ C | Thêm giá trị enum `ITEM_POOL_EXHAUSTED` | Phân biệt rõ nguyên nhân | Đổi enum + Diagram + schema |

**Q11 — Hết giờ / bỏ dở (`TIMEOUT`, `ABANDONED`)?** *(C-09)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Kiểm **lười** mỗi request (không cần bộ lập lịch) | Không thêm hạ tầng | Phiên bỏ dở vẫn `IN_PROGRESS` tới lần gọi kế (chỉ ảnh hưởng thống kê) |
| ☐ B | Job định kỳ (`@nestjs/schedule`/BullMQ) quét phiên quá hạn | Dữ liệu sạch | Thêm hạ tầng; BullMQ là "Recommended" trong SRS |
| ☐ C | Không xử lý `ABANDONED` ở TL | Ít việc | Giữ enum chết |

**Q13 — Ai sinh `LanguageProfile` khi phiên kết thúc?** *(D-04)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | `test-session` gọi `GenerateProfileUseCase` của `language-profile` (đồng bộ, cùng transaction qua port) | Khớp Diagram (`computeResult(): LanguageProfile`, `generateFromSession`); đơn giản | Phụ thuộc module `test-session → language-profile` |
| ☐ B | Sự kiện `SessionCompleted` (EventEmitter) | Lỏng lẻo hơn | Mất transaction chung; khó test; thêm cơ chế |
| ☐ C | Giữ như hiện tại | Không đổi | Hai module cùng ghi một bảng |

**Q14 — Mức độ tách cổng (port) cho tầng application?** *(D-02)*
| | Phương án | Ưu | Nhược |
|---|---|---|---|
| ☐ A ★ | Port cho aggregate ghi (Session, Profile, Explanation) + một `IClassReportQuery` cho báo cáo đọc | Đủ sạch, ít file | Báo cáo là "query service" có Prisma ở infrastructure |
| ☐ B | Port cho *mọi* thứ kể cả đọc báo cáo | Thuần nhất | Nhiều file hơn mức cần cho quy mô TL |

### 3.2. Nhóm II — xác nhận quyết định đã "ngầm" có trong scaffold (mặc định: **giữ**)

| Mã | Điều cần xác nhận | Mặc định ★ | Phương án khác |
|---|---|---|---|
| ☐ Q12 | TypeScript: `strict:false` + 40 `any` | ★ bật `noImplicitAny` ngay, `strict` từng module sau (P3.8) | A bật `strict` toàn bộ ngay · C giữ nguyên |
| ☐ Q15 | Prisma 6.4.1 ghim (kế hoạch Tuần 3 dự kiến 7) | ★ giữ 6.4.1; chỉ nâng khi có lý do và tra tài liệu | Nâng lên 7 + `adapter-pg` |
| ☐ Q16 | Trình quản lý gói: npm (Quyết định #12 pnpm nay hết cơ sở vì #34 tách repo) | ★ giữ npm | Chuyển pnpm |
| ☐ Q17 | Test runner: vitest (kế hoạch Tuần 3 ghi jest) | ★ giữ vitest | Đổi lại jest |
| ☐ Q18 | Hạ tầng dev/test: Postgres+Redis | ★ thêm `docker-compose.yml` trong repo backend (Redis bật AOF `appendfsync everysec` — NFR R4; DB `apt_test` riêng) | Testcontainers · repo infra riêng |
| ☐ Q19 | Cấu trúc thư mục `backend/backend` lồng | ★ gốc repo = thư mục trong cùng (bạn tự di chuyển khi `git init`; Agent **không** tự di chuyển) | Giữ lồng |
| ☐ Q-D8 | `ItemSelectionStrategy` | ★ tạo interface mỏng + `RandomizedTopNStrategy` ngay | Để KL |
| ☐ Q-S5 | Kiểm cấu trúc JSON hồ sơ | ★ `zod` (đang cài mà không dùng) | `class-validator` · không kiểm |
| ☐ Q-A6 | Refresh token | ★ lưu băm trong Redis, rotation, `logout` xóa | Bảng DB · JWT refresh không lưu (không thu hồi được) |
| ☐ Q-C10 | `aiRecommendations` khi chưa có AI gateway | ★ để mảng rỗng, ghi rõ "chờ gateway", **không** sinh bằng luật cứng tự bịa | Sinh gợi ý theo luật từ `errorPatterns` (cần bạn duyệt luật) |
| ☐ Q-G1 | Phạm vi AI | ★ ngoài kế hoạch này (xem `ai-llm-gateway.md`) | Làm provider Gemini thật ngay |

### 3.3. Phản hồi của bạn (điền khi duyệt)

```
Duyệt: ☐ hết mặc định (★)   ☐ có chỉnh — ghi các mã khác mặc định:
Ghi chú: ...
Ngày duyệt: ...
```

---

## 4. Đối chiếu Class Diagram ↔ code (tóm tắt)

| Class Diagram | Code | Nhận xét |
|---|---|---|
| `User` abstract + `Student/Teacher/Admin` | `users` + `student_profiles`/`teacher_profiles` (#17) | ✅ Khớp quyết định; thiếu ràng buộc role↔profile (S-02) |
| `Institution 1—1..* User` | `institution_id` nullable cho ADMIN (#22) | ✅ Khớp quyết định; diagram/`Mo_ta` chưa cập nhật (S-06) |
| `TestSession` composition `SessionResponse` | `onDelete: Cascade` | ✅ |
| `SessionCacheState` + `EAPComputationState` | cache phẳng; entity không dùng | ⚠️ D-07 |
| `CATEngine` `<<service>>` không giữ state | `CatEngineService` ủy quyền 4 use-case | ✅; ⚠️ chữ ký (D-06) |
| `Item` (+ `findForCAT`) | `IItemRepository.findForCAT` lọc `APPROVED` ở repo | ✅ đúng R9; chỉnh `limit` lấy từ cấu hình |
| `Item 1◆0..1 Explanation` | `explanations.item_id UNIQUE` + lazy cache | ✅ |
| `LanguageProfile` aggregate root, `generateFromSession`, `exportForEduZ` | entity chỉ là DTO; sinh hồ sơ nằm ở `compute-result` | ⚠️ C-10, D-04 |
| `ClassReport` `<<service>>` | use-case dùng Prisma, chỉ phân bố + CSV | ⚠️ E-05, E-06 |

---

## 5. Giải pháp tổng thể & thứ tự ưu tiên

1. **Chặn rủi ro an toàn trước** (A-01…A-04, A-09, C-01, C-02): đây là các lỗi làm mất uy tín khi demo/public repo.
2. **Test-first cho lõi CAT** (Q-01): bằng chứng cho TC2.3/TC2.5; mọi sửa C-xx đi kèm test đỏ→xanh.
3. **Đưa schema vào migration chuẩn** (S-01) để test tích hợp có nền.
4. **Dọn kiến trúc** (D-01…D-08) *sau* khi có test (an toàn khi refactor).
5. **Hoàn thiện hợp đồng API & F-06** (E-xx, C-10).
6. **Đồng bộ tài liệu & minh chứng** (P9).

---

## 6. Phân tích: có thay đổi tính năng cốt lõi không?

**Không.** Đối chiếu với 4 hành vi lõi (`CLAUDE.md`, SRS IV):

| Hành vi lõi | Đặc tả sau kế hoạch | Thay đổi quan sát được? |
|---|---|---|
| `pickNextSkill()` | Round-robin, câu 1 ngẫu nhiên 50/50, giữ nguyên | Chỉ khác khi **pool cạn** (Q10) hoặc **dựng lại phiên** (hiện sai ⇒ đúng) |
| `selectNextItem()` | Randomized Top-N (N từ cấu hình = 5), lọc `APPROVED` ở repo | Không |
| `computeEAP()` | 41 điểm, N(0,1), clip ±4 | **Có**: θ/SE tính đúng sau khi sửa C-01 (lỗi, không phải đổi đặc tả); bỏ sàn SE 0.1 |
| `checkStoppingCriterion()` | Thứ tự SE → biên → 25 → timeout | **Có thể**: thêm ΔSE (Q2=A) ⇒ dừng biên *ít* hơn hiện tại |

Các điểm có thể bị hội đồng hỏi "đã đổi đặc tả chưa?": (1) ΔSE — *không*, đây là thêm cho đúng SRS; (2) bỏ sàn `max(0.1,SE)` — sàn này **không có trong SRS**; (3) tính lại EAP khi Redis mất — SRS VIII yêu cầu đúng điều này. Bất kỳ chỗ nào lệch SRS thực sự (Q2=B, Q-C6=B, Q1=B) sẽ được ghi vào `DECISIONS_LOG` và danh sách **đề xuất SRS v2.7**, không âm thầm sửa.

**Ảnh hưởng tới các kết quả đã/đang chuẩn bị:** dữ liệu đo (KPI Bước 3: số câu trung bình, SE cuối bài, exposure) **chưa có** — nên sửa C-01 bây giờ *không làm mất* số liệu nào. Nếu để tới sau khi đo thì phải đo lại toàn bộ.

---

## 7. Phụ thuộc giữa các phase

```
P0 (cổng: duyệt Mục 3, đọc tài liệu, feature-plan)
 └─► P1 (vệ sinh & nền: .gitignore, ENV fail-fast, CORS, strict, dọn gói)
        ├─► P2 (CAT thuần — test-first) ──────────┐
        └─► P7 (schema → migration chuẩn, drift) ─┤   ∥ (P2 ∥ P7)
                                                  ▼
                                    P3 (refactor kiến trúc: port, use-case, mapper)
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    ▼                             ▼                             ▼
          P4 (phiên thi: quyền,        P5 (Auth: băm, refresh,        P6 (Item/Profile/Report/
              state, reconstruct,          seed, rate-limit)               Explain API)
              hồ sơ F-06)                                                    
                    └──────────────┬──────────────┴─────────────────────────────┘
                                   ▼
                      P8 (integration + API test, đo coverage thật)
                                   ▼
                      P9 (khép sổ: log, weekly-log, sửa CLAUDE.md/README/Mo_ta, SRS v2.7)
```

`∥` = chạy song song được. **P4, P5, P6 song song** vì chạm các module khác nhau (ghi chú xung đột ở Mục 10.4).

---

## 8. Kế hoạch triển khai chi tiết (cho AI Agent)

Ký hiệu: 🤖 Agent · 👤 Người · ⛔ cổng chặn · `∥` song song · **Xác minh** là điều kiện bắt buộc trước khi đánh ✅. Lệnh chạy trong `D:\TLCN\backend\backend` (npm, PowerShell/Git Bash nhất quán).

### Phase 0 — Cổng vào (tuần tự)
| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| P0.1 | Người dùng điền Mục 3.3 (duyệt) | 👤 ⛔ | Có phản hồi duyệt; Agent chép nguyên văn vào tracking |
| P0.2 | Kiểm trạng thái: không có git? có `.gitignore`? có `prisma/migrations`? DB/Redis chạy chưa? | 🤖 ⛔ | Ghi kết quả vào tracking. **Không** tự `git init`, **không** tự chạy `migrate reset` |
| P0.3 | Đọc theo thứ tự Mục 10.2 | 🤖 | Ghi "đã đọc" |
| P0.4 | Tạo `0.docs/tracking/feature-plans/backend-hardening.md` từ `_template.md` (Mục 1–2 từ kế hoạch này; Mục 3 chép Mục 3 + câu trả lời) | 🤖 | File tồn tại đủ mục |
| P0.5 | Ghi quyết định đã chốt vào `DECISIONS_LOG.md` (#48+, đủ cột như các dòng cũ) | 🤖 | Mỗi Q có một dòng |

### Phase 1 — Vệ sinh & nền (`∥` nội bộ)
| ID | Việc | Xác minh |
|---|---|---|
| P1.1 | Tạo `.gitignore` (node_modules, dist, `.env`, `*.tsbuildinfo`, coverage, `.env.*` trừ `.example`) | `git check-ignore -v .env` (nếu đã init) hoặc đọc file; **A-09** |
| P1.2 | Bỏ fallback secret ở `auth.module.ts`, `jwt.strategy.ts`, `eduz-api-key.guard.ts`; Joi: `EDUZ_API_KEY` bắt buộc khi `NODE_ENV=production` | Khởi động không `JWT_SECRET` ⇒ lỗi rõ; test cấu hình (P2.8) |
| P1.3 | CORS theo `CORS_ORIGINS` (ENV + Joi + `.env.example`) | Origin lạ bị từ chối (test) |
| P1.4 | `tsconfig`: `noImplicitAny: true` (theo Q12) — sửa lỗi phát sinh | `npm run build` 0 lỗi |
| P1.5 | `HttpExceptionFilter` thêm nhánh bắt lỗi Prisma (`P2002`→409, `P2025`→404) và lỗi lạ→500 không lộ stack | Test filter (đơn vị) |
| P1.6 | Xóa/viết lại `test/app.e2e-spec.ts` (hiện sai route) | `npm run test:e2e` không đỏ vì sai route |
| P1.7 | `vitest.config.ts`: coverage (v8), ngưỡng chưa đặt (không bịa), alias | `npm run test:cov` chạy được |
| P1.8 | Gỡ phụ thuộc không dùng sau `grep` xác nhận (`zod` **giữ** nếu Q-S5=zod; `@types/ioredis`…) | Build + test xanh |
| P1.9 | Tra tài liệu (Context7) phiên bản Nest/Prisma/ioredis/Lua `EVAL` đang dùng; ghi **phiên bản thật** và bất kỳ chỗ cú pháp khác vào tracking | Có ghi nhận |

### Phase 2 — Lõi CAT thuần, test-first (`∥ P7`)
| ID | Việc | Xác minh |
|---|---|---|
| P2.1 | Tính **giá trị chuẩn EAP độc lập** (script Python/numpy trong scratchpad, **ngoài repo**) cho: 5 đúng liên tiếp, 5 sai liên tiếp, xen kẽ, 1 câu, các `b` khác nhau; ghi kết quả + lệnh tái tạo vào chú thích spec | Có số + nguồn |
| P2.2 | `compute-eap.use-case.spec.ts` (đỏ trước): 3 case SRS 4.3 + hữu hạn khi toàn đúng/toàn sai + θ trong [-4,4] + SE giảm khi thêm dữ liệu + không NaN | Spec đủ; đỏ vì C-01/C-06 nếu có |
| P2.3 | Sửa `ComputeEapUseCase` theo Q-C6 (bỏ sàn SE; giữ clip) | Spec xanh |
| P2.4 | `check-stopping-criterion` theo Q2: nhận `recentSE: number[]`; spec phủ **mọi nhánh** (SE; biên có/không ΔSE; <8 câu; 25 câu; timeout; thứ tự ưu tiên khi nhiều điều kiện cùng đúng) | Spec xanh; đồng hồ giả (`vi.useFakeTimers`) |
| P2.5 | `ThetaCefrMapper` (Value Object) + spec đủ 6 dải **và biên** (−2.0, −1.0, 0.0, 1.0, 2.0) | Spec xanh |
| P2.6 | `CefrConfidencePolicy` theo Q9 + `boundaryEffect` (SRS 4.5/4.7) + spec | Spec xanh |
| P2.7 | `CatConfig` typed (một nguồn) inject cho use-case; xóa `?? giá trị` trùng lặp và `-0.5`/`5` cứng ở controller/resume | `grep` không còn số cứng liệt kê ở C-07 |
| P2.8 | Spec `pick-next-skill` (câu 1 ngẫu nhiên 50/50 với `randomSource` giả; xen kẽ), `select-next-item` (rỗng ⇒ null, đều) và `ProfileAccessPolicy` (mỗi dòng bảng SRS 15.4 ≥1 test) | Xanh |
| P2.9 | **Nhắc người dùng đối chiếu công thức với SRS 4.3/4.5 trước khi merge** | Ghi nhận |

### Phase 7 — Schema & migration (`∥ P2`; tuần tự bên trong)
| ID | Việc | Xác minh |
|---|---|---|
| P7.0 | 👤 Cung cấp/khởi động Postgres dev; Agent dựng `docker-compose.yml` (Postgres 16 + Redis AOF) theo Q18 | `docker compose up -d` healthy |
| P7.1 | `prisma validate`; `prisma migrate dev --create-only --name init` → **đọc SQL sinh ra**, đối chiếu schema | File migration có |
| P7.2 | Apply; `\dt` đủ 9 bảng | ✅ |
| P7.3 | `--create-only --name cat_partial_index_and_checks`; **chuyển nội dung** `custom_migrations.sql` vào migration này (giữ file cũ làm tham chiếu, ghi chú đã chuyển); apply | `\d items` có `idx_items_cat … WHERE status='APPROVED'` và các CHECK |
| P7.4 | **Kiểm drift:** `migrate dev` lần nữa không sinh migration mới; `migrate diff --exit-code` | Không có `DROP INDEX idx_items_cat`. Nếu có ⇒ **dừng hỏi** |
| P7.5 | (Có điều kiện, theo S-02) Chỉ **hỏi** nếu muốn ràng buộc role↔`student_profiles` ở DB | Không làm tự động |
| P7.6 | (Chỉ nếu Q1=B) cột `session_responses.item_irt_b` + migration + cập nhật repo/seed | Test lưu snapshot |
| P7.7 | (Chỉ nếu Q5=A/C) migration partial unique index `(student_id) WHERE status='IN_PROGRESS'` | Test chèn hai phiên ⇒ lỗi |
| P7.8 | `prisma generate`; xác nhận không commit client | Build xanh |

### Phase 3 — Refactor kiến trúc (sau P2, P7; có test bảo vệ)
| ID | Việc | Xác minh |
|---|---|---|
| P3.1 | Thay `@prisma/client` trong `language-profile.entity`, `class-report.entity` bằng enum domain (`CefrLevel`, `CefrConfidence`, `StoppingReason`) | Không import Prisma trong `domain/` |
| P3.2 | Port + token DI: `ITestSessionRepository`, `ILanguageProfileRepository`, `IExplanationRepository`, `IStudentLookup`, `IClassReportQuery` (Q14); chuyển code Prisma sang `infrastructure/` | `grep PrismaService` chỉ còn trong `infrastructure/` |
| P3.3 | `GetNextItemUseCase`; controller mỏng (che `correctAnswer`) | Spec use-case (mock port) |
| P3.4 | `LanguageProfile.generateFromSession()` + `GenerateProfileUseCase` trong `language-profile` (Q13); `ComputeResultUseCase` gọi nó; ghi trong **một transaction**, idempotent | Spec: cùng input hai lần ⇒ 1 hồ sơ |
| P3.5 | Đồng bộ `ICATEngineDomainService` ↔ impl; ghi lệch Diagram (nếu giữ) | Build xanh |
| P3.6 | `SessionCacheState`: dùng `EAPComputationState` (theo Q1) hoặc ghi quyết định lệch | Test cache (mock Redis) |
| P3.7 | `ItemSelectionStrategy` + `RandomizedTopNStrategy` (Q-D8) | Spec; `CatEngineService` nhận qua constructor |
| P3.8 | Bật `strict` theo từng module đã sạch (Q12); loại `any` dần | Build 0 lỗi mỗi bước |
| P3.9 | Schema `zod` cho `skill_profiles`/`error_patterns`/`test_metadata` + mapper (Q-S5) | Spec hợp lệ/không hợp lệ |
| P3.10 | Cấu hình `no-restricted-imports` (oxlint) cấm `@prisma/client` trong `domain/**`, `application/**` | Thử file mẫu ⇒ lint đỏ, xóa mẫu |

### Phase 4 — Phiên thi (`∥ P5, P6`; chạm `test-session`, `cat-engine`)
| ID | Việc | Xác minh |
|---|---|---|
| P4.1 | `SessionOwnershipGuard`/kiểm trong use-case: không phải chủ ⇒ **404** (A-03) | Test: SV A không đụng phiên SV B; Teacher bị 403 khi `POST /sessions` |
| P4.2 | `@Roles(STUDENT)` cho `POST /sessions`; use-case kiểm `role===STUDENT` | Test |
| P4.3 | `SessionStateReconstructor` dùng chung `start/next-item/submit/resume`: `itemsAdministered`, **tính lại EAP**, `lastSkillPicked` từ câu trả lời cuối, `READY_FOR_NEXT` (C-04) | Test: xóa key Redis giữa bài ⇒ tiếp tục đúng, không lặp câu |
| P4.4 | Lua CAS chuyển state + bắt `P2002`→409 (Q4) | Test **2 request đồng thời** ⇒ đúng 1 thành công, 1 là 409; không 500 |
| P4.5 | `submit`: chỉ nhận khi `WAITING_FOR_ANSWER` và `itemId===currentItemId` (C-02); DTO `class` kiểm `response ∈ A–D` | Test các nhánh từ chối |
| P4.6 | `submit`: cung cấp `irtB` lịch sử theo Q1 (C-01); `recentSE` cho stopping (Q2) | **Test hồi quy C-01** (trước: sai, sau: khớp giá trị chuẩn P2.1) |
| P4.7 | Kiểm phiên đã kết thúc/hết giờ ở mọi request; `TIMEOUT`/`ABANDONED` (Q11) | Test đồng hồ giả |
| P4.8 | Hết câu kỹ năng (Q10) | Test pool cạn |
| P4.9 | Hoàn tất phiên: sinh hồ sơ đủ SRS VII (SkillProfile, ErrorPattern, TestMetadata, `boundary_effect`) (C-10) | Test số liệu tính tay |
| P4.10 | `POST /sessions` idempotent theo Q5 | Test |
| P4.11 | `GET /sessions/:id/result` (SRS X) cho phiên `COMPLETED` của chính mình | Test |

### Phase 5 — Auth (`∥ P4, P6`)
| ID | Việc | Xác minh |
|---|---|---|
| P5.1 | Cài thư viện băm theo Q3; kiểm build trên máy này (Windows) | `node -e "require('argon2')"` hoặc tương đương |
| P5.2 | `PasswordHasher` (port) + hiện thực; `LoginUseCase` dùng `verify`; thông báo lỗi chung (A-01) | Test: đúng/sai/không có hash/`authProvider≠LOCAL` |
| P5.3 | Tài khoản `authProvider≠LOCAL` không đăng nhập bằng mật khẩu | Test |
| P5.4 | `EduZApiKeyGuard`: `timingSafeEqual`, không fallback (A-02) | Test |
| P5.5 | `seed.ts`: băm; chỉ ADMIN LOCAL từ ENV; đánh dấu dữ liệu mẫu; chặn `production` (A-05, S-09) | `npm run db:seed` chạy 2 lần không lỗi (idempotent) |
| P5.6 | `POST /auth/refresh`, `/auth/logout` theo Q-A6 (**chưa chốt ⇒ dừng hỏi**) | Test rotation + thu hồi |
| P5.7 | Rate-limit (`@nestjs/throttler`) cho login/explain/sessions (A-07); ghi DECISIONS_LOG | Test vượt ngưỡng ⇒ 429 |

### Phase 6 — Item / Profile / Report / Explain (`∥ P4, P5`)
| ID | Việc | Xác minh |
|---|---|---|
| P6.1 | DTO `class` + validator cho tạo/sửa Item (khoảng `irtB` từ cấu hình biên Item Bank, A–D, độ dài) | Test 400 |
| P6.2 | Máy trạng thái trong `ItemEntity` (chuyển hợp lệ, `approve/reject` có điều kiện) | Spec ma trận chuyển trạng thái |
| P6.3 | `GET /items/:id`, `PUT /items/:id` (Q6), `DELETE /items/:id` (xóa mềm hay cứng — **dừng hỏi** nếu chưa có trong SRS: SRS X chỉ ghi DELETE) | Test |
| P6.4 | Phân trang mặc định cho `GET /items`; che trường nhạy cảm theo vai trò | Test |
| P6.5 | `LanguageProfileJsonMapper` v1 đúng khóa SRS VII (Q8) | Test so khớp JSON mẫu SRS (đổi giá trị) |
| P6.6 | Route M2M theo Q7 (guard chấp nhận JWT hoặc API Key, API Key chỉ GET) | Test 4 tổ hợp |
| P6.7 | `ProfileAccessGuard`: **404** cho không tồn tại và không có quyền (#32) | Test từng dòng bảng SRS 15.4 |
| P6.8 | `GET /placement-profiles/:studentCode/history` (SRS X) | Test |
| P6.9 | Explain: quy tắc truy cập (A-04), cache, giới hạn tốc độ; provider đổi tên/ghi chú **STUB** + cảnh báo `production` (AI-01) | Test: SV chưa nộp ⇒ không lấy được giải thích |
| P6.10 | Reporting: Admin xem tất cả/`?institutionId=`; Teacher ép institution (E-05); đổi `class-distribution` | Test |
| P6.11 | `GET /reports/error-patterns` (sau P4.9) | Test dữ liệu tổng hợp |
| P6.12 | CSV: thoát ký tự, chống injection, BOM (A-10) | Test ô `=1+1` |

### Phase 8 — Test tích hợp & đo thật (sau P4–P7)
| ID | Việc | Xác minh |
|---|---|---|
| P8.1 | Cấu hình test tích hợp: DB `apt_test`, `migrate deploy` ở `globalSetup`, dọn bảng giữa test | `npm run test:int` chạy được |
| P8.2 | Test `findForCAT`: chỉ `APPROVED`; loại `usedIds`; đúng skill; sắp `|b−θ|`; `EXPLAIN` dùng `idx_items_cat` với ≥1.000 dòng | ✅ |
| P8.3 | Test ràng buộc: item `APPROVED` thiếu `approved_by`; `correct_answer='E'`; trùng `(session,item)`; cascade xóa phiên; `UNIQUE(item_id)` explanations; FK tenant | ✅ |
| P8.4 | E2E luồng chính (supertest): login → start → next-item → submit… → dừng → result → profile; cùng Redis mất giữa chừng | ✅ |
| P8.5 | Mô phỏng phiên (không gọi API): 1.000 SV giả, kiểm số câu/SE/exposure Top-5 — **dữ liệu mô phỏng ghi rõ là mô phỏng**, không đưa vào TRACKING như số đo thật | Báo cáo trong tracking, nhãn "mô phỏng" |
| P8.6 | `npm run test:cov` — ghi **số thật** (hoặc N/A) | Không bịa |

### Phase 9 — Khép sổ & minh chứng (bắt buộc theo `rubric-tracker`)
| ID | Việc | Xác minh |
|---|---|---|
| P9.1 | Cập nhật `AI_USAGE_LOG.md` sau **mỗi phiên** có AI sinh/sửa code (ghi rõ lỗi AI/scaffold phát hiện: các mục 🔴) — nguồn cho "≥5 lỗi AI tự phát hiện" (TC2.3) | Dòng mới |
| P9.2 | `TRACKING_BACKEND_SCAFFOLD.md`: thêm mục "Trạng thái thực" + liên kết (không xóa) | Có mục |
| P9.3 | `weekly-log/Tuan-04.md` (tạo từ `_template.md` nếu chưa có): mục "Thay đổi thiết kế & lý do" nêu các Q đã chốt | File có |
| P9.4 | Viết `README.md` thật cho backend | Người lạ chạy được theo README |
| P9.5 | Sửa `CLAUDE.md` mục "CATEngine — 4 hành vi lõi" cho khớp SRS (thứ tự dừng, ΔSE, guard) | Diff đúng phạm vi |
| P9.6 | Cập nhật `Mo_ta_So_do_Lop_ClassDiagram.md` (S-06); diagram `.drawio` 👤 xuất lại | Có |
| P9.7 | Danh sách **đề xuất SRS v2.7** (lệch SRS↔code đã chốt) vào `weekly-log/Tuan-04.md` — **không sửa** `.docx` | Có danh sách |
| P9.8 | `TRACKING.md` chỉ số **đo thật**; chưa đo ⇒ N/A | Không có số bịa |
| P9.9 | Nhắc bạn commit (Conventional Commits, `GIT_CONVENTIONS.md`) — **không tự commit/push** | — |

---

### Phase X — Yêu cầu từ kế hoạch Frontend (thêm 2026-10-07; xem `KE_HOACH_TRIEN_KHAI_FRONTEND.md` Mục 5)
> Phase này **chỉ thêm**, không đổi task cũ. Dòng ghi "= Px.y" nghĩa là đã có trong phase tương ứng, chỉ để đối chiếu mã BE-X. PX.14 và PX.17 làm đổi hợp đồng hiện tại; PX.16/PX.17 đổi schema theo quyết định #55 (người dùng đã chốt Q-F23…Q-F28).

| ID | Mã FE | Việc | Phụ thuộc | Xác minh |
|---|---|---|---|---|
| PX.1 | BE-X1 | CORS allowlist theo ENV (`CORS_ORIGINS`) | gộp với P1 (CORS) — nếu P1 đã làm thì chỉ kiểm | Test: origin lạ bị từ chối |
| PX.2 | BE-X2 | Thêm `@nestjs/swagger`, xuất `openapi.json` (Q-F4 = A); gắn decorator cho DTO/response | Sau P3 (DTO là class) | Truy cập `/api/docs`; `openapi.json` hợp lệ |
| PX.3 | BE-X3 | `POST /auth/refresh`, `/auth/logout` — **chính là P5.6**, hình dạng token theo BFF (Q-F3 = A: FE giữ cookie, BE trả token trong body) | = P5.6 | Theo P5.6 |
| PX.4 | BE-X4 | `GET /sessions/:id/result` — **chính là P4.11** | = P4.11 | Theo P4.11 |
| PX.5 | BE-X5 | `GET /placement-profiles/:code/history` — **chính là P6.8** | = P6.8 | Theo P6.8 |
| PX.6 | BE-X6 | `class-distribution`, `error-patterns` — **chính là P6.10–P6.11**; thêm tham số tùy chọn `examRoundId` khi PX.17 xong | = P6.10–11 | Theo P6.10–11 |
| PX.7 | BE-X7 | `GET/PUT/DELETE /items/:id` — **chính là P6.1–P6.3** | = P6.1–3 | Theo P6.1–3 |
| PX.8 | BE-X8 | `GET /sessions/active` (phiên `IN_PROGRESS` của chính mình hoặc `null`); liên quan Q5 | Sau P4.1–P4.3 | Test: có/không phiên; không trả phiên người khác |
| PX.9 | BE-X9 | Siêu dữ liệu phiên: `itemCount`, `maxItems`, `expiresAt`, `serverTime` ở `POST /sessions`, `next-item`, `resume`; giá trị từ `CatConfig` | Sau P4.4 | Test: `expiresAt` = bắt đầu + timeout cấu hình; nhất quán sau reconstruct |
| PX.10 | BE-X10 | `GET /sessions/:id/review`: chỉ phiên của chính mình và `COMPLETED`; trả `[{item, chosen, correct, isCorrect, explanation}]`; quy tắc truy cập giải thích cho phiên đang thi xem PX.16 | Sau P4.11, P6.9 | Test: phiên người khác ⇒ 403/404; chưa hoàn thành ⇒ từ chối |
| PX.11 | BE-X11 | Mã lỗi nghiệp vụ ổn định `code` (`SESSION_ITEM_MISMATCH`, `SESSION_EXPIRED`, …) trong `HttpExceptionFilter` | Sau P3 | Test: mỗi tình huống lỗi có `code` |
| PX.12 | BE-X12 | `next-item` khi hết câu: trạng thái/lý do rõ ràng — **theo Q10 của BE** | = theo Q10 | Theo Q10 |
| PX.13 | BE-X14 | `studentCode`, `fullName` trong `/auth/me` và `login.user` | Sau P5.2 | Test: SV có `studentCode`; GV/Admin `null` |
| PX.14 | BE-X16 | Bỏ `thetaAfter/seAfter` khỏi response `responses`; bỏ `cefrTarget` khỏi câu gửi SV; `isCorrect` chỉ khi phiên có cờ phản hồi (PX.16) | Sau P4.5–P4.6 | Test: mặc định không có khóa `theta/se/isCorrect` |
| PX.15 | BE-X17 | `GET /items`: lọc `cefr`, `source`, `q`, phân trang `{data,total}` | Sau P6.1 | Test: lọc + phân trang |
| PX.16 | BE-X19a | **ExamRound — schema & migration** (quyết định #55): bảng `exam_rounds` (`id, institution_id, name, created_by, opens_at, closes_at, show_item_feedback default false, created_at`), cột `test_sessions.exam_round_id` NULL được + cột chụp cờ phản hồi; ràng buộc/index; **cập nhật Class Diagram (giữ tiếng Anh) — hỏi người dùng trước** | Sau P7 (không chạm schema khi P7 đang chạy) | `prisma migrate` sạch; không drift; seed không vỡ |
| PX.17 | BE-X19b | **ExamRound — API**: CRUD `exam-rounds` (Teacher đơn vị mình + Admin); `GET /exam-rounds/open` cho SV; `POST /sessions` nhận `examRoundId` (kiểm đợt đang mở, cùng đơn vị) và chụp cờ; `responses` trả `isCorrect` + đáp án đúng + giải thích **chỉ khi** cờ phiên bật; cho phép `GET /explanations/items/:id` trong phiên đang thi **chỉ** cho câu đã trả lời của chính phiên đó và khi cờ bật (đổi dạng quy tắc A-04) | Sau PX.16, P4, P6.9 | Test: cờ tắt ⇒ không lộ gì; cờ bật ⇒ chỉ lộ câu đã trả lời; đổi cờ không ảnh hưởng phiên đang thi |


## 9. Ước lượng khối lượng (để PM cân đối Tuần 4–6)

Không phải cam kết; đo bằng số task: P0 5 · P1 9 · P2 9 · P7 9 · P3 10 · P4 11 · P5 7 · P6 12 · P8 6 · P9 9 = **87 task**. Đường găng: P0 → P1 → P2/P7 → P3 → P4 → P8. Nếu chỉ kịp **một đợt tối thiểu** trước mốc cam kết Bước 3 (cuối Tuần 6, gate G1): làm **P0, P1, P2, P4.1–P4.6, P5.1–P5.5** (xóa hết 🔴 + có test lõi); phần còn lại xếp vào Tuần 7+.

---

## 10. Hướng dẫn dành cho AI Agent thực thi kế hoạch này

### 10.1. Quy tắc bất biến
1. Kế hoạch được duyệt khi Mục 3.3 có phản hồi. Làm đúng nội dung đã duyệt; **không "cải tiến"** thêm.
2. **Chỉ tạo/sửa file được liệt kê trong task.** Không tạo file ngoài kế hoạch (trừ file test, migration, feature-plan P0.4, file mà task nêu rõ).
3. Domain thuần; `application/` không import Prisma/`ioredis`; Prisma/Redis chỉ trong `infrastructure/`.
4. Không hardcode tham số thuật toán/ngưỡng (θ₀, SE, boundary, Top-N, ngưỡng độ tin cậy) — qua `CatConfig`.
5. Ngôn ngữ: tài liệu/tracking **tiếng Việt**; định danh code & UML **tiếng Anh**.
6. Không bịa số liệu (coverage, KPI, kết quả mô phỏng). Chưa đo ⇒ "N/A". Số mô phỏng phải gắn nhãn.
7. Không tự ký `COMMITMENT_BASELINE.md`, không tự `git init`/commit/push (xem bộ nhớ: không tự push), không sửa file `.docx` SRS.
8. **Test trước, sửa sau** cho mọi mục C-xx/A-xx: chứng minh test đỏ vì lỗi cũ rồi mới sửa (đây là bằng chứng TC2.3).
9. Phép tính học thuật (EAP, SE, stopping, mapping): **luôn đối chiếu SRS** và nhắc người dùng trước khi merge.
10. Sau **mỗi** phiên có AI sinh/sửa: ghi `AI_USAGE_LOG.md` (Mục P9.1), không dồn cuối.

### 10.2. Thứ tự đọc bắt buộc (P0.3)
`CLAUDE.md` → `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md` → **file kế hoạch này** → `DECISIONS_LOG.md` (#13, #15–#18, #21–#24, #28, #32, #33, #34, #39, #40) → `feature-plans/f03-cat-engine.md` → `GIT_CONVENTIONS.md` → SRS v2.6 (Mục IV, VII, VIII, X, XV).

### 10.3. Điều kiện phải DỪNG và hỏi qua `AskUserQuestion` (≥ 2 phương án + trade-off)
- Bất kỳ ô Mục 3 còn trống mà task cần.
- Drift migration có `DROP INDEX idx_items_cat` (P7.4).
- `argon2`/native không build được (P5.1).
- `DELETE /items` xóa mềm hay cứng (P6.3); refresh token (P5.6) khi Q-A6 chưa chốt.
- Muốn thêm/đổi cột, bảng, enum, hoặc đổi tên bảng/cột đã có trong `schema.prisma` ngoài những gì task P7.6/P7.7 mô tả.
- Phiên bản thư viện thực tế khác cú pháp dùng trong kế hoạch.
- Phát hiện lỗi mới có mức 🔴 chưa liệt kê ở Mục 2 → **báo ngay**, thêm vào tracking mục "Phát hiện mới", không tự mở rộng phạm vi.
- **Bất kỳ** lựa chọn ảnh hưởng khả năng mở rộng/bảo trì mà SRS/Class Diagram/kế hoạch này đều không quy định.

### 10.4. Cách cập nhật file theo dõi (sau **mỗi** task hoàn thành)
Mở `Tuan4/TRACKING_RA_SOAT_VA_HOAN_THIEN_BACKEND.md` và:
1. Đổi ô trạng thái: ⬜ → 🔄 khi bắt đầu, → ✅ **chỉ khi đã chạy xong bước Xác minh**, hoặc 🚫 kèm câu hỏi dừng.
2. Điền cột "Bằng chứng": lệnh + kết quả tóm tắt + đường dẫn file tạo/sửa. Không dán log dài.
3. Tính lại % của phase và bảng tổng quan (= số ✅ / tổng task).
4. **Thêm một dòng** vào "Nhật ký cập nhật" cuối file (append-only, không sửa dòng cũ).
5. Nếu bị chặn: đặt 🚫, **không** chuyển sang task phụ thuộc.
6. Task song song (P4/P5/P6) chỉ cập nhật đúng **hàng của mình**. File chung dễ xung đột: `app.module.ts`, `package.json`, `schema.prisma`, `.env.example` — chỉ **một** nhánh sửa tại một thời điểm; nhánh khác chờ hoặc gộp tuần tự.
7. Khi phát hiện task mô tả sai thực tế (ví dụ đường dẫn): sửa ngay cột "Ghi chú", không âm thầm làm khác.

### 10.5. Định nghĩa "xong" (Definition of Done) cho cả kế hoạch
- [ ] Mọi mục 🔴 ở Mục 2 ở trạng thái ✅ có test hồi quy.
- [ ] `npm run build`, `npm run lint`, `npm test`, `npm run test:int` xanh; không còn import Prisma trong `domain/` và `application/` (P3.10).
- [ ] `prisma migrate deploy` trên DB rỗng dựng đúng 9 bảng + partial index + CHECK; **không drift** (P7.4).
- [ ] Hồ sơ năng lực sinh ra đủ khóa SRS Mục VII (trừ `ai_recommendations` nếu Q-C10 mặc định).
- [ ] `DECISIONS_LOG.md`, `AI_USAGE_LOG.md`, `weekly-log/Tuan-04.md`, `feature-plans/backend-hardening.md` đã cập nhật; có danh sách **đề xuất SRS v2.7**.
- [ ] `TRACKING.md` chỉ chứa số đo thật hoặc N/A.

### 10.6. Lệnh tham chiếu nhanh (PowerShell, `D:\TLCN\backend\backend`)
```powershell
npm run build ; npm run lint ; npm test ; npm run test:cov
npx prisma validate
npx prisma migrate dev --create-only --name init          # đọc SQL rồi mới apply
npx prisma migrate dev
npx prisma migrate diff --from-migrations prisma/migrations --to-schema-datamodel prisma/schema.prisma --exit-code
npx prisma generate ; npm run db:seed
```
> Cú pháp `migrate diff` thay đổi theo phiên bản Prisma — Agent kiểm `npx prisma migrate diff --help` (P1.9) trước khi dùng. `migrate reset`/`db push` **chỉ** trên DB dev cá nhân và chỉ khi bạn đồng ý; CI/staging chỉ `migrate deploy`.

---

## 11. Rủi ro & câu hỏi mở (Agent **không** tự trả lời)

| # | Điều | Ảnh hưởng | Ghi chú |
|---|---|---|---|
| O1 | **Gauss–Hermite vs lưới đều** (Q3 Tuần 3): SRS gọi "Gaussian–Hermite 41 điểm" nhưng mô tả lưới đều bước 0.2 — code đang dùng lưới đều | Hội đồng có thể hỏi; độ chính xác EAP | Đề xuất SRS v2.7 sửa thuật ngữ hoặc đổi thuật toán — **chưa quyết** |
| O2 | SSO Google/Microsoft + import danh sách người dùng (#24, #28) | UC mới; ngoài kế hoạch này | Cần `feature-plans/sso-google-microsoft.md` |
| O3 | Gateway AI LiteLLM, Gemini thật, model mặc định `gemini-1.5-flash` còn dùng được không | F-05, TC2.3 | `ai-llm-gateway.md`; tôi chưa kiểm chứng |
| O4 | `bulk-import` Item (Excel/CSV) và bảng `reference_items`/`item_label_evidence` (#29, #31, #40) | F-02, nạp Item Bank | Kế hoạch Item Bank riêng |
| O5 | Rubric G5/G6/G8: git, CI (build→lint→test→scan→docker→deploy), `gitleaks` | TC2.4/2.6 | Việc của người + kế hoạch CI riêng; kế hoạch này chỉ chuẩn bị script |
| O6 | Chưa có Item Bank thật ⇒ không đo được KPI Bước 3 bằng dữ liệu thật; P8.5 chỉ là mô phỏng | `COMMITMENT_BASELINE` | Không đưa số mô phỏng vào KPI |
| O7 | Hiệu năng `findForCAT` nạp toàn bộ `{id,irtB}` mỗi lượt (đã chọn ở #23/A7) | NFR <20ms với ~280 câu: đủ; kiểm `EXPLAIN`/đo ở P8.2 | Nếu >~5.000 câu mới cần `ORDER BY ABS()` SQL |
| O8 | Quyền Teacher theo `institution` đối với `Item` (Item Bank dùng chung mọi trường — R1 Tuần 3) | KL multi-tenant | Ghi nhận |

---

*Kế hoạch này chỉ tạo tài liệu; chưa sửa dòng code nào, chưa cài package, chưa tạo migration, chưa `git init`. Mọi hành động thật nằm sau cổng P0.1 (bạn duyệt Mục 3).*
