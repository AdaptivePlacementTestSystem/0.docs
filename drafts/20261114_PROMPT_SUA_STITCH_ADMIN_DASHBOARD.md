# PROMPT SỬA STITCH: ADMIN / DASHBOARD (S36)

> **Ngày:** 14/11/2026 · **Trạng thái:** DRAFT (chưa chạy trên Stitch)
> **Project Stitch:** English Placement Test UI (`16753573200013570369`) · Màn: Admin/Dashboard (`2beaef86c94c465c85ac6351d75af594`)
> **Căn cứ:** Quyết định #136, SRS v3.0 mục 4.6 và 9b.19, UI mô tả S36 (đã chốt 14/11/2026), bảng đối chiếu D1–D17 ở `20261114_KE_HOACH_ADMIN_DASHBOARD_VA_QUAN_LY_NGUOI_DUNG.md` mục I.
> **Cách dùng:** dán "Quy tắc chung" rồi một lần prompt bên dưới vào Stitch (edit screen). Sau khi chạy, kiểm lại bằng danh sách ở cuối.

## Quy tắc chung (dán kèm đầu prompt)

```
Giữ nguyên phong cách hiện tại (màu #2563EB, font Be Vietnam Pro, thanh bên 240px, thẻ bo góc, bố cục tổng thể). Chỉ thay đổi đúng những điểm nêu bên dưới. Giữ nguyên mọi thuộc tính data-path và href hiện có. Mọi chữ hiển thị bằng tiếng Việt. Không thêm thành phần nào ngoài danh sách. Số liệu mẫu phải tự khớp nhau (tổng các phần bằng tổng chung).
```

## Prompt: màn Admin/Dashboard

