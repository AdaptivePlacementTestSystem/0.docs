CHƯƠNG 2: MÔ HÌNH HÓA YÊU CẦU

Hệ thống Chẩn đoán Năng lực Ngôn ngữ Toàn diện (Adaptive Placement Test)

Đặc tả Use Case Chi tiết & Lược đồ Ca sử dụng — Phiên bản v3.1
Ngày cập nhật: 22/11/2026

2.1. Tổng quan Mô hình Hóa Yêu Cầu

Chương này trình bày mô hình hóa yêu cầu chức năng của hệ thống Adaptive Placement Test (phiên bản v3.1 — đồng bộ Class Diagram 03/11/2026), bao gồm:

1. Xác định 3 tác nhân người dùng chính (Student, Teacher, Admin) theo mô hình hệ thống đơn trường (Single-tenant, DC-19) và 1 tác nhân hệ thống ngoài (EduZ System M2M qua API Key).

2. Danh mục Use Case toàn diện phản ánh các quy trình nghiệp vụ mới: Kỳ thi (ExamRound), Nhập danh sách dự thi và tài khoản theo cơ chế lưới tạm (Import Grid), Đăng nhập email/mật khẩu, Đổi/Quên mật khẩu OTP, cùng quy trình Sinh đề và Duyệt đề hai chặng qua AI (GV vai A duyệt/sửa và GV vai B confirm).

3. Bảng đặc tả chi tiết cho từng Use Case theo mẫu chuẩn kỹ thuật phần mềm, tích hợp đầy đủ Quy tắc nghiệp vụ (Business Rules BR-01..BR-30) và Tiêu chí chấp nhận (Acceptance Criteria dạng Given/When/Then) đáp ứng yêu cầu đánh giá TC2.1.

4. Phân tích các mối quan hệ Use Case Diagram (<<extend>>, <<include>>, và kế thừa nghiệp vụ).

2.2. Mô tả Tác nhân (Actors)

2.2.1. Sinh viên (Student)

Sinh viên năm nhất tham gia làm bài thi Placement Test. Tài khoản của sinh viên do Quản trị viên (Admin) tạo trên hệ thống (tạo từng người hoặc import qua file Excel). Sinh viên đăng nhập bằng Email và mật khẩu tạm, bắt buộc đổi mật khẩu ở lần đăng nhập đầu tiên. Sinh viên chỉ được làm bài thi khi thuộc danh sách của một kỳ thi đang mở (OPEN). Sau khi hoàn thành bài thi hoặc hết hạn phiên thi, sinh viên xem kết quả chẩn đoán CEFR, phân tích năng lực chi tiết và lời giải thích AI.

2.2.2. Giảng viên (Teacher)

Giảng viên phụ trách môn học tại trường. Tài khoản do Admin cấp phát. Giảng viên có quyền xem báo cáo tổng hợp lớp học (lọc theo kỳ thi) và tra cứu hồ sơ năng lực của sinh viên. Trong quy trình kiểm duyệt câu hỏi theo lô do Admin giao việc, Giảng viên đảm nhận một trong hai vai trò chuyên môn độc lập:

- Giảng viên vai A: Nhận phân bổ danh sách câu hỏi cần duyệt (được chia đều theo kỹ năng và trình độ), có quyền chỉnh sửa nội dung/đáp án/giải thích câu hỏi, duyệt (FIRST_APPROVED) hoặc từ chối (REJECTED) từng câu. Thông tin duyệt, nhận xét, thời hạn và snapshot bản gốc (nếu có chỉnh sửa) được lưu trực tiếp vào câu hỏi (`firstReview`).

- Giảng viên vai B (Đại diện/Trưởng bộ môn, B không thuộc nhóm A): Nhận danh sách các câu hỏi do GV A đã duyệt đạt (`FIRST_APPROVED`), xem xét ở chế độ chỉ đọc (đối chiếu bản gốc và bản sửa của A qua component C-DIFF), thực hiện Xác nhận (SECOND_APPROVED) hoặc Loại bỏ (REJECTED) từng câu, hoặc sử dụng chức năng 'Xác nhận tất cả câu còn lại được giao'. GV B không sửa nội dung và không trả về GV A.

2.2.3. Quản trị viên (Admin)

Quản trị viên của trường (hệ thống đơn trường). Kế thừa toàn bộ quyền xem báo cáo của Giảng viên và nắm toàn quyền quản trị vận hành hệ thống:

- Quản lý tài khoản: Tạo từng tài khoản SV/GV hoặc import hàng loạt qua file Excel theo lưới tạm (Redis), khóa/mở khóa tài khoản, gửi lại mật khẩu tạm, nâng/thu hồi quyền Admin.

- Quản lý kỳ thi: Tạo kỳ thi, cấu hình thời gian mở/đóng và thời lượng làm bài, import danh sách thí sinh dự thi theo lưới tạm, công bố và theo dõi tiến độ dự thi.

- Quản lý câu hỏi: Tạo lô câu hỏi bằng AI hoặc import file Excel (lưới tạm), giao việc duyệt đề cho nhóm GV A và GV B, theo dõi tiến độ lô, xử lý cảnh báo quá hạn, chạy kiểm tra AI lần 3 (C3), quyết định xử lý câu hỏi cờ mềm, và thực hiện Import cuối cùng vào ngân hàng câu hỏi (FINAL_APPROVED). Admin không trực tiếp sửa hay duyệt nội dung câu hỏi.

2.2.4. Hệ thống ngoài EduZ (EduZ System)

Tác nhân máy (M2M) kết nối thông qua REST API độc lập. EduZ xác thực qua API Key tĩnh cấu hình trước (role EDUZ_SERVICE), chỉ có quyền GET dữ liệu hồ sơ năng lực sinh viên (Placement Profile) định dạng JSON chuẩn hóa để đưa vào Lộ trình học tập (Learning Path Engine), không có giao diện người dùng.

2.3. Danh sách Use Case theo Actor

2.4. Bảng Đặc tả Chi tiết từng Use Case

Mỗi Use Case được đặc tả theo cấu trúc chuẩn gồm 11 mục thông tin: Mã, Tên chức năng, Mô tả, Tác nhân, Điều kiện trước, Điều kiện sau, Luồng chính, Luồng thay thế, Luồng ngoại lệ, Quy tắc nghiệp vụ liên quan (BR), và Tiêu chí chấp nhận (Acceptance Criteria dạng Given/When/Then).

Bảng đặc tả Use Case: Đăng nhập hệ thống (UCSV01)

Bảng đặc tả Use Case: Bắt đầu bài thi Placement Test (UCSV02)

Bảng đặc tả Use Case: Làm bài thi (nhận câu hỏi và nộp đáp án) (UCSV03)

Bảng đặc tả Use Case: Đổi mật khẩu (UCSV08)

Bảng đặc tả Use Case: Quên mật khẩu (OTP qua email) (UCSV09)

Bảng đặc tả Use Case: Duyệt và gửi gói câu hỏi (GV vai A) (UCGV14)

Bảng đặc tả Use Case: Xác nhận gói câu hỏi (GV vai B) (UCGV15)

Bảng đặc tả Use Case: Import tài khoản người dùng (SV và GV) (UCADM08)

Bảng đặc tả Use Case: Quản lý tài khoản người dùng (UCADM09)

Bảng đặc tả Use Case: Quản lý kỳ thi (Exam Round) (UCADM15)

Bảng đặc tả Use Case: Import danh sách sinh viên thi (UCADM16)

Bảng đặc tả Use Case: Theo dõi dự thi của kỳ thi (UCADM17)

Bảng đặc tả Use Case: Tạo lô câu hỏi bằng AI (UCADM11)

Bảng đặc tả Use Case: Import đề thi từ file Excel (UCADM12)

Bảng đặc tả Use Case: Giao việc duyệt câu hỏi và theo dõi lô (UCADM13)

Bảng đặc tả Use Case: Kiểm tra C3 và Import vào ngân hàng (UCADM14)

Bảng đặc tả Use Case: Xem kết quả bài thi (UCSV04)

Bảng đặc tả Use Case: Xem giải thích AI (AI Explainer) (UCSV05)

Bảng đặc tả Use Case: Xem lịch sử bài thi (UCSV06)

Bảng đặc tả Use Case: Tiếp tục bài thi bị gián đoạn (UCSV07)

Bảng đặc tả Use Case: Đăng nhập hệ thống (Giảng viên) (UCGV01)

Bảng đặc tả Use Case: Xem danh sách câu hỏi (Item Bank) (UCGV02)

Bảng đặc tả Use Case: Chỉnh sửa câu hỏi (UCGV04)

Bảng đặc tả Use Case: Xem báo cáo lớp học (UCGV07)

Bảng đặc tả Use Case: Xuất báo cáo CSV (UCGV08)

Bảng đặc tả Use Case: Xem hồ sơ năng lực sinh viên (UCGV09)

Bảng đặc tả Use Case: Đăng nhập hệ thống (Quản trị viên) (UCADM01)

Bảng đặc tả Use Case: Xem hồ sơ năng lực sinh viên (Quản trị viên) (UCADM04)

Bảng đặc tả Use Case: Xem báo cáo tổng thể toàn trường (UCADM05)

Bảng đặc tả Use Case: Quản lý toàn bộ ngân hàng câu hỏi (UCADM06)

2.5. Phân tích Các Mối quan hệ Use Case

2.5.1. Quan hệ Mở rộng (<<extend>>)

1. UCSV05 (Xem giải thích AI) <<extend>> UCSV04 (Xem kết quả bài thi): Sinh viên sau khi xem điểm chẩn đoán có thể chủ động bấm xem giải thích chi tiết đúng/sai cho từng câu hỏi.

2. UCGV08 (Xuất báo cáo CSV) <<extend>> UCGV07 (Xem báo cáo lớp học): Giảng viên khi xem dashboard lớp học có thể chọn xuất dữ liệu phân bố ra file CSV.

3. UCSV08 (Đổi mật khẩu) <<extend>> UCSV01 (Đăng nhập hệ thống): Kích hoạt bắt buộc khi cờ mustChangePassword = true ở lần đăng nhập đầu tiên.

4. UCSV09 (Quên mật khẩu) <<extend>> UCSV01 (Đăng nhập hệ thống): Kích hoạt khi người dùng quên mật khẩu tại màn hình đăng nhập.

2.5.2. Quan hệ Kế thừa & Bao trùm Nghiệp vụ (Generalization / Business Note)

1. Quản trị viên (Admin) kế thừa toàn bộ quyền xem báo cáo của Giảng viên (Teacher): UCADM04 bao trùm UCGV09, UCADM05 bao trùm UCGV07.

2. Quyền tổ chức kỳ thi (UCADM15, UCADM16, UCADM17) được thực hiện bởi tác nhân Quản trị viên theo quyết định kiến trúc DC-18/DC-19 (Giảng viên thường chỉ xem kết quả).

3. Quan hệ Sở hữu Tuyệt đối giữa Kỳ thi và Phiên thi (Composition: ExamRound ◆— 0..* TestSession): Một phiên thi (TestSession) sinh ra chỉ phục vụ duy nhất cho một kỳ thi cụ thể, không thể chuyển giao hay gán lại sang kỳ thi khác. CSDL áp dụng ràng buộc onDelete: Restrict khi kỳ thi đã có sinh viên làm bài.


### Bảng đặc tả / Danh mục 0

