# GS-02 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-02-TC-001` | Planning ref / not run | `AC-04` | See source acceptance section | P0 |

## 2. Test planning references

### GS-02-TC-001 — Acceptance planning reference (AC-04)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-02](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-04`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Tiêu chí nghiệm thu

- [x] Kế hoạch riêng được ghi trước DD/annotation và có trace expected/current.
- [x] Asset nguồn không bị sửa; ảnh nguồn và HTML được ghi nhận bằng hash.
- [x] 26 marker có ID duy nhất, theo thứ tự 1–26 và ánh xạ 1:1 tới 26 component group trong §3.
- [x] API #05/#07 được đối chiếu với route, validator, query, mapper, response, tests source và checked-in DDL; tests không chạy.
- [x] Expected behavior, current source, discrepancy, implementation blocker và runtime status được tách riêng.
- [x] 19 event được nhận diện và mô tả input, precondition, xử lý, API/nội bộ, output/error hoặc lý do bị chặn.
- [x] States, error mapping, pagination edge case, navigation, security and unresolved policies are documented.
- [ ] DD READY: chưa đạt; cần giải quyết B01–B09 và kiểm tra lại implementability.
- [ ] IMPLEMENTATION: chưa đạt; Study Web chưa có runtime source và các blocker nghiệp vụ/API còn mở.
- [ ] RUNTIME VERIFIED: chưa đạt; không có browser/app runtime verification.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blockers and acceptance gates

1. `GS02-B01 SOURCE_VARIANT_MISMATCH`: screenshot is loaded state while code.html is an empty-state Guest prototype; header/actor also differ. Product/Design must select/repair authoritative UI variant.
2. `GS02-B02 FACETS_UNSUPPORTED`: category produces 422; skill/duration/rating/tuition are not #07 inputs and DDL has no category relation. Do not submit visible selected filters.
3. `GS02-B03 SORT_RELEVANCE_UNSUPPORTED`: screenshot default “Phù hợp nhất” cannot map to API allowlist/default.
4. `GS02-B04 PAGE_SIZE_CONFLICT`: design paginates 6 items and shows 12 total, API fixed page size 20. Need align design or backend contract.
5. `GS02-B05 COURSE_CARD_SCHEMA`: current API lacks category, tags, currency, duration, rating and discount/old-price fields displayed in screenshot. No derived/mock values may be presented as real.
6. `GS02-B06 EMPTY_QUERY_SEMANTICS`: blank q makes API return all PUBLISHED courses, while AC/HTML may show a prompt. Decide if search route calls API for blank q and how URL/display case is normalized.
7. `GS02-B07 CACHE_AND_PARTIAL_LOAD`: AC-04 models #05 → #07 in sequence, while inventory F02/API #05 DD describe cache-first and allow independent parallel search; client source is absent, and TTL/invalidation/fallback/partial-load policy is not approved.
8. `GS02-B08 STUDY_WEB_UNWIRED`: no app source/router/package/entrypoint; no event, URL, debounce or navigation runtime is verified.
9. `GS02-B09 EXTRA_DESTINATIONS`: account utilities, learning-path/advisor promos and footer destinations have no route/service contract.
10. `GS02-B10 PAGE_RANGE_CONTRACT`: API catalog declares int32 but route uses unbounded Python int and checks only the lower bound; align contract/validation and oversized-offset behavior.

- [x] PNG/HTML dimensions and hashes inventoried; source assets retained.
- [x] API #05/#07 route, model, validator, SQL, mapper, responses, relevant tests, AC-04, catalog and checked-in DDL traced; tests not run.
- [x] 26 ordered markers match DD component groups; annotation visually reviewed for legibility/occlusion. A first render exposed overlapping callouts #19/#21; #19 was moved to y_source=1135 and the final crop has separated circles.
- [x] DD includes complete visible components, 19 event paths, states, API/error mapping and unresolved navigation/data contracts.
- [x] Static element/event/link/hash/image/tracker checks pass; the final worklog records the global context-validator result.
- [ ] Do not mark DD READY until design/source variants, facet/sort/page/card contracts and empty-query policy are resolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
