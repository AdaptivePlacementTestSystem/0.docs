# Kế hoạch Tuần 5: Chốt nghiệp vụ Import danh sách sinh viên & Kỳ thi, nâng đặc tả lên v3.0, bổ sung sơ đồ thiết kế, danh sách màn hình theo role

> **Ngày lập:** 2026-10-12 (cuối Tuần 4/12; kế hoạch này chạy Tuần 5–6). **Vai trò người lập:** Senior Software Developer + PM.
> **Trạng thái:** ⛔ **CHỜ BẠN DUYỆT (task W0.1).** Chưa sửa tài liệu thiết kế nào (SRS, UC, Class Diagram, Prisma, Sequence). Chỉ có hai file trong `Tuan5/` (kế hoạch này và tracking), cộng thêm các dòng đã ghi vào `DECISIONS_LOG.md` và `AI_USAGE_LOG.md` theo quy tắc 2 của `CLAUDE.md`.
> **Cập nhật 2026-10-13 (phiên 19, **đã bị DC-19 thay**):** thêm phân biệt **GV thường / QTV đơn vị (GV-QTV) / QTV hệ thống** (DC-15…DC-17, BR-16…BR-18, MD-15, UCADM09–10, S24–S25, Quyết định **#95**). Backup bản trước: `_BACKUP_20261013_KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE_ORIGINAL.md`. Trong file này, chữ "Admin" ở các mục cũ nay hiểu là **QTV hệ thống** trừ khi ghi "QTV đơn vị"; xem Mục 3.8.
> **Cập nhật 2026-10-13 (phiên 20) — DC-18, Quyết định #96:** **GV thường chỉ xem kết quả** (báo cáo lớp, tra cứu SV). **Soạn/duyệt câu hỏi, tạo kỳ thi, import danh sách thi, import + quản lý tài khoản SV chuyển sang GV-QTV (trường mình) và QTV hệ thống (mọi trường).** Đảo phần "GV tạo kỳ" của DC-07/#88 và quyền GV ở ma trận 3.8, BR-07, BR-16. **Đọc DC-18 trước:** ở các mục cũ còn chữ "Giảng viên/GV tạo kỳ", "Teacher ..> RosterImportService", cột "GV thường" ở các UCGV02–06, UCADM15–17 thì **hiểu theo DC-18** (ID UC giữ nguyên, actor đổi thành Admin). Backup: `_BACKUP_20261013_PHIEN20_*`.
> **Cập nhật 2026-10-13 (phiên 21) — DC-19, Quyết định #97: HỆ THỐNG CHỈ PHỤC VỤ 1 TRƯỜNG.** **Bỏ `Institution` và mọi `institution_id`; bỏ QTV hệ thống.** `ADMIN` = **Admin của trường** (siêu tập của `TEACHER`), giữ 4 giá trị `UserRole` và các chức năng như cũ. DC-15, DC-16, DC-17, MD-03, MD-09, MD-15, BR-16…BR-19 (bản cũ), UCADM10, S25 **bị thay/loại bỏ** (xem DC-19). Ở các mục cũ còn chữ "GV-QTV", "QTV hệ thống", "đơn vị/trường", "scope", `institutionId` thì **hiểu theo DC-19**. Backup: `_BACKUP_20261013_PHIEN21_*`.
> **Cập nhật 2026-10-13 (phiên 22) — DC-20…DC-23, Quyết định #93, #94, #98:** chốt **D-T = T2** (`durationMinutes` theo kỳ), **D-FP = C** (OTP 6 số qua email), **Q-8 = `users.is_active`**, và **đổi cơ chế import thành "lưới tạm" (grid)** cộng dồn nhiều file, bấm Lưu mới ghi DB, áp dụng cho cả import tài khoản và danh sách thi (đảo DC-04/DC-06/BR-04/MD-06; thay API `preview/confirm` bằng `upload/grid/save`). Các mục cũ còn chữ `preview`/`confirm`/`all-or-nothing`/`SKIPPED`/"chờ chọn" **hiểu theo DC-20…DC-23**. Backup: `_BACKUP_20261013_PHIEN22_*`.
> **Cập nhật 2026-10-13 (phiên 23) — DC-24…DC-26, Quyết định #99, #100, #101:** Admin tạo tài khoản **SV và GV** bằng **từng người hoặc import file** (đảo "không import giảng viên" của DC-05); `exam_rounds.duration_minutes` **NOT NULL DEFAULT 45**; EAP giữ **lưới đều 41 điểm θ ∈ [−4,+4], bước 0.2** (không gọi là Gaussian–Hermite). Backup: `_BACKUP_20261013_PHIEN23_*`.
> **File theo dõi đi kèm:** [`TRACKING_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md`](./TRACKING_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md) — **AI Agent tự cập nhật sau mỗi task** (quy tắc: Mục 1.4).
> **Nguồn đã đọc trực tiếp:** `HUONG_DAN_RUBRIC_VA_TRACKING.md`, `Mo_ta_So_do_Lop_ClassDiagram.md`, `SRS_TLCN_v2.6_Final.docx` (bản `docs-repo/requirements`, trùng byte với bản `0.docs - Sao chép`), `20260922_MoHinhHoaYeuCau.docx` (24 UC), `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (bản `0.docs - Sao chép`), `DECISIONS_LOG.md` (#22–#28, #53–#83), `Tuan4/20261010_PHAN_TICH_TAC_DONG_IMPORT_TAI_KHOAN_VA_KY_THI.md`, `Tuan4/20261010_MO_TA_MAN_HINH_TOI_GIAN_THEO_ROLE.md` (mục lục), `weekly-log/Tuan-04.md`, `prisma/schema.prisma`, `ClassDiagram.puml`, cấu trúc thư mục `backend/`, `frontend/`, `Tuan2/`.
> **Giới hạn của kế hoạch này (đọc trước khi tin):** (1) chưa chạy BE/FE, chưa mở bản `.docx` bằng Word, chưa mở `.xml` bằng Enterprise Architect hay draw.io; (2) hai file `.docx` đọc bằng script trích văn bản, nên **định dạng, hình, comment trong `.docx` chưa được kiểm**; (3) mức công sức S/M/L là định tính, **không phải số giờ đo được**; (4) tên class, ID UC, ID màn hình, đường dẫn API ở Mục 3–4 là **đề xuất của AI**, chỉ trở thành chốt khi bạn duyệt W0.1.

---

## 0. Tóm tắt điều hành

**Bốn việc, theo đúng thứ tự bạn nêu:**

| # | Việc | Khi nào | Sản phẩm chính |
|---|---|---|---|
| 1 | Chốt nghiệp vụ **import danh sách sinh viên** (tài khoản + kỳ thi) và cập nhật toàn bộ bộ tài liệu: Class Diagram, Use Case, Prisma/DB, kế hoạch 2 repo FE+BE, đặc tả **SRS v3.0** | Tuần 5 (làm đầu tiên) | `SRS_TLCN_v3.0.docx`, UC spec + UC Diagram cập nhật, Class Diagram (drawio/puml/mmd/md) cập nhật, `schema.prisma` cập nhật, 3 Sequence Diagram mới + 3 cập nhật, kế hoạch BE/FE bổ sung phase mới |
| 2 | Thêm **≥2 sơ đồ** cho TC2.1: **Component + Deployment** (đề xuất của Đăng; Phương hỏi AI riêng để đối chiếu) | Tuần 5, ngay sau việc 1, cố gắng không trễ | 1 file draw.io 2 trang + mô tả trong SRS v3.0 |
| 3 | Hoàn thiện **đặc tả Use Case**, bản vẽ UC, Sequence, cùng sơ đồ mới | Tuần 5 làm UC mới/đổi; Tuần 6 hoàn thiện phần còn lại; Tuần 7 bắt đầu code | Acceptance criteria + business rules cho từng UC trong phạm vi TL |
| 4 | **Danh sách màn hình theo role** (luồng + chức năng) | Cuối Tuần 5 – đầu Tuần 6 | `DANH_SACH_MAN_HINH_THEO_ROLE.md` |

**Kết luận một câu:** phạm vi đã chốt là **Phương án B** (Admin import tài khoản + **Admin** tạo kỳ thi và import danh sách thi — sửa theo DC-18, DC-19: hệ thống đơn trường), tức **đảo một phần Quyết định #59** và **đảo một phần #24/#28** (bỏ đăng nhập Google/Microsoft, chuyển sang email + mật khẩu). Đây là thay đổi chạm schema, API, 2 repo, báo cáo và phần lớn tài liệu, nên kế hoạch đặt **cổng khóa đặc tả (W0)** trước mọi việc sửa tài liệu.

**Ba điều cần bạn làm trước khi Agent chạy tiếp:**
1. **W0.1 — Duyệt kế hoạch** (kèm 15 đề xuất mặc định ở Mục 3.3 (thêm MD-15) và DC-18…DC-19 (GV thường chỉ xem; hệ thống đơn trường): duyệt = chốt, bạn có thể gạch/sửa từng dòng).
2. **W0.2 — Chọn mô hình giờ làm bài** (D-T, Mục 3.2): bạn đã yêu cầu "lên phương án", ba phương án nằm ở Mục 3.2.
3. **W0.3 — Chọn cơ chế "Quên mật khẩu"** (D-FP, Mục 3.2): bạn chốt SV tự bấm quên mật khẩu, còn cách làm cần chọn.

**Ba điều cần chú ý sớm (chi tiết ở Mục 2 và 12):**
- **Lỗi 🔴 đang có ở BE:** `login.use-case.ts` cho **mật khẩu nào cũng qua** nếu tài khoản có hash (theo `Tuan4/20261010_PHAN_TICH...` Mục 3.4, **chưa tái hiện bằng test**). Phải sửa trước khi làm luồng mật khẩu tạm; đã nằm trong phase P5 của kế hoạch BE, kế hoạch này chỉ thêm ràng buộc thứ tự.
- **Mốc G1 (cuối Tuần 6):** phạm vi tăng lên thì `COMMITMENT_BASELINE.md` phải phản ánh trước khi ký. Task W0.8 và W6.5.
- **Mâu thuẫn tài liệu hiện hữu:** `CLAUDE.md` ghi "chưa có code, chưa có git" nhưng `backend/backend` và `frontend` đã có mã (vẫn chưa `git init`, theo `Tuan-04.md`). Task W1.18 đề xuất sửa.

---

## 1. Hướng dẫn vận hành cho AI Agent (BẮT BUỘC đọc đầu tiên)

### 1.1. Thứ tự đọc trước khi làm bất kỳ task nào
1. `D:\TLCN\CLAUDE.md`, rồi `0.docs/docs/HUONG_DAN_RUBRIC_VA_TRACKING.md`.
2. **File kế hoạch này** (toàn bộ), rồi `TRACKING_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` để biết task nào ✅/🔄/⬜/🚫.
3. `0.docs/tracking/DECISIONS_LOG.md` (đặc biệt #22–#28, #53–#92).
4. Tài liệu nguồn của task đang làm (cột "Đầu vào" ở Mục 8). **Không đọc** các bản `SRS_TLCN*.md`, `SRS_TLCN_v2.3–2.5*.docx` ở gốc (chỉ là lịch sử).

### 1.2. Quy tắc tuyệt đối
1. **Không tự quyết định** bất cứ lựa chọn nào ảnh hưởng mở rộng/bảo trì mà kế hoạch này chưa chốt (tên, cấu trúc module, pattern, field cứng, đổi schema). Dừng, nêu ≥2 phương án kèm đánh đổi, hỏi qua `AskUserQuestion`, ghi `DECISIONS_LOG`.
2. **Cổng ⛔ là cổng cứng.** Task phụ thuộc vào cổng chưa mở thì đặt 🚫 và ghi lý do, **không làm "tạm" rồi sửa sau**.
3. **Backup trước khi sửa** mọi file có sẵn: sao chép thành `Tuan5/_BACKUP_20261012_<tên-file>_ORIGINAL.<đuôi>` (giống cách `Tuan2/` đã làm). Không ghi đè backup.
4. **Không sửa `SRS_TLCN_v2.6_Final.docx`.** Bản mới là `SRS_TLCN_v3.0.docx` tạo mới trong `Tuan5/` (từ bản sao của v2.6 Final).
5. **Ngôn ngữ (đã chốt, không tự đổi):** định danh UML (class, method, enum, tên lifeline) giữ **tiếng Anh**; mô tả, SRS, UC, tracking giữ **tiếng Việt**. Tên file EA XMI viết tiếng Việt **không dấu** (đúng mẫu `SD_01_DangNhapHeThong.xml`).
6. **Không bịa số liệu** (KPI, coverage, thời gian, hạn mức dịch vụ). Chưa đo thì ghi "N/A" hoặc "chưa kiểm chứng".
7. **Không `git push`, không tạo PR, không merge**; không ghi lên server; không động tới `farmnongviet`. Thư mục này chưa có git.
8. **Không đưa dữ liệu thật vào tài liệu/test/mẫu:** mọi file Excel mẫu, seed, ví dụ dùng dữ liệu giả. Mật khẩu tạm **không được xuất hiện trong log, tài liệu, ảnh chụp, ví dụ thật**.
9. **Đồng bộ:** mỗi lần sửa một tài liệu thiết kế phải rà các tài liệu cùng bộ (CLAUDE.md quy tắc 7). Việc rà là task W6.1, nhưng mỗi task sửa tài liệu phải ghi vào tracking cột "Tài liệu liên đới cần rà".
10. **Đối chiếu công thức CAT** (Rasch/EAP/stopping) với SRS khi đụng tới Mục IV; kế hoạch này **không** đổi thuật toán, chỉ đổi cách tính hạn phiên (D-T).
11. **Mọi thứ AI sinh phải tự kiểm chứng** theo cột "Xác minh". Task chưa chạy xác minh thì **không** được đánh ✅.

### 1.3. Vòng lặp cho mỗi task
`Đọc tracking → chọn task ⬜ có đủ phụ thuộc ✅ → đặt 🔄 → làm → chạy bước Xác minh → đặt ✅ (hoặc 🚫 kèm lý do) → ghi dòng vào "Nhật ký Agent" của tracking → nếu tạo/sửa tài liệu có ý nghĩa thì thêm dòng vào AI_USAGE_LOG.md → nếu có lựa chọn thiết kế thì ghi DECISIONS_LOG.md`.

### 1.4. Quy tắc cập nhật file tracking (Agent làm sau mỗi task)
- Đổi cột trạng thái của task; cập nhật bảng "Trạng thái tổng quan" (Xong/Tổng, %) bằng cách **đếm lại các dòng ✅**, không ước lượng.
- Mỗi task xong phải có **bằng chứng**: đường dẫn file đã tạo/sửa, lệnh xác minh và kết quả thật (ví dụ "xml parse OK, 0 tham chiếu hỏng"). Không có bằng chứng thì không ✅.
- Thêm một dòng vào bảng "Nhật ký Agent": ngày, task, kết quả, tài liệu liên đới cần rà.
- Không xóa dòng cũ; task hủy thì đặt ⏭ kèm lý do.
- Nếu một task làm lộ thêm việc, thêm dòng mới vào đúng phase với mã dạng `W1.7a`, ghi lý do. Không tự thêm file mới.

### 1.5. Khi bị chặn hoặc thiếu thông tin
Đặt 🚫, ghi lý do và câu hỏi vào mục "Câu hỏi đang chờ" của tracking, dùng `AskUserQuestion` nếu là quyết định thiết kế. **Không suy đoán để đi tiếp.**

### 1.6. Chạy song song
Chỉ chạy song song các task có ký hiệu `∥` cùng nhóm và **không cùng sửa một file**. Mục 10 có sơ đồ phụ thuộc.

### 1.7. Ghi chú kỹ thuật theo loại tài liệu (đúc kết từ các tuần trước)
| Loại | Cách làm | Cạm bẫy đã biết |
|---|---|---|
| `.docx` (SRS, UC) | Nạp skill `anthropic-skills:docx`. Sao chép rồi sửa bản sao; giữ style/heading của bản gốc. Chèn mục mới đúng vị trí, không dựng lại cả file. | Đọc bằng script trích văn bản không thấy hình/định dạng; sau khi sửa phải mở lại bằng thư viện đếm heading/bảng so với bản gốc. Người cần mở bằng Word xem (task có 👤). |
| EA XMI (`AdaptivePlacementTest.xml`, `SD_*.xml`) | Sửa/tạo bằng script Python theo cấu trúc trong `Tuan2/KE_HOACH_SEQUENCE_DIAGRAM.md` **Mục 5** (đã đọc: cấu trúc từ `Bai10.xml`). Script sinh XMI cũ **không còn trong repo**, Agent phải dựng lại từ một file `SD_0x.xml` có sẵn. | Mã hóa `windows-1252`: **không** dùng ký tự tiếng Việt có dấu trong tên/nhãn XMI, dùng tiếng Anh hoặc tiếng Việt không dấu. Khung `alt/opt/loop` **chưa có ground truth** trong EA 2.5 XMI, tránh dùng (Tuan2 Mục 5.2). Verify: `xml.dom.minidom` + đối chiếu `sender/receiver` và `DiagramElement`. |
| draw.io (`TLCN.drawio.xml`, sơ đồ mới) | Sửa/viết mxGraph XML trực tiếp. | Không render được trong phiên: Agent chỉ verify well-formed và tham chiếu `source/target`; **người mở diagrams.net xem** (task 👤). Ảnh PNG phải xuất lại bằng tay. |
| `ClassDiagram.puml` / `.mmd` | Sửa text. | `.puml` và `.mmd` hiện lệch nhau và lệch schema (Mục 2, F5); sửa cả hai cùng đợt. |
| `schema.prisma` | Chỉ sửa file schema + SQL tùy chỉnh; **không chạy migration lên DB dùng chung**. | Verify bằng `npx prisma validate` và `prisma migrate diff --from-schema-datamodel <cũ> --to-schema-datamodel <mới> --script` (không cần DB). Sau DC-19 không còn composite FK `institution_id`; kiểm composite FK `(exam_round_id, student_id)` của MD-02 ở bước validate. |
| Markdown tracking/UI | Sửa trực tiếp. | Giữ ID màn hình `S01–S15` đã dùng ở Tuan4; ID mới đánh tiếp từ `S16`. |

---

## 2. Kiểm chứng nguồn và các điểm lệch phát hiện khi đọc

| # | Điều đã kiểm | Kết quả |
|---|---|---|
| V1 | Vị trí SRS v2.6 Final | **Không có ở `0.docs/`** như bạn ghi. Có ở `docs-repo/requirements/` và `0.docs - Sao chép/` (trùng byte). `CLAUDE.md` gốc vẫn trỏ `0.docs/SRS_TLCN_v2.6_Final.docx` (đường dẫn không tồn tại). |
| V2 | Vị trí đặc tả 24 UC | `D:\TLCN\20260922_MoHinhHoaYeuCau.docx` (gốc) trùng byte với `docs-repo/requirements/`. |
| V3 | Vị trí Rubric | Chỉ ở `0.docs - Sao chép/` (không có ở `0.docs/`). |
| V4 | `0.docs` vs `docs-repo` | `docs-repo/tracking` **lệch** `0.docs/tracking` (`DECISIONS_LOG.md`, `AI_USAGE_LOG.md` khác; `ci-cd.md` và `status-reports/*.docx` chỉ có ở `0.docs`). Bản làm việc hiện hành là `0.docs` (đã chốt qua câu hỏi vị trí: sửa tại chỗ, đồng bộ sang `docs-repo` ở cuối). |
| V5 | Trạng thái code | `backend/backend` (NestJS, module: ai-explainer, auth, cat-engine, health, item-bank, language-profile, reporting, test-session) và `frontend` (Next, route `(student)`, `(teacher)`, `(exam)`, `(public)`) **đã tồn tại**; chưa `git init`. `CLAUDE.md` còn ghi "chưa có code". |
| V6 | Schema hiện tại | `User` chưa có `mustChangePassword`; chưa có `exam_rounds`, `exam_round_participants`; `TestSession` chưa có `examRoundId`, `expiresAt`; `AuthProviderType` có `LOCAL/GOOGLE/MICROSOFT` (không cần đổi, tài khoản import dùng `LOCAL`). |
| V7 | Quyết định mật khẩu | `Tuan4/20261010_PHAN_TICH...` ghi **bcrypt**, nhưng `DECISIONS_LOG` **#62 (Q3) đã chốt `argon2`**. **Kế hoạch dùng argon2.** |
| V8 | UCADM02 | Đặc tả hiện có luồng thay thế "Import hàng loạt CSV". UCADM02/03/07, UCGV10 **đã bị cắt khỏi TL ở #53**. Import tài khoản quay lại dưới dạng **UC mới có phạm vi hẹp** (chỉ tạo mới sinh viên), không phục hồi UCADM02. |
| V9 | UCSV01 hiện tại | Còn "Đăng nhập qua EduZ SSO" ở luồng thay thế và "email/MSSV". Phải sửa theo #85. |
| V10 | Hạn phiên hiện tại | #77: hạn = `CAT_TIMEOUT_MINUTES` (45) + dung sai cấu hình, **không** dùng TTL Redis 7200s; luật K5: đóng quá hạn ≥8 câu ⇒ `COMPLETED`+`TIMEOUT`, ít hơn ⇒ `ABANDONED`. Kỳ thi phải khớp với luật này (D-T). |
| V11 | Số quyết định | Số lớn nhất hiện có trong `DECISIONS_LOG` là **#83** (một số dòng nằm sai thứ tự trong bảng, ví dụ #79 trước #75). Quyết định mới bắt đầu từ **#84**. |
| V12 | Rubric TC2.1 | Mức 5 cần **≥4 loại sơ đồ** trong {context, component, ERD/class, sequence, deployment}, khớp 100% mã nguồn khi đối chiếu ngẫu nhiên; **100% UC có acceptance criteria**, có business rules. Hiện có: class/ERD (có), sequence (5 file). Thêm component + deployment ⇒ **đúng 4 loại, sát ngưỡng** (không có dư địa). |

**Các điểm lệch có sẵn của `ClassDiagram.puml` (không do yêu cầu này gây ra; xử lý cùng đợt theo quy tắc 7):**

| ID | Điểm lệch | So với |
|---|---|---|
| F1 | Enum `Skill` còn `WRITING` | #22 (A5) đã bỏ khỏi schema |
| F2 | `Institution "1" --> "0..*" User` | **Hết hiệu lực:** xóa `Institution` hoàn toàn (DC-19) |
| F3 | `Explanation` nối `SessionResponse`; `explain(item, response)` | #60/#63: gắn `Item`; sinh lúc soạn câu hỏi |
| F4 | Dùng `SessionStatus`, `ItemSource`, `CEFRConfidence`, `Severity` nhưng không khai báo enum | Schema có đủ |
| F5 | `Item` còn `exposureRate`, `pValue`, `itemFitMnsq`, `calibrated`, `timesUsed` | Class Diagram mới (`Mo_ta`, 2026-09-18) đã bỏ; schema hiện còn một số cột; **cần đối chiếu từng cột trước khi sửa** |
| F6 | `User`/`Student` thiếu `studentCode`, `passwordHash`, `authProvider` | Schema có |
| F7 | `TestSession` thiếu `studentId`, `startedAt`, `completedAt` | Schema có |
| F8 | `ItemBank` còn trong `.puml` | `Mo_ta` (2026-09-18) đã bỏ `ItemBank`, `findForCAT` chuyển sang `Item` |
| F9 | `.puml` còn `EduZServiceAccount` | Đã loại khỏi phạm vi TL |

---

## 3. Đặc tả nghiệp vụ — nguồn chân lý của kế hoạch

### 3.1. Đã chốt (bạn trả lời qua `AskUserQuestion` ngày 2026-10-12)

| ID | Nội dung đã chốt | Ghi vào |
|---|---|---|
| DC-01 | **Phạm vi = Phương án B:** Admin import tài khoản SV; ~~Giảng viên~~ **Admin** tạo kỳ thi và import danh sách thi (sửa theo DC-18, DC-19). Đảo một phần #59. | #84 |
| DC-02 | **Đăng nhập chỉ bằng email + mật khẩu.** Bỏ Google/Microsoft SSO khỏi Tiểu luận. EduZ SSO giữ ở gói Khóa luận. Đảo một phần #24/#28; phần "import sẵn danh sách, khớp theo email" của #28 giữ nguyên. | #85 |
| DC-03 | Mật khẩu tạm **gửi email tự động** qua `MailPort` + SMTP (nodemailer), **đẩy qua hàng đợi BullMQ có retry**. Đăng nhập lần đầu **bắt buộc đổi mật khẩu**. | #86 |
| DC-04 | ⚠️ **Một phần bị DC-22 thay (preview/confirm → upload/grid/save).** **Import 2 bước:** `preview` (phân tích + báo lỗi chi tiết, **chưa lưu**) rồi `confirm` (mới lưu). Dữ liệu tạm giữ ở **Redis, khóa có TTL ~30 phút**. Áp dụng **cả hai loại import**. Email mật khẩu tạm chỉ gửi **sau confirm**. | #87 |
| DC-05 | ⚠️ **Một phần bị DC-24 thay (nay import/tạo được cả GV).** **Import tài khoản (Admin):** chỉ **tạo mới sinh viên**; trùng email/MSSV ⇒ báo lỗi từng dòng; không import giảng viên; không cập nhật tài khoản có sẵn. | #87 |
| DC-06 | ⛔ **"All-or-nothing" bị DC-22 thay** (giữ: GV chỉ tra MSSV, không tạo tài khoản). **Import danh sách thi (GV): all-or-nothing.** Chỉ cho `confirm` khi **0 dòng lỗi**. MSSV không tồn tại trong hệ thống ⇒ báo lỗi chi tiết từng dòng. GV chỉ tra MSSV, **không tạo tài khoản**. | #87 |
| DC-07 | **Sinh viên bắt buộc thuộc một kỳ thi đang mở** mới bắt đầu được bài. ~~Giảng viên tạo kỳ~~ → **đảo bởi DC-18/DC-19:** chỉ Admin tạo kỳ (hệ thống đơn trường). | #88 |
| DC-08 | **1 phiên/kỳ/sinh viên, trừ phiên `ABANDONED`** (được thi lại trong cùng kỳ nếu cửa sổ còn mở). Một sinh viên có thể nằm trong **nhiều kỳ**. | #88 |
| DC-09 | **`closes_at` là hạn cứng**: ví dụ của bạn (kỳ 10h–11h, SV vào 10h30 chỉ còn 30 phút). Phiên bị đóng tại `closes_at` theo luật K5 (#77). *(Suy ra từ ví dụ; phần "thời lượng" còn mở ở D-T.)* | #88 |
| DC-10 | Trạng thái kỳ thi **lưu cột** `status` (enum `ExamRoundStatus`: DRAFT, SCHEDULED, OPEN, CLOSED); chuyển trạng thái **kiểu lazy**: tính theo giờ khi đọc/ghi, ghi lại cột khi chạm tới; không scheduler. | #89 |
| DC-11 | **Quên mật khẩu: sinh viên tự bấm "Quên mật khẩu" và tự đặt lại qua email** (bạn nêu: "quên tự bấm quên mật khẩu cập nhật lại"). Cơ chế cụ thể ở D-FP. Không có chuyện "import trùng để lấy lại mật khẩu"; import trùng chỉ báo lỗi dòng (DC-05). | #90 |
| DC-12 | **Phiên bản SRS mới = v3.0**, tạo `.docx` mới, giữ nguyên v2.6 Final. Sửa bản làm việc **tại chỗ có backup** (`0.docs` + gốc `D:\TLCN`), sản phẩm mới vào `Tuan5/`, **cuối cùng đồng bộ** sang `docs-repo` (không push). | #91 |
| DC-13 | **Sơ đồ bổ sung:** Component + Deployment. Phương hỏi AI riêng để đối chiếu. | #92 |
| DC-14 | **Đăng nhập chỉ nhận email** (đổi nhãn FE "Email hoặc MSSV" thành "Email"; DTO giữ `@IsEmail`). | #85 |
| DC-15 | ⛔ **THAY BỞI DC-19 (không còn hiệu lực).** **Phân biệt 3 cấp người dùng quản trị/giảng dạy, KHÔNG thêm role, KHÔNG thêm cột/bảng:** (1) **GV thường** = `role=TEACHER`, `institution_id` NOT NULL; (2) **QTV đơn vị (GV-QTV)** = `role=ADMIN` **và** `institution_id IS NOT NULL` (là một giáo viên của trường đó, được cấp quyền quản trị trong trường); (3) **QTV hệ thống** = `role=ADMIN` **và** `institution_id IS NULL`, có mọi quyền như kế hoạch cũ (mọi đơn vị). Quy tắc quyết định: `role=ADMIN ∧ institution≠null ⇒ có quyền thêm/quản lý tài khoản SV cho đúng trường đó`. Admin vẫn là siêu tập của Teacher (Tuần 1), nên GV-QTV có đủ quyền GV **trong trường của mình**. | #95 |
| DC-16 | ⛔ **THAY BỞI DC-19 (không còn hiệu lực).** **Phạm vi GV-QTV:** import tài khoản SV **và quản lý tài khoản SV đầy đủ** (xem danh sách, sửa họ tên/email, khóa/mở khóa, gửi lại mật khẩu tạm), **chỉ trong trường của mình**. | #95 |
| DC-17 | ⛔ **THAY BỞI DC-19 (không còn hiệu lực).** **Gán quyền GV-QTV** qua **màn hình riêng của QTV hệ thống** (chọn GV của một trường ⇒ nâng lên GV-QTV, hoặc thu hồi). Nâng/thu hồi = đổi `role` TEACHER↔ADMIN, giữ nguyên `institution_id`. | #95 |
| DC-18 | **Thu hẹp quyền GV thường (đảo một phần DC-07/#88):** (1) **GV thường** (`TEACHER`) chỉ: đăng nhập/đổi/quên mật khẩu, **xem báo cáo lớp (lọc theo kỳ), tra cứu hồ sơ SV** trong trường mình. (2) **GV-QTV và QTV hệ thống** làm: **soạn câu hỏi** vào ngân hàng ("tạo đề" = tạo `Item`, UCGV02–04), **duyệt câu hỏi** (UCGV05; **GV-QTV tự duyệt trong trường**, người soạn và người duyệt có thể là một người), **tạo kỳ thi, import danh sách thi, theo dõi dự thi** (UCADM15–17), **import + quản lý tài khoản SV** (UCADM08–09). (3) Chỉ QTV hệ thống: UCADM10, quản lý `Institution`/GV/QTV. ID UC giữ nguyên, **actor đổi sang `Admin`**; GV thường không thấy các màn S08–S11, S19–S24. Hệ quả: duyệt câu hỏi không tách người soạn/người duyệt (rủi ro chất lượng câu hỏi, ghi vào Risk SRS XIV). | #96 |
| DC-19 | **Hệ thống đơn trường (single-tenant):** (1) **Xóa bảng `institutions` và mọi cột/ràng buộc `institution_id`** (users, exam_rounds, exam_round_participants, test_sessions…), kể cả composite FK/CHECK tenant (#22, #27, MD-03, `chk_users_institution_required`). (2) **Bỏ QTV hệ thống và khái niệm GV-QTV**; `ADMIN` = **Admin của trường**, giữ nguyên 4 giá trị `UserRole` (STUDENT/TEACHER/ADMIN/EDUZ_SERVICE), Admin là siêu tập của Teacher. Chức năng Admin = tập chức năng DC-18 (soạn/duyệt câu hỏi, kỳ thi, import danh sách thi) + import/quản lý tài khoản SV (UCADM08–09) + **quản lý tài khoản giảng viên và cấp/thu hồi quyền Admin** (gộp vào UCADM09). (3) **Bỏ UCADM10 và S25**; không còn bộ chọn Đơn vị, không còn `resolveScope`/`AccessScope`. (4) **Tài khoản Admin đầu tiên tạo bằng seed.** (5) Muốn đa trường sau này ⇒ phạm vi **Khóa luận**, phải làm lại schema. | #97 |
| DC-20 | **D-T = T2:** kỳ thi có `durationMinutes` (GV/Admin nhập, mặc định hiển thị 45, ràng buộc 5 ≤ duration ≤ 180 và duration ≤ closes − opens); `test_sessions.expires_at = min(startedAt + durationMinutes, closesAt)` tính **một lần lúc bắt đầu phiên** và lưu DB. Sửa SRS IV.5: "45' là mặc định, ghi đè được theo kỳ". | #93 |
| DC-21 | **D-FP = C (OTP 6 số):** SV nhập email ⇒ hệ thống luôn trả 202; nếu tồn tại thì sinh mã OTP 6 chữ số (`crypto.randomInt`), **lưu bản băm trong Redis TTL 10 phút** (đề xuất AI, chưa hỏi), gửi qua `MailPort`/BullMQ; SV nhập email + mã + mật khẩu mới ở màn hình đặt lại; **tối đa 5 lần nhập sai** rồi hủy mã (đề xuất AI), rate limit theo email + IP; mã dùng 1 lần; đặt lại xóa `mustChangePassword`, không tự đăng nhập. Không đổi schema. | #94 |
| DC-22 | **Import theo "lưới tạm" (grid), áp dụng cả import tài khoản SV (UCADM08) và import danh sách thi (UCADM16):** (1) mỗi lần tải file `.xlsx`, BE phân tích và **gộp vào grid tạm** của người thao tác (Redis, khóa theo người dùng + loại import [+ kỳ thi], TTL ~30', làm mới mỗi lần thêm); **chưa ghi DB**. (2) **Dòng lỗi bị loại khỏi grid** (thiếu cột, sai định dạng email, trùng ngay trong file…) và **hiện popup liệt kê số dòng + lý do**. (3) **Tải thêm file khác:** dòng đã có trong grid thì **bỏ qua** (chỉ thêm dòng chưa có); (4) với **import tài khoản**: email/MSSV **đã tồn tại trong DB** ⇒ không vào grid, popup báo "tài khoản đã tồn tại"; với **import danh sách thi**: MSSV không tồn tại trong hệ thống ⇒ loại + popup; MSSV đã có trong kỳ ⇒ loại + popup "đã có trong kỳ". (5) Admin có thể xóa dòng/xóa cả grid. (6) **Bấm "Lưu" mới ghi DB** (một transaction), rồi (import tài khoản) sinh mật khẩu tạm + xếp hàng email. Hết TTL ⇒ `410 IMPORT_GRID_EXPIRED`. **Đảo:** phần "all-or-nothing" của DC-06, `preview/confirm` của DC-04, MD-06 (`SKIPPED`), Q-1/BR-04. Giữ: DC-05 (chỉ tạo mới SV, không cập nhật tài khoản có sẵn), email chỉ gửi sau Lưu, giới hạn file MD-08. Tên endpoint ở Phụ lục B là đề xuất. | #98 |
| DC-23 | **Khóa tài khoản = cột `users.is_active BOOLEAN NOT NULL DEFAULT true`** (Q-8). | #98 |
| DC-24 | **Tạo tài khoản SV và GV (đảo một phần DC-05):** Admin tạo **từng người (form)** hoặc **import file (lưới tạm DC-22)**, cho cả `STUDENT` và `TEACHER`. File SV: MSSV, Họ tên, Email; file GV: Mã GV (`teacherCode`), Họ tên, Email. Cả hai cách đều sinh mật khẩu tạm, `mustChangePassword=true`, gửi email sau khi lưu. Trùng email/MSSV/`teacherCode` ⇒ báo lỗi (popup khi import). Vẫn **không cập nhật** tài khoản có sẵn bằng import. API đề xuất: `POST /students`, `POST /teachers`; `POST /users/import/upload` thêm `kind=STUDENT\|TEACHER`, grid khóa theo (adminId, kind). Tạo từng người gộp vào UCADM09, import vào UCADM08 (cả hai là đề xuất, tránh thêm UC). | #99 |
| DC-25 | **`exam_rounds.duration_minutes` NOT NULL DEFAULT 45** (CHECK 5..180) — chốt sau câu hỏi của agent schema; thay `Int?` ở Phụ lục A. | #100 |
| DC-26 | **EAP: giữ lưới đều 41 điểm θ ∈ [−4,+4], bước 0.2, prior N(0,1)** (K7); sửa mô tả "Gaussian–Hermite quadrature" trong SRS, `CLAUDE.md` (đề xuất diff) và các tài liệu mô tả. **Không đổi thuật toán.** | #101 |

### 3.2. Đã chọn (D-T = T2, D-FP = C); bảng phương án giữ để truy vết

#### D-T — Mô hình giờ làm bài của kỳ thi (task W0.2)
**Vấn đề:** ví dụ của bạn có "kỳ 10h–11h, thời gian làm bài 1 tiếng". SRS Mục 4.5 hiện đặt trần **45 phút** (hard stop). Kỳ thi phải lưu những trường thời gian nào, và hạn riêng của mỗi phiên tính ra sao?

| | T1 — Chỉ cửa sổ, giữ trần 45' | **T2 — Thêm `durationMinutes` theo kỳ (đề xuất)** | T3 — Hạn = `closes_at`, bỏ trần riêng |
|---|---|---|---|
| Trường kỳ thi | `opensAt`, `closesAt` | `opensAt`, `closesAt`, `durationMinutes` (GV nhập; mặc định hiển thị = 45) | `opensAt`, `closesAt` |
| Hạn phiên `expiresAt` | `min(startedAt + 45', closesAt)` | `min(startedAt + durationMinutes, closesAt)` | `closesAt` |
| Ví dụ 10h–11h, vào 10h30 | còn 30' | còn `min(duration, 30')` = 30' nếu duration ≥ 30 | còn 30' |
| Ví dụ 10h–11h, vào 10h05 | tối đa 45' | tối đa `min(duration, 55')` (duration=60 ⇒ 55', do chạm `closesAt`) | 55' |
| Đổi SRS 4.5 (trần timeout) | Không | **Có**: "45' là mặc định, ghi đè được theo kỳ" | **Có**: bỏ trần cho phiên thuộc kỳ |
| Khớp ví dụ "làm bài 1 tiếng" | **Không** (SV vào đầu giờ chỉ có 45', không phải 60') | **Có** | Có, nhưng SV có thể ngồi lâu hơn nhu cầu |
| Rủi ro | Ít nhất; lệch ví dụ của bạn | Thêm 1 cột + ràng buộc (ví dụ 5 ≤ duration ≤ 180, `duration ≤ closes − opens`); NFR/KPI "thời gian TB <25'" không đổi | Mất trần an toàn; một SV bỏ treo máy giữ phiên đến hết cửa sổ; lệch SRS 4.5 nhiều nhất |
| Lưu `test_sessions.expires_at` | Có | Có | Có |

**Điểm chung ở cả ba:** `expires_at` được **tính một lần lúc bắt đầu phiên và lưu vào `test_sessions`**, để (a) FE hiện đồng hồ đúng (#52), (b) sửa kỳ thi sau đó không làm đổi hạn phiên đang chạy, (c) lazy cleanup của #77 chỉ cần so `now > expires_at`. Giới hạn 25 câu và các điều kiện dừng khác **không đổi**.
**Khuyến nghị của AI:** T2. **Bạn chọn: T2** ✅ (2026-10-13, DC-20, #93).

#### D-FP — Cơ chế Quên mật khẩu (task W0.3)
| | **A — Link token, lưu Redis TTL (đề xuất)** | B — Link token, lưu bảng DB | C — Mã OTP 6 số |
|---|---|---|---|
| Cách làm | Email chứa link `/reset-password?token=…`; BE lưu **hash** của token trong Redis, TTL 30', dùng 1 lần | Như A nhưng bảng `password_reset_tokens` | Email chứa mã 6 số, nhập ở màn hình |
| Đổi schema | Không | Thêm 1 bảng + migration | Không (nếu Redis) |
| Bảo mật | Token 32 byte ngẫu nhiên; phản hồi luôn 202 (không lộ email tồn tại); rate limit theo email + IP | Như A, có lịch sử | Dễ brute force hơn, phải giới hạn số lần thử |
| Trải nghiệm | Bấm link | Bấm link | Gõ mã |
| Rủi ro | Redis restart làm mất token đang chờ (SV xin lại) | Thêm bảng cần dọn rác | Cần thêm trạng thái "đã nhập mã" |
**Điểm chung:** mọi cách đều dùng `MailPort`, hàng đợi BullMQ và thao tác đặt lại phải xóa cờ `mustChangePassword`. Đặt lại mật khẩu **không** đăng nhập tự động.
**Bạn chọn: C (OTP 6 số)** ✅ (2026-10-13, DC-21, #94). TTL 10 phút và tối đa 5 lần nhập sai là đề xuất AI.

### 3.3. Đề xuất mặc định — **duyệt kế hoạch = chốt** (bạn có thể gạch/sửa từng dòng ở W0.1)

| ID | Đề xuất | Phương án khác | Lý do / đánh đổi |
|---|---|---|---|
| MD-01 | `test_sessions.exam_round_id` **NOT NULL**; dữ liệu seed/dev cũ được tạo lại (chưa có dữ liệu thật; staging seed tạo lại được, #70) | Nullable + kiểm trong code | DB tự bảo đảm DC-07. Hệ quả: seed/E2E hiện có phải sửa. |
| MD-02 | DB ép "SV phải thuộc kỳ": composite FK `(exam_round_id, student_id) → exam_round_participants(round_id, student_id)` | Chỉ kiểm trong use-case | Cùng tiền lệ composite FK của #27. Phải kiểm Prisma chấp nhận ở bước validate; không được thì dừng hỏi. |
| MD-03 | ⛔ **BỎ theo DC-19** (không còn `institution_id`; `exam_round_participants` chỉ có FK đơn `round_id`, `student_id`) | — | — |
| MD-04 | Partial unique index `test_sessions(exam_round_id, student_id) WHERE status <> 'ABANDONED'` (DC-08), cùng index `(student_id) WHERE status='IN_PROGRESS'` của #58 (kiểm đã có chưa trong `custom_migrations.sql`) | Kiểm trong code | Chống race hai request, đúng tinh thần #58/#77. |
| MD-05 | `POST /sessions` nhận **`examRoundId` bắt buộc**; FE hiện danh sách kỳ SV thuộc và đang mở | BE tự chọn nếu chỉ có một kỳ | Không âm thầm đoán (cùng lý do #58). SV nằm ≥2 kỳ mở chồng giờ vẫn rõ ràng. |
| MD-06 | ⛔ **Thay bởi DC-22:** MSSV đã có trong kỳ ⇒ bị loại khỏi grid kèm popup "đã có trong kỳ" (không còn trạng thái `SKIPPED`) | — | — |
| MD-07 | GV được **gỡ SV khỏi kỳ** (`DELETE …/participants/:studentId`) khi kỳ chưa `CLOSED` và SV chưa có phiên trong kỳ đó | Không cho gỡ | Sửa nhầm danh sách mà không phải hủy kỳ. |
| MD-08 | Giới hạn file: `.xlsx`, ≤ 2 MB, ≤ 1000 dòng dữ liệu (SRS: 50–500 SV/đợt); dòng đầu là tiêu đề; cột Phụ lục C; file mẫu tĩnh ở FE `public/templates/` (dữ liệu giả) | Cho CSV | Một định dạng, ít nhánh test. Chặn công thức/macro: đọc giá trị, bỏ công thức. |
| MD-09 | ⛔ **BỎ theo DC-19** (không còn chọn đơn vị khi import tài khoản; file vẫn chỉ 3 cột MSSV, Họ tên, Email) | — | — |
| MD-10 | Mật khẩu tạm: 12 ký tự ngẫu nhiên từ `crypto.randomInt`, băm **argon2** (theo #62), sinh **lúc confirm**, không lưu bản rõ ngoài hàng đợi email; `mustChangePassword = true`; chặn mọi route trừ `change-password`, `me`, `logout` bằng guard (mã lỗi `PASSWORD_CHANGE_REQUIRED`) | Mật khẩu hết hạn sau N ngày | Chưa có yêu cầu hết hạn; thêm sau nếu cần. Payload hàng đợi chứa mật khẩu rõ phải mã hóa/được xóa sau gửi (task PI.9). |
| MD-11 | Tên class mới (tiếng Anh): `ExamRound`, `ExamRoundParticipant`, `ExamRoundStatus` (enum), `ImportReport`, `ImportRowResult`, `ImportRowStatus` (enum VALID/ERROR/SKIPPED), `UserImportService <<service>>`, `RosterImportService <<service>>`, `MailPort <<interface>>`, `SmtpMailAdapter`, `PasswordResetService <<service>>` | Gộp hai service import thành một | Khớp 7b của phân tích Tuần 4. Tách theo actor để phân quyền rõ. |
| MD-12 | ID Use Case mới: `UCADM08` Import tài khoản sinh viên; `UCADM15` Quản lý kỳ thi; `UCADM16` Import danh sách sinh viên thi; `UCADM17` Theo dõi dự thi của kỳ; `UCSV08` Đổi mật khẩu; `UCSV09` Quên mật khẩu. `UCSV08/09` **dùng chung cho GV/Admin** (không nhân bản như UCxx01) | Nhân bản UC cho từng actor | Tránh phình số UC (Rubric đòi AC cho 100% UC). |
| MD-13 | ID màn hình mới tiếp từ `S16` (Mục 4.6); Admin dùng chung giao diện GV (#53) | — | Không đổi ID đã dùng ở Tuan4. |
| MD-15 | ⛔ **THAY theo DC-19:** không còn `resolveScope`/phạm vi theo trường. Dùng `RolesGuard` dùng chung theo `role`: `TEACHER` chỉ đọc báo cáo/hồ sơ; `ADMIN` làm mọi chức năng quản trị | Giữ policy `resolveScope` | Chỉ còn một cấp Admin nên policy phạm vi thừa. `ADMIN` không bắt buộc có `teacher_profiles` (Q-6 đóng: giữ dòng cũ nếu có) |
| MD-14 | SRS v3.0 **gộp luôn** các "đề xuất SRS v2.7" còn tồn trong `DECISIONS_LOG`/weekly-log/Tuan4 (ví dụ: bỏ SSO #24/#85, #53, #56, #60/#63, #64, K5, Explanation theo Item) | v3.0 chỉ chứa phần import/kỳ thi | Nếu không gộp thì v3.0 lệch với chính các quyết định đã chốt. Tăng khối lượng soạn SRS; danh mục tổng hợp ở W1.1. |

### 3.4. Quy tắc nghiệp vụ (business rules) — nguồn cho SRS, UC và test

| ID | Quy tắc |
|---|---|
| BR-01 | Tài khoản sinh viên chỉ được tạo qua import của **Admin** (DC-19); không tự đăng ký. |
| BR-02 | Email duy nhất toàn hệ thống (không phân biệt hoa thường); MSSV (`student_code`) duy nhất toàn hệ thống (đã `@unique`). |
| BR-03 | Dòng import tài khoản hợp lệ khi: MSSV, Họ tên, Email không rỗng; email đúng định dạng; không trùng trong grid hiện có; không trùng trong DB. Dòng không hợp lệ bị loại khỏi grid và báo qua popup (DC-22). |
| BR-04 | **Lưu theo grid (DC-22):** nút Lưu ghi **mọi dòng đang có trong grid** (đã lọc lỗi) trong một transaction; dòng lỗi/đã tồn tại không bao giờ vào grid nên không chặn Lưu; Lưu khi grid rỗng bị từ chối. (Thay BR-04 cũ.) |
| BR-05 | Tài khoản mới: `role=STUDENT`, `authProvider=LOCAL`, `mustChangePassword=true`. Email chỉ gửi sau khi bấm Lưu; gửi thất bại sau retry ⇒ ghi trạng thái "chưa gửi" để Admin xem được, không rollback tài khoản. |
| BR-06 | Đổi mật khẩu: mật khẩu mới ≠ mật khẩu hiện tại; độ dài tối thiểu (đề xuất 8, chốt ở W1.3 theo SRS 15.3); sau thành công `mustChangePassword=false`, cấp lại token. |
| BR-07 | **Chỉ Admin** tạo/sửa/công bố/đóng kỳ và import danh sách thi (DC-18, DC-19); GV thường chỉ xem kết quả. |
| BR-08 | `opensAt < closesAt`; kỳ `DRAFT` sửa tự do; sau `SCHEDULED` chỉ cho sửa tên và `closesAt` kéo dài (đề xuất, chốt ở W1.5); không sửa kỳ `CLOSED`. |
| BR-09 | Danh sách thi của một kỳ chỉ gồm tài khoản `role=STUDENT` đã tồn tại. |
| BR-10 | Bắt đầu phiên chỉ hợp lệ khi: SV thuộc danh sách của kỳ được chọn; kỳ ở trạng thái hiệu lực `OPEN` tại thời điểm hiện tại; SV chưa có phiên `IN_PROGRESS` (409 theo #58); SV chưa có phiên `COMPLETED` trong kỳ đó (DC-08). |
| BR-11 | `expires_at` của phiên tính theo D-T một lần lúc bắt đầu. Quá `expires_at` ⇒ luật K5/#77 (≥8 câu ⇒ `COMPLETED`+`TIMEOUT`; ít hơn ⇒ `ABANDONED`). |
| BR-12 | Kỳ `CLOSED` thủ công (GV bấm đóng): phiên đang chạy **không bị cắt ngay** hay **bị cắt**? **Chưa chốt** ⇒ câu hỏi mở Q-2; đề xuất: phiên đang chạy vẫn theo `expires_at`, chỉ chặn phiên mới (nhất quán DC-09 chỉ cắt theo `closes_at`). |
| BR-13 | Báo cáo lớp (UCGV07/08, UCADM05) lọc được theo kỳ; mặc định hiển thị toàn hệ thống. |
| BR-14 | Quên mật khẩu (DC-21, OTP): phản hồi luôn như nhau dù email có tồn tại hay không; rate limit; OTP 6 số dùng 1 lần, TTL 10', tối đa 5 lần nhập sai (đề xuất AI). |
| BR-15 | Mọi import ghi nhật ký kiểm toán tối thiểu: ai, khi nào, số dòng, kết quả (không ghi mật khẩu). |
| BR-16 | **Phân quyền chỉ theo `role` (DC-19):** `TEACHER` ⇒ chỉ xem báo cáo lớp và hồ sơ SV; `ADMIN` ⇒ mọi chức năng quản trị và chức năng Teacher; `STUDENT` ⇒ chỉ dữ liệu của mình. Không đủ quyền ⇒ `403`. |
| BR-17 | **Admin quản lý tài khoản giảng viên:** tạo, sửa, khóa/mở khóa; nâng `TEACHER`→`ADMIN` và thu hồi `ADMIN`→`TEACHER`. Admin không tự thu hồi quyền của chính mình. |
| BR-18 | **Nâng/thu hồi Admin:** ghi nhật ký kiểm toán (BR-15); **không thu hồi nếu đó là Admin cuối cùng** (đề xuất, vì không còn QTV hệ thống để cứu); token cũ của người bị đổi quyền phải mất hiệu lực quyền cũ (chốt ở W1.4). |
| BR-19 | **Quản lý tài khoản (Admin):** với SV và GV; khóa tài khoản ⇒ không đăng nhập được, phiên `IN_PROGRESS` xử lý theo K5; không xóa cứng tài khoản đã có phiên/hồ sơ (chỉ khóa). Gửi lại mật khẩu tạm ⇒ sinh mật khẩu mới, đặt lại `mustChangePassword=true`. |

### 3.5. Luồng chính (cơ sở cho Sequence Diagram và Use Case)

**L0 — Nâng/thu hồi Admin (thuộc UCADM09, DC-19):** Admin mở quản lý tài khoản GV ⇒ chọn GV ⇒ **Nâng lên Admin** / **Thu hồi** ⇒ `PATCH /users/:id/role` ⇒ BE đổi `role` TEACHER↔ADMIN, ghi kiểm toán. (UCADM10 đã bỏ.)
**L1 — Admin import tài khoản (UCADM08, DC-22):** Admin tải file `.xlsx` ⇒ `POST /users/import/upload` ⇒ BE kiểm định dạng/giới hạn, đọc dòng, kiểm BR-03 ⇒ **gộp vào grid tạm trong Redis** (khóa `import:accounts:<adminId>`, TTL ~30') ⇒ trả `{grid[], rejected[{row,mssv,reason}], added, ignoredDuplicates}` ⇒ FE hiện grid và **popup** các dòng bị loại (trùng DB ⇒ "tài khoản đã tồn tại") ⇒ Admin có thể tải thêm file (chỉ dòng chưa có trong grid được thêm) hoặc xóa dòng ⇒ bấm **Lưu** ⇒ `POST /users/import/save` ⇒ BE **tạo tài khoản trong một transaction**, sinh mật khẩu tạm, băm argon2 ⇒ đẩy job email vào BullMQ ⇒ trả `{created, queued}` ⇒ xóa grid. Hết TTL ⇒ `410 IMPORT_GRID_EXPIRED`.
**L2 — Đăng nhập lần đầu:** SV nhập email + mật khẩu tạm ⇒ `POST /auth/login` trả token kèm `mustChangePassword=true` ⇒ FE chuyển `/change-password` ⇒ guard chặn mọi route khác (`403 PASSWORD_CHANGE_REQUIRED`) ⇒ `POST /auth/change-password` ⇒ cờ về `false` ⇒ vào trang chủ.
**L3 — Admin tạo kỳ và danh sách thi (UCADM15, UCADM16; DC-18/19):** Admin tạo kỳ (`DRAFT`) ⇒ import danh sách (cùng cơ chế lưới tạm DC-22: dòng lỗi/MSSV lạ/đã có trong kỳ bị loại kèm popup, bấm Lưu mới ghi) ⇒ **Công bố** (`SCHEDULED`) ⇒ tới `opensAt` trạng thái hiệu lực là `OPEN` (lazy, DC-10) ⇒ tới `closesAt` là `CLOSED`.
**L4 — SV vào thi (UCSV02/03):** trang chủ liệt kê kỳ của SV (`GET /exam-rounds/mine`) ⇒ chọn kỳ đang mở ⇒ `POST /sessions {examRoundId}` ⇒ BE kiểm BR-10, tính `expires_at` ⇒ phiên bắt đầu. Sai điều kiện ⇒ `403 NOT_IN_ROUND` / `409 ROUND_NOT_OPEN` / `409 ROUND_ALREADY_COMPLETED` / `409 SESSION_IN_PROGRESS` (kèm `sessionId`, #58).
**L5 — Quên mật khẩu (UCSV09, DC-21):** SV nhập email ⇒ `POST /auth/forgot-password` ⇒ luôn `202` ⇒ nếu tồn tại, sinh OTP 6 số (hash lưu Redis TTL 10'), đẩy email ⇒ SV nhập email + OTP + mật khẩu mới ⇒ `POST /auth/reset-password {email, otp, newPassword}` ⇒ `mustChangePassword=false`, hủy mã (sai quá 5 lần ⇒ hủy mã).

### 3.6. Máy trạng thái kỳ thi (`ExamRoundStatus`)
`DRAFT` —(GV công bố, cần ≥1 SV trong danh sách và `opensAt` > bây giờ hoặc theo BR-08)→ `SCHEDULED` —(tới `opensAt`)→ `OPEN` —(tới `closesAt` hoặc GV đóng thủ công)→ `CLOSED`.
`DRAFT → CLOSED` (hủy) được phép. Không quay lui. **Hàm `effectiveStatus(round, now)`** là nguồn duy nhất cho mọi quyết định (BR-10); cột `status` chỉ được ghi lại khi chạm tới (lazy).

### 3.7. Mã lỗi nghiệp vụ đề xuất (cho SRS Mục X và hợp đồng API)
`PASSWORD_CHANGE_REQUIRED` (403), `NOT_IN_ROUND` (403), `ROUND_NOT_OPEN` (409), `ROUND_ALREADY_COMPLETED` (409), `SESSION_IN_PROGRESS` (409, kèm `sessionId`), `IMPORT_GRID_EXPIRED` (410), `IMPORT_GRID_EMPTY` (422), `IMPORT_FILE_INVALID` (400/413), `INVALID_RESET_OTP` (400), `RATE_LIMITED` (429). Định dạng lỗi hiện tại (`{statusCode, message, error, timestamp, path}`) chưa có mã ổn định; thêm trường `code` nằm trong kế hoạch BE (G-xx của Tuan4), kế hoạch này chỉ **dùng** nó.

### 3.8. Ma trận phân cấp quyền (DC-15…DC-17, BR-16…BR-19)

**Sau DC-19 chỉ còn 3 cấp theo `role` (không còn `institutionId`):**

| Chức năng | GV thường (`TEACHER`) | Admin của trường (`ADMIN`) |
|---|---|---|
| Soạn/sửa/duyệt `Item` (UCGV02–06; DC-18) | ❌ | ✅ (tự duyệt) |
| Tạo kỳ thi, import danh sách thi, theo dõi dự thi (UCADM15–17) | ❌ | ✅ |
| Báo cáo lớp (UCGV07/08) + tra cứu SV (UCGV09) | ✅ (quyền chính của GV thường) | ✅ |
| Import tài khoản SV (UCADM08) | ❌ | ✅ |
| Quản lý tài khoản SV và **tài khoản GV**, nâng/thu hồi Admin (UCADM09) | ❌ | ✅ |
| Tổng quan hệ thống, cấu hình (UCADM05) | ❌ | ✅ |
| Đổi/quên mật khẩu (UCSV08/09) | ✅ | ✅ |

**Hệ quả kỹ thuật:** (a) `RolesGuard` dùng chung (MD-15 mới); (b) không còn ca test phạm vi trường, thay bằng ca test `TEACHER` bị `403` ở API quản trị; (c) menu FE dựng theo `role`.

---

## 4. Danh mục tác động (impact matrix)

### 4.1. Tài liệu thiết kế
| Tài liệu | Thay đổi | Task |
|---|---|---|
| `SRS_TLCN_v3.0.docx` (mới) | Mục I.3 (người dùng), III (module + kiến trúc), IV.5 (timeout theo D-T), VI/VIII (DDL), IX (F-ID mới), X (API), XII (lộ trình), XIV (Risk), XV (15.3 bảo mật, 15.4 RBAC), XVII (lịch sử v3.0); mục mới "Nghiệp vụ Import & Kỳ thi"; mục mới "Sơ đồ thành phần/triển khai"; hấp thụ đề xuất v2.7 tồn đọng | W1.1–W1.6, W2.7 |
| `20260922_MoHinhHoaYeuCau.docx` | Sửa UCSV01/02/03/07, UCGV01/07/08, UCADM01; thêm 8 UC mới (kể cả UCADM09–10); mục 2.3, 2.5; đánh dấu UC ngoài phạm vi; thêm AC + BR | W1.7, W1.8, W3.1–W3.3 |
| `AdaptivePlacementTest.xml` | Thêm UC mới + quan hệ `extend`; sửa tên; ảnh JPG xuất lại bằng EA (👤) | W1.9 |
| `TLCN.drawio.xml` (trang `Trang-1`) | Thêm lớp/enum/quan hệ (Mục 4.3); sửa các lệch F1–F9; ảnh PNG xuất lại (👤) | W1.10 |
| `ClassDiagram.puml`, `ClassDiagram.mmd` | Đồng bộ với drawio | W1.11 |
| `Mo_ta_So_do_Lop_ClassDiagram.md` | Cập nhật mô tả, số class/enum, bảng quan hệ, xóa cảnh báo đã giải quyết | W1.12 |
| `Sequence`: `SD_01`, `SD_02`, `SD_05` (cập nhật), `SD_06/07/08` (mới) | Mục 6.2 | W1.14, W1.15 |
| `Tuan4/20261009_MO_TA_LUONG_VA_MAN_HINH_CHO_AI_SINH_UI.md`, `20261010_MO_TA_MAN_HINH_TOI_GIAN_THEO_ROLE.md`, `20261010_PROMPT_SINH_UI_3_ROLE.md` | Màn mới S16–S25; sửa S01/S02/S03/S04/S12 | W1.16 |
| `Tuan4/20261010_PHAN_TICH_TAC_DONG_...md` | Thêm ghi chú đầu file "Đã giải quyết bởi Quyết định #84–#92, xem Tuan5" | W1.16 |
| `CLAUDE.md` (gốc + `0.docs/CLAUDE.md`) | Sửa số class/enum, dòng Auth/SSO, trạng thái "chưa có code"; **đề xuất diff, 👤 duyệt** (CLAUDE.md quy định chỉ đổi khi tech stack/quy tắc đổi thật) | W1.18 |

### 4.2. Schema Prisma / DB (đề xuất — xem Phụ lục A)
- `enum ExamRoundStatus { DRAFT SCHEDULED OPEN CLOSED }`.
- `User`: `mustChangePassword Boolean @default(false)`, `passwordChangedAt DateTime?`.
- Bảng mới `exam_rounds`, `exam_round_participants` (Phụ lục A).
- `TestSession`: `examRoundId` (NOT NULL, MD-01), `expiresAt`.
- SQL tùy chỉnh: partial unique indexes (MD-04), `CHECK (closes_at > opens_at)`, `CHECK` cho `duration_minutes` nếu chọn T2.
- **DC-19 (đơn trường): XÓA bảng `institutions` và mọi cột `institution_id`** cùng FK/CHECK/unique liên quan (`chk_users_institution_required`, composite FK #27, `@@unique([id, institutionId])` ở `exam_rounds`); `UserRole` giữ 4 giá trị. Kiểm ở W1.13 bằng `prisma validate` + `migrate diff`; xác nhận không còn tham chiếu `Institution` trong `seed.ts`/mã BE. "Khóa tài khoản" (BR-19) vẫn cần trạng thái: đề xuất `User.isActive Boolean @default(true)` — chờ **Q-8**.
- Không đổi `AuthProviderType`. Không thêm bảng `import_batches` (Redis, #87) và không thêm bảng token (nếu D-FP = A).
- Seed: băm mật khẩu (argon2), thêm 1 kỳ mẫu và danh sách dữ liệu giả.

### 4.3. Class Diagram (đề xuất)
**Thêm:** `ExamRound {id, name, createdBy, opensAt, closesAt, durationMinutes?, status; isOpen(now), effectiveStatus(now), includes(student)}`, `ExamRoundParticipant {note}` (lớp liên kết), `ExamRoundStatus`, `ImportReport {total, valid, errors, skipped, rows}`, `ImportRowResult {rowNumber, status, message}`, `ImportRowStatus`, `UserImportService.importStudents(file)`, `RosterImportService.importRoster(round, file)`, `MailPort.send(message)`, `SmtpMailAdapter`, `PasswordResetService.request(email)/reset(token, newPassword)`.
**Sửa:** `User` (+`mustChangePassword`, +`changePassword(old, new)`), `TestSession` (+`examRound`, +`expiresAt`), `ClassReport` (+`examRoundId` tùy chọn), `Teacher` (**không** thêm quan hệ kỳ thi/import; DC-18), `Admin` (+`creates ExamRound`, `uses RosterImportService`, tạo/duyệt `Item`), `Admin` (+`uses UserImportService`, +`AccountAdminService`) và `AccountAdminService <<service>>` (`list/update/lock/unlock/resendTemporaryPassword` cho SV và GV, `grantAdmin(teacherId)/revokeAdmin(adminId)`; **tên chờ duyệt**). **Xóa** class `Institution`, quan hệ `Institution–User` và thuộc tính `institution`/`institutionId` ở mọi class (DC-19), `AuthProvider` (chỉ `JwtAuthProvider` trong gói TL; `EduZSSOAdapter`/`EduZSSOClient` chuyển gói Khóa luận), `Student` (+`studentCode`), `Explanation` gắn `Item` (F3), bỏ `ItemBank` (F8) và `EduZServiceAccount` (F9), `Skill` bỏ `WRITING` (F1), khai báo enum thiếu (F4), đồng bộ cột `Item` (F5), `TestSession` đủ field (F7).
**Quan hệ mới:** `Admin 1 → 0..* ExamRound : creates` (DC-18); `ExamRound 1 ◆ 0..* ExamRoundParticipant`; `Student 1 → 0..* ExamRoundParticipant`; `ExamRound 1 ← 1..* TestSession` (bội số `1` vì MD-01); `ClassReport ..> ExamRound`; `Admin ..> UserImportService`; `Admin ..> RosterImportService` (DC-18, trước đây Teacher); `*ImportService ..> ImportReport`; `*ImportService ..> MailPort` (chỉ `UserImportService`).
**Số class/enum sau thay đổi:** tính lại ở W1.12, **không** điền sẵn "31/10" cũ.

### 4.4. Use Case (đề xuất — Phụ lục E)
- **Sửa:** UCSV01 (bỏ SSO/MSSV; luồng `mustChangePassword`), UCSV02 (chọn kỳ, điều kiện BR-10, hiện giờ còn lại), UCSV03 và UCSV07 (hạn theo `expires_at`), UCGV01 và UCADM01 (đăng nhập), UCGV07/UCGV08/UCADM05 (lọc theo kỳ).
- **Thêm:** UCADM08, UCADM15, UCADM16, UCADM17, UCSV08, UCSV09 (MD-12) **và UCADM09 Quản lý tài khoản (SV + GV, nâng/thu hồi Admin)** ⇒ **7 UC mới, tổng 24 + 7 = 31** (UCADM10 đã bỏ theo DC-19). *Tên/ID UCADM09–10 là đề xuất, duyệt ở W0.1.*
- **Actor trên UC Diagram:** giữ actor `Admin` (Q-9 đóng: không có actor GV-QTV/QTV hệ thống riêng).
- UCADM08/09 chỉ `ADMIN` gọi được (BR-16); `TEACHER` ⇒ `403`.
- **Quan hệ:** `UCADM16 <<extend>> UCADM15`, `UCADM17 <<extend>> UCADM15`; `UCSV08 <<extend>> UCSV01` (khi `mustChangePassword`), `UCSV09 <<extend>> UCSV01`. Ghi chú nghiệp vụ: Admin kế thừa UCADM15–17 (cùng cách UCADM04–06 đã ghi).
- UCADM02/03/07, UCGV10: giữ văn bản nhưng đánh dấu "Ngoài phạm vi Tiểu luận (#53)"; UCADM08 ghi rõ là UC hẹp thay cho luồng 3a của UCADM02.

### 4.5. API (đề xuất — Phụ lục B) và Backend
Module mới trong `src/modules/`: `user-import`, `exam-round`, `mail` (port + adapter + processor BullMQ) và **`user-admin`** (quản lý tài khoản SV và GV, nâng/thu hồi Admin, `RolesGuard`; *tên module chờ duyệt*). Sửa: `auth` (đổi/quên/đặt lại mật khẩu, `mustChangePassword`, argon2), `test-session` (BR-10, `expires_at`, `GET /sessions/active` trả thông tin kỳ), `reporting` (lọc `examRoundId`). Danh sách task BE mới `PI.*` ở Mục 8 (W5.1).

### 4.6. Frontend và màn hình
- **Màn mới:** S16 Đổi mật khẩu (`/change-password`), S17 Quên mật khẩu (`/forgot-password`), S18 Đặt lại mật khẩu (`/reset-password`), S19 Admin: Import tài khoản (`/admin/import-users`; bước tải lên, xem trước, kết quả), S20 GV: Danh sách kỳ thi (`/teacher/exam-rounds`), S21 GV: Tạo/sửa kỳ thi (`/teacher/exam-rounds/new`, `/[id]/edit`), S22 GV: Chi tiết kỳ thi và theo dõi dự thi (`/teacher/exam-rounds/[id]`), S23 GV: Import danh sách thi (`/teacher/exam-rounds/[id]/import`), **S24 Quản trị: quản lý tài khoản sinh viên và giảng viên** (`/admin/students`, `/admin/teachers`; xem/lọc, sửa, khóa/mở khóa, gửi lại mật khẩu tạm, nâng/thu hồi Admin). **S25 đã bỏ (DC-19).** S08–S11 và S19–S24 chỉ hiện khi `role=ADMIN`.
- **Màn sửa:** S01 (nhãn "Email", chuyển hướng khi `mustChangePassword`, link "Quên mật khẩu"), S02 (thẻ "Kỳ thi của tôi"), S03 (chọn kỳ, hiện giờ còn lại), S04 (đồng hồ theo `expiresAt`), S12 (bộ lọc kỳ).
- Danh sách task FE mới `FI.*` ở Mục 8 (W5.2). Mock MSW phải thêm handler cho API mới (#82).

### 4.7. Sequence Diagram (Mục 6.2)
Cập nhật `SD_01` (đăng nhập + đổi mật khẩu lần đầu, bỏ SSO), `SD_02` (bắt đầu phiên có kiểm kỳ và `expires_at`), `SD_05` (báo cáo lọc theo kỳ). Mới: `SD_06_ImportTaiKhoanSinhVien`, `SD_07_ImportDanhSachThi`, `SD_08_QuenVaDatLaiMatKhau`.

---

## 5. Việc 2 — Hai sơ đồ bổ sung (Component + Deployment)

**Định dạng (đề xuất, chưa hỏi bạn):** một file draw.io `Tuan5/SO_DO_THANH_PHAN_VA_TRIEN_KHAI.drawio.xml` gồm **2 trang** (cùng họ `mxfile` với `TLCN.drawio.xml`; Agent viết mxGraph XML được và verify well-formed). EA XMI cho component/deployment **chưa có file mẫu** nên rủi ro cao hơn. Nếu bạn muốn EA, hãy cung cấp một file mẫu như đã làm với `Bai10.xml`. *(Ghi vào câu hỏi mở Q-3.)*

### 5.1. Trang 1 — Component Diagram (nội dung phải có)
- **Clients/Edge:** Trình duyệt; Nginx (API Gateway).
- **Frontend (Next.js):** UI theo role; **BFF route handlers** giữ token trong cookie `httpOnly` (#50); lớp truy cập API (kiểu sinh từ OpenAPI, #51); mock MSW chỉ ở môi trường dev/test (#82, ghi rõ "không triển khai").
- **Backend (NestJS, Clean Architecture):** các module `auth`, `item-bank`, `cat-engine`, `test-session`, `language-profile`, `ai-explainer`, `reporting`, `health` **(đã có trong mã)** và `user-import`, `exam-round`, `mail` **(kế hoạch, vẽ nét đứt)**. Với mỗi module vẽ ranh giới `presentation / application / domain / infrastructure` ở mức gộp, không vẽ từng class.
- **Giao diện (port/provided/required):** `ItemRepository`, `SessionRepository`, `MailPort`, cổng AI, `ProfileAccessGuard`, API Key guard cho EduZ.
- **Lưu trữ/hạ tầng:** PostgreSQL (nguồn sự thật); Redis (state machine phiên, staging import, token đặt lại mật khẩu, hàng đợi BullMQ); hàng đợi BullMQ + worker gửi email.
- **Hệ thống ngoài:** Gemini API (ngoài đường thi, #60/#63); máy chủ SMTP; EduZ System (M2M `GET placement-profiles` bằng API Key).
- **Quy ước:** nét liền = đã có trong mã; nét đứt = kế hoạch. **Mỗi thành phần vẽ phải truy được về thư mục/tệp thật hoặc dòng trong kế hoạch** (Rubric: khớp 100% khi hội đồng đối chiếu).

### 5.2. Trang 2 — Deployment Diagram (nội dung phải có)
- **Nút Developer/CI:** GitHub Actions (lint, typecheck, test, build, gitleaks + `npm audit` + dependency-review, `jscpd`; SonarCloud tùy chọn, #80/#81) ⇒ đẩy image lên **GHCR**.
- **Nút Staging (máy chủ 2 GB dùng chung):** Docker Compose gồm Nginx (cổng **8443**, TLS Let's Encrypt cấp thủ công bản ghi TXT, #71/#74), frontend, backend, PostgreSQL, Redis, log shipper (`vector`); cách deploy `docker compose pull` qua SSH (#65). **Không ghi địa chỉ IP/secret** vào sơ đồ (`STAGING_HOST` ở GitHub Secret). Mailpit chỉ ở máy dev.
- **Dịch vụ ngoài:** Gemini API, SMTP provider (chưa chọn nhà cung cấp, ghi "SMTP"), Better Stack (monitor + log, #79).
- **Ghi chú trong sơ đồ:** không sao lưu DB staging (#70); dùng chung server với dự án khác nên **không** đụng Nginx host (#71).
- **Phải đọc để vẽ đúng:** `backend/backend/deploy/docker-compose.yml`, `deploy/nginx/`, `deploy/vector/`, `.github/workflows/*`, `Tuan4/KE_HOACH_CI_CD_VA_TRIEN_KHAI.md`, `Tuan4/TRACKING_CI_CD_VA_TRIEN_KHAI.md`. Phần nào chưa triển khai thì nét đứt.

### 5.3. Đối chiếu với AI bên Phương (task W2.1, W2.5)
Phương dán **Phụ lục D** cho AI riêng, gửi lại kết quả. Agent lập bảng so sánh trong mục "Đối chiếu AI của Phương" của tracking: loại sơ đồ AI gợi ý, lý do, loại bỏ/giữ. Nếu AI của Phương gợi ý loại khác (ví dụ ERD, Context) thì **ghi nhận và hỏi bạn** có thêm không (sẽ có dư địa vượt ngưỡng 4 loại), **không tự thêm**. Kết quả ghi `DECISIONS_LOG` (#93 trở đi, số cuối theo thực tế).

### 5.4. Tiêu chí chấp nhận của hai sơ đồ
1. Mọi thành phần "nét liền" truy được tới thư mục/tệp thật (ghi bảng truy vết trong tracking, ≥10 điểm kiểm ngẫu nhiên).
2. Có chú giải ký hiệu; tên định danh tiếng Anh; chú thích tiếng Việt.
3. Mô tả bằng lời (3–6 câu/sơ đồ) và bảng "thành phần – trách nhiệm" đã nằm trong SRS v3.0.
4. 👤 đã mở bằng diagrams.net, hiển thị đúng, đã xuất PNG.

---

## 6. Việc 3 — Hoàn thiện Use Case và Sequence

### 6.1. Mẫu Acceptance Criteria + Business Rules cho mỗi UC
Thêm hai hàng vào bảng đặc tả của mỗi UC (giữ nguyên các hàng hiện có):
- **Quy tắc nghiệp vụ liên quan:** liệt kê `BR-xx` (Mục 3.4) hoặc quy tắc đã có trong SRS.
- **Tiêu chí chấp nhận:** 3–6 mệnh đề `Given / When / Then`, **ít nhất** 1 luồng chính, 1 ngoại lệ, 1 biên (ví dụ: vào lúc còn 30 phút, 0 dòng lỗi, hết TTL). Mỗi mệnh đề phải kiểm chứng được bằng test (liên kết sang TC2.5).

### 6.2. Danh sách Sequence Diagram
| Mã | Luồng | Trạng thái | Ghi chú |
|---|---|---|---|
| SD_01 | Đăng nhập | **Cập nhật** | Email + mật khẩu; nhánh `mustChangePassword`; bỏ SSO; lỗi 401 |
| SD_02 | Làm bài thi thích ứng | **Cập nhật** | Thêm bước chọn kỳ, kiểm BR-10, tính `expires_at`; hết hạn theo K5 |
| SD_03, SD_04 | Duyệt câu hỏi; kết quả + giải thích AI | **Rà** | Cập nhật tên theo Class Diagram mới (`Explanation` gắn `Item`, #60) |
| SD_05 | Báo cáo lớp | **Cập nhật** | Tham số `examRoundId` |
| SD_06 | Import tài khoản sinh viên | **Mới** | preview ⇒ Redis ⇒ confirm ⇒ transaction ⇒ BullMQ ⇒ SMTP |
| SD_07 | Import danh sách thi | **Mới** | preview, all-or-nothing, confirm; MSSV tra DB |
| SD_08 | Quên và đặt lại mật khẩu | **Mới** | Theo D-FP |
| (nền) SD_09 Tiếp tục bài thi, SD_10 Xuất CSV | 🟡 **Không bắt buộc** | Backlog Tuần 6–7 nếu còn thời gian |

### 6.3. Lịch hoàn thiện
- **Tuần 5:** AC + BR cho UC mới/đổi (17 UC: UCSV01/02/03/07/08/09, UCGV01/07/08/11/12/13, UCADM01/05/08/09/10) + SD_01/02/05/06/07/08.
- **Tuần 6:** AC + BR cho UC còn lại trong phạm vi TL (UCSV04–06, UCGV02–06, UCGV09, UCADM04, UCADM06); rà SD_03/04. *(UCADM09–10 đã nằm trong danh sách Tuần 5.)*
- **Tuần 7:** bắt đầu code; sơ đồ được đối chiếu lại với mã (backlog BK1).

---

## 7. Việc 4 — `DANH_SACH_MAN_HINH_THEO_ROLE.md` (dàn ý bắt buộc)
1. **Tổng quan:** 3 role (Student, Teacher, Admin = siêu tập Teacher) + actor ngoài EduZ (không có giao diện); sơ đồ quyền ngắn.
2. **Bản đồ luồng theo role:** một sơ đồ luồng văn bản/Mermaid cho từng role (vào ⇒ màn ⇒ màn ⇒ ra), có điều kiện rẽ nhánh (đổi mật khẩu lần đầu, chưa thuộc kỳ, kỳ chưa mở, đang có phiên dở).
3. **Bảng màn hình từng role:** `ID | Tên | Đường dẫn | Mục đích | Chức năng chính | Trạng thái giao diện (rỗng/đang tải/lỗi/thành công) | UC | API | Ghi chú`. Gồm cả S01–S15 hiện có (từ Tuan4, có đối chiếu mã `frontend/src/app`) và S16–S25 mới.
4. **Màn dùng chung:** đăng nhập, đổi/quên/đặt lại mật khẩu, lỗi (S15).
5. **Ma trận UC ↔ màn hình ↔ API ↔ role** (cơ sở truy vết và test E2E).
6. **Ghi chú trạng thái:** màn nào "đã có trong mã", "mock", "kế hoạch" (đối chiếu `Tuan4/TRACKING_TRIEN_KHAI_FRONTEND.md`).
7. **Điểm cần xác nhận** (nếu có, `TODO-CONFIRM` như Tuan4).
Phải khớp ID với 3 file mô tả giao diện ở Tuan4 (task W4.3).

---

## 8. Danh sách task chi tiết

Ký hiệu: 🤖 Agent · 👤 Người · ⛔ cổng chặn · `∥` song song được · Kích cỡ S/M/L là định tính.

### Phase W0 — Cổng vào và khóa đặc tả
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W0.1 | 👤⛔ | Duyệt kế hoạch, gồm 15 đề xuất mặc định Mục 3.3 và DC-15…DC-17 (gạch/sửa dòng nào không đồng ý), danh mục file Mục 9, tên class/UC/màn hình | — | Điền "Đã duyệt" + ngày ở đầu tracking; Agent chép các sửa đổi vào Mục 3.3 |
| W0.2 | 👤⛔ | Chọn D-T (T1/T2/T3) | W0.1 | `AskUserQuestion` hoặc điền tracking; ghi #93 |
| W0.3 | 👤⛔ | Chọn D-FP (A/B/C) | W0.1 | Ghi #94 |
| W0.4 | 👤 | (Khuyến nghị, không chặn) Hỏi GVHD: đảo #59, bỏ SSO, thêm quy tắc K5/kỳ thi; ghi câu trả lời | W0.1 | Ghi vào weekly-log Tuan-05 (Tuan-04 đã ghi cần hỏi GVHD về #59/#60) |
| W0.5 | 🤖 | Kiểm trạng thái nguồn: `ls`/`cmp` các file ở Mục 9 tồn tại; xác nhận chưa có git; ghi bản nào là bản làm việc | W0.1 | Bảng "Kiểm trạng thái" trong tracking |
| W0.6 ∥ | 🤖 | Backup mọi file sẽ sửa (Mục 9.2) vào `Tuan5/_BACKUP_20261012_*` | W0.1 | `ls` đủ N backup, kích thước trùng bản gốc (`cmp`) |
| W0.7 | 🤖 | Tạo `0.docs/tracking/feature-plans/import-va-ky-thi.md` (từ `_template.md`) và `weekly-log/Tuan-05.md` (từ `_template.md`); ghi các `DECISIONS_LOG` còn thiếu (D-T, D-FP, MD đã duyệt) | W0.2, W0.3 | Hai file tồn tại; bảng quyết định có dòng mới |
| W0.8 | 🤖 | Soạn **bản nháp** cập nhật `COMMITMENT_BASELINE.md` (khối lượng mới: import, kỳ thi, 2 sơ đồ, AC); **không ký** | W0.1 | Diff đề xuất trong tracking; ký ở W6.5 |

### Phase W1 — Việc 1: đồng bộ đặc tả (chạy sau khi W0.1–W0.3 ✅)
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W1.1 | 🤖 | Tổng hợp **mọi "đề xuất SRS v2.7" tồn đọng** từ `DECISIONS_LOG`, `weekly-log/Tuan-01..04`, `Tuan3/`, `Tuan4/` thành bảng (nội dung, nguồn, mục SRS bị ảnh hưởng) trong tracking | W0.7 | Bảng ≥ các mục: #24, #53, #56, #60, #63, #64, K5, Explanation theo Item; mỗi dòng có nguồn |
| W1.2 | 🤖 | Tạo `Tuan5/SRS_TLCN_v3.0.docx` từ bản sao v2.6 Final; sửa tiêu đề, phiên bản, ngày; thêm hàng v3.0 vào XVII | W0.6, W1.1 | Mở lại bằng script: số heading/bảng ≥ bản gốc; v2.6 Final không đổi (`cmp` với backup) |
| W1.3 | 🤖 | SRS: sửa Mục I.3, III (module breakdown + sơ đồ ASCII), IX (F-01 sửa; thêm F-18 Import tài khoản, F-19 Quản lý kỳ thi, F-20 Import danh sách thi, F-21 Đổi/Quên mật khẩu), X (API), XII (lộ trình) | W1.2 | Đối chiếu Phụ lục B; mọi ID khớp Mục 3–4 |
| W1.4 | 🤖 | SRS: sửa IV.5 (timeout theo D-T), VI/VIII (DDL), XIV (Risk R12–R15: email, Redis staging, lộ danh sách, phụ thuộc server), XV (15.3 băm mật khẩu, rate limit; 15.4 RBAC cho endpoint mới) | W1.2, W0.2 | NFR định lượng mới: ≥1 chỉ số mới (ví dụ thời gian xử lý `preview` ≤ N giây cho 500 dòng — **N chưa đo, ghi "mục tiêu thiết kế, chưa đo"**) |
| W1.5 | 🤖 | SRS: thêm mục mới "Nghiệp vụ Import & Kỳ thi" (BR-01…, luồng L1–L5, máy trạng thái, mã lỗi); chốt BR-06/BR-08 | W1.3, W1.4 | Mọi BR trong Mục 3.4 có chỗ trong SRS; câu hỏi Q-1/Q-2 đã chốt hoặc ghi "mở" |
| W1.6 | 🤖 | SRS: hấp thụ phần còn lại của bảng W1.1; thêm "Phụ lục: Bảng thay đổi v2.6 → v3.0" | W1.5 | Mỗi dòng bảng W1.1 → 1 vị trí SRS; không còn chữ "EduZ SSO" trong phạm vi TL (grep) |
| W1.7 ∥ | 🤖 | UC spec: sửa UCSV01/02/03/07, UCGV01/07/08, UCADM01 | W0.6, W0.2 | Không còn "EduZ SSO"/"MSSV" ở UCSV01 (grep); nhắc `BR-xx` |
| W1.8 | 🤖 | UC spec: thêm UCADM08–10, UCADM15–17, UCSV08–09 đủ mẫu hiện có; cập nhật 2.3, 2.5; đánh dấu UC ngoài phạm vi | W1.7 | Tổng UC = 24 + 8 (mục 2.3 khớp số bảng đặc tả); ID không trùng |
| W1.9 ∥ | 🤖 | UC Diagram `AdaptivePlacementTest.xml`: thêm UC mới + `extend`; backup trước | W1.8 | `minidom` parse OK; mọi `UML:UseCase` mới có ít nhất 1 liên kết actor hoặc extend; encoding `windows-1252` giữ nguyên |
| W1.10 ∥ | 🤖 | Class Diagram `TLCN.drawio.xml` trang `Trang-1`: Mục 4.3 + sửa F1–F9 (F5 đối chiếu từng cột với `schema.prisma` rồi **hỏi** nếu có cột chưa rõ) | W0.2, W0.3, MD-11 duyệt | XML well-formed; mọi `source/target` trỏ id tồn tại; 👤 xem lại W1.20 |
| W1.11 | 🤖 | `ClassDiagram.puml` và `.mmd` đồng bộ với drawio | W1.10 | Hai file cùng danh sách class/enum/quan hệ (script đếm); `.puml` không lỗi cú pháp (đọc kỹ, không có công cụ render thì ghi rõ "chưa render") |
| W1.12 | 🤖 | `Mo_ta_So_do_Lop_ClassDiagram.md`: mô tả lớp mới, bảng quan hệ, tính lại số class/enum, xóa ⚠️ đã giải quyết | W1.10 | Số class/enum khớp drawio; mọi class trong drawio có mục mô tả |
| W1.13 ∥ | 🤖 | `schema.prisma` + SQL tùy chỉnh + `seed.ts` (Phụ lục A) | W0.2, W0.3 | `npx prisma validate` OK; `migrate diff … --script` sinh SQL, kiểm các index/CHECK/FK có mặt; seed không còn mật khẩu thô; **không chạy migrate** |
| W1.14 ∥ | 🤖 | Cập nhật SD_01, SD_02, SD_05 (backup trước) | W1.8, W0.2 | `minidom` + script đối chiếu `sender/receiver/DiagramElement` |
| W1.15 | 🤖 | Tạo SD_06, SD_07, SD_08 | W1.14 (dùng lại khuôn) | Như W1.14; tên participant tiếng Anh, khớp tên class W1.10 |
| W1.16 ∥ | 🤖 | Cập nhật 3 file mô tả giao diện Tuan4 + ghi chú đầu file phân tích import | W1.8 | ID S16–S25 và sửa S01–S04, S12 nhất quán với Mục 4.6 |
| W1.17 | 🤖 | Cập nhật `Tuan4/KE_HOACH_RA_SOAT_VA_HOAN_THIEN_BACKEND.md` + `TRACKING_...` (phase PI) và `KE_HOACH_TRIEN_KHAI_FRONTEND.md` + `TRACKING_...` (phase FI) theo danh sách W5.1/W5.2; **chỉ thêm, không xóa** task cũ; ghi PX/Pn liên quan | W1.13 | Số task mới khớp; tổng quan hai tracking đã cộng đúng |
| W1.18 | 🤖👤 | Soạn diff đề xuất cho `CLAUDE.md` (gốc + `0.docs/`): số class/enum, dòng Auth/SSO, trạng thái code, đường dẫn SRS; **không áp dụng trước khi bạn duyệt** | W1.12 | Diff trong tracking; 👤 duyệt; Agent áp dụng |
| W1.19 | 🤖 | Ghi `DECISIONS_LOG`, `AI_USAGE_LOG`, `weekly-log/Tuan-05` cho từng nhóm task xong (liên tục) | mỗi task | Dòng log khớp tracking |
| W1.20 | 👤 | Mở `TLCN.drawio.xml` bằng diagrams.net, xem Class Diagram; mở SRS v3.0/UC bằng Word; mở UC/SD `.xml` bằng EA; báo lỗi hiển thị | W1.8–W1.15 | Ghi kết quả vào tracking; lỗi trình bày không chặn nội dung |

### Phase W2 — Việc 2: Component + Deployment (sau khi W1.10 ✅ tối thiểu)
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W2.1 ∥ | 👤 | Phương dán Phụ lục D cho AI riêng, gửi kết quả vào mục "Đối chiếu AI của Phương" | W0.1 | Có nội dung dán vào tracking |
| W2.2 ∥ | 🤖 | Thu thập "sự thật" từ mã/hạ tầng thật (module, import giữa module, compose, workflow) thành bảng truy vết | W0.5 | Bảng ≥ 20 dòng "thành phần → đường dẫn" |
| W2.3 | 🤖 | Dựng trang Component (Mục 5.1) | W2.2, W1.10 | XML well-formed; tham chiếu hợp lệ; chú giải đủ |
| W2.4 | 🤖 | Dựng trang Deployment (Mục 5.2) | W2.2 | Như trên; không có IP/secret (grep) |
| W2.5 | 🤖 | So sánh với đề xuất AI của Phương; nếu khác ⇒ `AskUserQuestion` | W2.1, W2.3 | Bảng so sánh + `DECISIONS_LOG` |
| W2.6 | 🤖 | Kiểm tra khớp mã: ≥10 điểm ngẫu nhiên trong sơ đồ ⇒ truy ra mã thật; ghi tỉ lệ khớp thật | W2.3, W2.4 | Bảng ngẫu nhiên có seed ghi rõ; điểm không khớp được sửa sơ đồ hoặc ghi "kế hoạch" |
| W2.7 | 🤖 | Viết mô tả và bảng thành phần trong SRS v3.0 (mục "Sơ đồ thành phần/triển khai") | W2.6, W1.6 | Mục có trong `.docx`, đủ tiêu chí 5.4.3 |
| W2.8 | 👤 | Mở bằng diagrams.net, xuất PNG | W2.3, W2.4 | Ghi kết quả |

### Phase W3 — Việc 3: hoàn thiện UC và Sequence
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W3.1 | 🤖 | AC + BR cho 17 UC mới/đổi (Mục 6.3 Tuần 5) | W1.8 | Mỗi UC ≥3 mệnh đề G/W/T gồm luồng chính + ngoại lệ + biên; đếm tự động bằng script |
| W3.2 | 🤖 | AC + BR cho UC còn lại trong phạm vi TL (Tuần 6) | W3.1 | Tỉ lệ UC có AC = 100% trong phạm vi TL (đếm thật, ghi `TRACKING.md`) |
| W3.3 | 🤖 | Đánh dấu UCADM02/03/07, UCGV10 "Ngoài phạm vi TL (#53)" | W1.8 | grep đúng 4 UC |
| W3.4 | 🤖 | Rà SD_03/SD_04 theo Class Diagram mới | W1.12 | Danh sách chỉnh; cập nhật nếu lệch |
| W3.5 | 🟡 | (Không bắt buộc) SD_09, SD_10 | W3.4 | — |
| W3.6 | 👤 | Mở EA kiểm tra XML mới (SD_06–08, UC) | W1.15 | Ghi kết quả (tương đương G6 của Tuan2) |

### Phase W4 — Việc 4: danh sách màn hình
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W4.1 | 🤖 | Khảo sát `frontend/src/app` và `Tuan4/TRACKING_TRIEN_KHAI_FRONTEND.md` để biết màn nào "có trong mã/mock/kế hoạch" | W0.5 | Bảng màn ↔ route thật |
| W4.2 | 🤖 | Soạn `Tuan5/DANH_SACH_MAN_HINH_THEO_ROLE.md` theo Mục 7 | W1.16, W4.1 | Đủ 7 mục; mỗi màn có UC + API |
| W4.3 | 🤖 | Đối chiếu ID/route với 3 file Tuan4 | W4.2 | Không lệch ID (script so) |
| W4.4 | 👤 | Review (đặc biệt `TODO-CONFIRM`) | W4.3 | Ghi kết quả |

### Phase W5 — Chuẩn bị mã nguồn (chỉ lên kế hoạch; **mã bắt đầu từ Tuần 7**)
**W5.1 — Task BE sẽ thêm thành phase `PI` vào kế hoạch/tracking BE (W1.17):**
| Mã | Việc | Ghi chú |
|---|---|---|
| PI.0 | 🔴 Sửa `login.use-case.ts` dùng `argon2.verify`; băm seed | Đã có ở P5; **phải xong trước PI.1–PI.12** |
| PI.1 | Migration: `ExamRoundStatus`, cột `User`, bảng `exam_rounds`/`participants`, `TestSession.examRoundId/expiresAt`, SQL tùy chỉnh | Từ W1.13; migration chỉ thêm (expand/contract, #68) |
| PI.2 | Module `mail`: `MailPort`, `SmtpMailAdapter` (nodemailer), BullMQ processor + retry; Mailpit cho dev | #86 |
| PI.3 | Module `user-import`: đọc xlsx, validate, preview/confirm (Redis), tạo tài khoản trong transaction | DC-04/05 |
| PI.4 | Guard `mustChangePassword`; `POST /auth/change-password` | BR-06 |
| PI.5 | Quên/đặt lại mật khẩu theo D-FP | DC-11 |
| PI.6 | Module `exam-round`: CRUD, publish/close, `effectiveStatus`, lazy cập nhật cột | DC-10 |
| PI.7 | Import danh sách thi theo lưới tạm (upload/grid/save, loại dòng lỗi, popup) | DC-22 |
| PI.8 | `POST /sessions` kiểm BR-10, tính `expires_at`; `GET /sessions/active` trả kỳ | D-T |
| PI.9 | Mã hóa/xóa payload mật khẩu tạm sau gửi; cấm log mật khẩu | MD-10 |
| PI.10 | Báo cáo lọc `examRoundId` (UCGV07/08) | BR-13 |
| PI.11 | Test: đủ ca ở Mục 11 (bảng test bắt buộc) | TC2.5 |
| PI.12 | Seed + Swagger cập nhật; sinh lại kiểu OpenAPI cho FE (#51); seed thêm 1 Admin (tài khoản đầu tiên, DC-19), 1 GV thường (dữ liệu giả) | — |
| PI.13 | `RolesGuard` dùng chung theo `role`; chặn `TEACHER` ở `/items` ghi, `/exam-rounds`, `/users`, `/students`, `/teachers` | DC-19, MD-15 (mới), BR-16. **Làm trước PI.3/PI.6** |
| PI.14 | Module `user-admin`: `GET/PATCH /students` và `/teachers`, khóa/mở khóa, gửi lại mật khẩu tạm | DC-19, BR-19; phụ thuộc Q-8 |
| PI.15 | `PATCH /users/:id/role` (nâng/thu hồi Admin; chặn thu hồi Admin cuối) + hiệu lực quyền với token cũ; kiểm toán | DC-19, BR-17/18 |

**W5.2 — Task FE sẽ thêm thành phase `FI` vào kế hoạch/tracking FE (W1.17):**
| Mã | Việc |
|---|---|
| FI.1 | Hợp đồng API + handler MSW cho endpoint mới |
| FI.2 | S01 sửa (nhãn Email, `mustChangePassword`, link quên mật khẩu), S16 Đổi mật khẩu, middleware chặn khi chưa đổi |
| FI.3 | S17/S18 Quên và đặt lại mật khẩu |
| FI.4 | S19 Admin: Import tài khoản (tải lên → xem trước → xác nhận → kết quả) |
| FI.5 | S20–S22 GV: danh sách, tạo/sửa, chi tiết và theo dõi dự thi |
| FI.6 | S23 GV: Import danh sách thi |
| FI.7 | S02/S03/S04: kỳ của tôi, chọn kỳ, đồng hồ theo `expiresAt` |
| FI.8 | S12: bộ lọc kỳ |
| FI.9 | File mẫu `.xlsx` (dữ liệu giả) trong `public/templates/` |
| FI.10 | Test: Vitest + Playwright cho luồng chính mỗi màn mới |
| FI.11 | S24 Admin: quản lý tài khoản SV và GV, nâng/thu hồi Admin; menu theo `role` (S25 đã bỏ) |

### Phase W6 — Khép sổ
| Mã | Loại | Việc | Phụ thuộc | Xác minh / Đầu ra |
|---|---|---|---|---|
| W6.1 | 🤖 | **Quét nhất quán** toàn bộ tài liệu (Phụ lục F): từ khóa lỗi thời, số liệu, ID | W1.*, W2.*, W3.1, W4.* | Báo cáo quét trong tracking; mọi hit được sửa hoặc giải thích |
| W6.2 | 🤖 | Đồng bộ bản cuối sang `docs-repo/` (copy; không push), ghi các file đã chép | W6.1 | `cmp` bản nguồn = bản chép |
| W6.3 | 🤖 | Cập nhật `TRACKING.md` (số loại sơ đồ, tỉ lệ UC có AC) bằng **số đếm thật**; không điền KPI chưa đo | W3.2, W2.6 | Số khớp kiểm đếm |
| W6.4 | 🤖 | Tổng kết `weekly-log/Tuan-05.md` gồm mục "Nợ đồng bộ tài liệu" nếu còn | W6.1 | Mọi tài liệu hoãn được liệt kê |
| W6.5 | 👤⛔ | **Ký `COMMITMENT_BASELINE.md`** (hạn cuối Tuần 6) | W0.8, W6.4 | Có chữ ký SV + GVHD |
| W6.6 | 🤖 | `AI_USAGE_LOG.md` bản cuối: mỗi nhóm file một dòng, ghi "cần thành viên tự kiểm chứng" | W6.1 | Dòng khớp tracking |

### Backlog (chưa lên lịch)
- **BK1:** Sau khi code (Tuần 7+), đối chiếu lại Component/Deployment/Class/Sequence với mã thật (Rubric: khớp 100%).
- **BK2:** Sơ đồ Context hoặc ERD (chỉ khi bạn quyết định tạo dư địa vượt ngưỡng 4 loại).
- **BK3:** SD_09, SD_10.

---

## 9. Danh mục file

### 9.1. File **tạo mới** (chỉ những file này, không sáng tạo thêm)
| File | Tạo bởi |
|---|---|
| `Tuan5/KE_HOACH_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` (file này) | lượt lập kế hoạch |
| `Tuan5/TRACKING_NGHIEP_VU_IMPORT_VA_BO_SUNG_THIET_KE.md` | lượt lập kế hoạch |
| `Tuan5/SRS_TLCN_v3.0.docx` | W1.2 |
| `Tuan5/SD_06_ImportTaiKhoanSinhVien.xml`, `SD_07_ImportDanhSachThi.xml`, `SD_08_QuenVaDatLaiMatKhau.xml` | W1.15 |
| `Tuan5/SO_DO_THANH_PHAN_VA_TRIEN_KHAI.drawio.xml` | W2.3–W2.4 |
| `Tuan5/DANH_SACH_MAN_HINH_THEO_ROLE.md` | W4.2 |
| `Tuan5/_BACKUP_20261012_*` | W0.6 |
| `0.docs/tracking/feature-plans/import-va-ky-thi.md`, `0.docs/tracking/weekly-log/Tuan-05.md` | W0.7 (yêu cầu của `CLAUDE.md` quy tắc 3, 5 và template tuần) |

### 9.2. File **sửa** (đều có backup trước)
`20260922_MoHinhHoaYeuCau.docx`, `AdaptivePlacementTest.xml`, `TLCN.drawio.xml`, `ClassDiagram.puml`, `ClassDiagram.mmd`, `0.docs/Mo_ta_So_do_Lop_ClassDiagram.md`, `Tuan2/SD_01_DangNhapHeThong.xml`, `SD_02_LamBaiThiThichUng.xml`, `SD_05_XemBaoCaoLopHoc.xml` (+ SD_03/04 nếu W3.4 cần), `backend/backend/prisma/schema.prisma`, `custom_migrations.sql`, `seed.ts`, 3 file mô tả giao diện Tuan4 + file phân tích import, 2 kế hoạch + 2 tracking của BE/FE, `0.docs/tracking/{DECISIONS_LOG,AI_USAGE_LOG,TRACKING,COMMITMENT_BASELINE}.md`, `CLAUDE.md` (sau khi duyệt W1.18).
*Ghi chú:* `ClassDiagram.puml/.mmd` đã lệch lâu so với drawio (xem `Mo_ta` cuối file: "chưa được cập nhật"); W1.11 sửa cả hai.

---

## 10. Phụ thuộc và song song

```
W0.1 ──► W0.2 ┐
   │          ├─► W0.7 ─► W1.1 ─► W1.2 ─► W1.3 ─► W1.4 ─► W1.5 ─► W1.6 ──────────────┐
   ├─► W0.3 ──┘                     │                                                │
   ├─► W0.5, W0.6 ∥                 └──────────────► W2.7 ◄── W2.6 ◄── W2.3, W2.4  │
   └─► W0.4, W0.8                                                                    │
W0.2/W0.3 ──► W1.7 ─► W1.8 ─► W1.9 ∥ W1.14 ─► W1.15                                 │
          └─► W1.10 ─► W1.11, W1.12 ;  W1.13 ∥ ;  W1.16 ∥ ─► W4.2 ─► W4.3 ─► W4.4   │
W1.8 ─► W3.1 ─► W3.2 ;  W1.13 ─► W1.17 ;  W1.12 ─► W1.18                             │
W2.1 ∥ W2.2 ─► W2.3 ∥ W2.4 ─► W2.5 ─► W2.6                                          ▼
                                                              W6.1 ─► W6.2, W6.3, W6.4 ─► W6.5 ⛔ ─► W6.6
```
**Có thể chạy song song (hai Agent hoặc hai luồng) sau khi W0.1–W0.3 ✅:** nhóm A (SRS: W1.2–W1.6), nhóm B (UC: W1.7–W1.9), nhóm C (Class + Prisma: W1.10–W1.13), nhóm D (Sequence: W1.14–W1.15), nhóm E (UI: W1.16, W4.*), nhóm F (sơ đồ mới: W2.*). **Điểm hội tụ cần chờ:** W2.7 (cần SRS đã có khung), W6.1.
**Thứ tự ưu tiên nếu thiếu thời gian (Tuần 5):** W0 ⇒ W1.1–W1.8 và W1.10 ⇒ W1.13 ⇒ W2.2–W2.4 ⇒ W1.14–W1.15 ⇒ W4.2. Việc hoãn được: AC cho UC cũ (W3.2), SD_03/04 (W3.4), backlog.

---

## 11. Tác động tới Rubric, tiến độ và kiểm thử

| Tiêu chí | Tác động của kế hoạch này | Chú ý |
|---|---|---|
| **TC2.1** | +2 loại sơ đồ (component, deployment) ⇒ đủ 4 loại; AC cho 100% UC; thay đổi thiết kế có lý do (#84–#9x); đủ NFR định lượng (SRS đã có ≥5) | Ngưỡng 4 loại **không có dư địa**; "khớp 100% mã" chỉ kiểm được khi code xong (BK1) |
| **TC2.2** | Khối lượng tăng (import, kỳ thi, mật khẩu, email) | Phản ánh vào `COMMITMENT_BASELINE` trước khi ký (W0.8/W6.5) |
| **TC2.3** | Mọi sinh/sửa tài liệu có dòng `AI_USAGE_LOG` | Đặc biệt SRS và XMI do AI sinh: thành viên phải đọc lại và giải thích được |
| **TC2.5** | Danh sách ca test bắt buộc (dưới) | |
| **TC2.4** | Chưa `git init` cho `backend/`, `frontend/` | Không thuộc kế hoạch này nhưng là rủi ro đang mở (Tuan-04) |

**Ca test bắt buộc cho PI.11/FI.10:** đăng nhập sai mật khẩu bị từ chối (hồi quy lỗi 🔴); đăng nhập lần đầu bị ép đổi; chặn route khi chưa đổi; file sai định dạng/quá cỡ/quá dòng; email trùng (trong file, trong DB); MSSV trùng; preview hết TTL; confirm khi còn lỗi (danh sách thi); MSSV không tồn tại; SV chưa vào kỳ; kỳ chưa mở/đã đóng; vào lúc còn 30 phút (hạn đúng); đóng đúng `closes_at` (K5 cả hai nhánh ≥8 và <8); 2 request đồng thời bắt đầu phiên (409, race); thi lần 2 sau `COMPLETED` bị chặn, sau `ABANDONED` cho phép; **GV thường gọi import/quản lý TK, `/items` ghi, `/exam-rounds` ⇒ 403; Admin làm được tất cả; không thu hồi được Admin cuối; thu hồi quyền có hiệu lực với token cũ;** email thất bại sau retry không rollback tài khoản; mật khẩu tạm không xuất hiện trong log.

---

## 12. Rủi ro và câu hỏi còn mở

| ID | Rủi ro / câu hỏi | Mức | Xử lý |
|---|---|---|---|
| R-1 | Khối lượng tài liệu lớn trong 2 tuần; BE đang 0/87 task, FE sinh trước theo thiết kế không có kỳ thi | 🔴 | Thứ tự ưu tiên Mục 10; W1.17 gộp việc mới vào hai tracking; cân nhắc hoãn PI.* sau mốc G1 nếu BE trễ |
| R-2 | Đảo #59 chưa hỏi GVHD (Tuan-04 đã ghi cần hỏi) | 🟠 | W0.4 (không chặn nhưng ghi lại) |
| R-3 | SRS v3.0 sửa bằng script có thể làm hỏng định dạng `.docx` | 🟠 | Backup, sửa bản sao, 👤 mở bằng Word |
| R-4 | XMI `windows-1252` và khung `alt/opt` không có ground truth | 🟠 | Mục 1.7; tránh dấu và khung |
| R-5 | Hạn mức gửi email của nhà cung cấp SMTP **chưa kiểm chứng**; hàng trăm email/lần | 🟠 | Port/adapter đổi nhà cung cấp bằng env; chọn nhà cung cấp ở PI.2; hạn mức chỉ ghi sau khi kiểm |
| R-6 | Payload hàng đợi chứa mật khẩu tạm; log rò | 🟠 | MD-10, PI.9, ca test "không có trong log" |
| R-7 | Redis mất giữa preview và confirm | 🟡 | `410 IMPORT_BATCH_EXPIRED`, GV tải lại |
| R-8 | Dùng chung server staging 2 GB (Redis + queue + Mailpit) | 🟡 | Mailpit chỉ dev; theo dõi RAM khi có số đo |
| R-9 | Gỡ `institution_id` khỏi schema/seed/mã BE đã có (thay rủi ro composite FK cũ) | 🟡 | W1.13: `prisma validate` + `migrate diff` (DC-19) |
| R-10 | `COMMITMENT_BASELINE` chưa ký, G1 hết Tuần 6 | 🔴 | W0.8, W6.5 |
| **Q-1** | ✅ **ĐÃ CHỐT (DC-22, #98):** lưới tạm, dòng lỗi loại khỏi grid, bấm Lưu mới ghi DB; áp dụng cả hai loại import | — | — |
| **Q-2** | GV **đóng thủ công** kỳ giữa lúc có phiên đang chạy: cắt ngay hay để chạy tới `expires_at`? (đề xuất: để chạy) | — | Hỏi ở W0.1 |
| **Q-3** | Định dạng sơ đồ mới: draw.io (đề xuất) hay EA XMI (cần file mẫu)? | — | Hỏi ở W0.1 |
| **Q-4** | Ngưỡng độ dài mật khẩu và chính sách mật khẩu (đề xuất ≥8 ký tự; SRS chưa quy định) | — | Chốt ở W1.4 qua `AskUserQuestion` nếu SRS 15.3 không có |
| **Q-6** | GV-QTV (`role=ADMIN`) có giữ `teacher_profiles` (`teacherCode`) khi được nâng quyền không? Đề xuất: **giữ** dòng cũ, `Admin` không bắt buộc có hồ sơ (không thêm cột/dòng) | — | Hỏi ở W0.1 | ⛔ **ĐÓNG theo DC-19.**
| **Q-7** | Chặn thu hồi GV-QTV cuối cùng của một trường? (đề xuất cũ: không chặn) | — | Hỏi ở W0.1 | ⛔ **ĐÓNG theo DC-19** (BR-18 mới: chặn thu hồi Admin cuối).
| **Q-8** | ✅ **ĐÃ CHỐT (DC-23, #98):** `users.is_active BOOLEAN NOT NULL DEFAULT true` | — | — |
| **Q-9** | UC Diagram: GV-QTV là actor riêng (kế thừa `Teacher`) hay giữ actor `Admin` + ghi chú scope? | — | Hỏi ở W1.9 | ⛔ **ĐÓNG theo DC-19.**
| **Q-5** | Chọn nhà cung cấp SMTP cụ thể (Gmail App Password, Brevo, Resend… — **hạn mức chưa kiểm chứng**) | — | Hỏi ở PI.2 (Tuần 7), không chặn tài liệu |

---

## Phụ lục A — Prisma đề xuất (đã ghép D-T = T2; nếu chọn T1/T3 bỏ `durationMinutes`)

```prisma
enum ExamRoundStatus {
  DRAFT
  SCHEDULED
  OPEN
  CLOSED
}

model User {
  // …các field hiện có…
  mustChangePassword Boolean   @default(false) @map("must_change_password")
  passwordChangedAt  DateTime? @map("password_changed_at") @db.Timestamptz(6)

  createdExamRounds ExamRound[]            @relation("ExamRoundCreator")
  examParticipation ExamRoundParticipant[]
}

model ExamRound {
  id              String          @id @default(uuid()) @db.Uuid
  name            String          @db.VarChar(200)
  createdById     String          @map("created_by") @db.Uuid
  opensAt         DateTime        @map("opens_at") @db.Timestamptz(6)
  closesAt        DateTime        @map("closes_at") @db.Timestamptz(6)
  durationMinutes Int             @default(45) @map("duration_minutes")
  status          ExamRoundStatus @default(DRAFT)
  createdAt       DateTime        @default(now()) @map("created_at") @db.Timestamptz(6)
  updatedAt       DateTime        @updatedAt @map("updated_at") @db.Timestamptz(6)

  createdBy    User                   @relation("ExamRoundCreator", fields: [createdById], references: [id], onDelete: Restrict)
  participants ExamRoundParticipant[]
  sessions     TestSession[]

  @@index([status])
  @@map("exam_rounds")
}

model ExamRoundParticipant {
  roundId       String   @map("round_id") @db.Uuid
  studentId     String   @map("student_id") @db.Uuid
  note          String?  @db.VarChar(255)
  addedAt       DateTime @default(now()) @map("added_at") @db.Timestamptz(6)

  round   ExamRound @relation(fields: [roundId], references: [id], onDelete: Cascade)
  student User      @relation(fields: [studentId], references: [id], onDelete: Restrict)
  sessions TestSession[]

  @@id([roundId, studentId])
  @@index([studentId])
  @@map("exam_round_participants")
}

model TestSession {
  // …các field hiện có…
  examRoundId String   @map("exam_round_id") @db.Uuid
  expiresAt   DateTime @map("expires_at") @db.Timestamptz(6)

  participant ExamRoundParticipant @relation(fields: [examRoundId, studentId], references: [roundId, studentId], onDelete: Restrict)
  round       ExamRound            @relation(fields: [examRoundId], references: [id], onDelete: Restrict)

  @@index([examRoundId, status])
}
```
**SQL tùy chỉnh (`custom_migrations.sql`):**
```sql
ALTER TABLE exam_rounds ADD CONSTRAINT ck_exam_round_window CHECK (closes_at > opens_at);
ALTER TABLE exam_rounds ADD CONSTRAINT ck_exam_round_duration
  CHECK (duration_minutes BETWEEN 5 AND 180);  -- T2 (DC-20), NOT NULL DEFAULT 45 (DC-25)
CREATE UNIQUE INDEX uq_session_round_student ON test_sessions (exam_round_id, student_id)
  WHERE status <> 'ABANDONED';
-- (student_id) WHERE status = 'IN_PROGRESS' của #58: kiểm đã có chưa, chưa thì thêm.
```
*Lưu ý Agent:* đây là đề xuất, **chưa được Prisma validate**; nếu Prisma không chấp nhận hai quan hệ của `TestSession` hoặc composite FK, **dừng và hỏi**, không tự đơn giản hóa.

## Phụ lục B — API đề xuất

| Nhóm | Phương thức & đường dẫn | Role | Ghi chú |
|---|---|---|---|
| Auth | `POST /auth/login` (trả thêm `mustChangePassword`) | công khai | |
| | `POST /auth/change-password` `{currentPassword,newPassword}` | mọi role đã đăng nhập | cho phép khi `mustChangePassword` |
| | `POST /auth/forgot-password` `{email}` ⇒ 202 | công khai | rate limit |
| | `POST /auth/reset-password` `{email,otp,newPassword}` | công khai | |
| Import TK (lưới tạm, DC-22) | `POST /users/import/upload` (multipart `file`; gộp vào grid) | ADMIN | trả `{grid[],rejected[],added,ignoredDuplicates}` |
| | `GET /users/import/grid`; `DELETE /users/import/grid/:rowKey`; `DELETE /users/import/grid`; `POST /users/import/save` | ADMIN | `save` trả `{created,queued}` |
| QL tài khoản SV/GV | `GET /students`, `GET /teachers` (tìm theo MSSV/email, phân trang) | ADMIN | UCADM09 |
| | `PATCH /students/:id`, `PATCH /teachers/:id` `{fullName,email}`; `POST /students/:id/lock`, `…/unlock`, `…/resend-temporary-password` | ADMIN | BR-19; khóa cần Q-8 |
| Nâng/thu hồi Admin | `PATCH /users/:id/role` `{role}` | ADMIN | UCADM09, BR-17/18 (thay UCADM10) |
| Kỳ thi | `POST /exam-rounds`, `GET /exam-rounds`, `GET /exam-rounds/:id`, `PATCH /exam-rounds/:id` | ADMIN | |
| | `POST /exam-rounds/:id/publish`, `POST /exam-rounds/:id/close` | ADMIN | |
| | `POST /exam-rounds/:id/participants/import/upload`, `GET …/import/grid`, `DELETE …/import/grid[/:rowKey]`, `POST …/import/save` | ADMIN | lưới tạm (DC-22) |
| | `GET /exam-rounds/:id/participants` (kèm trạng thái dự thi) | ADMIN | UCADM17 |
| | `DELETE /exam-rounds/:id/participants/:studentId` | ADMIN | MD-07 |
| | `GET /exam-rounds/mine` | STUDENT | kỳ tôi thuộc + trạng thái hiệu lực |
| Phiên | `POST /sessions` `{examRoundId}`; `GET /sessions/active` trả `expiresAt`, kỳ | STUDENT | MD-05 |
| Báo cáo | `GET /reports/class-distribution?examRoundId=` và export CSV | TEACHER, ADMIN | |

## Phụ lục C — Cột Excel (đề xuất)
- **Import tài khoản (`.xlsx`):** dòng 1 tiêu đề; cột A `MSSV`, B `Họ tên`, C `Email`.
- **Import danh sách thi:** cột A `MSSV`, B `Ghi chú` (tùy chọn, ≤255 ký tự).
- Báo cáo từng dòng: `rowNumber`, `status` (`VALID`/`ERROR`/`SKIPPED`), `message` (ví dụ "MSSV không tồn tại trong hệ thống").
- Chuẩn hóa: cắt khoảng trắng, email về chữ thường; ô bắt đầu bằng `= + - @` khi **xuất** CSV phải được vô hiệu hóa (chống CSV injection; áp dụng cho `exportCSV` đã có).

## Phụ lục D — Prompt để Phương hỏi AI riêng (copy nguyên văn)

> Tôi làm đồ án "Adaptive Placement Test" (kiểm tra xếp lớp tiếng Anh thích ứng CAT–Rasch). Kiến trúc: Next.js (BFF giữ token trong cookie httpOnly) → Nginx → NestJS (Clean Architecture, module: auth, item-bank, cat-engine, test-session, language-profile, ai-explainer, reporting, và sắp thêm user-import, exam-round, mail) → PostgreSQL (nguồn sự thật), Redis (state machine phiên thi, lưu tạm import, hàng đợi BullMQ), dịch vụ ngoài: Gemini API, SMTP; hệ thống EduZ gọi API đọc hồ sơ bằng API Key. Triển khai bằng Docker Compose trên một máy chủ staging, CI/CD GitHub Actions đẩy image lên GHCR.
> Hiện đã có: Use Case, Class Diagram, 5 Sequence Diagram. Rubric của Khoa cho tiêu chí "Phân tích và thiết kế" yêu cầu ≥4 loại sơ đồ trong: context, component, ERD/class, sequence, deployment, và sơ đồ phải khớp mã nguồn.
> Hãy cho biết nên bổ sung **tối thiểu 2 loại sơ đồ nào** để đạt yêu cầu này, với mỗi loại: (1) lý do chọn, (2) các thành phần/ranh giới nên vẽ, (3) lỗi hay gặp khiến sơ đồ không khớp mã nguồn, (4) ký hiệu chuẩn nên dùng. Xếp hạng các loại còn lại theo giá trị/chi phí. Không bịa tên công nghệ ngoài danh sách trên.

## Phụ lục E — Use Case mới (khung, để W1.8 điền đủ mẫu hiện có)
| ID | Tên | Actor | Mô tả ngắn | AC mẫu (Given/When/Then) |
|---|---|---|---|---|
| UCADM08 | Import tài khoản sinh viên | Admin | Tải một hoặc nhiều file `.xlsx` vào lưới tạm, xem lưới, bấm Lưu để tạo tài khoản và gửi mật khẩu tạm qua email | Given file có dòng email trùng DB, When tải lên, Then dòng đó không vào grid và popup báo "tài khoản đã tồn tại". Given file thứ 2 có dòng đã có trong grid, When tải lên, Then chỉ thêm dòng chưa có. Given grid có dòng, When bấm Lưu, Then tài khoản được tạo với `mustChangePassword=true` và email chỉ xếp hàng sau lúc này. Given grid hết TTL, When Lưu, Then `IMPORT_GRID_EXPIRED`. |
| UCADM15 | Quản lý kỳ thi | Admin | Tạo, sửa, công bố, đóng kỳ thi | Given `opensAt ≥ closesAt`, When lưu, Then bị từ chối. Given kỳ `CLOSED`, When sửa, Then bị từ chối. |
| UCADM16 | Import danh sách sinh viên thi | Admin | Tải file `.xlsx` MSSV vào lưới tạm của một kỳ; bấm Lưu để ghi | Given MSSV không tồn tại, When tải lên, Then dòng bị loại và popup báo lỗi. Given MSSV đã có trong kỳ, When tải lên, Then dòng bị loại và popup "đã có trong kỳ". Given grid rỗng, When Lưu, Then bị từ chối. |
| UCADM17 | Theo dõi dự thi của kỳ | Admin | Xem từng SV: chưa thi, đang thi, hoàn thành, bỏ dở | Given kỳ có 3 SV, When mở chi tiết, Then thấy đủ 3 dòng kèm trạng thái đúng. |
| UCADM09 | Quản lý tài khoản (SV + GV) | Admin | Xem, sửa, khóa/mở khóa tài khoản SV và GV; gửi lại mật khẩu tạm; nâng GV lên Admin / thu hồi Admin | Given GV thường gọi API, When gửi, Then `403`. Given SV bị khóa, When đăng nhập, Then bị từ chối. Given thu hồi Admin cuối cùng, When gửi, Then bị từ chối (BR-18). Given gửi lại mật khẩu tạm, When thành công, Then mật khẩu cũ vô hiệu và `mustChangePassword=true`. |
| ~~UCADM10~~ | ~~Gán/thu hồi QTV đơn vị~~ | — | **Đã bỏ theo DC-19**; nâng/thu hồi Admin nằm trong UCADM09 | — |
| UCSV08 | Đổi mật khẩu | Sinh viên/GV/Admin | Đổi mật khẩu, bắt buộc ở lần đăng nhập đầu | Given `mustChangePassword=true`, When gọi API khác ngoài đổi mật khẩu, Then `403 PASSWORD_CHANGE_REQUIRED`. |
| UCSV09 | Quên mật khẩu | Sinh viên/GV/Admin | Nhận OTP 6 số qua email để đặt lại mật khẩu | Given email không tồn tại, When gửi yêu cầu, Then phản hồi y hệt email tồn tại. Given OTP sai 5 lần, When nhập lần tiếp, Then mã bị hủy (`INVALID_RESET_OTP`). Given OTP hết 10 phút, When đặt lại, Then `INVALID_RESET_OTP`. |

## Phụ lục F — Danh sách quét nhất quán (W6.1)
Tìm và xử lý mọi hit trong **phạm vi Tiểu luận** của: `EduZ SSO`, `Email hoặc MSSV`, `Google`, `Microsoft` (đăng nhập), `ExamRound` thiếu ở nơi cần, `exam_round`, `31 class`, `10 enum`, `ItemBank`, `EduZServiceAccount`, `WRITING` (trong `Skill`), `v2.7` (đổi thành v3.0 hoặc giải thích), `#59` (bổ sung "đảo một phần bởi #84"), `bcrypt` (đúng là argon2, #62), `CHƯA CÓ CODE`. Kiểm: số UC ở 2.3 = số bảng đặc tả; mọi class trong drawio có trong `.puml`, `.mmd`, `Mo_ta`; mọi màn S16–S25 có UC và API; ID API trong SRS = Phụ lục B (hoặc bản đã điều chỉnh).
