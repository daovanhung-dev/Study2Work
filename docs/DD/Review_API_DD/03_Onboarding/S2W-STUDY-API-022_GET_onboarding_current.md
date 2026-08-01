# Review API DD — S2W-STUDY-API-022

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-022_GET_onboarding_current.xlsx`
- Endpoint: `GET /api/v1/onboarding/current`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A9:E11`, `A22:H22` | Response dùng envelope cũ, snake_case và `meta.request_id`. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Chuyển sang canonical envelope/camelCase/`traceId`. |
| P0 | `2.Response!A17:H21`, `3.Data mapping!A12:H12`, `A20` | `current_step` bị khai String dù DDL là Integer; `completed_steps`, `draft_answers`, `last_saved_at` và `selected_path_id` không tồn tại. Cột thật là `selected_learning_path_id`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:340-359`; `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:76-96` | Map `status/currentStep/selectedLearningPathId` từ cột thật; nếu cần draft chi tiết phải chốt storage/schema thay vì giả cột. |
| P0 | `4.Error!A13:H15` | API dùng để bắt đầu/tiếp tục onboarding nhưng lại trả `ONBOARDING_REQUIRED`; `ACTIVE_PATH_EXISTS` và `PATH_NOT_PUBLISHED` cũng không liên quan tải bản nháp. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:87-96,186-194`; `docs/BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md:15-20` | Cho phép learner chưa hoàn tất tải current; chỉ chặn unverified/suspended và xử lý record chưa tồn tại bằng trạng thái `NOT_STARTED`. |
| P1 | `3.Data mapping!A12:H12`, `A20` | Query không có điều kiện `user_id=:auth_user_id`, nên thiếu ownership và có nguy cơ trả draft người khác. | `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:57-76`; SQL `:340-359` | Bắt buộc lookup theo unique `onboarding_records.user_id`; thêm negative ownership test. |
| P1 | `Lịch sử!A4:F4`, `00.Hướng dẫn!A17:B18` | Workbook `VERIFIED` dù response/query còn placeholder và chưa có reviewer. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Hạ trạng thái, hoàn thiện OpenAPI/query/test rồi review lại. |

## Điều kiện duyệt lại

- [ ] Current contract biểu diễn đúng `NOT_STARTED/IN_PROGRESS/COMPLETED` và draft storage thật.
- [ ] Query owner-safe, không chặn learner vì chính `ONBOARDING_REQUIRED`.
- [ ] Kiểu/cột và envelope khớp canonical/schema.
