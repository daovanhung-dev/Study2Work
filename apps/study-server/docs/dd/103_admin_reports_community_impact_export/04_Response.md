---
title: "Response"
order: 4
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| HTTP success | 202 |
| businessCode | DESIGN_OPERATION_ACCEPTED |

## Xung đột payload — chưa tự chọn một phương án

| Nguồn | HTTP / code | Payload | Trạng thái |
|---|---|---|---|
| API #103 endpoint row | 202 / DESIGN_OPERATION_ACCEPTED | ApiEnvelope<Report> | DIRECT |
| Operation tracking paragraph | 202 / DESIGN_OPERATION_ACCEPTED | ApiEnvelope<Operation> | DIRECT; mâu thuẫn với endpoint row |
| AC-38 flow | Generate CSV/XLSX/PDF hoặc job; UI download; poll Operation node | Không khóa response payload cụ thể | DIRECT logical flow |

### Payload theo endpoint row — Report

| No | Path | Logical name | Type | Source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|---|
| 1 | success | Cờ thành công | boolean | Envelope | 5.1 | Envelope dùng chung |
| 2 | businessCode | Mã nghiệp vụ | string | Catalog | 5.1 | DESIGN_OPERATION_ACCEPTED |
| 3 | message | Thông báo | string | Application | 5.1 | Chưa quy định nội dung cụ thể |
| 4 | data | Report | object: Report | Catalog row | 5.1 | Mâu thuẫn với Operation tracking |
| 4.1 | data.period | Khoảng ngày | DateRange | Report schema | 5.1 | Schema yêu cầu from và to |
| 4.1.1 | data.period.from | Ngày bắt đầu | date | DateRange schema | 5.1 | Ngữ nghĩa kỳ chỉ kế thừa proposal #102 |
| 4.1.2 | data.period.to | Ngày kết thúc | date | DateRange schema | 5.1 | Ngữ nghĩa kỳ chỉ kế thừa proposal #102 |
| 4.2 | data.metrics | Các metric | ImpactMetric[] | Report schema | 5.1 | #103 không quy định key/công thức |
| 4.2.1 | data.metrics[].key | Key metric | string | ImpactMetric schema | 5.1 | Metric ứng viên nằm trong DD #102 Draft |
| 4.2.2 | data.metrics[].value | Giá trị metric | decimal-string | ImpactMetric schema | 5.1 | Giá trị ứng viên #102 là DERIVED |
| 4.2.3 | data.metrics[].label | Nhãn metric | string | ImpactMetric schema | 5.1 | Chưa quy định nhãn cụ thể |
| 4.3 | data.generated_at | Thời điểm tạo | date-time | Report schema | 5.1 | Chưa chốt clock/timezone |
| 5 | meta | Metadata | object | ApiEnvelope | 5.1 | Chưa quy định shape riêng của endpoint |
| 6 | traceId | Mã trace | uuid | API guideline | 5.1 | Hành vi runtime hiện tại chưa xác minh |

### Payload theo Operation tracking — phương án mâu thuẫn

| No | Path | Logical name | Type | Source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|---|
| 1 | success | Cờ thành công | boolean | Envelope | 5.2 | Envelope dùng chung |
| 2 | businessCode | Mã nghiệp vụ | string | Catalog | 5.2 | DESIGN_OPERATION_ACCEPTED |
| 3 | message | Thông báo | string | Application | 5.2 | Chưa quy định nội dung cụ thể |
| 4 | data.id | ID Operation | uuid | Operation schema | 5.2 | Row API #18 ghi int64; có xung đột |
| 4.1 | data.kind | Loại Operation | OperationKind | Operation schema | 5.2 | Chưa quy định giá trị enum |
| 4.2 | data.status | Trạng thái Operation | OperationStatus | Operation schema | 5.2 | Chưa quy định trạng thái ban đầu/lifecycle |
| 4.3 | data.owner_id | ID chủ sở hữu | int64 | Operation schema | 5.2 | Principal mapping/persistence SOURCE_REQUIRED |
| 4.4 | data.submitted_at | Thời điểm gửi | date-time | Operation schema | 5.2 | Chưa rõ source/clock |
| 4.5 | data.updated_at | Thời điểm cập nhật | date-time | Operation schema | 5.2 | Chưa rõ source/lifecycle |
| 4.6 | data.completed_at | Thời điểm hoàn tất | date-time optional | Operation schema | 5.2 | Chưa rõ quy tắc null/omit |
| 4.7 | data.result | Kết quả | Payment optional trong schema dùng chung | Operation schema | 5.2 | Không mô tả export report; xem Q-103-02 |
| 5 | meta | Metadata | object | ApiEnvelope | 5.2 | Chưa quy định shape riêng của endpoint |
| 6 | traceId | Mã trace | uuid | API guideline | 5.2 | Hành vi runtime hiện tại chưa xác minh |

### Kết quả bất đồng bộ đề xuất — DERIVED, chưa được duyệt

| Field kết quả | Kiểu ứng viên | Nguồn ứng viên | Trạng thái |
|---|---|---|---|
| Kết quả Operation khi hoàn tất | ExportAsset | Metadata của file đã tạo | DERIVED; Operation dùng chung hiện khai báo result là Payment |
| ExportAsset.download_url | uri | Storage file tạm | SOURCE_REQUIRED |
| ExportAsset.format | ExportFormat | Format được yêu cầu/mặc định | Enum/default SOURCE_REQUIRED |
| ExportAsset.expires_at | date-time | Thời hạn lưu artifact tạm | Expiry policy SOURCE_REQUIRED |

### Ví dụ theo row contract — chỉ minh họa shape, HTTP 202

~~~json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "<NOI_DUNG_MESSAGE_CHUA_QUY_DINH>",
  "data": {
    "period": {
      "from": "2026-10-01",
      "to": "2026-10-24"
    },
    "metrics": [
      {
        "key": "<METRIC_KEY_CHUA_CHOT>",
        "value": "<CHUOI_SO_THAP_PHAN_CHUA_CHOT>",
        "label": "<NHAN_METRIC_CHUA_CHOT>"
      }
    ],
    "generated_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000103"
}
~~~

Các placeholder trong ví dụ là giá trị minh họa; ví dụ chỉ thể hiện Report theo row, không xác nhận payload này phù hợp với job/export.

### Ví dụ Operation đề xuất — DERIVED, HTTP 202

~~~json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "<NOI_DUNG_MESSAGE_CHUA_QUY_DINH>",
  "data": {
    "id": "00000000-0000-4000-8000-000000000103",
    "kind": "<LOAI_OPERATION_SOURCE_REQUIRED>",
    "status": "<TRANG_THAI_OPERATION_SOURCE_REQUIRED>",
    "owner_id": 123,
    "submitted_at": "2026-10-24T10:00:00Z",
    "updated_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000103"
}
~~~

Operation ID trong ví dụ theo reusable UUID schema; row API #18 vẫn khai báo int64. Enum và field persistence chỉ là placeholder, contract chưa chốt.

## Response lỗi

Các case trực tiếp của #103 chỉ gồm 401, 403, 503 và 500; xem [06_Error.md](./06_Error.md). Các xung đột payload được ghi tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-103-01-response-report-or-operation).

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
