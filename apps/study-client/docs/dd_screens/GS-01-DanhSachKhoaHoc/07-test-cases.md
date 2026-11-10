# GS-01 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-01-TC-001` | Planning ref / not run | `AC-03` | See source acceptance section | P0 |

## 2. Test planning references

### GS-01-TC-001 — Acceptance planning reference (AC-03)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-01](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-03`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Tiêu chí nghiệm thu

- [x] 16 screenshot marker có ID duy nhất, theo thứ tự và có mô tả element tương ứng.
- [x] Expected behavior tách khỏi current screenshot/HTML/API source; không mô tả prototype giả là runtime.
- [x] #05/#06 đã đối chiếu route, query validation, DB read/mapping, response/business code và error path trong source. Test source đã đọc nhưng không chạy.
- [x] Không gửi category; out-of-range page, error và empty catalog được phân biệt.
- [x] Search, sort, paging, card và nav event được mô tả với giới hạn source/design rõ ràng.
- [x] Blocker và dependency liên kết GS-02/GS-03 được ghi rõ.
- [ ] Loaded-state design, cache/error policy, category support, search handoff và schema/display contract được duyệt; điều kiện DD READY chưa đạt.
- [ ] Study Web runtime/router wired and verified; runtime verification chưa được thực hiện.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blockers and acceptance gates

1. `GS01-B01 LOADED_STATE_DESIGN`: source image and HTML show empty state only; card, sort, result count and pagination controls/layout are missing despite AC/inventory expectations. Cannot claim DD READY without an approved loaded-state design or approved source.
2. `GS01-B02 CATEGORY_FILTER_UNSUPPORTED`: catalog/API declaration permits category, but current #06 validator rejects it and no course-category relation exists in checked-in DDL. Do not enable/send category.
3. `GS01-B03 SEARCH_HANDOFF_UNRESOLVED`: two search inputs and CTA lack working behavior; GS-02/#07/q is a screen link, but exact query handoff/normalization is unapproved; prototype fake count must not be copied.
4. `GS01-B04 PARTIAL_LOAD_AND_CACHE_POLICY`: inventory says cache-first #05 then #06; there is no client cache source/TTL or failure policy when one request fails. Do not invent behavior.
5. `GS01-B05 COURSE_SHAPE_DISCREPANCY`: reusable catalog Course includes optional category; current #06 response omits it. Currency and rating/duration fields are also absent from source.
6. `GS01-B06 EMPTY_PAGE_AND_ERROR_COPY`: API #06 can return empty `items` for both zero total and out-of-range page, while screenshot copy conflates empty and updating. Define separate error/empty-page recovery/copy before implementation.
7. `GS01-B07 STUDY_WEB_UNWIRED`: current checkout has no app source/router/package/entrypoint; no route, cache or interaction is runtime verified.
8. `GS01-B08 SOURCE_VARIANT_MISMATCH`: screenshot header omits the Study2Work brand visible in HTML; HTML has duplicate brand/nav markup and broken orphan filter script. Keep screenshot source intact; product must choose/correct source of truth.

- [x] Screen source image and HTML hashes/dimensions inventoried; originals must remain unchanged.
- [x] Current API #05/#06 source and relevant test source, API catalog, AC-03 and DDL relation checked; tests/runtime not run.
- [x] 16 ordered markers match 16 visible DD elements; annotation visually reviewed and marker overlap corrected.
- [x] DD includes visible elements, conditional events, states, API/error/navigation trace and source-backed unresolved blockers.
- [x] Static marker/element/event/link/hash/image/tracker/worklog checks pass (see session worklog).
- [ ] Screen stays `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` until blockers are resolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
