# Kế hoạch: Admin tạo đề (AI hoặc import file) → AI check → GV A duyệt → GV B confirm → Admin kiểm tra và import

> **Ngày lập:** 2026-10-14 (Tuần 5). **Phiên bản 5 (viết lại toàn bộ theo luồng mới).** Các bản trước lưu ở `_BACKUP_20261014_KE_HOACH_SINH_VA_DUYET_DE_AI_V1…V4.md`.
> **Trạng thái:** ⛔ **CHỜ BẠN DUYỆT.** Chưa sửa SRS, Use Case, Class Diagram, Prisma, Sequence, màn hình. Tên bảng, endpoint, UC, màn hình, tên trạng thái phụ và mọi con số ngưỡng là **đề xuất của AI**; chỉ những dòng ghi nguồn "Bạn" là quyết định của bạn.
> **Giới hạn:** chưa chạy thử lời gọi AI nào; chưa đo chi phí, độ trễ, tỷ lệ trùng; tên mô hình embedding và hạn mức Gemini **chưa kiểm chứng**; chưa kiểm `pg_trgm` trên image Postgres staging.
> **Nguồn:** `Tuan2/Phuong_an_sua_doi_AI.md`, `ai-llm-gateway.md`, `DECISIONS_LOG.md` (#8, #9, #56, #60, #63, #64, #96, #102–#109), `schema.prisma`.

---

## 1. Quyết định (cột "Nguồn" cho biết ai chốt)

| ID | Nội dung | Nguồn | Log |
|---|---|---|---|
| DC-27 | **Luồng mới:** Admin tạo đề bằng **AI** hoặc **tự import file** → **AI check** → Admin xem kết quả rồi bấm **Giao việc** → **GV A duyệt** → A xong phần mình thì **gửi một gói** cho **GV B** → **B confirm** → Admin bấm **Kiểm tra** (AI check lần cuối) → Admin **Import** → `FINAL_APPROVED`. | Bạn | #110 |
| DC-28 | **GV không import đề.** Chỉ Admin nhập file. (Đảo DC-28 cũ/#103.) | Bạn | #110 |
| DC-29 | **Admin không gõ câu bằng form**, chỉ AI sinh hoặc import file; Admin không soạn và không duyệt nội dung. (Sửa #104.) | Bạn + AI diễn giải | #110 |
| DC-30 | **Lọc trùng nhiều tầng, dùng chung** mọi điểm AI check (Mục 4). Chấp nhận tốn API nhưng tiết kiệm nhất có thể. | Bạn | #105 |
| DC-31 | **Giải thích AI sinh cùng lúc sinh câu hỏi**, lưu bảng `explanations` (xác nhận lại #60/#63). | Đã chốt trước | #105 |
| DC-32 | Không ai thêm từng câu bằng form (bỏ UCGV03). `ItemSource`: `MANUAL` → `IMPORTED` (tên mới là đề xuất). | Bạn + AI đặt tên | #106 |
| DC-33 | **B xử lý từng câu: Xác nhận hoặc Loại bỏ** (`REJECTED`, không lưu lý do, #56) **và có nút "Xác nhận tất cả câu còn lại"**. **Không có trả về cho A.** B không sửa nội dung. A được sửa nội dung, đáp án, giải thích. | Bạn | #109, #112 |
| DC-34 | `irt_b` hợp lệ khi lọc: **−4 đến +4** (cấu hình); khác `CLAUDE.md` (−2.5…+1.5) ⇒ sửa `CLAUDE.md`. | Bạn | #107 |
| DC-35 | **Làm đủ T3 (embedding) và G5 (kiểm đáp án độc lập) từ đầu.** | Bạn | #107 |
| DC-37 | **Hạn do Admin đặt, tính từ ngày giao**, Admin chỉnh được. Chi tiết Mục 6.3. | Bạn + AI chi tiết | #108 |
| DC-38 | **Nhắc việc trước hạn 24 giờ.** | Bạn | #108 |
| DC-39 | **Trạng thái `Item`:** `DRAFT` → `FIRST_APPROVED` → `SECOND_APPROVED` → `FINAL_APPROVED` (thay `APPROVED` cũ); `REJECTED` (người loại); thêm `AI_REJECTED` (máy loại, **tên là đề xuất**). | Bạn + AI thêm `AI_REJECTED` | #109, #112 |
| DC-40 | **Hai nhóm tách riêng:** nhóm **A** (nhiều GV duyệt) và **B** (**một GV đại diện, như trưởng bộ môn**). B do **Admin chọn khi bấm Giao việc**, B không thuộc nhóm A. | Bạn | #111 |
| DC-41 | **Giao việc sau khi AI check xong**, Admin xem kết quả rồi bấm "Giao việc"; hệ thống **chia đều** cho nhóm A (Mục 5). | Bạn | #111 |
| DC-42 | **A duyệt xong toàn bộ phần của mình thì gửi một lần, thành một gói riêng cho B.** Nhiều A ⇒ nhiều gói, gửi vào các thời điểm khác nhau. | Bạn | #111 |
| DC-43 | **Câu A loại** ⇒ `REJECTED`, giữ trong lô, Admin xem danh sách và thống kê, không dùng lại. **Câu AI loại** ⇒ `AI_REJECTED`, lưu nội dung và lý do, chỉ Admin xem, không đưa cho GV. | Bạn | #112 |
| DC-44 | **Admin chỉ import khi cả lô đã confirm xong hoặc quá hạn.** Trước khi import, Admin bấm **Kiểm tra** (AI check lần 3). | Bạn | #112 |
| DC-45 | **Ba điểm AI check, mỗi điểm tối ưu riêng** (Mục 4). **Câu rớt ở lần 3:** lỗi cứng tự `AI_REJECTED`, lỗi mềm Admin quyết. | Bạn **ủy quyền** AI cân nhắc, **chờ bạn xác nhận** | #113 |

**Hệ quả vai trò (sửa DC-18):** GV có thêm **duyệt (A)** và, nếu được Admin chọn, **confirm (B)** các câu được giao. GV **không** import, không tạo lô, không duyệt tùy ý. Admin: tạo lô, import file, giao việc, giao lại, chỉnh hạn, kiểm tra, import cuối; không sửa nội dung câu.
**Phạm vi:** `ai-question-generator` (KL) kéo vào TL ⇒ phạm vi tăng, phải cập nhật `COMMITMENT_BASELINE.md` trước khi ký (gate G1, hết Tuần 6).

---

## 2. Vòng đời và trạng thái

### 2.1. Sơ đồ

```
Admin tạo lô (AI sinh) ──┐
                         ├─► [C1/C2: AI check] ──┬─ qua ─► DRAFT ─► (Admin Giao việc) ─► A duyệt ─► FIRST_APPROVED ─► (A gửi gói) ─► B confirm ─► SECOND_APPROVED
Admin import file ───────┘                       └─ rớt ─► AI_REJECTED                          └─ A loại ─► REJECTED              └─ B loại ─► REJECTED

SECOND_APPROVED ─(cả lô xong hoặc quá hạn)─► Admin bấm Kiểm tra (C3) ─┬─ qua ─────────────► Admin Import ─► FINAL_APPROVED
                                                                      ├─ lỗi cứng ───────► AI_REJECTED
                                                                      └─ lỗi mềm ────────► Admin quyết: Import hoặc Loại (REJECTED)
```
Một chiều, **không có đường quay lại**. Chỉ `FINAL_APPROVED` được `CATEngine.selectNextItem()` chọn (đổi tên từ `APPROVED`, tác động Mục 11).

### 2.2. Bảng trạng thái

| Trạng thái | Ý nghĩa | Ai/cái gì chuyển |
|---|---|---|
| `DRAFT` (đã có) | Đã qua AI check, chờ Admin giao việc, hoặc đã giao và chờ A duyệt | Hệ thống (sau C1/C2) |
| `FIRST_APPROVED` (**thêm**) | A đã duyệt câu; nằm trong "phần của A" cho đến khi A gửi gói; sau khi gửi thì chờ B | A bấm Duyệt |
| `SECOND_APPROVED` (**thêm**) | B đã confirm; chờ Admin kiểm tra và import | B bấm Xác nhận (từng câu hoặc "tất cả còn lại") |
| `FINAL_APPROVED` (**đổi tên từ `APPROVED`**) | Đã vào ngân hàng, dùng cho CAT, cấm sửa (#64) | Admin bấm Import |
| `REJECTED` (đã có) | **Người** loại: A, B hoặc Admin lúc quyết lỗi mềm. Không lưu lý do (#56) | A, B, Admin |
| `AI_REJECTED` (**thêm, đề xuất**) | **Máy** loại ở C1, C2 hoặc C3; lưu mã lý do (lý do của hệ thống, khác với #56 vốn nói về lý do của người) | Hệ thống |
| ~~`PENDING_REVIEW`~~, ~~`APPROVED`~~ | **Bỏ** | — |

### 2.3. Trạng thái của lô (`item_batches.status`, đề xuất)
`GENERATING|IMPORTING` → `CHECKING` → `READY_TO_ASSIGN` → `IN_REVIEW` → `READY_TO_FINALIZE` (mọi gói đã confirm xong **hoặc** mọi hạn đã qua) → `FINAL_CHECKED` (sau khi Admin bấm Kiểm tra) → `DONE`. Lỗi: `FAILED`; hết ngân sách: `PARTIAL`.

---

## 3. Tạo đề (Admin)

### 3.1. Bằng AI (lô sinh)
Đầu vào: `skill`, `cefr_level`, `topic_tag` (tùy chọn), **N**. (Nhóm GV **chưa chọn ở bước này**, chỉ chọn lúc Giao việc, DC-41.)
Chạy nền BullMQ; Admin nhận `batchId` và xem tiến độ.

| Bước | Việc | Tốn API? |
|---|---|---|
| G1 | Lấy k = 3–5 câu mẫu cùng bộ lọc từ ngân hàng tham chiếu (few-shot); `k` cấu hình | Không |
| G2 | **Sinh dư** `N' = ⌈N × (1 + overRate)⌉`, chia thành các lời gọi nhỏ; mỗi lời gọi trả **một mảng JSON** gồm nội dung, 4 đáp án, đáp án đúng, `irt_b` gợi ý và **giải thích** | **Có** (lời gọi chính) |
| C1 | **AI check lần 1** (Mục 4.1) | Chỉ ở tầng cuối |
| G6 | **Bù thiếu:** còn ít hơn N thì sinh thêm **chỉ phần thiếu**, tối đa R vòng (cấu hình); hết R vòng ⇒ báo "thiếu x câu" | Có, nhỏ |
| G7 | Cắt về N; `irt_b` khởi tạo = trung bình `irt_b` của k mẫu, `calibrated=false`, `source=AI_GENERATED`; lưu `Explanation` | Không |

Kiểm soát chi phí: trần số lời gọi/token mỗi lô; ghi tên và phiên bản mô hình thật cho từng lời gọi (TC2.3); đi qua **LLM Gateway có dự phòng**; cache theo hash prompt; không bịa số chi phí, đo ở lần chạy thử đầu.

### 3.2. Bằng import file (Admin)
- Dùng **lưới tạm** DC-22 (tải nhiều file, dòng lỗi bị loại + popup, bấm **Lưu** mới ghi). Cột `.xlsx` (đề xuất): `Skill`, `CEFR`, `Topic`, `Câu hỏi`, `A`, `B`, `C`, `D`, `Đáp án`, `Giải thích` (tùy chọn), `Độ khó (irt_b)` (tùy chọn).
- Bấm **Lưu** ⇒ tạo lô `source=IMPORTED`, chạy **C2** (Mục 4.2) trên các dòng trong lưới, rồi cùng luồng sau đó.
- Dòng thiếu giải thích ⇒ sinh theo nhóm một lượt (chỉ dòng thiếu).

---

## 4. AI check — ba điểm, mỗi điểm một cách tối ưu

**Nguyên tắc chung (lý do thiết kế):**
1. **Rẻ trước, đắt sau:** bộ lọc không tốn API (luật cứng, băm, `pg_trgm`) chạy trước; embedding và lời gọi AI chỉ chạy cho câu còn sống sót.
2. **Gộp nhiều câu vào một lời gọi AI**, không gọi từng câu.
3. **Không tính lại điều đã biết:** mỗi câu có `content_hash` (chuẩn hóa nội dung + đáp án + giải thích). Kết quả check gắn với hash; hash không đổi thì **tái sử dụng**, kể cả ở lần 3.
4. **Embedding tính đúng một lần cho mỗi nội dung**, lưu `item_embeddings`.
5. Mỗi lần check ghi **báo cáo có mã lý do**, để Admin hiểu và để hiệu chỉnh ngưỡng.

### 4.1. C1 — sau khi AI sinh (đầu vào chưa đáng tin, lọc nặng nhất)
Lý do làm đầy đủ ở đây: câu hỏng loại sớm nhất tiết kiệm được **toàn bộ** thời gian của A và B, và đây là lần duy nhất ta có số câu dư để loại thoải mái.

| Tầng | Việc | Tốn API | Kết quả |
|---|---|---|---|
| 1. Luật cứng | Đủ 4 đáp án khác nhau, đúng 1 đáp án đúng, độ dài hợp lệ, `irt_b` ∈ [−4,+4], đúng `skill`/`cefr`, có giải thích | Không | Hỏng ⇒ `AI_REJECTED` |
| 2. Trùng T1 | Băm chuẩn hóa so với: ngân hàng, câu đang trong mọi lô khác, các câu cùng lô | Không | Trùng ⇒ `AI_REJECTED` |
| 3. Trùng T2 | `pg_trgm` trên nội dung + đáp án | Không | ≥ ngưỡng cao: `AI_REJECTED`; giữa hai ngưỡng: **cờ mềm** |
| 4. Trùng T3 | Embedding (chỉ câu còn lại), cosine tính trong ứng dụng | **Có** (embedding) | ≥ ngưỡng: **cờ mềm** kèm câu bị nghi trùng |
| 5. G5 | Kiểm đáp án độc lập: đưa câu + 4 đáp án (không kèm đáp án đúng) cho AI tự chọn; cùng lời gọi hỏi "giải thích có ủng hộ đáp án vừa chọn không" | **Có** (gộp nhóm) | Lệch ⇒ **cờ mềm** (không loại: AI có thể sai, người sẽ xem) |

### 4.2. C2 — khi Admin import file có sẵn (đầu vào do người soạn, chưa biết đáp án có đúng không)
Khác C1: **không sinh dư, không bù thiếu** (câu do người đưa vào, không loại số lượng bừa); **luôn có kiểm trùng nội bộ file/lưới**. Vẫn chạy đủ tầng 1–5 vì nguồn file chưa được máy kiểm; nhưng:
- Tầng 1: thêm kiểm **cột bắt buộc, kiểu dữ liệu, giá trị CEFR/Skill hợp lệ**; dòng sai ⇒ không vào lưới, popup lý do (khác C1: ở đây lỗi hiện **ngay trên lưới**, chưa lưu).
- Tầng 2–4 (trùng): chạy **ngay lúc tải file lên lưới** để Admin thấy sớm; trùng với dòng đã có trong lưới ⇒ bỏ qua (DC-22).
- Tầng 5 (G5): chạy **một lần khi bấm Lưu**, không chạy mỗi lần tải thêm file (tiết kiệm API).
- Giải thích thiếu ⇒ sinh bổ sung theo nhóm.

### 4.3. C3 — trước `FINAL_APPROVED`: Admin bấm **Kiểm tra**
Chỉ chạy được khi lô ở `READY_TO_FINALIZE` (DC-44). **Mục tiêu khác C1:** không lọc chất lượng ban đầu mà **bắt các hỏng hóc xảy ra sau khi người can thiệp** và **bắt xung đột với ngân hàng đã thay đổi trong lúc lô chờ**. Vì vậy chạy **theo thay đổi (delta)**:

| Kiểm | Chạy trên | Cách tiết kiệm | Loại lỗi |
|---|---|---|---|
| Luật cứng (tầng 1) | **Mọi** câu `SECOND_APPROVED` | Không tốn API | Cứng |
| Toàn vẹn quy trình | Mọi câu | Không tốn API: A ≠ B, gói đủ, mọi câu có người duyệt và người confirm, trạng thái đi đúng chiều | Cứng |
| Trùng T1–T2 | Mọi câu, so với **ngân hàng hiện tại** (có thể có câu mới vào từ lô khác) và các câu cùng lô | Không tốn API | Cứng (T1, T2 ≥ ngưỡng cao); mềm (giữa hai ngưỡng) |
| Trùng T3 | Câu **đã đổi hash**, hoặc câu chưa có embedding; còn lại chỉ so với các câu ngân hàng **mới thêm kể từ lần check trước** (so theo thời điểm) | Embedding đã lưu, cosine trong ứng dụng | Mềm |
| G5 + giải thích khớp | **Chỉ câu mà A đã sửa** (hash khác hash lúc qua C1/C2) | Câu không sửa dùng lại kết quả lần trước; gộp nhóm | Mềm |
| Thống kê | — | — | Báo cáo: số câu A sửa, tỷ lệ A/B loại |

**Vì sao delta:** sau C1/C2, phần lớn câu **không đổi** nên không cần tốn AI lần nữa; hỏng hóc chỉ có thể sinh ra từ **(a) A sửa nội dung** và **(b) ngân hàng thay đổi**, và hai thứ này phát hiện được rẻ bằng so hash và so theo thời điểm.

**Kết quả C3 hiển thị cho Admin:** bảng theo câu (qua / cờ mềm / lỗi cứng, mã lý do, câu bị nghi trùng, bản gốc so với bản đã sửa), tổng hợp theo gói. **Import bị khóa** cho đến khi có báo cáo C3 còn hiệu lực (không câu nào đổi và ngân hàng không đổi kể từ lúc kiểm); nếu đổi, hệ thống yêu cầu kiểm lại phần chênh. Lúc bấm Import, hệ thống vẫn chạy lại **T1–T2 nhanh** để chặn tranh chấp (hai Admin import cùng lúc).

### 4.4. Xử lý câu rớt C3 (AI đề xuất theo ủy quyền của bạn, **chờ xác nhận**)

| Phương án | Ưu | Nhược |
|---|---|---|
| O1. Mọi câu rớt tự `AI_REJECTED` | Đơn giản, chặt | Loại nhầm câu chỉ bị cờ nhẹ; lãng phí công của A và B |
| **O2. Lỗi cứng tự `AI_REJECTED`; lỗi mềm hiện cho Admin quyết (Import hoặc Loại)** (**đề xuất**) | Lỗi cứng là khách quan (cấu trúc, trùng gần như giống hệt) không cần phán đoán; lỗi mềm mang tính phán đoán, người đã xem hai lần, Admin chịu trách nhiệm cuối; không cần đường quay lại | Admin phải đọc các câu mềm |
| O3. Trả lại A để sửa | Cứu được câu | Mở lại vòng lặp (đảo #109), cần hạn và theo dõi, dễ kéo dài vô hạn |

Chọn **O2** vì: (1) giữ luồng một chiều như bạn đã chốt ở #109; (2) không dồn phán đoán chủ quan cho máy; (3) Admin không sửa nội dung nên không phá tính độc lập. Câu bị cờ mềm mà Admin chọn Import vẫn ghi lại "Admin chấp nhận cờ" để truy vết.

---

## 5. Giao việc (assign)

**Điều kiện:** lô ở `READY_TO_ASSIGN` (đã qua C1/C2); Admin xem được số câu còn lại, danh sách "AI đã loại" (Mục 7) và cờ mềm.

**Các bước Admin:**
1. Bấm **Giao việc**. Chọn **nhóm A** (một hoặc nhiều GV, khuyên ≥ 2 để chia việc), chọn **GV B** (một người, **không được nằm trong nhóm A**, vi phạm ⇒ `409`).
2. Đặt hạn: **`reviewDays`** (hạn cho A, tính từ ngày giao) và **`confirmDays`** (hạn cho B, tính từ ngày mỗi gói được gửi). Mỗi số ≥ 1.
3. Hệ thống hiện **xem trước phân bổ** (bảng GV – số câu, theo từng kỹ năng/CEFR); Admin bấm **Xác nhận giao**.

**Cách chia đều (nhóm A):** sắp xếp các câu `DRAFT` theo (`skill`, `cefr`, thứ tự sinh); câu thứ i giao cho A thứ `i mod M` (M = số GV A). Nhờ sắp theo (`skill`, `cefr`) trước, mỗi GV nhận **mức trộn đều** các loại câu. Số câu mỗi GV chênh nhau tối đa 1 (100 câu / 5 GV = 20; 103 câu: 3 người 21, 2 người 20).

**Sau khi giao:** tạo `item_review_assignments` (mỗi câu một dòng, assignee A, `assigned_at`, `due_at`); lô `IN_REVIEW`; A nhận thông báo (trong ứng dụng, email tùy chọn) "Bạn có x câu cần duyệt, hạn dd/mm"; đặt lịch nhắc (Mục 6.3).

**Giao lại:** Admin chuyển các câu chưa xử lý của một A cho A khác (hoặc đổi B của gói chưa gửi/chưa xử lý), với ràng buộc B ∉ nhóm A; hạn tính lại từ ngày giao lại; ghi kiểm toán.

---

## 6. Quy trình GV A, gói, GV B, và sau confirm

### 6.1. GV A duyệt
1. A mở "Hộp việc → Cần duyệt": **chỉ thấy câu giao cho mình**, kèm cờ mềm, giải thích, hạn còn lại.
2. Với mỗi câu A được **sửa** nội dung/đáp án/giải thích, rồi chọn **Duyệt** (`FIRST_APPROVED`) hoặc **Từ chối** (`REJECTED`, không lưu lý do).
3. Sau mỗi lần sửa, hệ thống chạy lại **luật cứng + T1–T2** trên bản sửa (rẻ); hỏng/trùng ⇒ chặn Duyệt, báo lý do.
4. Khi **mọi câu giao cho A đã có quyết định** (Duyệt hoặc Từ chối), A bấm **Gửi cho B** ⇒ tạo **gói** gồm các câu `FIRST_APPROVED` của A (câu A loại **không** vào gói). A không bấm gửi được khi còn câu chưa quyết.
5. A gửi **một lần**; sau khi gửi, A không sửa lại các câu trong gói.

### 6.2. GV B confirm
1. B mở "Hộp việc → Cần confirm": thấy **từng gói** (một gói/mỗi A), chỉ đọc. Mỗi câu hiện cờ và dấu **"A đã sửa"** kèm bản gốc so với bản sửa.
2. B xử lý **từng câu: Xác nhận** (`SECOND_APPROVED`) **hoặc Loại bỏ** (`REJECTED`), hoặc bấm **"Xác nhận tất cả câu còn lại"** (xác nhận hết câu chưa quyết trong gói; ghi log hành động hàng loạt).
3. B **không sửa**, **không trả về** A (DC-33). B ≠ A đã bảo đảm lúc giao.
4. Gói xong khi mọi câu trong gói có quyết định; gói `DONE`.

### 6.3. Hạn và nhắc
- **A:** `due_at` = cuối ngày (ngày giao + `reviewDays`). **B:** mỗi gói `due_at` = cuối ngày (ngày gửi gói + `confirmDays`) (đề xuất, vì gói đến B vào các thời điểm khác nhau; hỏi ở Q-3). Giờ chốt 23:59:59 giờ Việt Nam (cấu hình) — **đề xuất, chờ bạn xác nhận**.
- **Admin chỉnh hạn** (cả `reviewDays`, `confirmDays`; chỉ áp dụng cho việc chưa xử lý) ⇒ tính lại `due_at`, hủy và tạo lại lịch nhắc.
- **Nhắc:** job trễ BullMQ chạy lúc `due_at − 24 giờ`, nếu nhóm (lô, bước, GV, gói) còn việc chưa xong thì gửi **một** thông báo gộp (trong ứng dụng + email `MailPort`); hạn còn < 24 giờ lúc giao/chỉnh ⇒ nhắc ngay một lần (đề xuất); kèm đối chiếu lazy khi mở hộp việc phòng mất job.
- **Quá hạn:** chỉ hiển thị "quá hạn" cho Admin và GV (tính lazy), **không tự đổi trạng thái hay tự giao lại**. Admin chọn: chỉnh hạn, giao lại, hoặc ép gửi gói hiện có thay A (đề xuất, Q-2).

### 6.4. Sau khi B confirm
1. Câu `SECOND_APPROVED` nằm chờ trong lô. **Chưa** vào ngân hàng.
2. Khi **mọi gói đã `DONE` hoặc mọi hạn đã qua** ⇒ lô `READY_TO_FINALIZE`. Admin thấy thống kê: bao nhiêu câu `SECOND_APPROVED`, `REJECTED` bởi A/B, `AI_REJECTED`, chưa xử lý.
3. Admin bấm **Kiểm tra** (C3, Mục 4.3), đọc báo cáo, xử lý lỗi mềm.
4. Admin bấm **Import** ⇒ các câu qua (và lỗi mềm Admin chấp nhận) thành `FINAL_APPROVED`, ghi `approved_by`, `approved_at`; câu có hiệu lực cho CAT, `calibrated=false`.
5. Câu **chưa xử lý** khi quá hạn (còn `DRAFT` hoặc `FIRST_APPROVED` chưa tới B) **không** được import; nằm lại trong lô, Admin giao lại với hạn mới hoặc loại. Lô `DONE` khi mọi câu ở trạng thái cuối (`FINAL_APPROVED`, `REJECTED`, `AI_REJECTED`).

---

## 7. Câu bị loại sống ở đâu

| Loại bởi | Trạng thái | Lưu gì | Ai xem | Dùng lại? |
|---|---|---|---|---|
| Máy ở C1, C2, C3 | `AI_REJECTED` | Nội dung + **mã lý do** + câu bị nghi trùng (nếu có) | Chỉ Admin (tab "AI đã loại") | Không; Admin dùng để chỉnh ngưỡng. Dọn sau N ngày (cấu hình) |
| GV A hoặc GV B | `REJECTED` | Nội dung; **không lưu lý do** (#56) | Admin (danh sách và thống kê theo GV) | Không; Admin muốn bù thì tạo lô mới |
| Admin (lỗi mềm ở C3) | `REJECTED` | Như trên | Admin | Không |

Câu `AI_REJECTED` **không** được đưa cho GV. Thống kê bắt buộc: tỷ lệ loại theo tầng AI, theo A, theo B, để hiệu chỉnh.

---

## 8. Giải thích

Giải thích sinh **cùng lời gọi** G2, lưu `explanations` gắn `Item` (#63). A xem và sửa; B chỉ xem; C1 tầng 5 và C3 kiểm giải thích khớp đáp án. Câu import thiếu giải thích: sinh bổ sung theo nhóm. Phải sửa tài liệu còn ghi "lazy": `CLAUDE.md`, `Tuan2/Phuong_an_sua_doi_AI.md` mục 1.4.

---

## 9. Luồng chi tiết (cơ sở cho Sequence Diagram, UC, test)

Ký hiệu: **A**=GV duyệt, **B**=GV confirm, **Ad**=Admin, **H**=hệ thống.

**L-1. Tạo lô bằng AI (UCADM11).** Ad nhập skill, CEFR, topic, N ⇒ H kiểm giới hạn, tạo lô (`GENERATING`), đẩy job ⇒ Worker: G1 → G2 → **C1** → G6 → G7 ⇒ lô `READY_TO_ASSIGN` (hoặc `PARTIAL`/`FAILED`) ⇒ thông báo Ad. Mỗi lời gọi ghi mô hình, token.
**L-2. Tạo lô bằng import file (UCADM12, đề xuất).** Ad tải một hoặc nhiều file vào lưới (C2 tầng 1–4 chạy ngay) ⇒ xem lưới/popup ⇒ **Lưu** ⇒ H tạo lô `IMPORTED`, chạy C2 tầng 5 ⇒ `READY_TO_ASSIGN`.
**L-3. Xem kết quả và giao việc (UCADM13, đề xuất).** Ad xem số câu qua, danh sách AI đã loại, cờ ⇒ **Giao việc** (chọn A, B, `reviewDays`, `confirmDays`) ⇒ xem trước phân bổ ⇒ xác nhận ⇒ H tạo assignment, lô `IN_REVIEW`, thông báo và đặt lịch nhắc.
**L-4. A duyệt và gửi gói (UCGV14).** A sửa/duyệt/từ chối từng câu (H kiểm lại cứng + T1–T2 sau sửa) ⇒ khi hết việc, **Gửi cho B** ⇒ tạo gói, `due_at` của gói, nhắc cho B.
**L-5. B confirm (UCGV15).** B mở gói ⇒ xử lý từng câu hoặc "xác nhận tất cả còn lại" ⇒ gói `DONE`.
**L-6. Theo dõi, chỉnh hạn, giao lại.** Ad xem tiến độ theo gói/GV, chỉnh hạn, giao lại, ép gửi gói thay A.
**L-7. Kiểm tra và import (UCADM14, đề xuất).** Lô `READY_TO_FINALIZE` ⇒ Ad bấm **Kiểm tra** (C3) ⇒ xem báo cáo ⇒ quyết lỗi mềm ⇒ **Import** (H chạy lại T1–T2 nhanh) ⇒ `FINAL_APPROVED`.
**L-8. Quá hạn.** Hiển thị, không tự đổi; Ad xử lý như L-6.

### Bảng quyền

| Hành động | Admin | GV A (đúng người) | GV B (đúng người) | GV khác | SV |
|---|---|---|---|---|---|
| Tạo lô AI, import file, giao việc, giao lại, chỉnh hạn, Kiểm tra, Import, quyết lỗi mềm | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sửa nội dung, Duyệt/Từ chối, Gửi gói | ❌ | ✅ câu của mình | ❌ | ❌ | ❌ |
| Xác nhận/Loại, "xác nhận tất cả còn lại" | ❌ | ❌ | ✅ gói gửi cho mình | ❌ | ❌ |
| Xem "AI đã loại" và thống kê | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 10. Dữ liệu, API, mã lỗi (đề xuất)

**Schema:**
- `ItemStatus`: `DRAFT`, `FIRST_APPROVED`, `SECOND_APPROVED`, `FINAL_APPROVED`, `REJECTED`, `AI_REJECTED`; bỏ `PENDING_REVIEW`, `APPROVED`. `ItemSource`: `AI_GENERATED`, `IMPORTED`.
- `item_batches` (id, source, createdBy, skill, cefrTarget, topicTag, requestedCount, `status`, createdAt). Hạn `review_days`/`confirm_days` chỉ có khi đã giao ⇒ đặt ở bảng `item_batch_assignments` (batchId, reviewDays, confirmDays, confirmerId) để tránh cột trống.
- `item_review_assignments` (itemId, assigneeId, `assigned_at`, `due_at`, `reminder_sent`, UNIQUE(itemId)).
- `item_packages` (id, batchId, reviewerId, confirmerId, `status` `OPEN|SENT|DONE`, `due_at`, `reminder_sent`).
- `items.content_hash`, `items.batch_id`, `items.package_id` (khi vào gói), `item_embeddings` (itemId, vector `Float[]`, model, createdAt), `item_check_results` (itemId, checkpoint `C1|C2|C3`, content_hash, level `PASS|SOFT|HARD`, reason_codes, checkedAt).
- `item_review_events` (tùy chọn, truy vết): `APPROVE|REJECT|CONFIRM|REMOVE|CONFIRM_ALL|IMPORT|REASSIGN|EXTEND|FORCE_SEND|ACCEPT_FLAG`.
- Chỉ mục: băm chuẩn hóa (T1), GIN `pg_trgm` (T2). `CREATE EXTENSION pg_trgm`.

**API:**

| Nhóm | Endpoint | Role |
|---|---|---|
| Lô | `POST /item-batches` (AI), `POST /item-imports/upload`, `GET`/`DELETE /item-imports/grid[/:rowKey]`, `POST /item-imports/save`, `GET /item-batches[/:id]`, `GET /item-batches/:id/ai-rejected` | Admin |
| Giao việc | `POST /item-batches/:id/assign` `{reviewerIds, confirmerId, reviewDays, confirmDays}`, `GET /item-batches/:id/assign-preview`, `POST /item-batches/:id/reassign`, `PATCH /item-batches/:id/deadlines`, `POST /item-packages/:id/force-send` | Admin |
| Kiểm tra / import | `POST /item-batches/:id/final-check`, `GET /item-batches/:id/final-check`, `POST /item-batches/:id/import`, `POST /items/:id/decision` (chấp nhận hoặc loại lỗi mềm) | Admin |
| Chặng A | `GET /me/review-tasks`, `PATCH /items/:id`, `POST /items/:id/approve`, `POST /items/:id/reject`, `POST /item-packages/mine/send` | GV A |
| Chặng B | `GET /me/confirm-packages`, `POST /items/:id/confirm`, `POST /items/:id/remove`, `POST /item-packages/:id/confirm-all` | GV B |

**Mã lỗi:** `NOT_ASSIGNED` (403), `CONFIRMER_IN_REVIEW_GROUP` (409), `PACKAGE_INCOMPLETE` (409: A chưa quyết hết câu), `FINAL_CHECK_REQUIRED` (409), `FINAL_CHECK_STALE` (409), `BATCH_NOT_READY_TO_FINALIZE` (409), `DUPLICATE_AFTER_EDIT` (422), `INVALID_AFTER_EDIT` (422), `BATCH_BUDGET_EXCEEDED` (409), `IMPORT_GRID_EXPIRED` (410).

---

## 11. Tác động tài liệu và mã (nợ đồng bộ)

- **Đổi tên `APPROVED` → `FINAL_APPROVED`:** lọc của CAT (`selectNextItem()`), seed, SRS v3.0, `CLAUDE.md`, Class Diagram, schema, UC spec, mã BE hiện có (`item-bank`, `cat-engine`). Chưa sửa gì.
- **Use Case (ID đề xuất):** `UCADM11` Tạo lô AI, `UCADM12` Import đề (lưới tạm), `UCADM13` Giao việc và theo dõi, `UCADM14` Kiểm tra và import cuối; `UCGV14` Duyệt và gửi gói (A), `UCGV15` Confirm gói (B). Bỏ UCGV03 và UCGV05 cũ; sửa UCGV02/04/06 theo quyền mới. DC-18 viết lại.
- **Class:** `ItemBatch`, `ItemPackage`, `ItemReviewAssignment`, `ItemCheckResult`, `ItemGenerationService`, `ItemCheckService` (3 checkpoint), `ItemDuplicateChecker` (+ `DuplicateStrategy`), `ReviewDistributionService`, `DeadlineReminderService`.
- **Sequence mới:** sinh lô + C1; import + C2; giao việc; A duyệt và gửi; B confirm; Kiểm tra + import.
- **Màn hình (ID từ S26):** Admin: tạo lô, lưới import, giao việc, chi tiết lô và tiến độ, "AI đã loại", Kiểm tra và Import; GV: hộp việc A, màn duyệt, hộp việc B, màn gói.
- **SRS:** F-ID mới, III module `item-generation`, VI/VIII DDL, X API, XIV Risk (phạm vi; chi phí API; Admin là điểm tập trung), `COMMITMENT_BASELINE.md`.

---

## 12. Câu hỏi còn mở (chưa tự quyết)

| Mã | Câu hỏi | Đề xuất của AI |
|---|---|---|
| Q-1 | **Xác nhận O2** cho câu rớt C3 (Mục 4.4): lỗi cứng tự `AI_REJECTED`, lỗi mềm Admin quyết | O2 |
| Q-2 | Quá hạn: câu chưa xử lý nằm lại lô và Admin xử lý thủ công (giao lại, ép gửi, loại) | Đúng như Mục 6.3, 6.4 |
| Q-3 | Hạn của B tính từ **ngày gói được gửi** (đề xuất) hay từ ngày Admin giao việc? | Từ ngày gửi gói |
| Q-4 | Giờ chốt "ngày hạn" 23:59:59 giờ Việt Nam; nhắc ngay nếu hạn < 24 giờ lúc giao | Như đề xuất |
| Q-5 | Giới hạn: số GV tối thiểu nhóm A (1 hay ≥2); giới hạn kích thước gói; Admin có bắt buộc chọn B trước khi giao không | A ≥ 1; B bắt buộc |
| Q-6 | Tên trạng thái phụ `AI_REJECTED` và `IMPORTED` (đổi từ `MANUAL`) | Như đề xuất |
| Q-7 | Các ngưỡng/tham số: `overRate`, cỡ mỗi lời gọi, ngưỡng T2 và T3 (cứng, mềm), số vòng bù R, trần lời gọi mỗi lô, số ngày dọn `AI_REJECTED` | Đặt trong cấu hình; hiệu chỉnh sau thử nghiệm nhỏ |
| Q-8 | Nguồn ngân hàng tham chiếu cho few-shot và **điều khoản bản quyền** phân phối lại cho SV | Kiểm bộ Tuần 3 (CEFR-J, CLOTH); hỏi GVHD nếu cần |
| Q-9 | **Mô hình embedding**, hạn mức, chi phí: chưa kiểm chứng | Xác minh trong tài liệu nhà cung cấp, qua LLM Gateway, trước khi code |
| Q-10 | `pg_trgm` bật được trên image Postgres staging không | Kiểm sớm; nếu không thì T2 tính trong ứng dụng |
| Q-11 | Phạm vi và thời gian: sinh đề AI nay vào TL, làm đủ T3 và G5 | Cập nhật `COMMITMENT_BASELINE.md` trước khi ký; ghi rủi ro trễ |
| Q-12 | Khoảng `irt_b` −4…+4 khác `CLAUDE.md`: sửa `CLAUDE.md` và kiểm tác động chọn câu CAT | Sửa `CLAUDE.md`, kiểm test CAT |

---

## 13. Ca test bắt buộc (khi code)

- **Giao việc:** 100 câu / 5 GV A ⇒ 20 mỗi người; 103 ⇒ chênh tối đa 1; mỗi A nhận mức trộn đều skill/CEFR; B nằm trong nhóm A ⇒ `409`; thiếu B ⇒ lỗi.
- **Gói:** A chưa quyết hết câu mà bấm Gửi ⇒ `PACKAGE_INCOMPLETE`; câu A loại không vào gói; nhiều A ⇒ nhiều gói độc lập; B chỉ thấy gói gửi cho mình.
- **B:** Xác nhận/Loại từng câu; "xác nhận tất cả còn lại" chỉ ảnh hưởng câu chưa quyết; gọi API sửa hoặc "trả về" ⇒ lỗi.
- **Kiểm tra C3:** câu không đổi dùng lại kết quả; câu A sửa bị chạy lại G5; có câu mới vào ngân hàng trong lúc chờ ⇒ T1–T2 bắt trùng; lỗi cứng ⇒ `AI_REJECTED`; lỗi mềm ⇒ Admin quyết, ghi `ACCEPT_FLAG`; sửa/đổi sau khi kiểm ⇒ `FINAL_CHECK_STALE`.
- **Import:** chỉ khi lô `READY_TO_FINALIZE` (mọi gói `DONE` hoặc mọi hạn qua) và C3 còn hiệu lực; câu chưa xử lý không được import; hai Admin import cùng lúc không tạo trùng.
- **Lọc trùng:** giống hệt (T1), gần giống chữ (T2), diễn đạt lại (T3 cảnh báo), trùng giữa hai file trong lưới, trùng với câu đang chờ ở lô khác.
- **Trạng thái:** chỉ `FINAL_APPROVED` được CAT chọn; `FINAL_APPROVED` không sửa; chuyển trạng thái chỉ đi một chiều.
- **Hạn và nhắc:** hạn = ngày giao (hoặc ngày gửi gói) + số ngày; Admin đổi số ngày ⇒ hạn việc chưa xử lý đổi theo; nhắc đúng 24 giờ trước hạn, mỗi nhóm một lần, không nhắc khi đã xong; hạn < 24 giờ lúc giao ⇒ nhắc ngay.
- **Quyền:** GV chỉ thấy câu/gói của mình; GV thường gọi API Admin ⇒ 403; GV không import (UC bỏ).
- **Chi phí:** vượt trần lời gọi/token ⇒ dừng và báo; cùng prompt không gọi lại; Gateway chuyển nhà cung cấp khi hết hạn mức (nhà cung cấp giả khi test).
- **Khoảng `irt_b`:** −4 và +4 hợp lệ, ngoài biên bị loại.

## 14. Bước tiếp theo

1. Bạn trả lời Q-1…Q-12 (ít nhất Q-1, Q-3, Q-5, Q-11).
2. Ghi các điều chốt thêm vào `DECISIONS_LOG`; tạo `feature-plans/ai-item-generation.md` đầy đủ.
3. Đồng bộ tài liệu theo Mục 11 (cả đổi tên `APPROVED`).
4. Thử nghiệm nhỏ trước khi code đầy đủ: sinh một lô nhỏ, đo tỷ lệ loại theo tầng, chi phí và độ trễ thật.
