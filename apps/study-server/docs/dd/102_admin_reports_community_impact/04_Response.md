---
title: "Response"
order: 4
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |
| HTTP success | `200` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Thành công | `success` | boolean | No | N/A | N/A | 6.1 | Hằng `true` khi thành công | Không null | Shared envelope |
| 2 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | No | N/A | N/A | 6.1 | `DESIGN_RESOURCE_RETRIEVED` | Không null | DIRECT catalog |
| 3 | `message` | Thông báo | `message` | string | No | N/A | N/A | 6.1 | Nội dung an toàn do ứng dụng chọn | Literal chưa nêu | Không suy ra text contract |
| 4 | `data` | Report | `data` | object | No | N/A | N/A | 6.1 | Map reusable `Report` | Không null theo schema | DIRECT shape |
| 5 | `data.period` | Kỳ báo cáo | `period` | `DateRange` | No | N/A | N/A | 6.1 | Effective date window | Không null theo schema | DIRECT schema; default DERIVED |
| 6 | `data.period.from` | Ngày bắt đầu | `from` | date | No | N/A | N/A | 6.1 | Effective lower bound | Không null | String parsing/default chưa được chốt |
| 7 | `data.period.to` | Ngày kết thúc | `to` | date | No | N/A | N/A | 6.1 | Effective upper bound | Không null | String parsing/default chưa được chốt |
| 8 | `data.metrics` | Danh sách metric | `metrics` | `ImpactMetric[]` | No | Candidate aggregate sources | Multiple | 6.1 | Chọn metric theo `segment` | Empty collection behavior chưa nêu | DIRECT shape; contents DERIVED |
| 9 | `data.metrics[].key` | Mã metric | `key` | string | No | N/A | N/A | 6.1 | Candidate stable key | Không null | Key list DERIVED |
| 10 | `data.metrics[].value` | Giá trị metric | `value` | decimal-string | No | Candidate query result | `COUNT`/`COUNT DISTINCT` | 6.1 | Decimal integer → string | `"0"` proposal cho count rỗng | Type DIRECT; formula DERIVED |
| 11 | `data.metrics[].label` | Nhãn metric | `label` | string | No | N/A | N/A | 6.1 | Nhãn tiếng Việt candidate | Không null | Exact labels DERIVED |
| 12 | `data.generated_at` | Thời điểm tạo report | `generated_at` | date-time | No | N/A | N/A | 6.1 | Thời điểm tổng hợp response | Không null | UTC assembly clock DERIVED |
| 13 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 6.1 | Metadata envelope | Endpoint fields chưa nêu | Shared envelope |
| 14 | `traceId` | Trace ID | `traceId` | uuid | No | Request context | Trace helper | 6.1 | Propagate request trace | Không null | API guideline |

## Metric keys đề xuất — DERIVED

| Key | Segment | Nhãn candidate | Candidate source |
|---|---|---|---|
| `unique_enrolled_learners` | `learning` | Người học ghi danh | Distinct `enrollments.user_id` theo `enrolled_at` |
| `course_completions` | `learning` | Lượt hoàn thành khóa học | Enrollment rows theo `completed_at` |
| `discussion_topics_created` | `community` | Chủ đề thảo luận | `discussions` rows có `parent_id IS NULL` |
| `discussion_replies_created` | `community` | Phản hồi thảo luận | `discussions` rows có `parent_id IS NOT NULL` |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy báo cáo tác động cộng đồng.",
  "data": {
    "period": {
      "from": "2026-10-01",
      "to": "2026-10-24"
    },
    "metrics": [
      {
        "key": "unique_enrolled_learners",
        "value": "74",
        "label": "Người học ghi danh"
      },
      {
        "key": "course_completions",
        "value": "28",
        "label": "Lượt hoàn thành khóa học"
      }
    ],
    "generated_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

Request example dùng `segment=learning`; hai metric keys/values, labels, period, message và timestamp chỉ minh họa. Metric set/formula và segment semantics đều `DERIVED`.

## Ví dụ thành công — `segment=community`

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy báo cáo tác động cộng đồng.",
  "data": {
    "period": {
      "from": "2026-10-01",
      "to": "2026-10-24"
    },
    "metrics": [
      {
        "key": "discussion_topics_created",
        "value": "19",
        "label": "Chủ đề thảo luận"
      },
      {
        "key": "discussion_replies_created",
        "value": "63",
        "label": "Phản hồi thảo luận"
      }
    ],
    "generated_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

Đây là ví dụ candidate cho segment community; các giá trị và metric semantics chưa được duyệt.

## Ví dụ lỗi — 401

```json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Yêu cầu xác thực.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

HTTP 401 và business code là DIRECT catalog; envelope lỗi theo API guideline. Trace UUID và literal message chỉ minh họa.

## Nguồn response

- `data.period` phản ánh effective range dùng cho mọi query; đầu vào raw là string nhưng `DateRange` output là date.
- `data.metrics[]` giữ nguyên reusable schema; `segment` chỉ chọn các item, không thêm field vào response.
- `data.generated_at` là thời điểm tạo báo cáo theo proposal; read consistency giữa các query chưa xác định.
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
