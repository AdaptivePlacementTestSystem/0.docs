# PHẠM VI THỰC HIỆN CỦA ĐỀ TÀI

**Đề tài:** Kiến trúc hệ thống chẩn đoán năng lực ngôn ngữ toàn diện (Placement Test) tích hợp AI tự thích ứng
**Hạn nộp:** 16:46 thứ Sáu 27/11/2026 · **Cần GVHD xác nhận**
**Trạng thái:** BẢN NHÁP, viết theo mục "Đối tượng và phạm vi nghiên cứu" của mẫu Nhom20_FinalProject. Phạm vi phải khớp với mục tiêu và bản cam kết. Nguồn: SRS v3.0 Mục I, IX, IXb, XII, XVI.

## 1. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU

**Đối tượng nghiên cứu:** quy trình chẩn đoán năng lực tiếng Anh thích ứng (CAT dựa trên IRT Rasch), kỹ thuật xây dựng và kiểm soát chất lượng ngân hàng câu hỏi có hỗ trợ AI, và hồ sơ năng lực chuẩn hóa cho hệ thống học tập.

**Phạm vi hệ thống:** hệ thống đơn trường, ba vai trò (Sinh viên, Giảng viên, Admin) và một tác nhân máy (EduZ, gọi API bằng API Key, không có giao diện). Quy mô sinh viên 50–500 người mỗi đợt; giảng viên và Admin 5–20 người.

**Phạm vi kỹ năng:** Vocabulary và Grammar, thang CEFR (chủ yếu A1–B1).

**Phạm vi môi trường:** môi trường staging một instance trên máy chủ 2 GB RAM dùng chung (Quyết định #123); mục tiêu 100 người dùng đồng thời là mức production, không kiểm chứng đầy đủ trên staging.

## 2. TRONG PHẠM VI

| Nhóm | Chức năng (mã) | Ưu tiên | Trạng thái xác nhận |
|---|---|---|---|
| Lõi chẩn đoán | CAT Engine: Rasch 1PL, EAP 41 điểm, Top-5 b-matching, điều kiện dừng (F-03); phiên thi Dual-Write (F-04) | P0 | Đã chốt |
| Định danh | Đăng nhập JWT, phân quyền 3 vai trò (F-01); đổi và quên mật khẩu bằng OTP (F-21) | P0 | F-01 đã chốt; F-21 mới v3.0 |
| Ngân hàng câu hỏi | Vòng đời một chiều đến `FINAL_APPROVED` (F-02) | P0 | Đã chốt |
| AI giải thích | Giải thích sinh cùng lúc sinh câu hỏi, dùng chung mọi sinh viên (F-05) | P0 | Đã chốt |
| Hồ sơ năng lực | Language Profile JSON v1 và API (F-06, F-07) | P0 | Đã chốt |
| Báo cáo | Dashboard sinh viên (F-08); báo cáo lớp, lọc theo kỳ, xuất CSV (F-09) | P1 | Đã chốt |
| Người dùng và kỳ thi | Tạo và import tài khoản SV, GV (F-18, F-22); kỳ thi (F-19); import danh sách thi (F-20) | P0/P1 | ⚠ Mới v3.0, **chờ GVHD** (Q-11) |
| Sinh và duyệt đề | Tạo lô bằng AI hoặc import (F-23, F-24); giao việc và hạn (F-25); GV A duyệt (F-26); GV B xác nhận (F-27); kiểm cuối C3 và import (F-28) | P0 | ⚠ Mới v3.0, **chờ GVHD** (Q-11) |
| Tùy chọn | Gán `topic_tag` bằng AI (F-10); ghi bất đồng bộ BullMQ | P2 | Làm nếu đủ thời gian |
| Kỹ thuật và chất lượng | Docker, Nginx, CI/CD, staging, bộ kiểm thử, phân tích tĩnh, quét secret | — | Theo các mục nộp 07–08/12 |

**Ràng buộc nghiệp vụ đã chốt:** Admin không sửa nội dung câu và không soạn câu bằng form; giảng viên không import đề; GV A khác GV B; câu `FINAL_APPROVED` không được sửa; chỉ câu `FINAL_APPROVED` được CAT chọn; câu hỏi và đáp án đúng không trả về client trước khi nộp bài (SRS Mục IXb, 15.3).

## 3. NGOÀI PHẠM VI (THUỘC KHÓA LUẬN)

| Hạng mục | Mã |
|---|---|
| Kỹ năng Writing và AI Writing Assessor | F-15 |
| Đa trường (multi-tenant) | DC-19, Mục XVI |
| SSO với EduZ | — |
| Webhook đẩy Profile sang EduZ | F-14 |
| Kiểm soát lộ đề Sympson-Hetter | F-17 |
| Chống gian lận trong phiên (đổi tab, xáo thứ tự đáp án) | F-16 |
| Language Profile v2 (radar, gợi ý lộ trình) | F-13 |
| Pipeline hiệu chỉnh v2 chạy lại từ dữ liệu sử dụng thực | F-12 |
| User Study 50–100 sinh viên (CAT so với Linear) | Mục XII |
| Thông báo thời gian thực (chỉ có email và Hộp việc) | — |

## 4. TIÊU CHÍ CHẤP NHẬN PHẠM VI

- Mỗi chức năng trong phạm vi có đủ: đặc tả (SRS), use case, thiết kế (Class, Sequence), mã nguồn, kiểm thử và bằng chứng chạy trên môi trường triển khai.
- Chức năng đánh dấu ⚠ nếu không được GVHD chấp nhận thì loại khỏi bản cam kết kèm lý do.
- Thay đổi phạm vi sau khi nộp phải có xác nhận của GVHD và ghi vào `DECISIONS_LOG`.

## 5. PHƯƠNG PHÁP VÀ GIẢ ĐỊNH

- **Phương pháp:** kiến trúc Clean Architecture (NestJS), CAT-Rasch tự cài đặt bằng TypeScript cho luồng chạy thật, hiệu chỉnh độ khó ngoại tuyến bằng py-irt hoặc catR (Docker sidecar), kiểm thử tự động và đo độ phủ.
- **Giả định:** tham số CAT nằm trong cấu hình và có thể đổi sau hiệu chỉnh; nguồn câu hỏi và bản quyền ngân hàng tham chiếu còn mở (Q-8); mô hình embedding chưa chốt (Q-9).

## 6. RỦI RO VỀ PHẠM VI

| Rủi ro | Hướng xử lý |
|---|---|
| Phạm vi tăng ở v3.0 (F-18 đến F-28) vượt khả năng 2 người | GVHD xác nhận trước khi ký; nếu thiếu thời gian thì giữ P0 lõi, hạ F-22, F-10 |
| Mã nguồn đang chuyển sang mô hình duyệt từng câu | Hoàn tất áp quyết định #133 trước khi mở rộng |
| Chưa có dữ liệu Pre-test | Lập kế hoạch tuyển ≥ 60 sinh viên; nếu chưa có thì M2, M3 chỉ báo cáo mô phỏng |

## 7. XÁC NHẬN

- Sinh viên: ____________ Ngày: ______
- Giảng viên hướng dẫn: ____________ Ngày: ______
