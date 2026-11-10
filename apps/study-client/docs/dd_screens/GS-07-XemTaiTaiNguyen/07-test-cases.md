# GS-07 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-07-TC-001` | Planning ref / not run | `AC-06` | See source acceptance section | P2 |

## 2. Test planning references

### GS-07-TC-001 — Acceptance planning reference (AC-06)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-07](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-06`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: G. Tiêu chí nghiệm thu và traceability

### Tiêu chí nghiệm thu cho DD

- [x] 26 marker IDs có một hàng tương ứng trong §C; original source PNG/HTML được bảo toàn.
- [x] Static header, breadcrumb, API card, viewer controls, demo tabs, error sample, disabled download/back/footer được mô tả theo current HTML.
- [x] API #12 route/auth/query/model/status trace tách biệt khỏi AC-06/catalog/mock expectations.
- [x] Signed URL, permission, visibility, MIME, 403/410, 404 screen mapping, source/return context và Study Web wiring được ghi là quyết định mở.
- [x] Tất cả 8 event có trigger, precondition, input, processing, output và exception riêng; API/source discrepancies và simulator behavior không bị gộp thành runtime behavior.
- [x] Prototype/design-system/accessibility discrepancy được đối chiếu với `.agents/web-study/design.md`; badge WCAG không được coi là kết quả audit.
- [ ] Implementation/runtime flow verified — bị chặn; không có frontend/runtime evidence.

### Nguồn

- Inventory/flow: [`list_screen.md`](../../list_screen.md) — GS-07, F02, F04, G-07, API #12; links GS-06/ST-12/SH-06.
- AC expectation: `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` — AC-06.
- Assets: `screen.png`, `code.html` trong cùng thư mục; HTML inspection tĩnh, không request/renderer node.
- API catalog/DD: `docs/lists/list_api.md`; `apps/study-server/docs/dd/12_resources_detail/`.
- Current API: `apps/study-server/app/api/v1.py`; `app/modules/guest/api_12_resources_detail/{view,query,validate,models}.py`.
- Test source (read only, not run): `apps/study-server/tests/modules/guest/api_12_resources_detail/test_resources_detail.py`.
- DB context/candidates: `.agents/server-study/database.md`, `infra/postgres/study-server/DB.sql`, `infra/postgres/02_study_db.sql`; checked-in DDL is not live-schema evidence.
- Related screen context: `GS-06.md`/`GS-06_PLAN.md`, ST-12 inventory row, SH-06 DD; Study Web status `.agents/web-work/study/INDEX.md` and `.agents/web-study/design.md`.
- Context/preflight: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/{INDEX,architecture,dependencies}.md`, `.agents/web-work/`, `.agents/server-study/`, `.agents/skills/INDEX.md`, `.agents/context-manifest.json`; exact-type docs worklogs selected and reviewed as recorded in the session worklog.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 4. Planned output and acceptance

- Keep `screen.png` and `code.html` byte-identical.
- Create 26 ordered unique markers with exact DD element-ID mapping, SVG overlay and annotated image at scale 2 with side gutters.
- Create `GS-07.md` with overview, current/expected flow, every element, per-control event procedures, API #12 details/errors, simulator/API discrepancies, states, navigation/origin handoff, acceptance and sources.
- Update `dd_screens/PLAN.md` progress from 13/83 to 14/83 and set GS-08 as next; keep `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` separate.
- Create current-session worklog with exact-type preflight review and verification. Do not run backend tests or claim runtime verification.

### Acceptance checklist

- [x] Plan exists before marker/annotated/DD authoring.
- [x] Source PNG/HTML hashes unchanged; source image valid and complete.
- [x] 26 markers are ordered, unique, in bounds and map one-to-one to DD rows.
- [x] Disabled zoom/download, active local state tabs, back/breadcrumb/header/footer anchors and their actual static behavior are documented.
- [x] API #12 endpoint/auth/path/response/current code/errors are traced to source and catalog; no signed URL/403/410/423/501 mock is promoted as runtime behavior.
- [x] `url` direct/source semantics, nullable model, parent check condition, missing visibility and DB/live-schema boundary are explicit.
- [x] GS-06/ST-12 entry and return route semantics; SH-06 404 applicability; preview MIME/type policy and storage/permission gates are identified without invented behavior.
- [x] Tracker and worklog are updated; static asset/marker audit, visual review and `git diff --check` pass.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
