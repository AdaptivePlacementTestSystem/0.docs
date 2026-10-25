# BẢN CHỐT QUYẾT ĐỊNH KỸ THUẬT VÀ ĐỒNG BỘ TOÀN DIỆN HỆ THỐNG
**Dự án:** Hệ thống Đánh giá Năng lực Thích ứng (Adaptive Placement Test - APT)  
**Tài liệu đối chiếu:** `20261016_PHAN_TICH_RA_SOAT_UPDATE_VA_GIAI_PHAP_ITEMBATCH_ITEMPACKAGE (2).md`  
**Ngày lập:** 16/10/2026  
**Người lập:** Đăng (Tech Lead / Architect)  
**Trạng thái:** CHÍNH THỨC CHỐT (Final Technical Decisions) — Gửi trực tiếp cho Teammate

---

## LỜI MỞ ĐẦU

Nhóm kỹ thuật đánh giá rất cao bản rà soát chi tiết, nghiêm túc và có tính phản biện chuyên môn sắc bén của Teammate tại bản `(2).md`. Đặc biệt, **Mục 10** đã chỉ rõ những điểm lệch pha giữa phần diễn giải khái niệm (conceptual) trước đó với mô hình vật lý (physical schema) đã được thiết kế ngày 14/10.

Với tôn chỉ: **Tuân thủ tuyệt đối Rubric đánh giá đồ án (TC2.1, TC2.2), chuẩn hóa CSDL bậc 3 (3NF), áp dụng Clean Architecture chuẩn mực và không làm tạm bợ**, dưới đây là toàn bộ quyết định kỹ thuật chính thức được chốt dứt điểm để toàn đội ngũ thống nhất thực hiện.

---

## 1. QUYẾT ĐỊNH 1: CHUẨN HÓA MÔ HÌNH VẬT LÝ KHỚP 100% VỚI `schema.prisma` VÀ ĐẶC TẢ 14/10

Mục 3 trong bản phản hồi trước đó được trích từ tài liệu khái niệm sơ khởi, chưa cập nhật theo bản thiết kế chi tiết ngày 14/10 (`20261014_KE_HOACH_SINH_VA_DUYET_DE_AI.md`). **Chính thức đính chính và chốt đồng bộ 100% theo `schema.prisma` và đặc tả 14/10 như sau:**

### 1.1. Bảng đối chiếu và chuẩn hóa thực thể

