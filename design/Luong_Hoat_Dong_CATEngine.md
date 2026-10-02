# LUỒNG HOẠT ĐỘNG CHI TIẾT — CAT ENGINE (Bắt đầu → Kết thúc bài thi)

**Tài liệu tham chiếu:** `SRS_TLCN (3).md` Mục 4.1–4.5, 6.3, VII, 15.5; `Mo_ta_So_do_Lop_ClassDiagram.md` mục 5–11.
**Quyết định thiết kế áp dụng trong tài liệu này:** xem `tracking/feature-plans/f03-cat-engine.md` Mục 3 — quy tắc chọn skill là **Round-robin cố định** (Vocabulary/Grammar xen kẽ), do người dùng chốt ngày 2026-09-14 vì mô hình hiện tại là **unidimensional** (1 θ chung, không có SE riêng theo từng skill).

---

## I. TRẢ LỜI 3 CÂU HỎI GỐC

### 1. Tham số `skill` trong `findForCAT` là gì?

`skill` là **một giá trị cụ thể** trong 2 giá trị `'vocabulary' | 'grammar'` (Tiểu luận chỉ có 2 skill — SRS Mục 6.3: Item Bank có 160 câu Vocabulary + 120 câu Grammar = 280 câu). Nó **không phải** "tập các kỹ năng trường cần đánh giá" — nó là filter SQL cho **đúng 1 lần gọi `findForCAT`**, xác định "lần này tìm câu thuộc skill nào".

Vì mô hình Rasch 1PL hiện tại chỉ có **một θ chung** cho cả bài thi (không tách θ riêng theo skill — xem SRS Mục 4.1), nên **không có điều kiện dừng riêng theo skill**. Việc phân bổ số câu đều giữa 2 skill được đảm bảo bằng cách **luân phiên (round-robin)** khi chọn skill cho câu tiếp theo, không phải bằng cách so sánh SE giữa các skill.

### 2. `findForCAT` dùng kỹ thuật gì, và được gọi khi nào?

- **Kỹ thuật:** SQL 2 bước (SRS Mục 4.4):
  1. Lọc `WHERE status='APPROVED' AND skill=$1 AND id != ALL(usedIds)`, sắp theo `ABS(irt_b - currentTheta)` tăng dần, `LIMIT 5` → ra **Top-5 câu gần θ hiện tại nhất** thuộc đúng skill được chọn.
  2. `ORDER BY RANDOM() LIMIT 1` trên 5 câu đó → chọn ngẫu nhiên đều 1 câu (mỗi câu 20% cơ hội).
- **Khi nào được gọi:** **Mỗi lần cần câu mới**, không phải 1 lần lúc bắt đầu session. Xác nhận qua SRS Mục 15.5 (Redis State Machine): mỗi lần SV gọi `GET /next-item` mà `state == READY_FOR_NEXT`, hệ thống chạy lại `CATEngine` với **θ hiện tại** (đã cập nhật từ câu trước) để tìm câu mới. Nếu `state == WAITING_FOR_ANSWER` (SV bấm refresh/spam), trả lại câu cũ, **không** gọi lại `findForCAT`.

### `selectNextItem(session, pool)` hoạt động thế nào? (đầy đủ)

```
CATEngine.selectNextItem(session, pool):
  1. skill = pickNextSkill(session.itemsAdministered)   // round-robin, xem Mục II
  2. candidates = ItemBank.findForCAT(skill, session.usedIds, session.theta)  // Top-5 + random 1 câu
  3. return candidates   // 1 Item cụ thể
```

`pool` trong tên hàm `selectNextItem(session, pool)` (ghi trong Class Diagram) chính là **kết quả của `findForCAT`** — không phải toàn bộ Item Bank, mà là Top-5 câu đã lọc theo skill + độ khó + chưa dùng.

### 3. Class/phương thức nào tính lại θ, SE và chủ động dừng bài?

