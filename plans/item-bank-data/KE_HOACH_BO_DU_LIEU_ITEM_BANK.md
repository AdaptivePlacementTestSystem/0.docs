# Kế hoạch: Chọn bộ dữ liệu cho Item Bank — đánh giá, thiếu hụt, giải pháp bù, triển khai

- Phạm vi: Tiểu luận (TL) — Adaptive Placement Test (CAT-Rasch)
- Ngày lập: 2026-10-01 (Tuần 3/12)
- Người soạn: Claude Code (Sonnet 5.5), theo yêu cầu người dùng (vai trò Senior SE + PM)
- File theo dõi đi kèm (AI Agent tự cập nhật sau mỗi bước): [`TRACKING_BO_DU_LIEU_ITEM_BANK.md`](./TRACKING_BO_DU_LIEU_ITEM_BANK.md)
- **Tài liệu phân tích kèm theo (cập nhật 2026-10-01, phiên 2):** [`PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md`](./PHAN_TICH_CLOTH_PHU_HOP_VA_BU_DAP.md) · [`PHAN_TICH_CEFR_J_PHU_HOP_VA_BU_DAP.md`](./PHAN_TICH_CEFR_J_PHU_HOP_VA_BU_DAP.md) · [`PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md`](./PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md) (chi tiết phase **PL**, Mục 7).
- Nguồn đã đối chiếu: `0.docs/SRS_TLCN_v2.6_Final.docx` (Mục 4.2, 4.4, 4.6, 6.1–6.4, XII, Risk R1/R2), `0.docs/Mo_ta_So_do_Lop_ClassDiagram.md` (`Item`), `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md` (TC1, TC2.1, TC2.3), `0.docs/tracking/DECISIONS_LOG.md` (#1, #8, #9, #14, #15–#18), `Tuan2/Phuong_an_sua_doi_AI.md`, `Tuan3/KE_HOACH_PRISMA_SCHEMA_VA_6_HANG_MUC.md` (Q2, A3, P4.D1), và các nguồn web ở Mục 2 (tra cứu 2026-10-01).
- **Trạng thái phê duyệt (cập nhật 2026-10-01):** ✅ **Người dùng đã chốt các mặc định còn lại (P0.1) — kế hoạch được coi là đã duyệt, gồm D2, D4, D5, D7, D8, D9 theo cột "Mặc định" ở Mục 6**, cùng D1 = P3, D3, Q1, DL1–DL5 (xem file P3). Phần dưới là ghi chú trạng thái trước đó: ✅ **D1 đã được người dùng chọn: phương án P3 (lai)** trong phiên 2026-10-01 (chi tiết quy trình ở `PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md`; ghi `DECISIONS_LOG.md` ở task P2.1). ⬜ **Còn CHỜ NGƯỜI DUYỆT:** toàn bộ kế hoạch (P0.1), các quyết định D2–D9 và DL1–DL5 (Mục 6 và file P3). Sau khi bạn duyệt, mọi việc ở Mục 7 được coi là đã được cho phép; AI Agent chỉ dừng hỏi ở các điều kiện của Mục 8.3.
- **Cách tôi hiểu "Lược đồ trên" trong yêu cầu:** vì yêu cầu này nói về bộ dữ liệu, tôi hiểu "lược đồ" là **lược đồ của `Item`** (SRS 6.2 + Class Diagram + schema Prisma đã lập ở Tuan3) **đối chiếu với lược đồ của từng bộ dữ liệu ứng viên**. Nếu bạn muốn nói tới lược đồ khác, báo lại — Mục 3.2 là phần bị ảnh hưởng.
- **Lưu ý trạng thái repo:** chưa có git repo, chưa có `apps/backend` (G6 chưa chạy). Kế hoạch chia làm 2 loại task: *tài liệu/dữ liệu* (làm được ngay) và *code/schema* (chặn tới khi G6 + kế hoạch Prisma Tuan3 xong).

---

## 0. Tóm tắt điều hành

1. **Không có bộ dữ liệu nào "chuẩn nhất" theo nghĩa đủ cả 4 điều kiện cùng lúc:** (a) câu trắc nghiệm 4 đáp án Vocabulary/Grammar, (b) nhãn CEFR cấp *câu hỏi*, (c) độ khó IRT đã hiệu chỉnh (logit), (d) giấy phép cho phép phân phối lại cho sinh viên làm bài. Tôi tìm được tài nguyên đáp ứng từng điều kiện *riêng lẻ*, không có tài nguyên nào đáp ứng cả bốn (Mục 2–3). Tôi **không** tìm thấy bộ MCQ có nhãn CEFR cấp câu hỏi và giấy phép mở; nếu bạn biết một bộ cụ thể, đưa tôi tên/đường dẫn để kiểm chứng.
2. **Khuyến nghị: phương án lai "Khung CEFR-J + nội dung AI sinh có GV duyệt + độ khó neo CEFR"** (Mục 4, phương án B):
   - **CEFR-J Vocabulary/Grammar Profile** làm *khung phân loại* (nhãn CEFR + `topic_tag`) — **Vocabulary Profile và Grammar Profile bản 20180315** cho phép dùng cả nghiên cứu lẫn thương mại kèm trích dẫn (README GitHub); **trang chính thức ghi Grammar Profile bản 2025 cần xin phép khi dùng thương mại** (xem `PHAN_TICH_CEFR_J_…` G1);
   - **Gemini sinh câu hỏi** dựa trên các mục của khung đó (đúng Giai đoạn 0 SRS 6.1 và hướng Quyết định #8/#9), **GV duyệt** từng câu;
   - **`irt_b` ban đầu = neo theo CEFR + dàn đều trong cấp** (đúng cơ chế fallback đã có trong SRS 6.1), `calibrated = false`, tinh chỉnh bằng dữ liệu thật khi có (F-12, hướng KL).
3. **Đánh đổi chính:** `irt_b` là *thang thứ tự theo CEFR*, không phải độ khó thực đo ⇒ θ̂ và CEFR kết quả tin cậy ở mức "xếp thứ tự", chưa phải "đo chuẩn". **Bù lại bằng 4 biện pháp** (Mục 4.3): GV chấm độc lập độ khó + đo độ đồng thuận, mô phỏng Monte Carlo cho engine, dàn `irt_b` theo cấp con để tránh hòa hạng, đánh dấu rõ `calibrated=false` + báo cáo hạn chế.
4. **Phân loại các bộ còn lại:** CLOTH (99.433 câu cloze do giáo viên soạn) là ứng viên *nội dung* tốt nhất về chất lượng sư phạm nhưng **giấy phép chưa nêu rõ** ⇒ chỉ dùng nội bộ làm ví dụ few-shot tới khi có xác nhận; RACE/CEFR-SP/EFCAMDAT bị ràng buộc **phi thương mại** hoặc không phải MCQ; English Vocabulary Profile (Cambridge) **cấm dùng thương mại** nếu không có thỏa thuận ⇒ không nhập (Mục 3.1).
5. **Ảnh hưởng tới tính năng cốt lõi: KHÔNG** thay đổi thuật toán CAT hay phạm vi TL (Mục 5). Có **3 điểm chạm dữ liệu** cần bạn duyệt (D3, D4, D5): marker độ khó fallback (chính là Q2 của kế hoạch Prisma), bảng/nhãn nguồn gốc cho ngân hàng tham chiếu, và giá trị enum nguồn câu hỏi.
6. **Cập nhật 2026-10-01 (phiên 2):** đã tải và đếm trực tiếp CEFR-J (từ vựng 7.799 mục, **không có cấp con**; ngữ pháp 500 dòng, chỉ **170 dòng có nhãn**, có cấp con A1.1–B2.2); người dùng chọn P3; phạm vi A2–B1 được chi tiết hóa thành phase **PL** (Mục 7). Các nhận định cũ về giấy phép Grammar Profile và về cấp con ở Mục 2, DS1, M1 đã được sửa.
7. **Q1 đã được trả lời (2026-10-01): Tiểu luận thuần học thuật, không thương mại.** Hệ quả: các nguồn giấy phép phi thương mại (CEFR-SP, EFCAMDAT, RACE…) và Grammar Profile CEFR-J bản 2025 *được phép dùng cho nghiên cứu/giáo dục*; tuy vậy nguồn phi thương mại vẫn không được đưa nội dung vào Item Bank phân phối cho sinh viên nếu điều khoản chặn. **Nếu sau này chạy thương mại thì phải rà lại.** (Mục dưới đây giữ nguyên bản gốc để đối chiếu.)
8. *(Bản gốc)* **Cần bạn trả lời sớm 1 câu quyết định mọi thứ:** hệ thống TL có thuần học thuật phi thương mại, hay sẽ chạy trong hệ sinh thái EduZ (có thể thương mại)? (Q1, Mục 10). Câu trả lời quyết định có được dùng các bộ giấy phép NC hay không.

---

## 1. Bài toán cần dữ liệu gì (rút từ SRS + Class Diagram)

| Mã | Yêu cầu dữ liệu | Nguồn trong tài liệu | Bắt buộc? |
|---|---|---|---|
| R-D1 | ~250 câu (mục tiêu bảng 6.3: 280, sinh dư) trắc nghiệm **4 đáp án A–D, 1 đáp án đúng**, kỹ năng **Vocabulary + Grammar** | SRS 6.2, 6.3; Class Diagram `Item.options/correctAnswer/skill` | Có |
| R-D2 | Phân bổ theo cấp: A1 70 · A2 80 · B1 80 · B2 50 | SRS 6.3 | Có |
| R-D3 | Nhãn `cefr_target` ∈ {A1,A2,B1,B2} (diagram có đủ 6 giá trị, TL chỉ phủ A1–B2) | SRS 6.2, 4.6 | Có |
| R-D4 | `irt_b` (logit) trong dải **[−2.5, +1.5]**; mỗi cấp có khoảng logit: A1 [−2,−1), A2 [−1,0), B1 [0,1), B2 [1,2) | SRS 4.6, 4.7 | Có |
| R-D5 | `topic_tag` (VD `past_simple`, `academic_vocab`) | SRS 6.2 | Nên có (F-10 auto-tag là P2) |
| R-D6 | Giấy phép cho phép **hiển thị nguyên văn cho sinh viên làm bài** | Quyết định #9 (người dùng đã chấp nhận rủi ro bản quyền, yêu cầu phải xác nhận điều khoản) | Có — ràng buộc pháp lý |
| R-D7 | Mật độ item đủ ở vùng θ≈0 (A2–B1) để Top-5 b-matching có ≥5 ứng viên/kỹ năng | SRS 4.4 (mục exposure: vùng A2–B1 ~35 câu) | Có |
| R-D8 | Truy vết nguồn gốc từng câu (nguồn, giấy phép, mẫu nào đã dùng) | Tuan2 `Phuong_an_sua_doi_AI.md` Mục 4 #3; TC2.3 | Nên có |
| R-D9 | Mọi câu qua GV duyệt (`status=APPROVED`) trước khi vào CAT | SRS 6.2, CLAUDE.md (filter ở Repository) | Có |
| R-D10 | Dữ liệu *phản hồi* (response matrix) để kiểm thử engine/hiệu chỉnh — **không bắt buộc** ở TL (Quyết định #1) | SRS 6.4 | Không (bù bằng mô phỏng) |

---

## 2. Kết quả tìm kiếm và mức độ kiểm chứng (bằng chứng, không suy đoán)

Ký hiệu: ✅ đã đọc trang nguồn/kết quả tìm kiếm nêu rõ · ⚠️ chỉ thấy thông tin gián tiếp, **cần xác minh trực tiếp** ở task S* · ❌ không xác minh được.

| Nguồn | Điều đã xác lập | Mức | Liên kết |
|---|---|---|---|
| CEFR-J Vocabulary Profile v1.5 + Grammar Profile (v20180315) | **Đã tải và đếm (2026-10-01):** từ vựng 7.799 mục (A1 1.164, A2 1.411, B1 2.446, B2 2.778), **không có cấp con**; ngữ pháp 500 dòng, **170 có nhãn** (A1.1–B2.2), 330 trống. Giấy phép theo README GitHub: nghiên cứu và thương mại, không phí, kèm trích dẫn; bản quyền Tono Laboratory, TUFS. **Trang chính thức:** Wordlist v1.6 cho thương mại kèm trích dẫn; **Grammar Profile bản 2025: thương mại cần liên hệ, có thể mất phí**. Không bảo đảm chính xác | ✅ giấy phép (hai nguồn không thống nhất cho ngữ pháp) · ✅ số đếm | https://github.com/openlanguageprofiles/olp-en-cefrj · http://www.cefr-j.org/download.html |
| Octanove Vocabulary Profile C1/C2 | CC BY-SA 4.0; chỉ cấp C1/C2 ⇒ **ngoài dải A1–B2 của bank** | ✅ | cùng repo trên |
| CLOTH | 7.131 đoạn, 99.433 câu cloze, do giáo viên Trung Quốc soạn cho thi cấp 2/cấp 3 (CLOTH-M, CLOTH-H). Bài báo **không nêu giấy phép**; tải tại trang CMU. Không có nhãn CEFR, không có `irt_b` | ✅ quy mô · ⚠️ giấy phép (trang CMU không tải được khi kiểm tra) | https://arxiv.org/abs/1711.03225 · http://www.cs.cmu.edu/~glai1/data/cloth/ |
| RACE | Đọc hiểu (không phải Vocab/Grammar). Tác giả không đặt giấy phép nhưng **chỉ cho nghiên cứu phi thương mại** | ✅ (nguồn thứ cấp) | https://arxiv.org/abs/1704.04683 |
| CEFR-SP (`UniversalCEFR/cefr_sp_en`) | 10.004 **câu** nhãn A1–C2; **CC BY-NC-SA 4.0**; không phải MCQ | ✅ | https://huggingface.co/datasets/UniversalCEFR/cefr_sp_en |
| EFCAMDAT | Bài viết người học, 16 cấp gắn CEFR; thỏa thuận chỉ cho **học thuật/nghiên cứu phi thương mại**, phải đăng ký | ✅ | https://ef-lab.mmll.cam.ac.uk/EFCAMDAT.html · https://ef-lab.mmll.cam.ac.uk/assets/pdf/EFCamDat-User-Agreement-2023.pdf |
| English Vocabulary Profile (Cambridge) | Điều khoản **cấm dùng thương mại** nếu chưa ký Application Development Agreement; cấm bán/cho thuê/cấp phép lại nội dung | ✅ (qua kết quả tìm kiếm điều khoản) | https://dictionary-api.cambridge.org/api/terms-and-conditions |
| Oxford 3000/5000 (có nhãn CEFR) | Danh sách do OUP biên soạn, có bản quyền; **không tìm thấy điều khoản cho phép phân phối lại** | ⚠️ | https://www.oxfordlearnersdictionaries.com/about/wordlists/ |
| NGSL (New General Service List) | Danh sách tần suất từ, CC BY-SA 4.0 (các bản Graded Reader/Spoken ghi rõ; bản chính ghi "Share-alike CC"); **không có nhãn CEFR cấp từ** | ✅ | https://www.newgeneralservicelist.com/ |
| Kaggle "TOEFL CEFR Vocabulary" | 14.848 từ/cụm từ gắn A1–C2, ghi CC BY 4.0. **Nguồn gốc dữ liệu chưa xác minh** (không đọc được mô tả trang) ⇒ rủi ro sao chép từ danh sách có bản quyền | ⚠️ | https://www.kaggle.com/datasets/panteamohamadkhani/toefl-cefr-vocabulary |
| Item Response Warehouse (IRW) | >900 bộ dữ liệu phản hồi trắc nghiệm công khai; hạ tầng IRW CC BY 4.0 nhưng **mỗi bộ giữ giấy phép gốc**; chưa kiểm được có bộ tiếng Anh nào dùng được | ✅ giấy phép khung · ⚠️ nội dung | https://itemresponsewarehouse.org · https://pmc.ncbi.nlm.nih.gov/articles/PMC12413415/ |
| ECPE (gói `dcmdata`, R) | 28 câu nhị phân đo 3 kỹ năng (hình thái-cú pháp, liên kết, từ vựng) của kỳ thi tiếng Anh ECPE — **chỉ là ma trận phản hồi**, không có nội dung câu hỏi | ⚠️ (kết quả tìm kiếm) | https://cran.r-project.org/web/packages/dcmdata/refman/dcmdata.html |
| Duolingo SLAM 2018 | Dữ liệu lỗi người học (token-level), **giấy phép chưa xác minh**; không phải MCQ | ❌ giấy phép | https://sharedtask.duolingo.com/2018.html |

**Tìm kiếm không cho kết quả:** không thấy bộ MCQ Vocabulary/Grammar tiếng Anh có nhãn CEFR *cấp câu hỏi* và giấy phép mở (tìm bằng 2 truy vấn mở rộng trên Hugging Face/Kaggle/web). Đây là *kết luận từ tìm kiếm của phiên này*, không phải bằng chứng rằng bộ như vậy không tồn tại.

---

## 3. Bảng nhận xét chi tiết

Mức độ: 🔴 chặn (phải xử lý trước khi dùng) · 🟡 có phương án bù · 🟢 phù hợp.

### 3.1. Nhận xét từng bộ dữ liệu

| # | Bộ dữ liệu | Có gì (so với R-D*) | Thiếu gì | Mức | Giải pháp bù | Vì sao giải pháp đó | Ảnh hưởng hệ thống |
|---|---|---|---|---|---|---|---|
| DS1 | **CEFR-J Vocab + Grammar Profile** | Nhãn CEFR cấp từ/cấu trúc ngữ pháp (R-D3, R-D5); giấy phép thương mại OK cho từ vựng và ngữ pháp bản 2018 (R-D6 cho *khung*); **ngữ pháp bản 2025 cần xin phép** | Không có câu hỏi, không có đáp án, không có `irt_b` thực đo; từ vựng không có cấp con; 66% dòng ngữ pháp thiếu nhãn | 🟢 làm khung (🟡 với ngữ pháp bản 2025) | Dùng làm **khung phân loại**: mỗi mục ngữ pháp → 1 `topic_tag` + `cefr_target`; mỗi từ → mục tiêu của câu từ vựng | Giấy phép sạch nhất trong các nguồn tìm được; nhãn do nhóm chuyên gia, giải trình được trước hội đồng | Cần `reference` truy vết nguồn (D4) |
| DS2 | **CLOTH** | Chất lượng sư phạm cao: câu cloze 4 lựa chọn do giáo viên soạn, đáp án gây nhiễu tinh tế (R-D1 gần đúng); 99k câu | Không nhãn CEFR; ngữ cảnh thi Trung Quốc; **giấy phép chưa rõ**; không `irt_b`; một phần là đọc-điền từ theo đoạn, không phải câu độc lập | 🔴 cho phân phối · 🟡 cho nội bộ | (1) Xin xác nhận bằng văn bản từ tác giả (S3); (2) tới khi có xác nhận: chỉ làm **ví dụ few-shot nội bộ**, không hiển thị cho SV, không nhập thẳng vào `items`; (3) CLOTH-M/H là tín hiệu độ khó thô (cấp 2 < cấp 3) | Quyết định #9 cho phép "duyệt thẳng", nhưng chỉ an toàn khi giấy phép xác nhận; không thể "chấp nhận rủi ro" thay chủ sở hữu | Cờ `license_status` chặn duyệt thẳng (D4) |
| DS3 | **RACE** | Quy mô lớn, MCQ | Đọc hiểu, không đúng kỹ năng; phi thương mại | 🔴 | **Loại** khỏi dự án | Sai kỹ năng + hạn chế giấy phép | Không |
| DS4 | **CEFR-SP** | Nhãn CEFR A1–C2 cấp câu; hữu ích để *kiểm tra* độ khó câu dẫn | Không MCQ; CC BY-NC-SA | 🟡 | Chỉ dùng **nội bộ nghiên cứu** (kiểm tra độ khó văn bản câu hỏi AI sinh) nếu Q1 = phi thương mại; **không đưa nội dung vào Item Bank** | SA/NC truyền sang sản phẩm phái sinh, làm phức tạp giấy phép của cả bank | Không (chỉ công cụ kiểm tra) |
| DS5 | **EFCAMDAT** | Lỗi thực của người học theo cấp → nguồn cho `ErrorPattern`, nhiễu đáp án | Không MCQ; đăng ký + phi thương mại | 🟡 | Tùy chọn: rút **mẫu lỗi thường gặp** (không sao chép văn bản) để thiết kế đáp án nhiễu | Giá trị thực nhưng không cần thiết cho TL; chi phí đăng ký + thỏa thuận | Không |
| DS6 | **English Vocabulary Profile** | Danh sách CEFR cấp từ chất lượng cao | Cấm thương mại; cấm cấp phép lại | 🔴 | **Không nhập.** Chỉ cho GV *tra cứu thủ công* khi duyệt, không sao chép hàng loạt | Rủi ro pháp lý không đáng so với DS1 | Không |
| DS7 | **Oxford 3000/5000** | Nhãn CEFR cấp từ | Bản quyền OUP, không thấy điều khoản phân phối | 🔴 | Như DS6 | Như DS6 | Không |
| DS8 | **NGSL** | Tần suất từ (CC BY-SA) → xếp thứ tự độ phổ biến | Không có CEFR; SA | 🟡 | Dùng làm **tín hiệu phụ** để dàn `irt_b` trong cấp (từ hiếm hơn ⇒ khó hơn) *nếu* chấp nhận SA | Tín hiệu có cơ sở ngôn ngữ học, rẻ | Cần chốt D7 |
| DS9 | **Kaggle TOEFL-CEFR vocab** | Nhãn A1–C2, CC BY 4.0 | Nguồn gốc không rõ ⇒ có thể lấy từ danh sách có bản quyền | 🔴 | **Mặc định không dùng**; chỉ xem lại nếu S5 xác minh được nguồn gốc sạch | "CC BY" do người đăng gán không chứng minh họ có quyền | Không |
| DS10 | **IRW / ECPE** | Ma trận phản hồi thật, để thử engine (R-D10) | Không có nội dung câu hỏi; chưa xác minh bộ tiếng Anh dùng được; số câu nhỏ (28) | 🟡 | Dùng làm **dữ liệu kiểm thử độc lập** cho `computeEAP` và đối chiếu py-irt (không phải nguồn item) | Cho oracle thật ngoài mô phỏng tự sinh; hỗ trợ TC2.5/TC2.3 | Chỉ test |
| DS11 | **AI sinh (Gemini) có khung DS1 + GV duyệt** | Đúng R-D1, R-D2, R-D5, R-D6 (nội dung do nhóm tạo, bản quyền rõ), R-D8, R-D9 | `irt_b` không thực đo; nguy cơ đáp án mơ hồ/lỗi AI | 🟡 | Self-consistency check + GV duyệt (đã thiết kế ở `Phuong_an_sua_doi_AI.md` 1.3b); `irt_b` = neo CEFR | Đã nằm trong SRS 6.1 Giai đoạn 0–1 ⇒ không phát sinh việc ngoài phạm vi | Nhóm D3–D5 |

### 3.2. Đối chiếu lược đồ: trường của `Item` ↔ từng nguồn

✅ có sẵn · ◐ có một phần/phải suy ra · ✖ không có.

| Trường `Item` (SRS 6.2 / diagram) | DS1 CEFR-J | DS2 CLOTH | DS4 CEFR-SP | DS11 AI + GV | Ghi chú |
|---|---|---|---|---|---|
| `content` | ✖ | ✅ | ◐ (câu, không có chỗ trống) | ✅ | |
| `options` (A–D) | ✖ | ✅ | ✖ | ✅ | |
| `correct_answer` | ✖ | ✅ | ✖ | ✅ (GV xác nhận) | |
| `skill` | ◐ (từ vựng/ngữ pháp) | ◐ (cloze trộn cả hai) | ✖ | ✅ | |
| `topic_tag` | ✅ (Grammar Profile) | ✖ | ✖ | ✅ (từ DS1) | |
| `cefr_target` | ✅ | ✖ (chỉ M/H) | ✅ (cấp câu) | ✅ (từ DS1) | |
| `irt_b` | ✖ | ✖ | ✖ | ◐ neo theo CEFR | Không nguồn nào có |
| `irt_a`, `irt_c` | ✖ | ✖ | ✖ | mặc định | Rasch: a=1, c dự phòng KL |
| `status`, `approved_by/at` | ✖ | ✖ | ✖ | ✅ (quy trình GV) | Tạo trong hệ thống |
| `source` (`MANUAL`/`AI_GENERATED`) | — | cần giá trị mới? | — | `AI_GENERATED` | Xem D5 |
| Truy vết nguồn + giấy phép | ✅ cần lưu | ✅ cần lưu | — | ✅ cần lưu | Xem D4 |

**Kết luận từ bảng:** `irt_b` là cột *không bộ nào cung cấp* ⇒ đây là thiếu hụt cốt lõi; mọi phương án phải trả lời "`irt_b` lấy từ đâu và độ tin cậy ra sao" (Mục 4).

---

## 4. Đánh giá phương án và khuyến nghị

### 4.1. Ba phương án

| | **A. Nhập thẳng một bộ MCQ có sẵn** (CLOTH…) | **B. Lai: khung CEFR-J + AI sinh + GV duyệt + neo CEFR** *(khuyến nghị)* | **C. Tự thu thập dữ liệu thật rồi hiệu chỉnh** |
|---|---|---|---|
| Nội dung | Có sẵn, chất lượng sư phạm cao | Tự tạo ~280 câu, GV duyệt | Như B |
| Giấy phép (R-D6) | 🔴 chưa rõ/NC | 🟢 nội dung do nhóm tạo; khung CEFR-J cho phép thương mại | 🟢 |
| Nhãn CEFR | ✖ phải gán lại | ✅ từ khung | ✅ |
| `irt_b` | ✖ | ◐ neo CEFR | ✅ thực đo |
| Khối lượng | Thấp (nhưng phải gán nhãn lại + xin phép) | Trung bình (đã nằm trong SRS 6.1: Gemini + GV, Tuần 1–4) | **Rất cao** — chính là Pre-test ≥60 SV đã bị loại ở Quyết định #1 |
| Hợp phạm vi/quyết định cũ | Lệch: không khớp Giai đoạn 0–1 SRS | Khớp SRS 6.1 + Quyết định #1, #8, #9 | **Đi ngược Quyết định #1** |
| Rủi ro lớn nhất | Pháp lý + đề thi Trung Quốc lệch ngữ cảnh | `irt_b` kém tin cậy; chất lượng AI | Quá khối lượng |
| Hợp khuyến nghị | ❌ (giữ như nguồn few-shot nội bộ) | ✅ | ❌ (để dành KL) |

**Khuyến nghị: B**, có **CLOTH là phụ trợ nội bộ** (ví dụ few-shot) chỉ khi S3 cho phép, và **không phụ thuộc vào CLOTH** để hệ thống chạy.

### 4.2. Đánh đổi của phương án B (nói thẳng)

| Đánh đổi | Hệ quả cụ thể |
|---|---|
| `irt_b` không thực đo, chỉ neo theo CEFR | Mọi câu cùng cấp con có cùng `irt_b` ⇒ Top-5 b-matching hòa hạng, thứ tự trong cấp là tùy ý; θ̂ chỉ tin ở mức xếp thứ tự thô; SE theo công thức Rasch có thể *quá lạc quan* so với độ bất định thật của `b` |
| Chất lượng câu phụ thuộc AI + GV | GV là nút thắt (250–300 câu); đáp án mơ hồ lọt qua làm sai lệch θ̂ |
| Đo CEFR của chính hệ thống dựa trên CEFR của câu hỏi (vòng tròn) | CEFR kết quả không độc lập với nhãn CEFR đã gán cho câu hỏi ⇒ không thể dùng để "chứng minh độ chính xác" |
| Không có thang so sánh với bài thi chuẩn | Không báo cáo được "tương quan với IELTS/…" |

### 4.3. Bù đắp (biện pháp → tiêu chí được bảo vệ)

| # | Biện pháp | Bù cho đánh đổi nào | Bằng chứng tạo ra | Task |
|---|---|---|---|---|
| M1 | **Dàn `irt_b` trong cấp** theo cấp con CEFR-J (**đã xác minh: chỉ ngữ pháp có cấp con; từ vựng không có**) + tín hiệu phụ cho từ vựng (độ dài/tần suất NGSL nếu D7 duyệt); luôn trong [−2.5,+1.5] | Hòa hạng Top-5 | Bảng quy đổi sub-level → `irt_b` có công thức, tái lập được | P3.5 |
| M2 | **2 GV chấm độc lập** thứ tự độ khó cho mẫu (≥60 câu); báo cáo mức đồng thuận (hệ số kappa có trọng số) giữa nhãn khung và GV | Không có thực đo; vòng tròn CEFR | Bảng đồng thuận — số liệu *thật*, không điền khi chưa đo | P4.2 |
| M3 | **Mô phỏng Monte Carlo** engine với `b` neo + nhiễu `b` (độ lệch chuẩn đặt theo kịch bản 0.3/0.5/0.8): đo SE, số câu, sai số xếp CEFR | `b` kém tin cậy | Báo cáo độ nhạy (cũng thay số "ước lượng sơ bộ" ở SRS 4.4 bằng số mô phỏng) | P4.3 |
| M4 | **Cờ `calibrated=false`** + mục "Hạn chế" trong báo cáo; GV review kỹ item fallback (đúng SRS 6.1 NOTE) | Kỳ vọng sai về độ chính xác | Trường dữ liệu + đoạn báo cáo | P2.x, P5.3 |
| M5 | **Dữ liệu ECPE/IRW** làm oracle ngoài cho `computeEAP` (nếu S6 xác minh dùng được) | Test chỉ dựa dữ liệu tự sinh | Test so khớp với py-irt/catR | P4.4 |
| M6 | **Đường nâng cấp:** `session_responses` lưu đủ để chạy MMLE (F-12) sau này | `irt_b` neo vĩnh viễn | Không cần làm ngay | — |

---

## 5. Thay đổi này có ảnh hưởng tính năng cốt lõi không?

**Không.** Lý do theo từng thành phần:

| Thành phần | Có đổi? | Lý do |
|---|---|---|
| `pickNextSkill`, `selectNextItem`, `computeEAP`, `checkStoppingCriterion` | Không | Chỉ nhận `irt_b` từ `items`; nguồn của giá trị không thuộc engine. Lọc `APPROVED` vẫn ở Repository |
| Tham số θ₀=−0.5, SE 0.35, 25 câu, 8 câu, biên [−2.5,+1.5] | Không | Cấu hình, không phụ thuộc nguồn dữ liệu. **Lưu ý:** biên b_min/b_max là *giả định về dải của bank*; sau khi neo CEFR phải kiểm tra bank thực tế có phủ dải này (P3.6) |
| Phạm vi TL | Không | Không thêm F-ID; Quyết định #1 giữ nguyên (không Pre-test). Việc import ngân hàng tham chiếu vẫn là mở rộng nhỏ đã duyệt (#8/#9), chưa triển khai |
| Dữ liệu (`items` + bảng nguồn) | **Có — thêm cột/bảng** | Xem D3–D5. Là thay đổi *cộng thêm*, nhẹ |
| Tài liệu (SRS 6.1/6.2/6.4, diagram, đặc tả UC "Import Reference Item Bank") | Có — cần đồng bộ | Mục 7, phase P2 |
| Rủi ro mới | Có | Xem Mục 9 |

**Ảnh hưởng tới rubric:** (a) **TC1** — Quyết định #14 đã thay khảo sát SV/GV bằng tìm nguồn đề; việc khảo sát bộ dữ liệu *không tự động* thay thế khảo sát bên liên quan. Bước M2 (2 GV chấm độc lập) tạo ra dữ liệu từ bên liên quan thật — **nhóm cần hỏi GVHD** xem có tính là bằng chứng TC1 không; tôi không có thẩm quyền xác nhận. (b) **TC2.3** — mỗi câu AI sinh phải có dòng trong `AI_USAGE_LOG.md` (ghi theo lô, kèm prompt gốc và tỷ lệ GV sửa/loại). (c) **TC2.1** — mọi thay đổi thiết kế ghi vào `DECISIONS_LOG.md`/weekly-log.

---

## 6. Quyết định — **cần bạn duyệt khi duyệt kế hoạch**

Các mục dưới đây SRS/diagram chưa quy định (CLAUDE.md quy tắc 1). Cột "Mặc định" là đề xuất của tôi — **chưa phải quyết định đã chốt**. Duyệt kế hoạch = duyệt cột "Mặc định". Muốn đổi, ghi số mục + phương án; Agent sẽ cập nhật kế hoạch trước khi thi công.

> **Cập nhật 2026-10-01:** nhóm đã chốt các mặc định còn lại — D2 (CEFR-J, Grammar Profile bản 20180315), D4 (bảng `reference_items` + `license_status` + `generated_from_ref_ids`), D5 (giữ `MANUAL`, `AI_GENERATED`), D7 (không dùng NGSL), D8 (`apps/backend/prisma/seed/`), D9 (tham số ở cấu hình). D1, D3, D6 đã chốt trước đó. **D7 = không dùng NGSL nghĩa là từ vựng không có cách dàn `irt_b` trong cấp: các câu từ vựng cùng cấp hòa hạng** (đã chấp nhận, ghi vào "Hạn chế dữ liệu").

| # | Điểm | **Mặc định** | Phương án thay thế | Đánh đổi | Nếu đổi sau khi đã có dữ liệu |
|---|---|---|---|---|---|
| D1 | Chiến lược nguồn dữ liệu | ✅ **Đã chọn: P3 (lai)** — khung CEFR-J + sinh câu theo nhãn trước + GV gán nhãn độc lập; đề thi (CLOTH/VNHSGE) chỉ học mẫu và kiểm tra phương pháp. Chi tiết: `PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md` | A hoặc C (phương án P1/P2 trong file P3) | Xem 4.1 và file P3 | Đổi sang A/C: tốn nhiều |
| D2 | Khung nhãn | **CEFR-J Vocabulary + Grammar Profile bản 20180315**, trích dẫn đúng theo yêu cầu giấy phép (bản 2025 chỉ dùng sau khi xin phép nếu Q1 là thương mại) | EVP/Oxford (bị cấm/không rõ) | DS1 là nguồn duy nhất trong danh sách có giấy phép thương mại rõ và nội dung tải được | Nhẹ (chỉ là nhãn) |
| D3 | Marker "độ khó neo CEFR" (Q2 của kế hoạch Prisma) | ✅ **Đã chọn (2026-10-01): giữ cột `calibrated BOOLEAN DEFAULT FALSE`** trên `items` (đúng SRS 6.2; cũng là A3 của kế hoạch Prisma) | (b) enum `b_source` {CEFR_ANCHOR, SOURCE_CALIBRATED, EMPIRICAL}; (c) không có marker | Boolean đủ cho TL (mọi `b` đều là neo); enum phân biệt được 3 trạng thái nhưng thêm độ phức tạp chưa cần. Diagram đã bỏ `calibrated` ở buổi họp GVHD 18/09 ⇒ đây là *khôi phục một cột đã bị bỏ khỏi diagram*, cần giải thích | Thêm cột: nhẹ; đổi boolean → enum: trung bình |
| D4 | Truy vết nguồn gốc + giấy phép | **Bảng `reference_items`** (đúng thiết kế `ReferenceItemBank` của `Phuong_an_sua_doi_AI.md` Mục 4 #1) gồm `source_provider`, `license_status` ∈ {VERIFIED_OPEN, UNVERIFIED, NON_COMMERCIAL_ONLY}; **chặn duyệt thẳng** mục không phải `VERIFIED_OPEN`; `items.generated_from_ref_ids` (mảng id) | Chỉ ghi nguồn trong file/tài liệu, không có bảng | Bảng cho phép chặn bằng ràng buộc và trả lời hội đồng "câu này từ đâu"; đổi lại thêm 1 bảng ⇒ cần sửa kế hoạch Prisma (hiện 9 bảng) và Class Diagram | Thêm bảng sau: trung bình |
| D5 | Enum `ItemSource` (hiện `MANUAL`, `AI_GENERATED`) | **Giữ 2 giá trị**; câu AI sinh + GV sửa = `AI_GENERATED` (truy vết chi tiết bằng D4). Đây cũng chính là câu hỏi mở của `Phuong_an_sua_doi_AI.md` Mục 2 | Thêm `REFERENCE_IMPORT`/`AI_EDITED` | Giữ 2 giá trị = không đổi diagram; thêm giá trị = rõ hơn nhưng phải sửa diagram + SRS. Thêm giá trị enum Postgres dễ, **xóa rất khó** | Thêm: nhẹ; xóa: khó |
| D6 | Dùng CLOTH | **Chỉ dùng nội bộ, `license_status=UNVERIFIED`, không hiển thị cho SV, được phép gửi mẫu nhỏ tới API bên ngoài theo DL3 (kèm rào chắn; giấy phép vẫn chưa xác minh)** (xem DL3 trong file P3); vai trò: kiểm tra phương pháp gán nhãn (A2–B1) và nguồn mẫu cho mô tả chiến lược ra nhiễu | (b) Bỏ hẳn; (c) Duyệt thẳng như Quyết định #9 | (c) là hướng bạn từng chọn nhưng chỉ an toàn sau khi có xác nhận giấy phép; (b) mất nguồn mẫu chất lượng cao | Nhẹ |
| D7 | NGSL làm tín hiệu phụ cho `irt_b` trong cấp | **Không dùng** (giữ đơn giản; dàn theo cấp con CEFR-J trước) | Dùng, chấp nhận CC BY-SA | SA chỉ áp lên *danh sách/dẫn xuất của nó*, không rõ có áp lên toàn bank; tránh khi chưa cần | Nhẹ |
| D8 | Vị trí code/script nạp dữ liệu | **`apps/backend/prisma/seed/`** (cạnh `seed.ts` của kế hoạch Prisma P4.D1); script sinh câu hỏi ngoài request path | Thư mục `tools/` ở gốc monorepo | Cấu trúc Tuan2 chưa quy định thư mục `tools/` ⇒ không tự tạo | Nhẹ |
| D9 | Mô hình/tham số sinh câu (k mẫu, N/lần, ngưỡng trùng lặp) | **Cấu hình qua `ConfigService`/file cấu hình, không hardcode**; giá trị khởi đầu k=3, N≤10 *là đề xuất để thử, chưa chốt* | Chốt cứng | Các số này vẫn mở ở `Phuong_an_sua_doi_AI.md` Mục 2 | Nhẹ |

---

## 7. Kế hoạch triển khai

Ký hiệu: 🤖 Agent · 👤 Người · ⛔ Cổng chặn · `∥` song song được · "Xác minh" = bước bắt buộc trước khi đánh ✅.
Mỗi task ghi: **Vào** (đọc gì) → **Làm** → **Ra** (file/ bằng chứng) → **Xác minh**. Đường dẫn tương đối `D:\TLCN`.

### Sơ đồ phụ thuộc

```
P0 (cổng: duyệt + Q1) ──► P1 (xác minh nguồn)  ∥ ── S1 S2 S3 S4 S5 S6   (6 nhánh độc lập)
                              │
                              ▼
                       P2 (đồng bộ tài liệu + mô hình dữ liệu)   [P2.x code chờ G6 + Prisma Tuan3]
                              │
                              ▼
                       P3 (pipeline nội dung)  ── P3.1→P3.2→P3.3→P3.4→P3.5→P3.6 (tuần tự)
                              │
                              ▼
        P4 (bù đắp)  ∥ ── P4.1 GV chấm   P4.3 mô phỏng   P4.4 oracle ECPE      (3 nhánh)
                              │
                              ▼
                       P5 (khép sổ & minh chứng)
```

> **Phase PL (A2–B1):** chạy sau P1/P2, thay thế P3.1–P3.5 cho 160 câu A2–B1 và dùng chung công cụ (prompt, bộ lọc, gán `irt_b`) với P3 cho phần còn lại (A1/B2, chờ DL5). Sơ đồ phụ thuộc riêng của PL nằm ở `PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md` Mục 5.

### P0 — Cổng vào (tuần tự)

| ID | Việc | Loại | Vào → Ra / Xác minh |
|---|---|---|---|
| P0.1 | Người dùng duyệt kế hoạch + Mục 6 (D1–D9) | 👤 ⛔ | Ghi nguyên văn lời duyệt vào tracking |
| P0.2 | Người dùng trả lời Q1 (phi thương mại hay EduZ thương mại) | 👤 ⛔ | Ghi vào `DECISIONS_LOG.md` (#19) — quyết định mọi quyền dùng DS4/DS5/DS8 |
| P0.3 | Đọc theo thứ tự Mục 8.2 | 🤖 | Ghi "đã đọc" + file nào chỉ tra từ khóa |
| P0.4 | Tạo `0.docs/tracking/feature-plans/item-bank-data-source.md` từ `_template.md` (CLAUDE.md quy tắc 3) | 🤖 | File tồn tại, trỏ về kế hoạch này |

### P1 — Xác minh nguồn (`∥` toàn bộ nhánh S1–S6 sau P0)

| ID | Việc | Loại | Vào → Làm → Ra | Xác minh |
|---|---|---|---|---|
| S1 | **CEFR-J**: tải Vocabulary + Grammar Profile từ trang chính thức | 🤖 (tải về `_work/` tạm trong thư mục job, chưa đưa vào repo) | Vào: http://www.cefr-j.org/download.html, https://github.com/openlanguageprofiles/olp-en-cefrj → Làm: ghi **phiên bản, ngày tải, SHA-256, tên cột, số dòng theo cấp, có sub-level hay không**; chép nguyên văn yêu cầu trích dẫn → Ra: mục "Nguồn S1" trong tracking | Số dòng/cấp là số *đếm thật*; có đủ dải A1–B2; **nếu không có sub-level thì ghi rõ và M1 chuyển sang chỉ dàn bằng cách khác — dừng hỏi** |
| S1′ | *(đã làm một phần, phiên 2026-10-01)* Tải và đếm hai file CSV (v1.5 từ vựng, 20180315 ngữ pháp) từ kho OLP; SHA-256, số đếm, sub-level đã ghi ở `PHAN_TICH_CEFR_J_…` Mục 2 | 🤖 | **Còn lại:** tải Grammar Profile **2025** (ZIP Excel/PDF) để so với bản 2018; ghi câu trích dẫn đúng yêu cầu; xin xác nhận giấy phép nếu Q1 thương mại | Không dùng bản 2025 khi chưa tải/đọc điều khoản |
| S2 | **Octanove C1/C2**: xác nhận ngoài phạm vi | 🤖 | Ra: ghi "⏭ ngoài dải A1–B2" | — |
| S3 | **CLOTH**: xác nhận giấy phép | 👤+🤖 | 🤖 mở trang CMU thủ công/qua trình duyệt, đọc điều khoản, soạn email xin xác nhận (nội dung: mục đích học thuật, có phân phối lại cho SV hay không) → 👤 gửi → Ra: kết quả trong tracking (`UNVERIFIED` cho tới khi có trả lời bằng văn bản) | Không tải dữ liệu vào repo khi chưa rõ |
| S4 | **EVP/Oxford**: ghi nhận "không nhập" + quy tắc cho GV (tra cứu thủ công, không sao chép hàng loạt, không scrape) | 🤖 | Ra: đoạn quy tắc trong feature-plan | — |
| S5 | **Kaggle TOEFL-CEFR**: xác minh nguồn gốc | 🤖 | Mở trang dataset, đọc phần mô tả/nguồn → kết luận Dùng/Không dùng; **mặc định Không dùng nếu không chỉ ra được nguồn gốc** | Trích nguyên văn dòng nguồn gốc (hoặc ghi "không có") |
| S6 | **IRW/ECPE**: xác minh có bộ tiếng Anh dùng được không, giấy phép gốc | 🤖 | Vào: https://itemresponsewarehouse.org → liệt kê bộ có "English/language/ECPE"; đọc giấy phép gốc từng bộ | Bảng bộ-giấy phép; nếu không có → ⏭ và M5 bị hủy (ghi rõ) |

### P2 — Đồng bộ tài liệu & mô hình dữ liệu

| ID | Việc | Loại | Vào → Ra | Xác minh |
|---|---|---|---|---|
| P2.1 | Ghi Quyết định #19+ (D1–D9 đã duyệt, Q1) vào `DECISIONS_LOG.md` | 🤖 | Đủ cột như các dòng #15–#18 | Đọc lại: không trống cột |
| P2.2 | Ghi "Đề xuất SRS v2.7" vào `weekly-log/Tuan-03.md`: 6.1 (nguồn thực tế = khung CEFR-J + AI + GV, không còn "tìm nguồn độ khó chuẩn" như đã mô tả), 6.2 (`calibrated`), 6.4, Risk R1/R2, F-10b | 🤖 | Không sửa `.docx` | Mục mới xuất hiện trong file |
| P2.3 | Cập nhật `Mo_ta_So_do_Lop_ClassDiagram.md`: `Item` (field `calibrated`, `generatedFromRefIds`), `ReferenceItem` (**chỉ nếu D4 duyệt**) | 🤖 | Đánh dấu rõ "bản đề xuất, diagram `.xml` chưa sửa" | grep tên field mới |
| P2.4 | **Đề xuất delta schema** cho kế hoạch Prisma: thêm `items.calibrated` (đã chọn, A3), `items.generated_from_ref_ids`, bảng `reference_items` (+ enum `ReferenceLicenseStatus`), **bảng `item_label_evidence` (DL4 — nhóm đã chọn bảng riêng, tên/cột là đề xuất)**; cần thêm vào đây: ảnh hưởng tới tổng số bảng (9 → 10 hoặc 11) | 🤖 | Viết thành mục "Delta" trong `feature-plans/item-bank-data-source.md`; **không sửa** `Tuan3/KE_HOACH_PRISMA_…md` hay `schema.prisma` (thuộc kế hoạch khác) — báo người dùng để quyết định gộp | Bảng delta khớp D3–D5 |
| P2.5 | 🔒 Áp delta vào `schema.prisma` + migration | 🤖 ⛔ | **Chỉ sau khi** G6 + P3 của kế hoạch Prisma xong + người dùng đồng ý gộp | `prisma validate` sạch; test partial index vẫn xanh |
| P2.6 | Gợi ý cập nhật Use Case "Import Reference Item Bank" (Admin) + UCGV03 theo `Phuong_an_sua_doi_AI.md` Mục 3 | 🤖 | Chỉ ghi danh sách việc; sửa `.docx/.xml` là task riêng, cần yêu cầu rõ | — |

### P3 — Pipeline nội dung (tuần tự; code chờ G6)

| ID | Việc | Loại | Vào → Làm → Ra | Xác minh |
|---|---|---|---|---|
| P3.1 | **Bảng đặc tả bank mục tiêu**: 280 hàng (kỹ năng × cấp theo SRS 6.3) gắn với mục khung CEFR-J cụ thể (từ/cấu trúc nào) | 🤖 | Vào: kết quả S1 → Ra: bảng trong feature-plan (không phải dữ liệu thô CEFR-J nếu giấy phép yêu cầu trích dẫn; ghi trích dẫn) | Tổng = 280; từng ô khớp bảng 6.3; mỗi mục khung dùng ≤ số lần quy định (đặt trong cấu hình) |
| P3.2 | **Prompt sinh câu hỏi** (few-shot, đầu ra JSON mảng N câu) + schema kiểm tra (Zod) | 🤖 | Ra: file prompt + schema trong `prisma/seed/` (**sau G6**) hoặc bản nháp trong feature-plan (trước G6) | Chạy thử 1 lô nhỏ N=3: JSON hợp lệ; ghi prompt vào `AI_USAGE_LOG.md` |
| P3.3 | **Lớp kiểm duyệt tự động** (cứng: đủ 4 đáp án/1 đáp án đúng/`irt_b` trong biên/trùng lặp; mềm: self-consistency) | 🤖 | Theo `Phuong_an_sua_doi_AI.md` 1.3b; **ngưỡng đọc từ cấu hình (D9)**, không hardcode | Test đơn vị ≥ 4 ca: thiếu đáp án, 2 đáp án đúng, trùng ≥ ngưỡng, `irt_b` ngoài biên |
| P3.4 | **Sinh theo lô + GV duyệt** (người duyệt, không Agent tự duyệt) | 🤖→👤 ⛔ | Agent sinh các lô; GV duyệt qua UCGV03/05 (hoặc bảng tạm trước khi có UI) | Mỗi lô có số liệu: sinh bao nhiêu, bị loại tự động, bị cờ, GV sửa/loại — **số đếm thật** vào tracking; `AI_USAGE_LOG.md` thêm dòng/lô |
| P3.5 | **Gán `irt_b`** theo cấp (M1): bảng quy đổi cấp con → `irt_b` (trung điểm khoảng SRS 4.6 + dàn đều trong cấp), đặt `calibrated=false` | 🤖 | Công thức + giá trị trong cấu hình; mỗi cấp nằm trong khoảng 4.6 | Test: mọi `irt_b` ∈ [−2.5,+1.5] và trong khoảng cấp; không còn hai câu cùng cấp con trùng nhau *quá ngưỡng* (đặt ngưỡng ở D9) |
| P3.6 | **Kiểm tra độ phủ bank**: số câu APPROVED theo kỹ năng × cấp; số câu trong vùng θ∈[−1,+1] ≥ 5 mỗi kỹ năng cho mọi cửa sổ Top-5 | 🤖 | Ra: bảng độ phủ + danh sách ô thiếu | **Số đếm thật**. Nếu vùng A2–B1 thưa hơn SRS 4.4 ("~35 câu") → ghi và báo người dùng (ảnh hưởng exposure) |

### P4 — Bù đắp (`∥`)

| ID | Việc | Loại | Vào → Ra | Xác minh |
|---|---|---|---|---|
| P4.1 | Soạn tài liệu hướng dẫn 2 GV chấm độc lập (mẫu ≥60 câu, xếp thứ tự/gán cấp, không thấy nhãn khung) + mẫu bảng thu kết quả | 🤖 | Ra: bảng thu trong tracking | Mẫu phân tầng theo kỹ năng × cấp |
| P4.2 | **Thu thập và tính đồng thuận** | 👤 ⛔ → 🤖 | 👤 hai GV chấm; 🤖 tính kappa có trọng số **bằng công cụ tính độc lập** (Python/R) | Số liệu ghi nguyên trạng, **không làm tròn thành "đạt"**; nếu thấp → báo, không tự sửa nhãn |
| P4.3 | **Mô phỏng Monte Carlo** (M3): θ thật ~ N(μ,1), `b` thật = `b` neo + nhiễu (kịch bản 0.3/0.5/0.8), chạy engine, đo SE cuối, số câu, % trúng cấp CEFR | 🤖 (**sau G6 + engine F-03**) | Ra: báo cáo độ nhạy | Cố định seed; chạy lại ra cùng số; ghi *tham số kịch bản là giả định*, không phải dữ liệu thật |
| P4.4 | **Oracle ECPE/IRW** (M5) nếu S6 ✅ | 🤖 (sau engine) | Đối chiếu θ̂ của `computeEAP` với py-irt/catR trên cùng ma trận | Bảng sai khác; nếu lớn → dừng hỏi |

### PL — Gán nhãn CEFR cho bộ trắc nghiệm A2–B1 (phương án P3)

Chi tiết từng task (Vào → Làm → Ra → Xác minh), quy tắc sinh câu, quy tắc nhãn cuối và điều kiện dừng: **`PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md` Mục 3, 6, 7, 9**. Tóm tắt:

| ID | Việc | Loại |
|---|---|---|
| PL.0 | Cổng: P0.1, P0.2, S1, DL1–DL4 đã có câu trả lời | 👤 ⛔ |
| PL.1 | Cấu hình quota, hệ số sinh dư, ngưỡng | 🤖 |
| PL.2 | Chọn đích kiểm tra từ CEFR-J `∥` PL.3 | 🤖 |
| PL.3 | Rubric gán nhãn + câu mẫu neo do đội/GV tự viết `∥` PL.2 | 🤖+👤 |
| PL.4 | Prompt sinh + schema + bộ lọc tự động | 🤖 🔒 |
| PL.5 | Pilot lô nhỏ + GV xem | 🤖→👤 |
| PL.6 | Sinh đầy đủ + lọc tự động | 🤖 |
| PL.7 | Gán nhãn tự động bằng ≥2 mô hình | 🤖 |
| PL.8 | Hàng đợi GV + 2 GV gán độc lập | 👤 ⛔ |
| PL.9 | Đồng thuận (kappa có trọng số) + nhãn cuối | 🤖 |
| PL.10 | Kiểm tra ngoài bằng CLOTH (chỉ khi DL3 cho phép) `∥` PL.11 | 🤖 ⛔ |
| PL.11 | Gán `irt_b` + báo cáo độ phủ `∥` PL.10 | 🤖 |
| PL.12 | Khép sổ (log, quyết định, weekly) | 🤖 |

### P5 — Khép sổ & minh chứng

| ID | Việc | Loại | Xác minh |
|---|---|---|---|
| P5.1 | `AI_USAGE_LOG.md`: dòng cho phiên lập kế hoạch + từng lô sinh câu | 🤖 | Có đủ cột (công cụ, prompt, phần AI sinh, phần sửa, lỗi AI phát hiện) |
| P5.2 | `weekly-log/Tuan-03.md` (và tuần sau): mục "Thay đổi thiết kế & lý do" cho D1–D9 | 🤖 | Khớp `DECISIONS_LOG.md` |
| P5.3 | Cập nhật `TRACKING.md` chỉ với số **đã đo** (độ phủ, đồng thuận, % GV sửa); ô chưa đo = "N/A" | 🤖 | Không có số bịa |
| P5.4 | Mục "Hạn chế dữ liệu" cho báo cáo (độ khó neo CEFR, vòng tròn nhãn, nguồn NC không dùng) | 🤖 | Trích đúng Mục 4.2 |
| P5.5 | Nhắc nhóm: **không tự ký** `COMMITMENT_BASELINE.md`; bộ dữ liệu phải chốt trước mốc Tuần 6 (G1); **không tự commit** | 🤖 | — |

---

## 8. Hướng dẫn dành cho AI Agent thực thi kế hoạch này

### 8.1. Quy tắc bất biến
1. Chỉ làm sau khi P0.1 đã được ghi trong tracking. Làm đúng Mục 6 cột "Mặc định" (hoặc phương án người dùng đã ghi); không "cải tiến" cấu trúc.
2. **Không tự quyết** lựa chọn nào mà kế hoạch này, SRS, diagram đều chưa quy định (CLAUDE.md quy tắc 1) — dừng và hỏi theo 8.3.
3. **Không nhập vào repo hay `items`** bất kỳ nội dung nào từ nguồn có `license_status` khác `VERIFIED_OPEN`. Không scrape EVP/Oxford/trang cần đăng nhập. Không tải bộ yêu cầu đăng ký/ký thỏa thuận (EFCAMDAT) khi chưa được người dùng xác nhận.
4. **Không bịa số liệu** (số dòng, kappa, độ phủ, % sửa) — chỉ ghi số đã đếm/tính bằng lệnh, kèm tên lệnh. Chưa đo = "N/A".
5. Không để Agent tự `APPROVE` câu hỏi; mọi `approved_by` là người thật (GV).
6. Ngôn ngữ: tài liệu/tracking **tiếng Việt**; UML **tiếng Anh**; không dịch diagram (Quyết định #5/#7).
7. Tham số (k, N, ngưỡng, bảng quy đổi `irt_b`) nằm ở cấu hình, không hardcode.
8. Không sửa `.docx`, `AdaptivePlacementTest.xml`, `TLCN.drawio.xml`, `Tuan3/KE_HOACH_PRISMA_…md`, `schema.prisma` trong kế hoạch này (trừ P2.5 sau cổng).
9. Không tự `git init`/commit (chưa có repo; G6 cần xác nhận riêng).

### 8.2. Thứ tự đọc bắt buộc (P0.3)
`CLAUDE.md` → `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md` → file này → `DECISIONS_LOG.md` (#1, #8, #9, #14) → `Tuan2/Phuong_an_sua_doi_AI.md` → `Tuan3/KE_HOACH_PRISMA_SCHEMA_VA_6_HANG_MUC.md` (Q2, A3, P4.D1) → SRS Mục 4.6, 6.1–6.4.

### 8.3. Điều kiện phải DỪNG và hỏi qua `AskUserQuestion` (≥2 phương án + trade-off)
- Q1 chưa được trả lời mà task cần dùng nguồn NC/SA.
- S1: file CEFR-J không có sub-level, hoặc số mục A1–B2 không đủ cho P3.1.
- S3 có phản hồi hạn chế (không cho phân phối lại) hoặc không phản hồi sau thời hạn người dùng đặt.
- P3.6: độ phủ vùng θ∈[−1,+1] dưới ngưỡng Top-5 hoặc thấp hơn nhiều so với SRS 4.4.
- P4.2: đồng thuận GV thấp (cần quyết định: gán lại nhãn, đổi dải `irt_b`, hay chấp nhận và ghi hạn chế).
- P4.4: sai khác lớn giữa `computeEAP` và py-irt/catR.
- Cần thêm bảng/cột/enum ngoài D3–D5, hoặc đổi `ItemSource`.
- Bất kỳ lựa chọn nào ảnh hưởng mở rộng/bảo trì mà không có quy định.

### 8.4. Cách cập nhật file theo dõi (sau **mỗi** task)
Mở `Tuan3/TRACKING_BO_DU_LIEU_ITEM_BANK.md` và:
1. Đổi trạng thái (⬜ → 🔄 khi bắt đầu → ✅ khi **đã chạy xong bước Xác minh**; 🚫 kèm lý do; ⏭ kèm lý do).
2. Điền cột "Bằng chứng": tên lệnh + kết quả tóm tắt + đường dẫn file. Không dán log dài.
3. Tính lại % phase = số ✅ / tổng task của phase.
4. **Thêm 1 dòng** vào "Nhật ký cập nhật" cuối file (append-only).
5. Bị chặn: đặt 🚫, ghi câu hỏi, **không** chuyển sang task phụ thuộc.
6. Task `∥` chỉ cập nhật hàng của chính nó.
7. Khi một quyết định D* đổi hoặc Q* được trả lời: cập nhật bảng "Quyết định" trong tracking **và** ghi `DECISIONS_LOG.md`.

### 8.5. Định nghĩa "xong" (DoD)
- [ ] P1: mỗi nguồn S1–S6 có kết luận Dùng/Không dùng/Chưa rõ kèm bằng chứng.
- [ ] Bank ≥ số câu APPROVED theo bảng 6.3 (hoặc ghi rõ thiếu bao nhiêu), mọi câu có truy vết nguồn, `calibrated=false`, `irt_b` trong khoảng cấp.
- [ ] Không có nội dung từ nguồn `UNVERIFIED`/NC trong `items`.
- [ ] Số liệu đồng thuận GV, độ phủ, mô phỏng đã đo hoặc ghi "N/A" có lý do.
- [ ] `DECISIONS_LOG.md`, `AI_USAGE_LOG.md`, `weekly-log/Tuan-03.md`, `feature-plans/item-bank-data-source.md` đã cập nhật.
- [ ] Danh sách đề xuất SRS v2.7 đã ghi.

---

## 9. Rủi ro

| # | Rủi ro | Xác suất/Tác động | Giảm thiểu |
|---|---|---|---|
| RK1 | CLOTH/nguồn khác không cho phân phối lại | Cao / Trung bình | B không phụ thuộc CLOTH (D6) |
| RK2 | CEFR-J không đủ mục để phủ 280 câu cân đối | Trung bình / Trung bình | S1 đếm trước; dừng hỏi nếu thiếu; có thể gom thêm biến thể câu cho cùng mục |
| RK3 | Chất lượng AI sinh kém ⇒ GV quá tải | Trung bình / Cao | Lớp kiểm duyệt tự động; duyệt hàng loạt; sinh dư 20% (SRS 6.1) |
| RK4 | `irt_b` neo sai lệch hệ thống (vd toàn bộ lệch dương) làm CAT dừng sớm/kéo dài | Trung bình / Cao | M3 mô phỏng độ nhạy; M2 đồng thuận GV; ghi hạn chế |
| RK5 | Hòa hạng Top-5 | Cao nếu không dàn `b` / Thấp | M1/P3.5 |
| RK6 | Rubric TC1 không chấp nhận "tìm nguồn" thay khảo sát (Quyết định #14) | Chưa rõ / Cao | Hỏi GVHD; M2 tạo dữ liệu bên liên quan thật |
| RK7 | Trễ mốc G1 (Tuần 6) | Trung bình / Rất cao | Chốt D1–D2 và S1 trong Tuần 3–4; không đợi S3 |
| RK8 | Vấn đề "vòng tròn CEFR" bị hội đồng chất vấn | Trung bình / Trung bình | Nói rõ ở "Hạn chế"; không dùng kết quả để chứng minh độ chính xác |

---

## 10. Câu hỏi mở (cần bạn trả lời)

| # | Câu hỏi | Vì sao cần | Cần trước |
|---|---|---|---|
| Q1 | Hệ thống TL thuần học thuật phi thương mại, hay sẽ chạy trong EduZ (có thể thương mại)? | Quyết định được dùng giấy phép NC/SA (DS4, DS5, DS8) hay không | P0.2 |
| Q2 | Có ai trong nhóm/GVHD có liên hệ với tác giả CLOTH hoặc có bộ đề nội bộ của trường (đã có quyền sử dụng) không? | Bộ đề nội bộ của trường có thể là nguồn có quyền rõ nhất, thay thế nhu cầu CLOTH | P1 |
| Q3 | Bạn biết bộ MCQ Vocab/Grammar có nhãn CEFR cấp câu mà tôi chưa tìm thấy không? | Phiên này không tìm thấy; tìm thêm bằng đường dẫn cụ thể | P1 |
| Q4 | Có sẵn 2 GV ngoại ngữ để chấm độc lập (M2) không? Số lượng và thời điểm | Quyết định tính khả thi P4.2 | P3.4 |
| Q5 | Cần xác nhận lại D3: chấp nhận khôi phục cột `calibrated` mà diagram đã bỏ ở buổi họp GVHD 18/09? | Có thể ngược với ý GVHD | P2.4 |

---

*Tài liệu tạo trong phiên 2026-10-01 bằng Claude Code (Sonnet 5.5). Các thông tin giấy phép lấy từ kết quả tìm kiếm/trang nguồn tại thời điểm tra cứu; **bắt buộc xác minh lại trực tiếp ở P1 trước khi dùng** — đừng coi bảng Mục 2 là tư vấn pháp lý.*
