# Hướng dẫn đáp ứng Rubric & Hệ thống ghi log/tracking
### Đồ án: Adaptive Placement Test (CAT–Rasch) — Nhóm 2 người, 12 tuần Tiểu luận

> Nguồn đối chiếu: `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` (bản Khoa cấp), `SRS_TLCN (3).md` v2.4/2.5, `SRS_TLCN_ClassDiagram_Analysis.md`, `Mo_ta_So_do_Lop_ClassDiagram.md`.
> Tài liệu này trả lời 2 câu hỏi: **(1)** rubric thực sự đòi hỏi minh chứng gì, và **(2)** với đúng kiến trúc/thuật toán trong SRS của nhóm, minh chứng đó lấy từ đâu / làm thế nào cho đủ Mức 4–5.
> Đi kèm là hệ thống log/tracking đã khởi tạo tại `tracking/` và Skill Claude Code tại `.claude/skills/rubric-tracker/` để việc ghi log không bị quên giữa lúc code.

---

## 0. Đọc vị rubric trước khi làm gì khác

Ba điều quyết định điểm số nhiều hơn cả chất lượng code:

1. **"Chấm theo minh chứng" (Nguyên tắc 3, Mục 1):** thiếu minh chứng cho một tiêu chí → tiêu chí đó **không thể vượt quá Mức 3**, bất kể sản phẩm thực tế tốt đến đâu. Rubric không chấm "cái đã làm", nó chấm **"cái chứng minh được là đã làm"**.
2. **Quy tắc chặn điểm (Mục 7, G1–G10)** đứng trên mọi mô tả mức. Ví dụ: dù TC2.5 (kiểm thử) mô tả kỹ đến đâu, nếu không có test tự động **và** không có tài liệu test thủ công thì G5 áp trần Mức 1 (≤1,75đ) — không bàn cãi theo mức mô tả nữa.
3. **Mốc cam kết Bước 3 trước 50% thời gian (~cuối Tuần 6/12)** là gate cứng nhất (G1): không chốt được sản phẩm cuối + bộ metric bằng văn bản có chữ ký trước mốc này → **cả đồ án bị đánh giá Không đạt**, không có cách nào gỡ lại ở Bước 4.

Vì nhóm dùng Claude Code (Agentic AI) xuyên suốt, **TC2.3 (AI Usage Log)** và **Mục 6 (chống đạo văn)** là rủi ro lớn nhất nếu không ghi log ngay từ đầu — hội đồng chọn ngẫu nhiên ≥5 vị trí (2 trong luận văn, 3 trong code/minh chứng) và sinh viên có **3 phút/vị trí** để giải thích. Không giải thích được → tối thiểu mất điểm tiêu chí đó (V1), tệ nhất mất **toàn bộ đồ án** (V3/V4). Đây là lý do chính khiến hệ thống tracking dưới đây bắt buộc phải chạy song song với việc code, không phải làm hồi tố cuối kỳ.

---

## 1. Timeline rủi ro cao (giả định Tuần 1 bắt đầu từ hiện tại, 12 tuần TL)

| Mốc | Khi nào | Gate | Hồ sơ bắt buộc |
|---|---|---|---|
| Chốt đề tài, phân công thành viên | Cuối Tuần 1 | Bước 1–2 | Phiếu đăng ký + bảng phân công theo `tracking/COMMITMENT_BASELINE.md` |
| Báo cáo tiến độ hàng tuần, ≥1 lần/tuần | Từ Tuần 1, liên tục | G2 (<0,5 lần/tuần → TC2.2 & TC2.4 mỗi tiêu chí giảm 1 mức) | `tracking/weekly-log/Tuan-XX.md`, có xác nhận GVHD |
| **Cam kết sản phẩm cuối + bộ KPI (Bước 3)** | **Trước Tuần 6** | **G1 — không đạt = KHÔNG ĐẠT toàn đồ án** | `tracking/COMMITMENT_BASELINE.md` có chữ ký SV + GVHD |
| Linear Pre-test ≥60 SV (SRS Mục VI.1) | Tuần 7–8 | Nền cho R1/R2 (Risk Register SRS) | Biên bản + response matrix — cũng là dịp gộp luôn khảo sát TC1 và thực nghiệm TC2.7 |
| IRT Calibration (py-irt/MMLE) | Tuần 9–10 | — | Báo cáo calibration + item fit (MNSQ) |
| CI/CD chạy được tại thời điểm bảo vệ | Trước bảo vệ | G6 (không có = TC2.6 trần Mức 2) | `tracking/evidence-checklist.md` mục 9 |
| Thực nghiệm người dùng thật, càng sớm càng tốt để kịp đo lại vòng 2 | Nên xong trước Tuần 10 | G7 (không có = TC2.5→TC2.7 trần Mức 1) | Biên bản thực nghiệm, ẩn danh |

