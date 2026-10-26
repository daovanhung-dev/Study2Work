---
title: "Request"
order: 3
dd_id: "85"
api_name: "Đổi trạng thái lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PATCH |
| URI | `/api/v1/admin/lessons/{lesson_id}/status` |
| Character encoding | UTF-8 |
| Content-Type | application/json là DERIVED cho body đã implement; catalog chưa khai báo. |
| Authentication | Bearer JWT |
| Role | `ADMIN` guard được dùng; lesson-management permission riêng theo AC-34 chưa được thực thi. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | Yes | `Bearer <token>` | Shared guard yêu cầu role `ADMIN`; AC-34 permission chuyên biệt chưa được kiểm tra. | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) |
| 2 | Content type | `Content-Type` | DERIVED | `application/json` | Body JSON status đã implement. | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) |
| 3 | Trace ID | `X-Trace-Id` | No | UUID | Current Study middleware convention; không phải input nghiệp vụ. | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Lesson ID | `lesson_id` | int64 | Yes | Chưa đặc tả | Chưa đặc tả | Số nguyên 64-bit | Chỉ xác nhận type int64 | N/A | ID lesson; candidate predicate tới legacy lessons.id. | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) |

## Query parameters

N/A — catalog và AC-34 diagram không khai báo query parameter.

## Request body — DERIVED fallback implemented locally

Catalog và diagram chỉ khai báo path. Implementation dùng body tối thiểu `{status}`; enum là DERIVED fallback theo API #76, chưa phải Lesson-specific approved contract.

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Trạng thái lesson | `status` | string enum | Yes, DERIVED | 1 | 10 | Unicode | N/A | `DRAFT`, `PUBLISHED`, `SUSPENDED` | Không có | Target status; enum tái dùng API #76, chưa có owner approval riêng cho Lesson. | [Step 2](./05_Data_Mapping.md#step-2-check-status-proposal) |

Không gửi lesson_id hoặc metadata trong body. Status field, JSON encoding, requiredness và body 422 conditions là DERIVED implementation choices; owner approval riêng cho Lesson vẫn mở.

## Ví dụ Request data — DERIVED

```http
PATCH /api/v1/admin/lessons/501/status
Authorization: Bearer <admin-access-token>
Content-Type: application/json
X-Trace-Id: 00000000-0000-0000-0000-000000000085

{
  "status": "DRAFT"
}
```

Body enum gồm DRAFT, PUBLISHED, SUSPENDED theo DERIVED API #76 fallback. Legacy DDL chỉ xác nhận default DRAFT, không xác nhận toàn bộ enum.

## Quy tắc input đang mở

- Catalog xác nhận lesson_id:int64!; positive/minimum constraint chưa được đặc tả.
- Catalog có 422 DESIGN_VALIDATION_ERROR nhưng không chỉ rõ body schema hoặc field validation.
- Body chỉ nhận `status` đúng một trong ba giá trị DERIVED; thiếu/thừa field, sai type hoặc status ngoài enum trả 422. Same-status là no-op không audit; transition matrix/idempotency key không được thêm.
- Không suy ra readiness, enrollment, moderation hoặc audit reason rules từ schema khác.

---

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U13:X13`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
