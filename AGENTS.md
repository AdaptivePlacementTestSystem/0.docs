# Hướng dẫn Codex — Adaptive Placement Test

Áp dụng trong `D:\TLCN`. Đây là bản chỉ dẫn và bản đồ tra cứu, không thay thế SRS, quyết định đã chốt, mã hiện hành hay chỉ dẫn ưu tiên cao hơn. Trước mỗi nhiệm vụ, đọc thêm AGENTS.md trong thư mục con có liên quan; bảo vệ các thay đổi có sẵn của người dùng.

## Nguồn sự thật và cách kiểm chứng

1. Đọc `docs-repo/CLAUDE.md`, `docs-repo/process/HUONG_DAN_RUBRIC_VA_TRACKING.md`, và phần liên quan trong `0.docs/tracking/DECISIONS_LOG.md`. Đây là tracking vận hành tại máy; `docs-repo/tracking/` có thể chỉ là bản sao. Kiểm tra ngày và nội dung trước khi kết luận.
2. Tra yêu cầu và các mục còn đề xuất/chờ chốt trong `docs-repo/requirements/SRS_TLCN_v3.0.md` (bản DOCX cần đồng bộ), đặc tả use case, `docs-repo/design/`, `docs-repo/plans/` và quyết định liên quan. `docs-repo/drafts/` và worktree dưới `.claude/worktrees/` không mặc nhiên là bản chuẩn.
3. Đọc mã, migration, test, cấu hình và trạng thái Git thực tế trước khi khẳng định chức năng hoạt động. Thiết kế, sơ đồ, README, test cũ và log lịch sử không chứng minh tính năng hiện đang chạy. Khi các nguồn lệch nhau, nêu rõ nguồn, thời điểm và mức độ xác minh; không tự quyết định thay đổi thiết kế để xóa mâu thuẫn.
4. Khi làm việc trong repo, tìm `0.docs/AI-WORKFLOW.md` từ gốc repo lên các thư mục cha; nếu có thì đọc trước khi sửa mã và làm đúng quy ước phiếu ở cuối commit. Đầu phiên đọc `~/.hqsoft-ai-usage/nhac-phieu.md` nếu tồn tại và báo ngắn nội dung nhắc.

## Rubric và kỷ luật dự án

- Mọi đề xuất, phương pháp và đánh giá phải liên hệ tiêu chí, gate và minh chứng thích hợp trong `docs-repo/process/` và tracking; hướng tới mức cao nhưng không khẳng định đạt điểm nếu chưa có bằng chứng. Số liệu chưa đo ghi chưa đo/N/A, không bịa KPI, kết quả test hay xác nhận.
- Theo dõi G1 (cam kết sản phẩm/KPI có xác nhận), báo cáo tuần, kiểm thử, CI/CD, thực nghiệm và chứng cứ. Tại thời điểm đọc 23/11/2026, `0.docs/tracking/COMMITMENT_BASELINE.md` ghi **chưa ký**, thiếu ngày bắt đầu; cần người dùng xác minh thực tế, không suy diễn trạng thái hiện tại hay thời hạn.
- Khi AI sinh/sửa mã hoặc tài liệu đáng kể, ghi `0.docs/tracking/AI_USAGE_LOG.md`: ngày, thành viên, công cụ, phạm vi, prompt, phần AI sinh, phần con người cần kiểm và commit nếu biết. Không tự nhận đã có người review. Cập nhật weekly-log phù hợp khi có thông tin xác thực; không tự đoán tuần/người thực hiện.
- Trước tính năng, refactor hay bugfix không tầm thường, đọc `0.docs/tracking/PROMPT_TEMPLATE_FEATURE.md`, tạo/cập nhật feature plan từ template, truy vết F-ID/SRS, quyết định, thiết kế OOP và kiểm thử. Khi quyết định chưa rõ có tác động kiến trúc, schema, khả năng bảo trì/mở rộng, nêu ít nhất hai phương án và đánh đổi; làm các phần độc lập trước và xin người dùng chốt phần cần thiết.
- Khi thay đổi phạm vi, API, schema, quyền, thuật toán, luồng hoặc UI đã được chốt, rà soát SRS, đặc tả UC, diagrams, schema, UI, kế hoạch, quyết định và log; ghi rõ nợ đồng bộ. Tài liệu chưa chốt đặt tại `docs-repo/drafts/`; không tự biến đề xuất thành bản chuẩn. Diagram dùng tiếng Anh, tài liệu và tracking tiếng Việt trừ khi được yêu cầu khác.
- Đọc `docs-repo/workspace-setup/tlcn-devkit-plugin/tlcn-devkit/skills/rubric-tracker/SKILL.md` để hiểu quy trình dự án; đây là tài liệu skill của Claude, không giả định nó tự chạy trong Codex. Khi có xung đột đường dẫn hoặc nội dung cũ, đối chiếu nguồn hiện hành.

## Bản đồ hệ thống

