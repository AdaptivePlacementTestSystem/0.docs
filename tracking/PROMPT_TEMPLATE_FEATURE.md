# Mẫu Prompt chuẩn (đầy đủ) — Triển khai một Chức năng / Xử lý một Vấn đề

> Dùng mẫu này **mỗi khi giao việc** cho Claude Code (hoặc AI khác) để: triển khai một F-ID trong SRS, sửa một bug, refactor một module, hoặc thêm một API mới. Mục đích: ép mọi lần triển khai đều bám đúng SRS + Class Diagram, đúng OOP, không âm thầm tạo ra thứ khó sửa/khó mở rộng sau này, và **mọi quyết định thiết kế còn bỏ ngỏ phải được hỏi-chốt-ghi log cho từng vấn đề** thay vì để AI tự quyết định.
>
> Cần ra lệnh nhanh, không muốn điền đủ 7 phần? Dùng bản rút gọn: [`PROMPT_TEMPLATE_SIMPLE.md`](./PROMPT_TEMPLATE_SIMPLE.md) — AI vẫn phải tuân thủ đầy đủ các quy tắc bên dưới, chỉ khác ở công sức soạn prompt.

## Cấu trúc prompt chuẩn — 7 phần, copy & điền trước khi gửi cho AI

### 1. Bối cảnh & phạm vi
- Tên chức năng/vấn đề:
- F-ID / Mục SRS liên quan (SRS Mục IX):
- Phạm vi: **TL** hay **KL** theo bảng "Must-Have TL vs Spec KL" (SRS Mục XIV) — nêu rõ để AI không lỡ code phần KL vào TL hoặc ngược lại (rủi ro R11 trong Risk Register).
- File kế hoạch: yêu cầu AI tạo/cập nhật `tracking/feature-plans/<slug>.md` (từ `_template.md`) **trước khi viết code**.

### 2. Tham chiếu bắt buộc AI phải đọc trước khi code
- Mục SRS cụ thể liên quan đến chức năng này.
- (Các) lớp trong Class Diagram liên quan — tên lớp + quan hệ (`Mo_ta_So_do_Lop_ClassDiagram.md`, `SRS_TLCN_ClassDiagram_Analysis.md`).
- Interface/pattern đã có sẵn cần tuân theo (ví dụ `AuthProvider` — Adapter Pattern, `ItemRepository`, DI của NestJS...).

### 3. Yêu cầu OOP & khả năng mở rộng — không thương lượng, luôn áp dụng
- Tuân thủ SOLID, đặc biệt **Single Responsibility** (không tạo God Class/God Service) và **Open/Closed** (mở để mở rộng, đóng để sửa đổi) — vì kiến trúc SRS đã cố tình tách rõ phạm vi TL vs KL, code phải cho phép KL "cắm thêm" mà không phải viết lại phần TL.
- Không hardcode giá trị/nhánh logic nghiệp vụ có khả năng thay đổi (ngưỡng SE/timeout, thuật toán chọn item, mapping CEFR, θ₀...) — đưa ra sau `ConfigService`/biến môi trường hoặc interface (Strategy) thay vì hardcode trong service.
- Dependency Injection qua constructor (đúng chuẩn NestJS) — không `new` trực tiếp một implementation cụ thể trong service khác.
- Value Object phải bất biến (immutable) — đúng quyết định OOAD đã có sẵn cho `AbilityEstimate` (xem Mục 9, `SRS_TLCN_ClassDiagram_Analysis.md`).
- Nếu đây là điểm SRS đã báo trước sẽ mở rộng ở KL (SRS Mục XIV) — **bắt buộc** thiết kế qua interface/Strategy pattern ngay từ TL, không chờ đến KL mới tách.

### 4. Ràng buộc rubric cần giữ khi code phần này
- Liệt kê tiêu chí rubric liên quan (VD: TC2.1 — thiết kế phải khớp mã nguồn khi đối chiếu; TC2.4 — lint/duplication/git convention; TC2.5 — bắt buộc có test kèm; TC2.3 — nếu AI hỗ trợ nhiều, cần log chi tiết).
- Yêu cầu unit test đi kèm ngay trong cùng lần triển khai, đặc biệt nếu đụng tới thuật toán học thuật (Rasch/EAP/quadrature...).