| Việc | Class.phương thức | Input | Output |
|---|---|---|---|
| Tính lại θ, SE sau mỗi câu | **`CATEngine.computeEAP(responses[])`** | Toàn bộ lịch sử `{b_i, isCorrect}` của session tới hiện tại | `AbilityEstimate {theta, standardError, confidenceInterval95}` |
| Quyết định có nên dừng không | **`CATEngine.checkStoppingCriterion(session)`** | `session` (có θ, SE, số câu đã hỏi, thời gian bắt đầu) | `{shouldStop: boolean, reason: StoppingReason}` |
| **Thực thi** việc dừng (đổi trạng thái, tạo hồ sơ) | **`TestSession.submitResponse()` → `TestSession.computeResult()`** | — | Cập nhật `status = COMPLETED`, gọi `LanguageProfile.generateFromSession()` |

Điểm quan trọng: `CATEngine` chỉ **quyết định** (trả về tín hiệu dừng), **không tự** đổi trạng thái `TestSession` hay tạo `LanguageProfile` — đúng với nguyên tắc `<<service>>` không sở hữu dữ liệu (xem `Mo_ta_So_do_Lop_ClassDiagram.md` mục 6, phần "Liên kết"). `TestSession` là nơi **thực thi** hành động dựa trên tín hiệu đó.

---

## II. QUY TẮC CHỌN SKILL — `pickNextSkill()` (Round-robin, random skill bắt đầu)

> **Quyết định #2** (xem `tracking/feature-plans/f03-cat-engine.md` Mục 3): skill cho **câu đầu tiên** được chọn **random 50/50**, không cố định Vocabulary hay Grammar — vì SRS không quy định và người dùng cho rằng thứ tự bắt đầu "không quan trọng". Từ câu 2, alternate cố định dựa trên skill đã ra ở câu 1 (không phải đếm chẵn/lẻ đơn giản, vì điểm bắt đầu là random).

```
pickNextSkill(session): Skill
  if session.lastSkillPicked == null:
    skill = randomChoice(['vocabulary', 'grammar'])   // random 50/50 — CHỈ xảy ra ở câu 1
  else:
    skill = (session.lastSkillPicked == 'vocabulary') ? 'grammar' : 'vocabulary'  // alternate

  session.lastSkillPicked = skill   // ghi lại vào SessionCacheState (Redis) để lượt sau dùng
  return skill
```

`lastSkillPicked` là field **mở rộng thêm vào `SessionCacheState`** (không có trong Redis Key Schema gốc của SRS Mục "Redis Key Schema" — vì round-robin bản thân cũng là quyết định ngoài SRS). Field này do `CATEngine.pickNextSkill(session)` đọc/ghi trên `session`, **không** lưu trong `CATEngine` — giữ đúng nguyên tắc `<<service>>` không giữ state (xem `Mo_ta_So_do_Lop_ClassDiagram.md` mục 6).

Với bài thi dừng ở số câu lẻ (vd dừng ở câu 15), skill ra ở **câu 1** sẽ luôn có 1 câu nhiều hơn skill còn lại — nhưng skill nào là skill đó thì **khác nhau giữa các session** (do random ở câu 1), không cố định luôn là Vocabulary như một bản nháp trước đó của tài liệu này.

---

## III. LUỒNG HOẠT ĐỘNG ĐẦY ĐỦ — TỪ BẮT ĐẦU ĐẾN KẾT THÚC

### Bước 0 — Bắt đầu bài thi

| | |
|---|---|
| **Gọi bởi** | Sinh viên nhấn "Bắt đầu thi" |
| **Class.phương thức** | `TestSession.start(studentId)` |
| **Nhận** | `studentId` |
| **Làm gì** | Tạo record `TestSession` mới: `status='IN_PROGRESS'`, `startedAt=now()`. Khởi tạo `SessionCacheState` trên Redis: `theta=-0.5` (`thetaInit`), `se=null` (chưa có ước lượng), `itemsAdministered=[]`, `lastSkillPicked=null`, `state='READY_FOR_NEXT'`. |
| **Trả về** | `sessionId` |
| **Ai xử lý tiếp** | Client gọi `GET /next-item` với `sessionId` này |

