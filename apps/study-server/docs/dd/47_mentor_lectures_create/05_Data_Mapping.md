---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Xác thực Bearer JWT và role Mentor.
1. Parse path/body; kiểm tra title tối đa 200 theo legacy candidate; giữ asset_refs opaque.
2. Đọc course theo ID; kiểm tra candidate direct owner bằng principal Mentor.
3. Bắt đầu transaction và INSERT một dòng lessons candidate.
4. Đọc lại RETURNING row; asset resolver chưa có nên chưa thể tạo đầy đủ assets[].
5. Chỉ commit/trả 201 khi mọi field Lecture bắt buộc có nguồn mapping đã được duyệt.
~~~

## Request Usage Matrix

| Request field | Source | Validate | Query/mutation usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header | Bearer JWT hợp lệ; role Mentor | Principal dùng cho candidate owner check; không nhận mentor ID từ client | Không trả token/claims | Mentor guard và identity mapping chưa có source |
| course_id | Path | Parse int64; không thêm positive-only rule | Q1 c.id; M1 lessons.course_id | data.course_id | Legacy BIGINT/pilot UUID và live schema chưa chốt |
| title | Body | Required string; max 200 là DERIVED từ legacy VARCHAR(200) | M1 lessons.name | data.title | Không suy ra min/trim |
| content | Body | Required int64 | M1 lessons.content nhận decimal-string candidate | data.content:string? | DISCREPANCY về meaning/type |
| asset refs | Body catalog label | Required string; không parse trước khi có format | Không có Q/M committed | data.assets[] | SOURCE_REQUIRED; provisional wire key asset_refs cần confirm |
| order | Body | Required int32; không thêm range | M1 lessons.sort_order | data.order | Legacy INT candidate |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Alias | Column | JOIN | WHERE | ORDER | Pagination | Result | Branch / status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Tìm course theo path | SELECT | courses | c | c.id | N/A | c.id = :course_id | N/A | N/A | candidate_course | Không có row → candidate 404 |
| Q1 | Đọc direct owner candidate | SELECT | courses | c | c.mentor_id | N/A | c.id = :course_id | N/A | N/A | candidate_course | So sánh với principal; assignment chưa thể xét |
| Q2 | Resolve asset refs | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có source ID/metadata lookup; SOURCE_REQUIRED |

Q1 candidate SQL, chỉ dùng nếu legacy schema được xác nhận:

~~~sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :course_id;
~~~

- Không thêm c.status = PUBLISHED: AC-21 là luồng Mentor tạo lecture.
- Nếu Q1 không có course: candidate 404.
- Nếu có course nhưng mentor_id khác principal: candidate 403.
- Nếu course được phân công qua relation khác: chưa có nguồn; không giả lập quan hệ.

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Target column | Value source | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | course_id | Path course_id | 07_lessons_insert.md | Cùng transaction với các field M1 | Rollback khi lỗi; catalog 500 cho lỗi hệ thống |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | name | Request title | 07_lessons_insert.md | Cùng transaction với các field M1 | Title > 200 bị 422 theo giới hạn DB candidate |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | content | Decimal string từ request content | 07_lessons_insert.md | Cùng transaction với các field M1 | Chỉ candidate DERIVED; meaning cần xác nhận |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | sort_order | Request order | 07_lessons_insert.md | Cùng transaction với các field M1 | Không áp thêm quy tắc thứ tự |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | created_at | CURRENT_TIMESTAMP | 07_lessons_insert.md | Cùng transaction với các field M1 | Legacy DDL không có default; live schema chưa xác minh |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | updated_at | CURRENT_TIMESTAMP | 07_lessons_insert.md | Cùng transaction với các field M1 | Dùng cùng transaction timestamp candidate |
| M1 | INSERT | lessons candidate | Q1 course tồn tại và direct-owner candidate check đạt | status | Bỏ khỏi INSERT để nhận default DRAFT | 07_lessons_insert.md | Cùng transaction với các field M1 | Default/enum là candidate; cần xác nhận |
| M2 | Chưa xác định | N/A | Asset resolver/format không có | N/A | N/A | N/A | N/A | Không tạo resources/uploads mutation giả; SOURCE_REQUIRED |

