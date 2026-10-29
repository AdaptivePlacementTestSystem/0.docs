# CLAUDE.md

File này hướng dẫn Claude Code (và mọi AI Agent khác) khi làm việc trong repo này.

## Bắt đầu từ đâu (Start Here)

- **Trước bất kỳ việc gì có ý nghĩa**, đọc kỹ `process/HUONG_DAN_RUBRIC_VA_TRACKING.md` — tài liệu nền giải thích vì sao dự án có hệ thống tracking này (rubric chấm điểm của Khoa) và toàn bộ bối cảnh.
- Dự án đã kích hoạt skill **`rubric-tracker`** (plugin `tlcn-devkit`, `.claude/`) — skill này tự động nhắc các hành vi bắt buộc bên dưới khi làm việc trên file dự án. Không tắt/bỏ qua skill này.
- File này (CLAUDE.md) là bản tóm tắt nhanh — **không thay thế** `HUONG_DAN_RUBRIC_VA_TRACKING.md` hay `tracking/DECISIONS_LOG.md`.

---

## Tổng quan hệ thống

**Adaptive Placement Test — hệ thống CAT-Rasch**: hệ thống kiểm tra xếp lớp tiếng Anh thích ứng (Computerized Adaptive Testing) dùng mô hình IRT Rasch, ánh xạ năng lực sang thang CEFR. Đồ án **Tiểu luận (TL)**, 2 thành viên, 12 tuần. Một số phần đánh dấu **[KL]** (Khóa luận) — ngoài phạm vi TL, không code trừ khi có quyết định mở rộng riêng (xem `DECISIONS_LOG.md`).

> ⚠️ **Trạng thái hiện tại (2026-10-16, Tuần 5/12): ĐÃ CÓ MÃ NGUỒN KHỞI TẠO NHƯNG CHƯA CÓ GIT REPOSITORY.** `backend/backend` (NestJS; module có sẵn: ai-explainer, auth, cat-engine, health, item-bank, language-profile, reporting, test-session) và `frontend` (Next.js; route group `(student)`, `(teacher)`, `(exam)`, `(public)`) đã tồn tại, nhưng chưa `git init` ở thư mục gốc (`` là repo git riêng cho tài liệu). Mã hiện còn theo mô hình cũ (ví dụ `item-bank` còn `APPROVED`/`PENDING_REVIEW`/`MANUAL`, `ItemSource` trong domain); `schema.prisma` và đặc tả v3.0 đã đi trước mã. Phần lớn tính năng Tuần 5 (kỳ thi, import, đổi/quên mật khẩu, sinh và duyệt đề) mới ở mức **tài liệu thiết kế**. Luôn `ls`/`git status` và đọc mã thật trước khi thao tác; không giả định lệnh build/run chạy được nếu chưa kiểm.

### Tech stack đã chốt (SRS Mục III; bản chuẩn `requirements/SRS_TLCN_v3.0.docx`/`.md`; bản cũ (v2.6 Final…) ở `_ARCHIVE_20261024/`)

