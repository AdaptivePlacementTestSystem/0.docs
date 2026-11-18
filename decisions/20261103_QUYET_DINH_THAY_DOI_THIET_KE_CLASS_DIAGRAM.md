# TỔNG HỢP QUYẾT ĐỊNH THAY ĐỔI THIẾT KẾ CLASS DIAGRAM & TRẠNG THÁI ÁP DỤNG

* **Ngày lập:** 03/11/2026 — **cập nhật:** 04/11/2026
* **Căn cứ:** Kết luận cuộc họp với Giảng viên hướng dẫn (GVHD) và thống nhất yêu cầu kỹ thuật; các lựa chọn bổ sung ngày 04/11/2026 (mục 1.3) do nhóm chốt sau khi phân tích đánh đổi.
* **Nguyên tắc cốt lõi:** **Nghiệp vụ hệ thống giữ nguyên 100%**, chỉ tái cấu trúc và chuẩn hóa thiết kế mô hình lớp (Class Model).
* **Trạng thái:** **Đã áp dụng vào bộ tài liệu thiết kế** (Class Diagram draw.io/PlantUML/Mermaid, `Mo_ta_So_do_Lop_ClassDiagram.md`, `schema.prisma` bản tham chiếu, các tài liệu nghiệp vụ liệt kê ở mục 5). **Chưa áp vào mã nguồn** (`backend/backend/prisma`, `packages/shared-types`, frontend): xem mục 6.

---

## 1. TỔNG HỢP CÁC QUYẾT ĐỊNH THAY ĐỔI

### Quyết định 1: Đổi quan hệ `ExamRound — TestSession` thành Composition (`ExamRound ◆— 0..* TestSession`)
* **Hiện trạng cũ:** Quan hệ Hiệp hội đơn hướng (`ExamRound` → `0..*` `TestSession`).
* **Quyết định mới:** Chuyển sang quan hệ **Composition** (`ExamRound ◆— 0..* TestSession`) với đầu hình thoi đen đặc nằm ở phía `ExamRound`.
* **Cơ sở kiến trúc & đánh giá:**
  * **Sở hữu tuyệt đối:** Một phiên thi sinh ra chỉ phục vụ duy nhất một kỳ thi, không thể chuyển hay gán lại sang kỳ khác.
  * **Phụ thuộc tồn tại:** Phiên thi là thành phần cấu thành không thể tách rời của kỳ thi.
  * **Toàn vẹn dữ liệu trong CSDL:** Về UML là Composition, nhưng ở mức lưu trữ (`schema.prisma`) áp dụng `onDelete: Restrict` (hoặc Soft Delete) khi kỳ thi đã có sinh viên làm bài, để bảo vệ lịch sử thi. (Schema hiện đã là `Restrict`.)
  * **Quan hệ với Sinh viên:** `Student — TestSession` giữ là **Association**.

---

### Quyết định 2: Bỏ `ItemPackage`, chuyển cơ chế duyệt vào trực tiếp `Item`
* **Hiện trạng cũ:**
  * Câu hỏi quản lý theo Lô (`ItemBatch`); lô chia thành các Gói (`ItemPackage`) giao cho từng cặp GV A (`reviewerId`) và GV B (`confirmerId`).
  * Phải hoàn thành và gửi cả gói (`canSend`, `PackageStatus = SENT`) thì GV B mới vào xác nhận.
* **Quyết định mới:**
  * **Xóa hoàn toàn `ItemPackage` và enum `PackageStatus`.**
  * **Giao việc theo từng câu (Cách A):** Admin phân công trực tiếp từng câu cho GV A và GV B; mỗi `Item` mang thông tin người duyệt vòng 1 và người thẩm định vòng 2.
  * Kết quả hai vòng duyệt lưu trong `Item` qua hai thuộc tính kiểu giá trị `FirstReviewDetail` và `SecondReviewDetail` (Value Object / `<<DataType>>` trong UML, lưu JSON trong CSDL).
  * **Hạn chót:** mỗi vòng có hạn `dueAt` riêng nằm trong chính cấu trúc của vòng đó.

### 1.3 Lựa chọn bổ sung (chốt 04/11/2026, sau phân tích đánh đổi)

