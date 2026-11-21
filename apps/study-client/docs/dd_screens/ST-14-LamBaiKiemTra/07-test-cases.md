# ST-14 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-14-TC-001` | Planning ref / not run | `AC-16` | See source acceptance section | P1 |

## 2. Test planning references

### ST-14-TC-001 — Acceptance planning reference (AC-16)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-14](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-16`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu, discrepancy và nguồn

### F.1. Blocker/discrepancy cần owner xử lý

| ID | Bằng chứng | Trạng thái | Tác động |
|---|---|---|---|
| ST14-B01 | AC-16 order là GET #28 → eligibility → POST #29; ST-13 row/DD gắn #29 với Start, ST-14 row cũng liệt kê #29 và path ST-14 đã đòi `attemptId`. | `DISCREPANCY / BLOCKER` | Chốt một screen trigger và route handoff; giữ AC-16 API order và không tạo attempt hai lần. |
| ST14-B02 | PNG là quiz mockup; HTML là unavailable fallback với hai anchor tĩnh, không có form/control/API/timer handler. | `DISCREPANCY` | Không coi mockup UI hoặc anchor tĩnh là runtime. |
| ST14-B03 | Study Web editable source/router thiếu; Student API #28–#32 không có route/module/test. | `UNWIRED / NOT_FOUND / DECLARED_NOT_RUNNABLE` | Không thể xác minh auth, UI, API integration, side effect hoặc navigation. |
| ST14-B04 | API #30 `answer(s):string` chưa có physical JSON property/representation; legacy `quiz_answers` có một `choice_id`/row, còn V1-PILOT dùng UUID answer snapshot immutable sau submit; upsert key/concurrency/transaction mở. | `BLOCKER — API/DB contract` | Không thể đặc tả request validation/persistence hoặc retry an toàn; không có mapping được duyệt giữa các schema artifacts với API. |
| ST14-B05 | #30 attempt ownership/state/expiry/question relation/response answers và answer-disclosure policy chưa chốt. | `BLOCKER — access/response policy` | Không thể định nghĩa authorization, response mapping và state transitions. |
| ST14-B06 | Inventory thiếu GET attempt/answer; refresh/direct-entry không có restore source. | `BLOCKER — lifecycle` | Không thể hydrate answer/progress/flag/timer cho route có `attemptId`. |
| ST14-B07 | Hai timer; progress `14/20`, answered/unanswered `13/6`, flag count `1` chưa có overlap rule; không có time source/formula. | `DESIGN_ONLY / SOURCE_REQUIRED` | Không tính hoặc khóa attempt từ số mẫu. |
| ST14-B08 | WebSocket ping, idempotent autosave, instructor, attempt count/part/points/tags đều không có contract/source tương ứng. | `DESIGN_ONLY / SOURCE_REQUIRED` | Không biến mockup copy thành functionality/data. |
| ST14-B09 | Flag persistence, filter semantics, answer ordering/cardinality, exit and dirty-state policy chưa có nguồn. | `BLOCKER — UI/API decisions` | Cần quyết định trước implementation để không mất/hiểu sai state. |
| ST14-B10 | API #30 catalog không có 409; timeout may be ambiguous; #29 idempotency chưa chốt; ST-15 state machine mở. | `BLOCKER — retry/submit lifecycle` | Không tự retry, autosubmit, hoặc tuyên bố submitted/saved. |

### F.2. Checklist

- [x] ST-14 plan được tạo trước markers/DD; worklog ghi exact-type docs preflight và source trace.
- [x] Giữ nguyên source `screen.png`/`code.html`; ghi kích thước và SHA-256.
- [x] Có 32 marker tuần tự `#1–#32`; marker IDs ánh xạ một-một tới bảng element.
- [x] Có `screen_annotated.png` và SVG transparent overlay; marker positions được xem trực quan và chỉnh marker #13 khỏi text.
- [x] Expected/current behavior tách riêng; UI/API/DB design không bị gọi nhầm runtime.
- [x] Events mô tả input, prerequisite, ordered processing, API/error boundary, side effect/output và điểm chưa chốt.
- [x] #28/#29/#30, AC-16, G-09, ST-13 handoff và ST-15 submit boundary được truy vết.
- [x] State/navigation, role/access và answer disclosure policy/blocker được nêu.
- [x] Static audit hoàn tất: marker order/bounds/map, PNG dimensions/hash, SVG labels, local links và scoped `git diff --check` đã kiểm tra; không chạy application tests, browser runtime hoặc live DB.
- [ ] Owner chốt #29 trigger/handoff, #30 answer contract/storage/upsert/access/response/retry, resume/time source, flag and UI recovery.
- [ ] Student routes/API được triển khai và kiểm chứng runtime.

**Kết luận:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Bộ tài liệu truy vết được và nêu rõ quyết định còn thiếu, nhưng chưa đủ implement autosave/resume/submit flow mà không suy luận.

### F.3. Nguồn

- [Screen inventory, F05, API index và G-09](../../list_screen.md)
- [ST-14 plan](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_PLAN.md), [source PNG](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/screen.png), [source HTML](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/code.html)
- [ST-13 handoff DD](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md), [ST-15 submit screen](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra)
- [API catalog #28–#32](../../../../../docs/lists/list_api.md)
- API #28/#29 open questions: [#28](../../../../study-server/docs/dd/28_quizzes_detail/OPEN_QUESTIONS.md), [#29](../../../../study-server/docs/dd/29_quizzes_attempts/OPEN_QUESTIONS.md)
- [AC-16 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- API #30 DD: [request](../../../../study-server/docs/dd/30_attempts_answers/03_Request.md), [response](../../../../study-server/docs/dd/30_attempts_answers/04_Response.md), [mapping](../../../../study-server/docs/dd/30_attempts_answers/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/30_attempts_answers/06_Error.md), [open questions](../../../../study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md)
- [Answer table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT schema artifact](../../../../../infra/postgres/02_study_db.sql)
- [Study Server declared routes](../../../../../.agents/server-study/apis/declared-routes.md), [current API router](../../../../study-server/app/api/v1.py), [Study Web wiring status](../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../.agents/web-study/design.md)

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
