---
title: "Data Mapping"
order: 5
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Theo design contract, xác thực Bearer JWT và quyền Student.
1. Nhận raw query declaration “course_id list hoặc aggregate?:string”; parse/validate chưa thể chốt.
2. Theo AC-13, API #20 nạp Course, API #21 đọc lesson progress/completion và client ghép course + progress.
3. Theo AC-18, API #21 tạo dữ liệu tổng hợp theo user; công thức, độ hạt và projection chưa được đặc tả.
4. Khi Student chọn một course, flow dùng API #37 cho progress chi tiết; API #38 đọc achievements riêng.
5. DB design có lesson_progress và quan hệ qua lessons tới courses; query API #21 là DESIGN_ONLY, chưa có SQL runtime.
6. Catalog response là ApiEnvelope<UserProfile>; mapping UserProfile/progress chưa được giải quyết.
7. Trả các status/business codes đã khai báo; không thêm status hoặc field.
~~~

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | HTTP header | 0 | Bearer JWT; role Student theo contract | Candidate current-user scope; API #21 chưa gọi auth helper | Authentication/authorization | N/A | Current-user query binding chưa được endpoint source xác nhận. |
| course_id list hoặc aggregate?:string | Query declaration trong catalog | 1/3 | Field grammar, kiểu list, optionality và allowed values chưa rõ | Candidate filter/aggregate selector; predicate chưa xác định | SOURCE_REQUIRED | Progress scope chưa được xác định | Không chuẩn hóa query phrase thành wire field tự đặt. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Đọc dữ liệu progress phục vụ aggregate theo user | SELECT — DESIGN_ONLY | lesson_progress | lp | Cột cần đọc và projection API #21 chưa được xác nhận | N/A trong căn cứ tối thiểu | Candidate lp.user_id = authenticated user ID; predicate API-specific SOURCE_REQUIRED | Aggregate formula/keys SOURCE_REQUIRED | N/A | N/A | user_progress_rows | DB guide gắn API #21/#37 vào SELECT; chưa có runtime query. |
| Q2 | Liên hệ lesson progress với course nếu cần gom theo course | SELECT relationship — DESIGN_ONLY | lessons, courses | l, c | l.id, l.course_id, c.id là khóa quan hệ trong DB design | lp.lesson_id = l.id; l.course_id = c.id — quan hệ schema, chưa xác nhận API query | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | course_progress_candidates | AC-13 cần ghép course + progress ở client; không chứng minh API #21 query join course. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A — read-only | N/A | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | API #21 không có mutation theo method GET. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Envelope schema | ApiEnvelope<T> | 4.1/4.2/4.3 | true on success; false on error | N/A | Runtime API #21 mapping chưa tồn tại. |
| businessCode | string | Design contract | DESIGN_* code by status | 4.1/4.2/4.3 | Fixed by branch | N/A | Exact codes are preserved from catalog. |
| message | string | Message source | SOURCE_REQUIRED | 4.1/4.2/4.3 | SOURCE_REQUIRED | N/A | Contract does not specify message text. |
| data | UserProfile | Contract schema | ApiEnvelope<UserProfile> | 3/4.1 | Per reusable UserProfile schema | Success null/empty behavior unspecified | Progress aggregate does not have a declared matching schema. |
| data.id | int64 | Contract schema | UserProfile.id; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | No API #21 field mapping. |
| data.full_name | string | Contract schema | UserProfile.full_name; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | No API #21 field mapping. |
| data.email | email | Contract schema | UserProfile.email; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | No API #21 field mapping. |
| data.role | UserRole | Contract schema | UserProfile.role; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | Enum and physical source are not established. |
| data.avatar_url | uri, optional | Contract schema | UserProfile.avatar_url; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Null/omit unspecified | No API #21 field mapping. |
| data.bio | string, optional | Contract schema | UserProfile.bio; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Null/omit unspecified | No API #21 field mapping. |
| data.phone | string, optional | Contract schema | UserProfile.phone; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Null/omit unspecified | No API #21 field mapping. |
| data.status | UserStatus | Contract schema | UserProfile.status; query source unresolved | 3/4.1 | SOURCE_REQUIRED | Required by schema | Enum and physical source are not established. |
| data.created_at | date-time | Contract schema | UserProfile.created_at; query source unresolved | 3/4.1 | ISO-8601 per schema | Required by schema | No API #21 field mapping. |
| data.updated_at | date-time | Contract schema | UserProfile.updated_at; query source unresolved | 3/4.1 | ISO-8601 per schema | Required by schema | No API #21 field mapping. |
| meta | object | Envelope schema | ApiEnvelope<T> | 4.1/4.2/4.3 | Object | Fields unspecified | No aggregate metadata is declared. |
| traceId | uuid | Envelope schema/current Study trace helper | Request trace context if wired | 4.1/4.2/4.3 | UUID | Required by reusable schema | API #21 runtime trace behavior is not verified. |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- Current [auth.py](../../../app/utils/auth.py) có helper xác thực Bearer/JWT, parse sub thành positive integer và yêu cầu role STUDENT.
- API #21 chưa có route gọi helper này; current helper behavior không phải endpoint runtime proof.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT | sub | Current helper parses numeric string to user ID | Endpoint #21 chưa xác nhận cách bind vào SQL. |
| JWT | roles | Current helper requires STUDENT | API #21 catalog cũng yêu cầu role=Student. |
| lesson_progress | user_id | Candidate equals authenticated user ID | /me intent and DB relation support the candidate; endpoint predicate remains SOURCE_REQUIRED. |

