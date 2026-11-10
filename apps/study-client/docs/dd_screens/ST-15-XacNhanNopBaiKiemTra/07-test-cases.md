# ST-15 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-15-TC-001` | Planning ref / not run | `AC-16` | See source acceptance section | P1 |

## 2. Test planning references

### ST-15-TC-001 — Acceptance planning reference (AC-16)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-15](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-16`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu, blocker và nguồn

### F.1. Blocker/discrepancy cần owner xử lý

1. Chốt #30 answer JSON shape/encoding, upsert key, ownership/state validation, queue ordering/serialization, retry/idempotency/versioning và cách xác định một write đã thực sự được lưu; xác định schema target giữa legacy BIGINT và V1-PILOT UUID/lifecycle.
2. Chốt #31 ownership vs masked 404, allowed attempt states, quiz-open/deadline rule, repeat submit, concurrency/idempotency/locking, 409 semantics, transaction/rollback và response/status fields; ánh xạ AC-16 sang schema/runtime được phê duyệt.
3. Chốt grading formula, cách xác định câu manual, `PENDING_GRADE`/`GRADED` projection, score/timestamp disclosure và result-read timing.
4. Chốt ST-14 → ST-15 handoff: summary source, pending queue, refresh/direct entry, attemptId route validation và continue/back restoration.
5. Chốt authoritative countdown/expiry policy, unanswered definition, flag source, saved-count semantics, attempt ordinal/limit và nội dung policy copy.
6. Sửa discrepancy PNG confirmation vs HTML unavailable fallback; loại bỏ/duyệt claim chấm điểm tức thì và hardcoded hash route.
7. Wire Study Web route/UI và Student API #31 implementation; hiện tại không có source/test/runtime path để verify.
8. Chốt dialog close/header destinations, accessibility behavior, responsive layout và error/recovery copy trước triển khai.

### F.2. Checklist

- [x] Có plan riêng được lập trước marker/DD; giữ nguyên `screen.png` và `code.html`.
- [x] 18 marker tuần tự khớp duy nhất 18 `Element ID` trong mục C.
- [x] Có luồng route, confirm, continue, flush-before-submit, submit success, error/conflict/ambiguous và state matrix.
- [x] Ghi rõ #30/#31 contract, business codes và giới hạn design-only/current source.
- [x] Ghi expected/current behavior và discrepancy PNG/HTML/timer/summary.
- [x] Có navigation handoff ST-14/ST-16, security/privacy và UI accessibility target.
- [x] Static audit: 18 marker tuần tự/in-bounds; 18 marker map một-một với 18 element rows và SVG labels/groups; tọa độ JSON/SVG khớp; annotated PNG đúng 2×; 22 link DD và 20 link plan resolve; PNG/HTML hash và kích thước đối chiếu plan.
- [x] Event references của Continue/Submit khớp EV-02/EV-03; raw và annotated PNG đã được xem lại; HTML fallback và route/source absence được ghi là current-source evidence.
- [ ] Chốt các blocker ở F.1 trước khi tuyên bố DD READY hoặc implementation-ready.
- [ ] Có route/UI/API source và verification runtime trước khi đánh dấu RUNTIME VERIFIED.

### F.3. Nguồn truy vết

- [Kế hoạch ST-15](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_PLAN.md), [marker map](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_markers.json), [ảnh nguồn](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/code.html), [ảnh chú thích](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen_annotated.png).
- [Inventory, F05 và G-09](../../list_screen.md); [ST-14 handoff](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md).
- [API catalog #30–#32](../../../../../docs/lists/list_api.md); [API #30 open questions](../../../../study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md).
- API #31 DD: [overview](../../../../study-server/docs/dd/31_attempts_submit/02_Overview.md), [request](../../../../study-server/docs/dd/31_attempts_submit/03_Request.md), [response](../../../../study-server/docs/dd/31_attempts_submit/04_Response.md), [mapping](../../../../study-server/docs/dd/31_attempts_submit/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/31_attempts_submit/06_Error.md), [open questions](../../../../study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md).
- [AC-16 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [UI target](../../../../../.agents/web-study/design.md).
- Candidate DB references: [table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql); these do not establish live schema.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
