# ST-20 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-20-TC-001` | Planning ref / not run | `AC-18` | See source acceptance section | P2 |

## 2. Test planning references

### ST-20-TC-001 — Acceptance planning reference (AC-18)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-20](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-18`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### F.1. Checklist

- [x] 16 nhóm element đang nhìn thấy trên HTML-derived screenshot được đánh số, có mapping một-một trong DD và marker JSON.
- [x] PNG gốc và HTML gốc được giữ nguyên; ảnh render bổ sung ghi rõ provenance và giới hạn static-only.
- [x] Expected inventory, AC-18/API design và current source được tách riêng; conflict inventory vs AC-18 được ghi rõ.
- [x] API #21/#38 method/path/auth/query/body/response/success/errors và `DECLARED_NOT_RUNNABLE` status được ghi theo catalog/source.
- [x] 11 event có trigger, input, processing, output và ngoại lệ; không tạo API/schema/metric/award rule chưa được xác nhận.
- [x] Mỗi event ghi element/lifecycle kích hoạt và loại event; CTA #9 được mô tả theo đúng semantic anchor link của HTML.
- [x] State matrix, điều hướng ST-08/ST-21/ST-22 và session/access constraints được ghi.
- [ ] API #21 có query grammar, progress DTO, aggregate formula/scope/denominator/rounding, user binding và empty semantics được duyệt.
- [ ] API #38 có award criteria, response projection, course filter, pagination/order và empty policy được duyệt.
- [ ] Inventory/API orchestration được reconciled với AC-18 sequencing qua #37.
- [ ] Study Web route/runtime và Student API #21/#38 được triển khai/wire, sau đó mới có thể xác minh runtime.
- [ ] Loaded-state UI cho progress/achievements và phân biệt partial/empty/error được thiết kế.
- [ ] Prototype/loaded-state visual được đối chiếu và thống nhất với Study Web design target.

### F.2. Blockers

1. API #21 Student route/module/query/test `NOT_FOUND`; response `UserProfile` không biểu diễn progress. Query selector syntax, aggregate source/formula/scope, merge key, owner binding và no-enrollment/no-progress shape chưa chốt.
2. API #38 Student route/module/query/test `NOT_FOUND`; không có award policy/registry/table được xác nhận. Projection, course filter/access, pagination/order, duplicate/empty semantics chưa chốt.
3. Inventory yêu cầu #21/#38 độc lập; AC-18 diagram mô tả #21 → tổng hợp → #37 → tổng hợp → #38 → render. Thứ tự orchestration/partial timing chưa được reconcile.
4. Original PNG thiếu toàn bộ main content; HTML chỉ có static empty state. Loaded dashboard design chưa có trong tài sản hiện hành.
5. Study Web route/auth guard/runtime cho ST-20 chưa có; ST-21/ST-22 route/data handoff chưa được wire.
6. Candidate DDL `lesson_progress` không xác nhận live schema và không có achievements table; không đủ căn cứ để tính progress hoặc awards.
7. Prototype HTML tải remote CDN/font, dùng layout 1440px và trộn primary token khác intended Study Web design target; loaded-state design chưa được duyệt.

**Kết luận:** DD BLOCKED vì còn quyết định nghiệp vụ/API cần xác nhận; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Không chạy tests hoặc gọi runtime trong phiên tài liệu này.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Verification plan

- Record original PNG/HTML hashes/dimensions; ensure originals remain byte-identical.
- If browser render succeeds: record Chromium render provenance/hash/dimensions; inspect HTML-derived image and use it for annotation with clear source metadata. Otherwise annotate original PNG and mark main body unavailable.
- Validate ordered markers/count/coordinates, unique mapping against DD element rows, event IDs, relative links, API error sets, tracker status/counters/next pointers and whitespace.
- Run `git diff --check`; no tests or runtime API checks are planned.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
