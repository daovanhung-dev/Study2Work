# ST-15 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-15-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Xem số câu chưa làm, xác nhận nộp và khóa chỉnh sửa khi server chấp nhận.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #30 body/queue/upsert/order/outcome/retry và #31 ownership/state/repeat/deadline/concurrency/grading/transaction/response còn mở; ST-14 summary/dirty-queue handoff/direct entry chưa có contract; legacy BIGINT và V1-PILOT UUID/payload/lifecycle khác; PNG/HTML, timer/count/saved/attempt/instant-grading claims không thống nhất; Student #30–#32 route/module/test NOT_FOUND; Study Web UNWIRED; live schema chưa xác minh
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
