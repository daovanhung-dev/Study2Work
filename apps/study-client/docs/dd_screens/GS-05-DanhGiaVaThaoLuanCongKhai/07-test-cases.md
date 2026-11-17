# GS-05 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

> **Implementation verification update (T021, 2026-11-17):** The planning references below remain distinct from executable tests. Current Angular evidence: focused GS03+GS05 12/12 and full Study Web 153/153. Current API #10 focused suite: 22 passed with fake/overridden DB sessions. Desktop/mobile headless Chrome rendered via temporary in-memory local API stub; live API/DB/deployment remain unverified.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-05-TC-001` | Planning ref / not run | `AC-05` | See source acceptance section | P2 |

## 2. Test planning references

### GS-05-TC-001 — Acceptance planning reference (AC-05)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-05](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-05`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: H. Traceability, blockers và acceptance

| Claim | Evidence | Status |
|---|---|---|
| Guest route, review/reply intent, pagination, empty-vs-404, no average without rating contract | `apps/study-client/docs/list_screen.md` GS-05/F02/G-06 | Expected design source |
| AC-05 aggregate-rating expectation and eager sequence | `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` | Expected activity flow; conflicts with GS-05 rating gate/F02 lazy flow |
| Static visible elements | `code.html`, original PNG and separately rendered image | Current asset only |
| Course public gate | #08 current route/module/query and test source | `SOURCE_BACKED`; tests not run; runtime/deployment unverified |
| Reviews endpoint | `apps/study-server/app/api/v1.py`, `modules/guest/api_10_courses_reviews/`, focused API #10 tests | `SOURCE_BACKED`; DD remains Draft; 22 tests use fake DB only |
| Discussion title/rating/live database | Draft DD + legacy `discussions` DDL + V1-PILOT assessment-review DDL + database context | `DISCREPANCY`; live schema unverified |
| Study Web | `GS03Page`, `GS05Page`, `GS05ReviewsService`, API_010 descriptor, focused/full specs | `PARTIAL SOURCE-WIRED`; 12 focused and 153 full suite tests pass; live API/DB/deployment unverified |

### Acceptance checklist

- [x] Plan written before render/annotation/DD.
- [x] Original image and HTML retained; hashes recorded.
- [x] HTML rendered separately to 1440×1200 and visually inspected; original PNG remains unchanged.
- [x] Annotated render visually inspected at reduced size; 9 markers point to visible current-state elements and stay in side gutters.
- [x] Marker map lists ordered, unique IDs corresponding 1:1 to DD element rows.
- [x] DD documents expected/current flow, each current element's type/position, all eight events' trigger/type/precondition/input/process/output/error, route, API #08/#10 status, states, navigation and blockers.
- [x] Reviews title/rating/aggregate, visibility, pagination and AC-05/F02 discrepancies remain explicit; no unsupported behavior was introduced.
- [ ] API #10 implementation/contract, title source, rating source and public visibility approved; required for `DD READY`.
- [ ] Loaded review/reply/pagination/loading/error design and cache/orchestration are approved; current implementation is derived and does not close this gate.
- [x] Study Web route/client integration and a local stub-backed browser render were captured.
- [ ] Live API/DB/deployment runtime is verified.

### Final classification

- `DD BLOCKED`: API #10 DD remains Draft; title/rating/query-key/public-visibility rules and AC-05/F02/cache decisions remain unresolved.
- `IMPLEMENTATION PARTIAL SOURCE-WIRED`: GS03/GS05/#10 current local source and tests are wired; loaded view is derived without DD visual approval; enrollment is not implemented.
- `STUB-BROWSER-VERIFIED; LIVE RUNTIME NOT VERIFIED`: local desktop/mobile render used an in-memory stub; no live API, DB schema or deployment was checked.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Acceptance checklist

1. [x] This plan exists before creating render, annotation or DD.
2. [x] Render HTML separately to `screen_rendered.png`; preserve original PNG/HTML and record hash/dimensions.
3. [x] Finalize ordered unique marker map from rendered/current visible elements; no markers for absent loaded UI.
4. [x] Create SVG overlay and `screen_annotated.png`; visually inspect for mapping, legibility and overlap.
5. [x] Write `GS-05.md` with full trace, each element, event input/process/output/error, state transitions and linked screen handoff.
6. [x] Static audit JSON/IDs, DD rows, links, hashes, image sizes, SVG/marker bounds, inventory counts/artifact totals and `git diff --check`; do not run tests.
7. [x] Update global tracker and worklog; statuses are `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` because API #10, schema/title/rating/visibility and Study Web wiring are unresolved.

### DD READY gates still unresolved

- API #10 has no executable route/module/test; DD stays Draft — Needs Confirmation.
- Discussion title and rating/aggregate source are missing; literal rating query name/semantics unresolved.
- Public roots/replies visibility and moderation rules are assumptions; checked-in DDL/live schema do not establish approval.
- No visual/interaction design for loaded review cards, replies, pagination, loading/error states.
- AC-05 eager request sequence conflicts with F02 lazy tab; #08 cache policy/direct-entry behavior is missing.
- Study Web remains `UNWIRED`; proposed routes and `href="#"` anchors are not runtime evidence.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
