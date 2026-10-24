---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "41"
api_name: "Thêm bình luận/trả lời"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo approved catalog và AC-19. API #41 chưa có implementation/query được xác minh. Các query/mapping dưới đây là đề xuất design-only; DERIVED là suy luận đơn giản để làm rõ flow, không phải runtime evidence.

## 0. Check quyền

### 0.1. Lấy principal

- Require Bearer JWT hợp lệ và role Student theo catalog.
- Dùng principal ID từ JWT; không nhận user_id trong path/body.
- Current Study helper app/utils/auth.py parse JWT subject thành user ID số và kiểm tra Student role cho route đã wired; API #41 chưa gọi helper.

### 0.2. Lấy topic cha và kiểm tra quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| discussions AS parent | id, parent_id | parent.id = :discussion_id AND parent.parent_id IS NULL | DERIVED: chỉ reply trực tiếp vào topic gốc; ID comment bị xem là resource không hợp lệ/không tìm thấy. |
| Current authenticated principal | user_id | Principal từ JWT | Identity source; không lấy từ request. |
| enrollments AS e | user_id, course_id, status | e.user_id = principal ID AND e.course_id = parent.course_id AND e.status = 'ACTIVE' | DERIVED access predicate dùng bảng/status đã có trong DDL; cần xác nhận policy. |
| discussions AS parent | status | parent.status = 'ACTIVE' | DERIVED để chỉ cho reply vào topic public/active; enum/visibility semantics cần xác nhận. |

### 0.3. Check kết quả

- JWT thiếu/không hợp lệ: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Không phải Student, không có enrollment ACTIVE, hoặc topic không ở trạng thái ACTIVE: HTTP 403 DESIGN_ACCESS_DENIED theo đề xuất DERIVED.
- Không tìm thấy topic được chỉ định: HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Việc phân biệt topic không tồn tại với topic ẩn/không được truy cập cần policy xác nhận; không thêm error code.

## 1. Validate data input

### 1.1. Validate discussion_id

- Path field bắt buộc kiểu int64 theo catalog.
- discussion_id được diễn giải là ID topic gốc; tạo child reply với parent_id bằng giá trị này (DERIVED).
- Không có min/max hoặc quy tắc cho phép reply vào một comment khác.

### 1.2. Validate content

- Body field bắt buộc kiểu int64 theo catalog.
- Không có length, blank, range, moderation hoặc content policy trong contract.
- Mapping candidate chuyển số nguyên sang chuỗi thập phân để lưu TEXT và trả DiscussionComment.content:string; phải được xác nhận do contract/schema/DDL khác kiểu.
- Không thêm quy tắc content ngoài required/type.

## 2. Get thông tin

### 2.1. Query matrix

| Query ID | Mục đích | Candidate source | Status |
|---|---|---|---|
| Q1 | Resolve topic cha, lấy course và author ID | discussions.id, course_id, user_id, parent_id, status | DERIVED; physical schema design-only; live schema chưa xác minh. |
| Q2 | Resolve quyền Student trên course | enrollments.user_id, course_id, status | DERIVED candidate: enrollment ACTIVE cho principal và parent.course_id; cần xác nhận status/policy. |
| Q3 | Lấy author summary nếu POST trả thread đã cập nhật | users.id, full_name, avatar_url | Candidate mapping; response read flow chưa được duyệt. |

### 2.2. Parent row projection

| Target table | Column candidate | Candidate purpose | Status |
|---|---|---|---|
| discussions AS parent | parent.id | Topic ID | ERD/DDL candidate |
| ↑ | parent.course_id | Course chứa topic | ERD required; DDL nullable |
| ↑ | parent.user_id | Topic author ID | ERD required; DDL nullable |
| ↑ | parent.parent_id | Xác định row là root topic | DERIVED; xử lý khi path ID trỏ comment cần xác nhận |
| ↑ | parent.status | Visibility/moderation state | Enum/policy chưa được định nghĩa |

### 2.3. JOIN / WHERE

- Candidate lookup condition: parent.id = :discussion_id AND parent.parent_id IS NULL.
- DERIVED course gate: tồn tại enrollment e với e.user_id = principal ID, e.course_id = parent.course_id và e.status = 'ACTIVE'.
- DERIVED visibility gate: parent.status = 'ACTIVE'; không có enum/policy nguồn để khẳng định ngoài đề xuất này.
- Candidate author lookup: users.id = :principal_user_id.
- Các gate trên là suy luận từ AC-19 precondition và column/status có sẵn trong DDL, chưa phải predicate được phê duyệt.

### 2.4. ORDER BY

- Parent lookup không cần sort.
- DERIVED: sau insert, nạp mọi child trực tiếp có status ACTIVE và sắp created_at ASC, id ASC, đúng thứ tự API #42 dùng khi reload thread.