### Bước 1 — Lấy câu hỏi đầu tiên

| | |
|---|---|
| **Gọi bởi** | Client `GET /next-item` |
| **Class.phương thức** | `TestSession.getNextItem()` → delegate `CATEngine.selectNextItem(session, pool)` |
| **Nhận** | `session` (theta=-0.5, itemsAdministered=[], usedIds=[]) |
| **Làm gì** | 1. `pickNextSkill(session)` → `lastSkillPicked=null` → **random 50/50** → giả sử ra **`vocabulary`** (ghi lại `lastSkillPicked='vocabulary'` vào `SessionCacheState`).<br>2. `ItemBank.findForCAT('vocabulary', [], -0.5)` → SQL lọc Vocabulary APPROVED, sắp theo `\|b - (-0.5)\|`, lấy Top-5.<br>3. Random 1 câu trong Top-5. |
| **Trả về** | 1 `Item` (không kèm đáp án đúng) |
| **Ai xử lý tiếp** | `SessionCacheState` cập nhật `current_item_id`, `state='WAITING_FOR_ANSWER'`; câu hỏi hiển thị cho SV |

**Ví dụ số liệu:** Giả sử `pickNextSkill()` random ra `vocabulary` cho câu 1 (một session khác có thể ra `grammar` — đây là random, không cố định). Item Bank Vocabulary có các câu với `irt_b` gần `-0.5`: `[-0.75, -0.60, -0.45, -0.30, -0.55]` (Top-5 sau khi sắp theo khoảng cách). Random chọn được câu **V-102** (`b = -0.45`).

### Bước 2 — Sinh viên trả lời câu 1

| | |
|---|---|
| **Gọi bởi** | Client `POST /responses {item_id: 'V-102', response: 'B'}` |
| **Class.phương thức** | `TestSession.submitResponse(itemId, response)` |
| **Nhận** | `itemId='V-102'`, `response='B'` |
| **Làm gì** | 1. Guard: `itemId` phải khớp `current_item_id` trong Redis (chống double-submit — SRS 15.5).<br>2. Tra `Item.correctAnswer` của V-102 → so sánh → `isCorrect = true` (giả sử SV trả lời đúng).<br>3. Gọi **`CATEngine.computeEAP(responses=[{b:-0.45, isCorrect:true}])`**.<br>4. Gọi **`CATEngine.checkStoppingCriterion(session)`** với θ/SE mới.<br>5. Tạo record `SessionResponse` (itemId, response, isCorrect, thetaAfter, seAfter).<br>6. Cập nhật `SessionCacheState`: `theta`, `se`, `itemsAdministered=['V-102']`, `state='READY_FOR_NEXT'`.<br>7. Đẩy job async (BullMQ) ghi PostgreSQL, trả HTTP 200 ngay. |
| **Trả về (từ `computeEAP`)** | `AbilityEstimate {theta: -0.18, standardError: 0.95}` |
| **Trả về (từ `checkStoppingCriterion`)** | `{shouldStop: false}` — vì `SE=0.95` chưa `<0.35`, chưa chạm biên, mới 1/25 câu, chưa hết giờ |
| **Ai xử lý tiếp** | Client gọi lại `GET /next-item` |

**Vì sao θ chỉ tăng từ `-0.5` lên `-0.18` (không nhảy lên hẳn dương) dù trả lời đúng:** hiệu ứng *shrinkage* của Prior `N(0,1)` — với chỉ 1 điểm dữ liệu, Bayesian estimation chưa đủ tự tin để dịch θ đi xa, nó bị "kéo" một phần về giá trị trung tâm của prior (SRS Mục 4.3).

### Bước 3 — Lấy câu hỏi thứ 2

