# BẢN CAM KẾT SẢN PHẨM CUỐI CÙNG VÀ BỘ METRIC ĐÁNH GIÁ

**Đề tài:** Kiến trúc hệ thống chẩn đoán năng lực ngôn ngữ toàn diện (Placement Test) tích hợp AI tự thích ứng
**Hạn nộp:** 16:49 thứ Hai 23/11/2026 · **Cần GVHD xác nhận**
**Trạng thái:** BẢN NHÁP, viết theo cấu trúc mẫu Nhom20_FinalProject. Con số ghi **[ĐỀ XUẤT]** do AI soạn từ SRS và rubric, nhóm và GVHD phải xác nhận hoặc đổi trước khi nộp. Chưa có số đo thực tế nào.

## 1. MỤC ĐÍCH

Văn bản này xác định sản phẩm cuối cùng nhóm cam kết bàn giao và các chỉ số định lượng để đánh giá. Sau khi hai bên ký, sản phẩm và chỉ số là cơ sở đánh giá; mọi thay đổi phải được GVHD xác nhận và ghi vào nhật ký quyết định.

## 2. SẢN PHẨM CAM KẾT

| # | Sản phẩm | Mã chức năng | Tiêu chí hoàn thành (đo được) |
|---|---|---|---|
| S1 | Đăng nhập JWT, đổi mật khẩu lần đầu, quên mật khẩu bằng OTP | F-01, F-21 | Luồng chạy trên môi trường triển khai; kiểm thử e2e đạt |
| S2 | Ngân hàng câu hỏi với vòng đời một chiều đến `FINAL_APPROVED` | F-02 | Test chứng minh CAT không chọn câu khác `FINAL_APPROVED` |
| S3 | CAT Engine: Rasch 1PL, EAP 41 điểm, Top-5 b-matching, điều kiện dừng | F-03 | 3 ca bắt buộc (toàn đúng, toàn sai, xen kẽ) đạt |
| S4 | Phiên thi Dual-Write (Redis, PostgreSQL), máy trạng thái chống race condition | F-04 | Khôi phục phiên từ PostgreSQL trong ≤ 7200 giây |
| S5 | AI Tutor Explainer (Gemini) | F-05 | 100% câu `FINAL_APPROVED` có giải thích |
| S6 | Language Profile JSON v1 và API | F-06, F-07 | Phản hồi đúng schema v1 |
| S7 | Dashboard kết quả sinh viên; báo cáo lớp cho giảng viên (lọc theo kỳ, xuất CSV) | F-08, F-09 | Màn hình chạy được, tệp CSV mở được |
| S8 | Quản lý tài khoản SV/GV (tạo lẻ, import), kỳ thi, import danh sách thi | F-18 đến F-20, F-22 | ⚠ Mới v3.0, **chờ GVHD xác nhận** (Q-11) |
| S9 | Tạo lô câu hỏi bằng AI hoặc import, AI kiểm C1/C2/C3, giao việc, GV A duyệt, GV B xác nhận, Admin import | F-23 đến F-28 | ⚠ Mới v3.0, **chờ GVHD xác nhận** (Q-11) |
| S10 | Triển khai (CI/CD, Docker, Nginx), tài liệu SRS/SDD, bộ kiểm thử | — | Liên kết môi trường, lịch sử pipeline |

Hạng mục tùy chọn, làm nếu đủ thời gian: ghi bất đồng bộ qua BullMQ kèm email nhắc việc; gán `topic_tag` bằng AI (F-10).

## 3. BỘ METRIC ĐÁNH GIÁ

| # | Chỉ số | Cách đo | Mục tiêu | Căn cứ |
|---|---|---|---|---|
| M1 | Số câu trung bình đến khi dừng | Log `items_administered` | Trong khoảng 20–25 câu; trung bình **≤ 22** | Khoảng 20–25: SRS; 22: **[ĐỀ XUẤT]** |
| M2 | Tỉ lệ phiên dừng do SE < 0,35 trước khi đủ 25 câu | Thống kê `stopping_reason` | **≥ 70%** | **[ĐỀ XUẤT]**, chốt sau Pre-test |
| M3 | Thời gian làm bài trung bình | `test_duration_seconds` | **≤ 20 phút** (trần 45 phút) | Trần: SRS; 20 phút: **[ĐỀ XUẤT]** |
| M4 | Độ trễ API nộp câu và lấy câu tiếp | APM hoặc log | **< 300 ms** ở p95 | SRS 15.1 |
| M5 | Thời gian tính EAP | Đo trong tiến trình | **< 50 ms** | SRS 15.1 |
| M6 | Độ trễ lấy Profile | APM hoặc log | **< 500 ms** ở p95 | SRS 15.1 |
| M7 | Độ phủ kiểm thử module `cat-engine` | Báo cáo coverage | **≥ 70%** | Ngưỡng Mức 5 của rubric, **[ĐỀ XUẤT]** |
| M8 | Độ phủ kiểm thử toàn backend | Báo cáo coverage | **≥ 50%** | **[ĐỀ XUẤT]** |
| M9 | Ca kiểm thử CAT bắt buộc đạt | CI | **3/3** | SRS 4.3 |
| M10 | Độ sẵn sàng trong giờ thi | Giám sát | **≥ 99%** | SRS 15.2 |
| M11 | Số sinh viên tham gia Linear Pre-test | Số liệu pre-test | **≥ 60** | Lộ trình rubric, Tuần 7–8 |
| M12 | Tỉ lệ câu `FINAL_APPROVED` có giải thích | Truy vấn DB | **100%** | SRS F-05 |
| M13 | Tỉ lệ chức năng P0 hoàn thành trong phạm vi đã chốt | Đối chiếu tiêu chí mục 2 | **100%** | **[ĐỀ XUẤT]** |
| M14 | Lỗi nghiêm trọng còn mở khi nộp | Danh sách defect | **0** | **[ĐỀ XUẤT]** |
| M15 | Giải thích được mã do AI sinh khi hội đồng hỏi | Vấn đáp ≥ 5 vị trí ngẫu nhiên | **100%** | Rubric Mức 5 (AI Usage Log) |

**Chưa cam kết số:** độ chính xác CAT so với bài Linear (RQ1). Cần chốt có cam kết một chỉ số, ví dụ tương quan giữa θ của CAT và điểm Linear, và ngưỡng của nó.

## 4. ĐIỀU KIỆN VÀ GIẢ ĐỊNH

- M2 và M3 chỉ đo được sau khi có dữ liệu Pre-test và hiệu chỉnh IRT (Tuần 9–10). Con số có thể điều chỉnh khi có dữ liệu, nhưng phải có xác nhận của GVHD.
- S8 và S9 làm tăng phạm vi so với bản đầu. Nếu GVHD không xác nhận thì giảm khối lượng và ghi rõ lý do.
- Các tham số CAT (θ₀ = −0,5; SE 0,35; tối đa 25 câu; tối thiểu 8 câu trước Early Stop) nằm trong cấu hình và có thể đổi sau hiệu chỉnh.

## 5. KHỐI LƯỢNG VÀ PHÂN CÔNG

| Thành viên | Module phụ trách chính | % khối lượng |
|---|---|---|
| Phương | (điền) | (điền) |
| Đăng | (điền) | (điền) |

Bảng phân công chi tiết theo từng thành viên nộp riêng ngày 30/11.

## 6. XÁC NHẬN

- Sinh viên: ____________ Ngày: ______
- Giảng viên hướng dẫn: ____________ Ngày: ______
