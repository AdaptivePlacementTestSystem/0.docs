# Hồ sơ Kiểm thử & Quản lý Defect (`0.docs/testing/`)

Thư mục này chứa toàn bộ hệ thống quản lý Test Case (YAML → Excel), Báo cáo độ phủ mã, Minh chứng CI/NFR và Defect Log phục vụ **Rubric TC2.5 (Mức 5)** của đồ án **Adaptive Placement Test (CAT–Rasch v3.0)**.

---

## 1. Cấu trúc thư mục

```text
0.docs/testing/
├── README.md                     # Tài liệu hướng dẫn này
├── KE_HOACH_KIEM_THU_TLCN.md     # Sản phẩm 1: Kế hoạch kiểm thử (Chương 3 + bảng F-ID → AC-ID)
├── BAO_CAO_DO_PHU_MA.md          # Sản phẩm 4: Báo cáo Line Coverage BE & FE (≥ 70% core)
├── DEFECT_LOG.md                 # Sản phẩm 5: Tổng hợp từ GitHub Issues + Phiếu Bảng 6.2 + Regression
├── cases/                        # Nguồn sự thật (Source of Truth) dạng YAML
│   ├── _schema.yaml              # Quy ước schema & enum hợp lệ
│   ├── auth.yaml                 # AUTH_001..010 (Phương & Đăng)
│   ├── student-cat.yaml          # STU_001..016  (Đăng viết — Phương review)
│   ├── teacher-review.yaml       # TCH_001..012  (Đăng viết — Phương review)
│   ├── admin.yaml                # ADM_001..026  (Phương viết — Đăng review)
│   ├── m2m-eduz.yaml             # M2M_001..003  (Phương & Đăng)
│   └── nfr.yaml                  # NFR_001..004  (Phương & Đăng)
├── scripts/
│   ├── build_testcases_xlsx.py   # Validate YAML → sinh output/TLCN_TestCases.xlsx (thuần openpyxl)
│   └── export_defect_log.py      # Kéo GitHub Issues (gh CLI / API / JSON) → DEFECT_LOG.md
├── evidence/                     # Log CI BE & FE (URL + stdout + SHA), ảnh coverage, E2E, p95
└── output/
    └── TLCN_TestCases.xlsx       # Sản phẩm 2: File Excel sinh tự động (Summary + 1 sheet/TC)
```

---

## 2. Sinh file Excel `TLCN_TestCases.xlsx` từ YAML

Yêu cầu Python 3.10+ có `pyyaml` và `openpyxl` (`pip install pyyaml openpyxl`).

### Chạy bình thường (sinh bản khung / cập nhật Excel)
```powershell
python testing/scripts/build_testcases_xlsx.py
```

### Chạy chế độ nghiệm thu `--strict` (khóa cổng Rubric Mức 5)
Kiểm tra:
1. 100% file YAML hợp lệ schema (`ac_ref`, `case_type`, `test_level`, `automation`, không trùng `id`).
2. Tỉ lệ tự động hóa **`% Automation ≥ 70%`**.
3. Mọi TC có `automation: auto` đều có `spec_ref` tồn tại trên đĩa và chuỗi `test_name` xuất hiện thật trong file spec đó.

```powershell
python testing/scripts/build_testcases_xlsx.py --strict --backend-root ../apt-workspace/backend --frontend-root ../apt-workspace/frontend/frontend
```
*(Nếu thư mục repo trên máy là `AdaptivePlacementTestSystem/{0.docs,backend,frontend}`, chỉ cần truyền `--backend-root ../backend --frontend-root ../frontend`.)*

---

## 3. Quy trình mở & đóng Defect trên GitHub Issues (`AdaptivePlacementTestSystem/0.docs`)

### 3.1. Khởi tạo bộ nhãn chuẩn (chạy 1 lần bằng `gh` CLI)
```powershell
$repo = "AdaptivePlacementTestSystem/0.docs"
$labels = @(
  @("type:defect","d73a4a","Lỗi phát hiện trong kiểm thử TC2.5"),
  @("severity:blocker","b60205","Chặn hoàn toàn luồng chính"),
  @("severity:critical","d93f0b","Lỗi nghiêm trọng nghiệp vụ/bảo mật/mất dữ liệu"),
  @("severity:major","fbca04","Lỗi chức năng có cách đi vòng"),
  @("severity:minor","0e8a16","Lỗi nhỏ UI/nội dung"),
  @("priority:high","e11d48","Ưu tiên sửa ngay"),
  @("priority:medium","f59e0b","Ưu tiên trung bình"),
  @("priority:low","6b7280","Ưu tiên thấp"),
  @("module:be","1d4ed8","Phạm vi Backend"),
  @("module:fe","7c3aed","Phạm vi Frontend"),
  @("module:docs","0f766e","Phạm vi Tài liệu/SRS/Schema"),
  @("status:open","dc2626","Mới mở"),
  @("status:in-progress","2563eb","Đang sửa"),
  @("status:fixed","d97706","Đã sửa trên develop, chờ verify"),
  @("status:verified","16a34a","Đã re-test & regression pass")
)
foreach ($l in $labels) {
  gh label create $l[0] --repo $repo --color $l[1] --description $l[2] --force
}
```

### 3.2. Vòng đời xử lý lỗi trên nhánh `develop`
1. **Mở lỗi:** Dùng form **Báo cáo lỗi (Defect — Bảng 6.2)** tại `AdaptivePlacementTestSystem/0.docs/issues/new/choose`.
2. **Sửa lỗi:** Mở PR vào `develop` ở `backend`/`frontend` có ghi `Refs AdaptivePlacementTestSystem/0.docs#<id>`. Sau khi merge, chuyển label sang `status:fixed` và bình luận theo mẫu:
   ```markdown
   ### Resolution & Regression
   - **Fix PR / Commit:** `backend#12` (`<commit_sha>`)
   - **Root Cause:** <nguyên nhân gốc>
   - **Regression Test Ref:** `backend/src/modules/.../xxx.spec.ts :: <tên test hồi quy>`
   - **Verified By & Date:** <Phương/Đăng> — <YYYY-MM-DD>
   - **CI Run Link:** <link GitHub Actions run pass 100%>
   ```
3. **Verify & đóng lỗi:** Thành viên còn lại re-test trên bản hợp nhất + xác nhận test hồi quy pass → gắn `status:verified` và **đóng Issue thủ công** *(vì GitHub chỉ tự đóng Issue qua `Fixes` khi merge vào default branch `main`)*.

### 3.3. Xuất `DEFECT_LOG.md` đúng mẫu Bảng 6.2
```powershell
# Kéo trực tiếp từ GitHub bằng gh CLI (đã đăng nhập gh auth login)
python testing/scripts/export_defect_log.py --repo AdaptivePlacementTestSystem/0.docs

# Hoặc chạy offline từ file JSON export sẵn (phục vụ kiểm thử script)
python testing/scripts/export_defect_log.py --input testing/evidence/sample_issues.json --output testing/DEFECT_LOG.md
```
