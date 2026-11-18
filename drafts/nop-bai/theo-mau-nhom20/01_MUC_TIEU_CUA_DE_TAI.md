# MỤC TIÊU CỦA ĐỀ TÀI

**Đề tài:** Kiến trúc hệ thống chẩn đoán năng lực ngôn ngữ toàn diện (Placement Test) tích hợp AI tự thích ứng
**Hạn nộp:** 16:44 thứ Sáu 20/11/2026 · **Cần GVHD xác nhận**
**Trạng thái:** BẢN NHÁP, viết theo cấu trúc phần mở đầu của mẫu Nhom20_FinalProject. Nguồn: SRS v3.0 Mục I, II, XIII.

## 1. LÝ DO CHỌN ĐỀ TÀI

Sinh viên năm nhất ở các trường Cao đẳng và Đại học hiện làm bài kiểm tra xếp lớp tiếng Anh (Placement Test) bằng bộ đề cố định gồm 40–50 câu. Cách làm này có ba hạn chế. Thứ nhất, bài kiểm tra kém chính xác và tốn thời gian: sinh viên khá mất thời gian ở các câu dễ, sinh viên yếu nản lòng trước các câu quá khó. Thứ hai, kết quả chỉ là một con số điểm, không cho biết sinh viên yếu cụ thể ở đâu, chẳng hạn thì quá khứ hay từ vựng học thuật. Thứ ba, kết quả không phải là dữ liệu có cấu trúc nên hệ thống học tập EduZ không thể dùng để cá nhân hóa lộ trình học.

Kiểm tra thích ứng trên máy tính (Computerized Adaptive Testing, CAT) dựa trên lý thuyết ứng đáp câu hỏi (IRT) là hướng giải quyết đã được kiểm chứng: mỗi câu hỏi được chọn theo năng lực ước lượng hiện tại của người làm bài, nhờ đó cần ít câu hơn để đạt cùng độ tin cậy. Tuy vậy, một hệ thống CAT dùng được trong thực tế còn đòi hỏi ngân hàng câu hỏi có chất lượng kiểm soát, phiên thi không mất dữ liệu khi gián đoạn, và đầu ra đủ chuẩn hóa để hệ thống khác sử dụng. Xuất phát từ bối cảnh đó, đề tài được thực hiện nhằm xây dựng một microservice chẩn đoán năng lực ngôn ngữ bằng CAT mô hình Rasch, kết hợp AI giải thích kết quả, và xuất hồ sơ năng lực (Language Competency Profile) dạng JSON cho EduZ.

## 2. MỤC TIÊU NGHIÊN CỨU

**Mục tiêu chính.** Xây dựng microservice kiểm tra xếp lớp tiếng Anh thích ứng (CAT, mô hình IRT Rasch 1PL) kèm AI giải thích, ước lượng năng lực người học trên thang CEFR trong 20–25 câu thay cho 40–50 câu cố định, và xuất Language Competency Profile (JSON) chuẩn hóa cho EduZ. Phạm vi kỹ năng của Tiểu luận là Vocabulary và Grammar.

**Mục tiêu cụ thể.** Mỗi mục tiêu gắn với một cách kiểm chứng để có thể đo được:

1. **Chẩn đoán năng lực bằng CAT-Rasch**, nghĩa là ước lượng năng lực θ bằng EAP trên lưới 41 điểm, chọn câu theo Randomized Top-5 b-matching và dừng khi sai số chuẩn SE < 0,35 hoặc đủ 25 câu. *Kiểm chứng:* chạy bộ kiểm thử tự động và ghi `test_metadata` của từng phiên.
2. **Rút ngắn bài kiểm tra** so với đề cố định 40–50 câu. *Kiểm chứng:* số câu trung bình mỗi phiên (`items_administered`).
3. **Giải thích đúng/sai bằng AI** sau bài thi, giải thích được sinh cùng lúc sinh câu hỏi và dùng chung cho mọi sinh viên. *Kiểm chứng:* mọi câu `FINAL_APPROVED` đều có bản ghi trong bảng `explanations`.
4. **Xuất hồ sơ năng lực chuẩn hóa** qua API cho EduZ. *Kiểm chứng:* gọi `GET /api/v1/placement-profiles/{student_id}` và đối chiếu schema v1.
5. **Kiểm soát chất lượng ngân hàng câu hỏi**, nghĩa là câu chỉ vào ngân hàng sau khi AI kiểm tra và hai giảng viên (vai A, vai B) duyệt, rồi Admin import. *Kiểm chứng:* mọi câu CAT chọn đều có trạng thái `FINAL_APPROVED`, kiểm bằng test ở tầng Repository.
6. **Vận hành tin cậy trong giờ thi**, nghĩa là độ trễ thấp, sẵn sàng cao và khôi phục được phiên bị gián đoạn. *Kiểm chứng:* các chỉ số độ trễ, uptime, khôi phục phiên trong bản cam kết metric.

