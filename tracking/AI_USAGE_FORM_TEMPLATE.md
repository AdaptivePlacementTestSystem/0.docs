# Mẫu khai báo "Công cụ AI đã dùng" theo form báo cáo tuần

> Trích từ form báo cáo tuần (ảnh chụp màn hình người dùng cung cấp 2026-09-18): "Khai báo từng công cụ AI đã dùng — GVHD/GVPB sẽ xem lại thông tin này khi chấm." Form có nút "+ Thêm công cụ AI" → lặp lại 1 khối bên dưới cho mỗi công cụ khác nhau dùng trong tuần.
>
> Nguồn dữ liệu để điền: `tracking/AI_USAGE_LOG.md` (đã ghi chi tiết theo từng lần tương tác) — form này chỉ là bản **tổng hợp theo tuần, theo từng công cụ**, không thay thế AI_USAGE_LOG.md.

## Prompt chuẩn (dùng lại mỗi tuần — điền vào 5 ô của form)

> "Prompt đã dùng" không phải chép nguyên văn cả hội thoại — mà phải **cho thấy nhóm dùng đúng quy trình prompt chuẩn 7 phần** đã lập ở `tracking/PROMPT_TEMPLATE_FEATURE.md` (bối cảnh/phạm vi → tài liệu tham chiếu bắt buộc → yêu cầu OOP → ràng buộc rubric → quy tắc không tự quyết định → ghi log → tracking), rút gọn thành 5 khối dưới đây. Đây chính là bằng chứng cho TC2.3 Mức 5 ("quy trình hóa thành hệ thống"), không phải mô tả chung chung "dùng AI viết code".

```
Công cụ AI: <VD: Claude Code, ChatGPT, GitHub Copilot>
Phiên bản / model: <VD: Claude Sonnet 5, GPT-5>

Prompt đã dùng:
[Bối cảnh & phạm vi] <Việc gì, thuộc F-ID/mục SRS nào, phạm vi Tiểu luận hay Khóa luận (bảng Must-Have TL vs Spec KL, SRS Mục XIV) — nêu rõ để AI không code lố phạm vi>

[Tài liệu tham khảo bắt buộc AI phải đọc trước] <Liệt kê đúng tên file/mục: SRS Mục ___, Mo_ta_So_do_Lop_ClassDiagram.md mục ___, feature-plan liên quan nếu có>

[Yêu cầu ghi log] <Yêu cầu tường minh trong prompt: "ghi lại vào tracking/AI_USAGE_LOG.md — nêu rõ phần AI sinh và phần thành viên tự sửa"; nếu có quyết định thiết kế mới phát sinh, yêu cầu ghi vào Mục 3 file feature-plan>

[Yêu cầu tracking] <Yêu cầu tường minh: cập nhật tracking/weekly-log/Tuan-XX.md mục "Thay đổi thiết kế & lý do" / "Công việc đã hoàn thành"; cập nhật tracking/TRACKING.md nếu có số liệu KPI thay đổi>

[Nội dung yêu cầu cụ thể] <Câu lệnh chính đã gõ thực tế, tóm tắt 1-3 dòng>

Nội dung AI tạo ra:
<Liệt kê cụ thể: file nào / đoạn nào / class nào AI sinh ra hoặc sửa đổi trong tuần>

Phần bạn đã sửa / hoàn thiện:
<Liệt kê phần thành viên tự kiểm tra, sửa, bổ sung, hoặc việc còn phải làm để xác nhận — KHÔNG được để trống, đây là phần rubric TC2.3 kiểm tra kỹ nhất>
```

(Nếu tuần đó dùng nhiều công cụ AI khác nhau, copy khối trên và lặp lại — tương ứng nút "+ Thêm công cụ AI".)

---

## Ví dụ đã điền — Tuần 1 (tổng hợp từ `AI_USAGE_LOG.md`, dòng 2026-09-13 → 2026-09-14)

```
Công cụ AI: Claude Code
Phiên bản / model: Claude Sonnet 5

Prompt đã dùng:
[Bối cảnh & phạm vi]
- Thiết lập hạ tầng quản lý dự án theo đúng Rubric Khoa: hệ thống tracking + Skill Claude Code rubric-tracker (không gắn F-ID cụ thể, thuộc quy trình chung TC2.3/TC5).
- Phân tích chi tiết F-03 CATEngine (SRS Mục 4.1–4.5), phạm vi Tiểu luận: Rasch 1PL unidimensional, Randomized Top-5 b-matching, EAP 41-quadrature — không bao gồm phần đã xếp cho Khóa luận (Sympson-Hetter, đa chiều).
- Xác định phạm vi Must-have TL vs Spec KL cho EduZServiceAccount và RBAC Admin/Teacher (SRS Mục XIV, Mục 15.3–15.4).

[Tài liệu tham khảo bắt buộc AI phải đọc trước]
- `SRS_TLCN (3).md` — Mục 4.1–4.5 (CAT Engine/Rasch/EAP), Mục XIV (bảng Must-Have TL vs Spec KL), dòng 691 (chốt phạm vi RBAC M2M), Mục 15.3–15.4 (RBAC).
- `0.docs/Mo_ta_So_do_Lop_ClassDiagram.md` — mục CATEngine, EduZServiceAccount, User, quan hệ Institution.
- `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (rubric chấm điểm của Khoa) để đối chiếu TC1/TC2.x khi dựng hệ thống tracking.

