# SH-07 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-07-TC-001` | Planning ref / not run | `AC-12` | See source acceptance section | P2 |
| `SH-07-TC-002` | Planning ref / not run | `AC-25` | See source acceptance section | P2 |
| `SH-07-TC-003` | Planning ref / not run | `AC-36` | See source acceptance section | P2 |
| `SH-07-TC-004` | Planning ref / not run | `AC-38` | See source acceptance section | P2 |

## 2. Test planning references

### SH-07-TC-001 — Acceptance planning reference (AC-12)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-12`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md).
### SH-07-TC-002 — Acceptance planning reference (AC-25)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-25`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md).
### SH-07-TC-003 — Acceptance planning reference (AC-36)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-36`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md).
### SH-07-TC-004 — Acceptance planning reference (AC-38)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-38`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 11. Tiêu chí nghiệm thu

- [x] Kế hoạch được tạo trước DD/marker/annotation.
- [x] Giữ ảnh nguồn; có `screen_annotated.png` và marker JSON sau static audit.
- [x] 35 marker mặc định ánh xạ đúng 35 visible Element IDs; hidden modal được mô tả riêng.
- [x] Current API #18 route/module/query/test/store được đối chiếu; API #63/#64/#93/#96 producer/status-specific behavior được phân biệt.
- [x] API contract, source runtime, test source, schema và prototype không bị trộn lẫn; discrepancies/blockers được ghi.
- [x] DD mô tả 10 event, API #18 expected request/error shape, states/navigation/security/a11y/design drift và acceptance gaps.
- [x] Không tạo API/field/enum/TTL/polling/SSE/result/download/route behavior chưa có nguồn.
- [ ] DD READY — chưa đạt vì contract #18 và end-to-end ID/status mapping còn blocker; trạng thái giữ `DD BLOCKED`.
- [ ] RUNTIME VERIFIED — chưa đạt; Study Web UI/router và API #18 runtime không có source hiện hành. Subcontext docs hiện có nhưng giữ status `UNWIRED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blockers and acceptance gate

1. `SH07-B01 API18_UNWIRED`: no route/module/query/test or Study Operation table; operation tracking cannot be runtime verified.
2. `SH07-D01 OPERATION_ID_TYPE`: API #18 row int64 vs UUID convention/schema/AC and producer #63/#93 UUID.
3. `SH07-D02 STATUS_AND_KIND`: enum/lifecycle/terminal states unresolved; notification-specific QUEUED/FAILED/SENT do not define generic status.
4. `SH07-D03 AUTHORIZATION`: owner-only vs owner/Admin and wrong-owner 403/404 semantics unresolved.
5. `SH07-D04 PRODUCER_AND_RESULT`: #93 row/source/summary disagree; #103 Report vs Operation result and `result?:Payment` mismatch; #17/#103 not source-backed.
6. `SH07-B02 POLLING_AND_RETENTION`: no cadence/retry/SSE/TTL contract; prototype-specific 3s, 24h, 15min are unsupported.
7. `SH07-B03 NAVIGATION_ORIGIN`: generic safe-return origin not specified; CTAs in source conflict with inventory linkage.
8. `SH07-B04 PROTOTYPE_ONLY_UI`: UUID fallback, mock environment, diagnostic claims and backend architecture copy cannot be presented as live user/job data.

- [x] `SH-07_PLAN.md` was created before DD/markers/annotation; source trace was revalidated before any DD or image edit in this session.
- [x] Original image and HTML hashes remain unchanged; source and annotated images are 1503×1600.
- [x] Annotated source has 35 ordered unique markers mapping exactly to 35 visible DD elements; hidden modal is excluded from default-image numbering. Visual review moved #23 into the left gutter so it does not cover the diagnostic code.
- [x] DD covers every visible element plus hidden modal controls, 10 event paths, state/error/navigation, security, accessibility, design-system drift and source links; re-audit corrected its stale Study Web subcontext status statement before final verification.
- [x] API #18 and producer sources are distinguished from design catalog; no API/field/enum/route behavior is invented.
- [x] Major unresolved contract decisions are blockers; set `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until approved evidence closes them.
- [x] Static ID/element/event/link/image/hash/whitespace audit and tracker/worklog update are complete; the 83 inventory IDs match the 83 tracker rows and the next handoff is GS-01.

### Trích từ DD nguồn: 7. Session result (fill after review)

- Result: Current Study source and contract trace revalidated; marker #23 moved clear of the schema diagnostic; static audit passed with 83 inventory IDs matching 83 tracker rows, 35 ordered marker-to-element mappings, 10 unique events, resolving local links, unchanged source hashes, equal 1503×1600 image dimensions, and clean `git diff --check`. Tests and runtime were not run/verified.
- DD status: `DD BLOCKED` because API #18 and end-to-end operation ID/status/owner/producer contracts remain inconsistent or absent; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Screen ID: GS-01, the first unstarted W0 screen in the tracker, for a separate session. No other Screen ID is part of this session.

### Re-audit note (2026-11-07)

- Rechecked the Study Web context claim: `.agents/web-work/study/AGENTS.md` and `INDEX.md` exist and the manifest registers them as `study-web: UNWIRED`; editable app source and `package.json` remain absent. Corrected the DD, this plan and tracker to distinguish context docs from runtime evidence.
- Static verification passed: 83 inventory IDs match 83 tracker rows; all 35 ordered markers map to 35 DD element rows, marker coordinates are in bounds, the SVG parses with labels 1–35, 10 unique event IDs are present, and all 23 local DD/plan links resolve. Original `screen.png` and `code.html` hashes are unchanged; both source and annotated images are 1503×1600. The annotation was viewed and marker #23 is clear of the diagnostic text.
- Tests, browser/runtime, live database and deployment were not run or verified. Status remains `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
