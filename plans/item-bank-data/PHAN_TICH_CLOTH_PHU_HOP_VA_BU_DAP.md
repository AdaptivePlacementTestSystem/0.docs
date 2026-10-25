# Phân tích bộ dữ liệu CLOTH: mức độ phù hợp, điểm thiếu và giải pháp bù đắp

- Phạm vi: Tiểu luận (TL) — Adaptive Placement Test (CAT-Rasch)
- Ngày lập: 2026-10-01 (Tuần 3/12)
- Người soạn: Claude Code (Sonnet 5.5), theo yêu cầu người dùng
- Tài liệu liên quan: [`KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`](./KE_HOACH_BO_DU_LIEU_ITEM_BANK.md) (DS2, D6, S3, P4.2), [`TRACKING_BO_DU_LIEU_ITEM_BANK.md`](./TRACKING_BO_DU_LIEU_ITEM_BANK.md)
- Nguồn: Xie et al., "Large-scale Cloze Test Dataset Created by Teachers", EMNLP 2018 — https://arxiv.org/abs/1711.03225 ; trang dữ liệu http://www.cs.cmu.edu/~glai1/data/cloth/
- **Trạng thái:** phân tích tham khảo, **chưa phải quyết định**. Chưa sửa kế hoạch, tracking, SRS hay schema.
- **Mức kiểm chứng:** quy mô dữ liệu (7.131 đoạn, 99.433 câu, chia CLOTH-M/CLOTH-H) đã đối chiếu qua kết quả tìm kiếm. Các điểm sau **viết từ trí nhớ về bài báo, chưa đọc lại trực tiếp, phải kiểm chứng ở task S3**: phân loại dạng câu hỏi (ngữ pháp, suy luận ngắn/dài hạn…), ánh xạ cấp 2/cấp 3 Trung Quốc sang CEFR theo thang CSE 2018. **Giấy phép chưa xác minh** (bài báo không nêu; trang CMU không tải được khi kiểm tra).

---

## 0. Kết luận

1. CLOTH phù hợp làm **nguồn nội dung cho vùng A2–B1**, không phù hợp làm bộ dữ liệu duy nhất. Nó không có nhãn cấp CEFR, không có độ khó thực đo, và không phủ A1/B2.
2. Thiếu nhãn cấp độ giải quyết được bằng quy trình gán nhãn 4 bước (Mục 3). Nhãn thu được là **nhãn ước lượng có GV kiểm chứng**, không phải nhãn gốc.
3. Hai điểm thiếu lớn nhất là **giấy phép chưa rõ** (chặn việc phân phối cho sinh viên) và **định dạng theo đoạn văn** (vi phạm độc lập cục bộ của IRT nếu dùng sai). Cả hai có giải pháp ở Mục 4.
4. CLOTH **bổ sung** cho phương án B (khung CEFR-J + AI sinh + GV duyệt), không thay thế. Phần A1 và B2 vẫn phải đi theo phương án B.
5. Nếu giấy phép bị từ chối, CLOTH vẫn dùng được làm mẫu few-shot nội bộ. Hệ thống không phụ thuộc vào việc nhập thẳng câu CLOTH vào `items`.

---

## 1. Vì sao CLOTH đáng dùng

| # | Luận điểm | Liên hệ với bài toán |
|---|---|---|
| L1 | **Đáp án nhiễu do giáo viên soạn.** Bài báo mô tả các lựa chọn được thiết kế tinh tế. Đây là phần khó nhất của một câu trắc nghiệm. | Câu AI sinh hay lỗi ở nhiễu quá dễ hoặc có hai đáp án đúng. CLOTH cho mẫu chuẩn để làm few-shot và để so sánh chất lượng. |
| L2 | **Có sẵn dạng 4 lựa chọn, 1 đáp án đúng.** | Khớp lược đồ `Item` (`options` A–D, `correct_answer`) mà không đổi cấu trúc. |
| L3 | **Quy mô 99.433 câu.** | Bank chỉ cần khoảng 280 câu (SRS 6.3), nên có thể chọn lọc kỹ thay vì lấy hết. |
| L4 | **Phủ vùng A2–B1.** CLOTH-M thuộc cấp 2, CLOTH-H thuộc cấp 3. Theo trí nhớ về thang CSE 2018, đầu ra cấp 2 xấp xỉ A2 và đầu ra cấp 3 xấp xỉ B1 (cần kiểm chứng). | SRS 4.4 ghi vùng A2–B1 (θ≈0) là vùng mỏng nhất của bank và dễ lộ đề nhất. Đây đúng là vùng cần thêm câu chất lượng. |
| L5 | **Đã qua thực tế thi cử**, có bài báo EMNLP 2018 kèm số liệu người làm và mô hình. | Dễ giải trình nguồn có uy tín học thuật. Lưu ý: "đã dùng trong thi cử" không đồng nghĩa với "đã hiệu chỉnh độ khó bằng IRT". |
| L6 | **Khớp Quyết định #8/#9** (ngân hàng tham chiếu cho few-shot). | Không phát sinh luồng mới ngoài kế hoạch. |

