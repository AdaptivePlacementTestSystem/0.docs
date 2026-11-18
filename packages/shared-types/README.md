# @apt/shared-types

Enum, mã lỗi (`ErrorCode`) và kiểu nền (`ApiError`) dùng chung BE/FE — mô hình C, Quyết định #122. DTO request/response sinh từ OpenAPI, không đặt ở đây.

## Dùng
1. Đặt thư mục này tại `<gốc dự án>/packages/shared-types`.
2. `cd packages/shared-types && npm install && npm run build` (ra `dist/`).
3. BE (`backend/backend`): `"@apt/shared-types": "file:../../packages/shared-types"`; FE (`frontend`): `"file:../packages/shared-types"`; rồi `npm install` ở mỗi bên.
4. FE cần `turbopack.root` và `outputFileTracingRoot` trỏ lên thư mục cha trong `next.config.ts`.

Chi tiết: `tracking/feature-plans/shared-types.md`, `work/week-05/PHAN_TICH_SHARED_TYPES_DTO_ENUM_VA_GIAI_PHAP.md`.
