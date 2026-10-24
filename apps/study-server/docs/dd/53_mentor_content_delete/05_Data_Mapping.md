---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "53"
api_name: "Xóa nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Contract/diagram evidence và đề xuất suy dẫn được tách biệt. Logical Content không đồng nghĩa với physical table đã xác nhận.

## 0. Check quyền

### 0.1. Thực hiện check quyền

1. Đọc Authorization header và xác thực Bearer JWT.
2. Yêu cầu role Mentor theo catalog.
3. Kiểm tra Mentor có quyền quản lý course chứa Content theo tiền điều kiện AC-22.
4. Mentor claim, identity và assignment mapping chưa có source runtime.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Logical Content | course_id | Course chứa target Content | Physical relation SOURCE_REQUIRED. |
| Logical Course | id / owner or assignment | Mentor được phép quản lý course | Legacy courses.mentor_id chỉ là candidate DERIVED; không khẳng định assignment support. |

### 0.3. Check kết quả

- Thiếu hoặc invalid Bearer token: 401 theo catalog.
- Sai role hoặc không có quyền quản lý course: 403 theo catalog.
- Thứ tự giữa lookup Content/Course và lỗi 403/404 chưa được contract khóa.

## 1. Validate data input

- Parse path content_id theo kiểu int64 như catalog khai báo.
- Không thêm giới hạn số dương do nguồn không xác nhận.
- Path sai kiểu hoặc ngoài miền int64 có thể dùng 422 DESIGN_VALIDATION_ERROR; middleware mapping hiện chưa được wire cho endpoint.
- Không có request body hoặc query parameter.

## 2. Get thông tin

### 2.1. Load Content target — Q1

- Đọc Content theo content_id để lấy id, course_id, status và parent context cho access/dependency checks.
- Không chỉ định SQL, bảng hoặc cột vật lý vì chưa có generic Content schema tương thích.
- Không có target khả dụng: 404 DESIGN_RESOURCE_NOT_FOUND là mapping candidate; repeat-delete behavior cần xác nhận.

### 2.2. Kiểm tra dependency trực tiếp — Q2

- Reusable Content chỉ khai báo parent_id làm quan hệ parent-child.
- Tìm logical child Content có parent_id bằng target.id.
- Proposal chỉ xét child chưa soft-delete; marker và predicate vật lý SOURCE_REQUIRED.
- Không tự duyệt payload object, progress, asset, enrollment hoặc bảng khác để kết luận dependency.

### 2.3. Query matrix

| Query | Mục đích | Type | Logical source | Điều kiện | Kết quả/nhánh |
|---|---|---|---|---|---|
| Q1 | Load target and course context | SELECT logical | Content + owning Course chưa xác định | Content.id = content_id | Không có target → 404 candidate; không đủ quyền → 403. Physical mapping SOURCE_REQUIRED. |
| Q2 | Check direct children | EXISTS logical | Content chưa xác định | child.parent_id = target.id và child chưa soft-delete | Có child → 422 candidate, không mutation. Physical query SOURCE_REQUIRED. |

## 3. Check business condition

1. Nếu Content.status là PUBLISHED, proposal trả 422; Mentor gọi API #52 để unpublish trước.
2. Nếu Q2 tìm thấy direct child còn hiệu lực, trả 422 DESIGN_VALIDATION_ERROR; không cascade và không reparent.
3. Content không PUBLISHED và không có direct child được soft-delete theo proposal.
4. Xóa PENDING_REVIEW/APPROVED/REJECTED là DERIVED; không đổi Content.status và cần xác nhận tác động lên review queue.
5. Dependency ngoài parent_id và repeat-delete policy còn mở.

## 4. Soft-delete Content — M1

- AC-22 xác nhận logical action DELETE/soft delete Content.
- Ghi tombstone theo storage model được duyệt; không chỉ định deleted_at column, boolean, ContentStatus=DELETED hoặc physical DELETE.
- Giữ nguyên Content payload, version và moderation history theo proposal.
- Không cascade sang child Content hay resource khác.
- Transaction/audit do schema/API owner xác nhận; DD không tạo mutation SQL.
- Logical mapping: [07_content_soft_delete.md](./07_content_soft_delete.md).

## 5. Map response

| Response field | Mapping | Rule/status |
|---|---|---|
| data.id | ID target Content | Giữ nguyên ID; physical source SOURCE_REQUIRED. |
| data.status | Literal deleted | DIRECT từ DeleteResult. |
| data.deleted_at | Thời điểm soft-delete thành công | Field DIRECT; time source/storage chưa xác nhận. |
| success | true | Envelope convention. |
| businessCode | DESIGN_RESOURCE_DELETED | DIRECT từ catalog. |
| message | Thông báo an toàn bằng tiếng Việt | Message cụ thể DERIVED. |
| meta | Empty object candidate | Không có metadata riêng trong contract. |
| traceId | Request trace | Envelope convention; route chưa tồn tại. |

## 6. Trả về response

- Thành công: HTTP 200, DESIGN_RESOURCE_DELETED, ApiEnvelope<DeleteResult>.
- Lỗi: dùng đúng set 401/403/404/422/500 trong [06_Error.md](./06_Error.md); không thêm 409.
- Sau khi thành công, AC-22 yêu cầu client reload cây nội dung.
- Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) cho các proposal cần xác nhận.

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
