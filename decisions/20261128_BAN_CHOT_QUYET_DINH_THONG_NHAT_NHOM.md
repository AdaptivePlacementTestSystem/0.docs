# Bản Chốt Quyết Định Thống Nhất Nhóm (28/11/2026)

- **Ngày ban hành:** 28/11/2026  
- **Thành viên thống nhất:** **Đăng** (đảm nhận `UCSV*`, `UCGV*`, hệ thống chung/CAT/Teacher Review) và **Phương** (đảm nhận `UCADM*`, `item-generation`, `exam-round`, `user-admin`).  
- **Căn cứ đối chiếu:**  
  1. Bảng chốt hai chiều Q1–Q8 và mở rộng Mục 14–23 (`20261127_BANG_CHOT_PHUONG_DANG_Q1_Q8 (1).md`).  
  2. Gói bàn giao `handoff_item_generation_cho_Dang` (`feat/admin-ai-review` commit `9aea9e8`: `schema.prisma`, 16 migrations, danh sách route thực tế, `reasonCodes`, `DECISIONS_LOG.md` tới dòng 215).  
  3. Gói bàn giao `handoff_docs_BR08_BR12_cho_Dang` (cập nhật `BR-08`, `BR-12`, `S21`, `participants/import/template`).  
  4. Biên bản bổ sung Q1–Q8 ngày 27/11 (`decisions/20261127_BO_SUNG_Q1_Q8_VONG_DOI_LO_VA_API.md`).

> **Trạng thái hiệu lực:** Tài liệu này là **Nguồn sự thật duy nhất (Single Source of Truth)** cho đặc tả (`0.docs`), gói dùng chung (`@apt/shared-types` v3.1.0), và schema/migration Prisma (`backend` nhánh `chore/sync-prisma-schema-q1-q8`) để hai thành viên tiếp tục phát triển Backend & Frontend. Mọi thay đổi vận hành/AI chưa kiểm chứng runtime đều được đánh dấu rõ ràng ở trạng thái **pilot / chưa kiểm chứng**.

---

## I. Kiến trúc dữ liệu & Hợp đồng `@apt/shared-types` (v3.1.0)

### 1. Enum `ReviewAction` — Chuẩn hóa 12 giá trị (thay thế biên bản 25/11)
| Phạm vi ghi nhận | Giá trị hợp lệ | Quy tắc `item_id` & `details` |
|---|---|---|
| **Cấp câu hỏi** | `APPROVE`, `REJECT`, `CONFIRM`, `REMOVE`, `ASSIGN`, `REASSIGN` *(đổi GV A cho câu `DRAFT`)*, `ACCEPT_FLAG`, `IMPORT` | `item_id NOT NULL` |
| **Cấp lô (`ItemBatch`)** | `CONFIRM_ALL`, `UPDATE_DUE_DATE`, `CANCEL_PENDING`, `REASSIGN_CONFIRMER` *(đổi GV B chung)* | `item_id = NULL`, kèm `details JSONB` (danh sách `itemIds`, số lượng, người/hạn cũ–mới, `reason`) |

- **Bỏ `ReviewAction.EDIT`:** Thay đổi nội dung/đáp án/giải thích bởi GV A đã lưu vết đầy đủ trong `Item.firstReview.originalSnapshot` (chụp lần sửa đầu); bỏ `EDIT` giúp khớp 100% với 16 migration của Phương, `0.docs` và tránh rác bảng kiểm toán nếu GV bấm lưu nhiều lần. Nhánh `feat/teacher-item-review` (Đăng) sẽ gỡ phần tạo event `EDIT` trong `EditItemUseCase` khi đồng bộ code.
- **Giữ bỏ `EXTEND`, `FORCE_SEND`:** Không còn khái niệm gói (`ItemPackage` / `PackageStatus` giữ `@deprecated` ở `shared-types` chỉ để tránh gãy build ngược trước khi dọn hết legacy).

### 2. Schema Prisma & 18 Migrations (khóa nền DB)
- Kế thừa nguyên vẹn **16 migration đầu** từ `develop` + nhánh `feat/admin-ai-review` (`20261024000000_init` → `20261127160000_review_notice_outbox`, bao gồm `pg_trgm`, `item_batches.confirmer_id`, `PARTIALLY_IMPORTED`, `import_operation_id`, `import_group_id/import_part`, `ai_call_count/ai_call_limit = 250`, `item_batch_jobs`, `items.generated_from_ref_ids`, `CANCEL_PENDING`, `REASSIGN_CONFIRMER`, `review_notice_outbox`).
- Bổ sung **2 migration tăng dần tương thích ngược**:
  1. `20261128010000_review_notice_outbox_lease_and_error` (**Mục 14 — Outbox Đợt 1 cho thông báo đổi GV B**): Dùng tên bảng `review_notice_outbox` hiện hành của Phương; thêm 4 cột nullable `lease_token UUID`, `lease_until TIMESTAMPTZ(6)`, `last_error VARCHAR(200)`, `sent_at TIMESTAMPTZ(6)` và mở rộng `CHECK (status IN ('PENDING', 'PROCESSING', 'SENT', 'CANCELLED', 'DEAD'))` + lease invariant check. Chấp nhận ngữ nghĩa *at-least-once*. Việc chuyển sweep nhắc hạn 08:00 và `InProcessMailQueue` (mật khẩu tạm) tách sang hạng mục Mail/BullMQ riêng.
  2. `20261128020000_item_batch_failure_reason` (**Mục 15 — Lý do lô `FAILED`**): Thêm cột nullable `item_batches.failure_reason VARCHAR(100)` song song với `item_batch_jobs.last_error VARCHAR(100)` để truy vấn trực tiếp trên S28/S29 và ghi nhận lỗi ngoài job (ví dụ lô AI sinh `0` câu hợp lệ `NO_VALID_ITEMS_GENERATED`).
