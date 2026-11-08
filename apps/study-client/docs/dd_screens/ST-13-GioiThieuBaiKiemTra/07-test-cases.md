# ST-13 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-13-TC-001` | Planning ref / not run | `AC-16` | See source acceptance section | P1 |

## 2. Test planning references

### ST-13-TC-001 — Acceptance planning reference (AC-16)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-13](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-16`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md).

## 3. Source acceptance / test plan (not run)

> CẦN_XÁC_NHẬN: DD nguồn không có section test/acceptance được nhận diện.


#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Trạng thái, block và tiêu chí đầu ra

- Expected state từ inventory: `loading / closed / available / denied`; các trạng thái lỗi mạng/401/404/500 chỉ đặc tả khi gắn đúng response catalog. Không suy ra closed từ UI copy hay 409 cho API #28.
- Chụp nguyên ảnh gốc không chỉnh sửa; tạo `ST-13_markers.json`, `ST-13_markers_overlay.svg`, `screen_annotated.png` giữ đúng tỉ lệ; tạo `ST-13.md` gồm tổng quan A–F, element 1–30, event inputs/process/results, API mapping, state/navigation, acceptance checklist và source trace.
- BLOCKERS cần giữ: HTML/PNG mismatch; Study Web UNWIRED; API #28/#29 NOT_FOUND ở runtime; eligibility/access/status mapping; duration/deadline/time source; answer exposure/QuizChoice; attempt limit/resume/idempotency/409; sample values/history/proctor/auto-save/auto-submit/scoring/certification chưa có nguồn; CTA destinations chưa chốt; candidate schema khác nhau và live schema chưa xác nhận.
- Chỉ tĩnh kiểm tra hash nguyên bản, kích thước/tỉ lệ, marker sequence/bounds/ánh xạ, links và tracker, cùng `git diff --check`. Không chạy test, browser flow hay runtime.
- Không đánh dấu DD READY khi policy/route/data/event chưa đủ nguồn. Kết quả dự kiến: `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
