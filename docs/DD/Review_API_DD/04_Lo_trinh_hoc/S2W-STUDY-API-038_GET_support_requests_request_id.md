# Review API DD — S2W-STUDY-API-038

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-038_GET_support_requests_request_id.xlsx`
- Endpoint: `GET /api/v1/support-requests/{request_id}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate dùng `support_requests.request_id`, cột không tồn tại, và không lọc `user_id` owner. PK thật là `id`. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:662-689` | `WHERE id=:requestId AND user_id=:actor`; safe 404 cho không tồn tại/không sở hữu. |
| P0 | `2.Response!A16:H20` | `request`, `admin_response`, `decision_at`, `resulting_path_state` là field giả; schema có request fields, `admin_decision`, `resolved_at`, còn resulting path phải JOIN/audit. | SQL `:662-729`; `docs/BD/11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md:91-119` | Định nghĩa typed request detail từ cột thật; chỉ trả support-safe result/audit projection. |
| P1 | `2.Response!A16:H16` | Toàn bộ request bị ép String, không mô tả type/reason/current/target/status; client không thể hiển thị lịch sử xử lý. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:153-162` | Trả object typed, enum/nullability rõ. |
| P1 | `4.Error!A13:H13` | `resource_id` trong error không khớp path `request_id`; thiếu ownership-safe semantics. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Field error đúng `requestId`; chống enumeration. |
| P0 | `2.Response!A9:E11` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton response. |

## Điều kiện duyệt lại

- [ ] Query dùng PK + owner filter.
- [ ] Typed detail/result projection có nguồn thật.
- [ ] Safe not-found/error và canonical envelope.
- [ ] Endpoint suy dẫn được duyệt.
