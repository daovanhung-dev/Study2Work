# GS-04 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-04-TC-001` | Planning ref / not run | `AC-05` | See source acceptance section | P1 |

## 2. Test planning references

### GS-04-TC-001 — Acceptance planning reference (AC-05)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-04](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-05`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md).

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Thứ tự và acceptance checklist

1. [x] Kế hoạch này được ghi trước khi tạo render/annotation/DD.
2. [x] Render `code.html` trong Firefox thành `screen_rendered.png`; layout đã kiểm tra. Không ghi đè source.
3. [x] Tạo `GS-04_markers.json`, SVG overlay và `screen_annotated.png` với 10 marker đúng vùng và không che nội dung; preview đã được kiểm tra.
4. [x] Viết `GS-04.md` theo objective: overview; flow; 10 elements; event input/processing/output/error; #09 contract; state/navigation; security/access blockers; trace links.
5. [x] Static check JSON/order/ID mapping, local links, image dimensions/visual layout, original hashes, marker bounds/gutters, `git diff --check`, 83 ID count and total artifacts. Không chạy tests.
6. [x] Cập nhật tracker GS-04/progress và worklog sau kiểm tra. Do source/design còn thiếu access/preview policy, DDL discrepancy, cache rule, loaded list design và Study Web runtime: `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.

### Điều kiện DD READY chưa đạt

- Không có visual design cho loaded list, lesson hierarchy/preview affordance hoặc curriculum error/loading variants.
- API #09 trả lesson content/video URL công khai nhưng không có preview/access field; status filter là assumption trong DD #09.
- Hai checked-in DDL sources khác nhau; live schema chưa được xác minh.
- #08 cache freshness/miss behavior và AC-05 eager vs F02 lazy orchestration chưa chốt.
- Study Web/router chưa wired; route/back link hiện chỉ là proposal/`#` placeholder.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
