# AD-16 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-16-API-001` | #88 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-16-API-002` | #89 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #88, #89
- Orchestration/data notes: POST #88 khi tạo; PUT #89 khi sửa. Không giả định GET admin quiz detail; #87 metadata-only và `questions=[]` local. #89 catalog không khai báo body; local fallback yêu cầu replacement body. Autosave copy trong prototype chưa có persistence source.
- BE/source status và gate: **R** local #88/#89 route/module/query/model/validator/test source; API DDs remain Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** thiếu GET detail/question set, #89 body discrepancy, question/choice editor và course option mapping; field/range rules, AC-35 permission vs `ADMIN`, legacy/V1-PILOT/live schema, autosave/navigation và Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Contract API và current source

| API | Contract trực tiếp trong catalog | Current local source (không thay thế contract) |
|---|---|---|
| #88 Create | `POST /api/v1/admin/quizzes`; Bearer JWT/Admin; body `{config:string!, questions:string!}`; response `ApiEnvelope<Quiz>`; 201 `DESIGN_RESOURCE_CREATED`; 401/403/422/500. API DD `Draft — Needs Confirmation`. | Route #88 parse raw body sau shared `ADMIN` guard. Strict outer body gồm đúng hai chuỗi `config`, `questions`; validator decode hai chuỗi JSON và áp dụng nested shape `config{course_id:int,title:string,duration_minutes?:int|null,passing_score:string}`, `questions[{text,type,choices[{text,is_correct?}]}]`. Shape này là `DERIVED`. Local code chỉ xác nhận Course tồn tại, ghi Quiz + Question + Choice theo thứ tự request (candidate order zero-based), map response rồi mới commit; lỗi sau khi bắt đầu transaction rollback. Response local có `is_correct`. |
| #89 Update | `PUT /api/v1/admin/quizzes/{quiz_id}`; Bearer JWT/Admin; path `quiz_id:int64!`; catalog **không khai báo body**; response `ApiEnvelope<Quiz>`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. API DD `Draft — Needs Confirmation`. | Route local nhận raw body và path; shared `ADMIN` guard chạy trước parse. Local handler yêu cầu positive int64 và reuse validator/body như #88. Khóa Quiz/children; nếu có attempt hoặc answer history trả 422 trước write; xác nhận Course tồn tại (local fallback cho phép chuyển Quiz sang Course khác), không thấy policy course-status/enrollment; cập nhật metadata rồi xóa Choices trước Questions và thêm replacement set theo request order (candidate order zero-based); response mapping hoàn tất trước commit. Local source không có optimistic version. Body, full replacement, history refusal, course move, locks và tombstone handling là `DERIVED`. |

Không có `GET /api/v1/admin/quizzes/{quiz_id}` để tải dữ liệu edit. #87 là list metadata-only trong local source (`questions=[]`), còn catalog response cardinality cũng khác local Page projection. Vì vậy AD-16 không có nguồn xác nhận để prefill Quiz và Question Builder khi mở edit route. Không gọi #87 thay thế detail.

### Trích từ DD nguồn: Nguồn truy vết chính

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

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md)
