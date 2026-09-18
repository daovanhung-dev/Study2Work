---
title: "Data Mapping"
order: 5
dd_id: "loginBusiness"
api_name: "auth.view.loginBusiness"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
status: "Draft — Ready for Review"
---
# Data Mapping

## Execution flow

1. `traceMiddleware` accepts a valid `X-Trace-Id` or generates a UUID.
2. `express.json`/Multer parses the request according to the route transport.
3. Auth middleware optionally decodes Bearer JWT; protected route middleware enforces authentication and role.
4. Route parses model and calls the module view/use-case.
5. View validates, applies business rule and calls query/repository functions.
6. Prisma result is mapped through the success envelope; errors go to centralized exception mapping.

## Request Usage Matrix

| No | Location | Name | Rule | Use | Source |
| ---: | --- | --- | --- | --- | --- |
| 1 | header | X-Trace-Id | UUID hợp lệ; invalid/missing sẽ được generate | Trace ID được echo ở header và body. | [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts) |
| 2 | body | email | trim(); valid email format | Email used to find credentials. | [apps/work-server/src/modules/auth/models.ts](../../../src/modules/auth/models.ts) |
| 3 | body | password | min length 1; at least password or matkhau must be present | Canonical login password. | [apps/work-server/src/modules/auth/models.ts](../../../src/modules/auth/models.ts) |
| 4 | body | matkhau | min length 1; used when password is omitted | Legacy login compatibility alias. | [apps/work-server/src/modules/auth/models.ts](../../../src/modules/auth/models.ts) |

## Query Matrix

| No | Operation | Table/model | Columns/select | Where | Sort/pagination | Include/relation | Transaction |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | findBusinessCredentials | DoanhNghiep | id, email, matkhau | email = input.email | N/A | N/A | N/A |

## Mutation Matrix

| No | Operation | Table/model | Condition | Fields | Value source | Transaction | Failure behavior |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | rehash password | DoanhNghiep | credentials found and verifyPassword.needsRehash | matkhau | hashPassword(password), bcrypt cost 12 | No explicit transaction; failure is swallowed best-effort. | Login still returns success if rehash update fails. |

## Response Source Matrix

| No | Field | Kind | Source/transform | Mapping source |
| ---: | --- | --- | --- | --- |
| 1 | token | data field | HS256 JWT signed by signAccessToken; example is synthetic. | auth view authenticate and core security |
| 2 | user.id | data field | Number(credentials.id). | auth view authenticate and core security |
| 3 | user.email | data field | credentials.email or empty string. | auth view authenticate and core security |
| 4 | user.role | data field | Literal `business`. | auth view authenticate and core security |

## Validation and branch rules

- Parse loginRequestSchema.
- Use loginPassword to select password then matkhau alias.
- Query findBusinessCredentials by email selecting id/email/matkhau.
- verifyPassword supports bcrypt and legacy plaintext fallback.
- Best-effort rehash stores bcrypt hash when legacy plaintext verification succeeds.
- signAccessToken returns token and view returns AUTH_LOGIN_SUCCESS.


---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
