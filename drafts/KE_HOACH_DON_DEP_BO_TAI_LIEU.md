# Kế hoạch dọn bộ tài liệu (bản nháp, chưa thực hiện)

> **Ngày:** 2026-10-24. **Trạng thái:** ⚠️ NHÁP — chưa di chuyển hay xóa file nào. Cần người dùng chốt các điểm ở mục 5.
> **Yêu cầu gốc (Đăng):** dọn bộ doc, bỏ file dư thừa/cũ (SRS v2.6, mô tả bài toán và Class Diagram tháng 9–đầu tháng 10…), chỉ giữ bản mới; sau này đổi thiết kế thì nhờ AI rà cả bộ doc; tài liệu chưa chốt để thư mục riêng, chốt rồi mới thay bản cũ.
> **Nguyên tắc dọn:** không xóa vĩnh viễn trong lần đầu — chuyển bản cũ vào `_ARCHIVE_20261024/` (có thể phục hồi); cập nhật lại bản đồ tài liệu trong `CLAUDE.md`, `INDEX.md`, `README.md` sau khi dọn; ghi `AI_USAGE_LOG` và `DECISIONS_LOG`.

## 1. Hiện trạng (đếm 24/10)
- Tài liệu rải ở 7 nơi: `0.docs/` (42 file, gồm log và mô tả sơ đồ lớp), `Tuan2/` (22), `Tuan3/` (7), `Tuan4/` (19), `Tuan5/` (6), `Update/` (17), `docs-repo/` (191, gồm 67 file bản sao trong `work/`), cộng file lẻ ở gốc `D:\TLCN` (`ClassDiagram.*`, `TLCN.drawio.xml`, `AdaptivePlacementTest.xml`, `CAU_TRUC_BACKEND_FRONTEND.md`, `CI-CD/`).
- **Trùng bản:** `0.docs/` và `docs-repo/` giữ cùng log; `ClassDiagram.*`, `TLCN.drawio.xml`, `AdaptivePlacementTest.xml` có ở gốc, `Update/` và `docs-repo/design/`; `docs-repo/work/week-0x` là bản sao của `TuanN/`.
- `CLAUDE.md` đang trỏ nhiều đường dẫn vào `0.docs/`, `Update/`, `Tuan5/`; dọn xong phải sửa lại bản đồ này.

## 2. Bộ tài liệu GIỮ (bản mới nhất, nguồn chân lý)
| Nhóm | File |
|---|---|
| Đặc tả bài toán | `SRS_TLCN_v3.0.md` / `.docx` |
| Use Case | `20261016_MoHinhHoaYeuCau.docx` (30 bảng); `AdaptivePlacementTest.xml` (UC Diagram; còn UC đã bỏ, cần sửa) |
| Class Diagram | `TLCN.drawio.xml` + `TLCN-Trang-1.drawio.png`; `ClassDiagram.puml/.mmd`; `Mo_ta_So_do_Lop_ClassDiagram.md`; `schema.prisma` (bản thật ở repo backend) |
| Sequence | `SD_01`…`SD_12.xml` (SD_03, SD_04 cần cập nhật; SD_03 còn luồng thêm câu thủ công) |
| Component, Deployment | `TLCN_Component_Deployment.drawio`, `TLCN_ComponentDiagram.png`, `TLCN_DeploymentDiagram.png`, `MO_TA_COMPONENT_VA_DEPLOYMENT_DIAGRAM.md` |
| Cấu trúc dự án | `KE_HOACH_CAU_TRUC_DU_AN.md`, `CAU_TRUC_BACKEND_FRONTEND.md` |
| Luồng, màn hình | `20261017_MO_TA_LUONG_ROLE_VA_MAN_HINH_CHI_TIET_CHO_AI_AGENT.md`, `DANH_SACH_MAN_HINH_THEO_ROLE.md`, `Luong_Hoat_Dong_CATEngine.md` |
| Kế hoạch nghiệp vụ | `KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md`, `KE_HOACH_SINH_VA_DUYET_DE_AI.md` |
| CI/CD | thư mục `CI-CD/` (`MO_TA_CI_CD_VA_DIEM_CHAN.md`, `README.md`, `verify-local.sh`), `20261021_DANH_GIA_VA_PHUONG_AN_CICD_BACKEND.md` |
| Quyết định | `20261016_BAN_CHOT_QUYET_DINH_...md`, `PHAN_TICH_SHARED_TYPES_DTO_ENUM_VA_GIAI_PHAP.md`, `DECISIONS_LOG.md` |
| Dữ liệu câu hỏi (nghiên cứu nguồn, bản quyền) | `Tuan3/KE_HOACH_BO_DU_LIEU_ITEM_BANK.md`, `PHAN_TICH_CEFR_J_...`, `PHAN_TICH_CLOTH_...`, `PHUONG_AN_GAN_NHAN_CEFR_A2_B1_P3.md` |
| Quy trình và theo dõi | `process/` (rubric, playbook, quy trình), `tracking/` (log, TRACKING, baseline, weekly-log, GIT_CONVENTIONS, mẫu), báo cáo tuần `Nhom06_HeDT_BaoCaoTuan04.docx`, `KHAO_SAT_TaoGoogleForm.gs` |

