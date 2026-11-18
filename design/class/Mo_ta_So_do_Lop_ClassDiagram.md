# MÔ TẢ SƠ ĐỒ LỚP (CLASS DIAGRAM) — HỆ THỐNG PLACEMENT TEST THÍCH ỨNG

> **Phiên bản:** Tuần 7 (2026-10-26). Mô tả bản Class Diagram **gọn** `TLCN.drawio.xml` (3 trang: Tổng thể, Core CAT/Testing, Item Authoring/Review) và ảnh xem trước `TLCN-Trang-1.png`…`TLCN-Trang-3.png`.
> Bản mô tả cũ (47 lớp, theo `Trang-1` một trang) và sơ đồ cũ đã chuyển vào `_ARCHIVE_20261026/design/class/`.
> Ảnh PNG dựng bằng script (đường thẳng, có chỗ cắt qua hộp); **ảnh cuối cần xuất lại từ draw.io** sau khi chỉnh đường nối.
> Cập nhật 27/10: giữ lại `Item.irtA = 1.0`, `TestMetadata` (4 trường) và method của Admin/Teacher; xem `DECISIONS_LOG` #132. Đánh giá `schema.prisma`: `Tuan7/DANH_GIA_PRISMA_SAU_CHINH_LUOC_DO.md`.
> Bản gọn **không vẽ** một số cột vẫn tồn tại trong DB/`schema.prisma`: `User.isActive/mustChangePassword/createdAt`, `Item.contentHash/timesUsed/calibrated/irtC`, `ItemBatch.createdAt/createdById/skill/cefrTarget/requestedCount`, và các bảng lưu trữ `ExamRoundParticipant`, `ItemBatchAssignment`, `ItemReviewAssignment`, `ItemEmbedding`.
> Lý do từng chỗ sửa: `Tuan7/PHAN_TICH_DANH_GIA_CLASS_DIAGRAM_GON.md`. Quyết định: `DECISIONS_LOG` #128–#131.

## Lịch sử phiên bản

| Ngày | Thay đổi |
|---|---|
| 2026-09 → 2026-10-24 | Bản mô tả 47 lớp theo `Trang-1` (lưu ở `_ARCHIVE_20261026/design/class/`) |
| 2026-10-26 | Thay bằng bản gọn 3 trang và bảng mô tả theo từng lược đồ |
| 2026-10-27 | Thêm lại `irtA`, `TestMetadata`, method Admin/Teacher; bỏ `ItemBatch.createdAt`; thêm Mục 8–12 (quy tắc nghiệp vụ, đối chiếu `schema.prisma`, dữ liệu minh họa, module, tệp sinh tự động); sinh lại `ClassDiagram.puml/.mmd`; `schema.prisma` thêm khóa ngoại `ItemReviewEvent.packageId` |

---
# BẢNG MÔ TẢ 3 CLASS DIAGRAM (bản đề xuất đã rút gọn — Tuần 7)

> Mô tả bản `TLCN_ClassDiagram_Gon_Chuan_DeXuat.drawio.xml` (ảnh `TLCN_ClassDiagram_DeXuat_trang1/2/3.png`). **Chưa chốt** nên nằm ở `Tuan7/`, chưa thay bản chuẩn trong `docs-repo/`.
> Nguồn nghĩa: SRS v3.0, `schema.prisma`, `Mo_ta_So_do_Lop_ClassDiagram.md`, CLAUDE.md. Chỗ nào **tôi suy ra từ tên/ngữ cảnh** mà chưa đối chiếu được văn bản gốc thì ghi *(suy ra)*.
> Cách đọc: `-` thuộc tính, `+` phương thức, `/x` thuộc tính **suy ra** (tính khi cần, không lưu), `?` có thể rỗng (null), `◆` composition (bộ phận chết theo toàn thể), `▷` kế thừa, `→` association/phụ thuộc.

---

## 0. Ba lược đồ này là gì, khác nhau thế nào

| | Trang 1 — "Tổng thể" | Trang 2 — `Core_CAT_Testing_Domain` | Trang 3 — `Item_Authoring_Review_Workflow` |
|---|---|---|---|
| Loại | Class Diagram mức **toàn hệ thống** (miền nghiệp vụ) | Class Diagram **miền thi thích ứng** | Class Diagram **miền soạn–duyệt câu hỏi** |
| Thể hiện | Mọi lớp chính của TL trên một trang, để thấy hai miền nối nhau ở lớp `Item` | Sinh viên thi trong kỳ thi → phiên thi → chọn câu, ước lượng năng lực (CAT-Rasch) → hồ sơ năng lực | Câu hỏi được tạo theo **lô**, AI kiểm, giao GV duyệt hai chặng, Admin import cuối → mới được dùng để thi |
| Dành cho | Giới thiệu, báo cáo | Giải thích thuật toán CAT, phiên thi, hồ sơ xuất cho EduZ | Giải thích quy trình sinh–duyệt đề (F-23…F-28) |
| Số lớp / enum | 20 / 15 | 16 / 8 | 8 / 7 |

**Hai miền gặp nhau ở `Item`**: miền soạn–duyệt *sản xuất* câu hỏi; miền thi *tiêu thụ* câu hỏi, và chỉ lấy câu `FINAL_APPROVED`.

Ba trang là ba lát cắt của **cùng một mô hình**: lớp trùng tên (Item, TestSession…) là cùng một lớp. Mô tả chi tiết ở mục 1–3 dùng chung, mục 4–6 nói riêng từng trang (lớp nào nằm ở đâu, quan hệ nào).

---

## 1. Từ điển lớp — nhóm Người dùng và Kỳ thi

### 1.1 `User` `<<abstract>>` — người dùng hệ thống
Lớp cha của mọi tài khoản (hệ thống đơn trường, 3 role). Không tạo trực tiếp.

| Thuộc tính | Ý nghĩa |
|---|---|
| `id: UUID` | Mã định danh |
| `email: String` | Tên đăng nhập (đăng nhập chỉ email + mật khẩu; SSO thuộc Khóa luận) |
| `fullName: String` | Họ tên hiển thị |
| `role: UserRole` | Vai trò: `STUDENT`/`TEACHER`/`ADMIN`; quyết định quyền truy cập |

