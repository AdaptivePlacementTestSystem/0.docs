# Phương án P3: Bộ trắc nghiệm A2–B1 được dán nhãn CEFR có thể giải trình

- Phạm vi: Tiểu luận (TL) — Adaptive Placement Test (CAT-Rasch)
- Ngày lập: 2026-10-01 (Tuần 3/12)
- Người soạn: Claude Code (Sonnet 5.5), theo yêu cầu người dùng (vai trò Senior SE + PM)
- Kế hoạch mẹ: [`KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`](./KE_HOACH_BO_DU_LIEU_ITEM_BANK.md) (phase **PL** của file này nằm ở Mục 7 kế hoạch mẹ) · File theo dõi: [`TRACKING_BO_DU_LIEU_ITEM_BANK.md`](./TRACKING_BO_DU_LIEU_ITEM_BANK.md)
- Phân tích nguồn đi kèm: [`PHAN_TICH_CEFR_J_PHU_HOP_VA_BU_DAP.md`](./PHAN_TICH_CEFR_J_PHU_HOP_VA_BU_DAP.md), [`PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md`](./PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md)
- **Trạng thái phê duyệt:**
  - ✅ **Người dùng đã chọn phương án P3 (lai)** trong phiên 2026-10-01 (câu trả lời: "Chọn P3, viết thành file md và cập nhật kế hoạch đi").
  - ✅ **Đã duyệt (2026-10-01):** kế hoạch mẹ (P0.1) và các quyết định phụ **DL1–DL5**. Các mặc định còn lại (DL2 = 0,6; tên/cột bảng `item_label_evidence`; rào chắn DL3) được nhóm chốt cùng lượt. **Các con số ngưỡng (kappa 0,6; độ phủ 95%; hệ số sinh dư ×2) vẫn là đề xuất chưa tra nguồn, sẽ chỉnh sau pilot.**
- **Phạm vi file này:** ✅ **Nhóm chọn (2026-10-01, DL5): chạy cả A1–B2 (280 câu theo SRS 6.3)**; tên file giữ "A2_B1" vì phân tích gốc làm cho A2–B1 trước. Vẫn nên chạy A2–B1 trước làm pilot rồi mở rộng sang A1 và B2. **Rủi ro:** khối lượng gán nhãn gấp ~1,75 lần trong khi hiện chưa có GV nào (DL1).
- **Lưu ý trạng thái repo:** chưa có git repo, chưa có `apps/backend` (G6 chưa chạy). Các task *tài liệu/dữ liệu* làm được ngay sau khi duyệt; task cần code/engine chặn tới khi G6 xong.

---

## 0. Tóm tắt

1. **Mục tiêu:** có 160 câu trắc nghiệm Vocabulary/Grammar cấp A2 và B1 (A2: 45 từ vựng + 35 ngữ pháp; B1: 45 từ vựng + 35 ngữ pháp, theo SRS 6.3), mỗi câu có nhãn CEFR kèm bằng chứng gán nhãn.
2. **Nguyên tắc P3:** **nhãn có trước, câu hỏi sinh sau** (câu được thiết kế để kiểm tra đúng một mục CEFR-J đã biết cấp). Đề thi thật (CLOTH, VNHSGE) chỉ đóng vai trò **học mẫu cách ra đáp án nhiễu** và **kiểm tra phương pháp gán nhãn**, không phải nguồn câu của bank.
3. **"Chuẩn" nghĩa là gì ở đây:** nhãn *có thể giải trình* (có bằng chứng, nhiều phía gán độc lập, đo được mức đồng thuận). **Không** phải nhãn chính thức hay độ khó thực đo; kiểm định thực nghiệm chỉ làm được sau khi có dữ liệu thi thật (F-12, hướng Khóa luận).
4. **Có 4 bước:** (1) đặc tả, (2) sinh câu có kiểm soát ngữ cảnh, (3) gán nhãn độc lập từ 3 phía, (4) kiểm tra phương pháp bằng dữ liệu ngoài (có điều kiện).
5. **Điểm cần bạn quyết định sớm** (Mục 8): có 2 GV chấm độc lập không (DL1), ngưỡng đồng thuận (DL2), có được gửi nội dung CLOTH tới dịch vụ AI bên ngoài không (DL3 — quan trọng, xem Mục 3.2).

---

## 1. Phạm vi và số lượng

| Kỹ năng | A2 | B1 | Cần cuối cùng | Sinh dư (đề xuất ×2, cấu hình được) |
|---|---|---|---|---|
| Vocabulary | 45 | 45 | 90 | 180 |
| Grammar | 35 | 35 | 70 | 140 |
| **Tổng A2–B1** | 80 | 80 | **160** | **320** |

