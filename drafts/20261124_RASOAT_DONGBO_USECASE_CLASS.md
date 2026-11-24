# Rà soát và đề xuất đồng bộ Use Case với Class Diagram sau ngày 03/11

- **Ngày rà soát:** 24/11/2026. **Trạng thái:** bản đối chiếu và đề xuất để nhóm review; không thay thế SRS, quyết định, đặc tả Use Case hoặc xác nhận triển khai.
- **Đầu vào:** `D:\TLCN\20261121_TONG_HOP_DIEM_LECH_USECASE_VA_CLASS_DIAGRAM_KHUYEN_NGHI.md` (21/11/2026), đối chiếu lại các nguồn dưới đây. Đường dẫn ghi trong tài liệu 21/11 là môi trường cũ; không dùng để suy ra hiện trạng máy này.
- **Đối tượng:** nhóm phát triển, người duyệt thiết kế và người cập nhật đặc tả. Mục tiêu TC2.1: có thể truy vết từng thay đổi và phân biệt nợ tài liệu với chức năng đã chạy.
- **Cập nhật tiếp:** đã soạn nội dung đề xuất đầy đủ hơn tại `20261124_DE_XUAT_CAP_NHAT_USECASE_DUYET_CAU.md`; các điểm chưa chốt vẫn giữ nguyên trạng thái chờ nhóm xác nhận.

## 1. Nguồn và mức kiểm chứng

| Nguồn | Phiên bản/quan sát 24/11/2026 | Vai trò và giới hạn |
|---|---|---|
| `requirements/20261016_MoHinhHoaYeuCau.docx` | Đã đọc nội dung OOXML; UCGV14/UCGV15/UCADM13/14 vẫn mô tả gói | Đặc tả Word hiện có, chưa đồng bộ sau 03/11; không kết luận theo tên file về toàn bộ lịch sử sửa |
| `requirements/SRS_TLCN_v3.0.md`, mục 9b, BR-22–28, X | Có ghi bổ sung 03/11; một số nội dung ghi chờ xác nhận | Nguồn đối chiếu yêu cầu; DOCX SRS chưa được xác minh đồng bộ nội dung trong lần này |
| `decisions/20261103_QUYET_DINH_THAY_DOI_THIET_KE_CLASS_DIAGRAM.md` | 03/11 và bổ sung 04/11 | Bỏ gói, giao theo câu, FK, dữ liệu duyệt và Composition; không tự suy diễn các điểm không nêu |
| `design/class/ClassDiagram.puml`, `.mmd`, `TLCN.drawio.xml`, `Mo_ta_So_do_Lop_ClassDiagram.md`, `schema.prisma` | Đã rà phần liên quan | Mô hình thiết kế; không chứng minh chức năng đã chạy |
| `design/sequence/SD_03_ThemVaDuyetCauHoi.xml`, `SD_11_GiaoViecChinhHanNhacHan.xml`, `SD_12_KiemTraVaImportCuoi.xml` | Đã đối chiếu tên và thông điệp liên quan | Các route, mốc và chi tiết được đánh dấu chờ chốt trong sơ đồ không mặc nhiên là chuẩn |
| `design/ui/20261017_MO_TA_LUONG_ROLE_VA_MAN_HINH_CHI_TIET_CHO_AI_AGENT.md` | Có ghi chú 03/11; một số route và quyết định còn mở | Đặc tả UI; không mặc nhiên chứng minh mã hoạt động |
| BE `origin/develop` `9b41f7b`, FE `origin/develop` `5234146`, quan sát tĩnh từ phiên 24/11 | Prisma backend có FK và JSON; FE có `/exam/[sessionId]` và `/exams/[roundId]/take` | Không kết luận về runtime, migration đã áp dụng, trạng thái PR hoặc deploy chỉ từ mã/thiết kế |

## 2. Đánh giá tám điểm trong tài liệu ngày 21/11

