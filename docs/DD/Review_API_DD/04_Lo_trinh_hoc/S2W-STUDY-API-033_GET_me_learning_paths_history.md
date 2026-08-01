# Review API DD — S2W-STUDY-API-033

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-033_GET_me_learning_paths_history.xlsx`
- Endpoint: `GET /api/v1/me/learning-paths/history`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Filter `learning_paths.status/user_id` sai bảng; lịch sử thuộc `learning_path_enrollments`. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:387-414` | Query enrollment theo owner/status, JOIN path; sort `started_at` thay cột giả. |
| P0 | `2.Response!A16:H22` | `activated_at`, `cancelled_at`, `progress_snapshot` không tồn tại; cột thật là `started_at`, `completed_at`, `progress_percent`, `admin_reason`. | SQL `:387-403`; `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:166-184` | Dùng field/state thật hoặc bổ sung snapshot/cancel timestamp bằng migration có lý do. |
| P1 | `1.Request!A21:J23` | `status` là free text; không liệt kê canonical enrollment states và page min ghi 0 dù format nói ≥1. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:166-184`; `docs/BD/base/0. Study2Work_System_Architecture.md:702-721` | Enum chính xác, page min 1, cap pageSize. |
| P1 | `3.Data mapping!A13:H13` | History access khi path/content archived chưa được khóa, dù BD yêu cầu policy xem lại riêng. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:143-151` | Chốt historical access/redaction/version policy và tests. |
| P0 | `2.Response!A9:E11`, `A23:H26` | Pagination/envelope snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-721` | `meta.pagination` camelCase và `traceId`. |

## Điều kiện duyệt lại

- [ ] History query dùng enrollment + owner, enum/timestamps đúng.
- [ ] Có historical content access policy.
- [ ] Pagination/envelope canonical, không còn fields giả.
- [ ] Endpoint suy dẫn được duyệt.