| Phương thức | Làm gì |
|---|---|
| `+ hasRole(role): boolean` | Kiểm tra tài khoản có đúng vai trò; Guard dùng để cho/chặn API |

### 1.2 `Student` (kế thừa `User`) — sinh viên
| Thuộc tính / phương thức | Ý nghĩa |
|---|---|
| `- studentCode: String` | Mã số sinh viên (duy nhất; lưu ở bảng `student_profiles`) |
| `+ getLatestProfile(): LanguageProfile` | Lấy hồ sơ năng lực của lần thi gần nhất |

### 1.3 `Teacher` (kế thừa `User`) — giảng viên
| Thuộc tính | Ý nghĩa |
|---|---|
| `- teacherCode: String` | Mã giảng viên (bảng `teacher_profiles`) |

| Phương thức | Làm gì |
|---|---|
| `+ reviewItem(item, action): void` | GV A duyệt hoặc từ chối một câu được giao (ghi `ItemReviewEvent` `APPROVE`/`REJECT`) |
| `+ submitPackage(pkg): void` | GV A gửi gói đã duyệt xong cho GV B xác nhận |

Khi Admin giao việc, giảng viên làm **GV A** (sửa, duyệt/từ chối, gửi gói) hoặc **GV B** (xác nhận/loại). Hai phương thức trên là hành vi đại diện của vai A; việc GV B xác nhận gói nằm ở `ItemPackage`/`Item` (chủ ý không vẽ thêm để lớp gọn).

### 1.4 `Admin` (kế thừa `User`) — quản trị viên trường
Không có thuộc tính riêng: Admin chỉ khác ở **quyền**. Admin **không sửa nội dung câu hỏi**.

| Phương thức | Làm gì |
|---|---|
| `+ createItemBatch(src): ItemBatch` | Tạo lô câu hỏi (AI sinh hoặc import file) |
| `+ importBatch(batch): void` | Import cuối: kiểm C3 rồi chuyển các câu đã qua hai chặng duyệt sang `FINAL_APPROVED` |
| `+ createExamRound(): ExamRound` | Tạo kỳ thi |

Các việc còn lại của Admin (giao việc, giao lại, chỉnh hạn, ép gửi gói, quản lý tài khoản) chạy qua service, chưa vẽ thành method.

### 1.5 `ExamRound` — kỳ thi
Một đợt thi có cửa sổ thời gian, danh sách sinh viên được thi và thời lượng làm bài.

| Thuộc tính | Ý nghĩa |
|---|---|
| `id`, `name` | Mã và tên kỳ thi |
| `durationMinutes: int = 45` | Số phút làm bài (mặc định 45, hợp lệ 5–180) |
| `status: ExamRoundStatus` | `DRAFT` → `SCHEDULED` → `OPEN` → `CLOSED` (chuyển trạng thái kiểu lazy khi truy vấn) |
| `opensAt`, `closesAt` | Cửa sổ thời gian cho phép vào thi |

| Phương thức | Làm gì |
|---|---|
| `+ isOpen(at): boolean` | Tại thời điểm `at`, kỳ thi có đang mở không (theo trạng thái và `opensAt`/`closesAt`) |
| `+ includesStudent(id): boolean` | Sinh viên có trong danh sách thi không |
| `+ registerStudent(s): void` | Thêm sinh viên vào danh sách thi (tầng lưu trữ là bảng `exam_round_participants`) |

### 1.6 Enum
| Enum | Giá trị | Ý nghĩa |
|---|---|---|
| `UserRole` | STUDENT, TEACHER, ADMIN | Ba vai trò (vai `EDUZ_SERVICE` chỉ là API Key của EduZ, không phải người dùng) |
| `ExamRoundStatus` | DRAFT, SCHEDULED, OPEN, CLOSED | Nháp → đã lên lịch → đang mở → đã đóng |

---

## 2. Từ điển lớp — nhóm Phiên thi và thuật toán thích ứng (CAT)

### 2.1 `TestSession` — phiên thi
Một lần làm bài của một sinh viên trong một kỳ thi. Dữ liệu bền vững nằm ở PostgreSQL.

| Thuộc tính | Ý nghĩa |
|---|---|
| `id` | Mã phiên |
| `student: Student` | Sinh viên làm bài |
| `examRound: ExamRound` | Kỳ thi chứa phiên (bắt buộc từ v3.0) |
| `status: SessionStatus` | `IN_PROGRESS` / `COMPLETED` / `ABANDONED` |
| `thetaFinal: float?`, `seFinal: float?` | Năng lực θ và sai số chuẩn SE **cuối cùng**; rỗng khi đang thi (θ đang chạy nằm ở cache) |
| `stoppingReason: StoppingReason?` | Vì sao dừng; rỗng khi chưa dừng |
| `startedAt`, `completedAt?` | Bắt đầu / kết thúc |
| `expiresAt: DateTime` | Hạn phiên = min(`startedAt` + `durationMinutes`, `closesAt`), tính một lần lúc bắt đầu |

| Phương thức | Làm gì |
|---|---|
| `+ submitAnswer(itemId, ans): SessionResponse` | Nhận câu trả lời, ghi `SessionResponse`, cập nhật θ/SE, kiểm điều kiện dừng |
| `+ computeResult(): LanguageProfile` | Khi phiên kết thúc: tính CEFR và dựng hồ sơ năng lực |
| `+ terminate(reason): void` | Kết thúc phiên với lý do (đủ câu, SE đạt ngưỡng, hết giờ…) |

### 2.2 `SessionResponse` — một câu trả lời trong phiên
| Thuộc tính | Ý nghĩa |
|---|---|
| `response: char` | Đáp án sinh viên chọn (A/B/C/D) |
| `isCorrect: boolean` | Đúng/sai (lưu để không phải chấm lại) |
| `thetaAfter`, `seAfter` | θ và SE **sau** câu này (vẽ được đường hội tụ) |
| `responseTimeMs` | Thời gian trả lời (ms) |
| `answeredAt` | Thời điểm trả lời |

