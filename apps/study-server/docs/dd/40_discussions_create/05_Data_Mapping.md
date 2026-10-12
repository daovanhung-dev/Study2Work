---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "40"
api_name: "Tạo topic/câu hỏi mới"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo approved API catalog và AC-19. API #40 chưa có route/module/query/test runtime. Các database items dưới đây là candidate design mapping; chúng không xác nhận SQL, live schema hoặc business behavior.

## 0. Check quyền

### 0.1. Lấy principal

- Đọc `Authorization` theo Bearer JWT contract.
- Yêu cầu principal hợp lệ và có role `Student` theo catalog.
- Lấy user ID từ authenticated principal; không nhận user ID từ request body.
- Current helper `validate_current_user_request` kiểm tra JWT subject và Student role cho các route đã wire; API #40 hiện không gọi helper này.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Current authenticated principal | `user_id` | JWT `sub`, parsed as positive integer by current auth helper | Current helper evidence only; API #40 is unwired. |
| N/A — access predicate chưa xác định | Course participation | AC-19 precondition: Student có quyền tham gia discussion của course | Không tự suy ra enrollment, course ownership hoặc published status. |

### 0.3. Check kết quả

- Token thiếu hoặc không hợp lệ trả 401 theo catalog.
- Role khác Student hoặc course access bị từ chối trả 403 theo catalog.
- Predicate course access và cách phân biệt course không tồn tại/chưa có quyền cần xác nhận.
- Không thêm 404 hoặc error code ngoài catalog.

## 1. Validate data input

### 1.1. Validate `course_id`

- `course_id` bắt buộc, kiểu `int64` theo catalog.
- Min/max, parse boundary và existence behavior chưa được đặc tả.
- Course access check được yêu cầu ở mức precondition AC-19; query predicate chưa có nguồn.

### 1.2. Validate `title`

- `title` bắt buộc, kiểu `string` theo catalog.
- Length, blank handling và normalization chưa được đặc tả.
- Không suy ra column hoặc length từ các field khác.

### 1.3. Validate `content`

- `content` bắt buộc, kiểu `int64` theo catalog.
- Reusable `Discussion.content` là `string`, còn checked-in DDL dùng `TEXT`.
- Không cast integer sang string hoặc định nghĩa content encoding khi chưa có quyết định.

- Request validation failure dùng 422 `DESIGN_VALIDATION_ERROR` theo catalog.
- Field constraints ngoài required/type chưa được định nghĩa.

## 2. Get thông tin

### 2.1. Query matrix

| Query ID | Purpose | Candidate source | Status |
|---|---|---|---|
| Q1 | Lấy `UserSummary` nếu response yêu cầu author projection | `users.id`, `users.full_name`, `users.avatar_url` | Candidate only; query/re-read behavior chưa được phê duyệt. |
| Q2 | Xác minh course participation nếu cần | N/A — table/predicate chưa được xác định | `SOURCE_REQUIRED`; không tự chọn enrollment/ownership rule. |

### 2.2. Candidate user projection

| Target table | Column candidate | Candidate purpose | Status |
|---|---|---|---|
| `users AS u` | `u.id` | Author ID | DDL design evidence; current auth helper exposes principal ID. |
| `↑` | `u.full_name` | Required `UserSummary.full_name` | DDL design evidence; source lookup not specified. |
| `↑` | `u.avatar_url` | Optional author avatar | Nullable in DDL; null/omit response rule not endpoint-defined. |

### 2.3. JOIN / WHERE

- Candidate author lookup condition is `u.id = authenticated_principal.user_id`.
- No discussion/course access JOIN or WHERE clause is approved for API #40.
- Do not infer enrollment, ownership, course publication, or visibility predicates.

## 3. Insert/Update thông tin

### 3.1. Target table

- Candidate target is `discussions`, identified by the AC-19 `INSERT Discussion` node and DB guide.

### 3.2. Conditions

- This is the AC-19 “New topic” branch; the activity diagram sends replies to API #41 instead.
- DB guide says `parent_id IS NULL` identifies a root topic; using NULL for API #40 is a candidate mapping, not runtime evidence.

