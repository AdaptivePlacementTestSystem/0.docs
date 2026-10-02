# MÔ TẢ SƠ ĐỒ LỚP (CLASS DIAGRAM) — HỆ THỐNG PLACEMENT TEST THÍCH ỨNG

**Tài liệu này mô tả:** File thiết kế `TLCN-Trang-1.drawio.png` (bản cập nhật sau buổi họp GVHD ngày 2026-09-18)
**Thay thế:** `TLCN-Phương.drawio.png` (sơ đồ gốc — vẫn giữ trong repo làm lịch sử, không xoá)
**Tài liệu tham chiếu gốc:** `SRS_TLCN (3).md`, `SRS_TLCN_v2.6_Final.docx`
**Mục đích tài liệu:** Diễn giải cho khách hàng (KH) hiểu: mỗi khối (lớp/đối tượng) trong sơ đồ đại diện cho cái gì, dùng để làm gì, và các khối liên kết/phụ thuộc vào nhau ra sao trong vận hành thực tế của hệ thống.

> ⚠️ **Các điểm cần xác nhận lại với người vẽ sơ đồ (Phương) trước khi coi tài liệu này là chốt cuối cùng** — xem chi tiết từng điểm tại đúng mục liên quan bên dưới:
> 1. **Nhóm Auth (`AuthProvider`, `JwtAuthProvider`, `EduZSSOAdapter`, `EduZSSOClient`) không xuất hiện trong `TLCN-Trang-1.drawio.png`.** Tên file gợi ý đây có thể chỉ là **Trang 1** của một sơ đồ nhiều trang (Auth nằm ở trang khác), nhưng cũng có thể đã bị lược khỏi phạm vi hiển thị. Tài liệu này **tạm giữ nguyên** mô tả Auth cũ (Mục II.3) cho đến khi xác nhận — không tự suy luận thêm.
> 2. **`Explanation` giờ gắn với `Item` (1 Item — 0..1 Explanation, composition) thay vì gắn với `SessionResponse` như bản cũ.** Nghĩa là lời giải thích AI được sinh và lưu **1 lần cho mỗi câu hỏi**, dùng chung cho mọi sinh viên trả lời câu đó — khác hẳn ý nghĩa "giải thích riêng cho từng lượt trả lời" trước đây. Đây là thay đổi nghiệp vụ đáng kể, cần xác nhận có đúng chủ đích không.
> 3. **`AIExplainerService` không còn liệt kê `generateRecommendations(patterns: ErrorPattern[])`.** `LanguageProfile` vẫn có field `aiRecommendations: String[]` — nhưng sơ đồ mới không cho thấy method nào sinh ra dữ liệu này. Cần xác nhận: gợi ý học tập được sinh ở đâu (trong `generateFromSession()` của `LanguageProfile`, hay method này chỉ bị ẩn bớt lúc vẽ cho gọn hình)?
> 4. **`ClassReport` không có đường nối tới `LanguageProfile`** trong sơ đồ mới (đứng độc lập, không có mũi tên nào). Tài liệu này **tạm giữ** quan hệ logic cũ (tổng hợp dữ liệu từ nhiều `LanguageProfile`) vì đó là điều duy nhất hợp lý để `generateClassDistribution()` hoạt động — nhưng cần xác nhận đây chỉ là giản lược hình vẽ.
> 5. **`Item` không còn vẽ các field audit** `approvedBy`, `approvedAt`, `createdAt`, `updatedAt` (ngoài các field hiệu chỉnh độ khó `calibrated`, `timesUsed`, `exposureRate`, `pValue`, `itemFitMnsq` đã được chốt bỏ theo đúng cuộc họp). Nếu chỉ là giản lược hình vẽ thì các field audit này **vẫn còn** ở tầng DB schema (SRS Mục 6.2) — không cần sửa gì; nếu là chủ đích bỏ hẳn thì cần cập nhật lại SRS Mục 6.2 tương ứng.

---

## I. TỔNG QUAN CÁCH ĐỌC SƠ ĐỒ

Sơ đồ là **UML Class Diagram** — bản thiết kế chi tiết các "đối tượng dữ liệu" (class) mà phần mềm sẽ quản lý, cùng các thuộc tính (dữ liệu lưu trữ) và hành vi (hàm/chức năng) của từng đối tượng. `TLCN-Trang-1.drawio.png` gồm 5 nhóm khối chức năng chính, được tổ chức theo luồng nghiệp vụ:

