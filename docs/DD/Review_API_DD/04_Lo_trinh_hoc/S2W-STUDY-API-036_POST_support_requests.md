# Review API DD — S2W-STUDY-API-036

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-036_POST_support_requests.xlsx`
- Endpoint: `POST /api/v1/support-requests`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A21:J25`, `A28` | Direct SEQ12 contract dùng `type="CHANGE_LEARNING_PATH"`, current/target learning-path IDs; DD đổi thành enum `CHANGE,RESET,CANCEL` và bắt buộc enrollment ID. | `docs/BD/diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md:46-57` | Khớp direct contract hoặc chốt một canonical vocabulary cùng module 11/schema. |
| P0 | `7.DB_Insert_Main!A8:I14` | Insert dùng `request_type,current_enrollment_id,target_path_id,note,created_at,created_by`; schema thật dùng `type,user_id,current_learning_path_id,target_learning_path_id,current_learning_path_enrollment_id` và không có note/timestamps. Thiếu `user_id` là lỗi ownership nghiêm trọng. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:662-682` | Map đúng cột/enum; bổ sung migration nếu cần note/createdAt; luôn set actor `user_id`. |
| P0 | `2.Response!A16:H19` | `request_id`, `submitted_at`, `expected_next_step` không tồn tại; direct response chỉ cam kết ID + `OPEN`. | `docs/BD/diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md:60-73`; SQL `:662-682` | Trả `SUPPORT_REQUEST_CREATED`, `data.requestId=id`, `status=OPEN`; chỉ thêm field có nguồn thật. |
| P1 | `4.Error!A12:H13` | Thiếu lỗi endpoint-specific: không có active path/context, target trùng/current, target not published, duplicate open request; chỉ generic validation/conflict. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:153-162`; SQL `:673-681` | Thêm cross-field/state errors và chính sách duplicate/idempotency. |
| P0 | `2.Response!A9:E11` | Envelope cũ. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`. |

## Điều kiện duyệt lại

- [ ] Contract/vocabulary khớp SEQ12 và module 11.
- [ ] Insert đúng cột, actor ownership và cross-field validation.
- [ ] Response/error/idempotency có test endpoint-specific.
