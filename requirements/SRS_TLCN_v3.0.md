# BẢN ĐẶC TẢ KỸ THUẬT & THIẾT KẾ HỆ THỐNG (SRS v3.0)

**Tên đề tài:** Kiến trúc hệ thống chẩn đoán năng lực ngôn ngữ toàn diện (Placement Test) tích hợp AI tự thích ứng

**Định vị:** Microservice độc lập, tích hợp Plug-and-Play vào Hệ sinh thái Giáo dục số EduZ

**Tọa độ ALDM-L:** Toàn diện × Diagnose × AI Assessor

**Lộ trình:** Tiểu luận chuyên ngành (3 tháng) → Khóa luận tốt nghiệp (3 tháng tiếp theo)

**Nhóm:** 2 người | **Cập nhật:** 14/10/2026 (v3.0 — Hệ thống đơn trường; Admin tạo tài khoản SV và GV (từng người hoặc import); Kỳ thi; đăng nhập email + mật khẩu; đổi/quên mật khẩu qua OTP; vòng 3 (14/10/2026): Admin tạo lô câu hỏi bằng AI hoặc import file, AI check ba điểm, duyệt hai vòng GV A và GV B, Admin kiểm tra và import cuối)

**[NOTE]** **Changelog v2.3:** Bổ sung 4 bản vá kiến trúc theo Team Review vòng 2: (1) Tránh lộ đề với Randomized Top-5 b-matching; (2) Chuyển Async Write (BullMQ) chống nghẽn cổ chai PostgreSQL; (3) Thêm cơ chế Early-Stop chống Deadlock kịch trần; (4) Redis State Machine chống API Race Condition.

**[NOTE]** Changelog v3.0 (từ v2.6 Final): (1) Hệ thống chỉ phục vụ một trường — bỏ khái niệm đa trường (tenant) và 3 cấp quản trị cũ, còn 3 role STUDENT / TEACHER / ADMIN; (2) GV thường chỉ xem kết quả, mọi chức năng quản trị do Admin thực hiện; (3) đăng nhập chỉ bằng email + mật khẩu, tài khoản SV và GV do Admin tạo (từng người trên giao diện hoặc import file), mật khẩu tạm gửi email; (4) thêm Kỳ thi (ExamRound) — SV phải thuộc một kỳ đang mở mới được thi, hạn phiên theo kỳ; (5) import theo "lưới tạm" cho tài khoản và danh sách thi; (6) quên mật khẩu bằng OTP 6 số qua email; (7) khóa tài khoản bằng users.is_active. Chi tiết: Mục IXb và Phụ lục A cuối tài liệu.

