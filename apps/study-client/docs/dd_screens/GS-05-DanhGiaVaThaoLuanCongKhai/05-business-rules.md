# GS-05 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-05-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Danh sách review/reply; không hiển thị sao trung bình khi không có rating contract.
- Gate/status (T021, 2026-11-17): **#10 SOURCE_BACKED locally; GS05 caller WIRED; API DD remains Draft**. **BLOCK:** API #10 Draft requires `Discussion.title` with no source; course rating/aggregate, rating query key/semantics and public root/reply visibility/order lack approval; current implementation filters ACTIVE rows but that source behavior is not business-rule approval; AC-05 aggregate/eager #08→#09→#10 differs from F02 lazy; no client cache; loaded presentation is derived; live schema/deployment unverified.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: H. Traceability, blockers và acceptance

| Claim | Evidence | Status |
|---|---|---|
| Guest route, review/reply intent, pagination, empty-vs-404, no average without rating contract | `apps/study-client/docs/list_screen.md` GS-05/F02/G-06 | Expected design source |
| AC-05 aggregate-rating expectation and eager sequence | `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` | Expected activity flow; conflicts with GS-05 rating gate/F02 lazy flow |
| Static visible elements | `code.html`, original PNG and separately rendered image | Current asset only |
| Course public gate | #08 current route/module/query and test source | `SOURCE_BACKED`; tests not run; runtime/deployment unverified |
| Reviews endpoint | API #10 route/module/source tests under `apps/study-server`; separate from #97/#98 ADMIN moderation | `SOURCE_BACKED`; DD Draft; focused suite 22/22 fake DB |
| Discussion title/rating/live database | Draft DD + legacy `discussions` DDL + V1-PILOT assessment-review DDL + database context | `DISCREPANCY`; live schema unverified |
| Study Web | GS03/GS05 page, API_010 descriptor and Angular specs | `PARTIAL SOURCE-WIRED`; focused 12/12 and full 153/153 pass; live API/DB/deployment unverified |

### Acceptance checklist

- [x] Plan written before render/annotation/DD.
- [x] Original image and HTML retained; hashes recorded.
- [x] HTML rendered separately to 1440×1200 and visually inspected; original PNG remains unchanged.
- [x] Annotated render visually inspected at reduced size; 9 markers point to visible current-state elements and stay in side gutters.
- [x] Marker map lists ordered, unique IDs corresponding 1:1 to DD element rows.
- [x] DD documents expected/current flow, each current element's type/position, all eight events' trigger/type/precondition/input/process/output/error, route, API #08/#10 status, states, navigation and blockers.
- [x] Reviews title/rating/aggregate, visibility, pagination and AC-05/F02 discrepancies remain explicit; no unsupported behavior was introduced.
- [ ] API #10 implementation/contract, title source, rating source and public visibility approved; required for `DD READY`.
- [ ] Loaded review/reply/pagination/loading/error design and cache/orchestration are approved; current implementation remains derived.
- [x] Study Web route/client integration and local stub-backed browser render are captured.
- [ ] Live API/DB/deployment runtime is verified.

### Final classification

- `DD BLOCKED`: API #10 DD remains Draft; title/rating/query-key/public-visibility rules and AC-05/F02/cache decisions remain unresolved.
- `IMPLEMENTATION PARTIAL SOURCE-WIRED`: GS03/GS05/#10 are wired locally; loaded view is derived without DD visual approval; enrollment remains unimplemented.
- `STUB-BROWSER-VERIFIED; LIVE RUNTIME NOT VERIFIED`: local desktop/mobile render used an in-memory stub; live API, DB schema and deployment were not checked.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
