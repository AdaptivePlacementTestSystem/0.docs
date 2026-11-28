# QUYẾT ĐỊNH THAY ĐỔI THIẾT KẾ: BỔ SUNG ENDPOINT TRUY VẤN PHIÊN THI HIỆN TẠI THEO KỲ THI (`GET /exam-rounds/:roundId/session/current`) VÀ PHÒNG THỦ IDOR

* **Ngày lập:** 11/11/2026
* **Căn cứ:**
  * Phản biện kiến trúc từ thành viên nhóm (Phương) đối với RFC-CAT-03 về sự lệch pha giữa URL S04 (`roundId`) và không gian định danh CAT Engine (`sessionId`).
  * Quyết định 1 ngày 03/11/2026: Quan hệ giữa `ExamRound` và `TestSession` là **Composition** (`ExamRound ◆— 0..* TestSession`).
  * Ràng buộc nghiệp vụ khảo thí SRS v3.0 mục 820: Mỗi sinh viên chỉ có tối đa 1 phiên thi hợp lệ trong một kỳ thi (`ROUND_ALREADY_COMPLETED`, `SESSION_IN_PROGRESS`).
* **Trạng thái:** **Đã hoàn thành và kiểm thử thành công trên cả Backend và Frontend.**

---

## 1. Bối cảnh & Vấn đề kỹ thuật

Trước đó, màn hình làm bài thi S04 mang URL: `/student/exams/[roundId]/take`. Do URL chỉ chứa `roundId`, client frontend phải thực hiện giải pháp tạm thời:
1. Đọc query param `?sessionId=...` nếu có.
2. Nếu không có (F5 hoặc truy cập bookmark thuần), frontend phải gọi `GET /api/v1/sessions/active` để tìm phiên đang mở toàn hệ thống, sau đó mới gọi tiếp `GET /api/v1/sessions/:id/resume` (bị hiện tượng Waterfall Request).

**Phản biện từ teammate đã chỉ ra 2 lỗ hổng nghiêm trọng:**
1. **Lỗ hổng Cross-Round Session Injection:** Nếu client tin mù query string `?sessionId=`, một sinh viên có thể dán `sessionId` của Kỳ thi B vào URL `/exams/Ky_A/take?sessionId=sess_B`. Do backend chỉ kiểm tra quyền sở hữu sinh viên (`session.studentId === user.id`) mà không kiểm tra `examRoundId`, phiên thi của Kỳ B sẽ hiển thị sai ngữ cảnh dưới Kỳ A.
2. **Phiên đã hoàn tất (Dead/Completed Session):** Nếu truy cập lại URL cũ khi phiên đã `COMPLETED`, giao diện chưa có nhánh chuyển hướng tự động sang màn S05.
3. **Cần bằng chứng kiểm thử IDOR thực tế:** Cần test case tự động chứng minh Sinh viên A không thể can thiệp phiên thi của Sinh viên B (phải trả 403 Forbidden).

---

## 2. Quyết định thay đổi

### 2.1. Backend API: Bổ sung endpoint `GET /api/v1/exam-rounds/:roundId/session/current`
- **Bộ điều khiển (Controller):** `ExamRoundController`
- **Use Case:** `GetCurrentRoundSessionUseCase`
- **Logic xử lý:**
  1. Kiểm tra kỳ thi tồn tại và thí sinh có thuộc danh sách thi hay không (`ExamRoundParticipant`). Nếu không $\rightarrow$ `403 Forbidden`.
  2. Truy vấn phiên thi gần nhất của thí sinh gắn chặt với `examRoundId`:
     $$\text{where: } \{ \texttt{studentId: userId, examRoundId: roundId} \}$$
  3. Trả về trạng thái một cách tường minh:
     * `NOT_STARTED`: Sinh viên chưa bắt đầu làm bài.
     * `COMPLETED`: Đã nộp bài hoàn tất kèm `sessionId` (frontend tự redirect sang S05).
     * `ABANDONED`: Bài thi bị hủy hoặc dừng bất thường.
     * `IN_PROGRESS`: Phiên đang diễn ra. Kiểm tra hạn K5 Lazy Cleanup. Nếu còn hạn, nạp câu hỏi hiện tại `currentItem` và đồng hồ `expiresAt`.

### 2.2. Frontend: Tái cấu trúc `TakeExamContainer`
- Bỏ hoàn toàn cơ chế phụ thuộc query string `?sessionId=` trên thanh URL.
- Gọi trực tiếp `getCurrentRoundSession(roundId)`:
  - Nhận `IN_PROGRESS`: Khởi chạy `<ExamRunner sessionId={data.sessionId} />` với ID được server bảo chứng 100%.
  - Nhận `COMPLETED`: Tự động điều hướng sang `/results/${data.sessionId}` (S05).
  - Nhận `NOT_STARTED`: Tự động điều hướng về `/exams/${roundId}` (S03) để đọc quy chế thi.
- URL phòng thi S04 giữ nguyên hoàn toàn sạch sẽ: `/student/exams/[roundId]/take`, khớp 100% tài liệu thiết kế Stitch UI.

### 2.3. Tăng cường an toàn bảo mật
1. **Bổ sung Suite Kiểm thử IDOR (`session-idor.spec.ts`):** 8 test cases chứng minh Sinh viên A mang token của mình gọi các API `resume`, `submit`, `result`, `review` của Sinh viên B đều bị chặn cứng với mã lỗi **`403 Forbidden`**.
2. **Cấu hình `Referrer-Policy: same-origin`:** Bổ sung vào `frontend/next.config.ts` để ngăn chặn rò rỉ session ID qua header Referer.
3. **`ResumeSessionResponse`:** Bổ sung trường `examRoundId` để phục vụ đối chiếu phòng thủ chiều sâu (Defense-in-depth).

---

## 3. Đánh giá kết quả & Tác động

* **Loại bỏ Waterfall Request:** Giảm từ 2 round-trips (`/sessions/active` + `/sessions/:id/resume`) xuống còn đúng **1 round-trip duy nhất**.
* **Triệt tiêu nguy cơ Cross-Round Injection:** Không thể can thiệp bằng URL query string vì server chỉ truy vấn theo `roundId` trên route path.
* **Toàn bộ kiểm thử tự động đạt 100%:**
  * Backend: 20 test files, **102 tests pass**.
  * Frontend: 13 test files, **53 tests pass**.
