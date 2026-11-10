# AD-14 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-14-TC-001` | Planning ref / not run | `AC-34` | See source acceptance section | P1 |

## 2. Test planning references

### AD-14-TC-001 — Acceptance planning reference (AC-34)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-14](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-34`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Giữ nguyên `screen.png`/`code.html`; tạo riêng annotated image và marker map; marker đọc được và tránh nội dung chính.
- [x] Có A–F; 72 marker tương ứng 72 element rows; source/API references được truy vết.
- [x] EV-01…EV-07 ghi input, thứ tự xử lý, output/error và expected/current separation.
- [x] Đối chiếu current routes, validators, queries, models, transaction effects, test source và error envelope cho #83–#86.
- [x] Ghi rõ AC/API/body/status/dependency/permission/schema/UI discrepancies; không biến DERIVED fallback thành contract đã duyệt.
- [x] `DD READY` gate được đánh giá riêng; các contract/owner/schema/UI decisions còn mở nên chưa đạt.
- [ ] Owner chốt #84 body/editor mapping, #85 status enum/transition/audit, #86 dependency set/confirmation, fine-grained permission và deployed schema.
- [ ] Study Web route/client được wire và runtime được xác minh.

### Trạng thái

- **Screen DD:** `DD BLOCKED` — blockers trong A/D/F còn quyết định trực tiếp field mapping, status action, delete eligibility và permission.
- **Implementation:** `IMPLEMENTATION BLOCKED` — Study Web source/router/client không có; screen/API contract còn mở.
- **Runtime:** `RUNTIME NOT VERIFIED` — không chạy frontend/API hoặc live database trong phiên.
- API #84–#86: current local route/module/test source is present (`R` inventory classification); API DD folders remain `Draft — Needs Confirmation`.

### Sources

- [Screen inventory, AC-34 flow and reverse API index](../../list_screen.md)
- [AD-13 handoff DD](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13.md)
- [API catalog #83–#86](../../../../../docs/lists/list_api.md)
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md)
- [AC-34 Admin management diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API routes](../../../../study-server/app/api/v1.py)
- [API #84 update module](../../../../study-server/app/modules/admin/api_84_admin_lesson_update)
- [API #85 status module](../../../../study-server/app/modules/admin/api_85_admin_lesson_status)
- [API #86 delete module](../../../../study-server/app/modules/admin/api_86_admin_lesson_delete)
- [API #84 focused test source](../../../../study-server/tests/modules/admin/api_84_admin_lesson_update/test_admin_lesson_update.py)
- [API #85 focused test source](../../../../study-server/tests/modules/admin/api_85_admin_lesson_status/test_admin_lesson_status.py)
- [API #86 focused test source](../../../../study-server/tests/modules/admin/api_86_admin_lesson_delete/test_admin_lesson_delete.py)
- [API #84 Draft DD and questions](../../../../study-server/docs/dd/84_admin_lesson_update/OPEN_QUESTIONS.md)
- [API #85 Draft DD and questions](../../../../study-server/docs/dd/85_admin_lesson_status/OPEN_QUESTIONS.md)
- [API #86 Draft DD and questions](../../../../study-server/docs/dd/86_admin_lesson_delete/OPEN_QUESTIONS.md)
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql)
- [API #85 audit migration candidate](../../../../../infra/postgres/study-server/migrations/012_lesson_status_audit_logs.sql)
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md)

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Work order and acceptance checklist

1. [x] Re-read objective/router/context/worklog contract; classify `docs`; selector READY 3/219 and read all selected AD-01/02/03 worklogs plus AD-13 handoff.
2. [x] Load cross-scope project, Web Study, Server Study, registry/workflow context; inspect AC-34, inventory, APIs #84–#86 route/module/query/model/test source and DDL evidence.
3. [x] Save this plan before marker JSON/SVG, annotated image, or AD-14 DD.
4. [x] Create 72 ordered marker entries in JSON and SVG; render annotated image 2× and inspect it directly.
5. [x] Author A–F DD with exactly 72 §C rows; fully specify observed events, inputs, local processing, API boundaries, responses/errors, states, navigation and explicit blockers.
6. [x] Update AD-14 inventory and API reverse index #084–#086 based on local route/module/test source; append global checkpoint and finalize worklog. Keep API DDs Draft and do not alter AD-15.
7. [x] Static audit source hashes/dimensions, JSON/XML, marker sequence/coords/stroke bounds, 1:1 rows, local links, 83 IDs/folders/core artifact count, image review, whitespace and `git diff --check`. Do not run app tests/runtime.
8. [x] End after AD-14; preserve `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` wherever current evidence requires them.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
