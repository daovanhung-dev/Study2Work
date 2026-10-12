---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "38"
api_name: "Lấy achievement/badge nếu có"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft flow theo API catalog và AC-18. Achievement được DB guide mô tả là derived từ dữ liệu hiện có; award rule, input projection, query, filter semantics và pagination chưa được xác nhận. Các bảng bên dưới chỉ là candidate; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 0. Check quyền

### 0.1. Lấy principal

- Đọc Authorization header theo Bearer JWT contract.
- Xác thực token và yêu cầu Student role theo API catalog.
- Current shared auth helper chuẩn hóa JWT sub thành numeric user_id và kiểm tra Student role; API #38 chưa có route nên chưa gọi helper này.
- Dùng principal hiện tại làm scope cho route /me; không nhận user_id từ request.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Current authenticated principal | user_id | JWT sub theo current shared auth helper | Runtime helper evidence; API #38 chưa wire. |
| N/A — chưa xác định | N/A | Course enrollment/ownership/access predicate | AC-18 không chỉ định course access rule cho filter course_id. |

### 0.3. Check kết quả

- Nếu token thiếu hoặc không hợp lệ: trả 401 theo [06_Error.md](./06_Error.md).
- Nếu principal không có Student role hoặc access bị từ chối: contract có 403.
- Không suy ra access theo course chỉ từ việc course_id được truyền.
- Không thêm 404 hoặc business code ngoài catalog.

## 1. Validate data input

### 1.1. Validate course_id

- course_id là query parameter optional kiểu int64 theo catalog.
- Min/max, miền hợp lệ, parse failure và error mapping chưa được đặc tả.
- Catalog không liệt kê 422 cho API #38; không tự thêm 422 hoặc 400.

### 1.2. Filter semantics

- Nếu course_id có giá trị hợp lệ, filter theo course là intended query dimension.
- Không rõ achievement không gắn course có được đưa vào response khi course_id được truyền.
- Nếu course_id bị lược bỏ, phạm vi award toàn cục/course chưa được định nghĩa.

## 2. Get achievement đã mở khóa

### 2.1. Query matrix

| Query ID | Mục đích | Candidate input | Query status |
|---|---|---|---|
| Q1 | Tạo Page<Achievement> cho Student hiện tại | Dữ liệu progress/assessment hiện có | SOURCE_REQUIRED — chưa có award rule, source projection hoặc SQL được duyệt. |

### 2.2. Candidate read sources

DB design nói achievements được tính từ dữ liệu hiện có nhưng không chỉ định bảng hoặc field nào là điều kiện award. Những liên hệ sau chỉ là khả năng để owner xác nhận, không phải query đã chốt.

| Target table | Column candidate | Candidate purpose | Status |
|---|---|---|---|
| lesson_progress | user_id | Scope tiến độ theo Student. | DESIGN_ONLY candidate |
| lesson_progress | lesson_id | Nối tới lesson/course. | DESIGN_ONLY candidate |
| lesson_progress | status | Có thể là input của rule học tập. | Rule chưa xác nhận |
| lesson_progress | progress_percent | Có thể là input của rule hoàn thành. | Rule chưa xác nhận |
| lesson_progress | completed_at | Có thể là event time candidate. | Không xác nhận awarded_at source |
| lessons | id | Join candidate từ lesson_progress. | DESIGN_ONLY candidate |
| lessons | course_id | Course relation candidate. | Filter semantics chưa chốt |
| quiz_attempts | user_id | Scope attempt theo Student. | DESIGN_ONLY candidate |
| quiz_attempts | quiz_id | Nối tới quiz/course. | DESIGN_ONLY candidate |
| quiz_attempts | status | Có thể là input của rule assessment. | Rule chưa xác nhận |
| quiz_attempts | submitted_at | Event time candidate. | Không xác nhận awarded_at source |
| quiz_attempts | score | Có thể là input của rule assessment. | Threshold chưa xác nhận |
| quizzes | id | Join candidate từ quiz_attempts. | DESIGN_ONLY candidate |
| quizzes | course_id | Course relation candidate. | Filter semantics chưa chốt |
| assignment_submissions | user_id | Scope submission theo Student. | DESIGN_ONLY candidate |
| assignment_submissions | assignment_id | Nối tới assignment/course. | DESIGN_ONLY candidate |
| assignment_submissions | status | Có thể là input của rule submission. | Rule chưa xác nhận |
| assignment_submissions | submitted_at | Event time candidate. | Không xác nhận awarded_at source |
| assignment_submissions | score | Có thể là input của rule grading. | Threshold chưa xác nhận |
| assignments | id | Join candidate từ submission. | DESIGN_ONLY candidate |
| assignments | course_id | Course relation candidate. | Filter semantics chưa chốt |

