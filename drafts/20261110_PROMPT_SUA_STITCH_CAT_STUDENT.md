# BỘ PROMPT SỬA STITCH: NHÓM "LÀM BÀI THI CAT" (STUDENT)

> **Ngày:** 10/11/2026 · **Trạng thái:** DRAFT (chưa chạy trên Stitch)
> **Project Stitch:** English Placement Test UI (`16753573200013570369`)
> **Căn cứ:** Quyết định #134 (Q-A…Q-D) và `20261110_CAN_CHOT_UI_STITCH_CAT_STUDENT_v2.md`
> **Cách dùng:** mỗi màn một lần `edit_screens` (hoặc dán vào ô chat của Stitch), chạy theo thứ tự S04 → S02 → S03 → S05 → S07 → S06. Sau mỗi màn, kiểm tra lại HTML rồi mới sang màn kế.

## Quy tắc chung (dán kèm đầu mỗi prompt)

```
Giữ nguyên phong cách hiện tại (màu #2563EB, font Be Vietnam Pro, bố cục, thành phần). Chỉ thay đổi đúng những điểm nêu bên dưới. Giữ nguyên mọi thuộc tính data-testid và data-path đang có. Toàn bộ nội dung bằng tiếng Việt. Không thêm tính năng ngoài danh sách.
```

## Bảng route chuẩn (dùng cho mọi `href`)

| Chức năng | Route |
|---|---|
| Trang chủ SV | `/student/dashboard` |
| Giới thiệu bài thi (S03) | `/student/exams/{roundId}` |
| Làm bài (S04) | `/student/exams/{roundId}/take` |
| Kết quả (S05) | `/student/results/{sessionId}` |
| Xem lại đáp án (S06) | `/student/results/{sessionId}/review` |
| Lịch sử (S07) | `/student/history` |
| Đổi mật khẩu | `/change-password` |

---

## 1. S04 – Làm bài thi (`5191ec16bf9a4cb498b78e5319f4daec`) — ưu tiên cao nhất

```
1. Bỏ trạng thái chọn sẵn: khi vào câu hỏi, KHÔNG có phương án nào được chọn (không có đáp án A mặc định, aria-checked="false" cho cả 4, biến lưu lựa chọn khởi tạo rỗng).
2. Nút "Nộp đáp án" (data-testid="submit-answer") ở trạng thái vô hiệu (disabled, màu xám) cho đến khi người dùng chọn một phương án. Phím Enter chỉ nộp khi đã chọn phương án; nếu chưa chọn thì không làm gì.
3. Thêm các biến thể trạng thái (hiển thị bằng cách chuyển đổi trong mã, không cần màn riêng):
   a. Còn dưới 5 phút: đồng hồ (data-testid="timer") đổi sang nền đỏ nhạt, chữ và viền đỏ #DC2626.
   b. Hết giờ: khóa cả 4 phương án và nút nộp, hiện thông báo "Đã hết thời gian. Hệ thống đang ghi nhận kết quả của bạn..." kèm biểu tượng đang xử lý.
   c. Mất kết nối: hiện thanh cảnh báo màu cam phía trên "Mất kết nối mạng. Đáp án của bạn được giữ tạm và sẽ gửi lại khi có mạng." Nút nộp chuyển thành "Đang chờ kết nối" (disabled).
   d. Lỗi nộp: hiện thông báo lỗi dưới nút "Không gửi được đáp án. Vui lòng thử lại." và cho phép bấm lại.
4. Đồng hồ chạy ngược từ cùng một giá trị khởi tạo với giá trị hiển thị ban đầu (hiện đang hiển thị 21:44 nhưng đếm từ 24:15; thống nhất một giá trị).
5. Không thêm bố cục đọc hiểu (không có đoạn văn bên trái). Chỉ câu trắc nghiệm ngắn.
6. Giữ layout không header/footer (phòng thi tập trung).
```

## 2. S02 – Trang chủ (`4263dbd27067441298730195430d7569`)

