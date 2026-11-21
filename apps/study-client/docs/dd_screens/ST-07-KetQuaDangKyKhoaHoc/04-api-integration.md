# ST-07 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-07-API-001` | #18 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-07-API-002` | #19 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-07-API-003` | #20 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #18, #19, #20
- Orchestration/data notes: AC-12 #19 Enrollment+Progress transaction → #20 reload; exact #19 trigger/screen owner chưa chốt. #18 chỉ khi có trusted operation_id và contract thống nhất.
- BE/source status và gate: **#18/#19/#20 D; DD BLOCKED**; **BLOCK:** AC-12 không nêu ST-07 riêng/#18 detached; Operation ID/access/lifecycle và ST-06 handoff chưa rõ; #19 identity/eligibility/duplicate/transaction chưa chốt; #20 UserProfile không biểu diễn Course list; Study Web/API UNWIRED; post-#19 reload recovery và destination chưa rõ
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API boundary

| API | Request / quyền | Success | Errors | Runtime/effect boundary |
|---|---|---|---|---|
| #18 | `GET /api/v1/operations/{operation_id}`; Bearer JWT; row path `int64!`, AC/shared schema `uuid` | 200 `DESIGN_OPERATION_RETRIEVED`; `ApiEnvelope<Operation>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR` | Catalog/Draft only; no Study route/store/query/test. Owner vs owner/Admin, Operation fields/lifecycle/result, ID handoff and poll cadence unresolved; AC-12 node detached. |
| #19 | `POST /api/v1/courses/{course_id}/enrollments`; Bearer Student; path `course_id:int64!`; body `{course_id:int64!, user từ JWT:string!}` per catalog notation | 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Enrollment>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 409 `DESIGN_STATE_CONFLICT`, 500 `DESIGN_INTERNAL_ERROR` | Catalog/API DD only. AC describes Enrollment + Progress transaction; no runtime route/query/model/test. Identity field, eligibility, duplicates/transaction, status/lesson initialization and DDL/live schema remain unresolved. |
| #20 | `GET /api/v1/users/me/courses`; Bearer Student; optional query `status:string`, `page:int32`; no body | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<UserProfile>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` | Catalog/API DD only. AC-13 requires Enrollment+Course list and separate #21 progress; schema/filter/page/empty/identity mismatch; no runtime route/query/model/test. |

No client-supplied payment callback or URL parameter may be treated as trusted outcome. The present screen route carries only `courseId`, so #18 cannot be called unless a separate approved state handoff supplies a canonical Operation ID.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07.md)