---

## 2. Ánh xạ từng tiêu chí → việc cụ thể phải làm trong dự án này

### TC1 — Tính thực tiễn & hiểu vấn đề (10đ)

Rubric Mức 5 cần: ≥3 bên liên quan phỏng vấn hoặc ≥30 phiếu khảo sát; so sánh ≥3 giải pháp hiện có; chốt ≥5 KPI định lượng **ngay tại Bước 3** và giữ nguyên đến khi bảo vệ.

Gợi ý cho đề tài CAT-Rasch:
- **Đối tượng khảo sát:** SV năm nhất đã từng làm placement test cố định, GV phụ trách chấm/nhập điểm, (nếu có) người phụ trách chương trình đào tạo ngoại ngữ — đúng 3 nhóm liên quan SRS đã mô tả (Mục I.3).
- **So sánh ≥3 giải pháp hiện có:** (1) bộ đề cố định 40–50 câu hiện tại của trường, (2) công cụ CAT thương mại (Duolingo English Test/Pearson) — nêu rõ vì sao không dùng được (chi phí, không tích hợp EduZ, không xuất profile có cấu trúc), (3) chấm tay/Google Form của GV.
- **5 KPI định lượng nên chốt ở Bước 3** (khớp thẳng với NFR ở SRS Mục XV và thuật toán Mục IV, nên số liệu không bịa mà lấy thẳng từ đặc tả đã duyệt):
  1. Số câu trung bình để đạt điều kiện dừng ≤ 25 (so với 40–50 câu cố định).
  2. Thời gian hoàn thành trung bình < 25 phút (so với ngưỡng timeout 45 phút).
  3. SE(θ) cuối bài < 0,35 đạt được ở ≥ X% phiên thi (X tự chốt sau pre-test).
  4. API latency p95 submit+next-item < 300ms (đã có sẵn trong NFR — chỉ cần đo và báo cáo).
  5. Exposure rate câu phổ biến nhất giảm từ ước tính 100% (deterministic) xuống theo số đo thực tế của Randomized Top-5 (SRS Mục 4.4 đã có bảng ước lượng 60–70% — dùng làm baseline rồi đo thực tế sau khi có dữ liệu 500 SV/đợt).

  → Ghi các KPI này vào `tracking/COMMITMENT_BASELINE.md` **trước Tuần 6**, không đổi sau đó trừ khi có biên bản điều chỉnh của bộ môn.

### TC2.1 — Phân tích nghiệp vụ & thiết kế (10đ)

Đã có nền tốt: SRS đầy đủ use case ngầm định trong Mục IX (F-01→F-10), Class Diagram 31 lớp (`Mo_ta_So_do_Lop_ClassDiagram.md`), NFR đầy đủ (Mục XV, ≥5 yêu cầu định lượng → đã đạt ngưỡng Mức 5 của tiêu chí phụ này).

Còn thiếu để đạt "≥4 loại sơ đồ" (Mức 5 yêu cầu context, component, ERD/class, sequence, deployment):
- ✅ Class diagram — đã có.
- ✅ Component/module diagram — có sẵn dạng cây thư mục `src/modules/` (SRS Mục III) — nên vẽ lại thành sơ đồ chính thức (Mermaid `graph` hoặc `component`).
- ❌ **Sequence diagram** — cần vẽ tối thiểu luồng `submitResponse → CATEngine.computeEAP → checkStoppingCriterion → getNextItem`, và luồng dual-write (Mục VIII SRS) — đây là phần "trái tim" nên hội đồng rất dễ hỏi.
- ❌ **Deployment diagram** — Nginx / Next.js / NestJS / PostgreSQL / Redis / Docker — SRS Mục III đã có sơ đồ ASCII, chỉ cần chuyển thành UML deployment diagram chuẩn.

**Điểm mấu chốt để lên Mức 5, không phải Mức 4:** "mọi thay đổi thiết kế đều được ghi nhận lý do trong báo cáo tiến độ". SRS của nhóm đã có changelog rất tốt (v2.1→v2.5) — **duy trì thói quen này trong `tracking/weekly-log/`** mỗi khi đổi thiết kế (ví dụ nếu sau pre-test phải đổi ngưỡng SE hoặc thay đổi command). Đây chính xác là lý do Skill dưới đây bắt Claude phải hỏi/ghi log thay đổi thiết kế mỗi tuần.