**Mở rộng theo DL5 (A1 và B2, SRS 6.3):**

| Kỹ năng | A1 | B2 | Cần cuối cùng | Sinh dư ×2 |
|---|---|---|---|---|
| Vocabulary | 40 | 30 | 70 | 140 |
| Grammar | 30 | 20 | 50 | 100 |
| **Tổng A1+B2** | 70 | 50 | **120** | **240** |

Tổng cả bank: **280 câu cuối, 560 câu ứng viên**. Nguồn mục đích kiểm tra (đã đếm): từ vựng A1 1.164, B2 2.778; ngữ pháp dòng có nhãn A1 63 (đủ cho 30 câu), B2 34 trong đó 4 dòng `B2.2*` chưa rõ nghĩa (còn 30 dòng cho 20 câu).

- Số lượng cuối lấy từ SRS 6.3. Hệ số sinh dư ×2 là **đề xuất** (SRS 6.1 chỉ nói sinh dư 20%; hệ số này sẽ được hiệu chỉnh sau pilot ở PL.5 dựa trên tỉ lệ loại thật).
- Nguồn mục đích kiểm tra (đã đếm thật từ file CEFR-J tải về, xem `PHAN_TICH_CEFR_J_…` Mục 2):

| | A2 | B1 |
|---|---|---|
| Từ vựng (file 1.5) | 1.411 mục | 2.446 mục |
| Ngữ pháp (bản 20180315, dòng có nhãn) | 32 dòng (A2.1: 24, A2.2: 7, A2: 1) | 41 dòng (B1.1: 25, B1.2: 13, B1: 3) |

**Điểm nghẽn:** ngữ pháp A2 chỉ có 32 dòng cho 70 câu sinh dư (≈2,2 câu/dòng) và 35 câu cuối (≈1,1 câu/dòng). Phải sinh nhiều biến thể trên một dòng, hoặc mở rộng bằng mục con đã được GV xác nhận cấp (không tự thừa hưởng).

---

## 2. "Chuẩn" và các giới hạn nói thẳng

| Điều làm được | Điều **không** làm được |
|---|---|
| Nhãn có bằng chứng: mục CEFR-J đích, độ phủ từ vựng, nhãn từng phía, mức đồng thuận | Tuyên bố nhãn là "CEFR chính thức" hay đã liên kết với một bài thi chuẩn |
| Ước lượng sai số gán nhãn bằng mẫu ngẫu nhiên có GV | Độ khó thực đo (`irt_b` vẫn chỉ là neo theo cấp, `calibrated=false`) |
| Kiểm tra phương pháp bằng dữ liệu ngoài khi được phép dùng | Chứng minh độ chính xác của CEFR kết quả: vòng tròn (CEFR của kết quả dựa vào CEFR của câu hỏi) |

Hướng quy trình tham khảo: tài liệu Council of Europe về liên kết bài thi với CEFR (đặc tả → gán nhãn bởi nhiều người → kiểm định thực nghiệm). Tôi nhớ tài liệu này nhưng **chưa đọc lại**; đừng trích dẫn vào báo cáo trước khi đối chiếu bản gốc.

---

## 3. Quy trình 4 bước

### 3.1. Bước 1 — Đặc tả đích kiểm tra

Mỗi câu gắn **một** mục đích kiểm tra duy nhất:

- **Từ vựng:** một mục `headword + pos` trong CEFR-J Vocabulary cấp A2 hoặc B1. Ưu tiên noun/verb/adjective/adverb; loại từ chức năng. Mỗi mục dùng tối đa số lần cấu hình (ví dụ mặc định đề xuất 1, chưa chốt).
- **Ngữ pháp:** một dòng có nhãn `CEFR-J Level` trong Grammar Profile. Dòng không có nhãn **không** dùng, trừ khi GV xác nhận cấp (không thừa hưởng tự động từ mục cha).
- Cấp con (ngữ pháp A2.1/A2.2/B1.1/B1.2) được giữ lại làm đầu vào cho dàn `irt_b` (Mục 3.6). Từ vựng không có cấp con.
- **Dữ liệu CEFR-J cần làm sạch trước khi dùng** (xem `PHAN_TICH_CEFR_J_…` G8): 3 dòng nhập nhầm cột (ID 132, 135, 136), 4 dòng `B2.2*` chưa rõ nghĩa (không thuộc A2–B1 nên không ảnh hưởng ở file này).

### 3.2. Bước 2 — Sinh câu có kiểm soát ngữ cảnh

