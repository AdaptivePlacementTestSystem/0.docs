# MÔ TẢ SƠ ĐỒ LỚP (CLASS DIAGRAM) — HỆ THỐNG PLACEMENT TEST THÍCH ỨNG

**Tài liệu này mô tả:** File thiết kế `TLCN.drawio.xml` (trang `Trang-1`; ảnh xuất `TLCN-Trang-1.drawio.png` **chưa được xuất lại** sau Phiên 22/25 — xem ghi chú ở cuối tài liệu). Bản cập nhật Phiên 22 (2026-10-13) đồng bộ theo `Tuan5/KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` (DC-18 … DC-23); **Phiên 25 (2026-10-14)** bổ sung Nhóm 8 "Sinh và duyệt đề AI" theo `Tuan5/KE_HOACH_SINH_VA_DUYET_DE_AI.md` bản 5 (DC-27 … DC-45).
**Thay thế:** `TLCN-Phương.drawio.png` (sơ đồ gốc — vẫn giữ trong repo làm lịch sử, không xoá); bản mô tả trước Phiên 22 được lưu tại `Tuan5/_BACKUP_20261013_PHIEN22_Mo_ta_So_do_Lop_ClassDiagram_ORIGINAL.md`; bản trước Phiên 25 tại `Tuan5/_BACKUP_20261014_Mo_ta_ClassDiagram_ORIGINAL.md`.
**Tài liệu tham chiếu gốc:** `SRS_TLCN_v2.6_Final.docx` (SRS v3.0 đang soạn ở `Tuan5/`), `backend/backend/prisma/schema.prisma` (đối chiếu cột), kế hoạch Tuần 5.
**Mục đích tài liệu:** Diễn giải cho khách hàng (KH) hiểu: mỗi khối (lớp/đối tượng) trong sơ đồ đại diện cho cái gì, dùng để làm gì, và các khối liên kết/phụ thuộc vào nhau ra sao trong vận hành thực tế của hệ thống.

**Số lượng thật (đếm bằng script từ chính `TLCN.drawio.xml` / `Trang-1`, Phiên 25):** **47 class** (gồm `<<interface>>`, `<<service>>`, lớp liên kết) **+ 18 enum = 65 khối**, **89 quan hệ** (Phiên 22: 30 class + 13 enum, 53 quan hệ; Phiên 25 thêm 17 class + 5 enum và 37 quan hệ mới, bỏ 1 quan hệ `Admin–Item`: 53 + 37 − 1 = 89). Ba file `TLCN.drawio.xml`, `ClassDiagram.puml`, `ClassDiagram.mmd` khớp nhau về tập class / enum / quan hệ (kết quả kiểm: cuối Mục "Ghi chú Phiên 25"). Con số "31 class / 10 enum" ghi ở các tài liệu cũ **không còn đúng**.

> Quy ước nhãn: **[đề xuất]** = tên/chữ ký do AI đề xuất, chưa được người dùng duyệt (kế hoạch Tuần 5, Mục 1.2 quy tắc 4); **[cần xác nhận]** = điểm chưa chắc, phải hỏi lại trước khi coi là chốt.

> ⚠️ **Tình trạng các điểm cần xác nhận cũ (đánh số theo bản trước Phiên 22) và các điểm mới:**
> 1. ~~Nhóm Auth không có trong `Trang-1`.~~ **Đã xử lý Phiên 22:** `AuthProvider` (`<<interface>>`) và `JwtAuthProvider` được **vẽ vào `Trang-1`** (Tiểu luận chỉ đăng nhập email + mật khẩu, DC-02). `EduZSSOAdapter` / `EduZSSOClient` **chuyển sang gói Khóa luận**, không còn trong sơ đồ TL. Thêm enum `AuthProviderType` (LOCAL/GOOGLE/MICROSOFT) vì `schema.prisma` còn giữ enum này và `User.authProvider` dùng nó; **[cần xác nhận]** có nên rút `GOOGLE`/`MICROSOFT` khỏi enum không (kế hoạch ghi "không cần đổi", vì tài khoản import dùng `LOCAL`).
> 2. ~~`Explanation` gắn `Item` hay `SessionResponse`?~~ **Đã chốt** theo #60/#63: gắn **`Item`** (1 lần/Item, dùng chung cho mọi SV; **sinh cùng lúc sinh câu hỏi**, DC-31 — Phiên 25 sửa chỗ ghi "lazy" cũ). Phiên 22 chỉnh ký hiệu cạnh trong draw.io từ hình thoi rỗng (kết hợp) sang **hình thoi đặc (composition)** cho khớp mô tả và `ON DELETE CASCADE` trong schema.
> 3. `AIExplainerService` không có `generateRecommendations(...)` nhưng `LanguageProfile.aiRecommendations: String[]` vẫn còn. **[cần xác nhận]** nơi sinh gợi ý học tập (vẫn mở, Phiên 22 không đổi).
> 4. ~~`ClassReport` không có đường nối.~~ **Đã xử lý [đề xuất]:** thêm phụ thuộc `ClassReport ..> LanguageProfile` (tổng hợp) và `ClassReport ..> ExamRound` (lọc theo kỳ, BR-13). Cần người vẽ sơ đồ xác nhận.
> 5. **Cột của `Item` — đối chiếu từng cột với `schema.prisma` (xử lý F5, bảng ở Mục IV.11):** `exposureRate`, `pValue`, `itemFitMnsq` **không có trong schema** (đã bỏ khỏi `.puml`/`.mmd`). Nhưng `calibrated`, `timesUsed` **còn trong schema** dù Class Diagram (họp 2026-09-18) đã bỏ; và các cột audit `approvedBy`, `approvedAt`, `createdAt`, `updatedAt` có trong schema mà **chưa vẽ** trong sơ đồ. **[cần xác nhận]**: hoặc vẽ thêm vào sơ đồ, hoặc bỏ cột khỏi schema. Phiên 22 **không tự quyết**, giữ nguyên sơ đồ.
> 7. **[đề xuất, mới — Phiên 25]** Toàn bộ tên lớp/chữ ký ở Nhóm 8 (Mục VI-D) là đề xuất của AI theo Mục 10–11 của kế hoạch AI bản 5, riêng `ItemImportService` là lớp AI **tự thêm** (Mục 11 kế hoạch không liệt kê lớp điều phối lưới tạm cho import đề, nhưng UCADM12 cần một lớp tương đương `UserImportService`) — chờ duyệt. Ngưỡng/mô hình của lọc trùng (Q-7, Q-9), bản quyền ngân hàng tham chiếu (Q-8), `pg_trgm` trên staging (Q-10) **chưa chốt**.
> 6. **[đề xuất, mới]** Toàn bộ chữ ký phương thức và tên lớp mới ở Nhóm 6–7 (xem Mục VI.B) là đề xuất; `ImportReport`, `ImportRowResult`, `ImportRowStatus` theo MD-11 nhưng **giá trị `ImportRowStatus` đã đổi** (VALID / REJECTED / IGNORED_DUPLICATE) vì DC-22 bỏ `SKIPPED` — chờ chốt.

---

## I. TỔNG QUAN CÁCH ĐỌC SƠ ĐỒ

Sơ đồ là **UML Class Diagram** — bản thiết kế chi tiết các "đối tượng dữ liệu" (class) mà phần mềm sẽ quản lý, cùng các thuộc tính (dữ liệu lưu trữ) và hành vi (hàm/chức năng) của từng đối tượng. `Trang-1` gồm 8 nhóm khối chức năng, được tổ chức theo luồng nghiệp vụ. **Hệ thống phục vụ một trường duy nhất (DC-19)** nên không còn lớp `Institution`.

| Nhóm | Vai trò trong hệ thống | Các lớp chính |
|---|---|---|
| **1. Người dùng & Vai trò** | Ai được đăng nhập, vai trò gì | `User`, `Student`, `Teacher`, `Admin`, `UserRole`, `AuthProvider`, `JwtAuthProvider`, `AuthProviderType` |
| **2. Phiên thi & Thuật toán thích ứng** | Sinh viên làm bài, hệ thống chọn câu hỏi thông minh theo năng lực | `TestSession`, `CATEngine`, `SessionResponse`, `SessionCacheState`, `EAPComputationState`, `AbilityEstimate` |
| **3. Ngân hàng câu hỏi** | Kho câu hỏi thi, vòng đời trạng thái, câu nào được dùng (chỉ `FINAL_APPROVED`) | `Item` (không còn `ItemBank`), `ItemStatus`; nguồn câu hỏi ở `ItemBatch.source` (`ItemBatchSource`) |
| **4. AI Giải thích & Gợi ý** | Sau khi thi xong, AI giải thích vì sao đúng/sai và gợi ý học gì | `AIExplainerService`, `Explanation` |
| **5. Hồ sơ năng lực & Báo cáo** | Kết quả cuối cùng xuất ra cho sinh viên, giảng viên, và hệ thống EduZ | `LanguageProfile`, `SkillProfile`, `ErrorPattern`, `TestMetadata`, `ClassReport` |
| **6. Kỳ thi (mới Phiên 22)** | Sinh viên phải thuộc một kỳ đang mở mới được thi | `ExamRound`, `ExamRoundParticipant`, `ExamRoundStatus` |
| **7. Import, quản lý tài khoản, thư (mới Phiên 22)** | Admin import danh sách (lưới tạm), quản lý tài khoản, gửi mật khẩu tạm / OTP | `UserImportService`, `RosterImportService`, `AccountAdminService`, `ImportReport`, `ImportRowResult`, `ImportRowStatus`, `PasswordResetService`, `MailPort`, `SmtpMailAdapter` |
| **8. Sinh và duyệt đề AI (mới Phiên 25)** | Admin tạo đề bằng AI hoặc import file, AI kiểm, GV A duyệt, GV B confirm, Admin kiểm tra và import cuối | `ItemBatch`, `ItemBatchAssignment`, `ItemPackage`, `ItemReviewAssignment`, `ItemReviewEvent`, `ItemEmbedding`, `ItemCheckResult`, `ItemGenerationService`, `ItemImportService`, `ItemCheckService`, `ItemDuplicateChecker`, `DuplicateStrategy`, `HashStrategy`, `TrigramStrategy`, `EmbeddingStrategy`, `ReviewDistributionService`, `DeadlineReminderService`, 5 enum |

Ký hiệu trong sơ đồ dùng nhiều **khuôn mẫu thiết kế (stereotype)** đặt trong dấu `<<...>>` để nói rõ vai trò kỹ thuật của từng khối:

- `<<interface>>` — một "hợp đồng" quy định phải có chức năng gì, không tự chứa dữ liệu thật (ví dụ `AuthProvider`, `MailPort`).
- `<<abstract>>` — một khối "khuôn mẫu chung" không tồn tại độc lập, chỉ dùng để các khối con kế thừa (ví dụ `User`).
- `<<service>>` — một khối xử lý nghiệp vụ/thuật toán, không lưu trữ dữ liệu lâu dài (ví dụ `CATEngine`, `AIExplainerService`, `ClassReport`, `UserImportService`).
- `<<value object>>` — một khối dữ liệu nhỏ, "gắn liền" với một đối tượng cha, không có vòng đời riêng (ví dụ `SkillProfile`, `AbilityEstimate`, `EAPComputationState`).
- `<<aggregate root>>` — khối dữ liệu trung tâm, là điểm truy cập chính cho một nhóm dữ liệu liên quan (ví dụ `LanguageProfile`).
- `<<association class>>` — lớp liên kết giữa hai lớp, mang thêm dữ liệu của mối quan hệ (ví dụ `ExamRoundParticipant` giữa `ExamRound` và `Student`).
- `<<Enumeration>>` — danh sách các giá trị cố định được phép chọn (ví dụ `CEFRLevel` chỉ có 6 giá trị: Pre-A1, A1, A2, B1, B2, C1+).
- `<<Adapter>>`, `<<Redis>>` — đánh dấu khối cài đặt kết nối hệ thống bên ngoài (SMTP) hoặc cache Redis.


