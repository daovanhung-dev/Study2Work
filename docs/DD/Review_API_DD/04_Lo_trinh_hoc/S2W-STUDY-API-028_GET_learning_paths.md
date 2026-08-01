# Review API DD — S2W-STUDY-API-028

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-028_GET_learning_paths.xlsx`
- Endpoint: `GET /api/v1/learning-paths`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | WHERE dùng `search_document`, `goal`, `difficulty`, `status`; các cột không tồn tại (`level`, `publish_status` mới là cột thật). Sort `order_index,created_at` cũng không có trên `learning_paths`. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-338` | Viết query trên cột thật hoặc migration FTS; whitelist filter/sort và chỉ trả path visible. |
| P0 | `2.Response!A16:H20` | `public`, learner enrollment state, progress, activation state bị coi là cột của `learning_paths`; `progress_percent` còn khai String. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:58-67`; SQL `:323-338,387-414` | Định nghĩa path summary và LEFT JOIN enrollment theo actor; percent numeric, derived activation reason rõ. |
| P1 | `1.Request!A23:J24` | Filter `difficulty/status` là free text và có thể cho learner yêu cầu DRAFT/ARCHIVED; BD chỉ cho learner mới kích hoạt path published. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:69-95,218-227` | Dùng enum canonical và server-enforced visibility; không tin filter client để mở nội dung. |
| P1 | `4.Error!A14:H16` | `ONBOARDING_REQUIRED`, `ACTIVE_PATH_EXISTS`, `PATH_NOT_PUBLISHED` bị dùng như lỗi list; các trạng thái này nên quyết định `activationAllowed/blockingReason`, không chặn xem. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:58-67` | Trả cards kèm action state; error chỉ cho auth/filter/system. |
| P0 | `2.Response!A9:E11`, `A21:H24` | Envelope/pagination snake_case trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-721` | Dùng canonical envelope và `meta.pagination.{page,pageSize,total}`. |

## Điều kiện duyệt lại

- [ ] Query/filter/sort chạy trên schema thật và không lộ non-public path.
- [ ] Learner state/progress có JOIN/typing/ownership rõ.
- [ ] List không bị chặn bởi activation-state errors.
- [ ] Contract/pagination canonical và endpoint suy dẫn được duyệt.
