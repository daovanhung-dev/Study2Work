# Review API DD — S2W-STUDY-API-031

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-031_POST_learning_paths_path_id_activate.xlsx`
- Endpoint: `POST /api/v1/learning-paths/{path_id}/activate`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A22:J23`, `A26` | Direct contract dùng `accepted_rules` + optional `confirmation_token`, thiếu hai xác nhận mẫu `acceptedOneActivePathRule` và `confirmedLearningPathSummary`. | `docs/BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md:35-48` | Khớp exact sequence contract/camelCase hoặc có quyết định đổi contract. |
| P0 | `3.Data mapping!A14:H15`, `5.DB_Update_Main!A8:I11` | DD ghi input vào `learning_paths`; activation phải INSERT `learning_path_enrollments`, khởi tạo first `course_enrollments`, progress và outbox trong transaction. Các cột DD đều không có trên path. | `docs/BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md:17-30,94-97`; SQL `:387-437` | Transaction recheck + insert enrollment/course state; notification qua outbox sau commit; dùng unique active index. |
| P0 | `2.Response!A16:H21`, `A25` | Response thiếu `learningPathId`, `progressPercent=0`, structured `firstCourse` và `nextAction`; gán enrollment fields vào sai bảng. | `docs/BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md:51-74` | Trả exact `LEARNING_PATH_ACTIVATED` payload từ enrollment/first course. |
| P0 | `4.Error!A16:H18` | Error code `ACTIVE_PATH_EXISTS` không khớp explicit `LEARNING_PATH_ACTIVE_ALREADY_EXISTS`; không mô tả duplicate retry/idempotency và database unique conflict. | `docs/BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md:77-91`; SQL `:405-408` | Dùng stable code/field reason mẫu, `Idempotency-Key`, request hash và deterministic conflict mapping. |
| P0 | `2.Response!A9:E11` | Envelope cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`. |

## Điều kiện duyệt lại

- [ ] Exact SEQ05 request/response/error được giữ.
- [ ] Activation transaction ghi đúng enrollment/course/outbox, không mutate catalog path.
- [ ] Unique-concurrency và idempotent retry có test.
- [ ] Preconditions verified/onboarded/not suspended/published được recheck trong transaction.