```
1. Banner bài thi dở dang (data-testid="resume-banner"): thêm tên kỳ thi, ví dụ "Bạn đang có bài thi dở dang tại kỳ XẾP LỚP ANH VĂN ĐẦU KHÓA K2026". Giữ "Đã làm 7 câu · còn 24:15". Nút "Tiếp tục bài thi" (data-testid="resume-btn") trỏ tới /student/exams/{roundId}/take.
2. Khi đang có bài thi dở dang của kỳ nào, thẻ kỳ đó (data-testid="round-card-1") KHÔNG hiện nút "Bắt đầu bài thi". Thay bằng nút vô hiệu "Đang có bài thi dở" hoặc nút "Tiếp tục bài thi" (cùng đích với banner). Mục đích: không cho tạo phiên mới khi còn phiên dở.
3. Thêm một biến thể của banner khi phiên đã hết hạn: ẩn nút "Tiếp tục bài thi", hiện dòng "Phiên thi đã hết thời gian. Hệ thống đang ghi nhận kết quả của bạn." và một dòng nhỏ "Vui lòng tải lại sau ít phút".
4. Thẻ kỳ "Chưa mở" (XẾP LỚP BỔ SUNG ĐỢT 2): đổi thời điểm mở sang ngày trong tương lai so với 10/11/2026 (ví dụ "Mở lúc 14:00, 25/11/2026").
5. Thẻ "Kết quả gần nhất": đổi dữ liệu mẫu cho khớp màn Lịch sử: kỳ "Kỳ thi Xếp lớp Anh văn Đầu khóa K2026", ngày 12/10/2026, 25 câu, CEFR B1, Theta ước lượng +0.28.
6. Gắn liên kết thật thay cho href="#":
   - Logo và "Trang chủ" → /student/dashboard
   - "Lịch sử bài thi" (menu và liên kết trong khối Kết quả gần nhất) → /student/history
   - "Bắt đầu bài thi" → /student/exams/{roundId}
   - "Chi tiết" (kỳ đã thi) và "Xem kết quả" → /student/results/{sessionId}
   - "Đổi mật khẩu" → /change-password
```

## 3. S03 – Giới thiệu bài thi (`46e63b7d2b7a4d54b96eca523c52480b`)

```
1. Bỏ nhãn "Phòng thi số 04" (hệ thống không có khái niệm phòng thi).
2. Sửa quy tắc số 2 thành: "Bạn có tối đa 45 phút để làm bài. Thời gian này không vượt quá giờ đóng kỳ thi (11:30), nên nếu vào muộn bạn chỉ còn phần thời gian còn lại." Đồng bộ với dòng phía trên "Kỳ đóng lúc 11:30 hôm nay (còn 45 phút)".
3. Thêm một dòng ngay trên nút bắt đầu: "Đồng hồ chỉ bắt đầu chạy khi bạn bấm 'Tôi đã hiểu, bắt đầu làm bài'."
4. Nút bắt đầu (data-testid="confirm-start") trỏ tới /student/exams/{roundId}/take (thay vì /student/exams/round-k2026/test). Nút "Quay lại" (data-testid="intro-back") trỏ tới /student/dashboard.
5. Thêm các biến thể thông báo lỗi (hộp thông báo thay cho phần nút bắt đầu):
   - Không có tên trong danh sách kỳ thi: "Bạn không nằm trong danh sách dự thi của kỳ này."
   - Kỳ chưa mở hoặc đã đóng: "Kỳ thi chưa mở hoặc đã đóng."
   - Đã thi xong kỳ này: "Bạn đã hoàn thành kỳ thi này." kèm nút "Xem kết quả".
   - Đang có bài thi dở: "Bạn đang có bài thi dở dang." kèm nút "Tiếp tục bài thi".
6. Gắn liên kết thật cho menu (Trang chủ → /student/dashboard, Lịch sử bài thi → /student/history, Đổi mật khẩu → /change-password).
```

## 4. S05 – Kết quả bài thi (`11035123aa954b68bf6c451a39cbf518`)

```
1. Phần "Năng lực theo hợp phần ngôn ngữ": mỗi kỹ năng chỉ hiển thị "Số câu đúng / tổng số câu". Ví dụ "Từ vựng (Vocabulary): 9/13 câu", "Ngữ pháp (Grammar): 7/12 câu". BỎ thanh tiến trình %, BỎ số phần trăm, BỎ nhãn "Ước lượng B1" / "Ước lượng A2". Giữ data-testid="skill-vocab" và "skill-grammar". Chỉ giữ CEFR tổng ở khối đầu trang.
2. Dưới thang CEFR 6 nấc, thêm dòng "θ = +0.28 ± 0.31 (SE)" (cùng dữ liệu mẫu với màn Lịch sử: B1, θ +0.28, SE 0.31).
3. Thêm dòng "Lý do kết thúc bài thi" dưới khối CEFR tổng, ví dụ "Đạt ngưỡng tin cậy (SE < 0.35)". Thêm 3 biến thể thay thế để thể hiện bằng phương án chuyển đổi: "Đủ 25 câu", "Kết thúc sớm do năng lực nằm ngoài vùng đo", "Hết thời gian làm bài".
4. Thêm biến thể banner cảnh báo vùng biên ở đầu trang khi kết quả thuộc Pre-A1 hoặc C1+: "Kết quả nằm ở vùng biên của thang đo. Mức này có thể chưa phản ánh chính xác năng lực của bạn, hãy trao đổi với giáo viên khi xếp lớp." Màu cam nhạt.
5. Nhãn "Độ tin cậy": giữ, nhưng ghi nhỏ bên cạnh "(dựa trên sai số chuẩn SE)".
6. Xóa hoàn toàn Khối 5 "Gợi ý học tập cá nhân hóa từ AI" (đang để trống) và mọi chỗ trống liên quan.
7. Nút "Xem giải thích chi tiết đáp án" (data-testid="open-review") trỏ tới /student/results/{sessionId}/review. "Về trang chủ sinh viên" trỏ tới /student/dashboard.
```

