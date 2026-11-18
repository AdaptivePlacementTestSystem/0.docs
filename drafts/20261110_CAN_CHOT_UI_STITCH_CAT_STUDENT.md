# CÁC ĐIỂM CẦN CHỐT: UI STITCH ↔ ĐẶC TẢ v3.0 (nhóm "Làm bài thi CAT" của Student)

> **Ngày:** 10/11/2026
> **Gửi:** Đăng
> **Nguồn:** `D:\20261109_DANH_GIA_KHOP_UI_STITCH_VA_USECASE_CAT_STUDENT.md` (báo cáo đánh giá 09/11/2026)
> **Phạm vi:** UCSV02, UCSV03, UCSV07 (cốt lõi); UCSV04, UCSV05, UCSV06 (bổ trợ)
> **Trạng thái:** DRAFT, chờ chốt. Chưa sửa SRS, Use Case, Sequence hay tài liệu chuẩn nào.
> **Lưu ý:** Các nhận định dưới đây dựa trên báo cáo, chưa đối chiếu trực tiếp với file HTML Stitch.

---

## 1. Kết luận nhanh

Thiết kế Stitch bám sát luồng CAT và dùng được gần như nguyên bản cho S02, S04, S07 và phần lớn S05. Có **3 điểm cần Đăng quyết định** (ảnh hưởng phạm vi hoặc tài liệu), **4 điểm cần chỉnh** (không đổi phạm vi), và một màn hình còn thiếu (S06).

---

## 2. Phần phù hợp (giữ nguyên)

| Màn | Nội dung khớp |
|---|---|
| S02 Dashboard | Thẻ "Kỳ thi của tôi" với 3 trạng thái Đang mở / Chưa mở / Đã thi (khớp BR-10, `ExamRoundStatus`); banner bài thi dở dang (UCSV07) |
| S04 Phòng thi | Layout không header; đồng hồ theo `expiresAt`; 4 phương án; không hiện đúng/sai hay θ; phím tắt A-D / 1-4 |
| S05 Kết quả | Thang CEFR 6 bậc; θ và SE; kỹ năng Vocab/Grammar; chủ đề yếu |
| S07 Lịch sử | Bảng (desktop) và thẻ (mobile); nhãn "Dừng sớm"; phân trang |
| Route | Hướng chuẩn hóa: `/student/exams/[roundId]/take`, `/student/results/[sessionId]`, `/student/history`, bỏ `href="#"` |

---

## 3. Cần Đăng quyết định

### Q-A. Layout đọc hiểu 60/40 (Reading passage)

- **Hiện trạng:** Báo cáo lấy từ `DESIGN.md` rằng bài thi có đọc hiểu dài, cần layout 2 cột 60/40. Nhưng TL v3.0 chỉ có **Vocabulary và Grammar**, `Item` chưa có trường ngữ liệu.
- **Phương án:**
  1. **Bỏ khỏi TL, ghi [KL] (khuyến nghị).** Không đổi phạm vi và schema.
  2. **Làm trong TL.** Phải thêm skill Reading và trường ngữ liệu vào `Item`/schema, cập nhật `COMMITMENT_BASELINE` trước G1 (hết Tuần 6), và rà soát lại cả bộ tài liệu.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

### Q-B. Màn S03 (Giới thiệu bài thi) chen giữa Dashboard và phòng thi

- **Hiện trạng:** Đặc tả UCSV02 bấm "Bắt đầu" là gọi API tạo phiên và vào thẳng phòng thi. Stitch có thêm S03 liệt kê 6 quy tắc rồi mới vào.
- **Phương án:**
  1. **Giữ S03 (khuyến nghị).** Tránh bấm nhầm và tính giờ oan. Phải cập nhật UCSV02, Sequence Diagram, mô tả màn hình và `DECISIONS_LOG`. Phải chốt: **đồng hồ chỉ bắt đầu khi `POST /sessions`**, không phải khi mở S03.
  2. **Bỏ S03.** Giữ đúng đặc tả; chuyển 6 quy tắc thành hộp xác nhận (modal) trên Dashboard.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

### Q-C. Xử lý khi vào lại sau khi phiên đã quá hạn (`now >= expiresAt`)