---

## 2. Điểm thiếu của CLOTH so với `Item`

| Trường `Item` | CLOTH cung cấp | Thiếu gì |
|---|---|---|
| `content` | Có, nhưng là chỗ trống trong **đoạn văn** | Phải tách thành câu đứng một mình |
| `options`, `correct_answer` | Có (4 lựa chọn) | — |
| `skill` | Không rõ ràng (cloze trộn từ vựng và ngữ pháp) | Phải gán |
| `topic_tag` | Không | Phải gán |
| `cefr_target` | Chỉ chia M/H | Phải gán |
| `irt_b` | Không | Phải ước lượng |
| Giấy phép phân phối | Chưa rõ | Phải xác nhận |
| A1, B2 | Gần như không phủ | Phải lấy nguồn khác |

---

## 3. Giải quyết việc không có nhãn cấp độ (quy trình 4 bước)

| Bước | Làm gì | Cho ra gì | Điều kiện chuyển bước |
|---|---|---|---|
| 1. Tiên nghiệm thô | Dùng chia M/H làm cận: câu M thường nằm ở A1–A2+, câu H thường nằm ở A2+–B1+. | Dải khả dĩ, chưa phải nhãn | Kiểm chứng ánh xạ M/H → CEFR ở S3 |
| 2. Đặc trưng ngôn ngữ | Dùng CEFR-J (giấy phép sạch) để tra cấp của từ đáp án, từ nhiễu và các từ trong câu; gắn mục ngữ pháp CEFR-J nếu câu kiểm tra cấu trúc; tính thêm độ dài và độ phức tạp của câu. | Điểm đặc trưng có thể tái lập | Phụ thuộc kết quả S1 (số mục A1–B2, có sub-level hay không) |
| 3. Hiệu chuẩn bằng GV | 2 GV gán cấp độc lập cho mẫu phân tầng khoảng 150–200 câu (con số đề xuất, chưa chốt). Dùng mẫu đó học ánh xạ đặc trưng → cấp CEFR (hồi quy thứ tự), áp cho phần còn lại. | Nhãn kèm số đo đồng thuận (kappa có trọng số) | Cần Q4 (có 2 GV chấm hay không) |
| 4. Tín hiệu phụ | Cho vài mô hình ngôn ngữ làm bài; dùng tỉ lệ đúng/sai làm "thí sinh giả lập". | Cờ cho câu bất thường | Chỉ để lọc ngoại lai, **không** dùng làm độ khó chính (độ khó với mô hình không đồng nhất với độ khó với người) |

- `irt_b` ban đầu lấy trung điểm khoảng logit của cấp (SRS 4.6) cộng dàn đều trong cấp, `calibrated=false`, đúng phương án B.
- Nếu mức đồng thuận GV thấp: **không tự sửa nhãn**, dừng và báo người dùng quyết định (kế hoạch P4.2).
- Mọi số liệu (kappa, tỉ lệ khớp) chỉ ghi khi đã đo thật; chưa đo thì ghi `N/A`.

---

## 4. Điểm thiếu và giải pháp bù

