---
title: "Overview"
order: 2
dd_id: "loginBusiness"
api_name: "auth.view.loginBusiness"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---
# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `loginBusiness` |
| Source runtime handler/use-case | auth.view.loginBusiness |
| Module | Auth |
| Method | `POST` |
| Endpoint | `/api/v1/auth/business/login` |
| Purpose | Authenticate a business account and issue a stateless JWT. |
| Consumer/Actor | Business client |
| Authentication | No |
| Authorization | Public login endpoint |
| Basis | DIRECT — current registered route |
| Status | Draft — Ready for Review |
| Transaction | N/A for lookup; best-effort password rehash performs a conditional update outside an explicit transaction. |
| Side effects | Conditional legacy plaintext-to-bcrypt rehash after successful login. |

## Sources

- [apps/work-server/src/modules/auth/routes.ts](../../../src/modules/auth/routes.ts).
- [apps/work-server/src/modules/auth/models.ts](../../../src/modules/auth/models.ts).
- [apps/work-server/src/modules/auth/validate.ts](../../../src/modules/auth/validate.ts).
- [apps/work-server/src/modules/auth/view.ts](../../../src/modules/auth/view.ts).
- [apps/work-server/src/modules/auth/query.ts](../../../src/modules/auth/query.ts).
- [apps/work-server/src/core/security/password.ts](../../../src/core/security/password.ts).
- [apps/work-server/src/core/security/access-token.ts](../../../src/core/security/access-token.ts).
- [apps/work-server/src/core/responses.ts](../../../src/core/responses.ts).
- [apps/work-server/src/core/exceptions.ts](../../../src/core/exceptions.ts).
- [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts).
- [apps/work-server/prisma/schema.prisma](../../../prisma/schema.prisma).

## Tables read

- DoanhNghiep.

## Tables write

- DoanhNghiep.

## Mục chú ý

- `password` is canonical; `matkhau` is accepted when password is omitted.
- Bcrypt cost is 12 for new hash/rehash.
- JWT claims are id/email/role; algorithm is HS256.
- Password/hash is never returned.

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
