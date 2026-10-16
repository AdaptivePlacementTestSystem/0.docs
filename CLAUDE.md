# CLAUDE.md

File này hướng dẫn Claude Code (và mọi AI Agent khác) khi làm việc trong repo này.

## Bắt đầu từ đâu (Start Here)

- **Trước bất kỳ việc gì có ý nghĩa**, đọc kỹ `process/HUONG_DAN_RUBRIC_VA_TRACKING.md` — tài liệu nền giải thích vì sao dự án có hệ thống tracking này (rubric chấm điểm của Khoa) và toàn bộ bối cảnh.
- Dự án đã kích hoạt skill **`rubric-tracker`** (plugin `tlcn-devkit`, `.claude/`) — skill này tự động nhắc các hành vi bắt buộc bên dưới khi làm việc trên file dự án. Không tắt/bỏ qua skill này.
- File này (CLAUDE.md) là bản tóm tắt nhanh — **không thay thế** `HUONG_DAN_RUBRIC_VA_TRACKING.md` hay `tracking/DECISIONS_LOG.md`.

---

## Tổng quan hệ thống

**Adaptive Placement Test — hệ thống CAT-Rasch**: hệ thống kiểm tra xếp lớp tiếng Anh thích ứng (Computerized Adaptive Testing) dùng mô hình IRT Rasch, ánh xạ năng lực sang thang CEFR. Đồ án **Tiểu luận (TL)**, 2 thành viên, 12 tuần. Một số phần đánh dấu **[KL]** (Khóa luận) — ngoài phạm vi TL, không code trừ khi có quyết định mở rộng riêng (xem `DECISIONS_LOG.md`).

> ⚠️ **Trạng thái hiện tại (2026-10-16, Tuần 5/12): ĐÃ CÓ MÃ NGUỒN KHỞI TẠO NHƯNG CHƯA CÓ GIT REPOSITORY.** `backend/backend` (NestJS; module có sẵn: ai-explainer, auth, cat-engine, health, item-bank, language-profile, reporting, test-session) và `frontend` (Next.js; route group `(student)`, `(teacher)`, `(exam)`, `(public)`) đã tồn tại, nhưng chưa `git init` ở thư mục gốc (repo `docs` này là repo git riêng cho tài liệu). Mã hiện còn theo mô hình cũ (ví dụ `item-bank` còn `APPROVED`/`PENDING_REVIEW`/`MANUAL`, `ItemSource` trong domain); `schema.prisma` và đặc tả v3.0 đã đi trước mã. Phần lớn tính năng Tuần 5 (kỳ thi, import, đổi/quên mật khẩu, sinh và duyệt đề) mới ở mức **tài liệu thiết kế**. Luôn `ls`/`git status` và đọc mã thật trước khi thao tác; không giả định lệnh build/run chạy được nếu chưa kiểm.

### Tech stack đã chốt (SRS Mục III; bản làm việc mới nhất `requirements/SRS_TLCN_v3.0.docx`; bản Final trước đó `requirements/SRS_TLCN_v2.6_Final.docx` — không sửa v2.6)

