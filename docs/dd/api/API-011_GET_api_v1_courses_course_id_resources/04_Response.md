---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Response"
format: markdown
---

# Response

## 1. Success response

| Field | Type | Source | Remarks |
|---|---|---|---|
| `data.resource_id` | `TBD` | Explicit output in AC | Mapping chi tiết xem Data Mapping |
| `data.type` | `TBD` | Explicit output in AC | Mapping chi tiết xem Data Mapping |
| `data.visibility` | `TBD` | Explicit output in AC | Mapping chi tiết xem Data Mapping |

## 2. HTTP status

- Success HTTP status: `TBD` trừ khi Activity Diagram định nghĩa explicit.
- Error status explicit được liệt kê tại `06_Error.md`.

## 3. Response envelope

- Diagram target design không khóa đầy đủ envelope dùng chung cho 102 API.
- Không tự ép response hiện tại của backend (`success/businessCode/message/data/meta/traceId`) lên target DD vì đã chọn **diagram-first**.
- Envelope canonical: `TBD / SOURCE_REQUIRED` nếu diagram không chỉ rõ.
