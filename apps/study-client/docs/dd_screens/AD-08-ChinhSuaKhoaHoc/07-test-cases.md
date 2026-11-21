# AD-08 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-08-TC-001` | Planning ref / not run | `AC-32` | See source acceptance section | P1 |

## 2. Test planning references

### AD-08-TC-001 — Acceptance planning reference (AC-32)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-08](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Planning reference này không chứng minh pass/fail của UI source hoặc runtime; xem current source verification bên dưới.
- **References:** `AC-32`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Checklist

- [x] Có source screenshot nguyên trạng; hash được kiểm tra, không sửa ảnh nguồn.
- [x] Có 61 marker liên tục, unique; DD có một hàng cho mỗi marker.
- [x] Current prototype controls, links, static values và API/server behavior được phân biệt.
- [x] #74/#75 đối chiếu catalog, AC, route/model/validator/view/query, API DD và test evidence.
- [x] Auth, candidate body, validation, transaction, response/errors và API limitations được truy vết.
- [x] States/navigation và expected/current discrepancy được ghi rõ.
- [x] Angular route/page/GET #74 caller, local-draft behavior and save/upload disabled state được đối chiếu source.
- [ ] API #75 body, validation, schema và permission mapping được owner xác nhận.
- [ ] Thumbnail upload/storage contract và return/revalidation behavior được quyết định.
- [ ] API #75 write flow được implement; browser/deployment runtime verified.

### Blockers

1. API catalog/AC thiếu body #75; local body, replacement/null semantics, title/price bounds và legacy schema mapping đang là `DERIVED`.
2. AC-32 course-management permission chưa được chứng minh bằng local shared role `ADMIN`.
3. Mockup mô tả mentor edit nhưng #75 không sửa mentor; thumbnail upload/S3/multipart không có endpoint/contract trong module #75.
4. Legacy BIGINT schema và V1-PILOT UUID/versioned schema khác nhau; live DB/deployment chưa được xác minh.
5. Response singleton Page và yêu cầu revalidation thứ hai chưa được owner/client contract xác nhận.
6. Angular route/read/local-draft source exists; there is no PUT #75 caller or dirty/persistence flow. Prototype Back/Cancel differ from Angular AD-07 links; static metrics/audit/RBAC claims lack source.

**Completion decision:** Tài liệu mô tả evidence và các quyết định còn mở nhưng chưa đạt `DD READY` vì blocker ảnh hưởng đến body, authorization, persistence, upload và revalidation. Trạng thái màn hình: **DD BLOCKED** · **IMPLEMENTATION PARTIAL SOURCE; WRITE FLOW BLOCKED** · **RUNTIME NOT VERIFIED**. API #75 reverse inventory có thể là `R` cho local route/module/test source; API DD vẫn Draft.

## 4. Current source verification — 2026-11-16

`npm test -- --progress=false --include src/app/features/admin/AD08/pages/ad08-page.spec.ts` passed (1 file, 4 tests). It covers raw route ID/Bearer use, local draft with Save/upload disabled, missing-data error, Back-to-AD-07 navigation/no PUT, and exact large ID display. `npm run build` passed; existing CSS budget warnings remain for student layout, shared Student static CSS and ST-22. Browser/deployment runtime is not verified. Full command outcomes are recorded in `.agents/worklog/2026-11-16/implement-study-screens-apis.md`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Complete docs preflight; read selected docs worklogs and required context pages.
2. [x] Review inventory, prototype/image, AC-32, API catalog/DD/source/tests, schema candidates and Study Web source boundary; update worklog expected/current trace.
3. [x] Write this plan before creating marker JSON, annotation or DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated PNG; inspect image and move markers away from text where practical.
5. [x] Author A–F DD with 1:1 marker rows, sequenced events, API matrix/errors, state/navigation matrix and explicit blockers.
6. [x] Update AD-08 inventory and API #075 reverse source index; update global tracker/checkpoint.
7. [x] Static audit source hashes/dimensions, marker sequence/uniqueness/bounds and C-table bijection, JSON/XML/links, inventory IDs/folders and core bundle count. Application tests/runtime not run.
8. [x] Finalize worklog; do not process another Screen ID.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