| # | Điểm rà soát | Đánh giá sau đối chiếu | Cập nhật / việc còn lại |
|---|---|---|---|
| 1 | Bỏ ItemPackage/PackageStatus, bỏ gửi/ép gửi gói | **Đúng về thay đổi kiến trúc** theo quyết định 03/11; Word UCGV14/15 còn luồng gói. Khẳng định B thấy câu **ngay** sau A duyệt là quá mức: SRS 9b.13 còn để mở thời điểm hiển thị. | Cập nhật bản UC khi được duyệt; bỏ các bước/điều kiện `PACKAGE_INCOMPLETE`, không tự chốt thời điểm B thấy câu. |
| 2 | Bỏ ItemReviewAssignment, giao trên Item | **Đúng** theo bổ sung 04/11: `reviewerId`, `confirmerId` nullable, FK Restrict; `firstReview`/`secondReview` là JSON. | Đồng bộ UCADM13 và mô tả quan hệ; cách chọn từng người/nhóm và thuật toán chia đều còn chờ xác nhận. |
| 3 | ReviewAction bỏ FORCE_SEND/EXTEND, thêm ASSIGN và ACCEPT_FLAG | Quyết định 03/11 bỏ hai action gắn gói và thêm `ASSIGN`; tập action trong quyết định cũng có `ACCEPT_FLAG`. Cách audit thao tác chỉnh hạn còn chờ chốt, không gán `EXTEND` trở lại. | Rà schema và shared-types theo phiên bản thực tế; không thay enum DB hay phát hành gói trong phiên rà soát tài liệu. |
| 4 | ExamRound ◆ TestSession | **Đúng trong mô hình**: Composition; DB dùng `Restrict` để bảo vệ lịch sử, không hiểu là cascade xóa. | Đồng bộ mô tả quan hệ/UC; không sửa chính sách xóa hay migration. |
| 5 | Điều kiện READY_TO_FINALIZE | Theo quyết định: mọi câu đã xử lý hoặc các câu còn lại quá hạn. Câu chưa xử lý quá hạn **không được import**; lô chỉ `DONE` khi mọi câu ở trạng thái cuối. Cần phân biệt A từ chối với B xác nhận. | Đồng bộ UCADM14; không mô tả đơn giản thành “mọi câu xong vòng 2” và không tự tạo thông báo Admin nếu chưa xác minh yêu cầu/triển khai. |
| 6 | Teacher reviewItem/confirmItem | **Đúng ở class model**; bỏ `submitPackage`. Tên phương thức thiết kế không chứng minh API hoặc code đã được triển khai. | Đồng bộ đặc tả mô tả quyền; không bắt buộc tên class/method thực hiện phải trùng nếu chưa có quyết định tương ứng. |
| 7 | `irtA = 1.0` | Có trong class model, Prisma và quyết định #132; Rasch 1PL dùng `a=1`. Đây không phải thay đổi mới được yêu cầu từ tài liệu 21/11. | Giữ dữ liệu không bịa; không suy ra câu đã được calibration hoặc thay đổi tham số CAT. |
| 8 | URL làm bài | **Chưa đủ căn cứ chốt URL mới.** FE develop có cả `/exam/[sessionId]` và `/exams/[roundId]/take`; Word UCSV07 và tài liệu UI không thống nhất. Cần đối chiếu đường điều hướng, F5/resume và quyết định có thẩm quyền. | Lập bảng route thực/thiết kế, kiểm browser và chốt một hợp đồng điều hướng trước khi sửa SRS/UC/code. Không khẳng định tự đổi URL khắc phục triệt để. |

## 3. Bản gốc và bản GV A sửa

- Theo SRS 6.2, thiết kế 03/11 và Prisma tham chiếu: snapshot nằm trong `firstReview.originalSnapshot`; lưu nội dung, lựa chọn, đáp án, giải thích trước lần sửa đầu tiên. Dữ liệu hiện hành chứa bản sau sửa; không tạo item thứ hai chỉ để đối chiếu.
- Định danh trong mô hình hiện hành là **`content`**, không phải `stem`. `Item.options` là JSON; ví dụ mảng `{key,text}` trong báo cáo 21/11 không phải hợp đồng đã chứng minh. Nhánh teacher-review được rà tĩnh ngày 24/11 dùng object theo khóa A–D và snapshot `content`, `options`, `correctAnswer`, `explanation`; đây là mã nhánh, chưa chứng minh đã merge hoặc chạy trên DB thật.
- B chỉ đọc và có thể đối chiếu bản gốc/bản sửa nếu snapshot có. C-DIFF, kiểu tô sáng và tính trợ năng là yêu cầu giao diện cần đối chiếu bản UI được duyệt; không suy từ Class Diagram rằng component đã chạy.
- Quyết định “không lưu lý do từ chối” của SRS cần được phân biệt với trường `comment` nullable trong mô hình. Không tự kết luận có thể lưu lý do từ chối; cần nhóm làm rõ nội dung comment được phép và rà hành vi code.

## 4. Đề xuất chỉnh sửa đặc tả Use Case — chưa áp dụng vào DOCX

Các mục dưới là hướng thay thế có truy vết, không chốt các tham số đang mở.