| Nhóm | Vai trò trong hệ thống | Các lớp chính |
|---|---|---|
| **1. Người dùng & Vai trò** | Ai được đăng nhập, vai trò gì, thuộc trường nào | `User`, `Admin`, `Student`, `Teacher`, `Institution`, `UserRole` (+ Auth — xem cảnh báo ở trên) |
| **2. Phiên thi & Thuật toán thích ứng** | Sinh viên làm bài, hệ thống chọn câu hỏi thông minh theo năng lực | `TestSession`, `CATEngine`, `SessionResponse`, `SessionCacheState`, `EAPComputationState` |
| **3. Ngân hàng câu hỏi** | Kho câu hỏi thi, ai duyệt, câu nào được dùng | `Item` (không còn `ItemBank` — đã bỏ khỏi phạm vi Tiểu luận) |
| **4. AI Giải thích & Gợi ý** | Sau khi thi xong, AI giải thích vì sao đúng/sai và gợi ý học gì | `AIExplainerService`, `Explanation` |
| **5. Hồ sơ năng lực & Báo cáo** | Kết quả cuối cùng xuất ra cho sinh viên, giảng viên, và hệ thống EduZ | `LanguageProfile`, `SkillProfile`, `ErrorPattern`, `TestMetadata`, `ClassReport` |

Ký hiệu trong sơ đồ dùng nhiều **khuôn mẫu thiết kế (stereotype)** đặt trong dấu `<<...>>` để nói rõ vai trò kỹ thuật của từng khối:

- `<<interface>>` — một "hợp đồng" quy định phải có chức năng gì, không tự chứa dữ liệu thật (ví dụ `AuthProvider`).
- `<<abstract>>` — một khối "khuôn mẫu chung" không tồn tại độc lập, chỉ dùng để các khối con kế thừa (ví dụ `User`).
- `<<service>>` — một khối xử lý nghiệp vụ/thuật toán, không lưu trữ dữ liệu lâu dài (ví dụ `CATEngine`, `AIExplainerService`, `ClassReport`).
- `<<value object>>` — một khối dữ liệu nhỏ, "gắn liền" với một đối tượng cha, không có vòng đời riêng (ví dụ `SkillProfile`, `AbilityEstimate`, `EAPComputationState`).
- `<<aggregate root>>` — khối dữ liệu trung tâm, là điểm truy cập chính cho một nhóm dữ liệu liên quan (ví dụ `LanguageProfile`).
- `<<Enumeration>>` — danh sách các giá trị cố định được phép chọn (ví dụ `CEFRLevel` chỉ có 6 giá trị: Pre-A1, A1, A2, B1, B2, C1+).
- `<<Adapter>>`, `<<external>>`, `<<M2M>>`, `<<Redis>>` — đánh dấu khối kết nối với hệ thống bên ngoài (SSO của EduZ, cache Redis, tài khoản máy-với-máy).

---

## II. NHÓM 1 — NGƯỜI DÙNG & VAI TRÒ

### 1. `Institution` (Trường/Đơn vị đào tạo)
Đại diện cho **một trường** sử dụng hệ thống (ví dụ Trường Đại học Tôn Đức Thắng). Lưu `id`, `name` (tên trường), `slug` (mã định danh ngắn).

