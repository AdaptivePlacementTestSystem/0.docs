# Phân tích bộ CEFR-J Vocabulary + Grammar Profile: mức độ phù hợp, điểm thiếu và giải pháp bù đắp

- Phạm vi: Tiểu luận (TL) — Adaptive Placement Test (CAT-Rasch)
- Ngày lập: 2026-10-01 (Tuần 3/12)
- Người soạn: Claude Code (Sonnet 5.5), theo yêu cầu người dùng
- Tài liệu liên quan: [`KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`](./KE_HOACH_BO_DU_LIEU_ITEM_BANK.md) (DS1, D2, S1, M1, P3.1, P3.5), [`PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md`](./PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md), [`TRACKING_BO_DU_LIEU_ITEM_BANK.md`](./TRACKING_BO_DU_LIEU_ITEM_BANK.md)
- Nguồn: kho Open Language Profiles https://github.com/openlanguageprofiles/olp-en-cefrj ; trang chính thức http://www.cefr-j.org/download.html
- **Trạng thái:** phân tích tham khảo, **chưa phải quyết định**. Chưa sửa kế hoạch, tracking, SRS hay schema.
- **Mức kiểm chứng:** khác với bản phân tích CLOTH, lần này tôi **đã tải trực tiếp hai file CSV** và đếm bằng script (Mục 2). Các số trong Mục 2 là số đếm thật từ hai file đó. Giấy phép lấy từ README của kho GitHub và trang tải chính thức, **hai nguồn này nói không giống nhau** về Grammar Profile (Mục 3, điểm G1).

---

## 0. Kết luận

1. CEFR-J **phù hợp làm khung phân loại** (nhãn CEFR + chủ đề) cho Item Bank. Dải A1–B2 của nó trùng khít với dải `cefr_target` của SRS 6.2, và độ phủ đủ lớn cho 280 câu.
2. CEFR-J **không có nội dung câu hỏi, không có đáp án, không có độ khó thực đo**. Nó là "bản đồ nội dung theo cấp", không phải bộ đề.
3. Có **bốn điểm thiếu đã xác nhận bằng dữ liệu thật** (Mục 3): giấy phép của Grammar Profile bản mới cần xin phép thương mại; bộ từ vựng không có cấp con; 330/500 dòng ngữ pháp thiếu nhãn cấp; mức độ khó thuộc về *từ/cấu trúc*, không thuộc về *câu hỏi*.
4. **Sửa lại một nhận định trong kế hoạch trước:** `KE_HOACH_BO_DU_LIEU_ITEM_BANK.md` (Mục 2 và DS1) viết cả hai bộ CEFR-J cho phép dùng thương mại. Điều đó **đúng với Vocabulary Profile và với Grammar Profile bản 20180315 trên GitHub**, nhưng **trang chính thức ghi Grammar Profile bản 2025 cần liên hệ xin phép và có thể mất phí khi dùng thương mại** (Mục 3, G1).
5. Nên dùng bản nào của Grammar Profile và có xin phép hay không là quyết định của bạn (Mục 6).

---

## 1. Vì sao CEFR-J đáng chọn làm khung

| # | Luận điểm | Liên hệ với bài toán |
|---|---|---|
| L1 | **Dải cấp trùng khít.** CEFR-J phủ A1–B2; bank của SRS 6.2/6.3 cũng chỉ A1–B2. Cấp C1/C2 (bộ Octanove, CC BY-SA) nằm ngoài dải nên không cần. | Không phải ánh xạ hay cắt bớt giữa hai thang. |
| L2 | **Độ phủ lớn.** Từ vựng 7.799 mục (bản 1.5) với 1.164 A1, 1.411 A2, 2.446 B1, 2.778 B2. Ngữ pháp 500 dòng. | Bank cần 160 câu từ vựng và 120 câu ngữ pháp (SRS 6.3). Số mục sẵn có nhiều gấp nhiều lần nhu cầu, nên chọn lọc và tránh trùng được. |
| L3 | **Có sẵn chủ đề.** Cột `CoreInventory 1/2` gắn chủ đề cho khoảng 1.698 từ (ví dụ Education, Work and Jobs, Food and drink). Ngữ pháp có mã (`Shorthand Code`) và tên mục cấu trúc. | Cung cấp `topic_tag` cho `Item` (SRS 6.2) mà không phải tự đặt tên chủ đề, đồng thời hỗ trợ F-10 (auto-tag, P2). |
| L4 | **Ngữ pháp có cấp con.** Cột `CEFR-J Level` có A1.1, A1.2, A1.3, A2.1, A2.2, B1.1, B1.2, B2.1, B2.2. | Cho 2–3 bậc trong mỗi cấp, đúng thứ cần để dàn `irt_b` trong cấp và tránh hòa hạng Top-5 (kế hoạch M1/P3.5). |
| L5 | **Có đối chiếu chéo.** File ngữ pháp có thêm cột `Core Inventory`, `EGP`, `GSELO`, `FREQ*DISP`; file từ vựng có `CoreInventory` và `Threshold`. | Có thể đo mức khớp giữa CEFR-J và các hệ khác ngay trong cùng file, làm bằng chứng kiểm định nhãn mà không phải nhập dữ liệu có bản quyền. |
| L6 | **Nguồn học thuật rõ ràng.** Tono Laboratory, Đại học Ngoại ngữ Tokyo (TUFS); có yêu cầu trích dẫn cụ thể. | Dễ giải trình trước hội đồng "nhãn CEFR lấy từ đâu". |
| L7 | **Khớp phương án B và SRS 6.1 Giai đoạn 0–2** (AI sinh → GV duyệt → gán `b_i` theo cấp CEFR). | Không phát sinh việc ngoài phạm vi. |
| L8 | **Tải được ngay, định dạng CSV.** | Có thể đếm, lọc, tái lập bằng script. |