## 3. Bộ tài liệu CHUYỂN VÀO `_ARCHIVE_20261024/` (cũ hoặc đã được thay)
| File / nhóm | Lý do |
|---|---|
| `SRS_TLCN_v2.6_Final.docx` | Đã thay bằng v3.0 (CLAUDE.md đang nhắc là "bản Final trước đó", sẽ bỏ dòng này) |
| `20260922_MoHinhHoaYeuCau.docx` (24 UC) | Thay bằng bản 30 bảng |
| Mô tả bài toán và sơ đồ lớp tháng 9, đầu tháng 10 (bản thu nhỏ `Update/TLCN.drawio.xml` cũ đã backup, `UC_Overview_AdaptivePlacementTest.jpg` lỗi thời, `TLCN-Phương.drawio.png`, `TLCN-Trang-1.drawio (1).png`) | Lỗi thời so với v3.0 |
| `Tuan2/`: `KE_HOACH_HOAN_THIEN_USE_CASE`, `KE_HOACH_SEQUENCE_DIAGRAM`, `PHUONG_AN_XU_LY_BA_REVIEW_KHUYETDIEM`, `REVIEW_AND_XML_FIXES`, `PRomt.*`, `PromtSequence.txt`, `TRACKING_*` | Kế hoạch và prompt của giai đoạn đã xong |
| `Tuan3/`: `KE_HOACH_PRISMA_SCHEMA_VA_6_HANG_MUC.md`, `TRACKING_*` | Schema đã nằm trong `schema.prisma` |
| `Tuan4/`: biên bản thảo luận và quyết định (`20261007…20261010_*`), `KIEN_THUC_KIEN_TRUC_HE_THONG`, `CONG_NGHE_SU_DUNG_CHO_NGUOI_KHONG_CHUYEN`, `TRACKING_*` | Đã tổng hợp vào SRS v3.0 và `DECISIONS_LOG` |
| `Tuan4/`: `KE_HOACH_RA_SOAT_VA_HOAN_THIEN_BACKEND`, `KE_HOACH_TRIEN_KHAI_FRONTEND`, `KE_HOACH_CI_CD_VA_TRIEN_KHAI`, `HUONG_DAN_CI_CD_TU_A_DEN_Z` | ❓ Cần xác nhận: còn là kế hoạch đang dùng hay đã bị `CI-CD/` và `CAU_TRUC_BACKEND_FRONTEND.md` thay |
| `Tuan5/DE_XUAT_SUA_CLAUDE_MD.md`, `TRACKING_NGHIEP_VU_...md` | Đã áp dụng / đã tổng hợp vào `weekly-log` |
| `Update/`: `20261016_TONG_HOP_...md`, `PHAN_TICH_RA_SOAT_...md`, `NHAN_XET_CLASS_DIAGRAM_GON_CHUAN.md`, `PROMPT_1_...md`, `GOI_CAP_NHAT_GUI_DANG_20261016*` | Biên bản và công cụ tạm; kết luận đã nằm trong bản chốt và log |
| Bản trùng: `ClassDiagram.*`, `TLCN.drawio.xml`, `AdaptivePlacementTest.xml` ở gốc; `docs-repo/work/week-0x/` | Giữ đúng một bản ở nơi chuẩn |
| Các thư mục `_BACKUP_*` (`Update/_BACKUP_20261016`, `_20261018`, `_20261019`) | Sao lưu tạm, sau khi dọn không còn cần |

