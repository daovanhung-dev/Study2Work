# Review API DD — S2W-STUDY-API-094

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-094_GET_admin_learning_paths.xlsx`
- Method + endpoint: `GET /api/v1/admin/learning-paths`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD ghi nguồn chỉ có 44 file và không có schema, trong khi `docs/BD` hiện có 48 file và có schema SQL. Căn cứ review vì thế bị stale. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; quy ước canonical tại `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật danh mục 48 file, ghi rõ thứ tự ưu tiên `base/0` → BD module → diagram/schema, và bỏ tuyên bố “không có schema”. |
| P0 | `2.Response!D9:D11`, `2.Response!A38` | Envelope `{data, meta}` / `{error}` và `request_id` không phải envelope canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng `success`, `businessCode`, `message`, `data`/`errors`, `traceId`; JSON camelCase. |
| P1 | `2.Response!A26`, `2.Response!C20:C23` | Đây là list nhưng pagination đặt trực tiếp trong `meta`, thiếu `totalPages`, dùng `page_size`; `request_id` cũng bị nhét vào `meta`. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-700,702-721` | Trả `data.items` và `meta.pagination.{page,pageSize,total,totalPages}`; `traceId` ở top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL còn `<FK condition>` và dùng các tên tổng hợp như cột thật, trong khi checklist tự đánh dấu không còn placeholder và đã review schema. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700,738-752`; schema `:323-385` | Thay bằng query/JOIN/GROUP BY thực thi được; chỉ tick checklist sau khi OpenAPI, schema và query được kiểm chứng. |
| P0 | `1.Request!D22:I27`, `3.Data mapping!F12`, `3.Data mapping!A20` | Filter/mapping dùng `learning_paths.status`, `difficulty`, `updated_by`, `search_document`, `order_index`, `created_at`; các cột này không tồn tại. Schema dùng `publish_status`, `level` và bảng không có audit timestamps/FTS. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-338` | Đổi filter thành enum `publishStatus`, `level`; bỏ hoặc bổ sung có migration các filter `updatedBy`/FTS/sort. WHERE phải dùng alias `m` và cột thật. |
| P0 | `2.Response!C16:H19` | `admin`, `publication_status`, `course_count`, `learner_impact_count` bị khai là cột của `learning_paths`; hai count còn sai kiểu `String`. | Schema `:323-338,376-414`; yêu cầu xem tác động tại `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md:159-167` | Trả summary có `id,title,slug,level,publishStatus`; count là integer và được tính bằng JOIN/aggregate có định nghĩa rõ. |
| P1 | `4.Error!A13:H16` | Error của learner (`ACCOUNT_NOT_VERIFIED`, `ONBOARDING_REQUIRED`, `ACTIVE_PATH_EXISTS`, `PATH_NOT_PUBLISHED`) không liên quan API admin đọc danh sách. | Vai trò module tại BD-10 `:24-31`; chức năng quản lý lộ trình `:57-70` | Giữ lỗi thực tế: authn, permission, validation filter, rate/system; bỏ lỗi onboarding/kích hoạt lộ trình. |

## Checklist duyệt lại

- [ ] Danh mục nguồn là 48 file và có thứ tự ưu tiên tài liệu.
- [ ] Success/error theo canonical envelope, camelCase và có `traceId`.
- [ ] List dùng `data.items` + `meta.pagination`; không còn pagination mẫu sai.
- [ ] Filter, enum, kiểu dữ liệu và sort chỉ dùng cột/schema có thật.
- [ ] Query JOIN/count thực thi được, không còn placeholder.
- [ ] Error catalog chỉ chứa tình huống của API admin này.
- [ ] Permission `study.content.manage` được map tới RBAC vật lý.
- [ ] OpenAPI và test bao phủ filter, paging, permission và aggregate count.
