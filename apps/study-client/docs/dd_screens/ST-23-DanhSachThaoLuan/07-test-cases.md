# ST-23 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-23-TC-001` | Planning ref / not run | `AC-19` | See source acceptance section | P2 |

## 2. Test planning references

### ST-23-TC-001 — Acceptance planning reference (AC-19)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-23](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-19`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Screen ID, actor, route, AC/API references and cross-screen relations are traceable to inventory/AC/API sources.
- [x] Original blank PNG and HTML are preserved; HTML render is a separate artifact with renderer, size and source hash recorded.
- [x] Every visible rendered HTML group has a unique ordered marker and exactly one DD row.
- [x] Ten events specify trigger/input/ordered handling/output/exceptions; unsupported controls/actions remain explicitly blocked.
- [x] API #39 fields, query names, response and 200/401/403/500 catalog codes are transcribed; no size/other query or new status is invented.
- [x] Expected empty/list/filter/create behavior is separated from current static HTML/API source; public review API #10 remains a separate flow.
- [x] `loading/empty/ready/error`, navigation and security/access gaps are documented.
- [ ] **DD READY:** blocked until API #39’s seven questions, title source, comments boundary, loaded list/filter/sort/create design and ST-24/40 contract are approved.
- [ ] **IMPLEMENTATION READY:** blocked until Study Web routes/components and Student API #39 runtime are wired against a resolved contract.
- [ ] **RUNTIME VERIFIED:** not verified; static HTML render is not application/API runtime evidence.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Verification plan

- Verify original PNG/HTML hashes and dimensions unchanged; record `screen_rendered.png` provenance/size separately.
- Visually inspect the full rendered HTML and annotated image; adjust marker positions if any marker covers copy/controls.
- Static audit: marker order/uniqueness/bounds; one-to-one map to DD rows; SVG XML; DD sections A–F; event numbering/input-process-output-exception coverage; API #39 contract/query/status exactness; local Markdown links; tracker counts/next pointers; `git diff --check`.
- No API calls, runtime verification or tests (not requested).
- No `.agents/` context changes are planned; run context validator only if a context page/manifest actually changes.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
