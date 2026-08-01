# Review API DD — S2W-STUDY-API-026

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-026_GET_onboarding_review.xlsx`
- Endpoint: `GET /api/v1/onboarding/review`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A16:H23`, `3.Data mapping!A12:H12`, `A20` | Review dùng các “cột” tổng hợp `basic_info`, `background`, `goals`, `selected_path`, `missing_fields` không tồn tại; `study_time` còn khai date-time dù nghiệp vụ là giờ học/tuần. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:139-150`; SQL `:287-301,340-359` | Compose từ `user_profiles`, onboarding columns và learning path; định nghĩa nested objects/types và derived missing fields. |
| P0 | `4.Error!A13:H15` | `ONBOARDING_REQUIRED` không thể là lỗi của màn review trước confirm; `ACTIVE_PATH_EXISTS` cũng không phải blocker để xem dữ liệu review. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:139-150,154-167` | Cho phép status in-progress; trả missing fields/selected-path invalid như dữ liệu hoặc lỗi cụ thể. |
| P1 | `3.Data mapping!A12:H12` | Không có filter `onboarding_records.user_id=:auth_user_id`, thiếu ownership. | `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:57-76`; SQL `:340-359` | Bắt buộc owner predicate và negative tests. |
| P1 | `2.Response!A21:H22` | “one active path rule” và “exception policy” không có version/text source; client có thể xác nhận nội dung không truy vết được. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:139-150` | Chốt policy identifier/version và chính xác nội dung learner xác nhận. |
| P0 | `2.Response!A9:E11`, `A24:H24` | Envelope cũ, snake_case và pagination mẫu thừa cho singleton. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope, bỏ pagination, dùng camelCase. |

## Điều kiện duyệt lại

- [ ] Review projection có schema nested và nguồn thật.
- [ ] Ownership, policy version và missing-field logic được test.
- [ ] Không còn lỗi completion/activation sai ngữ cảnh.
- [ ] Endpoint suy dẫn được owner phê duyệt.