## 3. Phán đoán trạng thái

- Nếu token và role hợp lệ, resolve topic trước khi insert.
- Nếu topic không tồn tại, dùng 404 DESIGN_RESOURCE_NOT_FOUND.
- Nếu Student không có enrollment ACTIVE hoặc topic không ACTIVE, trả 403 DESIGN_ACCESS_DENIED theo predicate DERIVED; policy cần xác nhận.
- Chỉ insert khi parent tồn tại và access check thành công.
- Không có status code 409 cho việc khóa/đóng topic trong API #41 catalog; không thêm code này.

## 4. Insert thông tin trong transaction

### 4.1. Target table

- Target candidate là discussions, theo ERD self-reference và AC-19 node INSERT Comment.
- Một reply được lưu thành row con: parent_id = discussion_id (DERIVED).
- course_id kế thừa từ parent để mọi row trong thread thuộc cùng course (DERIVED).
- user_id lấy từ Student principal.

### 4.2. Insert mapping

Xem [07_discussions_insert.md](./07_discussions_insert.md). Candidate values:

| Column | Candidate value | Evidence/status |
|---|---|---|
| id | Database-generated | BIGSERIAL trong checked-in DDL; live schema chưa xác minh. |
| course_id | parent.course_id | DERIVED; DDL nullable, logical guide yêu cầu. |
| user_id | Authenticated principal ID | JWT identity; DDL nullable, logical guide yêu cầu. |
| parent_id | discussion_id | DERIVED direct-child reply. |
| content | Decimal string của request integer | DERIVED proposal; DISCREPANCY với string/TEXT contract. |
| status | DDL default ACTIVE | Candidate only; enum/visibility policy chưa được xác nhận. |
| created_at | Server clock tại thời điểm insert | DERIVED; DDL NOT NULL, không có default. |
| updated_at | Cùng giá trị created_at | DERIVED; DDL NOT NULL, không có default. |

### 4.3. Transaction và counters

- Candidate mutation là một insert child row trong transaction.
- AC-19 ghi “update counters”, nhưng discussions, ERD và DDL không có counter field hoặc bảng riêng. Không thực hiện UPDATE lên column chưa được khai báo.
- Đề xuất DERIVED: nếu cần số lượng comment, tính từ child rows khi đọc thread; không lưu counter. Xác nhận giao diện/contract có cần counter hay không.
- Nếu sau này có counter storage được duyệt, insert và counter update phải nguyên tử. Hiện không có mapping để mô tả write đó.

## 5. Map response

### 5.1. Success envelope

- HTTP 201 và DESIGN_RESOURCE_CREATED.
- Giữ ApiEnvelope<Page<Discussion>> đúng catalog.
- DERIVED proposal: trả một item là parent thread sau insert, chứa mọi direct child comment ACTIVE theo created_at ASC, id ASC; metadata {page:1,size:1,total:1,total_pages:1}.
- AC-19 sau đó gọi API #42 để reload thread; response proposal của API #41 không thay thế bước reload này.

### 5.2. Discussion/comment projection

| Response field | Candidate source | Transform | Status |
|---|---|---|---|
| Root id, course_id, content, status | Parent discussions row | Direct candidate | Content/title/visibility issues remain. |
| Root title | No physical source | N/A | SOURCE_REQUIRED; DB guide/ERD/DDL omit column. |
| Root author | users via parent.user_id | UserSummary | Candidate; query and null policy unconfirmed. |
| comments[].id | Direct ACTIVE child discussions.id | Direct | Candidate; include all direct ACTIVE children after insert, ordered by created_at ASC, id ASC. |
| comments[].discussion_id | Child parent_id | Map physical parent ID to logical field | DERIVED; direct child only. |
| comments[].content | Child discussions.content | Decimal string conversion candidate | DISCREPANCY; confirmation required. |
| comments[].author | users via child.user_id | UserSummary | Candidate; required profile lookup not defined. |
| comments[].created_at | Child created_at | ISO-8601 | Server-clock source is DERIVED; order with id ASC tie-break. |
| pagination | Single updated-thread response | Fixed one-item page candidate | DERIVED; no response page policy. |

### 5.3. Error response

- Use only catalog codes listed in [06_Error.md](./06_Error.md).
- Include shared meta and traceId behavior from API guidelines.
- No endpoint-specific message ID is defined.

## 6. Reconciliation boundaries

- API #40 creates a root topic; API #41 creates a child; API #42 reloads the topic plus children.
- Reuse the database self-reference only as design evidence. It does not prove a live table or index.
- Do not copy review-specific visibility/order behavior from API #10 into AC-19 without approval.
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