| Thành phần | Công nghệ | Ghi chú |
|---|---|---|
| Backend | NestJS (TypeScript), Clean Architecture | Dự kiến monorepo (cấu trúc đích: `work/week-05/KE_HOACH_CAU_TRUC_DU_AN.md`), `src/modules/{auth, item-bank, cat-engine, test-session, language-profile, ai-explainer, reporting}` + module mới v3.0 (tên chờ duyệt): `user-import`, `user-admin`, `exam-round`, `mail`, `item-generation` |
| Frontend | Next.js (TypeScript) | Tách repo riêng hay chung monorepo — SRS chưa quy định, hỏi trước khi khởi tạo |
| Database | PostgreSQL | Source of Truth |
| Cache / State | Redis | State machine chống race-condition khi làm bài thi + L1 cache; lưới tạm import (TTL ~30 phút); OTP; ghi async qua BullMQ |
| Email | `MailPort` + SMTP (nodemailer), đẩy qua hàng đợi BullMQ có retry | Mật khẩu tạm, OTP quên mật khẩu, email nhắc việc duyệt/xác nhận. Tiểu luận **không** làm chuông thông báo thời gian thực (chỉ email + Hộp việc). Nhà cung cấp SMTP chưa chọn (Q-5) |
| Mật khẩu / đăng nhập | argon2; mật khẩu tạm 12 ký tự; bắt buộc đổi lần đầu; đăng nhập chỉ email + mật khẩu (SSO thuộc Khóa luận) | Độ dài tối thiểu 8 (đề xuất, chờ chốt Q-4) |
| AI | Gemini Flash (qua LLM Gateway có dự phòng) | Sinh câu hỏi + giải thích (cùng lời gọi), kiểm đáp án độc lập, embedding cho lọc trùng (mô hình chưa chốt, Q-9); xem `work/week-05/KE_HOACH_SINH_VA_DUYET_DE_AI.md` |
| Calibration (offline, KHÔNG chạy trong request path) | py-irt hoặc catR API | Docker sidecar riêng |
| Gateway | Nginx | |

Module sinh câu hỏi bằng AI (`ai-question-generator`, tên module backend là đề xuất, có thể gọi `item-generation`) **thuộc phạm vi TL** theo DC-27…DC-45 / Quyết định #102–#113: Admin tạo lô (AI sinh hoặc import file lưới tạm) → AI kiểm 3 điểm (C1/C2/C3) → Admin giao việc → GV A duyệt và gửi gói → GV B xác nhận → Admin kiểm tra và import (`FINAL_APPROVED`). **Chưa triển khai**; còn mở Q-7…Q-12 (ngưỡng, bản quyền ngân hàng tham chiếu, mô hình embedding, `pg_trgm`, phạm vi tăng, test CAT với biên `irt_b` mới). Nguồn chân lý: `work/week-05/KE_HOACH_SINH_VA_DUYET_DE_AI.md` (`work/week-02/Phuong_an_sua_doi_AI.md` đã bị thay). Phạm vi tăng ⇒ phải cập nhật `tracking/COMMITMENT_BASELINE.md` trước khi ký (G1, hết Tuần 6).

---

## Quy tắc bắt buộc riêng của dự án này (quan trọng hơn code)

