---
title: "Overview"
order: 2
dd_id: "loginBusiness"
api_name: "Business login"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `loginBusiness` |
| Module | Work API |
| Method | `POST` |
| Endpoint | `/api/v1/auth/business/login` |
| Purpose | Đăng nhập doanh nghiệp và phát hành JWT Bearer token. |
| Consumer/Actor | Work Web client |
| Authentication | Không bắt buộc; middleware chỉ parse token nếu có |
| Authorization | N/A — public route |
| Basis | DIRECT — current registered route |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — không có DB mutation |
| Side effects | N/A |

## Sources

- `apps/work-server/src/routes/api_routes.ts`.
- `apps/work-server/src/services/*.ts` — service được route import.
- `apps/work-server/src/middleware/auth.middleware.ts` và `src/config/multer.ts` nếu áp dụng.
- `apps/work-server/prisma/schema.prisma` và checked-in migrations.
- `contracts/openapi/work/legacy-web.openapi.json` — operationId/consumer cross-check.
- `apps/work-client/web/src/shared/api/work.ts` — actual consumer call.

## Tables read

- `DoanhNghiep`.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- Source chuẩn hóa `password`; vẫn nhận alias legacy `matkhau` khi `password` không có.
- Service verify bcrypt và fallback plaintext legacy; login legacy thành công sẽ best-effort rehash.

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