[Yêu cầu ghi log]
- Yêu cầu AI ghi lại mỗi lần tương tác quan trọng vào `tracking/AI_USAGE_LOG.md` (bảng "Bảng nhật ký") — nêu rõ phần AI sinh và phần thành viên phải tự sửa/kiểm chứng, không ghi chung chung.
- Yêu cầu tạo `tracking/feature-plans/f03-cat-engine.md` để lưu các câu hỏi/quyết định thiết kế phát sinh khi phân tích F-03 (round-robin, skill bắt đầu...) thay vì để AI tự chọn ngầm.
- Yêu cầu AI tự ghi lại vào bảng "Lỗi/ảo giác AI đã tự phát hiện" trong `AI_USAGE_LOG.md` nếu tự phát hiện mình từng ngầm quyết định thay người dùng.

[Yêu cầu tracking]
- Yêu cầu mọi thay đổi thiết kế mới chốt (Institution-User, bỏ EduZServiceAccount khỏi TL, round-robin chọn skill, phạm vi Admin) phải ghi vào `tracking/weekly-log/Tuan-01.md` mục "Thay đổi thiết kế & lý do" — kèm lý do, không chỉ kết luận.
- Yêu cầu cập nhật `tracking/TRACKING.md` (Dashboard) khi có số liệu KPI/metric của tuần thay đổi (VD: hàng AI Usage Log ở TC2.3, tần suất báo cáo ở mục Quy trình thực hiện).

[Nội dung yêu cầu cụ thể — một số câu lệnh chính đã gõ]
- "Giải thích chi tiết CATEngine.selectNextItem/checkStoppingCriterion đối chiếu SRS, ghi toàn bộ giải thích vào file .md."
- "Mô tả luồng hoạt động đầy đủ của CAT Engine từ đầu đến cuối bài thi kèm ví dụ số liệu, xuất ra file .md."
- "Bỏ EduZServiceAccount khỏi phạm vi Tiểu luận — dựa vào đâu mà có entity này?" (câu hỏi ngược buộc AI đối chiếu lại SRS thay vì giữ nguyên giả định ban đầu).
- "Phân biệt quyền của các User trong hệ thống" rồi yêu cầu làm rõ riêng Admin và Teacher.
- "Vậy ban đầu nó chọn skill như nào?" (phát hiện AI tự quyết định ngầm, buộc AI dừng lại hỏi qua `AskUserQuestion`).

Nội dung AI tạo ra:
- `docs/HUONG_DAN_RUBRIC_VA_TRACKING.md`, các template trong `tracking/` (AI Usage Log, Commitment Baseline, Git Conventions, Evidence Checklist, Dashboard, Weekly Log, HUONG_DAN_BAO_CAO_TUAN.md) và `.claude/skills/rubric-tracker/`.
- `tracking/PROMPT_TEMPLATE_FEATURE.md`, `tracking/feature-plans/_template.md`, `tracking/feature-plans/f03-cat-engine.md`.
- Các mục bổ sung trong `0.docs/Mo_ta_So_do_Lop_ClassDiagram.md` (ghi chú EduZServiceAccount, giải thích chi tiết CATEngine, phân biệt quyền User).
- `0.docs/Luong_Hoat_Dong_CATEngine.md` (luồng đầy đủ CAT kèm ví dụ số liệu minh hoạ).

Phần bạn đã sửa / hoàn thiện:
- Cần đọc lại và điều chỉnh KPI trong `COMMITMENT_BASELINE.md` cho khớp thực tế đề tài trước khi ký (chưa ký).
- Xác nhận lại với người vẽ sơ đồ gốc `TLCN-Phương.drawio.png` về việc bỏ `EduZServiceAccount` khỏi phạm vi Tiểu luận.
- Đối chiếu công thức/số liệu CAT (θ₀, prior, 41 quadrature points, ngưỡng SE<0.35...) với đúng phiên bản SRS hiện hành trước khi dùng để bảo vệ.
- Số liệu ví dụ trong `Luong_Hoat_Dong_CATEngine.md` là minh hoạ tự tạo, cần thay bằng số liệu thật khi có unit test `computeEAP` chạy thật.
- Phát hiện 1 lỗi AI tự quyết định (chọn skill Vocabulary bắt đầu) mà chưa hỏi trước khi có số liệu minh hoạ — đã sửa bằng cách hỏi lại và chốt random 50/50 (ghi ở bảng "Lỗi/ảo giác AI đã tự phát hiện" trong AI_USAGE_LOG.md).
```
