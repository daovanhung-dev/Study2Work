# GS-05 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-05-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Danh sách review/reply; không hiển thị sao trung bình khi không có rating contract.
- Gate/status (giữ nguyên): **D (#10 declared; no current route/module/test)**; **BLOCK:** #08 catalog `course_id:int64` lệch route `str`/parser không giới hạn signed int64; API #10 Draft yêu cầu `Discussion.title` nhưng không có source; không có course-rating/aggregate source, literal rating-filter key/semantics hoặc public root/reply visibility approval; legacy `discussions` thiếu title/rating và V1-PILOT assessment reviews là model khác; AC-05 aggregate/eager #08→#09→#10 lệch F02 lazy tab, inventory yêu cầu #08 cache reuse; loaded review/reply/page/loading/error UI thiếu; live schema và Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: H. Traceability, blockers và acceptance

| Claim | Evidence | Status |
|---|---|---|
| Guest route, review/reply intent, pagination, empty-vs-404, no average without rating contract | `apps/study-client/docs/list_screen.md` GS-05/F02/G-06 | Expected design source |
| AC-05 aggregate-rating expectation and eager sequence | `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` | Expected activity flow; conflicts with GS-05 rating gate/F02 lazy flow |
| Static visible elements | `code.html`, original PNG and separately rendered image | Current asset only |
| Course public gate | #08 current route/module/query and test source | `SOURCE_BACKED`; tests not run; runtime/deployment unverified |
| Reviews endpoint | API catalog + API #10 Draft DD; route/test search under current source; existing #97/#98 are ADMIN moderation routes | `DECLARED_NOT_RUNNABLE` |
| Discussion title/rating/live database | Draft DD + legacy `discussions` DDL + V1-PILOT assessment-review DDL + database context | `DISCREPANCY`; live schema unverified |
| Study Web | `.agents/web-work/study/AGENTS.md` and current app tree/dist review | `UNWIRED`; no GS-05 route/API wiring found |

### Acceptance checklist

- [x] Plan written before render/annotation/DD.
- [x] Original image and HTML retained; hashes recorded.
- [x] HTML rendered separately to 1440×1200 and visually inspected; original PNG remains unchanged.
- [x] Annotated render visually inspected at reduced size; 9 markers point to visible current-state elements and stay in side gutters.
- [x] Marker map lists ordered, unique IDs corresponding 1:1 to DD element rows.
- [x] DD documents expected/current flow, each current element's type/position, all eight events' trigger/type/precondition/input/process/output/error, route, API #08/#10 status, states, navigation and blockers.
- [x] Reviews title/rating/aggregate, visibility, pagination and AC-05/F02 discrepancies remain explicit; no unsupported behavior was introduced.
- [ ] API #10 implementation/contract, title source, rating source and public visibility approved; required for `DD READY`.
- [ ] Loaded review/reply/pagination/loading/error design and cache/orchestration confirmed; required before implementation.
- [ ] Study Web route/client integration and real runtime evidence captured; required for runtime verification.

### Final classification

- `DD BLOCKED`: API #10 is not runnable; title/rating/public-visibility policy unresolved; loaded state has no design.
- `IMPLEMENTATION BLOCKED`: missing API #10, cache/orchestration decisions, UI design and Study Web wiring.
- `RUNTIME NOT VERIFIED`: static assets, API #08 source and API #10 declaration do not demonstrate an end-to-end deployed screen.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
