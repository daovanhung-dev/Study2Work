# ST-17 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-17-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Đề bài, hạn nộp, điểm tối đa, file liên quan và nút nộp.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #33 Draft, Student route/module/test NOT_FOUND; access/deadline/submission-rule/403-vs-409 unresolved; Assignment response thiếu phần lớn loaded-screen fields; legacy BIGINT assignment tables vs V1-PILOT không có business assignment tables, adapter/live schema chưa xác minh; PNG/HTML actor-state mismatch và visual target mismatch; Study Web UNWIRED; #34 chỉ là upload source-backed, #35/#36 Student routes chưa có
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