| # | Vấn đề | Lựa chọn | Phương án đã loại và lý do |
|---|---|---|---|
| a | Hai bảng giao việc `ItemReviewAssignment`, `ItemBatchAssignment` | **Bỏ cả hai bảng** | Giữ cả hai: dữ liệu lặp với JSON, dễ lệch. Chỉ bỏ `ItemReviewAssignment`: `ItemBatchAssignment` còn lại gần như vô dụng (`confirmerId`, `confirmDays` mất nghĩa khi không còn gói; khóa chính `batchId` chỉ cho giao một lần mỗi lô) |
| b | Nơi lưu ID người duyệt/xác nhận | **Cột riêng trên `Item`: `reviewerId`, `confirmerId`** (khóa ngoại tới `users`, `Restrict`), **sơ đồ UML vẽ hai thuộc tính này trên `Item`**, không nằm trong hai cấu trúc con | Thuần JSON: không có khóa ngoại (xóa GV đang có việc không bị chặn), phải viết index bằng SQL thô. Cột riêng + giữ nguyên sơ đồ: sơ đồ lệch DB, cần mapper tách/ghép. **Đánh đổi chấp nhận:** khác chữ thỏa thuận họp GVHD (các cấu trúc con không còn chứa ID người duyệt) → cần báo GVHD |
| c | Cờ "đã nhắc hạn" | **Hai cột `firstReminderSent`, `secondReminderSent` trên `items`**, không vẽ trên sơ đồ (chi tiết lưu trữ, ghi ở Mục 9 của `Mo_ta`) | Để trong JSON: job nhắc hạn phải đọc–ghi cả JSON, có thể ghi đè kết quả duyệt của GV (mất cập nhật) |
| d | Ghi "ai giao, lúc nào" | **Ghi `ItemReviewEvent`**: thêm giá trị `ASSIGN` vào `ReviewAction`; mỗi câu một dòng; giao lại dùng `REASSIGN` | Nhét `assignedBy/assignedAt` vào JSON: làm phình JSON và trùng chức năng nhật ký kiểm toán |

---

## 2. CHUẨN ĐẶT TÊN TIẾNG ANH & CẤU TRÚC CHI TIẾT TRONG `Item`

### 2.1 Thuộc tính mới của `Item`
* `- reviewerId: UUID {nullable}` — GV A được giao duyệt (cột FK; rỗng khi chưa giao)
* `- confirmerId: UUID {nullable}` — GV B được giao xác nhận (cột FK)
* `- firstReview: FirstReviewDetail {nullable}` — Vòng 1 (cột JSON `first_review`)
* `- secondReview: SecondReviewDetail {nullable}` — Vòng 2 (cột JSON `second_review`)
* `+ isOverdue(round: int, at: DateTime): boolean`
* Bỏ `originalSnapshot` khỏi `Item` (chuyển vào `FirstReviewDetail`). Cột `original_snapshot` riêng trong DB cũng bỏ.

### 2.2 `FirstReviewDetail` (Vòng 1 — Giảng viên A)
| Thuộc tính | Kiểu | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| `dueAt` | `DateTime` | Hạn hoàn thành vòng 1 cho câu này |
| `action` | `ReviewAction?` | `APPROVE` hoặc `REJECT`; null khi chưa duyệt |
| `reviewedAt` | `DateTime?` | Thời điểm GV A duyệt |
| `comment` | `String?` | Ghi chú, lý do sửa hoặc từ chối |
| `originalSnapshot` | `Json?` | Bản gốc nội dung/đáp án/giải thích trước khi GV A sửa lần đầu (ghi một lần) |

### 2.3 `SecondReviewDetail` (Vòng 2 — Giảng viên B)
| Thuộc tính | Kiểu | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| `dueAt` | `DateTime` | Hạn hoàn thành vòng 2 cho câu này |
| `action` | `ReviewAction?` | `CONFIRM` hoặc `REMOVE`; null khi chưa xác nhận |
| `confirmedAt` | `DateTime?` | Thời điểm GV B xác nhận hoặc loại |
| `comment` | `String?` | Nhận xét của GV B |

> So với bản 03/11: `reviewerId` và `confirmerId` **đã chuyển ra `Item`** (lựa chọn 1.3b).

---

## 3. BẢN ĐỒ TÁC ĐỘNG THIẾT KẾ

```
[ExamRound]  ◆────── 0..* [TestSession]      (Composition, thay cho Association)
[ItemBatch]  ◆────── 1..* [Item]             (quan hệ trực tiếp duy nhất; bỏ ItemBatch ◆ ItemPackage)
[Item]  ◆── 0..1 [FirstReviewDetail]         (<<DataType>>, vẽ ở Trang 3)
[Item]  ◆── 0..1 [SecondReviewDetail]        (<<DataType>>, vẽ ở Trang 3)
[Item]   + reviewerId, confirmerId, firstReview, secondReview, isOverdue()
         - originalSnapshot (đã vào FirstReviewDetail)
[Teacher] + reviewItem(item, action, comment)   - submitPackage(pkg)
          + confirmItem(item, action, comment)
[Teacher] ──▶ [Item]  «reviews / confirms»
[ItemPackage], [PackageStatus]                 ==> ĐÃ XÓA
[ItemReviewAssignment], [ItemBatchAssignment]  ==> ĐÃ XÓA (chỉ có ở schema)
[ReviewAction]  − EXTEND, FORCE_SEND   + ASSIGN
[ItemReviewEvent] chỉ ghi log cho Item và ItemBatch (bỏ liên kết ItemPackage, bỏ cột packageId)
```