### 2.3 `SessionCacheState` `<<Redis>>` — trạng thái phiên trong bộ nhớ đệm
Bản sao nóng của phiên đang thi để phản hồi nhanh và chống đua (race condition). Mất Redis thì dựng lại từ DB.

| Thuộc tính | Ý nghĩa |
|---|---|
| `state: SessionState` | `WAITING_FOR_ANSWER` (đã ra câu, chờ trả lời) / `READY_FOR_NEXT` (chờ chọn câu kế) |
| `currentItemId` | Câu đang hỏi |
| `eapState: EAPComputationState` | Trạng thái ước lượng năng lực đang dở |
| `lastSkillPicked: Skill` | Kỹ năng vừa ra, để luân phiên Vocabulary/Grammar |
| `itemsAdministered: UUID[]` | Các câu đã ra (không ra lại) |
| `lastUpdated` | Lần cập nhật cuối |
| `ttlSeconds = 7200` | Thời hạn cache 2 giờ (hạn phiên thật dựa vào `expiresAt` ở DB, không dựa TTL) |

| Phương thức | Làm gì |
|---|---|
| `+ reconstructFromDB(): void` | Dựng lại toàn bộ cache (kể cả `eapState`, `lastSkillPicked`) từ lịch sử `SessionResponse` khi Redis mất dữ liệu |

### 2.4 `EAPComputationState` `<<value object>>` — trạng thái tính EAP đang dở
| Thuộc tính | Ý nghĩa |
|---|---|
| `posteriorWeights: float[41]` | Trọng số xác suất hậu nghiệm tại 41 điểm θ ∈ [−4, +4], bước 0,2 |
| `theta`, `standardError` | θ và SE hiện thời tính từ các trọng số đó |

### 2.5 `CATEngine` `<<service>>` — bộ máy thi thích ứng
Không lưu trạng thái; mọi tham số (θ₀ = −0,5; ngưỡng SE 0,35; tối đa 25 câu; tối thiểu 8 câu trước Early Stop) lấy từ cấu hình.

| Phương thức | Làm gì |
|---|---|
| `+ pickNextSkill(cache): Skill` | Chọn kỹ năng kế tiếp theo round-robin cố định |
| `+ selectNextItem(cache, pool): Item` | Lấy 5 câu `FINAL_APPROVED` có độ khó b gần θ nhất, chọn ngẫu nhiên đều 1 câu (chống lộ đề) |
| `+ computeEAP(responses[]): AbilityEstimate` | Ước lượng θ theo EAP (lưới 41 điểm, prior N(0,1)); trả θ, SE, khoảng tin cậy 95% |
| `+ checkStoppingCriterion(cache): StoppingReason?` | Kiểm tra điều kiện dừng; trả lý do hoặc rỗng nếu tiếp tục |

### 2.6 `AbilityEstimate` `<<value object>>` — ước lượng năng lực
`theta` (năng lực θ), `standardError` (SE; càng nhỏ càng chắc), `confidenceInterval95: float[]` (khoảng tin cậy 95%). Do `CATEngine.computeEAP` sinh ra và được `LanguageProfile` chứa.

### 2.7 `LanguageProfile` `<<aggregate root>>` — hồ sơ năng lực
Kết quả cuối của một phiên, là dữ liệu xuất cho EduZ (JSON Profile v1).

| Thuộc tính | Ý nghĩa |
|---|---|
| `abilityEstimate` | θ, SE, khoảng tin cậy |
| `completedAt` | Thời điểm hoàn thành |
| `cefrLevel: CEFRLevel` | Trình độ CEFR suy từ θ |
| `cefrConfidence: CEFRConfidence` | Độ tin cậy của xếp loại (HIGH/MEDIUM/LOW) |
| `boundaryEffect: boolean` | `true` nếu θ nằm ngoài vùng phủ của ngân hàng câu hỏi (kết quả có thể chưa phân biệt tốt các mức biên) |
| `skillProfiles: List` | Điểm theo từng kỹ năng (`SkillProfile`) |
| `errorPatterns: List` | Các chủ đề hay sai (`ErrorPattern`) |
| `aiRecommendations: String[]` | Gợi ý học tập do AI sinh |

| Phương thức | Làm gì |
|---|---|
| `+ generateFromSession(s): void` | Dựng hồ sơ từ một phiên đã xong |
| `+ exportForEduZ(): String` | Xuất JSON Profile v1 cho hệ sinh thái EduZ |

### 2.8 `SkillProfile`, `ErrorPattern`, `TestMetadata` `<<value object>>`
| Lớp | Thuộc tính |
|---|---|
| `SkillProfile` | `skill` (kỹ năng); `scorePercent` (% đúng); `cefrEstimate` (CEFR riêng kỹ năng); `itemsAdministered` (số câu đã ra); `correctCount` (số câu đúng) |
| `TestMetadata` | `itemsAdministered` (số câu đã ra); `testDurationSeconds` (thời gian làm bài, giây); `algorithm = "EAP-41"` (thuật toán ước lượng, lưới 41 điểm); `stoppingReason` (vì sao dừng: đủ 25 câu, SE < 0,35, biên ngân hàng hoặc hết giờ). Gắn vào `LanguageProfile` để EduZ biết bài thi dừng vì lý do gì. Lưu ở cột JSON `test_metadata` |
| `ErrorPattern` | `topicTag` (chủ đề, vd. past_simple); `skill`; `itemsAttempted`; `correctCount`; `accuracyRate` (= đúng/đã làm); `/severity` (mức nghiêm trọng, **suy ra** từ `accuracyRate`) |

### 2.9 Enum miền thi
| Enum | Giá trị | Ý nghĩa |
|---|---|---|
| `SessionStatus` | IN_PROGRESS, COMPLETED, ABANDONED | Đang thi / đã xong / bỏ dở (hết hạn khi < 8 câu) |
| `StoppingReason` | MAX_ITEMS_REACHED, SE_THRESHOLD, ITEM_BANK_BOUNDARY, TIMEOUT | Đủ 25 câu / SE < 0,35 / kẹt ngoài vùng phủ ngân hàng (Outlier Early Stop) / hết giờ khi đã ≥ 8 câu |
| `SessionState` | WAITING_FOR_ANSWER, READY_FOR_NEXT | Trạng thái máy trạng thái trong Redis |
| `CEFRConfidence` | HIGH, MEDIUM, LOW | Độ tin cậy kết quả |
| `Skill` | VOCABULARY, GRAMMAR | Hai kỹ năng thuộc phạm vi TL |
| `CEFRLevel` | PRE_A1, A1, A2, B1, B2, C1_PLUS | Thang CEFR dùng trong hệ thống |