Acceptance criteria: SRS hiện là đặc tả kỹ thuật (thuật toán, schema, API), chưa phải dạng "user story + acceptance criteria". Nên bổ sung một bảng ánh xạ F-01→F-10 sang user story ngắn (Given/When/Then) trong tài liệu SRS/SDD nộp — không cần viết lại từ đầu, chỉ cần **thêm bảng** để đạt tiêu chí "100% user story có acceptance criteria".

### TC2.2 — Mức độ hoàn thiện sản phẩm & khối lượng công việc (10đ)

Mức 5 cần: 100% chức năng cam kết chạy ổn định, ≥100% khối lượng, **chạy trên production/staging công khai có người dùng thật**, demo trực tiếp không lỗi, có xử lý ngoại lệ/edge case/phân quyền/log/trạng thái biên.

- Vì layer hạ tầng đã thiết kế Docker + Nginx (SRS Mục XI), **deploy lên VPS/staging công khai ngay từ khi có bản chạy được đầu tiên** (đừng để tới tuần cuối) — vì Mức 3 chỉ "chạy local" trong khi Mức 4 cần "staging truy cập từ bên ngoài".
- Bảng lộ trình 12 tuần trong SRS (Mục XII) chính là "khối lượng cam kết Bước 3" — copy đúng bảng đó (hoặc bản điều chỉnh sau khảo sát thực tế) vào `COMMITMENT_BASELINE.md`, rồi theo dõi % hoàn thành hàng tuần trong `tracking/TRACKING.md`.
- Edge case bắt buộc phải test và demo được (đã có sẵn trong SRS, đừng bỏ sót khi demo): outlier early-stop (SV rất giỏi/rất yếu), Redis mất session → `reconstructFromDB()`, double-submit khi spam `GET /next-item`, MLE fallback khi toàn đúng/toàn sai.

### TC2.3 — Làm chủ & kiểm soát AI (5đ) — **quan trọng nhất với cách nhóm đang làm việc**

Đọc kỹ Mức 5: cần **AI Usage Log đầy đủ đối chiếu được với git history** (công cụ, phạm vi, prompt chính, phần AI sinh, phần SV sửa); giải thích đúng **100%** vị trí code AI sinh khi hội đồng hỏi ngẫu nhiên ≥5 vị trí; nêu được ≥5 lỗi/ảo giác AI đã tự phát hiện kèm phân tích nguyên nhân; có quy trình kiểm soát đầu ra AI thành hệ thống (checklist review, đối chiếu tài liệu chính thức, kiểm tra license/dữ liệu nhạy cảm trong prompt).

Rủi ro cụ thể của dự án này: công thức Rasch/EAP/Gaussian-Hermite quadrature rất dễ bị AI sinh sai tinh vi (SRS đã tự cảnh báo ở Mục 4.3: "EAP là phần dễ bug nhất"). Đây vừa là rủi ro kỹ thuật (R3 trong Risk Register) vừa là **cơ hội điểm** — nếu nhóm chủ động viết unit test đối chiếu tay 3 case biết trước (toàn đúng/toàn sai/xen kẽ) và ghi lại trong AI Usage Log rằng "AI sinh code EAP lần đầu bị lỗi X, phát hiện qua test case Y, đã sửa ở commit Z" — đó **chính là bằng chứng cho cả TC2.3 Mức 5 lẫn TC5 (trả lời hội đồng về phần có AI hỗ trợ)**.

Việc bắt buộc:
- Ghi `tracking/AI_USAGE_LOG.md` **ngay khi** AI sinh ra đoạn code/tài liệu có ý nghĩa (không dồn cuối kỳ — sẽ không khớp lịch sử commit, rơi vào G4 → TC2.3 = 0đ + kích hoạt Mục 6).
- Mỗi thành viên tự giải thích được (không chỉ người prompt) — vì hội đồng hỏi ngẫu nhiên bất kỳ ai.
- Có "review checklist" cố định trước khi merge PR có phần AI sinh (mẫu tại `tracking/GIT_CONVENTIONS.md`).

### TC2.4 — Chất lượng mã nguồn & QLCL phần mềm (10đ)

Mức 5 cần: 0 lint error tồn, static analysis 0 Blocker/Critical, duplication ≤3%, ≥90% số tuần có commit, ≥90% thay đổi qua PR có review, 0 secret lộ, có README + tài liệu kỹ thuật + danh mục nợ kỹ thuật.

