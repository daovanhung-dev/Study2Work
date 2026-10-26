---
title: "Data Mapping"
order: 5
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Nhận Bearer token, `course_id` path và trace ID.
2. Xác thực token và role `MENTOR`; nhận numeric user ID từ JWT subject.
3. Parse raw `course_id` theo signed int64; sai định dạng/tràn int64 trả catalog 404.
4. Đọc course theo ID; không tồn tại trả 404, owner khác trả 403.
5. Đọc distinct Student có enrollment `ACTIVE`, giữ scope trực tiếp `courses.mentor_id` trong SQL.
6. Map tối thiểu thành `UserSummary[]`; roster rỗng trả 200 `[]`.
7. Không ghi DB hoặc gọi dịch vụ gửi thông báo; #63 sở hữu notification dispatch.

### Mục lục

- [0. Auth và nhận request](#step-0-auth-va-nhan-request)
- [1. Parse course ID](#step-1-parse-course-id)
- [2. Check course scope](#step-2-check-course-scope)
- [3. Đọc active Student roster](#step-3-doc-active-student-roster)
- [4. Map response](#step-4-map-response)
- [5. Return/error](#step-5-returnerror)
- [Ma trận request/query/response](#ma-tran-requestqueryresponse)

<a id="step-0-auth-va-nhan-request"></a>

## 0. Auth và nhận request

### 0.1. Authorization

- Đọc `Authorization` từ request header.
- Gọi `validate_current_user_request(..., role="MENTOR")` trước database access.
- Guard dùng Study JWT decoder, kiểm tra Bearer/JWT, `sub` numeric dương và `roles` chứa `MENTOR`.
- Lỗi auth trả 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có role Mentor trả 403 `DESIGN_ACCESS_DENIED`.

### 0.2. Trace

- Dùng trace ID từ middleware qua `get_trace_id(request)`.
- Envelope và response header dùng cùng trace ID.

<a id="step-1-parse-course-id"></a>

## 1. Parse course ID

- Nhận `course_id` dưới dạng raw path string để giữ catalog error set.
- Chấp nhận signed decimal integer trong range `[-2^63, 2^63-1]`.
- Không thêm điều kiện `course_id > 0` ngoài contract.
- Nếu path không phải số nguyên hoặc vượt signed-int64, trả 404 `DESIGN_RESOURCE_NOT_FOUND` trước DB access.

<a id="step-2-check-course-scope"></a>

## 2. Check course scope

### 2.1. Q1 — kiểm tra course

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | So khớp path ID | Legacy BIGSERIAL/BIGINT; live schema chưa xác minh. |
| `courses AS c` | `c.mentor_id` | Direct owner của course | So với numeric JWT subject. |

**WHERE**

- `c.id = :course_id`.

**LIMIT**

- `1` row.

### 2.2. Branch theo Q1

- Không có row: rollback read transaction và trả 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Projection không phải mapping hoặc `id` khác path: rollback và trả 500 `DESIGN_INTERNAL_ERROR`.
- `mentor_id` không bằng authenticated Mentor ID: rollback và trả 403 `DESIGN_ACCESS_DENIED`.
- Owner khớp: tiếp tục Q2.

Direct owner là fallback theo API #46/#49/#54. Assigned-Mentor relation không có trong schema legacy đã chọn và không được cấp quyền bởi #62.

<a id="step-3-doc-active-student-roster"></a>

## 3. Đọc active Student roster

### 3.1. Q2 — danh sách recipient

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `users AS u` | `u.id` | Recipient ID | `DISTINCT`; sort tăng dần. |
| `users AS u` | `u.full_name` | Tên hiển thị tối thiểu | Required trong legacy DDL. |
| `users AS u` | `u.avatar_url` | Avatar tùy chọn | NULL sẽ bị omit trong response. |
| `courses AS c` | `c.id` | Course scope | Khớp `course_id` trong path. |
| `courses AS c` | `c.mentor_id` | Mentor scope lần nữa | Bảo vệ roster query bằng direct owner predicate. |
| `enrollments AS e` | `e.user_id` | Link tới User | INNER JOIN loại enrollment không có user. |
| `enrollments AS e` | `e.course_id` | Link tới Course | INNER JOIN loại enrollment không có course. |
| `enrollments AS e` | `e.status` | Enrollment eligibility | Exact match `ACTIVE`. |
| `users AS u` | `u.role` | Actor eligibility | Exact match `STUDENT`. |

**JOIN**

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | N/A | BASE |
| `enrollments AS e` | `e.course_id = c.id` | INNER JOIN |
| `users AS u` | `u.id = e.user_id` | INNER JOIN |

**WHERE**

- `c.id = :course_id`.
- `c.mentor_id = :mentor_id`.
- `e.status = 'ACTIVE'`.
- `u.role = 'STUDENT'`.

**SELECT behavior**

- `DISTINCT` trên `u.id`, `u.full_name`, `u.avatar_url` để cùng một user chỉ xuất hiện một lần.
- Không lọc `users.status`; AC-25, catalog và legacy DDL chưa đặt điều kiện account status.

**ORDER BY**

- `u.id ASC`.

**Pagination**

- N/A — Request không khai báo `page` hoặc `size`; không thêm input hoặc PageMeta.

### 3.2. Empty result

- Course đã qua scope nhưng Q2 trả 0 row: trả HTTP 200 với `data: []`.
- Empty recipient set không phải lỗi 404.

<a id="step-4-map-response"></a>

## 4. Map response

- `response.data[].id = query_result.u.id`.
- `response.data[].full_name = query_result.u.full_name`.
- `response.data[].avatar_url = query_result.u.avatar_url` khi giá trị khác NULL.
- Reject duplicate IDs, missing/non-string `full_name`, invalid positive int64 ID hoặc non-string `avatar_url` bằng lỗi 500; không trả projection một phần.
- Omit `avatar_url` khi SQL value là NULL.
- `response.meta = {}`; không dựng pagination metadata.
- Không đưa email, phone, account status hoặc enrollment ID vào response.

<a id="step-5-returnerror"></a>

## 5. Return/error

- Thành công: HTTP 200 `DESIGN_RESOURCE_RETRIEVED` và `UserSummary[]`.
- Auth lỗi: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Role/owner mismatch: 403 `DESIGN_ACCESS_DENIED`.
- Invalid signed-int64 path hoặc course không tồn tại: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- DB query/projection lỗi: 500 `DESIGN_INTERNAL_ERROR`; rollback dọn read transaction.
- Không thêm 422, 409 hoặc 503.
- Không commit; không ghi Notification, recipient, queue hoặc delivery.
- #63 `recipients:string!` encoding vẫn open; #62 trả số User ID và không serialize cho endpoint khác.

## Ma trận request/query/response

### Request Usage Matrix

| Request field | Source | Use | Validation/branch |
|---|---|---|---|
| `Authorization` | HTTP header | Auth guard | Bearer JWT và role `MENTOR` trước DB. |
| `course_id` | Path | Q1 và Q2 | signed-int64; malformed/out-of-range→404. |
| Query/body | N/A | N/A | Không khai báo. |

### Query Matrix

| Query | Type | Tables and projection | Conditions | Order/pagination | Result |
|---|---|---|---|---|---|
| Q1 | SELECT | `courses.id`, `courses.mentor_id` | `id=:course_id` | `LIMIT 1` | phân biệt missing, owner match và 403. |
| Q2 | SELECT DISTINCT | `users.id/full_name/avatar_url`, `courses`, `enrollments` | course ID, Mentor owner, ACTIVE enrollment, STUDENT role | `users.id ASC`; no pagination | recipient summary rows. |

### Mutation Matrix

| Operation | Target | Behavior |
|---|---|---|
| N/A | N/A | N/A — READ-ONLY API; no commit or external call. |

### Response Source Matrix

| Response field | Type | Source | Transform | Empty/null rule |
|---|---|---|---|---|
| `data[].id` | int64 | `users.id` | Direct | Required. |
| `data[].full_name` | string | `users.full_name` | Direct | Required. |
| `data[].avatar_url` | uri? | `users.avatar_url` | Direct | Omit when NULL. |
| `data` | array | Q2 rows | One summary per distinct user | Empty → `[]`. |
| `meta` | object | Envelope | `{}` | Always present. |

## Boundary với API #63/#64

- #62 chỉ đọc roster.
- #63 nhận `recipients:string!` nhưng chưa chỉ định CSV, JSON hay ID khác; implementation #62 không chọn encoding.
- #64 đọc delivery status; không có side effect hoặc notification status trong #62.
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