---

## 3. Từ điển lớp — nhóm Ngân hàng câu hỏi và Soạn–duyệt

### 3.1 `Item` — câu hỏi trắc nghiệm
Đơn vị trung tâm, nối hai miền.

| Thuộc tính | Ý nghĩa |
|---|---|
| `content`, `options: Json`, `correctAnswer: char` | Nội dung, các lựa chọn, đáp án đúng |
| `skill`, `topicTag?`, `cefrTarget` | Kỹ năng, chủ đề, mức CEFR hướng tới |
| `irtB: float` | Độ khó b theo mô hình Rasch (khoảng hợp lệ −4…+4, cấu hình được) |
| `irtA: float = 1.0 {Rasch}` | Độ phân biệt a, **cố định 1,0 cho mọi câu**: đây là điều kiện để mô hình là Rasch (1PL); nếu a thay đổi theo câu thì thành 2PL. `irtC` (đoán mò) không vẽ, thuộc Khóa luận |
| `status: ItemStatus` | Vòng đời một chiều (xem 3.8); **chỉ `FINAL_APPROVED` được CAT chọn** |

| Phương thức | Làm gì |
|---|---|
| `+ probability(θ): float` | Xác suất làm đúng theo Rasch: 1 / (1 + e^−(θ − b)) |
| `+ fisherInformation(θ): float` | Lượng thông tin của câu tại θ: P·(1 − P); lớn nhất khi b ≈ θ |
| `+ transitionTo(next): void` | Chuyển trạng thái duyệt, chỉ cho phép đi một chiều theo vòng đời |

*(Trang 3 chỉ vẽ `transitionTo`; hai phương thức Rasch chỉ ở trang 1–2 vì thuộc miền thi.)*

### 3.2 `Explanation` — lời giải thích
`content` (nội dung giải thích), `generatedAt` (lúc sinh). **Một lần cho mỗi câu**, dùng chung cho mọi sinh viên, sinh cùng lúc sinh câu hỏi; câu import thiếu giải thích thì sinh bổ sung.

### 3.3 `ItemBatch` — lô câu hỏi
Gom câu hỏi theo nguồn để kiểm và duyệt cùng nhau. Nguồn của câu hỏi nằm ở lô, **không** nằm trên `Item`.

| Thuộc tính | Ý nghĩa |
|---|---|
| `name?` | Nhãn hiển thị (dùng cho lô seed theo bộ nguồn) |
| `source: ItemBatchSource` | `AI_GENERATED` hoặc `IMPORTED` |
| `status: ItemBatchStatus` | Vị trí của lô trong quy trình (xem 3.8) |

> Ba cột `skill?`, `cefrTarget?`, `requestedCount?` (đích và số lượng yêu cầu của lô AI sinh) **không vẽ trên lược đồ**; chúng chỉ nằm ở DB, tạo sau. Chủ đề của từng câu được biểu diễn bằng `Item.topicTag?`.

| Phương thức | Làm gì |
|---|---|
| `+ transitionTo(next): void` | Chuyển trạng thái lô hợp lệ |
| `+ canAssign(): boolean` | Lô đã qua kiểm C1/C2 và ở `READY_TO_ASSIGN` nên Admin giao việc được (kế hoạch Mục 3) |
| `+ canFinalize(): boolean` | Lô ở `READY_TO_FINALIZE`: mọi gói đã `DONE` **hoặc** mọi hạn đã qua; chỉ khi đó Admin mới chạy kiểm C3 và import (DC-44) |

### 3.4 `ItemPackage` — gói duyệt
Mỗi GV A có **một gói** trong một lô, tạo lúc Admin giao việc. A duyệt xong thì **gửi** gói cho GV B xác nhận.

| Thuộc tính | Ý nghĩa |
|---|---|
| `reviewerId` | GV A (người duyệt/sửa) |
| `confirmerId` | GV B (người xác nhận) |
| `status: PackageStatus` | `OPEN` → `SENT` → `DONE` |
| `sentAt?`, `dueAt?` | Ngày gửi và hạn xác nhận; rỗng khi gói còn `OPEN` |

| Phương thức | Làm gì |
|---|---|
| `+ canSend(): boolean` | Gói đủ điều kiện để A gửi cho B: A đã duyệt xong phần của mình, gửi một lần (DC-42); điều kiện chi tiết xem kế hoạch |
| `+ isOverdue(at): boolean` | Quá hạn tại thời điểm `at` (quá `dueAt` mà chưa `DONE`) |

### 3.5 `ItemCheckResult` — kết quả AI kiểm một câu
Một dòng cho mỗi lần kiểm một câu ở một điểm kiểm.

| Thuộc tính | Ý nghĩa |
|---|---|
| `checkpoint: CheckPoint` | Điểm kiểm: `C1` (sau khi AI sinh), `C2` (khi import file), `C3` (trước import cuối) |
| `level: CheckLevel` | `PASS` / `SOFT` (cảnh báo) / `HARD` (lỗi nặng) |
| `reasonCodes: String[]` | Mã lý do (sai đáp án, nghi trùng…) |
| `suspectedDuplicateId?` | Câu nghi bị trùng (nếu lý do là trùng) |
| `checkedAt` | Lúc kiểm |

| Phương thức | Làm gì |
|---|---|
| `+ isPassed(): boolean` | Kết quả kiểm có đạt không *(suy ra từ `level`; ngưỡng chi tiết xem `KE_HOACH_SINH_VA_DUYET_DE_AI.md`)* |

### 3.6 `ItemReviewEvent` — nhật ký kiểm toán
Mỗi thao tác duyệt/giao việc để lại một dòng (truy vết, phục vụ hội đồng hỏi).

