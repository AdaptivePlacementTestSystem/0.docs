# Mẫu Prompt Nhanh — Giao việc cho AI (bản rút gọn)

> Dành cho người ra lệnh (bạn) khi không muốn/không cần điền đủ 7 phần chi tiết của
> [`PROMPT_TEMPLATE_FEATURE.md`](./PROMPT_TEMPLATE_FEATURE.md). Bạn chỉ cần mô tả **việc cần làm**
> theo mẫu dưới — phần "tự đọc SRS, tự áp OOP, tự hỏi khi cần quyết định, tự ghi log tracking"
> AI phải tự làm, không cần bạn nhắc lại mỗi lần (được ép bởi skill `rubric-tracker`).
>
> Lấy cảm hứng từ cách ra lệnh ngắn gọn kiểu `Prompt-WW.txt`: liệt kê gạch đầu dòng, không viết văn.

---

## Cách dùng — copy khối dưới, điền vào chỗ `<...>`, các dòng để trống nếu không biết (AI sẽ tự tìm hoặc hỏi lại)

```
- Yêu cầu: <mô tả ngắn gọn — tính năng mới / sửa bug / refactor. Nêu rõ tên màn hình, API,
  hoặc hành vi mong muốn. Đính kèm ảnh chụp màn hình/link lỗi nếu có>

- Tham chiếu (điền nếu biết, để trống nếu không):
  - F-ID / Mục SRS: <VD: F-03, SRS Mục 4.4>
  - Phạm vi TL hay KL (SRS Mục XIV): <TL / KL / không biết>
  - Class/file liên quan đã biết: <VD: CATEngine, ItemBank>

- Dữ liệu/môi trường (nếu liên quan đến DB, API thật, bug cụ thể): <mô tả hoặc để trống>

- Ràng buộc riêng (nếu có — deadline, hiệu năng NFR, phải tương thích ngược...): <...>

- Lưu kế hoạch vào: tracking/feature-plans/<slug>.md  (để trống → AI tự đặt slug hợp lý)

- Luôn áp dụng (không cần chép lại, AI tự tuân thủ mỗi lần):
  1. Đọc kỹ SRS + Class Diagram liên quan trước khi code (Mo_ta_So_do_Lop_ClassDiagram.md,
     SRS_TLCN_ClassDiagram_Analysis.md).
  2. Tuân thủ đầy đủ `tracking/PROMPT_TEMPLATE_FEATURE.md` (OOP/SOLID, DI, Value Object bất biến,
     không hardcode phần SRS Mục XIV báo trước sẽ mở rộng ở KL) và skill `rubric-tracker`.
  3. Gặp lựa chọn ảnh hưởng khả năng mở rộng/bảo trì mà SRS/Class Diagram KHÔNG nói rõ →
     DỪNG LẠI, hỏi tôi kèm ít nhất 2 phương án + đánh đổi, không tự quyết định.
  4. Sau khi xong: cập nhật `tracking/feature-plans/<slug>.md`, `tracking/AI_USAGE_LOG.md`,
     và `tracking/weekly-log/Tuan-XX.md` nếu có quyết định thiết kế mới.
  5. Nếu thiếu thông tin để làm đúng → hỏi lại tôi, không tự suy đoán rồi làm liều.
```

---

## Ví dụ điền thực tế (tương đương ví dụ CAT Engine trong bản đầy đủ)

```
- Yêu cầu: Cài đặt hàm chọn câu hỏi tiếp theo cho CAT Engine (selectNextItem).

- Tham chiếu:
  - F-ID / Mục SRS: F-03, SRS Mục 4.4
  - Phạm vi: TL (Randomized Top-5 b-matching)
  - Class/file liên quan: CATEngine, ItemBank.findForCAT()

- Dữ liệu/môi trường: dùng item bank giả lập, chưa có dữ liệu thật.

- Ràng buộc riêng: không có.

- Lưu kế hoạch vào: tracking/feature-plans/cat-engine-item-selection.md

- (áp dụng mặc định 5 điều ở trên)
```

Với ví dụ này AI phải tự nhận ra: SRS Mục XIV đã báo trước Sympson-Hetter Exposure Control (F-17)
sẽ thay logic này ở KL → phải hỏi bạn "hardcode thẳng hay tách qua `ItemSelectionStrategy`
injection?" kèm trade-off, rồi mới code tiếp, đúng như quy trình ở
`PROMPT_TEMPLATE_FEATURE.md`.

---

## Khi nào KHÔNG cần tạo feature-plan riêng

Việc quá nhỏ, không ảnh hưởng khả năng mở rộng (sửa lỗi chính tả, đổi 1 dòng CSS, đổi text
thông báo...) — chỉ cần mô tả ở phần "Yêu cầu" và AI ghi 1 dòng vào `tracking/AI_USAGE_LOG.md`
nếu có ý nghĩa, không cần tạo `feature-plans/<slug>.md`. Nếu không chắc việc có "tầm thường"
hay không, cứ để AI tự đánh giá — nếu nghi ngờ AI sẽ tạo feature-plan cho chắc.

## Khi nào nên dùng bản đầy đủ thay vì bản rút gọn này

- Bạn (người ra lệnh) muốn tự tay kiểm soát chi tiết OOP/pattern ngay từ đầu thay vì để AI đề xuất.
- Chức năng phức tạp, nhiều lớp liên quan, muốn soạn sẵn Mục 1–4 của feature-plan trước khi giao AI.
- Chuẩn bị hồ sơ minh chứng cho hội đồng và muốn prompt gốc đã đầy đủ chi tiết ngay trong log.

Trong mọi trường hợp còn lại — kể cả khi dùng bản rút gọn này — kết quả cuối cùng (feature-plan,
AI_USAGE_LOG, weekly-log) phải đầy đủ như thể dùng bản chi tiết; khác biệt duy nhất là **công sức
soạn prompt của người ra lệnh**, không phải mức độ tuân thủ của AI.

## Liên kết

- Bản đầy đủ (7 phần, dùng khi cần soạn kỹ): `tracking/PROMPT_TEMPLATE_FEATURE.md`
- File kế hoạch mỗi chức năng/vấn đề: `tracking/feature-plans/<slug>.md` (tạo từ `_template.md`)
- Báo cáo tuần: `tracking/weekly-log/Tuan-XX.md` (xem thêm `tracking/HUONG_DAN_BAO_CAO_TUAN.md`)
- Nhật ký AI: `tracking/AI_USAGE_LOG.md`
- Skill canh gác tự động: `.claude/skills/rubric-tracker/SKILL.md`
- Hướng dẫn tổng quan rubric: `docs/HUONG_DAN_RUBRIC_VA_TRACKING.md`