| Thành phần | Công nghệ | Ghi chú |
|---|---|---|
| Backend | NestJS (TypeScript), Clean Architecture | Hai repo riêng (#48) + gói dùng chung `packages/shared-types` nối bằng `file:` (#122), cấu trúc đích: `design/structure/KE_HOACH_CAU_TRUC_DU_AN.md`; `src/modules/{auth, item-bank, cat-engine, test-session, language-profile, ai-explainer, reporting}` + module mới v3.0 (tên chờ duyệt): `user-import`, `user-admin`, `exam-round`, `mail`, `item-generation` |
| Frontend | Next.js (TypeScript) | Repo riêng (#48); dùng `@apt/shared-types` cho enum và mã lỗi (#122), DTO sinh từ OpenAPI (#51) |
| Database | PostgreSQL | Source of Truth |
| Cache / State | Redis | State machine chống race-condition khi làm bài thi + L1 cache; lưới tạm import (TTL ~30 phút); OTP; ghi async qua BullMQ |
| Email | `MailPort` + SMTP (nodemailer), đẩy qua hàng đợi BullMQ có retry | Mật khẩu tạm, OTP quên mật khẩu, email nhắc việc duyệt/xác nhận. Tiểu luận **không** làm chuông thông báo thời gian thực (chỉ email + Hộp việc). Nhà cung cấp SMTP chưa chọn (Q-5) |
| Mật khẩu / đăng nhập | argon2; mật khẩu tạm 12 ký tự; bắt buộc đổi lần đầu; đăng nhập chỉ email + mật khẩu (SSO thuộc Khóa luận) | Độ dài tối thiểu 8 (đề xuất, chờ chốt Q-4) |
| AI | Gemini Flash (qua LLM Gateway có dự phòng) | Sinh câu hỏi + giải thích (cùng lời gọi), kiểm đáp án độc lập, embedding cho lọc trùng (mô hình chưa chốt, Q-9); xem `plans/KE_HOACH_SINH_VA_DUYET_DE_AI.md` |
| Calibration (offline, KHÔNG chạy trong request path) | py-irt hoặc catR API | Docker sidecar riêng |
| Gateway | Nginx | |

Module sinh câu hỏi bằng AI (`ai-question-generator`, tên module backend là đề xuất, có thể gọi `item-generation`) **thuộc phạm vi TL** theo DC-27…DC-45 / Quyết định #102–#113: Admin tạo lô (AI sinh hoặc import file lưới tạm) → AI kiểm 3 điểm (C1/C2/C3) → Admin giao việc → GV A duyệt và gửi gói → GV B xác nhận → Admin kiểm tra và import (`FINAL_APPROVED`). **Chưa triển khai**; còn mở Q-7…Q-12 (ngưỡng, bản quyền ngân hàng tham chiếu, mô hình embedding, `pg_trgm`, phạm vi tăng, test CAT với biên `irt_b` mới). Nguồn chân lý: `plans/KE_HOACH_SINH_VA_DUYET_DE_AI.md` (phương án cũ ở `_ARCHIVE_20261024/` đã bị thay). Phạm vi tăng ⇒ phải cập nhật `tracking/COMMITMENT_BASELINE.md` trước khi ký (G1, hết Tuần 6).

---

## Quy tắc bắt buộc riêng của dự án này (quan trọng hơn code)

1. **KHÔNG tự quyết định thay** bất kỳ lựa chọn nào ảnh hưởng khả năng mở rộng/bảo trì mà SRS hoặc Class Diagram chưa quy định rõ — đặt tên, cấu trúc module, pattern, mức coupling, field cứng, đổi schema... Phải **dừng lại**, trình bày ≥2 phương án kèm trade-off, hỏi qua `AskUserQuestion`. Đây là quy tắc **tuyệt đối, không ngoại lệ**. Xem ví dụ thật đã xảy ra (rất nhiều): `tracking/DECISIONS_LOG.md`.
2. **Ghi `tracking/AI_USAGE_LOG.md`** sau mỗi lần AI sinh/sửa code hoặc tài liệu dự án có ý nghĩa — bắt buộc cho TC2.3 (chống đạo văn), hội đồng có thể hỏi bất kỳ dòng nào.
3. **Trước khi code 1 F-ID/bugfix không tầm thường:** tạo `tracking/feature-plans/<slug>.md` từ `_template.md` (xem `tracking/PROMPT_TEMPLATE_FEATURE.md`).
4. **Quy ước ngôn ngữ tài liệu — đã chốt, không tự đổi:** UML diagram (`AdaptivePlacementTest.xml`, Class Diagram) giữ **tiếng Anh** mặc định (khớp định danh code thật); đặc tả `.docx`/SRS/toàn bộ hệ thống tracking giữ **tiếng Việt**. Chỉ dịch diagram sang tiếng Việt khi được yêu cầu rõ ràng ở đúng phiên đó, không suy diễn từ ngữ cảnh (xem `DECISIONS_LOG.md` #5/#7 — đã từng dịch rồi phải đảo ngược lại vì AI tự suy diễn sai).
5. Đọc `tracking/HUONG_DAN_BAO_CAO_TUAN.md` trước khi soạn/rà soát báo cáo tuần; đọc `tracking/GIT_CONVENTIONS.md` trước khi commit (khi đã có git).
6. Không tự bịa số liệu (KPI, coverage, kết quả khảo sát) vào `TRACKING.md` — để trống/"N/A" nếu chưa đo được.
7. **Đồng bộ tài liệu thiết kế:** mỗi khi chốt/đổi phạm vi, use case, Class Diagram, schema, API hoặc màn hình, phải rà soát **cả bộ** trong `` (bảng "Bản đồ tài liệu" bên dưới: SRS, đặc tả UC, UC/Class/Sequence/Component/Deployment, cấu trúc dự án, mô tả luồng và màn hình, kế hoạch, `schema.prisma`) rồi `DECISIONS_LOG`/weekly-log. **Tài liệu CHƯA chốt:** AI chỉ lưu vào `drafts/`, không sửa bản chuẩn; khi người dùng chốt mới thay bản chuẩn, chuyển bản cũ vào `_ARCHIVE_<ngày>/` và ghi bảng lịch sử phiên bản. Tài liệu nào hoãn thì ghi "Nợ đồng bộ tài liệu" ở weekly-log. Chi tiết: mục 4b của skill `rubric-tracker`.

---

## CATEngine — 4 hành vi lõi (đã audit & chốt Tuần 1)

Chi tiết đầy đủ: `tracking/feature-plans/f03-cat-engine.md`, `design/catengine/Luong_Hoat_Dong_CATEngine.md`.

- **`pickNextSkill()`** — chọn kỹ năng kế tiếp (Vocabulary/Grammar; Writing không thuộc TL v3.0); **round-robin cố định** (chốt qua `AskUserQuestion`, SRS không tự quy định con số này — đừng suy đoán lại).
- **`selectNextItem()`** — **Randomized Top-5 b-matching**: lọc Top-5 item `status='FINAL_APPROVED'` theo `|b_i − θ̂|` tăng dần, chọn ngẫu nhiên đều 1 trong 5 (chống lộ đề). Guard bắt buộc filter `FINAL_APPROVED` ở tầng Repository, không phải ở service. Vòng đời `Item` (một chiều): `DRAFT` → `FIRST_APPROVED` (GV A) → `SECOND_APPROVED` (GV B) → `FINAL_APPROVED` (Admin import); `REJECTED` do người loại, `AI_REJECTED` do máy loại; chỉ `FINAL_APPROVED` được CAT chọn.
- **`computeEAP()`** — Expected A Posteriori, **lưới đều 41 điểm θ ∈ [−4, +4], bước 0,2** (tích phân số kiểu hình thang; không phải Gaussian–Hermite quadrature; DC-26, Quyết định #101), Prior N(0,1); có MLE fallback guard (chỉ dùng khi ≥1 đúng và ≥1 sai trong session; clip θ về [-4, +4]).
- **`checkStoppingCriterion()`** — dừng khi (theo thứ tự ưu tiên): SE < 0.35, HOẶC đủ 25 câu, HOẶC Outlier Early Stop (θ > 1.5 hoặc θ < −2.5 kèm điều kiện hội tụ của SRS Mục 4.5, sau ≥8 câu), HOẶC hết hạn phiên: `expires_at = min(startedAt + durationMinutes của kỳ thi, closesAt)`; `durationMinutes` mặc định 45 (5–180). Quá hạn: ≥ 8 câu ⇒ `COMPLETED` + `TIMEOUT`, ít hơn ⇒ `ABANDONED`.
- **Tham số cấu hình** (đặt trong `ConfigService`/env, **KHÔNG hardcode** — SRS tự ghi chú các số này sẽ đổi sau khi có dữ liệu calibration thật): θ₀ = **−0.5** (không phải 0.0), ngưỡng SE **0.35**, max items **25**, min items trước khi Early Stop có hiệu lực **8**, khoảng `irt_b` hợp lệ của Item Bank `b_min = −4, b_max = +4` (DC-34, #107; thay `−2.5…+1.5`, vẫn là cấu hình). `−2.5` và `+1.5` chỉ còn là ngưỡng θ của Outlier Early Stop (cơ sở độ phủ ngân hàng): phải chạy lại ≥3 ca test CAT sau khi đổi (Q-12).
- Với mọi thay đổi liên quan thuật toán này (Rasch/EAP/quadrature/stopping): **luôn đối chiếu công thức với SRS trước khi merge**, viết ≥3 test case bắt buộc (toàn đúng, toàn sai, xen kẽ — SRS Mục 4.3 đã tự liệt kê).

---

## Class Diagram — nhóm entity chính

Đầy đủ: `design/class/Mo_ta_So_do_Lop_ClassDiagram.md`; số class/enum thay đổi theo từng phiên nên **không ghi cứng ở đây** — đếm từ sơ đồ hiện hành (sơ đồ draw.io `design/class/TLCN.drawio.xml` — bản gọn 3 trang cập nhật 26/10/2026 (bản cũ ở `_ARCHIVE_20261026/`), ảnh xem trước `TLCN-Trang-1…3.png` dựng bằng script, cần xuất lại từ draw.io; Component và Deployment ở `design/component-deployment/`).

- **User/Actor:** `AuthProvider` (interface; gói TL chỉ có `JwtAuthProvider`, đăng nhập chỉ email + mật khẩu; EduZ SSO thuộc Khóa luận), `User` (abstract; role qua enum `UserRole`: `STUDENT`/`TEACHER`/`ADMIN`; `EDUZ_SERVICE` chỉ là role của API Key cho EduZ, không phải dòng trong bảng `users`; có `mustChangePassword`, `isActive`). **Không còn `Institution`** (hệ thống đơn trường, DC-19).
- **Kỳ thi & import (tên đề xuất):** `ExamRound`, `ExamRoundParticipant`, `ExamRoundStatus` (DRAFT/SCHEDULED/OPEN/CLOSED, chuyển lazy); `TestSession` gắn `examRoundId` và `expiresAt`; import theo lưới tạm Redis (bấm Lưu mới ghi DB); `PasswordResetService` (OTP 6 số), `MailPort`.
- **Session/CAT:** `TestSession`, `CATEngine` (`<<service>>`, không lưu state), `EAPComputationState`, `AbilityEstimate`, `SessionResponse`, `SessionCacheState` (Redis)
- **Item Bank:** `Item` (dùng 3 enum: `Skill` / `CEFRLevel` / `ItemStatus`; **không có `source`**: nguồn câu hỏi nằm ở `ItemBatch.source` với enum `ItemBatchSource` = `AI_GENERATED`/`IMPORTED`; `Item.batchId` bắt buộc, câu seed thuộc các lô seed `IMPORTED`/`DONE`, mỗi bộ nguồn một lô)
- **Lô câu hỏi và duyệt (tên đề xuất):** `ItemBatch` (trạng thái lô: `GENERATING|IMPORTING` → `CHECKING` → `READY_TO_ASSIGN` → `IN_REVIEW` → `READY_TO_FINALIZE` → `FINAL_CHECKED` → `DONE`; `FAILED`, `PARTIAL`), `ItemBatchAssignment`, `ItemPackage` (một gói mỗi GV A trong một lô, tạo lúc Admin giao việc: `OPEN` → `SENT` → `DONE`), `ItemReviewAssignment` (giao việc theo từng câu), `ItemCheckResult` (C1/C2/C3; `PASS|SOFT|HARD`, mã lý do), `ItemEmbedding` (vector `Float[]`, cosine tính trong ứng dụng, không dùng pgvector), `ItemReviewEvent` (nhật ký kiểm toán: `APPROVE`, `REJECT`, `CONFIRM`, `REMOVE`, `CONFIRM_ALL`, `IMPORT`, `REASSIGN`, `EXTEND`, `FORCE_SEND`, `ACCEPT_FLAG`)
- **AI:** `AIExplainerService` — `explain(item: Item): Explanation`, gắn `Item`, **sinh cùng lúc sinh câu hỏi** (cùng lời gọi sinh câu của lô, **không lazy**; câu import thiếu giải thích thì sinh bổ sung theo nhóm), lưu bảng `explanations`, **1 lần/Item**, dùng chung cho mọi SV — không phải theo từng `SessionResponse` (DC-31, #60/#63/#105). Mọi lời gọi AI đi qua LLM Gateway
- **Report:** `LanguageProfile` (aggregate root, có `exportForEduZ()`), `ClassReport` (`<<service>>`)
- **Đã loại khỏi phạm vi TL (không còn trong Class Diagram):** `EduZServiceAccount`, `Institution`, `ItemBank` (`findForCAT` chuyển sang `Item`), `EduZSSOAdapter`/`EduZSSOClient`. TL chỉ dùng API Key cấu hình qua Guard/Middleware cho EduZ, không tạo bảng riêng.

Phân quyền (DC-18, DC-19, DC-27…DC-45 — thay quyết định Tuần 1 về `institution_id`): hệ thống **đơn trường**, 3 role `STUDENT`/`TEACHER`/`ADMIN`. `TEACHER` xem kết quả (báo cáo lớp lọc theo kỳ, hồ sơ SV, đổi/quên mật khẩu) và, **khi Admin giao việc**, làm **GV A** (sửa nội dung/đáp án/giải thích, duyệt hoặc từ chối câu được giao, gửi gói cho B) hoặc **GV B** (xác nhận hoặc loại bỏ câu trong gói, không sửa, không trả về A); GV xem ngân hàng câu hỏi ở chế độ chỉ xem (câu được giao). Không có role riêng "Trưởng bộ môn". `ADMIN` = Admin của trường, kế thừa `User` và có toàn bộ quyền của `TEACHER` thông qua phân quyền (không phải quan hệ kế thừa lớp): tạo lô câu hỏi (AI hoặc import file), giao việc/giao lại/chỉnh hạn/ép gửi gói, kiểm tra C3 và import cuối, xem câu `AI_REJECTED`; tạo/công bố/đóng kỳ thi, import danh sách thi, import + quản lý tài khoản SV và GV, nâng/thu hồi Admin (không thu hồi Admin cuối). **Admin không sửa nội dung câu và không gõ câu bằng form; GV không import đề.** Admin đầu tiên tạo bằng script cài đặt (trước các lô seed).

---

## Bản đồ tài liệu (đọc theo nhu cầu)

Bộ tài liệu chuẩn nằm trong `` (bản mới nhất duy nhất). Chưa chốt → `drafts/`. Bản cũ → `D:\TLCN\_ARCHIVE_20261024\` (kèm `MANIFEST_DI_CHUYEN.csv`). Riêng **nhật ký và theo dõi** nằm ở `D:\TLCN\0.docs\tracking\` (plugin `tlcn-devkit` đọc ở đó; `tracking/` là bản sao).

| Tài liệu | Nội dung |
|---|---|
| `requirements/SRS_TLCN_v3.0.md` / `.docx` | **SRS bản chuẩn** (nghiệp vụ, DB, API, quyền, BR-01…BR-30). Hai bản `.md` và `.docx` phải giống nhau |
| `requirements/20261016_MoHinhHoaYeuCau.docx` | Đặc tả 30 Use Case (mã kỳ thi UCADM15–17) |
| `design/usecase/AdaptivePlacementTest.xml` | Use Case Diagram (XMI text, sửa bằng script được) |
| `design/class/` | Class Diagram: `TLCN.drawio.xml` + `.png` (bản gọn), `ClassDiagram.puml/.mmd`, `Mo_ta_So_do_Lop_ClassDiagram.md`, `schema.prisma` (bản tham chiếu; bản thật ở `backend/backend/prisma`) |
| `design/sequence/SD_01…SD_12.xml` | Sequence Diagram (SD_03, SD_04 còn cần cập nhật) |
| `design/component-deployment/` | Component và Deployment Diagram + mô tả |
| `design/structure/` | Cấu trúc dự án đích và cấu trúc thực tế backend/frontend |
| `design/ui/` | Mô tả luồng theo role và màn hình chi tiết cho AI sinh UI; danh sách màn hình |
| `design/catengine/Luong_Hoat_Dong_CATEngine.md` | Luồng CAT Engine (số liệu minh họa) |
| `plans/` | Kế hoạch nghiệp vụ import/kỳ thi, sinh và duyệt đề AI; `cicd/` (CI/CD); `item-bank-data/` (nguồn câu hỏi, bản quyền) |
| `decisions/` | Bản chốt quyết định 16/10/2026 và phân tích shared-types (#122) |
| `process/` | Hướng dẫn rubric và tracking, playbook, quy trình nhóm |
| `drafts/` | Tài liệu **chưa chốt**; `cho-xac-nhan/` là kế hoạch Tuần 4 chờ xác nhận còn dùng hay không |
| `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` | Rubric của Khoa (bản local, không nằm trong repo) |
| `tracking/DECISIONS_LOG.md` | **Đọc trước khi tự quyết định điều chưa rõ** — lịch sử quyết định kèm lý do |
| `tracking/TRACKING.md`, `COMMITMENT_BASELINE.md`, `weekly-log/`, `feature-plans/`, `AI_USAGE_LOG.md` | Dashboard, cam kết Bước 3 (gate G1), nhật ký tuần, kế hoạch tính năng, nhật ký AI |

---

*File này canonical tại `D:\TLCN\CLAUDE.md`. Chỉ cập nhật khi tech stack/quy tắc dự án đổi thật — các quyết định nhỏ, cụ thể thuộc về `tracking/DECISIONS_LOG.md`, không viết vào đây.*
