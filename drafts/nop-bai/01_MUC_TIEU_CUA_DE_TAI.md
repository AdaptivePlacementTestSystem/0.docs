# Mục tiêu của đề tài

> **Hạn nộp:** 16:44 thứ Sáu 20/11/2026 · **Cần GVHD xác nhận** · Tiêu chí: Tính thực tiễn của đề tài và sự hiểu biết về vấn đề nghiên cứu
> **Trạng thái:** BẢN NHÁP, chưa chốt. Nguồn: SRS v3.0 Mục I, II, XIII.

## 1. Tên đề tài

Kiến trúc hệ thống chẩn đoán năng lực ngôn ngữ toàn diện (Placement Test) tích hợp AI tự thích ứng.

## 2. Vấn đề thực tiễn

Sinh viên năm nhất ở các trường Cao đẳng/Đại học hiện làm Placement Test bằng **bộ đề cố định** (40–50 câu). Có ba hạn chế:

1. **Kém chính xác và tốn thời gian:** sinh viên khá mất thời gian ở câu dễ, sinh viên yếu nản vì câu khó.
2. **Kết quả chỉ là một con số điểm:** không cho biết sinh viên yếu cụ thể ở đâu (ví dụ thì quá khứ, từ vựng học thuật).
3. **Không có dữ liệu có cấu trúc** để hệ thống học tập (EduZ) cá nhân hóa lộ trình.

## 3. Mục tiêu chính

> Xây dựng một **microservice kiểm tra xếp lớp tiếng Anh thích ứng** (CAT dùng mô hình IRT Rasch 1PL) kèm AI giải thích, ước lượng năng lực người học trên thang CEFR trong **20–25 câu** thay cho 40–50 câu cố định, và xuất **Language Competency Profile (JSON)** chuẩn hóa để EduZ sử dụng.

Phạm vi kỹ năng của Tiểu luận: **Vocabulary và Grammar**. Hệ thống đơn trường, 3 vai trò (Sinh viên, Giảng viên, Admin).

## 4. Mục tiêu cụ thể (mỗi mục gắn một cách kiểm chứng)

| # | Mục tiêu cụ thể | Cách kiểm chứng |
|---|---|---|
| MT1 | Chẩn đoán năng lực bằng CAT-Rasch: ước lượng θ bằng EAP (lưới 41 điểm), chọn câu bằng Randomized Top-5 b-matching, dừng khi SE < 0,35 hoặc đủ 25 câu | Chạy test tự động, log `test_metadata` mỗi phiên |
| MT2 | Rút ngắn bài kiểm tra so với đề cố định 40–50 câu | Số câu trung bình mỗi phiên (`items_administered`) |
| MT3 | Giải thích đúng/sai bằng AI sau bài thi, dùng chung cho mọi sinh viên | Mọi câu `FINAL_APPROVED` đều có giải thích trong bảng `explanations` |
| MT4 | Xuất Language Profile JSON chuẩn hóa qua API cho EduZ | Gọi `GET /api/v1/placement-profiles/{student_id}` và so với schema v1 |
| MT5 | Bảo đảm chất lượng ngân hàng câu hỏi: câu chỉ vào ngân hàng sau khi AI kiểm và GV A, GV B duyệt hai vòng, Admin import | Mọi câu CAT chọn có `status = FINAL_APPROVED` (test ở tầng Repository) |
| MT6 | Vận hành tin cậy cho giờ thi | Độ trễ API, uptime, khôi phục phiên (chỉ số ở file cam kết) |

## 5. Câu hỏi nghiên cứu (SRS Mục XIII)

- **RQ1:** CAT-Rasch có đạt độ chính xác tương đương bài Linear dài gấp đôi không?
- **RQ2:** AI Explainer có cải thiện trải nghiệm và nhận thức của sinh viên về điểm yếu không?
- **RQ3:** Language Profile JSON có đủ thông tin để EduZ cá nhân hóa lộ trình không?

> ⚠ Phần trả lời thực nghiệm RQ1/RQ2 phụ thuộc dữ liệu Linear Pre-test và User Study; phạm vi User Study 50–100 SV hiện ghi ở Khóa luận (SRS Mục XII). **Cần chốt với GVHD** Tiểu luận trả lời đến mức nào.

## 6. Tính mới (SRS Mục XIII)

CAT-Rasch kết hợp LLM Explainer trong một hệ thống; Language Profile JSON chuẩn hóa; mẫu Dual-Write cho độ tin cậy phiên CAT; CEFR A1–B1 cho sinh viên cao đẳng năm nhất Việt Nam; quy trình AI sinh câu hỏi rồi chuyên gia duyệt.

## 7. Ngoài mục tiêu (thuộc Khóa luận)

Writing, đa trường, SSO EduZ, kiểm soát lộ đề Sympson-Hetter, webhook EduZ, Profile v2.
