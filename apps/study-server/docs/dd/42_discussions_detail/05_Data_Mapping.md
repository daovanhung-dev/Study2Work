---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "42"
api_name: "Tải lại thread thảo luận"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo approved catalog và AC-19. API #42 chưa có implementation/query được xác minh. Q1/Q2 là candidate đọc design-only. Các gate, order và page behavior được đánh dấu DERIVED.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Xác thực Bearer JWT và yêu cầu role Student theo API catalog.
- Lấy user_id từ JWT principal; không nhận user_id từ request.
- DERIVED: yêu cầu enrollment có user_id bằng principal, course_id bằng topic.course_id và status ACTIVE.
- DERIVED: chỉ cho đọc topic có status ACTIVE.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Bearer JWT | sub, roles | user_id dương; role STUDENT | Current Study helper precedent; API #42 chưa wired. |
| discussions AS root | id, course_id, parent_id, status | id=:discussion_id; parent_id IS NULL; status='ACTIVE' | Root/visible gate DERIVED. |
| enrollments AS e | user_id, course_id, status | e.user_id=:principal_id AND e.course_id=root.course_id AND e.status='ACTIVE' | Enrollment gate DERIVED, cần xác nhận. |

### 0.3. Check kết quả

- Thiếu/sai JWT: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Sai role, không có enrollment ACTIVE hoặc topic không ACTIVE: HTTP 403 DESIGN_ACCESS_DENIED theo đề xuất DERIVED.
- Không tồn tại topic gốc hoặc path ID trỏ tới comment: HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Không để lộ nội dung comment trước khi hoàn tất gate truy cập.

## 1. Validate data input

- Path discussion_id bắt buộc kiểu int64 theo catalog.
- Không có query parameter hoặc request body.
- Không có range/positivity rule trong catalog.
- Catalog không khai báo 422 cho API #42. Đề xuất DERIVED: path ID không parse được cũng trả 404 để không mở thêm business code; phải ghi đè framework default 422 nếu runtime cần.
- Không thêm 422 hoặc business code khác vào contract.

## 2. Get thông tin

### 2.1. Query

| Query ID | Mục đích | Candidate source | Status |
|---|---|---|---|
| Q1 | Resolve root discussion và topic author | discussions + users | DESIGN_ONLY candidate; title source thiếu. |
| Q2 | Lấy comments trực tiếp cùng author | discussions child rows + users | DESIGN_ONLY candidate; chỉ ACTIVE, không phân trang riêng. |
| Q3 | Kiểm tra quyền theo enrollment | enrollments | DERIVED candidate; status ACTIVE/policy cần xác nhận. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| discussions AS root | N/A | BASE |
| users AS author | author.id = root.user_id | Candidate author join; logical FK required, DDL nullable. |
| discussions AS child | child.parent_id = root.id | Candidate direct-child read. |
| users AS comment_author | comment_author.id = child.user_id | Candidate author join; logical FK required, DDL nullable. |
| enrollments AS e | e.course_id = root.course_id AND e.user_id = principal_id | DERIVED access existence check; e.status='ACTIVE'. |

### 2.3. WHERE

- Q1: root.id = :discussion_id.
- Q1: root.parent_id IS NULL; root status = 'ACTIVE' là visibility proposal DERIVED.
- Q2: child.parent_id = root.id.
- Q2: child.status = 'ACTIVE' là visibility proposal DERIVED.
- Q3: e.user_id = :principal_id AND e.course_id = root.course_id AND e.status = 'ACTIVE'.
- Nếu author không tồn tại hoặc FK NULL, không bỏ lặng lẽ thread/comment; xem là lỗi dữ liệu và trả 500 do response schema yêu cầu author.

### 2.4. ORDER BY

- Q1: một root duy nhất, không cần sort.
- Q2: child.created_at ASC, child.id ASC (DERIVED) để hiển thị cũ trước, mới sau và ổn định khi trùng timestamp.
- Không phân trang riêng comments vì contract không có cursor/limit.

## 3. Insert/Update thông tin

### 3.1. Target table

- N/A — API #42 chỉ đọc.

### 3.2. Conditions

- N/A — không có mutation.

### 3.3. Items update/insert

- N/A — không có INSERT/UPDATE. API #41 owns comment creation.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| discussion_id | Path parameter | Resolve root discussion. |
| principal_id | Student JWT | Dùng cho enrollment gate, không lấy từ request. |

## 4. Check kết quả execute query

### 4.1. Thành công

- Trả HTTP 200 và DESIGN_RESOURCE_RETRIEVED.
- Giữ ApiEnvelope<Page<Discussion>>.
- DERIVED: data.items có đúng một root thread; pagination page=1, size=1, total=1, total_pages=1.
- comments[] gồm tất cả child ACTIVE trực tiếp, theo created_at ASC rồi id ASC.
- Không trả count field/counter vì reusable schema không có field và DB không có cột counter.

### 4.2. Lỗi hệ thống

- Q1/Q2/author mapping/database failure: HTTP 500 DESIGN_INTERNAL_ERROR.
- Trả data=null, safe message, meta và traceId theo API guidelines.
- Không expose SQL, stack trace hoặc raw database detail.

### 4.3. Validate lỗi

- Path int64 invalid: đề xuất 404 DESIGN_RESOURCE_NOT_FOUND theo catalog; không thêm 422. Đây là DERIVED mapping do framework behavior chưa có source.
- Không có body/query validation.

### 4.4. Ngoài trường hợp trên

- Topic không tồn tại hoặc path ID không phải root: 404 DESIGN_RESOURCE_NOT_FOUND.
- Không có quyền theo enrollment/status: 403 DESIGN_ACCESS_DENIED.
- Nếu policy yêu cầu concealment, cần thay 403 bằng 404 nhưng vẫn phải theo code catalog.

## 5. Response source reconciliation

| Response field | Candidate source | Mapping | Status |
|---|---|---|---|
| Discussion id/course_id/content/status | discussions root row | Direct, content TEXT -> string | Candidate; course_id/status semantics need review. |
| Discussion title | N/A | No source | SOURCE_REQUIRED; do not derive from content. |
| Discussion author | users by root.user_id | UserSummary; omit avatar_url if NULL | Candidate; DDL FK nullable. |
| Comment id/content/created_at | discussions child row | Direct; content TEXT -> string; timestamp ISO-8601 | Candidate design mapping. |
| Comment discussion_id | child.parent_id | Direct logical parent ID | Candidate. |
| Comment author | users by child.user_id | UserSummary; omit avatar_url if NULL | Candidate; DDL FK nullable. |
| PageMeta | One root thread | Fixed 1/1/1/1 | DERIVED; catalog does not define detail-page values. |
| Trace ID | Request trace helper | UUID string | Shared envelope convention. |

## 6. Boundary with adjacent APIs

- API #39 lists root threads; API #42 returns one full thread. Both use the same Discussion/DiscussionComment projection.
- API #40 inserts a root; API #41 inserts a direct child; API #42 reloads the resulting thread.
- API #41 provisional decimal-string write mapping makes comment content a string on read. API #40 must use the same provisional mapping for root content.
- Keep counters derived from child rows only if needed; API #42 response currently has no count field and performs no write.
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