- **Vì sao cần:** Hệ thống thiết kế theo hướng **đa đơn vị (multi-tenant)** — có thể phục vụ nhiều trường cùng lúc mà không lẫn dữ liệu.
- **Liên kết với `User` — đã chốt lại (2026-09-30, `tracking/DECISIONS_LOG.md` #15):** `Institution` **1** — **1..\*** `User` (association, mỗi `User` thuộc đúng **một** `Institution`). *(Bản 2026-09-18 từng vẽ `1..*`—`1..*` (nhiều-nhiều) và bỏ `institutionId` khỏi `User`; đã sửa lại trong `TLCN.drawio.xml` trang `Trang-1` vì RBAC SRS 15.4 cần so sánh `institution_id`, và `LanguageProfile.institutionId`/`ClassReport.institutionId` đã tồn tại trên chính sơ đồ.)* Ở tầng dữ liệu, đầu "1" được hiện thực bằng khoá ngoại `users.institution_id` (xem `Tuan3/KE_HOACH_PRISMA_SCHEMA_VA_6_HANG_MUC.md`); sơ đồ lớp không cần vẽ thêm field `institutionId` trên `User` vì đã biểu diễn bằng association.
  - Việc EduZ gọi API lấy dữ liệu của trường được xác thực bằng **API Key cấu hình (M2M)**, không phải một entity `EduZServiceAccount` lưu trong DB (xem mục 2 bên dưới — không đổi so với bản cũ).

### 2. Truy cập M2M của hệ sinh thái EduZ — **KHÔNG phải một class/entity riêng** (không đổi so với bản cũ)
> ⚠️ **Điều chỉnh so với sơ đồ gốc `TLCN-Phương.drawio.png`:** Sơ đồ gốc có vẽ một class riêng `EduZServiceAccount` (`<<M2M>>`). Sau khi đối chiếu với `SRS_TLCN (3).md` dòng 691 — bảng chốt phạm vi Must-have Tiểu luận vs Spec Khóa luận — mục "RBAC chi tiết (M2M, EduZ Service Account)" được SRS xếp rõ vào cột **Spec/Khóa luận**, không phải Must-have của Tiểu luận. Người dùng đã xác nhận (2026-09-14): **bỏ entity này khỏi phạm vi Tiểu luận**, chỉ giữ một role M2M đơn giản.
>
> **Cách hiểu lại cho Tiểu luận:** `EduZ System` là một **actor bên ngoài** (không phải `User`, không có bảng riêng trong DB). Khi EduZ gọi API (`GET /api/v1/placement-profiles/:student_id`), request đi kèm một **API Key tĩnh cấu hình qua `.env`/config**, được middleware/guard kiểm tra và gán role tương đương `EDUZ_SERVICE` (enum `UserRole`) cho request đó — tương tự cách `ADMIN`/`M2M` "pass through" trong `ProfileAccessGuard` (xem SRS Mục 15.4). Guard chỉ cho phép `GET`, không cho `POST`/`DELETE`.
>
> **Việc cần làm ở Khóa luận (không phải bây giờ):** nếu sau này cần nhiều đối tác M2M khác nhau, nhiều `apiKey` khác nhau theo từng `Institution`, hoặc thu hồi/luân chuyển key — lúc đó mới cần nâng cấp thành một entity `EduZServiceAccount` thật sự lưu trong DB.

### 3. `AuthProvider` — `<<interface>>` và các cách triển khai
> ⚠️ **Chưa xuất hiện trong `TLCN-Trang-1.drawio.png` — xem cảnh báo #1 ở đầu tài liệu.** Nội dung dưới đây giữ nguyên theo sơ đồ gốc `TLCN-Phương.drawio.png`, cần xác nhận lại còn hiệu lực hay không.

Đây là "hợp đồng xác thực": bất kỳ cách đăng nhập nào cũng phải có hàm `authenticate(credentials): User`. Có **2 cách triển khai cụ thể**, thể hiện 2 kịch bản đăng nhập:

- **`JwtAuthProvider`** — đăng nhập trực tiếp bằng email/mật khẩu do hệ thống tự quản lý, cấp JWT token (`issueToken`) và làm mới token (`refresh`).
- **`EduZSSOAdapter`** (`<<Adapter>>`) — cho phép sinh viên/giảng viên **đăng nhập bằng tài khoản EduZ có sẵn** (Single Sign-On), không cần tạo tài khoản riêng. Khối này "bọc" (adapt) `EduZSSOClient` (`<<external>>`, đại diện cho hệ thống SSO bên ngoài của EduZ) để nó tuân theo cùng hợp đồng `AuthProvider` như đăng nhập thường.
- **Ý nghĩa nghiệp vụ:** Nhờ mẫu thiết kế Adapter này, module Placement Test có thể **cắm vào (plug-and-play)** bất kỳ trường nào — dù trường đó dùng tài khoản riêng hay tài khoản EduZ — mà không phải sửa lại logic xác thực cốt lõi.

### 4. `User` — `<<abstract>>` (Người dùng — khuôn mẫu chung)
Không tồn tại độc lập, chứa các thông tin **chung cho mọi loại người dùng**: `id`, `email`, `passwordHash`, `fullName`, `role`, `createdAt`. **Không vẽ field `institutionId` trên `User`** — quan hệ "thuộc trường nào" được biểu diễn bằng association `Institution 1—1..* User` (xem mục 1 — chốt lại 2026-09-30). Vai trò `role` được xác định theo enum `UserRole` gồm: `STUDENT`, `TEACHER`, `ADMIN`, `EDUZ_SERVICE`.

Ba lớp con kế thừa từ `User` (hollow-triangle inheritance), mỗi lớp là **một vai trò cụ thể** trong hệ thống:

| Vai trò | Field/Method riêng trong sơ đồ | Việc chính trong hệ thống |
|---|---|---|
| **`Student`** (Sinh viên) | `studentCode`; `getLatestProfile(): LanguageProfile`; `getTestHistory(): TestSession[]` | Làm bài thi thích ứng (`TestSession`), nhận kết quả (`LanguageProfile`) |
| **`Teacher`** (Giảng viên) | `teacherCode`; `approveItem(itemId): void`; `rejectItem(itemId): void`; `updateContentItem(itemId, content): void` | Trực tiếp duyệt/loại/sửa `Item` (không còn qua `ItemBank` — xem Mục IV) |
| **`Admin`** (Quản trị) | *(không có field/method riêng trong sơ đồ, chỉ kế thừa `User`)* | Quản lý toàn hệ thống, không giới hạn theo trường |

#### Phân biệt quyền chi tiết giữa các vai trò (đối chiếu SRS Mục 15.3–15.4, F-02, F-09)

> **Lưu ý:** phần dưới đây gồm cả nội dung **SRS đã quy định rõ** và **1 quyết định do người dùng chốt** (đánh dấu rõ ràng) vì SRS không đặc tả chi tiết phạm vi `Admin` ngoài 1 endpoint duy nhất. Nội dung không đổi so với bản trước — chỉ thay các chỗ nhắc tới `ItemBank` bằng `Item` cho khớp sơ đồ mới.

**a. `Student` — chỉ thao tác trên dữ liệu của chính mình**
- Tạo và làm `TestSession` của riêng mình (không làm hộ/xem hộ SV khác).
- Xem `LanguageProfile` **của chính mình** — API `GET /placement-profiles/:student_id` bắt buộc `student_id` khớp `sub` trong JWT (SRS 15.4). Xem hồ sơ của SV khác → bị chặn ở tầng Guard, không phải chỉ ẩn ở UI.
- **Không có quyền gì** trên `Item` (không tạo/sửa/duyệt câu hỏi) và không xem được câu hỏi + đáp án đúng trước khi nộp bài (SRS 15.3).

**b. `Teacher` — quyền chuyên môn, giới hạn theo `institution_id` của mình**
- **`Item`** (F-02): quyền đầy đủ và duy nhất — tự tạo câu hỏi từ đầu, sửa tự do nội dung/đáp án do AI sinh ra (`updateContentItem`), `approveItem()`/`rejectItem()`. AI chỉ là "trợ lý nháp", không có quyền tự duyệt.
- **`LanguageProfile`**: xem được của **bất kỳ `Student` nào cùng `institution_id`** với mình (SRS 15.4) — không xem được SV trường khác.
- **`ClassReport`** (F-09): xem báo cáo tổng hợp cả lớp/khoá, cũng giới hạn theo `institution_id` của mình.
- Không có quyền quản lý `User`/`Institution` (tạo/xoá tài khoản, đổi vai trò người khác).

**c. `Admin` — Quyết định đã chốt (2026-09-14): Admin = "siêu tập" của `Teacher` + quản trị hệ thống**
> SRS chỉ xác nhận "Admin toàn quyền" ở đúng 1 chỗ (API `placement-profiles`, Mục 15.4); các module khác (`Item`, `ClassReport`) SRS chỉ nói đến `Teacher`, không nhắc `Admin`. Người dùng đã chốt cách hiểu theo nghĩa đen của "toàn quyền": **`Admin` làm được mọi việc `Teacher` làm được, trên MỌI `Institution`, cộng thêm phần quản trị hệ thống mà `Teacher` không đụng tới.**
>
> Cụ thể:
> - Mọi quyền của `Teacher` (CRUD/duyệt `Item`, xem `ClassReport`) — nhưng **không bị giới hạn theo `institution_id`**.
> - Xem `LanguageProfile` của **bất kỳ `Student` nào**, không giới hạn trường (đã có sẵn trong SRS 15.4).
> - Quản lý `User`/`Institution` (tạo/sửa/xoá tài khoản, gán vai trò) — phần này `Teacher`/`Student` không có.
>
> **Ý nghĩa khi code Guard:** `Admin` luôn pass qua nhánh kiểm tra `institutionId` — tương tự cách `ProfileAccessGuard` hiện tại đã cho `ADMIN`/`M2M` "pass through" (SRS 15.4).

**d. `EduZ System (M2M)` — không phải `User`, xem lại mục 2 ở trên**
Chỉ có quyền `GET` hồ sơ năng lực qua API Key cấu hình, không `POST`/`DELETE`, không liên quan gì đến `Item`/`ClassReport`.

---

## III. NHÓM 2 — PHIÊN THI & THUẬT TOÁN THÍCH ỨNG (TRÁI TIM HỆ THỐNG)

### 5. `TestSession` (Phiên làm bài thi)
Đại diện cho **một lượt sinh viên làm bài thi**, từ lúc bắt đầu đến lúc nộp bài. Lưu `studentId`, **`responses: List<SessionResponse>`** (field tường minh — thay đổi 2026-09-18, trước đây chỉ suy ra ngầm từ quan hệ 1-nhiều), `status` (enum `SessionStatus`), `thetaFinal`, `seFinal`, `startedAt`/`completedAt`, và `stoppingReason` (enum `StoppingReason`).

- **Hành vi chính:** `start()`, `submitResponse(itemId, answer)`, `getNextItem(): Item`, `computeResult(): LanguageProfile`, `reconstructFromResponses()`.
- **Liên kết:**
  - `Student` **1** — "has" — **0..\*** `TestSession` (một sinh viên có thể có nhiều lượt thi).
  - `TestSession` **1** ◆ (composition) — **0..\*** `SessionResponse` — khớp đúng với field `responses` tường minh ở trên: xoá `TestSession` thì toàn bộ `SessionResponse` của nó cũng mất theo.
  - `TestSession` **1** — "has" — **1** `LanguageProfile` — một phiên thi hoàn tất sinh ra một hồ sơ năng lực.
  - `TestSession` **1** — `SessionCacheState` — đồng bộ trạng thái tạm thời qua Redis để tăng tốc độ phản hồi trong lúc thi.
  - `TestSession` **phụ thuộc (dependency)** vào `CATEngine` để quyết định câu hỏi tiếp theo và tính năng lực.

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
- `quadraturePoints = 41`: số điểm rời rạc dùng để tính tích phân EAP bằng **Gaussian–Hermite quadrature**, phân bố đều trên `[-4, +4]`, bước `0.2`.

**c. `pickNextSkill(session)` — quyết định thiết kế đã chốt, giờ chính thức lên sơ đồ**
Round-robin **không** dựa theo tỷ lệ Item Bank (160 Vocab : 120 Grammar) mà dựa trên số câu đã hỏi trong session; câu 1 random 50/50, từ câu 2 alternate cố định theo skill đã ra ở câu 1. Cần lưu `lastSkillPicked` trong `SessionCacheState` (đã có trong sơ đồ) và **khôi phục đúng giá trị này** trong `reconstructFromDB()` khi Redis mất dữ liệu — nếu không sẽ random lại giữa bài thi, phá vỡ pattern alternate.

**d. `selectNextItem(session, pool)` — không phải "chọn câu gần θ nhất"**
SRS Mục 4.4: nếu chọn **tất định** câu có độ khó `b_i` gần θ̂ nhất, mọi sinh viên khởi tạo cùng `θ₀ = -0.5` sẽ luôn nhận **đúng cùng một câu đầu tiên**. Thuật toán thật (**Randomized Top-5 b-matching**): lọc câu chưa dùng + `APPROVED` + đúng `skill`, sắp theo `|b_i − θ̂|` tăng dần, lấy Top-5, chọn ngẫu nhiên đều 1 câu (mỗi câu 20%).

> **Điều kiện bắt buộc:** filter `status = 'APPROVED'` phải nằm ở tầng **Repository** (`Item.findForCAT`), không phải business logic của `CATEngine`.

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

> ⚠️ **`ItemBank` đã bị bỏ hẳn khỏi sơ đồ** (quyết định 2026-09-18, đã ghi trong `tracking/weekly-log/Tuan-01.md`). Hệ quả trực tiếp: `Teacher` giờ **quản lý `Item` trực tiếp** (association `create/approve`), và hàm tìm câu cho CAT (`findForCAT`) chuyển thành **method trên chính `Item`** thay vì trên một aggregate root riêng.

### 11. `Item` (Câu hỏi)
Đại diện cho **một câu hỏi trắc nghiệm** cụ thể: `content: String`, `options: Map<char, String>`, `correctAnswer: char`, `skill: Skill`, `topicTag: String`, `cefrTarget: CEFRLevel`, `irtB: float`, `irtA: float`, `irtC: float` *(reserved — dự phòng 2PL/3PL Khóa luận)*, `status: ItemStatus`, `source: ItemSource`.

- **Field đã bỏ (2026-09-18, theo đúng chốt tại buổi họp GVHD):** `calibrated`, `timesUsed`, `exposureRate`, `pValue`, `itemFitMnsq` — các field phục vụ hiệu chỉnh độ khó bằng dữ liệu thực, không thuộc phạm vi Must-have Tiểu luận ở giai đoạn hiện tại (khớp quyết định bỏ Pre-test tự tổ chức, xem `SRS_TLCN_v2.6_Final.docx` Mục 6.1/6.4).
- **Field không thấy trong sơ đồ (cần xác nhận — cảnh báo #5):** `approvedBy`, `approvedAt`, `createdAt`, `updatedAt`. Có thể chỉ là giản lược hình vẽ; SRS Mục 6.2 (PostgreSQL schema) hiện vẫn giữ các field này.
- **Hành vi:** `approve(): void`, `reject(): void`, `probability(theta: float): float` (công thức lõi Rasch), và **`findForCAT(skill, usedIds, theta): Item[]`** — method mới chuyển từ `ItemBank` sang, đại diện cho truy vấn Repository lấy các câu ứng viên cho `CATEngine.selectNextItem()`.
- **Điểm quan trọng về nghiệp vụ:** Chỉ `Item` có `status = APPROVED` mới được `CATEngine` chọn vào bài thi thật.
- **Liên kết:**
  - `Teacher` **1** — "create/approve" — **0..\*** `Item` (association trực tiếp, không qua `ItemBank`).
  - `Item` **sử dụng (Use, dependency)** 4 enum: `Skill`, `CEFRLevel`, `ItemStatus`, `ItemSource`.
  - `Item` **1** ◆ (composition) — **0..1** `Explanation` — xem Mục V.13 (thay đổi so với bản cũ).

---

## V. NHÓM 4 — AI GIẢI THÍCH & GỢI Ý HỌC TẬP

### 12. `AIExplainerService` (Dịch vụ AI giải thích) — `<<service>>`
Là lớp gọi đến **Gemini API** để tự động sinh lời giải thích, cấu hình bằng `modelName: String`, `systemPrompt: String`.

- **Hành vi chính (khớp đúng sơ đồ mới):**
  - `explain(item: Item): Explanation` — sinh lời giải thích cho **một câu hỏi** (không còn nhận `response` làm tham số như bản cũ — xem cảnh báo #2).
  - `buildPrompt(item: Item, context: String): String`, `callGeminiAPI(prompt: String): String` — các bước kỹ thuật xây dựng câu lệnh và gọi mô hình AI.
- **Method không còn thấy trong sơ đồ (cần xác nhận — cảnh báo #3):** `generateRecommendations(patterns: ErrorPattern[])` của bản cũ không xuất hiện nữa, trong khi `LanguageProfile.aiRecommendations: String[]` vẫn còn. Cần xác nhận nơi sinh ra gợi ý học tập.
- **Liên kết:** `AIExplainerService` **đọc (Use)** `Item`, và **tạo ra** `Explanation`.

### 13. `Explanation` (Lời giải thích) — **thay đổi quan hệ sở hữu (2026-09-18)**
Kết quả cụ thể do AI sinh ra: `id: UUID`, **`itemId: UUID`**, `content: String`, `generatedAt: DateTime`.

- **Thay đổi so với bản cũ:** trước đây `Explanation` gắn (composition) với **một `SessionResponse`** — nghĩa là mỗi lượt trả lời có giải thích riêng. Sơ đồ mới vẽ `Explanation` gắn (composition, `Item` **1** ◆ — **0..1** `Explanation`) với **`Item`** — nghĩa là **một câu hỏi có tối đa 1 giải thích, dùng chung cho mọi sinh viên** từng trả lời câu đó.
- **Vì sao thay đổi này hợp lý (suy luận, cần xác nhận là đúng chủ đích — cảnh báo #2):** với cùng một câu hỏi, lời giải thích "vì sao đáp án A đúng/vì sao B sai" về bản chất **không đổi theo từng sinh viên** — gắn `Explanation` vào `Item` cho phép sinh 1 lần, tái sử dụng cho mọi lượt trả lời sau, giảm số lần gọi Gemini API (tiết kiệm chi phí + độ trễ) so với sinh lại mỗi `SessionResponse`.

---

## VI. NHÓM 5 — HỒ SƠ NĂNG LỰC & BÁO CÁO

### 14. `LanguageProfile` (Hồ sơ năng lực ngôn ngữ) — `<<aggregate root>>`
**Sản phẩm đầu ra quan trọng nhất** của toàn hệ thống. Lưu: `id`, `schemaVersion: String`, `studentId`, `institutionId`, `testSessionId`, **`abilityEstimate: AbilityEstimate`** (field tường minh — mới 2026-09-18, xem Mục III.8), `completedAt`, `cefrLevel: CEFRLevel`, `cefrConfidence: CEFRConfidence`, `boundaryEffect: boolean`, `errorPatterns: List<ErrorPattern>`, `skillProfiles: List<SkillProfile>`, `aiRecommendations: String[]`, `testMetadata: TestMetadata`.

- **Hành vi chính:** `generateFromSession(s: TestSession): void`, `toJSON(): String`, `exportForEduZ(): String`.
- **Chứa (composition) 4 loại "khối dữ liệu con":**
  - **`AbilityEstimate`** (**1**, mới tường minh) — năng lực cuối cùng (θ, SE, khoảng tin cậy).
  - **`SkillProfile`** (**1..\***) — điểm số theo từng kỹ năng riêng.
  - **`ErrorPattern`** (**0..\***) — các mẫu lỗi sai lặp lại theo chủ điểm.
  - **`TestMetadata`** (**1**) — thông tin kỹ thuật về cách bài thi đã diễn ra.
- **Liên kết:** Một `TestSession` (đã hoàn thành) sinh ra **đúng một** `LanguageProfile` (xem Mục III.5).

### 15. `ClassReport` (Báo cáo lớp học) — `<<service>>`
Dịch vụ dành cho `Teacher` xem tổng quan năng lực của cả một lớp/khoá, giới hạn theo `institutionId: UUID`.

- **Hành vi chính:** `generateClassDistribution(): Map<CEFRLevel, int>`, `exportCSV(): File`.
- **Liên kết (cần xác nhận — cảnh báo #4):** sơ đồ mới không vẽ đường nối nào từ `ClassReport` tới lớp khác. Tài liệu này **tạm giữ** quan hệ logic cũ: `ClassReport` **tổng hợp (phụ thuộc, đọc)** dữ liệu từ nhiều `LanguageProfile` — vì đây là cách duy nhất hợp lý để `generateClassDistribution()` có dữ liệu — nhưng cần Phương xác nhận lại.

---

## VII. BẢNG TỔNG HỢP QUAN HỆ GIỮA CÁC LỚP

| Từ lớp | Đến lớp | Kiểu quan hệ | Ghi chú |
|---|---|---|---|
| `Admin`, `Student`, `Teacher` | `User` | Kế thừa | Ba vai trò cụ thể hoá từ khuôn mẫu người dùng chung |
| `User` | `UserRole` | Sử dụng (Use) | Enum vai trò |
| `Institution` | `User` | **Association 1 — 1..\*** (chốt lại 2026-09-30, Quyết định #15) | Mỗi `User` thuộc đúng 1 `Institution`; hiện thực bằng FK `users.institution_id`; xem Mục II.1 |
| ⚠️ `JwtAuthProvider`, `EduZSSOAdapter` | `AuthProvider` | Hiện thực hoá (implements) | **Chưa xác nhận còn trong phạm vi Trang-1 hay không** — xem cảnh báo #1 |
| ⚠️ `EduZSSOAdapter` | `EduZSSOClient` | Sử dụng | Như trên |
| *(chỉ Khóa luận)* `Institution` | `EduZServiceAccount` | 1 - 1/0..1 | Ở Tiểu luận: EduZ xác thực bằng API Key cấu hình (M2M), không có entity riêng — xem Mục II.2 |
| `Student` | `TestSession` | 1 - 0..\* ("has") | Một sinh viên có thể có nhiều lượt thi |
| `Teacher` | `Item` | 1 - 0..\* ("create/approve") | **Thay `Teacher`→`ItemBank` cũ** — giảng viên quản lý câu hỏi trực tiếp |
| `TestSession` | `CATEngine` | Phụ thuộc | Phiên thi gọi bộ máy CAT để chọn câu & tính năng lực |
| `TestSession` | `SessionResponse` | 1 - 0..\* (composition ◆) | Field tường minh `responses: List<SessionResponse>` |
| `TestSession` | `SessionCacheState` | Đồng bộ | Trạng thái phiên thi được cache trên Redis |
| `TestSession` | `LanguageProfile` | 1 - 1 ("has", khi hoàn thành) | Một phiên thi hoàn tất sinh ra một hồ sơ năng lực |
| `SessionCacheState` | `EAPComputationState` | 1 - 1 (composition ◆) | **Mới 2026-09-18** — thay 2 field rời rạc `theta`/`se` |
| `CATEngine` | `SessionCacheState`, `Item`, `SessionResponse` | Phụ thuộc (đọc, Use) | Không sở hữu, chỉ đọc để tính toán |
| `CATEngine` | `AbilityEstimate` | Tạo ra | Kết quả tính năng lực sau mỗi câu (`computeEAP`) |
| `SessionResponse` | `Item` | Tham chiếu (0..\* - 1) | Mỗi câu trả lời gắn với đúng một câu hỏi đã hỏi |
| `Item` | `Explanation` | 1 - 0..1 (composition ◆) | **Đổi từ `SessionResponse`→`Explanation` (bản cũ)** — xem cảnh báo #2 |
| `Item` | `Skill`, `CEFRLevel`, `ItemStatus`, `ItemSource` | Sử dụng (Use) | Chuẩn hoá giá trị |
| `AIExplainerService` | `Item` | Phụ thuộc (đọc, Use) | Lấy ngữ cảnh để sinh giải thích |
| `AIExplainerService` | `Explanation` | Tạo ra | Sinh lời giải thích bằng AI |
| `LanguageProfile` | `AbilityEstimate` | 1 (composition ◆) | **Field tường minh mới** `abilityEstimate` |
| `LanguageProfile` | `SkillProfile` | 1..\* (composition ◆) | Điểm theo từng kỹ năng |
| `LanguageProfile` | `ErrorPattern` | 0..\* (composition ◆) | Mẫu lỗi sai lặp lại |
| `LanguageProfile` | `TestMetadata` | 1 (composition ◆) | Thông tin kỹ thuật bài thi |
| ⚠️ `ClassReport` | `LanguageProfile` | Phụ thuộc (tổng hợp) | **Không thấy vẽ trong sơ đồ mới** — xem cảnh báo #4 |

---

## VIII. CÁC KIỂU LIỆT KÊ (ENUM) DÙNG TRONG HỆ THỐNG

*(Không đổi so với bản trước — cả 10 enum đều khớp với sơ đồ mới.)*

| Enum | Giá trị | Dùng ở đâu |
|---|---|---|
| `UserRole` | STUDENT, TEACHER, ADMIN, EDUZ_SERVICE | Phân quyền người dùng (`User`) |
| `SessionStatus` | IN_PROGRESS, COMPLETED, ABANDONED | Trạng thái phiên thi (`TestSession`) |
| `SessionState` | WAITING_FOR_ANSWER, READY_FOR_NEXT | Trạng thái chống race-condition trên Redis (`SessionCacheState`) |
| `StoppingReason` | MAX_ITEMS_REACHED, SE_THRESHOLD, ITEM_BANK_BOUNDARY, TIMEOUT | Lý do dừng bài thi (`TestSession`, `TestMetadata`) |
| `CEFRLevel` | PRE_A1, A1, A2, B1, B2, C1_PLUS | Trình độ ngôn ngữ theo khung Châu Âu (`Item`, `LanguageProfile`) |
| `CEFRConfidence` | LOW, MEDIUM, HIGH | Độ tin cậy của kết quả xếp loại (`LanguageProfile`) |
| `Skill` | VOCABULARY, GRAMMAR, WRITING | Kỹ năng ngôn ngữ được đánh giá (`Item`, `SkillProfile`, `SessionCacheState.lastSkillPicked`) |
| `ItemStatus` | DRAFT, PENDING_REVIEW, APPROVED, REJECTED | Quy trình kiểm duyệt câu hỏi (`Item`) |
| `ItemSource` | MANUAL, AI_GENERATED | Nguồn gốc câu hỏi: giảng viên soạn hay AI sinh (`Item`) |
| `ErrorSeverity` | LOW, MEDIUM, HIGH | Mức độ nghiêm trọng của một mẫu lỗi sai lặp lại (`ErrorPattern`) |

---

## IX. TÓM TẮT LUỒNG HOẠT ĐỘNG TỔNG THỂ

1. **Đăng nhập:** `Student`/`Teacher` đăng nhập, được xác định thuộc `Institution` nào. *(Cơ chế cụ thể qua `AuthProvider`/SSO — xem cảnh báo #1.)*
2. **Chuẩn bị đề:** `Teacher` soạn hoặc duyệt `Item` **trực tiếp** (`approveItem`/`rejectItem`/`updateContentItem`) — không còn qua `ItemBank` trung gian; chỉ câu `APPROVED` mới được dùng.
3. **Làm bài:** `Student` bắt đầu một `TestSession`; mỗi bước, `CATEngine.pickNextSkill()` chọn kỹ năng, `selectNextItem()` chọn `Item` phù hợp (qua `Item.findForCAT()`), ghi lại thành `SessionResponse`; trạng thái tạm thời (gồm `EAPComputationState`) giữ ở `SessionCacheState` (Redis).
4. **Giải thích:** `AIExplainerService` sinh `Explanation` **gắn với `Item`** (dùng lại cho mọi sinh viên trả lời cùng câu đó) — không còn sinh riêng cho từng `SessionResponse` như bản cũ.
5. **Tổng kết:** Khi `TestSession` hoàn thành, hệ thống tổng hợp thành `LanguageProfile` — gồm `AbilityEstimate`, điểm theo kỹ năng (`SkillProfile`), mẫu lỗi sai (`ErrorPattern`), thông tin kỹ thuật (`TestMetadata`), và gợi ý học tập AI (nguồn sinh cụ thể — xem cảnh báo #3).
6. **Sử dụng kết quả:** `LanguageProfile` được xuất cho sinh viên xem, cho `ClassReport` tổng hợp báo cáo lớp cho `Teacher` (liên kết cần xác nhận — cảnh báo #4), và xuất theo chuẩn JSON cho hệ sinh thái **EduZ**.

---

*Tài liệu được biên soạn dựa trên sơ đồ lớp `TLCN-Trang-1.drawio.png` (đọc trực tiếp từ ảnh do người dùng cung cấp ngày 2026-09-18) và đối chiếu thuật ngữ với `SRS_TLCN (3).md`/`SRS_TLCN_v2.6_Final.docx`. Các điểm không đọc chắc chắn được từ ảnh (đặc biệt nhóm Auth, quan hệ `ClassReport`) đã được đánh dấu rõ ràng bằng ⚠️ trong toàn bộ tài liệu thay vì tự suy luận — cần Phương xác nhận lại trước khi dùng làm căn cứ chính thức cho báo cáo/bảo vệ. File nguồn dạng text (`ClassDiagram.mmd`, `ClassDiagram.puml` ở gốc repo) **chưa được cập nhật theo sơ đồ này** — cần đồng bộ riêng nếu vẫn còn dùng.*
