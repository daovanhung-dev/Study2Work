---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `course_id` | `path["course_id"]` | Parse `int64`; malformed path follows contract `404` | Q1, Q2, Q4 scope | `data.items[].course_id` | Positive/minimum rule chưa được source xác nhận |
| `page` | `query["page"]` khi có | Parse `int32`; `>= 1` là design-only | Q2 `LIMIT/OFFSET` | `data.pagination.page` | Malformed optional query không có status riêng trong contract |
| `rating` | `query["rating"]` theo chuẩn hóa source literal “rating filter” | String shape nếu có | Không thêm predicate vì rating source chưa tồn tại | Không map trực tiếp | Tên vật lý, filter semantics và rating source TBD |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected column | Result variable | Branch |
|---|---|---|---|---|---|---|
| `Q1` | Gate course public | `READ` | `courses AS c` | `c.id` | `published_course` | `3.2` |
| `Q1` | Gate course public | `READ` | `courses AS c` | `c.status` | `published_course` | `3.2` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.id` | `review_page` | `4.1` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.course_id` | `review_page` | `4.1` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.user_id` | `review_page` | `4.1` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.content` | `review_page` | `4.1` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.status` | `review_page` | `4.1` |
| `Q2` | Lấy page review gốc | `READ` | `discussions AS d` | `d.created_at` | `review_page` | `4.1` |
| `Q2` | Lấy author review | `READ` | `users AS u` | `u.id` | `review_page` | `4.1` |
| `Q2` | Lấy author review | `READ` | `users AS u` | `u.full_name` | `review_page` | `4.1` |
| `Q2` | Lấy author review | `READ` | `users AS u` | `u.avatar_url` | `review_page` | `4.1` |
| `Q3` | Lấy replies của page review | `READ` | `discussions AS r` | `r.id` | `review_comments` | `4.2` |
| `Q3` | Lấy replies của page review | `READ` | `discussions AS r` | `r.parent_id` | `review_comments` | `4.2` |
| `Q3` | Lấy replies của page review | `READ` | `discussions AS r` | `r.user_id` | `review_comments` | `4.2` |
| `Q3` | Lấy replies của page review | `READ` | `discussions AS r` | `r.content` | `review_comments` | `4.2` |
| `Q3` | Lấy replies của page review | `READ` | `discussions AS r` | `r.created_at` | `review_comments` | `4.2` |
| `Q3` | Lấy author reply | `READ` | `users AS cu` | `cu.id` | `review_comments` | `4.2` |
| `Q3` | Lấy author reply | `READ` | `users AS cu` | `cu.full_name` | `review_comments` | `4.2` |
| `Q3` | Lấy author reply | `READ` | `users AS cu` | `cu.avatar_url` | `review_comments` | `4.2` |
| `Q4` | Đếm review gốc phù hợp | `READ` | `discussions AS d` | `COUNT(*)` | `total_reviews` | `4.3` |

### Query conditions

| Query ID | Clause type | Filter/condition | Remarks |
|---|---|---|---|
| `Q1` | Filter | `c.id = :course_id` | Scope theo path parameter |
| `Q1` | Filter | `c.status = 'PUBLISHED'` | Public-course gate |
| `Q2` | Filter | `d.course_id = :course_id` | Scope review theo course |
| `Q2` | Filter | `d.parent_id IS NULL` | Review gốc; hierarchy assumption |
| `Q2` | Filter | `d.status = 'ACTIVE'` | Visibility assumption cần xác nhận |
| `Q2` | Filter | `rating` | Không thêm predicate; rating source chưa tồn tại |
| `Q2` | Sort | `d.created_at DESC` | Design-only default |
| `Q2` | Sort | `d.id DESC` | Deterministic tie-breaker |
| `Q2` | Pagination | `LIMIT = 20` | Design-only page size |
| `Q2` | Pagination | `OFFSET = (effective_page - 1) * 20` | `effective_page` mặc định `1` |
| `Q3` | Filter | `r.parent_id IN (:review_ids)` | Self-reference replies của page hiện tại |
| `Q3` | Filter | `r.status = 'ACTIVE'` | Visibility assumption cần xác nhận |
| `Q4` | Filter | `d.course_id = :course_id` | Cùng scope Q2 |
| `Q4` | Filter | `d.parent_id IS NULL` | Chỉ đếm review gốc |
| `Q4` | Filter | `d.status = 'ACTIVE'` | Cùng visibility assumption Q2 |
| `Q4` | Aggregate | `COUNT(*)` | Không áp dụng `LIMIT/OFFSET` |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `6.1/6.2/6.3` | `true` on success | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `6.1/6.2/6.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `6.1/6.2/6.3` | Fixed by branch | Text TBD | N/A |
| `data.items[].id` | `int64` | Query result | `discussions.id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].course_id` | `int64` | Query result | `discussions.course_id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].title` | `string` | Unresolved source | `N/A — discussions.title missing` | `5.1` | No fallback transform | `TBD` | Required contract field has no ERD source |
| `data.items[].content` | `string` | Query result | `discussions.content` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].author.id` | `int64` | Joined query result | `users.id` via `discussions.user_id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].author.full_name` | `string` | Joined query result | `users.full_name` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].author.avatar_url` | `uri` | Joined query result | `users.avatar_url` | `5.1` | Direct mapping | `null` when `NULL` | Optional `UserSummary` field |
| `data.items[].status` | `DiscussionStatus` | Query result | `discussions.status` | `5.1` | Filter `ACTIVE` | `N/A` | Visibility assumption |
| `data.items[].comments[].id` | `int64` | Query result | `discussions.id` for child | `5.2` | Direct mapping | `N/A` | N/A |
| `data.items[].comments[].discussion_id` | `int64` | Parent relation | `discussions.parent_id` | `5.2` | Map to parent review ID | `N/A` | N/A |
| `data.items[].comments[].content` | `string` | Query result | `discussions.content` for child | `5.2` | Direct mapping | `N/A` | N/A |
| `data.items[].comments[].author.id` | `int64` | Joined query result | `users.id` via child `user_id` | `5.2` | Direct mapping | `N/A` | N/A |
| `data.items[].comments[].author.full_name` | `string` | Joined query result | `users.full_name` | `5.2` | Direct mapping | `N/A` | N/A |
| `data.items[].comments[].author.avatar_url` | `uri` | Joined query result | `users.avatar_url` | `5.2` | Direct mapping | `null` when `NULL` | Optional `UserSummary` field |
| `data.items[].comments[].created_at` | `date-time` | Query result | `discussions.created_at` for child | `5.2` | ISO-8601 serialization | `N/A` | N/A |
| `data.pagination.page` | `int32` | Design constant/query | `effective_page` | `5.3` | Default `1` | `1` when omitted | Design-only default |
| `data.pagination.size` | `int32` | Design constant | `20` | `5.3` | Fixed page size | `20` | Not a client query field |
| `data.pagination.total` | `int64` | Aggregate query | `COUNT(*)` Q4 | `4.3/5.3` | `total_reviews` | `0` when empty | N/A |
| `data.pagination.total_pages` | `int32` | Derived | `total_reviews`, `20` | `5.3` | `ceil(total_reviews / 20)` | `0` when total is `0` | Design-only page size |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | No aggregate rating extension |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | Request correlation UUID | `TBD — exact generator` | N/A |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có role/function authorization check.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `N/A` | `N/A` | `N/A` | Public endpoint; không query quyền |

