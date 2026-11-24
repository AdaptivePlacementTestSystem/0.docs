# Đề xuất cập nhật đặc tả Use Case duyệt câu hỏi theo từng câu

- Ngày soạn: 24/11/2026. **Trạng thái: bản dự thảo, chưa thay thế file Word và chưa xác nhận các điểm mở.**
- Căn cứ: `requirements/20261016_MoHinhHoaYeuCau.docx`, `requirements/SRS_TLCN_v3.0.md` mục 9b/BR-22–28, quyết định ngày 03/11 và bổ sung 04/11, cùng `20261124_RASOAT_DONGBO_USECASE_CLASS.md`.
- Ký hiệu: **[ĐÃ CÓ CĂN CỨ]** là đối chiếu tài liệu thiết kế; **[CHỜ CHỐT]** không phải hành vi được mặc định triển khai. Nội dung này không chứng minh tính năng có trong mã hay đã được kiểm thử.

## 1. Đoạn mô tả tác nhân đề xuất

**GV vai A:** xem các câu được phân công, có thể sửa nội dung, lựa chọn, đáp án hoặc giải thích của câu đủ điều kiện, sau đó duyệt hoặc từ chối từng câu. Thông tin vòng 1 được lưu trong `firstReview`; bản gốc được chụp một lần trước lần sửa đầu tiên. Không có bước gửi gói.

**GV vai B:** xem và xác nhận hoặc loại từng câu được phân công, đủ điều kiện theo trạng thái; chỉ đọc nội dung, được đối chiếu bản gốc và bản A đã sửa nếu có. B không sửa nội dung, không trả câu về A. Có hành động xác nhận hàng loạt; **[ĐÃ CHỐT 24/11/2026]** phạm vi theo từng lô (`batchId`) đang mở trên giao diện, không phải toàn bộ hệ thống.

**Admin:** tạo/import lô, giao và giao lại công việc, chỉnh hạn, theo dõi, kiểm tra C3 và import câu đủ điều kiện; không sửa hoặc duyệt nội dung thay GV. Người được giao A và B trên cùng câu phải khác nhau; quy tắc B có được thuộc nhóm A của cùng lô hay không còn chờ xác nhận theo SRS.

## 2. UCGV14 — Duyệt câu hỏi (GV vai A)

- **Tác nhân:** GV được phân công vai A; ID/tên thay thế đang chờ đồng bộ sơ đồ Use Case.
- **Điều kiện trước:** đã xác thực; câu thuộc phần việc của A, còn `DRAFT` và cho phép thao tác theo quy trình được duyệt.
- **Kết quả:** câu được duyệt chuyển `FIRST_APPROVED`, hoặc bị từ chối chuyển `REJECTED`; ghi `firstReview` và sự kiện theo thiết kế. Câu từ chối không đi tiếp để B xác nhận.
- **Luồng chính:**
  1. A mở hộp việc; hệ thống hiển thị câu được giao, trạng thái, cờ, giải thích và hạn nếu dữ liệu sẵn có.
  2. A mở câu; có thể sửa nội dung, lựa chọn, đáp án, giải thích khi đủ quyền.
  3. Khi sửa lần đầu, hệ thống lưu một snapshot bản gốc trong `firstReview.originalSnapshot`; lần sửa tiếp theo không thay bản gốc.
  4. Hệ thống kiểm tra luật cứng và trùng T1–T2 trên bản sửa, cập nhật hash theo thiết kế khi bản sửa hợp lệ.
  5. A chọn Duyệt hoặc Từ chối; hệ thống kiểm tra lại quyền/trạng thái và ghi quyết định, thời điểm, sự kiện liên quan theo transaction phù hợp.
  6. Hệ thống trả kết quả và cập nhật tiến độ từng câu; không tạo hay gửi ItemPackage.