**[NOTE]** Changelog v3.0 vòng 3 (14/10/2026, DC-27 đến DC-45, Quyết định #110 đến #113): (1) luồng câu hỏi mới: Admin tạo lô bằng AI hoặc tự import file (lưới tạm) ⇒ AI check ⇒ Admin xem kết quả và Giao việc ⇒ GV vai A sửa/duyệt/từ chối ⇒ A gửi một gói cho GV vai B ⇒ B xác nhận hoặc loại từng câu ⇒ Admin Kiểm tra (C3) ⇒ Admin Import ⇒ FINAL_APPROVED; (2) trạng thái Item mới DRAFT → FIRST_APPROVED → SECOND_APPROVED → FINAL_APPROVED, thêm AI_REJECTED, bỏ trạng thái chờ duyệt cũ và đổi tên trạng thái đã duyệt cũ thành FINAL_APPROVED (CAT chỉ chọn FINAL_APPROVED); ItemSource được lược bỏ hoàn toàn khỏi Item (nguồn gốc xác định qua Lô ItemBatch); (3) GV không import, không có form thêm từng câu, Admin không sửa nội dung câu; (4) giải thích AI được sinh cùng lúc với câu hỏi (không sinh lazy), lưu bảng explanations; (5) khoảng irt_b hợp lệ [−4, +4] (cấu hình) khác CLAUDE.md; (6) phạm vi tăng: ai-question-generator (F-11) kéo từ Khóa luận vào Tiểu luận (F-23 đến F-28). Các đề xuất mặc định của kế hoạch sinh/duyệt đề AI bản 5 (Q-1 chọn O2, Q-3, Q-4, Q-5, Q-6) được coi là đã chấp nhận; Q-7 đến Q-10 (ngưỡng, bản quyền, mô hình embedding, pg_trgm) còn chờ chốt. Mọi tên bảng, endpoint, mã UC, màn hình và ngưỡng của phần này là đề xuất. Chi tiết: Mục IXb (9b.9 đến 9b.18) và Phụ lục A.

---

## I. TỔNG QUAN BÀI TOÁN

### 1.1. Bối cảnh & Động lực

Sinh viên năm nhất tại các trường Cao đẳng/Đại học phải làm **Placement Test bằng bộ đề cố định**:

- Không chính xác: sinh viên mạnh tốn thời gian câu dễ, sinh viên yếu nản với câu khó.

- Output chỉ là điểm số — không biết sinh viên yếu *ở đâu cụ thể* (Past Tense? Academic Vocab?).

- Không có dữ liệu cấu trúc cho EduZ cá nhân hóa lộ trình học.

### 1.2. Giải pháp

**Adaptive Placement Microservice** ứng dụng **CAT (IRT-Rasch)** + **AI Explainer (Gemini)**:

1. Chẩn đoán chính xác trong 20–25 câu thay vì 40–50 câu cố định.

2. Xuất **Language Competency Profile (JSON)** chuẩn hóa cho EduZ consume.

3. Microservice plug-and-play vào bất kỳ LMS nào.

### 1.3. Người dùng & Quy mô

| **Nhóm** | **Mô tả** | **Quy mô** |
| --- | --- | --- |
| Sinh viên (STUDENT) | Năm nhất làm Placement Test; tài khoản do Admin tạo (từng người hoặc import; không tự đăng ký); đăng nhập email + mật khẩu | 50–500 người/đợt |
| Giảng viên (TEACHER) | GV thường (tài khoản do Admin tạo, từng người hoặc import): xem kết quả — báo cáo lớp (lọc theo kỳ), tra cứu hồ sơ SV; đổi/quên mật khẩu. Khi Admin giao một lô câu hỏi: vai A (sửa/duyệt/từ chối câu được giao rồi gửi gói) hoặc vai B (một GV đại diện, xác nhận/loại từng câu trong gói gửi cho mình). GV không import đề, không tạo lô | 5–20 người (gộp GV + Admin, số liệu v2.6) |
| Admin (ADMIN) | Admin của trường, siêu tập của Teacher: tạo lô câu hỏi (AI sinh hoặc import file), giao việc, theo dõi, kiểm tra và import cuối (không soạn, không sửa nội dung câu); quản lý kỳ thi + danh sách thi, tạo từng người hoặc import tài khoản, quản lý tài khoản SV/GV, nâng/thu hồi Admin; tài khoản đầu tiên tạo bằng seed | Trong tổng 5–20 người nêu trên |
| EduZ System | Consume Language Profile qua API | Machine-to-machine |

- Hệ thống đơn trường (v3.0): không có bảng đơn vị/trường, không có cột khóa theo trường; đa trường là phạm vi Khóa luận (xem Mục XVI và R13).

- Đăng nhập chỉ bằng email + mật khẩu; UserRole giữ 4 giá trị STUDENT / TEACHER / ADMIN / EDUZ_SERVICE (EDUZ_SERVICE là tác nhân máy, truy cập bằng API Key, không có giao diện).

---

## II. ĐỊNH VỊ TRONG MA TRẬN ALDM-L

```
Trục X (Learning Stage):   DIAGNOSE  ← Điểm neo của toàn bộ hệ thống
Trục Y (Competency):       TOÀN DIỆN (TL: Vocabulary + Grammar | KL: + Writing)
Trục Z (AI Role):          AI ASSESSOR (chẩn đoán) + AI TUTOR (giải thích)
```

Module này là **node đầu tiên** trong vòng lặp học tập. Không có dữ liệu chẩn đoán chất lượng → các module phía sau (Đề tài 3, 4, 8) không cá nhân hóa được.

---

## III. KIẾN TRÚC HỆ THỐNG

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           EduZ Ecosystem                                   │
│  [ Learning Path Engine ]  [ Teacher Dashboard ]  [ Other Modules ]       │
└───────────────┬──────────────────────┬─────────────────────────────────────┘
                │  REST Pull           │  Webhook / BullMQ Push  (Khóa luận)
                ▼                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         Nginx API Gateway                                  │
└──────────┬───────────────────────────────────────────────────────┬─────────┘
           │                                                       │
    ┌──────▼──────┐                                  ┌────────────▼──────────────┐
    │  Frontend   │                                  │   Backend Microservice    │
    │  Next.js    │◄─────────────────────────────────│   NestJS (TypeScript)     │
    │  TypeScript │                                  │   Clean Architecture      │
    └─────────────┘                                  └──────┬────────────────────┘
                                                            │
              ┌─────────────────────────────────────────────┼──────────────────┐
              │                          │                   │                  │
       ┌──────▼──────┐  Async   ┌────────▼──────┐   ┌───────▼──────┐  ┌───────▼──────┐
       │ PostgreSQL  │◄─────────┤     Redis     │   │ AI Services  │  │  py-irt /    │
       │ (Source of  │ (BullMQ) │ (State Machine│   │ Gemini Flash │  │  catR API    │
       │ Truth)      │          │  & L1 Cache)  │   │ (Explainer)  │  │  (Calibrate) │
       └─────────────┘          └───────────────┘   └──────────────┘  └──────────────┘
```

### NestJS Module Breakdown

```
src/modules/
├── auth/                  # JWT Auth: email + mật khẩu (argon2), đổi/quên/đặt lại mật khẩu (OTP), mustChangePassword
├── user-import/           # (v3.0) Import tài khoản SV/GV theo lưới tạm, tham số kind (UCADM08)
├── user-admin/            # (v3.0) Tạo từng tài khoản SV/GV, quản lý tài khoản SV/GV, nâng/thu hồi Admin, RolesGuard (UCADM09) [tên module: đề xuất]
├── exam-round/            # (v3.0) Kỳ thi, danh sách thi, import danh sách thi theo lưới tạm (UCADM15-17)
├── mail/                  # (v3.0) MailPort + SmtpMailAdapter (SMTP) + BullMQ processor gửi email
├── item-bank/             # CRUD câu hỏi + IRT params
├── item-generation/       # (v3.0 vòng 3, đề xuất) Lô câu hỏi: AI sinh + import file; ItemCheckService (C1/C2/C3), ItemDuplicateChecker; giao việc, gói A→B, hạn và nhắc (UCADM11-14, UCGV14-15)
├── llm-gateway/           # (v3.0 vòng 3, đề xuất) Cổng gọi LLM dùng chung: dự phòng nhà cung cấp, cache theo hash prompt, ghi mô hình/token
├── cat-engine/            # ⭐ CAT Algorithm: IRT + EAP + Item Selection
├── test-session/          # Session management: dual-write Redis + PostgreSQL
├── language-profile/      # Tổng hợp + xuất JSON Profile
├── ai-explainer/          # Gemini: giải thích đúng/sai
├── ai-question-generator/ # (v3.0 vòng 3: phần sinh đề đã kéo vào TL, nằm trong item-generation; không tạo thư mục riêng — đề xuất)
└── reporting/             # Dashboard báo cáo GV/Admin (lọc theo kỳ thi)
```

**[NOTE]** Thay đổi kiến trúc v3.0: (1) bỏ Adapter Pattern cho đăng nhập ngoài — gói Tiểu luận chỉ có JwtAuthProvider (email + mật khẩu), việc tích hợp đăng nhập của EduZ thuộc Khóa luận; (2) Redis dùng thêm cho lưới tạm import (TTL ~30 phút) và bản băm OTP quên mật khẩu (TTL 10 phút); (3) BullMQ dùng cho hàng đợi gửi email có retry (MailPort); (4) máy chủ SMTP là hệ thống ngoài (nhà cung cấp chưa chọn — chờ chốt Q-5); (5) hệ thống đơn trường nên không còn lớp phạm vi theo trường (AccessScope/resolveScope); phân quyền chỉ theo role bằng RolesGuard dùng chung. Sơ đồ ASCII phía trên chưa vẽ SMTP; sơ đồ thành phần/triển khai chính thức để bổ sung sau. Vòng 3 (14/10/2026): thêm module item-generation và llm-gateway (đề xuất), BullMQ dùng thêm cho sinh/kiểm lô câu hỏi và nhắc hạn; phần ai-question-generator chuyển từ Khóa luận vào Tiểu luận.

### Thành phần mới v3.0 vòng 3 — sinh và duyệt câu hỏi (đề xuất)

| **Thành phần** | **Vai trò** | **Ghi chú** |
| --- | --- | --- |
| ItemGenerationService | Điều phối lô: nhận yêu cầu (skill, CEFR, topic, N), chạy nền qua BullMQ các bước G1 đến G7, tạo lô, ghi tên/phiên bản mô hình và token mỗi lời gọi | UCADM11, UCADM12 |
| ItemCheckService (3 checkpoint) | Một dịch vụ, ba điểm kiểm: C1 sau khi AI sinh, C2 khi import file, C3 trước FINAL_APPROVED; tầng rẻ (luật cứng, băm, pg_trgm) chạy trước, embedding và AI chỉ chạy cho câu còn sống; kết quả gắn content_hash và được tái sử dụng | Mục 9b.12 |
| ItemDuplicateChecker (+ DuplicateStrategy) | Lọc trùng ba tầng dùng chung mọi điểm kiểm: T1 băm chuẩn hóa, T2 pg_trgm, T3 embedding (cosine tính trong ứng dụng); mỗi tầng là một strategy | DC-30, DC-35 |
| ReviewDistributionService | Chia đều câu cho nhóm A (sắp theo skill, CEFR rồi chia vòng tròn); giao lại | Mục 9b.13 |
| DeadlineReminderService | Tính due_at (cuối ngày), đặt job trễ BullMQ nhắc trước hạn 24 giờ, đối chiếu lazy khi mở hộp việc phòng mất job | Mục 9b.14 |
| LLM Gateway | Cổng gọi LLM có dự phòng nhà cung cấp, cache theo hash prompt, trần lời gọi/token mỗi lô; dùng cho sinh câu, giải thích, kiểm đáp án độc lập (G5) và embedding | Mô hình embedding chờ chốt (Q-9) |
| Thực thể mới | ItemBatch, ItemPackage, ItemReviewAssignment, ItemCheckResult (cùng ItemReviewEvent tùy chọn) | Mục 6.2b |

**[NOTE]** Tên lớp, tên module và tên bảng ở trên là đề xuất theo kế hoạch sinh/duyệt đề AI bản 5 (Mục 11); Class Diagram và Sequence sẽ cập nhật ở tài liệu riêng. Sơ đồ ASCII ở đầu Mục III chưa vẽ LLM Gateway.

---

## IV. ĐẶC TẢ THUẬT TOÁN CAT — RASCH MODEL (1PL)

**[IMPORTANT]** Đây là **trái tim** hệ thống. Phần này được làm chặt theo phản hồi team review (v2.1).

### 4.1. Mô hình IRT

**Tiểu luận:** Rasch Model (1PL)

$$
P(\theta,b_i) = \frac{e^{(\theta-b_i)}}{1+e^{(\theta-b_i)}}
$$

- $\theta$ = năng lực người học

- $b_i$ = độ khó câu hỏi $i$ (đơn vị logit)

**Khóa luận (nâng cấp):** 2PL Model — thêm tham số $a_i$ (độ phân biệt).

### 4.2. Khởi tạo θ₀ — Đã điều chỉnh

**[WARNING]** **v2.1 FIX:** $\theta_0 = 0.0$ theo bảng mapping chính là **ranh giới A2/B1**, không phải giữa A2. Với sinh viên cao đẳng năm nhất (thường yếu hơn mặt bằng chung), khởi tạo tại ranh giới này khiến nhiều SV yếu phải "đi xuống" nhiều bước đầu → tốn câu hỏi, giảm hiệu quả CAT.

**Điều chỉnh:** $\theta_0 = -0.5$ (giữa dải A2: −1.0 to 0.0), phù hợp hơn với phân phối kỳ vọng của dân số mục tiêu.

$\theta_0$ có thể được cập nhật thành $\text{mean}(\theta)$ thực tế sau khi có đủ dữ liệu từ các phiên thi CAT thật (không còn phụ thuộc vào một đợt Pre-test calibration riêng, xem Mục 6.1/6.4).

### 4.3. Ability Update — EAP (Expected A Posteriori)

**Đặc tả đầy đủ (v2.1):**

| **Tham số** | **Giá trị** | **Ghi chú** |
| --- | --- | --- |
| Prior distribution | $\mathcal{N}(\mu = 0,\sigma^2 = 1)$ | Standard normal; có thể cập nhật từ data thực |
| Điểm lưới (grid points) | 41 điểm | Phân bổ đều trên $[-4,+4]$, bước 0.2 |
| Integration method | Lưới đều 41 điểm trên [−4, +4], bước 0.2, prior N(0,1) (tích phân số kiểu hình thang) | Đủ chính xác cho Rasch, không cần MCMC. Sửa mô tả theo K7 (DC-26): không dùng Gaussian–Hermite; thuật toán không đổi |

[NOTE] Sửa mô tả theo K7 (DC-26, vòng 2 phiên 23): các bản trước ghi "Gaussian–Hermite quadrature" là chưa đúng với thuật toán đã triển khai. Thuật toán EAP là tổng rời rạc trên lưới đều 41 điểm θₖ ∈ [−4, +4], bước 0.2, prior N(0,1) (tích phân số kiểu hình thang); công thức EAP/SE bên dưới giữ nguyên. Vì các điểm cách đều nên hệ số bước 0.2 triệt tiêu giữa tử số và mẫu số. Đây là sửa mô tả, không đổi thuật toán, không đổi mã.

**Công thức EAP:**

$$
\hat{\theta}_{\mathrm{EAP}} = \frac{\sum_{k = 1}^{41} \theta_k \cdot L(\mathbf{u}|\theta_k) \cdot \pi(\theta_k)}{\sum_{k = 1}^{41} L(\mathbf{u}|\theta_k) \cdot \pi(\theta_k)}
$$

Trong đó $L(\mathbf{u}|\theta_k)$ là likelihood của chuỗi phản hồi $\mathbf{u}$ cho trước $\theta_k$.

**Standard Error:**

$$
\mathrm{SE}(\hat{\theta}) = \sqrt{\frac{\sum_{k = 1}^{41} (\theta_k-\hat{\theta})^2 \cdot L(\mathbf{u}|\theta_k) \cdot \pi(\theta_k)}{\sum_{k = 1}^{41} L(\mathbf{u}|\theta_k) \cdot \pi(\theta_k)}}
$$

**[NOTE]** **Phân biệt θ₀ và Prior (hai vai trò tách biệt):**  | | θ₀ = −0.5 | Prior N(0,1) | |---|---|---| | **Vai trò** | Điểm khởi tạo để chọn **câu hỏi đầu tiên** | Phân phối Bayes để ước lượng θ **sau mỗi response** | | **Ảnh hưởng** | Chỉ ảnh hưởng item selection round 1 | Ảnh hưởng EAP estimation suốt bài thi | | **Sau câu 1** | Không còn dùng nữa, bị thay bởi EAP | Tiếp tục đóng vai trò prior |  Hiệu ứng **shrinkage** của prior N(0,1) (kéo θ về 0 trong 20-25 câu đầu) là hành vi đúng và mong muốn của Bayesian estimation — ngăn θ bị ước lượng quá cực đoan khi còn ít data. Prior N(-0.5, 1) là lựa chọn hợp lệ hơn về mặt lý thuyết nếu biết chắc dân số có mean = -0.5, nhưng N(0,1) là chuẩn học thuật được áp dụng rộng rãi (weakly informative).  **Sau khi có calibration data thực tế (Tuần 9-10):** Có thể cập nhật prior mean thành mean(θ) thực tế của cohort để giảm shrinkage bias.

**[WARNING]** **MLE Fallback Guard (nếu EAP bị bug):** MLE trong Rasch model **không hội tụ** khi sinh viên trả lời đúng hết hoặc sai hết — θ → ±∞, hệ thống crash hoặc trả về `NaN`. Trường hợp này xảy ra thường xuyên (SV Pre-A1 sai 5-10 câu đầu liên tiếp).  **Guard condition bắt buộc khi dùng MLE fallback:** 1. Chỉ invoke MLE khi có ≥ 1 câu đúng VÀ ≥ 1 câu sai trong session. 2. Nếu chưa đủ điều kiện (toàn đúng hoặc toàn sai): dùng EAP với prior mạnh hơn N(0, 0.5) tạm thời. 3. Clip θ kết quả về [-4, +4] trong MỌI trường hợp — không để θ vượt ra ngoài lưới 41 điểm.

**[NOTE]** EAP với lưới đều 41 điểm là phần **dễ bug nhất** khi tự code TypeScript — cần viết unit test riêng với các test case biết trước (ví dụ: 5 câu đúng hết → θ phải tăng đáng kể; 5 câu sai hết → θ phải giảm; xen kẽ đúng/sai → θ hội tụ về giữa).

### 4.4. Item Selection Strategy

**Chiến lược:** Randomized Top-5 b-matching (Tiểu luận) / Sympson-Hetter Exposure Control (Khóa luận)

$$
I_i(\theta) = P_i(\theta) \cdot [1-P_i(\theta)]
$$

#### Thuật toán Tiểu luận — Randomized Top-5 b-matching

Nếu chọn câu có $b_i$ gần $\hat{\theta}$ nhất theo kiểu tất định (deterministic), mọi sinh viên khởi tạo tại cùng $\theta_0 = -0.5$ sẽ nhận cùng câu hỏi đầu tiên. Bất cứ sinh viên nào thi xong đợt sáng đều có thể tuồn câu hỏi cho đợt chiều — bài thi biến thành học thuộc lòng.

**Thuật toán đã triển khai:**

1. Lọc ra **Top-N** câu chưa sử dụng (N=5 mặc định), sắp xếp theo $|b_i-\hat{\theta}|$ tăng dần.

2. Chọn **ngẫu nhiên đều 1 câu** từ pool N câu đó (uniform random sampling).

**Ước lượng hiệu quả giảm exposure (với Item Bank 280 câu, vùng A2–B1 có ~35 câu):**

| **Chiến lược** | **Xác suất chọn câu bất kỳ ở câu đầu** | **Expected max exposure sau 100 SV** |
| --- | --- | --- |
| Deterministic (b-match tuyệt đối) | 100% cùng 1 câu | Exposure = 100% |
| Randomized Top-5 | 1/5 = 20% mỗi câu | Expected max exposure ≈ 60-70% ¹ |
| Sympson-Hetter (KL) | Capped < 30% mỗi câu | Max exposure ≤ 30% (đảm bảo) |

¹ **Ước lượng sơ bộ theo lý thuyết** (dựa trên Birthday Problem approximation với N=5, pool=35 câu vùng A2-B1, 100 SV). Chưa có mô phỏng Monte Carlo đứng sau con số này. **Sẽ xác nhận bằng dữ liệu log chọn câu thực tế sau khi CAT đi vào hoạt động** (không còn đợt Pre-test riêng để thu thập trước, xem Mục 6.1).

**[NOTE]** Randomized Top-5 không giải quyết hoàn toàn bài toán exposure (vùng A2-B1 còn 20-35 câu, 500 SV vẫn sẽ thấy lại câu cũ sau 25-50 lượt). Tuy nhiên, đây là biện pháp **phòng thủ theo chiều sâu** phù hợp với quy mô Tiểu luận: không phức tạp, không tốn thêm câu hỏi, giảm đáng kể tính tất định so với b-match tuyệt đối. **Khóa luận sẽ implement Sympson-Hetter** với exposure cap cứng ≤ 0.3 như đặc tả Mục 4.8.

**[IMPORTANT]** **Guard condition bắt buộc:** Query item selection **PHẢI** filter `WHERE status = 'FINAL_APPROVED'`. Item có status khác FINAL_APPROVED (DRAFT, FIRST_APPROVED, SECOND_APPROVED, REJECTED, AI_REJECTED) tuyệt đối không được đưa vào bài thi. Đây phải được đặt ở tầng Repository, không phải business logic. ```typescript // ItemRepository.findForCAT() — Randomized Top-5 return this.db.query( `WITH TopMatches AS ( SELECT * FROM items WHERE status = 'FINAL_APPROVED' AND skill = $1 AND id != ALL($2) ORDER BY ABS(irt_b - $3) LIMIT 5 ) SELECT * FROM TopMatches ORDER BY RANDOM() LIMIT 1;`, [skill, usedIds, currentTheta] ); ```

**[NOTE]** Vòng 3 (DC-39): trạng thái đã duyệt cũ được đổi tên thành FINAL_APPROVED; FIRST_APPROVED và SECOND_APPROVED là hai mức duyệt trung gian (GV vai A, GV vai B) và chưa được CAT chọn. Điều kiện lọc ở tầng Repository, Partial Index (Mục 6.2) và R9 đều đổi theo; công thức và các bước chọn câu Top-5 không đổi. Mã BE và seed hiện có còn dùng tên cũ — nợ đồng bộ, chưa sửa ở tài liệu này.

### 4.5. Stopping Criterion

| **Điều kiện** | **Ngưỡng** | **Loại** |
| --- | --- | --- |
| Số câu tối đa | 25 câu | Hard stop |
| Standard Error | $\mathrm{SE}(\hat{\theta}) < 0.35$ | Preferred stop (dừng sớm khi đủ tin cậy) |
| Timeout (hạn phiên theo kỳ thi) | durationMinutes của kỳ thi (NOT NULL, mặc định 45 phút; 5 ≤ duration ≤ 180); expires_at = min(startedAt + durationMinutes, closesAt) | Hard stop |
| Outlier Early Stop | $\theta > 1.5$ hoặc $\theta < -2.5$ VÀ $\Delta\mathrm{SE} < 0.01$ trong 3 câu liên tiếp VÀ đã làm ≥ 8 câu | Boundary stop (Chống Item Bank Deadlock) |

**Giải thích Outlier Early Stop:**

Khi năng lực sinh viên $\theta$ vượt ra ngoài dải độ khó của Item Bank ($b_{\mathrm{min}} = -2.5$, $b_{\mathrm{max}} = +1.5$), Fisher Information tại $\theta$ xấp xỉ 0:

$$
I_i(\theta) = P_i(\theta) \cdot [1-P_i(\theta)] \approx 0\text{ khi }|\theta-b_i| \gg 0
$$

Khi đó $\mathrm{SE}(\hat{\theta})$ ngừng giảm (đi ngang) qua mỗi câu hỏi, không bao giờ đạt ngưỡng < 0.35. Nếu không có cơ chế dừng sớm, sinh viên rất giỏi hoặc rất yếu bị ép làm đủ 25 câu không phù hợp — gây trải nghiệm người dùng rất tệ.

**[NOTE]** Các mốc b_min = −2.5 và b_max = +1.5 ở đây là vùng phủ thực tế hiện tại của Item Bank (CEFR A1 đến B2) và là căn cứ của Outlier Early Stop; chúng không còn là giới hạn hợp lệ của irt_b khi nhập/lọc câu hỏi (xem NOTE về khoảng irt_b ở Mục 4.7). Công thức và ngưỡng Early Stop không đổi.

**[NOTE]** **Tại sao cần ≥ 8 câu tối thiểu:** Nếu Early Stop kích hoạt sau 5-6 câu đầu, θ ước lượng còn rất chưa ổn định — SE đi ngang ở giai đoạn đó có thể chỉ là nhiễu ngẫu nhiên, không phải boundary effect thật sự. Với ≥ 8 câu, EAP đã có đủ signal để θ hội tụ về vùng đúng trước khi quyết định dừng.

**Thuật toán phát hiện:**

```
// Sau mỗi item (kiểm tra theo thứ tự ưu tiên):
if (itemCount >= 8 && (theta > 1.5 || theta < -2.5)) {
  const dSE1 = Math.abs(SE[k]   - SE[k-1]);
  const dSE2 = Math.abs(SE[k-1] - SE[k-2]);
  if (dSE1 < 0.01 && dSE2 < 0.01) {
    // SE đi ngang 3 câu liên tiếp sau ≥8 câu → dừng sớm
    stopReason = 'item_bank_boundary';
    boundaryEffect = true;
    break;
  }
}
```

**Output và thông báo — Phân biệt rõ 2 khái niệm:**

**[IMPORTANT]** **θ > 1.5 / θ < -2.5 ≠ "ngoài CEFR"** — đây là "ngoài vùng phủ của Item Bank hiện tại", không phải ngoài thang CEFR. Ví dụ: SV B2 thật (θ=1.7) vẫn được xếp loại B2 đúng ở Mục 4.6, nhưng hệ thống không có đủ câu khó để đo thêm (b_max ≈ +1.5 < 1.7). Hai khái niệm này phải được tách bạch rõ trong thông báo:

| **Trường hợp** | **cefr_level** | **boundary_effect** | **Thông báo hiển thị** |
| --- | --- | --- | --- |
| θ=1.7 (B2 thật, ngoài item bank) | B2 | true | *"Hệ thống đã xếp loại bạn ở B2. Kết quả có thể chưa phân biệt tốt B2 với C1 vì ngân hàng đề chưa có câu đủ khó ở vùng này."* |
| θ=2.3 (C1+, ngoài CEFR và item bank) | C1+ | true | *"Năng lực của bạn vượt ngoài phạm vi đánh giá hiện tại (C1+). Vui lòng liên hệ Giảng viên để được tư vấn bổ sung."* |
| θ=-2.8 (Pre-A1, ngoài CEFR và item bank) | Pre-A1 | true | *"Năng lực của bạn chưa đến mức A1. Vui lòng liên hệ Giảng viên để được hỗ trợ thêm."* |

**[NOTE]** Thứ tự ưu tiên dừng: **SE < 0.35** > **Boundary Stop (≥8 câu)** > **Hard Stop 25 câu** > **Timeout**.

**[IMPORTANT]** Hạn phiên theo kỳ thi (v3.0, thay Timeout cố định 45 phút của v2.6): "45 phút" nay là giá trị mặc định, có thể ghi đè theo từng kỳ (durationMinutes). Hạn của mỗi phiên expires_at = min(startedAt + durationMinutes, closesAt) được tính một lần lúc bắt đầu phiên và lưu vào test_sessions.expires_at; sửa kỳ thi sau đó không đổi hạn của phiên đang chạy. Ví dụ kỳ 10:00–11:00, durationMinutes = 60: SV vào 10:30 còn 30 phút; vào 10:05 còn 55 phút.

- Quá hạn xử lý theo luật K5 (#77): đã làm ≥ 8 câu ⇒ phiên COMPLETED với stopping_reason = TIMEOUT; dưới 8 câu ⇒ ABANDONED (SV được thi lại trong cùng kỳ nếu cửa sổ còn mở).

- Hạn phiên so với expires_at lưu ở PostgreSQL, không dựa vào TTL của Redis (TTL 7200 giây ở Mục VIII/15.2 chỉ là thời hạn cache để khôi phục phiên).

- Giới hạn 25 câu, ngưỡng SE < 0.35 và Outlier Early Stop không đổi.

### 4.6. Mapping θ → CEFR

| **Theta (θ)** | **CEFR** | **Ghi chú** |
| --- | --- | --- |
| $\theta < -2.0$ | Pre-A1 | ⚠️ Ngoài phủ sóng Item Bank — xem mục 4.7 |
| $-2.0 \leq \theta < -1.0$ | A1 | Phủ bởi Item Bank |
| $-1.0 \leq \theta < 0.0$ | A2 | Phủ bởi Item Bank |
| $0.0 \leq \theta < 1.0$ | B1 | Phủ bởi Item Bank |
| $1.0 \leq \theta < 2.0$ | B2 | Phủ bởi Item Bank |
| $\theta \geq 2.0$ | C1+ | ⚠️ Ngoài phủ sóng Item Bank — xem mục 4.7 |

### 4.7. Ceiling / Floor Effect — Giới hạn đã biết

**[WARNING]** Item Bank chỉ phủ CEFR A1–B2 (logit $b \approx -2.5$ đến $+1.5$). Sinh viên rơi vào **Pre-A1 hoặc C1+** sẽ không có item đủ dễ/khó để đo chính xác → $\mathrm{SE}(\theta)$ khó đạt < 0.35 → hầu hết bị hard-stop ở 25 câu với độ tin cậy thấp.

**[NOTE]** Khoảng irt_b (v3.0 vòng 3, DC-34, Quyết định #107): khoảng hợp lệ của irt_b khi nhập/lọc câu hỏi (luật cứng tầng 1 của AI check, Mục 9b.12) là [−4, +4] và là tham số cấu hình, thay cho [−2.5, +1.5] mà CLAUDE.md đang ghi cho "boundary Item Bank". CLAUDE.md không áp dụng trực tiếp cho phần này; việc sửa CLAUDE.md chỉ ở dạng đề xuất (Q-12). Lý do theo quyết định: kế hoạch sinh/duyệt đề AI bản 5 chốt khoảng này ở DC-34; kế hoạch không ghi thêm lý do (diễn giải của AI: để câu AI sinh hoặc import có irt_b gợi ý ngoài vùng A1 đến B2 không bị loại cứng, còn vùng phủ thực tế vẫn như mô tả ở trên). Đối chiếu công thức CAT: mô hình Rasch, EAP trên lưới 41 điểm [−4, +4], SE, chọn Top-5 theo |b − θ|, tiêu chí dừng đều không đổi. Phần còn lại là kiểm tác động lên việc chọn câu CAT bằng test (Q-12, chưa làm).

**Xử lý trong TL:**

- Report kết quả với warning flag: "boundary_effect": true trong JSON Profile.

- Hiển thị cho SV: *"Hệ thống đánh giá bạn thuộc nhóm [Pre-A1/C1+] — kết quả ở vùng biên có thể kém chính xác hơn. Vui lòng liên hệ Giảng viên."*

**Hướng mở rộng (KL):** Bổ sung item Pre-A1 (b < −2.5) và B2+ (b > +1.5).

### 4.8. Item Exposure Control — Rủi ro cần ghi nhận

**[CAUTION]** **Rủi ro lộ đề (Item Exposure):** Item bank 250 câu với 50–500 SV/đợt. Vùng A2–B1 (xung quanh θ = 0) có mật độ item mỏng nhất. Các câu phổ biến (b ≈ 0) sẽ bị chọn lặp lại nhiều lần → SV thi sau có thể biết trước câu hỏi từ SV thi trước trong cùng đợt.

**Đây khác với F-16 (Anti-Cheating trong lúc thi).**

**Không implement trong TL** (do item bank còn nhỏ và chưa đủ dữ liệu để ước lượng exposure rate). Ghi nhận trong Risk Register.

**Hướng giải quyết sau (KL):** Randomized Item Selection với exposure constraint — chỉ chọn câu có $\text{exposure\_rate} < 0.3$ (Sympson-Hetter method hoặc đơn giản hơn là max-use cap).

---

## V. KIẾN TRÚC IRT — HAI QUY TRÌNH TÁCH BIỆT (v2.2)

**[IMPORTANT]** Phiên bản trước gộp nhầm hai bài toán hoàn toàn khác nhau vào một "lựa chọn A/B". Đây là tái cơ cấu lại đúng.

Runtime EAP (ước lượng năng lực) và Offline Calibration (hiệu chỉnh tham số item) là **hai quy trình độc lập** về mục đích, tần suất và yêu cầu kỹ thuật:

|  | **Runtime EAP** | **Offline Calibration** |
| --- | --- | --- |
| Mục đích | Ước lượng θ sau mỗi câu trả lời | Tính toán lại b_i từ dữ liệu thực |
| Tần suất | 25 lần/bài thi, realtime | 1-2 lần/kỳ thi, batch |
| Yêu cầu latency | < 50ms (trong 1 HTTP request) | Không giới hạn (chạy offline) |
| Yêu cầu accuracy | Đủ tốt để chọn item tiếp theo | Cao nhất có thể (MMLE) |

---

### Quyết định 1 (Bắt buộc): Runtime Ability Estimation = TypeScript tự implement

**Lý do bắt buộc:** Latency. Mỗi khi sinh viên submit câu trả lời, hệ thống phải tính EAP và trả về câu tiếp theo trong < 50ms. Nếu gọi sang Python REST endpoint bên ngoài (py-irt), mỗi request tốn thêm:

- Network round-trip: 10-50ms

- Python cold-start nếu container sleep: 500ms+

- Với 25 lần/bài thi và 500 SV đồng thời → không thể chấp nhận.

**Kết luận:** EAP runtime **luôn là TypeScript tự code** — không có lựa chọn nào khác về mặt kiến trúc.

| **Tiêu chí** | **Đánh giá** |
| --- | --- |
| Tính học thuật | ✅ Cao — hiểu sâu, biểu hiện tốt trong báo cáo và defense |
| Latency | ✅ In-process, < 5ms |
| Rủi ro | 🟡 EAP với lưới 41 điểm dễ bug → cần unit test kỹ (xem Mục 4.3) |
| Phù hợp khi GVHD yêu cầu "tự xây dựng mô hình" | ✅ Có source code tự viết toàn bộ |

---

### Quyết định 2 (Linh hoạt): Offline Calibration = py-irt hoặc tự code

Đây là quy trình chạy batch, offline, 1-2 lần/kỳ. Không có yêu cầu latency nên có thể linh hoạt hơn. **Không bắt buộc trong Tiểu luận** (Tiểu luận không tự chạy calibration ban đầu — xem Mục 6.1/6.4); có thể triển khai sau này khi cần tinh chỉnh lại b_i từ dữ liệu sử dụng thực tế (F-12, hướng Khóa luận).

| **Tiêu chí** | **Phương án A: py-irt (Python)** | **Phương án B: catR (R)** |
| --- | --- | --- |
| Accuracy | ✅ MMLE chuẩn, được kiểm chứng | ✅ Chuẩn học thuật, nhiều paper dùng |
| Học thuật | ✅ Dễ cite | ✅ Dễ cite hơn (R phổ biến trong Psychometrics) |
| Tích hợp | Docker Python service nhỏ | Docker R service |
| Output | JSON params | CSV/JSON params |

**Khuyến nghị:** Dùng **py-irt** vì team đã có Python environment (Gemini API). Chạy dưới dạng Docker sidecar, chỉ invoke khi chạy calibration job, không liên quan đến runtime của backend.

---

## VI. NGÂN HÀNG CÂU HỎI (ITEM BANK)

### 6.1. Kế hoạch Bootstrap — Đã điều chỉnh Timeline

**[WARNING]** v2.6 FIX (thay v2.1): Kế hoạch tự tổ chức Pre-test tuyến tính cho ≥60 sinh viên (đã đặc tả ở v2.1–v2.5) bị loại khỏi phạm vi Tiểu luận theo nhận xét GVHD — khối lượng tổ chức một đợt thi riêng cho ≥60 SV là quá lớn so với quy mô nhóm 2 người/12 tuần. Thay vào đó, b_i ban đầu được lấy từ nguồn câu hỏi/ngân hàng đề đã có độ khó chuẩn hóa từ trước (xem NOTE bên dưới và Mục 6.4).

| **Giai đoạn** | **Nội dung** | **Tuần (TL)** |
| --- | --- | --- |
| 0 — AI Generation | Gemini sinh theo lô qua module item-generation (F-23; sinh dư rồi lọc bằng AI check C1) hoặc Admin import file (F-24); mục tiêu ~300 câu Vocab/Grammar (dự phòng 20% bị loại) | 1–2 |
| 1 — Expert Validation | Duyệt hai vòng: GV vai A sửa/duyệt, GV vai B xác nhận (F-26, F-27); Admin kiểm tra C3 và import (F-28) → giữ lại ~250 câu FINAL_APPROVED | 3–4 |
| 2 — Sourcing độ khó chuẩn | Tìm nguồn câu hỏi/ngân hàng đề đã được chuẩn hóa độ khó (CEFR-graded hoặc đã IRT-calibrated); đối chiếu và gán b_i ban đầu cho từng câu trong Item Bank dựa trên nguồn đó — thay cho việc tự tổ chức Pre-test và tự chạy calibration | 7–8 |
| 3 — Validate & Fallback | Kiểm tra tính hợp lý của b_i đã gán (đối chiếu CEFR anchor Mục 4.6, GV Ngoại ngữ review chéo); gán b_i fallback theo CEFR anchor cho item không tìm được độ khó chuẩn từ nguồn | 9–10 |
| 4 — Activate CAT | Deploy item bank đã gán độ khó chuẩn; bắt đầu CAT thật | 11 |

**[NOTE]** **Nguồn câu hỏi độ khó chuẩn:** ưu tiên tìm ngân hàng đề đã được chuẩn hóa độ khó theo CEFR hoặc đã IRT-calibrated công khai, quy đổi/đối chiếu sang thang logit của hệ thống (xem Mục 4.6). Nguồn cụ thể chưa chốt tại thời điểm v2.6 — xem tracking/DECISIONS_LOG.md. **Tiêu chí fallback** nếu một item không tìm được độ khó chuẩn từ nguồn tham chiếu: gán b_i tạm thời theo **CEFR anchor** (giá trị giữa dải logit ứng với cefr_target của item — xem bảng Mục 4.6), đánh dấu calibrated = false, và GV Ngoại ngữ review kỹ các item fallback này trước khi các câu này được Admin import thành FINAL_APPROVED.

### 6.2. PostgreSQL Schema — Items Table

```
CREATE TABLE items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content         TEXT NOT NULL,
    options         JSONB NOT NULL,          -- {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer  CHAR(1) NOT NULL,        -- 'A' | 'B' | 'C' | 'D'
    skill           VARCHAR(20) NOT NULL,    -- 'vocabulary' | 'grammar'
    topic_tag       VARCHAR(50),             -- 'past_simple' | 'academic_vocab' | ...
    cefr_target     VARCHAR(3) NOT NULL,     -- 'A1' | 'A2' | 'B1' | 'B2'
    irt_b           FLOAT NOT NULL,          -- Difficulty (logit); hợp lệ [-4, +4], cấu hình (DC-34)
    irt_a           FLOAT DEFAULT 1.0,       -- Discrimination [2PL — KL, default 1.0 = Rasch]
    -- NOTE: irt_c là field DỰ PHÒNG cho KL (3PL guessing parameter).
    -- KHÔNG được sử dụng trong thuật toán Rasch 1PL hiện tại của TL.
    irt_c           FLOAT DEFAULT 0.25,      -- [RESERVED - KL only, 3PL]

    -- Approval workflow fields (bắt buộc để CAT không chọn nhầm item DRAFT)
    status          VARCHAR(20) DEFAULT 'DRAFT',  -- 'DRAFT' | 'FIRST_APPROVED' | 'SECOND_APPROVED' | 'FINAL_APPROVED' | 'REJECTED' | 'AI_REJECTED'
    approved_by     UUID REFERENCES users(id),    -- Admin bấm Import; NULL tới khi FINAL_APPROVED
    approved_at     TIMESTAMPTZ,                  -- NULL tới khi FINAL_APPROVED
    content_hash    VARCHAR(64),                  -- v3.0 vòng 3: SHA-256 (hex) của nội dung + đáp án + giải thích đã chuẩn hóa (T1)
    batch_id        UUID NOT NULL REFERENCES item_batches(id),   -- lô sinh/import; bắt buộc (quyết định 16/10/2026), câu seed thuộc lô seed
    package_id      UUID REFERENCES item_packages(id),  -- gói A→B; NULL tới khi A gửi gói (đề xuất)
    -- Audit: chỉ item có status='FINAL_APPROVED' được CAT engine dùng (xem Mục 4.4)

    calibrated      BOOLEAN DEFAULT FALSE,   -- Đã calibrate thực tế chưa?
    times_used      INT DEFAULT 0,
    exposure_rate   FLOAT DEFAULT 0.0,       -- [RESERVED] Tỉ lệ xuất hiện/tổng phiên thi
    p_value         FLOAT,                   -- Tỉ lệ trả lời đúng thực tế
    item_fit_mnsq   FLOAT,                   -- Rasch item fit (MNSQ, expected ≈ 1.0)
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index cho CAT query performance
CREATE INDEX idx_items_cat ON items(status, skill, irt_b) WHERE status = 'FINAL_APPROVED';
-- Chỉ mục lọc trùng (v3.0 vòng 3, đề xuất)
CREATE INDEX idx_items_content_hash ON items (content_hash);                      -- T1: băm chuẩn hóa
CREATE INDEX idx_items_content_trgm ON items USING GIN (content gin_trgm_ops);    -- T2: cần CREATE EXTENSION pg_trgm (chờ chốt Q-10)
```

**[NOTE]** v3.0 (vòng 3): approved_by / approved_at ghi Admin bấm Import (chuyển câu sang FINAL_APPROVED); nội dung câu được duyệt bởi GV vai A (FIRST_APPROVED) và GV vai B (SECOND_APPROVED), truy vết ở item_review_events. Nội dung này thay quy tắc DC-18 "Admin tự duyệt câu hỏi do mình soạn": Admin không soạn và không sửa nội dung câu (DC-29); câu FINAL_APPROVED cấm sửa (#64). Rủi ro chất lượng xem R12, R17, R18. Điều kiện guard của CAT đổi thành WHERE status = 'FINAL_APPROVED' (Mục 4.4). Vì items tham chiếu item_batches và item_packages, khi viết migration phải tạo hai bảng này trước (hoặc thêm khóa ngoại sau bằng ALTER).

**[NOTE]** Lô seed (quyết định 16/10/2026): mọi câu thuộc một lô, kể cả câu seed. Script cài đặt phải tạo tài khoản Admin hệ thống trước (ví dụ admin@apt.edu.vn), sau đó lấy id Admin điền vào created_by của các lô seed. Mỗi lô seed ghi source = IMPORTED, status = DONE, requested_count = NULL, name = tên bộ nguồn (một lô cho mỗi bộ: CEFR-J, CLOTH, đề GV tự soạn); câu nạp vào gán batch_id đúng lô. Migration cho dữ liệu cũ: gán batch_id của các câu chưa có lô vào lô seed tương ứng rồi mới đặt NOT NULL. Lô seed không chạy C1/C2/C3 và không có gói/giao việc.

### 6.2b. Bảng bổ sung cho lô, giao việc và kiểm tra (v3.0 vòng 3 — đề xuất)

```
CREATE EXTENSION IF NOT EXISTS pg_trgm;   -- chờ chốt Q-10 (image Postgres staging chưa kiểm)

-- Enum (mô tả): ItemStatus = DRAFT | FIRST_APPROVED | SECOND_APPROVED | FINAL_APPROVED | REJECTED | AI_REJECTED
--              (Item không còn trường source: nguồn gốc lưu tại item_batches.source, enum ItemBatchSource = AI_GENERATED | IMPORTED; quyết định 16/10/2026)

CREATE TABLE item_batches (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source          VARCHAR(20) NOT NULL,          -- ItemBatchSource: AI_GENERATED | IMPORTED
    name            VARCHAR(100),                  -- nhãn tùy chọn; lô seed ghi tên bộ nguồn (CEFR-J, CLOTH, GV tự soạn)
    created_by      UUID NOT NULL REFERENCES users(id),   -- Admin
    skill           VARCHAR(20),                   -- lô AI: bắt buộc; lô import: NULL (mỗi dòng có Skill/CEFR riêng) — đề xuất
    cefr_target     VARCHAR(3),
    topic_tag       VARCHAR(50),
    requested_count INT,                           -- N (lô AI)
    status          VARCHAR(20) NOT NULL,          -- GENERATING | IMPORTING | CHECKING | READY_TO_ASSIGN | IN_REVIEW |
                                                   -- READY_TO_FINALIZE | FINAL_CHECKED | DONE | FAILED | PARTIAL
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Hạn chỉ có khi đã giao việc => bảng riêng, tránh cột trống
CREATE TABLE item_batch_assignments (
    batch_id        UUID PRIMARY KEY REFERENCES item_batches(id),
    confirmer_id    UUID NOT NULL REFERENCES users(id),   -- GV vai B, không thuộc nhóm A (kiểm ở tầng ứng dụng)
    review_days     INT NOT NULL CHECK (review_days >= 1),
    confirm_days    INT NOT NULL CHECK (confirm_days >= 1)
);

CREATE TABLE item_review_assignments (
    item_id         UUID PRIMARY KEY REFERENCES items(id),   -- UNIQUE(item_id): mỗi câu một người vai A
    assignee_id     UUID NOT NULL REFERENCES users(id),
    assigned_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    due_at          TIMESTAMPTZ NOT NULL,           -- cuối ngày (ngày giao + review_days), 23:59:59 giờ VN (cấu hình)
    reminder_sent   BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE item_packages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id        UUID NOT NULL REFERENCES item_batches(id),
    reviewer_id     UUID NOT NULL REFERENCES users(id),   -- GV vai A gửi gói (mỗi A một gói)
    confirmer_id    UUID NOT NULL REFERENCES users(id),   -- GV vai B
    status          VARCHAR(10) NOT NULL,           -- OPEN | SENT | DONE
    due_at          TIMESTAMPTZ,                    -- đặt khi gói được gửi: cuối ngày (ngày gửi + confirm_days)
    reminder_sent   BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE item_embeddings (
    item_id         UUID PRIMARY KEY REFERENCES items(id),
    vector          FLOAT8[] NOT NULL,              -- Float[]; cosine tính trong ứng dụng
    model           VARCHAR(100) NOT NULL,          -- ghi mô hình thật (mô hình chờ chốt Q-9)
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE item_check_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id         UUID NOT NULL REFERENCES items(id),
    checkpoint      VARCHAR(2) NOT NULL,            -- C1 | C2 | C3
    content_hash    VARCHAR(64) NOT NULL,           -- kết quả gắn với hash: hash không đổi thì tái sử dụng
    level           VARCHAR(4) NOT NULL,            -- PASS | SOFT | HARD
    reason_codes    TEXT[],
    checked_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tùy chọn, phục vụ truy vết
CREATE TABLE item_review_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id        UUID REFERENCES item_batches(id),
    item_id         UUID REFERENCES items(id),
    package_id      UUID REFERENCES item_packages(id),
    actor_id        UUID REFERENCES users(id),
    event_type      VARCHAR(20) NOT NULL,           -- APPROVE | REJECT | CONFIRM | REMOVE | CONFIRM_ALL | IMPORT |
                                                    -- REASSIGN | EXTEND | FORCE_SEND | ACCEPT_FLAG
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**[NOTE]** Toàn bộ DDL ở Mục 6.2b là mô tả theo Mục 10 của kế hoạch sinh/duyệt đề AI bản 5: tên bảng, tên cột, kiểu dữ liệu và giá trị enum là đề xuất, chưa có trong schema.prisma và custom_migrations.sql. Nguồn chân lý thực thi vẫn là schema.prisma + custom_migrations.sql sau khi đồng bộ. Bảng explanations (giải thích gắn Item, sinh cùng lúc sinh câu hỏi) đã tồn tại theo #63 và không nằm trong danh sách trên. Các kiểm tra "B không thuộc nhóm A", "A khác B" và "mỗi A một gói" thực hiện ở tầng ứng dụng.

### 6.3. Phân bổ Item Bank

| **Kỹ năng** | **A1** | **A2** | **B1** | **B2** | **Tổng** |
| --- | --- | --- | --- | --- | --- |
| Vocabulary | 40 | 45 | 45 | 30 | 160 |
| Grammar | 30 | 35 | 35 | 20 | 120 |
| Tổng | 70 | 80 | 80 | 50 | 280 |

*(Sinh nhiều hơn mục tiêu để dự phòng bị loại trong quá trình validation)*

---

### 6.4. Quy trình Huấn luyện (Calibration) mô hình IRT và Nguồn dữ liệu

Trong ngữ cảnh CAT, "huấn luyện mô hình" (Training) chính là quá trình **Hiệu chỉnh (Calibration)** tham số độ khó $b_i$ của các câu hỏi dựa trên xác suất thống kê.

- **Nguồn dữ liệu lấy từ đâu?** Dữ liệu huấn luyện là một **Ma trận phản hồi nhị phân (Response Matrix)**. Mỗi dòng là một sinh viên, mỗi cột là một câu hỏi, giá trị 1 là trả lời đúng, 0 là sai.

- **Giai đoạn 1 (Lấy độ khó ban đầu - Cold Start):** Không tự tổ chức Pre-test/khảo sát riêng để thu response matrix. Thay vào đó, b_i ban đầu được lấy/quy đổi từ một nguồn câu hỏi/ngân hàng đề đã có độ khó chuẩn hóa từ trước (xem Mục 6.1) — item bank đi vào hoạt động CAT ngay, không cần chờ thu thập dữ liệu và chạy calibration trước.

- **Giai đoạn 2 (Học liên tục — tinh chỉnh, hướng Khóa luận):** Khi hệ thống CAT đi vào hoạt động thực tế, mỗi lượt sinh viên thi sẽ tiếp tục sinh ra dữ liệu. Hệ thống lưu trữ lịch sử này tại bảng session_responses; dữ liệu này có thể dùng để tinh chỉnh lại b_i sau này khi đã đủ số lượng response/item (không bắt buộc cho Tiểu luận).

- **Cách Train (Calibrate) — nếu thực hiện tinh chỉnh lại (không bắt buộc ở TL):** Xuất Ma trận phản hồi từ Database, đưa vào thư viện py-irt (sử dụng thuật toán Marginal Maximum Likelihood Estimation - MMLE). Thuật toán sẽ phân tích chéo tỷ lệ đúng/sai của tất cả sinh viên trên tất cả câu hỏi để tính toán ra b_i chính xác cho từng câu, sau đó hệ thống cập nhật lại b_i vào Item Bank.

## VII. LANGUAGE COMPETENCY PROFILE — JSON SCHEMA

### Schema v1 (Tiểu luận)

```
{
  "$schema": "https://eduz.vn/schemas/language-profile/v1",
  "student_id": "SV2026-001",
  "test_session_id": "550e8400-e29b-41d4-a716-446655440000",
  "completed_at": "2026-09-09T10:35:22+07:00",

  "ability_estimate": {
    "theta": -0.28,
    "standard_error": 0.31,
    "confidence_interval_95": [-0.89, 0.33]
  },

  "cefr_level": "A2",
  "cefr_confidence": "medium",

  "boundary_effect": false,

  "skill_profiles": {
    "vocabulary": {
      "score_percent": 68,
      "cefr_estimate": "B1",
      "items_administered": 14,
      "correct_count": 9
    },
    "grammar": {
      "score_percent": 52,
      "cefr_estimate": "A2",
      "items_administered": 11,
      "correct_count": 6
    }
  },

  "error_patterns": [
    {
      "topic_tag": "past_simple",
      "skill": "grammar",
      "items_attempted": 4,
      "correct_count": 1,
      "accuracy_rate": 0.25,
      "severity": "high"
    }
  ],

  "ai_recommendations": [
    "Ưu tiên luyện Past Simple và Past Continuous trước.",
    "Mở rộng vốn từ Academic Word List (AWL) cấp độ A2-B1."
  ],

  "test_metadata": {
    "items_administered": 25,
    "test_duration_seconds": 1247,
    "algorithm": "CAT-Rasch-1PL",
    "theta_init": -0.5,
    "quadrature_points": 41,
    "prior": "N(0,1)",
    "item_bank_version": "1.0.0",
    "stopping_reason": "max_items_reached"
  }
}
```

**[NOTE]** v3.0: JSON Profile v1 không còn trường định danh trường/tenant do hệ thống đơn trường (xem Mục XVI). Nếu EduZ cần phân biệt nhiều trường thì đó là phạm vi Khóa luận.

---

## VIII. CHIẾN LƯỢC LƯU TRỮ SESSION — DUAL-WRITE (v2.1)

**[CAUTION]** **v2.1 FIX:** Session state chỉ lưu Redis (TTL 3600s) là **thiếu an toàn**. Nếu Redis restart hoặc TTL hết hạn do SV bị gián đoạn mạng dài, toàn bộ phiên thi mất. F-04 ("chống reload mất data") không thể thực hiện được.

### Kiến trúc Dual-Write đề xuất

```
SV Submit câu trả lời
        │
        ├── [Sync] Ghi vào PostgreSQL: bảng session_responses
        │         (ghi ngay, không đợi bài hoàn thành)
        │
        └── [Sync] Cập nhật Redis: θ mới, SE mới, items_used[]
                  (Cache tăng tốc cho câu tiếp theo)

Nếu Redis miss (hết TTL hoặc restart):
        │
        └── Reconstruct session từ PostgreSQL:
              1. Load toàn bộ responses của session_id từ DB
              2. Chạy lại EAP estimation từ đầu
              3── Tiếp tục bài thi từ câu đã làm (không mất)
```

### PostgreSQL Schema bổ sung

```
-- Bảng session chính
CREATE TABLE test_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID NOT NULL REFERENCES users(id),   -- v3.0: UUID (khớp FK users và FK kỳ thi)
    exam_round_id   UUID NOT NULL,                        -- v3.0: phiên luôn thuộc một kỳ thi
    expires_at      TIMESTAMPTZ NOT NULL,                 -- v3.0: min(started_at + duration, closes_at), tính 1 lần
    status          VARCHAR(20) DEFAULT 'in_progress',
    theta_final     FLOAT,
    se_final        FLOAT,
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ,
    stopping_reason VARCHAR(50)
);

-- Ghi từng response ngay khi submit — không đợi bài hoàn thành
CREATE TABLE session_responses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES test_sessions(id),
    item_id         UUID REFERENCES items(id),
    response        CHAR(1) NOT NULL,        -- 'A' | 'B' | 'C' | 'D'
    is_correct      BOOLEAN NOT NULL,
    theta_after     FLOAT NOT NULL,          -- θ sau khi cập nhật EAP
    se_after        FLOAT NOT NULL,
    response_time_ms INT,
    answered_at     TIMESTAMPTZ DEFAULT NOW()
);
```

**[NOTE]** v3.0: student_id đổi từ VARCHAR(50) sang UUID để khớp FK; giá trị status của phiên theo enum SessionStatus trong schema.prisma (chữ hoa: IN_PROGRESS, COMPLETED, ABANDONED...). Ràng buộc "mỗi SV chỉ một phiên IN_PROGRESS" giữ theo Quyết định #58. Các câu lệnh dưới đây là DDL mô tả; nguồn chân lý thực thi là schema.prisma + custom_migrations.sql. Kiểm tra duration ≤ (closes_at − opens_at) thực hiện ở tầng ứng dụng.

### PostgreSQL Schema bổ sung v3.0 — Người dùng & Kỳ thi

```
-- Bảng users: bổ sung cột (bảng users đã có từ v2.2)
ALTER TABLE users ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE users ADD COLUMN password_changed_at  TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN is_active            BOOLEAN NOT NULL DEFAULT true;  -- khóa tài khoản (DC-23)
-- Hệ thống đơn trường (DC-19): không có bảng đơn vị/trường, không có cột khóa theo trường ở bất kỳ bảng nào.

-- Kỳ thi
CREATE TABLE exam_rounds (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name             VARCHAR(200) NOT NULL,
    created_by       UUID NOT NULL REFERENCES users(id),   -- Admin tạo kỳ
    opens_at         TIMESTAMPTZ NOT NULL,
    closes_at        TIMESTAMPTZ NOT NULL,
    duration_minutes INT NOT NULL DEFAULT 45,                -- phút làm bài của kỳ (DC-20, DC-25)
    status           VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- DRAFT | SCHEDULED | OPEN | CLOSED
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_exam_round_window   CHECK (closes_at > opens_at),
    CONSTRAINT ck_exam_round_duration CHECK (duration_minutes BETWEEN 5 AND 180)
);

-- Danh sách sinh viên thi của kỳ
CREATE TABLE exam_round_participants (
    round_id   UUID NOT NULL REFERENCES exam_rounds(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    note       VARCHAR(255),
    added_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (round_id, student_id)
);

-- Ràng buộc DB: SV chỉ có phiên trong kỳ mà mình thuộc danh sách
ALTER TABLE test_sessions
  ADD CONSTRAINT fk_session_participant
  FOREIGN KEY (exam_round_id, student_id) REFERENCES exam_round_participants (round_id, student_id);

-- 1 phiên/kỳ/SV, trừ phiên ABANDONED (DC-08)
CREATE UNIQUE INDEX uq_session_round_student
  ON test_sessions (exam_round_id, student_id) WHERE status <> 'ABANDONED';
```

**[NOTE] Tạo tài khoản (DC-24): MSSV lưu ở student_profiles.student_code (UNIQUE) và Mã GV lưu ở teacher_profiles.teacher_code (UNIQUE, VARCHAR(50)); cả hai bảng đã có trong schema.prisma nên tạo tài khoản SV/GV không cần thêm bảng hay cột. ADMIN không bắt buộc có teacher_profiles. duration_minutes là NOT NULL DEFAULT 45 nên không còn trường hợp NULL hay giá trị thay thế khi đọc.**

### Redis Key Schema (L1 Cache — không phải Source of Truth)

```
cat:session:{session_id}  →  {
  theta: float,
  se: float,
  items_administered: string[],
  status: 'in_progress' | 'completed',
  last_updated: timestamp
}
TTL: 7200 giây (2 giờ — tăng lên để dễ tiếp tục bài nếu gián đoạn mạng)
```

### Redis Key bổ sung v3.0 (lưới tạm import, OTP)

```
import:accounts:{adminId}:{kind} →  lưới tạm import tài khoản, kind = STUDENT | TEACHER (TTL ~30 phút, làm mới mỗi lần thêm file; tên khóa: đề xuất)
import:roster:{adminId}:{roundId} →  lưới tạm import danh sách thi của một kỳ (tên khóa: đề xuất)
pwreset:otp:{email}              →  { otpHash, attempts }  TTL 10 phút (tên khóa: đề xuất)
import:items:{adminId}          →  lưới tạm import đề (TTL ~30 phút; chỉ khi bấm Lưu mới tạo item_batches + items; tên khóa: đề xuất)
bull:{mail|item-generation|item-check|review-reminder}  →  hàng đợi BullMQ (gửi email, sinh lô, kiểm lô, nhắc hạn; tên hàng đợi: đề xuất)
```

Lưới tạm và OTP chỉ nằm trong Redis, không có bảng PostgreSQL tương ứng (không thêm bảng import_batches hay bảng token). Hết TTL ⇒ lỗi IMPORT_GRID_EXPIRED (410) hoặc INVALID_RESET_OTP (400). Vòng 3: lưới tạm import đề cũng chỉ nằm trong Redis; bảng item_batches (Mục 6.2b) là bảng của lô câu hỏi và chỉ được tạo khi bấm Lưu, không phải nơi lưu lưới. Hết TTL lưới import đề ⇒ IMPORT_GRID_EXPIRED (410).

---

## IX. ĐẶC TẢ CHỨC NĂNG

### Tiểu Luận — Scope Đã Xác Định

| **ID** | **Tính năng** | **Mô tả** | **Ưu tiên** |
| --- | --- | --- | --- |
| F-01 | Auth & Identity | JWT auth, đăng nhập email + mật khẩu (argon2); bắt buộc đổi mật khẩu lần đầu (mustChangePassword); phân quyền theo role (STUDENT/TEACHER/ADMIN) | P0 |
| F-02 | Item Bank — quản lý câu hỏi và vòng đời | Câu hỏi vào ngân hàng chỉ qua lô (F-23, F-24) và đi một chiều DRAFT → FIRST_APPROVED → SECOND_APPROVED → FINAL_APPROVED (REJECTED: người loại; AI_REJECTED: máy loại). Không có form thêm từng câu; GV không import; GV vai A được sửa nội dung/đáp án/giải thích câu được giao; Admin không sửa nội dung câu; câu FINAL_APPROVED cấm sửa (#64); chỉ FINAL_APPROVED được CAT chọn. Thay mô tả "Admin tự tạo, tự duyệt" của v3.0 vòng 1-2 (DC-29, DC-39) | P0 |
| F-03 | CAT Engine | Rasch 1PL, EAP (lưới đều 41 điểm), b-matching selection | P0 |
| F-04 | Test Session — Dual-Write | Redis cache + PostgreSQL source of truth, chống mất data | P0 |
| F-05 | AI Tutor Explainer | Gemini giải thích đúng/sai sau bài thi; giải thích được AI sinh cùng lúc sinh câu hỏi (cùng lời gọi G2), lưu bảng explanations gắn Item và dùng chung mọi SV (DC-31; #60, #63), không sinh lazy theo lần xem | P0 |
| F-06 | Language Profile v1 | JSON output: skill scores + error patterns | P0 |
| F-07 | Profile API Endpoint | GET /api/v1/placement-profiles/{student_id} | P0 |
| F-08 | Student Result Dashboard | Radar chart, CEFR level, gợi ý cải thiện | P1 |
| F-09 | Teacher Class Report | Phân phối CEFR, error pattern toàn lớp, lọc theo kỳ thi, export CSV (GV thường và Admin xem) | P1 |
| F-10 | AI Question Tagging | AI gán topic_tag tự động | P2 |
| F-18 | Tạo tài khoản SV và GV (từng người hoặc import) | Admin tạo từng người bằng form (SV: MSSV, họ tên, email; GV: Mã GV, họ tên, email) hoặc tải một/nhiều file .xlsx (chọn loại SV/GV) vào lưới tạm rồi bấm Lưu; cả hai cách sinh mật khẩu tạm, mustChangePassword = true, gửi email sau khi lưu (UCADM08, UCADM09; DC-24) | P0 (đề xuất) |
| F-19 | Quản lý kỳ thi | Admin tạo/sửa/công bố/đóng kỳ; durationMinutes; trạng thái DRAFT/SCHEDULED/OPEN/CLOSED; theo dõi dự thi (UCADM15, UCADM17) | P0 (đề xuất) |
| F-20 | Import danh sách sinh viên thi | Admin tải file .xlsx MSSV vào lưới tạm của kỳ; bấm Lưu mới ghi (UCADM16) | P0 (đề xuất) |
| F-21 | Đổi / Quên mật khẩu | POST change-password; mustChangePassword; quên mật khẩu bằng OTP 6 số qua email (UCSV08, UCSV09) | P0 (đề xuất) |
| F-22 | Quản lý tài khoản SV & GV | Admin tạo từng tài khoản SV/GV, xem/sửa/khóa/mở khóa, gửi lại mật khẩu tạm; nâng/thu hồi quyền Admin (UCADM09) | P1 (đề xuất) |
| F-23 | Tạo lô câu hỏi bằng AI | Admin nhập skill, CEFR, topic (tùy chọn), N; chạy nền BullMQ: lấy câu mẫu few-shot, sinh dư kèm giải thích trong cùng lời gọi, AI check C1, bù phần thiếu; qua LLM Gateway, có trần chi phí mỗi lô (UCADM11; DC-27, DC-31, DC-45) | P0 (đề xuất) |
| F-24 | Import đề từ file (lưới tạm) | Chỉ Admin; tải một hoặc nhiều file .xlsx vào lưới tạm, dòng lỗi/trùng bị loại kèm popup, bấm Lưu mới tạo lô source IMPORTED; AI check C2; dòng thiếu giải thích được AI sinh bổ sung (UCADM12; DC-22, DC-28, DC-32) | P0 (đề xuất) |
| F-25 | Giao việc, chia đều, hạn và nhắc | Admin chọn nhóm A (≥ 1 GV) và một GV B không thuộc A, reviewDays, confirmDays; xem trước rồi chia đều; hạn cuối ngày; nhắc trước 24 giờ; chỉnh hạn, giao lại, ép gửi gói (UCADM13; DC-37, DC-38, DC-40, DC-41) | P0 (đề xuất) |
| F-26 | GV vai A: duyệt và gửi gói | Hộp việc chỉ chứa câu giao cho mình; sửa nội dung/đáp án/giải thích, Duyệt (FIRST_APPROVED) hoặc Từ chối (REJECTED, không lý do); sau mỗi lần sửa kiểm lại luật cứng + T1–T2; quyết hết câu mới Gửi cho B, mỗi A một gói (UCGV14; DC-33, DC-42, DC-43) | P0 (đề xuất) |
| F-27 | GV vai B: confirm gói | Chỉ đọc; Xác nhận (SECOND_APPROVED) hoặc Loại bỏ (REJECTED) từng câu, hoặc "Xác nhận tất cả câu còn lại"; không sửa, không trả về A (UCGV15; DC-33, DC-40) | P0 (đề xuất) |
| F-28 | Kiểm tra cuối (C3) và Import vào ngân hàng | Khi lô READY_TO_FINALIZE, Admin bấm Kiểm tra (C3 chạy theo delta), xử lý lỗi cứng/mềm, rồi Import ⇒ FINAL_APPROVED; Import bị khóa khi chưa có báo cáo C3 còn hiệu lực (UCADM14; DC-44, DC-45) | P0 (đề xuất) |

**[NOTE]** F-18 đến F-22 là chức năng bổ sung của v3.0 (F-18 mở rộng ở vòng 2: tạo tài khoản cho cả SV và GV, tạo từng người gộp vào UCADM09 — đề xuất, ít UC mới nhất), đánh số tiếp sau F-17 vì F-11 đến F-17 đã thuộc phạm vi Khóa luận; mức ưu tiên ghi "đề xuất" chờ nhóm xác nhận. F-01 và F-02 được sửa theo DC-02, DC-18, DC-19. F-23 đến F-28 là chức năng bổ sung của vòng 3 (14/10/2026), kéo phần ai-question-generator (F-11) từ Khóa luận vào Tiểu luận; tên, mức ưu tiên và mã UC đều là đề xuất. Phạm vi tăng phải được ghi vào COMMITMENT_BASELINE.md trước khi ký (R15, Q-11). F-02 và F-05 được sửa theo DC-29, DC-31, DC-39.

### Khóa Luận — Scope Mở Rộng

| **ID** | **Tính năng** | **Mô tả** |
| --- | --- | --- |
| F-11 | AI Question Generator | Đã kéo vào Tiểu luận ở v3.0 vòng 3: xem F-23 đến F-28. Luồng mới là Admin tạo lô bằng AI hoặc import, AI check, duyệt hai vòng GV A và B, Admin import (không còn "GV nhập yêu cầu"). Dòng này giữ lại để truy vết |
| F-12 | IRT Calibration Pipeline | py-irt tinh chỉnh lại b_i từ dữ liệu sử dụng thực tế (session_responses) sau khi hệ thống đã hoạt động; item fit check — không phải bước Cold-Start (xem Mục 6.1/6.4) |
| F-13 | Language Profile v2 | radar, learning_path_suggestion, Writing score |
| F-14 | EduZ Webhook Integration | BullMQ async push Profile sang EduZ |
| F-15 | AI Writing Assessor | Chấm bài viết ngắn (~150 từ), rubric 4 tiêu chí |
| F-16 | Anti-Cheating (In-session) | Tab-switch detection, randomize thứ tự options |
| F-17 | Item Exposure Control | Max-use cap per item per session batch |

---

## IXb. NGHIỆP VỤ IMPORT, KỲ THI & CÂU HỎI (bổ sung v3.0)

**[NOTE]** Mục này đặc tả nghiệp vụ mới của v3.0. Đánh số "IXb" để giữ nguyên số các mục X đến XVII của v2.6 (các tham chiếu chéo không bị lệch); có thể đánh số lại khi xuất bản chính thức. Tên endpoint, module, class và khóa Redis là đề xuất theo kế hoạch Tuần 5; các điểm chưa chốt ghi "chờ chốt" ở Mục 9b.8. Từ vòng 3, mục này còn chứa nghiệp vụ sinh và duyệt câu hỏi (9b.9 đến 9b.18).

### 9b.1. Phạm vi và nguyên tắc

- Hệ thống đơn trường (DC-19). Tài khoản SV và GV chỉ do Admin tạo (từng người trên giao diện hoặc import file), không tự đăng ký (BR-01, DC-24). Đăng nhập chỉ bằng email + mật khẩu (DC-02).

- Sinh viên phải thuộc danh sách của một kỳ thi đang mở mới bắt đầu được phiên thi (DC-07, BR-10); mỗi SV một phiên cho mỗi kỳ, trừ phiên ABANDONED (DC-08).

- Import tài khoản và import danh sách thi đều theo cơ chế "lưới tạm": cộng dồn nhiều file, dòng lỗi bị loại kèm popup, bấm Lưu mới ghi cơ sở dữ liệu (DC-22).

- Mật khẩu tạm sinh khi Lưu và gửi qua email bằng MailPort + SMTP, qua hàng đợi BullMQ có retry (DC-03). Quên mật khẩu bằng OTP 6 số (DC-21). Khóa tài khoản bằng users.is_active (DC-23).

- Ngoài phạm vi Tiểu luận: đa trường, đăng nhập qua hệ thống ngoài của EduZ (Khóa luận).

- Nghiệp vụ câu hỏi (vòng 3, 14/10/2026): xem 9b.9 đến 9b.18. Mọi tên bảng, endpoint, mã UC, màn hình (đánh số từ S26) và ngưỡng của phần này là đề xuất; Q-7 đến Q-10 còn chờ chốt.

### 9b.2. Vai trò và ma trận quyền

| **Chức năng (Use Case)** | **TEACHER (không được giao)** | **GV vai A** | **GV vai B** | **ADMIN** |
| --- | --- | --- | --- | --- |
| Tạo lô câu hỏi bằng AI; import đề từ file (UCADM11, UCADM12) | ❌ | ❌ | ❌ | ✅ |
| Giao việc, giao lại, chỉnh hạn, ép gửi gói, theo dõi lô (UCADM13) | ❌ | ❌ | ❌ | ✅ |
| Kiểm tra (C3), quyết lỗi mềm, Import cuối (UCADM14) | ❌ | ❌ | ❌ | ✅ |
| Xem "AI đã loại" và thống kê loại theo tầng/GV/lô | ❌ | ❌ | ❌ | ✅ |
| Sửa nội dung/đáp án/giải thích; Duyệt/Từ chối; Gửi gói cho B (UCGV14) | ❌ | ✅ câu giao cho mình | ❌ | ❌ (Admin không sửa nội dung) |
| Xác nhận / Loại bỏ từng câu; xác nhận tất cả câu còn lại (UCGV15) | ❌ | ❌ | ✅ gói gửi cho mình | ❌ |
| Tạo kỳ thi, import danh sách thi, theo dõi dự thi (UCADM15–17) | ❌ | ❌ | ❌ | ✅ |
| Báo cáo lớp (UCGV07/08), tra cứu hồ sơ SV (UCGV09) | ✅ | ✅ | ✅ | ✅ |
| Import tài khoản SV/GV (UCADM08) | ❌ | ❌ | ❌ | ✅ |
| Tạo từng tài khoản SV/GV; quản lý tài khoản SV và GV; nâng/thu hồi Admin (UCADM09) | ❌ | ❌ | ❌ | ✅ |
| Tổng quan hệ thống, cấu hình (UCADM05) | ❌ | ❌ | ❌ | ✅ |
| Đổi / quên mật khẩu (UCSV08/09) | ✅ | ✅ | ✅ | ✅ |

STUDENT chỉ truy cập dữ liệu của chính mình, thi, đổi/quên mật khẩu. Admin là siêu tập của Teacher về xem kết quả; riêng nghiệp vụ câu hỏi, Admin chỉ tạo lô, giao việc, kiểm tra và import, không sửa và không duyệt nội dung (DC-29). Tài khoản Admin đầu tiên tạo bằng seed; không thu hồi Admin cuối cùng (BR-18). Không đủ quyền ⇒ HTTP 403 (BR-16). Vai A và vai B do Admin gán theo từng lô (DC-40) cho GV; ràng buộc đã chốt là trong cùng một lô B không thuộc nhóm A (việc chỉ gán cho tài khoản role TEACHER và việc một GV làm A ở lô này, B ở lô khác là diễn giải của AI, chờ xác nhận). Mã UC: UCADM15–17 và UCADM08–09 tác nhân Admin như trên. Phần câu hỏi vòng 3 (đề xuất): UCADM11 Tạo lô AI, UCADM12 Import đề (lưới tạm), UCADM13 Giao việc và theo dõi, UCADM14 Kiểm tra và import cuối; UCGV14 Duyệt và gửi gói (GV vai A), UCGV15 Confirm gói (GV vai B); bỏ UCGV03 (không còn form thêm từng câu) và thay UCGV05 cũ (duyệt do Admin); UCGV02, UCGV04, UCGV06 sửa theo quyền mới (Mục 9b.16).

### 9b.3. Luồng nghiệp vụ chính

**L0 — Nâng/thu hồi Admin (UCADM09):** Admin mở quản lý tài khoản GV, chọn GV, bấm Nâng lên Admin hoặc Thu hồi ⇒ PATCH /api/v1/users/:id/role ⇒ BE đổi role TEACHER ↔ ADMIN và ghi nhật ký kiểm toán.

**L1 — Admin import tài khoản SV/GV (UCADM08, DC-24):** Admin chọn loại tài khoản (SV hoặc GV) và tải file .xlsx ⇒ POST /users/import/upload?kind=STUDENT|TEACHER ⇒ BE kiểm định dạng/giới hạn, đọc từng dòng, kiểm BR-03 ⇒ gộp vào lưới tạm trong Redis (khóa theo adminId + kind) ⇒ trả {grid[], rejected[{row, code, reason}], added, ignoredDuplicates} ⇒ FE hiện lưới và popup các dòng bị loại (trùng DB ⇒ "tài khoản đã tồn tại") ⇒ Admin tải thêm file hoặc xóa dòng ⇒ bấm Lưu ⇒ POST /users/import/save ⇒ BE tạo tài khoản trong một transaction, sinh mật khẩu tạm, băm argon2, đẩy job email vào BullMQ ⇒ trả {created, queued} (role = STUDENT hoặc TEACHER theo kind) ⇒ xóa lưới. Hết TTL ⇒ 410 IMPORT_GRID_EXPIRED.

**L1b — Admin tạo từng tài khoản (gộp vào UCADM09, đề xuất):** Admin mở form tạo tài khoản, chọn SV hoặc GV, nhập SV: MSSV, họ tên, email; GV: Mã GV (teacherCode), họ tên, email ⇒ POST /students hoặc POST /teachers ⇒ BE kiểm trùng email/MSSV/teacherCode (trùng ⇒ 409, báo lỗi) ⇒ tạo tài khoản role STUDENT/TEACHER, sinh mật khẩu tạm 12 ký tự, băm argon2, mustChangePassword = true ⇒ đẩy job email vào BullMQ sau khi lưu ⇒ trả tài khoản vừa tạo (không kèm mật khẩu).

**L2 — Đăng nhập lần đầu:** SV nhập email + mật khẩu tạm ⇒ POST /auth/login trả token kèm mustChangePassword = true ⇒ FE chuyển đến màn đổi mật khẩu ⇒ guard chặn mọi route khác (403 PASSWORD_CHANGE_REQUIRED) ⇒ POST /auth/change-password ⇒ cờ về false.

**L3 — Admin tạo kỳ và danh sách thi (UCADM15, UCADM16):** Admin tạo kỳ (DRAFT) ⇒ import danh sách thi bằng cùng cơ chế lưới tạm (MSSV lạ hoặc đã có trong kỳ bị loại kèm popup; bấm Lưu mới ghi) ⇒ Công bố (SCHEDULED) ⇒ tới opensAt trạng thái hiệu lực là OPEN (lazy) ⇒ tới closesAt là CLOSED.

**L4 — SV vào thi (UCSV02/03):** Trang chủ liệt kê kỳ của SV (GET /exam-rounds/mine) ⇒ chọn kỳ đang mở ⇒ POST /sessions {examRoundId} ⇒ BE kiểm BR-10 và tính expires_at ⇒ phiên bắt đầu. Sai điều kiện ⇒ 403 NOT_IN_ROUND / 409 ROUND_NOT_OPEN / 409 ROUND_ALREADY_COMPLETED / 409 SESSION_IN_PROGRESS (kèm sessionId, theo #58).

**L5 — Quên mật khẩu (UCSV09):** SV nhập email ⇒ POST /auth/forgot-password ⇒ luôn trả 202 ⇒ nếu email tồn tại, sinh OTP 6 số (băm, lưu Redis TTL 10 phút) và đẩy email ⇒ SV nhập email + OTP + mật khẩu mới ⇒ POST /auth/reset-password ⇒ mustChangePassword = false, hủy mã; sai quá 5 lần ⇒ hủy mã. Không tự đăng nhập sau khi đặt lại.

### 9b.4. Cơ chế lưới tạm (import grid)

- Mỗi lần tải file, BE phân tích và gộp vào lưới tạm của người thao tác (Redis; khóa theo người dùng + loại import [+ loại tài khoản kind = STUDENT | TEACHER với import tài khoản] [+ kỳ thi]; TTL khoảng 30 phút, làm mới mỗi lần thêm). Chưa ghi PostgreSQL.

- Dòng lỗi bị loại khỏi lưới và hiện popup liệt kê số dòng cùng lý do. Dòng đã có trong lưới thì bỏ qua (chỉ thêm dòng chưa có).

- Admin có thể xóa từng dòng hoặc xóa cả lưới. Chỉ khi bấm Lưu mới ghi cơ sở dữ liệu (một transaction); Lưu khi lưới rỗng bị từ chối (IMPORT_GRID_EMPTY).

- Không còn bước preview/confirm, không còn cơ chế all-or-nothing hay trạng thái SKIPPED của các bản nháp trước.

| **Loại import** | **Điều kiện loại dòng khỏi lưới** | **Thông báo popup** |
| --- | --- | --- |
| Tài khoản SV/GV | Thiếu MSSV (file SV) hoặc Mã GV (file GV), Họ tên, Email; email sai định dạng; trùng ngay trong file | Số dòng + lý do cụ thể |
| Tài khoản SV/GV | Email, MSSV hoặc Mã GV đã tồn tại trong cơ sở dữ liệu | "Tài khoản đã tồn tại" |
| Danh sách thi | MSSV không tồn tại trong hệ thống (hoặc không phải STUDENT) | Số dòng + "MSSV không tồn tại" |
| Danh sách thi | MSSV đã có trong kỳ | "Đã có trong kỳ" |
| Cả hai | Dòng đã có sẵn trong lưới | Bỏ qua (không tính lỗi) |

Giới hạn file (mặc định đề xuất MD-08): chỉ .xlsx, tối đa 2 MB, tối đa 1000 dòng dữ liệu, dòng đầu là tiêu đề, chỉ đọc giá trị (bỏ công thức/macro). Cột import tài khoản: file SV: A = MSSV, B = Họ tên, C = Email; file GV: A = Mã GV (teacherCode), B = Họ tên, C = Email. Cột import danh sách thi: A = MSSV, B = Ghi chú (tùy chọn, tối đa 255 ký tự). Chuẩn hóa: cắt khoảng trắng, email về chữ thường. File mẫu chỉ chứa dữ liệu giả.

Mật khẩu tạm (MD-10, áp dụng cho SV lẫn GV, cả tạo từng người và import): 12 ký tự ngẫu nhiên từ crypto.randomInt, băm argon2, sinh lúc bấm Lưu, mustChangePassword = true; không được ghi vào log, tài liệu hay ví dụ thật.

### 9b.5. Máy trạng thái kỳ thi (ExamRoundStatus)

| **Từ** | **Sang** | **Điều kiện** |
| --- | --- | --- |
| DRAFT | SCHEDULED | Admin công bố; cần ít nhất 1 SV trong danh sách (điều kiện về opensAt chờ chốt theo BR-08) |
| SCHEDULED | OPEN | Tới opensAt (chuyển kiểu lazy) |
| OPEN | CLOSED | Tới closesAt, hoặc Admin đóng thủ công |
| DRAFT | CLOSED | Hủy kỳ |

Không quay lui trạng thái. Hàm effectiveStatus(round, now) là nguồn duy nhất cho mọi quyết định (BR-10); cột status chỉ được ghi lại khi có truy cập (lazy, không dùng scheduler) — DC-10. closes_at là hạn cứng: phiên bị đóng tại closes_at theo luật K5 (Mục 4.5).

### 9b.6. Quy tắc nghiệp vụ (Business Rules)

| **Mã** | **Quy tắc** |
| --- | --- |
| BR-01 | Tài khoản sinh viên và giảng viên chỉ do Admin tạo (từng người trên giao diện hoặc import file); không tự đăng ký. |
| BR-02 | Email duy nhất toàn hệ thống (không phân biệt hoa thường); MSSV (student_code) và Mã GV (teacher_code) duy nhất toàn hệ thống. |
| BR-03 | Dòng import tài khoản hợp lệ khi MSSV (file SV) hoặc Mã GV (file GV), Họ tên, Email không rỗng; email đúng định dạng; không trùng trong lưới hiện có; không trùng trong cơ sở dữ liệu. Dòng không hợp lệ bị loại khỏi lưới và báo qua popup. |
| BR-04 | Lưu theo lưới: nút Lưu ghi mọi dòng đang có trong lưới trong một transaction; dòng lỗi/đã tồn tại không vào lưới nên không chặn Lưu; Lưu khi lưới rỗng bị từ chối. |
| BR-05 | Tài khoản mới: role = STUDENT (file/form SV) hoặc TEACHER (file/form GV), authProvider = LOCAL, mustChangePassword = true. Email chỉ gửi sau khi bấm Lưu (import) hoặc sau khi tạo thành công (tạo từng người); gửi thất bại sau retry ⇒ ghi trạng thái "chưa gửi" để Admin xem được, không rollback tài khoản. |
| BR-06 | Đổi mật khẩu: mật khẩu mới khác mật khẩu hiện tại; độ dài tối thiểu 8 ký tự (đề xuất — chờ chốt Q-4); sau thành công mustChangePassword = false và cấp lại token. |
| BR-07 | Chỉ Admin tạo/sửa/công bố/đóng kỳ và import danh sách thi; GV thường chỉ xem kết quả (và xử lý các câu hỏi được giao, BR-21 đến BR-30). |
| BR-08 | opensAt < closesAt; kỳ DRAFT sửa tự do; sau SCHEDULED chỉ cho sửa tên và kéo dài closesAt (đề xuất — chờ chốt); không sửa kỳ CLOSED. |
| BR-09 | Danh sách thi của một kỳ chỉ gồm tài khoản role = STUDENT đã tồn tại. |
| BR-10 | Bắt đầu phiên chỉ hợp lệ khi: SV thuộc danh sách của kỳ được chọn; kỳ ở trạng thái hiệu lực OPEN tại thời điểm hiện tại; SV chưa có phiên IN_PROGRESS (409 theo #58); SV chưa có phiên COMPLETED trong kỳ đó. |
| BR-11 | expires_at tính một lần lúc bắt đầu phiên theo DC-20. Quá expires_at ⇒ luật K5/#77 (≥ 8 câu ⇒ COMPLETED + TIMEOUT; ít hơn ⇒ ABANDONED). |
| BR-12 | Admin đóng thủ công kỳ khi còn phiên đang chạy: phiên đang chạy vẫn theo expires_at, chỉ chặn phiên mới (đề xuất — chờ chốt Q-2). |
| BR-13 | Báo cáo lớp (UCGV07/08, UCADM05) lọc được theo kỳ; mặc định hiển thị toàn hệ thống. |
| BR-14 | Quên mật khẩu: phản hồi luôn như nhau dù email có tồn tại hay không; rate limit theo email + IP; OTP dùng một lần, hiệu lực 10 phút, tối đa 5 lần nhập sai (DC-21). |
| BR-15 | Mọi import ghi nhật ký kiểm toán tối thiểu: ai, khi nào, số dòng, kết quả (không ghi mật khẩu). |
| BR-16 | Phân quyền theo role và theo phân công: TEACHER xem báo cáo lớp và hồ sơ SV, và chỉ xử lý câu/gói được giao cho mình (vai A hoặc B); ADMIN làm mọi chức năng quản trị (không sửa nội dung câu) và chức năng xem của Teacher; STUDENT chỉ dữ liệu của mình. Không đủ quyền ⇒ 403 (NOT_ASSIGNED với việc không được giao). |
| BR-17 | Admin quản lý tài khoản giảng viên: tạo, sửa, khóa/mở khóa; nâng TEACHER → ADMIN và thu hồi ADMIN → TEACHER. Admin không tự thu hồi quyền của chính mình. |
| BR-18 | Nâng/thu hồi Admin ghi nhật ký kiểm toán; không thu hồi nếu đó là Admin cuối cùng (đề xuất); token cũ của người bị đổi quyền phải mất hiệu lực quyền cũ. |
| BR-19 | Quản lý tài khoản (SV và GV): khóa tài khoản ⇒ không đăng nhập được, phiên IN_PROGRESS xử lý theo K5; không xóa cứng tài khoản đã có phiên/hồ sơ (chỉ khóa). Gửi lại mật khẩu tạm ⇒ sinh mật khẩu mới, mustChangePassword = true. |
| BR-20 | Tạo từng tài khoản (UCADM09, đề xuất): SV nhập MSSV, họ tên, email; GV nhập Mã GV, họ tên, email; trùng email/MSSV/Mã GV ⇒ từ chối và báo lỗi (HTTP 409; mã lỗi cụ thể chờ chốt). Sinh mật khẩu tạm 12 ký tự, argon2, mustChangePassword = true, gửi email qua MailPort/BullMQ sau khi lưu — giống import. Import không cập nhật tài khoản có sẵn. |
| BR-21 | Câu hỏi chỉ vào ngân hàng qua lô (AI sinh hoặc Admin import file). Không có form thêm từng câu; GV không import; Admin không sửa nội dung câu (DC-28, DC-29, DC-32). |
| BR-22 | Giao việc: nhóm A có ít nhất 1 GV (khuyên ≥ 2); phải chọn đúng một GV B và B không thuộc nhóm A (vi phạm ⇒ 409 CONFIRMER_IN_REVIEW_GROUP); reviewDays và confirmDays ≥ 1; lô phải ở READY_TO_ASSIGN (DC-40, DC-41; Q-5 mặc định). |
| BR-23 | Chia đều: sắp các câu DRAFT theo (skill, CEFR, thứ tự sinh) rồi giao vòng tròn cho từng GV A; số câu mỗi GV chênh nhau tối đa 1. |
| BR-24 | Hạn: A có due_at = cuối ngày (ngày giao + reviewDays); mỗi gói của B có due_at = cuối ngày (ngày gửi gói + confirmDays); giờ chốt 23:59:59 giờ Việt Nam (cấu hình); Admin chỉnh được cho việc chưa xử lý. Nhắc bằng job trễ BullMQ trước hạn 24 giờ, mỗi nhóm (lô, bước, GV, gói) một lần. Quá hạn chỉ cảnh báo, không tự đổi trạng thái hay tự giao lại (Q-2, Q-3, Q-4 mặc định). |
| BR-25 | Gửi gói: A chỉ bấm Gửi cho B khi mọi câu được giao đã có quyết định (Duyệt hoặc Từ chối), ngược lại ⇒ 409 PACKAGE_INCOMPLETE; A gửi một lần, mỗi A một gói; câu A loại không vào gói; sau khi gửi A không sửa các câu trong gói. |
| BR-26 | GV vai B chỉ đọc: Xác nhận hoặc Loại bỏ từng câu, hoặc "Xác nhận tất cả câu còn lại" (chỉ ảnh hưởng câu chưa quyết, ghi log hành động hàng loạt). B không sửa nội dung và không có thao tác trả về A (DC-33). |
| BR-27 | Sau mỗi lần A sửa, hệ thống chạy lại luật cứng và T1–T2 trên bản sửa; hỏng hoặc trùng ⇒ chặn Duyệt (422 INVALID_AFTER_EDIT / DUPLICATE_AFTER_EDIT). |
| BR-28 | Import chỉ khi lô ở READY_TO_FINALIZE (mọi gói DONE hoặc mọi hạn đã qua) và có báo cáo C3 còn hiệu lực (409 FINAL_CHECK_REQUIRED / FINAL_CHECK_STALE / BATCH_NOT_READY_TO_FINALIZE); lúc Import vẫn chạy lại T1–T2 nhanh chống tranh chấp; câu chưa xử lý không được import (DC-44). |
| BR-29 | Câu loại: người loại ⇒ REJECTED, không lưu lý do (#56); máy loại ⇒ AI_REJECTED, lưu mã lý do, chỉ Admin xem và không đưa cho GV (DC-43). Lỗi cứng ở C3 ⇒ AI_REJECTED; lỗi mềm ⇒ Admin quyết Import (ghi ACCEPT_FLAG) hoặc Loại (REJECTED). |
| BR-30 | Trạng thái Item chỉ đi một chiều, không có đường quay lại; FINAL_APPROVED không sửa (#64); irt_b hợp lệ trong [−4, +4] (cấu hình, DC-34); câu mới calibrated = false, irt_b khởi tạo theo trung bình irt_b của các câu mẫu hoặc giá trị file (nếu có). |

### 9b.7. Mã lỗi nghiệp vụ

| **Mã lỗi** | **HTTP** | **Ngữ cảnh** |
| --- | --- | --- |
| PASSWORD_CHANGE_REQUIRED | 403 | Tài khoản còn mustChangePassword gọi route ngoài change-password / me / logout |
| NOT_IN_ROUND | 403 | SV không thuộc danh sách của kỳ được chọn |
| ROUND_NOT_OPEN | 409 | Kỳ chưa mở hoặc đã đóng tại thời điểm bắt đầu phiên |
| ROUND_ALREADY_COMPLETED | 409 | SV đã có phiên COMPLETED trong kỳ |
| SESSION_IN_PROGRESS | 409 | SV đang có phiên IN_PROGRESS (kèm sessionId) |
| IMPORT_GRID_EXPIRED | 410 | Lưới tạm đã hết TTL |
| IMPORT_GRID_EMPTY | 422 | Bấm Lưu khi lưới rỗng |
| IMPORT_FILE_INVALID | 400 / 413 | File sai định dạng, quá dung lượng hoặc quá số dòng |
| INVALID_RESET_OTP | 400 | OTP sai, hết hạn hoặc đã bị hủy sau 5 lần sai |
| RATE_LIMITED | 429 | Vượt giới hạn tần suất (quên mật khẩu, v.v.) |

Định dạng lỗi hiện tại ({statusCode, message, error, timestamp, path}) chưa có mã ổn định; trường code là việc của backend, SRS chỉ dùng các mã trên. Mã lỗi nghiệp vụ của phần câu hỏi (vòng 3): xem Mục 9b.18.

### 9b.8. Điểm còn mở (chờ chốt)

- Q-2: Admin đóng thủ công kỳ khi còn phiên đang chạy — cắt ngay hay để chạy tới expires_at (đề xuất: để chạy; BR-12).

- Q-4: độ dài mật khẩu tối thiểu và chính sách mật khẩu (đề xuất 8 ký tự; BR-06; Mục 15.3).

- Q-5: nhà cung cấp SMTP cụ thể (hạn mức gửi email chưa kiểm chứng).

- Q-3: định dạng sơ đồ thành phần/triển khai (không thuộc nội dung bản SRS này; để bổ sung sau).

- BR-08 (sửa kỳ sau SCHEDULED) và BR-18 (chặn thu hồi Admin cuối) là đề xuất, chưa có xác nhận riêng.

- Đề xuất vòng 2 (DC-24), chờ xác nhận: UCADM08 mở rộng thành "Import tài khoản (SV, GV)"; tạo từng người gộp vào UCADM09 (không thêm UC mới); tên endpoint POST /students, POST /teachers, tham số kind; mã lỗi khi trùng khi tạo từng người.

- Lưu ý mã: các mã Q-7 đến Q-12 dưới đây thuộc kế hoạch sinh/duyệt đề AI bản 5; chúng khác với các câu hỏi Q-2 đến Q-5 phía trên (thuộc kế hoạch import/kỳ thi).

- Q-7 (chờ chốt): các tham số và ngưỡng — tỷ lệ sinh dư overRate, cỡ mỗi lời gọi, ngưỡng T2 và T3 (cứng, mềm), số vòng bù R, trần lời gọi/token mỗi lô, số ngày dọn AI_REJECTED. Đặt trong cấu hình, hiệu chỉnh sau thử nghiệm nhỏ; chưa có số liệu đo.

- Q-8 (chờ chốt): nguồn ngân hàng tham chiếu cho few-shot và điều khoản bản quyền khi phân phối lại cho SV (kiểm bộ Tuần 3: CEFR-J, CLOTH; hỏi GVHD nếu cần).

- Q-9 (chờ chốt): mô hình embedding, hạn mức và chi phí — chưa kiểm chứng; phải xác minh trong tài liệu nhà cung cấp, qua LLM Gateway, trước khi code.

- Q-10 (chờ chốt): pg_trgm có bật được trên image Postgres staging không; nếu không, T2 tính trong ứng dụng.

- Q-11 (chưa thực hiện): phạm vi và thời gian — sinh đề AI nay vào Tiểu luận, làm đủ T3 và G5; cập nhật COMMITMENT_BASELINE.md trước khi ký (gate G1, hết Tuần 6) và ghi rủi ro trễ (R15). Q-12 (chưa thực hiện): sửa CLAUDE.md theo khoảng irt_b [−4, +4] và kiểm tác động chọn câu CAT bằng test.

- Đã chấp nhận theo mặc định của kế hoạch bản 5: Q-1 chọn O2 (lỗi cứng ở C3 tự AI_REJECTED, lỗi mềm Admin quyết); Q-2 (câu quá hạn nằm lại lô, Admin xử lý thủ công); Q-3 (hạn của B tính từ ngày gửi gói); Q-4 (23:59:59 giờ Việt Nam, nhắc ngay nếu hạn dưới 24 giờ lúc giao); Q-5 (nhóm A ≥ 1 GV, B bắt buộc); Q-6 (tên AI_REJECTED và IMPORTED). Các tên và con số này vẫn là đề xuất của AI cho tới khi nhóm xác nhận lại.

### 9b.9. Phạm vi và vòng đời câu hỏi (vòng 3)

Từ vòng 3 (DC-27 đến DC-45), câu hỏi chỉ vào Item Bank qua một lô (batch) và đi một chiều: Admin tạo lô bằng AI hoặc tự import file ⇒ AI check ⇒ Admin xem kết quả rồi bấm Giao việc ⇒ GV vai A sửa/duyệt/từ chối ⇒ A xong phần mình thì gửi một gói cho GV vai B ⇒ B xác nhận hoặc loại từng câu ⇒ khi cả lô xong hoặc quá hạn, Admin bấm Kiểm tra (AI check lần cuối) ⇒ Admin Import ⇒ FINAL_APPROVED. Không có đường quay lại: B không trả về A, câu rớt C3 không trả về A.

Không ai thêm từng câu bằng form (bỏ UCGV03); GV không import; Admin không soạn, không sửa và không duyệt nội dung câu, chỉ quản lý lô, giao việc, kiểm tra và import.

```
Admin tạo lô (AI sinh) hoặc import file
        │
        ▼
[C1 / C2: AI check] ── rớt ──► AI_REJECTED
        │ qua
        ▼
DRAFT ── Admin bấm Giao việc ──► GV vai A duyệt
        │ Duyệt                      │ Từ chối
        ▼                            ▼
FIRST_APPROVED                    REJECTED
        │ A quyết hết câu, bấm Gửi cho B (mỗi A một gói)
        ▼
GV vai B:  Xác nhận ──► SECOND_APPROVED
           Loại bỏ  ──► REJECTED
        │ cả lô xong hoặc quá hạn
        ▼
Admin bấm Kiểm tra (C3)
   ├─ qua ───────► Admin Import ──► FINAL_APPROVED
   ├─ lỗi cứng ──► AI_REJECTED
   └─ lỗi mềm ───► Admin quyết: Import (ghi ACCEPT_FLAG) hoặc Loại (REJECTED)
```

### 9b.10. Trạng thái câu hỏi và trạng thái lô

| **Trạng thái Item** | **Ý nghĩa** | **Ai/cái gì chuyển** |
| --- | --- | --- |
| DRAFT | Đã qua AI check, chờ Admin giao việc, hoặc đã giao và chờ A duyệt | Hệ thống (sau C1/C2) |
| FIRST_APPROVED (mới) | A đã duyệt; nằm trong "phần của A" cho đến khi A gửi gói; sau khi gửi thì chờ B | A bấm Duyệt |
| SECOND_APPROVED (mới) | B đã xác nhận; chờ Admin kiểm tra và import | B bấm Xác nhận (từng câu hoặc "tất cả câu còn lại") |
| FINAL_APPROVED (đổi tên từ trạng thái đã duyệt cũ) | Đã vào ngân hàng, dùng cho CAT, cấm sửa (#64); calibrated = false | Admin bấm Import (ghi approved_by, approved_at) |
| REJECTED | Người loại: A, B hoặc Admin (khi quyết lỗi mềm). Không lưu lý do (#56) | A, B, Admin |
| AI_REJECTED (mới, tên là đề xuất) | Máy loại ở C1, C2 hoặc C3; lưu mã lý do (lý do của hệ thống, khác #56 vốn nói về lý do của người) | Hệ thống |

Hai trạng thái cũ "chờ duyệt" và "đã duyệt" (tên cũ) bị bỏ; không còn giá trị nào ngoài sáu giá trị trên.

Trạng thái của lô (item_batches.status, đề xuất): GENERATING hoặc IMPORTING ⇒ CHECKING ⇒ READY_TO_ASSIGN ⇒ IN_REVIEW ⇒ READY_TO_FINALIZE (mọi gói đã xong hoặc mọi hạn đã qua) ⇒ FINAL_CHECKED (sau khi Admin bấm Kiểm tra) ⇒ DONE (mọi câu ở trạng thái cuối: FINAL_APPROVED, REJECTED, AI_REJECTED). Lỗi: FAILED; hết ngân sách: PARTIAL.

### 9b.11. Tạo lô: bằng AI và bằng import file

**Bằng AI (UCADM11).** Đầu vào: skill, cefr_level, topic_tag (tùy chọn), N. Nhóm GV chưa chọn ở bước này, chỉ chọn lúc Giao việc (DC-41). Chạy nền BullMQ; Admin nhận batchId và xem tiến độ.

| **Bước** | **Việc** | **Tốn API?** |
| --- | --- | --- |
| G1 | Lấy k = 3 đến 5 câu mẫu cùng bộ lọc từ ngân hàng tham chiếu (few-shot); k cấu hình | Không |
| G2 | Sinh dư: số câu sinh bằng N nhân (1 + overRate), làm tròn lên, chia thành các lời gọi nhỏ; mỗi lời gọi trả một mảng JSON gồm nội dung, 4 đáp án, đáp án đúng, irt_b gợi ý và giải thích | Có (lời gọi chính) |
| C1 | AI check lần 1 (Mục 9b.12) | Chỉ ở tầng cuối |
| G6 | Bù thiếu: còn ít hơn N thì sinh thêm chỉ phần thiếu, tối đa R vòng (cấu hình); hết R vòng ⇒ báo "thiếu x câu" | Có, nhỏ |
| G7 | Cắt về N; irt_b khởi tạo = trung bình irt_b của k câu mẫu, calibrated = false, source = AI_GENERATED; lưu Explanation | Không |

- Giải thích AI sinh cùng lời gọi G2 và lưu vào bảng explanations gắn Item (DC-31; #60, #63); A xem và sửa, B chỉ xem; C1 tầng 5 và C3 kiểm giải thích khớp đáp án. Không sinh lazy.

- Kiểm soát chi phí: trần số lời gọi/token mỗi lô (BATCH_BUDGET_EXCEEDED); ghi tên và phiên bản mô hình thật của từng lời gọi (TC2.3); đi qua LLM Gateway có dự phòng; cache theo hash prompt. Chưa có số liệu chi phí, độ trễ hay tỷ lệ trùng — đo ở lần chạy thử đầu (chưa đo).

**Bằng import file (UCADM12, chỉ Admin).** Dùng lưới tạm DC-22 (tải nhiều file, dòng lỗi bị loại kèm popup, bấm Lưu mới ghi). Cột .xlsx (đề xuất): Skill, CEFR, Topic, Câu hỏi, A, B, C, D, Đáp án, Giải thích (tùy chọn), Độ khó irt_b (tùy chọn). Bấm Lưu ⇒ tạo lô source = IMPORTED, chạy C2 trên các dòng trong lưới, rồi cùng luồng sau đó. Dòng thiếu giải thích được sinh bổ sung theo nhóm một lượt (chỉ các dòng thiếu).

### 9b.12. Ba điểm AI check (C1, C2, C3)

Nguyên tắc chung (DC-30, DC-45): (1) rẻ trước, đắt sau — luật cứng, băm, pg_trgm chạy trước; embedding và lời gọi AI chỉ chạy cho câu còn sống; (2) gộp nhiều câu vào một lời gọi AI; (3) không tính lại điều đã biết — mỗi câu có content_hash, kết quả gắn với hash và được tái sử dụng khi hash không đổi, kể cả ở lần 3; (4) embedding tính đúng một lần cho mỗi nội dung và lưu item_embeddings; (5) mỗi lần check ghi báo cáo có mã lý do để Admin hiểu và hiệu chỉnh ngưỡng.

**C1 — sau khi AI sinh** (đầu vào chưa đáng tin, lọc nặng nhất; đây là lần duy nhất có số câu dư để loại thoải mái):

| **Tầng** | **Việc** | **Tốn API** | **Kết quả** |
| --- | --- | --- | --- |
| 1. Luật cứng | Đủ 4 đáp án khác nhau, đúng 1 đáp án đúng, độ dài hợp lệ, irt_b trong [−4, +4], đúng skill/CEFR, có giải thích | Không | Hỏng ⇒ AI_REJECTED |
| 2. Trùng T1 | Băm chuẩn hóa so với ngân hàng, câu đang trong mọi lô khác và các câu cùng lô | Không | Trùng ⇒ AI_REJECTED |
| 3. Trùng T2 | pg_trgm trên nội dung + đáp án | Không | ≥ ngưỡng cao: AI_REJECTED; giữa hai ngưỡng: cờ mềm |
| 4. Trùng T3 | Embedding (chỉ câu còn lại), cosine tính trong ứng dụng | Có (embedding) | ≥ ngưỡng: cờ mềm kèm câu bị nghi trùng |
| 5. G5 | Kiểm đáp án độc lập: đưa câu + 4 đáp án (không kèm đáp án đúng) cho AI tự chọn; cùng lời gọi hỏi giải thích có ủng hộ đáp án vừa chọn không | Có (gộp nhóm) | Lệch ⇒ cờ mềm (không loại: AI có thể sai, người sẽ xem) |

**C2 — khi Admin import file có sẵn** (đầu vào do người soạn): không sinh dư, không bù thiếu; luôn có kiểm trùng nội bộ file/lưới; vẫn chạy đủ tầng 1 đến 5 nhưng: tầng 1 thêm kiểm cột bắt buộc, kiểu dữ liệu, giá trị CEFR/Skill hợp lệ và lỗi hiện ngay trên lưới (dòng sai không vào lưới, có popup); tầng 2 đến 4 chạy ngay lúc tải file lên lưới để Admin thấy sớm (trùng dòng đã có trong lưới ⇒ bỏ qua, DC-22); tầng 5 (G5) chạy một lần khi bấm Lưu, không chạy mỗi lần tải thêm file; giải thích thiếu ⇒ sinh bổ sung theo nhóm.

**C3 — trước FINAL_APPROVED, Admin bấm Kiểm tra** (chỉ khi lô ở READY_TO_FINALIZE, DC-44). Mục tiêu khác C1: bắt các hỏng hóc xảy ra sau khi người can thiệp và xung đột với ngân hàng đã thay đổi trong lúc lô chờ; vì vậy chạy theo thay đổi (delta):

| **Kiểm** | **Chạy trên** | **Cách tiết kiệm** | **Loại lỗi** |
| --- | --- | --- | --- |
| Luật cứng (tầng 1) | Mọi câu SECOND_APPROVED | Không tốn API | Cứng |
| Toàn vẹn quy trình | Mọi câu | Không tốn API: A khác B, gói đủ, mọi câu có người duyệt và người confirm, trạng thái đi đúng chiều | Cứng |
| Trùng T1–T2 | Mọi câu, so với ngân hàng hiện tại (có thể có câu mới từ lô khác) và các câu cùng lô | Không tốn API | Cứng (T1, T2 ≥ ngưỡng cao); mềm (giữa hai ngưỡng) |
| Trùng T3 | Câu đã đổi hash hoặc chưa có embedding; còn lại chỉ so với các câu ngân hàng mới thêm kể từ lần check trước | Embedding đã lưu, cosine trong ứng dụng | Mềm |
| G5 + giải thích khớp | Chỉ câu A đã sửa (hash khác hash lúc qua C1/C2) | Câu không sửa dùng lại kết quả lần trước; gộp nhóm | Mềm |
| Thống kê | — | — | Báo cáo: số câu A sửa, tỷ lệ A/B loại |

Kết quả C3 hiển thị cho Admin theo câu (qua / cờ mềm / lỗi cứng, mã lý do, câu bị nghi trùng, bản gốc so với bản đã sửa) và tổng hợp theo gói. Import bị khóa cho đến khi có báo cáo C3 còn hiệu lực (không câu nào đổi và ngân hàng không đổi kể từ lúc kiểm); nếu đổi, hệ thống yêu cầu kiểm lại phần chênh (FINAL_CHECK_STALE).

**Xử lý câu rớt C3 (phương án O2, mặc định đã chấp nhận):** lỗi cứng (cấu trúc, trùng gần như giống hệt) tự chuyển AI_REJECTED; lỗi mềm hiện cho Admin quyết: Import hoặc Loại (REJECTED); câu bị cờ mềm mà Admin chọn Import được ghi ACCEPT_FLAG để truy vết. Hai phương án đã loại: O1 (mọi câu rớt tự AI_REJECTED — loại nhầm câu chỉ bị cờ nhẹ) và O3 (trả lại A để sửa — mở lại vòng lặp, đảo #109). Lý do chọn O2: giữ luồng một chiều; không dồn phán đoán chủ quan cho máy; Admin không sửa nội dung nên không phá tính độc lập.

### 9b.13. Giao việc và chia đều

Điều kiện: lô ở READY_TO_ASSIGN (đã qua C1/C2); Admin xem được số câu còn lại, danh sách "AI đã loại" và cờ mềm. Các bước Admin:

- Bấm Giao việc; chọn nhóm A (một hoặc nhiều GV, khuyên ≥ 2 để chia việc) và đúng một GV B không nằm trong nhóm A (vi phạm ⇒ 409 CONFIRMER_IN_REVIEW_GROUP; thiếu B ⇒ lỗi kiểm tra đầu vào, mã chưa định).

- Đặt hạn: reviewDays (hạn cho A, tính từ ngày giao) và confirmDays (hạn cho B, tính từ ngày mỗi gói được gửi); mỗi số ≥ 1.

- Hệ thống hiện xem trước phân bổ (bảng GV – số câu, theo từng kỹ năng/CEFR); Admin bấm Xác nhận giao.

Cách chia đều: sắp xếp các câu DRAFT theo (skill, cefr, thứ tự sinh) rồi giao vòng tròn: câu thứ i giao cho GV A thứ (i chia dư M), M là số GV A. Nhờ sắp theo skill và CEFR trước, mỗi GV nhận mức trộn đều các loại câu; số câu mỗi GV chênh nhau tối đa 1 (ví dụ 100 câu cho 5 GV là 20 câu mỗi người; 103 câu thì 3 người nhận 21 và 2 người nhận 20).

Sau khi giao: tạo item_review_assignments (mỗi câu một dòng: người nhận, assigned_at, due_at) và tạo mỗi GV A một item_packages ở trạng thái OPEN (confirmer_id = GV B của lô, chưa có sent_at/due_at) — quyết định 16/10/2026; lô chuyển IN_REVIEW; A nhận email nhắc việc qua MailPort (BullMQ) "Bạn có x câu cần duyệt, hạn dd/mm" và thấy việc trong Hộp việc (Tiểu luận không làm chuông thông báo thời gian thực); đặt lịch nhắc. Giao lại: Admin chuyển các câu chưa xử lý của một A cho A khác (hoặc đổi B của gói chưa gửi/chưa xử lý), vẫn ràng buộc B không thuộc nhóm A; hạn tính lại từ ngày giao lại; ghi kiểm toán (REASSIGN).

### 9b.14. Gói, GV vai A, GV vai B, hạn và nhắc

**GV vai A (UCGV14).** Mở "Hộp việc → Cần duyệt", chỉ thấy câu giao cho mình kèm cờ mềm, giải thích, hạn còn lại. Với mỗi câu, A được sửa nội dung/đáp án/giải thích rồi chọn Duyệt (FIRST_APPROVED) hoặc Từ chối (REJECTED, không lưu lý do). Sau mỗi lần sửa, hệ thống chạy lại luật cứng và T1–T2 trên bản sửa; hỏng hoặc trùng ⇒ chặn Duyệt. Khi mọi câu giao cho A đã có quyết định, A bấm Gửi cho B ⇒ gói OPEN của A chuyển SENT (ghi sent_at, tính due_at của B) gồm các câu FIRST_APPROVED của A (gán package_id; câu A loại không vào gói). A không gửi được khi còn câu chưa quyết (PACKAGE_INCOMPLETE); gửi một lần, sau đó không sửa lại.

**GV vai B (UCGV15).** Mở "Hộp việc → Cần confirm", thấy từng gói (một gói cho mỗi A), chỉ đọc; mỗi câu hiện cờ và dấu "A đã sửa" kèm bản gốc so với bản sửa. B xử lý từng câu: Xác nhận (SECOND_APPROVED) hoặc Loại bỏ (REJECTED), hoặc bấm "Xác nhận tất cả câu còn lại" (xác nhận hết câu chưa quyết trong gói; ghi log hành động hàng loạt). B không sửa, không trả về A. Gói xong (DONE) khi mọi câu trong gói có quyết định.

**Hạn và nhắc.** A: due_at = cuối ngày (ngày giao + reviewDays); B: mỗi gói due_at = cuối ngày (ngày gửi gói + confirmDays); giờ chốt 23:59:59 giờ Việt Nam (cấu hình). Admin chỉnh hạn (reviewDays, confirmDays; chỉ áp dụng cho việc chưa xử lý) ⇒ tính lại due_at, hủy và tạo lại lịch nhắc. Nhắc: job trễ BullMQ chạy lúc due_at trừ 24 giờ, nếu nhóm (lô, bước, GV, gói) còn việc chưa xong thì gửi một email nhắc gộp qua MailPort (việc vẫn hiện trong Hộp việc); hạn còn dưới 24 giờ lúc giao/chỉnh ⇒ nhắc ngay một lần; kèm đối chiếu lazy khi mở hộp việc phòng mất job. Quá hạn: chỉ hiển thị "quá hạn" cho Admin và GV (tính lazy), không tự đổi trạng thái hay tự giao lại; Admin chọn chỉnh hạn, giao lại, hoặc ép gửi gói hiện có thay A (FORCE_SEND: gói OPEN chuyển SENT chỉ với các câu A đã FIRST_APPROVED; câu A chưa quyết không vào gói và nằm lại trong lô; ghi item_review_events FORCE_SEND; Admin không sửa nội dung câu).

**Sau khi B confirm.** Câu SECOND_APPROVED nằm chờ trong lô, chưa vào ngân hàng. Khi mọi gói DONE hoặc mọi hạn đã qua ⇒ lô READY_TO_FINALIZE; Admin thấy thống kê (SECOND_APPROVED, REJECTED bởi A/B, AI_REJECTED, chưa xử lý). Admin bấm Kiểm tra (C3), đọc báo cáo, xử lý lỗi mềm, rồi bấm Import ⇒ câu qua (và lỗi mềm Admin chấp nhận) thành FINAL_APPROVED, ghi approved_by, approved_at, có hiệu lực cho CAT, calibrated = false. Câu chưa xử lý khi quá hạn (còn DRAFT hoặc FIRST_APPROVED chưa tới B) không được import; nằm lại trong lô để Admin giao lại với hạn mới hoặc loại thành REJECTED (không cần lý do, không sửa nội dung). Lô chỉ chuyển DONE khi mọi câu đã ở trạng thái cuối; nếu sau Import còn câu chưa xử lý, lô giữ FINAL_CHECKED và việc giao lại đưa lô về IN_REVIEW (đề xuất, chờ chốt — bổ sung nghiệp vụ 16/10/2026).

### 9b.15. Câu bị loại

| **Loại bởi** | **Trạng thái** | **Lưu gì** | **Ai xem** | **Dùng lại?** |
| --- | --- | --- | --- | --- |
| Máy ở C1, C2, C3 | AI_REJECTED | Nội dung + mã lý do + câu bị nghi trùng (nếu có) | Chỉ Admin (tab "AI đã loại") | Không; Admin dùng để chỉnh ngưỡng; dọn sau N ngày (cấu hình, Q-7) |
| GV vai A hoặc B | REJECTED | Nội dung; không lưu lý do (#56) | Admin (danh sách và thống kê theo GV) | Không; muốn bù thì tạo lô mới |
| Admin (lỗi mềm ở C3) | REJECTED | Như trên | Admin | Không |

Câu AI_REJECTED không được đưa cho GV. Thống kê bắt buộc: tỷ lệ loại theo tầng AI, theo A, theo B, để hiệu chỉnh.

### 9b.16. Ma trận quyền nghiệp vụ câu hỏi

| **Hành động** | **Admin** | **GV vai A (đúng người)** | **GV vai B (đúng người)** | **GV khác** | **SV** |
| --- | --- | --- | --- | --- | --- |
| Tạo lô AI, import file, giao việc, giao lại, chỉnh hạn, Kiểm tra, Import, quyết lỗi mềm | ✅ | ❌ | ❌ | ❌ | ❌ |
| Sửa nội dung, Duyệt/Từ chối, Gửi gói | ❌ | ✅ câu của mình | ❌ | ❌ | ❌ |
| Xác nhận/Loại, "xác nhận tất cả còn lại" | ❌ | ❌ | ✅ gói gửi cho mình | ❌ | ❌ |
| Xem "AI đã loại" và thống kê | ✅ | ❌ | ❌ | ❌ | ❌ |

Các UC cũ sửa theo quyền mới (đề xuất, chờ đồng bộ với đặc tả Use Case): UCGV02 (xem/lọc ngân hàng): Admin xem mọi câu của lô kể cả AI_REJECTED; GV chỉ thấy câu/gói được giao (xem chỉ đọc ở màn Ngân hàng câu hỏi của giảng viên /teacher/item-bank và qua Hộp việc). UCGV04 (xem/sửa chi tiết câu): chỉ GV vai A sửa câu được giao khi còn DRAFT; từ FIRST_APPROVED trở đi không sửa; FINAL_APPROVED cấm sửa (#64). UCGV06 (xóa câu Nháp/Từ chối): câu REJECTED và AI_REJECTED giữ trong lô (DC-43), AI_REJECTED dọn theo cấu hình; việc UCGV06 còn tồn tại hay không chờ chốt. UCGV03 (thêm câu bằng form) bỏ; UCGV05 (duyệt) được thay bằng UCGV14, UCGV15.

### 9b.17. Luồng nghiệp vụ câu hỏi L-1 đến L-8

Ký hiệu: A = GV vai A, B = GV vai B, Ad = Admin, H = hệ thống.

**L-1 — Tạo lô bằng AI (UCADM11).** Ad nhập skill, CEFR, topic, N ⇒ H kiểm giới hạn, tạo lô (GENERATING), đẩy job ⇒ worker chạy G1, G2, C1, G6, G7 ⇒ lô READY_TO_ASSIGN (hoặc PARTIAL / FAILED) ⇒ thông báo Ad. Mỗi lời gọi ghi mô hình và token.

**L-2 — Tạo lô bằng import file (UCADM12, đề xuất).** Ad tải một hoặc nhiều file vào lưới (C2 tầng 1 đến 4 chạy ngay) ⇒ xem lưới và popup ⇒ bấm Lưu ⇒ H tạo lô IMPORTED, chạy C2 tầng 5 ⇒ READY_TO_ASSIGN.

**L-3 — Xem kết quả và giao việc (UCADM13, đề xuất).** Ad xem số câu qua, danh sách AI đã loại, cờ ⇒ Giao việc (chọn A, B, reviewDays, confirmDays) ⇒ xem trước phân bổ ⇒ xác nhận ⇒ H tạo assignment, lô IN_REVIEW, thông báo và đặt lịch nhắc.

**L-4 — A duyệt và gửi gói (UCGV14).** A sửa/duyệt/từ chối từng câu (H kiểm lại luật cứng + T1–T2 sau sửa) ⇒ khi hết việc, bấm Gửi cho B ⇒ H tạo gói, đặt due_at của gói, nhắc cho B.

**L-5 — B confirm (UCGV15).** B mở gói ⇒ xử lý từng câu hoặc "xác nhận tất cả còn lại" ⇒ gói DONE.

**L-6 — Theo dõi, chỉnh hạn, giao lại.** Ad xem tiến độ theo gói/GV, chỉnh hạn, giao lại, ép gửi gói thay A.

**L-7 — Kiểm tra và import (UCADM14, đề xuất).** Lô READY_TO_FINALIZE ⇒ Ad bấm Kiểm tra (C3) ⇒ xem báo cáo ⇒ quyết lỗi mềm ⇒ Import (H chạy lại T1–T2 nhanh) ⇒ FINAL_APPROVED.

**L-8 — Quá hạn.** Hiển thị, không tự đổi trạng thái; Ad xử lý như L-6.

### 9b.18. Mã lỗi nghiệp vụ — phần câu hỏi (đề xuất)

| **Mã lỗi** | **HTTP** | **Ngữ cảnh** |
| --- | --- | --- |
| NOT_ASSIGNED | 403 | GV thao tác câu/gói không được giao cho mình (hoặc sai vai A/B) |
| CONFIRMER_IN_REVIEW_GROUP | 409 | GV B được chọn nằm trong nhóm A của cùng lô |
| PACKAGE_INCOMPLETE | 409 | A bấm Gửi cho B khi còn câu chưa quyết |
| FINAL_CHECK_REQUIRED | 409 | Import khi chưa có báo cáo C3 |
| FINAL_CHECK_STALE | 409 | Import khi báo cáo C3 hết hiệu lực (câu hoặc ngân hàng đã đổi sau lúc kiểm) |
| BATCH_NOT_READY_TO_FINALIZE | 409 | Kiểm tra/Import khi lô chưa ở READY_TO_FINALIZE |
| DUPLICATE_AFTER_EDIT | 422 | Bản A sửa bị trùng (T1–T2) ⇒ chặn Duyệt |
| INVALID_AFTER_EDIT | 422 | Bản A sửa vi phạm luật cứng ⇒ chặn Duyệt |
| BATCH_BUDGET_EXCEEDED | 409 | Vượt trần lời gọi/token mỗi lô |
| IMPORT_GRID_EXPIRED | 410 | Lưới tạm import đề hết TTL (mã dùng chung với Mục 9b.7) |

**[NOTE]** Ca test bắt buộc khi code (theo kế hoạch bản 5, Mục 13): giao việc 100 câu cho 5 GV A ra 20 câu mỗi người, 103 câu chênh tối đa 1, B nằm trong nhóm A ⇒ 409; gói chưa quyết hết mà Gửi ⇒ PACKAGE_INCOMPLETE, câu A loại không vào gói, nhiều A ⇒ nhiều gói độc lập; B gọi API sửa hoặc "trả về" ⇒ lỗi; C3 dùng lại kết quả với câu không đổi, chạy lại G5 với câu A sửa, bắt trùng với câu mới vào ngân hàng; Import chỉ khi READY_TO_FINALIZE và C3 còn hiệu lực, hai Admin import cùng lúc không tạo trùng; chỉ FINAL_APPROVED được CAT chọn; irt_b −4 và +4 hợp lệ, ngoài biên bị loại. Chưa chạy ca test nào (chưa có mã).

---

## X. API CONTRACT

```
AUTH
  POST   /api/v1/auth/login
  POST   /api/v1/auth/refresh
  POST   /api/v1/auth/logout
  POST   /api/v1/auth/change-password        # {currentPassword,newPassword}; cho phép khi mustChangePassword
  POST   /api/v1/auth/forgot-password        # {email} -> luôn 202; rate limit
  POST   /api/v1/auth/reset-password         # {email,otp,newPassword}

TEST SESSION
  POST   /api/v1/sessions                    # Tạo phiên thi, body {examRoundId} (BR-10)
  GET    /api/v1/sessions/:id/next-item      # CAT chọn câu tiếp
  POST   /api/v1/sessions/:id/responses      # Ghi response (dual-write)
  GET    /api/v1/sessions/:id/result         # Kết quả sau hoàn thành
  GET    /api/v1/sessions/:id/resume         # Tiếp tục phiên nếu bị gián đoạn

LANGUAGE PROFILE
  GET    /api/v1/placement-profiles/:student_id
  GET    /api/v1/placement-profiles/:student_id/history

CÂU HỎI / ITEM BANK  (v3.0 vòng 3)  [đề xuất]
  # Bỏ POST/PUT/DELETE /items và POST /items/bulk-import của bản cũ (không còn form thêm từng câu; import chuyển sang lưới tạm)
  GET    /api/v1/items , /api/v1/items/:id                  # Admin xem mọi câu; GV chỉ câu được giao

LÔ CÂU HỎI (ADMIN)  [đề xuất]
  POST   /api/v1/item-batches                               # tạo lô AI {skill,cefr,topic,count}
  POST   /api/v1/item-imports/upload                        # multipart "file"; gộp vào lưới tạm
  GET    /api/v1/item-imports/grid
  DELETE /api/v1/item-imports/grid[/:rowKey]
  POST   /api/v1/item-imports/save                          # tạo lô IMPORTED, chạy C2
  GET    /api/v1/item-batches , /api/v1/item-batches/:id
  GET    /api/v1/item-batches/:id/ai-rejected               # tab "AI đã loại"

GIAO VIỆC (ADMIN)  [đề xuất]
  GET    /api/v1/item-batches/:id/assign-preview
  POST   /api/v1/item-batches/:id/assign                    # {reviewerIds,confirmerId,reviewDays,confirmDays}
  POST   /api/v1/item-batches/:id/reassign
  PATCH  /api/v1/item-batches/:id/deadlines
  POST   /api/v1/item-packages/:id/force-send

KIỂM TRA VÀ IMPORT CUỐI (ADMIN)  [đề xuất]
  POST   /api/v1/item-batches/:id/final-check               # chạy C3
  GET    /api/v1/item-batches/:id/final-check               # xem báo cáo C3
  POST   /api/v1/items/:id/decision                         # chấp nhận hoặc loại lỗi mềm
  POST   /api/v1/item-batches/:id/import                    # => FINAL_APPROVED

CHẶNG A (GV vai A)  [đề xuất]
  GET    /api/v1/me/review-tasks
  PATCH  /api/v1/items/:id                                  # sửa nội dung/đáp án/giải thích (câu của mình, DRAFT)
  POST   /api/v1/items/:id/approve | reject
  POST   /api/v1/item-packages/mine/send                    # Gửi cho B

CHẶNG B (GV vai B)  [đề xuất]
  GET    /api/v1/me/confirm-packages
  POST   /api/v1/items/:id/confirm
  POST   /api/v1/items/:id/remove
  POST   /api/v1/item-packages/:id/confirm-all              # xác nhận tất cả câu còn lại

REPORTING
  GET    /api/v1/reports/class-distribution  # ?examRoundId= (TEACHER, ADMIN)
  GET    /api/v1/reports/error-patterns

IMPORT TÀI KHOẢN SV/GV (ADMIN) — lưới tạm, khóa theo (adminId, kind)  [đề xuất]
  POST   /api/v1/users/import/upload?kind=STUDENT|TEACHER   # multipart "file"; gộp vào lưới
  GET    /api/v1/users/import/grid?kind=
  DELETE /api/v1/users/import/grid/:rowKey?kind=
  DELETE /api/v1/users/import/grid
  POST   /api/v1/users/import/save?kind=     # -> {created, queued}

QUẢN LÝ TÀI KHOẢN (ADMIN)  [đề xuất]
  GET    /api/v1/students , /api/v1/teachers # tìm theo MSSV/email, phân trang
  POST   /api/v1/students , /api/v1/teachers          # tạo từng người: SV {studentCode,fullName,email}; GV {teacherCode,fullName,email}; trùng => 409
  PATCH  /api/v1/students/:id , /api/v1/teachers/:id   # {fullName,email}
  POST   /api/v1/students/:id/lock | unlock | resend-temporary-password
  PATCH  /api/v1/users/:id/role              # {role} nâng/thu hồi Admin

KỲ THI  [đề xuất]
  POST/GET  /api/v1/exam-rounds ; GET/PATCH /api/v1/exam-rounds/:id     # ADMIN
  POST   /api/v1/exam-rounds/:id/publish | close                        # ADMIN
  POST   /api/v1/exam-rounds/:id/participants/import/upload             # ADMIN, lưới tạm
  GET    /api/v1/exam-rounds/:id/participants/import/grid
  DELETE /api/v1/exam-rounds/:id/participants/import/grid[/:rowKey]
  POST   /api/v1/exam-rounds/:id/participants/import/save
  GET    /api/v1/exam-rounds/:id/participants                           # theo dõi dự thi (UCADM17)
  DELETE /api/v1/exam-rounds/:id/participants/:studentId                # gỡ SV khi kỳ chưa CLOSED
  GET    /api/v1/exam-rounds/mine                                       # STUDENT: kỳ tôi thuộc + trạng thái hiệu lực
```

Ghi chú v3.0: GET /sessions/active trả thêm expiresAt và thông tin kỳ. Các endpoint nhóm "đề xuất" chưa chốt tên; mã lỗi và quy tắc xem Mục IXb (9b.6, 9b.7). Nhóm câu hỏi (vòng 3) do kế hoạch sinh/duyệt đề AI bản 5 đề xuất; mã lỗi: Mục 9b.18; phân quyền: Mục 9b.16 và 15.4. Không có endpoint nào cho phép giảng viên import đề hoặc Admin sửa nội dung câu.

---

## XI. STACK CÔNG NGHỆ

| **Layer** | **Technology** | **Ghi chú** |
| --- | --- | --- |
| Backend | NestJS (TypeScript) | Modular, DI, Clean Architecture |
| Frontend | Next.js (React/TypeScript) | SSR |
| Database | PostgreSQL | Source of Truth — item bank, sessions, responses |
| Cache | Redis | L1 cache cho CAT session (không phải source of truth) |
| AI | Gemini 1.5 Flash | Sinh câu hỏi + giải thích cùng lúc (Item Generation), Explainer, Question Tagging; gọi qua LLM Gateway có dự phòng (đề xuất) |
| IRT (runtime) | TypeScript tự implement (Phương án A) | EAP trên lưới đều 41 điểm θ ∈ [−4, +4], bước 0.2 (tích phân số kiểu hình thang) |
| IRT (calibration) | py-irt hoặc catR | Chạy offline, expose REST endpoint |
| Infra | Docker + Docker Compose + Nginx |  |
| Async | BullMQ (Redis-backed) | TL (v3.0): gửi email, sinh/kiểm lô câu hỏi, nhắc hạn; KL: push Profile sang EduZ |
| Embedding (T3) | Mô hình embedding — chờ chốt (Q-9) | Chưa kiểm chứng; vector lưu item_embeddings (Float[]), cosine tính trong ứng dụng |
| Lọc trùng T2 | PostgreSQL pg_trgm (GIN) | Chờ chốt (Q-10); nếu không bật được thì tính trong ứng dụng |

---

## XII. LỘ TRÌNH THỰC HIỆN — ĐÃ ĐIỀU CHỈNH

### Tiểu Luận (~12 tuần / 2 người)

| **Tuần** | **Người 1 (P1)** | **Người 2 (P2)** |
| --- | --- | --- |
| 1–2 | DB schema + NestJS project setup | Tìm & đánh giá nguồn câu hỏi độ khó chuẩn (CEFR-graded/IRT-calibrated) + AI Question Generation pipeline |
| 3–4 | Item Bank CRUD API | Auth module (JWT + Adapter Pattern) |
| 4 | *(cùng)* Item Bank Bootstrap: 250 câu + GV validate |  |
| 5–6 | CAT Engine: Rasch + 41-pt EAP + b-matching | Test Session: Dual-write Redis + PostgreSQL |
| 7 | CAT Integration test + unit test EAP | Import & gán b_i từ nguồn độ khó chuẩn vào Item Bank; xử lý fallback CEFR anchor |
| 8 | Language Profile v1: calculation + JSON | AI Tutor Explainer (Gemini) |
| 9–10 | Frontend: Giao diện làm bài thi | Validate độ khó đã gán (đối chiếu CEFR anchor, GV Ngoại ngữ review chéo); hoàn thiện fallback cho item thiếu độ khó chuẩn |
| 10 | Profile API Endpoint + Swagger | Frontend: Student Result Dashboard + Radar |
| 11 | Activate item bank đã gán độ khó chuẩn; smoke test toàn hệ thống | Teacher Class Report basic + Dockerize |
| 12 | *(cùng)* Demo + Viết báo cáo |  |

### Khóa Luận (~12 tuần tiếp)

| **Tuần** | **Nội dung** |
| --- | --- |
| 1–4 | AI Q.Generator (nội dung cốt lõi đã chuyển vào TL ở vòng 3, F-23 đến F-28; phần còn lại chờ chốt) + Calibration Pipeline v2 + Language Profile v2 + BullMQ |
| 5–8 | EduZ Webhook Integration thực tế + AI Writing Assessor + Item Exposure Control (F-17) |
| 9–11 | User Study: 50–100 SV (CAT vs Linear comparison) + Data Analysis cho RQ1/RQ2/RQ3 |
| 12 | Viết báo cáo KL + Defense preparation |

---

## XIII. TÍNH MỚI & CÂU HỎI NGHIÊN CỨU

| **Đóng góp** | **Loại** |
| --- | --- |
| CAT-Rasch + LLM Explainer trong một system | Kỹ thuật |
| Language Profile JSON schema chuẩn hóa, federate-able | Thiết kế hệ thống |
| Dual-write session pattern cho độ tin cậy CAT | Engineering pattern |
| CEFR A1–B1 CAT cho SV cao đẳng năm nhất Việt Nam | Ngữ cảnh ứng dụng mới |
| Item Bank bootstrap: AI-generate → Expert-validate pipeline | Phương pháp luận |

**RQ1:** CAT-Rasch có đạt độ chính xác tương đương Linear Test dài gấp đôi không?

**RQ2:** AI Explainer có cải thiện UX và self-awareness của SV về điểm yếu không?

**RQ3:** Language Profile JSON có đủ thông tin để EduZ cá nhân hóa lộ trình không?

---

## XIV. RISK REGISTER

| **#** | **Rủi ro** | **Mức** | **Giảm thiểu** |
| --- | --- | --- | --- |
| R1 | Item Bank Cold-Start | 🔴 Cao | Bootstrap từ Tuần 1; tìm & đối chiếu nguồn câu hỏi độ khó chuẩn từ Tuần 1-2 (không cần tuyển SV Pre-test) |
| R2 | Nguồn câu hỏi độ khó chuẩn không đủ/không khớp | 🟡 TB | Fallback: gán b_i theo CEFR anchor cho item thiếu dữ liệu độ khó (Mục 6.1); GV Ngoại ngữ review kỹ item fallback trước khi import thành FINAL_APPROVED |
| R3 | EAP bug trong TypeScript | 🟡 TB | Unit test riêng với case biết trước; MLE fallback với guard condition (clip [-4,4], ≥1 đúng+1 sai) |
| R4 | Redis/BullMQ job loss | 🟡 TB | Bật Redis AOF persistence + job retry 3 lần; Near-zero loss, không phải 0% tuyệt đối |
| R5 | Item Exposure (lộ đề) | 🟡 TB | Randomized Top-5 giảm exposure từ 100% → ~60-70% (Mục 4.4); KL: Sympson-Hetter cap cứng ≤ 30% |
| R6 | Scope creep | 🔴 Cao | TL = Vocab+Grammar CAT; KL mới mở rộng. Vòng 3 đã kéo sinh/duyệt đề AI vào TL — xem R15 |
| R7 | SV biên (Pre-A1/C1+) | 🟡 TB | Outlier Early Stop (Mục 4.5) + boundary_effect flag |
| R8 | GVHD yêu cầu "tự train model" | 🟡 TB | Runtime EAP luôn là TypeScript tự code — đáp ứng yêu cầu |
| R9 | Item DRAFT bị CAT chọn nhầm | 🔴 Cao | WHERE status='FINAL_APPROVED' trong ItemRepository (Mục 4.4) + Partial Index |
| R10 | MLE không hội tụ (toàn đúng/sai) | 🟡 TB | Guard condition: chỉ MLE khi ≥1 đúng+1 sai; clip θ về [-4,+4] |
| R11 | SRS spec vượt trước implementation | 🔴 Cao | Phân tầng rõ ràng Must-Have TL vs Spec KL (xem Bảng cuối Mục XIV). Kiểm chứng code tương ứng mỗi mục trước khi bảo vệ. |
| R12 | Chất lượng câu hỏi khi Admin không sửa nội dung và việc duyệt phụ thuộc hai GV (thay R12 cũ "Admin tự duyệt", DC-18; nay theo DC-29, DC-40) | 🟡 TB | Duyệt hai vòng độc lập (A sửa/duyệt, B xác nhận, B không thuộc nhóm A); AI check C1/C2/C3; approved_by/approved_at ghi Admin bấm Import, item_review_events truy vết; GV Ngoại ngữ review mẫu trước khi import (Mục 6.1) |
| R13 | Hệ thống đơn trường: muốn phục vụ nhiều trường phải làm lại schema (DC-19) | 🟡 TB | Đa trường là phạm vi Khóa luận; TL không giữ cột khóa tenant; ghi rõ trong Mục XVI để hội đồng không hiểu nhầm là thiếu sót |
| R14 | OTP 6 số quên mật khẩu dễ bị dò (brute force) (DC-21) | 🟡 TB | OTP lưu bản băm trong Redis, TTL 10 phút, dùng 1 lần, tối đa 5 lần nhập sai rồi hủy; rate limit theo email + IP (RATE_LIMITED); forgot-password luôn trả 202 |
| R15 | Phạm vi tăng: ai-question-generator (F-11) kéo từ Khóa luận vào Tiểu luận — thêm lô, giao việc, ba điểm AI check, lọc trùng T1–T3, embedding, G5 (DC-27, DC-35) | 🔴 Cao | Cập nhật COMMITMENT_BASELINE.md trước khi ký (gate G1, hết Tuần 6); thử một lô nhỏ trước khi code đầy đủ; nếu trễ thì hỏi nhóm quyết định cắt phần nào, không tự cắt; xem Q-11 |
| R16 | Chi phí và hạn mức API (sinh dư, embedding T3, G5, giải thích) chưa đo; mô hình embedding và hạn mức Gemini chưa kiểm chứng (Q-9) | 🟡 TB | Trần lời gọi/token mỗi lô (BATCH_BUDGET_EXCEEDED); cache theo hash prompt; tầng rẻ chạy trước; gộp nhiều câu mỗi lời gọi; LLM Gateway dự phòng; đo chi phí và độ trễ thật ở lần thử đầu, không ghi số khi chưa đo |
| R17 | Admin và GV vai B là điểm tập trung: mọi lô qua Admin (giao việc, kiểm tra, import) và một GV B mỗi lô; B vắng hoặc trễ làm chậm cả lô | 🟡 TB | Hạn + nhắc trước 24 giờ; Admin chỉnh hạn, giao lại, ép gửi gói (FORCE_SEND); item_review_events truy vết; Admin không sửa nội dung nên không phá tính độc lập |
| R18 | Bấm "Xác nhận tất cả câu còn lại" làm B bỏ qua cờ mềm và dấu "A đã sửa" (DC-33) | 🟡 TB | Ghi log hành động hàng loạt (CONFIRM_ALL); C3 kiểm lại luật cứng, trùng và G5 cho câu A sửa trước khi import; Admin quyết lỗi mềm; hiển thị số cờ còn lại trước khi xác nhận (đề xuất giao diện) |
| R19 | Khoảng irt_b hợp lệ [−4, +4] (DC-34) khác CLAUDE.md [−2.5, +1.5] và khác vùng phủ hiện tại của Item Bank; irt_b gợi ý của AI chưa hiệu chỉnh | 🟡 TB | Sửa CLAUDE.md (đề xuất tại DE_XUAT_SUA_CLAUDE_MD.md); kiểm test CAT (Q-12); câu mới calibrated = false; khoảng này là tham số cấu hình |
| R20 | Lọc trùng sai: ngưỡng T2/T3 chưa hiệu chỉnh (loại nhầm hoặc lọt); pg_trgm có thể không bật được (Q-7, Q-10) | 🟡 TB | Cờ mềm giữa hai ngưỡng, loại cứng chỉ ở ngưỡng cao; thống kê tỷ lệ loại theo tầng để hiệu chỉnh; nếu không có pg_trgm thì tính T2 trong ứng dụng |
| R21 | Bản quyền ngân hàng tham chiếu dùng làm few-shot khi phân phối lại cho SV (Q-8) | 🟡 TB | Kiểm điều khoản bộ Tuần 3 (CEFR-J, CLOTH); hỏi GVHD nếu cần; ghi nguồn từng lô |

**Bảng Must-Have TL vs Spec KL (Chốt phạm vi):**

| **Tính năng** | **Trạng thái** | **Phạm vi** |
| --- | --- | --- |
| CAT Engine (Rasch 1PL, EAP 41-pt) | Must-have | Tiểu luận |
| Item Bank + vòng đời hai vòng duyệt (FINAL_APPROVED) | Must-have | Tiểu luận |
| Randomized Top-5 b-matching | Must-have (đơn giản, 1 dòng SQL) | Tiểu luận |
| Outlier Early Stop | Must-have (vài dòng if-else) | Tiểu luận |
| Redis State Machine (state + current_item_id) | Must-have (giảm bug double-submit) | Tiểu luận |
| Language Profile JSON v1 + AI Explainer | Must-have | Tiểu luận |
| Tạo tài khoản SV/GV (từng người, import lưới tạm) + Kỳ thi + Import danh sách thi (lưới tạm) — F-18..F-20 | Must-have (v3.0) | Tiểu luận |
| Đổi/Quên mật khẩu (OTP) + mustChangePassword — F-21 | Must-have (v3.0) | Tiểu luận |
| Quản lý tài khoản SV/GV, nâng/thu hồi Admin — F-22 | Recommended (v3.0) | Tiểu luận nếu đủ thời gian |
| Sinh đề AI, import đề, AI check C1/C2/C3, giao việc, duyệt hai vòng A/B, kiểm tra và import cuối — F-23 đến F-28 (gồm T3 embedding và G5) | Must-have (v3.0 vòng 3, đề xuất) | Tiểu luận (kéo từ Khóa luận; cần cập nhật COMMITMENT_BASELINE) |
| BullMQ Async Write | Recommended (phức tạp hơn) | Tiểu luận nếu đủ thời gian, KL nếu không |
| RBAC chi tiết (M2M, EduZ Service Account) | Spec | Khóa luận |
| Sympson-Hetter Exposure Control | Spec | Khóa luận |
| Multi-tenant thực sự (đa trường) | Spec | Khóa luận (v3.0: Tiểu luận chỉ đơn trường — DC-19) |
| Writing Skill Assessment | Spec | Khóa luận |
| Pre-test tự tổ chức cho ≥60 SV để Cold-Start Calibration | Loại khỏi phạm vi (v2.6) | Thay bằng sourcing nguồn câu hỏi độ khó chuẩn (Mục 6.1) — không áp dụng TL lẫn KL |

---

## XV. NON-FUNCTIONAL REQUIREMENTS (NFR)

**[IMPORTANT]** Mục này bắt buộc có trong SRS của đề tài kỹ thuật phần mềm.

### 15.1. Hiệu năng (Performance)

| **Chỉ số** | **Ngưỡng** | **Điều kiện** |
| --- | --- | --- |
| API latency — Submit response + lấy câu tiếp | < 300ms p95 | 1 user |
| API latency — EAP computation | < 50ms | In-process TypeScript |
| API latency — Lấy kết quả Profile | < 500ms p95 | Bao gồm AI recommendation |
| Throughput | 100 concurrent users | Nginx + 2 NestJS instances |
| Item Bank query | < 20ms | Nhờ Partial Index (status='FINAL_APPROVED') |

### 15.2. Độ tin cậy (Reliability)

| **Chỉ số** | **Ngưỡng** | **Điều kiện** |
| --- | --- | --- |
| Uptime | ≥ 99% trong giờ thi |  |
| Data durability | Near-zero loss (không phải 0% tuyệt đối) | Yêu cầu: Redis AOF bật (appendfsync everysec) + BullMQ job retry 3 lần khi worker fail |
| Session recovery | Khôi phục được phiên thi bị gián đoạn trong ≤ 7200s | Reconstruct từ PostgreSQL |
| Redis TTL | 7200s (2 giờ) |  |

**[NOTE]** **Tại sao không phải 0% tuyệt đối:** Kiến trúc BullMQ Async (thêm vào v2.3) trả HTTP 200 trước khi ghi PostgreSQL xong. Nếu Redis crash trong khoảng thời gian từ khi trả 200 đến khi job được worker pop và ghi DB, response đó sẽ mất. Với **Redis AOF persistence** (`appendfsync everysec`), window mất dữ liệu tối đa là ~1 giây — chấp nhận được cho Tiểu luận, và đây là trade-off đã biết trước giữa **latency** và **durability**. 0% tuyệt đối chỉ đạt được với 2-phase commit hoặc ghi đồng bộ (sync), đổi lại latency cao hơn.

### 15.3. Bảo mật (Security)

| **Yêu cầu** | **Triển khai** |
| --- | --- |
| Auth | JWT Bearer token, refresh token rotation; đăng nhập chỉ bằng email + mật khẩu |
| Băm mật khẩu | argon2 (Quyết định #62); mật khẩu tạm 12 ký tự từ crypto.randomInt, bắt buộc đổi lần đầu (mustChangePassword); không ghi mật khẩu vào log/tài liệu; độ dài tối thiểu khi đổi: 8 ký tự (đề xuất — chờ chốt Q-4) |
| Quên mật khẩu | OTP 6 số, lưu bản băm trong Redis TTL 10 phút, dùng 1 lần, tối đa 5 lần sai; phản hồi forgot-password luôn 202 (không lộ email tồn tại) |
| Rate limit | Giới hạn tần suất theo email + IP cho forgot/reset password (mã RATE_LIMITED, 429); ngưỡng cụ thể chưa đo, chốt khi triển khai |
| Upload import | Import tài khoản, danh sách thi và đề: chỉ .xlsx, tối đa 2 MB và 1000 dòng; chỉ đọc giá trị, bỏ công thức; xuất CSV vô hiệu hóa ô bắt đầu bằng = + - @ (chống CSV injection) |
| Gọi LLM và khóa API | Khóa API chỉ ở backend; mọi lời gọi đi qua LLM Gateway; trần lời gọi/token mỗi lô; ghi tên và phiên bản mô hình thật (TC2.3); câu chưa FINAL_APPROVED và đáp án đúng không trả về SV; mã lý do AI_REJECTED chỉ Admin xem (đề xuất) |
| HTTPS | TLS 1.2+ qua Nginx |
| RBAC | Xem Mục 15.4 |
| Item protection | Câu hỏi + đáp án đúng không bao giờ trả về client trước khi nộp bài |

### 15.4. RBAC — Phân quyền API

**[IMPORTANT]** `GET /api/v1/placement-profiles/:student_id` — ai được gọi?

| **Role** | **Quyền** | **Ghi chú** |
| --- | --- | --- |
| STUDENT | Chỉ xem Profile của chính mình (student_id phải khớp JWT sub) | Không xem được Profile của SV khác |
| TEACHER | Xem Profile của bất kỳ SV nào; xem báo cáo lớp (lọc theo kỳ); với lô được giao: vai A sửa/duyệt/từ chối câu của mình và gửi gói, vai B xác nhận/loại câu trong gói gửi cho mình; không import, không tạo lô, không ghi ngoài phạm vi được giao | GV thường chỉ xem kết quả (DC-18) ngoài việc được giao (DC-40); API câu hỏi kiểm phân công (NOT_ASSIGNED, 403); hệ thống đơn trường nên không còn phạm vi theo trường |
| ADMIN | Siêu tập của TEACHER + toàn bộ chức năng quản trị: lô câu hỏi (tạo, import, giao việc, kiểm tra, import cuối), kỳ thi, import, tài khoản SV/GV, nâng/thu hồi Admin; không sửa và không duyệt nội dung câu (DC-29) | Không thu hồi được Admin cuối cùng (BR-18); Admin đầu tiên tạo bằng seed |
| EduZ System (M2M) | Service Account với API Key riêng (không phải JWT) | Chỉ GET, không POST/DELETE |

```
// NestJS Guard example
@Get('placement-profiles/:studentId')
@UseGuards(JwtAuthGuard, ProfileAccessGuard)
async getProfile(@Param('studentId') studentId: string, @CurrentUser() user: User) {
  // ProfileAccessGuard kiểm tra:
  // - STUDENT: user.id === studentId
  // - TEACHER: pass through (chỉ đọc; hệ thống đơn trường, không lọc theo trường)
  // - ADMIN/M2M: pass through
}
```

**[NOTE]** v3.0: phân quyền các endpoint quản trị mới (import, kỳ thi, tài khoản, ghi câu hỏi) dùng RolesGuard dùng chung theo role; TEACHER gọi các endpoint này nhận 403. Ma trận chức năng theo role: xem Mục 9b.2. Vòng 3: endpoint chặng A và chặng B (Mục X) dùng RolesGuard (TEACHER) cộng thêm kiểm phân công đúng người (A của câu, B của gói); việc không được giao ⇒ 403 NOT_ASSIGNED.

### 15.5. Chống Race Condition API (Redis State Machine)

**[IMPORTANT]** Ngăn chặn sinh viên spam `GET /next-item` gây lỗi trạng thái hoặc double-submit đáp án. Thay vì dùng Distributed Lock (Redlock) quá cồng kềnh, hệ thống sử dụng State Machine ngay trên Redis Session.

Tại mỗi phiên thi trong Redis, duy trì trạng thái:

- state: WAITING_FOR_ANSWER hoặc READY_FOR_NEXT

- current_item_id: UUID của câu hỏi đang hiển thị.

**Quy tắc:**

1. **Gọi `GET /next-item`:**

- Nếu state == WAITING_FOR_ANSWER: Trả lại current_item_id cũ (không chạy lại CAT engine).

- Nếu state == READY_FOR_NEXT: Chạy CAT tìm câu mới, lưu vào current_item_id, đổi state thành WAITING_FOR_ANSWER.

1. **Gọi `POST /responses` (nộp đáp án):**

- Bắt buộc payload phải chứa item_id trùng khớp với current_item_id.

- Nếu hợp lệ: Đổi state thành READY_FOR_NEXT, sau đó ghi response xuống DB.

- **Nếu BullMQ đã implement:** Đẩy job vào queue (async), trả HTTP 200 ngay lập tức.

- **Nếu chưa có BullMQ (fallback cho TL):** Ghi PostgreSQL đồng bộ trực tiếp, rồi mới trả HTTP 200. State Machine vẫn hoạt động độc lập và đúng — chỉ khác nhau về latency.

**Kịch bản Recovery khi Redis mất (State Machine phải được nối với Session Reconstruct):**

Khi Redis TTL hết hoặc restart, hệ thống reconstruct session từ PostgreSQL (đọc lại toàn bộ session_responses). Sau reconstruct, State Machine được khởi tạo lại theo quy tắc:

```
// SessionRepository.reconstruct()
const lastResponse = await db.query(
  `SELECT item_id FROM session_responses 
   WHERE session_id = $1 ORDER BY answered_at DESC LIMIT 1`,
  [sessionId]
);

// Quy tắc: Nếu response cuối đã ghi vào DB → response đó đã được xử lý
// → Mặc định state = READY_FOR_NEXT (sẵn sàng nhận câu tiếp theo)
// → current_item_id = null (câu cũ trước crash không còn hiệu lực)
await redis.hSet(`session:${sessionId}`, {
  state: 'READY_FOR_NEXT',
  current_item_id: '',  // Clear item cũ
  theta: reconstructedTheta,
  se: reconstructedSE,
});
// Sinh viên gọi GET /next-item → CAT engine tính câu mới từ theta hiện tại
```

**[NOTE]** Quy tắc reconstruct: "Response đã trong PostgreSQL = đã được xử lý đầy đủ". Điều này đảm bảo SV không bao giờ bị kẹt ở `WAITING_FOR_ANSWER` mãi mãi sau khi mất kết nối.

---

## XVI. PHẠM VI ĐƠN TRƯỜNG (SINGLE-TENANT) — QUYẾT ĐỊNH DC-19

**[NOTE]** Từ v3.0 hệ thống chỉ phục vụ một trường: không còn khái niệm đa trường (tenant) trong schema, API hay JSON Profile. Nội dung này thay thế thiết kế multi-tenant của v2.2 đến v2.6.

### Nội dung quyết định

Để giảm khối lượng Tiểu luận và loại bỏ phạm vi quản trị theo trường, v3.0 chốt:

1. **Bỏ dữ liệu đa trường:** xóa bảng đơn vị/trường và mọi cột khóa tenant (người dùng, kỳ thi, danh sách thi, phiên thi), kể cả composite FK/CHECK liên quan.

2. **Một cấp Admin:** ADMIN là Admin của trường, siêu tập của TEACHER; không còn quản trị viên cấp hệ thống hay cấp đơn vị, không còn lớp phạm vi theo trường (AccessScope/resolveScope); UserRole giữ 4 giá trị. Tài khoản Admin đầu tiên tạo bằng seed.

3. **JSON Profile gọn hơn:** Profile v1 không còn trường định danh trường; EduZ gọi API bằng API Key như Mục 15.4.

### Hệ quả và hướng Khóa luận

```
// v3.0: JSON Profile v1 không có trường định danh trường (tenant).
// Nếu EduZ cần phục vụ nhiều trường -> phạm vi Khóa luận, phải thiết kế lại schema.
```

Hiện tại (TL): 1 trường duy nhất. Muốn đa trường ⇒ Khóa luận, làm lại schema và phân quyền theo trường (xem rủi ro R13).

---

---

## XVII. REVISION HISTORY (Lịch sử Sửa đổi)

| **Phiên bản** | **Ngày** | **Người thực hiện** | **Nội dung thay đổi chính** |
| --- | --- | --- | --- |
| v1.0 | 09/09/2026 | Nhóm | Bản khởi tạo SRS ban đầu |
| v2.1 | 09/09/2026 | Nhóm + Team Review vòng 1 | Điều chỉnh θ₀=-0.5; đặc tả EAP 41-point; ghi chú irt_c; ceiling/floor effect; dual-write Redis+PostgreSQL; đẩy calibration lên Tuần 7-8; fallback calibration criteria |
| v2.2 | 09/09/2026 | Nhóm + Team Review vòng 2 | Thêm status/source/approved_by/approved_at vào Items schema; WHERE status='FINAL_APPROVED' tại ItemRepository (tên trạng thái đã duyệt được đổi ở v3.0 vòng 3); tái cơ cấu Mục V (Runtime vs Calibration); làm rõ θ₀ vs Prior; MLE Fallback Guard clip[-4,+4]; thêm NFR Mục XV; RBAC 4 role; giải thích thiết kế multi-tenant (đã bỏ ở v3.0, xem Mục XVI) |
| v2.3 | 09/09/2026 | Nhóm + Team Review vòng 3 | Randomized Top-5 b-matching; Outlier Early Stop; Redis State Machine chống Race Condition; BullMQ Async Write; R9/R10 vào Risk Register |
| v2.4 | 10/09/2026 | Nhóm + Nhận xét GVHD vòng 1 | Viết đầy đủ thuật toán Top-5 tại Mục 4.4 kèm bảng exposure; viết Early Stop pseudocode tại Mục 4.5; sửa NFR 15.2 thành near-zero loss; State Machine recovery spec; R5→🟡TB; thêm R11; Bảng Must-Have TL vs Spec KL |
| v2.5 | 10/09/2026 | Nhóm + Nhận xét GVHD vòng 2 | Thêm điều kiện ≥8 câu tối thiểu cho Outlier Early Stop; tách rõ "ngoài Item Bank" vs "ngoài CEFR" trong thông báo; chú thích ước lượng sơ bộ cho exposure rate; thêm BullMQ fallback note trong State Machine; dọn nhãn version khỏi thân bài vào phụ lục này |
| v2.6 | 18/09/2026 | Nhóm + Nhận xét GVHD vòng 3 | Bỏ kế hoạch Pre-test tự tổ chức cho ≥60 SV (Mục 6.1 giai đoạn 2, Mục 6.4 giai đoạn 1) — GVHD nhận xét khối lượng công việc quá lớn so với quy mô Tiểu luận; chuyển sang tìm nguồn câu hỏi đã có độ khó chuẩn hóa (CEFR-graded/IRT-calibrated) để khởi tạo b_i ban đầu; cập nhật Mục 4.2, 4.4, V, VI, IX (F-12), XII, Risk Register R1/R2 tương ứng |
| v3.0 | 13/10/2026 | Nhóm (soạn có hỗ trợ AI — cần thành viên rà soát) | Hệ thống đơn trường (bỏ đa trường, 3 role); GV thường chỉ xem kết quả, Admin làm mọi chức năng quản trị; bỏ đăng nhập ngoài (EduZ SSO thuộc Khóa luận), chỉ email + mật khẩu; thêm Kỳ thi (hạn phiên theo durationMinutes, sửa Mục 4.5); import tài khoản và danh sách thi theo lưới tạm; đổi/quên mật khẩu (OTP); khóa tài khoản is_active; DDL exam_rounds / exam_round_participants / test_sessions.exam_round_id, expires_at; F-18..F-22; mục mới IXb; API Mục X; Risk R12–R14; RBAC Mục 15.3/15.4; viết lại Mục XVI. Chi tiết: Phụ lục A |
| v3.0 (vòng 2) | 13/10/2026 | Nhóm (soạn có hỗ trợ AI — cần thành viên rà soát) | Phiên 23 (DC-24..DC-26, #99..#101): Admin tạo tài khoản SV và GV từng người hoặc import file (UCADM08 mở rộng, tạo từng người gộp UCADM09; API POST /students, POST /teachers, tham số kind); exam_rounds.duration_minutes NOT NULL DEFAULT 45; sửa mô tả EAP thành lưới đều 41 điểm [−4, +4] bước 0.2 (không phải Gaussian–Hermite; không đổi thuật toán); toàn bộ công thức chuyển sang phương trình Word gốc (OMML); xuất thêm bản Markdown SRS_TLCN_v3.0.md |
| v3.0 (vòng 3) | 14/10/2026 | Nhóm (soạn có hỗ trợ AI — cần thành viên rà soát) | Phiên 25 (DC-27 đến DC-45, #110 đến #113): luồng Admin tạo lô bằng AI hoặc import ⇒ AI check C1/C2/C3 ⇒ giao việc ⇒ GV A duyệt ⇒ gói ⇒ GV B confirm ⇒ Admin kiểm tra và import cuối; ItemStatus mới (FIRST_APPROVED, SECOND_APPROVED, FINAL_APPROVED, AI_REJECTED), ItemSource AI_GENERATED/IMPORTED; GV không import, Admin không sửa nội dung; giải thích AI sinh cùng lúc; khoảng irt_b [−4, +4]; F-23 đến F-28; Mục III (item-generation, ItemCheckService, ItemDuplicateChecker, LLM Gateway, BullMQ); DDL 6.2 và 6.2b; IXb 9b.9 đến 9b.18; API Mục X; Risk R15 đến R21; Q-7 đến Q-10 còn chờ chốt |
| v3.0 (vòng 4) | 16/10/2026 | Nhóm (soạn có hỗ trợ AI — cần thành viên rà soát) | Chốt đồng bộ: Item không còn source (nguồn ở item_batches.source, enum ItemBatchSource); items.batch_id NOT NULL kèm các lô seed theo bộ nguồn; gói ItemPackage tạo lúc giao việc (OPEN → SENT → DONE); thông báo chỉ email nhắc việc + Hộp việc (không chuông thời gian thực); bổ sung nghiệp vụ ép gửi và xử lý câu chưa xử lý sau hạn; GV xem ngân hàng ở /teacher/item-bank (chỉ xem); mã UCADM15–17 cho kỳ thi |

*SRS v2.5 — 10/09/2026 | Bản nhận xét GVHD được tích hợp đầy đủ. Changelog v2.4: (1) Viết đầy đủ thuật toán Randomized Top-5 tại Mục 4.4 kèm bảng ước lượng exposure rate; (2) Viết đầy đủ Outlier Early Stop tại Mục 4.5 kèm pseudocode phát hiện deadlock; (3) Sửa NFR 15.2: "near-zero loss" thay vì "0% tuyệt đối", giải thích rõ điều kiện Redis AOF; (4) Bổ sung State Machine Recovery sau reconstruct từ PostgreSQL tại Mục 15.5; (5) Điều chỉnh Risk R5 về 🟡 TB (Randomized Top-5 giảm nhưng không triệt tiêu exposure); (6) Thêm R11 (SRS spec vượt trước implementation); (7) Bảng phân tầng Must-Have TL vs Spec KL.*

*SRS v3.0 — 14/10/2026 | Bản cập nhật theo quyết định Tuần 5 (DC-01..DC-45, Quyết định #84 đến #113 trong DECISIONS_LOG). Các nội dung dự kiến cho "v2.7" ngoài phạm vi liệt kê tại Phụ lục A chưa được đưa vào bản này.*

---

## PHỤ LỤC A. BẢNG THAY ĐỔI SRS v2.6 → v3.0

| **Mục SRS** | **Thay đổi** | **Căn cứ** |
| --- | --- | --- |
| Đầu trang | Tiêu đề v3.0, ngày 13/10/2026, changelog v3.0 | DC-12 (#91) |
| I.3 | Người dùng: 3 role STUDENT / TEACHER / ADMIN (+ EduZ máy); GV thường chỉ xem; hệ thống đơn trường | DC-18, DC-19 (#96, #97) |
| III | Module mới user-import, user-admin, exam-round, mail; bỏ Adapter Pattern đăng nhập ngoài; Redis/BullMQ/SMTP dùng thêm | DC-02, DC-03 (#85, #86) |
| IV.5 | Timeout theo durationMinutes của kỳ; expires_at lưu DB; quá hạn theo K5 | DC-20 (#93) |
| VI | Ghi chú Admin duyệt/tự duyệt câu hỏi | DC-18 (#96) |
| VII | JSON Profile v1 bỏ trường định danh trường | DC-19 (#97) |
| VIII | DDL: test_sessions (student_id UUID, exam_round_id, expires_at), users (+3 cột), exam_rounds, exam_round_participants, ràng buộc/index; khóa Redis lưới tạm và OTP | DC-07/08/10/20/22/23 |
| IX | F-01, F-02, F-09 sửa; thêm F-18 đến F-22 | DC-01, DC-05, DC-11, DC-18 |
| IXb (mới) | Nghiệp vụ Import & Kỳ thi: vai trò, luồng L0–L5, lưới tạm, máy trạng thái kỳ, BR-01..BR-19, mã lỗi, điểm mở | DC-04..DC-11, DC-21, DC-22 |
| X | API: đổi/quên/đặt lại mật khẩu, import lưới tạm, quản lý tài khoản, kỳ thi; POST /sessions nhận examRoundId | DC-21, DC-22 |
| XIV | Risk R12 (Admin tự duyệt), R13 (đơn trường), R14 (OTP dễ dò); bảng Must-have thêm F-18..F-22 | DC-18, DC-19, DC-21 |
| XV | 15.3: argon2, mật khẩu tạm, OTP, rate limit, upload; 15.4: RBAC 3 role, bỏ phạm vi theo trường | DC-19, MD-10, MD-15 |
| XVI | Viết lại: từ multi-tenant sang phạm vi đơn trường | DC-19 (#97) |
| XVII | Thêm dòng v3.0; chỉnh chú thích dòng v2.2 cho khớp | — |
| IV.3, V, IX, XI | Mô tả EAP: "Gaussian–Hermite quadrature" sửa thành lưới đều 41 điểm θ ∈ [−4, +4], bước 0.2, prior N(0,1) (tích phân số kiểu hình thang); thêm NOTE K7; công thức EAP/SE giữ nguyên, không đổi thuật toán | DC-26 (#101) |
| IV.5, VIII | exam_rounds.duration_minutes INT NOT NULL DEFAULT 45, CHECK 5..180 (bỏ nullable / "NULL = 45"); expires_at = min(startedAt + durationMinutes, closesAt) | DC-25 (#100) |
| I.3, III, IX (F-18, F-22), IXb, X | Tạo tài khoản SV và GV: từng người (form) hoặc import file (kind = STUDENT\|TEACHER; lưới tạm khóa theo adminId + kind); BR-01/02/03/05 sửa, thêm BR-20 (đề xuất); luồng L1 sửa, thêm L1b; API POST /students, POST /teachers; Mã GV lưu ở teacher_profiles.teacher_code (có sẵn) | DC-24 (#99) |
| IV, mọi công thức | Công thức chuyển từ văn bản thô (cú pháp LaTeX trong dấu đô-la) sang phương trình Word gốc OMML (m:oMathPara / m:oMath); bản Markdown SRS_TLCN_v3.0.md giữ công thức dạng LaTeX đặt trong cặp dấu đô-la đơn (nội dòng) hoặc đôi (khối) | Yêu cầu vòng 2 (mục 15) |
| Đầu trang, I.3 | Cập nhật 14/10/2026; changelog vòng 3; GV thường có thêm vai A/B theo lô được giao, Admin không soạn/sửa nội dung câu | DC-27, DC-29, DC-40 (#110, #111) |
| III | Thêm module item-generation, llm-gateway (đề xuất); bảng thành phần ItemGenerationService, ItemCheckService (3 checkpoint), ItemDuplicateChecker, ReviewDistributionService, DeadlineReminderService, LLM Gateway; BullMQ dùng thêm cho sinh/kiểm lô và nhắc hạn; ai-question-generator chuyển từ KL vào TL | DC-27, DC-30, DC-35, DC-45 (#110, #105, #107, #113) |
| IV.4, 6.2, XIV R9, 15.1 | Đổi tên trạng thái đã duyệt cũ thành FINAL_APPROVED (guard CAT, Partial Index, R9, NFR); bỏ trạng thái chờ duyệt cũ; công thức và thuật toán CAT không đổi | DC-39 (#109, #112) |
| IV.5, IV.7 | NOTE khoảng irt_b [−4, +4] (cấu hình) so với mốc −2.5/+1.5 (vùng phủ hiện tại, ngưỡng Early Stop) và CLAUDE.md; việc sửa CLAUDE.md và kiểm test CAT là Q-12 | DC-34 (#107) |
| VI (6.1, 6.2, 6.2b) | DDL items: status 6 giá trị, source AI_GENERATED/IMPORTED (bỏ giá trị thủ công), thêm content_hash, batch_id, package_id; chỉ mục băm T1 và GIN pg_trgm T2; bảng mới item_batches, item_batch_assignments, item_review_assignments, item_packages, item_embeddings, item_check_results, item_review_events; CREATE EXTENSION pg_trgm (chờ chốt Q-10) | DC-30, DC-32, DC-39 (#105, #106, #109) |
| VIII | Khóa Redis lưới tạm import đề; hàng đợi BullMQ cho sinh/kiểm lô, nhắc hạn | DC-22, DC-27 |
| IX | F-02 viết lại; F-05 giải thích sinh cùng lúc; F-11 ghi đã kéo vào TL; thêm F-23 đến F-28 (đề xuất) | DC-27 đến DC-33, DC-31 |
| IXb | Đổi tên mục; ma trận quyền 9b.2 (thêm vai A, B); BR-07, BR-16 sửa, thêm BR-21 đến BR-30; mục mới 9b.9 đến 9b.18 (vòng đời, trạng thái, tạo lô, C1/C2/C3, giao việc và chia đều, gói/hạn/nhắc, câu bị loại, ma trận quyền, luồng L-1 đến L-8, mã lỗi); 9b.8 thêm Q-7 đến Q-12 | DC-27 đến DC-45 |
| X | API nhóm lô câu hỏi, giao việc, kiểm tra/import cuối, chặng A, chặng B theo Mục 10 kế hoạch bản 5 (đề xuất); bỏ POST/PUT/DELETE /items và bulk-import | DC-27, DC-28, DC-32 |
| XI, XII | Stack: AI qua LLM Gateway, embedding (chờ chốt Q-9), pg_trgm (chờ chốt Q-10), BullMQ dùng trong TL; F-11 ở lộ trình KL ghi chú đã chuyển vào TL | DC-27, DC-35 |
| XIV | R6 ghi chú; R12 viết lại; thêm R15 (phạm vi), R16 (chi phí API), R17 (Admin/B tập trung), R18 (xác nhận tất cả), R19 (khoảng irt_b), R20 (lọc trùng), R21 (bản quyền); bảng Must-have thêm F-23 đến F-28 | DC-27, DC-33, DC-34, DC-35 |
| XV | 15.1 Partial Index; 15.3 thêm hàng gọi LLM và khóa API; 15.4 RBAC TEACHER/ADMIN thêm vai A/B | DC-29, DC-40 |
| XVII | Thêm dòng v3.0 (vòng 3); chỉnh chú thích dòng v2.2 | — |

Chưa thực hiện trong bản này: Mục XII (lộ trình) chưa cập nhật tuần cho khối lượng mới (tạo tài khoản GV, kỳ thi, lưới tạm); sơ đồ thành phần/triển khai; hấp thụ các đề xuất v2.7 ngoài phạm vi trên. Các mục đó được ghi nợ đồng bộ tài liệu ở tracking. Vòng 3 chưa thực hiện thêm: cập nhật COMMITMENT_BASELINE.md cho phạm vi tăng (Q-11); sửa CLAUDE.md theo khoảng irt_b (Q-12); đổi tên trạng thái đã duyệt cũ trong mã backend và seed; Mục XII (lộ trình) chưa cập nhật tuần cho khối lượng sinh/duyệt đề; Class Diagram, Sequence, đặc tả Use Case và màn hình từ S26 do các tài liệu khác đảm nhiệm; Q-7 đến Q-10 còn chờ chốt.
