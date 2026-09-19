---
title: "Overview"
order: 2
dd_id: "logout"
api_name: "auth.view.logout"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `logout` |
| Source runtime handler/use-case | auth.view.logout |
| Module | Auth |
| Method | `POST` |
| Endpoint | `/api/v1/auth/logout` |
| Purpose | Return stateless logout success without server-side session mutation. |
| Consumer/Actor | Authenticated student or business |
| Authentication | Yes |
| Authorization | Any valid JWT role |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | N/A |
| Side effects | N/A |

## Sources

- [apps/work-server/src/modules/auth/routes.ts](../../../src/modules/auth/routes.ts).
- [apps/work-server/src/modules/auth/view.ts](../../../src/modules/auth/view.ts).
- [apps/work-server/src/middleware/auth.middleware.ts](../../../src/middleware/auth.middleware.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).

## Tables read

- N/A — no Prisma table read.

## Tables write

- N/A — no persistent table write.

## Mục chú ý

- JWT is stateless; route does not revoke token or write DB.
- Missing/invalid Bearer is typed UNAUTHORIZED.

## Assumptions

- N/A — documentation records current source behavior; it does not add a target-domain rule.

## Conflicts

- Target-only operations in `contracts/openapi/work/openapi.json` are excluded because they are not registered in the current router.

## Security note

- Password/hash fields are used only for authentication/storage and are excluded from public projections.

## Performance note

- Query shape, order and pagination are documented exactly from the current Prisma query functions.


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