- **Ngoại lệ:** sai người/role ⇒ từ chối; sai trạng thái ⇒ không ghi; bản sửa không hợp lệ hoặc trùng ⇒ không duyệt, mã lỗi cụ thể theo hợp đồng đã được duyệt. Không còn `PACKAGE_INCOMPLETE` cho bước gửi gói đã bị bỏ.
- **Đã chốt (24/11/2026):** GV B thấy ngay từng câu ngay khi GV A bấm duyệt câu đó (`FIRST_APPROVED`), không cần đợi A duyệt hết cả lô. Trường `comment` là tùy chọn (optional): GV có thể nhập lý do/ghi chú nếu muốn, nhưng hệ thống không bắt buộc (không validate required). SRS BR-25 ghi A không sửa lại sau khi đã quyết định.
- **Tiêu chí kiểm:** sai người không thay đổi dữ liệu; A sửa hai lần chỉ có một snapshot gốc; bản sửa lỗi/trùng không được duyệt; hành động lặp/cạnh tranh không ghi đè quyết định.

## 3. UCGV15 — Xác nhận câu hỏi (GV vai B)

- **Tác nhân:** GV được phân công vai B. **Điều kiện trước:** đã xác thực, đúng người được giao, câu qua vòng A và đáp ứng điều kiện hiển thị do nhóm chốt.
- **Kết quả:** mỗi câu được xác nhận thành `SECOND_APPROVED` hoặc bị loại thành `REJECTED`; ghi `secondReview` và sự kiện; chưa vào ngân hàng.
- **Luồng chính:**
  1. B mở hộp việc xác nhận; hệ thống chỉ trả câu B được giao và đủ điều kiện.
  2. B xem câu ở chế độ chỉ đọc; nếu có snapshot, xem bản gốc so với bản A đã sửa.
  3. B chọn Xác nhận hoặc Loại; hệ thống kiểm tra quyền và trạng thái ngay khi ghi, lưu kết quả và audit.
  4. Hệ thống cập nhật tiến độ và điều kiện sẵn sàng của lô theo quy tắc được chốt.
- **Luồng thay thế:** B chọn Xác nhận tất cả câu còn lại; chỉ ảnh hưởng các câu chưa được quyết định, B được giao và đủ điều kiện; ghi sự kiện `CONFIRM_ALL` theo hợp đồng audit. **[ĐÃ CHỐT 24/11/2026]** phạm vi theo từng lô (`batchId`) đang mở trên giao diện, không phải toàn bộ hệ thống.
- **Ngoại lệ:** B gọi chức năng sửa hoặc trả về A ⇒ từ chối; sai người/trạng thái ⇒ không ghi; yêu cầu cạnh tranh hoặc lặp phải có kết quả nhất quán, không ghi đè quyết định khác.
- **Tiêu chí kiểm:** B chỉ thấy câu đúng phân công; A từ chối không tới B; B không sửa được; xác nhận hàng loạt không tác động câu của người khác hoặc đã quyết.

## 4. UCADM13 — Giao việc duyệt câu hỏi và theo dõi lô

- **Tác nhân:** Admin. **Điều kiện trước:** lô đủ điều kiện giao sau C1/C2; danh sách câu và trạng thái còn hiệu lực.
- **Luồng chính:**
  1. Admin mở lô, xem số câu đủ điều kiện, câu AI loại và cờ theo quyền.
  2. Admin thiết lập người A, B và hạn từng vòng theo phương án được nhóm chốt; A khác B trên cùng câu.
  3. Hệ thống xác minh tài khoản, quyền theo phương án được chốt và trạng thái lô/câu; trình xem trước nếu phương án chọn có bước đó.
  4. Admin xác nhận; hệ thống gán `reviewerId`/`confirmerId` và hạn cho từng câu, ghi sự kiện `ASSIGN` tương ứng, cập nhật trạng thái lô và xử lý thông báo/nhắc theo thiết kế.
  5. Admin theo dõi tiến độ theo câu và người được giao.