### 0.3. Check kết quả

- Không áp dụng check quyền; tiếp tục xử lý `1`.

## 1. Get request data

### 1.1. Get request header

- `authorization`: không bắt buộc; endpoint public.
- `content_type`: không bắt buộc vì GET không có request body.

### 1.2. Get request path

- `course_id`: lấy từ path parameter `/api/v1/courses/{course_id}/reviews`.
- Request field contract chi tiết tại [03_Request.md](./03_Request.md).

### 1.3. Get query

- `page`: lấy từ `query["page"]` nếu được gửi; dùng `1` nếu vắng mặt.
- `rating`: lấy từ `query["rating"]` theo cách chuẩn hóa literal `rating filter`.
- Không nhận `size` hoặc query field khác ngoài contract.

## 2. Validate data input

- Validate từng field theo [03_Request.md](./03_Request.md).
- Không tự thêm HTTP `422` vì API #10 không khai báo status này.

### 2.1. Validate `page`

- Nếu `page` vắng mặt: dùng `effective_page = 1`.
- Nếu `page` có mặt và parse được `int32` với `page >= 1`: dùng làm `effective_page`.
- Nếu `page` không parse được: semantics lỗi là `TBD` do contract không khai báo status validation; không tự tạo business code.

### 2.2. Validate `rating filter`