| Thuộc tính | Ý nghĩa |
|---|---|
| `batchId` | Lô liên quan |
| `itemId?` | Câu liên quan; rỗng với thao tác tác động nhiều câu/gói (`CONFIRM_ALL`, `REASSIGN`, `EXTEND`, `FORCE_SEND`) |
| `actorId` | Người thực hiện |
| `action: ReviewAction` | Hành động |
| `createdAt` | Lúc xảy ra |

### 3.7 Enum miền soạn–duyệt
| Enum | Giá trị | Ý nghĩa |
|---|---|---|
| `ItemBatchSource` | AI_GENERATED, IMPORTED | Lô do AI sinh / import từ file |
| `ItemBatchStatus` | GENERATING / IMPORTING → CHECKING → READY_TO_ASSIGN → IN_REVIEW → READY_TO_FINALIZE → FINAL_CHECKED → DONE; FAILED, PARTIAL | Đang sinh hoặc đang import → AI đang kiểm → chờ giao việc → đang duyệt → chờ import cuối → đã kiểm C3 → xong; lỗi; xong một phần |
| `PackageStatus` | OPEN, SENT, DONE | Gói đang soạn / A đã gửi B / B đã xác nhận xong |
| `CheckPoint` | C1, C2, C3 | Ba điểm kiểm AI |
| `CheckLevel` | PASS, SOFT, HARD | Đạt / cảnh báo / lỗi nặng |
| `ReviewAction` | APPROVE, REJECT, CONFIRM, REMOVE, CONFIRM_ALL, IMPORT, REASSIGN, EXTEND, FORCE_SEND, ACCEPT_FLAG | A duyệt / A từ chối / B xác nhận / B loại / B xác nhận cả gói / Admin import / giao lại / gia hạn / ép gửi gói / chấp nhận cảnh báo |

### 3.8 `ItemStatus` — vòng đời câu hỏi
| Giá trị | Ý nghĩa |
|---|---|
| `DRAFT` | Mới tạo |
| `FIRST_APPROVED` | GV A đã duyệt |
| `SECOND_APPROVED` | GV B đã xác nhận |
| `FINAL_APPROVED` | Admin đã import cuối → **được CAT dùng** |
| `REJECTED` | Người loại |
| `AI_REJECTED` | Máy loại (lưu mã lý do ở `ItemCheckResult`) |

Đi một chiều: `DRAFT → FIRST_APPROVED → SECOND_APPROVED → FINAL_APPROVED`; `REJECTED`/`AI_REJECTED` là điểm cuối.

---

## 4. Trang 1 — Lược đồ tổng thể

**Thể hiện:** toàn bộ miền nghiệp vụ TL trên một trang: người dùng, kỳ thi, phiên thi + CAT, hồ sơ năng lực, ngân hàng câu hỏi và quy trình soạn–duyệt.
**Thực thể (21 lớp):** User, Student, Teacher, Admin, ExamRound, TestSession, SessionResponse, SessionCacheState, EAPComputationState, CATEngine, AbilityEstimate, LanguageProfile, SkillProfile, ErrorPattern, TestMetadata, Item, Explanation, ItemCheckResult, ItemBatch, ItemPackage, ItemReviewEvent. **15 enum** nằm cạnh lớp dùng chúng (không vẽ mũi tên từ lớp tới enum; kiểu thuộc tính đã cho biết).

| Quan hệ | Loại / bội số | Ý nghĩa |
|---|---|---|
| Student, Teacher, Admin ▷ User | Kế thừa | Ba loại người dùng chung thuộc tính tài khoản |
| Admin — ExamRound | Association | Admin tạo/công bố/đóng kỳ thi |
| ExamRound — Student | Association (N–N) | Danh sách sinh viên được thi trong kỳ |
| ExamRound → TestSession | `0..*` | Một kỳ thi có nhiều phiên (mới tạo thì chưa có) |
| Student — TestSession | Association | Sinh viên làm các phiên thi |
| TestSession ◆ SessionResponse | Composition `1..*` | Phiên gồm các câu trả lời; xoá phiên thì mất câu trả lời |
| SessionResponse — Item | Association | Mỗi câu trả lời tham chiếu đúng một câu hỏi |
| TestSession — SessionCacheState | Association | Mỗi phiên đang thi có một trạng thái cache |
| SessionCacheState ◆ EAPComputationState | Composition `1` | Cache chứa trạng thái ước lượng, không sống riêng |
| CATEngine → SessionCacheState | Phụ thuộc (Use) | Engine đọc/ghi cache; **một chiều** để không vòng |
| CATEngine → Item | Phụ thuộc (Use) | Engine chọn câu từ ngân hàng và dùng công thức Rasch của `Item` |
| LanguageProfile — TestSession | Association | Hồ sơ sinh ra từ một phiên |
| LanguageProfile — Student | Association | Hồ sơ thuộc về một sinh viên |
| LanguageProfile ◆ AbilityEstimate / SkillProfile / ErrorPattern / TestMetadata | Composition `1` | Các khối con của hồ sơ |
| Explanation ◆→ Item | Composition `0..1` | Mỗi câu có tối đa một giải thích |
| Item ◆ ItemCheckResult | Composition `0..*` | Câu có nhiều lần kiểm (C1, C2, C3) |
| ItemBatch ◆ Item | Composition `1..*` | Mọi câu thuộc đúng một lô |
| ItemBatch ◆ ItemPackage | Composition `1..*` | Lô được chia thành các gói (mỗi GV A một gói) |
| ItemPackage → Item | Association `0..*` | Gói chứa các câu A đã gửi (câu A loại không vào gói) |

*ItemReviewEvent không nối cạnh ở trang này (xem trang 3).*

---

## 5. Trang 2 — `Core_CAT_Testing_Domain`: miền thi thích ứng

