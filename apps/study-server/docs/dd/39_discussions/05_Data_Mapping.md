---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "39"
api_name: "Lấy danh sách thread"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo approved API catalog và AC-19. API #39 chưa có implementation/query được xác minh. Các truy vấn dưới đây là query matrix/candidate mapping để chỉ ra nguồn và khoảng trống, không phải SQL đã được duyệt.

## 0. Check quyền

### 0.1. Lấy principal

- Đọc Authorization header theo Bearer JWT contract.
- Yêu cầu token hợp lệ và Student role theo API catalog.
- Dùng principal từ token; không nhận user ID từ request.
- Current shared auth helper có Student guard cho các route đã wire; API #39 chưa gọi helper này vì chưa có route.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Current authenticated principal | user_id | Principal lấy từ Bearer JWT | Expected contract scope; API #39 chưa wire. |
| N/A — chưa xác định | N/A | Quyền tham gia course/discussion | AC-19 nêu precondition nhưng không cung cấp access predicate. |

### 0.3. Check kết quả

- Nếu token thiếu hoặc không hợp lệ: trả 401 theo [06_Error.md](./06_Error.md).
- Nếu role không phải Student hoặc access bị từ chối: contract có 403.
- Không suy ra course enrollment/ownership rule từ course_id.
- Không thêm error code ngoài catalog.

## 1. Validate data input

### 1.1. Validate course_id

- course_id là query parameter optional kiểu int64 theo catalog.
- Miền giá trị và parse failure behavior chưa được đặc tả.
- Nếu có course_id, đây là candidate filter dimension; access predicate vẫn chưa rõ.
- Catalog không khai báo 400/422 cho API #39.

### 1.2. Validate page

- page là query parameter optional kiểu int32 theo catalog.
- Giá trị tối thiểu/tối đa, default và malformed-value mapping chưa được đặc tả.
- Response yêu cầu PageMeta nhưng không thể suy ra default page từ schema.

### 1.3. Validate sort

- sort là query parameter optional kiểu string theo catalog.
- Allowlist field, direction syntax, default sort và deterministic tie-break chưa được đặc tả.
- Không tạo ORDER BY từ input tùy ý hoặc tự chọn sort field.
- Catalog không khai báo 400/422 cho API #39.

## 2. Get discussion thread list

### 2.1. Query matrix

| Query ID | Mục đích | Candidate source | Query status |
|---|---|---|---|
| Q1 | Lấy page Discussion theo API #39 | discussions và users | DESIGN_ONLY candidate; predicates, projection và paging chưa chốt. |
| Q2 | Lấy tổng số row cho PageMeta.total | discussions | DESIGN_ONLY candidate; phải dùng cùng scope/filter như Q1 khi được quyết định. |

### 2.2. Candidate projection

| Target table | Column candidate | Candidate purpose | Status |
|---|---|---|---|
| discussions AS d | d.id | Discussion ID | ERD/DDL design evidence |
| discussions AS d | d.course_id | Course relation/filter | ERD required; checked-in DDL nullable |
| discussions AS d | d.user_id | Author relation | ERD required; checked-in DDL nullable |
| discussions AS d | d.parent_id | Phân biệt root và reply | Nullable self-reference theo ERD/DDL |
| discussions AS d | d.content | Discussion content | TEXT NOT NULL trong checked-in DDL |
| discussions AS d | d.status | Logical DiscussionStatus candidate | DB.sql default ACTIVE; enum/visibility semantics chưa chốt |
| discussions AS d | d.created_at | Thread timestamp candidate | Timestamp field trong ERD/DDL |
| users AS u | u.id | Author ID | DB.sql design evidence |
| users AS u | u.full_name | Author display name | VARCHAR(150) NOT NULL trong DB.sql |
| users AS u | u.avatar_url | Optional author avatar | TEXT NULL trong DB.sql |
| discussions AS c | c.id | Comment ID candidate | Chỉ dùng nếu list response bao gồm comments |
| discussions AS c | c.parent_id | Parent discussion ID candidate | Map sang DiscussionComment.discussion_id |
| discussions AS c | c.content | Comment content candidate | TEXT NOT NULL trong checked-in DDL |
| discussions AS c | c.user_id | Comment author relation candidate | Nullable trong checked-in DDL |
| discussions AS c | c.created_at | Comment timestamp candidate | Chỉ dùng nếu list response bao gồm comments |
| users AS cu | cu.id | Comment author ID candidate | Join candidate qua c.user_id |
| users AS cu | cu.full_name | Comment author name candidate | Join candidate qua c.user_id |
| users AS cu | cu.avatar_url | Optional comment author avatar | Join candidate qua c.user_id |

