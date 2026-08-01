# Review API DD — S2W-STUDY-API-004

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-004_GET_catalog_courses.xlsx`
- Endpoint: `GET /api/v1/catalog/courses`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J32` | `page` có min 0 trong khi convention bắt đầu từ 1; `page_size`/snake_case và giới hạn không nhất quán với chuẩn API. | `docs/BD/base/0. Study2Work_System_Architecture.md:699-710` | Dùng `page>=1`, `pageSize` với max thống nhất; chuẩn hóa `keyword`, `level` và các filter được BD duyệt. |
| P0 | `2.Response!A15:H30`, `3.Data mapping!A12:H14` | Payload và SQL dùng nhiều field không có trong `courses`: `short_description`, `duration`, các count tổng hợp, `related_paths`, `learner_access`, `search_document`, `technology`, `topic`, `admin_order`, `updated_at`. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:99-119`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Map field thật (`title`, `summary`, `level`, `estimated_minutes`, `publish_status`); chỉ thêm aggregate với query/definition cụ thể. |
| P1 | `2.Response!A15:H30` | Các count đang dùng kiểu String và các array/object không có schema. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:48-139,169-179` | Dùng Integer cho count; định nghĩa item schema, nullability và pagination total. |
| P1 | `4.Error` | `CONTENT_LOCKED` không phải lỗi của API list public. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:169-179` | Chỉ giữ validation, public visibility và lỗi hệ thống phù hợp. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.
