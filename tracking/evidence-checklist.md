# Checklist hồ sơ minh chứng bắt buộc (Mục 8 rubric)

> Thiếu minh chứng nào → tiêu chí tương ứng **không được xếp từ Mức 4 trở lên**, chỉ chấm theo trình bày/vấn đáp.

| # | Hồ sơ / minh chứng | Phục vụ tiêu chí | File/nơi lưu trong dự án | Trạng thái |
|---|---|---|---|---|
| 1 | Phiếu đăng ký đề tài (GV + SV) + bảng phân công công việc | Bước 1, 2 | `tracking/COMMITMENT_BASELINE.md` §1, §5 | ⬜ |
| 2 | Sổ theo dõi tiến độ hằng tuần có xác nhận GVHD | Bước 3, gate G2 | `tracking/weekly-log/Tuan-XX.md` | ⬜ (tiếp diễn) |
| 3 | Bản cam kết sản phẩm cuối + bộ metric, chốt trước 50% thời gian | Bước 3, gate G1, TC1, TC2.2 | `tracking/COMMITMENT_BASELINE.md` | ⬜ **hạn: trước Tuần 6** |
| 4 | Link repository Git đầy đủ lịch sử, cấp quyền cho hội đồng | TC2.2, TC2.4, gate G8 | `docs-repo` đã `git init` (2 commit, 02/10; origin `AdaptivePlacementTest/0.docs`). `backend/`, `frontend/` **chưa** `git init` | ⬜ (một phần) |
| 5 | AI Usage Log hoặc bản cam kết không dùng AI | TC2.3, gate G3/G4 | `tracking/AI_USAGE_LOG.md` | ⬜ (tiếp diễn) |
| 6 | SRS/SDD kèm sơ đồ thiết kế (≥4 loại cho Mức 5) | TC2.1 | `requirements/SRS_TLCN_v2.6_Final.docx`, `design/Mo_ta_So_do_Lop_ClassDiagram.md`, `work/week-02/SD_01..05_*.xml` (5 sequence); còn thiếu: deployment diagram | ⬜ thiếu deployment |
| 7 | Báo cáo phân tích tĩnh, báo cáo quét secret, coding convention | TC2.4 | CI artifact (SonarCloud/CodeQL, gitleaks) | ⬜ |
| 8 | Kế hoạch kiểm thử, test case, mã test tự động, coverage report, danh sách defect | TC2.5 | `test/` + coverage report trong CI | ⬜ |
| 9 | Cấu hình pipeline, lịch sử chạy/deploy, link môi trường triển khai | TC2.6 | `.github/workflows/`, deploy log | ⬜ |
| 10 | Báo cáo thực nghiệm người dùng: kịch bản, danh sách ẩn danh, dữ liệu, chỉ số, cải tiến | TC2.7 | `tracking/user-testing/` (tạo khi tới Tuần 7–8) | ⬜ |
| 11 | Báo cáo kiểm tra trùng lặp luận văn + danh mục TLTK có đánh dấu tài liệu ngoại ngữ | TC4 | Nộp kèm luận văn cuối kỳ | ⬜ |
| 12 | Minh chứng kết quả nổi bật (bài báo, giải thưởng, xác nhận đơn vị dùng thật, IP...) | TC6 | Tuỳ phát sinh | ⬜ (không bắt buộc) |
