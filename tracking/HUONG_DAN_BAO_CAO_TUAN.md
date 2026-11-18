# Hướng dẫn chi tiết: Báo cáo tiến độ hàng tuần

> File này giải thích **vì sao** báo cáo tuần quan trọng hơn vẻ ngoài hành chính của nó, **tần suất** cần đạt, **nội dung bắt buộc**, **cách GVHD xác nhận cho hợp lệ**, và **ví dụ** báo cáo tốt/chưa đạt. Áp dụng cùng với mẫu tại `tracking/weekly-log/_template.md`.

## 1. Vì sao không thể coi nhẹ việc này

Báo cáo tuần không chỉ phục vụ 1 tiêu chí — nó là minh chứng chạy xuyên suốt **5 chỗ khác nhau** trong rubric:

| Nơi dùng đến báo cáo tuần | Hệ quả nếu thiếu/yếu |
|---|---|
| Điều kiện bắt buộc của **Bước 3** (quy trình) | Bộ môn rà soát tại mốc 50% — không có sổ theo dõi đều đặn = khó chứng minh đề tài "rõ ràng" |
| **Gate G2** — tần suất báo cáo | Xem bảng ngưỡng ở Mục 2 dưới đây |
| **TC2.1 Mức 5** — "mọi thay đổi thiết kế đều được ghi nhận lý do trong báo cáo tiến độ" | Không ghi lý do đổi thiết kế → tối đa dừng ở Mức 4 dù thiết kế cuối cùng tốt |
| **TC2.3 / Mục 6** — đối chiếu AI Usage Log với "tiến độ thực tế" | Báo cáo tuần là bằng chứng phụ cho thấy AI Usage Log khớp với những gì thực sự diễn ra, không phải dựng lại cuối kỳ |
| **Mục 8 hồ sơ minh chứng #2** | Thiếu hồ sơ này → không tiêu chí nào liên quan được xếp từ Mức 4 trở lên (Nguyên tắc 3) |

Nói cách khác: báo cáo tuần yếu → kéo điểm ở TC2.1, TC2.2, TC2.4 cùng lúc, chứ không chỉ là "thủ tục cho có".

## 2. Tần suất — ngưỡng điểm chính xác theo rubric (Mục 5, bảng "Quy trình thực hiện")

| Ngưỡng | Mức 3 | Mức 4 | Mức 5 |
|---|---|---|---|
| Tần suất báo cáo tiến độ (đo bằng: tổng số lần báo cáo ÷ tổng số tuần thực hiện) | ≥ 0,5 lần/tuần | ≥ 0,8 lần/tuần | ≥ 1,0 lần/tuần |

**Cách tính ra con số này:** đếm số file `tracking/weekly-log/Tuan-XX.md` đã có xác nhận GVHD, chia cho tổng số tuần đã trôi qua. Ví dụ ở Tuần 10: nếu chỉ có 6 tuần được xác nhận → 6/10 = 0,6 lần/tuần → chỉ đạt ngưỡng Mức 3, **không** đạt Mức 4.

**Gate G2 (Mục 7)** độc lập với bảng trên và nghiêm khắc hơn: nếu tần suất **dưới 0,5 lần/tuần** tại bất kỳ thời điểm rà soát nào → **TC2.2 và TC2.4 mỗi tiêu chí bị giảm 1 mức ngay lập tức**, bất kể sản phẩm/code tốt thế nào. Vì vậy mục tiêu tối thiểu tuyệt đối là **không bao giờ để tụt dưới 1 báo cáo / 2 tuần**, và mục tiêu thực tế nên nhắm là **đều đặn mỗi tuần 1 lần** (ngưỡng Mức 5) vì đây là việc ít tốn công nhất trong toàn bộ rubric để giữ điểm.

## 3. Nội dung bắt buộc của một báo cáo tuần (đã có trong `_template.md`, giải thích lý do từng phần)