Candidate insert statement:

~~~sql
INSERT INTO lessons (
    course_id,
    name,
    content,
    sort_order,
    created_at,
    updated_at
)
VALUES (
    :course_id,
    :title,
    :content_text_candidate,
    :order,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING id, course_id, name, content, sort_order, status, created_at, updated_at;
~~~

status được bỏ khỏi INSERT để nhận default DRAFT chỉ khi legacy DDL là schema được duyệt. INSERT chưa ghi asset reference vì contract format và metadata resolver chưa có nguồn.

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty/omit rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Branch constant | API outcome | 5 | true on success | N/A | Direct envelope convention |
| businessCode | string | Contract constant | Catalog #47 | 5 | DESIGN_RESOURCE_CREATED | N/A | Direct |
| message | string | Application | Application | 5 | Safe localized message | Text not specified | N/A |
| data.id | int64 | INSERT result | lessons.id | 4 | Direct | N/A | Legacy candidate |
| data.course_id | int64 | INSERT result | lessons.course_id | 4 | Direct | N/A | Legacy candidate |
| data.title | string | INSERT result alias | lessons.name | 4 | name → title | N/A | Legacy candidate |
| data.content | string? | INSERT result | lessons.content | 4 | Candidate decimal string | Omit if DB NULL only if optional omission is approved | Request/response type conflict |
| data.assets[] | UploadAsset[] | Unresolved source | N/A | Pending | Resolve each ref to complete UploadAsset | No null/empty fallback defined | SOURCE_REQUIRED; required response field |
| data.assets[].id | int64 | Unresolved source | N/A | Pending | N/A | N/A | API #34 ID generation/lookup unknown |
| data.assets[].name | string | Unresolved source | N/A | Pending | N/A | N/A | No legacy metadata relation |
| data.assets[].url | uri | Unresolved source | N/A | Pending | N/A | N/A | Storage URL policy unknown |
| data.assets[].content_type | string | Unresolved source | N/A | Pending | N/A | N/A | MIME source unknown |
| data.assets[].size_bytes | int64 | Unresolved source | N/A | Pending | N/A | N/A | Size metadata source unknown |
| data.assets[].status | UploadStatus | Unresolved source | N/A | Pending | N/A | N/A | Enum/persistence unknown |
| data.order | int32 | INSERT result alias | lessons.sort_order | 4 | sort_order → order | N/A | Legacy candidate |
| data.status | LessonStatus | INSERT result/default | lessons.status | 4 | Candidate DRAFT default | N/A | Enum values unknown |
| meta | object | Envelope default | N/A | 5 | {} | {} | API guidelines |
| traceId | uuid | Request context | Trace helper | 5 | Propagate trace | Always present | API #47 route absent |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Dùng Bearer JWT và guard Mentor được duyệt; current Study helper chỉ có Student guard.
- Lấy principal từ token, không nhận owner ID từ request.
- Candidate ownership chỉ kiểm tra direct owner theo API #46; assignment relation và identity mapping cần xác nhận.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | roles | Phải có Mentor role | Catalog direct; runtime Mentor guard chưa có |
| courses AS c | c.id | Bằng path course_id | Legacy candidate |
| courses AS c | c.mentor_id | Bằng numeric principal ID | Candidate DERIVED; không hỗ trợ assignment relation chưa có nguồn |

### 0.3. Check kết quả

- JWT thiếu/sai/không hợp lệ → 401 theo catalog.
- Token không có role Mentor → 403 theo catalog.
- Course không tồn tại → candidate 404.
- Course tồn tại nhưng không khớp direct-owner candidate → candidate 403.
- AC-21 cho phép course được phân công; nếu quyền đến từ assignment, cần relation đã duyệt, không suy diễn bảng.

## 1. Validate data input

- Parse course_id thành int64; không thêm điều kiện dương.
- title là string bắt buộc; giới hạn tối đa 200 ký tự là DERIVED từ legacy lessons.name VARCHAR(200). Không suy ra trim hoặc minimum length.
- content là int64 bắt buộc; không suy ra giá trị dương.
- asset refs là string bắt buộc; không parse, tách delimiter hay coi là URL trước khi có format được duyệt.
- order là int32 bắt buộc; không thêm điều kiện không âm.
- Lỗi parse/required/giới hạn candidate ánh xạ 422 theo catalog; chưa thêm business error code.

## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| courses AS c | c.id | ID để xác định course | Q1 |
| ↑ | c.mentor_id | Mentor owner candidate | Q1 |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| courses AS c | N/A | BASE |

Không JOIN resources, contents hoặc file_objects vì chưa có reference format/asset lookup được xác nhận.

### 2.3. WHERE

- c.id = :course_id.
- Không thêm c.status = PUBLISHED.
- Không thêm assignment predicate nếu chưa có relation nguồn.

### 2.4. ORDER BY

- N/A — query chỉ tìm course theo primary ID.

## 3. Insert/Update thông tin

### 3.1. Target table

- M1: legacy candidate lessons.
- Không UPDATE lecture hiện có; API #47 là create.
- Không INSERT resources/uploads/contents khi chưa có nguồn mapping đã xác nhận.

### 3.2. Conditions

- Q1 trả đúng course_id.
- Principal có role Mentor.
- Candidate direct owner: c.mentor_id = current numeric Mentor ID.
- Thứ tự kiểm tra và 403/404 phân biệt là DERIVED theo error set; cần đối chiếu với API #46.

### 3.3. Items update/insert

- M1 chỉ insert một row lessons; tham chiếu [07_lessons_insert.md](./07_lessons_insert.md).
- M2 asset association chưa xác định; không tạo mutation mapping.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| course_id | Path course_id | int64; legacy candidate |
| title | Request title | INSERT lessons.name |
| content_text_candidate | Chuyển request int64 thành chuỗi thập phân | DERIVED; meaning cần xác nhận |
| order | Request order | INSERT lessons.sort_order |
| created_at | CURRENT_TIMESTAMP | Legacy DDL không có default |
| updated_at | CURRENT_TIMESTAMP | Dùng cùng transaction timestamp candidate |
| status | Omitted | Nhận legacy default DRAFT nếu schema được duyệt |

## 4. Check kết quả execute query

### 4.1. Thành công

- INSERT trả về một row và transaction commit thành công.
- Map Lecture.id/course_id/title/content/order/status từ row candidate.
- Chỉ trả HTTP 201 khi mọi field bắt buộc trong Lecture, đặc biệt assets[], có nguồn mapping đã duyệt.
- Nếu asset refs chưa thể resolve thì không giả lập thành công; contract chưa định nghĩa fallback hợp lệ.

### 4.2. Lỗi hệ thống

- Query/transaction lỗi không ánh xạ được an toàn → rollback và 500 DESIGN_INTERNAL_ERROR.
- Không trả SQL, exception hoặc dữ liệu storage nội bộ.

### 4.3. Validate lỗi

- Field bắt buộc/type parse sai hoặc title vượt candidate 200 → 422 DESIGN_VALIDATION_ERROR.
- Không phát sinh error code khác catalog.

### 4.4. Ngoài trường hợp trên

- Dùng 401/403/404/422/500 đúng catalog.
- Không dùng 503 cho API #47; lỗi storage ở bước upload thuộc API #34 contract.
- API guidelines yêu cầu data:null khi lỗi, nhưng current helper mặc định {}; discrepancy cần xử lý ở implementation contract chung.

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