---

## 2. Dữ liệu đã kiểm chứng (đếm từ file tải về)

Nguồn tải: `raw.githubusercontent.com/openlanguageprofiles/olp-en-cefrj/master/…` (2026-10-01). Đếm bằng script Python trên hai file.

| File | Kích thước | SHA-256 |
|---|---|---|
| `cefrj-vocabulary-profile-1.5.csv` | 233.214 byte | `b0dd3c635f1c9a4fdf1490c7e5b7c48e8bbe55b652ad0c9860a95f98e10ae498` |
| `cefrj-grammar-profile-20180315.csv` | 72.272 byte | `94953af376c1336166257e56c78d2139697b40ad8cf6f1235d8f9e89c2efc428` |

### 2.1. Vocabulary Profile v1.5

Cột: `headword, pos, CEFR, CoreInventory 1, CoreInventory 2, Threshold`. **7.799 dòng.**

| Cấp | Số dòng (file 1.5) | Số mục theo trang chính thức v1.6 |
|---|---|---|
| A1 | 1.164 | 1.166 |
| A2 | 1.411 | 1.411 |
| B1 | 2.446 | 2.445 |
| B2 | 2.778 | 2.779 |
| Tổng | 7.799 | 7.801 |

Số liệu hai phiên bản lệch nhẹ (bản trên GitHub là 1.5, bản chính thức là 1.6, cập nhật 2020-03-24). Chọn bản nào phải ghi rõ trong tài liệu và phần trích dẫn.

Phân bố loại từ: noun 4.091, adjective 1.494, verb 1.349, adverb 552, còn lại dưới 100 mỗi loại. Riêng cấp A2: noun 773, adjective 243, verb 204, adverb 122.

### 2.2. Grammar Profile 20180315

Cột: `ID, Shorthand Code, Grammatical Item, Sentence Type, CEFR-J Level, FREQ*DISP, Core Inventory, EGP, GSELO, Notes`. **500 dòng**, trong đó 262 dòng có ID cấp trên (không có dấu `-`) và 238 dòng là mục con.

| Cấp | Số dòng có nhãn `CEFR-J Level` | Chi tiết |
|---|---|---|
| A1 | 63 | A1.1: 33, A1.2: 19, A1.3: 11 |
| A2 | 32 | A2.1: 24, A2.2: 7, `A2` (không cấp con): 1 |
| B1 | 41 | B1.1: 25, B1.2: 13, `B1` (không cấp con): 3 |
| B2 | 34 | B2.1: 22, B2.2: 7, `B2.2*`: 4, `B2` (không cấp con): 1 |
| **Có nhãn** | **170** | |
| **Không có nhãn** | **330** (66%) | 211 là mục con; 119 là mục cấp trên bị bỏ trống |

---

## 3. Điểm thiếu và giải pháp bù

Mức độ: 🔴 chặn hoặc cần quyết định · 🟡 có giải pháp · 🟢 ghi nhận.

