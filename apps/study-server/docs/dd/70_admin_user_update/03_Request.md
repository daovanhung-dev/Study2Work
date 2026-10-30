---
title: "Request"
order: 3
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PUT |
| URI | /api/v1/admin/users/{user_id} |
| Character encoding | UTF-8 |
| Content-Type | `application/json` trong runtime fallback `DERIVED`; catalog/diagram không đặc tả body. |
| Authentication | Bearer JWT |
| Role | Shared JWT guard yêu cầu `ADMIN`; permission user-management riêng còn `SOURCE_REQUIRED`. |
| Direct input | `path{user_id:int64!}` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Principal phải được xác thực và được phép quản lý user; Admin guard/policy chưa có trong Study source. | 0.1 |

Không có header nghiệp vụ bổ sung trong catalog. Trace ID do middleware xử lý; không được khai báo riêng như field #70.

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | User ID | user_id | int64 | Yes | Không quy định | Không quy định | Số nguyên signed 64-bit | Trong signed-int64 range | Không có | Sai định dạng/vượt miền trả 422; ID hợp lệ không có row trả 404. | 1.1 |

## Query parameters

N/A — catalog không khai báo query parameter.

## Request body

**Direct contract:** catalog và diagram không đặc tả body schema. Không thể kết luận body bị cấm hoặc xác định requiredness từ path-only input notation.

**Runtime body fallback — DERIVED; không được catalog/diagram đặc tả:**

| No | Location | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | body | Full name | full_name | string | Yes | 1 | 150 | UTF-8 string | Không rỗng sau trim | N/A | Required PUT field; reuse API #14 trim/nonblank/max rule. | 1.2 |
| 2 | body | Phone | phone | string or null | Yes | 0 | 20 nếu string | UTF-8 string or JSON null | N/A | Null hoặc blank-to-null | Required key để thể hiện full replacement; reuse API #14 normalization. | 1.2 |
| 3 | body | Avatar URL | avatar_url | string or null | Yes | N/A | Không giới hạn trong runtime | String or JSON null | URI syntax không validate | Null hoặc blank-to-null | Required key; reuse API #14 normalization; URL syntax chưa có rule source. | 1.2 |
| 4 | body | Role | role | UserRole string | Yes | N/A | N/A | Exact uppercase string | `STUDENT`, `MENTOR`, `ADMIN` | N/A | Allowlist DERIVED từ các role hiện dùng trong Study source. | 1.2 |

Đây là full-replacement fallback: đủ bốn keys phải có; `phone` và `avatar_url` có thể null để xóa. Extra fields bị từ chối. Không đưa `status` (API #71), `bio` (không có persistence source), `email`, `id`, `created_at`, `updated_at` hoặc `password_hash` vào writable body.

## Ví dụ Request data

Ví dụ dưới đây minh họa body runtime fallback `DERIVED`; `role` dùng một trong ba giá trị hiện cho phép.

~~~http
PUT /api/v1/admin/users/1001
Authorization: Bearer <admin-access-token>
Content-Type: application/json

{
  "full_name": "Nguyen Van A",
  "phone": null,
  "avatar_url": null,
  "role": "STUDENT"
}
~~~

## Quy tắc input đang mở

- `user_id:int64!` là input trực tiếp; malformed/out-of-range map 422 theo error set #70.
- Catalog có 422 `DESIGN_VALIDATION_ERROR`; runtime dùng mã này cho body/path validation.
- `full_name` trim/nonblank/max 150; phone trim/max 20/blank-to-null; avatar_url trim/blank-to-null theo API #14 precedent.
- Body phải có đủ bốn keys; `phone`/`avatar_url` nhận null; extra keys bị từ chối.
- Role phải chính xác là `STUDENT`, `MENTOR` hoặc `ADMIN`; enum/transition policy chưa được owner xác nhận.

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
