---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "37"
api_name: "Lấy tiến độ chi tiết course"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft flow. Các bước đọc và mapping bên dưới là khung thiết kế theo AC-18; query predicates, aggregation và response projection chưa được xác nhận. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 0. Check quyền

### 0.1. Lấy principal

- Đọc Bearer JWT từ Authorization header theo contract.
- Xác thực token và yêu cầu role Student theo API catalog.
- Lấy identity của principal đã xác thực để giới hạn dữ liệu của route /me; tên claim và mapping tới user ID chưa được endpoint contract xác nhận.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| N/A — chưa xác định | N/A | Enrollment/ownership/course visibility predicate chưa được chốt. | Không giả định rằng có enrollment là điều kiện duy nhất. |

### 0.3. Check kết quả

- Nếu token thiếu hoặc không hợp lệ: trả 401 theo [06_Error.md](./06_Error.md).
- Nếu principal không có Student role hoặc không có access: contract có 403; predicate access cần xác nhận.
- Phân biệt access denied với resource not found chưa được chốt; xem câu hỏi Q-05.

## 1. Validate data input

- Nhận course_id từ path theo kiểu int64 bắt buộc trong [03_Request.md](./03_Request.md).
- Quy tắc domain, range, parse failure và error mapping chưa có trong catalog.
- Catalog không liệt kê 422 cho API #37; không tự thêm error code mới.

## 2. Get thông tin

### 2.1. Query candidates

Các nguồn dưới đây là candidate read sets, không phải SQL đã duyệt hoặc query runtime.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| lesson_progress AS lp | user_id | Gắn candidate lesson progress với user hiện tại. | Predicate/filter chưa chốt. |
| ↑ | lesson_id | Quan hệ tới lesson. | Join candidate. |
| ↑ | status | Candidate lesson state. | Semantics chưa canonical hóa. |
| ↑ | progress_percent | Candidate lesson progress value. | Không phải công thức course progress. |
| ↑ | last_accessed_at | Candidate activity timestamp. | Có được trả về hay không chưa rõ. |
| ↑ | completed_at | Candidate completion timestamp. | Completion rule chưa chốt. |
| lessons AS l | id | Join key từ lesson_progress.lesson_id. | Candidate join. |
| ↑ | course_id | Candidate scope theo course_id. | Course visibility filter chưa chốt. |
| quizzes AS q | id | Join candidate quiz attempts tới quiz. | Candidate join. |
| ↑ | course_id | Candidate scope theo course_id. | Quiz inclusion rule chưa chốt. |
| quiz_attempts AS qa | user_id | Candidate attempt ownership. | Principal mapping/filter chưa chốt. |
| ↑ | quiz_id | Join key tới quizzes.id. | Candidate join. |
| ↑ | submitted_at | Candidate attempt completion marker. | Attempt selection/status policy chưa chốt. |
| ↑ | score | Candidate score. | Inclusion/weight/visibility chưa chốt. |
| ↑ | status | Candidate attempt state. | Status values chưa đầy đủ. |
| assignments AS a | id | Join candidate submissions tới assignment. | Candidate join. |
| ↑ | course_id | Candidate scope theo course_id. | Assignment inclusion rule chưa chốt. |
| assignment_submissions AS s | user_id | Candidate submission ownership. | Principal mapping/filter chưa chốt. |
| ↑ | assignment_id | Join key tới assignments.id. | Candidate join. |
| ↑ | submitted_at | Candidate submission timestamp. | Submission selection policy chưa chốt. |
| ↑ | score | Candidate grade. | Inclusion/weight/visibility chưa chốt. |
| ↑ | status | Candidate submission state. | Status values chưa đầy đủ. |

### 2.2. JOIN candidates

| Target table | Join condition | Join type |
|---|---|---|
| lesson_progress AS lp | N/A | BASE candidate |
| lessons AS l | l.id = lp.lesson_id | JOIN type and null behavior TBD |
| courses AS c | c.id = l.course_id | JOIN type and access predicate TBD |
| quizzes AS q | q.course_id = course_id | Relation candidate; exact query TBD |
| quiz_attempts AS qa | qa.quiz_id = q.id | JOIN type and user predicate TBD |
| assignments AS a | a.course_id = course_id | Relation candidate; exact query TBD |
| assignment_submissions AS s | s.assignment_id = a.id | JOIN type and user predicate TBD |

### 2.3. WHERE

- User identity predicate must bind reads to authenticated principal; physical key source and exact condition need confirmation.
- course_id scope must bind to the requested course; exact existence/access filtering needs confirmation.
- Lesson, quiz, assignment and submission status filters are not defined.
- No executable SQL or parameter binding is specified by this DD.

### 2.4. ORDER BY

- Chưa được đặc tả; không áp dụng sort mặc định trong DD này.

### 2.5. Aggregate and projection

- AC-18 names lesson + quiz + assignment progress as aggregate inputs.
- Formula, denominator, weighting, status interpretation, rounding and incomplete-data policy are SOURCE_REQUIRED.
- No course_progress table is modeled in DB_UNICA_ERD; this DD does not add one.
- Candidate source fields do not establish the endpoint response schema.
- Multi-attempt quiz policy and multi-submission assignment policy are SOURCE_REQUIRED.

## 3. Insert/Update thông tin

### 3.1. Target table

- N/A — GET read-only.

### 3.2. Conditions

- N/A — không có mutation condition.

### 3.3. Items update/insert

- N/A — không có insert/update mapping. Xem [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| N/A | N/A | Không có mutation parameters. |

## 4. Check kết quả execute query

### 4.1. Thành công

- Khi data source và output contract được quyết định, trả HTTP 200 với DESIGN_RESOURCE_RETRIEVED.
- Catalog response type hiện tại là ApiEnvelope<UserProfile>.
- Mapping thực tế từ dữ liệu progress tới data chưa thể hoàn tất do response gap trong [04_Response.md](./04_Response.md).

### 4.2. Lỗi hệ thống

- Lỗi không xử lý được trả HTTP 500 với DESIGN_INTERNAL_ERROR theo catalog.
- Chi tiết client-safe error envelope tham chiếu [06_Error.md](./06_Error.md).

### 4.3. Validate lỗi

- Catalog không khai báo business validation code cho path parse/range của API #37.
- Không chốt status/code cho invalid course_id; xem Q-07 trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

### 4.4. Ngoài trường hợp trên

- Không định nghĩa nhánh ngoài contract.
- Không thêm status hoặc business code chưa có trong API catalog.

---
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
