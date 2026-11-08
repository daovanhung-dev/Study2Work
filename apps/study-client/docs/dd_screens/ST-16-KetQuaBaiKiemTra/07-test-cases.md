# ST-16 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-16-TC-001` | Planning ref / not run | `AC-16` | See source acceptance section | P1 |

## 2. Test planning references

### ST-16-TC-001 — Acceptance planning reference (AC-16)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-16](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-16`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md).

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