- **Luồng thay thế:** Admin chỉnh hạn hoặc giao lại phần chưa xử lý. Hệ thống kiểm tra lại trạng thái, quyền, hạn, nhật ký và lịch nhắc; không ép gửi gói.
- **Đã chốt (24/11/2026):** Mốc hạn B cố định theo ngày giao việc của đợt (A = Ngày giao + reviewDays; B = Ngày giao + confirmDays, chốt 23:59:59); không thả nổi hạn của B theo lúc A duyệt để tránh trôi hạn và xung đột lịch nhắc tự động BullMQ. Chọn thủ công từng câu hay nhóm + phân bổ; giá trị action audit khi chỉnh hạn; quy tắc B so với toàn nhóm A tiếp tục theo dõi.
- **Tiêu chí kiểm:** không giao A=B; sai trạng thái hoặc quyền không ghi; xác nhận trùng hoặc hai Admin cùng giao không tạo phân công/sự kiện mâu thuẫn; quá hạn không tự giao lại.

## 5. UCADM14 — Kiểm tra cuối và import vào ngân hàng

- **Tác nhân:** Admin. **Điều kiện trước:** lô sẵn sàng theo quy tắc cuối cùng được xác nhận; câu còn chưa quyết không được import.
- **Luồng chính:** Admin yêu cầu C3 → hệ thống kiểm tra tính hợp lệ, luồng và trùng so với ngân hàng hiện hành → Admin xem báo cáo và xử lý các cờ được phép → Admin chọn Import khi kết quả C3 còn hiệu lực → hệ thống kiểm tra lại điều kiện/trùng nhanh và đưa câu đủ điều kiện vào `FINAL_APPROVED`, ghi người và thời điểm import.
- **Ngoại lệ:** lô chưa sẵn sàng hoặc kết quả kiểm tra hết hiệu lực ⇒ không import; lỗi giữa chừng và hai Admin thao tác đồng thời phải không tạo dữ liệu trùng hay trạng thái giả thành công.
- **Chờ chốt:** cách xử lý trường hợp còn câu chưa quyết đã quá hạn sau import; tài liệu SRS và kế hoạch hiện có hai cách diễn đạt. Cách xử lý cờ mềm/hard và ngưỡng theo quyết định hiện hành, không lấy đề xuất AI chưa được xác nhận làm chốt.
- **Tiêu chí kiểm:** chỉ câu `FINAL_APPROVED` được CAT chọn; câu chưa quyết/đã loại không được import; lô chỉ `DONE` theo điều kiện trạng thái cuối được xác nhận.

## 6. UCGV02/UCGV04 và quan hệ mô hình

- **UCGV02:** GV chỉ xem câu thuộc phạm vi được giao theo quyền/điều kiện đủ; Admin xem theo quyền quản trị. Thay mọi tham chiếu “câu trong gói” bằng liên kết phân công từng câu.
- **UCGV04:** A chỉ sửa câu được giao khi đủ điều kiện, đối chiếu quy tắc trạng thái và snapshot của UCGV14; route cụ thể `[batchId]` hay `[itemId]` **chưa chốt**.
- **Quan hệ:** `ExamRound ◆ TestSession` là composition trong mô hình; `onDelete: Restrict` trong Prisma bảo vệ lịch sử, không diễn giải thành xóa cascade.
- **CAT/route:** UCSV02/UCSV07 cần phân biệt roundId và sessionId. Không thay bằng một URL mới cho tới khi chốt và kiểm thử bắt đầu/tiếp tục/reload.

## 7. Đồng bộ sau khi review

Sau khi nhóm chốt điểm mở, cập nhật file Word đặc tả, Use Case Diagram và xuất ảnh, rồi đối chiếu SRS Markdown/DOCX, CD, SQ, UI và API. Bản dự thảo này không phải phê duyệt thay cho nhóm. Ghi người/ngày quyết định và bằng chứng kiểm thử; không đánh dấu đã review, đã merge hoặc đã triển khai nếu chưa xảy ra.

## 8. Truy vết cập nhật Use Case — rà soát 24/11/2026

