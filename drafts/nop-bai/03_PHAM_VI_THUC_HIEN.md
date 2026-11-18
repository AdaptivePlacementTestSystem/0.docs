# Phạm vi thực hiện của đề tài

> **Hạn nộp:** 16:46 thứ Sáu 27/11/2026 · **Cần GVHD xác nhận** · Tiêu chí: Phân tích nghiệp vụ, đặc tả yêu cầu và thiết kế – giải pháp
> **Trạng thái:** BẢN NHÁP. Phạm vi này là cơ sở đánh giá, phải khớp với mục tiêu (file 01) và cam kết (file 02). Nguồn: SRS v3.0 Mục I, IX, IXb, XII, XVI.

## 1. Đối tượng và bối cảnh

Hệ thống đơn trường. Người dùng: Sinh viên (50–500 người/đợt), Giảng viên và Admin (5–20 người), và EduZ (máy gọi máy qua API Key, không có giao diện).

## 2. Trong phạm vi (Tiểu luận)

| Nhóm | Chức năng (F-ID) | Ưu tiên | Trạng thái xác nhận |
|---|---|---|---|
| Lõi chẩn đoán | CAT Engine Rasch 1PL, EAP 41 điểm, Top-5 b-matching, điều kiện dừng (F-03); phiên thi Dual-Write (F-04) | P0 | Đã chốt |
| Định danh | Đăng nhập JWT, phân quyền 3 vai trò (F-01); đổi/quên mật khẩu OTP (F-21) | P0 | F-01 đã chốt; F-21 mới v3.0 |
| Ngân hàng câu hỏi | Vòng đời một chiều đến `FINAL_APPROVED` (F-02) | P0 | Đã chốt |
| AI giải thích | Giải thích sinh cùng lúc sinh câu hỏi, dùng chung mọi SV (F-05) | P0 | Đã chốt |
| Hồ sơ năng lực | Language Profile JSON v1 và API (F-06, F-07) | P0 | Đã chốt |
| Báo cáo | Dashboard sinh viên (F-08); báo cáo lớp, lọc theo kỳ, xuất CSV (F-09) | P1 | Đã chốt |
| Người dùng và kỳ thi | Tạo/import tài khoản SV, GV (F-18, F-22); kỳ thi (F-19); import danh sách thi (F-20) | P0/P1 | ⚠ **Mới v3.0, chờ GVHD** (Q-11) |
| Sinh và duyệt đề | Tạo lô bằng AI hoặc import (F-23, F-24); giao việc và hạn (F-25); GV A duyệt (F-26); GV B xác nhận (F-27); kiểm cuối C3 và import (F-28) | P0 | ⚠ **Mới v3.0, chờ GVHD** (Q-11) |
| Tùy chọn | Gán `topic_tag` bằng AI (F-10); ghi bất đồng bộ BullMQ | P2 | Làm nếu đủ thời gian |
| Kỹ thuật và chất lượng | Docker, Nginx, CI/CD, môi trường staging, bộ test, phân tích tĩnh, quét secret | — | Theo các mục nộp 07–08/12 |

Ràng buộc nghiệp vụ chính đã chốt: Admin không sửa nội dung câu và không gõ câu bằng form; giảng viên không import đề; GV A khác GV B; câu `FINAL_APPROVED` cấm sửa; chỉ `FINAL_APPROVED` được CAT chọn; câu hỏi và đáp án đúng không trả về client trước khi nộp bài. Chi tiết: SRS Mục IXb.

## 3. Ngoài phạm vi (thuộc Khóa luận, không code ở Tiểu luận)

| Hạng mục | F-ID |
|---|---|
| Kỹ năng Writing và AI Writing Assessor | F-15 |
| Đa trường (multi-tenant) | DC-19, Mục XVI |
| SSO EduZ | — |
| Webhook đẩy Profile sang EduZ | F-14 |
| Kiểm soát lộ đề Sympson-Hetter | F-17 |
| Chống gian lận trong phiên (đổi tab, xáo thứ tự đáp án) | F-16 |
| Language Profile v2 (radar, gợi ý lộ trình) | F-13 |
| Pipeline calibration v2 chạy lại từ dữ liệu sử dụng thực | F-12 |
| User Study 50–100 SV (CAT so với Linear) | Mục XII |
| Chuông thông báo thời gian thực (chỉ có email và Hộp việc) | — |

## 4. Tiêu chí chấp nhận phạm vi

- Mỗi F-ID trong phạm vi có: đặc tả (SRS), use case, thiết kế (Class/Sequence), mã, test, và bằng chứng chạy trên môi trường triển khai.
- Chức năng chưa có xác nhận GVHD (hàng ⚠) nếu bị bác thì loại khỏi cam kết ở file 02 và ghi lý do.
- Mọi thay đổi phạm vi sau khi nộp phải có xác nhận của GVHD và ghi vào `DECISIONS_LOG`.

## 5. Điều kiện ràng buộc

- 2 thành viên, 12 tuần. Môi trường staging 1 instance, server 2 GB RAM dùng chung (Quyết định #123).
- Nguồn câu hỏi và bản quyền ngân hàng tham chiếu còn mở (Q-8); mô hình embedding chưa chốt (Q-9).
- Giả định kỹ thuật: tham số CAT (θ₀ = −0,5; SE 0,35; tối đa 25 câu; tối thiểu 8 câu trước Early Stop) đặt trong cấu hình và có thể đổi sau khi calibration.

## 6. Rủi ro phạm vi

| Rủi ro | Hướng xử lý |
|---|---|
| Phạm vi tăng ở v3.0 (F-18 đến F-28) vượt khả năng 2 người | GVHD xác nhận trước khi ký; nếu không đủ thời gian thì giữ P0 lõi, hạ F-22/F-10 |
| Mã backend và frontend đang chuyển theo mô hình duyệt từng câu | Hoàn tất áp quyết định #133 trước khi mở rộng |
| Dữ liệu Pre-test chưa có | Lập kế hoạch tuyển ≥60 SV; chưa có thì M2, M3 chỉ báo cáo mô phỏng |

## 7. Xác nhận

- Sinh viên: ____________ Ngày: ______
- GVHD: ____________ Ngày: ______
