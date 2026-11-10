# AD-16 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-16-TC-001` | Planning ref / not run | `AC-35` | See source acceptance section | P1 |

## 2. Test planning references

### AD-16-TC-001 — Acceptance planning reference (AC-35)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-16](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-35`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có ảnh gốc được giữ nguyên và annotated image 2×; 35 marker tuần tự, unique, bounded và ánh xạ một-một tới §C.
- [x] Các element tĩnh, controls, trạng thái disabled, copy và navigation anchors quan sát được đều được mô tả.
- [x] EV-01…EV-10 có trigger, đầu vào, bước xử lý, API boundary, kết quả và ngoại lệ; current behavior tách khỏi expected/candidate.
- [x] API #88/#89 direct catalog được ghi tách biệt với local server source; API DD status vẫn Draft.
- [x] Thiếu detail GET, #89 body, question/course schema, form rules, permission, storage deployment và post-save navigation được ghi thành blocker; không tự thêm contract.
- [ ] Có contract/decision để populate edit screen và question/choice builder.
- [ ] Có request body/validation/permission mapping được owner duyệt và API DD #88/#89 không còn open cho các quyết định AD-16 cần dùng.
- [ ] Có Study Web route/client/auth implementation để xác minh runtime behavior.

**Kết luận:** Tài liệu mô tả đầy đủ prototype và source fallback, nhưng chưa đạt `DD READY` vì edit initialization và mutation payload/UI question builder thiếu contract. Trạng thái màn hình là `DD BLOCKED`; implementation `BLOCKED`; runtime `NOT VERIFIED`.

### Nguồn truy vết chính

- [Screen inventory row 74 và flow Admin quiz](../../list_screen.md)
- [API catalog #87–#91](../../../../../docs/lists/list_api.md)
- [AC-35 Admin quiz diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [Study Server API #88 route](../../../../study-server/app/api/v1.py#L2435), [#89 route](../../../../study-server/app/api/v1.py#L2491)
- [API #88 local models](../../../../study-server/app/modules/admin/api_88_admin_quizzes_create/models.py#L12), [validator](../../../../study-server/app/modules/admin/api_88_admin_quizzes_create/validate.py#L73), [handler](../../../../study-server/app/modules/admin/api_88_admin_quizzes_create/view.py#L271)
- [API #89 validator](../../../../study-server/app/modules/admin/api_89_admin_quizzes_update/validate.py#L19), [query](../../../../study-server/app/modules/admin/api_89_admin_quizzes_update/query.py#L1), [handler](../../../../study-server/app/modules/admin/api_89_admin_quizzes_update/view.py#L310)
- [Study Server database context for Quiz APIs](../../../../../.agents/server-study/database.md#api-88-admin-quiz-create)
- [Migration 013](../../../../../infra/postgres/study-server/migrations/013_quiz_question_type_and_choice_order.sql)
- [API #88 open questions](../../../../study-server/docs/dd/88_admin_quizzes_create/OPEN_QUESTIONS.md), [API #89 open questions](../../../../study-server/docs/dd/89_admin_quizzes_update/OPEN_QUESTIONS.md)
- [Study Web target design](../../../../../.agents/web-study/design.md)

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Work order và checklist

1. [x] Đọc goal objective, root router/context, selector và đúng 3 docs worklogs; thêm handoff AD-15.
2. [x] Đọc project/scope context, AC-35, inventory/API catalog/API DD, server source/tests/schema context, Study Web assets/design.
3. [x] Lưu plan này trước marker JSON/SVG, annotated image hoặc AD-16 DD.
4. [x] Tạo marker JSON/SVG và `screen_annotated.png`; static audit xác nhận source hashes, order, unique IDs, bounds, không overlap, tọa độ và visual legibility.
5. [x] Viết DD A–F với event sequence, field/control table, API variants/errors, states, route handoffs, source citations và blockers.
6. [x] Cập nhật inventory/API reverse index/global checkpoint/worklog; giữ API DDs Draft.
7. [x] Chạy static audit tài liệu/assets/links/counts/whitespace; không chạy application tests/runtime.
8. [x] Chốt AD-16 only, report `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; dừng trước AD-17.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