```
1. Thanh bên (menu Quản trị): dùng đủ 7 mục theo thứ tự: Tổng quan, Ngân hàng câu hỏi, Lô câu hỏi (chấm vàng), Kỳ thi, Tài khoản, rồi một đường kẻ, rồi Báo cáo lớp học, Hồ sơ sinh viên. Mục "Tổng quan" đang được chọn (nền xanh nhạt, chữ xanh đậm).

2. Thanh trên cùng: bỏ chữ "Học kỳ 1 • 2024-2025" và mục "Hỗ trợ kỹ thuật". Giữ huy hiệu "HỆ THỐNG CAT-RASCH" và avatar.

3. Đầu trang: bỏ huy hiệu "Trực tiếp • Kỳ 1 2024-2025" và dòng "Phiên bản CAT-Rasch v2.4". Tiêu đề "Tổng quan hệ thống". Dòng phụ: "Số liệu toàn hệ thống; chọn một kỳ thi để lọc số sinh viên và phân phối CEFR." Bên phải tiêu đề: một ô chọn "Kỳ thi" (mặc định "Tất cả kỳ thi") và nút phụ "Làm mới". BỎ nút "Xuất báo cáo tổng quan".

4. Bốn thẻ số (giữ bố cục 4 cột):
   - "Sinh viên đã thi": 1.240. BỎ dòng "+14% so với kỳ trước". Thay bằng dòng nhỏ "Đã hoàn thành ít nhất một bài thi".
   - "Câu hỏi vào ngân hàng": 486. Dòng nhỏ: "Đã vào ngân hàng chính thức" (BỎ chữ "kiểm định & hiệu chuẩn Rasch").
   - "Lô câu hỏi cần xử lý": 3, huy hiệu "Cần xử lý", liên kết "Xem các lô câu hỏi" (giữ).
   - "Kỳ thi đang mở": 2. BỎ dòng "Phòng máy A1 & Khảo thí phân luồng". Thêm liên kết "Xem các kỳ thi" (data-path="ky-thi").

5. Khối "Phân phối trình độ CEFR": giữ dạng 6 thanh ngang, nút chuyển "Biểu đồ | Bảng số liệu". Nhãn chỉ gồm: Pre-A1, A1, A2, B1, B2, C1+ (BỎ hậu tố "Beginner", "Elementary", "Intermediate", "Upper-Intermediate", "Advanced"). Sửa khoảng θ đúng như sau: Pre-A1: θ < −2,0; A1: −2,0 ≤ θ < −1,0; A2: −1,0 ≤ θ < 0,0; B1: 0,0 ≤ θ < 1,0; B2: 1,0 ≤ θ < 2,0; C1+: θ ≥ 2,0. Mỗi thanh một màu riêng theo huy hiệu: Pre-A1 #E0F2FE, A1 #BAE6FD, A2 #7DD3FC, B1 #38BDF8, B2 #0EA5E9, C1+ #0369A1 (chữ trắng ở B2 và C1+). Số mẫu (tổng 1.240): Pre-A1 43, A1 188, A2 353, B1 300, B2 311, C1+ 45 (cộng đúng 1.240); phần trăm làm tròn một chữ số thập phân (có thể lệch 0,1 do làm tròn). BỎ dòng "Điểm chuẩn trung vị toàn trường đạt B1, phân bổ chuẩn Gaussian" và "Độ tin cậy SEM < 0.32". Dòng mô tả: "Theo mức CEFR mới nhất của mỗi sinh viên".

6. Khối "Trạng thái câu hỏi": thay biểu đồ vòng (donut) bằng 6 thanh ngang, mỗi thanh một màu trạng thái, có nút chuyển "Biểu đồ | Bảng số liệu" giống khối CEFR. Sáu dòng, theo thứ tự: "Chờ duyệt vòng 1" 45, "Đã duyệt vòng 1" 68, "Đã xác nhận vòng 2" 52, "Đã vào ngân hàng chính thức" 486, "Đã loại bởi GV" 18, "AI đã loại" 24 (tổng 693, ghi tổng ở dòng phụ "Tổng 693 câu"). Giữ liên kết "Quản lý chi tiết ngân hàng".

7. Bảng "Các kỳ thi đang mở" (đổi tiêu đề từ "Các kỳ thi khảo thí đang diễn ra"): BỎ dòng "Cập nhật tự động mỗi 30s" và chấm nhấp nháy; thay bằng chữ nhỏ "Cập nhật lúc [giờ]" và nút "Làm mới". BỎ dòng "Mã ca thi: ...". Cột: Tên kỳ thi, Giờ mở — đóng (ghi cả ngày và giờ, ví dụ "15/10/2026 08:00 — 16/10/2026 17:00"), Thời lượng (45 phút), Sinh viên (ba số: chưa thi / đang thi / hoàn thành), Trạng thái ("Đang mở"), Hành động ("Vào quản lý kỳ thi"). Đổi năm mẫu cho đồng nhất thành 2026.

8. Thêm ba trạng thái (hiển thị bằng cách ẩn/hiện, mặc định ẩn): (a) khi chưa có sinh viên nào hoàn thành: dòng "Chưa có sinh viên nào hoàn thành bài thi." thay vùng biểu đồ CEFR; (b) khi không có kỳ nào đang mở: "Hiện không có kỳ thi nào đang mở." trong bảng; (c) lỗi tải: thông báo "Không tải được số liệu." kèm nút "Thử lại".
```

## Danh sách kiểm lại sau khi chạy

- [ ] Thanh bên đủ 7 mục, không còn "Học kỳ", "Hỗ trợ kỹ thuật", "Mã ca thi", "Phòng máy", "+14%", "Xuất báo cáo tổng quan", "Gaussian", "SEM".
- [ ] Khoảng θ khớp SRS mục 4.6; nhãn CEFR chỉ 6 nhãn ngắn; 6 màu khác nhau.
- [ ] Tổng 6 mức CEFR = 1.240; tổng 6 trạng thái câu = 693; phần trăm khớp.
- [ ] Có ô chọn "Kỳ thi" và nút "Làm mới"; không có tự cập nhật.
- [ ] Biểu đồ trạng thái là 6 thanh ngang, có chuyển Biểu đồ/Bảng.
- [ ] Giữ nguyên `data-path` và `href` cũ; nút xuất báo cáo đã bỏ.

## Màn "Admin/Danh Sách Lô Câu Hỏi" (S28) — chưa sửa trong đợt này

Ghi nhận để làm sau: đổi tên cột "Tiến độ C1-C3" thành "Tiến độ duyệt"; nhãn nguồn "AI sinh (C1)" thành "AI sinh"; bỏ "mã đợt" vì `ItemBatch` chỉ có `name` tùy chọn; thêm nhãn "Quá hạn"; bỏ thẻ "Tỉ lệ duyệt đạt chuẩn", "Bộ lọc nâng cao", "Xuất báo cáo"; tab trạng thái đủ `FINAL_CHECKED`, `FAILED`, `PARTIAL`.
