# AD-15 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-15-TC-001` | Planning ref / not run | `AC-35` | See source acceptance section | P1 |

## 2. Test planning references

### AD-15-TC-001 — Acceptance planning reference (AC-35)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-15](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-35`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Kế hoạch được lập trước markers/ảnh đánh số/DD; scope chỉ AD-15.
- [x] `screen.png` và `code.html` được giữ nguyên; hash nguồn được ghi trong worklog.
- [x] 50 marker tuần tự được mô tả một-một tại §C và có trong JSON/SVG; ảnh annotated 2×.
- [x] AC-35, inventory, catalog/API DD #87 và local route/module/query/model/test/DDL được đối chiếu; expected/current và discrepancy tách rõ.
- [x] Mọi element đánh số có loại/mục đích, nguồn/state hiện tại và event hoặc ghi rõ không có event.
- [x] EV-01…EV-12 có trigger, điều kiện, input, xử lý, API/handoff, kết quả và ngoại lệ trong giới hạn bằng chứng.
- [x] Trạng thái empty/loading/auth/forbidden/validation/service/network được phân biệt; 422 local được đánh dấu derived ngoài catalog.
- [x] Điều hướng AD-16/17/18 và ID/filter transfer được gắn nhãn expected/candidate, chưa tuyên bố route chạy thật.
- [x] Relative artifact links, annotation bounds/order/mapping và source hashes đã được audit tĩnh.
- [x] Status riêng: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- [ ] Owner chốt response list/page, field projection, search/course/status mapping, permission và schema live.
- [ ] Study Web route/client được implement; API/runtime behavior được xác minh trong môi trường phù hợp.

### Nguồn truy vết chính

- `apps/study-client/docs/list_screen.md` row 73, §8.1 và reverse index #087.
- AC-35: `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` và `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`.
- API catalog: `docs/lists/list_api.md`, API #87. API DD #87 hiện `Draft — Needs Confirmation`.
- Local API: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/admin/api_87_admin_quizzes_list/` (view, models, query, validate) và `apps/study-server/tests/modules/admin/api_87_admin_quizzes_list/test_admin_quizzes_list.py`.
- Candidate schema: `infra/postgres/study-server/DB.sql`; source này không xác nhận live schema/deployment. Study Web design target: `.agents/web-study/design.md`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Work order và checklist

1. [x] Đọc objective/router/context/worklog preflight; docs selector READY 3/220; đọc AD-01/02/03 và handoff AD-14.
2. [x] Đọc registry/scopes, AC-35, inventory, API catalog/#87 Draft DD, server route/module/query/model/test/DDL, Study Web assets/tree và design target.
3. [x] Lưu plan này trước marker JSON/SVG, annotated image hoặc AD-15 DD.
4. [x] Tạo 50 JSON/SVG marker; render PNG 3200×2788; kiểm tra order/coords/bounds/overlap/1:1 mapping và xem trực tiếp.
5. [x] Viết DD A–F với 50 §C rows, EV-01…EV-12, API/error/state/navigation và blocker/source trace.
6. [x] Cập nhật inventory/API #087 reverse index, global AD-15 checkpoint/core artifact count và worklog; giữ API #87 DD Draft.
7. [x] Audit source hashes, dimensions, JSON/XML, links, 83 folders/IDs, core artifact count, whitespace và `git diff --check`; không chạy application tests/runtime.
8. [x] Chốt AD-15 only; trạng thái màn hình `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; dừng trước AD-16.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