**Quy tắc cho mọi câu sinh ra** (đây là tiêu chí lọc cứng, đọc từ cấu hình):

| # | Quy tắc | Mục đích |
|---|---|---|
| Q1 | Câu dẫn là **một câu**, có đúng **một** chỗ trống; 4 đáp án A–D; đúng 1 đáp án đúng | Khớp lược đồ `Item` |
| Q2 | Mọi từ còn lại trong câu **không khó hơn cấp đích** theo CEFR-J Vocabulary (tính tỉ lệ từ thuộc cấp ≤ cấp đích; ngưỡng mặc định đề xuất **95%**, chưa chốt — chưa tra nguồn nào cho con số này). Danh từ riêng và số được miễn; từ không có trong CEFR-J bị gắn cờ. | Độ khó đến từ đúng cái cần đo, không từ một từ lạ |
| Q3 | Đáp án nhiễu cùng loại từ với đáp án đúng, **không khó hơn cấp đích**, và hợp lý theo một kiểu lỗi người học hay mắc | Nhiễu thật sự hấp dẫn, không vì từ lạ mà dễ loại |
| Q4 | Không dùng "all of the above", không có hai đáp án cùng đúng, độ dài đáp án gần nhau | Chất lượng trắc nghiệm |
| Q5 | Vị trí đáp án đúng được **xáo ngẫu nhiên** giữa A–D sau khi sinh (kiểm tra phân bố, không để lệch) | Tránh lộ đáp án theo vị trí |
| Q6 | Ghi mã mục đích kiểm tra và tham số sinh vào bản ghi | Truy vết (R-D8) |

**Vấn đề quan trọng về CLOTH khi dùng làm mẫu few-shot.** Gửi nội dung câu CLOTH tới dịch vụ AI bên ngoài (như Gemini API) là **đưa nội dung chưa rõ giấy phép ra ngoài**. Điều này có thể vi phạm điều khoản nguồn và, một khi đã gửi, không thu hồi được. Vì vậy:

- **Cập nhật 2026-10-01:** nhóm đã chọn **cho phép gửi** (DL3, thuần học thuật), thay cho mặc định ban đầu "không gửi" của AI. Rào chắn: chỉ mẫu nhỏ, không đưa nguyên văn vào Item Bank/báo cáo, kiểm tra điều khoản dữ liệu của gói API, ghi log. Mô tả chiến lược ra nhiễu bằng lời vẫn là cách ưu tiên khi đủ dùng.
- *(Mặc định gốc của AI, giữ để đối chiếu)* **không** gửi văn bản câu CLOTH nào tới API bên ngoài khi giấy phép còn `UNVERIFIED`.
- Thay vào đó, đội viết **mô tả chiến lược ra nhiễu** bằng lời (ví dụ "nhiễu cùng gốc từ khác loại từ", "nhiễu sai thì động từ") — đây là kiến thức chung, không phải trích đoạn đề thi — và dùng đó làm mẫu cho prompt.
- Nếu muốn dùng chính câu CLOTH làm mẫu: đợi xác nhận từ tác giả (S3), hoặc dùng mô hình chạy cục bộ (không gửi dữ liệu ra ngoài). Đây là quyết định DL3.

### 3.3. Bộ lọc tự động (trước khi GV nhìn thấy)

Theo thiết kế ở `Tuan2/Phuong_an_sua_doi_AI.md` Mục 1.3b, bổ sung kiểm tra Q2 (độ phủ từ vựng):

| Loại | Kiểm tra | Hành động |
|---|---|---|
| Cứng | Q1, Q4, Q5; độ phủ Q2 dưới ngưỡng; `irt_b` ngoài biên; trùng lặp vượt ngưỡng với câu khác trong lô | Loại |
| Mềm | Tự giải lại bằng **một mô hình khác** mô hình đã sinh (không cho biết đáp án): không khớp đáp án đã đánh dấu | Gắn cờ "đáp án có thể mơ hồ" |
| Mềm | Từ trong câu không có trong CEFR-J | Gắn cờ "từ chưa rõ cấp" |

Ngưỡng cụ thể nằm ở cấu hình (D9 của kế hoạch mẹ), không hardcode.

### 3.4. Bước 3 — Gán nhãn độc lập từ 3 phía