| Mã UC | Nội dung cần đồng bộ | Căn cứ và điểm cần xác nhận |
|---|---|---|
| UCGV02 | Giới hạn câu giáo viên được xem theo phân công; Admin xem câu thuộc lô kể cả AI_REJECTED theo quyền. | SRS 9b.16, BR-16. |
| UCGV04 | Chỉ A được sửa câu được giao còn DRAFT; snapshot gốc lưu một lần; không sửa sau khi đã quyết định. Sửa là tùy chọn trong UCGV14. | SRS 6.2, BR-25, BR-27, 9b.14–9b.16; rà quan hệ include vì không được mô tả việc sửa là bắt buộc. |
| UCGV06 | REJECTED được giữ trong lô; AI_REJECTED được dọn theo cấu hình. | SRS 9b.15–9b.16; sự tồn tại của UC xóa còn chờ chốt, không tự xóa UC hay cấp quyền xóa. |
| UCGV14 | A duyệt hoặc từ chối từng câu, không gửi gói; sau sửa chạy luật cứng và T1–T2; không lưu lý do từ chối theo quy tắc hiện hành. | F-26, BR-25, BR-27; cần làm rõ trường comment nullable so với quy tắc không lưu lý do. |
| UCGV15 | B chỉ đọc, xác nhận hoặc loại; SECOND_APPROVED chưa vào ngân hàng; xác nhận hàng loạt chỉ tác động câu đủ điều kiện được giao và chưa quyết. | F-27, BR-26; thời điểm hiển thị và phạm vi hàng loạt còn chờ chốt. |
| UCADM13 | Giao A/B khác nhau trên từng câu khi lô READY_TO_ASSIGN; hạn hai vòng riêng; ghi ASSIGN và theo dõi. | F-25, BR-22–24; phân bổ, mốc hạn B, audit chỉnh hạn và ràng buộc nhóm A/B còn mở. SRS 9b.2 chưa xác nhận việc chỉ chọn tài khoản TEACHER. |
| UCADM14 | Kiểm tra C3 khi đủ điều kiện; báo cáo C3 còn hiệu lực trước import; kiểm T1–T2 lại, không nhập câu chưa xử lý. | F-28, BR-28, 9b.12–9b.14; xử lý câu còn quá hạn sau import đang có hai cách diễn đạt, không mặc định lô DONE khi câu chưa ở trạng thái cuối. |
| UCSV02/UCSV07 | Phân biệt kỳ thi và phiên thi; mô tả bắt đầu, phiên đang chạy, tải lại và tiếp tục. | Đã chốt xong (11/11/2026): URL phòng thi là `/student/exams/[roundId]/take`, gọi API `/api/v1/exam-rounds/:roundId/session/current` để lấy session an toàn chống IDOR; khi thi xong tự redirect về `/results/[sessionId]` (S05). |

### Ca kiểm tra cần truy vết khi triển khai

1. Người không được giao hoặc sai vai không được thao tác ngoài phạm vi; A và B khác nhau trên cùng câu.
2. A sửa nhiều lần chỉ lưu một snapshot gốc, hệ thống kiểm tra bản sửa; thao tác trùng hoặc cạnh tranh không ghi đè quyết định.
3. B chỉ xác nhận câu đúng phân công và đủ điều kiện; xác nhận hàng loạt không tác động câu đã quyết hay của người khác. Phạm vi cuối cùng theo quyết định được phê duyệt.
4. Quá hạn không tự giao lại hoặc đổi trạng thái; nhắc không ghi đè chi tiết review. Kiểm tra mốc hạn B và audit theo quyết định được chốt.
5. C3 cũ bị khóa khi không còn hiệu lực; import đồng thời không tạo dữ liệu trùng; chỉ FINAL_APPROVED được CAT chọn. Cần chốt kết quả mong đợi khi còn câu quá hạn sau import.

Đây là các ca cần kiểm chứng, không phải kết quả kiểm thử đã chạy. Word chính thức và ảnh Use Case vẫn cần đồng bộ sau khi hoàn tất kiểm tra.
