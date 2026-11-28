# KẾ HOẠCH KIỂM THỬ PHẦN MỀM (TEST PLAN)
## Hệ thống Kiểm tra xếp lớp tiếng Anh thích ứng CAT–Rasch (v3.0 — Phạm vi Tiểu luận)

- **Mã tài liệu:** `TP-TLCN-v1.0`
- **Ngày ban hành:** 2026-11-28
- **Nhóm thực hiện:** Huỳnh Hoài Phương & Đăng (Nhóm 2 thành viên — 12 tuần Tiểu luận)
- **Nguồn đối chiếu:**
  - `0.docs/requirements/SRS_TLCN_v3.0.md` (22 chức năng Tiểu luận `F-01..F-10`, `F-18..F-29`; Business Rules `BR-01..BR-30`; NFR Mục 15.1–15.3)
  - `0.docs/decisions/20261128_BAN_CHOT_QUYET_DINH_THONG_NHAT_NHOM.md` (Q1–Q8 & thống nhất kỹ thuật)
  - Rubric Đồ án CNPM V2-1 (TC2.5 trang 8 & 14; Mục 6 Chống đạo văn trang 16; Gate G5 & Mục 8 STT 8 trang 17)

---

## 3.1. Tổng quan

### 3.1.1. Mục đích
Xác minh tính đúng đắn nghiệp vụ, độ chính xác học thuật của thuật toán **CAT–Rasch (1PL, EAP lưới đều 41 điểm $[-4, +4]$ bước $0.2$)**, tính an toàn phân quyền RBAC/IDOR, tính toàn vẹn dữ liệu giao dịch đồng thời (PostgreSQL + Redis) và hiệu năng đáp ứng NFR trước khi nghiệm thu và bảo vệ đồ án.

### 3.1.2. Phạm vi kiểm thử
1. **Trong phạm vi Tiểu luận — 22 chức năng (`F-01..F-10`, `F-18..F-29`):**
   - Nhóm Xác thực & Phân quyền (`F-01`, `F-21`)
   - Nhóm Sinh viên & CAT Engine (`F-03`, `F-04`, `F-05`, `F-06`, `F-08`)
   - Nhóm Giảng viên — Báo cáo & Duyệt câu hỏi 2 vòng GV A/B (`F-02`, `F-09`, `F-26`, `F-27`)
   - Nhóm Quản trị viên — Dashboard, Tài khoản, Import lưới tạm Redis, Kỳ thi, Roster, Sinh lô AI + AI Question Tagging (`F-10`), Import đề, Giao việc, Kiểm C1/C2/C3 & Import cuối (`F-10`, `F-18..F-20`, `F-22..F-25`, `F-28`, `F-29`)
   - Nhóm Tích hợp M2M EduZ (`F-07`: `GET /api/v1/placement-profiles/:studentCode/eduz-export`)
   - Yêu cầu phi chức năng (NFR Mục 15.1–15.3: độ trễ p95, rate-limit, CSV Injection, bảo mật JWT/API Key)
2. **Ngoài phạm vi Tiểu luận (loại trừ rõ ràng — dành cho Khóa luận `[KL]`):**
   - Kỹ năng `Writing` (TL chỉ triển khai `Vocabulary` và `Grammar`).
   - Đa trường / Multi-tenant (`Institution`, đã bỏ theo DC-19).
   - Đăng nhập một lần EduZ SSO & bảng `EduZServiceAccount` (TL dùng API Key qua Guard/Middleware).
   - Chuông thông báo thời gian thực WebSocket (TL dùng email + Hộp việc + nhắc hạn định kỳ).

### 3.1.3. Giới thiệu hệ thống được kiểm thử
- **Backend (`backend/`):** NestJS (TypeScript), Clean Architecture, PostgreSQL + Prisma (Source of Truth), Redis (State machine CAT, lưới tạm TTL 30 phút, OTP, rate-limit), LLM Gateway (OpenAI-compatible / Gemini), Nodemailer/Brevo SMTP.
- **Frontend (`frontend/`):** Next.js (App Router) + React + TypeScript + BFF Proxy (`/api/proxy/[...path]`, `/api/auth/*`).
- **Tài liệu & Quản lý kiểm thử (`0.docs/`):** YAML Test Cases (`0.docs/testing/cases/*.yaml`) → `TLCN_TestCases.xlsx`, và GitHub Issues tập trung `AdaptivePlacementTestSystem/0.docs` → `DEFECT_LOG.md`.

