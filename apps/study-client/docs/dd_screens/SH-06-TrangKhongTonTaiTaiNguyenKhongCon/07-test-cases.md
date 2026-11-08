# SH-06 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-06-TC-001` | Planning ref / not run | `AC-05` | See source acceptance section | P0 |

## 2. Test planning references

### SH-06-TC-001 — Acceptance planning reference (AC-05)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-06](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-05`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 10. Tiêu chí nghiệm thu

- [x] Có `SH-06_PLAN.md` lập trước khi tạo DD/ảnh chú thích.
- [x] Ảnh nguồn được giữ nguyên; ảnh chú thích và marker JSON có đủ 22 marker theo thứ tự.
- [x] Bảng element có 22 dòng tương ứng, bao gồm course mock, CTA, nav, contact và footer controls.
- [x] Có route-404/resource-404/service-error/forbidden phân biệt; 500 không đổi thành 404.
- [x] API #08 route → validation → query → mapping → status/error → test source được đối chiếu; sai khác nhãn inventory/API index, trạng thái contract/API DD và source được ghi riêng.
- [x] AC-05 403 discrepancy và DDL/live DB limitations được ghi rõ; không tạo data/API/route mới.
- [x] 10 event có đầu vào, điều kiện, thứ tự xử lý, API/hành động, output/ngoại lệ.
- [ ] Product/UX đã chốt disposition recommendation/contact/footer/legal surfaces và từng destination. Đây là lý do DD vẫn `BLOCKED`.
- [ ] AC-05/API #08 `404/403` discrepancy đã được owner giải quyết.
- [ ] Study Web router/source tồn tại và route paths đã được xác nhận trong source; implementation vẫn `BLOCKED`.
- [x] Local links, marker map (22/22), image dimensions (1600×1425) và source hashes đã được kiểm tra tĩnh; `git diff --check` đạt.
- [ ] Study Web implementation/runtime verification chưa đạt vì thiếu client source/router và dependency decisions.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blocker, discrepancy và acceptance gate

1. `BLOCKER: SH06_PRODUCTION_SURFACE_UNDECIDED` — recommendation cards, help/contact strip, footer destinations và copyright/legal copy hiện có trong prototype nhưng chưa có content/route contract. Cần quyết định giữ/ẩn/bỏ từng surface và xác nhận dữ liệu/đích; không biến `href="#"` hoặc text mẫu thành production behavior.
2. `BLOCKER: AC05_NOT_FOUND_STATUS_CONFLICT` — AC-05 vẽ `404/403` cho nhánh course không tồn tại/PUBLISHED; API catalog và handler #08 chỉ có 404 cho invalid/missing/unpublished, 500 cho internal failure. Cần chỉnh AC hoặc xác nhận ý nghĩa 403 trước khi chốt luồng giữa SH-06 và SH-05.
3. `DISCREPANCY: API_08_STATUS_LABELS_VS_SOURCE` — dòng SH-06 trong screen inventory ghi BE `D`, API index ghi #008 `R`, root API contract là approved design nhưng chưa runtime-verified và API DD #08 vẫn Draft; route/module/test source hiện tồn tại. Deployment/live DB chưa verified. #08 success trả ApiEnvelope có `data: Page<Course>` singleton; không nhầm `Page<Course>` là toàn response.
4. `IMPLEMENTATION_BLOCKER: STUDY_WEB_ROUTER_NOT_FOUND` — không có `src/`/package manifest; dist bundle cũ không chứng minh `/not-found` hoặc route actions.
5. `DESIGN_SYSTEM_DRIFT` — HTML dùng remote Google Fonts/Tailwind CDN và max-width 1440px; Study guide chỉ định system/Inter local, content width khoảng 1120px, control 44px+, responsive reflow. Cần xác nhận có hiệu lực với prototype này hay không.

Kế hoạch sau source review: cập nhật SH-06 DD với expected/current tách biệt, 22 element, 10 event, mapping #08 có trace, và blockers không suy đoán. Không gọi màn hình `DD READY` khi các surface nhìn thấy chưa có quyết định triển khai hoặc AC-05 còn mâu thuẫn. Kiểm tra tĩnh marker→element, link, ảnh và hash sau khi cập nhật; không chạy tests/runtime trong phiên tài liệu.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