| # | Thiếu gì | Mức | Bằng chứng | Giải pháp bù | Vì sao |
|---|---|---|---|---|---|
| G1 | **Giấy phép Grammar Profile không nhất quán giữa hai nguồn.** README kho GitHub (bản 20180315): dùng cho nghiên cứu và thương mại, không phí, kèm trích dẫn. Trang chính thức (bản 2025): nghiên cứu và giáo dục được phép; **thương mại cần liên hệ và có thể mất phí**. Vocabulary Profile: cả hai nguồn đều cho thương mại kèm trích dẫn. | 🔴 phụ thuộc Q1 | Đọc trực tiếp hai trang | (a) Nếu Q1 = phi thương mại: dùng được cả hai bản. (b) Nếu có thể thương mại: dùng bản 20180315 theo README GitHub **và** gửi email xác nhận cho Tono Laboratory rằng điều khoản README vẫn áp dụng cho bản đã tải. (c) Không dùng bản 2025 cho mục đích thương mại khi chưa được phép. Ghi rõ phiên bản, ngày tải, đúng câu trích dẫn theo yêu cầu. | Chỉ có chủ sở hữu mới xác nhận được điều khoản còn hiệu lực; không tự suy luận. |
| G2 | **Từ vựng không có cấp con** (chỉ A1, A2, B1, B2). Dàn `irt_b` trong cấp (M1) không thể dựa vào cấp con như ngữ pháp. | 🟡 | Cột `CEFR` chỉ có 4 giá trị | Dùng tín hiệu phụ **kiểm chứng được**: tần suất từ, độ dài, loại từ, số nghĩa. Nguồn tần suất cần giấy phép rõ (NGSL là CC BY-SA, xem D7); hoặc tự đếm tần suất từ một kho văn bản đã được phép dùng. **Chưa chốt**, thuộc quyết định D7. Hiệu chuẩn bằng GV (kế hoạch P4.2) để xem tín hiệu phụ có khớp cảm nhận độ khó không. | Không bịa cấp con. Tín hiệu phụ chỉ để sắp xếp trong cấp, không nâng thành nhãn mới. |
| G3 | **330/500 dòng ngữ pháp thiếu nhãn cấp** (66%) | 🟡 | 211 mục con, 119 mục cấp trên trống | (a) Chỉ sinh câu từ 170 dòng đã có nhãn (đủ số lượng cho nhu cầu, xem Mục 4). (b) Mục con thừa hưởng cấp của mục cha chỉ khi GV xác nhận mẫu. (c) 119 mục cấp trên bị trống: bỏ hoặc cho GV gán cấp. | Thừa hưởng tự động có thể sai (mục con phủ định/nghi vấn thường khó hơn mục khẳng định). |
| G4 | **Không có nội dung câu hỏi** (câu dẫn, 4 đáp án, đáp án đúng). Dòng ngữ pháp chỉ có tên cấu trúc, không có ví dụ câu. | 🔴 cốt lõi | Cấu trúc cột ở 2.1–2.2 | Phần sinh câu là việc của AI + GV duyệt (phương án B): AI sinh câu theo mục khung, nhiễu thiết kế theo lỗi điển hình, có thể dùng CLOTH làm mẫu few-shot nếu giấy phép cho phép. | CEFR-J là bản đồ, không phải đề. |
| G5 | **Độ khó thuộc về từ/cấu trúc, không thuộc về câu hỏi.** Cùng một từ B1 có thể xuất hiện trong câu dễ hoặc câu khó tùy nhiễu và ngữ cảnh. | 🟡 | Bản chất dữ liệu | `irt_b` ban đầu = neo theo cấp (SRS 4.6) + dàn trong cấp; `calibrated=false`; kiểm định bằng GV (kappa) và mô phỏng độ nhạy; đường nâng cấp MMLE sau này. | Giống các biện pháp M1–M6 của kế hoạch chính. |
| G6 | **Nhãn theo từ + loại từ, không theo nghĩa.** Một từ nhiều nghĩa chỉ có một cấp. | 🟡 | Cột `headword, pos, CEFR` | Câu từ vựng phải chỉ định rõ nghĩa được hỏi trong ngữ cảnh; GV loại câu hỏi nghĩa hiếm không cùng cấp với nhãn. | Tránh gán nhãn A2 cho câu thực sự hỏi nghĩa B2. |
| G7 | **Xây cho người học Nhật.** CEFR-J điều chỉnh CEFR theo bối cảnh giáo dục tiếng Anh ở Nhật, nên cấp của một số mục có thể lệch so với người học Việt. | 🟡 | Mô tả nguồn (kết quả tìm kiếm) | GV Việt kiểm tra lại mẫu phân tầng; đối chiếu với các cột `EGP`, `GSELO`, `Core Inventory` đã có trong file ngữ pháp; ghi vào "Hạn chế dữ liệu". | Không có nguồn nào chắc chắn đúng cho người học Việt; cần kiểm định cục bộ. |
| G8 | **Chất lượng dữ liệu có lỗi nhỏ.** Cột `Sentence Type` của 3 dòng (ID 132, 135, 136) chứa giá trị `B1.1`, `A2.2` (lẽ ra thuộc cột cấp). Cột cấp chứa `B2.2*` (4 dòng, dấu `*` chưa rõ nghĩa), `B1`/`A2`/`B2` không có cấp con, và nhiều giá trị đối chiếu dạng khoảng (`A1-C1`). | 🟢 | Đếm ở 2.2 | Ghi bước làm sạch có kiểm tra: không tự đoán ý nghĩa dấu `*`; hỏi người dùng hoặc tra ghi chú đi kèm bản chính thức trước khi dùng 4 dòng này. | Dữ liệu nền sai làm hỏng cả chuỗi phía sau. |
| G9 | **Không có Pre-A1 và C1/C2 trong bộ chính.** | 🟢 | Dải A1–B2 | Không cần cho TL (SRS 4.7 ghi rõ Pre-A1/C1+ nằm ngoài vùng phủ Item Bank). | Phù hợp phạm vi. |

