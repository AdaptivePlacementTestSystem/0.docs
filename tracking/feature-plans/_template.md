# Kế hoạch triển khai: <Tên chức năng / vấn đề>

- Slug: `<ten-slug-khong-dau>`
- F-ID (SRS Mục IX) hoặc mô tả vấn đề nếu là bugfix: 
- Phạm vi: ⬜ Tiểu luận (TL)  ⬜ Đặc tả Khóa luận (KL) — đối chiếu bảng "Must-Have TL vs Spec KL", SRS Mục XIV
- Ngày tạo kế hoạch: 
- Người phụ trách: 
- Tuần thực hiện (link): `tracking/weekly-log/Tuan-XX.md`

> File này phải được tạo **trước khi bắt đầu code** cho một chức năng/vấn đề không tầm thường (không cần cho việc sửa 1 dòng vô hại). Xem cách dùng đầy đủ tại `tracking/PROMPT_TEMPLATE_FEATURE.md`.

## 1. Tham chiếu bắt buộc

- SRS: Mục ___
- Class Diagram liên quan (tên lớp, quan hệ): ___ (xem `Mo_ta_So_do_Lop_ClassDiagram.md` / `SRS_TLCN_ClassDiagram_Analysis.md`)
- Interface/pattern có sẵn cần tuân theo (nếu có): ___
- Tiêu chí rubric bị ảnh hưởng: ___

## 2. Thiết kế OOP dự kiến

- Class/Interface mới hoặc bị sửa:
- Pattern áp dụng (Strategy / Adapter / Repository / DI / Value Object...) và lý do chọn:
- Điểm mở rộng cho KL, nếu SRS Mục XIV đã báo trước phần này sẽ mở rộng sau (bắt buộc thiết kế qua interface ngay từ TL nếu có):
- Rủi ro "khó update về sau" đã lường trước và cách phòng tránh (nếu không có rủi ro nào, ghi rõ "không có" thay vì để trống):

## 3. Câu hỏi cần chốt & Quyết định

> **Quy tắc bắt buộc:** bất kỳ lựa chọn nào ảnh hưởng đến khả năng mở rộng/bảo trì về sau mà Mục 1–2 ở trên **chưa** có câu trả lời rõ ràng từ SRS/Class Diagram → phải dừng lại, hỏi người phụ trách/GVHD, **không được tự quyết định thay**. Ghi lại đầy đủ tại đây — kể cả (các) phương án không được chọn — để có thể giải thích lý do khi hội đồng hỏi (TC5, quy trình chống đạo văn Mục 6).

| # | Câu hỏi | Phương án đã đưa ra & đánh đổi (trade-off) | Quyết định | Lý do chọn | Ngày chốt | Đã nhắc ở báo cáo tuần nào |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## 4. Kế hoạch test

- Unit test:
- Integration/API test (nếu có):
- Case đặc biệt cần test (edge case theo SRS, nếu có):

## 5. Trạng thái

- [ ] Đang lên kế hoạch (Mục 1–2 đã điền, mọi câu hỏi mở ở Mục 3 đã được hỏi và chốt)
- [ ] Đang code
- [ ] Test pass
- [ ] Đã merge — commit/PR:
- [ ] Đã cập nhật `tracking/AI_USAGE_LOG.md`
- [ ] Đã nhắc trong `tracking/weekly-log/Tuan-XX.md` tương ứng (bắt buộc nếu Mục 3 có ít nhất 1 quyết định)
