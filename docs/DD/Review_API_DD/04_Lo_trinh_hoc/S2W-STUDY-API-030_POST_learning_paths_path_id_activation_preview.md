# Review API DD — S2W-STUDY-API-030

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-030_POST_learning_paths_path_id_activation_preview.xlsx`
- Endpoint: `POST /api/v1/learning-paths/{path_id}/activation-preview`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A14:H15`, `5.DB_Update_Main!A8:I10` | “Preview” lại được phân loại `UPDATE_ACTION`, lock và UPDATE `learning_paths.status`; còn tạo audit/notification. Một preview theo BD chỉ kiểm eligibility/hiển thị xác nhận. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:69-87,190-200` | Đổi thành read-only calculation; không mutate path/audit/notify. Nếu tạo token thì thiết kế store/TTL/purpose riêng. |
| P0 | `3.Data mapping!A12:H12` | Predicate dùng `learning_path_id` thay vì PK `id`; response fields như `eligible/checks/confirmation_token` bị SELECT như cột. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-414` | Query cột thật; derive checks từ user/onboarding/enrollment/path trong một snapshot. |
| P1 | `2.Response!A16:H23` | `eligible` khai String, course order/completion/community summary không có object schema; `confirmation_token` không có security/expiry/replay semantics. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:71-95` | Dùng boolean, typed checks/path summary và định nghĩa token hoặc bỏ token. |
| P1 | `4.Error!A15:H18` | Eligibility failures bị trộn giữa success checks và error (`ACTIVE_PATH_EXISTS`, path not published, conflict) nên client không biết preview trả 200 hay 409. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:69-87` | Khóa semantics: expected ineligibility là `eligible=false`; chỉ auth/not-found/system là transport error. |
| P0 | `2.Response!A9:E11` | Envelope không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`. |

## Điều kiện duyệt lại

- [ ] Preview hoàn toàn read-only.
- [ ] Eligibility checks/type/token semantics rõ và test được.
- [ ] Không còn query/cột giả; HTTP/business-error matrix nhất quán.
- [ ] Endpoint suy dẫn được phê duyệt.