Với nhóm 2 người: thiết lập ngay từ Tuần 1 — ESLint + Prettier (NestJS/Next.js đều hỗ trợ sẵn), Husky pre-commit hook chạy lint, `.env` + `.env.example` (không commit `.env` thật), review chéo bắt buộc (A review PR của B và ngược lại — với 2 người vẫn tính là "qua PR có review"). Dùng SonarQube Community/SonarCloud (miễn phí cho repo public) hoặc CodeQL free cho GitHub. Quét secret bằng `gitleaks` trong CI (xem TC2.6).

### TC2.5 — Kiểm thử phần mềm (5đ)

Mức 5 cần ≥4 tầng test (unit/integration/API/E2E hoặc phi chức năng), coverage ≥70% module core, automation ≥70%, 0 defect Critical/Blocker tồn đọng, có bug tracker.

Ưu tiên tuyệt đối: **unit test cho `CATEngine`** (EAP, Gaussian-Hermite quadrature, `checkStoppingCriterion`, MLE fallback guard) — SRS đã tự chỉ định 3 test case bắt buộc (Mục 4.3): 5 câu đúng liên tiếp → θ tăng rõ rệt; 5 câu sai liên tiếp → θ giảm; xen kẽ → θ hội tụ giữa; cộng thêm case toàn đúng/toàn sai để test MLE guard + clip [-4,4]. Đây vừa đúng yêu cầu rubric vừa đúng risk R3/R10 trong SRS.

### TC2.6 — CI/CD & vận hành (5đ)

Mức 5 cần pipeline ≥6 chặng (build → lint → test → security/dependency scan → đóng gói Docker → deploy tự động), build xanh ≥90%, ≥10 lần deploy tự động trải đều, commit→staging ≤15 phút, quản lý secret qua nền tảng CI, có health check + log tập trung + alert.

Gợi ý: GitHub Actions (miễn phí) với các job: `lint` → `test` (kèm coverage) → `gitleaks/npm audit` → `docker build` → `deploy` (SSH hoặc registry + webhook). Bắt đầu pipeline **từ Tuần 3–4**, không để cuối kỳ mới dựng — vì Mức 5 cần "≥10 lần triển khai tự động **trải đều theo tiến độ**", dồn cuối sẽ bị đánh giá thấp hơn dù đủ số lần.

### TC2.7 — Thực nghiệm người dùng thực & cải tiến (5đ)

Mức 5 cần ≥10 người dùng thật đúng nhóm mục tiêu (SV năm nhất, không phải bạn cùng lớp), task success ≥90%, SUS≥80, **≥1 vòng cải tiến có đo lại và so sánh trước–sau**.

Tận dụng luôn đợt **Linear Pre-test ≥60 SV (Tuần 7–8)** trong SRS — đây vốn dĩ đã cần tuyển SV thật, nên gộp thêm bảng khảo sát SUS/task success vào cùng đợt đó để không phải tuyển thêm lần nữa. Sau khi Activate CAT (Tuần 11), nếu kịp, chạy thêm một vòng nhỏ để có số liệu "trước–sau" (linear test vs CAT) — vừa phục vụ TC2.7 Mức 5 vừa phục vụ RQ1 (SRS Mục XIII: "CAT-Rasch có đạt độ chính xác tương đương Linear Test dài gấp đôi không?").

### TC3, TC4, TC5, TC6 — ghi chú nhanh

- **TC3 (thuyết trình):** demo phải chạy trên môi trường đã deploy thật (không video) để đạt Mức 5; chuẩn bị sẵn số liệu coverage/CI/thực nghiệm dạng biểu đồ trực quan trong slide.
- **TC4 (luận văn):** cần ≥5 tài liệu ngoại ngữ chất lượng (paper IRT/Rasch, EAP, CAT — không thiếu vì đây là mảng học thuật có nhiều paper gốc, ví dụ Lord, Bock & Mislevy 1982 cho EAP) và trùng lặp ≤20%.
- **TC5 (hỏi đáp hội đồng):** chuẩn bị riêng phần "giải thích các đoạn AI hỗ trợ" — chính là tái sử dụng `AI_USAGE_LOG.md`, không phải nhớ lại từ đầu.
- **TC6 (điểm thưởng):** nếu Language Profile JSON hoặc CAT Engine có tiềm năng viết thành bài báo ngắn/report hội nghị sinh viên, cân nhắc sớm — đây là điểm cộng gần như miễn phí nếu đã làm tốt TC2.