| # | Thiếu gì | Mức | Giải pháp bù | Vì sao giải pháp đó |
|---|---|---|---|---|
| G1 | **Giấy phép chưa rõ** | 🔴 chặn phân phối | Gửi email xin xác nhận bằng văn bản (S3): mục đích học thuật, có phân phối lại cho SV làm bài hay không. Tới khi có trả lời: chỉ dùng nội bộ làm mẫu few-shot, `license_status=UNVERIFIED`, không hiển thị cho SV, không nhập vào `items`. | Không thể "chấp nhận rủi ro" thay chủ sở hữu. Quyết định #9 chỉ an toàn khi giấy phép được xác nhận. |
| G2 | **Không phủ A1 và B2** (bank cần A1 70 + B2 50 = 120/280 câu; CLOTH tối đa phủ khoảng 160 câu A2+B1, tức 57%) | 🔴 | Phần A1/B2 đi theo phương án B (CEFR-J + AI sinh + GV duyệt). | CLOTH bổ sung, không thay thế. |
| G3 | **Đoạn văn, không phải câu độc lập** (mỗi đoạn khoảng 14 chỗ trống phụ thuộc ngữ cảnh); dùng nhiều chỗ của cùng đoạn vi phạm độc lập cục bộ của IRT | 🟡 | (a) Chỉ lấy chỗ trống mà đáp án **xác định được trong cùng một câu**, loại dạng suy luận dài hạn. (b) Viết lại thành câu đứng một mình. (c) Tối đa 1 câu mỗi đoạn trong một phiên thi. (d) LLM kiểm tra "đáp án duy nhất khi chỉ có câu này", GV duyệt. | Bảo toàn giả định của mô hình Rasch và tránh lộ đoạn văn. |
| G4 | **Trộn kỹ năng** (cloze trộn từ vựng và ngữ pháp) | 🟡 | Gán `skill` bằng luật theo loại từ cộng LLM, GV xác nhận. Gán `topic_tag` theo mục ngữ pháp CEFR-J. | Class Diagram yêu cầu `skill` rõ ràng cho `pickNextSkill()`. |
| G5 | **Ngữ cảnh người học khác** (nhiễu thiết kế cho lỗi điển hình của người Trung Quốc, không phải người Việt) | 🟡 | GV loại câu có nhiễu quá đặc thù; ghi vào mục "Hạn chế". | Giảm rủi ro nhiễu không còn "hấp dẫn" với SV Việt. |
| G6 | **Độ khó thực đo bằng 0** | 🟡 | `irt_b` neo CEFR + mô phỏng Monte Carlo độ nhạy + đường nâng cấp MMLE (F-12) sau này. | Giống các biện pháp M1–M6 của kế hoạch. |
| G7 | **Dữ liệu cào từ web, có thể lỗi/thiếu sạch** | 🟢 | Lọc cấu trúc + self-consistency check + GV duyệt từng câu. | Đã có trong thiết kế (`Phuong_an_sua_doi_AI.md` 1.3b). |

---

## 5. Đánh giá thẳng thắn

- **Không thể khẳng định "chắc chắn phù hợp".** Việc dùng được phụ thuộc vào giấy phép (G1) và mức đồng thuận GV (bước 3). Cả hai chưa có số liệu.
- **Vòng tròn nhãn:** CEFR của kết quả thi dựa trên CEFR gán cho câu hỏi, nên không dùng kết quả để chứng minh độ chính xác. Ghi trong mục "Hạn chế dữ liệu".
- **Chi phí ẩn:** bước 3 cần thời gian của 2 GV. Nếu không có, nhãn CLOTH chỉ dựa trên đặc trưng ngôn ngữ và có độ tin cậy thấp hơn nhãn của phương án B (vì nhãn B xuất phát trực tiếp từ mục khung CEFR-J).
- **Vai trò theo kịch bản:**

| Kịch bản | Vai trò CLOTH |
|---|---|
| Giấy phép được xác nhận + GV đồng thuận tốt | Nguồn nội dung chính cho A2–B1, nhập vào `items` sau GV duyệt |
| Giấy phép được xác nhận + GV đồng thuận thấp | Nguồn nội dung có điều kiện; dừng hỏi người dùng (đổi dải `irt_b` hoặc ghi hạn chế) |
| Giấy phép bị từ chối hoặc không phản hồi | Chỉ làm mẫu few-shot nội bộ; không nhập vào `items` |

---

## 6. Việc cần làm tiếp (chưa thực hiện)

| # | Việc | Người |
|---|---|---|
| 1 | Gửi email xin giấy phép CLOTH | 👤 (Agent soạn nội dung ở S3) |
| 2 | Trả lời **Q1** (phi thương mại hay EduZ thương mại) và **Q4** (có 2 GV chấm hay không) | 👤 |
| 3 | Sửa `KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`: D6 thành "CLOTH cho vùng A2–B1 theo quy trình 4 bước"; thêm task trích xuất và chuẩn hóa câu, task hiệu chuẩn GV; thêm G2/G3 vào bảng rủi ro; cập nhật tracking tương ứng | 🤖 sau khi bạn đồng ý |
| 4 | Kiểm chứng trực tiếp bài báo (dạng câu hỏi, ánh xạ M/H → CEFR) và trang dữ liệu CMU | 🤖 ở S3 |

---

*Tài liệu tạo trong phiên 2026-10-01 bằng Claude Code (Sonnet 5.5). Thông tin giấy phép và ánh xạ cấp độ chưa xác minh trực tiếp; không phải tư vấn pháp lý.*