**Thể hiện:** đường đi từ kỳ thi đến hồ sơ năng lực: Sinh viên → Kỳ thi → Phiên thi → (cache Redis + CATEngine chọn câu/ước lượng) → Câu trả lời → Hồ sơ năng lực.
**Thực thể (17 lớp):** User, Student, Teacher, Admin, ExamRound, TestSession, SessionResponse, SessionCacheState, EAPComputationState, CATEngine, AbilityEstimate, LanguageProfile, SkillProfile, ErrorPattern, TestMetadata, Item, Explanation. **8 enum**: UserRole, ExamRoundStatus, SessionStatus, StoppingReason, SessionState, CEFRConfidence, Skill, CEFRLevel.
Trên trang này `Item` chỉ có phần phục vụ thi (`probability`, `fisherInformation`); phần duyệt ở trang 3.

| Quan hệ | Bội số | Ý nghĩa |
|---|---|---|
| Student/Teacher/Admin ▷ User | — | Kế thừa |
| Student → TestSession | `0..*` | Sinh viên có nhiều phiên theo thời gian |
| ExamRound → TestSession | `0..*` | Kỳ thi có nhiều phiên |
| ExamRound → Student | `0..*` | Sinh viên đăng ký thi (bảng lưu trữ `ExamRoundParticipant`) |
| TestSession ◆ SessionResponse | `1..*` | Các câu trả lời của phiên |
| SessionResponse → Item | `1` | Câu trả lời ứng với một câu hỏi |
| TestSession → SessionCacheState | Use | Phiên dùng cache Redis |
| SessionCacheState ◆ EAPComputationState | `1` | Trạng thái ước lượng đang dở |
| CATEngine → AbilityEstimate | «compute» | Engine tính ra ước lượng năng lực |
| CATEngine → Item | «select» | Engine chọn câu kế tiếp |
| TestSession → LanguageProfile | `0..1` | Phiên xong tạo tối đa một hồ sơ |
| Student → LanguageProfile | `0..*` | Một sinh viên có nhiều hồ sơ (mỗi lần thi một hồ sơ) |
| LanguageProfile ◆ SkillProfile | `1..*` | Có điểm theo kỹ năng |
| LanguageProfile ◆ ErrorPattern | `0..*` | Có thể không có lỗi nổi bật |
| LanguageProfile ◆ TestMetadata | `1` | Thông tin bài thi đi kèm hồ sơ |
| Item ◆ Explanation | `0..1` | Giải thích của câu |

Ghi chú trên trang: `ExamRoundParticipant` là bảng lưu trữ của quan hệ N–N (có `note`, `addedAt`), không vẽ riêng; `CATEngine` không giữ trạng thái.
*Chưa vẽ cạnh `SessionCacheState`→`CATEngine`: đã bỏ để tránh phụ thuộc vòng.*

---

## 6. Trang 3 — `Item_Authoring_Review_Workflow`: soạn và duyệt câu hỏi

**Thể hiện:** vòng đời một câu hỏi từ khi sinh/import đến khi dùng được: Admin tạo **lô** (AI sinh hoặc import file) → AI kiểm C1/C2 → Admin giao việc, hệ thống tạo **gói** cho từng GV A → A duyệt/sửa rồi gửi gói → GV B xác nhận → Admin kiểm C3 và import cuối (`FINAL_APPROVED`). Mọi thao tác ghi vào nhật ký.
**Thực thể (8 lớp):** Item, Explanation, ItemCheckResult, ItemBatch, ItemPackage, ItemReviewEvent, Admin, Teacher. **7 enum**: ItemStatus, CheckPoint, CheckLevel, ItemBatchSource, ItemBatchStatus, PackageStatus, ReviewAction.

| Quan hệ | Bội số | Ý nghĩa |
|---|---|---|
| ItemBatch ◆ Item | `1..*` | Lô gồm các câu |
| ItemBatch ◆ ItemPackage | `1..*` | Lô chia thành các gói giao cho từng GV A |
| ItemPackage → Item | `0..*` | Gói chứa các câu A gửi lên B |
| Item ◆ Explanation | `0..1` | Giải thích của câu |
| Item ◆ ItemCheckResult | `0..*` | Các lần AI kiểm của câu |
| Item → ItemReviewEvent | `0..*` | Lịch sử thao tác trên câu |
| ItemPackage → ItemReviewEvent | `0..*` | Thao tác ở mức gói (gửi, ép gửi, gia hạn…) |
| Admin → ItemBatch | «creates» | Admin tạo lô (AI sinh hoặc import) |
| Teacher → ItemPackage | «reviews» | Giảng viên duyệt (GV A) hoặc xác nhận (GV B) gói được giao |

Ghi chú trên trang: `ItemBatchAssignment` và `ItemReviewAssignment` (giao việc) và `ItemEmbedding` (vector lọc trùng) chỉ có ở schema, không vẽ ở đây vì là chi tiết lưu trữ.

**Vai trò theo quy trình** (để đọc cạnh «creates»/«reviews»): Admin tạo lô, giao việc, kiểm C3, import cuối, **không sửa nội dung câu**. GV A sửa nội dung/đáp án/giải thích, duyệt hoặc từ chối, gửi gói. GV B xác nhận hoặc loại câu trong gói, **không sửa**, không trả về A. GV không import đề.

---

## 7. Hai điểm cần lưu ý khi dùng bảng này

1. **Đây là mô tả bản đề xuất rút gọn**, khác bản mô tả hiện hành `Mo_ta_So_do_Lop_ClassDiagram.md` ở chỗ: bỏ `ErrorSeverity`, hằng số trong `CATEngine`, thuộc tính danh sách của Admin/Teacher, một số trường KL và trường kiểm toán (`createdAt` của `User`/`ItemBatch`...). Đã **giữ lại** `Item.irtA = 1.0`, `TestMetadata` và 2–3 method của Admin/Teacher theo yêu cầu 27/10. Nếu nhóm không chấp nhận bản đề xuất thì bảng này cần chỉnh lại.
2. `canAssign`, `canFinalize`, `canSend` đã đối chiếu với `KE_HOACH_SINH_VA_DUYET_DE_AI.md` (Mục 2.3, DC-42, DC-44). Riêng `ItemCheckResult.isPassed()` vẫn là *suy ra*: kế hoạch chỉ nêu ba mức PASS/SOFT/HARD, chưa đọc được quy tắc "đạt" chính xác (SOFT có tính đạt không); cần xác nhận trước khi đưa vào báo cáo.