---

## 4. Đối chiếu năng lực cung ứng với nhu cầu của bank (SRS 6.3)

Đây là phép đếm số lượng, không phải đảm bảo chất lượng.

**Từ vựng (cần 160 câu):**

| Cấp | Cần | Mục khả dụng trong file 1.5 | Nhận xét |
|---|---|---|---|
| A1 | 40 | 1.164 | Dư nhiều |
| A2 | 45 | 1.411 | Dư nhiều |
| B1 | 45 | 2.446 | Dư nhiều |
| B2 | 30 | 2.778 | Dư nhiều |

**Ngữ pháp (cần 120 câu):**

| Cấp | Cần | Dòng có nhãn | Câu/dòng cần tối thiểu | Nhận xét |
|---|---|---|---|---|
| A1 | 30 | 63 | 0,5 | Dư |
| A2 | 35 | 32 | 1,1 | **Vừa đủ, ít đa dạng chủ đề**; nên bổ sung bằng mục con đã được GV xác nhận cấp |
| B1 | 35 | 41 | 0,85 | Đủ |
| B2 | 20 | 34 (gồm 4 dòng `B2.2*` chưa rõ) | 0,6 | Đủ nếu loại 4 dòng chưa rõ thì còn 30 |

**Điểm nghẽn thật là ngữ pháp cấp A2** (vùng θ≈0, vùng mỏng nhất theo SRS 4.4): 32 dòng cho 35 câu. Giải pháp: sinh nhiều biến thể (ngữ cảnh, nhiễu khác nhau) trên cùng một dòng, hoặc mở rộng bằng mục con (G3). Đây cũng là vùng CLOTH được đề xuất bù (xem phân tích CLOTH).

---

## 5. Cách dùng đề xuất trong pipeline (chưa thực hiện)

| Bước | Dùng CEFR-J để | Liên hệ kế hoạch |
|---|---|---|
| 1 | Chọn mục: lập bảng 280 hàng gắn kỹ năng × cấp với mục từ vựng/ngữ pháp cụ thể | P3.1 |
| 2 | Sinh câu hỏi (Gemini): mỗi câu dựa trên một mục khung, ghi mã mục (`ID`/`headword`) để truy vết | P3.2, P3.4, `generated_from_ref_ids` (D4) |
| 3 | `topic_tag`: lấy từ `CoreInventory 1` (từ vựng) hoặc `Shorthand Code`/tên cấu trúc (ngữ pháp) | R-D5 |
| 4 | `cefr_target`: lấy từ cấp của mục khung | R-D3 |
| 5 | `irt_b`: trung điểm khoảng logit của cấp (SRS 4.6) + dàn theo cấp con (ngữ pháp) hoặc tín hiệu phụ (từ vựng); `calibrated=false` | P3.5, M1 |
| 6 | Kiểm định: GV chấm độc lập mẫu, tính đồng thuận; đối chiếu `EGP`/`GSELO` có sẵn | P4.1, P4.2 |
| 7 | Ghi trích dẫn đúng yêu cầu giấy phép trong báo cáo và tài liệu | S1 |

---

## 6. Đánh giá thẳng thắn