| | |
|---|---|
| **Class.phương thức** | `CATEngine.selectNextItem()` |
| **Làm gì** | 1. `pickNextSkill(session)` → `lastSkillPicked='vocabulary'` (từ câu 1) → alternate → **`grammar`** (ghi lại `lastSkillPicked='grammar'`).<br>2. `findForCAT('grammar', ['V-102'], -0.18)` → Top-5 câu Grammar gần `θ=-0.18`.<br>3. Random 1 câu. |
| **Ví dụ** | Chọn được **G-045** (`b = -0.20`) |

### Bước 4 → Bước N — Lặp lại chu trình (submit → next)

Chu trình **Bước 2 ↔ Bước 3** lặp lại, xen kẽ skill theo round-robin, θ/SE được cập nhật liên tục. Bảng dưới minh hoạ 14 câu đầu (số liệu minh hoạ, không phải kết quả chạy thật):

| Câu # | Skill | Item (b_i) | Trả lời | θ sau | SE sau | Dừng? |
|---|---|---|---|---|---|---|
| 1 | vocabulary | V-102 (-0.45) | Đúng | -0.18 | 0.95 | Không |
| 2 | grammar | G-045 (-0.20) | Đúng | 0.02 | 0.78 | Không |
| 3 | vocabulary | V-089 (0.05) | Sai | -0.10 | 0.68 | Không |
| 4 | grammar | G-112 (-0.05) | Đúng | 0.08 | 0.60 | Không |
| 5 | vocabulary | V-133 (0.10) | Đúng | 0.20 | 0.54 | Không |
| ... | ... | ... | ... | ... | ... | ... |
| 13 | vocabulary | V-201 (0.28) | Đúng | 0.30 | 0.37 | Không (0.37 ≥ 0.35) |
| 14 | grammar | G-198 (0.26) | Đúng | **0.33** | **0.34** | **Có** — `SE=0.34 < 0.35` |

### Bước 5 — Dừng bài thi

| | |
|---|---|
| **Class.phương thức** | `CATEngine.checkStoppingCriterion(session)` trả `{shouldStop: true, reason: 'se_threshold'}` sau câu 14 |
| **Ai thực thi việc dừng** | `TestSession.submitResponse()` thấy `shouldStop=true` → tự gọi **`TestSession.computeResult()`** |
| **`computeResult()` làm gì** | 1. `theta_final = 0.33`, `se_final = 0.34`.<br>2. Map θ→CEFR (SRS Mục 4.6): `0.0 ≤ θ < 1.0` → **B1**.<br>3. `status = 'COMPLETED'`, `completedAt = now()`, `stoppingReason = 'se_threshold'`.<br>4. Gọi **`LanguageProfile.generateFromSession(session)`**. |

### Bước 6 — Sinh hồ sơ năng lực

| | |
|---|---|
| **Class.phương thức** | `LanguageProfile.generateFromSession(session)` |
| **Nhận** | Toàn bộ `SessionResponse[]` của session (14 câu) |
| **Làm gì** | 1. Nhóm theo `skill` → tính `SkillProfile`:<br>&nbsp;&nbsp;- Vocabulary: 7 câu hỏi, 5 đúng → `scorePercent=71%`<br>&nbsp;&nbsp;- Grammar: 7 câu hỏi, 6 đúng → `scorePercent=86%`<br>2. Gom `ErrorPattern` theo `topicTag` của các câu sai.<br>3. Tạo `TestMetadata` (itemsAdministered=14, algorithm='CAT-Rasch-1PL', thetaInit=-0.5, quadraturePoints=41, stoppingReason='se_threshold').<br>4. Gọi **`AIExplainerService.generateRecommendations(errorPatterns)`** → điền `aiRecommendations`. |
| **Trả về** | `LanguageProfile` hoàn chỉnh (cefrLevel='B1', cefrConfidence tính từ SE=0.34 → 'medium') |
| **Ai dùng tiếp** | SV xem kết quả; `ClassReport` tổng hợp nhiều `LanguageProfile` cho Giảng viên; `exportForEduZ()` xuất JSON cho hệ sinh thái EduZ (qua API Key M2M — xem `Mo_ta_So_do_Lop_ClassDiagram.md` mục 2) |