| Thành phần | Chuẩn chốt chính thức (Khớp 100% `schema.prisma` & Kế hoạch 14/10) | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| **`ItemBatchStatus`** | `GENERATING` \| `IMPORTING` \| `CHECKING` \| `READY_TO_ASSIGN` \| `IN_REVIEW` \| `READY_TO_FINALIZE` \| `FINAL_CHECKED` \| `DONE`<br>*(Trạng thái ngoại lệ: `FAILED`, `PARTIAL`)* | Máy trạng thái Lô một chiều, phản ánh chính xác tiến độ từ lúc sinh/import đến khi hoàn tất. |
| **Trạng thái Gói (`PackageStatus`)** | **Chỉ có đúng 3 trạng thái:** `OPEN` $\rightarrow$ `SENT` $\rightarrow$ `DONE` | Bỏ các trạng thái thừa như `UNASSIGNED`, `SUBMITTED`, `CONFIRMED`. |
| **Quy tắc Gom Gói (`ItemPackage`)** | Ràng buộc: `UNIQUE(batchId, reviewerId)`.<br>**Mỗi Giảng viên A nhận đúng MỘT Gói trong một Lô** (tất cả các câu giao cho GV A trong lô đó được gom vào 1 gói duy nhất). | GV A duyệt hết toàn bộ câu trong gói mới được bấm "Gửi cho GV B" một lần duy nhất. |
| **Phân công duyệt (`ItemReviewAssignment`)** | Phân công theo **từng câu hỏi**: `itemId` là UNIQUE, có `assigneeId`, `dueAt`, `reminderSent`.<br>Không lưu `status` riêng (trạng thái câu do `Item.status` quản lý: `DRAFT` $\rightarrow$ `FIRST_APPROVED` $\rightarrow$ `SECOND_APPROVED` $\rightarrow$ `FINAL_APPROVED`). | Trỏ trực tiếp tới `itemId`, không trỏ tới gói. |
| **Hành động Audit (`ReviewAction`)** | `APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG`. | Chuẩn hóa bảng ghi vết bất biến `ItemReviewEvent`. |
| **Kiểm tra AI (`ItemCheckResult`)** | - Checkpoint: `C1` (sau sinh AI), `C2` (sau import), `C3` (trước khi final import).<br>- Level: `PASS, SOFT, HARD`.<br>- Thuộc tính: `reasonCodes String[]`, `suspectedDuplicateId String?`. | Lỗi cứng (`HARD`) tự động chuyển `AI_REJECTED`. Lỗi mềm (`SOFT`) hiển thị cờ cho Admin xem xét. |
| **Vector Embedding (`ItemEmbedding`)** | - Thuộc tính: `vector Float[]`.<br>- Cosine Similarity **được tính toán trong ứng dụng (in-app)**.<br>- **Không phụ thuộc vào pgvector** ở giai đoạn này (theo đúng ghi chú schema để chờ chốt Q-9/Q-10). | Đảm bảo tính khả thi triển khai trên mọi môi trường DB PostgreSQL. |
| **Vai trò người dùng (Roles)** | Hệ thống chỉ có **3 vai trò duy nhất**: `STUDENT`, `TEACHER`, `ADMIN`.<br>- Người xác nhận vòng 2 (Confirmer) là một `TEACHER` (GV B) được chỉ định trong `ItemBatchAssignment` (`confirmerId`).<br>- **KHÔNG CÓ ROLE RIÊNG "Trưởng bộ môn" (HOD)** và không có màn hình `/hod/`. | Giữ vững nguyên tắc phân quyền RBAC 3 vai trò đã chốt. |
| **Tên chuẩn Use Case `UCADM15..17`** | - `UCADM15`: **Quản lý kỳ thi** (Manage Exams / Exam Rounds).<br>- `UCADM16`: **Import danh sách thí sinh dự thi** (Import Exam Roster).<br>- `UCADM17`: **Theo dõi tiến độ kỳ thi** (Monitor Exam Progress). | Không dùng các tên cũ như "Phân ca thi" hay "Khóa/Hủy kỳ thi". |

---

## 2. QUYẾT ĐỊNH 2: XỬ LÝ `ItemSource` VÀ CÂU HỎI SEED THEO CHUẨN 3NF VÀ RUBRIC

Về băn khoăn của Teammate: *"Nếu bỏ `Item.source` thì câu hỏi Seed ban đầu (`batchId` nullable) sẽ mất nguồn gốc"*:

### 2.1. Phân tích theo Chuẩn Thiết kế Phần mềm & Rubric TC2.1, TC2.2
* **Phương án giữ cả hai (`Item.source` và `ItemBatch.source`):** Là giải pháp phi chuẩn hóa (denormalization) tạm bợ. Vi phạm chuẩn 3NF, vi phạm nguyên tắc Single Source of Truth, tạo ra dư thừa dữ liệu và rủi ro Update Anomaly (ví dụ: Batch có source là `AI_GENERATED` nhưng câu con lại ghi `IMPORTED`). Hội đồng chấm đồ án rất dễ trừ điểm lỗi kiến trúc cơ bản này.
* **Phương án Chuẩn mực (Clean Database Design):** Mọi dữ liệu câu hỏi trong hệ thống ngân hàng đề thi đều phải được quản lý theo một đợt nhập liệu (Lô) có nguồn gốc rõ ràng, không được phép có dữ liệu mồ côi (orphaned data).

