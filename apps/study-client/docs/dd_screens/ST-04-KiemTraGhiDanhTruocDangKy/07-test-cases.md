# ST-04 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-04-TC-001` | Planning ref / not run | `AC-12` | See source acceptance section | P1 |

## 2. Test planning references

### ST-04-TC-001 — Acceptance planning reference (AC-12)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-04](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-12`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### Kiểm tra đã hoàn thành trong phiên ST-04

- [x] Có plan chi tiết trước khi tạo render, markers hoặc DD.
- [x] Giữ nguyên `screen.png` và `code.html`; tạo render riêng từ HTML tĩnh với provenance rõ ràng.
- [x] Đã xem trực tiếp render và annotated image; annotation không che nội dung quan trọng.
- [x] 13 marker sequential/unique và có một dòng đặc tả tương ứng trong mục C.
- [x] Expected flow, current source, API #08/#15 và blocker được tách riêng; không suy diễn nhánh enrollment.
- [x] Không chạy application tests hoặc khẳng định runtime verified.

### Điều kiện còn thiếu để chuyển sang DD READY

- [ ] Product/backend chốt identity source cho #15, uniqueness/selection rule, 404 semantics, status enum và PUBLISHED predicate.
- [ ] AC-12 thống nhất authenticated Student precondition với API #15 public contract và Study Web auth/route guard.
- [ ] Chốt course ID mapping, điều kiện miễn phí/paid/eligibility, payment confirmation, duplicate enrollment và #18 ordering.
- [ ] Có contract cho các downstream #16–#20 cùng route payload/return/expiry/error state của ST-04–ST-08.
- [ ] Có UI decisions cho loading, course-not-found/not-published, API error, enrollment branches, accessibility/status announcement và responsive nav.
- [ ] Study Web route/client được nối nếu mục tiêu triển khai cần current runtime evidence; runtime verification còn riêng biệt.

**Kết luận:** ST-04 có thể truy vết đến prototype tĩnh, AC-12, catalog/Draft API và current source #08, nhưng chưa đủ thông tin để frontend triển khai an toàn. Giữ `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` cho tới khi các blocker phía trên được quyết định.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion/status criteria

- **Completed:** created `screen_rendered_from_html.png` (2560×2048) from the HTML at a 1280×1024 CSS viewport and device scale 2, after fonts loaded; original screenshot and HTML remain unchanged.
- **Completed:** browser-measured 13 targets and wrote `ST-04_markers.json`, overlay SVG and `screen_annotated.png`; final image visually reviewed.
- **Completed:** wrote A–F DD with all 13 visible targets and EV-01…EV-06, including API request/response/error boundaries and unresolved branches.
- **Completed:** updated ST-04 inventory/global row and API #08 reverse index to `R` from current local source evidence; #15 remains `D`/unwired.
- **Completed:** recorded `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED` while identity/selection and enrollment/payment rules remain unresolved.
- **Completed:** static checks passed for marker/coordinate alignment, dimensions, JSON/XML, local links, original source hashes, 83-screen inventory/folder audit, core artifact count (79/83), and scoped `git diff --check`. No application test/runtime claim.

### Render and marker measurement record

- `screen.png` SHA-256 remains `7df0dac4e7598c3b336d5c5d78f5fd9a851526712aa7dd0fd7224a6ffe61ad7f`; `code.html` SHA-256 remains `24b0e361877b15db88298a29d806a2a17f0151e6685df71647d103477276f4fa`.
- Browser DOM bounds were captured with viewport 1280×1024 CSS px, `deviceScaleFactor=2`; `screen_rendered_from_html.png` and `screen_annotated.png` are both 2560×2048.
- `ST-04_markers.json` stores CSS target bounds and marker centers, plus raster centers at 2×. The visual review moved markers #1/#2/#3/#4/#12/#13 to whitespace/edge callouts so labels do not cover text.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
