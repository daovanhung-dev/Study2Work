---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-INT-011"
api_name: "GET wss://work-api.study2work.vn/api/v1/realtime"
status: "Draft — Needs Confirmation"
---

# Request

## WebSocket handshake

| Thuộc tính | Giá trị | Handling |
| ---: | --- | --- |
| URI | `wss://work-api.study2work.vn/api/v1/realtime` | DIRECT protocol endpoint. |
| Client authentication | Access token via secure subprotocol or first authentication frame | DIRECT lifecycle contract; exact physical carrier remains SOURCE_REQUIRED. |
| Connection authorization | Server checks recipient object, session and projection | DIRECT lifecycle contract. |

## Client message contract

| No | Message | Field | Value | Status | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- |
| 1 | subscribe | `type` | `subscribe` | DIRECT named field/value. | [S03](./05_Data_Mapping.md#s03) |
| 2 | subscribe | `applicationId` | `SOURCE_REQUIRED` | DIRECT named field; type/requiredness is not split by source. | [S03](./05_Data_Mapping.md#s03) |
| 3 | subscribe | `lastSequence` | `SOURCE_REQUIRED` | DIRECT named field; type/requiredness is not split by source. | [S03](./05_Data_Mapping.md#s03) |

## Connection lifecycle

- Liveness check every 25 seconds; timeout after 60 seconds.
- Client reconnects with exponential backoff.
- Subscription authorization is evaluated per application and recruiter assignment.

## Server event linkage

- Server event frame and at-least-once delivery semantics are defined in [04_Response.md](./04_Response.md).

## Contract source

> Ứng dụng khách gửi mã truy cập qua giao thức con bảo mật/khung xác thực đầu tiên; máy chủ kiểm đối tượng nhận/phiên/bản chiếu. Đăng ký theo dõi `{type:"subscribe", applicationId, lastSequence}`; máy chủ kiểm quyền cho từng đơn ứng tuyển và phân công nhà tuyển dụng. Sự kiện `message.created`, `message.tombstoned`, `receipt.updated`, `conversation.read_only`, `interview.changed`, `notification.created`. Có `eventId`, `sequence`, `occurredAt`; giao ít nhất một lần nên ứng dụng khách khử trùng lặp và phát hiện khoảng trống rồi gọi lịch sử REST. Gói kiểm tra sống mỗi 25 giây, hết thời gian 60 giây, kết nối lại theo cấp số nhân. Kết nối WebSocket không là nguồn dữ liệu và không nhận chuyển trạng thái ATS.

## Ví dụ client message

N/A — a complete physical WebSocket frame schema is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