### 2.2. Quyết định chốt chính thức (Cách 1)
1. **Loại bỏ hoàn toàn cột `source` trên bảng `Item`**, bỏ enum `ItemSource`.
2. **Chỉ giữ duy nhất một enum:** `enum ItemBatchSource { AI_GENERATED, IMPORTED }` gắn tại bảng `ItemBatch`.
3. **Chuyển trường `Item.batchId` thành `NOT NULL`** (khóa ngoại bắt buộc trỏ tới `ItemBatch`).
4. **Giải pháp xử lý triệt để cho câu hỏi Seed / Cũ:**
   - Trong migration/seed script khởi tạo hệ thống, tạo sẵn một Lô hạt giống mặc định:
     * `id`: UUID cố định của seed batch.
     * `batchCode`: `"BATCH_SYSTEM_INITIAL_SEED"`.
     * `name`: `"Ngân hàng câu hỏi hạt giống khởi tạo hệ thống"`.
     * `source`: `IMPORTED`.
     * `status`: `DONE`.
   - Chạy lệnh cập nhật toàn bộ câu seed cũ trỏ `batchId` về Lô khởi tạo này:
     ```sql
     UPDATE items SET batch_id = '<SEED_BATCH_UUID>' WHERE batch_id IS NULL;
     ALTER TABLE items ALTER COLUMN batch_id SET NOT NULL;
     ```
5. **Kết quả đạt được:** Đảm bảo toàn vẹn tham chiếu 100%, chuẩn hóa 3NF tuyệt đối, mọi câu hỏi đều có nguồn gốc `IMPORTED` thông qua Lô hạt giống, sạch sẽ và hoàn toàn tự tin giải trình trước Hội đồng.

---

## 3. QUYẾT ĐỊNH 3: THỐNG NHẤT BỘ ROUTE ROLE-BASED CHUẨN NEXT.JS APP ROUTER

Thống nhất duy nhất một bộ route chính thức làm nguồn chân lý (Single Source of Truth) trên toàn bộ dự án (từ Backend API, Next.js Frontend đến Use Case Spec):

| Nghiệp vụ | Route chuẩn chính thức | Lý do chuẩn hóa |
| :--- | :--- | :--- |
| **GV A duyệt vòng 1** | **`/teacher/tasks/reviews`** | Tuân thủ Route Group `(teacher)` của Next.js v3.0, phân quyền role-based sạch sẽ qua Middleware/Guard. |
| **Chi tiết gói duyệt của GV A** | **`/teacher/tasks/reviews/[packageId]`** | Resource-oriented URL chuẩn RESTful. |
| **GV B xác nhận vòng 2** | **`/teacher/tasks/confirms`** | GV B thực hiện nhiệm vụ với vai trò `TEACHER`, không tạo prefix `/hod/`. |
| **Chi tiết gói xác nhận của GV B** | **`/teacher/tasks/confirms/[packageId]`** | Rõ ràng, đồng nhất cấu trúc với reviews. |
| **Admin quản lý Lô câu hỏi** | **`/admin/item-batches`** | Resource route chuẩn Admin. |
| **Chi tiết Lô & Giao việc** | **`/admin/item-batches/[id]`** | Xem trạng thái lô, chạy C3 và chia gói giao việc. |

*(Khai tử hoàn toàn các biến thể cũ: `/me/review-tasks`, `/teacher/inbox/...`, `/hod/...`).*

---

## 4. QUYẾT ĐỊNH 4: ĐỒNG BỘ DỨT ĐIỂM TOÀN BỘ MÃ `UCGV11..13` $\rightarrow$ `UCADM15..17`

1. **Hiện trạng tại repo chính:**
   - Đã quét sạch và chuyển đổi hoàn toàn 100% sang `UCADM15..17` trên toàn bộ các tài liệu chính:
     - `SRS_TLCN_v3.0.md` & `SRS_TLCN_v3.0.docx`.
     - `20261014_KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` (đã cập nhật sạch ở phiên này).
     - `20261013_KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` (đã cập nhật sạch).
     - `AdaptivePlacementTest.xml` và các bản Use Case docx.
     - `CauTrucDuAn/KE_HOACH_CAU_TRUC_DU_AN.md`.
     - `Mo_ta_So_do_Lop_ClassDiagram.md`.
