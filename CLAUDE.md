# CLAUDE.md

File này hướng dẫn Claude Code (và mọi AI Agent khác) khi làm việc trong repo này.

## Bắt đầu từ đâu (Start Here)

- **Trước bất kỳ việc gì có ý nghĩa**, đọc kỹ `process/HUONG_DAN_RUBRIC_VA_TRACKING.md` — tài liệu nền giải thích vì sao dự án có hệ thống tracking này (rubric chấm điểm của Khoa) và toàn bộ bối cảnh.
- Dự án đã kích hoạt skill **`rubric-tracker`** (plugin `tlcn-devkit`, `.claude/`) — skill này tự động nhắc các hành vi bắt buộc bên dưới khi làm việc trên file dự án. Không tắt/bỏ qua skill này.
- File này (CLAUDE.md) là bản tóm tắt nhanh — **không thay thế** `HUONG_DAN_RUBRIC_VA_TRACKING.md` hay `tracking/DECISIONS_LOG.md`.

---

## Tổng quan hệ thống

**Adaptive Placement Test — hệ thống CAT-Rasch**: hệ thống kiểm tra xếp lớp tiếng Anh thích ứng (Computerized Adaptive Testing) dùng mô hình IRT Rasch, ánh xạ năng lực sang thang CEFR. Đồ án **Tiểu luận (TL)**, 2 thành viên, 12 tuần. Một số phần đánh dấu **[KL]** (Khóa luận) — ngoài phạm vi TL, không code trừ khi có quyết định mở rộng riêng (xem `DECISIONS_LOG.md`).

> ⚠️ **Trạng thái hiện tại (2026-09-23, Tuần 2/12): CHƯA CÓ CODE, CHƯA CÓ GIT REPOSITORY.** Toàn bộ dự án hiện chỉ là tài liệu thiết kế (SRS, Class Diagram, Use Case Diagram + đặc tả). Không giả định có codebase để đọc/sửa — luôn `ls`/`git status` trước khi thao tác. Không bịa lệnh build/run vì chưa có gì để build.

### Tech stack đã chốt (SRS Mục III, `requirements/SRS_TLCN_v2.6_Final.docx`)

| Thành phần | Công nghệ | Ghi chú |
|---|---|---|
| Backend | NestJS (TypeScript), Clean Architecture | Dự kiến monorepo, `src/modules/{auth, item-bank, cat-engine, test-session, language-profile, ai-explainer, reporting}` |
| Frontend | Next.js (TypeScript) | Tách repo riêng hay chung monorepo — SRS chưa quy định, hỏi trước khi khởi tạo |
| Database | PostgreSQL | Source of Truth |
| Cache / State | Redis | State machine chống race-condition khi làm bài thi + L1 cache; ghi async qua BullMQ |
| AI | Gemini Flash | Dùng cho `AIExplainerService`; xem thêm `work/week-02/Phuong_an_sua_doi_AI.md` (đề xuất mở rộng, chưa triển khai) |
| Calibration (offline, KHÔNG chạy trong request path) | py-irt hoặc catR API | Docker sidecar riêng |
| Gateway | Nginx | |