---

## 3.2. Chiến lược kiểm thử

### 3.2.1. Các tầng & kiểu kiểm thử (≥ 4 tầng theo Rubric Mức 5)
| Tầng | Phạm vi & Mục tiêu | Công cụ thực tế | Tiêu chí đạt |
|---|---|---|---|
| **Tầng 1 — Unit Test** | Thuật toán `CATEngine` (3 ca bắt buộc SRS 4.3, Outlier Early Stop $\ge 8$ câu + $\Delta\text{SE} < 0.01$ 3 câu, clip $[-4,+4]$), use-case, domain validation, guard, component FE | **Vitest** + **@vitest/coverage-v8** + **Testing Library** | **Line coverage ≥ 70%** cho toàn bộ module core BE & FE (exclude `src/mocks/**` ở FE) |
| **Tầng 2 — Integration Test** | Giao dịch PostgreSQL thật (khóa nguyên tử Admin cuối, race công bố/đóng kỳ, `RosterImportEvent` idempotency, Q1–Q8 `batchRevision`, `reassign-confirmer`, `cancel-pending`, `ai_call_count` trần 250) và Redis thật (lưới tạm TTL, xóa dòng) | **Vitest E2E** (`vitest.config.e2e.ts`) + **Supertest** + Docker Postgres/Redis | 100% pass trên CI BE (sau khi bật `prisma migrate deploy` + `npm run test:e2e`) |
| **Tầng 3 — API / Contract Test** | Hợp đồng OpenAPI 3.0 giữa BE và FE, phát hiện breaking change, bảo mật RBAC/IDOR (401/403), M2M API Key (`401`/`200`) | `check-openapi-coverage.cjs`, `test-openapi-contract.cjs`, `check-api-types.cjs`, Supertest | 0 breaking change, 100% pass trên CI |
| **Tầng 4 — E2E Trình duyệt (UI + Backend thật)** | 4–5 luồng người dùng đầu-cuối trên trình duyệt chạy backend + DB thật (không dùng `MOCK_API=1`): Auth/RBAC, Admin kỳ thi & Roster, SV thi CAT + Kết quả/Radar, Duyệt câu 2 vòng A→B→C3, Báo cáo/Tra cứu | **Playwright** (`playwright.admin-real.config.ts` / real config) | 100% kịch bản E2E thật pass, lưu log + ảnh chụp + SHA |
| **Tầng 5 — Phi chức năng & Pilot Smoke** | Độ trễ NFR (`submit+next-item p95 < 300ms`, `computeEAP < 50ms`, `Profile API p95 < 500ms`, `Item Bank query < 20ms`), rate-limit (429), CSV Injection, Pilot Smoke Test Gemini + Brevo SMTP có kiểm soát ngân sách | Script đo p95 / k6, `oxlint`, `eslint`, `tsc`, `gitleaks` | Đạt ngưỡng NFR SRS 15.1–15.3; 0 lỗi Blocker/Critical |

### 3.2.2. Quy trình quản lý Defect & Regression Test
1. Mọi lỗi phát hiện từ 28/11/2026 mở GitHub Issue tại **`AdaptivePlacementTestSystem/0.docs`** theo mẫu `.github/ISSUE_TEMPLATE/defect.yml` (14 trường chuẩn Bảng 6.2).
2. Khi sửa lỗi trên nhánh `develop` của `backend`/`frontend`, PR ghi `Refs AdaptivePlacementTestSystem/0.docs#<id>`.
3. Sau khi merge, người sửa thêm/chạy **Regression Test**, bình luận block `### Resolution & Regression` (`Fix PR / Commit`, `Root Cause`, `Regression Test Ref`, `Verified By & Date`, `CI Run Link`) và gắn label `status:fixed`.
4. Thành viên còn lại re-test trên bản hợp nhất → gắn `status:verified` và **đóng Issue thủ công**.
5. Trước khi nghiệm thu cuối kỳ, chạy **full regression suite** trên CI (BE & FE), đảm bảo **100% test pass** và **0 Blocker/Critical còn mở**, rồi chạy `export_defect_log.py` xuất `DEFECT_LOG.md`.