---

## IV. SƠ ĐỒ TÓM TẮT (DÒNG CHẢY GIỮA CÁC CLASS)

```
Student
  │ start()
  ▼
TestSession ───create───► SessionCacheState (Redis: theta=-0.5, state=READY_FOR_NEXT)
  │ getNextItem()
  ▼
CATEngine.selectNextItem()
  │ pickNextSkill() → skill
  │ ItemBank.findForCAT(skill, usedIds, theta) ──► Item (Top-5 + random 1)
  ▼
[Item hiển thị cho SV]  ── SessionCacheState: state=WAITING_FOR_ANSWER

Student trả lời
  │ submitResponse(itemId, response)
  ▼
TestSession
  │──► CATEngine.computeEAP(responses[]) ──► AbilityEstimate{theta, se}
  │──► CATEngine.checkStoppingCriterion(session) ──► {shouldStop, reason}
  │──► tạo SessionResponse
  │──► cập nhật SessionCacheState (theta, se, state=READY_FOR_NEXT)
  │
  ├─ nếu shouldStop=false ──► lặp lại getNextItem()
  │
  └─ nếu shouldStop=true
        ▼
     TestSession.computeResult()
        │──► LanguageProfile.generateFromSession()
        │       │──► SkillProfile (theo skill)
        │       │──► ErrorPattern (theo topicTag)
        │       │──► AIExplainerService.generateRecommendations()
        ▼
     [Trả kết quả cho SV] ──► ClassReport (Giảng viên) / exportForEduZ() (EduZ)
```

---

## V. LƯU Ý KHI CODE (ĐỂ KHÔNG LỆCH KHỎI QUYẾT ĐỊNH ĐÃ CHỐT)

- `pickNextSkill()` **không** đọc tỷ lệ 160:120 từ Item Bank — câu 1 random 50/50, từ câu 2 alternate dựa trên `session.lastSkillPicked` (không phải đếm `itemsAdministered.length % 2`, vì điểm bắt đầu không cố định). Nếu sau này đổi chiến lược (Mục 3 phương án B/C trong `tracking/feature-plans/f03-cat-engine.md`), chỉ cần sửa đúng hàm này.
- `lastSkillPicked` phải được persist cùng `theta`/`se`/`itemsAdministered` trong `SessionCacheState`, và phải có trong `reconstructFromResponses()`/`SessionRepository.reconstruct()` khi khôi phục session từ PostgreSQL sau khi Redis mất dữ liệu (SRS Mục 15.5) — nếu không, sau reconstruct hệ thống sẽ tưởng là "câu đầu tiên" và random lại, có thể phá vỡ alternate pattern giữa lúc đang thi. Cách khôi phục đúng: suy ra `lastSkillPicked` từ `skill` của `item_id` trong `SessionResponse` **cuối cùng** đã lưu.
- `findForCAT` **luôn** filter `status='APPROVED'` ở tầng Repository (SQL), không phải business logic — xem SRS Mục 4.4, cảnh báo bắt buộc.
- Test case bắt buộc cho `computeEAP`: toàn đúng, toàn sai, xen kẽ (SRS Mục 4.3) — áp dụng luôn cho từng skill riêng nếu muốn chắc chắn round-robin không làm lệch kết quả EAP (EAP không quan tâm skill, chỉ quan tâm `b_i` và `isCorrect`, nên về mặt toán học không có rủi ro thêm — nhưng vẫn nên test).
- Test case cho `pickNextSkill()`: vì câu 1 có random, unit test cần **mock/inject nguồn random** (không test "ra đúng skill X" ở câu 1, mà test "câu 2 luôn ngược với câu 1 đã ra", lặp lại nhiều lần hoặc chạy với cả 2 giá trị seed).
