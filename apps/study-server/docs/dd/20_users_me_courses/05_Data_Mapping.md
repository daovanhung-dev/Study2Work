---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

~~~text
0. Nhận Authorization Bearer và xác thực Student theo design contract.
1. Đọc optional query status:string và page:int32; không áp thêm enum/range/default chưa có nguồn.
2. Theo AC-13, đọc enrollment/course qua quan hệ enrollments.course_id = courses.id.
3. Identity predicate, status predicate, projection, ordering và pagination cần xác nhận.
4. Contract hiện khai báo data là UserProfile; chưa có mapping từ query enrollment/course sang schema này.
5. Trả các business code đã khai báo; không thêm progress vào API #20.
~~~

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | HTTP header | 0 | Bearer JWT theo contract; current helper có thể xác thực nhưng API #20 chưa gọi | Current user selector chưa được xác nhận cho query API #20 | Authentication/authorization | N/A | Runtime endpoint chưa wired. |
| status | Query | 1/3 | string; enum/valid values chưa có | Target filter và predicate chưa xác định | Optional filter | N/A | Có thể là Enrollment hoặc Course status; không chọn thay owner. |
| page | Query | 1/3 | int32; min/max/default chưa có | Offset/limit chưa xác định | Optional pagination | meta content chưa xác định | Chưa có page base, size, order hay total-count rule. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Đọc quan hệ Enrollment và Course theo AC-13 | SELECT — DESIGN_ONLY | enrollments | e | e.user_id, e.course_id, c.id là khóa/điều kiện đã có; projection response SOURCE_REQUIRED | courses AS c ON e.course_id = c.id | Candidate current-user predicate e.user_id = authenticated user ID; áp dụng cần xác nhận API-specific mapping | N/A | SOURCE_REQUIRED | SOURCE_REQUIRED | enrollment_course_rows | Không tự đặt filter visibility, status, single-row hoặc pagination rule. |
| Q1 | Áp dụng optional status | SELECT filter — DESIGN_ONLY | enrollments / courses | e / c | status column chưa xác định | Q1 | SOURCE_REQUIRED | N/A | SOURCE_REQUIRED | N/A | enrollment_course_rows | Không thể xác định cột, enum, semantics hoặc kết quả invalid status từ contract hiện tại. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A — read-only | N/A | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | API #20 không có DB mutation. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Envelope constant | ApiEnvelope<T> schema | 4.1/4.2/4.3/4.4 | true on success; false on error | N/A | Exact runtime endpoint mapping not verified. |
| businessCode | string | Design contract | DESIGN_* code per status | 4.1/4.2/4.3/4.4 | Fixed by branch | N/A | Catalog is design-only, not runtime proof. |
| message | string | Message source | Not specified by API contract | 4.1/4.2/4.3/4.4 | SOURCE_REQUIRED | N/A | Do not reuse API #14 profile-specific messages. |
| data | UserProfile | Contract schema | ApiEnvelope<UserProfile> | 3/4.1 | Per reusable UserProfile schema | Success null/empty behavior unspecified | AC-13 requires course list; query columns cannot be mapped to UserProfile from current sources. |
| data.id | int64 | Contract schema | UserProfile.id; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | Enrollment/Course join does not define this field source. |
| data.full_name | string | Contract schema | UserProfile.full_name; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | No mapping established for API #20. |
| data.email | email | Contract schema | UserProfile.email; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | No mapping established for API #20. |
| data.role | UserRole | Contract schema | UserProfile.role; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | Enum values and query source not established here. |
| data.avatar_url | uri, optional | Contract schema | UserProfile.avatar_url; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Optional/null semantics unspecified | No mapping established for API #20. |
| data.bio | string, optional | Contract schema | UserProfile.bio; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Optional/null semantics unspecified | No mapping established for API #20. |
| data.phone | string, optional | Contract schema | UserProfile.phone; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Optional/null semantics unspecified | No mapping established for API #20. |
| data.status | UserStatus | Contract schema | UserProfile.status; physical query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | Enum values and query source not established here. |
| data.created_at | date-time | Contract schema | UserProfile.created_at; physical query source unresolved | 3/4.1 | ISO-8601 per schema | Required by schema | No mapping established for API #20. |
| data.updated_at | date-time | Contract schema | UserProfile.updated_at; physical query source unresolved | 3/4.1 | ISO-8601 per schema | Required by schema | No mapping established for API #20. |
| meta | object | Envelope | ApiEnvelope<T> schema | 4.1/4.2/4.3/4.4 | Object | Content unspecified | Query page does not establish PageMeta output. |
| traceId | uuid | Current Study trace convention / shared schema | Request trace context | 4.1/4.2/4.3/4.4 | Current envelope field | Required by schema | API #20 runtime response not verified. |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- Current [auth.py](../../../app/utils/auth.py) tách Bearer token, kiểm tra access claims, parse sub thành positive integer và yêu cầu STUDENT.
- Đây là reusable source hiện hành; API #20 chưa có route gọi helper.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT | sub | Current helper parses numeric string to user ID | Current helper behavior; API #20 query binding chưa xác minh. |
| JWT | roles | Must include STUDENT in current helper | Current helper behavior; design contract also says role=Student. |
| enrollments | user_id | Candidate equals authenticated user ID | Expected from /me intent and table relation; retain as SOURCE_REQUIRED until API #20 mapping is approved. |

