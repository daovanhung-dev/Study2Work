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

1. Xác thực Bearer và role Mentor.
2. Parse `course_id:int64`; không tự thêm positivity rule.
3. Đọc course trong authorization scope; direct-owner legacy predicate chỉ là candidate.
4. Sau khi scope được kiểm tra, đọc active enrollments; không dispatch notification.
5. Đối chiếu response: `Page<Course>` không khớp roster; không tạo mapping giả.
6. Trả đúng catalog error codes; framework path parsing và middleware chưa được API #62 xác nhận.

### Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Nhận request](#step-1-nhan-request)
- [2. Course lookup/scope](#step-2-course-lookup-scope)
- [3. Enrollment roster](#step-3-enrollment-roster)
- [4. Response/pagination](#step-4-response-pagination)
- [5. Return/error](#step-5-return-error)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Actor

- Bearer JWT và role `MENTOR` là yêu cầu DIRECT từ catalog.
- Helper Study hiện chỉ hỗ trợ Student; không khẳng định helper này phân quyền được cho Mentor.
- Claim Mentor và ánh xạ identity numeric/UUID là SOURCE_REQUIRED.

### 0.2. Course scope

- AC-25 yêu cầu Mentor có quyền gửi thông báo tới learner trong course.
- Legacy `courses.mentor_id = authenticated Mentor ID` chỉ là candidate direct-owner; relation legacy đã kiểm tra không biểu diễn course được phân công.
- Không trả roster trước khi kiểm tra scope; thứ tự 403/404 cần quyết định về quyền riêng tư.

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles` | Phải có `MENTOR` | Role DIRECT; chưa có guard. |
| Legacy `courses` | `mentor_id` | Candidate bằng Mentor ID đã xác thực | Chỉ DERIVED; claim/key chưa rõ. |
| Course assignment | N/A | Chưa có relation được duyệt | SOURCE_REQUIRED. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

| Field | Source | Use | Rule/status |
|---|---|---|---|
| `course_id` | Path int64 bắt buộc | Q1 lookup và Q2 lọc course | Type DIRECT; chưa quy định range/giá trị dương. |
| Query/body | Catalog không khai báo | None | Không thêm page/size. |

Catalog không có mã lỗi riêng cho path sai định dạng hoặc tràn int64 của API #62. Không thêm 422.

<a id="step-2-course-lookup-scope"></a>

## 2. Course lookup/scope

### 2.1. Q1 — logical course lookup

| Target | Field | Purpose | Evidence/status |
|---|---|---|---|
| Course | `id` | Khớp `course_id` | Legacy BIGINT candidate; xung đột với UUID của V1-PILOT. |
| Course | Owner/assignment | Xác thực Mentor scope | Quyền là DIRECT theo AC-25; predicate vật lý SOURCE_REQUIRED. |
| Course | Trạng thái vòng đời | Quy định hành vi với course archived/draft | Diagram không nói; không tự thêm filter. |

Điều kiện candidate legacy: `courses.id = :course_id`; `courses.mentor_id = :mentor_id`. Course không tồn tại → candidate 404. Course tồn tại nhưng ngoài scope đã duyệt → catalog 403, còn phụ thuộc xác nhận thứ tự kiểm tra/quyền riêng tư. Đây chưa phải SQL runtime được duyệt.

<a id="step-3-enrollment-roster"></a>

## 3. Enrollment roster

### 3.1. Q2 — legacy query candidate

| Target table | Column | Use | Evidence/status |
|---|---|---|---|
| `enrollments` | `course_id` | Khớp path course | Legacy BIGINT; nullable trong DDL đã kiểm tra. |
| `enrollments` | `user_id` | Join learner | Legacy BIGINT; nullable trong DDL đã kiểm tra. |
| `enrollments` | `status` | Predicate enrollment active | Diagram nói active; `ACTIVE` từ default legacy là DERIVED. |
| `enrollments` | `enrolled_at` | Có thể dùng để sắp xếp ổn định | Catalog không quy định sort; chưa sắp xếp. |
| `users` | `id` | Candidate UserSummary ID | Legacy BIGINT; pilot mapping khác. |
| `users` | `full_name` | Candidate tên hiển thị | Bắt buộc trong legacy; projection riêng tư còn mở. |
| `users` | `avatar_url` | Candidate avatar optional | Legacy nullable; quy tắc hiển thị còn mở. |
| `users` | `role` | Candidate lọc role Student | `STUDENT` suy ra từ endpoint/AC; DERIVED. |

Nếu schema legacy được duyệt, đây là query read-only candidate cho response `Page<UserSummary>` đã được sửa:

```sql
SELECT DISTINCT u.id, u.full_name, u.avatar_url
FROM enrollments AS e
JOIN users AS u ON u.id = e.user_id
WHERE e.course_id = :course_id
  AND e.status = 'ACTIVE'
  AND u.role = 'STUDENT';
```

Query này không thể tạo `Course[]` theo catalog hiện tại và chưa phải SQL production được duyệt. Legacy DDL cho phép reference NULL và không có unique key `(course_id,user_id)`. Inner join sẽ bỏ các reference không hợp lệ; `DISTINCT` là đề xuất DERIVED để tránh hiện cùng người nhận nhiều lần. Cách xử lý orphan và grain đếm còn mở.

V1-PILOT nối UUID `course_enrollments.learner_id`/`course_version_id` qua `course_versions.course_id` tới UUID `courses.id`; learner identity nằm trong `learner_profiles`. Status là `ENROLLED|IN_PROGRESS|COMPLETED`, khác `ACTIVE` của legacy. Không join ngầm hai model.

### 3.2. Q3 — count/pagination

- `PageMeta.total` phụ thuộc grain của response: số Course hay số người nhận duy nhất.
- Không có query page/size; size/default/max/order/offset và cách lấy trang tiếp theo là SOURCE_REQUIRED.
- Nếu contract `Page<UserSummary>` và query phân trang được duyệt, hãy đếm learner đủ điều kiện duy nhất bằng cùng predicate Q2. Không đếm enrollment rows khi chưa được duyệt.

<a id="step-4-response-pagination"></a>

## 4. Response/pagination

- Giữ `ApiEnvelope<Page<Course>>` theo catalog.
- Toàn bộ field Course/PageMeta được liệt kê trong [04_Response.md](./04_Response.md).
- Query enrollment trả learner candidate, không trả Course row: `DISCREPANCY / SOURCE_REQUIRED`; không lặp Course thành một item cho mỗi student.
- `Page<UserSummary>` chỉ là đề xuất sửa contract ở mức DERIVED. `id`, `full_name`, `avatar_url?` là field User candidate từ legacy.
- Roster rỗng trả 200 với page rỗng là đề xuất; số liệu/default metadata cần xác nhận.

<a id="step-5-return-error"></a>

## 5. Return/error

- Thành công trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED`.
- Course không tồn tại candidate map sang 404; sai role/ngoài quyền candidate map sang 403.
- Roster rỗng là collection thành công theo đề xuất DERIVED, không phải resource không tồn tại.
- Lỗi query/projection ngoài dự kiến map sang 500 theo catalog.
- Không thêm 422, 409 hoặc 503; #62 không gọi dịch vụ gửi bên ngoài.
- Guideline yêu cầu error `data:null`; helper hiện tại mặc định `{}` và route chưa nằm trong allowlist. Đây chỉ là discrepancy khi wiring trong tương lai.

## Request Usage Matrix

| Request item | Source | Mapping step | Query use | Gap |
|---|---|---|---|---|
| Authorization | Bearer JWT | 0.1 | Principal cho scope | Guard/claim Mentor chưa rõ. |
| `course_id` | Path int64 | 1 | Q1 và Q2 | Xung đột ID giữa legacy/pilot. |
| Query/body | None | N/A | None | Không có input phân trang. |

## Query Matrix

| Query | Type | Candidate base/join | Predicate | Output/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses` | `id=:course_id`; Mentor scope đã duyệt | Direct-owner chỉ là candidate DERIVED. |
| Q2 | SELECT DISTINCT | Legacy `enrollments` JOIN `users` | Khớp course; candidate ACTIVE + STUDENT | Roster candidate xung đột response Course. |
| Q3 | COUNT DISTINCT | Cùng roster candidate | Cùng scope/active predicate | SOURCE_REQUIRED đến khi duyệt item grain và phân trang. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Tra cứu chỉ đọc | Không INSERT/UPDATE/DELETE | `N/A — API chỉ đọc`; #63 sở hữu ghi/gửi. |

## Response Source Matrix

| Response field/group | Contract | Candidate source | Status |
|---|---|---|---|
| `data.items[]` | `Course[]` | Không map được từ learner rows | `DISCREPANCY / SOURCE_REQUIRED`. |
| Field của Course item | Course schema | `courses` biểu diễn course, không phải người nhận | Shape DIRECT; lệch ngữ nghĩa. |
| `data.pagination` | PageMeta | Chưa duyệt page/size/default/grain đếm | SOURCE_REQUIRED. |
| `UserSummary` đề xuất | id/full_name/avatar_url | Legacy users qua enrollments | Chỉ là đề xuất sửa contract DERIVED. |
| `meta`, `traceId` | Quy ước envelope | Helper dùng chung | Endpoint chưa có runtime. |

## Mutation / DB mapping

N/A — API #62 chỉ đọc; không có mapping ghi hoặc định nghĩa table mới.
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