---

## 3.3. Tài nguyên & Môi trường kiểm thử

### 3.3.1. Phân công nhân sự (2 thành viên — review chéo 100%)
| Thành viên | Nhóm Test Case viết (`Created By`) | Nhóm Test Case rà soát (`Reviewed By`) | Trách nhiệm chính |
|---|---|---|---|
| **Phương** | `ADM_001..028` (Admin & `F-10`), 1/2 `AUTH`, `M2M`, `NFR` | `STU_001..016`, `TCH_001..012`, 1/2 `AUTH`, `M2M`, `NFR` | CI/CD, Admin/Exam/AI Generation, chạy `build_testcases_xlsx.py` & `export_defect_log.py` |
| **Đăng** | `STU_001..016` (Student & CAT), `TCH_001..012` (Teacher Review), 1/2 `AUTH`, `M2M`, `NFR` | `ADM_001..028`, 1/2 `AUTH`, `M2M`, `NFR` | CAT Engine ($\Delta\text{SE} < 0.01$), Student/Teacher flows, đối chiếu Coverage & E2E |

### 3.3.2. Môi trường kiểm thử
- **Local Docker:** PostgreSQL 16 + Redis 7 tách biệt cho test, Node.js 24, Python 3.10+ (`pyyaml`, `openpyxl`).
- **CI GitHub Actions:** `ubuntu-latest` với service container `postgres:16-alpine` & `redis:7-alpine` chạy trên mọi PR/push vào `develop`/`main`.
- **Staging / Demo:** Môi trường triển khai công khai (ghi rõ URL, OS, trình duyệt khi thực thi B6).

---

## 3.4. Test Milestones (Lộ trình B2 → B7)

| Chặng | Nội dung chính | Hạn dự kiến | Tiêu chí hoàn thành |
|---|---|---|---|
| **B2** | Dựng `0.docs/testing/`, `_schema.yaml`, `build_testcases_xlsx.py`, `export_defect_log.py`, `defect.yml` | 2026-11-28 *(Hoàn thành)* | Sinh Excel 25×11 + `Summary` & xuất `DEFECT_LOG.md` thành công |
| **B3** | Lập bảng `F-ID → AC-ID` (22 chức năng TL), viết `KE_HOACH_KIEM_THU_TLCN.md` & 6 file YAML (~68 TC) | 2026-11-28 *(Đang hoàn tất)* | `build_testcases_xlsx.py --strict` đạt 0 lỗi, `% Automation ≥ 70%` |
| **B4** | Merge 3 nhánh (`feat/admin-exam-rounds` → `feat/admin-ai-review` → `feat/teacher-item-review`), sửa CAT $\Delta\text{SE} < 0.01$ & EduZ guard, bật `prisma migrate deploy` + `test:e2e` trên CI BE, đo NFR p95 & Pilot Smoke | `[Chốt với Đăng]` | CI BE & FE xanh; có log p95 + Pilot + SHA trong `testing/evidence/` |
| **B5** | Bù Line coverage ≥ 70% cho toàn bộ core BE & FE (exclude `src/mocks/**`), dọn `features/items` legacy, hoàn thiện 4–5 luồng Playwright thật | `[Chốt với Đăng]` | 100% module core BE & FE đạt Line coverage ≥ 70%; xuất `BAO_CAO_DO_PHU_MA.md` |
| **B6** | Thực thi bộ ~68 TC trên môi trường thật, quản lý Defect + Regression trên `0.docs`, chạy full regression CI cuối | `[Chốt với Đăng]` | `TLCN_TestCases.xlsx` 100% kết quả thật; `DEFECT_LOG.md` có 0 Blocker/Critical mở; CI cuối pass 100% |
| **B7** | Cập nhật `TRACKING.md`, `evidence-checklist.md` (mục 8), `AI_USAGE_LOG.md`, `weekly-log`, đưa biểu đồ vào slide TC3 | `[Chốt với Đăng]` | Đủ 5/5 sản phẩm minh chứng TC2.5 sẵn sàng bảo vệ |