### 0.3. Check kết quả

- Theo contract, authentication failure trả HTTP 401 / DESIGN_AUTHENTICATION_REQUIRED.
- Theo contract, access/role denial trả HTTP 403 / DESIGN_ACCESS_DENIED.
- Không kết luận API #21 đang thực thi các checks trên; endpoint chưa wired.

## 1. Validate data input

### 1.1. Progress query selector

- Catalog ghi nguyên phrase course_id list hoặc aggregate?:string.
- Tên field, list serialization, kiểu từng course_id, optionality và semantics của aggregate đều SOURCE_REQUIRED.
- Không tự đặt enum, default, range, duplicate handling hoặc 422 condition; API #21 catalog không liệt kê 422.

## 2. Get thông tin

### 2.1. Candidate progress source

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| lesson_progress AS lp | user_id | Cột liên kết user theo DB design | Candidate scope predicate; endpoint-specific binding SOURCE_REQUIRED. |
| lesson_progress AS lp | lesson_id | Quan hệ tới lessons.id | Cột quan hệ; projection response chưa xác nhận. |
| lesson_progress AS lp | status | Trạng thái lesson progress | Enum values và ý nghĩa aggregate chưa canonical hóa. |
| lesson_progress AS lp | progress_percent | Phần trăm ở cấp lesson theo DB design | Không suy ra công thức tổng hợp hoặc response percentage. |
| lesson_progress AS lp | completed_at | Thời điểm lesson được đánh dấu hoàn thành | Có trong DB design; null/empty output chưa được xác định. |
| lessons AS l | id, course_id | Quan hệ từ lesson tới course | Chỉ dùng nếu aggregate cần course grouping; query API #21 chưa xác nhận. |
| courses AS c | id | Quan hệ course | API #20 nạp course riêng ở AC-13; không mặc định API #21 JOIN courses. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| lesson_progress AS lp | N/A | BASE — candidate source from DB design |
| lessons AS l | l.id = lp.lesson_id | Relationship in checked-in DB design; runtime join not verified. |
| courses AS c | c.id = l.course_id | Relationship in checked-in DB design; API #21 join need is SOURCE_REQUIRED. |

### 2.3. WHERE

- lp.user_id = authenticated user ID là candidate ownership predicate từ /me + Student semantics; API #21 source chưa xác nhận binding.
- Query course selector predicate là SOURCE_REQUIRED.
- Enrollment status, Course status, Lesson status và visibility filters của API #21 chưa được xác định.

### 2.4. GROUP/HAVING, ORDER BY and pagination

- Aggregate keys, formula, denominator, inclusion/exclusion rules and rounding: SOURCE_REQUIRED.
- ORDER BY: SOURCE_REQUIRED nếu endpoint trả collection.
- Pagination không được API #21 catalog khai báo.

## 3. Map result

- AC-13 cho biết client ghép Course từ API #20 với progress từ API #21 rồi hiển thị tiến độ; wire merge key chưa được nêu ở API #21.
- AC-18 gọi kết quả API #21 là aggregate progress theo user; không đưa công thức hoặc payload fields.
- API #37 là endpoint riêng cho course detail, với diagram mô tả aggregate lesson + quiz + assignment progress; không chuyển danh sách nguồn này thành API #21 behavior.
- API #38 là endpoint riêng cho achievements.
- Response data vẫn ApiEnvelope<UserProfile> theo catalog; progress-to-UserProfile mapping, empty progress and no-enrollment result remain SOURCE_REQUIRED.

## 4. Check result and return response

### 4.1. Thành công

- HTTP status = 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Response generic được giữ ApiEnvelope<UserProfile> theo catalog pending contract-owner resolution.

### 4.2. Authentication / authorization errors

- HTTP status = 401; businessCode = DESIGN_AUTHENTICATION_REQUIRED.
- HTTP status = 403; businessCode = DESIGN_ACCESS_DENIED.

### 4.3. System error

- HTTP status = 500; businessCode = DESIGN_INTERNAL_ERROR.
- Không trả raw database errors, stack traces hoặc internal details.

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
