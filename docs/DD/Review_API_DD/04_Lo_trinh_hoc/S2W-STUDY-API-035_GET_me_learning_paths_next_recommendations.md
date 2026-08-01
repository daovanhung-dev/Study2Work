# Review API DD — S2W-STUDY-API-035

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-035_GET_me_learning_paths_next_recommendations.xlsx`
- Endpoint: `GET /api/v1/me/learning-paths/next-recommendations`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Query `learning_paths.user_id` và SELECT `learning_path_id,reason,prerequisites_met,estimated_minutes,activation_allowed` dùng cột sai/không tồn tại. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-338,387-414` | Xác định completed enrollment của actor, query candidate published paths, derive reason/eligibility từ nguồn thật. |
| P0 | `2.Response!A16:H20` | `estimated_minutes` được gán cho learning path dù schema dùng `estimated_hours`; reason/prerequisites/activationAllowed không có thuật toán hay nguồn. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:127-141`; SQL `:323-338` | Dùng đúng duration unit; mô tả deterministic recommendation config/rules và human-readable reason. |
| P1 | `4.Error!A14:H15` | `ACTIVE_PATH_EXISTS` và `PATH_NOT_PUBLISHED` bị trả như errors cho list recommendations; nếu chưa đủ điều kiện nên trả empty/eligibility reason, candidate unpublished phải bị lọc. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:127-141` | Khóa eligibility/no-result semantics và chỉ trả published candidates. |
| P1 | `Lịch sử!A4:F4`, `Cover!B19` | Endpoint hoàn toàn suy dẫn nhưng `VERIFIED`, reviewer/approver trống và source/schema stale. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:135-141`; SQL `:1-31` | PO/API owner chốt có cần API riêng và thuật toán trước khi approve. |
| P0 | `2.Response!A9:E11` | Envelope/pagination mẫu không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton/list semantics, camelCase. |

## Điều kiện duyệt lại

- [ ] Eligibility/candidate/ranking/empty semantics được chốt.
- [ ] Query dùng completed enrollment và path fields thật.
- [ ] Duration/source/types và envelope đúng.
- [ ] Endpoint suy dẫn được phê duyệt.