- Nếu query key chuẩn hóa `rating` không có kiểu `string`: semantics lỗi là `TBD` do contract không khai báo status validation.
- Nếu có giá trị string: giữ `rating_filter` để trace; không thêm predicate vì ERD không có rating source.
- Chi tiết discrepancy: [02_Overview.md](./02_Overview.md#conflicts).

### 2.3. Validate `course_id`

- Parse path segment thành `int64`.
- Nếu path không parse được thành `int64`: đi tới nhánh `404 DESIGN_RESOURCE_NOT_FOUND` theo [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc quy tắc số dương vì contract chưa đặc tả.

## 3. Check course public

### 3.1. Query course visibility — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `courses AS c` | `c.status` | Course status | `Q1`; phải là `PUBLISHED` |

**WHERE**

| Filter/condition | Remarks |
|---|---|
| `c.id = :course_id` | Scope theo path parameter |
| `c.status = 'PUBLISHED'` | Public-course gate |

### 3.2. Check result

- Nếu Q1 trả đúng một course `PUBLISHED`: tiếp tục xử lý `4`.
- Nếu Q1 không trả record: trả `404 DESIGN_RESOURCE_NOT_FOUND`; không expose course draft/private.

## 4. Get reviews

### 4.1. Query review roots — Q2

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `discussions AS d` | `d.id` | Review ID | `Q2` |
| `discussions AS d` | `d.course_id` | Course ID | `Q2` |
| `discussions AS d` | `d.user_id` | Review author FK | `Q2` |
| `discussions AS d` | `d.content` | Review content | `Q2` |
| `discussions AS d` | `d.status` | Review status | `Q2`; filter `ACTIVE` |
| `discussions AS d` | `d.created_at` | Review created time | `Q2`; sort |
| `users AS u` | `u.id` | Author ID | `Q2` join |
| `users AS u` | `u.full_name` | Author name | `Q2` join |
| `users AS u` | `u.avatar_url` | Author avatar | `Q2` join; nullable |

**JOIN**

| Target table | Join condition | Join type |
|---|---|---|
| `discussions AS d` | `N/A` | `BASE` |
| `users AS u` | `u.id = d.user_id` | `INNER JOIN` |

**WHERE**

| Filter/condition | Remarks |
|---|---|
| `d.course_id = :course_id` | Scope review theo course |
| `d.parent_id IS NULL` | Review gốc; hierarchy assumption |
| `d.status = 'ACTIVE'` | Visibility assumption cần xác nhận |
| `rating` | Không thêm predicate; rating source chưa tồn tại |

**ORDER BY**

| Sort expression | Remarks |
|---|---|
| `d.created_at DESC` | Design-only default |
| `d.id DESC` | Deterministic tie-breaker |

**Pagination**

| Pagination item | Value | Remarks |
|---|---|---|
| `effective_page` | `page` hoặc `1` nếu page vắng mặt | Design-only default |
| `page_size` | `20` | Không nhận `size` từ client |
| `LIMIT` | `20` | Design-only page size |
| `OFFSET` | `(effective_page - 1) * 20` | Design-only pagination |

### 4.2. Query replies — Q3

- Nếu `review_page` rỗng: không chạy Q3; map `comments = []`.
- Nếu `review_page` có record: lấy `review_ids` từ Q2.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `discussions AS r` | `r.id` | Reply ID | `Q3` |
| `discussions AS r` | `r.parent_id` | Parent review ID | `Q3` |
| `discussions AS r` | `r.user_id` | Reply author FK | `Q3` |
| `discussions AS r` | `r.content` | Reply content | `Q3` |
| `discussions AS r` | `r.created_at` | Reply created time | `Q3` |
| `users AS cu` | `cu.id` | Reply author ID | `Q3` join |
| `users AS cu` | `cu.full_name` | Reply author name | `Q3` join |
| `users AS cu` | `cu.avatar_url` | Reply author avatar | `Q3` join; nullable |

**JOIN**

| Target table | Join condition | Join type |
|---|---|---|
| `discussions AS r` | `N/A` | `BASE` |
| `users AS cu` | `cu.id = r.user_id` | `INNER JOIN` |

**WHERE**

| Filter/condition | Remarks |
|---|---|
| `r.parent_id IN (:review_ids)` | Self-reference replies của page hiện tại |
| `r.status = 'ACTIVE'` | Visibility assumption cần xác nhận |

### 4.3. Count review roots — Q4

| Query item | Value | Remarks |
|---|---|---|
| Aggregate | `COUNT(*)` trên `discussions AS d` | Lưu vào `total_reviews` |
| Filter | `d.course_id = :course_id` | Cùng scope Q2 |
| Filter | `d.parent_id IS NULL` | Chỉ đếm review gốc |
| Filter | `d.status = 'ACTIVE'` | Cùng visibility assumption Q2 |
| Pagination | `N/A` | Không áp dụng `LIMIT/OFFSET` |

### 4.4. Check result

- Nếu Q2 có record: tiếp tục xử lý `5`.
- Nếu Q2 trả `0` record: tiếp tục xử lý `5` với `items = []`, `total = 0`; không trả `404`.
- Nếu Q1/Q2/Q3/Q4 hoặc mapping thất bại: đi tới nhánh `500 DESIGN_INTERNAL_ERROR`.

## 5. Map response

### 5.1. Map từng review

- `data.items[].id = review_page[].id`.
- `data.items[].course_id = review_page[].course_id`.
- `data.items[].title = TBD` vì `discussions.title` không tồn tại trong ERD.
- `data.items[].content = review_page[].content`.
- `data.items[].author.id = review_page[].author.id`.
- `data.items[].author.full_name = review_page[].author.full_name`.
- `data.items[].author.avatar_url = review_page[].author.avatar_url`.
- `data.items[].status = review_page[].status`.
- Không map `rating` hoặc aggregate rating vì contract không có field response tương ứng.

### 5.2. Map replies

- `data.items[].comments[].id = review_comments[].id`.
- `data.items[].comments[].discussion_id = review_comments[].parent_id`.
- `data.items[].comments[].content = review_comments[].content`.
- `data.items[].comments[].author.id = review_comments[].author.id`.
- `data.items[].comments[].author.full_name = review_comments[].author.full_name`.
- `data.items[].comments[].author.avatar_url = review_comments[].author.avatar_url`.
- `data.items[].comments[].created_at = review_comments[].created_at`.
- Nếu review không có reply active: `comments = []`.

### 5.3. Map pagination và envelope

- `data.pagination.page = effective_page`.
- `data.pagination.size = 20`.
- `data.pagination.total = total_reviews`.
- `data.pagination.total_pages = ceil(total_reviews / 20)`.
- `data.pagination.total_pages = 0` khi `total_reviews = 0`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `message = application success message`.
- `meta = {}`.
- `traceId = request correlation UUID`.
- Response schema: [04_Response.md](./04_Response.md).

## 6. Trả về response

### 6.1. Thành công

- `HTTPStatus = 200`.
- Trả `ApiEnvelope<Page<Discussion>>` theo [04_Response.md](./04_Response.md).

### 6.2. Not found

- `HTTPStatus = 404`.
- `success = false`.
- `businessCode = DESIGN_RESOURCE_NOT_FOUND`.
- `data = {}`.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

### 6.3. System error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = DESIGN_INTERNAL_ERROR`.
- `data = {}`.
- Không trả raw SQL, stack trace hoặc storage detail.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

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
