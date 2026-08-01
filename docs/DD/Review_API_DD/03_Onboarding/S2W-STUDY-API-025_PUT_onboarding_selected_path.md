# Review API DD — S2W-STUDY-API-025

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-025_PUT_onboarding_selected_path.xlsx`
- Endpoint: `PUT /api/v1/onboarding/selected-path`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `5.DB_Update_Main!A8:I10`, `3.Data mapping!A14:H14` | DD cập nhật `learning_path_id`, `updated_at`, `updated_by`, trong khi bảng thật dùng `selected_learning_path_id` và không có hai audit column sau. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:340-359` | Update đúng row theo `user_id`, đúng `selected_learning_path_id`; chốt version/concurrency nếu cần. |
| P0 | `2.Response!A16:H19`, `3.Data mapping!A12:H12` | `selected_path`, `selected_at`, `still_published`, `activation_not_started` bị coi là cột của onboarding record; ba field sau không tồn tại và các boolean còn khai String. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:123-150`; SQL `:323-359` | Trả selected path projection từ JOIN và boolean derived có type/source rõ; không giả cột. |
| P1 | `1.Request!A21:J21`, `4.Error!A16:H16` | Chỉ kiểm UUID; chưa định nghĩa path phải `PUBLISHED`/activatable, xử lý reselection và race path bị unpublish. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:137,186-194` | Recheck publish state trong transaction và stable error yêu cầu chọn lại. |
| P1 | `4.Error!A14:H15` | `ONBOARDING_REQUIRED`/`ACTIVE_PATH_EXISTS` được copy không đúng: chọn path là bước 7 trước completion, không phải activation. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:59-70` | Thay bằng invalid step/selection/state transition errors. |
| P0 | `2.Response!A9:E11` | Envelope và snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`. |

## Điều kiện duyệt lại

- [ ] Column mapping và ownership đúng schema.
- [ ] Publish/race/reselection policy được đặc tả.
- [ ] Response có kiểu và nguồn thật; error đúng bước chọn path.
- [ ] Endpoint suy dẫn được phê duyệt.