`ai-question-generator/` có trong module breakdown của SRS nhưng đánh dấu **(KL)** — không thuộc phạm vi TL. **Ngoại lệ đã chốt:** một phần mở rộng nhỏ "AI-assisted item drafting từ Ngân hàng tham chiếu" đã được duyệt phạm vi (Quyết định #8/#9) nhưng **chưa triển khai**, còn nhiều câu hỏi con chưa chốt — xem `work/week-02/Phuong_an_sua_doi_AI.md` trước khi động vào phần này.

---

## Quy tắc bắt buộc riêng của dự án này (quan trọng hơn code)

1. **KHÔNG tự quyết định thay** bất kỳ lựa chọn nào ảnh hưởng khả năng mở rộng/bảo trì mà SRS hoặc Class Diagram chưa quy định rõ — đặt tên, cấu trúc module, pattern, mức coupling, field cứng, đổi schema... Phải **dừng lại**, trình bày ≥2 phương án kèm trade-off, hỏi qua `AskUserQuestion`. Đây là quy tắc **tuyệt đối, không ngoại lệ**. Xem ví dụ thật đã xảy ra (rất nhiều): `tracking/DECISIONS_LOG.md`.
2. **Ghi `tracking/AI_USAGE_LOG.md`** sau mỗi lần AI sinh/sửa code hoặc tài liệu dự án có ý nghĩa — bắt buộc cho TC2.3 (chống đạo văn), hội đồng có thể hỏi bất kỳ dòng nào.
3. **Trước khi code 1 F-ID/bugfix không tầm thường:** tạo `tracking/feature-plans/<slug>.md` từ `_template.md` (xem `tracking/PROMPT_TEMPLATE_FEATURE.md`).
4. **Quy ước ngôn ngữ tài liệu — đã chốt, không tự đổi:** UML diagram (`design/AdaptivePlacementTest.xml`, Class Diagram) giữ **tiếng Anh** mặc định (khớp định danh code thật); đặc tả `.docx`/SRS/toàn bộ hệ thống tracking giữ **tiếng Việt**. Chỉ dịch diagram sang tiếng Việt khi được yêu cầu rõ ràng ở đúng phiên đó, không suy diễn từ ngữ cảnh (xem `DECISIONS_LOG.md` #5/#7 — đã từng dịch rồi phải đảo ngược lại vì AI tự suy diễn sai).
5. Đọc `tracking/HUONG_DAN_BAO_CAO_TUAN.md` trước khi soạn/rà soát báo cáo tuần; đọc `tracking/GIT_CONVENTIONS.md` trước khi commit (khi đã có git).
6. Không tự bịa số liệu (KPI, coverage, kết quả khảo sát) vào `TRACKING.md` — để trống/"N/A" nếu chưa đo được.

---

## CATEngine — 4 hành vi lõi (đã audit & chốt Tuần 1)

Chi tiết đầy đủ: `tracking/feature-plans/f03-cat-engine.md`, `design/Luong_Hoat_Dong_CATEngine.md`.

- **`pickNextSkill()`** — chọn kỹ năng kế tiếp (Vocabulary/Grammar/Writing); **round-robin cố định** (chốt qua `AskUserQuestion`, SRS không tự quy định con số này — đừng suy đoán lại).
- **`selectNextItem()`** — **Randomized Top-5 b-matching**: lọc Top-5 item `status='APPROVED'` theo `|b_i − θ̂|` tăng dần, chọn ngẫu nhiên đều 1 trong 5 (chống lộ đề). Guard bắt buộc filter `APPROVED` ở tầng Repository, không phải ở service.
- **`computeEAP()`** — Expected A Posteriori, 41-point Gaussian-Hermite quadrature, Prior N(0,1); có MLE fallback guard (chỉ dùng khi ≥1 đúng và ≥1 sai trong session; clip θ về [-4, +4]).
- **`checkStoppingCriterion()`** — dừng khi (theo thứ tự ưu tiên): SE < 0.35, HOẶC đủ 25 câu, HOẶC Outlier Early Stop (θ > 1.5 hoặc θ < −2.5 sau ≥8 câu), HOẶC timeout 45 phút.
- **Tham số cấu hình** (đặt trong `ConfigService`/env, **KHÔNG hardcode** — SRS tự ghi chú các số này sẽ đổi sau khi có dữ liệu calibration thật): θ₀ = **−0.5** (không phải 0.0), ngưỡng SE **0.35**, max items **25**, min items trước khi Early Stop có hiệu lực **8**, boundary Item Bank `b_min = −2.5, b_max = +1.5`.
- Với mọi thay đổi liên quan thuật toán này (Rasch/EAP/quadrature/stopping): **luôn đối chiếu công thức với SRS trước khi merge**, viết ≥3 test case bắt buộc (toàn đúng, toàn sai, xen kẽ — SRS Mục 4.3 đã tự liệt kê).

---

## Class Diagram — nhóm entity chính

Đầy đủ (31 class / 10 enum): `design/Mo_ta_So_do_Lop_ClassDiagram.md` (đối chiếu ảnh gốc `design/TLCN-Trang-1.drawio.png`).

- **User/Actor:** `Institution`, `AuthProvider` (interface), `User` (abstract; role qua enum `UserRole`: `STUDENT`/`TEACHER`/`ADMIN`/`EDUZ_SERVICE`)
- **Session/CAT:** `TestSession`, `CATEngine` (`<<service>>`, không lưu state), `EAPComputationState`, `AbilityEstimate`, `SessionResponse`, `SessionCacheState` (Redis)
- **Item Bank:** `Item` (dùng 4 enum: `Skill` / `CEFRLevel` / `ItemStatus` / `ItemSource`)
- **AI:** `AIExplainerService` — `explain(item: Item): Explanation`, **lazy** (chạy khi SV đầu tiên xem kết quả, không phải lúc tạo câu hỏi), sinh **1 lần/Item** rồi cache, dùng chung cho mọi SV — không phải theo từng `SessionResponse`
- **Report:** `LanguageProfile` (aggregate root, có `exportForEduZ()`), `ClassReport` (`<<service>>`)
- **Đã loại khỏi phạm vi TL:** `EduZServiceAccount` (dời Khóa luận; TL chỉ dùng API Key cấu hình qua Guard/Middleware, không tạo bảng riêng)

Phân quyền: `Admin` = siêu tập của `Teacher` + quản trị hệ thống, **không giới hạn `institution_id`** (đã chốt qua `AskUserQuestion` Tuần 1 — SRS không tự quy định phần này rõ ràng).

---

## Bản đồ tài liệu (đọc theo nhu cầu)

> **Lưu ý file chỉ lưu máy (Quyết định #37):** `tracking/DECISIONS_LOG.md`, `COMMITMENT_BASELINE.md`, `TRACKING.md`, `weekly-log/Tuan-*`, `feature-plans/*` (trừ `_template.md`) và `work/` không nằm trong repo public. Khi thiếu các file này, hỏi người dùng thay vì suy đoán; `tracking/AI_USAGE_LOG.md` thì có trong repo (Quyết định #38).

| Tài liệu | Nội dung |
|---|---|
| `requirements/SRS_TLCN_v2.6_Final.docx` | **SRS bản mới nhất — luôn dùng bản này.** Các bản SRS cũ (v2.3–2.5) không nằm trong repo; nếu gặp thì chỉ là lịch sử, đừng đọc nhầm |
| `design/Mo_ta_So_do_Lop_ClassDiagram.md` | Mô tả đầy đủ Class Diagram |
| `design/Luong_Hoat_Dong_CATEngine.md` | Luồng hoạt động đầy đủ CAT Engine kèm ví dụ số liệu minh họa (số liệu là minh họa, không phải kết quả chạy thật) |
| `design/AdaptivePlacementTest.xml` (ảnh `UC_Overview_AdaptivePlacementTest.jpg` chỉ lưu máy) | Use Case Diagram — file `.xml` là **text XMI thuần**, sửa trực tiếp được bằng script, không cần Enterprise Architect. Ảnh JPG hiện đang lỗi thời so với `.xml`, xem `work/week-02/TRACKING_TIEN_DO.md` mục G5b |
| `requirements/20260922_MoHinhHoaYeuCau.docx` | Đặc tả đầy đủ 24 Use Case |
| `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (bản local của nhóm, không nằm trong repo) | Rubric chấm điểm của Khoa — đối chiếu khi làm bất kỳ việc gì |
| `tracking/DECISIONS_LOG.md` | **Đọc trước khi tự quyết định bất kỳ điều gì chưa rõ trong SRS** — lịch sử đầy đủ quyết định thiết kế kèm lý do, phương án đã cân nhắc |
| `tracking/TRACKING.md` | Dashboard số liệu đo lường vs ngưỡng rubric Mức 3/4/5 |
| `tracking/COMMITMENT_BASELINE.md` | Cam kết Bước 3 — **phải ký trước mốc 50% thời gian đồ án** (gate nghiêm trọng nhất) |
| `tracking/weekly-log/Tuan-XX.md` | Nhật ký từng tuần |
| `tracking/feature-plans/*.md` | Kế hoạch từng tính năng (bắt buộc có trước khi code tính năng đó) |
| `work/` (chỉ lưu máy) | Sản phẩm làm việc Tuần 2: sửa Use Case Diagram, báo cáo phương án AI item drafting |

---

*File này canonical tại `CLAUDE.md` ở gốc repo `docs`. Chỉ cập nhật khi tech stack/quy tắc dự án đổi thật — các quyết định nhỏ, cụ thể thuộc về `tracking/DECISIONS_LOG.md`, không viết vào đây.*
