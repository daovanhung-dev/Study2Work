---
title: "Data Mapping"
order: 5
dd_id: "createBusinessJob"
api_name: "jobs.view.createBusinessJob"
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
| 3 | body | ten_vi_tri | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 4 | body | phong_ban | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 5 | body | cap_bac | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 6 | body | bao_cao_cho | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 7 | body | nhiem_vu | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 8 | body | trinh_do | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 9 | body | kinh_nghiem | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 10 | body | ky_nang | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 11 | body | ky_nang_mem | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 12 | body | uu_tien | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 13 | body | muc_luong | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 14 | body | phuc_loi | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 15 | body | moi_truong | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 16 | body | dia_diem | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 17 | body | thoi_gian | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 18 | body | han_nop | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 19 | body | cach_ung_tuyen | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 20 | body | mo_ta | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 21 | body | ten_cong_ty | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 22 | body | nganh | trim() when present; unknown fields pass Zod but are ignored by normalizeJobData | JD mutation field. | [apps/work-server/src/modules/jobs/models.ts](../../../src/modules/jobs/models.ts) |
| 23 | file | avt | Multer filter/limit | Filename is passed to normalize function. | [apps/work-server/src/config/multer.ts](../../../src/config/multer.ts) |

## Query Matrix

| No | Operation | Table/model | Columns/select | Where | Sort/pagination | Include/relation | Transaction |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | requireBusiness | DoanhNghiep | businessPublicSelect | id = token.id | N/A | N/A | inside transaction |
| 2 | insertJob | JD | jobPublicSelect | N/A | N/A | N/A | inside transaction |

## Mutation Matrix

| No | Operation | Table/model | Condition | Fields | Value source | Transaction | Failure behavior |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | INSERT | JD | business exists and required fields present | ten_vi_tri, phong_ban, cap_bac, bao_cao_cho, nhiem_vu, trinh_do, kinh_nghiem, ky_nang, ky_nang_mem, uu_tien, muc_luong, phuc_loi, moi_truong, dia_diem, thoi_gian, han_nop, cach_ung_tuyen, mo_ta, ten_cong_ty, nganh, avt, doanhnghiep_id | normalized body; file path; token business id; business.hoten fallback | Prisma $transaction | missing business -> USER_NOT_FOUND |

## Response Source Matrix

| No | Field | Kind | Source/transform | Mapping source |
| ---: | --- | --- | --- | --- |
| 1 | id | data field | jobPublicSelect field. | jobs view/query |
| 2 | ten_vi_tri | data field | jobPublicSelect field. | jobs view/query |
| 3 | phong_ban | data field | jobPublicSelect field. | jobs view/query |
| 4 | cap_bac | data field | jobPublicSelect field. | jobs view/query |
| 5 | bao_cao_cho | data field | jobPublicSelect field. | jobs view/query |
| 6 | nhiem_vu | data field | jobPublicSelect field. | jobs view/query |
| 7 | trinh_do | data field | jobPublicSelect field. | jobs view/query |
| 8 | kinh_nghiem | data field | jobPublicSelect field. | jobs view/query |
| 9 | ky_nang | data field | jobPublicSelect field. | jobs view/query |
| 10 | ky_nang_mem | data field | jobPublicSelect field. | jobs view/query |
| 11 | uu_tien | data field | jobPublicSelect field. | jobs view/query |
| 12 | muc_luong | data field | jobPublicSelect field. | jobs view/query |
| 13 | phuc_loi | data field | jobPublicSelect field. | jobs view/query |
| 14 | moi_truong | data field | jobPublicSelect field. | jobs view/query |
| 15 | dia_diem | data field | jobPublicSelect field. | jobs view/query |
| 16 | thoi_gian | data field | jobPublicSelect field. | jobs view/query |
| 17 | han_nop | data field | jobPublicSelect field. | jobs view/query |
| 18 | cach_ung_tuyen | data field | jobPublicSelect field. | jobs view/query |
| 19 | mo_ta | data field | jobPublicSelect field. | jobs view/query |
| 20 | ten_cong_ty | data field | jobPublicSelect field. | jobs view/query |
| 21 | nganh | data field | jobPublicSelect field. | jobs view/query |
| 22 | ngay_tao | data field | jobPublicSelect field. | jobs view/query |
| 23 | doanhnghiep_id | data field | jobPublicSelect field. | jobs view/query |
| 24 | avt | data field | jobPublicSelect field. | jobs view/query |

## Validation and branch rules

- Multer parses optional avt.
- jobMutationSchema parses body and allows passthrough fields.
- normalizeJobData keeps only JOB mutation whitelist and maps file to `/uploads/` path.
- assertCreateJob requires ten_vi_tri and dia_diem.
- Transaction loads business and inserts JD.


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
