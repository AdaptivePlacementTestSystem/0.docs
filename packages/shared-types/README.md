# @apt/shared-types

> **Lưu ý nguồn chính thức (28/11/2026):** Thư mục này trong `0.docs` chỉ là **bản tham chiếu đồng bộ** (đã cập nhật tới `v3.1.0`). Nguồn mã nguồn độc lập chính thức dùng để build và phát hành cho BE/FE nằm tại repo `AdaptivePlacementTestSystem/shared-types`.

Enum, mã lỗi (`ErrorCode`) và kiểu nền (`ApiError`) dùng chung BE/FE — mô hình C, Quyết định #122. DTO request/response sinh từ OpenAPI, không đặt ở đây.

## Dùng
1. Đặt thư mục này tại `<gốc dự án>/packages/shared-types`.
2. `cd packages/shared-types && npm install && npm run build` (ra `dist/`).
3. BE (`backend/backend`): `"@apt/shared-types": "file:../../packages/shared-types"`; FE (`frontend`): `"file:../packages/shared-types"`; rồi `npm install` ở mỗi bên.
4. FE cần `turbopack.root` và `outputFileTracingRoot` trỏ lên thư mục cha trong `next.config.ts`.

Chi tiết: `tracking/feature-plans/shared-types.md`, `work/week-05/PHAN_TICH_SHARED_TYPES_DTO_ENUM_VA_GIAI_PHAP.md`.
