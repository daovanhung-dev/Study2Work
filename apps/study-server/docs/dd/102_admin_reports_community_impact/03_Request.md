---
title: "Request"
order: 3
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
status: "Draft — Needs Confirmation"
---

# Request

## Phạm vi input

`GET /api/v1/admin/reports/community-impact` nhận Bearer JWT và ba query string tùy chọn theo catalog. Không có path parameter hoặc request body.

## Header

| Header | Required | Type | Mục đích | Basis/status |
|---|---:|---|---|---|
| `Authorization` | Yes | `Bearer <JWT>` | Xác thực principal Admin và quyền report/analytics | DIRECT requirement; claim/guard SOURCE_REQUIRED |

`X-Trace-Id` thuộc API guideline chung, không phải query/header riêng được khai báo ở row #102.

## Query parameters

| Name | Required | Type | Default | Description/use | Validation / unresolved |
|---|---:|---|---|---|---|
| `from` | No | string | Không nêu | Bound đầu kỳ | Catalog type DIRECT; ISO `YYYY-MM-DD` parse là DERIVED proposal; invalid-date mapping chưa có code |
| `to` | No | string | Không nêu | Bound cuối kỳ | Catalog type DIRECT; ISO `YYYY-MM-DD` parse là DERIVED proposal; invalid-date mapping chưa có code |
| `segment` | No | string | Không nêu | Chọn nhóm metric học tập/cộng đồng | `learning`/`community` là DERIVED proposal; allowed values và unknown-value behavior cần xác nhận |

## Path parameters

Không có path parameter.

## Request body

Không có request body theo catalog.

## Query không khai báo

Không nhận `filters` hoặc `format`; hai query đó thuộc API #103. Không nhận `page`/`size` vì response trực tiếp là `Report`, không phải `Page<ImpactMetric>`.

## Quy tắc date window đề xuất — DERIVED

Để cùng kỳ với API #101 và đủ `Report.period.from/to`:

- Nếu có cả `from` và `to`, parse hai chuỗi thành ISO calendar date và dùng inclusive range.
- Nếu không truyền ngày nào, dùng 30 ngày lịch gần nhất tính cả ngày hiện tại.
- Nếu chỉ truyền `from`, dùng `from` đến ngày hiện tại.
- Nếu chỉ truyền `to`, dùng 30 ngày lịch kết thúc tại `to`.
- Đây là proposal kế thừa từ DD #101; catalog #102 chỉ khai báo `string` và không chốt parser/default.
- `from > to`, date không hợp lệ, timestamp boundary/timezone, khoảng tối đa và HTTP/business-code mapping chưa xác định. Catalog chỉ có 401/403/500; không tự thêm 400/422.

## Segment đề xuất — DERIVED

| Giá trị đề xuất | Metrics được trả |
|---|---|
| Không truyền | Cả bốn metric |
| `learning` | `unique_enrolled_learners`, `course_completions` |
| `community` | `discussion_topics_created`, `discussion_replies_created` |

Đây là grouping để phục vụ filter trên dashboard theo AC-38; catalog không định nghĩa enum hoặc cách xử lý giá trị rỗng/khác.

## Ví dụ request

```text
GET /api/v1/admin/reports/community-impact?from=2026-10-01&to=2026-10-24&segment=learning
Authorization: Bearer <JWT>
```

Ngày và segment chỉ minh họa đề xuất; không xác nhận contract validation hoặc business vocabulary.
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