| Vị trí | Nội dung đề xuất cho bản cập nhật | Điều kiện/cần xác nhận |
|---|---|---|
| 2.2.2, 2.3 | Mô tả GV A sửa/duyệt/từ chối câu được giao; GV B chỉ đọc và xác nhận/loại câu được giao; đổi tên UCGV14/15 bỏ “gửi gói/gói”. | Không khẳng định chia đều và B không thuộc toàn bộ nhóm A nếu quy tắc mới chưa chốt; tối thiểu A khác B trên cùng câu theo SRS. |
| UCGV14 | Khi A sửa lần đầu lưu snapshot một lần; chạy luật cứng và T1–T2, câu không đạt bị chặn; `APPROVE` → `FIRST_APPROVED`, `REJECT` → `REJECTED`; ghi kết quả/event theo thiết kế. Bỏ bước gửi gói và `PACKAGE_INCOMPLETE`. | Thời điểm B nhìn thấy `FIRST_APPROVED` còn chờ chốt. Không ghi lý do từ chối nếu chưa làm rõ `comment`. |
| UCGV15 | B xem các câu đủ điều kiện được giao, chỉ đọc; xác nhận → `SECOND_APPROVED`, loại → `REJECTED`; ghi `secondReview`/event. Có thao tác xác nhận hàng loạt. | Phạm vi hàng loạt theo lô hay toàn hộp việc chưa chốt; không tự chốt theo lô chỉ từ báo cáo 21/11. |
| UCADM13 | Admin giao A/B, hạn và `ASSIGN` theo từng câu; bỏ thực thể bảng/gói và FORCE_SEND. Giao lại, chỉnh hạn chỉ tác động câu đủ điều kiện. | Cách chọn/thuật toán, mốc hạn B, giờ hạn và audit sửa hạn theo câu hỏi còn mở. Không mô tả “ngày nhận gói”. |
| UCADM14 | Điều kiện sẵn sàng đối chiếu mục 2 dòng 5; chạy C3, xử lý kết quả và import câu đủ điều kiện, kiểm tra C3 còn hiệu lực; câu chưa xử lý quá hạn không import. | Xử lý lỗi mềm/hard theo quyết định có hiệu lực; Q-1 và ngưỡng còn cần xác nhận theo kế hoạch. |
| UCGV02/UCGV04 | Thay “câu trong gói” bằng phân công trực tiếp, đúng vai trò; A chỉ sửa câu được giao còn DRAFT; B không sửa. | Route `[itemId]` trong báo cáo 21/11 là đề xuất, trong UI hiện còn `[batchId]` chờ xác nhận; không tự đổi route. |
| UCSV02/UCSV07 | Giữ đúng phân biệt ID kỳ và ID phiên; mô tả tình huống bắt đầu, có phiên đang chạy, reload và tiếp tục. | Chưa thống nhất route cuối; kiểm tra mã và trải nghiệm thực trước khi thay route. |
| Mục 2.5 | Ghi Composition `ExamRound ◆ TestSession`, FK và chính sách Restrict. | Bổ sung đây là chi tiết mô hình lớp; không nhầm thành quan hệ use case hoặc hành vi xóa dây chuyền. |

## 5. Các điểm cần nhóm/GVHD quyết định

1. **Thời điểm B thấy câu:** (A) ngay sau A duyệt từng câu; (B) sau khi A xử lý hết phần được giao. Cả hai không cần khôi phục ItemPackage. Lựa chọn ảnh hưởng thông báo, thời hạn và test.
2. **Phạm vi xác nhận tất cả:** (A) câu đủ điều kiện trong lô đang mở; (B) toàn bộ câu đủ điều kiện của B. Cần xác nhận hành vi đồng thời và audit.
3. **Giao việc/hạn:** (A) gán trực tiếp từng câu; (B) chọn nhóm, xem trước rồi ghi phân công từng câu. Hạn B tính từ ngày giao hay lúc A duyệt; cách sửa hạn và ghi audit còn mở.
4. **Route S04/tiếp tục bài:** (A) lấy sessionId làm ID route; (B) giữ roundId và khôi phục phiên qua API. So sánh reload, phiên không tồn tại/nhiều phiên, quyền và lịch sử trước khi chốt.
5. **`comment` và từ chối:** (A) không ghi lý do từ chối, chỉ cho phép ghi chú trường hợp khác; (B) thay đổi quy tắc nghiệp vụ nếu nhóm muốn lưu lý do. Phương án B cần quyết định và đồng bộ SRS/UC/schema/UI.

## 6. Thay đổi tài liệu đã thực hiện và nợ còn lại

