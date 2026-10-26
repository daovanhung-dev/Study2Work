---
title: "Request"
order: 3
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `POST` |
| URI | `/api/v1/mentor/notifications` |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |

## Request header

| Không | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | Có | Bearer JWT | Catalog yêu cầu Mentor; claim và mapping identity số chưa có runtime source. | 0.1 |
| 2 | Trace ID | `X-Trace-Id` | Không | UUID nếu gửi | Header theo API Guidelines; endpoint hiện chưa có route. | 0.2 |
| 3 | Idempotency key | `Idempotency-Key` | Không khai báo | Không được gửi như contract field của API #63 hiện tại. | Retry deduplication remains unresolved; no key persistence is implemented. | 4.2 |

## Path parameters

N/A — endpoint không khai báo path parameter.

## Query parameters

N/A — catalog không khai báo query parameter.

## Request body — contract trực tiếp

| Không | Logical name | Field | Type | Required | Rule từ catalog | Data Mapping reference | Gap |
|---:|---|---|---|---:|---|---|---|
| 1 | Recipients | `recipients` | string | Có | CSV positive int64 Student `users.id`, ví dụ `101,202`; duplicate IDs được collapse theo lần đầu. | 2.1, 3.2 | Fallback DERIVED từ API #62 UserSummary IDs và legacy BIGINT users. |
| 2 | Title | `title` | string | Có | Tối đa 200 ký tự theo cột legacy `notifications.title`; giữ nguyên nội dung đầu vào. | 1.2, 3.1 | Max length là constraint vật lý local; live schema chưa xác minh. |
| 3 | Content | `content` | int64 | Có | Giữ scalar int64 trực tiếp; ghi vào TEXT dưới dạng chuỗi thập phân. | 1.3, 3.1 | Fallback DERIVED; vẫn lệch UI nhập text và reusable Notification.content. |
| 4 | Channels | `channels` | string | Có | CSV token `PUSH` và/hoặc `EMAIL`; duplicate token được collapse theo lần đầu. | 2.2, 3.3 | Fallback DERIVED từ nhãn Push/Email trong AC-25. |

## Quy ước query/body

- Giữ đúng bốn body fields trực tiếp của catalog; không thêm `course_id`, `operation_id` hoặc `notification_id`.
- Vì body không mang `course_id`, server chỉ chấp nhận khi toàn bộ recipient IDs cùng có ACTIVE enrollment trong ít nhất một course do Mentor trực tiếp sở hữu. Không thể xác nhận đó chính là course đã mở trên UI; đây là giới hạn DERIVED.
- `recipients` và `channels` là CSV; mỗi item được trim hai đầu, item rỗng hoặc sai format trả 422.
- Không thêm Idempotency-Key, recipient limit hoặc content length limit vào request API này.

## Validation đề xuất — chưa phải rule trong catalog

| Field/condition | Kiểm tra đơn giản đề xuất | Trạng thái |
|---|---|---|
| `recipients` | Parse positive int64 IDs; reject empty/non-numeric/out-of-range items; collapse duplicates preserving first-seen order. | DERIVED CSV mapping from #62 IDs. |
| Recipient scope | Require all IDs to be ACTIVE Students in a common course directly owned by the Mentor; reject the full request otherwise. | DERIVED; body cannot identify the exact course. |
| `title` | Enforce legacy database maximum 200 characters; do not trim or impose a non-empty rule beyond required string type. | Local DDL-backed limit; live schema unverified. |
| `content` | Require JSON integer/int64; persist its base-10 string form because legacy Notification stores TEXT. | DERIVED scalar-to-text mapping; business meaning remains open. |
| `channels` | Parse CSV; accept only `PUSH` and `EMAIL`; collapse duplicates preserving first-seen order. | DERIVED machine tokens from diagram labels. |
| Batch size/idempotency | No extra limit or idempotency behavior is added because neither is in the direct request contract or error set. | Retry deduplication remains unresolved. |

## Ví dụ request — chỉ minh họa kiểu trực tiếp

```json
{
  "recipients": "2001,2002",
  "title": "Thong bao lop hoc",
  "content": 123,
  "channels": "PUSH,EMAIL"
}
```

CSV encoding là fallback `DERIVED`, chưa phải contract owner phê duyệt. `content:123` được lưu thành chuỗi `"123"`; API không diễn giải nó thành free-form message hoặc template ID.
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