- **Hiện trạng:** Báo cáo đề xuất client tự gọi API kết thúc phiên theo luật K5.
- **Phương án:**
  1. **Server quyết định (khuyến nghị).** `GET /sessions/active` và `/resume` kiểm tra hạn ở server, áp luật K5 (≥ 8 câu thì `COMPLETED` + `TIMEOUT`, ít hơn thì `ABANDONED`), rồi trả trạng thái. Client chỉ hiển thị. Đồng hồ client không đáng tin.
  2. **Client gọi API kết thúc.** Dễ lệch giờ, dễ bị bỏ qua nếu sinh viên đóng tab.
- **Chốt:** ☐ Phương án 1 ☐ Phương án 2

---

## 4. Cần chỉnh (không đổi phạm vi)

| # | Màn | Vấn đề | Đề xuất |
|---|---|---|---|
| D | S05 | "Vocabulary 68%" và nhãn "Độ tin cậy: Cao". Rasch chỉ cho θ và SE, không có phần trăm. | Xác định nguồn dữ liệu thật (`LanguageProfile`/`AbilityEstimate`). Nếu không có thì đổi sang mức CEFR theo kỹ năng hoặc bỏ. Nhãn độ tin cậy phải suy ra từ SE theo quy tắc rõ ràng. |
| E | S04 | Phím Enter nộp ngay, trong khi không quay lại được câu trước. | Chỉ cho nộp khi đã chọn đáp án; cân nhắc xác nhận nhẹ. |
| F | S04 | Lưu tạm `localStorage` khi rớt mạng. | Cần idempotency (một câu chỉ chấm một lần); retry sau `expiresAt` bị server từ chối; UI có trạng thái "Đang chờ kết nối", không đoán đúng/sai. |
| G | Cấu trúc | Báo cáo đặt trang `take` trong `(student)`; frontend đã có nhóm `(exam)`. | Đặt `take` trong `(exam)` (layout trống). Đối chiếu `docs-repo/design/structure/`. |

Ghi chú: các con số "khớp 92%" và "88%" trong báo cáo gốc không có cách tính, **không đưa vào `TRACKING.md`**.

---

## 5. Việc cần chỉnh trên Stitch (sau khi chốt)

| Màn | Việc |
|---|---|
| S02 Dashboard | Thêm tên kỳ thi vào banner dở dang; biến thể "phiên đã hết hạn" (ẩn nút Tiếp tục, hiện "đang ghi nhận kết quả"); nút "Bắt đầu" trỏ `/student/exams/{roundId}` |
| S03 | Sửa link `/test` thành `/take`; nút Quay lại về `/student/dashboard`; thêm trạng thái lỗi `NOT_IN_ROUND`, `ROUND_NOT_OPEN`, `ROUND_ALREADY_COMPLETED`, `SESSION_IN_PROGRESS` |
| S04 | Đồng hồ dưới 5 phút chuyển đỏ `#DC2626`; trạng thái hết giờ (khóa phương án, "Đang nộp phiên..."); trạng thái mất mạng và lỗi nộp. Không làm biến thể Reading nếu chọn Q-A phương án 1 |
| S05 | Banner vùng biên (Pre-A1, C1+); dòng lý do dừng (SE < 0.35 / đủ 25 câu / Outlier Early Stop / hết giờ); xử lý mục D |
| **S06 (mới)** | Màn xem lại: danh sách câu đã làm, đáp án đã chọn, đáp án đúng, thẻ giải thích AI, trạng thái chưa có giải thích; chỉ đọc, cùng phong cách S04. Route `/student/results/[sessionId]/review` |
| S07 | Trạng thái rỗng; `ABANDONED` ("Bỏ dở", không có nút xem kết quả); `TIMEOUT` |
| Toàn bộ | Thay mọi `href="#"` và anchor giả bằng route chuẩn |

---

## 6. Sau khi chốt

1. Đồng bộ tài liệu theo quy tắc #7: SRS, đặc tả UC, Sequence, mô tả màn hình, danh sách màn hình.
2. Ghi quyết định vào `DECISIONS_LOG.md` và `AI_USAGE_LOG.md`.
3. Nếu chọn Q-A phương án 2: cập nhật `COMMITMENT_BASELINE.md` trước G1.
