# Kế hoạch sửa lỗi module `auth` (nhánh `feat/auth-module`)

- **Trạng thái:** BẢN NHÁP. Các quyết định D1–D7 đã chốt ngày 09/11/2026; kế hoạch chưa được duyệt để chuyển sang `plans/` (quy tắc 7 của CLAUDE.md).
- **Căn cứ:** đọc mã nguồn commit `b972977` (repo `AdaptivePlacementTestSystem/backend`, nhánh `feat/auth-module`, ngày 09/11/2026). Chưa chạy `npm test`/`build` nên mọi nhận định dưới đây dựa trên đọc mã.
- **Phạm vi:** `src/modules/auth/**`, `src/modules/mail/**`, `src/shared/guards/**`, `src/config/**`.

## 1. Hiện trạng đã xác minh trong mã

| # | Sự thật trong mã | Vị trí |
|---|---|---|
| H1 | `JwtStrategy.validate` chỉ trả `{sub, email, role}` từ payload, không truy vấn DB, không kiểm tra `isActive` hay `passwordChangedAt` | `infrastructure/providers/jwt.strategy.ts` |
| H2 | JWT payload chỉ có `sub, email, role`; không có cờ `mustChangePassword`; không guard nào chặn người dùng còn cờ này | `jwt.provider.ts`, `shared/guards/*` |
| H3 | Chưa có `@nestjs/throttler`; `login` và `forgot-password` không giới hạn tần suất | `package.json`, `auth.controller.ts` |
| H4 | `incrementAttempts` đọc rồi ghi lại cả JSON (get → set), không atomic; `reset-password` kiểm tra `attempts >= 5` trước khi so khớp; so hash bằng `!==` | `redis-otp-cache.service.ts`, `reset-password.use-case.ts` |
| H5 | `forgot-password` trả 202 (`@HttpCode(ACCEPTED)`), nhưng `saveOtp` (Redis) không bọc try/catch; Redis lỗi thì ném lỗi, trong khi nhánh email không tồn tại không chạm Redis, nên phản hồi khác nhau, lộ thông tin | `forgot-password.use-case.ts` |
| H6 | `ChangePasswordUseCase`, `ResetPasswordUseCase`, `AuthController` inject thẳng `PrismaService`, bỏ qua `IUserRepository` | các file tương ứng |
| H7 | `RedisOtpCacheService` khai báo hai lần trong `providers` (token chuỗi và class); mỗi service tự mở một kết nối ioredis | `auth.module.ts` |
| H8 | `LoginDto` có `MinLength(6)`; `ChangePasswordDto` và `ResetPasswordDto` có `MinLength(8)` | các DTO |
| H9 | `reset-password` không kiểm tra `isActive`; template email nhúng `fullName` không escape; `sendMail` nuốt lỗi và trả `false`, gửi đồng bộ trong request | `reset-password.use-case.ts`, `smtp-mail.adapter.ts` |
| H10 | Chưa có test cho `login`, `verify-token`; `@types/ioredis` v4 cùng `ioredis ^6.0.0`; `JwtStrategy.validate(payload: any)`, `expiresIn ... as any` | `package.json`, mã |

## 2. Quyết định đã chốt (ngày 09/11/2026, ghi tại `DECISIONS_LOG.md` #134; bổ sung sau rà soát chéo: #135)

| Mã | Quyết định | Ghi chú thực hiện |
|---|---|---|
| D1 | Ép đổi mật khẩu: guard đọc DB/cache mỗi request | Không đổi payload JWT; cache Redis TTL ngắn, giá trị cấu hình qua env |
| D2 | Vô hiệu token: `validate()` đọc DB/cache, kiểm `isActive` và so `iat` với `passwordChangedAt` | Không đổi schema; dùng chung một lần đọc người dùng với D1 |
| D3 | Rate-limit lưu ở Redis; `login` 5 lần/phút theo (IP + email), `forgot-password` 3 lần/giờ theo email | Ngưỡng cấu hình qua env; cần kiểm tra gói lưu trữ Redis cho `@nestjs/throttler` có tương thích phiên bản đang dùng không |
| D4 | Mật khẩu tối thiểu 8 ký tự, bắt buộc chữ thường, chữ Hoa, số và ký tự đặc biệt | Vượt đề xuất SRS (chỉ nêu độ dài 8, Q-4). Áp dụng cho đổi và đặt lại mật khẩu; `LoginDto` bỏ ràng buộc độ dài/độ phức tạp. Mật khẩu tạm 12 ký tự phải sinh đủ 4 nhóm. Cần đồng bộ SRS/BR |
| D5 | `forgot-password` luôn 202, lỗi Redis/SMTP chỉ log | Giữ BR-14 |
| D6 | Gửi mail ngay trong request + try/catch | BullMQ hoãn sang đợt riêng, ghi vào `TECH_DEBT.md`; bắt buộc có trước khi làm import hàng loạt (gửi mật khẩu tạm) |
| D7 | Chỉ thêm `updatePassword` vào `IUserRepository` và vá provider Redis khai báo trùng | `GetProfileUseCase` và `RedisModule` dùng chung để đợt sau |

### Nợ đồng bộ tài liệu phát sinh
- SRS (Q-4) và BR liên quan: quy tắc mật khẩu 4 nhóm ký tự.
- SD_08 và đặc tả UC đổi/quên mật khẩu: nếu mô tả quy tắc mật khẩu.
- Quy ước sinh mật khẩu tạm (12 ký tự) phải đủ 4 nhóm.