- **Quy tắc lô rỗng & kết thúc (Mục 6 & 15):**
  - Không có trạng thái thành công cho lô `0` item: import rỗng bị chặn (`400 IMPORT_GRID_EMPTY`), lô AI `0` item đánh `FAILED` kèm `failureReason`.
  - Lô có `>= 1` item đều kết thúc nhưng `0` câu `FINAL_APPROVED` chuyển **`DONE`** (hiện rõ *"0 câu được import"*), sửa mọi nhánh code đánh `FAILED` nhầm.
  - `PARTIALLY_IMPORTED` chỉ khi đã import `>= 1` câu và còn câu `SECOND_APPROVED`.

### 3. Từ điển Mã lý do kiểm AI & Mã lỗi (`@apt/shared-types` v3.1.0)
Chuẩn hóa hoàn toàn theo code thực tế của module `item-generation`:
- **`ItemCheckReasonCode` (6 mã lưu DB trong `item_check_results.reason_codes`):**
  - `HARD`: `DUPLICATE_EXACT`, `DUPLICATE_NEAR`
  - `SOFT`: `DUPLICATE_NEAR_SUSPECT`, `DUPLICATE_SEMANTIC_SUSPECT`, `INDEPENDENT_ANSWER_MISMATCH`
  - `PASS` *(marker kiểm stale)*: `INDEPENDENT_ANSWER_CHECKED`
- **`CandidateRejectionReason` (15 mã trả trong `rejected[].reasons` khi sinh AI hoặc upload Excel):**
  `CANDIDATE_INVALID`, `CONTENT_REQUIRED`, `EXPLANATION_REQUIRED`, `OPTIONS_INVALID`, `OPTIONS_DUPLICATE`, `ANSWER_INVALID`, `SKILL_INVALID`, `SKILL_MISMATCH`, `CEFR_INVALID`, `CEFR_MISMATCH`, `TOPIC_INVALID`, `IRT_B_INVALID`, `UNSUPPORTED_CELL_VALUE`, `DUPLICATE_IN_FILE`, `DUPLICATE_IN_BATCH`.
- **`ErrorCode`:** Bổ sung `AI_BUDGET_EXCEEDED` bên cạnh `BATCH_BUDGET_EXCEEDED` và `CONFIRMER_IN_REVIEW_GROUP`.

---

## II. Thống nhất Nghiệp vụ, API & AI Pilot

