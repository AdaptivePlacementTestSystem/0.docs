# Bản cam kết sản phẩm cuối cùng và bộ metric đánh giá

> **Hạn nộp:** 16:49 thứ Hai 23/11/2026 · **Cần GVHD xác nhận** · Tiêu chí: Tính thực tiễn của đề tài; Mức độ hoàn thiện sản phẩm và khối lượng công việc
> **Trạng thái:** BẢN NHÁP. Mọi con số ghi **[ĐỀ XUẤT]** do AI soạn từ SRS/rubric, nhóm và GVHD phải xác nhận hoặc đổi trước khi nộp. Chưa đo thực tế, không có số liệu giả.

## 1. Sản phẩm cuối cùng cam kết

| # | Sản phẩm | Nguồn | Tiêu chí hoàn thành (đo được) |
|---|---|---|---|
| S1 | Đăng nhập JWT, đổi mật khẩu lần đầu, quên mật khẩu bằng OTP | F-01, F-21 | Luồng chạy trên môi trường triển khai; e2e đạt |
| S2 | Ngân hàng câu hỏi, vòng đời một chiều đến `FINAL_APPROVED` | F-02 | Test: CAT không bao giờ chọn câu khác `FINAL_APPROVED` |
| S3 | CAT Engine: Rasch 1PL, EAP 41 điểm, Top-5 b-matching, điều kiện dừng | F-03 | ≥3 ca bắt buộc (toàn đúng, toàn sai, xen kẽ) đạt |
| S4 | Phiên thi Dual-Write (Redis + PostgreSQL), máy trạng thái chống race | F-04 | Khôi phục phiên từ PostgreSQL trong ≤7200 giây |
| S5 | AI Tutor Explainer (Gemini) | F-05 | 100% câu `FINAL_APPROVED` có giải thích |
| S6 | Language Profile JSON v1 và API | F-06, F-07 | Phản hồi đúng schema v1 |
| S7 | Dashboard kết quả sinh viên; báo cáo lớp cho giảng viên (lọc theo kỳ, xuất CSV) | F-08, F-09 | Màn hình chạy được, CSV mở được |
| S8 | Tài khoản SV/GV (tạo lẻ, import), kỳ thi, import danh sách thi | F-18 đến F-20, F-22 | ⚠ **mới v3.0, chờ GVHD xác nhận** (Q-11) |
| S9 | Tạo lô câu hỏi bằng AI hoặc import, AI kiểm C1/C2/C3, giao việc, GV A duyệt, GV B xác nhận, Admin import | F-23 đến F-28 | ⚠ **mới v3.0, chờ GVHD xác nhận** (Q-11) |
| S10 | Triển khai (CI/CD, Docker, Nginx), tài liệu SRS/SDD, bộ test | — | Link môi trường, lịch sử pipeline |

Hạng mục tùy chọn (làm nếu đủ thời gian): ghi bất đồng bộ qua BullMQ và email nhắc việc; F-10 gán topic_tag bằng AI.

## 2. Bộ metric đánh giá

| # | Metric | Cách đo | Mục tiêu | Nguồn mục tiêu |
|---|---|---|---|---|
| M1 | Số câu trung bình đến khi dừng | Log `items_administered` | ≤ 25 và trong khoảng 20–25 câu; trung bình mục tiêu **≤ 22** | Giới hạn 25 và 20–25 theo SRS; con số 22 **[ĐỀ XUẤT]** |
| M2 | Tỉ lệ phiên dừng do SE < 0,35 (trước khi chạm 25 câu) | Thống kê `stopping_reason` | **≥ 70%** | **[ĐỀ XUẤT]**, chốt sau Pre-test |
| M3 | Thời gian làm bài trung bình | `test_duration_seconds` | **≤ 20 phút** (trần 45 phút) | Trần theo SRS; 20 phút **[ĐỀ XUẤT]** |
| M4 | Độ trễ API submit và lấy câu tiếp | APM hoặc log | **< 300 ms p95** | SRS 15.1 |
| M5 | Thời gian tính EAP | Đo trong tiến trình | **< 50 ms** | SRS 15.1 |
| M6 | Độ trễ lấy Profile | APM hoặc log | **< 500 ms p95** | SRS 15.1 |
| M7 | Độ phủ test module `cat-engine` | Báo cáo coverage | **≥ 70%** | Ngưỡng Mức 5 của rubric (**[ĐỀ XUẤT]** chọn Mức 5) |
| M8 | Độ phủ test toàn backend | Báo cáo coverage | **≥ 50%** | **[ĐỀ XUẤT]** |
| M9 | Tỉ lệ ca test CAT bắt buộc đạt | CI | **3/3** (toàn đúng, toàn sai, xen kẽ) | SRS 4.3 |
| M10 | Độ sẵn sàng giờ thi | Giám sát | **≥ 99%** | SRS 15.2 |
| M11 | Pre-test tuyến tính (hiệu chỉnh độ khó) | Số SV tham gia | **≥ 60 SV** | Lộ trình rubric Tuần 7–8 |
| M12 | Tỉ lệ câu `FINAL_APPROVED` có giải thích | Query DB | **100%** | SRS F-05 |
| M13 | Tỉ lệ P0 hoàn thành | Đếm F-ID P0 đạt tiêu chí | **100% P0** thuộc phạm vi đã chốt | **[ĐỀ XUẤT]** |
| M14 | Lỗi nghiêm trọng còn mở khi nộp | Danh sách defect | **0** | **[ĐỀ XUẤT]** |
| M15 | Giải thích được code do AI sinh khi hội đồng hỏi | Vấn đáp ngẫu nhiên ≥5 vị trí | **100%** | Rubric Mức 5 (AI Usage Log) |

Tham chiếu RQ1 (chưa cam kết số): độ chính xác CAT so với Linear. **Cần chốt** có cam kết một chỉ số tương quan hay không (ví dụ so θ của CAT với điểm Linear), và ngưỡng.

## 3. Điều kiện và giả định

- Các chỉ số M2, M3 chỉ đo được sau khi có dữ liệu Pre-test và hiệu chỉnh IRT (Tuần 9–10); con số có thể điều chỉnh nếu có dữ liệu mới, nhưng phải có xác nhận GVHD.
- S8 và S9 làm tăng phạm vi so với bản ban đầu. Nếu GVHD không xác nhận thì giảm khối lượng, ghi rõ lý do.

## 4. Phân công và khối lượng

| Thành viên | Module chính | % khối lượng |
|---|---|---|
| Phương | (điền) | (điền) |
| Đăng | (điền) | (điền) |

(Bảng phân công chi tiết nộp riêng ngày 30/11.)

## 5. Xác nhận

- Sinh viên: ____________ Ngày: ______
- GVHD: ____________ Ngày: ______