- **Điểm mạnh nhất:** giấy phép tương đối sạch (với từ vựng và bản ngữ pháp 2018), dữ liệu tải được, đếm được, và nhãn tới từ một nhóm nghiên cứu có tên. Đây là lý do nó đứng đầu trong các bộ đã khảo sát, chứ không phải vì nó đầy đủ.
- **Điểm yếu nhất:** nó chỉ cung cấp "cái gì ở cấp nào", còn câu hỏi, nhiễu và độ khó thực đo phải do nhóm tạo ra và kiểm định. Nếu bỏ qua bước GV kiểm định (kappa), toàn bộ `irt_b` chỉ là suy diễn từ nhãn.
- **Nhận định đã đổi so với kế hoạch trước:** nhãn cấp con có ở ngữ pháp (nhưng chỉ 170 dòng) và **không có ở từ vựng**. Kế hoạch trước để mở câu hỏi này; nay đã có đáp án.
- **Vòng tròn nhãn:** CEFR kết quả của sinh viên dựa trên CEFR của câu hỏi, mà CEFR của câu hỏi lấy từ CEFR-J. Không dùng kết quả để "chứng minh độ chính xác" của CEFR-J; ghi vào "Hạn chế".

### Quyết định cần bạn xác nhận

> **Đã chốt theo mặc định (2026-10-01):** Q-A = bản 20180315; Q-B = chỉ cần gửi email xác nhận nếu sau này thương mại hóa (hiện thuần học thuật nên chưa cần); Q-C = không dàn thêm bằng tín hiệu phụ (D7: không dùng NGSL) nên từ vựng cùng cấp hòa hạng `irt_b`; Q-D = chỉ dùng 170 dòng ngữ pháp có nhãn, mục con chỉ thừa hưởng cấp khi GV xác nhận mẫu. *Lưu ý:* vì thuần học thuật, bản 2025 dùng được cho nghiên cứu/giáo dục nhưng chưa tải để đếm.

| # | Câu hỏi | Mặc định tôi đề xuất | Đánh đổi |
|---|---|---|---|
| Q-A | Dùng bản Grammar Profile nào? | **20180315** (README GitHub cho thương mại, có cấp con, đã tải và đếm) | Bản 2025 có thể mới hơn, nhưng cần xin phép thương mại và tôi **chưa tải được** để đếm |
| Q-B | Có gửi email xác nhận giấy phép cho Tono Laboratory (TUFS) không? | **Có, nếu Q1 (kế hoạch chính) là có khả năng thương mại**; không cần nếu thuần học thuật | Mất thời gian chờ phản hồi; không chặn các việc khác |
| Q-C | Dàn `irt_b` trong cấp cho từ vựng bằng gì? (G2) | Chưa chốt; gắn với D7 của kế hoạch chính | Dùng NGSL (CC BY-SA) có tín hiệu tần suất nhưng ràng buộc share-alike; không dùng thì chỉ có neo cấp (hòa hạng nhiều) |
| Q-D | Với 119 dòng cấp trên trống và 211 mục con: bỏ, thừa hưởng, hay GV gán? (G3) | Chỉ dùng 170 dòng có nhãn; thừa hưởng chỉ khi GV xác nhận mẫu | Thừa hưởng nhanh nhưng có thể sai |

---

## 7. Việc cần làm tiếp (chưa thực hiện)

| # | Việc | Người |
|---|---|---|
| 1 | Trả lời Q-A đến Q-D và Q1 của kế hoạch chính (phi thương mại hay EduZ thương mại) | 👤 |
| 2 | Gửi email xác nhận giấy phép cho Tono Laboratory nếu cần (Q-B) | 👤 (Agent soạn nội dung ở S1) |
| 3 | Cập nhật `KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`: sửa nhận định giấy phép Grammar Profile ở Mục 2 và DS1, ghi kết quả S1 thật (bản 1.5/20180315, số đếm, sub-level chỉ có ở ngữ pháp), thêm G2/G3/G8 vào rủi ro; cập nhật `TRACKING_BO_DU_LIEU_ITEM_BANK.md` mục "Kết quả xác minh nguồn" | 🤖 sau khi bạn đồng ý |
| 4 | Tìm cách tải và đọc bản Grammar Profile 2025 (Excel/PDF trong ZIP) để so với bản 2018 | 🤖 |
| 5 | Làm sạch dữ liệu (G8) theo bước có kiểm tra | 🤖 sau cổng P0 |

---

*Tài liệu tạo trong phiên 2026-10-01 bằng Claude Code (Sonnet 5.5). Số đếm ở Mục 2 là từ file tải về lúc lập tài liệu; giấy phép lấy từ README kho GitHub và trang cefr-j.org tại thời điểm tra cứu, không phải tư vấn pháp lý. Mô tả "xây cho người học Nhật" lấy từ kết quả tìm kiếm, chưa đọc từ tài liệu gốc của Tono.*