1. **`ItemBatch`:** `canFinalize()` — mọi `Item` trong lô đã xong vòng 2 (`SECOND_APPROVED` hoặc `REJECTED`) hoặc các câu còn lại đã quá hạn.
2. **`Teacher`:** bỏ `submitPackage(pkg)`; tách `reviewItem(...)` (GV A) và `confirmItem(...)` (GV B).
3. **`ItemReviewEvent`:** giao việc ghi `ASSIGN` một dòng mỗi câu; giao lại `REASSIGN`.
4. **Enum:** xóa `PackageStatus`; `ReviewAction` = `APPROVE`, `REJECT`, `CONFIRM`, `REMOVE`, `CONFIRM_ALL`, `IMPORT`, `ASSIGN`, `REASSIGN`, `ACCEPT_FLAG` (bỏ `EXTEND`, `FORCE_SEND` theo gói).

---

## 4. KẾT QUẢ ÁP DỤNG VÀO SƠ ĐỒ VÀ SCHEMA

| Hạng mục | Trạng thái |
|---|---|
| `TLCN.drawio.xml` Trang 1: bỏ `ItemPackage`/`PackageStatus`, sửa `Item`, `Teacher`, `ReviewAction`, `ExamRound ◆ TestSession` | ☑ |
| `TLCN.drawio.xml` Trang 2: `ExamRound ◆ TestSession` | ☑ |
| `TLCN.drawio.xml` Trang 3: bỏ gói, thêm `FirstReviewDetail`/`SecondReviewDetail`, `Item ◆` hai kiểu, `Teacher → Item` | ☑ (vị trí hộp và đường nối cần chỉnh tay trên draw.io) |
| `ClassDiagram.puml` / `.mmd` | ☑ sinh lại bằng `Tuan7/scripts/gen_uml.py` (đã cập nhật `RELATIONS`/`GROUPS`) |
| `Mo_ta_So_do_Lop_ClassDiagram.md` | ☑ |
| `docs-repo/design/class/schema.prisma` (bản tham chiếu) | ☑ `prisma validate` đạt |
| Ảnh `TLCN-Trang-1…3.png` | ⏸ cần xuất lại từ draw.io |

## 5. TÀI LIỆU KHÁC ĐÃ RÀ SOÁT

Xem bảng "Bản đồ đồng bộ" trong `0.docs/tracking/weekly-log/Tuan-08.md` và `DECISIONS_LOG` #133 (trạng thái từng tài liệu: SRS `.md`, kế hoạch sinh/duyệt đề, mô tả UI, Sequence, cấu trúc dự án; SRS `.docx` và đặc tả UC `.docx` còn đề xuất).

## 6. VIỆC CHƯA LÀM (NỢ ĐỒNG BỘ)
1. `backend/backend/prisma/schema.prisma` + migration mới (bỏ `item_packages`, `item_review_assignments`, `item_batch_assignments`, `items.package_id`, `items.original_snapshot`; thêm `reviewer_id`, `confirmer_id`, `first_review`, `second_review`, `first_reminder_sent`, `second_reminder_sent`; bỏ `item_review_events.package_id`). Migration `20261102000000_add_item_original_snapshot` do thành viên Đăng tạo sẽ bị thay thế.
2. `packages/shared-types`: bỏ `package-status.enum.ts`; sửa `ReviewAction` (bỏ `EXTEND`, `FORCE_SEND`, thêm `ASSIGN`).
3. Mã BE/FE theo gói (`item-bank` còn khái niệm cũ, route `[packageId]` ở frontend).
4. `SRS_TLCN_v3.0.docx`, `20261016_MoHinhHoaYeuCau.docx` (đặc tả UC).
5. Thông báo GVHD về lựa chọn 1.3b (ID người duyệt nằm trên `Item`, không trong hai cấu trúc con).
6. Chỉ mục (nếu cần) cho truy vấn hộp việc: `index (reviewer_id, status)`, `(confirmer_id, status)` — đã có trong schema tham chiếu.

---

## 7. CHECKLIST NGHIỆM THU
- [x] `ExamRound ◆ TestSession` ở Trang 1, Trang 2 draw.io và PlantUML/Mermaid.
- [x] Không còn `ItemPackage`, `PackageStatus` trong sơ đồ, `Mo_ta`, `schema.prisma` tham chiếu.
- [x] `firstReview`, `secondReview` mô tả đủ trường và ràng buộc.
- [x] `Teacher`, `ItemBatch`, `Item` khớp mô hình duyệt theo câu.
- [ ] Các tài liệu nghiệp vụ và mã nguồn đồng bộ (xem mục 6).
