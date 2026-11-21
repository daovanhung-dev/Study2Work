---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Nhận Authorization Bearer và raw course_id theo path.
2. Xác thực JWT/current user, yêu cầu role MENTOR và lấy numeric user ID.
3. Parse signed-int64 course_id; parse/range lỗi trả 404 DESIGN_RESOURCE_NOT_FOUND.
4. SELECT courses(id, mentor_id); thiếu course trả 404, owner khác principal trả 403.
5. SELECT mọi contents của course có deleted_at IS NULL, gồm mọi status; sort parent_id NULLS FIRST, content_order, id.
6. Validate projection, course scope, unique IDs, parent references và không cycle; lỗi query/mapping trả 500.
7. Trả Content[] phẳng trong success envelope; empty tree là [] và không có mutation.
~~~

## 0. Check quyền

| Target | Column/field | Condition/value | Remarks |
|---|---|---|---|
| JWT principal | role / user ID | `MENTOR`, numeric authenticated user ID | Dùng `validate_current_user_request`; token không được echo. |
| `courses` | `id` | bằng parsed path `course_id` | Chỉ course tồn tại mới tiếp tục. |
| `courses` | `mentor_id` | bằng principal ID | Current implementation direct-owner rule; assigned-course access không được kiểm tra. |

Kết quả: token thiếu/sai → 401; role sai hoặc owner mismatch → 403; course thiếu → 404; DB/mapping failure → 500. Ownership policy theo source implementation, chưa phải xác nhận cho assigned Mentor.

## 1. Validate input

| Request field | Source | Validate/use | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header | Bearer JWT; current Study guard; role Mentor | Xác định principal ID | Không echo | Assignment policy còn mở. |
| `course_id` | Path | Raw signed integer; int64 bounds | Bind vào Q1 và Q2 | Mỗi `data[].course_id` lấy từ row | Invalid/out-of-range ánh xạ 404 theo implementation. |
| Body/query | N/A | N/A | N/A | N/A | Không có. |

## 2. Get thông tin

### Query Matrix

| Query | Type | Table | Columns | Rule | Result/branch |
|---|---|---|---|---|---|
| Q1 | SELECT | `courses` | `id`, `mentor_id` | `id = :course_id LIMIT 1` | Missing → 404; owner mismatch → 403. |
| Q2 | SELECT | `contents` | `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order AS order` | `course_id = :course_id AND deleted_at IS NULL` | Ordered flat node rows; empty → `[]`. |

Q2 SQL:

~~~sql
SELECT id, course_id, content_type, title, payload, status, parent_id,
       content_order AS "order"
FROM contents
WHERE course_id = :course_id
  AND deleted_at IS NULL
ORDER BY parent_id NULLS FIRST, content_order ASC, id ASC;
~~~

No version, status visibility or publication filter is applied. Rows with draft-like and published-like statuses are both returned. Query constants reside in `app/modules/mentor/api_49_mentor_content_list/query.py`.

### Mapping and validation

| DB column | Response field | Mapping | Validation |
|---|---|---|---|
| `id` | `data[].id` | Direct | Strict signed int64; unique in response. |
| `course_id` | `data[].course_id` | Direct | Must equal requested course. |
| `content_type` | `data[].content_type` | Direct string | No closed enum validation. |
| `title` | `data[].title` | Direct string | Required. |
| `payload` | `data[].payload` | JSON object copy | Reject non-object/missing projection. |
| `status` | `data[].status` | Direct string | No closed enum or visibility validation. |
| `parent_id` | `data[].parent_id` | Direct nullable int64 | Null omitted; non-null parent must be present in result. |
| `content_order` | `data[].order` | Alias to int32 | SQL stable tie-breaker uses `id`. |

The view rejects duplicate IDs, missing parent references, cross-course rows and cycles as an internal mapping failure; it does not return a partial tree.

## 3. Mutation

N/A — read-only. No `INSERT`, `UPDATE`, `DELETE`, `commit` or content mutation occurs.

## 4. Response and errors

| Branch | HTTP | Business code | Data |
|---|---:|---|---|
| Read succeeds | 200 | `DESIGN_RESOURCE_RETRIEVED` | `Content[]`; may be empty. |
| Authentication missing/invalid | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | `null` |
| Role/owner denied | 403 | `DESIGN_ACCESS_DENIED` | `null` |
| Invalid/out-of-range ID or missing course | 404 | `DESIGN_RESOURCE_NOT_FOUND` | `null` |
| Query/projection/tree validation error | 500 | `DESIGN_INTERNAL_ERROR` | `null` |

All errors use the shared envelope and current middleware contract route entry. DB exceptions are rolled back and logged with trace ID; SQL/stack details are not exposed.

## 5. Storage and status boundary

The checked-in legacy DDL and migration define `contents` with BIGINT course/parent relations, JSONB object payload, open string `content_type`/`status`, `content_order` and nullable `deleted_at`. Migration `006_contents.sql` is an artifact only; no live DB was probed or migrated. The separate UUID V1-PILOT `content_blocks` schema is not used.

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
