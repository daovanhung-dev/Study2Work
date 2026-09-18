---
title: "Data Mapping"
order: 5
dd_id: "getMyCv"
api_name: "cv.view.getMyCv"
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
| 1 | header | Authorization | Bearer <JWT HS256> | Token được parse bởi authenticateToken; protected route gọi ensureAuthenticated/checkRole. | [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts) |
| 2 | header | X-Trace-Id | UUID hợp lệ; invalid/missing sẽ được generate | Trace ID được echo ở header và body. | [apps/work-server/src/core/middleware.ts](../../../src/core/middleware.ts) |

## Query Matrix

| No | Operation | Table/model | Columns/select | Where | Sort/pagination | Include/relation | Transaction |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | findStudentCv | Cv | all Cv columns | sinhvien_id = BigInt(token.id) | first row | N/A | N/A |

## Mutation Matrix

N/A — route has no persistent mutation.

## Response Source Matrix

| No | Field | Kind | Source/transform | Mapping source |
| ---: | --- | --- | --- | --- |
| 1 | id | data field | Raw Cv Prisma field. | cv view/query |
| 2 | avt | data field | Raw Cv Prisma field. | cv view/query |
| 3 | hoten | data field | Raw Cv Prisma field. | cv view/query |
| 4 | ngaysinh | data field | Raw Cv Prisma field. | cv view/query |
| 5 | gioitinh | data field | Raw Cv Prisma field. | cv view/query |
| 6 | email | data field | Raw Cv Prisma field. | cv view/query |
| 7 | sdt | data field | Raw Cv Prisma field. | cv view/query |
| 8 | diachi | data field | Raw Cv Prisma field. | cv view/query |
| 9 | vitri | data field | Raw Cv Prisma field. | cv view/query |
| 10 | nganh | data field | Raw Cv Prisma field. | cv view/query |
| 11 | muctieunghiep | data field | Raw Cv Prisma field. | cv view/query |
| 12 | hocvan | data field | Raw Cv Prisma field. | cv view/query |
| 13 | kinhnghiem | data field | Raw Cv Prisma field. | cv view/query |
| 14 | kynang | data field | Raw Cv Prisma field. | cv view/query |
| 15 | ngoaingu | data field | Raw Cv Prisma field. | cv view/query |
| 16 | chungchi | data field | Raw Cv Prisma field. | cv view/query |
| 17 | duan | data field | Raw Cv Prisma field. | cv view/query |
| 18 | giaithuong | data field | Raw Cv Prisma field. | cv view/query |
| 19 | hoatdong | data field | Raw Cv Prisma field. | cv view/query |
| 20 | social | data field | Raw Cv Prisma field. | cv view/query |
| 21 | portfolio | data field | Raw Cv Prisma field. | cv view/query |
| 22 | luongmongmuon | data field | Raw Cv Prisma field. | cv view/query |
| 23 | created_at | data field | Raw Cv Prisma field. | cv view/query |
| 24 | sinhvien_id | data field | Raw Cv Prisma field. | cv view/query |

## Validation and branch rules

- checkRole('student') executes before route.
- findStudentCv filters Cv.sinhvien_id by token id.
- Missing CV throws CV_NOT_FOUND.


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