2. **Yêu cầu đối với Teammate:**
   - Nếu phía Teammate còn lưu các file cũ ở các thư mục như `Tuan4`, `Tuan5`, đề nghị Teammate pull bản cập nhật mới nhất từ repo này để đồng bộ triệt để, chấm dứt tình trạng "nợ mã".

---

## 5. LỘ TRÌNH HÀNH ĐỘNG THỐNG NHẤT CHO NHÓM (TRƯỚC MỐC GATE G1)

Để đảm bảo nhóm đạt cột mốc Gate G1 (cuối Tuần 6) an toàn và chất lượng cao nhất:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   BƯỚC 1: LÀM SẠCH BASELINE TÀI LIỆU                   │
│  - Áp dụng C1–C18 từ DE_XUAT_SUA_CLAUDE_MD.md vào CLAUDE.md            │
│  - Cập nhật COMMITMENT_BASELINE.md bổ sung F-23..F-28                  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│              BƯỚC 2: CẬP NHẬT CLASS DIAGRAM (KHI MỞ NỢ)                │
│  - Tách 2 trang draw.io: Trang 1 (Core CAT) & Trang 2 (Review Batch)   │
│  - Cập nhật 7 thực thể mới theo đúng các enum đã chốt ở Quyết định 1    │
│  - Bỏ source trên Item, gắn batchId NOT NULL                           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│             BƯỚC 3: TRIỂN KHAI BACKEND & FRONTEND (TUẦN 5 - 6)         │
│  - Backend: ItemBatchModule, ItemPackageModule, Generic Grid Service   │
│  - Database: Migration tạo System Seed Batch và set batchId NOT NULL   │
│  - Frontend: 4 màn hình chuẩn Next.js App Router theo Quyết định 3     │
└────────────────────────────────────────────────────────────────────────┘
```

---
*Văn bản này là quyết định kỹ thuật chính thức cuối cùng của nhóm. Toàn bộ các bên căn cứ vào tài liệu này để triển khai code và đồng bộ hồ sơ báo cáo.*

---

## PHỤ LỤC (Phương, 16/10/2026): điều chỉnh sau rà soát và trả lời

1. **Lô seed (Quyết định 2):** bảng `item_batches` thực tế **không có** `batchCode`; lô seed chỉ cần `id`, `source = IMPORTED`, `status = DONE`, `created_by` = Admin hệ thống (tạo trước). Phương chốt **thêm cột tùy chọn `name`** (nullable) và **tạo một lô seed cho mỗi bộ nguồn** (CEFR-J, CLOTH, GV tự soạn; thêm một lô dữ liệu giả cho dev) thay vì một lô duy nhất. `requested_count` nullable (khớp SRS).
2. **Gói:** `ItemPackage` tạo ngay lúc Admin giao việc (OPEN → SENT → DONE).
3. **Route:** thêm `/admin/item-batches/[id]/assign`, `/admin/item-batches/[id]/final-check`, `/admin/exam-rounds/[id]/import`, `/admin/item-batches/generate|import`, `/teacher/item-bank` (chỉ xem), `/admin/item-bank`.
4. **Thông báo:** chỉ email nhắc việc (BullMQ + MailPort) và Hộp việc.
5. **Đồng bộ đã làm:** `schema.prisma`, `seed.ts`, SRS, UC spec, plan, danh sách màn hình, `ClassDiagram.puml/.mmd`, `Mo_ta`, `CLAUDE.md`, `COMMITMENT_BASELINE.md`. Chi tiết: `PHAN_TICH_RA_SOAT_...md` Mục 12 và `DECISIONS_LOG.md` #115–#117.