| Phía | Cách gán | Độ mạnh |
|---|---|---|
| **A. Theo thiết kế** | Cấp = cấp của mục đích kiểm tra (Bước 1) | Mạnh nhất về lý lẽ cấu trúc; nhưng chỉ đúng nếu câu thật sự chỉ kiểm tra mục đó |
| **B. Mô hình tự động** | ≥2 mô hình khác nhau gán cấp theo rubric kèm câu mẫu đã neo; lấy trung vị | Rẻ, quy mô lớn; có thể cùng thiên lệch |
| **C. GV** | 2 GV gán độc lập, không thấy nhãn của phía A và B | Nguồn quyết định |

**Quy tắc nhãn cuối** (GV không phải gán toàn bộ 320 câu):

1. Câu mà **A và B khớp** → giữ nhãn A, đưa vào nhóm "đã khớp".
2. Câu mà **A và B lệch** → bắt buộc vào hàng đợi GV.
3. **Mẫu ngẫu nhiên có phân tầng** từ nhóm "đã khớp" cũng vào hàng đợi GV, để ước lượng tỉ lệ sai của nhóm khớp.
4. Câu GV gán: nếu 2 GV khớp nhau → nhãn GV; nếu lệch → thảo luận thống nhất hoặc **bỏ câu** (không giữ nhãn tự động cho câu bất đồng).
5. **GV luôn thắng** khi lệch với A/B.

**Quy mô mẫu và số giờ GV chưa được chốt:** phụ thuộc DL1 (có bao nhiêu GV, mỗi người dành bao nhiêu giờ) và kết quả pilot ở PL.5. Tôi không ước lượng con số ở đây vì chưa có dữ liệu thời gian gán nhãn thật.

### 3.5. Bước 4 — Kiểm tra phương pháp bằng dữ liệu ngoài (có điều kiện)

- **Điều kiện:** chỉ chạy nếu DL3 cho phép xử lý CLOTH (hoặc chạy bằng mô hình cục bộ). Nếu không, bỏ bước này và ghi rõ.
- **Cách làm:** lấy một mẫu câu CLOTH-M và CLOTH-H, chạy **đúng quy trình gán nhãn phía A và B** trên chúng (không cần GV), rồi đo xem nhãn có phân biệt M và H hay không (hệ số tương quan thứ hạng).
- **Ý nghĩa:** CLOTH-M < CLOTH-H là một thứ tự thô có thật (cấp 2 < cấp 3). Nếu quy trình gán nhãn của bạn không tái hiện được thứ tự đó, quy trình có vấn đề; nếu tái hiện được, đó là một bằng chứng bên ngoài (chưa phải chứng minh).
- Không điền kết quả khi chưa chạy; ghi `N/A`.

### 3.6. Gán `irt_b` và định dạng đầu ra

| Việc | Quy tắc |
|---|---|
| `cefr_target` | A2 hoặc B1 (nhãn cuối của Mục 3.4) |
| `irt_b` khoảng cấp | Theo SRS 4.6: A1 ∈ [−2,−1), A2 ∈ [−1,0), B1 ∈ [0,1), B2 ∈ [1,2). **Lưu ý B2:** biên của Item Bank là `b_max = +1,5` (SRS 4.7) nên `irt_b` của câu B2 bị chặn ở **≤ +1,5**, tức chỉ phủ [1; 1,5] của khoảng B2 |
| Dàn trong cấp (ngữ pháp) | Dùng cấp con. Với cấp có n cấp con, cấp con thứ k lấy điểm giữa phân đoạn thứ k của khoảng cấp (công thức và giá trị nằm ở cấu hình, đề xuất chưa chốt) |
| Dàn trong cấp (từ vựng) | CEFR-J **không có cấp con**; để mặc định điểm giữa khoảng cấp (nhiều câu hòa hạng, Top-5 ngẫu nhiên giảm nhẹ hậu quả); dàn thêm bằng tín hiệu phụ chỉ khi quyết định D7 của kế hoạch mẹ được duyệt |
| `calibrated` | `false` |
| Bằng chứng gán nhãn | Mỗi câu một bản ghi (Mục 3.7) |

### 3.7. Bản ghi bằng chứng mỗi câu

| Trường | Nội dung |
|---|---|
| `target_ref` | Mã mục CEFR-J đích (`headword+pos` hoặc `ID` ngữ pháp) và phiên bản file |
| `design_level` | Cấp theo thiết kế (phía A) |
| `context_coverage` | Tỉ lệ từ trong câu thuộc cấp ≤ cấp đích; danh sách từ chưa rõ cấp |
| `model_labels` | Nhãn từng mô hình + tên mô hình + phiên bản |
| `rater_labels` | Nhãn từng GV (ẩn danh, mã rater), có hay không |
| `final_level`, `final_source` | Nhãn cuối và phía quyết định |
| `generation_meta` | Mô hình sinh, ngày, lô, mã prompt |
| `license_status` | `VERIFIED_OPEN` / `UNVERIFIED` / `NON_COMMERCIAL_ONLY` (như D4 kế hoạch mẹ) |

