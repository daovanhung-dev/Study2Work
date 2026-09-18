---
title: "Overview"
order: 2
dd_id: "getBusinessApplications"
api_name: "applications.view.getBusinessApplications"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `getBusinessApplications` |
| Source runtime handler/use-case | applications.view.getBusinessApplications |
| Module | Applications |
| Method | `GET` |
| Endpoint | `/api/v1/businesses/me/applications` |
| Purpose | List applicants for jobs associated with the authenticated business. |
| Consumer/Actor | Authenticated business |
| Authentication | Yes |
| Authorization | Valid Bearer JWT with role=business |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | N/A |
| Side effects | N/A |

## Sources

- [apps/work-server/src/modules/applications/routes.ts](../../../src/modules/applications/routes.ts).
- [apps/work-server/src/modules/applications/models.ts](../../../src/modules/applications/models.ts).
- [apps/work-server/src/modules/applications/validate.ts](../../../src/modules/applications/validate.ts).
- [apps/work-server/src/modules/applications/view.ts](../../../src/modules/applications/view.ts).
- [apps/work-server/src/modules/applications/query.ts](../../../src/modules/applications/query.ts).
- [apps/work-server/src/services/public-selectors.ts](../../../src/services/public-selectors.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).
- [apps/work-server/src/middleware/auth.middleware.ts](../../../src/middleware/auth.middleware.ts).
- [apps/work-server/prisma/schema.prisma](../../../prisma/schema.prisma).

## Tables read

- UngVien.
- SinhVien.
- JD.

## Tables write

- N/A — no persistent table write.

## Mục chú ý

- Filters UngVien.doanhnghiep_id by token id.
- Includes public student and public job projections.

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
