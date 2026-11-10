# ST-17 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-17-TC-001` | Planning ref / not run | `AC-17` | See source acceptance section | P1 |

## 2. Test planning references

### ST-17-TC-001 — Acceptance planning reference (AC-17)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-17](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-17`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Acceptance checklist, blockers and source trace

### F.1. Blockers to resolve before DD READY

1. Implement/register Student API #33 and Study Web route; add runnable route/module/test evidence before describing runtime behavior.
2. Approve direct assignment/course access predicate and 403-vs-404 masking.
3. Define whether #33 returns after deadline, exact deadline boundary/timezone/server-time source, and reconcile AC-17 403/409 with the catalog's 401/403/404/500 set.
4. Define the AC-17 “submission rule” schema and owner; do not add it to `Assignment` without contract approval.
5. Reconcile `course_id`/`max_score` required logical fields with nullable candidate DDL; define optional null/omit behavior, timestamp timezone and decimal scale/rounding.
6. Supply approved sources for course title, status/submitted state/history, weight/progress, rubric/objectives, resources/video, mentor/SLA, checklist, late policy and contact actions—or remove those claims from the loaded design.
7. Approve ST-17 → ST-18 route/eligibility handoff and define which server state enables the CTA.
8. Reconcile the loaded Student PNG with the Guest unavailable HTML fallback; align the selected state/layout with the Study Web font, width, responsive and control-size target; define empty/loading/error UI and destinations.
9. Reconcile the legacy BIGINT assignment tables with the V1-PILOT schema, which has no business assignment/submission tables; approve the source schema and API #33 adapter before implementation.

### F.2. Checklist

- [x] ST-17 plan completed before marker map, annotated image and DD authoring.
- [x] Original `screen.png` and `code.html` preserved; hashes/dimensions recorded.
- [x] 49 ordered markers map one-to-one to 49 elements in section C.
- [x] Route load, response mapping, deadline, checklist, resource/contact, ST-18 handoff and auth/error/navigation events described.
- [x] API catalog, API #33 Draft DD, AC-17, candidate DDL and current missing Student route/source kept distinct.
- [x] Screenshot/HTML discrepancy, unsupported fields/actions and API 403/409 discrepancy recorded.
- [x] Legacy BIGINT vs V1-PILOT assignment-schema gap and Study Web design-target mismatch recorded.
- [ ] Resolve F.1 contract/source blockers before declaring DD READY or implementation-ready.
- [ ] Verify actual route/API/runtime before marking RUNTIME VERIFIED.

### F.3. Source traceability

- [ST-17 plan](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_PLAN.md), [marker map](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_markers.json), [annotated screen](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen_annotated.png), [source PNG](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen.png), [HTML companion](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/code.html).
- [Screen inventory / ST-17 and linked ST-18/ST-09](../../list_screen.md).
- [API catalog #33 and Assignment schema](../../../../../docs/lists/list_api.md).
- API #33 DD: [overview](../../../../study-server/docs/dd/33_assignments_detail/02_Overview.md), [request](../../../../study-server/docs/dd/33_assignments_detail/03_Request.md), [response](../../../../study-server/docs/dd/33_assignments_detail/04_Response.md), [mapping](../../../../study-server/docs/dd/33_assignments_detail/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/33_assignments_detail/06_Error.md), [open questions](../../../../study-server/docs/dd/33_assignments_detail/OPEN_QUESTIONS.md), [verification report](../../../../study-server/docs/dd/33_assignments_detail/VERIFICATION_REPORT.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-17 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [Candidate assignment table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT schema artifact](../../../../../infra/postgres/02_study_db.sql).
- [Current Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../.agents/web-study/design.md).
- Current downstream upload source: [API #34 route](../../../../study-server/app/api/v1.py), [upload flow](../../../../study-server/app/modules/student/api_34_uploads/view.py). This does not establish current #35/#36 Student routes.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. State, navigation, acceptance and verification plan

- Target state flow from inventory: `loading → open | closed | not-found`; add access-denied/error states for catalog/runtime failures. Exact mapping of due/permission to #33 response remains blocked.
- Navigation: preceding assignment list/course context is not identified as an ST-17 route in the inventory; related ST-09 is not automatically a breadcrumb/CTA destination. The CTA relates to ST-18 and should hand off `assignmentId` only under approved route policy.
- Accessibility target follows `.agents/web-study/design.md`: semantic links/buttons, keyboard/focus, accessible names for icon actions, non-color status cues, responsive reflow/reduced motion. This is intended design, not current runtime.
- Static verification after authoring: preserve original hashes/dimensions; verify all 49 markers are ordered, in-bounds, non-overlapping and map one-to-one to DD; parse SVG; verify annotated image dimensions/visual legibility; check local links, inventory/folder count, tracker totals/next pointer and `git diff --check`. Do not run tests or claim runtime.
- Blockers: API #33 route/module/test absent; access/deadline/submission-rule/error mapping unresolved; response cannot support most loaded-screen content; image/HTML state/actor mismatch; Study Web UNWIRED.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
