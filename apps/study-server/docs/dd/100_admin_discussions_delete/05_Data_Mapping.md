---
title: "Data Mapping"
order: 5
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Xác thực và quyền

- Đọc Bearer JWT từ `Authorization` theo contract.
- Yêu cầu role Admin theo catalog; Study Admin guard/claim mapping hiện `SOURCE_REQUIRED`.
- Không ghi actor ID vào audit cho đến khi identity mapping được xác nhận.

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Admin principal | JWT role/claim | `Admin` | Role DIRECT; claim name/policy chưa có source |

### 1. Validate path input

- `discussion_id`: parse theo `int64` từ path.
- Không có query parameter.
- Không có request body.
- Catalog nêu 422 `DESIGN_VALIDATION_ERROR`; malformed/overflow trigger và chi tiết field chưa được chỉ rõ.

### 2. Get target candidate

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy `discussions` | `discussions.id` | Candidate target key | BIGSERIAL trong DDL legacy; live schema unverified |
| Legacy `discussions` | `discussions.status` | Candidate current state | Nullable `VARCHAR(20)`; allowed values chưa được xác nhận |
| Legacy `discussions` | `discussions.updated_at` | Candidate timestamp | Không phải dedicated delete timestamp |

#### WHERE

- Candidate target predicate: `discussions.id = :discussion_id`.
- Không thêm predicate theo `parent_id`, report state hoặc moderation status.
- Nếu target không tồn tại, catalog có 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Hành vi với target đã soft-delete chưa được xác định.

### 3. Soft-delete logical operation

- AC-37 yêu cầu soft delete; không xóa physical row.
- Có thể cân nhắc cập nhật `discussions.status` sang `DELETED` như proposal `DERIVED`; token và transition cần phê duyệt.
- Có thể cân nhắc gán `discussions.updated_at` bằng thời điểm operation để tạo `DeleteResult.deleted_at`; đây là proposal `DERIVED`, vì cột dùng chung cho cập nhật và không phải delete timestamp.
- Không có SQL executable hoặc physical mapping được duyệt.

### 4. Preserve audit trail

- Giữ nguyên các bản ghi moderation/audit hiện có theo yêu cầu logical của AC-37.
- AC-37 #100 không nói rõ có append delete event mới hay chỉ giữ lịch sử đã có.
- Legacy DDL không có audit relation cho `discussions`.
- Pilot `admin_adjustments.target_id` và `audit_events.resource_id` là UUID; không ánh xạ trực tiếp Discussion BIGINT khi chưa có thiết kế tương thích.
- Actor/action/time/retention/atomicity và failure behavior của audit là `SOURCE_REQUIRED`.

### 5. Build response

| Response path | Candidate source | Transform | Status |
|---|---|---|---|
| `data.id` | `discussion_id` hoặc `discussions.id` | Trả ID target | Field DIRECT; source consistency cần xác nhận |
| `data.status` | Reusable `DeleteResult` | Literal `deleted` | DIRECT |
| `data.deleted_at` | Operation timestamp | ISO-8601 date-time | Field/type DIRECT; persistence SOURCE_REQUIRED; ánh xạ từ `updated_at` chỉ DERIVED |
| `businessCode` | Catalog #100 | Literal `DESIGN_RESOURCE_DELETED` | DIRECT |
| `traceId` | Shared request context | UUID | Common API guideline |

### 6. Error branches

- 401/403 theo xác thực và role Admin; Admin enforcement source chưa có.
- 404 nếu target không tồn tại; trạng thái already-deleted chưa có rule.
- 422 code được catalog khai báo; trigger/parse policy chưa rõ.
- 500 code được catalog khai báo; exact infrastructure failure mapping chưa được source xác nhận.
- Chi tiết status/code xem [06_Error.md](./06_Error.md).

## Transaction và concurrency

- Soft delete và audit preservation phải được xem trong cùng thiết kế.
- Không có evidence cho atomic transaction, row lock, idempotency hoặc retry behavior.
- Chưa xác định update race và response khi một request khác xóa cùng target.

## Side effects không được suy ra

- Không hard-delete `discussions`.
- Không cascade update/delete replies hoặc reports.
- Không tự dismiss report.
- Không tự đặt prior moderation state làm precondition endpoint.

## Request Usage Matrix

| Request item | Source | Use | Rule/status |
|---|---|---|---|
| `Authorization` | Header Bearer JWT | Xác thực principal và yêu cầu Admin | DIRECT; Admin claim/guard SOURCE_REQUIRED |
| `discussion_id` | Required path `int64` | Chọn target row | DIRECT; malformed/overflow mapping SOURCE_REQUIRED |
| Body | Không khai báo | Không có | DIRECT |
| Query | Không khai báo | Không có | DIRECT |

## Query Matrix

| Query ID | Operation | Relation/fields | Predicate | Purpose | Status |
|---|---|---|---|---|---|
| Q1 | Candidate SELECT | Legacy `discussions.id`, `status`, `updated_at` | `id = :discussion_id` | Kiểm tra target và đọc candidate state/time | Design candidate only; live schema and projection unverified |
| Q2 | Audit lookup | No selected physical relation | Chưa xác định | Xác định lịch sử cần giữ | `SOURCE_REQUIRED`; không tạo query giả định |

## Mutation Matrix

| Mutation ID | Logical operation | Physical target | Fields/effect | Rule/status |
|---|---|---|---|---|
| M1 | Soft-delete Discussion | Candidate legacy `discussions` | Update candidate `status` and `updated_at` | Logical soft delete DIRECT; token/time mapping DERIVED; approval required |
| M2 | Preserve audit trail | Existing logical audit history | Không xóa history; append delete event chưa rõ | Preserve DIRECT; physical source/append/atomicity SOURCE_REQUIRED |
| M3 | Physical DELETE | None | No row deletion | Not performed; conflicts with AC-37 soft-delete instruction |
| M4 | Cascade to children/reports | None selected | No cascade inferred | `SOURCE_REQUIRED` |

## Response Source Matrix

| Response field | Contract type | Candidate source/transform | Evidence status |
|---|---|---|---|
| `success` | boolean | Envelope constant `true` | Shared envelope convention |
| `businessCode` | string | `DESIGN_RESOURCE_DELETED` | DIRECT catalog |
| `message` | string | Application-selected text | Exact literal unspecified |
| `data.id` | int64 | Path ID or candidate `discussions.id` | Response shape DIRECT; source/consistency candidate |
| `data.status` | literal `deleted` | Constant | DIRECT reusable schema |
| `data.deleted_at` | date-time | Soft-delete operation time | Field/type DIRECT; source SOURCE_REQUIRED; `updated_at` proposal DERIVED |
| `meta` | object | Shared envelope metadata | Endpoint fields unspecified |
| `traceId` | uuid | Request trace context | Shared API guideline |
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