> Candidate fields trên có trong DB guide/checked-in DDL làm design evidence. DDL không xác nhận live schema; một số FK cho phép NULL trong DDL dù guide mô tả bắt buộc.

### 2.3. JOIN candidates

| Target table | Join condition | Join type / status |
|---|---|---|
| lesson_progress AS lp | N/A | Candidate base input only |
| lessons AS l | l.id = lp.lesson_id | Candidate relation; query chưa chốt |
| quizzes AS q | q.id = quiz_attempts.quiz_id | Candidate relation; query chưa chốt |
| assignments AS a | a.id = assignment_submissions.assignment_id | Candidate relation; query chưa chốt |
| courses AS c | c.id = lessons.course_id / quizzes.course_id / assignments.course_id | Candidate scope; filter path chưa chốt |

### 2.4. WHERE and ordering

- Scope mọi record theo authenticated Student principal; exact query predicates chưa được duyệt.
- course_id, nếu có, dùng làm filter dimension; global-award inclusion chưa được chốt.
- Status/threshold rules để xác định achievement unlocked chưa được cung cấp.
- Sorting key, deterministic tie-break và pagination predicates chưa được đặc tả.
- Không tạo SQL hoặc giả định một physical achievements table.

## 3. Insert/Update thông tin

### 3.1. Target table

- N/A — API #38 là GET read-only.

### 3.2. Conditions

- N/A — không có mutation được khai báo.

### 3.3. Items update/insert

- N/A — không có insert/update mapping. Xem [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| N/A | N/A | Không có mutation parameters. |

## 4. Map response

### 4.1. Achievement item

- Catalog định nghĩa data.items[] theo Achievement.
- id = SOURCE_REQUIRED; không có achievement table hoặc deterministic derivation rule.
- code = SOURCE_REQUIRED; code registry/award definition chưa có.
- title = SOURCE_REQUIRED; title/localization source chưa có.
- awarded_at = SOURCE_REQUIRED; event timestamp không đồng nghĩa award timestamp nếu chưa có rule.
- course_id = SOURCE_REQUIRED; optional semantics và mapping từ course relation chưa có.

### 4.2. Pagination

- data.pagination.page, size, total và total_pages theo PageMeta schema trong catalog.
- Request không khai báo page/size; nguồn giá trị, default, giới hạn và cách đếm total cần xác nhận.
- Không dùng giá trị ví dụ trong [04_Response.md](./04_Response.md) làm default contract.

## 5. Check kết quả execute query

### 5.1. Thành công

- Khi query/source/projection được quyết định, trả HTTP 200 với DESIGN_RESOURCE_RETRIEVED.
- Success data giữ nguyên ApiEnvelope<Page<Achievement>> theo catalog.
- Empty Page behavior và pagination semantics chưa được đặc tả.

### 5.2. Lỗi hệ thống

- Lỗi hệ thống không được ánh xạ sang contract cụ thể trả 500 với DESIGN_INTERNAL_ERROR theo catalog.
- Error envelope tham chiếu [06_Error.md](./06_Error.md).

### 5.3. Lỗi xác thực hoặc quyền truy cập

- Authentication failure trả 401 với DESIGN_AUTHENTICATION_REQUIRED.
- Role/access denied trả 403 với DESIGN_ACCESS_DENIED.
- Điều kiện 403 theo course filter cần xác nhận.

### 5.4. Query validation

- Catalog không liệt kê 400 hoặc 422; parse/range behavior của course_id cần chốt qua contract.
- Không thêm status hoặc business code khi chưa cập nhật nguồn có thẩm quyền.
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
