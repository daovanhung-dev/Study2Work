# ME-06 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-06-TC-001` | Planning ref / not run | `AC-22` | See source acceptance section | P1 |

## 2. Test planning references

### ME-06-TC-001 — Acceptance planning reference (AC-22)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-06](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-22`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 8. Acceptance criteria

1. API #49 GET được gọi cho course ID numeric; loading/empty/ready/error/denied/not-found được tách trạng thái; response node IDs/status/order được giữ nguyên.
2. Client dựng parent-child từ `parent_id` sau khi validate response; không mất/đổi ID, không render một cây partial, không dùng Content ID như Lecture ID nếu chưa có mapping.
3. Không gắn nhãn published/draft/hidden từ sample; mapping chỉ dùng enum/lifecycle do API/Product owner duyệt.
4. Không hiện count/KPI/chart/quality/audit values hardcoded như dữ liệu course; phải có nguồn đọc được duyệt hoặc bỏ khỏi runtime.
5. Save reorder, child create, direct publish từ pending review, rubric/question bank và menu chưa có contract phải disabled/removed hoặc mở flow đã duyệt; không giả thành công bằng toast/DOM mutation.
6. Khi #50–#53 được dùng: direct-owner/role errors, 404/422/500 được hiển thị phù hợp; #51 version snapshot/review status và #53 dependency/soft-delete được tôn trọng; refresh #49 sau mutation theo decision đã duyệt.
7. Route, keyboard/focus/ARIA, responsive view, cache and retry behavior cần được verify trong Study Web runtime trước khi gắn `RUNTIME VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Tiêu chí hoàn tất phiên

- `screen.png` và `code.html` giữ nguyên hash; không sửa thêm Screen ID.
- Plan được viết trước marker/ảnh/DD; mọi quyết định lấy từ route/model/query/view/DB/test source nêu trên.
- Marker IDs 1–44 liên tiếp, unique, in-bounds; JSON/SVG/DD khớp 100%; annotated PNG đúng 2734×3200, tỷ lệ gốc, được kiểm tra trực quan.
- DD mô tả rõ API #49 và giới hạn #50–#53; ghi trạng thái riêng `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Tracker/checkpoint phản ánh đủ bốn core artifacts; worklog nêu preflight, nguồn, lệnh/hasil static audit và việc test/runtime không chạy.
- Chạy static artifact audit và `git diff --check`; không chạy tests, browser/runtime hay context validator (context pages không thay đổi).

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