**Câu hỏi nghiên cứu.**
- RQ1: CAT-Rasch có đạt độ chính xác tương đương bài Linear dài gấp đôi không?
- RQ2: AI Explainer có cải thiện trải nghiệm và nhận thức của sinh viên về điểm yếu của mình không?
- RQ3: Language Profile JSON có đủ thông tin để EduZ cá nhân hóa lộ trình không?

> ⚠ Việc trả lời thực nghiệm RQ1, RQ2 phụ thuộc dữ liệu Linear Pre-test và User Study. SRS hiện xếp User Study 50–100 sinh viên ở Khóa luận. **Cần chốt với GVHD** mức độ Tiểu luận trả lời các câu hỏi này.

## 3. TÍNH THỰC TIỄN VÀ TÍNH MỚI

**Tính thực tiễn:** giải quyết nhu cầu xếp lớp tiếng Anh đầu vào của sinh viên năm nhất (50–500 người mỗi đợt), giảm thời gian làm bài, cung cấp thông tin điểm yếu cho giảng viên qua báo cáo lớp và cho EduZ qua API.

**Tính mới:** (1) kết hợp CAT-Rasch và LLM Explainer trong một hệ thống; (2) schema Language Profile JSON chuẩn hóa, có thể chia sẻ giữa các hệ thống; (3) mẫu ghi kép Dual-Write (Redis và PostgreSQL) để phiên CAT không mất dữ liệu; (4) ngữ cảnh ứng dụng CEFR A1–B1 cho sinh viên cao đẳng năm nhất ở Việt Nam; (5) quy trình AI sinh câu hỏi rồi chuyên gia duyệt hai vòng.

## 4. PHƯƠNG PHÁP THỰC HIỆN

- **Mô hình hóa:** IRT Rasch 1PL, ước lượng EAP bằng tích phân số trên lưới đều 41 điểm θ ∈ [−4, +4].
- **Hiệu chỉnh độ khó:** Linear Pre-test với ít nhất 60 sinh viên, sau đó hiệu chỉnh IRT ngoại tuyến (py-irt hoặc catR) bằng dịch vụ riêng, không chạy trong luồng xử lý yêu cầu.
- **Kiến trúc:** NestJS (Clean Architecture), Next.js, PostgreSQL, Redis, BullMQ, Gemini qua LLM Gateway, Nginx.
- **Bảo đảm chất lượng:** kiểm thử tự động cho CAT Engine với ít nhất 3 ca bắt buộc (toàn đúng, toàn sai, xen kẽ), đo độ phủ, CI/CD và nhật ký sử dụng AI đối chiếu được với lịch sử Git.

## 5. KẾT QUẢ DỰ KIẾN

Một hệ thống chạy được trên môi trường triển khai, gồm CAT Engine, ngân hàng câu hỏi có vòng đời kiểm soát, AI giải thích, Language Profile JSON và API, giao diện cho sinh viên, giảng viên và Admin; kèm bộ metric đo được (xem bản cam kết sản phẩm) và tài liệu SRS, thiết kế, kiểm thử.

## 6. NGOÀI MỤC TIÊU (THUỘC KHÓA LUẬN)

Kỹ năng Writing, đa trường, SSO EduZ, kiểm soát lộ đề Sympson-Hetter, webhook EduZ, Language Profile v2.
