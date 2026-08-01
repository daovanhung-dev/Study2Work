# Review API DD — S2W-STUDY-API-023

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-023_PATCH_onboarding_draft.xlsx`
- Endpoint: `PATCH /api/v1/onboarding/draft`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A21:J23`, `A26` | Request `step_code`, generic `answers`, String `current_step` không khớp contract trực tiếp SEQ04: numeric `currentStep` và các nhóm `basicInfo`, `learningBackground`, `goals`, `weeklyStudyHours`. | `docs/BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md:46-67`; `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:98-137` | Giữ đúng shape sequence bằng camelCase, định nghĩa field-level validation/null/clear semantics. |
| P0 | `5.DB_Update_Main!A8:I12`, `3.Data mapping!A14:H14`, `A20` | Ghi `step_code`, `answers`, `updated_at`, `updated_by`; bốn cột này không có trong `onboarding_records`. UPSERT cũng không nêu conflict key `user_id`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:340-359` | Map vào các cột thật hoặc bổ sung migration draft JSON/version; upsert theo `user_id` và kiểm ownership. |
| P0 | `2.Response!A16:H21`, `A25` | `saved` bị khai String enum, response dựa trên các cột giả và không trả `recordId/status/currentStep` như mẫu SEQ04. | `docs/BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md:69-83` | Trả business code `ONBOARDING_DRAFT_SAVED` cùng record ID, `ONBOARDING_IN_PROGRESS`, current step và version/save time nếu được chốt. |
| P1 | `4.Error!A14:H16` | `ONBOARDING_REQUIRED`, `ACTIVE_PATH_EXISTS`, `PATH_NOT_PUBLISHED` không phải lỗi của lưu draft; thiếu lỗi invalid-step, lost update và suspended-mid-flow rõ nghĩa. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:87-96,186-194` | Thiết kế stable business codes theo step/state và optimistic version. |
| P0 | `2.Response!A9:E11` | Envelope/error shape cũ, snake_case. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase/`traceId`. |

## Điều kiện duyệt lại

- [ ] Request/response khớp SEQ04 hoặc có quyết định thay contract.
- [ ] Draft có storage, conflict key và concurrency thật.
- [ ] Error matrix chỉ chứa tình huống lưu draft.
- [ ] Không còn cột/placeholder không tồn tại.
