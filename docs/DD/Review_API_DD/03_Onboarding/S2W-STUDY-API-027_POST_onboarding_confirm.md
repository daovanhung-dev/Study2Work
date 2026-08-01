# Review API DD — S2W-STUDY-API-027

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-027_POST_onboarding_confirm.xlsx`
- Endpoint: `POST /api/v1/onboarding/confirm`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A21:J23`, `A26` | Direct DD đổi request mẫu `selectedLearningPathId`, `confirmedInformation`, `acceptedOneActivePathRule` thành `selected_path_id`, `confirmed`, `accepted_learning_rules`. | `docs/BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md:86-95` | Giữ contract trực tiếp/camelCase hoặc ghi quyết định breaking-contract có traceability. |
| P0 | `2.Response!A16:H20`, `A24` | `confirmed_at` bị khai Boolean; example trả `account_status="ACTIVE"` và placeholder, trái contract `READY_TO_LEARN`, selected ID và `ACTIVATE_LEARNING_PATH`. | `docs/BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md:98-112`; `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:44-55` | Trả `ONBOARDING_COMPLETED`, timestamp đúng type, readiness `READY_TO_LEARN`, selected ID và next action; không activate. |
| P0 | `5.DB_Update_Main!A8:I12`, `3.Data mapping!A14:H15` | Ghi năm cột không tồn tại (`selected_path_id`, `confirmed`, `accepted_learning_rules`, `updated_at`, `updated_by`) và side effect audit/notification chung chung; không atomically set `status`, `selected_learning_path_id`, `confirmed_at` cùng Study readiness. | SQL `:239-249,340-359`; `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:139-166` | Transaction recheck mandatory fields/path, update đúng cột/status, update readiness projection theo quyết định; tuyệt đối không tạo enrollment. |
| P0 | `4.Error!A14:H14` | `ONBOARDING_REQUIRED` được dùng làm lỗi cho chính thao tác hoàn tất onboarding; thiếu `MISSING_REQUIRED_FIELDS` và selected-path-unpublished/reselection rõ. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:186-194` | Thiết kế errors theo missing fields, invalid confirmation, suspended và stale selected path. |
| P0 | `2.Response!A9:E11` | Envelope không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`; giữ stable code từ SEQ04. |

## Điều kiện duyệt lại

- [ ] Request/response/business code khớp SEQ04.
- [ ] Confirm atomic, đúng cột/state và không tự activate path.
- [ ] Errors bao phủ missing fields, suspended và race unpublish.
- [ ] Test chứng minh idempotent retry không tạo side effect trùng.