---

## 3.5. Bảng ánh xạ Acceptance Criteria cho 22 chức năng Tiểu luận (`F-ID → AC-ID`)

> Bảng này là chuẩn truy vết chung cho **TC2.1** (100% chức năng có Acceptance Criteria) và **TC2.5** (trường `ac_ref` trong mọi Test Case YAML).

| F-ID | Tên chức năng (SRS v3.0) | Mã AC (`ac_ref`) | Tiêu chí chấp nhận cốt lõi (Given / When / Then) |
|---|---|---|---|
| **F-01** | Đăng nhập, đổi MK lần đầu, quên MK OTP, phân quyền | `AC-F01-01..06` | Đăng nhập đúng trả JWT + `mustChangePassword`; sai email/MK trả cùng `401` (không lộ email); sai 5 lần trả `429`; tài khoản khóa trả `403` & JWT cũ bị `401` ngay; đổi MK thỏa chính sách 8+ ký tự (hoa/thường/số/đặc biệt); quên MK luôn trả `200` (BR-14), OTP sai 5 lần bị hủy |
| **F-02** | Tra cứu hồ sơ & lịch sử thi sinh viên (GV/Admin) | `AC-F02-01..02` | GV và Admin tra cứu được hồ sơ & lịch sử của SV; SV chỉ xem được của chính mình (`me`), cố xem SV khác bị `403` |
| **F-03** | Thuật toán thích ứng CAT–Rasch (1PL, EAP 41 điểm) | `AC-F03-01..06` | `pickNextSkill` luân phiên Vocab/Grammar; `selectNextItem` Top-5 ngẫu nhiên chỉ lấy `FINAL_APPROVED` (`irt_b ∈ [-4,+4]`); EAP 41 điểm đạt 3 ca bắt buộc SRS 4.3 (toàn đúng/toàn sai/xen kẽ); dừng khi `SE < 0.35`, đủ 25 câu, hoặc Outlier ($\ge 8$ câu + $\theta > 1.5$ hoặc $< -2.5$ + $\Delta\text{SE} < 0.01$ trong 3 câu liên tiếp) |
| **F-04** | Phiên thi CAT (bắt đầu, nộp bài, resume, timeout) | `AC-F04-01..06` | Chỉ `STUDENT` thuộc danh sách kỳ `OPEN` được bắt đầu phiên (`ADMIN`/`TEACHER` bị `403`); không lộ đáp án/`irt_b` khi thi/resume; chống IDOR (`403`); quá hạn $\ge 8$ câu → `COMPLETED+TIMEOUT`, $< 8$ câu → `ABANDONED`; mất Redis tự khôi phục từ DB |
| **F-05** | Giải thích đáp án bằng AI (`AIExplainer`) | `AC-F05-01..02` | Mỗi `Item` có 1 lời giải dùng chung; SV xem được lời giải chi tiết sau khi hoàn thành phiên thi (màn Review) |
| **F-06** | Sinh Language Profile & lịch sử thi SV | `AC-F06-01..02` | Sau khi hoàn thành phiên thi, sinh `LanguageProfile` chứa CEFR, $\theta$, SE, CI 95%, `skillProfiles`, `errorPatterns`; màn lịch sử hiển thị đủ trạng thái `COMPLETED`/`TIMEOUT`/`ABANDONED` |
| **F-07** | Xuất `LanguageProfile` M2M cho EduZ | `AC-F07-01..03` | Endpoint `GET /api/v1/placement-profiles/:studentCode/eduz-export`: thiếu `X-Eduz-API-Key` → `401`; sai key → `401`; đúng key → `200` trả JSON đúng hợp đồng; không dùng fallback secret hardcode |
| **F-08** | Student Result Dashboard (Kết quả & Radar/Gợi ý) | `AC-F08-01..02` | Hiển thị huy hiệu CEFR, $\theta$/SE/CI 95%, tỉ lệ đúng theo kỹ năng (Q-D), cảnh báo biên (`boundaryEffect`), chủ đề cần cải thiện & gợi ý học |
| **F-09** | Teacher Class Report (Báo cáo lớp & Export CSV) | `AC-F09-01..03` | GV và Admin xem được phân phối CEFR & `errorPatterns` lọc theo `examRoundId` (UUID); xuất CSV vô hiệu hóa công thức `= + - @` (chống CSV Injection) |
| **F-10** | AI Question Tagging (AI tự gán `topic_tag`) | `AC-F10-01..02` | Khi tạo lô AI bỏ trống `topicTag`, AI tự gán `topicTag` hợp lệ (`≤ 50` ký tự) lưu xuống `items.topic_tag`; khi truyền `topicTag` cố định, toàn bộ câu sinh giữ đúng `batch.topicTag` |
| **F-18** | Quản lý & tạo tài khoản SV/GV đơn lẻ | `AC-F18-01..03` | Chỉ `ADMIN` được tạo/sửa SV/GV; sinh MK tạm 12 ký tự (BR-05), `mustChangePassword = true`, gửi email sau khi lưu; trùng email/MSSV/Mã GV trả `409` kèm tên trường |
| **F-19** | Quản lý kỳ thi (`ExamRound`) | `AC-F19-01..05` | Tạo `DRAFT` đúng khung giờ & thời lượng (5–180p); công bố chỉ khi có $\ge 1$ SV và `opensAt` tương lai (BR-08); trạng thái hiệu lực lazy (`DRAFT`/`SCHEDULED`/`OPEN`/`CLOSED`); kỳ đã công bố không đổi tên; đóng thủ công giữ nguyên phiên đang chạy (BR-12) |
| **F-20** | Import danh sách sinh viên thi (Roster lưới tạm Redis) | `AC-F20-01..04` | Tải mẫu & upload `.xlsx` kiểm tra định dạng/kích thước (≤ 2MB nén, ≤ 20MB giải nén)/công thức; cô lập lưới theo `(adminId, roundId)`; lưu idempotent bằng `operationId` (`RosterImportEvent`) ghi transaction PostgreSQL |
| **F-21** | Đổi mật khẩu bắt buộc lần đầu & chính sách MK | `AC-F21-01..02` | User còn `mustChangePassword = true` gọi endpoint thường bị chặn `403 PASSWORD_CHANGE_REQUIRED`; đổi MK thành công xóa cờ, cấp token mới và thu hồi token cũ |
| **F-22** | Quản lý tài khoản: khóa/mở khóa, gửi lại MK tạm, đổi role Admin | `AC-F22-01..03` | Khóa/mở khóa nguyên tử; không tự khóa mình, không khóa/thu hồi Admin cuối (`409` kể cả khi gọi đồng thời); gửi lại MK tạm không áp dụng cho Admin (`403`) |
| **F-23** | Import tài khoản SV/GV bằng file Excel (lưới tạm Redis) | `AC-F23-01..03` | Upload nhiều file cộng dồn vào lưới tạm Redis theo `(adminId, kind)`, phân tách dòng hợp lệ/lỗi/trùng DB; hết TTL trả `410`, lưới rỗng trả `422`; bấm Lưu chạy nền tạo tài khoản + gửi email |
| **F-24** | Tạo lô câu hỏi bằng AI & Kiểm tra C1/C2 | `AC-F24-01..04` | Tạo lô + job nguyên tử (idempotent theo `operationId`), lấy 3–5 câu mẫu `FINAL_APPROVED`, kiểm trần 250 lượt AI nguyên tử; chạy C1 (luật cứng + T1/T2/T3 + G5 độc lập); lô 0 câu hợp lệ → `FAILED` |
| **F-25** | Import đề từ file Excel vào lưới tạm Redis | `AC-F25-01..03` | Validate định dạng/zip bomb/tiêu đề/công thức; chia tự động tối đa 50 câu/lô khi Lưu (`save` idempotent), sinh job kiểm tra C1/C2 |
| **F-26** | GV A duyệt/sửa/từ chối câu hỏi được giao | `AC-F26-01..04` | GV A chỉ thấy & thao tác câu `DRAFT` được giao (`403` ngoài phân công); sửa `DRAFT` chạy lại luật cứng + T1–T2 (`422` nếu vi phạm BR-27); từ chối bắt buộc có `comment`; không sửa được câu đã `FIRST_APPROVED` |
| **F-27** | GV B xác nhận/loại câu hỏi (`FIRST_APPROVED`) | `AC-F27-01..04` | Một GV B chung cấp lô thấy ngay câu khi GV A duyệt; GV B không sửa nội dung; loại bỏ bắt buộc có `comment`; `confirm-all` ghi 1 sự kiện audit cấp lô và chỉ áp cho câu đủ điều kiện |
| **F-28** | Giao việc, giao lại, đổi hạn, hủy tồn đọng & Kiểm C3/Import cuối | `AC-F28-01..06` | `assign-preview` trả `batchRevision` (chặn revision cũ — BR-23), cấm GV B thuộc nhóm A; `reassign` chỉ cho `DRAFT` + `reason` (BR-22); `reassign-confirmer` đổi B nguyên tử + thu hồi quyền B cũ + outbox; `PATCH /deadlines` bắt buộc `reason` (BR-24); `cancel-pending` + `reason` (BR-29); C3 phát hiện stale khi Bank đổi, import từng phần (`PARTIALLY_IMPORTED`) vs toàn phần (`DONE`) |
| **F-29** | Admin Dashboard Tổng quan | `AC-F29-01..02` | Chỉ `ADMIN` truy cập (`403` với SV/GV); trả đúng 5 chỉ số định nghĩa (SV đã thi distinct, phân phối 6 mức CEFR, 6 trạng thái câu, lô cần xử lý, lọc theo `examRoundId`) |