1. **Công việc đã hoàn thành** — liệt kê cụ thể, có thể kiểm chứng (tên module/API/tính năng), không viết chung chung kiểu "tiếp tục phát triển hệ thống". Nên trỏ tới commit hoặc PR liên quan nếu đã có git.
2. **Đối chiếu với khối lượng cam kết** — so % hoàn thành tuần này với kế hoạch trong `COMMITMENT_BASELINE.md`/lộ trình 12 tuần. Đây là dữ liệu thô để tính TC2.2 ("đạt bao nhiêu % khối lượng cam kết") — không có phần này, hội đồng sẽ hỏi lại bằng vấn đáp và nhóm mất lợi thế minh chứng bằng văn bản.
3. **Vướng mắc/rủi ro phát sinh** — GVHD cần thấy nhóm tự nhận biết vấn đề, không đợi bộ môn phát hiện ở mốc 50%. Đây cũng là nơi ghi nhận sớm nếu một rủi ro trong Risk Register của SRS (R1–R11) đang xảy ra thật.
4. **Thay đổi thiết kế & lý do** — **bắt buộc điền nếu có**, để trống nếu không có thay đổi (đừng bịa lý do khi không có gì đổi). Đây chính là điều kiện Mức 5 của TC2.1.
5. **Cập nhật AI Usage Log tuần này?** — không phải câu hỏi hình thức: đây là bước chốt lại rằng log AI đã được ghi trong tuần, không phải nhớ lại cuối kỳ. Nếu tuần đó có dùng AI mà mục này để trống hoặc trả lời "chưa" → cần quay lại bổ sung `AI_USAGE_LOG.md` ngay, đừng để dồn.
6. **Kế hoạch tuần tiếp theo** — GVHD dùng phần này để đối chiếu tuần sau có đi đúng hướng không; cũng là cơ sở để phát hiện sớm nếu khối lượng còn lại không kịp so với thời gian còn lại (liên quan G9).
7. **Xác nhận** — xem Mục 4 dưới đây, đây là phần hay bị bỏ sót nhất trên thực tế.

## 4. Thế nào là "có xác nhận của GVHD" hợp lệ

Rubric không quy định cứng phải là chữ ký tay. Các hình thức sau đều chấp nhận được miễn **có dấu thời gian và có thể truy vết**:

- Chữ ký tay trên bản in, lưu lại (scan/ảnh).
- Email GVHD phản hồi/xác nhận nội dung báo cáo tuần đó (giữ lại email).
- GVHD comment/approve trực tiếp trên file (nếu dùng Google Docs/Notion) hoặc trên Pull Request tổng hợp báo cáo tuần (nếu để trong repo Git).
- Biên bản họp định kỳ có GVHD ký, ghi rõ tuần nào đã báo cáo nội dung gì.

Điều **không chấp nhận được**: tự điền "GVHD: đã duyệt" mà không có bất kỳ dấu vết nào GVHD thực sự xem — đây là rủi ro cao khi bộ môn rà soát ở mốc 50% (Bước 3: "Bộ môn rà soát các bản này. Nếu đề tài không rõ ràng... bộ môn đánh giá KHÔNG ĐẠT").

**Gợi ý thực tế cho nhóm 2 người:** sau mỗi buổi gặp/gọi với GVHD, gửi ngay email tóm tắt nội dung đã báo cáo và xin GVHD reply xác nhận 1 dòng ("Đã nhận, đồng ý kế hoạch tuần tới") — nhanh, có dấu thời gian, đủ làm minh chứng.

## 5. Ví dụ đối chiếu — báo cáo đạt yêu cầu vs báo cáo yếu

**Yếu (sẽ bị đánh giá thiếu minh chứng):**
> Tuần này làm CAT Engine. Có vài lỗi, tuần sau tiếp tục fix. Có dùng AI hỗ trợ code.

Vấn đề: không kiểm chứng được ("làm CAT Engine" là làm gì), không có số liệu, không có thay đổi thiết kế cụ thể, "có dùng AI" không đối chiếu được với AI Usage Log, không có xác nhận GVHD.

**Đạt yêu cầu (Mức 4–5):**
> Hoàn thành `CATEngine.computeEAP()` (41-point Gaussian-Hermite quadrature) và `checkStoppingCriterion()`, PR #14 (đã review bởi [tên]). Unit test 3 case theo SRS Mục 4.3 (toàn đúng/toàn sai/xen kẽ) đều pass, coverage module `cat-engine` đạt 62%. Khối lượng tuần này ~90% kế hoạch (chậm phần Outlier Early Stop, dời sang tuần sau). Vướng mắc: MLE fallback ban đầu bị NaN khi θ toàn đúng liên tiếp — đã fix theo guard condition SRS Mục 4.3, xem AI_USAGE_LOG dòng 2026-09-xx. Không có thay đổi thiết kế so với SRS. Kế hoạch tuần sau: hoàn thành Outlier Early Stop + bắt đầu Randomized Top-5.

Vấn đề đã giải quyết: cụ thể, có thể kiểm chứng qua PR/coverage report, trỏ đúng dòng AI Usage Log, phân biệt rõ % khối lượng, không có gì phải bịa ra ở mục thay đổi thiết kế.

## 6. Nếu lỡ bỏ một tuần

Đừng bỏ trống vĩnh viễn: tạo file `Tuan-XX.md` muộn, ghi rõ ràng ở đầu file "Báo cáo bổ sung cho Tuần XX, ghi nhận ngày [ngày thực tế]" và vẫn xin GVHD xác nhận muộn. Một báo cáo muộn có xác nhận vẫn tốt hơn một khoảng trống không giải thích được khi bộ môn/hội đồng rà soát — vì "không giải thích được" mới là thứ bị tính là vi phạm (Mục 6), không phải "báo cáo trễ" đơn thuần.
