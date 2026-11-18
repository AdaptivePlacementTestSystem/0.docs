# CÁC ĐIỂM CẦN CHỐT: UI STITCH ↔ ĐẶC TẢ v3.0 (nhóm "Làm bài thi CAT" của Student)

> **Ngày:** 10/11/2026 · **Gửi:** Đăng · **Trạng thái:** DRAFT, chờ chốt (chưa sửa SRS/UC/Sequence hay tài liệu chuẩn)
> **Bản này thay thế** `20261110_CAN_CHOT_UI_STITCH_CAT_STUDENT.md` (v1).
> **Nguồn đối chiếu:**
> - Báo cáo `20261109_DANH_GIA_KHOP_UI_STITCH_VA_USECASE_CAT_STUDENT.md`.
> - **Mã HTML thật** của project Stitch "English Placement Test UI" (ID `16753573200013570369`), tải 10/11/2026: S02 (`4263dbd2…`), S03 (`46e63b7d…`), S04 (`5191ec16…`), S05 (`11035123…`), S07 (`9139276e…`).
> - Chưa xem ảnh chụp màn hình; chưa đối chiếu từng dòng SRS (cần Đăng/nhóm xác nhận các mục ghi "đối chiếu SRS").

---

## 1. Kết luận

Thiết kế Stitch bám sát luồng CAT; S02, S04, S07 và phần lớn S05 dùng được sau khi sửa nhỏ. Cần:

- **3 quyết định** của Đăng (ảnh hưởng phạm vi/tài liệu): mục 3.
- **1 lỗi nghiêm trọng** ở S04 cần sửa trước khi code: mục 2.
- Các chỉnh sửa còn lại (mục 4, 5), không đổi phạm vi.

---

## 2. Lỗi nghiêm trọng (sửa bắt buộc, không cần chốt)

| Màn | Lỗi (đã xác minh trong mã) | Hậu quả | Sửa |
|---|---|---|---|
| **S04** | Đáp án **A được chọn sẵn** (`currentSelected = 'A'`, `aria-checked="true"`). | Bài thi không quay lại được câu trước; sinh viên bấm Enter là nộp nhầm A. | Không chọn sẵn đáp án nào. Nút "Nộp đáp án" vô hiệu cho đến khi chọn. |
| **S04** | Phím **Enter** gọi nộp ngay, không kiểm tra đã chọn đáp án. | Như trên. | Chỉ nộp bằng Enter khi đã chọn; cân nhắc xác nhận nhẹ. |
| **S02** | Banner "bài thi dở dang" hiện **cùng lúc** với nút "Bắt đầu bài thi" của kỳ đang mở. | Trái BR-10 và lỗi `SESSION_IN_PROGRESS` (không được tạo phiên mới khi còn phiên dở). | Khi có phiên dở, vô hiệu nút "Bắt đầu" của kỳ đó; chỉ cho "Tiếp tục". |

---

## 3. Cần Đăng quyết định

### Q-A. Layout đọc hiểu 60/40 (Reading passage)
- **Hiện trạng:** Báo cáo gốc nêu từ `DESIGN.md`. Các màn Stitch đã tải **chỉ có câu trắc nghiệm ngắn**, không có layout đọc hiểu. TL v3.0 chỉ có **Vocabulary và Grammar**; `Item` chưa có trường ngữ liệu.
- **Phương án:**
  1. **Không làm trong TL, ghi [KL] (khuyến nghị).** Không đổi phạm vi và schema.
  2. **Làm trong TL.** Thêm skill Reading và trường ngữ liệu vào `Item`/schema, cập nhật `COMMITMENT_BASELINE` trước G1 (hết Tuần 6), rà soát cả bộ tài liệu.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

### Q-B. Màn S03 (Giới thiệu bài thi) chen giữa Dashboard và phòng thi
- **Hiện trạng:** Đặc tả UCSV02: bấm "Bắt đầu" gọi API tạo phiên và vào thẳng phòng thi. Stitch có thêm S03 với 6 quy tắc.
- **Phương án:**
  1. **Giữ S03 (khuyến nghị).** Tránh bấm nhầm và tính giờ oan. Phải cập nhật UCSV02, Sequence, mô tả màn hình, `DECISIONS_LOG`; phải chốt **đồng hồ chỉ bắt đầu khi `POST /sessions`**, không phải lúc mở S03.
  2. **Bỏ S03.** Chuyển 6 quy tắc thành hộp xác nhận (modal) trên Dashboard.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

### Q-C. Vào lại khi phiên đã quá hạn (`now >= expiresAt`)
- **Hiện trạng:** Báo cáo gốc đề xuất client tự gọi API kết thúc phiên theo luật K5.
- **Phương án:**
  1. **Server quyết định (khuyến nghị).** `GET /sessions/active` và `/resume` kiểm tra hạn ở server, áp luật K5 (≥ 8 câu thì `COMPLETED` + `TIMEOUT`, ít hơn thì `ABANDONED`), trả trạng thái; client chỉ hiển thị.
  2. **Client gọi API kết thúc.** Phụ thuộc đồng hồ client, dễ lệch, sẽ sót nếu sinh viên đóng tab.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