### 5. Quy tắc "KHÔNG tự quyết định" — luôn giữ nguyên phần này trong mọi prompt
> Nếu trong lúc triển khai phát sinh một lựa chọn **ảnh hưởng đến khả năng mở rộng/bảo trì về sau** (đặt tên, cấu trúc module, chọn pattern, mức độ coupling giữa 2 lớp, thêm field cứng, đổi schema...) và SRS/Class Diagram **không** có chỉ dẫn rõ ràng cho lựa chọn đó — **DỪNG LẠI**. Nêu rõ câu hỏi, tối thiểu 2 phương án kèm đánh đổi (trade-off) của từng phương án, rồi chờ người dùng chốt. **Không tự chọn giúp.**
>
> Sau khi được chốt: ghi ngay vào Mục 3 ("Câu hỏi cần chốt & Quyết định") của file kế hoạch `tracking/feature-plans/<slug>.md` — kể cả phương án không được chọn, để còn giải thích được lý do khi hội đồng hỏi (TC5, quy trình chống đạo văn Mục 6) — và tóm tắt lại trong báo cáo tuần hiện tại (`tracking/weekly-log/Tuan-XX.md`, mục "Thay đổi thiết kế & lý do").

### 6. Định nghĩa "Xong" (Definition of Done) cho prompt này
- Code chạy được + unit test đi kèm pass.
- `tracking/feature-plans/<slug>.md` cập nhật đầy đủ, mọi câu hỏi ở Mục 3 đã có quyết định, trạng thái chuyển sang "Đã merge".
- `tracking/AI_USAGE_LOG.md` có dòng tương ứng cho phiên làm việc này.
- Nếu Mục 3 của feature plan có ít nhất 1 quyết định mới → đã nhắc lại trong `weekly-log` của đúng tuần đó.

### 7. (Tuỳ chọn) Ràng buộc phi chức năng cụ thể của phần này
- Trích từ NFR liên quan trong SRS Mục XV nếu chức năng này chạm tới latency/RBAC/reliability cụ thể (ví dụ: API submit+next-item phải <300ms p95).

---

## Ví dụ đầy đủ — áp dụng cho F-03 (CAT Engine)

> **1. Bối cảnh:** Triển khai `CATEngine.selectNextItem()`. F-03, SRS Mục 4.4. Phạm vi: TL (Randomized Top-5 b-matching).
>
> **2. Tham chiếu:** SRS Mục 4.4 (thuật toán + SQL mẫu); Class Diagram: `CATEngine` (service, dependency tới `Item`/`ItemBank`), `ItemBank.findForCAT()`.
>
> **3. OOP & mở rộng:** SRS Mục XIV đã báo trước Sympson-Hetter Exposure Control sẽ thay thế logic chọn item này ở KL (F-17) → **bắt buộc** tách logic chọn item ra sau một interface, không hardcode thẳng trong `CATEngine`.
>
> **4. Ràng buộc rubric:** TC2.1 (đối chiếu đúng SQL/thuật toán trong SRS), TC2.5 (test với item bank giả lập nhiều kích thước).
>
> **5. Câu hỏi cần chốt (ví dụ AI phải đặt ra thay vì tự quyết):**
> "`CATEngine.selectNextItem` nên (A) hardcode Randomized Top-5 ngay trong class, hay (B) nhận `ItemSelectionStrategy` qua constructor injection?
> - Phương án A: code nhanh hơn ở TL, nhưng khi làm KL (Sympson-Hetter, F-17) phải sửa lại toàn bộ `CATEngine` đã ổn định — tăng rủi ro regression cho phần lõi đã được chấm điểm ở TL.
> - Phương án B: tốn thêm ~30 phút thiết kế 1 interface, nhưng ở KL chỉ cần thêm 1 class mới implement interface đó, không đụng tới code TL.
> Bạn chọn phương án nào?"
> → Quyết định (ví dụ): chọn B, ghi vào `tracking/feature-plans/cat-engine-item-selection.md` Mục 3, nhắc lại ở `weekly-log/Tuan-05.md`.

## Prompt phản ví dụ — KHÔNG nên dùng

> "Viết giúp tôi CATEngine chọn câu hỏi tiếp theo."

Vấn đề: không tham chiếu SRS/Class Diagram, không có yêu cầu OOP, không có quy tắc dừng lại để hỏi → AI sẽ tự quyết định toàn bộ (kể cả những điểm lẽ ra phải hỏi), khó truy vết lý do sau này, và rất dễ bị đuối lý khi hội đồng hỏi tại Mục 6 (chống đạo văn) vì không ai giải thích được vì sao chọn cách này.

## Liên kết

- Bản rút gọn (ra lệnh nhanh): `tracking/PROMPT_TEMPLATE_SIMPLE.md`
- File kế hoạch mỗi chức năng/vấn đề: `tracking/feature-plans/<slug>.md` (tạo từ `_template.md`)
- Báo cáo tuần: `tracking/weekly-log/Tuan-XX.md` (xem thêm `tracking/HUONG_DAN_BAO_CAO_TUAN.md`)
- Nhật ký AI: `tracking/AI_USAGE_LOG.md`
- Hướng dẫn tổng quan rubric: `docs/HUONG_DAN_RUBRIC_VA_TRACKING.md`