> discussions.title không tồn tại trong ERD/checked-in DDL. Không map title = content và không tạo cột trong DD.

### 2.3. JOIN candidates

| Target table | Join condition | Join type / status |
|---|---|---|
| discussions AS d | N/A | Candidate base row |
| users AS u | u.id = d.user_id | Author projection candidate; DDL FK nullable |
| discussions AS c | c.parent_id = d.id | Child rows only if API #39 includes comments; unresolved |
| users AS cu | cu.id = c.user_id | Comment author only if comments are included; unresolved |

### 2.4. WHERE candidates

- d.course_id = :course_id chỉ khi query course_id được truyền.
- d.parent_id IS NULL là candidate root-thread filter theo DB guide; API #39 predicate cần xác nhận.
- Visibility predicate chưa được chốt; status = ACTIVE chỉ là candidate, không được coi là approved.
- Student participation/access predicate chưa được cung cấp.
- Nếu course_id vắng mặt, phạm vi course được phép đọc chưa được xác định.

### 2.5. ORDER BY

- sort có mặt trong contract nhưng allowlist, direction, default và tie-break chưa có nguồn.
- Không chốt thứ tự mặc định hoặc dùng raw sort trong SQL.

### 2.6. Pagination

- page là request input được catalog khai báo.
- PageMeta.size là response field nhưng catalog không khai báo request size.
- Page size, page default/range, total_pages formula và empty/out-of-range behavior cần được xác nhận.
- Count query phải áp dụng cùng scope/filter với list query sau khi các predicate được chốt.

## 3. Insert/Update thông tin

### 3.1. Target table

- N/A — API #39 là GET read-only.

### 3.2. Conditions

- N/A — không có mutation được khai báo.

### 3.3. Items update/insert

- N/A — không có insert/update mapping. Xem [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| N/A | N/A | API #39 không có mutation parameters. |

## 4. Map response

### 4.1. Discussion item

- data.items[].id lấy từ candidate discussions.id.
- data.items[].course_id lấy từ candidate discussions.course_id; DDL nullable trong khi contract required.
- data.items[].title là SOURCE_REQUIRED vì không có discussions.title; không lấy từ content.
- data.items[].content lấy từ candidate discussions.content.
- data.items[].author.id lấy từ users.id qua discussions.user_id nếu join được xác nhận.
- data.items[].author.full_name lấy từ users.full_name nếu join được xác nhận.
- data.items[].author.avatar_url lấy từ users.avatar_url; contract cho phép optional URI.
- data.items[].status lấy từ discussions.status candidate; enum values và visibility semantics chưa chốt.
- data.items[].comments[] có schema theo catalog nhưng việc API #39 load child rows cần xác nhận với API #42.

### 4.2. Comment item

- data.items[].comments[].id lấy từ candidate child discussions.id.
- data.items[].comments[].discussion_id map từ candidate child discussions.parent_id.
- data.items[].comments[].content lấy từ candidate child discussions.content.
- data.items[].comments[].author cần join child discussions.user_id tới users; inclusion trong list còn mở.
- data.items[].comments[].created_at lấy từ candidate child discussions.created_at; inclusion trong list còn mở.

### 4.3. Pagination

- data.pagination.page, size, total, total_pages theo PageMeta schema của catalog.
- page nhận query input nếu được truyền; default và invalid-value behavior chưa chốt.
- size không có query input trong catalog; không tự thêm size hoặc page_size.
- total cần count cùng scope/filter với Q1.
- total_pages phụ thuộc page size chưa được quyết định.

## 5. Check kết quả execute query

### 5.1. Thành công

- Trả HTTP 200 với DESIGN_RESOURCE_RETRIEVED theo API catalog.
- Giữ response contract ApiEnvelope<Page<Discussion>>.
- Empty page shape và pagination values chưa được đặc tả; không gán default trong DD.

### 5.2. Lỗi xác thực hoặc quyền truy cập

- Authentication failure trả 401 với DESIGN_AUTHENTICATION_REQUIRED.
- Student role/access denied trả 403 với DESIGN_ACCESS_DENIED.
- Điều kiện course access cụ thể cần được xác nhận.

### 5.3. Lỗi hệ thống

- Lỗi nội bộ không có mapping cụ thể trả 500 với DESIGN_INTERNAL_ERROR.
- Error envelope tham chiếu [06_Error.md](./06_Error.md).

### 5.4. Query validation

- Catalog không liệt kê 400/422.
- Parse/range failure cho course_id, page và giá trị sort cần được quyết định trong contract.
- Không thêm status hoặc business code ngoài catalog.
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