---

## 3. Hệ thống ghi log/tracking đã khởi tạo

```
tracking/
├── TRACKING.md              # Dashboard: metric hiện tại so với ngưỡng Mức 3/4/5 (Mục 5 rubric)
├── AI_USAGE_LOG.md          # Nhật ký sử dụng AI — bắt buộc cho TC2.3, cập nhật MỖI PHIÊN có AI hỗ trợ
├── COMMITMENT_BASELINE.md   # Bản cam kết Bước 3 — PHẢI ký trước Tuần 6 (gate G1)
├── GIT_CONVENTIONS.md       # Quy ước Git/PR — phục vụ TC2.4
├── evidence-checklist.md    # Checklist toàn bộ hồ sơ minh chứng (Mục 8 rubric)
├── HUONG_DAN_BAO_CAO_TUAN.md # Hướng dẫn chi tiết cách viết/xác nhận báo cáo tuần + ví dụ tốt/yếu
├── PROMPT_TEMPLATE_FEATURE.md # Mẫu prompt chuẩn khi triển khai 1 chức năng/vấn đề — OOP + quy tắc "không tự quyết định"
├── feature-plans/
│   └── _template.md         # File kế hoạch cho TỪNG chức năng — tham chiếu SRS/Class Diagram + bảng câu hỏi/quyết định
└── weekly-log/
    ├── _template.md
    └── Tuan-01.md           # Nhật ký tuần — phục vụ Bước 3, TC2.1 (lý do đổi thiết kế), gate G2
```

**Quy trình chuẩn khi bắt đầu một chức năng/vấn đề mới (bắt buộc từ nay):** dùng `tracking/PROMPT_TEMPLATE_FEATURE.md` để soạn prompt giao việc → AI tạo `tracking/feature-plans/<slug>.md` trước khi code → mọi lựa chọn thiết kế ảnh hưởng khả năng mở rộng mà SRS/Class Diagram chưa quyết định rõ đều phải hỏi lại và ghi vào Mục 3 của file kế hoạch đó, đồng thời nhắc lại trong `weekly-log` tuần tương ứng. Không có ngoại lệ "AI tự chọn cho nhanh".

Đây không phải giấy tờ hình thức — mỗi file map thẳng tới một tiêu chí hoặc một gate ở trên. Bỏ trống bất kỳ file nào cũng đồng nghĩa với việc tiêu chí tương ứng bị khóa trần ở Mức ≤3 hoặc kích hoạt gate G2–G8.

## 4. Skill Claude Code: `.claude/skills/rubric-tracker`

Đã tạo một Skill dự án tại `.claude/skills/rubric-tracker/SKILL.md`. Khi làm việc với Claude Code trong thư mục `D:\TLCN` (kể cả sau khi có source code thật), skill này sẽ được nạp và nhắc/tự thực hiện:

- Sau khi AI sinh ra đoạn code/tài liệu có ý nghĩa → thêm dòng vào `AI_USAGE_LOG.md` ngay trong phiên đó.
- Trước khi kết thúc phiên làm việc có thay đổi thiết kế → hỏi có cần ghi vào nhật ký tuần không.
- Đầu mỗi tuần làm việc mới → tạo `weekly-log/Tuan-XX.md` từ template nếu chưa có.
- Gần mốc 50% thời gian (Tuần 6) → nhắc chốt `COMMITMENT_BASELINE.md`.
- Khi chuẩn bị commit → nhắc quy ước tại `GIT_CONVENTIONS.md` (commit message, PR review).

Chi tiết hành vi và mẫu (templates) nằm trong `.claude/skills/rubric-tracker/references/`.

## 5. Checklist nhanh trước mỗi buổi báo cáo GVHD hàng tuần

- [ ] `weekly-log/Tuan-XX.md` đã điền đủ: việc đã làm, vướng mắc, thay đổi thiết kế (nếu có) kèm lý do, kế hoạch tuần sau.
- [ ] Đã có xác nhận/chữ ký (hoặc email) của GVHD cho tuần đó.
- [ ] `AI_USAGE_LOG.md` không có khoảng trống nào >3 ngày so với lịch sử commit thật.
- [ ] `TRACKING.md` đã cập nhật số liệu mới nhất (coverage, lint, số commit/tuần...) nếu có thay đổi.
- [ ] Nếu tuần này đã qua 50% thời gian mà `COMMITMENT_BASELINE.md` chưa có chữ ký → **dừng mọi việc khác, xử lý ngay** (gate G1).
