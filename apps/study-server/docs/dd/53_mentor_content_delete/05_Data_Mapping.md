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

> Contract/diagram evidence and local behavior remain separate from DERIVED guards. Migration 006 defines local `contents`; live availability is not verified.

## 0. Check quyền

### 0.1. Thực hiện check quyền

1. Đọc Authorization header và xác thực Bearer JWT.
2. Yêu cầu role Mentor theo catalog.
3. Kiểm tra Mentor có quyền quản lý course chứa Content theo tiền điều kiện AC-22.
4. Mentor claim, identity và assignment mapping chưa có source runtime.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `contents` | `course_id` | Course chứa target Content | Local BIGINT FK → `courses.id`; live schema unverified. |
| `courses` | `id` / `mentor_id` | Direct-owner access candidate | Current API #49 uses direct owner; assignment support remains unconfirmed. |

### 0.3. Check kết quả

- Thiếu hoặc invalid Bearer token: 401 theo catalog.
- Sai role hoặc không có quyền quản lý course: 403 theo catalog.
- Thứ tự giữa lookup Content/Course và lỗi 403/404 chưa được contract khóa.

## 1. Validate data input

- Parse path content_id theo kiểu int64 như catalog khai báo.
- Không thêm giới hạn số dương do nguồn không xác nhận.
- Raw path sai format hoặc ngoài miền signed-int64 trả 404 DESIGN_RESOURCE_NOT_FOUND theo convention hiện hành của Content APIs. Route template đã nằm trong `DESIGN_CONTRACT_PATHS` qua API #51.
- Không có request body hoặc query parameter.

## 2. Get thông tin

### 2.1. Load Content target — Q1

- Đọc Content theo content_id để lấy id, course_id, status và parent context cho access/dependency checks.
- Q1 reads `contents.id/course_id/status` and joins `courses`; the local query locks both rows.
- Không có active target, gồm ID đã soft-delete: runtime trả 404 DESIGN_RESOURCE_NOT_FOUND. Repeat-delete semantics vẫn là DERIVED.

### 2.2. Kiểm tra dependency trực tiếp — Q2

- Reusable Content chỉ khai báo parent_id làm quan hệ parent-child.
- Query local SQL tìm child cùng course với `parent_id = target.id`. API #50 khóa cùng Course trước insert; API #53 dùng lại khóa đó.
- Proposal chỉ xét child chưa soft-delete; local active predicate is `deleted_at IS NULL`.
- Không tự duyệt payload object, progress, asset, enrollment hoặc bảng khác để kết luận dependency.

### 2.3. Query matrix

| Query | Mục đích | Type | Logical source | Điều kiện | Kết quả/nhánh |
|---|---|---|---|---|---|
| Q1 | Load target and course context | SELECT ... FOR UPDATE | `contents` joined to `courses` | `content.id = content_id AND deleted_at IS NULL` | Không có active target → 404; non-owner → 403. Local source-backed mapping; live schema unverified. |
| Q2 | Check direct children | SELECT EXISTS | `contents` | same `course_id`, `parent_id = target.id`, `deleted_at IS NULL` | Có child → 422 theo DERIVED guard; không mutation. |

## 3. Check business condition

1. Nếu Content.status là PUBLISHED, proposal trả 422; Mentor gọi API #52 để unpublish trước.
2. Nếu Q2 tìm thấy direct child còn hiệu lực, trả 422 DESIGN_VALIDATION_ERROR; không cascade và không reparent.
3. Content không PUBLISHED và không có direct child được soft-delete theo fallback DERIVED; status PENDING_REVIEW/APPROVED/REJECTED hiện được phép.
4. Xóa PENDING_REVIEW/APPROVED/REJECTED là DERIVED; không đổi Content.status và cần xác nhận tác động lên review queue.
5. Dependency ngoài parent_id và repeat-delete policy còn mở.

## 4. Soft-delete Content — M1

- AC-22 xác nhận logical action DELETE/soft delete Content.
- Runtime cập nhật local `contents.deleted_at = CURRENT_TIMESTAMP` và đọc lại timestamp bằng `RETURNING`; migration deployment vẫn chưa được xác minh.
- Giữ nguyên Content payload, version và moderation history theo proposal.
- Không cascade sang child Content hay resource khác.
- View sở hữu transaction, validate DeleteResult rồi commit; lỗi query/mapping/commit rollback. Không ghi audit row hoặc xóa history trong implementation này.
- Logical mapping: [07_content_soft_delete.md](./07_content_soft_delete.md).

## 5. Map response

| Response field | Mapping | Rule/status |
|---|---|---|
| data.id | ID target Content | Giữ nguyên ID từ `contents.id`; local mapping verified. |
| data.status | Literal deleted | DIRECT từ DeleteResult. |
| data.deleted_at | Thời điểm soft-delete thành công | Trả `contents.deleted_at` do database `CURRENT_TIMESTAMP` ghi; timezone semantics remain open. |
| success | true | Envelope convention. |
| businessCode | DESIGN_RESOURCE_DELETED | DIRECT từ catalog. |
| message | Thông báo an toàn bằng tiếng Việt | Message cụ thể DERIVED. |
| meta | Empty object | `success_response` default; covered by current source. |
| traceId | Request trace | Envelope convention; covered by local HTTP tests. |

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