### Q-D. Chỉ số theo kỹ năng trên S05 (đối chiếu SRS trước)
- **Hiện trạng:** S05 hiển thị "Từ vựng 68% (9/13 câu đúng) – ước lượng B1" và "Ngữ pháp 58% (7/12) – ước lượng A2".
  - Tỷ lệ đúng là số tính được từ `SessionResponse`, nhưng với thi thích ứng nó luôn quanh 50% nên dễ gây hiểu lầm.
  - Tổng số câu 13 + 12 = 25, khớp mức tối đa 25 câu; không có mâu thuẫn số câu.
  - "Ước lượng B1/A2 theo kỹ năng" cần θ riêng từng kỹ năng; chưa thấy SRS quy định.
- **Phương án:**
  1. **Hiện số câu đúng/tổng theo kỹ năng, bỏ thanh phần trăm và bỏ mức CEFR theo kỹ năng (khuyến nghị nếu SRS không có θ theo kỹ năng).**
  2. **Giữ mức CEFR theo kỹ năng.** Chỉ khi SRS/`LanguageProfile` có θ theo kỹ năng; nếu chưa thì phải bổ sung vào SRS và schema.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

---

## 4. Cần chỉnh trên Stitch (không đổi phạm vi)

| Màn | Vấn đề | Sửa |
|---|---|---|
| S02 | Banner dở dang không có tên kỳ thi. | Thêm tên kỳ thi vào banner. Thêm biến thể "phiên đã hết hạn" (ẩn nút Tiếp tục, ghi "đang ghi nhận kết quả"). |
| S02 | Kỳ "Chưa mở" ghi mở 25/10/2026 (đã qua so với hôm nay 10/11). | Đổi dữ liệu mẫu sang ngày tương lai. |
| S02 ↔ S07 | Dữ liệu mẫu mâu thuẫn: S02 "gần nhất" 10/10/2026, θ +0.42, "học kỳ 1"; S07 lần gần nhất 12/10/2026, θ +0.28, kỳ K2026. | Thống nhất một bộ dữ liệu mẫu. |
| S03 | Nhãn "Phòng thi số 04": spec không có khái niệm phòng thi. | Bỏ nhãn. |
| S03 | Quy tắc 2 ghi "60 phút" cạnh "còn 45 phút". | Ghi rõ: "tối đa 45 phút do kỳ thi đóng lúc 11:30" (`min(durationMinutes, closesAt)`). |
| S04 | Không có trạng thái: dưới 5 phút (đỏ `#DC2626`), hết giờ (khóa phương án, "Đang nộp phiên..."), mất mạng/lỗi nộp. | Thêm 4 trạng thái. Lưu tạm đáp án khi rớt mạng phải kèm idempotency; retry sau `expiresAt` bị server từ chối. |
| S05 | Khối bị bỏ trống trong HTML: banner vùng biên (Pre-A1, C1+), lý do dừng thi. | Thêm banner và dòng lý do dừng (SE < 0.35 / đủ 25 câu / Outlier Early Stop / hết giờ). |
| S05 | Có Khối 5 "Gợi ý học tập AI" (đang để trống). Không thuộc phạm vi TL. | Bỏ hẳn. |
| S05 | Thang CEFR chỉ có marker, không hiện θ và SE (S07 có hiện). | Thêm "θ ± SE" dưới thang. Nhãn "Độ tin cậy: Cao" phải suy ra từ SE theo quy tắc rõ ràng. |
| S07 | Trạng thái chỉ có "Hoàn thành". | Thêm `ABANDONED` ("Bỏ dở", không có nút xem kết quả) và `TIMEOUT`; thêm trạng thái rỗng. |
| **S06** | **Chưa có** màn xem lại đáp án + giải thích AI (UCSV05). | Thiết kế mới, chỉ đọc: câu đã làm, đáp án đã chọn, đáp án đúng, thẻ giải thích AI, trạng thái chưa có giải thích. |
| Tất cả | Mọi link là `href="#"`; S03 trỏ `/student/exams/round-k2026/test`; "Quay lại" trỏ `/student`. | Dùng route chuẩn: `/student/dashboard`, `/student/exams/[roundId]`, `/student/exams/[roundId]/take`, `/student/results/[sessionId]`, `/student/results/[sessionId]/review`, `/student/history`, `/change-password`. |

---

## 5. Lưu ý cho khâu code

- Trang `take` đặt trong nhóm route `(exam)` (layout trống) đã có sẵn trong frontend, không phải `(student)`. Đối chiếu `docs-repo/design/structure/`.
- Các con số "khớp 92%" và "88%" trong báo cáo gốc không có cách tính: không đưa vào `TRACKING.md`.

---

## 6. Sau khi Đăng chốt

1. Đồng bộ cả bộ tài liệu (SRS, đặc tả UC, Sequence, mô tả màn hình, danh sách màn hình).
2. Ghi quyết định vào `DECISIONS_LOG.md` và `AI_USAGE_LOG.md`.
3. Nếu chọn Q-A phương án 2 hoặc Q-D phương án 2: cập nhật `COMMITMENT_BASELINE.md` trước G1.
4. Sửa Stitch theo mục 2 và 4, rồi xuất lại HTML.
