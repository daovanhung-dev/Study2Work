# ST-13 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-13-API-001` | #28 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #28
- Orchestration/data notes: GET #28 theo thiết kế; ST-13 row kỳ vọng POST #29 sau explicit Start, nhưng F05/ST-14 row/DD mâu thuẫn về screen owner và GET/POST order; ST-14 path còn yêu cầu `attemptId` trước entry nếu #29 được dời sang đó. Owner phải chốt một call-site/entry route, không gọi lặp.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #28/#29 Student route/module/test NOT_FOUND; PNG/HTML mismatch; eligibility, answer exposure, timing, attempt limit/resume/idempotency và CTA destinations open; #29 owner/order/entry route conflicts across ST-13/F05/ST-14; legacy BIGINT Quiz/Attempt differs from V1-PILOT UUID Assessment model; sample history/proctoring/scoring/certificate claims unsupported; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory, F05, API index, G-09](../../list_screen.md)
- [ST-13 plan](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_PLAN.md), [source PNG](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen.png), [source HTML](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/code.html)
- [API catalog](../../../../../docs/lists/list_api.md) — #28/#29; [AC-16 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [API #28 DD](../../../../study-server/docs/dd/28_quizzes_detail/00_Cover.md), [#28 open questions](../../../../study-server/docs/dd/28_quizzes_detail/OPEN_QUESTIONS.md)
- [API #29 DD](../../../../study-server/docs/dd/29_quizzes_attempts/00_Cover.md), [#29 open questions](../../../../study-server/docs/dd/29_quizzes_attempts/OPEN_QUESTIONS.md)
- [Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [current router](../../../../study-server/app/api/v1.py), [candidate DDL](../../../../../infra/postgres/study-server/DB.sql)
- [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [Study Web design guide](../../../../../.agents/web-study/design.md)
- [ST-14 source folder](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra), [ST-12 DD precedent](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md)