### 0.3. Check kết quả

- Nếu token không hợp lệ: đi tới [06_Error.md](./06_Error.md), HTTP 401 theo contract.
- Nếu role không đủ: đi tới [06_Error.md](./06_Error.md), HTTP 403 theo contract.
- API #20 current authorization behavior chưa được runtime kiểm chứng.

## 1. Validate data input

### 1.1. Query status

- status là optional string theo catalog.
- Giá trị hợp lệ, enum, target column, matching rule và default đều SOURCE_REQUIRED.
- Không tự ánh xạ status sang enrollments.status hoặc courses.status.

### 1.2. Query page

- page là optional int32 theo catalog.
- Min/max, page base, page size, sort order và default chưa được khai báo.
- Không tự tính LIMIT/OFFSET hoặc pagination metadata.

## 2. Get thông tin

### 2.1. Quan hệ Enrollment và Course

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| enrollments AS e | e.user_id | Candidate current-user predicate | Identity selector to endpoint query is SOURCE_REQUIRED. |
| enrollments AS e | e.course_id | Join key | Relation to courses.id is in DB design and checked-in DDL. |
| courses AS c | c.id | Join key | JOIN condition: e.course_id = c.id. |
| enrollments AS e / courses AS c | Response projection | Khóa học đăng ký | SOURCE_REQUIRED because response schema says UserProfile while AC-13 says course list. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| enrollments AS e | N/A | BASE |
| courses AS c | c.id = e.course_id | INNER JOIN — relationship specified by AC-13/DB design; final query not runtime-verified. |

### 2.3. WHERE

- e.user_id = authenticated user ID is a candidate predicate derived from /me + Student semantics; exact API #20 binding remains SOURCE_REQUIRED.
- status filter target and predicate are SOURCE_REQUIRED.
- Course visibility predicate is not specified for API #20.

### 2.4. ORDER BY and pagination

- ORDER BY: SOURCE_REQUIRED.
- Query parameter page exists; page size, offset calculation, total count and meta mapping are SOURCE_REQUIRED.

## 3. Map result

- AC-13 has the client call GET /api/v1/users/me/progress separately, then combine course and progress.
- API #20 does not include progress or percentage fields in its declared response.
- Mapping joined course rows into UserProfile is unresolved and tracked in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- If the result is empty, AC-13 specifies a client empty state; API response shape for no courses remains SOURCE_REQUIRED.

## 4. Check result and return response

### 4.1. Thành công

- HTTP status = 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Return shape remains ApiEnvelope<UserProfile> per catalog pending contract-owner resolution.

### 4.2. Authentication / authorization errors

- HTTP status = 401; businessCode = DESIGN_AUTHENTICATION_REQUIRED.
- HTTP status = 403; businessCode = DESIGN_ACCESS_DENIED.

### 4.3. Validation error

- HTTP status = 422; businessCode = DESIGN_VALIDATION_ERROR.
- Exact conditions for status and page validation are SOURCE_REQUIRED.

### 4.4. System error

- HTTP status = 500; businessCode = DESIGN_INTERNAL_ERROR.
- Do not return raw database errors, stack traces or internal details.

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
