---
title: "Overview"
order: 2
dd_id: "registerStudent"
api_name: "students.view.registerStudent"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `registerStudent` |
| Source runtime handler/use-case | students.view.registerStudent |
| Module | Student |
| Method | `POST` |
| Endpoint | `/api/v1/students` |
| Purpose | Create a student account and return the public student projection. |
| Consumer/Actor | Unauthenticated student client |
| Authentication | No |
| Authorization | Public registration endpoint |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | N/A — one Prisma create operation; password hashing occurs before insert. |
| Side effects | Creates SinhVien row with hashed matkhau. |

## Sources

- [apps/work-server/src/modules/students/routes.ts](../../../src/modules/students/routes.ts).
- [apps/work-server/src/modules/students/models.ts](../../../src/modules/students/models.ts).
- [apps/work-server/src/modules/students/validate.ts](../../../src/modules/students/validate.ts).
- [apps/work-server/src/modules/students/view.ts](../../../src/modules/students/view.ts).
- [apps/work-server/src/modules/students/query.ts](../../../src/modules/students/query.ts).
- [apps/work-server/src/core/security/password.ts](../../../src/core/security/password.ts).
- [apps/work-server/src/services/public-selectors.ts](../../../src/services/public-selectors.ts).
- [apps/work-server/src/config/multer.ts](../../../src/config/multer.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).
- [apps/work-server/prisma/schema.prisma](../../../prisma/schema.prisma).

## Tables read

- N/A — no Prisma table read.

## Tables write

- SinhVien.

## Mục chú ý

- matkhau is hashed with bcrypt cost 12 before insert.
- Public select excludes matkhau.
- Unique email P2002 maps to STUDENT_CREATE_FAILED.

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