**Nơi lưu (DL4 — ✅ nhóm chọn 2026-10-01: BẢNG RIÊNG, khác mặc định AI là file trong repo):** bảng thứ 10, đề xuất tên `item_label_evidence` (quan hệ 1–1 với `items`, `item_id` UNIQUE, `ON DELETE CASCADE`), các cột theo bảng trên (`target_ref`, `design_level`, `context_coverage`, `model_labels` JSONB, `rater_labels` JSONB, `final_level`, `final_source`, `generation_meta` JSONB, `license_status`). **Tên bảng, cột và quan hệ 1–1 (hay 1–N để giữ lịch sử gán lại) là đề xuất AI, chờ nhóm duyệt** — đây là thay đổi schema nên chỉ áp ở task P2.4/P2.5 của kế hoạch mẹ, sau G6. *(Mặc định gốc, giữ để đối chiếu:* file trong repo, không đổi schema; phương án thay thế: cột JSONB trên `items`, hoặc bảng riêng; hai phương án này **đổi schema** nên cần bạn duyệt và đồng bộ với kế hoạch Prisma.

---

## 4. Thay đổi này có ảnh hưởng tính năng cốt lõi không?

**Không.** Engine (`pickNextSkill`, `selectNextItem`, `computeEAP`, `checkStoppingCriterion`), tham số (θ₀, SE, 25 câu, 8 câu, biên [−2,5; +1,5]) và phạm vi TL đều không đổi. Phương án chỉ ảnh hưởng **nội dung và nhãn dữ liệu** của Item Bank. Theo mặc định DL4, **không đổi schema**.

Hai điểm cần theo dõi: (a) nếu nhóm chọn lưu bằng chứng trong DB (DL4 b/c) thì cộng thêm bảng/cột; (b) nếu độ phủ A2–B1 sau lọc ít hơn 5 câu mỗi kỹ năng trong một cửa sổ Top-5, engine vẫn chạy nhưng exposure tăng (SRS 4.4) — PL.11 kiểm tra điều này.

---

## 5. Ma trận phụ thuộc giữa các việc

```
PL.0 (cổng) ─► PL.1 (cấu hình) ─► PL.2 (chọn đích)  ∥  PL.3 (rubric + câu mẫu neo)
                                          └──────────┬──────────┘
                                                      ▼
                                   PL.4 (prompt + bộ lọc) ─► PL.5 (pilot) ─► PL.6 (sinh đầy đủ + lọc)
                                                                                    │
                                          PL.7 (gán nhãn tự động) ◄─────────────────┘
                                                    │
                                          PL.8 (GV gán độc lập) ⛔👤 ─► PL.9 (đồng thuận + nhãn cuối)
                                                                                    │
                       PL.10 (kiểm tra ngoài bằng CLOTH, có điều kiện DL3)  ∥  PL.11 (irt_b + độ phủ)
                                                                                    ▼
                                                                              PL.12 (khép sổ)
```

---

## 6. Danh sách task (chi tiết)

Ký hiệu: 🤖 Agent · 👤 Người · ⛔ Cổng chặn · `∥` song song được. Mỗi task: **Vào → Làm → Ra → Xác minh**. Đường dẫn tương đối `D:\TLCN`. Task 🔒 cần code/engine chờ G6.

| ID | Việc | Loại | Vào → Làm → Ra | Xác minh |
|---|---|---|---|---|
| PL.0 | **Cổng:** P0.1 và P0.2 của kế hoạch mẹ đã xong; S1 (xác minh CEFR-J) đã xong; DL1–DL4 đã có câu trả lời (DL3 bắt buộc trước PL.4) | 👤 ⛔ | Đọc tracking: các hàng liên quan phải ✅ | Ghi lời duyệt nguyên văn |
| PL.1 | **Cấu hình:** quota (Mục 1), hệ số sinh dư, ngưỡng Q2, số lần dùng tối đa mỗi mục đích, ngưỡng đồng thuận, tên mô hình | 🤖 | Vào: Mục 1, 3, 8 → Ra: file cấu hình (vị trí theo D8) hoặc bảng tham số trong feature-plan nếu trước G6 | Không còn số hardcode trong script; mọi số khớp Mục 1 |
| PL.2 | **Chọn đích kiểm tra:** lọc CEFR-J, lập danh sách mục A2/B1 ứng viên (từ vựng + ngữ pháp có nhãn) đủ cho bảng sinh dư | 🤖 `∥` PL.3 | Vào: CSV đã tải ở S1 → Làm: lọc theo pos/cấp, loại từ chức năng, làm sạch dòng lỗi (Mục 3.1), phân bổ mục cho từng ô kỹ năng × cấp → Ra: bảng đích kiểm tra | **Số đếm thật** bằng lệnh; mỗi ô đủ mục; ngữ pháp A2: báo rõ tỉ lệ câu/dòng thực tế |
| PL.3 | **Rubric gán nhãn + câu mẫu neo:** mô tả A2/B1 bằng ngôn ngữ cụ thể dựa trên CEFR-J; 3–5 câu mẫu mỗi cấp do **đội/GV tự viết** (không trích câu có giấy phép chưa rõ) | 🤖+👤 `∥` PL.2 | Ra: rubric + câu mẫu | GV đọc và xác nhận rubric (ghi tên GV, ngày) |
| PL.4 | **Prompt sinh + schema + bộ lọc tự động** (Mục 3.2–3.3). Prompt few-shot dùng **mô tả chiến lược ra nhiễu bằng lời** (hoặc nguồn đã được phép theo DL3) | 🤖 🔒 phần code | Ra: prompt, schema (Zod), bộ lọc cứng/mềm | Test đơn vị ≥6 ca: thiếu đáp án, 2 đáp án đúng, độ phủ Q2 dưới ngưỡng, từ chưa rõ cấp, `irt_b` ngoài biên, vị trí đáp án lệch |
| PL.5 | **Pilot:** sinh lô nhỏ (N cấu hình, đề xuất ≤10), chạy bộ lọc, **GV xem trực tiếp** | 🤖→👤 | Ra: tỉ lệ loại cứng, tỉ lệ cờ mềm, nhận xét GV, thời gian GV xem/câu | **Số đếm thật**; điều chỉnh hệ số sinh dư và prompt; ghi `AI_USAGE_LOG.md` cho lô |
| PL.6 | **Sinh đầy đủ + lọc tự động** cho toàn bộ 320 câu ứng viên (hoặc số đã chỉnh) theo lô | 🤖 | Ra: tập ứng viên sau lọc, kèm lý do loại | Số lượng từng ô kỹ năng × cấp; nếu ô nào thiếu → sinh bù hoặc dừng hỏi |
| PL.7 | **Gán nhãn tự động** bằng ≥2 mô hình khác nhau và khác mô hình sinh; lấy trung vị | 🤖 | Ra: `model_labels` cho mọi câu | Tỉ lệ khớp A–B báo bằng số đếm; ghi tên/phiên bản mô hình |
| PL.8 | **Hàng đợi GV + gán độc lập:** gồm (i) mọi câu A–B lệch, (ii) mẫu ngẫu nhiên phân tầng từ nhóm khớp; **theo DL1: 1 GV + thành viên nhóm gán độc lập** (không thấy nhãn A/B và nhãn của nhau) | 👤 ⛔ | Ra: `rater_labels` (mã rater, ghi rõ ai là GV, ai là thành viên nhóm) | Hai người làm độc lập; thời gian thực tế mỗi người |
| PL.9 | **Đồng thuận + nhãn cuối** theo Mục 3.4: kappa có trọng số GV–GV, GV–A, GV–B (tính bằng **công cụ độc lập**), ước lượng tỉ lệ sai nhóm khớp | 🤖 | Ra: bảng đồng thuận, nhãn cuối, danh sách câu bị bỏ | Số liệu ghi nguyên trạng, **không làm tròn thành "đạt"**; dưới ngưỡng DL2 → dừng hỏi (Mục 9.3) |
| PL.10 | **Kiểm tra ngoài bằng CLOTH** (Mục 3.5), **chỉ khi DL3 cho phép** | 🤖 ⛔ có điều kiện `∥` PL.11 | Ra: tương quan thứ hạng M/H vs nhãn | Nếu DL3 không cho phép → ⏭, ghi lý do; không điền số |
| PL.11 | **Gán `irt_b` + báo cáo độ phủ:** theo Mục 3.6; số câu A2/B1 mỗi kỹ năng, số câu trong cửa sổ θ∈[−1,+1] | 🤖 `∥` PL.10 | Ra: tập câu đã dán nhãn (định dạng theo DL4) + bảng độ phủ | Mọi `irt_b` ∈ [−1,1); tổng khớp quota hoặc ghi rõ thiếu bao nhiêu; **số đếm thật** |
| PL.12 | **Khép sổ:** `AI_USAGE_LOG.md` (từng lô), `DECISIONS_LOG.md` (DL1–DL5), `weekly-log/Tuan-03.md` (và tuần sau), mục "Hạn chế dữ liệu" | 🤖 | — | Khớp tracking |

---

## 7. Điều kiện phải DỪNG và hỏi (bổ sung cho Mục 8.3 kế hoạch mẹ)

- PL.0: DL1, DL3 chưa có câu trả lời.
- PL.2: số mục đích kiểm tra khả dụng ở một ô ít hơn nhu cầu (đặc biệt ngữ pháp A2).
- PL.5: tỉ lệ loại cứng hoặc cờ mềm quá cao khiến sinh dư ×2 không đủ.
- PL.9: kappa có trọng số GV–GV hoặc GV–A dưới ngưỡng DL2. Phải hỏi: gán lại rubric, bỏ nhóm câu, hạ cấp, hay chấp nhận kèm ghi hạn chế. **Không tự sửa nhãn.**
- PL.10: nhãn không tái hiện thứ tự M < H.
- Bất kỳ yêu cầu gửi nội dung có giấy phép chưa rõ tới dịch vụ bên ngoài.
- Cần đổi schema (DL4 b/c).

---

## 8. Quyết định chờ duyệt

Mặc định là **đề xuất của AI, chưa chốt**. Duyệt kế hoạch mẹ không tự động duyệt các mục này nếu bạn chưa trả lời.

| # | Điểm | **Mặc định** | Phương án thay thế | Đánh đổi |
|---|---|---|---|---|
| DL1 | Số GV chấm độc lập và thời gian dành được | ✅ **Nhóm chọn (2026-10-01): 1 GV + thành viên nhóm tự gán** (hiện chưa có GV nào; cần tìm 1 GV) | 2 GV (khuyến nghị gốc); không GV | **Không đo được đồng thuận GV–GV**; đo GV–nhóm thay thế (thành viên nhóm không phải chuyên gia); nhãn yếu hơn thiết kế gốc P3, phải ghi vào "Hạn chế dữ liệu" |
| DL2 | Ngưỡng đồng thuận chấp nhận (kappa có trọng số) | ✅ **Chốt 0,6 (2026-10-01)** *(con số này là đề xuất của tôi theo quy ước phổ biến "đồng thuận đáng kể"; chưa tra nguồn)* | Cao hơn (0,7–0,8) hoặc thấp hơn | Cao hơn: nhiều câu bị loại; thấp hơn: nhãn kém tin cậy |
| DL3 | Có được xử lý nội dung CLOTH bằng dịch vụ AI **bên ngoài** không | ✅ **Nhóm chọn (2026-10-01): cho phép gửi** (thuần học thuật, Q1) — **khác mặc định AI là "không gửi"**. Rào chắn đề xuất, chưa chốt: chỉ gửi **mẫu nhỏ cần thiết**; chỉ cho few-shot/gán nhãn/kiểm tra phương pháp; **không** đưa nguyên văn câu CLOTH vào Item Bank hoặc báo cáo nộp; kiểm tra điều khoản dữ liệu của gói API đang dùng trước khi gửi; ghi log những gì đã gửi | Không gửi; mô hình cục bộ | Rủi ro còn lại: giấy phép CLOTH chưa xác minh (S3), nội dung đã gửi không thu hồi được, nhiều bộ nghiên cứu cấm chuyển cho bên thứ ba. Bước 4 (kiểm tra bằng CLOTH) được mở |
| DL4 | Nơi lưu bằng chứng gán nhãn | ✅ **Nhóm chọn: bảng riêng** (`item_label_evidence`, đề xuất) | (a) file trong repo (mặc định AI); (b) cột JSONB trên `items` | Truy vấn được và GV xem được lý do nhãn; **bảng thứ 10**, phải sửa kế hoạch Prisma (hiện 9 bảng) và diagram; chi phí và thứ tự: P2.4/P2.5 |
| DL5 | Có áp dụng cùng quy trình cho A1 và B2 không | ✅ **Nhóm chọn: chạy luôn cả A1–B2** (khác mặc định AI là hoãn) | Hoãn tới khi có kết quả A2–B1 | Có đủ bộ 280 câu; nhưng khối lượng gán nhãn ~1,75 lần trong khi chưa có GV (DL1). Khuyến nghị vẫn chạy A2–B1 trước làm pilot |

Các quyết định D2–D9 của kế hoạch mẹ đã được chốt theo mặc định (2026-10-01).

---

## 9. Hướng dẫn dành cho AI Agent thực thi

### 9.1. Quy tắc bất biến
1. Chỉ làm sau khi PL.0 ghi nhận trong tracking. Làm đúng Mục 3 và 6; không "cải tiến" quy trình.
2. Với nguồn có `license_status` ≠ `VERIFIED_OPEN`: **không nhập vào `items`**. **Gửi tới dịch vụ AI bên ngoài chỉ được phép với CLOTH** (DL3 đã được duyệt, kèm rào chắn ở Mục 8); với VNHSGE/GAOKAO và mọi nguồn khác thì **không gửi** cho tới khi có quyết định riêng.
3. Agent **không** tự `APPROVE` câu, không tự thay nhãn GV, không tự quyết định câu bất đồng.
4. Không bịa số liệu (kappa, tỉ lệ khớp, độ phủ, thời gian GV); chưa đo = `N/A`.
5. Mọi tham số (ngưỡng, hệ số sinh dư, mô hình) nằm ở cấu hình, không hardcode.
6. Ngôn ngữ: tài liệu/tracking tiếng Việt; không đổi diagram.
7. Không tự `git init`/commit; không sửa `.docx`, `schema.prisma`, kế hoạch Prisma (trừ khi DL4 b/c được duyệt và có task riêng).
8. Ghi `AI_USAGE_LOG.md` cho **từng lô** sinh câu (prompt gốc, mô hình, tỉ lệ loại).

### 9.2. Thứ tự đọc bắt buộc
`CLAUDE.md` → `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md` → `KE_HOACH_BO_DU_LIEU_ITEM_BANK.md` → file này → `PHAN_TICH_CEFR_J_…` → `PHAN_TICH_CLOTH_…` → `DECISIONS_LOG.md` (#1, #8, #9, #14) → `Tuan2/Phuong_an_sua_doi_AI.md` (Mục 1.3b).

### 9.3. Cách cập nhật tracking
Theo Mục 8.4 của kế hoạch mẹ. Với PL, thêm: ghi tên mô hình và phiên bản mỗi khi dùng; ghi mã rater (không ghi tên GV) vào bằng chứng.

### 9.4. Định nghĩa "xong" cho phase PL
- [ ] 160 câu A2–B1 (hoặc ghi rõ thiếu bao nhiêu) có nhãn cuối và bản ghi bằng chứng đầy đủ.
- [ ] Bảng đồng thuận (GV–GV, GV–A, GV–B) có số đo thật; nếu thiếu GV thì ghi rõ nhãn nào chỉ do mô hình.
- [ ] Không câu nào từ nguồn `UNVERIFIED` trong tập đầu ra.
- [ ] Mọi `irt_b` ∈ khoảng cấp; `calibrated=false`.
- [ ] Mục "Hạn chế dữ liệu" đã soạn (nhãn theo chuyên gia, vòng tròn nhãn).

---

## 10. Rủi ro

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| RL1 | Câu sinh ra kiểm tra nhiều thứ hơn mục đích dự định → nhãn thiết kế (phía A) sai | Phía B và GV độc lập; mẫu ngẫu nhiên từ nhóm khớp để đo sai số |
| RL2 | Cả mô hình sinh và mô hình gán nhãn cùng thiên lệch | Mô hình gán nhãn khác mô hình sinh; GV là nguồn quyết định |
| RL3 | Ngữ pháp A2 chỉ có 32 dòng nhãn → ít đa dạng chủ đề | Nhiều biến thể trên một dòng; mở rộng bằng mục con có GV xác nhận |
| RL4 | GV không đủ thời gian | Chỉ GV gán câu lệch + mẫu; pilot đo thời gian thật trước khi cam kết (PL.5); DL1 |
| RL5 | Ngưỡng độ phủ Q2 quá chặt → loại quá nhiều | Pilot điều chỉnh; ghi lại giá trị cuối và lý do |
| RL6 | Từ vựng không có cấp con → hòa hạng `irt_b` | Chấp nhận, ghi hạn chế; D7 nếu muốn dàn thêm |
| RL7 | CEFR-J xây cho người học Nhật, cấp có thể lệch với người học Việt | GV Việt xác nhận mẫu; ghi hạn chế |
| RL8 | Trễ mốc G1 (Tuần 6) | Chốt DL1/DL3 và chạy PL.1–PL.5 trong Tuần 3–4 |

---

*Tài liệu tạo trong phiên 2026-10-01 bằng Claude Code (Sonnet 5.5). Các con số ngưỡng (95%, kappa 0,6, hệ số sinh dư ×2) là đề xuất chưa tra nguồn, sẽ chốt sau pilot. Thông tin giấy phép không phải tư vấn pháp lý.*