| Tài liệu | Trạng thái 24/11/2026 | Việc còn lại |
|---|---|---|
| ClassDiagram.puml, ClassDiagram.mmd, `TLCN.drawio.xml`, mô tả lớp | Đã sửa ký hiệu `ItemReviewEvent.itemId {nullable}` tại hai sơ đồ text và hai vị trí draw.io, khớp mô tả 3.6 và hai schema tham chiếu/mã | Xuất lại và kiểm tra PNG `TLCN-Trang-1…3.png`; xác minh bố cục trên draw.io. Không sửa số lớp/enum. |
| UC DOCX `20261016_MoHinhHoaYeuCau.docx` | Đã đọc; chưa sửa | Cập nhật theo mục 4 sau khi các điểm mở được chốt; đồng bộ Use Case Diagram nếu tên UC/quan hệ thay đổi. |
| SRS v3.0 `.md` | Đã bổ sung cảnh báo khác biệt về câu quá hạn/chưa xử lý sau Import; đã có ghi chú 03/11 và các điểm mở | Đối chiếu các mục có hai cách diễn đạt sau khi nhóm chốt; không tự áp các đề xuất chưa chốt. |
| SRS `.docx`, Use Case Diagram/XMI/JPG | Đã đọc SRS Word và thấy vẫn còn mô tả gửi/ép gửi gói; chưa sửa Word hoặc sơ đồ UC | Cập nhật các nội dung chắc chắn, ghi rõ các điểm cần chốt; kiểm tra bố cục Word và xuất lại ảnh nếu sửa diagram. |
| Sequence SD03/SD11/SD12, UI S10/S11/S33–S35, S03–S07 | UI đã sửa câu chữ còn gợi gửi gói; SD03/SD11 đã ghi rõ các lựa chọn về thời điểm, chọn người/hạn và chia đều còn chờ chốt. Đã dựng lại ảnh PNG SD03/SD11; SD12 và route/quy tắc mở chưa sửa | Sau khi chốt mục 5, cập nhật thông điệp/nhãn/route và dựng lại ảnh tương ứng. |
| Prisma, shared-types, BE/FE | Đối chiếu tĩnh tại SHA nêu ở mục 1 | Review enum, quyền, race và luồng thực theo báo cáo kỹ thuật riêng; không chạy migration, seed, sửa mã hoặc khẳng định triển khai hoàn tất. |
| Tracking | AI usage ghi phiên này; weekly log chưa cập nhật do chưa xác minh người và tuần | Bổ sung minh chứng/review và báo cáo tuần khi nhóm xác nhận. |

## 7. Kiểm chứng cần làm trước khi coi là đồng bộ

- GV A duyệt/từ chối từng câu; A chỉ sửa DRAFT của mình; snapshot chỉ ghi lần đầu; kiểm tra cứng và T1–T2 sau sửa; B không sửa/không trả lại A.
- Kiểm 403 khi sai vai trò hoặc sai người được giao; đồng thời approve/reject/confirm-all/reassign không ghi đè sai; `CONFIRM_ALL` đúng phạm vi đã chốt và log hợp lệ.
- Kiểm `READY_TO_FINALIZE` khi còn câu quá hạn, câu A từ chối, lô rỗng và import song song; câu chưa xử lý không được thành `FINAL_APPROVED`.
- Kiểm S04/F5 theo quyết định route cuối, dữ liệu thật, trạng thái phiên và quyền; kiểm các biểu diễn UML text/draw.io/ảnh và khớp schema.
- Chạy test/CI theo phần mã thay đổi khi có triển khai; cuộc rà soát tài liệu này không chứng minh nghiệp vụ runtime hay đạt rubric.


**Tiến độ 24/11:** SD03 và SD11 đã cập nhật, kiểm tra XML và xuất lại ảnh. Đã sửa bố cục và xuất lại ba ảnh Class Diagram. Hai bản Word đã tạo để kiểm tra nhưng chưa thay bản chính thức. XMI Use Case đã sửa tên UCGV04/14/15; ảnh Use Case còn cũ, quan hệ Admin với UCGV04 và quan hệ include chỉnh sửa cần rà theo SRS. Các quyết định ở mục 5 vẫn chờ nhóm xác nhận. Không coi bản dựng tạm là văn bản đã duyệt.

**Cập nhật tiếp:** Đã thay Word Use Case chính thức bằng bản kết xuất và kiểm tra, loại đường dẫn `packageId` cũ và ghi rõ UCGV06 chờ chốt. Word SRS chưa thay; ảnh và quan hệ Use Case còn cần đồng bộ, các quyết định nghiệp vụ mở vẫn giữ nguyên trạng thái chờ xác nhận.