## 5. S07 – Lịch sử bài thi (`9139276e902b46838362f8d784ff7c88`)

```
1. Cột "Trạng thái": ngoài "Hoàn thành", thêm hai biến thể: "Bỏ dở" (xám; dòng đó có CEFR/θ/SE hiển thị "—" và KHÔNG có nút "Xem chi tiết") và "Hết giờ" (cam nhạt; vẫn có kết quả). Thêm một dòng mẫu "Bỏ dở" (ví dụ 8 câu chưa đủ, ngày 03/03/2026) vào cả bảng desktop và thẻ mobile.
2. Thêm trạng thái rỗng (khi chưa có lần thi nào): biểu tượng, "Bạn chưa có bài thi nào", "Khi bạn hoàn thành một kỳ thi, kết quả sẽ xuất hiện tại đây." kèm nút "Về trang chủ".
3. Thay anchor giả #xem-chi-tiet-* bằng /student/results/{sessionId}. Menu: Trang chủ → /student/dashboard, Lịch sử bài thi → /student/history, Đổi mật khẩu → /change-password.
4. Dữ liệu dòng đầu giữ khớp với màn Trang chủ: Kỳ thi Xếp lớp Anh văn Đầu khóa K2026, 12/10/2026, 25 câu, B1, +0.28, 0.31.
5. Thống kê "Tổng số đợt thi" và "Cấp độ hiện tại" tính theo các lần có kết quả (không tính "Bỏ dở").
```

## 6. S06 – Xem lại đáp án và giải thích AI (MÀN MỚI, dùng `generate_screen_from_text`)

```
Tạo màn mới "S06 - Xem lại đáp án và giải thích (Result Review)" cho sinh viên, cùng phong cách và App Shell (header có Trang chủ, Lịch sử bài thi, menu tài khoản) với các màn Student hiện có. Route: /student/results/{sessionId}/review.

Nội dung:
- Tiêu đề "Xem lại bài thi", dòng phụ tên kỳ thi và ngày thi. Nút "← Quay lại kết quả" (/student/results/{sessionId}).
- Danh sách các câu đã làm theo thứ tự làm bài (tối đa 25), mỗi câu là một thẻ có thể mở rộng: số thứ tự, kỹ năng (Từ vựng/Ngữ pháp), nội dung câu, huy hiệu "Đúng" (xanh lá) hoặc "Sai" (đỏ nhạt).
- Khi mở thẻ: 4 phương án A-D chỉ đọc; đánh dấu "Bạn đã chọn" và "Đáp án đúng"; bên dưới là thẻ "Giải thích" (nền xanh nhạt, biểu tượng bóng đèn) với phần giải thích của AI.
- Biến thể khi chưa có giải thích: "Câu này chưa có giải thích."
- Phía trên danh sách có bộ lọc: Tất cả / Chỉ câu sai, và lọc theo kỹ năng.
- Chỉ đọc: không có nút nộp, không có đồng hồ.
- Responsive: thẻ xếp dọc trên mobile, không cuộn ngang.
- Không hiện θ, SE hay độ khó của câu (chỉ hiện đúng/sai và giải thích).
- Gắn data-testid: "review-list", "review-item-{n}", "review-explanation-{n}", "review-filter".
```

---

## Kiểm tra sau khi sửa (checklist)

- [ ] S04: mở lên không có phương án nào được chọn; Enter khi chưa chọn không làm gì.
- [ ] S02: khi có banner dở dang, thẻ kỳ không còn nút "Bắt đầu bài thi".
- [ ] S03: không còn "Phòng thi số 04"; link `/take`; có dòng "đồng hồ chỉ bắt đầu khi bấm".
- [ ] S05: không còn `%` và nhãn CEFR theo kỹ năng; có lý do dừng, θ ± SE, biến thể vùng biên; Khối 5 đã xóa.
- [ ] S07: có biến thể "Bỏ dở", "Hết giờ", trạng thái rỗng; dữ liệu dòng đầu khớp S02.
- [ ] S06: màn mới có đủ 4 `data-testid` nêu trên.
- [ ] Mọi màn: không còn `href="#"` hay anchor giả; mọi `data-testid` cũ được giữ.
- [ ] Không có bố cục đọc hiểu 60/40 (đã chốt [KL]).