---

## II. NHÓM 1 — NGƯỜI DÙNG & VAI TRÒ

### 1. `Institution` (Trường/Đơn vị đào tạo) — **ĐÃ LOẠI BỎ (DC-19, Quyết định #97, Phiên 21–22)**
Hệ thống chỉ phục vụ **một trường** (đơn trường / single-tenant). Vì vậy **xoá** lớp `Institution`, mọi thuộc tính `institutionId` (ở `User`, `LanguageProfile`, `ClassReport`) và mọi quan hệ `Institution–User`, `Institution–EduZServiceAccount`, `LanguageProfile–Institution`; ở tầng dữ liệu xoá bảng `institutions`, cột `institution_id`, các composite FK / CHECK theo trường. Không còn bộ chọn đơn vị, `AccessScope`, `resolveScope`.

- **Hệ quả phân quyền:** chỉ còn kiểm tra theo `role` (xem II.4). Muốn phục vụ nhiều trường (multi-tenant) là phạm vi **Khóa luận** và phải làm lại schema.
- *(Lịch sử: Quyết định #15 từng chốt `Institution 1—1..* User`; DC-19 thay thế hoàn toàn.)*

### 2. Truy cập M2M của hệ sinh thái EduZ — **KHÔNG phải một class/entity riêng** (không đổi so với bản cũ)
> ⚠️ **Điều chỉnh so với sơ đồ gốc `TLCN-Phương.drawio.png`:** Sơ đồ gốc có vẽ một class riêng `EduZServiceAccount` (`<<M2M>>`). Sau khi đối chiếu với `SRS_TLCN (3).md` dòng 691 — bảng chốt phạm vi Must-have Tiểu luận vs Spec Khóa luận — mục "RBAC chi tiết (M2M, EduZ Service Account)" được SRS xếp rõ vào cột **Spec/Khóa luận**, không phải Must-have của Tiểu luận. Người dùng đã xác nhận (2026-09-14): **bỏ entity này khỏi phạm vi Tiểu luận**, chỉ giữ một role M2M đơn giản.
>
> **Cách hiểu lại cho Tiểu luận:** `EduZ System` là một **actor bên ngoài** (không phải `User`, không có bảng riêng trong DB). Khi EduZ gọi API (`GET /api/v1/placement-profiles/:student_id`), request đi kèm một **API Key tĩnh cấu hình qua `.env`/config**, được middleware/guard kiểm tra và gán role tương đương `EDUZ_SERVICE` (enum `UserRole`) cho request đó — tương tự cách `ADMIN`/`M2M` "pass through" trong `ProfileAccessGuard` (xem SRS Mục 15.4). Guard chỉ cho phép `GET`, không cho `POST`/`DELETE`.
>
> **Việc cần làm ở Khóa luận (không phải bây giờ):** nếu sau này cần nhiều đối tác M2M khác nhau hoặc thu hồi/luân chuyển key — lúc đó mới cần nâng cấp thành một entity `EduZServiceAccount` thật sự lưu trong DB. Trong `Trang-1`, `.puml`, `.mmd` **không có** lớp này (xử lý F9).

### 3. `AuthProvider` — `<<interface>>` và cách triển khai trong Tiểu luận
> **Xử lý Phiên 22 (cảnh báo #1 cũ):** nhóm này nay **có trong `Trang-1`**. Tiểu luận chỉ đăng nhập **email + mật khẩu** (DC-02, Quyết định #85): bỏ Google/Microsoft SSO; **EduZ SSO thuộc Khóa luận**.

Đây là "hợp đồng xác thực": bất kỳ cách đăng nhập nào cũng phải có hàm `authenticate(credentials): User`. Gói Tiểu luận chỉ có **một** cách triển khai:

- **`JwtAuthProvider`** — đăng nhập trực tiếp bằng email/mật khẩu do hệ thống tự quản lý, cấp JWT token (`issueToken`) và làm mới token (`refresh`). Mật khẩu băm bằng **argon2** (Quyết định #62).
- **`EduZSSOAdapter`** (`<<Adapter>>`) và **`EduZSSOClient`** (`<<external>>`) — **chuyển sang Khóa luận**, không còn trong sơ đồ TL (kế hoạch Mục 4.3).
- **`AuthProviderType`** (enum: `LOCAL`, `GOOGLE`, `MICROSOFT`) — kiểu của `User.authProvider`; tài khoản do Admin import luôn là `LOCAL`. Hai giá trị còn lại chỉ được giữ vì `schema.prisma` chưa đổi (**[cần xác nhận]** có rút không).
- **Ý nghĩa nghiệp vụ:** vẫn giữ mẫu Adapter/interface để Khóa luận có thể cắm thêm SSO mà không sửa logic xác thực lõi.

### 4. `User` — `<<abstract>>` (Người dùng — khuôn mẫu chung)
Không tồn tại độc lập, chứa các thông tin **chung cho mọi loại người dùng**: `id`, `email`, `passwordHash`, `fullName`, `role`, `authProvider`, `createdAt`, và (Phiên 22) **`mustChangePassword`** (bắt buộc đổi mật khẩu ở lần đăng nhập đầu, DC-03), **`passwordChangedAt`**, **`isActive`** (khóa tài khoản, DC-23; `false` ⇒ không đăng nhập được). Phương thức mới: **`changePassword(currentPassword, newPassword)`** (UCSV08; độ dài tối thiểu mật khẩu mới **chờ chốt, Q-4, đề xuất 8**). Vai trò `role` được xác định theo enum `UserRole` gồm: `STUDENT`, `TEACHER`, `ADMIN`, `EDUZ_SERVICE`. **Không có `institutionId`** (DC-19).

> **[cần xác nhận]** `schema.prisma` còn cột `external_id` (dùng cho SSO) mà sơ đồ chưa vẽ; `studentCode`/`teacherCode` trong schema nằm ở bảng riêng `student_profiles`/`teacher_profiles` còn sơ đồ để trên `Student`/`Teacher` (đúng mức khái niệm).

Ba lớp con kế thừa từ `User` (hollow-triangle inheritance), mỗi lớp là **một vai trò cụ thể** trong hệ thống:

| Vai trò | Field/Method riêng trong sơ đồ | Việc chính trong hệ thống |
|---|---|---|
| **`Student`** (Sinh viên) | `studentCode`; `getLatestProfile(): LanguageProfile`; `getTestHistory(): TestSession[]` | Thuộc danh sách một hoặc nhiều `ExamRound` (qua `ExamRoundParticipant`); làm bài thi thích ứng (`TestSession`) trong kỳ đang mở; nhận kết quả (`LanguageProfile`) |
| **`Teacher`** (Giảng viên) | `teacherCode`; **[đề xuất, Phiên 25]** `editItem(itemId, content)`, `reviewItem(itemId, approve)`, `sendPackage(batchId): ItemPackage` (vai trò **A**), `confirmItem(itemId, confirm)` (vai trò **B**) | Xem kết quả (DC-18): báo cáo lớp (`ClassReport`), tra cứu hồ sơ SV; đổi/quên mật khẩu. **Thêm Phiên 25 (DC-27, DC-40):** chỉ khi được Admin giao việc — **A** sửa/duyệt/từ chối các câu được giao và gửi gói; **B** (một GV, không thuộc nhóm A) xác nhận/loại từng câu. **Không** import đề, **không** thêm câu bằng form, **không** dùng `ExamRound`/import tài khoản |
| **`Admin`** (Quản trị của trường) | **[đề xuất, Phiên 25]** `createAIBatch(skill, cefr, topicTag, count): ItemBatch`; `assignBatch(batchId, reviewerIds, confirmerId, reviewDays, confirmDays)`; `runFinalCheck(batchId)`; `decideSoftFlag(itemId, accept)`; `importBatch(batchId)`. *(Ba phương thức `approveItem`/`rejectItem`/`updateContentItem` của Phiên 22 **đã gỡ**: Admin không còn sửa/duyệt nội dung câu — DC-29.)* | Siêu tập của `Teacher` + tạo lô đề (AI hoặc import file qua `ItemImportService`), giao việc, theo dõi/chỉnh hạn/giao lại, bấm Kiểm tra (C3) và Import cuối; tạo/công bố/đóng `ExamRound` và import danh sách thi, import + quản lý tài khoản SV/GV, nâng/thu hồi Admin (xem Nhóm 6–8). **Không** sửa nội dung câu |

#### Phân biệt quyền chi tiết giữa các vai trò (đối chiếu SRS Mục 15.3–15.4, DC-18, DC-19, kế hoạch Mục 3.8)

> **Lưu ý:** phân quyền chỉ theo `role` (BR-16, `RolesGuard` dùng chung); `403` khi không đủ quyền. Admin đầu tiên được tạo bằng **seed**. Ma trận đầy đủ: kế hoạch Mục 3.8.

**a. `Student` — chỉ thao tác trên dữ liệu của chính mình**
- Chỉ bắt đầu `TestSession` khi thuộc `ExamRoundParticipant` của một kỳ đang mở (BR-10); mỗi kỳ tối đa một phiên không `ABANDONED`.
- Xem `LanguageProfile` **của chính mình** — API `GET /placement-profiles/:student_id` bắt buộc `student_id` khớp `sub` trong JWT (SRS 15.4).
- **Không có quyền gì** trên `Item`; không xem được câu hỏi + đáp án đúng trước khi nộp bài (SRS 15.3).

**b. `Teacher` — xem kết quả (DC-18) + duyệt/confirm đề khi được giao (DC-27, DC-40, Phiên 25)**
- Xem `ClassReport` (lọc theo kỳ) và `LanguageProfile` của sinh viên (không còn giới hạn theo trường vì chỉ có một trường).
- Chỉ thấy câu/gói **của mình** trong vai trò A hoặc B (`NOT_ASSIGNED` 403 nếu không đúng người).
- Không import đề, không thêm câu bằng form, không tạo kỳ thi, không import danh sách, không quản lý tài khoản.

**c. `Admin` — Admin của trường, siêu tập của `Teacher` (DC-18, DC-19)**
> Quyết định gốc 2026-09-14 ("Admin = siêu tập của Teacher + quản trị") **giữ nguyên**, nhưng phần "không giới hạn theo `institution_id`" **không còn ý nghĩa** (đơn trường).
> - Mọi quyền của `Teacher`; **Phiên 25 (DC-27…DC-29):** tạo lô đề (AI sinh hoặc import file), giao việc cho GV A/B, kiểm tra (C3) và import cuối thành `FINAL_APPROVED`; **không** soạn/sửa/duyệt nội dung câu (đảo DC-18 cũ "Admin tự duyệt").
> - Tạo/công bố/đóng `ExamRound`, import danh sách thi, theo dõi dự thi (UCADM15–17, actor = Admin).
> - Import tài khoản SV/GV (UCADM08, đề xuất mở rộng — DC-24), tạo từng người, quản lý tài khoản SV và GV, khóa/mở khóa, gửi lại mật khẩu tạm, **nâng/thu hồi Admin** (UCADM09; không thu hồi Admin cuối cùng, BR-18).

**d. `EduZ System (M2M)` — không phải `User`, xem lại mục 2 ở trên**
Chỉ có quyền `GET` hồ sơ năng lực qua API Key cấu hình, không `POST`/`DELETE`, không liên quan gì đến `Item`/`ClassReport`.


---

## III. NHÓM 2 — PHIÊN THI & THUẬT TOÁN THÍCH ỨNG (TRÁI TIM HỆ THỐNG)

### 5. `TestSession` (Phiên làm bài thi)
Đại diện cho **một lượt sinh viên làm bài thi**, từ lúc bắt đầu đến lúc nộp bài. Lưu `id`, `studentId`, **`examRoundId`** (kỳ thi mà phiên thuộc về, **NOT NULL**, Phiên 22), **`responses: List<SessionResponse>`** (field tường minh), `status` (enum `SessionStatus`), `thetaFinal`, `seFinal`, `startedAt`/`completedAt`, **`expiresAt`** (hạn phiên, Phiên 22) và `stoppingReason` (enum `StoppingReason`).

- **`expiresAt` (DC-20):** `min(startedAt + durationMinutes của kỳ, closesAt của kỳ)`, tính **một lần lúc bắt đầu phiên** và lưu DB (sửa kỳ sau đó không đổi hạn phiên đang chạy). Quá hạn ⇒ luật K5/#77: đã trả lời ≥ 8 câu ⇒ `COMPLETED` + `TIMEOUT`, ít hơn ⇒ `ABANDONED`.
- **Hành vi chính:** `start()`, `submitResponse(itemId, answer)`, `getNextItem(): Item`, `computeResult(): LanguageProfile`, `reconstructFromResponses()`.
- **Liên kết:**
  - `Student` **1** — "has" — **0..\*** `TestSession` (một sinh viên có thể có nhiều lượt thi, nhưng chỉ một phiên không `ABANDONED` trên mỗi kỳ — chốt bằng partial unique index ở DB, không phải bội số trên sơ đồ).
  - **`ExamRound` 1 — 0..\* `TestSession`** (mới): ở DB là composite FK `(exam_round_id, student_id) → exam_round_participants`, nên SV không thuộc kỳ thì **không thể** có phiên trong kỳ đó. *(Kế hoạch Mục 4.3 ghi bội số `1..*` ở đầu `TestSession`; Phiên 22 dùng `0..*` vì một kỳ mới tạo chưa có phiên nào — **[cần xác nhận]**.)*
  - `TestSession` **1** ◆ (composition) — **0..\*** `SessionResponse` — xoá `TestSession` thì toàn bộ `SessionResponse` của nó cũng mất theo.
  - `TestSession` **1** — **1** `LanguageProfile` — một phiên thi hoàn tất sinh ra một hồ sơ năng lực.
  - `TestSession` **1** — `SessionCacheState` — đồng bộ trạng thái tạm thời qua Redis.
  - `TestSession` **phụ thuộc (dependency)** vào `CATEngine`; chiều ngược `CATEngine → TestSession` cũng được vẽ (CATEngine đọc phiên để tính).

### 6. `CATEngine` (Bộ máy thi thích ứng) — `<<service>>`
Đây là **thuật toán lõi** của cả hệ thống: Computerized Adaptive Testing (CAT) dựa trên mô hình Rasch (IRT 1PL). Không lưu trữ dữ liệu cố định của riêng ai — nó chỉ là "cỗ máy tính toán" được gọi mỗi khi cần.

> **Hiểu đơn giản (không cần công thức):** Hãy tưởng tượng `CATEngine` như một **giáo viên hỏi vấn đáp thông minh**, không phải một đề thi in sẵn cùng thứ tự câu hỏi cho mọi người:
> 1. Câu đầu tiên, giáo viên đoán trình độ SV ở mức "trung bình yếu" và hỏi một câu tầm đó (`thetaInit = -0.5`); kỹ năng hỏi trước (Vocabulary/Grammar) được chọn **ngẫu nhiên 50/50** rồi xen kẽ cố định từ câu 2 — đây là việc `pickNextSkill()` làm.
> 2. Sau mỗi câu trả lời, giáo viên **cập nhật lại đánh giá** về trình độ SV — việc `computeEAP()` làm.
> 3. Việc chọn câu tiếp theo (`selectNextItem()`) không lấy đúng 1 câu "khớp nhất" mà chọn ngẫu nhiên trong nhóm 5 câu gần khớp nhất.
> 4. Giáo viên **dừng hỏi** (`checkStoppingCriterion()`) ngay khi đã đủ tự tin, hoặc khi SV quá giỏi/quá yếu so với Item Bank hiện có, hoặc khi đã hỏi đủ 25 câu / hết 45 phút.

- **Tham số cấu hình:** `thetaInit: float = -0.5`, `priorMean: float = 0.0`, `priorVariance: float = 1.0`, `quadraturePoints: int = 41`.
- **Hành vi chính (khớp đúng sơ đồ mới):**
  - `pickNextSkill(session: SessionCacheState): Skill` — chọn kỹ năng (Vocabulary/Grammar) cho câu tiếp theo. **Method mới xuất hiện tường minh trong sơ đồ** — trước đây chỉ có trong quyết định thiết kế ở `tracking/feature-plans/f03-cat-engine.md` (2026-09-14: random 50/50 câu 1, alternate cố định từ câu 2, đọc `lastSkillPicked` từ `SessionCacheState`).
  - `selectNextItem(session, pool): Item` — chọn câu hỏi phù hợp nhất với năng lực hiện tại từ danh sách `Item` khả dụng (`pool` lấy qua `Item.findForCAT(...)`, xem Mục IV).
  - `computeEAP(responses[]): AbilityEstimate` — tính lại năng lực (θ) sau mỗi câu trả lời.
  - `checkStoppingCriterion(session): StoppingReason` — kiểm tra điều kiện dừng bài thi.
- **Liên kết:** `CATEngine` **đọc (Use, dependency)** dữ liệu từ `Item`, `SessionResponse`, `SessionCacheState`, và **tạo ra** `AbilityEstimate` sau mỗi lượt — không sở hữu bất kỳ dữ liệu nào trong số đó.

#### Giải thích chi tiết — đối chiếu công thức gốc trong `SRS_TLCN (3).md` Mục 4.1–4.5

> Mục này tồn tại để bảo vệ được từng số liệu khi hỏi/đáp (GVHD/hội đồng), không chỉ nhắc lại tên tham số.

**a. Vì sao là `<<service>>`, không lưu dữ liệu**
`CATEngine` không có bảng riêng trong DB, không có `id` gắn với một sinh viên cụ thể. Mỗi lần được gọi, nó nhận **input** (một `TestSession`/`SessionCacheState` đang chạy + danh sách `Item` khả dụng) và trả **output** (câu hỏi kế tiếp hoặc một `AbilityEstimate` mới) — giống một hàm toán học thuần theo nghĩa nghiệp vụ. State thật (θ hiện tại, câu đã dùng, kỹ năng câu trước...) nằm ở `SessionCacheState`/`EAPComputationState`, không nằm trong `CATEngine`.

**b. Bốn tham số cấu hình — vì sao đúng những giá trị đó**
- `thetaInit = -0.5`: θ₀ — điểm khởi tạo để chọn **câu hỏi đầu tiên**. SRS Mục 4.2: bản đầu dùng θ₀ = 0.0 (ranh giới A2/B1) nhưng bị sửa vì sinh viên cao đẳng năm nhất thường yếu hơn mặt bằng chung. `-0.5` nằm giữa dải A2 (`-1.0` đến `0.0`).
- `priorMean/priorVariance`: phân phối **Prior Bayes N(μ=0, σ²=1)** — khác vai trò với `thetaInit` (SRS Mục 4.3): `thetaInit` chỉ ảnh hưởng câu đầu tiên; Prior ảnh hưởng **toàn bộ quá trình ước lượng EAP** suốt bài thi (hiệu ứng shrinkage).
- `quadraturePoints = 41`: số điểm rời rạc dùng để tính tích phân EAP bằng **lưới đều 41 điểm trên `[-4, +4]`, bước `0.2`, prior N(0,1)** (tích phân số kiểu hình thang; không phải Gaussian–Hermite quadrature).

**c. `pickNextSkill(session)` — quyết định thiết kế đã chốt, giờ chính thức lên sơ đồ**
Round-robin **không** dựa theo tỷ lệ Item Bank (160 Vocab : 120 Grammar) mà dựa trên số câu đã hỏi trong session; câu 1 random 50/50, từ câu 2 alternate cố định theo skill đã ra ở câu 1. Cần lưu `lastSkillPicked` trong `SessionCacheState` (đã có trong sơ đồ) và **khôi phục đúng giá trị này** trong `reconstructFromDB()` khi Redis mất dữ liệu — nếu không sẽ random lại giữa bài thi, phá vỡ pattern alternate.

**d. `selectNextItem(session, pool)` — không phải "chọn câu gần θ nhất"**
SRS Mục 4.4: nếu chọn **tất định** câu có độ khó `b_i` gần θ̂ nhất, mọi sinh viên khởi tạo cùng `θ₀ = -0.5` sẽ luôn nhận **đúng cùng một câu đầu tiên**. Thuật toán thật (**Randomized Top-5 b-matching**): lọc câu chưa dùng + `FINAL_APPROVED` + đúng `skill`, sắp theo `|b_i − θ̂|` tăng dần, lấy Top-5, chọn ngẫu nhiên đều 1 câu (mỗi câu 20%).

> **Điều kiện bắt buộc:** filter `status = 'FINAL_APPROVED'` (đổi tên từ `APPROVED`, DC-39) phải nằm ở tầng **Repository** (`Item.findForCAT`), không phải business logic của `CATEngine`.

**e. `computeEAP(responses[])` — công thức và các "guard" bắt buộc**

$$\hat\theta_{EAP} = \frac{\sum_{k=1}^{41}\theta_k \cdot L(\mathbf{u}|\theta_k)\cdot\pi(\theta_k)}{\sum_{k=1}^{41} L(\mathbf{u}|\theta_k)\cdot\pi(\theta_k)}$$

Hai "guard" bắt buộc: **MLE Fallback Guard** (chỉ dùng khi có ≥1 đúng + 1 sai, luôn clip θ về `[-4, +4]`) và 3 test case bắt buộc (toàn đúng, toàn sai, xen kẽ).

**f. `checkStoppingCriterion(session)` — 4 điều kiện dừng, kiểm tra theo đúng 1 thứ tự**

| Ưu tiên | Điều kiện | Khi nào đúng |
|---|---|---|
| 1 | Đủ tin cậy | `SE(θ̂) < 0.35` |
| 2 | Chạm biên (Boundary Stop) | `θ > 1.5` hoặc `θ < -2.5`, và `ΔSE < 0.01` qua 3 câu liên tiếp, sau ≥8 câu |
| 3 | Hết số câu | Đã hỏi 25 câu |
| 4 | Hết giờ | Quá 45 phút |

### 7. `EAPComputationState` — `<<value object>>` (MỚI — 2026-09-18)
Gói trạng thái tính toán Bayesian **đang dang dở** của một phiên thi: `posteriorWeights: float[41]` (trọng số xác suất hậu nghiệm tại 41 điểm quadrature), `theta: float`, `standardError: float`.

- **Vì sao cần tách riêng thành 1 class:** trước đây `SessionCacheState` giữ rời rạc 2 field `theta`/`se`; nay được gom vào `EAPComputationState` để (1) đóng gói đúng 1 khối dữ liệu "trạng thái ước lượng năng lực" thay vì rải rác, và (2) làm rõ đây chính là input/output của `computeEAP()` — không lẫn với các field quản lý phiên khác (`state`, `currentItemId`...).
- **Liên kết:** `SessionCacheState` **1** ◆ (composition) — **1** `EAPComputationState` — luôn tồn tại kèm theo, không có vòng đời riêng.

### 8. `AbilityEstimate` (Ước lượng năng lực) — `<<value object>>`
Một "gói kết quả nhỏ" do `CATEngine.computeEAP()` sinh ra: `theta`, `standardError`, `confidenceInterval95: float[]`.

- **Liên kết mới (2026-09-18):** ngoài việc `CATEngine` tạo ra, `LanguageProfile` giờ **chứa tường minh (composition, `abilityEstimate: AbilityEstimate`)** một `AbilityEstimate` — trước đây quan hệ này chỉ ngầm hiểu qua field rời rạc `theta`/`standardError` bên trong `LanguageProfile`. Xem Mục VI.

### 9. `SessionResponse` (Câu trả lời trong phiên thi)
Ghi lại **từng câu trả lời cụ thể**: `sessionId`, `itemId`, `response: char`, `isCorrect: boolean`, `thetaAfter`/`seAfter`, `responseTimeMs`, `answeredAt`.

- **Liên kết:**
  - `TestSession` **1** ◆ — **0..\*** `SessionResponse` (composition — xem Mục 5).
  - `SessionResponse` **0..\*** — **1** `Item` (mỗi câu trả lời tham chiếu đúng một câu hỏi đã hỏi).
  - **Thay đổi 2026-09-18 — không còn `Explanation` gắn ở đây:** bản cũ mô tả mỗi `SessionResponse` có thể có 1 `Explanation` riêng (composition). Sơ đồ mới chuyển quan hệ này sang `Item` (xem cảnh báo #2 ở đầu tài liệu và Mục V.13).

### 10. `SessionCacheState` (Trạng thái phiên thi trong bộ nhớ đệm) — `<<Redis>>`
Đại diện cho dữ liệu tạm thời của một phiên thi lưu trong **Redis**: `state: SessionState`, `currentItemId: UUID`, **`eapState: EAPComputationState`** (composition — thay cho 2 field rời rạc `theta`/`se` trước đây), **`lastSkillPicked: Skill`** (field mới, phục vụ `pickNextSkill()`), `itemsAdministered: UUID[]`, `lastUpdated: DateTime`, `ttlSeconds: int = 7200`.

- **Vì sao cần:** Giúp bài thi phản hồi nhanh (< 300ms) và **chống gian lận kỹ thuật**.
- **Cơ chế khôi phục:** `reconstructFromDB(): void` — dựng lại toàn bộ trạng thái (kể cả `eapState` và `lastSkillPicked`) từ lịch sử `SessionResponse` trong DB nếu Redis mất dữ liệu.

---

## IV. NHÓM 3 — NGÂN HÀNG CÂU HỎI

> ⚠️ **`ItemBank` đã bị bỏ hẳn khỏi sơ đồ** (quyết định 2026-09-18, `tracking/weekly-log/Tuan-01.md`; xử lý F8 — `.puml` cũ còn `ItemBank`, đã gỡ). Hàm tìm câu cho CAT (`findForCAT`) là **method trên chính `Item`**. **Phiên 25:** `Admin` không còn quan hệ `create/approve` trực tiếp với `Item` (cạnh đã gỡ); mọi câu mới đi qua một `ItemBatch` (Nhóm 8, Mục VI-D).

### 11. `Item` (Câu hỏi)
Đại diện cho **một câu hỏi trắc nghiệm** cụ thể: `content: String`, `options: Map<char, String>`, `correctAnswer: char`, `skill: Skill`, `topicTag: String`, `cefrTarget: CEFRLevel`, `irtB: float`, `irtA: float`, `irtC: float` *(reserved — dự phòng 2PL/3PL Khóa luận)*, `status: ItemStatus`, và (Phiên 25) `contentHash: String` (băm chuẩn hóa nội dung + đáp án + giải thích, phục vụ lọc trùng T1 và tái sử dụng kết quả check), `batchId: UUID` (**bắt buộc** từ 16/10/2026: mọi câu thuộc một lô; câu seed thuộc các lô seed `IMPORTED`/`DONE`; **`Item` không còn `source`**, nguồn suy ra từ `ItemBatch.source`), `packageId: UUID?` (chỉ có sau khi GV A gửi gói).

**Đối chiếu từng cột với `schema.prisma` (xử lý F5; không đoán):**

| Cột / field | Trong `Trang-1` | Trong `schema.prisma` (`items`) | Kết luận Phiên 22 |
|---|---|---|---|
| `id, content, options, correctAnswer, skill, topicTag, cefrTarget, irtB, irtA, irtC, status` | Có | Có | Khớp (`source` đã bỏ khỏi `Item`, 16/10/2026) |
| `contentHash`, `batchId`, `packageId` | Có (Phiên 25) | Có (`content_hash`, `package_id` nullable; `batch_id` NOT NULL từ 16/10/2026) | Khớp |
| `exposureRate`, `pValue`, `itemFitMnsq` | Không | **Không có** | Bỏ khỏi `.puml`/`.mmd` (từng thừa) |
| `calibrated`, `timesUsed` | Không (bỏ theo họp 2026-09-18) | **Còn** (`calibrated`, `times_used`) | **[cần xác nhận]** bỏ cột khỏi schema hay vẽ lại vào sơ đồ |
| `approvedBy` (FK → `User`), `approvedAt`, `createdAt`, `updatedAt` | Không vẽ | **Có** | **[cần xác nhận]** (cảnh báo #5): vẽ thêm hay coi là giản lược hình vẽ |

- **Hành vi:** **`transitionTo(next: ItemStatus): void`** *(Phiên 25, [đề xuất]; thay `approve()`/`reject()` — một chiều `DRAFT → FIRST_APPROVED → SECOND_APPROVED → FINAL_APPROVED`, hoặc sang `REJECTED`/`AI_REJECTED`, không có đường quay lại; chuyển sai chiều bị chặn)*, `probability(theta: float): float` (công thức lõi Rasch), và **`findForCAT(skill, usedIds, theta): Item[]`** (truy vấn Repository lấy câu ứng viên cho `CATEngine.selectNextItem()`; bắt buộc lọc `status = 'FINAL_APPROVED'` ở Repository).
- **`Skill` chỉ còn `VOCABULARY`, `GRAMMAR`** (F1: bỏ `WRITING`, khớp #22/A5 và schema).
- **Điểm quan trọng về nghiệp vụ:** Chỉ `Item` có `status = FINAL_APPROVED` mới được `CATEngine` chọn vào bài thi thật. Khoảng `irtB` hợp lệ khi lọc đề là **[−4, +4]** (cấu hình, DC-34; khác `CLAUDE.md` cũ ghi −2.5…+1.5 — `CLAUDE.md` chỉ được đề xuất diff, không sửa ở đây).
- **Liên kết:**
  - ~~`Admin` 1 — "create/approve" — 0..\* `Item`~~ **đã gỡ Phiên 25**; thay bằng `Admin` 1 — "creates" — 0..\* `ItemBatch` và `Item` 0..\* — 1 `ItemBatch` (Mục VI-D).
  - `Item` **sử dụng (Use, dependency)** 3 enum: `Skill`, `CEFRLevel`, `ItemStatus`; `ItemBatch` sử dụng `ItemBatchSource`.
  - `Item` **1** ◆ (composition) — **0..1** `Explanation` — xem Mục V.13.
  - **Mới Phiên 25:** `Item` **0..\*** — **1** `ItemBatch` ("belongs to"; cột `batch_id` nullable); `Item` **0..\*** — **0..1** `ItemPackage` ("groups"); `Item` **1** ◆ **0..1** `ItemReviewAssignment`; `Item` **1** ◆ **0..\*** `ItemCheckResult`; `Item` **1** ◆ **0..1** `ItemEmbedding`.

---

## V. NHÓM 4 — AI GIẢI THÍCH & GỢI Ý HỌC TẬP

### 12. `AIExplainerService` (Dịch vụ AI giải thích) — `<<service>>`
Là lớp gọi đến **Gemini API** để sinh lời giải thích (Phiên 25: giải thích của câu AI sinh được tạo **cùng lúc** với câu hỏi trong `ItemGenerationService`; `AIExplainerService` còn dùng cho câu import thiếu giải thích — phân chia trách nhiệm chính xác giữa hai lớp là **[cần xác nhận]**), cấu hình bằng `modelName: String`, `systemPrompt: String`.

- **Hành vi chính (khớp đúng sơ đồ mới):**
  - `explain(item: Item): Explanation` — sinh lời giải thích cho **một câu hỏi** (không còn nhận `response` làm tham số như bản cũ — xem cảnh báo #2).
  - `buildPrompt(item: Item, context: String): String`, `callGeminiAPI(prompt: String): String` — các bước kỹ thuật xây dựng câu lệnh và gọi mô hình AI.
- **Method không còn thấy trong sơ đồ (cần xác nhận — cảnh báo #3):** `generateRecommendations(patterns: ErrorPattern[])` của bản cũ không xuất hiện nữa, trong khi `LanguageProfile.aiRecommendations: String[]` vẫn còn. Cần xác nhận nơi sinh ra gợi ý học tập.
- **Liên kết:** `AIExplainerService` **đọc (Use)** `Item`, và **tạo ra** `Explanation`.

### 13. `Explanation` (Lời giải thích) — **gắn với `Item` (đã chốt #60/#63; F3)**
Kết quả cụ thể do AI sinh ra: `id: UUID`, **`itemId: UUID`**, `content: String`, `generatedAt: DateTime`.

- **Quan hệ sở hữu:** `Item` **1** ◆ — **0..1** `Explanation`, tức **một câu hỏi có tối đa 1 giải thích, dùng chung cho mọi sinh viên**; **sinh cùng lúc sinh câu hỏi** (DC-31, xác nhận lại #60/#63; cùng lời gọi G2 của `ItemGenerationService`, câu import thiếu giải thích thì sinh bổ sung theo nhóm) rồi lưu `explanations`, không còn "lazy" khi SV xem kết quả. Khớp `explanations.item_id UNIQUE` + `ON DELETE CASCADE` trong schema. `explain(item: Item)` — không còn tham số `response` (F3: đã sửa trong `.puml`, vốn còn `explain(item, response)` và `SessionResponse o-- Explanation`).
- Cảnh báo #2 cũ về "đúng chủ đích hay không": **đã đóng** bởi #60/#63.

---

## VI. NHÓM 5 — HỒ SƠ NĂNG LỰC & BÁO CÁO

### 14. `LanguageProfile` (Hồ sơ năng lực ngôn ngữ) — `<<aggregate root>>`
**Sản phẩm đầu ra quan trọng nhất** của toàn hệ thống. Lưu: `id`, `schemaVersion: String`, `studentId`, `testSessionId`, **`abilityEstimate: AbilityEstimate`**, `completedAt`, `cefrLevel: CEFRLevel`, `cefrConfidence: CEFRConfidence`, `boundaryEffect: boolean`, `errorPatterns: List<ErrorPattern>`, `skillProfiles: List<SkillProfile>`, `aiRecommendations: String[]`, `testMetadata: TestMetadata`. **Không còn `institutionId`** (DC-19).

- **Hành vi chính:** `generateFromSession(s: TestSession): void`, `toJSON(): String`, `exportForEduZ(): String`.
- **Chứa (composition) 4 loại "khối dữ liệu con":** `AbilityEstimate` (**1**), `SkillProfile` (**1..\***), `ErrorPattern` (**0..\***), `TestMetadata` (**1**).
- **Liên kết:** Một `TestSession` (đã hoàn thành) sinh ra **đúng một** `LanguageProfile` (xem Mục III.5).
- *(Schema lưu `theta`, `standard_error`, `confidence_interval_95` phẳng trong `language_profiles` và `skill_profiles`/`error_patterns`/`test_metadata` dạng JSON — chỉ khác cách lưu, không khác mô hình khái niệm.)*

### 15. `ClassReport` (Báo cáo lớp học) — `<<service>>`
Dịch vụ cho `Teacher`/`Admin` xem tổng quan năng lực của cả một lớp/khoá. Thuộc tính **`examRoundId: UUID?` (tùy chọn, Phiên 22; BR-13)**: có giá trị ⇒ lọc theo một kỳ, bỏ trống ⇒ toàn hệ thống. **Đã bỏ `institutionId`** (DC-19).

- **Hành vi chính:** `generateClassDistribution(): Map<CEFRLevel, int>`, `exportCSV(): File`.
- **Liên kết [đề xuất, cảnh báo #4]:** `ClassReport ..> LanguageProfile` (tổng hợp dữ liệu từ nhiều hồ sơ) và `ClassReport ..> ExamRound` (lọc theo kỳ).

---

## VI-B. NHÓM 6 — KỲ THI (MỚI, DC-07…DC-10, DC-20)

> Toàn bộ nhóm này **mới ở Phiên 22**. Tên lớp và thuộc tính theo kế hoạch Mục 4.3 / Phụ lục A và `schema.prisma` (đã đối chiếu: `exam_rounds`, `exam_round_participants`). Chữ ký phương thức là **[đề xuất]**.

### 16. `ExamRound` (Kỳ thi)
Một đợt thi có cửa sổ thời gian. Thuộc tính: `id`, `name`, `createdBy` (Admin tạo), `opensAt`, `closesAt`, **`durationMinutes: int`** (D-T = T2, DC-20: thời lượng làm bài của kỳ, giới hạn 5…180 và ≤ `closesAt − opensAt`, mặc định hiển thị 45; **cột `duration_minutes` là `NOT NULL DEFAULT 45`**, không nullable), `status: ExamRoundStatus`, `createdAt`, `updatedAt`.

- **Hành vi [đề xuất]:** `isOpen(now)`, `effectiveStatus(now)` (nguồn duy nhất cho mọi quyết định "kỳ có đang mở không"; cột `status` chỉ được ghi lại lazy khi chạm tới — DC-10), `includes(student)`.
- **Ràng buộc DB (không vẽ trên sơ đồ):** `CHECK (closes_at > opens_at)`, `CHECK (duration_minutes BETWEEN 5 AND 180)`.
- **Liên kết:** `Admin` **1** — "creates" — **0..\*** `ExamRound` (DC-18: **chỉ Admin** tạo/công bố/đóng; `Teacher` không dùng); `ExamRound` **1** ◆ **0..\*** `ExamRoundParticipant`; `ExamRound` **1** — **0..\*** `TestSession`; `ClassReport ..> ExamRound`; `ExamRound ..> ExamRoundStatus`.
- **Đóng thủ công khi còn phiên đang chạy:** **chờ chốt, Q-2** (đề xuất: để phiên đang chạy theo `expiresAt`, chỉ chặn phiên mới).

### 17. `ExamRoundParticipant` — `<<association class>>` (lớp liên kết `ExamRound` ↔ `Student`)
Một dòng = một sinh viên nằm trong danh sách thi của một kỳ. Thuộc tính: `roundId`, `studentId` (khoá chính ghép), `note` (≤ 255 ký tự, tùy chọn), `addedAt`. Một sinh viên có thể thuộc **nhiều kỳ** (DC-08).

- **Liên kết:** `ExamRound` **1** ◆ **0..\*** `ExamRoundParticipant`; `Student` **1** — "participates" — **0..\*** `ExamRoundParticipant`.
- Là đích của composite FK từ `TestSession` (SV không thuộc kỳ thì không có phiên trong kỳ).

### 18. `ExamRoundStatus` — `<<Enumeration>>`
`DRAFT` → `SCHEDULED` → `OPEN` → `CLOSED` (không quay lui; `DRAFT → CLOSED` = hủy). Lưu thành cột, chuyển **lazy** (không scheduler).

---

## VI-C. NHÓM 7 — IMPORT (LƯỚI TẠM), QUẢN LÝ TÀI KHOẢN, THƯ (MỚI, DC-19…DC-23)

> **Cơ chế lưới tạm (DC-22, Quyết định #98) — thay `preview/confirm`:** mỗi lần Admin tải một file `.xlsx`, BE phân tích và **gộp vào lưới tạm** của người thao tác (lưu **Redis**, khóa theo người dùng + loại import [+ kỳ thi], TTL ~30 phút, làm mới mỗi lần thêm; **chưa ghi DB**). Dòng lỗi **bị loại khỏi lưới** và hiện popup số dòng + lý do; dòng đã có trong lưới thì **bỏ qua**; tài khoản đã tồn tại trong DB (import tài khoản) / MSSV lạ hoặc đã có trong kỳ (import danh sách thi) bị loại kèm popup. Bấm **Lưu** mới ghi DB (một transaction); hết TTL ⇒ `410 IMPORT_GRID_EXPIRED`. **Không còn** preview/confirm, all-or-nothing, trạng thái `SKIPPED`. Lưới tạm không có lớp riêng trong sơ đồ: nó được thể hiện qua kết quả trả về `ImportReport` (các dòng hợp lệ + dòng bị loại) và qua `getGrid()`.

### 19. `UserImportService` — `<<service>>` (import tài khoản sinh viên và giảng viên, UCADM08 mở rộng — DC-24, đề xuất)
Chỉ **tạo mới** tài khoản sinh viên (không cập nhật). Theo DC-24 (#99) phạm vi import gồm **cả sinh viên lẫn giảng viên**, phân biệt bằng tham số `kind` (dùng lại enum `UserRole`, chỉ nhận `STUDENT` hoặc `TEACHER`; **không tạo enum mới** — nếu sau này muốn enum riêng như `ImportKind` thì là đề xuất, chờ chốt). File SV: MSSV, Họ tên, Email; file GV: Mã GV (`teacherCode`), Họ tên, Email. Lưới tạm khóa theo `(adminId, kind)`. Sau khi **Lưu**: sinh mật khẩu tạm 12 ký tự (`crypto.randomInt`, băm argon2), đặt `mustChangePassword = true`, đẩy email qua `MailPort` (BullMQ có retry).
- **Phương thức [đề xuất]:** `upload(kind, file, adminId): ImportReport`, `getGrid(kind, adminId)`, `removeRow(kind, adminId, rowKey)`, `clearGrid(kind, adminId)`, `save(kind, adminId): int`. Khớp API `POST /users/import/upload` (tham số `kind=STUDENT|TEACHER`), `GET /users/import/grid`, `DELETE /users/import/grid[/:rowKey]`, `POST /users/import/save` (Phụ lục B kế hoạch, cũng là đề xuất).
- **Liên kết:** `Admin ..> UserImportService`; `..> ImportReport`; `..> MailPort`.

### 20. `RosterImportService` — `<<service>>` (import danh sách thi, UCADM16; actor = Admin theo DC-18)
Tra MSSV có sẵn trong hệ thống để thêm vào `ExamRound`; **không tạo tài khoản**. Cùng cơ chế lưới tạm; MSSV lạ / đã có trong kỳ bị loại kèm popup.
- **Phương thức [đề xuất]:** như `UserImportService` nhưng có `roundId` (`upload(roundId, file, adminId)`, `save(roundId): int`…). **`Teacher` không dùng lớp này.**
- **Liên kết:** `Admin ..> RosterImportService`; `..> ImportReport`.

### 21. `AccountAdminService` — `<<service>>` (quản lý tài khoản, UCADM09) **[tên chờ duyệt]**
Quản lý tài khoản sinh viên **và giảng viên**: **`createStudent(studentCode, fullName, email)` / `createTeacher(teacherCode, fullName, email)`** (tạo từng người trên giao diện — DC-24, gộp vào UCADM09, *đề xuất*; API đề xuất `POST /students`, `POST /teachers`; trùng email/MSSV/`teacherCode` ⇒ báo lỗi; sinh mật khẩu tạm 12 ký tự, argon2, `mustChangePassword = true`, gửi email qua `MailPort` sau khi lưu — giống nhánh import), `list`, `update`, `lock` / `unlock` (đặt `User.isActive`), `resendTemporaryPassword` (sinh mật khẩu tạm mới, đặt lại `mustChangePassword = true`), **`grantAdmin(teacherId)` / `revokeAdmin(adminId)`** (đổi `role` TEACHER ↔ ADMIN; **không thu hồi Admin cuối cùng**, không tự thu hồi chính mình — BR-17/18). Không xoá cứng tài khoản đã có phiên/hồ sơ (BR-19). *Chữ ký phương thức là [đề xuất].*
- **Liên kết:** `Admin ..> AccountAdminService`.

### 22. `ImportReport`, `ImportRowResult`, `ImportRowStatus` — kết quả một lần tải file **[tên theo MD-11; nội dung theo DC-22 — đề xuất]**
- **`ImportReport`**: `totalRows`, `added` (số dòng vừa vào lưới), `rejected` (số dòng bị loại), `ignoredDuplicates` (dòng đã có trong lưới nên bỏ qua), `rows: ImportRowResult[]`. *(Kế hoạch MD-11 gốc ghi `{total, valid, errors, skipped, rows}`; đổi tên trường cho khớp mô tả `{grid[], rejected[], added, ignoredDuplicates}` của DC-22 — **[cần xác nhận]**.)*
- **`ImportRowResult`**: `rowNumber`, `rowKey` (khoá dòng để xoá khỏi lưới), `status`, `message` (lý do, ví dụ "email sai định dạng", "tài khoản đã tồn tại", "đã có trong kỳ").
- **`ImportRowStatus`** (enum): `VALID` (đã vào lưới), `REJECTED` (bị loại kèm lý do), `IGNORED_DUPLICATE` (đã có sẵn trong lưới). **Đề xuất, chờ chốt** — MD-11 từng ghi `VALID/ERROR/SKIPPED`, nhưng DC-22 bỏ `SKIPPED`.
- **Liên kết:** `ImportReport` **1** ◆ **0..\*** `ImportRowResult`; `ImportRowResult ..> ImportRowStatus`.
- Không lưu DB (lưới nằm ở Redis, không có bảng `import_batches`).

### 23. `PasswordResetService` — `<<service>>` (quên mật khẩu bằng OTP, UCSV09, DC-21)
`requestReset(email)` luôn phản hồi như nhau (HTTP 202) dù email có tồn tại hay không; nếu có thì sinh OTP 6 chữ số, lưu **bản băm trong Redis TTL 10 phút**, tối đa 5 lần nhập sai, gửi qua `MailPort`. `reset(email, otp, newPassword)` kiểm OTP, đặt mật khẩu mới, xoá `mustChangePassword`; **không tự đăng nhập**. Không đổi schema. *(Chữ ký là [đề xuất]; TTL 10 phút và 5 lần là đề xuất của AI chưa hỏi.)*
- **Liên kết:** `..> MailPort`.

### 24. `MailPort` — `<<interface>>` và `SmtpMailAdapter` — `<<Adapter>>`
`MailPort.send(to, subject, body)` là cổng gửi thư (mật khẩu tạm, OTP); `SmtpMailAdapter` hiện thực qua SMTP (nodemailer) và đẩy qua hàng đợi BullMQ có retry. **Nhà cung cấp SMTP chưa chọn — chờ chốt, Q-5.** Chữ ký `send(...)` là [đề xuất] (kế hoạch ghi `send(message)`). Thất bại sau retry ⇒ ghi trạng thái "chưa gửi" để Admin xem, không rollback tài khoản (BR-05).
- **Liên kết:** `SmtpMailAdapter ..|> MailPort`; `UserImportService ..> MailPort`; `PasswordResetService ..> MailPort`.

---

## VI-D. NHÓM 8 — SINH VÀ DUYỆT ĐỀ AI (MỚI PHIÊN 25, DC-27…DC-45)

> **Nguồn:** `Tuan5/KE_HOACH_SINH_VA_DUYET_DE_AI.md` bản 5 (Mục 2, 4, 5, 6, 10, 11). Mọi **tên lớp, thuộc tính, chữ ký** ở nhóm này là **[đề xuất]** của kế hoạch/AI; các đề xuất mặc định Q-1 (O2), Q-3, Q-4, Q-5, Q-6 coi như đã được chấp nhận theo lệnh "Đồng bộ tài liệu theo kế hoạch này"; các câu hỏi về ngưỡng/mô hình (Q-7, Q-9), bản quyền (Q-8), `pg_trgm` trên staging (Q-10) **vẫn chờ chốt**.

**Luồng một chiều:** Admin tạo lô (`ItemGenerationService` hoặc `ItemImportService`) → AI check C1/C2 (`ItemCheckService`) → lô `READY_TO_ASSIGN` → Admin **Giao việc** (nhóm A nhiều GV, 1 GV B không thuộc A; `ReviewDistributionService` chia đều: sắp theo `skill`/`cefr` rồi câu thứ i cho A thứ `i mod M`) → GV A sửa/duyệt/từ chối, xong thì **Gửi cho B** (mỗi A một `ItemPackage`) → GV B Xác nhận/Loại từng câu hoặc "Xác nhận tất cả câu còn lại" (B không sửa, **không trả về** A) → khi cả lô xong hoặc quá hạn, Admin bấm **Kiểm tra** (C3 chạy theo delta) → Admin **Import** → `FINAL_APPROVED`. Quá hạn chỉ cảnh báo (không tự đổi trạng thái); nhắc trước hạn 24 giờ do `DeadlineReminderService`.

### 25. Dữ liệu của lô (6 lớp) — **[đề xuất]**
- **`ItemBatch`** — một lô đề. `id`, `source: ItemBatchSource` (`AI_GENERATED` | `IMPORTED`), `name?` (nhãn tùy chọn, dùng cho lô seed theo bộ nguồn: CEFR-J, CLOTH, GV tự soạn), `createdBy`, `skill?`/`cefrTarget?` (để trống với lô import vì mỗi dòng file tự có), `topicTag?`, `requestedCount?` (chỉ lô AI), `status: ItemBatchStatus`, `createdAt`; hành vi `canAssign()`, `canFinalize()`. Quan hệ: `Admin` 1 — "creates" — 0..\* `ItemBatch`; `ItemBatch` 1 ◆ 0..1 `ItemBatchAssignment`, 1 ◆ 0..\* `ItemPackage`, 1 ◆ 0..\* `ItemReviewEvent`.
- **`ItemBatchAssignment`** — chỉ tồn tại sau khi Admin bấm Giao việc (tránh cột trống trên lô): `batchId`, `confirmerId` (GV B), `assignedBy`, `reviewDays`, `confirmDays` (cả hai ≥ 1, CHECK ở DB), `assignedAt`. Ràng buộc "GV B không thuộc nhóm A" kiểm ở **tầng ứng dụng** (`CONFIRMER_IN_REVIEW_GROUP`, 409), không biểu diễn được bằng khóa/CHECK; nhóm A = tập `assigneeId` trong `ItemReviewAssignment` của lô.
- **`ItemReviewAssignment`** — mỗi câu giao cho đúng một GV A (`itemId` UNIQUE): `assigneeId`, `assignedAt`, `dueAt` (cuối ngày giao + `reviewDays`, 23:59:59 giờ VN), `reminderSent`; `isOverdue(now)`.
- **`ItemPackage`** — gói A gửi cho B (mỗi A đúng một gói/lô, UNIQUE `(batchId, reviewerId)`): `reviewerId`, `confirmerId`, `status: PackageStatus` (`OPEN`/`SENT`/`DONE`), `sentAt?`, `dueAt?` (cuối ngày gửi gói + `confirmDays`; hai cột nullable vì gói `OPEN` chưa gửi), `reminderSent`; `send()`, `confirmAll()`, `isComplete()`. Câu A loại **không** vào gói.
- **`ItemCheckResult`** — báo cáo mỗi lần check, gắn `contentHash` để **tái sử dụng khi hash không đổi**: `itemId`, `checkpoint: CheckPoint` (`C1`/`C2`/`C3`), `level: CheckLevel` (`PASS`/`SOFT`/`HARD`), `reasonCodes: String[]`, `suspectedDuplicateId?`, `checkedAt`. Lý do máy loại (`AI_REJECTED`) lưu ở đây, chỉ Admin xem.
- **`ItemEmbedding`** — embedding tính **đúng một lần** cho mỗi nội dung: `itemId`, `vector: float[]`, `model`, `contentHash`, `createdAt`. Cosine tính trong ứng dụng; **mô hình embedding chưa chọn (Q-9)**.
- **`ItemReviewEvent`** *(tùy chọn theo kế hoạch Mục 10; đề xuất giữ để truy vết)* — `batchId`, `itemId?`, `packageId?`, `actorId`, `action: ReviewAction`, `createdAt`.

### 26. Dịch vụ điều phối (`<<service>>`) — **[đề xuất]**
- **`ItemGenerationService`** — `createBatch(skill, cefr, topicTag, count, adminId): ItemBatch`, `generate(batchId)` (nền BullMQ: lấy k câu mẫu → sinh dư `⌈N·(1+overRate)⌉` theo từng lời gọi nhỏ trả mảng JSON gồm câu, 4 đáp án, đáp án đúng, `irt_b` gợi ý **và giải thích** → C1 → bù thiếu tối đa R vòng → cắt về N, `irt_b` khởi tạo = trung bình k mẫu, `calibrated=false`, `source=AI_GENERATED`), `supplementMissing(batchId, missing)`. Chạy qua **LLM Gateway có dự phòng**, trần lời gọi/token mỗi lô, ghi tên và phiên bản mô hình thật (TC2.3).
- **`ItemImportService`** — **lớp AI tự thêm** (Mục 11 kế hoạch không liệt kê, nhưng UCADM12 cần lớp điều phối lưới tạm DC-22 như `UserImportService`): `upload`, `getGrid`, `removeRow`, `clearGrid`, `save(adminId): ItemBatch`. Lưới nằm ở Redis (không có bảng). Dòng lỗi bị loại + popup; kiểm trùng T1–T3 ngay lúc tải lên lưới; G5 một lần khi bấm Lưu; bấm Lưu mới tạo lô `source=IMPORTED`.
- **`ItemCheckService`** — ba điểm check: `checkC1` (sau sinh; lọc nặng nhất), `checkC2` (import file), `checkC3` (trước import cuối, chạy **theo delta**: luật cứng + toàn vẹn quy trình + T1–T2 trên mọi câu, T3 chỉ câu đổi hash hoặc so với câu ngân hàng mới thêm, G5 chỉ câu A đã sửa), và `recheckAfterEdit` (chạy lại luật cứng + T1–T2 sau mỗi lần A sửa; hỏng/trùng ⇒ chặn Duyệt, `DUPLICATE_AFTER_EDIT`/`INVALID_AFTER_EDIT`, 422). **Lỗi cứng ⇒ `AI_REJECTED`; lỗi mềm ⇒ Admin quyết (Import hoặc Loại ⇒ `REJECTED`, ghi `ACCEPT_FLAG`)** — phương án O2.
- **`ItemDuplicateChecker`** + `<<interface>>` **`DuplicateStrategy`** (Strategy pattern, mở rộng thêm tầng mà không sửa `ItemCheckService`) cùng 3 cách cài đặt: **`HashStrategy`** (T1, băm chuẩn hóa), **`TrigramStrategy`** (T2, `pg_trgm`; `hardThreshold`/`softThreshold`), **`EmbeddingStrategy`** (T3, cosine; `softThreshold`, chỉ cờ mềm). Ngưỡng đặt trong cấu hình, **chờ chốt (Q-7)**; nếu staging không bật được `pg_trgm` (Q-10) thì T2 tính trong ứng dụng.
- **`ReviewDistributionService`** — `preview` (xem trước phân bổ), `assign` (tạo `ItemReviewAssignment` + `ItemBatchAssignment`, lô sang `IN_REVIEW`, đặt lịch nhắc), `reassign`, `extendDeadline`.
- **`DeadlineReminderService`** — `schedule` (job trễ BullMQ lúc `dueAt − 24 giờ`, một thông báo gộp mỗi (lô, bước, GV, gói), qua `MailPort`), `remindDue`, `markOverdue` (đối chiếu lazy; chỉ hiển thị quá hạn, **không** tự đổi trạng thái hay tự giao lại).

### 27. Các enum mới (5)
`ItemBatchStatus` (GENERATING, IMPORTING, CHECKING, READY_TO_ASSIGN, IN_REVIEW, READY_TO_FINALIZE, FINAL_CHECKED, DONE, FAILED, PARTIAL), `PackageStatus` (OPEN, SENT, DONE), `CheckPoint` (C1, C2, C3), `CheckLevel` (PASS, SOFT, HARD), `ReviewAction` (APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG). Hai enum cũ được sửa: `ItemStatus` và `ItemSource` (Mục VIII).

### 28. Mã use case đề xuất tương ứng
`UCADM11` Tạo lô AI, `UCADM12` Import đề (lưới tạm), `UCADM13` Giao việc và theo dõi, `UCADM14` Kiểm tra và import cuối, `UCGV14` A duyệt và gửi gói, `UCGV15` B confirm; bỏ UCGV03, thay UCGV05, sửa UCGV02/04/06 (đặc tả Use Case do nhóm tài liệu khác cập nhật — không thuộc tài liệu này).

---

## VII. BẢNG TỔNG HỢP QUAN HỆ GIỮA CÁC LỚP

Danh sách dưới đây khớp 1-1 với **89 quan hệ** trong `TLCN.drawio.xml` / `ClassDiagram.puml` / `ClassDiagram.mmd` (kiểm bằng script; các mũi tên "Use" từ lớp tới enum chỉ liệt kê những cạnh đang được vẽ).

| Từ lớp | Đến lớp | Kiểu quan hệ | Ghi chú |
|---|---|---|---|
| `Admin`, `Student`, `Teacher` | `User` | Kế thừa | Ba vai trò cụ thể hoá từ khuôn mẫu người dùng chung |
| `User` | `UserRole`, `AuthProviderType` | Sử dụng (Use) | Hai enum của `User` |
| `JwtAuthProvider` | `AuthProvider` | Hiện thực hoá (implements) | Chỉ `JwtAuthProvider` trong gói TL; `AuthProvider ..> User` (`authenticate`) |
| `Admin` | `ExamRound` | 1 → 0..\* ("creates") | **Mới** (DC-18: chỉ Admin tạo kỳ) |
| `ExamRound` | `ExamRoundParticipant` | 1 - 0..\* (composition ◆) | **Mới** |
| `Student` | `ExamRoundParticipant` | 1 → 0..\* ("participates") | **Mới** |
| `ExamRound` | `TestSession` | 1 → 0..\* ("has") | **Mới** (xem Mục III.5 về bội số) |
| `ExamRound` | `ExamRoundStatus` | Sử dụng (Use) | **Mới** |
| `ClassReport` | `ExamRound` | Phụ thuộc | **Mới** (lọc theo kỳ) |
| `Admin` | `UserImportService`, `RosterImportService`, `AccountAdminService` | Phụ thuộc (Use) | **Mới**; `Teacher` **không** có các quan hệ này |
| `UserImportService`, `RosterImportService` | `ImportReport` | Phụ thuộc (Use) | **Mới** |
| `ImportReport` | `ImportRowResult` | 1 - 0..\* (composition ◆) | **Mới** |
| `ImportRowResult` | `ImportRowStatus` | Sử dụng (Use) | **Mới** |
| `UserImportService`, `PasswordResetService` | `MailPort` | Phụ thuộc (Use) | **Mới** |
| `SmtpMailAdapter` | `MailPort` | Hiện thực hoá | **Mới** |
| `Student` | `TestSession` | 1 - 0..\* ("has") | Một sinh viên có thể có nhiều lượt thi |
| ~~`Admin`~~ | ~~`Item`~~ | ~~1 → 0..\* ("create/approve")~~ | **Đã gỡ Phiên 25** (DC-29: Admin không soạn/duyệt nội dung câu); thay bằng `Admin → ItemBatch` bên dưới |
| `Admin` | `ItemBatch` | 1 → 0..\* ("creates") | **Mới Phiên 25** |
| `Admin` | `ItemGenerationService`, `ItemImportService`, `ReviewDistributionService`, `ItemCheckService` | Phụ thuộc (Use) | **Mới Phiên 25** (4 cạnh); `Teacher` không có |
| `Teacher` | `ItemReviewAssignment` | 1 → 0..\* ("reviews (A)") | **Mới Phiên 25** |
| `Teacher` | `ItemPackage` | 1 → 0..\* ("sends / confirms (B)") | **Mới Phiên 25** |
| `Item` | `ItemBatch` | 0..\* → 1 ("belongs to") | **Mới Phiên 25** (`items.batch_id` nullable) |
| `Item` | `ItemPackage` | 0..\* → 0..1 ("groups") | **Mới Phiên 25** (`items.package_id` nullable) |
| `Item` | `ItemReviewAssignment`, `ItemEmbedding` | 1 - 0..1 (composition ◆) | **Mới Phiên 25** |
| `Item` | `ItemCheckResult` | 1 - 0..\* (composition ◆) | **Mới Phiên 25** |
| `ItemBatch` | `ItemBatchAssignment` | 1 - 0..1 (composition ◆) | **Mới Phiên 25** |
| `ItemBatch` | `ItemPackage`, `ItemReviewEvent` | 1 - 0..\* (composition ◆) | **Mới Phiên 25** (2 cạnh) |
| `ItemBatch` | `ItemBatchStatus` | Sử dụng (Use) | **Mới Phiên 25** |
| `ItemPackage` | `PackageStatus` | Sử dụng (Use) | **Mới Phiên 25** |
| `ItemReviewEvent` | `ReviewAction` | Sử dụng (Use) | **Mới Phiên 25** |
| `ItemCheckResult` | `CheckPoint`, `CheckLevel` | Sử dụng (Use) | **Mới Phiên 25** (2 cạnh) |
| `ItemGenerationService`, `ItemImportService` | `ItemBatch` | Phụ thuộc (Use) | **Mới Phiên 25** (2 cạnh) |
| `ItemGenerationService`, `ItemImportService` | `ItemCheckService` | Phụ thuộc (Use) | **Mới Phiên 25** (2 cạnh; C1/C2) |
| `ItemImportService` | `ImportReport` | Phụ thuộc (Use) | **Mới Phiên 25** (dùng lại báo cáo lưới tạm) |
| `ReviewDistributionService` | `ItemReviewAssignment`, `ItemBatchAssignment` | Phụ thuộc (Use) | **Mới Phiên 25** (2 cạnh) |
| `DeadlineReminderService` | `ItemReviewAssignment`, `ItemPackage`, `MailPort` | Phụ thuộc (Use) | **Mới Phiên 25** (3 cạnh) |
| `ItemCheckService` | `ItemDuplicateChecker`, `ItemCheckResult` | Phụ thuộc (Use) | **Mới Phiên 25** (2 cạnh) |
| `ItemDuplicateChecker` | `DuplicateStrategy` | 1 → 1..\* ("uses") | **Mới Phiên 25** |
| `HashStrategy`, `TrigramStrategy`, `EmbeddingStrategy` | `DuplicateStrategy` | Hiện thực hoá | **Mới Phiên 25** (3 cạnh) |
| `EmbeddingStrategy` | `ItemEmbedding` | Phụ thuộc (Use) | **Mới Phiên 25** |
| `TestSession` | `CATEngine` (và ngược lại) | Phụ thuộc | Phiên gọi CATEngine; CATEngine đọc phiên |
| `TestSession` | `SessionResponse` | 1 - 0..\* (composition ◆) | Field tường minh `responses` |
| `TestSession` | `SessionCacheState` | 1 - 1 ("has") | Trạng thái phiên thi cache trên Redis |
| `TestSession` | `LanguageProfile` | 1 - 1 | Một phiên hoàn tất sinh ra một hồ sơ |
| `TestSession` | `SessionStatus`, `StoppingReason` | Sử dụng (Use) | |
| `SessionCacheState` | `EAPComputationState` | 1 - 1 (composition ◆) | Thay 2 field rời rạc `theta`/`se` |
| `SessionCacheState` | `SessionState` | Sử dụng (Use) | |
| `CATEngine` | `Item`, `SessionResponse`, `SessionCacheState` | Phụ thuộc (đọc, Use) | Không sở hữu, chỉ đọc để tính toán (hai cạnh sau trước đây là cạnh "treo" trong draw.io, Phiên 22 đã nối) |
| `CATEngine` | `AbilityEstimate` | Tạo ra (Use) | **Mới vẽ** (trước chỉ có ở `.puml`) |
| `SessionResponse` | `Item` | Tham chiếu (0..\* - 1) | |
| `Item` | `Explanation` | 1 - 0..1 (composition ◆) | Gắn `Item` (F3); đổi ký hiệu thoi đặc |
| `Item` | `Skill`, `CEFRLevel`, `ItemStatus` | Sử dụng (Use) | Chuẩn hoá giá trị |
| `ItemBatch` | `ItemBatchSource` | Sử dụng (Use) | Nguồn của lô |
| `AIExplainerService` | `Item`, `Explanation` | Phụ thuộc / Tạo ra | |
| `LanguageProfile` | `AbilityEstimate`, `SkillProfile`, `ErrorPattern`, `TestMetadata` | Composition ◆ (1, 1..\*, 0..\*, 1) | |
| `LanguageProfile` | `CEFRConfidence`; `ErrorPattern` → `ErrorSeverity` | Sử dụng (Use) | |
| `ClassReport` | `LanguageProfile` | Phụ thuộc (tổng hợp) | **[đề xuất]**, xem cảnh báo #4 |
| *(đã loại)* `Institution`–`User`, `Institution`–`EduZServiceAccount`, `LanguageProfile`–`Institution`, `ItemBank`–`Item`, `EduZSSOAdapter`–`EduZSSOClient` | | | Không còn trong sơ đồ TL (DC-19, F8, F9, DC-02) |

---

## VIII. CÁC KIỂU LIỆT KÊ (ENUM) DÙNG TRONG HỆ THỐNG

**18 enum** (Phiên 22: từ 10 lên 13, `Skill` bớt `WRITING`; Phiên 25: thêm 5 enum của Nhóm 8, đổi giá trị `ItemStatus`/`ItemSource`).

| Enum | Giá trị | Dùng ở đâu |
|---|---|---|
| `UserRole` | STUDENT, TEACHER, ADMIN, EDUZ_SERVICE | Phân quyền người dùng (`User`) |
| `AuthProviderType` | LOCAL, GOOGLE, MICROSOFT | Cách xác thực của `User` (**mới vẽ Phiên 22**; chỉ `LOCAL` được dùng trong TL — [cần xác nhận] có rút 2 giá trị còn lại) |
| `SessionStatus` | IN_PROGRESS, COMPLETED, ABANDONED | Trạng thái phiên thi (`TestSession`) |
| `SessionState` | WAITING_FOR_ANSWER, READY_FOR_NEXT | Trạng thái chống race-condition trên Redis (`SessionCacheState`) |
| `StoppingReason` | MAX_ITEMS_REACHED, SE_THRESHOLD, ITEM_BANK_BOUNDARY, TIMEOUT | Lý do dừng bài thi (`TestSession`, `TestMetadata`) |
| `CEFRLevel` | PRE_A1, A1, A2, B1, B2, C1_PLUS | Trình độ ngôn ngữ theo khung Châu Âu (`Item`, `LanguageProfile`) |
| `CEFRConfidence` | LOW, MEDIUM, HIGH | Độ tin cậy của kết quả xếp loại (`LanguageProfile`) |
| `Skill` | VOCABULARY, GRAMMAR | Kỹ năng được đánh giá (`Item`, `SkillProfile`, `SessionCacheState.lastSkillPicked`). **Bỏ `WRITING` (F1, #22/A5)** |
| `ItemStatus` | DRAFT, FIRST_APPROVED, SECOND_APPROVED, FINAL_APPROVED, REJECTED, AI_REJECTED | Vòng đời một chiều của câu hỏi (`Item`), DC-39. `FINAL_APPROVED` thay `APPROVED` (CAT chỉ chọn trạng thái này); `REJECTED` = người loại (không lưu lý do, #56); `AI_REJECTED` = máy loại (lưu mã lý do, chỉ Admin xem). **Bỏ `PENDING_REVIEW`, `APPROVED`** |
| `ItemBatchSource` | AI_GENERATED, IMPORTED | Nguồn của lô: AI sinh hay Admin import file (`ItemBatch`). **Đổi tên từ `ItemSource` ngày 16/10/2026** (nguồn không còn nằm trên `Item`); `MANUAL` đã đổi thành `IMPORTED` (DC-32) |
| `ErrorSeverity` | LOW, MEDIUM, HIGH | Mức độ nghiêm trọng của một mẫu lỗi (`ErrorPattern`; không có enum tương ứng trong schema vì lưu JSON) |
| `ExamRoundStatus` | DRAFT, SCHEDULED, OPEN, CLOSED | Trạng thái kỳ thi (`ExamRound`) — **mới** |
| `ImportRowStatus` | VALID, REJECTED, IGNORED_DUPLICATE | Trạng thái một dòng import (`ImportRowResult`) — **mới, đề xuất, chờ chốt** |
| `ItemBatchStatus` | GENERATING, IMPORTING, CHECKING, READY_TO_ASSIGN, IN_REVIEW, READY_TO_FINALIZE, FINAL_CHECKED, DONE, FAILED, PARTIAL | Trạng thái lô (`ItemBatch`) — **mới Phiên 25, đề xuất** |
| `PackageStatus` | OPEN, SENT, DONE | Trạng thái gói A gửi B (`ItemPackage`) — **mới Phiên 25, đề xuất** |
| `CheckPoint` | C1, C2, C3 | Điểm AI check (`ItemCheckResult`) — **mới Phiên 25, đề xuất** |
| `CheckLevel` | PASS, SOFT, HARD | Mức kết quả check: qua / cờ mềm / lỗi cứng (`ItemCheckResult`) — **mới Phiên 25, đề xuất** |
| `ReviewAction` | APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG | Hành động ghi vết (`ItemReviewEvent`) — **mới Phiên 25, đề xuất** |

---

## IX. TÓM TẮT LUỒNG HOẠT ĐỘNG TỔNG THỂ

1. **Tài khoản:** Admin tạo tài khoản SV/GV từng người (`AccountAdminService.createStudent/createTeacher`) hoặc import danh sách qua lưới tạm (`UserImportService`, tham số `kind` — DC-24, đề xuất), bấm Lưu ⇒ tạo tài khoản `LOCAL`, mật khẩu tạm gửi qua `MailPort`; sinh viên đăng nhập bằng **email + mật khẩu**, **bắt buộc đổi mật khẩu** ở lần đầu (`mustChangePassword`). Quên mật khẩu: OTP 6 số qua email (`PasswordResetService`).
2. **Chuẩn bị đề (Phiên 25, DC-27):** Admin tạo `ItemBatch` bằng AI (`ItemGenerationService`) hoặc import file qua lưới tạm (`ItemImportService`) → AI check C1/C2 → Admin Giao việc (`ReviewDistributionService`) → GV A sửa/duyệt/từ chối rồi gửi `ItemPackage` → GV B xác nhận/loại → Admin Kiểm tra (C3) và Import cuối (`FINAL_APPROVED`). Admin **không** sửa/duyệt nội dung câu; chỉ câu `FINAL_APPROVED` mới được dùng.
3. **Chuẩn bị kỳ thi:** Admin tạo `ExamRound` (`DRAFT`), import danh sách thi qua lưới tạm (`RosterImportService`) thành các `ExamRoundParticipant`, rồi công bố (`SCHEDULED`); đến `opensAt` kỳ hiệu lực là `OPEN` (lazy).
4. **Làm bài:** `Student` thuộc một kỳ đang mở chọn kỳ và bắt đầu một `TestSession` (`POST /sessions {examRoundId}`; `expiresAt` tính một lần); mỗi bước, `CATEngine.pickNextSkill()` chọn kỹ năng, `selectNextItem()` chọn `Item` phù hợp, ghi lại thành `SessionResponse`; trạng thái tạm thời giữ ở `SessionCacheState` (Redis).
5. **Giải thích:** `Explanation` **gắn với `Item`** (dùng chung cho mọi sinh viên), **sinh cùng lúc sinh câu hỏi** (DC-31; câu import thiếu giải thích thì sinh bổ sung) — không sinh riêng cho từng `SessionResponse`, không còn lazy.
6. **Tổng kết:** Khi `TestSession` hoàn thành, hệ thống tổng hợp thành `LanguageProfile` — gồm `AbilityEstimate`, `SkillProfile`, `ErrorPattern`, `TestMetadata`, gợi ý học tập AI (nguồn sinh — xem cảnh báo #3).
7. **Sử dụng kết quả:** `LanguageProfile` cho sinh viên xem; `ClassReport` tổng hợp (lọc theo kỳ) cho `Teacher`/`Admin` **chỉ xem**; xuất JSON cho hệ sinh thái **EduZ** (`exportForEduZ()`, API Key M2M).

---

## GHI CHÚ PHIÊN 22 (2026-10-13)

- **Đã làm:** xoá `Institution` và mọi `institutionId`; thêm 12 class + 3 enum mới (`ExamRound`, `ExamRoundParticipant`, `ExamRoundStatus`, `ImportReport`, `ImportRowResult`, `ImportRowStatus`, `UserImportService`, `RosterImportService`, `AccountAdminService`, `MailPort`, `SmtpMailAdapter`, `PasswordResetService`, `AuthProvider`, `JwtAuthProvider`, `AuthProviderType`); sửa `User`, `TestSession`, `ClassReport`, `Admin`, `Teacher`, `Skill`, `LanguageProfile`; xử lý F1–F9 (F5 còn **[cần xác nhận]** như ở cảnh báo #5).
- **Đồng bộ:** `ClassDiagram.puml` và `ClassDiagram.mmd` được **sinh lại từ `Trang-1`** nên khớp tập class/enum/quan hệ. Các lớp **Khóa luận** từng có trong hai file này (`AIQuestionGenerator`, `CalibrationJob`, `EduZWebhookJob`, `WritingSubmission`, `RubricScore`, `TabSwitchEvent`, `ExposureControlPolicy`) **không có trong `Trang-1`**; chúng được chuyển thành chú thích cuối file (không tính vào số đếm) — bản gốc còn trong `Tuan5/_BACKUP_20261013_PHIEN22_ClassDiagram_ORIGINAL.*`.
- **Trang 2 (`Phương`) của `TLCN.drawio.xml` giữ nguyên** (sơ đồ lịch sử, vẫn có `Institution`, `WRITING`...); không thuộc phạm vi đồng bộ.
- **Ảnh `TLCN-Trang-1.drawio.png` chưa xuất lại** (AI không render được draw.io). 👤 Mở `TLCN.drawio.xml` bằng diagrams.net, kiểm tra bố cục (các lớp mới nằm ở vùng trái/trên của canvas, có thể cần kéo lại cho đẹp), rồi xuất PNG đè ảnh cũ.
- **Việc còn mở (không tự quyết):** Q-2 (đóng thủ công kỳ khi còn phiên đang chạy), Q-4 (độ dài mật khẩu tối thiểu), Q-5 (nhà cung cấp SMTP), tên/chữ ký các lớp [đề xuất] ở Nhóm 6–7, cột `Item` (F5), giá trị `AuthProviderType`, bội số `ExamRound–TestSession`.

*Tài liệu gốc được biên soạn dựa trên sơ đồ lớp `TLCN-Trang-1.drawio.png` (đọc từ ảnh ngày 2026-09-18) và đối chiếu `SRS_TLCN_v2.6_Final.docx`; phần Phiên 22 được cập nhật trực tiếp từ `TLCN.drawio.xml` và `schema.prisma`.*

### Ghi chú Phiên 23 (DC-24, đề xuất)
- `AccountAdminService` thêm `createStudent`, `createTeacher`; `UserImportService` thêm tham số `kind: UserRole` (STUDENT|TEACHER) cho mọi phương thức (không thêm enum mới). Số class/enum/quan hệ **không đổi** (30 class + 13 enum, 53 quan hệ). `Teacher.teacherCode` đã có (`teacher_profiles.teacher_code UNIQUE`) nên **không đổi schema** cho phần này.
- `ExamRound.durationMinutes` là `Int NOT NULL DEFAULT 45` (CHECK 5..180); bỏ mọi ghi chú nullable.
- Mô tả EAP: lưới đều 41 điểm, bước 0.2, không gọi là Gaussian–Hermite (K7). Không đổi thuật toán.

---

## GHI CHÚ PHIÊN 25 (2026-10-14) — đồng bộ theo `KE_HOACH_SINH_VA_DUYET_DE_AI.md` bản 5

- **Đã làm trong `TLCN.drawio.xml` (Trang-1), rồi sinh lại `ClassDiagram.puml` / `ClassDiagram.mmd`:** thêm **17 class** (`ItemBatch`, `ItemBatchAssignment`, `ItemPackage`, `ItemReviewAssignment`, `ItemReviewEvent`, `ItemEmbedding`, `ItemCheckResult`, `ItemGenerationService`, `ItemImportService`, `ItemCheckService`, `ItemDuplicateChecker`, `DuplicateStrategy`, `HashStrategy`, `TrigramStrategy`, `EmbeddingStrategy`, `ReviewDistributionService`, `DeadlineReminderService`) và **5 enum** (`ItemBatchStatus`, `PackageStatus`, `CheckPoint`, `CheckLevel`, `ReviewAction`); sửa `Item` (thêm `contentHash`, `batchId`, `packageId`; `approve()`/`reject()` → `transitionTo(next)`), `ItemStatus` (6 giá trị), `ItemSource` (`MANUAL` → `IMPORTED`), `Admin` (gỡ 3 phương thức duyệt/sửa nội dung, thêm 5 phương thức mới), `Teacher` (thêm 4 phương thức A/B); gỡ cạnh `Admin–Item "create/approve"`.
- **Số đếm thật (script đọc lại `Trang-1`, so với hai file text):** 47 class + 18 enum, 89 quan hệ; ba file khớp. Kiểm tham chiếu `source`/`target` của mọi cạnh: 0 lỗi. Kiểm chồng lấn hình học giữa mọi khối cấp 1: 0 chồng lấn. Kiểm `minidom` (well-formed): đạt.
- **Bố cục:** cụm Nhóm 8 nằm **phía trên** (y từ khoảng −1900 đến −760) các nhóm cũ để cạnh từ `Item`/`Admin`/`Teacher` đi lên theo hành lang riêng; `Teacher` dời 20px sang phải và thu hẹp, `AuthProvider`/`JwtAuthProvider` thu hẹp 20px để chừa hành lang. **👤 Cần mở bằng diagrams.net để xem bố cục thực tế rồi xuất lại PNG** (AI không render được draw.io; đường nối dùng toạ độ tính tay nên có thể cần kéo chỉnh).
- **Đồng bộ ngoài tài liệu này:** `backend/backend/prisma/schema.prisma` (+ `custom_migrations.sql`, `seed.ts`) cập nhật cùng phiên; chưa chạy `prisma generate`/`migrate`; mã `src` chưa đổi (danh sách chỗ cần đổi ở phase PI nằm trong báo cáo bàn giao).
- **Còn chờ chốt / đề xuất của AI:** tên các lớp mới và chữ ký (đặc biệt `ItemImportService` do AI tự thêm); `Item.transitionTo` so với các phương thức tường minh; cách chia việc giữa `ItemGenerationService` và `AIExplainerService` cho phần giải thích; ngưỡng T2/T3 (Q-7), bản quyền ngân hàng tham chiếu (Q-8), mô hình embedding (Q-9), `pg_trgm` trên staging (Q-10); `Item.contentHash` và `batch_id`/`package_id` nullable; `CLAUDE.md` còn ghi `APPROVED`, `b ∈ [−2.5, +1.5]`, "lazy" — **chỉ đề xuất diff, không sửa** (phạm vi người điều phối).

### Cập nhật 16/10/2026 (đồng bộ `schema.prisma`)

- `Item.source` bỏ; `ItemSource` đổi tên `ItemBatchSource` (chỉ gắn `ItemBatch`); `Item.batchId` NOT NULL; `ItemBatch.name` (tùy chọn) thêm mới; `ItemBatch.requestedCount` nullable. Quyết định #115 (`0.docs/tracking/DECISIONS_LOG.md`).
- `ItemPackage` tạo lúc Admin giao việc (trạng thái OPEN), A bấm Gửi thì SENT, B xong thì DONE (#116).
- `ClassDiagram.puml`, `.mmd` và **`TLCN.drawio.xml` (trang `Trang-1`, bản đầy đủ 47 class)** đã sửa theo (Item bỏ `source`, `batchId` bắt buộc; `ItemBatch` có `source: ItemBatchSource`, `name?`, `requestedCount?`; enum đổi tên). **Từ 16/10/2026 `TLCN.drawio.xml` (Trang-1) là bản gọn khoảng 41 lớp** (nền là bản 28 lớp của Đăng, bổ sung nhóm lô/gói/duyệt và service; không vẽ `ItemEmbedding`, `ExamRoundParticipant`, các lớp import riêng lẻ), ảnh `TLCN-Trang-1.drawio.png` đã xuất lại từ bản này; `ClassDiagram.puml`/`.mmd` vẫn là bản chi tiết 47 lớp. Trang `Phương` trong file là bản cũ (còn `ItemSource`, `Institution`); bản đầy đủ 47 lớp của draw.io được backup ở `Update/_BACKUP_20261016/TLCN.drawio.xml`. Bản thu nhỏ trước đó của `Update/` được backup ở `Update/_BACKUP_20261016/Update__TLCN.drawio.xml`. Số class/enum không đổi sau thay đổi này (47 class, 18 enum theo bản puml/mmd) nhưng chưa đếm lại từ draw.io.
