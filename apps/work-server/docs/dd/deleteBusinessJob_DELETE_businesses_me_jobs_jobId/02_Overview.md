---
title: "Overview"
order: 2
dd_id: "deleteBusinessJob"
api_name: "jobs.view.deleteBusinessJob"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `deleteBusinessJob` |
| Source runtime handler/use-case | jobs.view.deleteBusinessJob |
| Module | Business Jobs |
| Method | `DELETE` |
| Endpoint | `/api/v1/businesses/me/jobs/:jobId` |
| Purpose | Delete an owned JD and return its numeric id. |
| Consumer/Actor | Authenticated business |
| Authentication | Yes |
| Authorization | Valid Bearer JWT with role=business and owned JD |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | Prisma $transaction checks ownership then deletes JD. |
| Side effects | Deletes JD row. |

## Sources

- [apps/work-server/src/modules/jobs/routes.ts](../../../src/modules/jobs/routes.ts).
- [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts).
- [apps/work-server/src/modules/jobs/validate.ts](../../../src/modules/jobs/validate.ts).
- [apps/work-server/src/modules/jobs/view.ts](../../../src/modules/jobs/view.ts).
- [apps/work-server/src/modules/jobs/query.ts](../../../src/modules/jobs/query.ts).
- [apps/work-server/src/middleware/auth.middleware.ts](../../../src/middleware/auth.middleware.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).
- [apps/work-server/prisma/schema.prisma](../../../prisma/schema.prisma).

## Tables read

- JD.

## Tables write

- JD.

## Mục chú ý

- No request body.
- Ownership check prevents deleting another business's JD.

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