- Hệ thống placement test tiếng Anh thích ứng CAT–Rasch, ánh xạ năng lực sang CEFR và tạo Language Profile. Phạm vi Tiểu luận gồm Vocabulary/Grammar, đơn trường, STUDENT/TEACHER/ADMIN, auth, kỳ thi, import, item bank và quy trình sinh/duyệt câu hỏi; Writing, SSO, multi-tenant và các mục [KL] thuộc phạm vi mở rộng, không tự triển khai.
- `apt-workspace/backend/`: repo NestJS/TypeScript, Prisma/PostgreSQL, Redis; xem `src/app.module.ts`, `src/modules/`, `prisma/schema.prisma`, `CODING_CONVENTION.md`, `TECH_DEBT.md`. Module gồm auth, item-bank, cat-engine, test-session, language-profile, reporting, mail, exam-round, user-import, user-admin, item-generation, llm-gateway, ai-explainer, health. Các module không đồng nghĩa với chức năng hoàn chỉnh.
- `apt-workspace/frontend/frontend/`: repo Next.js/React; routes `(admin)`, `(auth)`, `(exam)`, `(student)`, `(teacher)` và `api` BFF; xem `src/features/`, `src/lib/`, quy ước và AGENTS.md tại repo này. Trước khi sửa Next.js, đọc hướng dẫn tương ứng trong `node_modules/next/dist/docs/` theo AGENTS.md của frontend.
- Kiểm tra ngày 23/11/2026: `exam-round` đã có use case và test, trong khi `item-generation` chỉ thấy file module; `@apt/shared-types` trong package.json của cả hai repo trỏ đến Git tag `v3.0.0`, không phải `file:` như một số tài liệu cũ. Đây là quan sát tĩnh, phải kiểm tra lại trước khi dùng; chưa chứng minh luồng hoàn chỉnh.
- `apt-workspace/run-local.ps1` mô tả chạy local; script có thể khởi động Docker, container, migration và seed, nên đọc trước khi chạy. Backend có `npm run build`, `lint`, `typecheck`, `test`, `test:e2e`; frontend có `build`, `lint`, `typecheck`, `test`, `test:e2e`. Không tuyên bố các lệnh thành công nếu chưa chạy.

## Bất biến nghiệp vụ cần đối chiếu

- SRS mục IV là nguồn đối chiếu CAT: Rasch 1PL, EAP lưới đều 41 điểm từ -4 đến 4, prior N(0,1), chọn ngẫu nhiên trong Top-5 theo độ gần b–θ và chỉ dùng item `FINAL_APPROVED`. Đối chiếu chi tiết guard, cấu hình, thứ tự dừng và điều kiện biên với SRS cùng quyết định mới nhất; không lấy ví dụ minh họa làm số đo thực nghiệm.
- Các tham số dự kiến gồm θ ban đầu -0,5, SE 0,35, tối đa 25 câu, tối thiểu 8 câu trước early stop; ngưỡng phải cấu hình. Thay đổi EAP/Rasch/stopping cần đối chiếu công thức với SRS và kiểm thử toàn đúng, toàn sai, xen kẽ, cùng các biên liên quan trước merge.
- SRS v3.0 mô tả PostgreSQL là nguồn dữ liệu bền vững, Redis hỗ trợ trạng thái/đồng thời; kiểm tra implementation thực tế và hành vi mất Redis trước khi khẳng định dual-write/recovery. AI gateway, calibration offline, lưới tạm và hàng đợi phải được kiểm tra ở mã liên quan, không suy ra chỉ từ sơ đồ.
- Vòng đời câu hỏi và vai trò A/B/Admin, AI checks C1/C2/C3 và những câu hỏi chưa chốt: tra SRS mục 9b và `docs-repo/plans/KE_HOACH_SINH_VA_DUYET_DE_AI.md`; xác minh phiên bản quyết định trước khi đề xuất hay code.

## Git, devkit và quyền

- Đọc `docs-repo/devkit/README.md`, các hook thực tế, workflow và `0.docs/tracking/GIT_CONVENTIONS.md` trước commit/PR. Mô hình dự kiến: nhánh `feat|fix|docs|chore|test|refactor/<ten>` vào develop qua PR squash; develop vào main qua PR merge commit; hotfix vào main rồi đồng bộ develop. Không tự bypass hook, ruleset, review, secret scan hoặc push thẳng nhánh bảo vệ. Kiểm tra cấu hình thực tế; tài liệu devkit ghi một số ruleset/CI chưa được kiểm chứng từ thời điểm viết.
- Không đưa `.env`, token hoặc dữ liệu nhạy cảm vào log, commit hay prompt. Không chạy cài đặt devkit `--force`, thay ruleset GitHub, migration hoặc seed một cách mù quáng; đọc tác động và tôn trọng dữ liệu, thay đổi hiện có.
- Quyền workspace, mạng, Google, Docker và GitHub do môi trường/tài khoản cấp; file này không thể tự mở rộng sandbox, xác thực hay cấp quyền. Dùng connector hoặc CLI đã được cấp khi cần, kiểm tra quyền thực tế và báo rõ giới hạn; không né các điểm chặn bảo mật.