1. **KHÔNG tự quyết định thay** bất kỳ lựa chọn nào ảnh hưởng khả năng mở rộng/bảo trì mà SRS hoặc Class Diagram chưa quy định rõ — đặt tên, cấu trúc module, pattern, mức coupling, field cứng, đổi schema... Phải **dừng lại**, trình bày ≥2 phương án kèm trade-off, hỏi qua `AskUserQuestion`. Đây là quy tắc **tuyệt đối, không ngoại lệ**. Xem ví dụ thật đã xảy ra (rất nhiều): `tracking/DECISIONS_LOG.md`.
2. **Ghi `tracking/AI_USAGE_LOG.md`** sau mỗi lần AI sinh/sửa code hoặc tài liệu dự án có ý nghĩa — bắt buộc cho TC2.3 (chống đạo văn), hội đồng có thể hỏi bất kỳ dòng nào.
3. **Trước khi code 1 F-ID/bugfix không tầm thường:** tạo `tracking/feature-plans/<slug>.md` từ `_template.md` (xem `tracking/PROMPT_TEMPLATE_FEATURE.md`).
4. **Quy ước ngôn ngữ tài liệu — đã chốt, không tự đổi:** UML diagram (`AdaptivePlacementTest.xml`, Class Diagram) giữ **tiếng Anh** mặc định (khớp định danh code thật); đặc tả `.docx`/SRS/toàn bộ hệ thống tracking giữ **tiếng Việt**. Chỉ dịch diagram sang tiếng Việt khi được yêu cầu rõ ràng ở đúng phiên đó, không suy diễn từ ngữ cảnh (xem `DECISIONS_LOG.md` #5/#7 — đã từng dịch rồi phải đảo ngược lại vì AI tự suy diễn sai).
5. Đọc `tracking/HUONG_DAN_BAO_CAO_TUAN.md` trước khi soạn/rà soát báo cáo tuần; đọc `tracking/GIT_CONVENTIONS.md` trước khi commit (khi đã có git).
6. Không tự bịa số liệu (KPI, coverage, kết quả khảo sát) vào `TRACKING.md` — để trống/"N/A" nếu chưa đo được.
7. **Đồng bộ tài liệu thiết kế:** mỗi khi chốt/đổi phạm vi, use case, Class Diagram, schema, API hoặc màn hình, phải rà soát và cập nhật cả bộ: SRS (ghi đề xuất v2.7, không sửa bản Final trừ khi được yêu cầu rõ), đặc tả Use Case + UC Diagram, `ClassDiagram.puml` + `.mmd` + `Mo_ta_So_do_Lop_ClassDiagram.md`, `schema.prisma`, mô tả giao diện `work/week-04/` và `work/week-05/DANH_SACH_MAN_HINH_THEO_ROLE.md`, kế hoạch cấu trúc `work/week-05/KE_HOACH_CAU_TRUC_DU_AN.md`, rồi `DECISIONS_LOG`/weekly-log. SRS bản đang làm việc là `requirements/SRS_TLCN_v3.0.docx`/`.md` (ghi thay đổi vào bảng lịch sử phiên bản của SRS; không sửa v2.6 Final). Tài liệu nào hoãn thì ghi "Nợ đồng bộ tài liệu" ở weekly-log. Chi tiết: mục 4b của skill `rubric-tracker`.

---

## CATEngine — 4 hành vi lõi (đã audit & chốt Tuần 1)

Chi tiết đầy đủ: `tracking/feature-plans/f03-cat-engine.md`, `design/Luong_Hoat_Dong_CATEngine.md`.

- **`pickNextSkill()`** — chọn kỹ năng kế tiếp (Vocabulary/Grammar; Writing không thuộc TL v3.0); **round-robin cố định** (chốt qua `AskUserQuestion`, SRS không tự quy định con số này — đừng suy đoán lại).
- **`selectNextItem()`** — **Randomized Top-5 b-matching**: lọc Top-5 item `status='FINAL_APPROVED'` theo `|b_i − θ̂|` tăng dần, chọn ngẫu nhiên đều 1 trong 5 (chống lộ đề). Guard bắt buộc filter `FINAL_APPROVED` ở tầng Repository, không phải ở service. Vòng đời `Item` (một chiều): `DRAFT` → `FIRST_APPROVED` (GV A) → `SECOND_APPROVED` (GV B) → `FINAL_APPROVED` (Admin import); `REJECTED` do người loại, `AI_REJECTED` do máy loại; chỉ `FINAL_APPROVED` được CAT chọn.
- **`computeEAP()`** — Expected A Posteriori, **lưới đều 41 điểm θ ∈ [−4, +4], bước 0,2** (tích phân số kiểu hình thang; không phải Gaussian–Hermite quadrature; DC-26, Quyết định #101), Prior N(0,1); có MLE fallback guard (chỉ dùng khi ≥1 đúng và ≥1 sai trong session; clip θ về [-4, +4]).
- **`checkStoppingCriterion()`** — dừng khi (theo thứ tự ưu tiên): SE < 0.35, HOẶC đủ 25 câu, HOẶC Outlier Early Stop (θ > 1.5 hoặc θ < −2.5 kèm điều kiện hội tụ của SRS Mục 4.5, sau ≥8 câu), HOẶC hết hạn phiên: `expires_at = min(startedAt + durationMinutes của kỳ thi, closesAt)`; `durationMinutes` mặc định 45 (5–180). Quá hạn: ≥ 8 câu ⇒ `COMPLETED` + `TIMEOUT`, ít hơn ⇒ `ABANDONED`.
- **Tham số cấu hình** (đặt trong `ConfigService`/env, **KHÔNG hardcode** — SRS tự ghi chú các số này sẽ đổi sau khi có dữ liệu calibration thật): θ₀ = **−0.5** (không phải 0.0), ngưỡng SE **0.35**, max items **25**, min items trước khi Early Stop có hiệu lực **8**, khoảng `irt_b` hợp lệ của Item Bank `b_min = −4, b_max = +4` (DC-34, #107; thay `−2.5…+1.5`, vẫn là cấu hình). `−2.5` và `+1.5` chỉ còn là ngưỡng θ của Outlier Early Stop (cơ sở độ phủ ngân hàng): phải chạy lại ≥3 ca test CAT sau khi đổi (Q-12).
- Với mọi thay đổi liên quan thuật toán này (Rasch/EAP/quadrature/stopping): **luôn đối chiếu công thức với SRS trước khi merge**, viết ≥3 test case bắt buộc (toàn đúng, toàn sai, xen kẽ — SRS Mục 4.3 đã tự liệt kê).

---

## Class Diagram — nhóm entity chính

Đầy đủ: `design/Mo_ta_So_do_Lop_ClassDiagram.md`; số class/enum thay đổi theo từng phiên nên **không ghi cứng ở đây** — đếm từ sơ đồ hiện hành (sơ đồ draw.io `design/TLCN.drawio.xml` (trang `Trang-1`) đã cập nhật theo schema ngày 16/10/2026, chưa tách 2 trang; ảnh `TLCN-Trang-1.drawio.png` lỗi thời cho tới khi xuất lại).

- **User/Actor:** `AuthProvider` (interface; gói TL chỉ có `JwtAuthProvider`, đăng nhập chỉ email + mật khẩu; EduZ SSO thuộc Khóa luận), `User` (abstract; role qua enum `UserRole`: `STUDENT`/`TEACHER`/`ADMIN`; `EDUZ_SERVICE` chỉ là role của API Key cho EduZ, không phải dòng trong bảng `users`; có `mustChangePassword`, `isActive`). **Không còn `Institution`** (hệ thống đơn trường, DC-19).
- **Kỳ thi & import (tên đề xuất):** `ExamRound`, `ExamRoundParticipant`, `ExamRoundStatus` (DRAFT/SCHEDULED/OPEN/CLOSED, chuyển lazy); `TestSession` gắn `examRoundId` và `expiresAt`; import theo lưới tạm Redis (bấm Lưu mới ghi DB); `PasswordResetService` (OTP 6 số), `MailPort`.
- **Session/CAT:** `TestSession`, `CATEngine` (`<<service>>`, không lưu state), `EAPComputationState`, `AbilityEstimate`, `SessionResponse`, `SessionCacheState` (Redis)
- **Item Bank:** `Item` (dùng 3 enum: `Skill` / `CEFRLevel` / `ItemStatus`; **không có `source`**: nguồn câu hỏi nằm ở `ItemBatch.source` với enum `ItemBatchSource` = `AI_GENERATED`/`IMPORTED`; `Item.batchId` bắt buộc, câu seed thuộc các lô seed `IMPORTED`/`DONE`, mỗi bộ nguồn một lô)
- **Lô câu hỏi và duyệt (tên đề xuất):** `ItemBatch` (trạng thái lô: `GENERATING|IMPORTING` → `CHECKING` → `READY_TO_ASSIGN` → `IN_REVIEW` → `READY_TO_FINALIZE` → `FINAL_CHECKED` → `DONE`; `FAILED`, `PARTIAL`), `ItemBatchAssignment`, `ItemPackage` (một gói mỗi GV A trong một lô, tạo lúc Admin giao việc: `OPEN` → `SENT` → `DONE`), `ItemReviewAssignment` (giao việc theo từng câu), `ItemCheckResult` (C1/C2/C3; `PASS|SOFT|HARD`, mã lý do), `ItemEmbedding` (vector `Float[]`, cosine tính trong ứng dụng, không dùng pgvector), `ItemReviewEvent` (nhật ký kiểm toán: `APPROVE`, `REJECT`, `CONFIRM`, `REMOVE`, `CONFIRM_ALL`, `IMPORT`, `REASSIGN`, `EXTEND`, `FORCE_SEND`, `ACCEPT_FLAG`)
- **AI:** `AIExplainerService` — `explain(item: Item): Explanation`, gắn `Item`, **sinh cùng lúc sinh câu hỏi** (cùng lời gọi sinh câu của lô, **không lazy**; câu import thiếu giải thích thì sinh bổ sung theo nhóm), lưu bảng `explanations`, **1 lần/Item**, dùng chung cho mọi SV — không phải theo từng `SessionResponse` (DC-31, #60/#63/#105). Mọi lời gọi AI đi qua LLM Gateway
- **Report:** `LanguageProfile` (aggregate root, có `exportForEduZ()`), `ClassReport` (`<<service>>`)
- **Đã loại khỏi phạm vi TL (không còn trong Class Diagram):** `EduZServiceAccount`, `Institution`, `ItemBank` (`findForCAT` chuyển sang `Item`), `EduZSSOAdapter`/`EduZSSOClient`. TL chỉ dùng API Key cấu hình qua Guard/Middleware cho EduZ, không tạo bảng riêng.

Phân quyền (DC-18, DC-19, DC-27…DC-45 — thay quyết định Tuần 1 về `institution_id`): hệ thống **đơn trường**, 3 role `STUDENT`/`TEACHER`/`ADMIN`. `TEACHER` xem kết quả (báo cáo lớp lọc theo kỳ, hồ sơ SV, đổi/quên mật khẩu) và, **khi Admin giao việc**, làm **GV A** (sửa nội dung/đáp án/giải thích, duyệt hoặc từ chối câu được giao, gửi gói cho B) hoặc **GV B** (xác nhận hoặc loại bỏ câu trong gói, không sửa, không trả về A); GV xem ngân hàng câu hỏi ở chế độ chỉ xem (câu được giao). Không có role riêng "Trưởng bộ môn". `ADMIN` = Admin của trường, siêu tập của `Teacher`: tạo lô câu hỏi (AI hoặc import file), giao việc/giao lại/chỉnh hạn/ép gửi gói, kiểm tra C3 và import cuối, xem câu `AI_REJECTED`; tạo/công bố/đóng kỳ thi, import danh sách thi, import + quản lý tài khoản SV và GV, nâng/thu hồi Admin (không thu hồi Admin cuối). **Admin không sửa nội dung câu và không gõ câu bằng form; GV không import đề.** Admin đầu tiên tạo bằng script cài đặt (trước các lô seed).

---

## Bản đồ tài liệu (đọc theo nhu cầu)

> **Lưu ý file chỉ lưu máy (Quyết định #37):** `tracking/DECISIONS_LOG.md`, `COMMITMENT_BASELINE.md`, `TRACKING.md`, `weekly-log/Tuan-*`, `feature-plans/*` (trừ `_template.md`) và `work/` không nằm trong repo public. Khi thiếu các file này, hỏi người dùng thay vì suy đoán; `tracking/AI_USAGE_LOG.md` thì có trong repo (Quyết định #38).

| Tài liệu | Nội dung |
|---|---|
| `requirements/SRS_TLCN_v3.0.docx` (và `.md`) | **SRS bản làm việc mới nhất (16/10/2026; có phần đề xuất chờ chốt).** Bản Final trước đó: `requirements/SRS_TLCN_v2.6_Final.docx` (không sửa). Các file `SRS_TLCN*.md`, `SRS_TLCN_v2.3–2.5*.docx` ở gốc `D:\TLCN` chỉ là lịch sử, đừng đọc nhầm |
| `design/Mo_ta_So_do_Lop_ClassDiagram.md` | Mô tả đầy đủ Class Diagram |
| `design/Luong_Hoat_Dong_CATEngine.md` | Luồng hoạt động đầy đủ CAT Engine kèm ví dụ số liệu minh họa (số liệu là minh họa, không phải kết quả chạy thật) |
| `design/AdaptivePlacementTest.xml` (ảnh `UC_Overview_AdaptivePlacementTest.jpg` chỉ lưu máy) | Use Case Diagram — file `.xml` là **text XMI thuần**, sửa trực tiếp được bằng script, không cần Enterprise Architect. Ảnh JPG hiện đang lỗi thời so với `.xml`, xem `work/week-02/TRACKING_TIEN_DO.md` mục G5b |
| `requirements/20261016_MoHinhHoaYeuCau.docx` | Đặc tả Use Case v3.0 (30 bảng chi tiết, mã UCADM15–17 cho kỳ thi). Bản cũ `requirements/20260922_MoHinhHoaYeuCau.docx` (24 UC) chỉ là lịch sử |
| `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (bản local của nhóm, không nằm trong repo) | Rubric chấm điểm của Khoa — đối chiếu khi làm bất kỳ việc gì |
| `tracking/DECISIONS_LOG.md` | **Đọc trước khi tự quyết định bất kỳ điều gì chưa rõ trong SRS** — lịch sử đầy đủ quyết định thiết kế kèm lý do, phương án đã cân nhắc |
| `tracking/TRACKING.md` | Dashboard số liệu đo lường vs ngưỡng rubric Mức 3/4/5 |
| `tracking/COMMITMENT_BASELINE.md` | Cam kết Bước 3 — **phải ký trước mốc 50% thời gian đồ án** (gate nghiêm trọng nhất) |
| `tracking/weekly-log/Tuan-XX.md` | Nhật ký từng tuần |
| `tracking/feature-plans/*.md` | Kế hoạch từng tính năng (bắt buộc có trước khi code tính năng đó) |
| `work/week-02/*.md` | Sản phẩm làm việc Tuần 2 (một phần đã bị thay: `Phuong_an_sua_doi_AI.md` bởi `work/week-05/KE_HOACH_SINH_VA_DUYET_DE_AI.md`) |
| `work/week-05/20261016_BAN_CHOT_QUYET_DINH_DONG_BO_TOAN_DIEN_GUI_TEAMMATE.md` | **Quyết định chính thức 16/10/2026** (mô hình lô/gói, `ItemBatchSource`, route, lô seed). `20261016_TONG_HOP_...md` là biên bản thảo luận cũ |
| `work/week-05/KE_HOACH_CAU_TRUC_DU_AN.md` | Cấu trúc dự án đích (monorepo, modules, ma trận UC ↔ F-ID ↔ route) |
| `work/week-05/*.md` | Kế hoạch nghiệp vụ import/kỳ thi (`KE_HOACH_NGHIEP_VU_IMPORT...`), kế hoạch sinh và duyệt đề AI, danh sách màn hình theo role, tracking Tuần 5 |
| `work/week-05/PHAN_TICH_RA_SOAT_UPDATE_VA_GIAI_PHAP_ITEMBATCH_ITEMPACKAGE.md` | Rà soát mâu thuẫn giữa các tài liệu (Mục 9–11 cập nhật 16/10/2026) |

---

*File này canonical tại `CLAUDE.md` ở gốc repo `docs`. Chỉ cập nhật khi tech stack/quy tắc dự án đổi thật — các quyết định nhỏ, cụ thể thuộc về `tracking/DECISIONS_LOG.md`, không viết vào đây.*