### 4. Nghiệp vụ Kỳ thi & Tài khoản (`BR-08`, `BR-12`, `BR-05`, `BR-18`)
- **`BR-08` (Sửa & công bố kỳ thi):** Chỉ công bố (`DRAFT -> SCHEDULED`) khi có `>= 1` SV và `opensAt` còn ở tương lai. Sau công bố **chỉ sửa giờ** (không sửa tên): khi `SCHEDULED` chưa mở được sửa `opensAt`/`closesAt` nhưng `opensAt` mới phải ở tương lai và cửa sổ đủ `durationMinutes`; khi `OPEN` giữ `opensAt`, chỉ kéo dài `closesAt`; `CLOSED` không sửa. Giữ nguyên `expiresAt` của phiên đã bắt đầu.
- **`BR-12` (`Q-2` đã chốt):** Khi Admin đóng kỳ thủ công, các phiên `IN_PROGRESS` đang chạy tiếp tục tới `expires_at` đã cấp (hết giờ áp luật K5); chỉ chặn bắt đầu phiên mới.
- **`BR-05` (#120) & `BR-18` (#136):** Giữ quyết định `#136` **hoãn bảng `audit_logs` DB sang Khóa luận**; các thao tác quản trị (`CHANGE_ROLE`, `LOCK_ACCOUNT`, `UNLOCK_ACCOUNT`, `RESEND_TEMP_PASSWORD`, `CLOSE_EXAM_ROUND`) ghi log có cấu trúc Pino (cấm ghi mật khẩu/OTP). Không thêm cột trạng thái email trên `users`; lỗi gửi thư/DEAD đẩy log `ERROR` lên Better Stack và Admin xử lý bằng nút *"Gửi lại mật khẩu tạm"* trên S24. Chặn thu hồi Admin cuối và cấm Admin tự khóa/tự thu hồi quyền mình.

### 5. Kết nối AI, Hạn mức & Hàng đợi (`DECISIONS_LOG.md:207–215` — Trạng thái Pilot)
- **Kết nối LLM:** Gọi **Gemini trực tiếp qua endpoint tương thích OpenAI** cho môi trường thử nghiệm (không dùng LiteLLM dự phòng ở chế độ thử).
- **Embedding (`Q-9`):** Mặc định pilot `gemini-embedding-001` (`768` chiều) qua biến môi trường (`EMBEDDING_MODEL`, `EMBEDDING_DIM`), chuẩn hóa L2 + cosine trong ứng dụng; ghi rõ **pilot / chưa kiểm chứng runtime** cho đến khi smoke test sinh/C1 chạy thật thành công.
- **Hạn mức & Chia lô (`Q-7`):** Chia lần import thành các lô tối đa **`50` câu** (`import_group_id`, `import_part`) và trần **`250` lượt gọi AI / lô** (`ai_call_count`, `ai_call_limit`) gồm sinh, embedding, G5 (2 lượt gọi độc lập), C2/C3 và retry. Cấp lượt nguyên tử trong PostgreSQL; sinh/kiểm lô chạy trên hàng đợi PostgreSQL `item_batch_jobs` có lease.
- **Few-shot (`Q-8`):** Lấy tối đa `5` (tối thiểu `3`) câu đã duyệt cùng `skill`/`cefrTarget` từ DB hiện tại, ghi ID mẫu vào `items.generated_from_ref_ids`; cần rà bằng chứng bản quyền bộ nguồn trước khi phát hành ngoài phạm vi đồ án.

### 6. Hợp đồng Route Thực tế (`item-generation` vs `UCGV` & `exam-rounds`)
- **Module `item-generation` (`ADMIN` — Phương):**
  - `POST /api/v1/item-batches/generate`
  - `GET /api/v1/item-batches/import/template`, `POST .../import/upload`, `GET .../import/grid`, `DELETE .../import/grid[/:rowKey]`, `POST .../import/save` *(legacy `POST .../import/preview`)*
  - `GET /api/v1/item-batches`, `GET /api/v1/item-batches/:id`, `GET /api/v1/item-batches/rejected-stats`
  - `POST /api/v1/item-batches/:id/{retry-generation, retry-checks, refresh-status}`
  - `POST /api/v1/item-batches/:id/{assign-preview, assign, reassign, reassign-confirmer, cancel-pending}`, `PATCH /api/v1/item-batches/:id/deadlines`
  - `POST|GET /api/v1/item-batches/:id/final-check`, `POST .../items/:itemId/flag-decision`, `POST .../import`
- **Module `exam-round` (`ADMIN` — Phương):** Bổ sung `GET /api/v1/exam-rounds/:id/participants/import/template`.
- **Module `item-bank` / Teacher Review (`TEACHER` only — Đăng):** Toàn bộ `/api/v1/teacher/tasks/...` và `/api/v1/teacher/items/...` thuộc `UCGV14–15`, chỉ cho `@Roles(UserRole.TEACHER)` (khi hợp nhất BE, loại bỏ controller `/teacher/tasks` trùng và route cũ `/teacher-review` bên nhánh `item-generation`).
- **Luồng Sinh viên (`STUDENT` only — Đăng):** Route phòng thi `/student/exams/[roundId]/take`, `/student/results/[sessionId]`, `/student/results/[sessionId]/review`; chỉ chủ sở hữu `STUDENT` thao tác phiên và xem đáp án khi phiên `COMPLETED` (`K6`).

---

## III. Phân công & Danh sách Điểm nợ / Cần hoàn tất thủ công

- **Phân vai phát triển BE/FE (theo `20261016_MoHinhHoaYeuCau.docx`):**
  - **Đăng:** Toàn bộ `UCSV*` (thi CAT, hồ sơ năng lực, kết quả, đổi/quên mật khẩu) và `UCGV*` (duyệt A/B, báo cáo lớp, tra cứu SV, xem ngân hàng câu).
  - **Phương:** Toàn bộ `UCADM*` (`item-generation`, `exam-round`, `user-admin`, `user-import`, dashboard tổng quan Admin).
- **Điểm nợ chưa khóa schema trong đợt này:**
  - Bảng **nhật ký lần lưu roster** (`DECISIONS_LOG.md:196–198`) sẽ được bổ sung từ nhánh `feat/admin-exam-rounds` của Phương trước khi mở Wave 1 cho module `exam-round`.
- **Việc cần kiểm chứng / hoàn tất ngoài tự động hóa text:**
  1. Chạy `prisma migrate deploy && npx prisma db seed` trên PostgreSQL container trống (Wave 0C) khi bật Docker.
  2. Chạy smoke test thật với Gemini (`generate`, `C1`, `gemini-embedding-001@768`) và Brevo SMTP + SPF/DKIM.
  3. Kiểm tra giao diện trên Figma/Stitch, rà soát trực quan lần cuối 2 file `.docx` đã xuất lại TOC & 5 ảnh PNG, và cấu hình GitHub Ruleset / GVHD `COMMITMENT_BASELINE.md`.
