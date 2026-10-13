---
title: "Overview"
order: 2
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 26 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | `/api/v1/lessons/{lesson_id}/resources` |
| Purpose | Lấy dữ liệu tài nguyên gắn với lesson trong flow xem nội dung bài học; response projection chưa được contract làm rõ. |
| Consumer/Actor | Student / learning UI |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Role Student; AC-15 yêu cầu Student có quyền xem lesson, nhưng policy/predicate cho lời gọi API #26 chưa được đặc tả. |
| Basis | DIRECT — API catalog và AC-15 diagram cho method/path/actor/request/status; candidate resource relation từ DB design. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET/read-only theo contract. |
| Side effects | Không có mutation được khai báo; signed URL/external storage behavior chưa được API #26 xác nhận. |

## Sources

- [docs/lists/list_api.md](../../../../../docs/lists/list_api.md) — API #26 và reusable `ApiEnvelope<T>`, `Lesson`, `Resource` schemas.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-15 precondition/postcondition và endpoint list.
- [AC-15 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — Student flow và “Đọc lesson resources”.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — ERD V1 field/relation evidence và `visibility` discrepancy.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL, design evidence only.
- [Study router](../../../app/api/v1.py), [module inventory](../../../app/modules/) và [test inventory](../../../tests/) — current runtime comparison.
- [API #12 resource detail DD](../12_resources_detail/02_Overview.md) — adjacent design context; không dùng để khẳng định API #26 gọi API #12.

## Tables read

- `resources` — candidate read source từ ERD/DDL; query API #26 chưa được wire hoặc xác nhận.
- `lessons` — candidate parent/access context; API #26 join/access query chưa được đặc tả.

## Tables write

- `N/A — READ-ONLY API; không có DB mutation.`

## Mục chú ý

- Catalog và AC-15 diagram khai báo `ApiEnvelope<Lesson>`; endpoint name/purpose nói về tài nguyên, còn reusable `Resource` là schema riêng.
- ERD relation `resources.lesson_id → lessons.id` là candidate mapping, không xác nhận query, response cardinality hoặc live schema.
- API #12 có thiết kế signed URL cho private resource; không có source xác nhận API #26 gọi API #12 hoặc tự resolve URL.

## Assumptions

- Giữ method, path, actor, input, response type và codes theo API catalog cho đến khi canonical source được cập nhật.
- Dùng `resources.lesson_id` làm candidate relationship duy nhất để mô tả nguồn đọc; không đóng khung SQL hoặc thứ tự kết quả.
- Giữ status `Draft — Needs Confirmation` vì response payload và access/storage rules chưa được xác nhận.

## Conflicts

- `DISCREPANCY`: contract response `ApiEnvelope<Lesson>` không khai báo `Resource[]`; endpoint/AC intent là lấy tài nguyên đính kèm.
- `DISCREPANCY`: reusable `Resource.visibility` không có cột `resources.visibility` trong ERD/DDL.
- `DISCREPANCY`: ERD ghi `resources.lesson_id` bắt buộc, checked-in DDL không khai báo `NOT NULL`.
- API #26 route/module/query/focused test không có trong current Study source inventory (`UNWIRED / NOT_FOUND`).

## Security note

- Không kết luận predicate enrollment, prerequisite, publish state hoặc 403/404 split từ AC-15 precondition.
- Không suy ra quyền truy cập resource từ `visibility`, vì schema không có cột visibility đã xác nhận.
- Không đưa raw SQL, credential hoặc storage internals vào response.

## Performance note

- Contract không có pagination hoặc sort parameter.
- Không tự thêm ordering, pagination, cache hoặc signed URL operation.
- Cardinality và hiệu năng query phụ thuộc quyết định response/query còn mở.

