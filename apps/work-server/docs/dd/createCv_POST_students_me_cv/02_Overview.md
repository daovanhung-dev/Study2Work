---
title: "Overview"
order: 2
dd_id: "createCv"
api_name: "cv.view.createCv"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `createCv` |
| Source runtime handler/use-case | cv.view.createCv |
| Module | CV |
| Method | `POST` |
| Endpoint | `/api/v1/students/me/cv` |
| Purpose | Create the single CV record for the authenticated student. |
| Consumer/Actor | Authenticated student |
| Authentication | Yes |
| Authorization | Valid Bearer JWT with role=student |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | Prisma $transaction checks count then inserts Cv. |
| Side effects | Creates Cv row; unique sinhvien_id prevents duplicate CV. |

## Sources

- [apps/work-server/src/modules/cv/routes.ts](../../../src/modules/cv/routes.ts).
- [apps/work-server/src/modules/cv/models.ts](../../../src/modules/cv/models.ts).
- [apps/work-server/src/modules/cv/validate.ts](../../../src/modules/cv/validate.ts).
- [apps/work-server/src/modules/cv/view.ts](../../../src/modules/cv/view.ts).
- [apps/work-server/src/modules/cv/query.ts](../../../src/modules/cv/query.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).
- [apps/work-server/src/middleware/auth.middleware.ts](../../../src/middleware/auth.middleware.ts).
- [apps/work-server/src/config/multer.ts](../../../src/config/multer.ts).
- [apps/work-server/prisma/schema.prisma](../../../prisma/schema.prisma).

## Tables read

- Cv.

## Tables write

- Cv.

## Mục chú ý

- Create requires hoten and email.
- social string is JSON.parsed when non-empty; parse failure stores raw string and may fail at Prisma Json validation.
- avt is stored as Multer filename, not `/uploads/` path for CV.

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