### 3.3. Items update/insert

- Candidate insert mapping: [07_discussions_insert.md](./07_discussions_insert.md).
- No update, counter mutation, or additional write is specified for API #40 by the AC-19 create-topic node.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `course_id` | Request body `course_id` | Candidate direct mapping; DDL FK nullable but logical relation is required. |
| `user_id` | Authenticated principal ID | Candidate value source; DDL FK nullable but logical relation is required. |
| `parent_id` | `NULL` | Candidate root-topic mapping from DB guide and AC-19 branch separation. |
| `title` | `SOURCE_REQUIRED` | Required request/response field has no physical `discussions.title` column. |
| `content` | `SOURCE_REQUIRED` | Request is `int64`; DB is `TEXT`; conversion rule missing. |
| `status` | `SOURCE_REQUIRED` | DDL default is `ACTIVE`; whether API should rely on it and enum semantics are unresolved. |
| `created_at` | `SOURCE_REQUIRED` | DDL requires non-NULL timestamp and defines no default; source of value unresolved. |
| `updated_at` | `SOURCE_REQUIRED` | DDL requires non-NULL timestamp and defines no default; source of value unresolved. |
| `id` | Database-generated candidate | DDL declares `BIGSERIAL`; live schema/generation not verified. |

### 3.5. Transaction

- Transaction owner and rollback behavior are TBD because API #40 has no implementation or transaction contract.
- Do not claim the candidate mapping is executable SQL.

## 4. Map response

### 4.1. Success envelope

- HTTP status is 201 with `DESIGN_RESOURCE_CREATED` per API catalog.
- `data` retains `Page<Discussion>`; page construction is unresolved for this create endpoint.
- `traceId` and `meta` follow shared API guidelines.

### 4.2. Discussion item source matrix

| Response field | Candidate source | Transform | Status |
|---|---|---|---|
| `id` | Generated `discussions.id` | Integer ID | Candidate; BIGSERIAL design DDL only. |
| `course_id` | Request and inserted `discussions.course_id` | Direct | Candidate; DDL nullability conflicts with logical required field. |
| `title` | N/A | N/A | `SOURCE_REQUIRED`; no physical column. |
| `content` | `discussions.content` | N/A | `SOURCE_REQUIRED`; no approved conversion from request int64 to TEXT/string. |
| `author.id` | Authenticated principal / `users.id` | Candidate direct mapping | Profile query not specified. |
| `author.full_name` | `users.full_name` | Candidate direct mapping | Query required; DDL evidence only. |
| `author.avatar_url` | `users.avatar_url` | Candidate direct mapping | Null/omit rule unresolved. |
| `status` | `discussions.status` | Candidate status projection | Enum and create policy unresolved; DB default `ACTIVE` is not approved API behavior. |
| `comments[]` | Child `discussions` rows and users, if returned | N/A | API #42 reloads topic + comments; create response boundary unresolved. |

### 4.3. Page metadata

- `data.pagination.page`, `size`, `total`, and `total_pages` are required by `PageMeta`.
- API #40 has no page input or creation-specific page calculation source.
- Do not infer page size, count, total-pages formula, or return-page semantics.

## 5. Check kết quả execute query

### 5.1. Thành công

- Return HTTP 201 and `DESIGN_RESOURCE_CREATED` after successful creation per catalog.
- Keep response data typed as `Page<Discussion>`; unresolved fields remain documented in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

### 5.2. Lỗi xác thực hoặc quyền truy cập

- Authentication failure maps to 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Student role or course access denial maps to 403 `DESIGN_ACCESS_DENIED`.

### 5.3. Lỗi validation

- Invalid/missing required request fields map to 422 `DESIGN_VALIDATION_ERROR`.
- Do not add length, blank, parse, or cross-field rules beyond source evidence.

### 5.4. Lỗi hệ thống

- Internal/database failure maps to 500 `DESIGN_INTERNAL_ERROR`.
- Transaction rollback behavior is not specified; refer to [06_Error.md](./06_Error.md).
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