---

## 8. Quy tắc nghiệp vụ gắn với từng lớp

Các quy tắc dưới đây lấy từ SRS v3.0, `CLAUDE.md` và kế hoạch sinh đề; lược đồ không vẽ được chúng nên ghi ở đây để đọc cạnh bảng thuộc tính.

| Lớp | Quy tắc | Nguồn |
|---|---|---|
| `User` | Đăng nhập chỉ bằng email + mật khẩu (SSO thuộc Khóa luận). Mật khẩu tạm 12 ký tự, bắt buộc đổi ở lần đăng nhập đầu. Hệ thống đơn trường, không có `Institution` | SRS Mục III, DC-19 |
| `Admin` | Có toàn bộ quyền của `TEACHER` thông qua phân quyền (không phải kế thừa lớp). **Không sửa nội dung câu và không gõ câu bằng form**. Không thu hồi được Admin cuối cùng. Admin đầu tiên tạo bằng script cài đặt | CLAUDE.md, DC-29 |
| `Teacher` | Chỉ làm GV A hoặc GV B khi Admin giao việc; Admin không làm GV A/B (danh sách chọn chỉ lấy role `TEACHER`). GV không import đề | #120 |
| `ExamRound` | `durationMinutes` mặc định 45, hợp lệ 5–180; `opensAt` < `closesAt`; trạng thái chuyển **lazy** (tính khi truy cập): `DRAFT` → `SCHEDULED` → `OPEN` → `CLOSED` | SRS, DC-07…DC-10 |
| `TestSession` | `expiresAt = min(startedAt + durationMinutes, closesAt)`, tính **một lần** lúc bắt đầu phiên. Hết hạn: từ 8 câu trở lên thì `COMPLETED` + `TIMEOUT`, ít hơn thì `ABANDONED`. Mỗi sinh viên chỉ có một phiên đang chạy (mã lỗi `SESSION_IN_PROGRESS`). Sinh viên phải nằm trong danh sách của kỳ thi | DC-20, #122 |
| `CATEngine` | Không giữ trạng thái. Tham số **cấu hình, không hardcode**: θ₀ = −0,5; ngưỡng SE 0,35; tối đa 25 câu; tối thiểu 8 câu trước khi Early Stop có hiệu lực; lưới EAP 41 điểm trên [−4, +4] bước 0,2; prior N(0, 1). Thứ tự dừng: SE → đủ câu → Early Stop → hết hạn | CLAUDE.md, SRS 4.x |
| `Item` | Chỉ `FINAL_APPROVED` được CAT chọn, **lọc ở tầng Repository**. `irtA` cố định 1,0 (Rasch). `irtB` nằm trong [−4, +4]. Mọi câu thuộc đúng một `ItemBatch` (`batchId` bắt buộc). Câu `FINAL_APPROVED` cấm sửa. Vòng đời một chiều, không quay lại | SRS 6.x, #64, DC-34 |
| `ItemBatch` | Trạng thái đi một chiều `GENERATING`/`IMPORTING` → `CHECKING` → `READY_TO_ASSIGN` → `IN_REVIEW` → `READY_TO_FINALIZE` → `FINAL_CHECKED` → `DONE`; nhánh lỗi `FAILED`, `PARTIAL`. Lô seed của từng bộ nguồn là lô `IMPORTED`/`DONE` | KE_HOACH_SINH_VA_DUYET_DE_AI |
| `ItemPackage` | Một gói cho mỗi GV A trong một lô (unique `batchId` + `reviewerId`). `OPEN` → `SENT` → `DONE`. Gói `SENT` không trả về A | DC-42 |
| `ItemReviewEvent` | Chỉ ghi thêm, không sửa hay xóa. Hành động cấp lô hoặc gói (`CONFIRM_ALL`, `REASSIGN`, `EXTEND`, `FORCE_SEND`) có `itemId` rỗng | SRS 6.2b |
| `LanguageProfile` | Mỗi phiên hoàn thành tạo tối đa một hồ sơ (`testSessionId` duy nhất). Xuất cho EduZ ở dạng JSON Profile v1 qua `exportForEduZ()` | SRS Mục IX |

## 9. Đối chiếu với `schema.prisma`: cột có ở DB nhưng không vẽ