| Use Case ID | Tên Use Case | Tác nhân | Nhóm tính năng | Trạng thái v3.0 |
| --- | --- | --- | --- | --- |
| UCSV01 | Đăng nhập hệ thống | Sinh viên | Xác thực & Tài khoản | Cập nhật (bỏ SSO, luồng đổi mật khẩu lần đầu) |
| UCSV02 | Bắt đầu bài thi Placement Test | Sinh viên | Làm bài thi CAT | Cập nhật (ràng buộc kỳ thi OPEN, thuộc danh sách) |
| UCSV03 | Làm bài thi (nhận câu hỏi & nộp đáp án) | Sinh viên | Làm bài thi CAT | Cập nhật (hạn phiên theo expires_at của kỳ thi) |
| UCSV04 | Xem kết quả bài thi | Sinh viên | Kết quả & Báo cáo | Giữ nguyên |
| UCSV05 | Xem giải thích AI (AI Explainer) | Sinh viên | Kết quả & Báo cáo | Giữ nguyên (<<extend>> UCSV04, gắn theo Item) |
| UCSV06 | Xem lịch sử bài thi | Sinh viên | Kết quả & Báo cáo | Giữ nguyên |
| UCSV07 | Tiếp tục bài thi bị gián đoạn | Sinh viên | Làm bài thi CAT | Cập nhật (kiểm tra hạn expires_at còn hiệu lực) |
| UCSV08 | Đổi mật khẩu | Sinh viên, GV, Admin | Xác thực & Tài khoản | Mới v3.0 (dùng chung cho mọi vai trò) |
| UCSV09 | Quên mật khẩu (OTP qua email) | Sinh viên, GV, Admin | Xác thực & Tài khoản | Mới v3.0 (OTP 6 số qua email, Redis TTL 10m) |
| UCGV01 | Đăng nhập hệ thống | Giảng viên | Xác thực & Tài khoản | Cập nhật (Email + mật khẩu, đổi mật khẩu lần đầu) |
| UCGV02 | Xem danh sách câu hỏi (Item Bank) | Giảng viên | Ngân hàng câu hỏi | Cập nhật (chỉ xem, phục vụ chuyên môn) |
| UCGV04 | Chỉnh sửa câu hỏi | Giảng viên (vai A) | Kiểm duyệt đề thi | Cập nhật (chỉ GV vai A được sửa khi duyệt) |
| UCGV07 | Xem báo cáo lớp học | Giảng viên | Kết quả & Báo cáo | Cập nhật (bộ lọc theo kỳ thi examRoundId) |
| UCGV08 | Xuất báo cáo CSV | Giảng viên | Kết quả & Báo cáo | Cập nhật (<<extend>> UCGV07, lọc theo kỳ thi) |
| UCGV09 | Xem hồ sơ năng lực sinh viên | Giảng viên | Kết quả & Báo cáo | Cập nhật (tra cứu hồ sơ sinh viên toàn trường) |
| UCGV14 | Duyệt câu hỏi (GV vai A) | Giảng viên (vai A) | Kiểm duyệt đề thi | Cập nhật v3.1 (sửa, duyệt hoặc từ chối từng câu hỏi được giao, lưu firstReview) |
| UCGV15 | Xác nhận câu hỏi (GV vai B) | Giảng viên (vai B) | Kiểm duyệt đề thi | Cập nhật v3.1 (thẩm định, xác nhận hoặc loại bỏ từng câu hỏi đã qua vòng 1, lưu secondReview) |
| UCADM01 | Đăng nhập hệ thống | Quản trị viên | Xác thực & Tài khoản | Cập nhật (Email + mật khẩu) |
| UCADM04 | Xem hồ sơ năng lực sinh viên | Quản trị viên | Kết quả & Báo cáo | Cập nhật (đơn trường, kế thừa từ GV) |
| UCADM05 | Xem báo cáo tổng thể toàn trường | Quản trị viên | Kết quả & Báo cáo | Cập nhật (trang Tổng quan S36, F-29; lọc theo kỳ thi) |
| UCADM06 | Quản lý toàn bộ ngân hàng câu hỏi | Quản trị viên | Ngân hàng câu hỏi | Cập nhật (giám sát ngân hàng đề) |
| UCADM08 | Import tài khoản người dùng | Quản trị viên | Quản trị tài khoản | Mới v3.0 (SV & GV, cơ chế lưới tạm Redis) |
| UCADM09 | Quản lý tài khoản người dùng | Quản trị viên | Quản trị tài khoản | Mới v3.0 (tạo lẻ SV/GV, khóa, cấp lại MK, phân quyền) |
| UCADM15 | Quản lý kỳ thi (Exam Round) | Quản trị viên | Quản lý kỳ thi | Mới v3.0 (tạo, cấu hình opens/closes/duration, đóng) |
| UCADM16 | Import danh sách sinh viên thi | Quản trị viên | Quản lý kỳ thi | Mới v3.0 (lưới tạm, tra cứu MSSV hợp lệ) |
| UCADM17 | Theo dõi dự thi của kỳ thi | Quản trị viên | Quản lý kỳ thi | Mới v3.0 (giám sát trạng thái dự thi thời gian thực) |
| UCADM11 | Tạo lô câu hỏi bằng AI | Quản trị viên | Sinh & Duyệt đề AI | Mới v3.0 (sinh dư theo N, AI check C1, tạo lô) |
| UCADM12 | Import đề thi từ file Excel | Quản trị viên | Sinh & Duyệt đề AI | Mới v3.0 (lưới tạm file Excel, AI check C2, tạo lô) |
| UCADM13 | Giao việc duyệt câu hỏi và theo dõi lô | Quản trị viên | Sinh & Duyệt đề AI | Mới v3.0 (chia đều nhóm A, chỉ định B, hạn & nhắc) |
| UCADM14 | Kiểm tra C3 và Import vào ngân hàng | Quản trị viên | Sinh & Duyệt đề AI | Mới v3.0 (AI check delta C3, quyết cờ mềm, import) |
| UCADM02 | Quản lý tài khoản người dùng (cũ) | Quản trị viên | Quản trị hệ thống | Ngoài phạm vi TL (thay bởi UCADM08 & UCADM09) |
| UCADM03 | Phân quyền vai trò (cũ) | Quản trị viên | Quản trị hệ thống | Ngoài phạm vi TL (gộp vào UCADM09) |
| UCADM07 | Cấu hình thông số hệ thống | Quản trị viên | Quản trị hệ thống | Ngoài phạm vi TL (#53) |
| UCGV03 | Thêm câu hỏi thủ công | Giảng viên | Ngân hàng câu hỏi | Bỏ (DC-29, DC-32: không còn form thêm từng câu) |
| UCGV05 | Duyệt / Từ chối câu hỏi (cũ) | Giảng viên | Ngân hàng câu hỏi | Bỏ (thay bởi quy trình duyệt A/B: UCGV14, UCGV15) |
| UCGV06 | Xóa câu hỏi khỏi Item Bank | Giảng viên | Ngân hàng câu hỏi | Ngoài phạm vi TL (câu đã duyệt cấm xóa/sửa) |
| UCGV10 | Tự động gán chủ đề bằng AI (cũ) | Giảng viên | Ngân hàng câu hỏi | Ngoài phạm vi TL (tích hợp trực tiếp vào AI sinh câu) |

### Bảng đặc tả / Danh mục 1

| Use Case ID | UCSV01 |
| --- | --- |
| Tên chức năng | Đăng nhập hệ thống |
| Mô tả | Cho phép sinh viên xác thực danh tính để truy cập hệ thống Placement Test bằng Email và Mật khẩu. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã có tài khoản được cấp phát trong hệ thống (tài khoản do Admin import hoặc tạo lẻ). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Sinh viên được cấp JWT access token, chuyển đến Dashboard hoặc trang Đổi mật khẩu bắt buộc. |
| Luồng chính | 1. Sinh viên truy cập trang đăng nhập (/login).<br>2. Sinh viên nhập Email và Mật khẩu.<br>3. Hệ thống kiểm tra thông tin đăng nhập và trạng thái hoạt động (isActive) của tài khoản.<br>4. Hệ thống xác thực mật khẩu bằng thuật toán argon2.<br>5. Hệ thống kiểm tra cờ mustChangePassword.<br>6. Do mustChangePassword = false, hệ thống cấp JWT access token và refresh token.<br>7. Hệ thống chuyển sinh viên đến trang chủ Dashboard sinh viên. |
| Luồng thay thế | 5a. Tài khoản có cờ mustChangePassword = true (đăng nhập lần đầu):<br>  5a1. Hệ thống cấp JWT tạm thời chỉ có quyền truy cập đổi mật khẩu.<br>  5a2. Hệ thống chuyển hướng sinh viên sang trang Đổi mật khẩu bắt buộc (/change-password).<br>  5a3. Sinh viên thực hiện Use Case UCSV08. |
| Luồng ngoại lệ | 3a. Email không tồn tại hoặc sai mật khẩu: Hệ thống trả về lỗi 401 Unauthorized ('Email hoặc mật khẩu không chính xác').<br>3b. Tài khoản bị khóa (isActive = false): Hệ thống thông báo 'Tài khoản đã bị vô hiệu hóa, vui lòng liên hệ Quản trị viên' (HTTP 403).<br>2a. Sinh viên quên mật khẩu: Sinh viên chọn liên kết 'Quên mật khẩu' để chuyển sang Use Case UCSV09. |
| Quy tắc nghiệp vụ liên quan | BR-02 (Email duy nhất), BR-05 (authProvider=LOCAL, argon2), BR-06 (mustChangePassword), BR-19 (isActive kiểm tra đăng nhập). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên đã có tài khoản active và mật khẩu đúng When gửi yêu cầu đăng nhập Then hệ thống trả về HTTP 200 kèm JWT token và chuyển đến Dashboard.<br>- Given sinh viên đăng nhập lần đầu với mật khẩu tạm (mustChangePassword=true) When xác thực thành công Then hệ thống chuyển hướng sang /change-password và chặn mọi API nghiệp vụ khác (403 PASSWORD_CHANGE_REQUIRED).<br>- Given sinh viên nhập sai mật khẩu quá 5 lần liên tiếp When gửi yêu cầu Then hệ thống kích hoạt rate-limit tạm thời (HTTP 429). |

### Bảng đặc tả / Danh mục 2

| Use Case ID | UCSV02 |
| --- | --- |
| Tên chức năng | Bắt đầu bài thi Placement Test |
| Mô tả | Sinh viên chọn một kỳ thi đang mở mà mình được phân công để khởi tạo phiên thi thích ứng CAT. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã đăng nhập thành công, cờ mustChangePassword = false. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Một phiên thi TestSession mới được tạo ở trạng thái IN_PROGRESS, đồng bộ trạng thái ban đầu lên Redis. |
| Luồng chính | 1. Sinh viên mở danh sách kỳ thi của tôi (/exams).<br>2. Hệ thống hiển thị các kỳ thi mà sinh viên thuộc danh sách tham gia kèm trạng thái hiệu lực (effectiveStatus).<br>3. Sinh viên chọn một kỳ thi đang ở trạng thái OPEN; hệ thống chuyển sang màn hình S03 (Giới thiệu bài thi và 6 quy tắc CAT) tại /student/exams/[roundId]. Bước này chỉ hiển thị thông tin, chưa tạo phiên thi.<br>4. Sinh viên đọc phần giới thiệu và 6 quy tắc CAT rồi bấm 'Tôi đã hiểu, bắt đầu làm bài'. Chỉ khi đó giao diện mới gọi POST /api/v1/sessions và hệ thống kiểm tra điều kiện dự thi (BR-10):<br>   - Sinh viên có trong danh sách kỳ thi (examRoundParticipants).<br>   - Kỳ thi đang OPEN tại thời điểm hiện tại (now >= opensAt và now < closesAt).<br>   - Sinh viên chưa có phiên thi nào đang IN_PROGRESS.<br>   - Sinh viên chưa có phiên thi nào COMPLETED trong kỳ thi này.<br>5. Hệ thống tính toán thời hạn phiên: expires_at = min(now + durationMinutes, closesAt) và lưu vào TestSession.<br>6. Hệ thống khởi tạo trạng thái phiên thi trong Redis (SessionCacheState: thetaInit = -0.5, lưới 41 điểm EAP).<br>7. Hệ thống chuyển sinh viên đến giao diện làm bài thi (/exams/[id]/take). |
| Luồng thay thế | 4a. Sinh viên đang có phiên thi dở dang (IN_PROGRESS) của chính kỳ thi đó:<br>  4a1. Hệ thống phát hiện sessionId đang mở, trả về mã 409 kèm sessionId.<br>  4a2. Hệ thống hỏi sinh viên có muốn tiếp tục bài thi không và chuyển sang UCSV07. |
| Luồng ngoại lệ | 4b. Sinh viên không thuộc danh sách dự thi: Hệ thống báo lỗi HTTP 403 NOT_IN_ROUND.<br>4c. Kỳ thi chưa đến giờ mở hoặc đã đóng: Hệ thống báo lỗi HTTP 409 ROUND_NOT_OPEN.<br>4d. Sinh viên đã hoàn thành bài thi trong kỳ này: Hệ thống báo lỗi HTTP 409 ROUND_ALREADY_COMPLETED. |
| Quy tắc nghiệp vụ liên quan | BR-07 (Admin tạo kỳ), BR-08 (opensAt < closesAt), BR-09 (danh sách gồm STUDENT), BR-10 (điều kiện bắt đầu phiên), BR-11 (tính expires_at). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên thuộc kỳ thi đang OPEN và chưa thi When bấm 'Tôi đã hiểu, bắt đầu làm bài' tại màn hình S03 Then hệ thống (POST /api/v1/sessions) tạo TestSession mới với expires_at = min(startedAt + duration, closesAt) và trả về câu hỏi đầu tiên.<br>- Given sinh viên vào thi lúc 10:45 trong kỳ thi 10:00-11:00 (duration=45 phút) When bắt đầu Then expires_at được chốt tại 11:00 (thời gian làm bài thực tế chỉ còn 15 phút do chạm trần closesAt).<br>- Given sinh viên đã có bài thi COMPLETED trong kỳ When cố tình gửi request POST /sessions Then hệ thống trả về HTTP 409 ROUND_ALREADY_COMPLETED. |

### Bảng đặc tả / Danh mục 3

| Use Case ID | UCSV03 |
| --- | --- |
| Tên chức năng | Làm bài thi (nhận câu hỏi và nộp đáp án) |
| Mô tả | Sinh viên thực hiện trả lời lần lượt từng câu hỏi thích ứng do CATEngine lựa chọn cho đến khi chạm điều kiện dừng. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Phiên thi TestSession đang ở trạng thái IN_PROGRESS trong Redis. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Các phản hồi được ghi nhận, năng lực theta được cập nhật liên tục; khi dừng thì chuyển trạng thái COMPLETED và sinh LanguageProfile. |
| Luồng chính | 1. Màn hình hiển thị câu hỏi hiện tại, 4 phương án lựa chọn, và đồng hồ đếm ngược theo expiresAt.<br>2. Sinh viên chọn 1 phương án đáp án và bấm 'Xác nhận nộp câu trả lời'.<br>3. Hệ thống kiểm tra thời gian hiện tại so với expiresAt. Thời gian còn hợp lệ.<br>4. Hệ thống ghi nhận SessionResponse (isCorrect, responseTimeMs).<br>5. CATEngine chạy computeEAP cập nhật theta và standardError trên lưới 41 điểm.<br>6. CATEngine kiểm tra checkStoppingCriterion (SE < 0.35, Outlier Early Stop, Max 25 câu, Timeout).<br>7. Chưa thỏa mãn điều kiện dừng: CATEngine chọn câu hỏi tiếp theo (selectNextItem) bằng thuật toán Randomized Top-5 b-matching từ ngân hàng câu hỏi FINAL_APPROVED, xen kẽ kỹ năng qua pickNextSkill.<br>8. Hệ thống cập nhật SessionCacheState và trả về câu hỏi mới cho sinh viên. Lặp lại bước 1. |
| Luồng thay thế | 6a. Thỏa mãn một trong các điều kiện dừng:<br>  6a1. Hệ thống cập nhật TestSession: status = COMPLETED, thetaFinal, seFinal, completedAt = now, stoppingReason.<br>  6a2. Hệ thống gọi LanguageProfileService sinh hồ sơ năng lực chi tiết.<br>  6a3. Hệ thống xóa cache phiên trên Redis, chuyển hướng sinh viên sang trang Xem kết quả (UCSV04). |
| Luồng ngoại lệ | 3a. Hết thời gian làm bài (now > expiresAt):<br>  3a1. Áp dụng luật K5 (BR-11): Nếu sinh viên đã làm >= 8 câu, hệ thống hoàn tất phiên với status = COMPLETED và stoppingReason = TIMEOUT, tính điểm trên các câu đã làm.<br>  3a2. Nếu làm < 8 câu, hệ thống đánh dấu phiên = ABANDONED (sinh viên được phép thi lại nếu kỳ thi còn mở).<br>2a. Mất kết nối mạng khi nộp bài: Giao diện lưu tạm đáp án trên local storage và tự động thử lại khi có mạng. |
| Quy tắc nghiệp vụ liên quan | BR-10, BR-11 (luật K5 quá hạn phiên), Mục 4.1-4.5 SRS (Rasch 1PL, EAP 41 điểm, Top-5 b-matching, 4 điều kiện dừng). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên nộp đáp án câu thứ 18 đạt SE = 0.33 (< 0.35) When nộp đáp án Then bài thi dừng ngay lập tức, chuyển trạng thái COMPLETED với stoppingReason = SE_THRESHOLD.<br>- Given sinh viên làm đến câu 25 When nộp đáp án Then bài thi kết thúc với stoppingReason = MAX_ITEMS_REACHED.<br>- Given sinh viên hết thời gian làm bài khi mới làm được 5 câu When hệ thống quét phiên quá hạn Then phiên chuyển thành ABANDONED và cho phép sinh viên thi lại phiên mới trong cùng kỳ. |

### Bảng đặc tả / Danh mục 4

| Use Case ID | UCSV08 |
| --- | --- |
| Tên chức năng | Đổi mật khẩu |
| Mô tả | Cho phép người dùng (Sinh viên, Giảng viên, Admin) đổi mật khẩu tài khoản (bắt buộc lần đầu hoặc chủ động đổi). |
| Tác nhân | Sinh viên, Giảng viên, Quản trị viên |
| Điều kiện trước | Người dùng đã xác thực (có JWT token đăng nhập hoặc JWT tạm change-password). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Mật khẩu mới được băm argon2 và lưu trữ; cờ mustChangePassword chuyển thành false; cấp token mới. |
| Luồng chính | 1. Người dùng truy cập chức năng Đổi mật khẩu (/change-password).<br>2. Người dùng nhập: Mật khẩu hiện tại, Mật khẩu mới, Xác nhận mật khẩu mới.<br>3. Hệ thống kiểm tra mật khẩu hiện tại có khớp với passwordHash trong DB hay không.<br>4. Hệ thống kiểm tra mật khẩu mới: độ dài >= 8 ký tự, có chữ thường, chữ hoa, chữ số và ký tự đặc biệt, khác mật khẩu hiện tại, khớp với xác nhận mật khẩu.<br>5. Hệ thống băm mật khẩu mới bằng argon2 và cập nhật vào bảng users.<br>6. Hệ thống cập nhật mustChangePassword = false và passwordChangedAt = now().<br>7. Hệ thống thu hồi token cũ, cấp access token mới đầy đủ quyền và chuyển người dùng vào trang chủ. |
| Luồng thay thế | 1a. Người dùng đổi mật khẩu định kỳ từ menu Hồ sơ cá nhân (khi đang đăng nhập bình thường). |
| Luồng ngoại lệ | 3a. Mật khẩu hiện tại không đúng: Hệ thống báo lỗi HTTP 400 ('Mật khẩu hiện tại không chính xác').<br>4a. Mật khẩu mới trùng mật khẩu cũ: Báo lỗi 'Mật khẩu mới không được trùng mật khẩu cũ'.<br>4b. Mật khẩu mới không đạt độ phức tạp (< 8 ký tự hoặc thiếu chữ thường, chữ hoa, chữ số, ký tự đặc biệt): Báo lỗi 'Mật khẩu mới phải có ít nhất 8 ký tự, gồm chữ thường, chữ hoa, chữ số và ký tự đặc biệt'. |
| Quy tắc nghiệp vụ liên quan | BR-05 (băm mật khẩu argon2), BR-06 (mật khẩu mới khác mật khẩu cũ, độ dài >= 8, mustChangePassword=false). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given người dùng đăng nhập lần đầu với mustChangePassword=true When nhập mật khẩu mới hợp lệ (>= 8 ký tự gồm chữ thường, chữ hoa, chữ số, ký tự đặc biệt; khác mật khẩu cũ) Then hệ thống cập nhật passwordHash mới, set mustChangePassword=false và cho phép vào hệ thống.<br>- Given người dùng nhập mật khẩu mới giống hệt mật khẩu tạm hiện tại When gửi yêu cầu Then hệ thống từ chối và báo lỗi HTTP 400. |

### Bảng đặc tả / Danh mục 5

| Use Case ID | UCSV09 |
| --- | --- |
| Tên chức năng | Quên mật khẩu (OTP qua email) |
| Mô tả | Cho phép người dùng tự lấy lại mật khẩu thông qua mã xác thực OTP 6 số gửi về email đăng ký. |
| Tác nhân | Sinh viên, Giảng viên, Quản trị viên |
| Điều kiện trước | Người dùng không nhớ mật khẩu và không đăng nhập được. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Mật khẩu mới được cập nhật, mã OTP bị hủy, người dùng có thể đăng nhập bằng mật khẩu mới. |
| Luồng chính | 1. Người dùng chọn 'Quên mật khẩu' trên màn hình đăng nhập (/forgot-password).<br>2. Người dùng nhập Email tài khoản và bấm 'Gửi mã xác nhận'.<br>3. Hệ thống kiểm tra định dạng email và kiểm tra sự tồn tại của email trong DB.<br>4. Hệ thống sinh mã OTP 6 chữ số ngẫu nhiên, lưu bản băm của mã vào Redis với TTL = 10 phút, số lần thử = 0.<br>5. Hệ thống đẩy tác vụ gửi email chứa OTP vào hàng đợi BullMQ và gửi qua MailPort (SMTP).<br>6. Hệ thống luôn trả về HTTP 202 Accepted và chuyển giao diện sang trang nhập mã OTP (/reset-password).<br>7. Người dùng mở email, lấy mã OTP 6 số và nhập: Email, Mã OTP, Mật khẩu mới.<br>8. Hệ thống kiểm tra mã OTP trong Redis: đúng mã và còn hiệu lực.<br>9. Hệ thống cập nhật mật khẩu mới (argon2), xóa cờ mustChangePassword, xóa OTP khỏi Redis.<br>10. Hệ thống hiển thị thông báo thành công và chuyển hướng về trang Đăng nhập. |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 3a. Email không tồn tại trong hệ thống: Hệ thống vẫn trả về HTTP 202 Accepted (chống dò quét email, BR-14) nhưng không gửi email.<br>8a. Mã OTP sai: Hệ thống tăng bộ đếm sai. Nếu nhập sai >= 5 lần, hệ thống hủy mã OTP trong Redis và yêu cầu xin mã mới.<br>8b. Mã OTP đã hết hạn (> 10 phút): Báo lỗi HTTP 400 INVALID_RESET_OTP ('Mã xác thực đã hết hạn').<br>2a. Người dùng yêu cầu gửi mã quá nhiều lần liên tiếp: Bị chặn bởi rate-limit (HTTP 429). |
| Quy tắc nghiệp vụ liên quan | BR-14 (phản hồi 202 đồng nhất, rate limit, OTP 6 số, TTL 10 phút, tối đa 5 lần sai). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given email người dùng hợp lệ When yêu cầu quên mật khẩu Then nhận được mã OTP 6 số qua email trong vòng 10 giây và mã có hiệu lực 10 phút.<br>- Given người dùng nhập sai mã OTP 5 lần When gửi lần thứ 5 Then mã OTP bị xóa khỏi Redis và trả về HTTP 400.<br>- Given người dùng hoàn tất đặt lại mật khẩu bằng OTP When đăng nhập lại Then mật khẩu mới hoạt động bình thường và mustChangePassword = false. |

### Bảng đặc tả / Danh mục 6

| Use Case ID | UCGV14 |
| --- | --- |
| Tên chức năng | Duyệt câu hỏi (GV vai A) |
| Mô tả | Giảng viên vai A kiểm tra, chỉnh sửa nội dung/đáp án/giải thích các câu hỏi được phân công và quyết định duyệt hoặc từ chối từng câu hỏi. |
| Tác nhân | Giảng viên (vai A) |
| Điều kiện trước | Lô câu hỏi đang ở trạng thái IN_REVIEW, GV đã được Admin phân công nhiệm vụ duyệt. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Câu hỏi được cập nhật trạng thái FIRST_APPROVED (nếu duyệt) hoặc REJECTED (nếu từ chối); thông tin đợt 1 được ghi nhận vào firstReview (kèm originalSnapshot nếu có sửa) và ghi log vào ItemReviewEvent. Câu hỏi FIRST_APPROVED sẵn sàng cho GV B thẩm định. |
| Luồng chính | 1. GV A mở danh sách nhiệm vụ duyệt (/teacher/tasks/reviews).<br>2. Hệ thống hiển thị danh sách các câu hỏi DRAFT được phân công riêng cho GV A (kèm cờ mềm AI, giải thích AI, hạn còn lại due_at).<br>3. GV A chọn xem chi tiết từng câu hỏi (/teacher/tasks/reviews/[batchId]?item=[itemId]). GV A có thể chỉnh sửa nội dung câu hỏi, 4 phương án, đáp án đúng hoặc giải thích AI.<br>4. Sau khi chỉnh sửa, hệ thống kiểm tra luật cứng và lọc trùng T1-T2 trên bản sửa. Bản sửa hợp lệ.<br>5. GV A chọn 'Duyệt câu hỏi' (chuyển trạng thái câu thành FIRST_APPROVED) hoặc 'Từ chối' (chuyển trạng thái câu thành REJECTED, không cần lý do).<br>6. Hệ thống cập nhật trường Item.firstReview (action, reviewedAt, comment, originalSnapshot) và ghi nhận sự kiện vào ItemReviewEvent.<br>7. Hệ thống tự động chuyển sang câu hỏi tiếp theo trong danh sách được giao hoặc quay về danh sách nhiệm vụ nếu đã hoàn tất. |
| Luồng thay thế | 3a. Câu hỏi không cần sửa nội dung: GV A bấm Duyệt trực tiếp. |
| Luồng ngoại lệ | 4a. Sau khi sửa, câu hỏi bị trùng với câu hỏi khác trong ngân hàng hoặc sai cú pháp: Hệ thống từ chối lưu và báo lỗi (422 DUPLICATE_AFTER_EDIT / INVALID_AFTER_EDIT).<br>2a. Hạn duyệt sắp hết (còn 24h): Hệ thống gửi email nhắc nhở; việc vẫn hiện trong Hộp việc (Tiểu luận không làm chuông thông báo thời gian thực). |
| Quy tắc nghiệp vụ liên quan | BR-16 (chỉ xem câu của mình), BR-22 (B không thuộc nhóm A), BR-24 (hạn và nhắc việc), BR-25 (điều kiện gửi gói của A), BR-27 (kiểm tra lại sau khi sửa). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given GV A được giao 20 câu hỏi When duyệt được 19 câu Then còn 1 câu chưa quyết, 19 câu đã duyệt chuyển FIRST_APPROVED sẵn sàng cho GV B thẩm định.<br>- Given GV A sửa đáp án câu hỏi khiến câu hỏi trùng lặp T2 When bấm lưu Then hệ thống báo lỗi 422 DUPLICATE_AFTER_EDIT.<br>- Given GV A duyệt 15 câu FIRST_APPROVED và từ chối 5 câu REJECTED When hoàn tất Then 15 câu FIRST_APPROVED hiển thị trong danh sách cần xác nhận của GV B, 5 câu REJECTED được lưu lại trong lô để Admin thống kê. |

### Bảng đặc tả / Danh mục 7

| Use Case ID | UCGV15 |
| --- | --- |
| Tên chức năng | Xác nhận câu hỏi (GV vai B) |
| Mô tả | Giảng viên vai B (đại diện bộ môn) xem xét các câu hỏi do GV A đã duyệt và xác nhận hoặc loại bỏ từng câu hỏi. |
| Tác nhân | Giảng viên (vai B) |
| Điều kiện trước | Các câu hỏi được phân công cho GV B (confirmerId = currentUserId) đã được GV A duyệt đạt (status = FIRST_APPROVED). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Câu hỏi được chuyển sang trạng thái SECOND_APPROVED (nếu xác nhận) hoặc REJECTED (nếu loại bỏ); thông tin lưu vào secondReview và ghi log ItemReviewEvent. Khi toàn bộ câu hỏi trong lô hoàn thành vòng 2, lô chuyển sang READY_TO_FINALIZE. |
| Luồng chính | 1. GV B mở danh sách câu hỏi cần xác nhận (/teacher/tasks/confirms).<br>2. Hệ thống hiển thị các câu hỏi đang ở trạng thái FIRST_APPROVED được giao cho B, hiển thị rõ GV A phụ trách, dấu hiệu 'A đã sửa', và bản so sánh C-DIFF nếu có.<br>3. GV B mở chi tiết câu hỏi (/teacher/tasks/confirms/[batchId]?item=[itemId], chế độ chỉ đọc, đối chiếu bản gốc và bản sửa qua C-DIFF, không có quyền sửa nội dung).<br>4. Với từng câu hỏi, GV B chọn 'Xác nhận' (chuyển câu thành SECOND_APPROVED) hoặc 'Loại bỏ' (chuyển câu thành REJECTED).<br>5. Hệ thống cập nhật Item.secondReview và ghi ItemReviewEvent.<br>6. Khi toàn bộ các câu trong lô đều đã hoàn thành vòng 2 (hoặc các câu còn lại đã hết hạn), hệ thống cập nhật trạng thái lô câu hỏi thành READY_TO_FINALIZE và gửi email thông báo cho Admin. |
| Luồng thay thế | 4a. Xác nhận hàng loạt: GV B sau khi xem xét tổng thể bấm 'Xác nhận tất cả câu còn lại được giao trong lô' -> Hệ thống chuyển tất cả các câu chưa quyết định thành SECOND_APPROVED và ghi log kiểm toán hành động hàng loạt CONFIRM_ALL. |
| Luồng ngoại lệ | 3a. GV B gọi API sửa nội dung câu hỏi hoặc yêu cầu trả về cho GV A: Hệ thống từ chối (HTTP 403 / 400 do quy trình một chiều, B không được sửa và không có luồng trả về A theo DC-33).<br>1a. GV không phải là người được chỉ định B của câu hỏi truy cập: Bị chặn quyền HTTP 403 NOT_ASSIGNED. |
| Quy tắc nghiệp vụ liên quan | BR-16 (phân quyền B), BR-24 (hạn của B tính từ ngày nhận gói), BR-26 (B chỉ đọc, không sửa, không trả về A, có nút xác nhận tất cả còn lại). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given danh sách có 15 câu hỏi When GV B bấm 'Xác nhận tất cả câu còn lại' Then toàn bộ 15 câu chuyển sang SECOND_APPROVED và ghi nhận log kiểm toán CONFIRM_ALL.<br>- Given GV B chọn loại 2 câu và xác nhận 13 câu When hoàn tất Then 13 câu thành SECOND_APPROVED, 2 câu thành REJECTED, không câu nào bị trả ngược về A. |

### Bảng đặc tả / Danh mục 8

| Use Case ID | UCADM08 |
| --- | --- |
| Tên chức năng | Import tài khoản người dùng (SV và GV) |
| Mô tả | Quản trị viên tải file Excel danh sách sinh viên hoặc giảng viên để kiểm tra trên lưới tạm và lưu hàng loạt vào hệ thống. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Admin đã đăng nhập, có quyền quản trị tài khoản. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Tài khoản người dùng mới được tạo trong DB với role tương ứng; mật khẩu tạm được sinh và gửi email. |
| Luồng chính | 1. Admin truy cập màn hình Import tài khoản (/admin/users/import).<br>2. Admin chọn đối tượng import: Sinh viên (kind=STUDENT) hoặc Giảng viên (kind=TEACHER).<br>3. Admin chọn tải lên file .xlsx mẫu.<br>4. Hệ thống phân tích file: kiểm tra định dạng, kiểm tra các cột bắt buộc, kiểm tra trùng lặp trong file và trùng lặp với DB.<br>5. Các dòng hợp lệ được nạp vào lưới tạm (Redis, khóa import:accounts:<adminId>:<kind>, TTL 30 phút).<br>6. Các dòng lỗi (thiếu cột, sai định dạng email, trùng trong file) bị loại khỏi lưới và hiển thị ở popup "Dòng bị loại" (số dòng và lý do). Các dòng trùng email/MSSV/Mã GV đã có trong hệ thống hiển thị ở popup riêng "Tài khoản đã tồn tại"; chúng không vào lưới nên không chặn Lưu (chỉ tạo mới, không cập nhật tài khoản có sẵn).<br>7. Admin xem lưới tạm, có thể tải thêm file khác (các dòng đã có sẽ được bỏ qua) hoặc bấm xóa từng dòng trên lưới.<br>8. Admin bấm 'Lưu'; hệ thống trả ngay (HTTP 202) và chạy nền, giao diện hiện thanh tiến độ (GET /users/import/save-status).<br>9. Tác vụ nền kiểm trùng lại, rồi băm mật khẩu song song (1000 tài khoản mất ~50 giây) và thực hiện một transaction duy nhất tạo toàn bộ tài khoản có trong lưới (tất cả hoặc không có gì): cấp role tương ứng, authProvider=LOCAL, mustChangePassword=true, sinh mật khẩu tạm 12 ký tự ngẫu nhiên (argon2).<br>10. Sau khi ghi DB thành công, hệ thống xếp hàng email thông báo tài khoản và mật khẩu tạm vào hàng đợi gửi thư (cổng IMailQueue, chạy trong tiến trình, có thử lại; có thể thay bằng BullMQ).<br>11. Hệ thống xóa lưới tạm trên Redis; giao diện hiển thị "Đã tạo N tài khoản, M email đã xếp hàng gửi". |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 4a. File sai định dạng hoặc vượt quá 2MB / quá 1000 dòng: Báo lỗi HTTP 400/413 IMPORT_FILE_INVALID.<br>8a. Lưới tạm đã hết hạn TTL (30 phút): Báo lỗi HTTP 410 IMPORT_GRID_EXPIRED, yêu cầu tải lại file.<br>8b. Admin bấm Lưu khi lưới tạm rỗng: Báo lỗi HTTP 422 IMPORT_GRID_EMPTY.<br>9a. Có tài khoản trùng phát sinh giữa lúc Lưu (người khác vừa tạo trùng email/mã): tác vụ nền dừng với trạng thái FAILED (CONFLICT) kèm danh sách dòng trùng, không tạo tài khoản nào và giữ lưới để Admin xóa dòng trùng rồi Lưu lại.<br>10a. Gửi email thất bại sau số lần thử: ghi log ứng dụng, không rollback tài khoản và không lưu trạng thái gửi (Quyết định #120); Admin dùng 'Gửi lại mật khẩu tạm' ở UCADM09 (BR-05). |
| Quy tắc nghiệp vụ liên quan | BR-01 (Admin tạo tài khoản), BR-02 (email/MSSV duy nhất), BR-03 (lưới tạm và lọc dòng lỗi), BR-04 (lưu một transaction), BR-05 (mật khẩu tạm và email hàng đợi), BR-15 (nhật ký kiểm toán). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given file Excel gồm 100 dòng SV (trong đó 5 dòng trùng MSSV trong DB, 2 dòng sai email) When tải file Then lưới tạm chỉ nhận 93 dòng, popup hiển thị thông báo loại 7 dòng với lý do cụ thể.<br>- Given lưới tạm có 93 dòng When bấm Lưu Then 93 tài khoản được tạo trong DB, 93 email được xếp hàng gửi và lưới tạm bị xóa khỏi Redis (Lưu chạy nền, theo dõi được tiến độ).<br>- Given Admin để lưới tạm quá 30 phút không bấm Lưu When bấm Lưu Then hệ thống trả về HTTP 410 IMPORT_GRID_EXPIRED. |

### Bảng đặc tả / Danh mục 9

| Use Case ID | UCADM09 |
| --- | --- |
| Tên chức năng | Quản lý tài khoản người dùng |
| Mô tả | Quản trị viên tạo lẻ từng tài khoản SV/GV qua biểu mẫu, khóa/mở khóa tài khoản, gửi lại mật khẩu tạm, và nâng/thu hồi quyền Admin. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Admin đã đăng nhập với vai trò ADMIN. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Thông tin tài khoản được cập nhật (nhật ký kiểm toán hoãn: chưa có nơi lưu, tạm ghi log ứng dụng; BR-18). |
| Luồng chính | 1. Admin truy cập màn hình Tài khoản với hai tab là hai route: Sinh viên (/admin/users/students) và Giảng viên (/admin/users/teachers).<br>2. Admin tìm kiếm theo họ tên, email, MSSV/Mã GV; danh sách có phân trang. Tab Giảng viên gồm cả tài khoản Admin (có huy hiệu Admin) để thu hồi quyền.<br>3. Thao tác Tạo lẻ từng tài khoản (BR-20):<br>   - Admin chọn 'Thêm tài khoản', chọn loại SV hoặc GV.<br>   - Admin nhập thông tin: Họ tên, Email, MSSV (nếu SV) hoặc Mã GV (nếu GV).<br>   - Hệ thống kiểm tra trùng lặp email, mã. Không trùng: tạo tài khoản, sinh mật khẩu tạm 12 ký tự (argon2), mustChangePassword=true, gửi email mật khẩu tạm sau khi lưu (lỗi gửi không rollback tài khoản). Admin cũng có thể sửa họ tên và email của tài khoản (MSSV/Mã GV không sửa được).<br>4. Thao tác Khóa / Mở khóa tài khoản (BR-19):<br>   - Admin chọn một tài khoản và bấm 'Khóa tài khoản' hoặc 'Mở khóa'.<br>   - Hệ thống đảo cờ isActive (true <-> false). Nếu tài khoản bị khóa, mọi request đang dùng token cũ bị trả 401 ngay và không đăng nhập lại được. Admin không tự khóa mình và không khóa tài khoản Admin (phải thu hồi quyền trước).<br>5. Thao tác Gửi lại mật khẩu tạm (BR-19):<br>   - Admin chọn tài khoản và bấm 'Gửi lại mật khẩu tạm'.<br>   - Hệ thống sinh mật khẩu tạm mới, băm argon2, set mustChangePassword=true (token và mật khẩu cũ mất hiệu lực), gửi email mật khẩu mới. Áp dụng cho SV và GV kể cả khi đã đổi mật khẩu; không áp dụng cho Admin.<br>6. Thao tác Nâng / Thu hồi quyền Admin (BR-17, BR-18):<br>   - Admin chọn một Giảng viên và bấm 'Nâng lên Admin' -> role đổi thành ADMIN (có hiệu lực ngay, vì role được đọc từ cơ sở dữ liệu ở mỗi request). Chỉ đổi giữa TEACHER và ADMIN; không áp dụng cho sinh viên.<br>   - Admin chọn một Admin khác và bấm 'Thu hồi quyền Admin' -> role đổi về TEACHER. |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 3a. Email hoặc MSSV/Mã GV đã tồn tại: Hệ thống báo lỗi HTTP 409 Conflict kèm tên trường bị trùng; giao diện hiện lỗi ngay dưới đúng ô.<br>4a. Admin cố tình tự khóa mình hoặc khóa một tài khoản Admin khác: Hệ thống từ chối (HTTP 403).<br>6a. Admin cố tình tự thu hồi quyền Admin của chính mình: Hệ thống từ chối (HTTP 403).<br>6b. Thu hồi quyền của Admin cuối cùng: không xảy ra, vì người thao tác luôn là một Admin khác còn hoạt động và Admin không được tự thu hồi mình (BR-18).<br>6c. Đổi quyền của tài khoản sinh viên: Hệ thống từ chối (HTTP 400). |
| Quy tắc nghiệp vụ liên quan | BR-01, BR-02, BR-16, BR-17 (Admin quản lý GV), BR-18 (chặn thu hồi Admin cuối), BR-19 (khóa tài khoản, gửi lại mật khẩu), BR-20 (tạo lẻ SV/GV). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given Admin tạo lẻ 1 giảng viên với email và mã GV hợp lệ When bấm Tạo Then tài khoản được tạo ngay và email chứa mật khẩu tạm được gửi đi.<br>- Given tài khoản SV bị khóa (isActive=false) When sinh viên cố tình đăng nhập Then nhận thông báo lỗi 403 không cho phép đăng nhập.<br>- Given hệ thống chỉ còn 1 tài khoản Admin When tài khoản này cố tình hạ quyền xuống TEACHER Then hệ thống từ chối thực hiện. |

### Bảng đặc tả / Danh mục 10

| Use Case ID | UCADM15 |
| --- | --- |
| Tên chức năng | Quản lý kỳ thi (Exam Round) |
| Mô tả | Quản trị viên thiết lập đợt thi mới, cấu hình thời gian mở/đóng, thời lượng làm bài, và công bố kỳ thi cho sinh viên. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Admin đã đăng nhập. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Kỳ thi được tạo hoặc chuyển đổi trạng thái hợp lệ trong máy trạng thái (ExamRoundStatus). |
| Luồng chính | 1. Admin truy cập mục Quản lý kỳ thi (/admin/exam-rounds).<br>2. Admin bấm 'Tạo kỳ thi mới'.<br>3. Admin nhập: Tên kỳ thi, Thời điểm mở (opensAt), Thời điểm đóng (closesAt), Thời lượng làm bài (durationMinutes - mặc định 45 phút, giới hạn 5 đến 180 phút).<br>4. Hệ thống kiểm tra điều kiện thời gian: closesAt > opensAt và durationMinutes <= (closesAt - opensAt).<br>5. Kỳ thi được tạo ở trạng thái DRAFT.<br>6. Sau khi import danh sách thí sinh (UCADM16) đạt ít nhất 1 sinh viên, Admin bấm 'Công bố kỳ thi'.<br>7. Hệ thống chuyển trạng thái kỳ thi sang SCHEDULED.<br>8. Khi đồng hồ hệ thống chạm opensAt, trạng thái hiệu lực chuyển sang OPEN (tính toán lazy).<br>9. Khi chạm closesAt hoặc Admin bấm 'Đóng kỳ thi', kỳ thi chuyển sang CLOSED. |
| Luồng thay thế | 5a. Khi kỳ thi ở DRAFT, Admin có thể chỉnh sửa mọi thông tin hoặc bấm 'Hủy kỳ thi' (chuyển sang CLOSED).<br>7a. Khi kỳ thi ở SCHEDULED, Admin chỉ được sửa tên kỳ thi hoặc gia hạn kéo dài closesAt (BR-08). |
| Luồng ngoại lệ | 4a. opensAt >= closesAt hoặc thời lượng lớn hơn khoảng cách mở đóng: Báo lỗi validation HTTP 400.<br>6a. Admin công bố kỳ thi khi danh sách thí sinh đang rỗng: Báo lỗi 'Kỳ thi phải có ít nhất 1 thí sinh trước khi công bố'.<br>9a. Admin sửa kỳ thi đã CLOSED: Hệ thống chặn và báo lỗi 'Không được sửa kỳ thi đã đóng'. |
| Quy tắc nghiệp vụ liên quan | BR-07 (Admin tạo kỳ), BR-08 (máy trạng thái kỳ thi, điều kiện thời gian), BR-10 (điều kiện vào thi), BR-12 (đóng thủ công khi có phiên đang chạy). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given Admin tạo kỳ thi với durationMinutes = 60, opensAt = 08:00, closesAt = 10:00 When lưu Then kỳ thi DRAFT được tạo thành công.<br>- Given kỳ thi DRAFT có 50 sinh viên dự thi When Admin bấm Công bố Then trạng thái chuyển thành SCHEDULED.<br>- Given kỳ thi đang SCHEDULED với closesAt = 11:00 When Admin cập nhật closesAt = 12:00 Then hệ thống chấp nhận gia hạn. |

### Bảng đặc tả / Danh mục 11

| Use Case ID | UCADM16 |
| --- | --- |
| Tên chức năng | Import danh sách sinh viên thi |
| Mô tả | Quản trị viên tải file Excel danh sách MSSV tham gia kỳ thi theo cơ chế lưới tạm. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Kỳ thi đang ở trạng thái DRAFT hoặc SCHEDULED. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Danh sách sinh viên dự thi được liên kết vào kỳ thi (examRoundParticipants). |
| Luồng chính | 1. Admin mở chi tiết kỳ thi và chọn 'Nhập danh sách thí sinh' (/admin/exam-rounds/[id]/import).<br>2. Admin tải lên file .xlsx chứa cột MSSV và Ghi chú.<br>3. Hệ thống kiểm tra từng dòng:<br>   - Kiểm tra MSSV có tồn tại trong hệ thống với role STUDENT hay không.<br>   - Kiểm tra sinh viên đã có trong danh sách kỳ thi này chưa.<br>4. Các dòng hợp lệ được đưa vào lưới tạm trên Redis (TTL 30 phút).<br>5. Các dòng không hợp lệ (MSSV không tồn tại, MSSV đã có trong kỳ) bị loại kèm popup thông báo chi tiết.<br>6. Admin xem lưới tạm, có thể xóa bớt dòng hoặc tải thêm file khác.<br>7. Admin bấm 'Lưu danh sách'.<br>8. Hệ thống lưu toàn bộ sinh viên trong lưới vào danh sách dự thi của kỳ thi trong một transaction và xóa lưới tạm. |
| Luồng thay thế | 1a. Admin có thể gỡ bỏ 1 sinh viên khỏi kỳ thi nếu sinh viên đó chưa bắt đầu phiên thi nào trong kỳ (MD-07). |
| Luồng ngoại lệ | 3a. MSSV không tồn tại: Dòng bị loại, popup báo 'MSSV không tồn tại trong hệ thống' (Admin phải import tài khoản SV trước qua UCADM08).<br>8a. Lưới tạm rỗng hoặc hết hạn TTL: Báo lỗi tương tự UCADM08. |
| Quy tắc nghiệp vụ liên quan | BR-03, BR-04, BR-07, BR-09 (danh sách chỉ gồm tài khoản role STUDENT đã có trong hệ thống). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given file import danh sách thi có 50 MSSV (trong đó 2 MSSV chưa có tài khoản trong hệ thống) When tải file Then 48 MSSV vào lưới, popup báo loại 2 MSSV chưa tồn tại.<br>- Given Admin lưu danh sách 48 MSSV When lưu thành công Then 48 sinh viên này được quyền truy cập kỳ thi khi kỳ thi OPEN. |

### Bảng đặc tả / Danh mục 12

| Use Case ID | UCADM17 |
| --- | --- |
| Tên chức năng | Theo dõi dự thi của kỳ thi |
| Mô tả | Quản trị viên giám sát tiến độ làm bài của các thí sinh trong kỳ thi theo thời gian thực. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Kỳ thi ở trạng thái SCHEDULED, OPEN hoặc CLOSED. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Hiển thị danh sách thí sinh kèm trạng thái dự thi (Chưa thi, Đang thi, Đã hoàn thành, Bỏ thi/Quá hạn). |
| Luồng chính | 1. Admin mở trang chi tiết kỳ thi (/admin/exam-rounds/[id]).<br>2. Hệ thống thống kê tổng số thí sinh, số lượng theo từng trạng thái: Chưa thi, Đang thi (IN_PROGRESS), Đã hoàn thành (COMPLETED), Bỏ thi (ABANDONED).<br>3. Admin xem danh sách chi tiết từng thí sinh: MSSV, Họ tên, Trạng thái, Điểm chẩn đoán (nếu đã hoàn thành), Thời điểm bắt đầu, Thời điểm nộp bài.<br>4. Admin có thể lọc theo trạng thái dự thi hoặc tìm kiếm theo MSSV. |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | Không có. |
| Quy tắc nghiệp vụ liên quan | BR-07, BR-10, BR-11. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given kỳ thi đang OPEN có 100 sinh viên When Admin mở màn hình theo dõi Then thấy rõ số lượng sinh viên đang làm bài và danh sách cập nhật theo thời gian thực. |

### Bảng đặc tả / Danh mục 13

| Use Case ID | UCADM11 |
| --- | --- |
| Tên chức năng | Tạo lô câu hỏi bằng AI |
| Mô tả | Quản trị viên yêu cầu hệ thống sinh tự động một lô câu hỏi trắc nghiệm tiếng Anh kèm lời giải thích qua Gemini API. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Admin đã đăng nhập, có quyền quản lý ngân hàng câu hỏi. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Lô câu hỏi mới ItemBatch được tạo ở trạng thái READY_TO_ASSIGN; các câu hỏi đạt chuẩn C1 ở trạng thái DRAFT. |
| Luồng chính | 1. Admin truy cập màn hình Tạo đề thi AI (/admin/item-batches/generate).<br>2. Admin chọn các tham số: Kỹ năng (Vocabulary/Grammar), Trình độ CEFR mục tiêu (A1, A2, B1, B2), Chủ đề (topicTag), và Số lượng câu hỏi cần sinh (N).<br>3. Hệ thống tạo bản ghi ItemBatch (status = GENERATING, source = AI_GENERATED) và đẩy job vào hàng đợi BullMQ.<br>4. Worker AI thực hiện quy trình sinh câu hỏi nền:<br>   - G1: Lấy mẫu few-shot tương ứng từ ngân hàng tham chiếu.<br>   - G2: Sinh dư N' câu hỏi qua Gemini API. Mỗi câu hỏi gồm nội dung, 4 phương án, đáp án đúng, irt_b sơ bộ và lời giải thích AI.<br>   - C1: Chạy kiểm tra AI Checkpoint 1 (Luật cứng -> Băm T1 -> pg_trgm T2 -> Embedding T3 -> G5 kiểm tra đáp án độc lập).<br>   - G6: Nếu số câu đạt chuẩn < N, chạy vòng bù thiếu tối đa R lần.<br>   - G7: Cắt lấy đúng N câu đạt chuẩn, lưu câu hỏi ở trạng thái DRAFT và lưu Explanation gắn với Item.<br>   - Các câu rớt luật cứng hoặc trùng lặp cao được lưu ở trạng thái AI_REJECTED (kèm mã lý do).<br>5. Hệ thống cập nhật trạng thái lô câu hỏi thành READY_TO_ASSIGN và gửi email thông báo cho Admin (lô hiện trong danh sách lô). |
| Luồng thay thế | 4a. Vượt quá hạn mức chi phí / token hoặc hết số vòng bù mà vẫn thiếu câu: Lô chuyển sang trạng thái PARTIAL kèm cảnh báo số câu còn thiếu. |
| Luồng ngoại lệ | 3a. Gemini API không phản hồi / lỗi gateway: Hệ thống tự động chuyển sang provider dự phòng qua LLM Gateway; nếu thất bại hoàn toàn lô chuyển sang FAILED. |
| Quy tắc nghiệp vụ liên quan | BR-21 (câu hỏi chỉ vào qua lô), BR-29 (câu rớt AI chuyển AI_REJECTED), BR-30 (trạng thái đi một chiều, irt_b trong [-4, +4]), Mục 3.1 & 4.1 kế hoạch sinh đề AI. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given Admin yêu cầu sinh 20 câu B1 Grammar When AI sinh hoàn tất Then có đúng 20 câu DRAFT trong lô chuyển sang READY_TO_ASSIGN, mỗi câu đều có sẵn Explanation.<br>- Given câu hỏi sinh ra bị trùng lặp T1 (chuẩn hóa băm) với câu đã có trong ngân hàng When chạy C1 Then câu đó tự động bị đánh dấu AI_REJECTED và không đưa vào danh sách duyệt của giảng viên. |

### Bảng đặc tả / Danh mục 14

| Use Case ID | UCADM12 |
| --- | --- |
| Tên chức năng | Import đề thi từ file Excel |
| Mô tả | Quản trị viên tải file Excel chứa câu hỏi có sẵn để kiểm tra trên lưới tạm và tạo lô câu hỏi. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Admin có file .xlsx câu hỏi đúng định dạng cột quy định. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Lô câu hỏi ItemBatch được tạo ở trạng thái READY_TO_ASSIGN; các câu hỏi qua kiểm tra C2 ở trạng thái DRAFT. |
| Luồng chính | 1. Admin truy cập màn hình Import đề thi (/admin/item-batches/import).<br>2. Admin tải lên một hoặc nhiều file .xlsx chứa câu hỏi (Skill, CEFR, Topic, Câu hỏi, A, B, C, D, Đáp án, Giải thích, irt_b).<br>3. Hệ thống đọc file, chạy kiểm tra C2 (tầng 1-4: luật cứng, định dạng, trùng nội bộ file, băm T1, pg_trgm T2, embedding T3).<br>4. Dòng hợp lệ hiển thị trên lưới tạm; dòng lỗi hoặc trùng bị loại kèm popup thông báo chi tiết.<br>5. Admin xem lưới tạm, có thể tải thêm file hoặc xóa bớt dòng.<br>6. Admin bấm 'Lưu lô câu hỏi'.<br>7. Hệ thống chạy C2 tầng 5 (G5 kiểm tra đáp án độc lập), sinh bổ sung giải thích nếu câu hỏi thiếu, tạo ItemBatch (status = READY_TO_ASSIGN) và lưu các câu hỏi ở trạng thái DRAFT trong DB.<br>8. Hệ thống thông báo thành công và chuyển sang màn hình Giao việc (UCADM13). |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 2a. File không đúng định dạng cột: Báo lỗi và từ chối tải lên.<br>6a. Lưới rỗng khi bấm Lưu: Báo lỗi HTTP 422 IMPORT_GRID_EMPTY. |
| Quy tắc nghiệp vụ liên quan | BR-21, BR-29, BR-30, Mục 3.2 & 4.2 kế hoạch sinh đề AI. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given file Excel câu hỏi có 30 câu (1 câu thiếu đáp án đúng, 1 câu trùng lặp ngân hàng) When tải lên Then lưới tạm nhận 28 câu, popup báo loại 2 câu vi phạm.<br>- Given 28 câu trong lưới When bấm Lưu Then tạo thành công ItemBatch READY_TO_ASSIGN với 28 câu DRAFT. |

### Bảng đặc tả / Danh mục 15

| Use Case ID | UCADM13 |
| --- | --- |
| Tên chức năng | Giao việc duyệt câu hỏi và theo dõi lô |
| Mô tả | Quản trị viên phân công danh sách câu hỏi cho nhóm GV vai A duyệt và chỉ định 1 GV vai B confirm, cấu hình thời hạn và theo dõi tiến độ. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Lô câu hỏi đang ở trạng thái READY_TO_ASSIGN. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Các phân công ItemReviewAssignment được tạo, lô chuyển sang IN_REVIEW, lịch nhắc nhở được kích hoạt trong BullMQ. |
| Luồng chính | 1. Admin mở chi tiết lô câu hỏi và bấm 'Giao việc duyệt đề' (/admin/item-batches/[id]/assign).<br>2. Admin xem thống kê số câu DRAFT, danh sách câu AI đã loại và các cờ mềm.<br>3. Admin chọn nhóm Giảng viên vai A (chọn >= 1 GV, khuyến nghị >= 2 GV để san tải).<br>4. Admin chọn 1 Giảng viên vai B (người đại diện/trưởng bộ môn). Hệ thống kiểm tra: GV B không được nằm trong nhóm GV A.<br>5. Admin nhập thời hạn: reviewDays (hạn cho A, tính từ ngày giao) và confirmDays (hạn cho B, tính từ ngày nhận gói). Mỗi giá trị >= 1 ngày.<br>6. Hệ thống hiển thị xem trước phân bổ (chia đều số câu cho từng GV A theo thuật toán xoay vòng trộn kỹ năng/CEFR).<br>7. Admin bấm 'Xác nhận giao việc'.<br>8. Hệ thống tạo ItemReviewAssignment cho từng câu hỏi và gán trực tiếp reviewerId (GV A) và confirmerId (GV B) vào từng bản ghi Item, thiết lập dueAt cho vòng 1 và vòng 2 trong firstReview/secondReview, đặt trạng thái lô = IN_REVIEW, gửi email nhắc việc cho các GV A (việc hiện trong Hộp việc) và lên lịch nhắc việc trước 24h trong BullMQ. |
| Luồng thay thế | 1a. Điều chỉnh hạn hoặc Giao lại: Khi lô đang IN_REVIEW, Admin có thể chỉnh sửa reviewDays/confirmDays cho các phần việc chưa xong hoặc giao lại câu hỏi của một GV A sang GV A khác (hạn tính lại từ ngày giao lại, ghi nhật ký REASSIGN/EXTEND).<br>1b. Xử lý câu hỏi quá hạn vòng 1: Nếu GV A quá hạn mà chưa duyệt, các câu A đã duyệt (FIRST_APPROVED) vẫn được chuyển tiếp cho GV B thẩm định bình thường; các câu GV A chưa quyết định sẽ được Admin gia hạn thêm ngày (dueAt) hoặc gán lại (REASSIGN) sang một GV A khác (ghi nhật ký REASSIGN/EXTEND). Admin không sửa nội dung câu.<br>1c. Câu chưa xử lý sau hạn (còn DRAFT hoặc FIRST_APPROVED chưa tới B): không được import; Admin chọn giao lại với hạn mới (lô trở về IN_REVIEW) hoặc loại các câu đó thành REJECTED (không cần lý do, không sửa nội dung). Đề xuất bổ sung 16/10/2026, chờ chốt. |
| Luồng ngoại lệ | 4a. Admin chọn GV B trùng với một người trong nhóm GV A: Hệ thống chặn và báo lỗi HTTP 409 CONFIRMER_IN_REVIEW_GROUP.<br>3a. Nhóm GV A rỗng: Báo lỗi yêu cầu chọn ít nhất 1 giảng viên vai A. |
| Quy tắc nghiệp vụ liên quan | BR-22 (điều kiện giao việc), BR-23 (chia đều), BR-24 (hạn và nhắc việc trước 24h), BR-25 (gói chỉ gửi khi mọi câu của A đã có quyết định; trường hợp ngoại lệ ép gửi do Admin). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given lô có 100 câu DRAFT và Admin chọn 5 GV A When bấm xác nhận Then mỗi GV A nhận đúng 20 câu phân bổ đều theo skill và CEFR.<br>- Given Admin chọn thầy Nguyễn Văn X làm cả GV A và GV B When bấm giao việc Then hệ thống báo lỗi 409 CONFIRMER_IN_REVIEW_GROUP. |

### Bảng đặc tả / Danh mục 16

| Use Case ID | UCADM14 |
| --- | --- |
| Tên chức năng | Kiểm tra C3 và Import vào ngân hàng |
| Mô tả | Quản trị viên chạy kiểm tra AI lần 3 (C3), xem xét báo cáo diff và cờ mềm, và bấm Import câu hỏi hợp lệ vào ngân hàng đề thi. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Lô câu hỏi ở trạng thái READY_TO_FINALIZE (toàn bộ câu hỏi trong lô đã hoàn thành vòng 2 hoặc các câu còn lại đã quá hạn xử lý). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Các câu hỏi đạt chuẩn được cập nhật status = FINAL_APPROVED, sẵn sàng cho CAT Engine sử dụng. |
| Luồng chính | 1. Admin mở lô câu hỏi đang ở trạng thái READY_TO_FINALIZE (/admin/item-batches/[id]/final-check).<br>2. Admin bấm 'Kiểm tra lần cuối' (AI Checkpoint 3).<br>3. Hệ thống chạy C3 delta:<br>   - Kiểm tra luật cứng và toàn vẹn quy trình (A != B, tiến trình trạng thái một chiều, không sót câu cờ cứng).<br>   - Kiểm tra trùng T1-T2 so với ngân hàng hiện tại (phát hiện các câu mới vào ngân hàng trong thời gian chờ).<br>   - Chạy G5 và kiểm tra giải thích chỉ trên những câu mà GV A đã sửa nội dung (so sánh hash).<br>4. Hệ thống hiển thị báo cáo C3: danh sách câu qua, danh sách câu bị lỗi cứng (tự động chuyển AI_REJECTED), và danh sách câu có cờ mềm (nghi trùng T3 hoặc G5 lệch).<br>5. Với các câu cờ mềm, Admin xem xét và chọn: 'Chấp nhận cờ' (giữ để import) hoặc 'Loại bỏ' (chuyển sang REJECTED).<br>6. Khi báo cáo C3 còn hiệu lực, nút 'Import vào ngân hàng' được kích hoạt.<br>7. Admin bấm 'Import vào ngân hàng'.<br>8. Hệ thống chạy lại kiểm tra trùng nhanh T1-T2 chống race condition, chuyển toàn bộ câu SECOND_APPROVED hợp lệ thành FINAL_APPROVED (ghi nhận approvedBy, approvedAt). Lô chuyển DONE khi mọi câu đã ở trạng thái cuối (FINAL_APPROVED, REJECTED hoặc AI_REJECTED); nếu còn câu DRAFT/FIRST_APPROVED chưa xử lý (quá hạn), lô giữ FINAL_CHECKED để Admin giao lại hoặc loại các câu đó (UCADM13, luồng 1c). |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 2a. Lô chưa sẵn sàng kết thúc (vẫn còn câu chưa confirm và chưa quá hạn): Nút Kiểm tra bị vô hiệu hóa (HTTP 409 BATCH_NOT_READY_TO_FINALIZE).<br>7a. Bấm Import khi ngân hàng đã có câu mới thêm làm thay đổi tính hợp lệ: Hệ thống báo HTTP 409 FINAL_CHECK_STALE và yêu cầu chạy lại kiểm tra C3. |
| Quy tắc nghiệp vụ liên quan | BR-28 (điều kiện import), BR-29 (xử lý cờ mềm theo O2, lỗi cứng tự AI_REJECTED), BR-30 (FINAL_APPROVED cấm sửa, chỉ FINAL_APPROVED được CAT bốc). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given lô câu hỏi có 18 câu SECOND_APPROVED, trong đó 1 câu bị cờ mềm nghi trùng T3 When Admin chọn 'Chấp nhận cờ' và bấm Import Then toàn bộ 18 câu chuyển thành FINAL_APPROVED và sẵn sàng cho bài thi CAT.<br>- Given 1 câu bị lỗi cứng ở C3 (ví dụ trùng T1 với câu vừa được import từ lô khác) When C3 kết thúc Then câu này tự động chuyển thành AI_REJECTED và không được import. |

### Bảng đặc tả / Danh mục 17

| Use Case ID | UCSV04 |
| --- | --- |
| Tên chức năng | Xem kết quả bài thi |
| Mô tả | Sinh viên xem kết quả chẩn đoán của một phiên thi đã hoàn thành: mức CEFR, năng lực θ kèm sai số, điểm theo từng kỹ năng, chủ đề còn yếu và gợi ý cải thiện. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã đăng nhập (mustChangePassword = false). Phiên thi thuộc chính sinh viên này và đang ở trạng thái COMPLETED (hoàn thành thường hoặc dừng do TIMEOUT với ≥ 8 câu). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Kết quả được hiển thị đúng với LanguageProfile của phiên; không thay đổi dữ liệu nào trong hệ thống (chỉ đọc). |
| Luồng chính | 1. Sinh viên được chuyển sang trang kết quả (/results/[sessionId]) ngay sau khi phiên kết thúc (UCSV03), hoặc mở lại từ Lịch sử (UCSV06).<br>2. Hệ thống kiểm tra phiên thuộc về sinh viên đang đăng nhập và đang ở trạng thái COMPLETED.<br>3. Hệ thống lấy kết quả phiên và hồ sơ năng lực (GET /sessions/:id/result).<br>4. Hệ thống hiển thị:<br>   - Mức CEFR ước lượng (cefr_level) và độ tin cậy (cefr_confidence).<br>   - Năng lực θ, sai số chuẩn SE và khoảng tin cậy.<br>   - Số câu đúng và số câu đã làm theo từng kỹ năng (Vocabulary, Grammar).<br>   - Danh sách chủ đề còn yếu (error patterns) kèm mức độ nghiêm trọng và các gợi ý cải thiện do hệ thống tổng hợp.<br>   - Lý do dừng bài thi (stopping_reason) và thời lượng làm bài.<br>5. Sinh viên có thể chọn 'Xem giải thích' để thực hiện UCSV05 hoặc quay lại Lịch sử (UCSV06). |
| Luồng thay thế | 4a. Kết quả nằm ở vùng biên (boundary_effect = true: nhóm Pre-A1 hoặc C1+): Hệ thống hiển thị thêm thông báo 'kết quả ở vùng biên có thể kém chính xác hơn, vui lòng liên hệ Giảng viên' (SRS Mục 4.7). |
| Luồng ngoại lệ | 2a. Phiên không thuộc về sinh viên đang đăng nhập: Hệ thống từ chối với HTTP 403.<br>2b. Phiên còn IN_PROGRESS: Hệ thống không trả kết quả và gợi ý tiếp tục bài thi (UCSV07).<br>2c. Phiên ở trạng thái ABANDONED (hết hạn khi mới làm < 8 câu): Hệ thống thông báo không có kết quả và, nếu kỳ thi còn mở, cho phép thi lại (UCSV02).<br>3a. Không tìm thấy phiên: Hệ thống trả HTTP 404. |
| Quy tắc nghiệp vụ liên quan | BR-10, BR-11 (trạng thái phiên và luật quá hạn K5), BR-16 (sinh viên chỉ xem dữ liệu của chính mình), SRS Mục 4.7 (vùng biên) và Mục 15.4 (RBAC hồ sơ năng lực). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên vừa hoàn thành phiên thi với stoppingReason = SE_THRESHOLD When mở trang kết quả Then thấy mức CEFR, θ, SE, điểm hai kỹ năng và danh sách chủ đề yếu của chính phiên đó.<br>- Given phiên thuộc sinh viên khác When gọi GET /sessions/:id/result Then hệ thống trả HTTP 403 và không lộ dữ liệu.<br>- Given kết quả có boundary_effect = true When hiển thị Then trang kết quả có banner cảnh báo vùng biên. |

### Bảng đặc tả / Danh mục 18

| Use Case ID | UCSV05 |
| --- | --- |
| Tên chức năng | Xem giải thích AI (AI Explainer) |
| Mô tả | Sinh viên xem lại từng câu đã làm trong phiên đã hoàn thành, kèm đáp án đúng, đáp án đã chọn và lời giải thích do AI sinh sẵn cho câu hỏi đó. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã xem kết quả (UCSV04) của một phiên COMPLETED thuộc về mình. Chức năng xem lại đáp án đang được bật (cờ cấu hình REVIEW_ENABLED, quyết định K6 còn chờ chốt). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Sinh viên đọc được giải thích; không có thay đổi dữ liệu (chỉ đọc). Hệ thống không gọi lại mô hình AI. |
| Luồng chính | 1. Từ trang kết quả, sinh viên chọn 'Xem lại đáp án' (/results/[sessionId]/review) — quan hệ <<extend>> của UCSV04.<br>2. Hệ thống kiểm tra phiên thuộc sinh viên, đã COMPLETED và chức năng xem lại đang bật.<br>3. Hệ thống trả về danh sách các câu sinh viên đã làm theo thứ tự làm bài, mỗi câu gồm: nội dung, 4 phương án, đáp án sinh viên đã chọn, đáp án đúng và đúng/sai.<br>4. Với mỗi câu, hệ thống đọc lời giải thích đã lưu trong bảng explanations gắn với Item (giải thích được AI sinh cùng lúc với câu hỏi, dùng chung cho mọi sinh viên) và hiển thị kèm câu.<br>5. Sinh viên có thể lọc nhanh các câu làm sai, mở từng câu để đọc giải thích và quay lại trang kết quả. |
| Luồng thay thế | 4a. Câu hỏi không có giải thích (dữ liệu cũ hoặc chưa có): Hệ thống hiển thị đáp án đúng và ghi chú 'Câu này chưa có giải thích'. |
| Luồng ngoại lệ | 2a. Phiên chưa COMPLETED: Hệ thống từ chối (HTTP 409) và không trả đáp án đúng (bảo vệ nội dung đề).<br>2b. Phiên không thuộc sinh viên: HTTP 403.<br>2c. Chức năng xem lại đang tắt (REVIEW_ENABLED = false): Hệ thống ẩn nút và trả HTTP 403 REVIEW_DISABLED (đề xuất mã lỗi). |
| Quy tắc nghiệp vụ liên quan | BR-16, BR-30 (chỉ câu FINAL_APPROVED tham gia thi; giải thích gắn Item, không sinh lazy theo sinh viên), SRS Mục 15.3 (đáp án đúng chỉ trả về sau khi nộp bài), DC-31. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given phiên COMPLETED và REVIEW_ENABLED = true When sinh viên mở trang xem lại Then thấy từng câu đã làm kèm đáp án đúng, đáp án đã chọn và giải thích.<br>- Given phiên còn IN_PROGRESS When gọi API xem lại Then hệ thống trả HTTP 409 và không trả đáp án đúng của câu nào.<br>- Given hai sinh viên làm cùng một câu hỏi When cùng xem giải thích Then cả hai thấy cùng một nội dung giải thích (một bản gắn Item, không sinh lại theo từng lần xem). |

### Bảng đặc tả / Danh mục 19

| Use Case ID | UCSV06 |
| --- | --- |
| Tên chức năng | Xem lịch sử bài thi |
| Mô tả | Sinh viên xem danh sách các lần làm bài của mình và mở lại kết quả của từng lần đã hoàn thành. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã đăng nhập (mustChangePassword = false). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Danh sách lịch sử hiển thị đúng các phiên của sinh viên; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Sinh viên mở mục Lịch sử (/history).<br>2. Hệ thống lấy lịch sử hồ sơ năng lực của chính sinh viên (GET /placement-profiles/:student_id/history; student_id phải trùng JWT).<br>3. Hệ thống hiển thị bảng các lần thi, sắp xếp mới nhất trước, mỗi dòng gồm: thời điểm bắt đầu, thời lượng, mức CEFR, θ, trạng thái phiên (COMPLETED / ABANDONED / IN_PROGRESS) và lý do dừng.<br>4. Sinh viên chọn một dòng COMPLETED để xem lại kết quả chi tiết (UCSV04). |
| Luồng thay thế | 3a. Dòng IN_PROGRESS còn hạn: Hệ thống hiển thị nút 'Tiếp tục' dẫn tới UCSV07.<br>3b. Có thể bổ sung cột 'Kỳ thi' vào bảng (đề xuất, chưa được xác nhận trong SRS). |
| Luồng ngoại lệ | 2a. student_id khác người đăng nhập: Hệ thống trả HTTP 403.<br>3c. Sinh viên chưa có phiên nào: Hệ thống hiển thị trạng thái rỗng 'Bạn chưa có bài thi nào'. |
| Quy tắc nghiệp vụ liên quan | BR-10, BR-11, BR-16, SRS Mục 15.4 (STUDENT chỉ xem hồ sơ của chính mình). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên có 2 phiên (1 COMPLETED, 1 ABANDONED) When mở Lịch sử Then thấy đúng 2 dòng với trạng thái tương ứng, phiên mới nhất ở trên cùng.<br>- Given sinh viên chọn dòng COMPLETED When bấm vào dòng đó Then được chuyển tới trang kết quả của đúng phiên đó.<br>- Given sinh viên sửa student_id trong URL thành của người khác When gửi yêu cầu Then hệ thống trả HTTP 403. |

### Bảng đặc tả / Danh mục 20

| Use Case ID | UCSV07 |
| --- | --- |
| Tên chức năng | Tiếp tục bài thi bị gián đoạn |
| Mô tả | Sinh viên quay lại phiên thi đang dở (mất mạng, đóng trình duyệt, tải lại trang) và làm tiếp từ câu chưa trả lời, trong thời hạn của phiên. |
| Tác nhân | Sinh viên |
| Điều kiện trước | Sinh viên đã đăng nhập. Có một phiên TestSession ở trạng thái IN_PROGRESS của chính sinh viên và thời điểm hiện tại còn nhỏ hơn expires_at của phiên. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Phiên tiếp tục từ đúng trạng thái trước khi gián đoạn (θ, SE, các câu đã trả lời); đồng hồ vẫn tính theo expires_at đã chốt lúc bắt đầu, không được cấp lại thời gian. |
| Luồng chính | 1. Sinh viên mở trang chủ; hệ thống gọi GET /sessions/active và phát hiện phiên IN_PROGRESS, hiển thị thẻ 'Tiếp tục bài thi' kèm tên kỳ thi và thời gian còn lại (tính theo expiresAt).<br>2. Sinh viên bấm 'Tiếp tục'.<br>3. Hệ thống kiểm tra phiên thuộc sinh viên, trạng thái IN_PROGRESS và now < expires_at.<br>4. Hệ thống gọi GET /sessions/:id/resume để lấy lại trạng thái phiên: ưu tiên đọc SessionCacheState trong Redis (TTL 7200 giây).<br>5. Hệ thống trả về câu hỏi hiện tại chưa được trả lời (không lặp lại các câu đã trả lời), số câu đã làm và thời gian còn lại.<br>6. Sinh viên làm tiếp ở giao diện làm bài (/exam/[sessionId]) theo UCSV03. |
| Luồng thay thế | 4a. Cache Redis không còn (hết TTL hoặc Redis khởi động lại): Hệ thống dựng lại trạng thái từ PostgreSQL (nguồn dữ liệu gốc: các SessionResponse đã ghi) bằng cách chạy lại EAP trên các câu đã trả lời, rồi ghi lại cache và tiếp tục như bình thường.<br>1a. Sinh viên vừa vào UCSV02 mà đã có phiên dở của chính kỳ thi đó: Hệ thống trả 409 kèm sessionId và chuyển sang UCSV07 (UCSV02 luồng thay thế 4a). |
| Luồng ngoại lệ | 3a. Đã quá expires_at: Hệ thống không cho tiếp tục và áp dụng luật K5 — làm ≥ 8 câu thì phiên COMPLETED với stoppingReason = TIMEOUT, làm < 8 câu thì ABANDONED (cho thi lại nếu kỳ thi còn mở).<br>3b. Phiên không thuộc sinh viên đang đăng nhập: HTTP 403.<br>3c. Phiên đã COMPLETED: Hệ thống chuyển sinh viên sang trang kết quả (UCSV04).<br>4b. Không dựng lại được trạng thái (dữ liệu hỏng): Hệ thống báo lỗi HTTP 500 có thể thử lại và ghi log; không tự hủy phiên. |
| Quy tắc nghiệp vụ liên quan | BR-10, BR-11 (expires_at tính một lần, luật K5), SRS Mục 6 (Dual-Write Redis + PostgreSQL), yêu cầu phi chức năng phục hồi phiên ≤ 7200 giây. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given sinh viên đã trả lời 10 câu rồi mất mạng và quay lại sau 5 phút (còn hạn) When bấm Tiếp tục Then nhận đúng câu thứ 11, θ và SE giữ nguyên như trước khi gián đoạn.<br>- Given Redis đã mất khóa phiên nhưng PostgreSQL còn 10 câu trả lời When gọi resume Then hệ thống dựng lại trạng thái từ PostgreSQL và trả cùng kết quả như khi còn cache.<br>- Given phiên đã quá expires_at với 6 câu đã làm When sinh viên cố tiếp tục Then hệ thống chuyển phiên sang ABANDONED và không trả câu hỏi mới. |

### Bảng đặc tả / Danh mục 21

| Use Case ID | UCGV01 |
| --- | --- |
| Tên chức năng | Đăng nhập hệ thống (Giảng viên) |
| Mô tả | Cho phép giảng viên xác thực bằng Email và Mật khẩu để vào các chức năng báo cáo, tra cứu hồ sơ và Hộp việc duyệt câu hỏi. |
| Tác nhân | Giảng viên |
| Điều kiện trước | Giảng viên đã có tài khoản do Admin cấp (tạo lẻ hoặc import UCADM08), tài khoản đang hoạt động. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Giảng viên nhận access token và refresh token, được chuyển tới trang chủ giảng viên hoặc trang Đổi mật khẩu bắt buộc. |
| Luồng chính | 1. Giảng viên truy cập trang đăng nhập (/login).<br>2. Giảng viên nhập Email và Mật khẩu.<br>3. Hệ thống kiểm tra tài khoản tồn tại và còn hoạt động (isActive).<br>4. Hệ thống đối chiếu mật khẩu với bản băm argon2.<br>5. Hệ thống kiểm tra cờ mustChangePassword. Cờ bằng false.<br>6. Hệ thống cấp access token (JWT) và refresh token, kèm role TEACHER.<br>7. Hệ thống chuyển giảng viên tới trang chủ giảng viên (báo cáo lớp học); menu dựng theo role. Nếu giảng viên đang được giao việc duyệt/xác nhận, Hộp việc hiển thị số việc cần xử lý. |
| Luồng thay thế | 5a. Cờ mustChangePassword = true (lần đầu hoặc vừa được cấp lại mật khẩu tạm): Hệ thống cấp token tạm chỉ dùng cho đổi mật khẩu và chuyển sang /change-password; giảng viên thực hiện UCSV08.<br>2a. Giảng viên quên mật khẩu: chọn 'Quên mật khẩu' để thực hiện UCSV09. |
| Luồng ngoại lệ | 3a. Email không tồn tại hoặc sai mật khẩu: HTTP 401 ('Email hoặc mật khẩu không chính xác'), không tiết lộ yếu tố nào sai.<br>3b. Mật khẩu đúng nhưng tài khoản bị khóa (isActive = false): HTTP 403 ('Tài khoản đã bị vô hiệu hóa, vui lòng liên hệ Quản trị viên'). Nếu mật khẩu sai thì luôn trả 401 như 3a, để không lộ tài khoản nào đang bị khóa.<br>3c. Nhập sai mật khẩu liên tiếp vượt ngưỡng: hệ thống tạm khóa đăng nhập theo (IP + email) 5 lần/phút và theo IP 100 lần đăng nhập sai/10 phút (HTTP 429; ngưỡng cấu hình, chốt 09/11/2026). |
| Quy tắc nghiệp vụ liên quan | BR-02 (email duy nhất), BR-06 (mustChangePassword), BR-19 (isActive chặn đăng nhập), SRS Mục 15.3 (argon2, JWT, refresh token rotation). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given giảng viên có tài khoản active và mật khẩu đúng When gửi yêu cầu đăng nhập Then hệ thống trả về HTTP 200 kèm access token và refresh token, chuyển đến trang chủ giảng viên.<br>- Given tài khoản có mustChangePassword = true When xác thực thành công Then hệ thống chuyển hướng sang /change-password và chặn mọi API nghiệp vụ khác (403 PASSWORD_CHANGE_REQUIRED).<br>- Given tài khoản bị khóa (isActive = false) When đăng nhập với mật khẩu đúng Then hệ thống từ chối với HTTP 403 và không cấp token. |

### Bảng đặc tả / Danh mục 22

| Use Case ID | UCGV02 |
| --- | --- |
| Tên chức năng | Xem danh sách câu hỏi (Item Bank) |
| Mô tả | Giảng viên xem, lọc và đọc chi tiết các câu hỏi thuộc phạm vi công việc của mình để phục vụ chuyên môn; chỉ đọc, không có thao tác thêm, sửa hay xóa. |
| Tác nhân | Giảng viên |
| Điều kiện trước | Giảng viên đã đăng nhập (mustChangePassword = false). Giảng viên đang được Admin giao việc duyệt (vai A) hoặc xác nhận (vai B) ít nhất một lô; nếu chưa được giao thì danh sách rỗng. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Danh sách và chi tiết câu hỏi được hiển thị đúng phạm vi phân quyền; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Giảng viên mở màn Ngân hàng câu hỏi (/teacher/item-bank, chế độ chỉ xem) và hệ thống gọi GET /items.<br>2. Hệ thống chỉ trả về các câu thuộc phạm vi được giao cho giảng viên: câu giao cho GV vai A, hoặc câu hỏi được phân công thẩm định cho GV B (confirmerId = currentUserId).<br>3. Giảng viên lọc theo kỹ năng (Vocabulary/Grammar), mức CEFR, trạng thái, lô và tìm theo nội dung.<br>4. Giảng viên chọn một câu để xem chi tiết (GET /items/:id): nội dung, 4 phương án, đáp án đúng, giải thích AI, trạng thái, lô nguồn, người duyệt/xác nhận.<br>5. Từ chi tiết, giảng viên vai A đang có câu ở trạng thái DRAFT có thể chuyển sang chỉnh sửa trong quy trình duyệt (UCGV04 / UCGV14); các trường hợp khác chỉ xem. |
| Luồng thay thế | 3a. Câu mà GV A đã sửa: Hệ thống hiển thị thêm bản gốc đối chiếu bản sửa. |
| Luồng ngoại lệ | 2a. Giảng viên yêu cầu câu ngoài phạm vi được giao: Hệ thống trả HTTP 403 NOT_ASSIGNED.<br>2b. Câu ở trạng thái AI_REJECTED: không hiển thị cho giảng viên (chỉ Admin xem, BR-29).<br>4a. Mọi API thêm, sửa, xóa câu hỏi ngoài quy trình duyệt: Hệ thống từ chối (HTTP 403/405); câu FINAL_APPROVED cấm sửa và xóa (BR-30). |
| Quy tắc nghiệp vụ liên quan | BR-16 (phân quyền theo phân công), BR-21 (câu chỉ vào ngân hàng qua lô), BR-29 (câu AI_REJECTED chỉ Admin xem), BR-30 (FINAL_APPROVED cấm sửa/xóa). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given giảng viên A được giao 20 câu trong lô L1 When mở danh sách Then chỉ thấy 20 câu đó, không thấy câu của lô khác chưa giao.<br>- Given câu có trạng thái AI_REJECTED When giảng viên mở danh sách hoặc gọi trực tiếp GET /items/:id Then hệ thống không trả câu đó.<br>- Given giảng viên gọi DELETE /items/:id Then hệ thống từ chối và không xóa câu nào. |

### Bảng đặc tả / Danh mục 23

| Use Case ID | UCGV04 |
| --- | --- |
| Tên chức năng | Chỉnh sửa câu hỏi |
| Mô tả | Giảng viên vai A chỉnh sửa nội dung, bốn phương án, đáp án đúng hoặc giải thích của câu được giao trong lúc duyệt; bản sửa phải qua kiểm tra lại trước khi được lưu. |
| Tác nhân | Giảng viên (vai A) |
| Điều kiện trước | Lô câu hỏi đang IN_REVIEW. Câu đang ở trạng thái DRAFT và được giao đúng cho giảng viên này (ItemReviewAssignment). Chưa quá hạn xử lý hoặc quá hạn chỉ bị cảnh báo. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Bản sửa được lưu kèm dấu hiệu "A đã sửa" (băm nội dung đổi) để GV vai B và bước C3 đối chiếu; câu vẫn ở trạng thái DRAFT cho đến khi giảng viên Duyệt hoặc Từ chối. |
| Luồng chính | 1. Trong lúc duyệt (UCGV14), GV A mở chi tiết câu được giao (/teacher/tasks/reviews/[batchId]?item=[itemId]).<br>2. GV A chọn 'Sửa' và thay đổi nội dung, 4 phương án, đáp án đúng hoặc giải thích.<br>3. GV A bấm 'Lưu sửa' (PATCH /items/:id).<br>4. Hệ thống kiểm tra quyền (đúng người được giao, câu DRAFT).<br>5. Hệ thống chạy lại luật cứng và lọc trùng T1–T2 trên bản sửa (BR-27).<br>6. Bản sửa hợp lệ: hệ thống lưu, cập nhật băm nội dung và giữ lại bản gốc để đối chiếu (diff cho GV B và Admin).<br>7. GV A tiếp tục Duyệt hoặc Từ chối câu theo UCGV14. |
| Luồng thay thế | 2a. GV A không sửa gì và duyệt thẳng: bỏ qua các bước 2–6. |
| Luồng ngoại lệ | 4a. Người gọi không phải GV A được giao: HTTP 403 NOT_ASSIGNED.<br>4b. Câu không còn ở DRAFT (đã duyệt hoặc đã FINAL_APPROVED): Hệ thống từ chối (HTTP 409/403), câu FINAL_APPROVED cấm sửa (BR-30).<br>5a. Bản sửa sai luật cứng (thiếu phương án, đáp án không duy nhất...): HTTP 422 INVALID_AFTER_EDIT, không lưu và chặn Duyệt.<br>5b. Bản sửa trùng với câu đã có (T1–T2): HTTP 422 DUPLICATE_AFTER_EDIT, không lưu. |
| Quy tắc nghiệp vụ liên quan | BR-16, BR-27 (kiểm tra lại sau khi sửa), BR-30 (FINAL_APPROVED cấm sửa), BR-21. UCGV04 là bước con của UCGV14 (không phải chức năng sửa độc lập ngoài quy trình duyệt). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given GV A sửa đáp án của câu được giao thành đáp án hợp lệ và không trùng When bấm Lưu sửa Then hệ thống lưu bản sửa, đánh dấu câu đã được A sửa và giữ bản gốc.<br>- Given bản sửa làm câu trùng T2 với câu khác trong ngân hàng When bấm Lưu sửa Then hệ thống trả 422 DUPLICATE_AFTER_EDIT và câu giữ nguyên nội dung cũ.<br>- Given GV B (hoặc Admin) gọi PATCH /items/:id trên câu của lô Then hệ thống từ chối với HTTP 403. |

### Bảng đặc tả / Danh mục 24

| Use Case ID | UCGV07 |
| --- | --- |
| Tên chức năng | Xem báo cáo lớp học |
| Mô tả | Giảng viên xem báo cáo tổng hợp kết quả chẩn đoán của sinh viên: phân phối mức CEFR và các chủ đề sai phổ biến, có thể lọc theo kỳ thi. |
| Tác nhân | Giảng viên |
| Điều kiện trước | Giảng viên đã đăng nhập (mustChangePassword = false). Hệ thống đã có ít nhất một phiên COMPLETED để thống kê. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Báo cáo hiển thị đúng dữ liệu theo bộ lọc; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Giảng viên mở mục Báo cáo lớp (/teacher/reports).<br>2. Hệ thống mặc định hiển thị báo cáo toàn hệ thống (mọi kỳ thi) theo BR-13.<br>3. Giảng viên chọn bộ lọc 'Kỳ thi' (examRoundId) nếu muốn xem riêng một kỳ.<br>4. Hệ thống gọi GET /reports/class-distribution?examRoundId= và GET /reports/error-patterns để tổng hợp từ các phiên COMPLETED.<br>5. Hệ thống hiển thị: số sinh viên đã hoàn thành, phân phối theo mức CEFR (biểu đồ cột/tỷ lệ), danh sách chủ đề sai phổ biến (error patterns) theo kỹ năng.<br>6. Giảng viên có thể chọn 'Xuất CSV' để thực hiện UCGV08. |
| Luồng thay thế | 3a. Giảng viên đổi kỳ thi trong bộ lọc: Hệ thống tải lại số liệu theo kỳ mới; chọn 'Tất cả' để quay về toàn hệ thống. |
| Luồng ngoại lệ | 4a. Kỳ thi được lọc chưa có phiên COMPLETED: Hệ thống hiển thị trạng thái rỗng 'Chưa có dữ liệu cho kỳ thi này'.<br>4b. examRoundId không tồn tại: HTTP 404.<br>4c. Người dùng role STUDENT gọi API báo cáo: HTTP 403. |
| Quy tắc nghiệp vụ liên quan | BR-13 (lọc theo kỳ, mặc định toàn hệ thống), BR-16 (phân quyền theo role), SRS Mục 15.4. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given hệ thống có 80 phiên COMPLETED thuộc 2 kỳ thi When giảng viên mở báo cáo không lọc Then số liệu tính trên cả 80 phiên.<br>- Given giảng viên chọn lọc theo kỳ thi K1 When tải báo cáo Then phân phối CEFR chỉ tính trên các phiên COMPLETED của K1.<br>- Given sinh viên gọi GET /reports/class-distribution When gửi yêu cầu Then hệ thống trả HTTP 403. |

### Bảng đặc tả / Danh mục 25

| Use Case ID | UCGV08 |
| --- | --- |
| Tên chức năng | Xuất báo cáo CSV |
| Mô tả | Giảng viên xuất dữ liệu báo cáo lớp học đang xem ra tệp CSV để lưu trữ hoặc xử lý thêm. |
| Tác nhân | Giảng viên |
| Điều kiện trước | Giảng viên đang xem báo cáo lớp học (UCGV07) và báo cáo có dữ liệu. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Tệp CSV được tải về đúng với bộ lọc đang áp dụng; không thay đổi dữ liệu hệ thống. |
| Luồng chính | 1. Từ báo cáo lớp học (UCGV07), giảng viên bấm 'Xuất CSV' — quan hệ <<extend>> của UCGV07.<br>2. Hệ thống lấy lại dữ liệu theo đúng bộ lọc hiện hành (kỳ thi hoặc toàn hệ thống).<br>3. Hệ thống chuẩn hóa từng ô văn bản: ô bắt đầu bằng ký tự =, +, - hoặc @ được vô hiệu hóa (thêm tiền tố) để chống CSV injection.<br>4. Hệ thống trả tệp CSV (mã hóa UTF-8) và trình duyệt tải về, tên tệp có kỳ thi (nếu lọc) và ngày xuất. |
| Luồng thay thế | 2a. Báo cáo không có dữ liệu: Hệ thống vẫn xuất tệp chỉ có dòng tiêu đề, kèm thông báo 'Không có dữ liệu để xuất'. |
| Luồng ngoại lệ | 2b. Người dùng không đủ quyền (STUDENT): HTTP 403.<br>4a. Lỗi tạo tệp: Hệ thống báo 'Không thể xuất báo cáo, vui lòng thử lại' và ghi log; không để lại tệp dở. |
| Quy tắc nghiệp vụ liên quan | BR-13 (lọc theo kỳ), BR-16, SRS Mục 15.3 (chống CSV injection). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given giảng viên đang lọc kỳ thi K1 When bấm Xuất CSV Then tệp chỉ chứa dữ liệu của K1, cùng số liệu với màn hình báo cáo.<br>- Given dữ liệu có chuỗi bắt đầu bằng '=' (ví dụ chủ đề '=SUM(A1)') When xuất CSV Then ô đó được vô hiệu hóa, mở bằng Excel không thực thi công thức.<br>- Given báo cáo không có dữ liệu When bấm Xuất CSV Then tệp chỉ có dòng tiêu đề. |

### Bảng đặc tả / Danh mục 26

| Use Case ID | UCGV09 |
| --- | --- |
| Tên chức năng | Xem hồ sơ năng lực sinh viên |
| Mô tả | Giảng viên tra cứu một sinh viên theo MSSV và xem hồ sơ năng lực (LanguageProfile) cùng lịch sử các lần thi của sinh viên đó. |
| Tác nhân | Giảng viên |
| Điều kiện trước | Giảng viên đã đăng nhập (mustChangePassword = false). Sinh viên cần tra cứu đã có tài khoản. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Hồ sơ năng lực và lịch sử của sinh viên được hiển thị; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Giảng viên mở mục Tìm sinh viên (/teacher/students) và nhập chính xác MSSV.<br>2. Hệ thống tìm sinh viên theo MSSV và kiểm tra quyền (TEACHER và ADMIN được đọc hồ sơ của mọi sinh viên trong trường).<br>3. Hệ thống gọi GET /placement-profiles/:student_id và hiển thị hồ sơ mới nhất (/teacher/students/[code]): mức CEFR, θ và SE, điểm từng kỹ năng, chủ đề yếu, gợi ý, vùng biên.<br>4. Giảng viên xem lịch sử các lần thi của sinh viên (GET /placement-profiles/:student_id/history) và mở chi tiết từng lần. |
| Luồng thay thế | 1a. Tra cứu theo tên hoặc tìm gần đúng: chưa nằm trong phạm vi hiện tại (câu hỏi mở O6), hiện chỉ tra cứu theo MSSV chính xác. |
| Luồng ngoại lệ | 2a. MSSV không tồn tại: Hệ thống báo 'Không tìm thấy sinh viên' (HTTP 404).<br>3a. Sinh viên chưa có hồ sơ (chưa hoàn thành phiên nào): Hệ thống hiển thị 'Sinh viên chưa có kết quả bài thi'.<br>2b. Người dùng role STUDENT cố xem hồ sơ của sinh viên khác: HTTP 403. |
| Quy tắc nghiệp vụ liên quan | BR-16 (TEACHER xem hồ sơ sinh viên), SRS Mục 15.4 (ProfileAccessGuard), BR-02 (MSSV duy nhất). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given giảng viên nhập MSSV hợp lệ có 2 lần thi When tra cứu Then thấy hồ sơ mới nhất và lịch sử 2 lần thi.<br>- Given MSSV không tồn tại When tra cứu Then nhận thông báo không tìm thấy, không lộ dữ liệu khác.<br>- Given sinh viên A đã đăng nhập When gọi GET /placement-profiles/ của sinh viên B Then hệ thống trả HTTP 403. |

### Bảng đặc tả / Danh mục 27

| Use Case ID | UCADM01 |
| --- | --- |
| Tên chức năng | Đăng nhập hệ thống (Quản trị viên) |
| Mô tả | Cho phép quản trị viên xác thực bằng Email và Mật khẩu để vào các chức năng quản trị: tài khoản, kỳ thi, lô câu hỏi và báo cáo. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Quản trị viên đã có tài khoản role ADMIN (tạo bằng seed ban đầu hoặc được nâng quyền bởi Admin khác, UCADM09), tài khoản đang hoạt động. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Quản trị viên nhận access token và refresh token, được chuyển tới trang chủ quản trị hoặc trang Đổi mật khẩu bắt buộc. |
| Luồng chính | 1. Quản trị viên truy cập trang đăng nhập (/login).<br>2. Quản trị viên nhập Email và Mật khẩu.<br>3. Hệ thống kiểm tra tài khoản tồn tại và còn hoạt động (isActive).<br>4. Hệ thống đối chiếu mật khẩu với bản băm argon2.<br>5. Hệ thống kiểm tra cờ mustChangePassword. Cờ bằng false.<br>6. Hệ thống cấp access token (JWT) và refresh token, kèm role ADMIN.<br>7. Hệ thống chuyển quản trị viên tới trang chủ quản trị; menu dựng theo role ADMIN (Admin dùng thêm các màn hình báo cáo/hồ sơ của giảng viên). |
| Luồng thay thế | 5a. Cờ mustChangePassword = true: Hệ thống cấp token tạm chỉ dùng đổi mật khẩu và chuyển sang /change-password (UCSV08).<br>2a. Quên mật khẩu: chọn 'Quên mật khẩu' (UCSV09). |
| Luồng ngoại lệ | 3a. Email không tồn tại hoặc sai mật khẩu: HTTP 401 ('Email hoặc mật khẩu không chính xác').<br>3b. Mật khẩu đúng nhưng tài khoản bị khóa (isActive = false): HTTP 403; mật khẩu sai luôn trả 401.<br>3c. Nhập sai mật khẩu liên tiếp vượt ngưỡng: tạm khóa theo (IP + email) và theo IP (HTTP 429; 5 lần/phút theo IP + email, 100 lần đăng nhập sai/10 phút theo IP). |
| Quy tắc nghiệp vụ liên quan | BR-02, BR-06, BR-18 (đổi quyền làm token cũ mất hiệu lực quyền cũ), BR-19, SRS Mục 15.3. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given quản trị viên có tài khoản active và mật khẩu đúng When gửi yêu cầu đăng nhập Then hệ thống trả về HTTP 200 kèm access token và refresh token, chuyển đến trang chủ quản trị.<br>- Given tài khoản có mustChangePassword = true When xác thực thành công Then hệ thống chuyển hướng sang /change-password và chặn mọi API nghiệp vụ khác (403 PASSWORD_CHANGE_REQUIRED).<br>- Given tài khoản bị khóa (isActive = false) When đăng nhập với mật khẩu đúng Then hệ thống từ chối với HTTP 403 và không cấp token. |

### Bảng đặc tả / Danh mục 28

| Use Case ID | UCADM04 |
| --- | --- |
| Tên chức năng | Xem hồ sơ năng lực sinh viên (Quản trị viên) |
| Mô tả | Quản trị viên tra cứu và xem hồ sơ năng lực cùng lịch sử thi của bất kỳ sinh viên nào trong trường; kế thừa UCGV09. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Quản trị viên đã đăng nhập (mustChangePassword = false). Sinh viên cần tra cứu đã có tài khoản. |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Hồ sơ năng lực và lịch sử được hiển thị; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Quản trị viên mở mục Tìm sinh viên (/teacher/students; Admin dùng chung giao diện giảng viên) và nhập MSSV.<br>2. Hệ thống tìm sinh viên và kiểm tra quyền (ADMIN là siêu tập của TEACHER trong việc xem kết quả).<br>3. Hệ thống hiển thị hồ sơ mới nhất theo UCGV09 bước 3.<br>4. Quản trị viên xem lịch sử các lần thi, mở chi tiết từng lần.<br>5. Từ hồ sơ, quản trị viên có thể mở nhanh trang quản lý tài khoản của sinh viên đó (UCADM09). |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 2a. MSSV không tồn tại: HTTP 404 'Không tìm thấy sinh viên'.<br>3a. Sinh viên chưa có kết quả: thông báo 'Sinh viên chưa có kết quả bài thi'. |
| Quy tắc nghiệp vụ liên quan | BR-16 (ADMIN xem mọi hồ sơ), BR-17, SRS Mục 15.4. Quan hệ: UCADM04 bao trùm UCGV09. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given Admin nhập MSSV của sinh viên đã thi When tra cứu Then thấy hồ sơ và lịch sử giống như giảng viên thấy ở UCGV09.<br>- Given sinh viên chưa thi lần nào When Admin tra cứu Then hệ thống hiển thị 'chưa có kết quả', không báo lỗi. |

### Bảng đặc tả / Danh mục 29

| Use Case ID | UCADM05 |
| --- | --- |
| Tên chức năng | Xem báo cáo tổng thể toàn trường |
| Mô tả | Quản trị viên xem báo cáo tổng hợp toàn hệ thống đơn trường: phân phối CEFR, chủ đề sai phổ biến, có thể lọc theo kỳ thi và xuất CSV; kế thừa UCGV07. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Quản trị viên đã đăng nhập (mustChangePassword = false). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Báo cáo hiển thị đúng dữ liệu theo bộ lọc; không thay đổi dữ liệu (chỉ đọc). |
| Luồng chính | 1. Quản trị viên mở trang tổng quan/báo cáo (/admin/dashboard).<br>2. Hệ thống mặc định hiển thị toàn hệ thống (mọi kỳ thi) theo BR-13.<br>3. Quản trị viên chọn bộ lọc 'Kỳ thi' nếu cần.<br>4. Hệ thống tổng hợp từ các phiên COMPLETED (GET /reports/class-distribution, GET /reports/error-patterns) và hiển thị: số sinh viên hoàn thành, phân phối CEFR, chủ đề sai phổ biến.<br>5. Quản trị viên có thể xuất CSV theo UCGV08 và liên kết sang theo dõi dự thi của kỳ đang lọc (UCADM17). |
| Luồng thay thế | Không có. |
| Luồng ngoại lệ | 4a. Chưa có phiên COMPLETED: hiển thị trạng thái rỗng.<br>3a. examRoundId không tồn tại: HTTP 404. |
| Quy tắc nghiệp vụ liên quan | BR-13, BR-16, SRS Mục 15.4. Phạm vi: chỉ báo cáo; chức năng cấu hình hệ thống (UCADM07) nằm ngoài phạm vi Tiểu luận. Quan hệ: UCADM05 bao trùm UCGV07. |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given hệ thống có 120 phiên COMPLETED thuộc 3 kỳ thi When Admin mở báo cáo không lọc Then số liệu tính trên cả 120 phiên.<br>- Given Admin lọc kỳ thi K2 When tải lại Then số liệu chỉ tính trên các phiên COMPLETED của K2. |

### Bảng đặc tả / Danh mục 30

| Use Case ID | UCADM06 |
| --- | --- |
| Tên chức năng | Quản lý toàn bộ ngân hàng câu hỏi |
| Mô tả | Quản trị viên giám sát toàn bộ ngân hàng câu hỏi: xem, lọc và đọc chi tiết mọi câu cùng lịch sử kiểm tra và duyệt; Admin không sửa, không duyệt nội dung câu và không xóa. |
| Tác nhân | Quản trị viên |
| Điều kiện trước | Quản trị viên đã đăng nhập (mustChangePassword = false). |
| Điều kiện tiên quyết<br>(Hậu điều kiện) | Danh sách và chi tiết câu hỏi hiển thị đầy đủ; không thay đổi dữ liệu câu hỏi (chỉ đọc). Việc tạo lô hoặc xử lý lô được thực hiện ở UCADM11–14. |
| Luồng chính | 1. Quản trị viên mở Ngân hàng câu hỏi (/admin/item-bank).<br>2. Hệ thống trả về danh sách mọi câu hỏi (GET /items) kèm thống kê theo trạng thái.<br>3. Quản trị viên lọc theo kỹ năng, mức CEFR, trạng thái, nguồn lô (AI_GENERATED / IMPORTED, lấy từ ItemBatch.source), lô và tìm theo nội dung.<br>4. Quản trị viên chọn một câu để xem chi tiết chỉ đọc (GET /items/:id): nội dung, đáp án, giải thích, trạng thái, lô nguồn, kết quả kiểm tra AI C1/C2/C3 (mã lý do, câu nghi trùng), bản gốc so với bản GV A đã sửa, người duyệt/xác nhận/import và lịch sử sự kiện.<br>5. Quản trị viên chuyển nhanh tới 'Tạo lô bằng AI' (UCADM11), 'Import đề từ file' (UCADM12) hoặc danh sách lô cần xử lý (UCADM13, UCADM14). |
| Luồng thay thế | 3a. Xem câu bị máy loại: Quản trị viên mở tab 'AI đã loại' của lô (GET /item-batches/:id/ai-rejected) để xem câu AI_REJECTED kèm mã lý do (GV không xem được các câu này, BR-29). |
| Luồng ngoại lệ | 4a. Quản trị viên cố sửa nội dung, duyệt hoặc xóa câu: Hệ thống không cung cấp thao tác này; gọi trực tiếp API sẽ bị từ chối (HTTP 403).<br>4b. Câu FINAL_APPROVED: cấm sửa và xóa (BR-30). |
| Quy tắc nghiệp vụ liên quan | BR-16, BR-21 (không form thêm từng câu), BR-29, BR-30; DC-29 (Admin không sửa/duyệt nội dung câu). |
| Tiêu chí chấp nhận<br>(Acceptance Criteria) | - Given ngân hàng có 500 câu từ 3 lô When Admin lọc theo nguồn IMPORTED Then danh sách chỉ gồm các câu thuộc lô có ItemBatch.source = IMPORTED.<br>- Given câu FINAL_APPROVED When Admin xem chi tiết Then thấy người duyệt, người xác nhận, thời điểm import và kết quả C1/C2/C3, không có nút Sửa/Xóa.<br>- Given Admin gọi PATCH /items/:id Then hệ thống trả HTTP 403 và nội dung câu không đổi. |