---

## 3.6. Đánh giá rủi ro kiểm thử & Biện pháp giảm thiểu

| Mã rủi ro | Mô tả rủi ro | Biện pháp giảm thiểu |
|---|---|---|
| **R-T1** | Sai số học thuật ở `CATEngine` (đặc biệt điều kiện Outlier $\Delta\text{SE} < 0.01$ 3 câu) | Sửa code khớp SRS Mục 4.5 ở B4; bắt buộc pass 3 ca SRS 4.3 + ca Outlier trong CI |
| **R-T2** | Lệch tích hợp khi hợp nhất 3 nhánh (`feat/admin-exam-rounds`, `feat/admin-ai-review`, `feat/teacher-item-review`) | Merge tuần tự vào `develop`, gỡ controller duyệt câu trùng, chạy lại `openapi:generate` + toàn bộ regression suite |
| **R-T3** | Coverage thực tế thấp hơn ngưỡng 70% ở một số module core (BE 61,30%, FE 67,85% ngày 28/11) | Theo dõi sát bảng bù coverage theo từng module ở B5; exclude `src/mocks/**` và dọn `features/items` legacy |
| **R-T4** | Phụ thuộc API bên thứ ba (Gemini 503 / Brevo SMTP) làm chập chờn CI | Dùng fake/stub provider cho Unit/Integration trên CI; tách riêng **Pilot Smoke Test** có kiểm soát ngân sách trước demo |
| **R-T5** | Nguy cơ vi phạm trung thực minh chứng (lỗi V4 — điền khống `Pass` hoặc tạo Issue lùi ngày) | Giữ `Not executed` cho mọi TC chưa chạy; tách riêng mục lịch sử lỗi Git trước 28/11; kiểm chứng `spec_ref` + `test_name` tự động bằng `--strict` |