Lược đồ gọn là tập con của schema (quyết định #128, #130, #132). Bảng này cho biết từng lớp còn gì ở DB. Dùng khi viết migration hoặc khi hội đồng hỏi "cột X nằm ở đâu".

| Lớp (bảng) | Cột chỉ có ở DB | Ý nghĩa |
|---|---|---|
| `User` (`users`) | `passwordHash` | Mật khẩu đã băm (argon2) |
| | `authProvider`, `externalId` | Chỗ cho SSO của Khóa luận; TL chỉ dùng email + mật khẩu |
| | `mustChangePassword`, `passwordChangedAt` | Buộc đổi mật khẩu lần đầu, mốc đổi gần nhất |
| | `isActive` | Khóa/mở tài khoản |
| | `createdAt` | Mốc tạo |
| `Student`/`Teacher` (`student_profiles`, `teacher_profiles`) | `userId` | Khóa nối về `users` (một-một) |
| `ExamRound` (`exam_rounds`) | `createdById`, `createdAt`, `updatedAt` | Admin tạo kỳ thi và mốc kiểm toán |
| `ExamRoundParticipant` (`exam_round_participants`) | cả bảng | Bảng nối kỳ thi và sinh viên, có `note`, `addedAt`. **Không bỏ được ở DB**: `TestSession` có khóa kép `(examRoundId, studentId)` trỏ tới đây để chỉ sinh viên được đăng ký mới có phiên thi |
| `TestSession` (`test_sessions`) | `studentId`, `examRoundId` | Khóa ngoại của hai đường nối tới `Student` và `ExamRound` |
| `SessionResponse` (`session_responses`) | `sessionId`, `itemId` | Khóa ngoại của hai đường nối |
| `LanguageProfile` (`language_profiles`) | `schemaVersion` | Phiên bản định dạng JSON Profile |
| | `studentId`, `testSessionId` | Khóa ngoại |
| | `theta`, `standardError`, `confidenceInterval95` | Cột phẳng của `AbilityEstimate` (hồ sơ lưu kiểu lai: cột + JSON, #18) |
| | `skillProfiles`, `errorPatterns`, `testMetadata` | Cột JSON của `SkillProfile`, `ErrorPattern`, `TestMetadata` |
| `Item` (`items`) | `irtC` | Tham số đoán mò 0,25, **dành cho Khóa luận**, TL không dùng |
| | `timesUsed` | Số lần đã dùng, theo dõi mức lộ đề |
| | `calibrated` | Đã hiệu chuẩn `irtB` bằng dữ liệu thật chưa |
| | `contentHash` | Mã băm nội dung chuẩn hóa, dùng phát hiện trùng (kiểm C1) và tái dùng kết quả kiểm |
| | `approvedById`, `approvedAt` | Admin bấm Import; người duyệt thật nằm ở `ItemReviewEvent` |
| | `batchId`, `packageId` | Khóa ngoại tới lô (bắt buộc) và gói (rỗng tới khi A gửi gói) |
| | `createdAt`, `updatedAt` | Mốc kiểm toán |
| `Explanation` (`explanations`) | `itemId` | Khóa ngoại (một-một với `Item`) |
| `ItemEmbedding` (`item_embeddings`) | cả bảng | Vector `Float[]` của câu để lọc trùng; cosine tính trong ứng dụng, không dùng pgvector |
| `ItemCheckResult` (`item_check_results`) | `itemId`, `contentHash` | Khóa ngoại; băm nội dung tại thời điểm kiểm |
| `ItemBatch` (`item_batches`) | `createdById` | Admin tạo lô |
| | `skill`, `cefrTarget`, `topicTag`, `requestedCount` | Đích và số lượng yêu cầu; **chỉ lô AI sinh có**, lô import để trống |
| | `createdAt`, `updatedAt` | Mốc kiểm toán |
| `ItemBatchAssignment` (`item_batch_assignments`) | cả bảng | Cấu hình giao việc của lô: GV B xác nhận, số ngày duyệt/xác nhận, người giao |
| `ItemReviewAssignment` (`item_review_assignments`) | cả bảng | Giao từng câu cho GV A: người nhận, hạn, đã nhắc chưa |
| `ItemPackage` (`item_packages`) | `batchId` | Khóa ngoại tới lô |
| | `reminderSent` | Đã gửi email nhắc chưa |
| `ItemReviewEvent` (`item_review_events`) | `packageId` | Gói liên quan; khóa ngoại được bổ sung trong schema 27/10/2026 (cần migration) |

## 10. Dữ liệu minh họa

Các giá trị dưới đây **chỉ để minh họa cách đọc**, không phải kết quả đo thật.

`TestMetadata` (lưu ở cột JSON `test_metadata`):

```json
{ "itemsAdministered": 18, "testDurationSeconds": 1260, "algorithm": "EAP-41", "stoppingReason": "SE_THRESHOLD" }
```

`Item.topicTag` của bộ câu CLOTH đã gán (Mục 10 của `_data/README.md`, gán theo luật loại từ/chức năng của từ đáp án, chưa phải chủ đề ngữ nghĩa):

| Kỹ năng | Giá trị `topicTag` |
|---|---|
| Vocabulary | `vocab_noun`, `vocab_verb`, `vocab_adjective`, `vocab_adverb`, `vocab_other`, `vocab_unknown` |
| Grammar | `grammar_article`, `grammar_preposition`, `grammar_pronoun`, `grammar_wh_relative`, `grammar_conjunction`, `grammar_quantifier`, `grammar_be_have_do`, `grammar_modal`, `grammar_comparison`, `grammar_verb_form`, `grammar_word_form`, `grammar_other_function` |

`ErrorPattern.topicTag` dùng cùng cột chủ đề này để gom lỗi của sinh viên.

## 11. Lớp trên lược đồ và nơi dự kiến đặt trong mã

Tên module theo `CLAUDE.md`; các tên đánh dấu *(chờ duyệt)* là đề xuất chưa được nhóm chốt.

| Lớp | Module backend |
|---|---|
| `User`, `Student`, `Teacher`, `Admin` | `auth`, `user-admin` *(chờ duyệt)* |
| `ExamRound` | `exam-round` *(chờ duyệt)* |
| `TestSession`, `SessionResponse`, `SessionCacheState`, `EAPComputationState` | `test-session` |
| `CATEngine`, `AbilityEstimate` | `cat-engine` |
| `LanguageProfile`, `SkillProfile`, `ErrorPattern`, `TestMetadata` | `language-profile`, `reporting` |
| `Item`, `ItemCheckResult` | `item-bank` |
| `Explanation` | `ai-explainer` |
| `ItemBatch`, `ItemPackage`, `ItemReviewEvent` | `item-generation` *(chờ duyệt)* |

## 12. Tệp liên quan và cách sinh lại

| Tệp | Vai trò |
|---|---|
| `TLCN.drawio.xml` | **Nguồn chính**, 3 trang. Sửa ở đây trước |
| `TLCN-Trang-1.png`…`TLCN-Trang-3.png` | Ảnh xem trước dựng bằng script (đường thẳng, có chỗ cắt qua hộp); cần xuất lại từ draw.io |
| `ClassDiagram.puml`, `ClassDiagram.mmd` | Sinh tự động từ `TLCN.drawio.xml` bằng `Tuan7/scripts/gen_uml.py`, gộp 3 trang thành một mô hình (36 khối: 21 lớp và 15 enum, 29 quan hệ). **Không sửa tay**. Chưa được dựng thử bằng PlantUML hoặc Mermaid |
| `schema.prisma` | Bản tham chiếu của schema; bản thật ở `backend/backend/prisma` |

Sinh lại: `python -I Tuan7/scripts/gen_uml.py docs-repo/design/class/TLCN.drawio.xml docs-repo/design/class/ClassDiagram.puml docs-repo/design/class/ClassDiagram.mmd`.
