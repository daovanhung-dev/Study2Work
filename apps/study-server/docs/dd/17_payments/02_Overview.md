---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 17 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/payments |
| Purpose | Khởi tạo/xác nhận thanh toán cho Order trong nhánh paid course của AC-12 |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Role=Student theo contract; order ownership policy SOURCE_REQUIRED |
| Basis | DIRECT — approved design contract; flow context từ AC-12 |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | SOURCE_REQUIRED — ranh giới giữa Operation, payments và gateway chưa được đặc tả |
| Side effects | Contract trả HTTP 202 Operation; DB_UNICA_TABLES đánh dấu payments INSERT/external payment ở mức DESIGN_ONLY |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — endpoint, auth, request, Operation/Payment schemas và business codes API #17/#18.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12: nhánh free bỏ qua payment; nhánh paid gọi API #16, API #17 và Payment Gateway.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — payments columns/relationships, API #17 DESIGN_ONLY và không có runtime method.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — thiết kế ERD V1.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in payments table; không có orders hoặc operations.
- [database.md](../../../../../.agents/server-study/database.md) — DB.sql là schema/design artifact; live metadata chưa xác minh.
- [v1.py](../../../app/api/v1.py), [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) — current route declarations không có API #17.
- [OPEN_QUESTIONS.md API #16](../16_orders/OPEN_QUESTIONS.md) — Order schema/provider relationship chưa được giải quyết.

## Tables read

- Logical Order theo request order_id — physical table/query SOURCE_REQUIRED; V1 không khai báo bảng orders.
- Không có query/API lookup cụ thể nào được đặc tả cho API #17.

## Tables write

- payments — DB_UNICA_TABLES đánh dấu API #17 là INSERT/external payment ở DESIGN_ONLY; cách map từng giá trị được ghi trong [07_table.md](./07_table.md).
- Operation store — SOURCE_REQUIRED; reusable schema chỉ định hình dạng Operation, không chỉ định persistence.
- Payment Gateway — external call trong AC-12; protocol và ranh giới side effect SOURCE_REQUIRED.

## Mục chú ý

- API catalog có trạng thái APPROVED_DESIGN_CONTRACT nhưng chưa runtime-verified.
- API #17 nhận order_id:int64 và provider:string; contract không nêu provider allowlist hoặc order eligibility.
- Success contract là HTTP 202 DESIGN_OPERATION_ACCEPTED với ApiEnvelope<Operation>.
- AC-12 chỉ mô tả gateway success → paid/tiếp tục ghi danh; failure/cancel → dừng flow. Không chỉ định callback, retry, status transition hoặc response mapping cho payment failure.
- Payment schema có order_id nhưng DB.sql không có payments.order_id và không khai báo bảng orders.
- Không thêm HTTP 404/409 hoặc business code ngoài danh sách API #17.

## Assumptions

- API #17 được gọi trong nhánh paid course sau API #16 theo AC-12.
- API #17 trả Operation theo catalog; giá trị kind/status và cách lưu Operation chưa được xác định.
- Mapping gợi ý trong 07_table.md chỉ phản ánh cột có trong schema thiết kế, không phải implementation SQL đã được phê duyệt.

## Conflicts

- SOURCE_REQUIRED / DISCREPANCY: logical Payment.order_id không có cột tương ứng trong payments; physical orders table cũng vắng mặt.
- DISCREPANCY: list_api.md convention, Operation.id và AC diagrams dùng UUID cho operation_id; dòng API #18 lại khai báo path int64.
- DISCREPANCY: DB.sql cho phép NULL ở payments.user_id/course_id, còn DB_UNICA_TABLES gọi hai FK này là bắt buộc.
- SOURCE_REQUIRED: enum member values và storage model của Operation/Payment chưa có nguồn.
- UNWIRED / NOT_FOUND: runtime route/module/query/test API #17 không được tìm thấy.

## Security note

- Giữ Bearer JWT và role Student theo contract.
- Caller-to-order ownership, Order status/eligibility và user_id source chưa được xác nhận; không tự thêm authorization query hoặc HTTP error.
- Không đưa credential/provider secrets vào request/response DD.

## Performance note

- Contract không quy định timeout, retry, idempotency, queue SLA hoặc gateway latency.
- Không đề xuất queue, worker hoặc index khi chưa có persistence/protocol source.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md.
- Sheet logic: Overview.