## 3. Các giai đoạn thực hiện

### Giai đoạn 1 — Bảo mật (ưu tiên cao)
1. **Ép đổi mật khẩu lần đầu (H2, D1).** Thêm `MustChangePasswordGuard` chạy sau `JwtAuthGuard`, đọc cờ từ DB/cache; khi cờ bật chỉ cho qua `POST /auth/change-password` và `GET /auth/me`. Test: cờ bật gọi API khác → 403; đổi mật khẩu xong → 200.
2. **Vô hiệu token cũ (H1, D2).** Kiểm tra `isActive` và `passwordChangedAt` trong luồng xác thực. Test: đổi mật khẩu rồi dùng token cũ → 401; Admin khóa tài khoản → bị chặn.
3. **OTP atomic (H4).** Tách bộ đếm sang key riêng dùng `INCR` + `EXPIRE` (hoặc Lua script); kiểm tra giới hạn sau khi tăng; so hash bằng `crypto.timingSafeEqual`. Test: 20 request song song sai OTP → tối đa 5 lần được xử lý.
4. **Rate-limit (H3, D3).** Cài `@nestjs/throttler` với lưu trữ Redis; `login` 5/phút theo (IP + email), `forgot-password` 3/giờ theo email, ngưỡng qua env. Test e2e: vượt ngưỡng → 429.

### Giai đoạn 2 — Độ bền và nhất quán
5. **`forgot-password` đồng nhất (H5, D5).** Bọc toàn bộ nhánh Redis/SMTP trong try/catch, luôn trả 202, chỉ log lỗi.
6. **Chính sách mật khẩu (H8, D4).** Một decorator/hằng số dùng chung: tối thiểu 8, đủ chữ thường, chữ Hoa, số, ký tự đặc biệt, áp cho đổi và đặt lại; bỏ ràng buộc ở `LoginDto`; sửa bộ sinh mật khẩu tạm; thêm test cho từng nhóm ký tự.
7. **Tài khoản khóa và email (H9).** `reset-password` từ chối `isActive=false`; escape `fullName`/`email` trong template; tắt log OTP khi `NODE_ENV=production`; `sendMail` ném lỗi (không nuốt), use-case bắt và log (D6, gửi ngay trong request); ghi BullMQ vào `TECH_DEBT.md`.

### Giai đoạn 3 — Kiến trúc (H6, H7, H10, D7: phạm vi tối thiểu)
8. Thêm `updatePassword(userId, hash, {mustChangePassword})` vào `IUserRepository`; bỏ `PrismaService` khỏi `ChangePasswordUseCase` và `ResetPasswordUseCase` (`AuthController.getProfile` vẫn dùng Prisma, hoãn theo D7).
9. Sửa provider `RedisOtpCacheService` khai báo trùng bằng `useExisting` (H7).
10. Gỡ `@types/ioredis`; thay `any` ở `JwtStrategy` và `expiresIn` bằng kiểu rõ ràng.

### Giai đoạn 4 — Kiểm thử và tài liệu
11. Bổ sung spec cho `login`, `verify-token`, guard mới, bộ đếm OTP, rate-limit.
12. Chạy `npm run lint`, `npm test`, `npm run build`; chỉ ghi kết quả đo thật vào báo cáo.
13. Đồng bộ SRS, SD_08, Class Diagram theo mục nợ đồng bộ ở phần 2; ghi weekly-log và `AI_USAGE_LOG.md`.

## 4. Thứ tự và phụ thuộc
Giai đoạn 1 (1 → 2 → 3 → 4) → Giai đoạn 2 → Giai đoạn 3 → Giai đoạn 4. Giai đoạn 1 xong và có test trước khi merge nhánh. Không có ước lượng thời gian vì chưa đo.

## 5. Quy trình
- Làm trên nhánh con của `feat/auth-module`; không push/tạo PR khi chưa được yêu cầu rõ.
- Trước khi code tạo `0.docs/tracking/feature-plans/auth-hardening.md` từ `_template.md`.
- Ghi `AI_USAGE_LOG.md` sau mỗi lần AI sinh/sửa mã.

## 6. Việc để đợt sau
`GetProfileUseCase`; `RedisModule` dùng chung; BullMQ cho email (bắt buộc trước import hàng loạt).

## 7. Tiến độ thực hiện (cập nhật 10/11/2026)
- **Đã làm và đã push** lên `feat/auth-module` của repo backend: `86591d7` (giai đoạn 1–3 theo D1–D7) và `c12c98c` (bổ sung #135: trust proxy qua env, giới hạn đăng nhập theo IP chỉ đếm lần thất bại, giới hạn reset-password, đảo thứ tự kiểm tra khóa kèm verify giả).
- **Kết quả đo:** vitest 76/76, typecheck, lint, build sạch. Chưa chạy với Redis/Postgres thật và chưa thử sau Nginx.
- **Chưa làm:** đồng bộ SRS/BR/SD_08 (mục nợ đồng bộ ở phần 2); cache cho `JwtStrategy`; BullMQ cho email; `GetProfileUseCase` và `RedisModule` dùng chung; xác nhận rate-limit fail-open hay fail-closed.
