# VERIFICATION_REPORT — Study API #66

## Kết quả

- DD status: Draft — Needs Confirmation.
- Deliverables: đủ 8 template sheets và 3 reports, tổng cộng đúng 11 Markdown files.
- Runtime API #66: UNWIRED / NOT_FOUND; không có route, module hoặc focused test.
- AC-26 macro-review #65–#67: VERIFIED_WITH_OPEN_QUESTIONS sau khi tạo DD #67; xem phần group review và [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).
- Runtime tests: không chạy; phạm vi docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Đã đọc đủ #48, #49, #50; không thiếu worklog cùng loại. | PASS |
| Catalog/diagram | Contract catalog #66 khớp method/path/actor/input/response/error set; AC-26 sequence #65 → #66 → #67 được ghi riêng. | PASS |
| Source/schema | Không tìm thấy route/module/test #66; DDL đã rà soát không có approved learner event ledger. | PASS — STATIC SOURCE REVIEW |
| Manifest/front matter | Đúng 11-file set; cả 8 sheet có dd_id 66 và Draft — Needs Confirmation. | PASS |
| Contract/error set | GET path, Bearer JWT/Mentor, course_id:int64!, no query/body, ApiEnvelope<Page<Course>>, HTTP 200; đúng 4 lỗi 401/403/404/500, không thêm direct error. | PASS |
| Response/data mapping | Course, PageMeta, envelope fields được liệt kê; candidate metrics tách biệt và đánh dấu DERIVED. | PASS |
| Template appendix | 8/8 phần appendix đối chiếu nguồn bằng byte với registered template suffix. | PASS |
| JSON/Markdown | JSON hợp lệ; relative links resolve; tables nhất quán; fences cân bằng; không có trailing whitespace. | PASS |
| `git diff --check` | Kiểm tra sau khi cập nhật report và worklogs. | PASS |
| AC-26 macro-review | #65 roster, #66 event analytics, #67 Student progress tách biệt; response/page gap, shared access/schema/error questions được ghi lại. | VERIFIED_WITH_OPEN_QUESTIONS |
| Runtime tests | Không chạy; docs-only và API chưa wired. | NOT_RUN |
| Context validator | Không áp dụng; không sửa context page hoặc manifest. | NOT_APPLICABLE |

## Output fingerprints — SHA-256

| Sheet | SHA-256 |
|---|---|
| 00_Cover.md | bff1d84f3557a4dcf31defe8826c3596e286c521ec5e440fb52c82e3b5ed9836 |
| 01_Lich_su.md | 6b779d051ed1951735262acf8f8f886a4e9d3276d17434992f41efdcef92039a |
| 02_Overview.md | fc53b372ec6c1a6b4e602eed36ea0e85a7e1564eb522a1eb6f41225036712ccf |
| 03_Request.md | c266e3540613e32ec1ee4e052acb5feb08b0e11e8346dfb87da0c6ac181dab2e |
| 04_Response.md | 16fd9ff208be787f5969d1e15f7d87e6db5f1a275490b4941c7d46f3f0e96451 |
| 05_Data_Mapping.md | caaaf6a10612b9e46a25c88595bd5cf11ecc8c68668725f640530eeb612e36c8 |
| 06_Error.md | 154fe64006a27262e3d2831039eeeb299366f0f2c9e4b1ee05c7a02c2d1c2947 |
| 07_table.md | 5b88409dea0e224b7c87466c1f2738172b6820a53eb8c7d38549a49607ae5c6d |

## Macro-review AC-26 #65–#67 — 2026-10-24

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — review tài liệu/source tĩnh sau khi DD #67 tồn tại.

- **Luồng:** Mentor mở dashboard; #65 trả class-level enrollment/progress candidate; #66 riêng course-wide learning-event candidate; UI chọn Student rồi gọi #67. Diagram không mô tả server-to-server calls.
- **Payload trực tiếp:** Cả ba catalog row đều khai báo `ApiEnvelope<Page<Course>>`, không schema nào chứa progress hoặc analytics. Đây là discrepancy nhóm; catalog được giữ nguyên trong các DD. Các PageMeta cũng không có page/size request nên chưa có pagination semantics/bounds.
- **Candidate boundary:** #65 là roster summary; #66 là event aggregate. `students_with_learning_events` đếm Student có event hợp lệ, không đồng nghĩa tổng enrollment của #65. Không dùng `lesson_progress`, `last_accessed_at`, progress snapshots hoặc `last_event_id` để thay event source #66.
- **Progress consistency:** #65 và #67 candidate dùng cùng tập lesson PUBLISHED và cùng formula floor-average; #67 chỉ thêm current state theo lesson cho Student được chọn. Candidate #67 không thêm quiz/assignment vì AC-26 không nêu chúng; API #37/AC-18 là flow khác. Tập eligible enrollment, status, duplicate progress rows, formula, rounding và empty behavior vẫn phải được duyệt.
- **Authorization/data:** Ba API yêu cầu Mentor role và course scope; #67 còn phải xác minh Student thuộc cùng roster eligibility như #65. Mentor principal binding, owner/assignment, privacy-aware 403/404 order và schema live chưa có nguồn.
- **Shared error gap:** Cả ba có direct error set 401/403/404/500. Guideline `data:null` khác helper `{}`; cả ba path chưa nằm trong middleware design-code allowlist. Cần đồng bộ khi wiring.
- **Runtime:** #65–#67 đều không có route/module/focused test source hiện tại; review này không phải runtime verification.

Xem [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md) và open questions của từng DD.

