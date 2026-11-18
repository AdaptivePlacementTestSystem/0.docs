# Mô tả Component Diagram và Deployment Diagram (Tiểu luận v3.0)

- Ngày lập: 2026-10-21 (Tuần 5/12). Ký pháp theo `D:\UML tieng Viet.pdf` mục XII (Component) và XV (Deployment).
- Tệp: `Update/TLCN_Component_Deployment.drawio` (2 trang, mở bằng draw.io), ảnh `TLCN_ComponentDiagram.png`, `TLCN_DeploymentDiagram.png`.
- Nhãn trên sơ đồ giữ tiếng Anh theo quy ước CLAUDE.md #4; phần chú giải/ghi chú ngắn bằng tiếng Việt.
- Nguồn: SRS v3.0 Mục III, XV; `Update/KE_HOACH_CAU_TRUC_DU_AN.md` (mục 3, 3b); `CI-CD/MO_TA_CI_CD_VA_DIEM_CHAN.md`; DECISIONS_LOG #13, #48, #50, #51, #65, #70, #71, #74, #122; `backend/backend/src/app.module.ts`.

## 1. Quy ước ký pháp đã áp dụng
| PDF | Trong bản vẽ |
|---|---|
| Component `<<component>>` + icon góc phải trên; `<<subsystem>>` | Mọi module là component; Frontend và Backend là `<<subsystem>>` |
| Provided (ball) / Required (socket) | Ball-and-socket: MailPort, LlmProviderPort, ItemRepository, CATEngine, ExamRoundRepository, LanguageProfile, HTTPS, REST, SQL, RESP, SMTP |
| Port + delegation connector | Cổng "Web UI" và "REST /api/v1"; delegation vào 3 nhóm module |
| Node cube `<<device>>`/`<<executionEnvironment>>`, `name:type` | Server, Docker, 6 container, GitHub, GHCR… |
| `<<artifact>>`, `<<deployment spec>>`, `<<deploy>>` | image, migrations, nginx.conf, .env, compose; mũi tên `<<deploy>>` từ GitHub Actions và `<<pull image>>` |

## 2. Component Diagram — các thành phần
- **Ngoài hệ thống:** Web Browser, EduZ (M2M, API Key), SMTP, Gemini, Fallback LLM (đề xuất, nét đứt).
- **Nginx API Gateway** → Frontend (Web UI) và Backend (REST).
- **Frontend (Next.js):** UI Pages, BFF Route Handlers (cookie httpOnly, #50), API Client (kiểu từ OpenAPI, #51), `@apt/shared-types` (#122).
- **Backend (NestJS), 13 module khớp `app.module.ts`**, gom 3 nhóm:
  - Identity & Administration: auth, user-admin, user-import, mail.
  - Question Bank & AI: item-generation, llm-gateway, item-bank.
  - Exam, Assessment & Results: exam-round, test-session, cat-engine, language-profile, reporting, ai-explainer.
- **Infrastructure adapters:** PrismaModule, Redis Client, BullMQ.
- **Dữ liệu:** PostgreSQL 16, Redis 7; IRT Calibration (py-irt/catR) offline, nét đứt (thuộc KL/F-12).

## 3. Deployment Diagram — các node
- Client Device/Web Browser; EduZ Server (ngoài).
- **staging : Linux Server** (dùng chung, cổng 8443) chứa Docker Compose với 6 container: nginx, frontend, backend, postgres, redis, vector; kèm `farmnongviet` (xám, không được đụng, #71).
- Đường phát hành: Developer Workstation → GitHub Actions → GHCR → SSH `deploy.sh` → server (`<<deploy>>`, `<<pull image>>`).
- Ngoài: Gemini, SMTP (chưa chọn, Q-5), Better Stack (ping health + log), DNS BKNS.

## 4. Quyết định trình bày tôi đã tự chọn (đảo lại được, vui lòng xác nhận)
1. Xuất ra file draw.io riêng, **không sửa** `TLCN.drawio.xml` (đang là Class Diagram).
2. Interface lấy tên có sẵn trong tài liệu/mã; kết nối DB/Redis/queue vẽ gộp theo nhóm module (3 mũi tên) thay vì 13 đường.
3. Ai-explainer xếp ở nhóm "Exam, Assessment & Results" (phục vụ trang kết quả); đây là cách gom của tôi, SRS không quy định nhóm.
4. Deployment vẽ **staging** (môi trường duy nhất theo #65), không vẽ production.

## 5. Điểm chưa khớp / chưa xác minh (nợ đồng bộ)
- Topology staging là **thiết kế**: theo CI-CD ngày 10/10, container chưa khởi động, mã chưa đẩy GitHub; chưa thấy compose/nginx/deploy.sh trong thư mục dự án để đối chiếu (chỉ có `frontend/Dockerfile`).
- `ai-explainer` trong mã có `gemini-flash.provider` riêng, thiết kế đích gọi qua llm-gateway.
- `bullmq`, `nodemailer` chưa có trong `package.json` backend.
- Luật định tuyến Nginx (đường nào vào frontend/backend) chưa được tài liệu chốt.
- SRS 15.1 nhắm 2 instance NestJS; staging chạy 1.
- Mailpit chỉ ở môi trường dev, không vẽ trên staging.
- Chưa đưa vào `docs-repo/design/`, SRS (mục III có ghi "sơ đồ thành phần/triển khai để bổ sung sau"), `DECISIONS_LOG`, weekly-log. Cần khi bạn xác nhận.

## 6. Cập nhật 24/10/2026 (nhận xét của Đăng đã đối chiếu; chốt #123)
| Điểm | Kết luận | Việc còn lại |
|---|---|---|
| Worker BullMQ chạy cùng tiến trình backend | **Chốt: giữ chung tiến trình** (staging 1 container, server 2 GB). Rủi ro: tác vụ nặng (sinh đề AI, kiểm C1–C3) chiếm CPU và có thể làm trễ API làm bài (NFR < 300 ms). Giảm thiểu: giới hạn số job đồng thời của queue, tác vụ AI chủ yếu chờ I/O; theo dõi độ trễ bằng Better Stack | Sau khi có dữ liệu đo, xét tách container worker |
| Số instance backend | **Chốt:** SRS 15.1 ghi 2 instance là mục tiêu **production**; staging chạy 1 | Sơ đồ Deployment đã đúng (staging); thêm chú thích |
| Thiếu khối Health Probe | Cần thêm `HealthController` (`@nestjs/terminus`) nhóm Infrastructure; endpoint `/api/v1/health` và `/api/v1/ready`. Mã backend hiện không còn module `health` và chưa có `@nestjs/terminus` | Vẽ thêm khối vào sơ đồ; cài thư viện và viết module |
| Đường kiểm tra uptime | Better Stack ping **cả** `/api/health` (BFF frontend) **và** `/api/v1/health`, `/api/v1/ready` (backend); Nginx phải chuyển tiếp `/api/v1/*` tới backend | Ghi vào cấu hình Nginx khi có; vẽ mũi tên thứ hai trên sơ đồ |
| `prisma/migrations` trống | Đúng; artifact "migrations" trong sơ đồ là **kế hoạch**, chưa có migration đầu (điểm chặn Q1 của CI/CD) | Sinh migration đầu bằng `prisma migrate` sau khi chốt schema |
| `ai-explainer` gọi thẳng Gemini; `bullmq`, `nodemailer`, `@nestjs/terminus` chưa cài | Nợ đã ghi ở mục 5 | Sửa mã theo thiết kế |
