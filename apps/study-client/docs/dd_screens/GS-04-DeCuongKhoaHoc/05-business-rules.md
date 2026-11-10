# GS-04 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-04-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị danh sách lesson public theo sort_order; item private không mở bằng guest.
- Gate/status (giữ nguyên): **R (#09 source-backed locally)**; **BLOCK:** `course_id:int64` chưa khớp route string/parser range; visibility `PUBLISHED` chưa được API DD duyệt; response có content/video_url nhưng không preview/access field; legacy vs V1-PILOT schema/live DB chưa xác minh; cache/#08 reuse, AC-05 eager vs F02 lazy/direct-entry chưa chốt; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: H. Traceability, blockers và DoD

| Requirement / claim | Evidence | Status |
|---|---|---|
| Guest curriculum tab, proposed route, AC-05, API #09, GS-03/ST-10 links | `apps/study-client/docs/list_screen.md` | Expected design source |
| Static element/layout/hrefs | `code.html`, original and Firefox render | Current asset only; no app runtime |
| #09 route/view/query/model and error/empty mapping | Study Server current source listed in §F | `SOURCE_BACKED`; deployment unverified |
| #09 tests | `apps/study-server/tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py` | Read; not run; fake DB only |
| Published visibility/response shape design status | API #09 Draft DD | `Draft — Needs Confirmation`; does not settle access |
| Actual database schema in deployment | Two incompatible checked-in DDL artifacts; `.agents/server-study/database.md` marks live status unverified | `NOT VERIFIED` |
| Study Web route/UI wiring | Registered subcontext `.agents/web-work/study/INDEX.md` and current checkout | `UNWIRED` |

### Acceptance checklist

- [x] Screen plan written before render/annotation/DD; records expected/current evidence and blockers.
- [x] Original `screen.png` and `code.html` retained with hashes.
- [x] HTML rendered separately; original near-blank screenshot preserved.
- [x] Annotated image visually inspected at reduced preview; all 10 markers point to visible elements and stay in outer gutters.
- [x] Marker JSON contains 10 unique ordered element IDs matching this DD.
- [x] Expected and current behavior, elements, events, states, route handoff and API #09 source mapping are documented.
- [x] Private lesson access, public `content`/`video_url`, API-DD assumption, DDL mismatch, cache and eager/lazy discrepancies are explicit.
- [ ] Loaded lesson-list/preview/access/error designs and API projection policy approved; required for `DD READY`.
- [ ] Cache and orchestration/direct-entry behavior confirmed; required before implementation.
- [ ] Study Web route/client wired and real runtime evidence captured; required for implementation/runtime status.

### Final classification

- `DD BLOCKED`: loaded list and its access/preview contract are unresolved; current API visibility assumption is not approved.
- `IMPLEMENTATION BLOCKED`: UI runtime is unwired and policy/orchestration inputs remain unresolved.
- `RUNTIME NOT VERIFIED`: static render and backend source do not demonstrate deployed end-to-end behavior.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
