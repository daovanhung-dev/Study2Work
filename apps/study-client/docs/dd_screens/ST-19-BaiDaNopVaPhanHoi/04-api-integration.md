# ST-19 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-19-API-001` | #36 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #36
- Orchestration/data notes: GET #36 cho Student; inventory yêu cầu kiểm tra ownership nhưng predicate trong API #36 DD còn SOURCE_REQUIRED. Không tự hiển thị GRADED nếu response chỉ là SUBMITTED; score/feedback cần disclosure policy.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #36 chỉ có catalog/Draft DD, Student route/module/query/test NOT_FOUND; ownership/access predicate, 403-vs-404, score/feedback release, SubmissionStatus/timezone/path parsing còn mở; logical `files[]` không map được vào legacy scalar `file_url`, assignment/user nullability và live schema chưa xác minh; API #35 `data.id` vs inventory `submission_id` handoff chưa chốt; rubric/cohort/mentor/PR/booking/skill/next-assignment fields thiếu API contract; loaded graded PNG khác Guest fallback HTML (Tailwind CDN/config, remote fonts, max-width 1440px) và Study Web design target; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory / F06](../../list_screen.md)
- [Original PNG](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen.png), [HTML companion](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/code.html), [marker map](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen_annotated.png)
- [API catalog #36](../../../../../docs/lists/list_api.md)
- [API #36 overview](../../../../study-server/docs/dd/36_submissions_detail/02_Overview.md), [request](../../../../study-server/docs/dd/36_submissions_detail/03_Request.md), [response](../../../../study-server/docs/dd/36_submissions_detail/04_Response.md), [data mapping](../../../../study-server/docs/dd/36_submissions_detail/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/36_submissions_detail/06_Error.md), [open questions](../../../../study-server/docs/dd/36_submissions_detail/OPEN_QUESTIONS.md)
- [AC-17](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC-23](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio)
- [Mentor API #55 current implementation](../../../../study-server/app/modules/mentor/api_55_mentor_submissions_detail/view.py)
- [Candidate Study DDL](../../../../../infra/postgres/study-server/DB.sql), [Study Web current design/source status](../../../../../.agents/web-study/design.md)

### Trích từ DD nguồn: A.4. API contract và trạng thái source

| Thuộc tính | API #36 |
|---|---|
| Method / endpoint | `GET /api/v1/submissions/{submission_id}` |
| Authentication | Student Bearer JWT theo catalog; caller identity lấy từ token, không nhận user ID từ URL/body. |
| Path | `submission_id:int64!`; positivity, range và parse-failure response chưa được định nghĩa. |
| Query / body | Không khai báo query parameter hoặc request body. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Submission>`. |
| Errors | Chỉ 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Không thêm 400/422 theo suy đoán. |
| Current source | Student API #36 route/module/query/test `NOT_FOUND`; không có runtime call để xác minh. Mentor API #55 là operation khác. |
| Open policy | Owner/access predicate; 403-vs-404 masking; score/feedback release; file association/URL; status lifecycle/timezone; malformed path; candidate schema vs live schema. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md)
