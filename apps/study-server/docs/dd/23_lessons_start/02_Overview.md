---
title: "Overview"
order: 2
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 23 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/lessons/{lesson_id}/start |
| Purpose | Bắt đầu học lesson và ghi nhận tiến độ IN_PROGRESS trong AC-14. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | role=Student theo catalog; entitlement/enrollment rule cho lời gọi trực tiếp chưa được chốt. |
| Basis | DIRECT — API catalog và AC-14 |
| Status | Draft — Needs Confirmation |
| Transaction | SOURCE_REQUIRED — transaction boundary và atomicity chưa được định nghĩa. |
| Side effects | AC-14 mô tả UPSERT lesson progress = IN_PROGRESS; chi tiết cột và conflict target chưa xác nhận. |

## Sources

- [API #23 catalog row](../../../../../docs/lists/list_api.md) — method, path, actor, input, response và status/business codes.
- [AC-14 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và chuỗi API #22–#25.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — access decision trước API #23 và UPSERT progress sau API #23.
- [DB design](../../diagrams/DB_UNICA_TABLES.md) và [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate lesson_progress schema, không phải xác nhận live schema.
- [Current router](../../../app/api/v1.py), [Study app modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu runtime wiring hiện tại.

## Tables read

- lessons — candidate để định danh Lesson trong response catalog; query/projection API #23 chưa xác nhận.
- lesson_progress — candidate cần kiểm tra để thực hiện UPSERT; khóa và lookup predicate chưa xác nhận.
- Nguồn access/enrollment — AC-14/API #22 nêu bước kiểm tra trước start; nguồn query/API cho #23 chưa xác nhận.

## Tables write

- lesson_progress — AC-14 design flow ghi status IN_PROGRESS; physical write mapping chưa đủ nguồn để chốt.

## Mục chú ý

- API #23 là POST có side effect theo AC-14. DDL checked-in chỉ là schema design evidence; không chứng minh query, constraint hoặc live availability.
- API #22 access check, API #23 start, API #24 lesson retrieval và API #25 progress update là các bước/API riêng.
- Catalog khai báo ApiEnvelope<Lesson> và HTTP 201 DESIGN_RESOURCE_CREATED; diagram chỉ ghi ApiEnvelope và mô tả UPSERT. Giữ catalog làm contract response và ghi khác biệt để xác nhận.
- HTTP 422 được catalog khai báo dù request chỉ có path parameter; trigger/validation rule cụ thể chưa có nguồn.

## Assumptions

- Không chốt business assumption về khóa UPSERT, user identity binding, state transition, timestamp, transaction hoặc gọi lại; các điểm này nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## Expected behavior

- Student gửi Bearer JWT và path lesson_id dạng int64 bắt buộc.
- AC-14 mô tả kiểm tra access ở bước API #22 trước API #23; nếu flow tiếp tục thì API #23 UPSERT lesson progress thành IN_PROGRESS.
- Catalog quy định HTTP 201 DESIGN_RESOURCE_CREATED với ApiEnvelope<Lesson>; lỗi gồm 401, 403, 404, 422 và 500 cùng business codes đã công bố.

## Current behavior

- Không tìm thấy route, module, query hoặc focused test cho API #23 trong Study Server source/test hiện tại.
- Không tìm thấy runtime use of lesson_progress trong app/tests; checked-in DDL có bảng thiết kế candidate.
- Runtime status: UNWIRED / NOT_FOUND. Design contract/diagram không chứng minh endpoint hoặc mutation đã chạy.

## Conflicts

- DISCREPANCY: Catalog trả ApiEnvelope<Lesson>, diagram chỉ ghi ApiEnvelope; chưa có runtime serializer để đối chiếu.
- DISCREPANCY: Catalog gọi thành công 201 RESOURCE_CREATED trong khi AC-14 mô tả UPSERT; semantics khi bản ghi đã tồn tại chưa được quy định.
- ACCESS/404/422 details SOURCE_REQUIRED: code có trong catalog nhưng điều kiện API #23 chưa được đặc tả.

## Security note

- Không nhận user_id từ client; cách lấy identity từ JWT và bind tới lesson_progress.user_id cần nguồn xác nhận.
- Không suy luận lần gọi API #22 trước đó thay thế authorization check cho lời gọi API #23 độc lập.

## Performance note

- Contract không quy định latency/index/query plan. DDL không khai báo unique key cho cặp user_id/lesson_id; không đề xuất index hoặc khóa upsert trong DD này.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