**Không phải tài liệu, không đụng:** `backend/`, `frontend/`, `packages/`, `backend.zip`, `frontend.zip`, `_data/`, `CLOTH/`, `olp-en-cefrj-master/`, `PROJECT`.

## 4. Cấu trúc đích đề xuất (một nơi duy nhất)
```
docs-repo/
  requirements/   SRS v3.0, đặc tả UC
  design/         class/ (drawio, png, puml, mmd, mô tả, schema), usecase/, sequence/, component-deployment/, ui/ (luồng, màn hình), structure/ (cấu trúc dự án), catengine/
  plans/          nghiệp vụ import, sinh và duyệt đề AI, cicd/, dữ liệu câu hỏi
  decisions/      bản chốt, phân tích shared-types
  process/  tracking/
  drafts/         tài liệu CHƯA CHỐT (AI lưu vào đây; chốt xong mới chuyển lên thay bản cũ)
  _archive/       bản cũ (ngoài git)
```
Quy trình khi đổi thiết kế: nhờ AI rà **toàn bộ** `docs-repo/` theo quy tắc #7 của `CLAUDE.md`, ghi đề xuất vào `drafts/`, bạn chốt thì AI mới thay bản trong thư mục chuẩn và chuyển bản cũ vào `_archive/`.

## 5. Cần chốt trước khi thực hiện
1. Nơi chuẩn: `docs-repo/` (khuyến nghị) hay giữ cấu trúc `0.docs/` + `Update/`.
2. Bản cũ: chuyển vào `_ARCHIVE` (khuyến nghị) hay xóa hẳn.
3. Nhóm ❓ ở mục 3 (4 file kế hoạch Tuần 4): giữ hay chuyển.
4. Sau khi dọn: cập nhật `CLAUDE.md` (bản đồ tài liệu), `INDEX.md`, `README.md`, đường dẫn trong code (nếu có), ghi `DECISIONS_LOG`.

## 6. Điểm Component và Deployment (nhận xét của Đăng, đối chiếu 24/10)
| Điểm | Kiểm chứng | Đề xuất |
|---|---|---|
| Lệch 1: `ai-explainer` gọi thẳng Gemini | Đúng, đã ghi ở `MO_TA_COMPONENT_...` §5 | Giữ ghi chú nợ; sửa mã đưa qua `llm-gateway` |
| Lệch 2: thiếu `bullmq`, `nodemailer` | Đúng (`package.json` chưa có; thêm `@nestjs/terminus`) | Ghi nợ thư viện; cài khi code module mail và hàng đợi |
| Lệch 3: thiếu Health Probe | Đúng: sơ đồ không có; `src/modules` không còn module `health` | Thêm khối `HealthController (Terminus)` nhóm Infrastructure; endpoint `/api/v1/health`, `/api/v1/ready` |
| Mâu thuẫn 1: SRS 15.1 ghi 2 instance, staging 1 | Đúng (SRS dòng 1345) | ❓ cần chốt (câu hỏi) |
| Mâu thuẫn 2: worker BullMQ chạy chung tiến trình backend | Đúng theo sơ đồ | ❓ cần chốt (câu hỏi) |
| Mâu thuẫn 3: Better Stack ping `/api/health` (route FE BFF) | Đúng, chưa nói rõ Nginx có chuyển tiếp backend | Ghi rõ: ping cả `/api/health` (FE) và `/api/v1/health` + `/ready` (BE), Nginx forward `/api/v1/*` |
| Mâu thuẫn 4: `prisma/migrations` trống | Đúng (thư mục trống) | Ghi chú artifact "chưa sinh migration (chặn Q1 CI/CD)"; sinh migration đầu bằng `prisma migrate` sau khi chốt schema |
