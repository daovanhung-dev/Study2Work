# ST-16 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-16-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Điểm/trạng thái chấm và feedback nếu được trả; không lộ đáp án ngoài policy.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #32 Draft Q-32-01…06 còn mở về ownership, pending score, answer/feedback disclosure, shape/order và path/error; Student #32 route/module/test NOT_FOUND; Study Web UNWIRED; legacy BIGINT và V1-PILOT UUID attempt/answer models lệch, adapter/live schema chưa xác minh; PNG loaded Student và HTML unavailable Guest khác nhau, cả hai chưa khớp design target; screenshot fields/CTAs thiếu nguồn
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu, blocker và nguồn

### F.1. Blocker/discrepancy cần owner xử lý

1. Implement/register Student API #32 and Study Web route/UI; define current auth/ownership behavior and verify source/tests before calling it runnable.
2. Approve `attempt_id` parsing/range behavior and 403-vs-404 owner masking without adding errors beyond catalog unless the canonical contract changes.
3. Define when result is readable and exact `AttemptStatus` enum/transitions; specify pending score as omit/null/partial and behavior for non-GRADED/PENDING states.
4. Approve Student disclosure after grading: selected answers, correctness, per-answer score, answer key timing and feedback projection. Do not expose answer keys until policy says so.
5. Resolve logical/physical answer shape, text/multi-select storage, empty answer semantics and answer ordering; candidate DDL is not live evidence.
6. Resolve AC-16 feedback source/field. Do not add a `feedback` field without an approved schema/API change.
7. Decide which screenshot claims to remove or supply canonical sources for quiz title, passing threshold, GPA, skill metrics, question content, duration, attempt ordinal and next-lesson unlock.
8. Define PDF generation, course-outline, next-lesson destinations and eligibility/data handoff before activating controls.
9. Reconcile PNG loaded Student state with HTML unavailable Guest state and orphan review-filter script; align the selected design with the Study Web target's font, tokens, spacing and responsive controls.
10. Resolve the legacy BIGINT `quiz_attempts` model versus V1-PILOT UUID `assessment_attempts` model, including lifecycle, answer shape and the approved API #32 adapter; do not infer live schema from either design artifact.

### F.2. Checklist

- [x] ST-16 plan written before marker map/annotation/DD.
- [x] Original `screen.png` and `code.html` preserved; both baselines recorded.
- [x] 38 ordered markers map one-to-one to 38 element IDs in section C.
- [x] Route/load, both grading branches, review filters, navigation actions and API/auth/error states described.
- [x] API catalog, API #32 Draft DD, AC-16, candidate DDL and current missing route/source are kept distinct.
- [x] Expected/current behavior and screenshot/HTML discrepancy are recorded.
- [x] Legacy BIGINT versus V1-PILOT UUID schema discrepancy and Study Web design-system mismatch are recorded with source links.
- [x] Static marker audit: 38 sequential markers, 38 corresponding DD rows/SVG groups, unique in-bounds targets and resolved local links; original PNG/HTML hashes retained.
- [ ] Resolve F.1 blockers before declaring DD READY or implementation-ready.
- [ ] Verify actual route/API/runtime before marking RUNTIME VERIFIED.

### F.3. Nguồn truy vết

- [ST-16 plan](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_PLAN.md), [marker map](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_markers.json), [annotated screen](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen_annotated.png), [source PNG](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen.png), [HTML companion](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/code.html).
- [Screen inventory, F05 and G-09](../../list_screen.md); [ST-15 handoff](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md).
- [API catalog #32 and QuizAttempt/QuizAnswer schema](../../../../../docs/lists/list_api.md).
- API #32 DD: [overview](../../../../study-server/docs/dd/32_attempts_result/02_Overview.md), [request](../../../../study-server/docs/dd/32_attempts_result/03_Request.md), [response](../../../../study-server/docs/dd/32_attempts_result/04_Response.md), [mapping](../../../../study-server/docs/dd/32_attempts_result/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/32_attempts_result/06_Error.md), [open questions](../../../../study-server/docs/dd/32_attempts_result/OPEN_QUESTIONS.md).
- [API #31 grading questions](../../../../study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md); [AC-16 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md); [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [Candidate table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md); [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql); [V1-PILOT candidate schema](../../../../../infra/postgres/02_study_db.sql); [current route inventory](../../../../../.agents/server-study/apis/declared-routes.md).
- [Study Web design target](../../../../../.agents/web-study/design.md); [Study Web scope status](../../../../../.agents/web-work/study/INDEX.md).
- [Study Web source status](../../../../../.agents/web-work/study/INDEX.md); [Study Web design target](../../../../../.agents/web-study/design.md).

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
