---
title: "Overview"
order: 2
dd_id: "registerStudent"
api_name: "Register student"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `registerStudent` |
| Module | Work API |
| Method | `POST` |
| Endpoint | `/api/v1/students` |
| Purpose | Tạo tài khoản sinh viên mới bằng multipart form và ảnh tùy chọn. |
| Consumer/Actor | Work Web client |
| Authentication | Không bắt buộc; middleware chỉ parse token nếu có |
| Authorization | N/A — public route |
| Basis | DIRECT — current registered route |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — source gọi một Prisma mutation, không mở transaction explicit |
| Side effects | SinhVien |

## Sources

- `apps/work-server/src/routes/api_routes.ts`.
- `apps/work-server/src/services/*.ts` — service được route import.
- `apps/work-server/src/middleware/auth.middleware.ts` và `src/config/multer.ts` nếu áp dụng.
- `apps/work-server/prisma/schema.prisma` và checked-in migrations.
- `contracts/openapi/work/legacy-web.openapi.json` — operationId/consumer cross-check.
- `apps/work-client/web/src/shared/api/work.ts` — actual consumer call.

## Tables read

- `SinhVien`.

## Tables write

- `SinhVien`.

## Mục chú ý

- Legacy OpenAPI gọi email format email nhưng source route không validate format..
- Không ghi giá trị mật khẩu thực vào DD..

## Assumptions

- Reviewer/approver chưa được cung cấp; đây là metadata tài liệu, không phải API behavior.

## Conflicts

- Contract/source drift được liệt kê tại `../../OPEN_QUESTIONS.md` và không được silently reconcile.

## Security note

- Không ghi literal credential, JWT secret hoặc token. Public projection loại password/hash khỏi mọi response.

## Performance note

- Ghi đúng query hiện tại; không suy diễn index, pagination DB hoặc caching ngoài source.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
