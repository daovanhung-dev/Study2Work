---
title: "Data Mapping"
order: 5
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
DELETE route
→ validate shared ADMIN JWT role
→ parse raw user_id as signed int64
→ conditional soft-delete UPDATE users
→ validate returned id/deleted_at event time
→ commit
→ DeleteResult envelope
```

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Gọi `validate_current_user_request(..., role="ADMIN")` trước path parsing và database access.
- Guard trả 401 khi JWT thiếu/sai; trả 403 khi role không phải ADMIN.
- Mapping claim ADMIN thành quyền user-management là DERIVED theo APIs #68–#71; tenant/MFA/dedicated permission chưa có source.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Shared auth guard | Authorization | Bearer JWT và role ADMIN | Không query user trước khi guard pass. |

### 0.3. Check kết quả

- Guard lỗi: trả response lỗi nguyên trạng; không truy cập DB.
- Guard thành công: tiếp tục parse path.

## 1. Validate data input

- `user_id_value`: lấy raw string từ `request.path_params["user_id"]`.
- Parse signed int64; malformed hoặc overflow trả 422 `DESIGN_VALIDATION_ERROR`.
- Không có body hoặc query parameter.

## 2. Get thông tin

Không có SELECT riêng. UPDATE theo primary key vừa kiểm tra existence vừa thực hiện soft-delete atomically.

## 3. Insert/Update thông tin

### 3.1. Target table

- Target: legacy candidate `users`.
- Không dùng V1-PILOT UUID identity/profile relations.
- Không hard-delete row hoặc mutate relation phụ thuộc.

### 3.2. Conditions

- `users.id = :user_id`.
- `users.status IS DISTINCT FROM 'DELETED'`.

### 3.3. Items update/insert

- `users.status = 'DELETED'`.
- `users.updated_at = CURRENT_TIMESTAMP`.
- Soft-delete giữ nguyên `courses`, `enrollments`, `progress`, `submissions`, `discussions`, `notifications`, `payments`, `refresh_tokens` và các FK row khác.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `user_id` | Parsed path ID | Bind parameter; signed int64. |

SQL constant:

~~~sql
UPDATE users
SET
    status = 'DELETED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING id, updated_at AS deleted_at
~~~

## 4. Check kết quả execute query

### 4.1. Thành công

- Một row hợp lệ: `data.id = returned.id`.
- `data.status = "deleted"`.
- `data.deleted_at = returned.updated_at`, được SQL alias thành `deleted_at`.
- Validate `id` khớp requested ID và `deleted_at` là datetime trước COMMIT.
- Commit rồi trả 200 `DESIGN_RESOURCE_DELETED`.

### 4.2. Lỗi hệ thống

- Query, projection, model mapping hoặc commit lỗi: rollback và trả 500 `DESIGN_INTERNAL_ERROR`.
- Không đưa SQL/exception detail ra response.

### 4.3. Validate lỗi

- Raw path không phải signed int64: 422 `DESIGN_VALIDATION_ERROR`; không query.
- Access không hợp lệ: 401/403; không query.

### 4.4. Ngoài trường hợp trên

- Không có RETURNING row: 404 `DESIGN_RESOURCE_NOT_FOUND`; áp dụng cho user không tồn tại hoặc status đã `DELETED`.
- Đây là fallback repeat behavior; không thêm 409.
- Đây là soft-delete fallback: không anonymize PII, không kiểm tra/block từng relation và không xóa/cascade dữ liệu. Nếu policy yêu cầu các nhánh đó, cần owner approval.
- `deleted_at` chỉ là response alias từ `updated_at` của mutation hiện tại; schema không lưu deletion time riêng.
- API #03 chặn login/refresh mới do `status != ACTIVE`; existing access JWT có thể còn dùng tới expiry.

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
